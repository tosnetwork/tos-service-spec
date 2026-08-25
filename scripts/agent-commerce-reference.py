#!/usr/bin/env python3
"""Code-independent SemanticActionIdentityV1 conformance verifier.

This implementation intentionally uses only Python's standard library and the
released registry JSON. It shares no codec or hashing implementation with the
production Go package.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import copy
import hashlib
import json
import re
import struct
import sys
from pathlib import Path
from typing import Any


DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
TOKEN = re.compile(r"^[a-z][a-z0-9._-]{0,127}$")
MAX_FIELD_BYTES = 1 << 20


def _cbor_head(major: int, value: int) -> bytes:
    if value < 24:
        return bytes([(major << 5) | value])
    if value <= 0xFF:
        return bytes([(major << 5) | 24, value])
    if value <= 0xFFFF:
        return bytes([(major << 5) | 25]) + value.to_bytes(2, "big")
    if value <= 0xFFFFFFFF:
        return bytes([(major << 5) | 26]) + value.to_bytes(4, "big")
    if value <= 0xFFFFFFFFFFFFFFFF:
        return bytes([(major << 5) | 27]) + value.to_bytes(8, "big")
    raise ConformanceError("integer exceeds CBOR u64")


def canonical_cbor(value: Any, depth: int = 0) -> bytes:
    if depth > 16:
        raise ConformanceError("CBOR nesting exceeds V1 bound")
    if value is None:
        return b"\xf6"
    if isinstance(value, bool):
        return b"\xf5" if value else b"\xf4"
    if isinstance(value, int):
        return _cbor_head(0, value) if value >= 0 else _cbor_head(1, -1 - value)
    if isinstance(value, str):
        raw = value.encode("utf-8")
        if len(raw) > 256 << 10:
            raise ConformanceError("CBOR string exceeds V1 bound")
        return _cbor_head(3, len(raw)) + raw
    if isinstance(value, list):
        if len(value) > 4096:
            raise ConformanceError("CBOR array exceeds V1 bound")
        return _cbor_head(4, len(value)) + b"".join(canonical_cbor(item, depth + 1) for item in value)
    if isinstance(value, dict):
        if len(value) > 4096 or any(not isinstance(key, str) for key in value):
            raise ConformanceError("CBOR map exceeds V1 bound or has a non-text key")
        entries = [(canonical_cbor(key, depth + 1), canonical_cbor(item, depth + 1)) for key, item in value.items()]
        entries.sort(key=lambda item: (len(item[0]), item[0]))
        return _cbor_head(5, len(entries)) + b"".join(key + item for key, item in entries)
    raise ConformanceError(f"unsupported JSON model type {type(value)!r}")


def protocol_digest(domain: str, canonical: bytes) -> str:
    raw_domain = domain.encode("ascii")
    if not raw_domain or len(raw_domain) > 255:
        raise ConformanceError("invalid protocol digest domain")
    framed = b"TOS-PROTOCOL-CBOR\x00" + struct.pack(">H", len(raw_domain)) + raw_domain + canonical
    return "sha256:" + hashlib.sha256(framed).hexdigest()


# Independent, small RFC 8032 verifier. It intentionally shares no Go crypto
# implementation or generated code with the production SDK.
_Q = 2**255 - 19
_L = 2**252 + 27742317777372353535851937790883648493
_D = (-121665 * pow(121666, _Q - 2, _Q)) % _Q
_I = pow(2, (_Q - 1) // 4, _Q)


def _xrecover(y: int) -> int:
    xx = (y * y - 1) * pow(_D * y * y + 1, _Q - 2, _Q) % _Q
    x = pow(xx, (_Q + 3) // 8, _Q)
    if (x * x - xx) % _Q != 0:
        x = x * _I % _Q
    if x & 1:
        x = _Q - x
    return x


_BY = 4 * pow(5, _Q - 2, _Q) % _Q
_B = (_xrecover(_BY), _BY)


def _edwards(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    x1, y1 = left
    x2, y2 = right
    product = _D * x1 * x2 * y1 * y2 % _Q
    x3 = (x1 * y2 + x2 * y1) * pow(1 + product, _Q - 2, _Q) % _Q
    y3 = (y1 * y2 + x1 * x2) * pow(1 - product, _Q - 2, _Q) % _Q
    return x3, y3


def _scalarmult(point: tuple[int, int], scalar: int) -> tuple[int, int]:
    result = (0, 1)
    current = point
    while scalar:
        if scalar & 1:
            result = _edwards(result, current)
        current = _edwards(current, current)
        scalar >>= 1
    return result


def _decodepoint(encoded: bytes) -> tuple[int, int]:
    if len(encoded) != 32:
        raise ConformanceError("Ed25519 point length")
    value = int.from_bytes(encoded, "little")
    y = value & ((1 << 255) - 1)
    if y >= _Q:
        raise ConformanceError("non-canonical Ed25519 point")
    x = _xrecover(y)
    if (x & 1) != (value >> 255):
        x = _Q - x
    point = (x, y)
    if (-x * x + y * y - 1 - _D * x * x * y * y) % _Q != 0:
        raise ConformanceError("Ed25519 point is off curve")
    return point


def verify_ed25519(public_key: bytes, message: bytes, signature: bytes) -> bool:
    if len(public_key) != 32 or len(signature) != 64:
        return False
    try:
        point_a = _decodepoint(public_key)
        point_r = _decodepoint(signature[:32])
    except ConformanceError:
        return False
    scalar = int.from_bytes(signature[32:], "little")
    if scalar >= _L:
        return False
    challenge = int.from_bytes(hashlib.sha512(signature[:32] + public_key + message).digest(), "little") % _L
    # Cofactor multiplication also rejects small-order ambiguities.
    return _scalarmult(_scalarmult(_B, scalar), 8) == _scalarmult(_edwards(point_r, _scalarmult(point_a, challenge)), 8)


class ConformanceError(ValueError):
    """A deterministic V1 validation failure."""


def _lp16(value: bytes) -> bytes:
    if not value or len(value) > 0xFFFF:
        raise ConformanceError("invalid lp16 value")
    return struct.pack(">H", len(value)) + value


def _lp32(value: bytes) -> bytes:
    if not value or len(value) > MAX_FIELD_BYTES:
        raise ConformanceError("invalid lp32 value")
    return struct.pack(">I", len(value)) + value


def load_registry(path: Path) -> dict[str, dict[str, Any]]:
    document = json.loads(path.read_text(encoding="utf-8"))
    if document.get("schema") != "tos.semantic-action-registry.v1":
        raise ConformanceError("unknown registry schema")
    entries: dict[str, dict[str, Any]] = {}
    for entry in document.get("entries", []):
        kind = entry.get("action_kind")
        if not isinstance(kind, str) or not TOKEN.fullmatch(kind) or kind in entries:
            raise ConformanceError("invalid or duplicate action kind")
        if entry.get("registry_version") != 1 or entry.get("entry_version") != 1:
            raise ConformanceError("unsupported registry version")
        if entry.get("domain_tag") != f"tos.semantic-action.{kind}.v1":
            raise ConformanceError("invalid domain tag")
        names: set[str] = set()
        for field in entry.get("ordered_semantic_fields", []):
            name = field.get("field_name")
            field_type = field.get("field_type")
            if not isinstance(name, str) or not TOKEN.fullmatch(name) or name in names:
                raise ConformanceError("invalid or duplicate semantic field")
            if field_type not in {"id", "digest32", "u64", "kind", "state"}:
                raise ConformanceError("unknown semantic field type")
            names.add(name)
        if not names or entry.get("successor_policy") not in {"none", "terminal_successor", "authority_instance"}:
            raise ConformanceError("invalid registry entry")
        entries[kind] = entry
    if not entries:
        raise ConformanceError("empty registry")
    return entries


def _canonical_value(name: str, field_type: str, value: Any) -> bytes:
    if field_type == "u64":
        if isinstance(value, bool) or not isinstance(value, int) or value < 0 or value > 0xFFFFFFFFFFFFFFFF:
            raise ConformanceError(f"{name}: invalid u64")
        return struct.pack(">Q", value)
    if not isinstance(value, str) or not value or "\x00" in value:
        raise ConformanceError(f"{name}: invalid text")
    try:
        raw = value.encode("utf-8")
    except UnicodeEncodeError as error:
        raise ConformanceError(f"{name}: invalid UTF-8") from error
    if len(raw) > MAX_FIELD_BYTES:
        raise ConformanceError(f"{name}: overlong value")
    if field_type == "digest32":
        if not DIGEST.fullmatch(value):
            raise ConformanceError(f"{name}: non-canonical digest")
        return bytes.fromhex(value[7:])
    if field_type in {"kind", "state"} and not TOKEN.fullmatch(value):
        raise ConformanceError(f"{name}: non-canonical token")
    if field_type == "id":
        if len(raw) > 4096:
            raise ConformanceError(f"{name}: overlong identifier")
        if name == "amount_atomic" and not re.fullmatch(r"0|[1-9][0-9]{0,77}", value):
            raise ConformanceError("amount_atomic: non-canonical integer")
    return raw


def derive_action(registry: dict[str, dict[str, Any]], action_kind: str, values: dict[str, Any]) -> tuple[str, bytes]:
    entry = registry.get(action_kind)
    if entry is None:
        raise ConformanceError("unknown action kind")
    definitions = entry["ordered_semantic_fields"]
    expected = [field["field_name"] for field in definitions]
    if set(values) != set(expected) or len(values) != len(expected):
        raise ConformanceError("semantic field set mismatch")
    preimage = bytearray(b"TOS-SAI\x00")
    preimage += struct.pack(">HH", entry["registry_version"], entry["entry_version"])
    preimage += _lp16(entry["domain_tag"].encode("ascii"))
    preimage += _lp16(action_kind.encode("ascii"))
    preimage += struct.pack(">H", len(definitions))
    for field in definitions:
        name = field["field_name"]
        preimage += _lp16(name.encode("ascii"))
        preimage += _lp32(_canonical_value(name, field["field_type"], values[name]))
    digest = "sha256:" + hashlib.sha256(preimage).hexdigest()
    return digest, bytes(preimage)


def exact_request_digest(body: bytes) -> str:
    if not body or len(body) > 4 << 20:
        raise ConformanceError("invalid canonical request size")
    framed = b"tos.action-request.v1\x00" + struct.pack(">I", len(body)) + body
    return "sha256:" + hashlib.sha256(framed).hexdigest()


def verify_vectors(registry_path: Path, vector_path: Path) -> None:
    registry = load_registry(registry_path)
    document = json.loads(vector_path.read_text(encoding="utf-8"))
    if document.get("schema") != "tos.semantic-action-conformance.v1":
        raise ConformanceError("unknown vector schema")
    for vector in document.get("positive_vectors", []):
        identity, preimage = derive_action(registry, vector["action_kind"], vector["fields"])
        if identity != vector["stable_action_id"] or preimage.hex() != vector["preimage_hex"]:
            raise ConformanceError(f"positive vector {vector.get('name')} mismatch")
    for vector in document.get("negative_vectors", []):
        try:
            derive_action(registry, vector["action_kind"], vector["fields"])
        except ConformanceError:
            continue
        raise ConformanceError(f"negative vector {vector.get('name')} unexpectedly passed")


def _decode_prefixed_hex(value: str, prefix: str, length: int) -> bytes:
    if not isinstance(value, str) or not value.startswith(prefix):
        raise ConformanceError("invalid prefixed hexadecimal value")
    try:
        raw = bytes.fromhex(value[len(prefix):])
    except ValueError as error:
        raise ConformanceError("invalid hexadecimal value") from error
    if len(raw) != length or value != prefix + raw.hex():
        raise ConformanceError("non-canonical hexadecimal value")
    return raw


def _decode_signature(value: str) -> bytes:
    if not isinstance(value, str) or not value.startswith("ed25519:"):
        raise ConformanceError("invalid signature prefix")
    encoded = value[len("ed25519:"):]
    try:
        raw = base64.urlsafe_b64decode(encoded + "=" * ((4 - len(encoded) % 4) % 4))
    except (ValueError, binascii.Error) as error:
        raise ConformanceError("invalid signature encoding") from error
    if len(raw) != 64 or base64.urlsafe_b64encode(raw).decode().rstrip("=") != encoded:
        raise ConformanceError("non-canonical signature encoding")
    return raw


def verify_core_vectors(path: Path) -> None:
    document = json.loads(path.read_text(encoding="utf-8"))
    if document.get("schema") != "tos.agent-commerce-core-conformance.v1":
        raise ConformanceError("unknown core vector schema")
    objects: dict[str, dict[str, Any]] = {}
    for item in document.get("objects", []):
        name = item.get("name")
        if not isinstance(name, str) or not name or name in objects:
            raise ConformanceError("duplicate or invalid core object name")
        encoded = canonical_cbor(item.get("json_model"))
        if base64.b64encode(encoded).decode() != item.get("canonical_cbor_base64"):
            raise ConformanceError(f"{name}: canonical CBOR mismatch")
        if protocol_digest(item.get("digest_domain"), encoded) != item.get("digest"):
            raise ConformanceError(f"{name}: protocol digest mismatch")
        objects[name] = item
    if len(objects) < 8:
        raise ConformanceError("core vector set is incomplete")
    for item in document.get("signatures", []):
        source = objects.get(item.get("object_name"))
        if source is None:
            raise ConformanceError("signature references an unknown object")
        model = copy.deepcopy(source["json_model"])
        if item.get("name") == "authorized_action":
            model["authorization_proof"] = ""
        canonical = canonical_cbor(model)
        domain = item.get("message_domain")
        formula = item.get("message_formula")
        if formula not in {"length-framed-sha256", "framed-sha256", "domain-text-digest-sha256"} or not isinstance(domain, str):
            raise ConformanceError("unknown signature message formula")
        if formula == "domain-text-digest-sha256":
            body_digest = protocol_digest("tos.external-payment-attestation-body.v1", canonical)
            message = hashlib.sha256(domain.encode("ascii") + b"\x00" + body_digest.encode("ascii")).digest()
        else:
            framed = domain.encode("ascii") + b"\x00" + struct.pack(">I", len(canonical)) + canonical
            message = hashlib.sha256(framed).digest()
        if message.hex() != item.get("expected_message_hex"):
            raise ConformanceError(f"{item.get('name')}: signature message mismatch")
        public = _decode_prefixed_hex(item.get("public_key"), "ed25519:", 32)
        signature = _decode_signature(item.get("signature"))
        if not verify_ed25519(public, message, signature):
            raise ConformanceError(f"{item.get('name')}: Ed25519 signature mismatch")
    expected_mutations = {"mutated-intent-summary", "mutated-signature", "noncanonical-cbor"}
    if set(document.get("negative_mutations", [])) != expected_mutations:
        raise ConformanceError("core negative mutation registry mismatch")
    intent = objects["intent_body"]
    mutated = copy.deepcopy(intent["json_model"])
    mutated["payload"]["discovery_card"]["summary"] += "!"
    if protocol_digest(intent["digest_domain"], canonical_cbor(mutated)) == intent["digest"]:
        raise ConformanceError("mutated Intent preserved its digest")
    first_signature = document["signatures"][0]
    public = _decode_prefixed_hex(first_signature["public_key"], "ed25519:", 32)
    signature = bytearray(_decode_signature(first_signature["signature"]))
    signature[0] ^= 1
    message = bytes.fromhex(first_signature["expected_message_hex"])
    if verify_ed25519(public, message, bytes(signature)):
        raise ConformanceError("mutated Ed25519 signature was accepted")
    # A longer integer encoding is semantically equal but forbidden by RFC
    # 8949 Core Deterministic Encoding. The reference encoder must choose 0x01.
    if canonical_cbor(1) != b"\x01" or b"\x18\x01" == canonical_cbor(1):
        raise ConformanceError("non-canonical CBOR integer was accepted")


def main() -> int:
    parser = argparse.ArgumentParser()
    root = Path(__file__).resolve().parents[1]
    parser.add_argument("--registry", type=Path, default=root / "schemas/semantic-action-identity-v1.json")
    parser.add_argument("--vectors", type=Path, default=root / "test-vectors/agent-commerce-semantic-action-v1.json")
    parser.add_argument("--core-vectors", type=Path, default=root / "test-vectors/agent-commerce-core-v1.json")
    args = parser.parse_args()
    try:
        verify_vectors(args.registry, args.vectors)
        verify_core_vectors(args.core_vectors)
    except (ConformanceError, OSError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("PASS: independent Agent Commerce V1 action, CBOR, digest, and Ed25519 vectors")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
