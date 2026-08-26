#!/usr/bin/env python3
"""Independent Agent Relay Service V1 vector generator and verifier.

Only the Python standard library is used. The implementation shares neither
the Go codec nor the Go Ed25519 implementation used by pkg/agentrelay.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import copy
import hashlib
import ipaddress
import json
import re
import struct
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
CELL_DIGEST = re.compile(r"^tvm-cell-sha256:[0-9a-f]{64}$")
TOKEN = re.compile(r"^[a-z][a-z0-9._-]{0,127}$")
ATOMIC = re.compile(r"^(0|[1-9][0-9]{0,77})$")
MAX_SIGNED_BYTES = 64 << 10
MAX_ACTION_BYTES = 192 << 10
MAX_SPONSORSHIP_PROOF_BUNDLE_BYTES = 128 << 10
MAX_ABSENCE_PROOF_BUNDLE_BYTES = 128 << 10
MAX_CANONICAL_BYTES = 1 << 20
MAX_REQUEST_LIFETIME = 15 * 60
MAX_PROFILE_LIFETIME = 90 * 24 * 60 * 60

MODES = {"relay_exact", "sponsor_only", "sponsor_and_relay"}
ASSURANCE_LEVELS = {
    "trusted-local",
    "authorized-single-provider",
    "autonomous-decentralized",
}
BASE_READINESS_CAPABILITIES = {
    "complete_network_domain_pin",
    "exact_transaction_inspection",
    "underlying_action_authority",
    "single_primary_submit",
    "durable_ambiguity_journal",
    "truthful_resolution",
}
SPONSORSHIP_READINESS_CAPABILITIES = {
    "sponsorship_custody",
    "sponsorship_exposure_ledger",
    "exact_sponsorship_transaction_journal",
    "terminal_sponsorship_finality_evidence",
}
ASSURANCE_READINESS_CAPABILITIES = {
    "trusted-local": {"trusted_provider_binding"},
    "authorized-single-provider": {
        "signed_profile_quote_agreement",
        "authenticated_provider_transport",
        "provider_resolve",
    },
    "autonomous-decentralized": {
        "signed_profile_quote_agreement",
        "authenticated_provider_transport",
        "provider_resolve",
        "pinned_provider_provenance",
        "portable_evidence_verifier",
        "rollback_resistant_provider_journal",
        "rollback_resistant_side_effect_admission",
        "rollback_resistant_route_journal",
    },
}
OUTCOMES = {
    "finalized_success",
    "finalized_expired",
    "finalized_absent",
    "finalized_invalidated",
    "corroborated_expired",
    "corroborated_absent",
    "corroborated_invalidated",
    "finalized_sponsorship_only",
    "corroborated_sponsorship_only",
    "finalized_relay_only",
    "corroborated_relay_only",
    "corroborated_success",
}
STATES = {"prepared", "submitted", "accepted", "rejected", "conflict", "terminal"}
ABSENCE_KINDS = {"sponsorship_action", "client_transaction"}
ABSENCE_CONCLUSIONS = {"absent", "expired_without_inclusion", "invalidated_without_inclusion"}
AGREEMENT_BINDING_CONTENT_TYPE = "application/vnd.tos.agent-relay-agreement-binding.v1+cbor"
AGENT_SIGNATURE_PROFILE_URI = "tos.agreement.evidence.agent-signature.v1"
AGENT_SIGNATURE_PROFILE_DIGEST = "sha256:4a8eaf43746a0aeb781a75469f0b508f90efb73f4dc25e6707b61cd0d5c8268d"
AGREEMENT_ACCEPTANCE_CONTENT_TYPE = "application/vnd.tos.agreement-acceptance.v1+cbor"
RPC_CORROBORATION_PROFILE_URI = "agreement-payment-rpc-corroboration.v1"
TOS_RPC_ABSENCE_PROFILE_URI = "tos.relay-absence.tosctl-rpc-snapshot.v1"
CLIENT_CORROBORATED_TERMINAL_PROFILE_URI = \
    "tos.sponsorship.client-corroborated-terminal.v1"
PROVIDER_CORROBORATED_RELAY_PROFILE_URI = \
    "tos.relay.provider-corroborated-terminal.v1"
SPONSORSHIP_RELEASE_CLASSES = {"validator_finality", "observed_unproven"}
SPONSORSHIP_TERMINAL_CLASSES = {"validator_finality", "client_corroborated"}
RELAY_TERMINAL_CLASSES = {"validator_finality", "provider_corroborated"}
SPONSORSHIP_PAYMENT_COMMITMENT_TAG = 0x53504E31
PUBLISHED_SPONSORSHIP_PAYMENT_COMMITMENT_CELL_HASH = \
    "tvm-cell-sha256:00fa7b6beeb7e8ec086d2eff5fd9bff0136c4cdf8d3428c09db2b32d0a0d87a3"

EXPECTED_GO = {
    "network": "sha256:2bb4cdc2e2e1001bc54e519087598582717217b82cbfd005c0acfe03269f6a69",
    "underlying_payment_request": "sha256:bebcfeeaefba55c1a468eab68c01a91904ea62145716cd66dc6ce81473821004",
    "underlying_payment_stable_id": "sha256:f951d5db1f4a955b156164b9985a9be3e965e2959ca6dce6db2436147662e0ae",
    "underlying_payment_exact_request": "sha256:f218789c7750655634f28dc6607798d0004537aa63528e63b921fb9ea96c1039",
    "sponsorship_payment_request": "sha256:9d0b3d30969ac9e88d0722ba10e323b6bfe49849d49cf42bf5c831181c40d495",
    "sponsorship_payment_stable_id": "sha256:76c2ed4eebe65eb4469810d34dbd8cd7bce83209a0a6b3ae56a92e2fcebc196e",
    "sponsorship_payment_exact_request": "sha256:32b404a565b32f65aaf94cbbdc2b54bfae4b559fe185f034fad56839c40c31fe",
    "service_profile": "sha256:96bc9e18795563afbf31cf3b76814315991268e52a0070682236239f9fed4af2",
    "quote_request_body": "sha256:f4cd388f94c3ef2b7acd1e155468e49f42844712eac4d9979984c6a6a06c011b",
    "provider_quote_body": "sha256:4bca62f015d2efe25059d975a2d1564ceebc86fb9d8389c66b735656184fd02d",
    "request_public_key": "ed25519:48075a597e721a156e2e0799de5cc0c5324dc6e7eaf1cdd46250868ec53215dd",
    "request_signature": "ed25519:L-4GloB1NZ3m3cUlsT-GUYia5-6NDyKGSVgBgQ7PDyT6N9uKuvru4h7-qw-yUNSkL02NiEsJztdvBxhOBvj7DQ",
    "quote_public_key": "ed25519:5e212c0980e4b39fc09721134aa02109374edfd260c0d3d03cb501c8d65457a9",
    "quote_signature": "ed25519:RowIcF2oxsuY9o-ealz3aC5YvI4Hrn-sAe0vh_NfFiFtUv1cBUo9NOpuZfPtD4jGhIMPs6cTDTsEJFH_Ic4CCA",
}


class ConformanceError(ValueError):
    """Deterministic V1 conformance failure."""


def _head(major: int, value: int) -> bytes:
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
    raise ConformanceError("CBOR integer exceeds u64")


def canonical_cbor(value: Any, depth: int = 0) -> bytes:
    if depth > 16:
        raise ConformanceError("CBOR nesting exceeds 16")
    if value is None:
        return b"\xf6"
    if isinstance(value, bool):
        return b"\xf5" if value else b"\xf4"
    if isinstance(value, int):
        return _head(0, value) if value >= 0 else _head(1, -1 - value)
    if isinstance(value, str):
        raw = value.encode("utf-8")
        if len(raw) > 8 << 20:
            raise ConformanceError("CBOR string is overlong")
        return _head(3, len(raw)) + raw
    if isinstance(value, list):
        if len(value) > 4096:
            raise ConformanceError("CBOR array is overlong")
        return _head(4, len(value)) + b"".join(canonical_cbor(item, depth + 1) for item in value)
    if isinstance(value, dict):
        if len(value) > 4096 or any(not isinstance(key, str) for key in value):
            raise ConformanceError("CBOR map is invalid")
        pairs = [(canonical_cbor(key), canonical_cbor(item, depth + 1)) for key, item in value.items()]
        pairs.sort(key=lambda pair: (len(pair[0]), pair[0]))
        return _head(5, len(pairs)) + b"".join(key + item for key, item in pairs)
    raise ConformanceError(f"unsupported CBOR model type {type(value)!r}")


def bounded_canonical_cbor(value: Any) -> bytes:
    encoded = canonical_cbor(value)
    if len(encoded) > MAX_CANONICAL_BYTES:
        raise ConformanceError("canonical object exceeds 1 MiB")
    return encoded


def decode_canonical_cbor(encoded: bytes, maximum: int) -> Any:
    if not encoded or len(encoded) > maximum:
        raise ConformanceError("canonical CBOR byte length is invalid")

    def head(offset: int) -> tuple[int, int, int]:
        if offset >= len(encoded):
            raise ConformanceError("canonical CBOR is truncated")
        initial = encoded[offset]
        major, additional = initial >> 5, initial & 31
        offset += 1
        if additional < 24:
            return major, additional, offset
        widths = {24: 1, 25: 2, 26: 4, 27: 8}
        width = widths.get(additional)
        if width is None or offset + width > len(encoded):
            raise ConformanceError("canonical CBOR head is invalid")
        value = int.from_bytes(encoded[offset:offset + width], "big")
        if (width == 1 and value < 24 or width == 2 and value <= 0xFF or
                width == 4 and value <= 0xFFFF or
                width == 8 and value <= 0xFFFFFFFF):
            raise ConformanceError("canonical CBOR integer is overlong")
        return major, value, offset + width

    def item(offset: int, depth: int) -> tuple[Any, int]:
        if depth > 16:
            raise ConformanceError("canonical CBOR nesting exceeds 16")
        major, value, offset = head(offset)
        if major == 0:
            return value, offset
        if major == 1:
            return -1 - value, offset
        if major == 3:
            if offset + value > len(encoded):
                raise ConformanceError("canonical CBOR text is truncated")
            try:
                text_value = encoded[offset:offset + value].decode("utf-8")
            except UnicodeDecodeError as error:
                raise ConformanceError("canonical CBOR text is invalid UTF-8") from error
            return text_value, offset + value
        if major == 4:
            values = []
            for _ in range(value):
                decoded, offset = item(offset, depth + 1)
                values.append(decoded)
            return values, offset
        if major == 5:
            values: dict[str, Any] = {}
            for _ in range(value):
                key, offset = item(offset, depth + 1)
                if not isinstance(key, str) or key in values:
                    raise ConformanceError("canonical CBOR map key is invalid")
                decoded, offset = item(offset, depth + 1)
                values[key] = decoded
            return values, offset
        if major == 7 and value in {20, 21, 22}:
            return ({20: False, 21: True, 22: None}[value], offset)
        raise ConformanceError("canonical CBOR type is unsupported")

    value, offset = item(0, 0)
    if offset != len(encoded) or canonical_cbor(value) != encoded:
        raise ConformanceError("CBOR bytes are not one Core Deterministic item")
    return value


def protocol_digest(domain: str, value: Any) -> str:
    encoded = bounded_canonical_cbor(value)
    return protocol_digest_canonical(domain, encoded)


def protocol_digest_canonical(domain: str, encoded: bytes) -> str:
    raw_domain = domain.encode("ascii")
    if not raw_domain or len(raw_domain) > 0xFFFF or not encoded or len(encoded) > MAX_CANONICAL_BYTES:
        raise ConformanceError("digest domain is invalid")
    framed = b"TOS-PROTOCOL-CBOR\x00" + struct.pack(">H", len(raw_domain)) + raw_domain + encoded
    return "sha256:" + hashlib.sha256(framed).hexdigest()


def exact_request_digest(payload: bytes) -> str:
    if not payload or len(payload) > MAX_ACTION_BYTES:
        raise ConformanceError("underlying request byte length is invalid")
    return "sha256:" + hashlib.sha256(b"tos.action-request.v1\x00" + struct.pack(">I", len(payload)) + payload).hexdigest()


def raw_digest(payload: bytes) -> str:
    if not payload or len(payload) > MAX_SIGNED_BYTES:
        raise ConformanceError("signed transaction byte length is invalid")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _digest_payload(value: str) -> bytes:
    if not digest(value):
        raise ConformanceError("SPN1 input is not a SHA-256 digest")
    return bytes.fromhex(value.removeprefix("sha256:"))


def sponsorship_payment_commitment_cell_representation(
        agreement_payment_request_digest: str, stable_action_id: str) -> bytes:
    """Return the exact zero-reference ordinary-cell representation for SPN1.

    The cell has 544 byte-aligned bits: uint32(0x53504e31), the raw 32-byte
    PaymentRequest digest, and the raw 32-byte stable action ID. An ordinary
    level-zero cell with no references has descriptor one 0x00. For 68 whole
    data bytes descriptor two is floor(544/8)+ceil(544/8)=136 (0x88).
    """
    payload = (SPONSORSHIP_PAYMENT_COMMITMENT_TAG.to_bytes(4, "big") +
               _digest_payload(agreement_payment_request_digest) +
               _digest_payload(stable_action_id))
    if len(payload) != 68:
        raise ConformanceError("SPN1 payload length drifted")
    return bytes((0x00, 0x88)) + payload


def sponsorship_payment_commitment_cell_hash(
        agreement_payment_request_digest: str, stable_action_id: str) -> str:
    representation = sponsorship_payment_commitment_cell_representation(
        agreement_payment_request_digest, stable_action_id)
    return "tvm-cell-sha256:" + hashlib.sha256(representation).hexdigest()


def tosctl_framed_json_digest(domain_with_nul: bytes, value: Any) -> tuple[bytes, str]:
    if not domain_with_nul.endswith(b"\x00"):
        raise ConformanceError("tosctl JSON digest domain lacks final NUL")
    encoded = json.dumps(value, ensure_ascii=False, separators=(",", ":"),
                         sort_keys=True).encode("utf-8")
    digest_value = hashlib.sha256(
        domain_with_nul + struct.pack(">Q", len(encoded)) + encoded).hexdigest()
    return encoded, "sha256:" + digest_value


def signature_message(domain_with_nul: bytes, body: Any) -> bytes:
    if not domain_with_nul.endswith(b"\x00"):
        raise ConformanceError("signature domain lacks final NUL")
    encoded = bounded_canonical_cbor(body)
    return hashlib.sha256(domain_with_nul + struct.pack(">I", len(encoded)) + encoded).digest()


# Small RFC 8032 implementation, independent from production Go crypto.
_Q = 2**255 - 19
_L = 2**252 + 27742317777372353535851937790883648493
_D = (-121665 * pow(121666, _Q - 2, _Q)) % _Q
_I = pow(2, (_Q - 1) // 4, _Q)


def _xrecover(y: int) -> int:
    xx = (y * y - 1) * pow(_D * y * y + 1, _Q - 2, _Q) % _Q
    x = pow(xx, (_Q + 3) // 8, _Q)
    if (x * x - xx) % _Q:
        x = x * _I % _Q
    return _Q - x if x & 1 else x


_BY = 4 * pow(5, _Q - 2, _Q) % _Q
_B = (_xrecover(_BY), _BY)


def _edwards(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    x1, y1 = left
    x2, y2 = right
    product = _D * x1 * x2 * y1 * y2 % _Q
    return ((x1 * y2 + x2 * y1) * pow(1 + product, _Q - 2, _Q) % _Q,
            (y1 * y2 + x1 * x2) * pow(1 - product, _Q - 2, _Q) % _Q)


def _scalarmult(point: tuple[int, int], scalar: int) -> tuple[int, int]:
    result = (0, 1)
    current = point
    while scalar:
        if scalar & 1:
            result = _edwards(result, current)
        current = _edwards(current, current)
        scalar >>= 1
    return result


def _encodepoint(point: tuple[int, int]) -> bytes:
    x, y = point
    return (y | ((x & 1) << 255)).to_bytes(32, "little")


def _decodepoint(encoded: bytes) -> tuple[int, int]:
    if len(encoded) != 32:
        raise ConformanceError("Ed25519 point length is invalid")
    value = int.from_bytes(encoded, "little")
    y = value & ((1 << 255) - 1)
    if y >= _Q:
        raise ConformanceError("Ed25519 point is noncanonical")
    x = _xrecover(y)
    if (x & 1) != (value >> 255):
        x = _Q - x
    point = (x, y)
    if (-x * x + y * y - 1 - _D * x * x * y * y) % _Q:
        raise ConformanceError("Ed25519 point is off curve")
    return point


def _expand_seed(seed: bytes) -> tuple[int, bytes]:
    if len(seed) != 32:
        raise ConformanceError("Ed25519 seed length is invalid")
    digest = hashlib.sha512(seed).digest()
    scalar = int.from_bytes(bytes([digest[0] & 248]) + digest[1:31] + bytes([(digest[31] & 63) | 64]), "little")
    return scalar, digest[32:]


def public_from_seed(seed: bytes) -> bytes:
    scalar, _ = _expand_seed(seed)
    return _encodepoint(_scalarmult(_B, scalar))


def sign_ed25519(seed: bytes, message: bytes) -> bytes:
    scalar, prefix = _expand_seed(seed)
    public = public_from_seed(seed)
    nonce = int.from_bytes(hashlib.sha512(prefix + message).digest(), "little") % _L
    encoded_r = _encodepoint(_scalarmult(_B, nonce))
    challenge = int.from_bytes(hashlib.sha512(encoded_r + public + message).digest(), "little") % _L
    return encoded_r + ((nonce + challenge * scalar) % _L).to_bytes(32, "little")


def verify_ed25519(public: bytes, message: bytes, signature: bytes) -> bool:
    if len(public) != 32 or len(signature) != 64:
        return False
    try:
        point_a = _decodepoint(public)
        point_r = _decodepoint(signature[:32])
    except ConformanceError:
        return False
    scalar = int.from_bytes(signature[32:], "little")
    if scalar >= _L:
        return False
    challenge = int.from_bytes(hashlib.sha512(signature[:32] + public + message).digest(), "little") % _L
    return _scalarmult(_scalarmult(_B, scalar), 8) == _scalarmult(_edwards(point_r, _scalarmult(point_a, challenge)), 8)


def encode_public(seed: bytes) -> str:
    return "ed25519:" + public_from_seed(seed).hex()


def encode_signature(seed: bytes, message: bytes) -> str:
    return "ed25519:" + base64.urlsafe_b64encode(sign_ed25519(seed, message)).decode().rstrip("=")


def decode_public(value: str) -> bytes:
    if not isinstance(value, str) or not re.fullmatch(r"ed25519:[0-9a-f]{64}", value):
        raise ConformanceError("public key is invalid")
    return bytes.fromhex(value[8:])


def decode_signature(value: str) -> bytes:
    if not isinstance(value, str) or not value.startswith("ed25519:"):
        raise ConformanceError("signature is invalid")
    encoded = value[8:]
    try:
        raw = base64.urlsafe_b64decode(encoded + "=" * ((4 - len(encoded) % 4) % 4))
    except (ValueError, binascii.Error) as error:
        raise ConformanceError("signature is invalid") from error
    if len(raw) != 64 or base64.urlsafe_b64encode(raw).decode().rstrip("=") != encoded:
        raise ConformanceError("signature is noncanonical")
    return raw


def require_keys(value: Any, required: set[str], optional: set[str] = set()) -> None:
    if not isinstance(value, dict) or set(value) != required | (set(value) & optional):
        raise ConformanceError("object field set is invalid")


def identifier(value: Any, maximum: int = 256) -> bool:
    return isinstance(value, str) and 0 < len(value.encode()) <= maximum and value == value.strip() and not any(c in value for c in "\x00\r\n")


def digest(value: Any) -> bool:
    return isinstance(value, str) and DIGEST.fullmatch(value) is not None


def atomic(value: Any, positive: bool = False) -> bool:
    return isinstance(value, str) and ATOMIC.fullmatch(value) is not None and (not positive or value != "0")


def integer(value: Any, minimum: int, maximum: int) -> bool:
    """Return true only for a protocol integer in the exact closed range.

    Python's ``bool`` subclasses ``int``.  Using ``isinstance(value, int)`` in
    an independent verifier would therefore accept CBOR booleans for Go
    uint/int fields and let implementations disagree about a signed object.
    """
    return type(value) is int and minimum <= value <= maximum


def i32(value: Any) -> bool:
    return integer(value, -(1 << 31), (1 << 31) - 1)


def u16(value: Any) -> bool:
    return integer(value, 0, (1 << 16) - 1)


def u32(value: Any) -> bool:
    return integer(value, 0, (1 << 32) - 1)


def u64(value: Any) -> bool:
    return integer(value, 0, (1 << 64) - 1)


def positive_u64(value: Any) -> bool:
    return integer(value, 1, (1 << 64) - 1)


def decode_base64(value: Any, maximum: int) -> bytes:
    if not isinstance(value, str):
        raise ConformanceError("byte string is invalid")
    try:
        raw = base64.b64decode(value, validate=True)
    except (ValueError, binascii.Error) as error:
        raise ConformanceError("byte string is noncanonical") from error
    if not raw or len(raw) > maximum or base64.b64encode(raw).decode() != value:
        raise ConformanceError("byte string length or spelling is invalid")
    return raw


def validate_endpoint(value: Any) -> None:
    if not isinstance(value, str) or len(value) > 2048:
        raise ConformanceError("endpoint is invalid")
    parsed = urlsplit(value)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ConformanceError("endpoint is not a credential-free HTTPS path")
    if parsed.path == "":
        raise ConformanceError("endpoint path is empty")
    host = parsed.hostname.lower()
    if host == "localhost" or host.endswith(".localhost"):
        raise ConformanceError("endpoint targets loopback")
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        return
    if not address.is_global:
        raise ConformanceError("endpoint targets a non-public address")


def validate_network(value: Any) -> None:
    require_keys(value, {"network_id", "global_id", "zero_state_root_hash", "zero_state_file_hash", "workchain_id"})
    if not identifier(value["network_id"], 128) or not i32(value["global_id"]):
        raise ConformanceError("network domain identity is invalid")
    if not digest(value["zero_state_root_hash"]) or not digest(value["zero_state_file_hash"]):
        raise ConformanceError("network zero-state hash is invalid")
    if not i32(value["workchain_id"]):
        raise ConformanceError("network workchain is invalid")


def validate_network_order_fixture(values: Any) -> None:
    if not isinstance(values, list) or len(values) < 2:
        raise ConformanceError("network ordering fixture is incomplete")
    for value in values:
        validate_network(value)
    keys = [(item["network_id"], item["global_id"], item["zero_state_root_hash"],
             item["zero_state_file_hash"], item["workchain_id"]) for item in values]
    if keys != sorted(set(keys)):
        raise ConformanceError("network ordering fixture is not numeric tuple order")


def validate_asset(value: Any) -> None:
    require_keys(value, {"asset_namespace", "asset_identifier", "unit"})
    if not identifier(value["asset_namespace"], 128) or not identifier(value["asset_identifier"], 256) or not identifier(value["unit"], 128):
        raise ConformanceError("asset identity is invalid")


def validate_amount(value: Any, positive: bool = False) -> None:
    require_keys(value, {"asset", "amount_atomic"})
    validate_asset(value["asset"])
    if not atomic(value["amount_atomic"], positive):
        raise ConformanceError("asset amount is invalid")


def asset_key(value: dict[str, Any]) -> tuple[str, str, str]:
    return value["asset_namespace"], value["asset_identifier"], value["unit"]


def validate_finality(value: Any) -> None:
    required = {"profile_uri", "profile_digest", "terminal_evidence_class",
                "minimum_confirmation_depth", "minimum_observers",
                "minimum_operator_domains", "reorg_window_seconds", "maximum_resolution_seconds"}
    require_keys(value, required)
    if (not identifier(value["profile_uri"]) or not digest(value["profile_digest"]) or
            value["terminal_evidence_class"] not in
            (RELAY_TERMINAL_CLASSES | SPONSORSHIP_TERMINAL_CLASSES)):
        raise ConformanceError("finality profile identity is invalid")
    if (not u32(value["minimum_confirmation_depth"]) or
            not u16(value["minimum_observers"]) or
            not u16(value["minimum_operator_domains"]) or
            not u32(value["reorg_window_seconds"]) or
            not u32(value["maximum_resolution_seconds"])):
        raise ConformanceError("finality profile integer is invalid")
    if value["minimum_confirmation_depth"] == 0 or value["minimum_observers"] == 0 or value["minimum_operator_domains"] == 0:
        raise ConformanceError("finality minimum is zero")
    if value["minimum_operator_domains"] > value["minimum_observers"]:
        raise ConformanceError("finality operator diversity exceeds observers")
    if value["maximum_resolution_seconds"] == 0 or value["maximum_resolution_seconds"] > 86400:
        raise ConformanceError("finality resolution bound is invalid")
    if value["reorg_window_seconds"] > value["maximum_resolution_seconds"]:
        raise ConformanceError("finality reorg window is invalid")
    terminal_class = value["terminal_evidence_class"]
    if (terminal_class == "provider_corroborated" and
            value["profile_uri"] != PROVIDER_CORROBORATED_RELAY_PROFILE_URI):
        raise ConformanceError(
            "provider-corroborated relay profile URI is not the V1 profile")
    if (terminal_class == "client_corroborated" and
            value["profile_uri"] != CLIENT_CORROBORATED_TERMINAL_PROFILE_URI):
        raise ConformanceError(
            "client-corroborated sponsorship profile URI is not the V1 profile")


def validate_admission_limits(value: Any) -> None:
    names = {"maximum_quote_reservations", "maximum_active_executions", "maximum_active_per_requester",
             "maximum_quote_requests_per_window", "maximum_quote_requests_per_requester_window",
             "quote_request_window_seconds"}
    require_keys(value, names)
    if any(not u32(value[name]) or value[name] < 1 for name in names):
        raise ConformanceError("admission limit is not a positive integer")
    if any(value[name] > 1_000_000 for name in names - {"quote_request_window_seconds"}):
        raise ConformanceError("admission count exceeds the V1 bound")
    if value["quote_request_window_seconds"] > 86_400:
        raise ConformanceError("admission rate window exceeds the V1 bound")
    if value["maximum_active_per_requester"] > value["maximum_active_executions"]:
        raise ConformanceError("per-requester admission exceeds the active execution limit")
    if value["maximum_quote_requests_per_requester_window"] > value["maximum_quote_requests_per_window"]:
        raise ConformanceError("per-requester quote rate exceeds the provider-global quote rate")


def validate_profile(profile: Any) -> None:
    required = {"schema_version", "profile_id", "revision", "provider_agent_id", "network_domains", "supported_modes",
                "supported_assurance_levels",
                "transaction_profiles", "finality_profiles", "fee_assets", "exposure_limits", "maximum_request_bytes",
                "admission_limits", "endpoints", "policy_revision", "created_at_unix", "expires_at_unix"}
    require_keys(profile, required)
    if (not u16(profile["schema_version"]) or profile["schema_version"] != 1 or
            not identifier(profile["profile_id"]) or not positive_u64(profile["revision"]) or
            not identifier(profile["provider_agent_id"])):
        raise ConformanceError("service profile envelope is invalid")
    if (not u32(profile["maximum_request_bytes"]) or
            not 0 < profile["maximum_request_bytes"] <= MAX_SIGNED_BYTES or
            not positive_u64(profile["policy_revision"])):
        raise ConformanceError("service profile limit is invalid")
    if (not positive_u64(profile["created_at_unix"]) or not positive_u64(profile["expires_at_unix"]) or
            not profile["created_at_unix"] < profile["expires_at_unix"] or
            profile["expires_at_unix"] - profile["created_at_unix"] > MAX_PROFILE_LIFETIME):
        raise ConformanceError("service profile lifetime is invalid")
    networks = profile["network_domains"]
    if not isinstance(networks, list) or not 0 < len(networks) <= 64:
        raise ConformanceError("service network set is invalid")
    for item in networks:
        validate_network(item)
    network_keys = [(item["network_id"], item["global_id"], item["zero_state_root_hash"], item["zero_state_file_hash"], item["workchain_id"]) for item in networks]
    if network_keys != sorted(set(network_keys)):
        raise ConformanceError("service network set is not canonical")
    modes = profile["supported_modes"]
    if not isinstance(modes, list) or not 0 < len(modes) <= 3 or any(item not in MODES for item in modes) or modes != sorted(set(modes)):
        raise ConformanceError("service mode set is invalid")
    assurance_levels = profile["supported_assurance_levels"]
    if (not isinstance(assurance_levels, list) or
            not 0 < len(assurance_levels) <= len(ASSURANCE_LEVELS) or
            any(item not in ASSURANCE_LEVELS for item in assurance_levels) or
            assurance_levels != sorted(set(assurance_levels))):
        raise ConformanceError("service assurance-level set is invalid")
    transactions = profile["transaction_profiles"]
    if not isinstance(transactions, list) or not 0 < len(transactions) <= 32:
        raise ConformanceError("transaction profile set is invalid")
    transaction_keys = []
    for item in transactions:
        require_keys(item, {"profile_uri", "profile_digest", "maximum_signed_bytes", "inspectable_source_sequence", "inspectable_transaction_expiry"})
        if (not identifier(item["profile_uri"]) or not digest(item["profile_digest"]) or
                not u32(item["maximum_signed_bytes"]) or
                not 0 < item["maximum_signed_bytes"] <= profile["maximum_request_bytes"]):
            raise ConformanceError("transaction profile is invalid")
        if item["inspectable_source_sequence"] is not True or item["inspectable_transaction_expiry"] is not True:
            raise ConformanceError("transaction profile is not inspectable")
        transaction_keys.append((item["profile_uri"], item["profile_digest"]))
    if transaction_keys != sorted(set(transaction_keys)):
        raise ConformanceError("transaction profile set is not canonical")
    finalities = profile["finality_profiles"]
    if not isinstance(finalities, list) or not 0 < len(finalities) <= 16:
        raise ConformanceError("finality profile set is invalid")
    for item in finalities:
        validate_finality(item)
    finality_keys = [(item["profile_uri"], item["profile_digest"]) for item in finalities]
    if finality_keys != sorted(set(finality_keys)):
        raise ConformanceError("finality profile set is not canonical")
    assets = profile["fee_assets"]
    if not isinstance(assets, list) or not 0 < len(assets) <= 16:
        raise ConformanceError("fee asset set is invalid")
    for item in assets:
        validate_asset(item)
    if [asset_key(item) for item in assets] != sorted(set(asset_key(item) for item in assets)):
        raise ConformanceError("fee asset set is not canonical")
    exposures = profile["exposure_limits"]
    if not isinstance(exposures, list) or not 0 < len(exposures) <= 32:
        raise ConformanceError("exposure set is invalid")
    exposure_keys = []
    for item in exposures:
        require_keys(item, {"asset", "maximum_per_request_atomic", "maximum_outstanding_atomic"})
        validate_asset(item["asset"])
        if not atomic(item["maximum_per_request_atomic"], True) or not atomic(item["maximum_outstanding_atomic"], True):
            raise ConformanceError("exposure amount is invalid")
        if int(item["maximum_per_request_atomic"]) > int(item["maximum_outstanding_atomic"]):
            raise ConformanceError("per-request exposure exceeds outstanding exposure")
        exposure_keys.append(asset_key(item["asset"]))
    if exposure_keys != sorted(set(exposure_keys)):
        raise ConformanceError("exposure set is not canonical")
    validate_admission_limits(profile["admission_limits"])
    require_keys(profile["endpoints"], {"quote_url", "submit_url", "resolve_url", "evidence_url"})
    for endpoint in profile["endpoints"].values():
        validate_endpoint(endpoint)


def _find_profile(items: list[dict[str, Any]], uri: str, expected_digest: str) -> dict[str, Any] | None:
    return next((item for item in items if item["profile_uri"] == uri and item["profile_digest"] == expected_digest), None)


def validate_sponsorship_release_selection(body: dict[str, Any],
                                           terminal_profile_uri: str,
                                           terminal_profile_digest: str) -> None:
    names = ("sponsorship_release_evidence_class",
             "sponsorship_release_profile_uri",
             "sponsorship_release_profile_digest")
    if body["mode"] == "relay_exact":
        if any(name in body for name in names):
            raise ConformanceError("relay-only action carries a sponsorship release policy")
        return
    if any(name not in body for name in names):
        raise ConformanceError("sponsorship release policy is incomplete")
    evidence_class = body["sponsorship_release_evidence_class"]
    profile_uri = body["sponsorship_release_profile_uri"]
    profile_digest = body["sponsorship_release_profile_digest"]
    if (evidence_class not in SPONSORSHIP_RELEASE_CLASSES or
            not identifier(profile_uri, 256) or not digest(profile_digest)):
        raise ConformanceError("sponsorship release policy is invalid")
    if evidence_class == "validator_finality":
        if (profile_uri != terminal_profile_uri or
                profile_digest != terminal_profile_digest or
                body.get("sponsorship_terminal_evidence_class") !=
                "validator_finality"):
            raise ConformanceError("validator sponsorship release differs from selected finality")
    elif (body["assurance_level"] == "autonomous-decentralized" or
          profile_uri != RPC_CORROBORATION_PROFILE_URI or
          terminal_profile_uri != CLIENT_CORROBORATED_TERMINAL_PROFILE_URI or
          body.get("sponsorship_terminal_evidence_class") !=
          "client_corroborated"):
        raise ConformanceError("unproven sponsorship release is not permitted")


def validate_quote_request(signed: Any, profile: dict[str, Any]) -> None:
    require_keys(signed, {"body", "public_key", "signature"})
    body = signed["body"]
    required = {"schema_version", "request_id", "requester_agent_id", "provider_agent_id", "network", "mode",
                "assurance_level", "source_account",
                "source_account_authority_digest",
                "transaction_profile_uri", "transaction_profile_digest", "underlying_action_kind", "stable_action_id",
                "exact_request_digest", "signed_transaction_digest", "signed_transaction_cell_hash", "signed_transaction_size",
                "transaction_intent_digest", "source_sequence", "transaction_valid_until_unix", "maximum_service_fee",
                "maximum_network_fee_atomic", "maximum_transaction_value_atomic",
                "created_at_unix", "expires_at_unix"}
    optional = {"requested_sponsorship", "sponsorship_release_evidence_class",
                "sponsorship_release_profile_uri", "sponsorship_release_profile_digest",
                "relay_terminal_evidence_class",
                "sponsorship_terminal_evidence_class",
                "relay_finality_profile_uri", "relay_finality_profile_digest",
                "sponsorship_terminal_profile_uri",
                "sponsorship_terminal_profile_digest"}
    require_keys(body, required, optional)
    validate_network(body["network"])
    if (not u16(body["schema_version"]) or body["schema_version"] != 1 or
            not identifier(body["request_id"]) or not identifier(body["requester_agent_id"]) or
            not identifier(body["provider_agent_id"])):
        raise ConformanceError("quote request identity is invalid")
    if (body["provider_agent_id"] != profile["provider_agent_id"] or
            body["network"] not in profile["network_domains"] or
            body["mode"] not in profile["supported_modes"] or
            body["assurance_level"] not in profile["supported_assurance_levels"] or
            body["created_at_unix"] < profile["created_at_unix"] or
            body["expires_at_unix"] > profile["expires_at_unix"]):
        raise ConformanceError("quote request is outside service profile")
    relay_selected = body["mode"] in {"relay_exact", "sponsor_and_relay"}
    sponsorship_selected = body["mode"] in {"sponsor_only", "sponsor_and_relay"}
    relay_profile_fields = (
        "relay_finality_profile_uri", "relay_finality_profile_digest")
    sponsorship_profile_fields = (
        "sponsorship_terminal_profile_uri",
        "sponsorship_terminal_profile_digest")
    relay_class = body.get("relay_terminal_evidence_class")
    sponsorship_class = body.get("sponsorship_terminal_evidence_class")
    if relay_selected != all(name in body for name in relay_profile_fields) or \
            any(name in body for name in relay_profile_fields) != relay_selected:
        raise ConformanceError("relay finality profile selection is incomplete")
    if sponsorship_selected != all(name in body for name in sponsorship_profile_fields) or \
            any(name in body for name in sponsorship_profile_fields) != sponsorship_selected:
        raise ConformanceError("sponsorship terminal profile selection is incomplete")
    if (relay_selected != (relay_class in RELAY_TERMINAL_CLASSES) or
            sponsorship_selected !=
            (sponsorship_class in SPONSORSHIP_TERMINAL_CLASSES) or
            body["assurance_level"] == "autonomous-decentralized" and
            (relay_selected and relay_class != "validator_finality" or
             sponsorship_selected and sponsorship_class != "validator_finality")):
        raise ConformanceError("terminal evidence-class selection is invalid")
    if not sponsorship_selected and ("requested_sponsorship" in body or
            any(name in body for name in (
                "sponsorship_release_evidence_class",
                "sponsorship_release_profile_uri",
                "sponsorship_release_profile_digest"))):
        raise ConformanceError("relay-only request carries sponsorship")
    if sponsorship_selected:
        if "requested_sponsorship" not in body:
            raise ConformanceError("sponsorship request is missing")
        validate_amount(body["requested_sponsorship"], True)
        requested = body["requested_sponsorship"]
        exposure = next((item for item in profile["exposure_limits"]
                         if asset_key(item["asset"]) == asset_key(requested["asset"])), None)
        if exposure is None or int(requested["amount_atomic"]) > int(exposure["maximum_per_request_atomic"]):
            raise ConformanceError("requested sponsorship exceeds published exposure")
    if not identifier(body["source_account"]) or not digest(body["source_account_authority_digest"]) or not TOKEN.fullmatch(body["underlying_action_kind"]):
        raise ConformanceError("underlying action descriptor is invalid")
    for name in ("transaction_profile_digest", "stable_action_id", "exact_request_digest", "signed_transaction_digest",
                 "transaction_intent_digest") + tuple(
                     name for name in relay_profile_fields +
                     sponsorship_profile_fields if name in body and
                     name.endswith("_digest")):
        if not digest(body[name]):
            raise ConformanceError("quote request digest is invalid")
    if not isinstance(body["signed_transaction_cell_hash"], str) or not CELL_DIGEST.fullmatch(body["signed_transaction_cell_hash"]):
        raise ConformanceError("signed transaction cell hash is invalid")
    transaction = _find_profile(profile["transaction_profiles"], body["transaction_profile_uri"], body["transaction_profile_digest"])
    relay_finality = (_find_profile(
        profile["finality_profiles"], body["relay_finality_profile_uri"],
        body["relay_finality_profile_digest"]) if relay_selected else None)
    sponsorship_terminal = (_find_profile(
        profile["finality_profiles"], body["sponsorship_terminal_profile_uri"],
        body["sponsorship_terminal_profile_digest"])
        if sponsorship_selected else None)
    if (transaction is None or relay_selected != (relay_finality is not None) or
            sponsorship_selected != (sponsorship_terminal is not None)):
        raise ConformanceError("quote request profile is unsupported")
    if (relay_selected and
            relay_finality["terminal_evidence_class"] != relay_class or
            sponsorship_selected and
            sponsorship_terminal["terminal_evidence_class"] !=
            sponsorship_class):
        raise ConformanceError("quote request profile evidence class mismatch")
    if sponsorship_selected:
        validate_sponsorship_release_selection(
            body, body["sponsorship_terminal_profile_uri"],
            body["sponsorship_terminal_profile_digest"])
    if (not u32(body["signed_transaction_size"]) or
            not 0 < body["signed_transaction_size"] <= transaction["maximum_signed_bytes"]):
        raise ConformanceError("declared signed transaction size exceeds profile")
    validate_amount(body["maximum_service_fee"])
    if asset_key(body["maximum_service_fee"]["asset"]) not in [asset_key(item) for item in profile["fee_assets"]]:
        raise ConformanceError("maximum service fee asset is unsupported")
    if not atomic(body["maximum_network_fee_atomic"]) or not atomic(body["maximum_transaction_value_atomic"]):
        raise ConformanceError("transaction exposure is invalid")
    if (not u64(body["source_sequence"]) or
            not positive_u64(body["created_at_unix"]) or not positive_u64(body["expires_at_unix"]) or
            not positive_u64(body["transaction_valid_until_unix"]) or
            not body["created_at_unix"] < body["expires_at_unix"] < body["transaction_valid_until_unix"]):
        raise ConformanceError("quote request lifetime is invalid")
    if body["expires_at_unix"] - body["created_at_unix"] > MAX_REQUEST_LIFETIME:
        raise ConformanceError("quote request lifetime exceeds bound")
    if (sponsorship_selected and body["created_at_unix"] +
            sponsorship_terminal["maximum_resolution_seconds"] + 30 >=
            body["transaction_valid_until_unix"]):
        raise ConformanceError("sponsorship finality window is unsatisfiable")
    message = signature_message(b"tos.agent-relay-quote-request-signature.v1\x00", body)
    if not verify_ed25519(decode_public(signed["public_key"]), message, decode_signature(signed["signature"])):
        raise ConformanceError("quote request signature is invalid")


def validate_provider_quote(signed: Any, request: dict[str, Any], profile: dict[str, Any]) -> None:
    require_keys(signed, {"body", "public_key", "signature"})
    body = signed["body"]
    required = {"schema_version", "quote_id", "quote_request_digest", "service_profile_digest", "provider_agent_id", "mode",
                "assurance_level",
                "fee_lines", "maximum_network_fee_atomic", "maximum_transaction_value_atomic", "maximum_request_bytes",
                "status_endpoint", "provider_policy_revision", "valid_from_unix", "expires_at_unix"}
    optional = {"reserved_sponsorship", "offer_intent_digest",
                "sponsorship_release_evidence_class",
                "sponsorship_release_profile_uri", "sponsorship_release_profile_digest",
                "relay_terminal_evidence_class",
                "sponsorship_terminal_evidence_class",
                "relay_finality_profile", "sponsorship_terminal_profile"}
    require_keys(body, required, optional)
    if (not u16(body["schema_version"]) or body["schema_version"] != 1 or
            not identifier(body["quote_id"]) or
            body["provider_agent_id"] != request["body"]["provider_agent_id"]):
        raise ConformanceError("provider quote identity is invalid")
    if "offer_intent_digest" in body and not digest(body["offer_intent_digest"]):
        raise ConformanceError("provider quote offer Intent digest is invalid")
    if body["quote_request_digest"] != protocol_digest("tos.agent-relay-quote-request.v1", request["body"]):
        raise ConformanceError("provider quote request digest mismatch")
    if body["service_profile_digest"] != protocol_digest("tos.agent-relay-service-profile.v1", profile):
        raise ConformanceError("provider quote service profile mismatch")
    if (body["provider_agent_id"] != profile["provider_agent_id"] or
            body["mode"] != request["body"]["mode"] or
            body["assurance_level"] != request["body"]["assurance_level"]):
        raise ConformanceError("provider quote route, mode, or assurance mismatch")
    expected_fees = {
        "relay_exact": ["transaction_relay_fee"],
        "sponsor_only": ["gas_sponsorship_fee"],
        "sponsor_and_relay": ["gas_sponsorship_fee", "transaction_relay_fee"],
    }[body["mode"]]
    if [line.get("kind") for line in body["fee_lines"]] != expected_fees:
        raise ConformanceError("provider quote fee-line set is invalid")
    total = 0
    for line in body["fee_lines"]:
        require_keys(line, {"kind", "amount"})
        validate_amount(line["amount"])
        if asset_key(line["amount"]["asset"]) != asset_key(request["body"]["maximum_service_fee"]["asset"]):
            raise ConformanceError("provider quote fee asset mismatch")
        total += int(line["amount"]["amount_atomic"])
    if total > int(request["body"]["maximum_service_fee"]["amount_atomic"]):
        raise ConformanceError("provider quote exceeds maximum service fee")
    relay_selected = body["mode"] in {"relay_exact", "sponsor_and_relay"}
    sponsorship_selected = body["mode"] in {"sponsor_only", "sponsor_and_relay"}
    relay_class = body.get("relay_terminal_evidence_class")
    sponsorship_class = body.get("sponsorship_terminal_evidence_class")
    if relay_selected != ("relay_finality_profile" in body) or \
            sponsorship_selected != ("sponsorship_terminal_profile" in body):
        raise ConformanceError("provider quote profile matrix is invalid")
    if (relay_selected != (relay_class in RELAY_TERMINAL_CLASSES) or
            sponsorship_selected !=
            (sponsorship_class in SPONSORSHIP_TERMINAL_CLASSES) or
            relay_class != request["body"].get("relay_terminal_evidence_class") or
            sponsorship_class !=
            request["body"].get("sponsorship_terminal_evidence_class")):
        raise ConformanceError("provider quote changes terminal evidence class")
    if not sponsorship_selected and ("reserved_sponsorship" in body or
            any(name in body for name in (
                "sponsorship_release_evidence_class",
                "sponsorship_release_profile_uri",
                "sponsorship_release_profile_digest"))):
        raise ConformanceError("relay-only quote reserves sponsorship")
    if sponsorship_selected:
        if body.get("reserved_sponsorship") != request["body"].get("requested_sponsorship"):
            raise ConformanceError("provider quote changes sponsorship")
    if body["maximum_network_fee_atomic"] != request["body"]["maximum_network_fee_atomic"] or body["maximum_transaction_value_atomic"] != request["body"]["maximum_transaction_value_atomic"]:
        raise ConformanceError("provider quote changes transaction exposure")
    if (not u32(body["maximum_request_bytes"]) or
            body["maximum_request_bytes"] < request["body"]["signed_transaction_size"] or
            body["maximum_request_bytes"] > profile["maximum_request_bytes"]):
        raise ConformanceError("provider quote request-byte bound is invalid")
    if relay_selected:
        validate_finality(body["relay_finality_profile"])
        selected_relay = _find_profile(
            profile["finality_profiles"],
            request["body"]["relay_finality_profile_uri"],
            request["body"]["relay_finality_profile_digest"])
        if selected_relay is None or body["relay_finality_profile"] != selected_relay:
            raise ConformanceError("provider quote relay finality mismatch")
        if body["relay_finality_profile"]["terminal_evidence_class"] != relay_class:
            raise ConformanceError("provider quote relay profile class mismatch")
    if sponsorship_selected:
        validate_finality(body["sponsorship_terminal_profile"])
        selected_sponsorship = _find_profile(
            profile["finality_profiles"],
            request["body"]["sponsorship_terminal_profile_uri"],
            request["body"]["sponsorship_terminal_profile_digest"])
        if (selected_sponsorship is None or
                body["sponsorship_terminal_profile"] != selected_sponsorship):
            raise ConformanceError("provider quote sponsorship terminal mismatch")
        if (body["sponsorship_terminal_profile"]["terminal_evidence_class"] !=
                sponsorship_class):
            raise ConformanceError(
                "provider quote sponsorship profile class mismatch")
        validate_sponsorship_release_selection(
            body, body["sponsorship_terminal_profile"]["profile_uri"],
            body["sponsorship_terminal_profile"]["profile_digest"])
    for name in ("sponsorship_release_evidence_class",
                 "sponsorship_release_profile_uri",
                 "sponsorship_release_profile_digest"):
        if body.get(name) != request["body"].get(name):
            raise ConformanceError("provider quote changes sponsorship release policy")
    validate_endpoint(body["status_endpoint"])
    if (body["status_endpoint"] != profile["endpoints"]["resolve_url"] or
            not positive_u64(body["provider_policy_revision"]) or
            body["provider_policy_revision"] != profile["policy_revision"]):
        raise ConformanceError("provider quote endpoint or policy mismatch")
    if (not positive_u64(body["valid_from_unix"]) or not positive_u64(body["expires_at_unix"]) or
            not request["body"]["created_at_unix"] <= body["valid_from_unix"] <
            body["expires_at_unix"] <= request["body"]["expires_at_unix"]):
        raise ConformanceError("provider quote lifetime is invalid")
    if body["expires_at_unix"] - body["valid_from_unix"] > MAX_REQUEST_LIFETIME:
        raise ConformanceError("provider quote lifetime exceeds bound")
    message = signature_message(b"tos.agent-relay-provider-quote-signature.v1\x00", body)
    if not verify_ed25519(decode_public(signed["public_key"]), message, decode_signature(signed["signature"])):
        raise ConformanceError("provider quote signature is invalid")


def load_semantic_registry(path: Path) -> dict[str, dict[str, Any]]:
    document = json.loads(path.read_text(encoding="utf-8"))
    if document.get("schema") != "tos.semantic-action-registry.v1":
        raise ConformanceError("semantic registry schema is unknown")
    registry: dict[str, dict[str, Any]] = {}
    for entry in document.get("entries", []):
        kind = entry.get("action_kind")
        if not isinstance(kind, str) or not TOKEN.fullmatch(kind) or kind in registry:
            raise ConformanceError("semantic registry kind is invalid")
        registry[kind] = entry
    if not registry:
        raise ConformanceError("semantic registry is empty")
    return registry


def _lp16(value: bytes) -> bytes:
    if not value or len(value) > 0xFFFF:
        raise ConformanceError("semantic lp16 value is invalid")
    return struct.pack(">H", len(value)) + value


def _lp32(value: bytes) -> bytes:
    if not value or len(value) > 1 << 20:
        raise ConformanceError("semantic lp32 value is invalid")
    return struct.pack(">I", len(value)) + value


def _semantic_bytes(name: str, field_type: str, value: Any) -> bytes:
    if field_type == "u64":
        if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 0xFFFFFFFFFFFFFFFF:
            raise ConformanceError("semantic u64 is invalid")
        return struct.pack(">Q", value)
    if not isinstance(value, str) or not value or "\x00" in value:
        raise ConformanceError("semantic text is invalid")
    raw = value.encode()
    if field_type == "digest32":
        if not digest(value):
            raise ConformanceError("semantic digest is invalid")
        return bytes.fromhex(value[7:])
    if field_type in {"kind", "state"} and not TOKEN.fullmatch(value):
        raise ConformanceError("semantic token is invalid")
    if field_type == "id" and name == "amount_atomic" and not ATOMIC.fullmatch(value):
        raise ConformanceError("semantic atomic amount is invalid")
    return raw


def derive_semantic_id(registry: dict[str, dict[str, Any]], action_kind: str,
                       fields: list[dict[str, Any]]) -> str:
    entry = registry.get(action_kind)
    if entry is None:
        raise ConformanceError("underlying semantic action kind is unknown")
    definitions = entry["ordered_semantic_fields"]
    if len(fields) != len(definitions):
        raise ConformanceError("semantic field count mismatch")
    preimage = bytearray(b"TOS-SAI\x00")
    preimage += struct.pack(">HH", entry["registry_version"], entry["entry_version"])
    preimage += _lp16(entry["domain_tag"].encode("ascii"))
    preimage += _lp16(action_kind.encode("ascii"))
    preimage += struct.pack(">H", len(definitions))
    for definition, field in zip(definitions, fields):
        require_keys(field, {"name", "type"}, {"text", "number"})
        if field["name"] != definition["field_name"] or field["type"] != definition["field_type"]:
            raise ConformanceError("semantic fields are not in registry order")
        if field["type"] == "u64":
            if "number" not in field or "text" in field:
                raise ConformanceError("semantic number representation is invalid")
            value = field["number"]
        else:
            if "text" not in field or "number" in field:
                raise ConformanceError("semantic text representation is invalid")
            value = field["text"]
        preimage += _lp16(field["name"].encode("ascii"))
        preimage += _lp32(_semantic_bytes(field["name"], field["type"], value))
    return "sha256:" + hashlib.sha256(preimage).hexdigest()


def validate_writer_fence(fence: Any) -> None:
    require_keys(fence, {"body", "public_key", "fence_proof"})
    body = fence["body"]
    required = {"schema_version", "owner_id", "agent_id", "instance_id", "lease_id", "writer_generation",
                "issued_at_unix", "expires_at_unix", "authority_id", "scope"}
    require_keys(body, required)
    if (not u16(body["schema_version"]) or body["schema_version"] != 1 or
            any(not identifier(body[name]) for name in
                ("owner_id", "agent_id", "instance_id", "lease_id", "authority_id"))):
        raise ConformanceError("writer fence identity is invalid")
    if (not positive_u64(body["writer_generation"]) or not positive_u64(body["issued_at_unix"]) or
            not positive_u64(body["expires_at_unix"]) or
            not body["issued_at_unix"] < body["expires_at_unix"]):
        raise ConformanceError("writer fence lifetime or generation is invalid")
    if not isinstance(body["scope"], list) or not body["scope"] or body["scope"] != sorted(set(body["scope"])) or any(not TOKEN.fullmatch(item) for item in body["scope"]):
        raise ConformanceError("writer fence scope is invalid")
    message = signature_message(b"tos.writer-fence.v1\x00", body)
    if not verify_ed25519(decode_public(fence["public_key"]), message, decode_signature(fence["fence_proof"])):
        raise ConformanceError("writer fence signature is invalid")


def validate_authorized_action(action: Any, fence: dict[str, Any], fields: list[dict[str, Any]],
                               request_bytes: bytes, registry: dict[str, dict[str, Any]]) -> None:
    required = {"schema_version", "owner_id", "agent_id", "action_kind", "stable_action_id", "exact_request_digest",
                "writer_generation", "writer_fence_digest", "policy_revision", "mandate_digest", "expected_prior_state",
                "expires_at_unix", "authority_id", "authority_public_key", "authorization_proof"}
    require_keys(action, required, {"approval_digest"})
    if (not u16(action["schema_version"]) or action["schema_version"] != 1 or
            action["action_kind"] not in registry or
            not positive_u64(action["writer_generation"]) or
            not positive_u64(action["policy_revision"]) or
            not positive_u64(action["expires_at_unix"])):
        raise ConformanceError("authorized action kind is invalid")
    if action["stable_action_id"] != derive_semantic_id(registry, action["action_kind"], fields):
        raise ConformanceError("authorized action stable identity mismatch")
    if action["exact_request_digest"] != exact_request_digest(request_bytes):
        raise ConformanceError("authorized action exact request mismatch")
    semantic = {field["name"]: field.get("text", field.get("number")) for field in fields}
    if semantic.get("owner_id") != action["owner_id"] or semantic.get("agent_id") != action["agent_id"]:
        raise ConformanceError("authorized action owner or Agent mismatch")
    if action["writer_generation"] != fence["body"]["writer_generation"] or action["writer_fence_digest"] != protocol_digest("tos.writer-fence-envelope.v1", fence):
        raise ConformanceError("authorized action writer fence mismatch")
    if action["authority_id"] != fence["body"]["authority_id"] or action["authority_public_key"] != fence["public_key"]:
        raise ConformanceError("authorized action authority mismatch")
    unsigned = copy.deepcopy(action)
    unsigned["authorization_proof"] = ""
    message = signature_message(b"tos.authorized-action-proof.v1\x00", unsigned)
    if not verify_ed25519(decode_public(action["authority_public_key"]), message, decode_signature(action["authorization_proof"])):
        raise ConformanceError("authorized action signature is invalid")


def execution_projection(request: dict[str, Any]) -> dict[str, Any]:
    # AuthorizedAction and WriterFence are deliberately absent. They are
    # replaceable admission credentials during writer takeover.
    names = ["schema_version", "quote_request", "provider_quote", "agreement_body_digest", "agreement_expires_at_unix",
             "relay_obligation_id", "sponsorship_obligation_id", "fee_obligation_ids", "signed_transaction_bytes",
             "underlying_action_request", "semantic_fields", "created_at_unix", "expires_at_unix"]
    return {name: copy.deepcopy(request[name]) for name in names if name in request}


def execution_digest(request: dict[str, Any]) -> str:
    return protocol_digest("tos.agent-relay-execution-request.v1", execution_projection(request))


def _framed_sha256(domain: bytes, canonical: bytes) -> bytes:
    return hashlib.sha256(domain + struct.pack(">I", len(canonical)) + canonical).digest()


def prepare_agreement_targets(body: dict[str, Any]) -> dict[str, Any]:
    prepared = copy.deepcopy(body)
    core = {name: copy.deepcopy(value) for name, value in prepared.items()
            if name != "authorization_predicates"}
    policy = []
    for predicate in prepared["authorization_predicates"]:
        projected = {name: copy.deepcopy(value) for name, value in predicate.items()
                     if name != "evidence_target_projection_digest"}
        policy.append(projected)
    core_digest = _framed_sha256(b"tos.agreement-core.v1\x00", bounded_canonical_cbor(core))
    policy_digest = _framed_sha256(b"tos.agreement-authorization-policy.v1\x00",
                                   bounded_canonical_cbor(policy))
    for predicate in prepared["authorization_predicates"]:
        predicate_id = predicate["predicate_id"].encode()
        if not predicate_id or len(predicate_id) > 0xFFFF:
            raise ConformanceError("Agreement predicate identity is invalid")
        target = hashlib.sha256(b"tos.agreement-authorization-target.v1\x00" + core_digest +
                                policy_digest + struct.pack(">H", len(predicate_id)) + predicate_id).hexdigest()
        predicate["evidence_target_projection_digest"] = "sha256:" + target
    return prepared


def validate_agreement(agreement: Any, execution: dict[str, Any], binding: dict[str, Any]) -> None:
    require_keys(agreement, {"body", "authorization_evidence"})
    body = agreement["body"]
    required = {"schema_version", "agreement_id", "version", "network_context", "participants",
                "terms_content_type", "terms", "obligations", "authorization_predicates",
                "valid_from_unix", "expires_at_unix"}
    optional = {"predecessor_agreement_digest", "referenced_intents", "attachment_digests",
                "required_extensions", "optional_extensions"}
    require_keys(body, required, optional)
    binding_bytes = bounded_canonical_cbor(binding)
    if (not u16(body["schema_version"]) or body["schema_version"] != 1 or
            not positive_u64(body["version"]) or
            not identifier(body["agreement_id"]) or not identifier(body["network_context"]) or
            body["terms_content_type"] != AGREEMENT_BINDING_CONTENT_TYPE or
            decode_base64(body["terms"], 256 << 10) != binding_bytes or
            protocol_digest("tos.agent-agreement-body.v1", body) != execution["agreement_body_digest"] or
            not positive_u64(body["valid_from_unix"]) or not positive_u64(body["expires_at_unix"]) or
            body["valid_from_unix"] >= body["expires_at_unix"] or
            body["expires_at_unix"] != execution["agreement_expires_at_unix"]):
        raise ConformanceError("Submit Agreement does not bind its exact top-level terms")
    participants = body["participants"]
    participant_ids = [item.get("agent_id") for item in participants] if isinstance(participants, list) else []
    if participant_ids != sorted(set(participant_ids)) or set(participant_ids) != {
            execution["quote_request"]["body"]["requester_agent_id"],
            execution["quote_request"]["body"]["provider_agent_id"]}:
        raise ConformanceError("relay Agreement participant set is invalid")
    predicates = body["authorization_predicates"]
    if (not isinstance(predicates, list) or not predicates or
            [item.get("predicate_id") for item in predicates] !=
            sorted(set(item.get("predicate_id") for item in predicates))):
        raise ConformanceError("relay Agreement predicate set is invalid")
    unprepared = copy.deepcopy(body)
    for predicate in unprepared["authorization_predicates"]:
        predicate["evidence_target_projection_digest"] = ""
    expected_prepared = prepare_agreement_targets(unprepared)
    if expected_prepared["authorization_predicates"] != predicates:
        raise ConformanceError("relay Agreement authorization target is invalid")
    binding_b64 = _b64(binding_bytes)
    obligations = body["obligations"]
    if not isinstance(obligations, list) or not obligations:
        raise ConformanceError("relay Agreement obligation set is empty")
    by_id = {item.get("obligation_id"): item for item in obligations}
    if len(by_id) != len(obligations):
        raise ConformanceError("relay Agreement obligation identity is duplicated")
    quote = execution["provider_quote"]["body"]
    request = execution["quote_request"]["body"]
    expected: dict[str, tuple[str, str, str, dict[str, Any] | None, str | None]] = {}
    if "relay_obligation_id" in execution:
        expected[execution["relay_obligation_id"]] = (
            "transaction_relay", request["provider_agent_id"], request["requester_agent_id"], None, None)
    if "sponsorship_obligation_id" in execution:
        expected[execution["sponsorship_obligation_id"]] = (
            "gas_sponsorship", request["provider_agent_id"], request["requester_agent_id"],
            quote.get("reserved_sponsorship"), "tos.payment.direct.v1")
    fee_lines_by_kind = {line["kind"]: line for line in quote["fee_lines"]}
    if len(fee_lines_by_kind) != len(quote["fee_lines"]):
        raise ConformanceError("relay quote fee kind is duplicated")
    for obligation_id in execution["fee_obligation_ids"]:
        kind = by_id.get(obligation_id, {}).get("kind")
        line = fee_lines_by_kind.get(kind)
        if line is None:
            raise ConformanceError("relay fee obligation does not map by its frozen kind")
        expected[obligation_id] = (kind, request["requester_agent_id"],
                                   request["provider_agent_id"], line["amount"], "tos.payment.direct.v1")
    if not set(expected).issubset(by_id):
        raise ConformanceError("relay Agreement obligation set is incomplete")
    for obligation_id, (kind, obligor, beneficiary, amount, adapter) in expected.items():
        obligation = by_id[obligation_id]
        if (obligation.get("kind") != kind or obligation.get("obligor_agent_id") != obligor or
                obligation.get("beneficiary_agent_id") != beneficiary or
                obligation.get("subject_content_type") != AGREEMENT_BINDING_CONTENT_TYPE or
                obligation.get("subject") != binding_b64 or
                not obligation.get("authorization_predicate_ids")):
            raise ConformanceError("relay Agreement obligation binding is invalid")
        if amount is None:
            if "amount" in obligation or "settlement_adapter_uri" in obligation or "settlement_parameters" in obligation:
                raise ConformanceError("non-value relay obligation carries settlement data")
        else:
            expected_amount = {"asset_namespace": amount["asset"]["asset_namespace"],
                               "asset_identifier": amount["asset"]["asset_identifier"],
                               "amount_atomic": amount["amount_atomic"], "unit": amount["asset"]["unit"]}
            if (obligation.get("amount") != expected_amount or
                    obligation.get("settlement_adapter_uri") != adapter or
                    decode_base64(obligation.get("settlement_parameters"), 256 << 10) != b"\xa0"):
                raise ConformanceError("value-bearing relay obligation is not exact")
    reserved_kinds = {
        "transaction_relay", "gas_sponsorship",
        "transaction_relay_fee", "gas_sponsorship_fee",
    }
    for obligation_id, obligation in by_id.items():
        expected_entry = expected.get(obligation_id)
        reuses_binding = (obligation.get("subject_content_type") == AGREEMENT_BINDING_CONTENT_TYPE and
                          obligation.get("subject") == binding_b64)
        if ((obligation.get("kind") in reserved_kinds or reuses_binding) and
                (expected_entry is None or obligation.get("kind") != expected_entry[0])):
            raise ConformanceError("relay Agreement has an unreferenced or conflicting service obligation")
    evidence = agreement["authorization_evidence"]
    if not isinstance(evidence, list) or len(evidence) != 2:
        raise ConformanceError("relay Agreement authorization evidence is incomplete")
    agreement_digest = execution["agreement_body_digest"]
    predicate_by_id = {item["predicate_id"]: item for item in predicates}
    seen_subjects: set[str] = set()
    for item in evidence:
        required_evidence = {"agreement_id", "agreement_version", "agreement_body_digest", "authority_subject",
                             "predicate_ids", "evidence_profile_uri", "evidence_profile_version",
                             "evidence_profile_digest", "evidence_target_projection_digests",
                             "evidence_content_type", "evidence"}
        require_keys(item, required_evidence)
        subject = item["authority_subject"]
        subject_id = subject.get("subject_identifier") if isinstance(subject, dict) else None
        predicate_ids = item["predicate_ids"]
        target_digests = item["evidence_target_projection_digests"]
        if (item["agreement_id"] != body["agreement_id"] or item["agreement_version"] != body["version"] or
                item["agreement_body_digest"] != agreement_digest or item["evidence_profile_uri"] != AGENT_SIGNATURE_PROFILE_URI or
                item["evidence_profile_version"] != 1 or item["evidence_profile_digest"] != AGENT_SIGNATURE_PROFILE_DIGEST or
                item["evidence_content_type"] != AGREEMENT_ACCEPTANCE_CONTENT_TYPE or
                not isinstance(predicate_ids, list) or predicate_ids != sorted(set(predicate_ids)) or
                target_digests != [predicate_by_id[predicate_id]["evidence_target_projection_digest"]
                                   for predicate_id in predicate_ids] or
                any(predicate_by_id[predicate_id]["authority_subject"] != subject for predicate_id in predicate_ids) or
                subject_id in seen_subjects):
            raise ConformanceError("relay Agreement authorization evidence does not match its predicates")
        signed_acceptance = decode_base64(item["evidence"], 1 << 20)
        # The generic Agent Commerce verifier decodes and verifies this signed
        # envelope. This independent relay verifier still binds its exact bytes
        # into the Agreement and rejects empty, substituted, or partial groups.
        if not signed_acceptance:
            raise ConformanceError("relay Agreement acceptance evidence is empty")
        seen_subjects.add(subject_id)


def validate_submit_call(call: Any, profile: dict[str, Any], registry: dict[str, dict[str, Any]],
                         binding: dict[str, Any]) -> None:
    require_keys(call, {"request", "agreement"})
    validate_execution(call["request"], profile, registry)
    validate_agreement(call["agreement"], call["request"], binding)


def validate_agreement_binding(binding: Any, request: dict[str, Any], quote: dict[str, Any], profile: dict[str, Any]) -> None:
    required = {"schema_version", "quote_request_digest", "provider_quote_digest", "service_profile_digest", "mode",
                "assurance_level",
                "requester_agent_id", "provider_agent_id", "stable_action_id", "exact_request_digest", "signed_transaction_digest"}
    optional = {"sponsorship_release_evidence_class",
                "sponsorship_release_profile_uri", "sponsorship_release_profile_digest",
                "relay_terminal_evidence_class",
                "sponsorship_terminal_evidence_class",
                "relay_finality_profile_uri", "relay_finality_profile_digest",
                "sponsorship_terminal_profile_uri",
                "sponsorship_terminal_profile_digest"}
    require_keys(binding, required, optional)
    if not u16(binding["schema_version"]) or binding["schema_version"] != 1:
        raise ConformanceError("Agreement binding schema version is invalid")
    body = request["body"]
    expected = {
        "schema_version": 1,
        "quote_request_digest": protocol_digest("tos.agent-relay-quote-request.v1", body),
        "provider_quote_digest": protocol_digest("tos.agent-relay-provider-quote.v1", quote["body"]),
        "service_profile_digest": protocol_digest("tos.agent-relay-service-profile.v1", profile),
        "mode": body["mode"],
        "assurance_level": body["assurance_level"],
        "requester_agent_id": body["requester_agent_id"],
        "provider_agent_id": body["provider_agent_id"],
        "stable_action_id": body["stable_action_id"],
        "exact_request_digest": body["exact_request_digest"],
        "signed_transaction_digest": body["signed_transaction_digest"],
    }
    if body["mode"] in {"relay_exact", "sponsor_and_relay"}:
        expected.update({
            "relay_terminal_evidence_class": body[
                "relay_terminal_evidence_class"],
            "relay_finality_profile_uri": body["relay_finality_profile_uri"],
            "relay_finality_profile_digest": body[
                "relay_finality_profile_digest"],
        })
    if body["mode"] != "relay_exact":
        expected.update({
            "sponsorship_release_evidence_class": body["sponsorship_release_evidence_class"],
            "sponsorship_release_profile_uri": body["sponsorship_release_profile_uri"],
            "sponsorship_release_profile_digest": body["sponsorship_release_profile_digest"],
            "sponsorship_terminal_evidence_class": body[
                "sponsorship_terminal_evidence_class"],
            "sponsorship_terminal_profile_uri": body[
                "sponsorship_terminal_profile_uri"],
            "sponsorship_terminal_profile_digest": body[
                "sponsorship_terminal_profile_digest"],
        })
    if binding != expected:
        raise ConformanceError("Agreement binding does not match quote and request")


def validate_domain_bound_payment_request(request: Any, network: dict[str, Any],
                                          semantic_fields: list[dict[str, Any]] | None,
                                          registry: dict[str, dict[str, Any]]) -> tuple[bytes, list[dict[str, Any]]]:
    """Validate the exact AgreementPaymentRequestV3 model used by relay.

    V3 deliberately keeps ``network_id`` for the released payment.direct
    semantic registry while also committing the complete chain domain through
    ``network_domain_digest``.  The destination digest contains both values,
    so a payment cannot be replayed onto a different genesis that happens to
    reuse the same display network ID.
    """
    required = {
        "schema_version", "owner_id", "agent_id", "agreement_body_digest",
        "agreement_obligation_id", "obligation_instance_id", "payer_agent_id",
        "payee_agent_id", "network_id", "network_domain_digest", "amount",
        "destination", "settlement_adapter_uri", "stable_action_id",
        "expires_at_unix",
    }
    require_keys(request, required)
    validate_network(network)
    amount = request["amount"]
    require_keys(amount, {"asset_namespace", "asset_identifier", "amount_atomic", "unit"})
    if (not u16(request["schema_version"]) or request["schema_version"] != 3 or
            any(not identifier(request[name], limit) for name, limit in (
                ("owner_id", 256), ("agent_id", 256),
                ("agreement_obligation_id", 128), ("payer_agent_id", 256),
                ("payee_agent_id", 256), ("network_id", 128),
                ("settlement_adapter_uri", 256))) or
            not digest(request["agreement_body_digest"]) or
            not digest(request["obligation_instance_id"]) or
            not digest(request["network_domain_digest"]) or
            not digest(request["stable_action_id"]) or
            not positive_u64(request["expires_at_unix"]) or
            request["network_id"] != network["network_id"] or
            request["network_domain_digest"] != protocol_digest(
                "tos.agent-relay-network-domain.v1", network) or
            any(not identifier(amount[name], limit) for name, limit in (
                ("asset_namespace", 128), ("asset_identifier", 256), ("unit", 128))) or
            not atomic(amount["amount_atomic"], positive=True)):
        raise ConformanceError("domain-bound Agreement payment request is invalid")
    destination = decode_base64(request["destination"], 64 << 10)
    asset_digest = protocol_digest("tos.agreement-payment-asset.v1", {
        "namespace": amount["asset_namespace"],
        "identifier": amount["asset_identifier"],
        "unit": amount["unit"],
    })
    destination_digest = protocol_digest("tos.agreement-payment-destination.v1", {
        "network_id": request["network_id"],
        "network_domain_digest": request["network_domain_digest"],
        "adapter_uri": request["settlement_adapter_uri"],
        "destination": _b64(destination),
    })
    derived_fields = _semantic_fields(registry, "payment.direct", {
        "owner_id": request["owner_id"],
        "agent_id": request["agent_id"],
        "agreement_body_digest": request["agreement_body_digest"],
        "obligation_instance_id": request["obligation_instance_id"],
        "payer_id": request["payer_agent_id"],
        "payee_id": request["payee_agent_id"],
        "network_id": request["network_id"],
        "asset_digest": asset_digest,
        "amount_atomic": amount["amount_atomic"],
        "destination_digest": destination_digest,
    })
    if semantic_fields is not None and semantic_fields != derived_fields:
        raise ConformanceError("domain-bound Agreement payment semantic fields were substituted")
    if request["stable_action_id"] != derive_semantic_id(registry, "payment.direct", derived_fields):
        raise ConformanceError("domain-bound Agreement payment stable identity mismatch")
    return bounded_canonical_cbor(request), derived_fields


def relay_stage_mask(mode: str) -> list[str]:
    masks = {
        "relay_exact": ["broadcast"],
        "sponsor_only": ["sponsorship"],
        "sponsor_and_relay": ["broadcast", "sponsorship"],
    }
    if mode not in masks:
        raise ConformanceError("relay admission mode is invalid")
    return masks[mode]


def transaction_identity(request_body: dict[str, Any]) -> dict[str, Any]:
    names = (
        "network", "source_account", "source_account_authority_digest",
        "transaction_profile_uri", "transaction_profile_digest",
        "underlying_action_kind", "stable_action_id", "exact_request_digest",
        "signed_transaction_digest", "signed_transaction_cell_hash",
        "signed_transaction_size", "transaction_intent_digest",
        "source_sequence", "transaction_valid_until_unix",
    )
    return {"schema_version": 1, **{
        name: copy.deepcopy(request_body[name]) for name in names
    }}


def admission_lookup(body: dict[str, Any]) -> dict[str, Any]:
    names = [
        "schema_version", "owner_id", "agent_id", "authenticated_principal_id",
        "authority_id", "provider_agent_id", "service_profile_digest",
        "provider_quote_digest", "network_digest", "transaction_identity_digest",
        "mode", "assurance_level", "stage_mask", "route_attempt", "stable_action_id",
        "exact_request_digest", "relay_execution_request_digest",
    ]
    result = {name: copy.deepcopy(body[name]) for name in names}
    if "predecessor_receipt_digest" in body:
        result["predecessor_receipt_digest"] = body["predecessor_receipt_digest"]
    return result


def validate_admission_request(value: Any, execution: dict[str, Any]) -> None:
    required = {
        "schema_version", "owner_id", "agent_id", "authenticated_principal_id",
        "provider_agent_id", "service_profile_digest", "provider_quote_digest",
        "network_digest", "transaction_identity_digest", "mode", "assurance_level", "stage_mask",
        "route_attempt", "stable_action_id",
        "exact_request_digest", "relay_execution_request_digest",
        "authorized_action", "writer_fence", "underlying_action_request",
        "semantic_fields", "requested_start_not_after_unix",
    }
    require_keys(value, required, {"predecessor_receipt_digest"})
    action = execution["authorized_action"]
    fence = execution["writer_fence"]
    request_body = execution["quote_request"]["body"]
    quote_body = execution["provider_quote"]["body"]
    if (not u16(value["schema_version"]) or value["schema_version"] != 1 or
            any(not identifier(value[name]) for name in (
                "owner_id", "agent_id", "authenticated_principal_id",
                "provider_agent_id")) or
            not positive_u64(value["requested_start_not_after_unix"]) or
            not integer(value["route_attempt"], 1, 32)):
        raise ConformanceError("relay admission request identity is invalid")
    if ((value["route_attempt"] == 1) !=
            ("predecessor_receipt_digest" not in value)):
        raise ConformanceError("relay admission predecessor shape is invalid")
    if ("predecessor_receipt_digest" in value and
            not digest(value["predecessor_receipt_digest"])):
        raise ConformanceError("relay admission predecessor digest is invalid")
    if value["assurance_level"] not in ASSURANCE_LEVELS:
        raise ConformanceError("relay admission assurance level is invalid")
    if (value["route_attempt"] > 1 and
            value["assurance_level"] != "autonomous-decentralized"):
        raise ConformanceError("non-decentralized assurance cannot create a route successor")
    if value["mode"] != "relay_exact" and value["route_attempt"] != 1:
        raise ConformanceError("sponsorship route cannot have a V1 successor")
    if value["owner_id"] != action["owner_id"] or value["agent_id"] != action["agent_id"]:
        raise ConformanceError("relay admission request owner or Agent mismatch")
    if (value["provider_agent_id"] != quote_body["provider_agent_id"] or
            value["service_profile_digest"] != quote_body["service_profile_digest"] or
            value["provider_quote_digest"] != protocol_digest(
                "tos.agent-relay-provider-quote.v1", quote_body) or
            value["network_digest"] != protocol_digest(
                "tos.agent-relay-network-domain.v1", request_body["network"]) or
            value["transaction_identity_digest"] != protocol_digest(
                "tos.agent-relay-transaction-identity.v1",
                transaction_identity(request_body))):
        raise ConformanceError("relay admission request Provider route mismatch")
    if (value["mode"] != request_body["mode"] or
            value["assurance_level"] != request_body["assurance_level"] or
            value["stage_mask"] != relay_stage_mask(value["mode"]) or
            value["stable_action_id"] != action["stable_action_id"] or
            value["exact_request_digest"] != action["exact_request_digest"] or
            value["relay_execution_request_digest"] != execution_digest(execution) or
            value["authorized_action"] != action or value["writer_fence"] != fence or
            value["underlying_action_request"] != execution["underlying_action_request"] or
            value["semantic_fields"] != execution["semantic_fields"]):
        raise ConformanceError("relay admission request substituted its exact action")
    if (value["requested_start_not_after_unix"] <= execution["created_at_unix"] or
            value["requested_start_not_after_unix"] > min(
                execution["expires_at_unix"], execution["agreement_expires_at_unix"],
                quote_body["expires_at_unix"], action["expires_at_unix"],
                fence["body"]["expires_at_unix"],
                request_body["transaction_valid_until_unix"])):
        raise ConformanceError("relay admission requested start boundary is invalid")


def validate_admission_receipt(signed: Any, admission_request: dict[str, Any],
                               execution: dict[str, Any]) -> None:
    require_keys(signed, {"body", "public_key", "signature"})
    body = signed["body"]
    required = {
        "schema_version", "owner_id", "agent_id", "authenticated_principal_id",
        "authority_id", "provider_agent_id", "service_profile_digest",
        "provider_quote_digest", "network_digest", "transaction_identity_digest",
        "mode", "assurance_level", "stage_mask", "route_attempt", "stable_action_id",
        "exact_request_digest", "relay_execution_request_digest",
        "authorized_action_digest", "writer_fence_digest", "writer_lease_id",
        "writer_generation", "policy_revision", "mandate_digest",
        "admission_sequence", "issued_at_unix", "start_not_after_unix",
    }
    require_keys(body, required, {"approval_digest", "predecessor_receipt_digest"})
    action = execution["authorized_action"]
    fence = execution["writer_fence"]
    expected_from_request = {
        name: admission_request[name] for name in (
            "schema_version", "owner_id", "agent_id", "authenticated_principal_id",
            "provider_agent_id", "service_profile_digest", "provider_quote_digest",
            "network_digest", "transaction_identity_digest", "mode", "assurance_level", "stage_mask",
            "route_attempt", "stable_action_id",
            "exact_request_digest", "relay_execution_request_digest")
    }
    if "predecessor_receipt_digest" in admission_request:
        expected_from_request["predecessor_receipt_digest"] = admission_request["predecessor_receipt_digest"]
    if any(body[name] != expected for name, expected in expected_from_request.items()):
        raise ConformanceError("relay admission receipt substituted its admitted request")
    if (not identifier(body["authority_id"]) or
            body["authority_id"] != action["authority_id"] or
            body["authority_id"] != fence["body"]["authority_id"] or
            signed["public_key"] != action["authority_public_key"] or
            signed["public_key"] != fence["public_key"]):
        raise ConformanceError("relay admission receipt authority is invalid")
    if (((body["route_attempt"] == 1) !=
         ("predecessor_receipt_digest" not in body)) or
            (body["mode"] != "relay_exact" and body["route_attempt"] != 1) or
            body["stage_mask"] != relay_stage_mask(body["mode"]) or
            body["authorized_action_digest"] != protocol_digest(
                "tos.authorized-action-envelope.v1", action) or
            body["writer_fence_digest"] != action["writer_fence_digest"] or
            body["writer_lease_id"] != fence["body"]["lease_id"] or
            body["writer_generation"] != action["writer_generation"] or
            body["writer_generation"] != fence["body"]["writer_generation"] or
            body["policy_revision"] != action["policy_revision"] or
            body["mandate_digest"] != action["mandate_digest"] or
            body.get("approval_digest") != action.get("approval_digest")):
        raise ConformanceError("relay admission receipt authority context mismatch")
    if (not positive_u64(body["admission_sequence"]) or
            not positive_u64(body["issued_at_unix"]) or
            not positive_u64(body["start_not_after_unix"]) or
            not body["issued_at_unix"] < body["start_not_after_unix"] or
            body["start_not_after_unix"] - body["issued_at_unix"] > 60 or
            body["start_not_after_unix"] != admission_request["requested_start_not_after_unix"]):
        raise ConformanceError("relay admission receipt sequence or start window is invalid")
    request_body = execution["quote_request"]["body"]
    quote_body = execution["provider_quote"]["body"]
    if (body["issued_at_unix"] < execution["created_at_unix"] or
            body["start_not_after_unix"] > min(
                execution["expires_at_unix"], execution["agreement_expires_at_unix"],
                quote_body["expires_at_unix"], action["expires_at_unix"],
                fence["body"]["expires_at_unix"],
                request_body["transaction_valid_until_unix"])):
        raise ConformanceError("relay admission receipt exceeds a signed prerequisite")
    message = signature_message(
        b"tos.agent-relay-side-effect-admission-receipt-signature.v1\x00", body)
    if not verify_ed25519(decode_public(signed["public_key"]), message,
                          decode_signature(signed["signature"])):
        raise ConformanceError("relay admission receipt signature is invalid")


def validate_stored_admission_receipt(signed: Any) -> None:
    """Validate a signed receipt without trusting a live execution object.

    This is the reference durable-load boundary. A later route-head verifier
    must first authenticate every stored receipt before comparing lineage.
    """
    require_keys(signed, {"body", "public_key", "signature"})
    body = signed["body"]
    required = {
        "schema_version", "owner_id", "agent_id", "authenticated_principal_id",
        "authority_id", "provider_agent_id", "service_profile_digest",
        "provider_quote_digest", "network_digest", "transaction_identity_digest",
        "mode", "assurance_level", "stage_mask", "route_attempt", "stable_action_id",
        "exact_request_digest", "relay_execution_request_digest",
        "authorized_action_digest", "writer_fence_digest", "writer_lease_id",
        "writer_generation", "policy_revision", "mandate_digest",
        "admission_sequence", "issued_at_unix", "start_not_after_unix",
    }
    require_keys(body, required, {"approval_digest", "predecessor_receipt_digest"})
    if (body["schema_version"] != 1 or
            any(not identifier(body[name]) for name in (
                "owner_id", "agent_id", "authenticated_principal_id",
                "authority_id", "provider_agent_id", "writer_lease_id")) or
            any(not digest(body[name]) for name in (
                "service_profile_digest", "provider_quote_digest", "network_digest",
                "transaction_identity_digest", "stable_action_id",
                "exact_request_digest", "relay_execution_request_digest",
                "authorized_action_digest", "writer_fence_digest", "mandate_digest")) or
            ("approval_digest" in body and not digest(body["approval_digest"])) or
            not integer(body["route_attempt"], 1, 32) or
            body["assurance_level"] not in ASSURANCE_LEVELS or
            (body["route_attempt"] > 1 and
             body["assurance_level"] != "autonomous-decentralized") or
            body["stage_mask"] != relay_stage_mask(body["mode"]) or
            (body["mode"] != "relay_exact" and body["route_attempt"] != 1) or
            ((body["route_attempt"] == 1) !=
             ("predecessor_receipt_digest" not in body)) or
            ("predecessor_receipt_digest" in body and
             not digest(body["predecessor_receipt_digest"])) or
            any(not positive_u64(body[name]) for name in (
                "writer_generation", "policy_revision", "admission_sequence",
                "issued_at_unix", "start_not_after_unix")) or
            not body["issued_at_unix"] < body["start_not_after_unix"] or
            body["start_not_after_unix"] - body["issued_at_unix"] > 60):
        raise ConformanceError("stored relay admission receipt is invalid")
    message = signature_message(
        b"tos.agent-relay-side-effect-admission-receipt-signature.v1\x00", body)
    if not verify_ed25519(decode_public(signed["public_key"]), message,
                          decode_signature(signed["signature"])):
        raise ConformanceError("stored relay admission receipt signature is invalid")


def validate_admission_route_chain(chain: Any) -> None:
    if not isinstance(chain, list) or not 1 <= len(chain) <= 32:
        raise ConformanceError("relay admission route chain length is invalid")
    for index, signed in enumerate(chain):
        validate_stored_admission_receipt(signed)
        body = signed["body"]
        if index == 0:
            if body["route_attempt"] != 1 or "predecessor_receipt_digest" in body:
                raise ConformanceError("relay admission route chain does not start at attempt one")
            continue
        predecessor = chain[index - 1]["body"]
        if (predecessor["mode"] != "relay_exact" or body["mode"] != "relay_exact" or
                body["route_attempt"] != predecessor["route_attempt"] + 1 or
                body["predecessor_receipt_digest"] != protocol_digest(
                    "tos.agent-relay-side-effect-admission-receipt.v1", predecessor)):
            raise ConformanceError("relay admission route chain lineage is invalid")
        immutable = (
            "owner_id", "agent_id", "authenticated_principal_id", "authority_id",
            "network_digest", "transaction_identity_digest", "assurance_level", "stable_action_id",
            "exact_request_digest", "policy_revision", "mandate_digest",
        )
        if (any(body[name] != predecessor[name] for name in immutable) or
                body.get("approval_digest") != predecessor.get("approval_digest") or
                body["provider_agent_id"] == predecessor["provider_agent_id"] or
                body["admission_sequence"] <= predecessor["admission_sequence"]):
            raise ConformanceError("relay admission route head changed immutable authority context")


def validate_execution(request: Any, profile: dict[str, Any], registry: dict[str, dict[str, Any]]) -> None:
    required = {"schema_version", "quote_request", "provider_quote", "agreement_body_digest", "agreement_expires_at_unix",
                "fee_obligation_ids", "signed_transaction_bytes", "underlying_action_request", "semantic_fields",
                "authorized_action", "writer_fence", "admission_receipt",
                "created_at_unix", "expires_at_unix"}
    optional = {"relay_obligation_id", "sponsorship_obligation_id"}
    require_keys(request, required, optional)
    validate_quote_request(request["quote_request"], profile)
    validate_provider_quote(request["provider_quote"], request["quote_request"], profile)
    body = request["quote_request"]["body"]
    if (not u16(request["schema_version"]) or request["schema_version"] != 1 or
            not digest(request["agreement_body_digest"]) or
            not positive_u64(request["agreement_expires_at_unix"]) or
            not positive_u64(request["created_at_unix"]) or
            not positive_u64(request["expires_at_unix"])):
        raise ConformanceError("execution Agreement digest is invalid")
    if (not 0 < request["created_at_unix"] < request["expires_at_unix"] <= request["agreement_expires_at_unix"] or
            request["created_at_unix"] < body["created_at_unix"] or
            request["created_at_unix"] < request["provider_quote"]["body"]["valid_from_unix"]):
        raise ConformanceError("execution lifetime is invalid")
    if request["expires_at_unix"] > request["provider_quote"]["body"]["expires_at_unix"] or request["expires_at_unix"] > body["transaction_valid_until_unix"]:
        raise ConformanceError("execution window exceeds a signed prerequisite")
    fees = request["fee_obligation_ids"]
    if (not isinstance(fees, list) or not 0 < len(fees) <= 2 or fees != sorted(set(fees)) or
            any(not identifier(item, 128) for item in fees) or
            len(fees) != len(request["provider_quote"]["body"]["fee_lines"])):
        raise ConformanceError("execution fee obligation set is invalid")
    mode = body["mode"]
    if mode == "relay_exact" and (not identifier(request.get("relay_obligation_id"), 128) or "sponsorship_obligation_id" in request):
        raise ConformanceError("relay-only execution obligation set is invalid")
    if mode == "sponsor_only" and ("relay_obligation_id" in request or not identifier(request.get("sponsorship_obligation_id"), 128)):
        raise ConformanceError("sponsor-only execution obligation set is invalid")
    if mode == "sponsor_and_relay" and (not identifier(request.get("relay_obligation_id"), 128) or not identifier(request.get("sponsorship_obligation_id"), 128)):
        raise ConformanceError("combined execution obligation set is invalid")
    signed_transaction = decode_base64(request["signed_transaction_bytes"], MAX_SIGNED_BYTES)
    transaction_profile = _find_profile(profile["transaction_profiles"], body["transaction_profile_uri"],
                                        body["transaction_profile_digest"])
    if (transaction_profile is None or len(signed_transaction) != body["signed_transaction_size"] or
            len(signed_transaction) > transaction_profile["maximum_signed_bytes"] or
            raw_digest(signed_transaction) != body["signed_transaction_digest"]):
        raise ConformanceError("Submit transaction bytes do not match the signed quote request")
    underlying = decode_base64(request["underlying_action_request"], MAX_ACTION_BYTES)
    fields = request["semantic_fields"]
    stable = derive_semantic_id(registry, body["underlying_action_kind"], fields)
    if stable != body["stable_action_id"] or exact_request_digest(underlying) != body["exact_request_digest"]:
        raise ConformanceError("execution underlying action identity mismatch")
    validate_writer_fence(request["writer_fence"])
    validate_authorized_action(request["authorized_action"], request["writer_fence"], fields, underlying, registry)
    action = request["authorized_action"]
    if action["action_kind"] != body["underlying_action_kind"] or action["stable_action_id"] != body["stable_action_id"] or action["exact_request_digest"] != body["exact_request_digest"] or action["agent_id"] != body["requester_agent_id"]:
        raise ConformanceError("execution does not bind quoted underlying action")
    if request["expires_at_unix"] > action["expires_at_unix"] or request["expires_at_unix"] > request["writer_fence"]["body"]["expires_at_unix"]:
        raise ConformanceError("execution exceeds action or fence lifetime")


def absence_reference_digest(reference: dict[str, Any]) -> str:
    validate_absence_reference_shape(reference)
    return protocol_digest("tos.agent-relay-absence-observation-reference.v1", reference)


def absence_proof_bundle_model(sponsorship: list[dict[str, Any]],
                               transaction: list[dict[str, Any]],
                               proof_profile_uri: str,
                               proof_profile_digest: str,
                               proof_payload_model: dict[str, Any]) -> dict[str, Any]:
    if sponsorship and transaction:
        scope = "dual"
    elif sponsorship:
        scope = "sponsorship_only"
    elif transaction:
        scope = "transaction_only"
    else:
        raise ConformanceError("absence proof bundle has no evidence scope")
    payload = canonical_cbor(proof_payload_model)
    if not payload or len(payload) > MAX_ABSENCE_PROOF_BUNDLE_BYTES:
        raise ConformanceError("absence proof payload exceeds 128 KiB")
    model: dict[str, Any] = {
        "schema_version": 1,
        "proof_scope": scope,
        "proof_profile_uri": proof_profile_uri,
        "proof_profile_digest": proof_profile_digest,
        "proof_payload_digest": protocol_digest_canonical(
            "tos.agent-relay-absence-proof-payload.v1", payload),
        "proof_payload": _b64(payload),
    }
    if sponsorship:
        model["sponsorship_absence_observations"] = copy.deepcopy(sponsorship)
    if transaction:
        model["transaction_absence_observations"] = copy.deepcopy(transaction)
    return model


def absence_proof_bundle_bytes(model: dict[str, Any]) -> bytes:
    encoded = canonical_cbor(model)
    if not encoded or len(encoded) > MAX_ABSENCE_PROOF_BUNDLE_BYTES:
        raise ConformanceError("absence proof bundle exceeds 128 KiB")
    return encoded


def attach_absence_proof_bundle(body: dict[str, Any],
                                sponsorship: list[dict[str, Any]],
                                transaction: list[dict[str, Any]],
                                proof_profile_uri: str,
                                proof_profile_digest: str,
                                proof_payload_model: dict[str, Any]) -> dict[str, Any]:
    model = absence_proof_bundle_model(
        sponsorship, transaction, proof_profile_uri, proof_profile_digest,
        proof_payload_model)
    encoded = absence_proof_bundle_bytes(model)
    body["absence_proof_bundle_digest"] = protocol_digest_canonical(
        "tos.agent-relay-absence-proof-bundle.v1", encoded)
    body["absence_proof_bundle"] = _b64(encoded)
    return model


def validate_absence_proof_bundle_model(value: Any,
                                        sponsorship: list[dict[str, Any]],
                                        transaction: list[dict[str, Any]]) -> None:
    required = {"schema_version", "proof_scope", "proof_profile_uri",
                "proof_profile_digest", "proof_payload_digest",
                "proof_payload"}
    optional = {"sponsorship_absence_observations",
                "transaction_absence_observations"}
    require_keys(value, required, optional)
    expected_scope = ("dual" if sponsorship and transaction else
                      "sponsorship_only" if sponsorship else
                      "transaction_only" if transaction else None)
    if (value["schema_version"] != 1 or value["proof_scope"] != expected_scope or
            not identifier(value["proof_profile_uri"], 256) or
            not digest(value["proof_profile_digest"]) or
            not digest(value["proof_payload_digest"]) or
            value.get("sponsorship_absence_observations") !=
            (sponsorship if sponsorship else None) or
            value.get("transaction_absence_observations") !=
            (transaction if transaction else None)):
        raise ConformanceError("absence proof bundle scope or arrays do not match")
    payload = decode_base64(value["proof_payload"],
                            MAX_ABSENCE_PROOF_BUNDLE_BYTES)
    decode_canonical_cbor(payload, MAX_ABSENCE_PROOF_BUNDLE_BYTES)
    if value["proof_payload_digest"] != protocol_digest_canonical(
            "tos.agent-relay-absence-proof-payload.v1", payload):
        raise ConformanceError("absence proof payload digest is invalid")
    expected_outer_digest = protocol_digest(
        "tos.agent-relay-absence-proof-profile.v1", {
            "schema_version": 1,
            "profile_uri": TOS_RPC_ABSENCE_PROFILE_URI,
            "independent_snapshot_query": True,
            "maximum_bundle_bytes": MAX_ABSENCE_PROOF_BUNDLE_BYTES,
            "chain_side_effect": False,
        })
    nested_profiles = {
        (reference["observation_evidence_profile_uri"],
         reference["observation_evidence_profile_digest"])
        for reference in sponsorship + transaction
    }
    if (value["proof_profile_uri"] != TOS_RPC_ABSENCE_PROFILE_URI or
            value["proof_profile_digest"] != expected_outer_digest or
            len(nested_profiles) != 1 or
            next(iter(nested_profiles))[0] != RPC_CORROBORATION_PROFILE_URI):
        raise ConformanceError(
            "absence verifier or nested observation profile is unknown, mixed, or substituted")
    absence_proof_bundle_bytes(value)


def validate_absence_proof_bundle(body: dict[str, Any],
                                  sponsorship: list[dict[str, Any]],
                                  transaction: list[dict[str, Any]]) -> None:
    has_absence = bool(sponsorship or transaction)
    has_bytes = "absence_proof_bundle" in body
    has_digest = "absence_proof_bundle_digest" in body
    if not has_absence:
        if has_bytes or has_digest:
            raise ConformanceError("absence proof bundle exists without absence evidence")
        return
    if not has_bytes or not has_digest:
        raise ConformanceError("absence proof bundle bytes or digest are missing")
    encoded = decode_base64(body["absence_proof_bundle"],
                            MAX_ABSENCE_PROOF_BUNDLE_BYTES)
    model = decode_canonical_cbor(encoded, MAX_ABSENCE_PROOF_BUNDLE_BYTES)
    validate_absence_proof_bundle_model(model, sponsorship, transaction)
    used_classes = {item["terminal_evidence_class"]
                    for item in sponsorship + transaction}
    if (model["proof_profile_uri"] != TOS_RPC_ABSENCE_PROFILE_URI or
            body["assurance_level"] == "autonomous-decentralized" or
            "validator_finality" in used_classes):
        raise ConformanceError(
            "stock TOS RPC absence proof is lower-assurance only")
    if body["absence_proof_bundle_digest"] != protocol_digest_canonical(
            "tos.agent-relay-absence-proof-bundle.v1", encoded):
        raise ConformanceError("absence proof bundle digest is invalid")


def validate_absence_reference_shape(reference: Any) -> None:
    required = {"schema_version", "observation_kind", "conclusion", "provider_agent_id", "network_digest",
                "relay_stable_action_id", "relay_exact_request_digest", "relay_execution_request_digest",
                "sponsorship_stable_action_id", "sponsorship_exact_request_digest", "sponsorship_valid_until_unix",
                "signed_transaction_digest",
                "signed_transaction_cell_hash", "terminal_profile_uri",
                "terminal_profile_digest", "terminal_evidence_class",
                "finalized_checkpoint_id", "finalized_checkpoint_sequence", "finalized_checkpoint_unix",
                "observer_id", "operator_domain_id",
                "observation_evidence_profile_uri", "observation_evidence_profile_digest", "observation_digest",
                "observed_at_unix"}
    require_keys(reference, required)
    if (not u16(reference["schema_version"]) or reference["schema_version"] != 1 or
            reference["observation_kind"] not in ABSENCE_KINDS or
            reference["conclusion"] not in ABSENCE_CONCLUSIONS or
            any(not digest(reference[name]) for name in (
                "network_digest", "relay_stable_action_id", "relay_exact_request_digest",
                "relay_execution_request_digest", "sponsorship_stable_action_id",
                "sponsorship_exact_request_digest", "signed_transaction_digest",
                "terminal_profile_digest",
                "observation_evidence_profile_digest", "observation_digest")) or
            reference["terminal_evidence_class"] not in
            (RELAY_TERMINAL_CLASSES | SPONSORSHIP_TERMINAL_CLASSES) or
            not positive_u64(reference["sponsorship_valid_until_unix"]) or
            not CELL_DIGEST.fullmatch(reference["signed_transaction_cell_hash"]) or
            any(not identifier(reference[name], 1024 if name == "finalized_checkpoint_id" else 256)
                for name in ("provider_agent_id", "terminal_profile_uri", "finalized_checkpoint_id", "observer_id",
                             "operator_domain_id", "observation_evidence_profile_uri")) or
            not positive_u64(reference["finalized_checkpoint_sequence"]) or
            not positive_u64(reference["finalized_checkpoint_unix"]) or
            not positive_u64(reference["observed_at_unix"])):
        raise ConformanceError("relay absence observation reference is invalid")
    if reference["finalized_checkpoint_unix"] > reference["observed_at_unix"] + 5 * 60:
        raise ConformanceError("relay absence checkpoint is implausibly newer than its observation")


def validate_absence_observations(sponsorship: Any, transaction: Any, body: dict[str, Any],
                                  execution: dict[str, Any]) -> list[str]:
    quote = execution["quote_request"]["body"]
    mode = quote["mode"]
    sponsorship_terminal = body.get("sponsorship_terminal_profile")
    relay_finality = body.get("relay_finality_profile")
    if (not isinstance(sponsorship, list) or not isinstance(transaction, list) or
            not sponsorship and not transaction or
            sponsorship_terminal is None or
            mode == "sponsor_and_relay" and relay_finality is None or
            mode not in {"sponsor_only", "sponsor_and_relay"} or
            transaction and mode != "sponsor_and_relay"):
        raise ConformanceError("relay absence profile matrix is invalid")
    network_digest = protocol_digest("tos.agent-relay-network-domain.v1", body["network"])
    expected_common = {
        "provider_agent_id": body["provider_agent_id"],
        "network_digest": network_digest,
        "relay_stable_action_id": body["stable_action_id"],
        "relay_exact_request_digest": body["exact_request_digest"],
        "relay_execution_request_digest": body["relay_execution_request_digest"],
        "sponsorship_stable_action_id": body["sponsorship_stable_action_id"],
        "sponsorship_exact_request_digest": body["sponsorship_exact_request_digest"],
        "sponsorship_valid_until_unix": body["sponsorship_valid_until_unix"],
        "signed_transaction_digest": body["signed_transaction_digest"],
        "signed_transaction_cell_hash": body["signed_transaction_cell_hash"],
    }
    if quote["stable_action_id"] != body["stable_action_id"]:
        raise ConformanceError("relay absence scenario does not bind the execution")
    expected_transaction_conclusion = {
        "finalized_absent": "absent",
        "finalized_expired": "expired_without_inclusion",
        "finalized_invalidated": "invalidated_without_inclusion",
        "corroborated_absent": "absent",
        "corroborated_expired": "expired_without_inclusion",
        "corroborated_invalidated": "invalidated_without_inclusion",
    }.get(body["outcome"])
    sponsorship_not_before = (
        body["sponsorship_valid_until_unix"] +
        sponsorship_terminal["reorg_window_seconds"])
    if not positive_u64(sponsorship_not_before):
        raise ConformanceError(
            "relay sponsorship absence terminal window overflows")
    transaction_not_before = None
    if transaction and expected_transaction_conclusion is None:
        expected_transaction_conclusion = transaction[0].get("conclusion") \
            if isinstance(transaction[0], dict) else None
    if transaction and expected_transaction_conclusion not in ABSENCE_CONCLUSIONS:
        raise ConformanceError("relay transaction-absence conclusion is invalid")
    if transaction and expected_transaction_conclusion != "invalidated_without_inclusion":
        transaction_not_before = (
            body["transaction_valid_until_unix"] +
            relay_finality["reorg_window_seconds"])
        if not positive_u64(transaction_not_before):
            raise ConformanceError(
                "relay client-transaction absence terminal window overflows")
    proof_sets: list[set[str]] = []
    wrapper_digests: list[str] = []
    sets = []
    if sponsorship:
        sets.append((sponsorship, "sponsorship_action",
                     "expired_without_inclusion", sponsorship_terminal,
                     sponsorship_not_before))
    if transaction:
        sets.append((transaction, "client_transaction",
                     expected_transaction_conclusion, relay_finality,
                     transaction_not_before))
    for values, kind, conclusion, terminal_profile, not_before in sets:
        if (conclusion is None or not isinstance(values, list) or
                not terminal_profile["minimum_observers"] <= len(values) <= 64):
            raise ConformanceError("relay absence observation threshold is incomplete")
        observers: set[str] = set()
        domains: set[str] = set()
        proofs: set[str] = set()
        digests: list[str] = []
        checkpoint: tuple[str, int, int] | None = None
        for reference in values:
            validate_absence_reference_shape(reference)
            if (reference["observation_kind"] != kind or reference["conclusion"] != conclusion or
                    any(reference[name] != expected for name, expected in expected_common.items()) or
                    reference["terminal_profile_uri"] != terminal_profile["profile_uri"] or
                    reference["terminal_profile_digest"] != terminal_profile["profile_digest"] or
                    reference["terminal_evidence_class"] !=
                    terminal_profile["terminal_evidence_class"] or
                    reference["observed_at_unix"] > body["observed_at_unix"] or
                    reference["observer_id"] in observers or reference["observation_digest"] in proofs):
                raise ConformanceError("relay absence observation conflicts with the exact action context")
            current_checkpoint = (
                reference["finalized_checkpoint_id"],
                reference["finalized_checkpoint_sequence"],
                reference["finalized_checkpoint_unix"])
            if checkpoint is None:
                checkpoint = current_checkpoint
            elif checkpoint != current_checkpoint:
                raise ConformanceError(
                    "relay absence observations disagree on their checkpoint")
            observers.add(reference["observer_id"])
            domains.add(reference["operator_domain_id"])
            proofs.add(reference["observation_digest"])
            digests.append(absence_reference_digest(reference))
        if (digests != sorted(set(digests)) or
                len(observers) < terminal_profile["minimum_observers"] or
                len(domains) < terminal_profile["minimum_operator_domains"] or
                not_before is not None and checkpoint[2] < not_before):
            raise ConformanceError("relay absence observation profile threshold is not met")
        proof_sets.append(proofs)
        wrapper_digests.extend(digests)
    if len(proof_sets) == 2 and proof_sets[0] & proof_sets[1]:
        raise ConformanceError("one observer proof was relabelled for both absent side effects")
    merged = sorted(set(wrapper_digests))
    if len(merged) != len(wrapper_digests) or len(merged) > 64:
        raise ConformanceError("relay absence observation set is too large or conflated")
    validate_absence_proof_bundle(body, sponsorship, transaction)
    return merged


def validate_evidence(signed: Any, execution: dict[str, Any], profile: dict[str, Any],
                      registry: dict[str, dict[str, Any]]) -> str:
    require_keys(signed, {"body", "public_key", "signature"})
    body = signed["body"]
    required = {"schema_version", "provider_agent_id", "network",
                "assurance_level", "stable_action_id", "exact_request_digest",
                "relay_execution_request_digest", "signed_transaction_digest",
                "signed_transaction_cell_hash", "transaction_valid_until_unix", "source_account",
                "source_sequence", "outcome", "observed_at_unix",
                "signing_authority_at_unix"}
    optional = {"sponsorship_stable_action_id", "sponsorship_exact_request_digest",
                "sponsorship_valid_until_unix", "sponsorship_transfer_reference",
                "sponsorship_transaction_evidence", "sponsorship_absence_observations",
                "transaction_absence_observations", "absence_proof_bundle_digest",
                "absence_proof_bundle", "submitted_transaction_hash", "source_execution_reference",
                "destination_credit_references", "relay_finality_profile",
                "sponsorship_terminal_profile", "relay_terminal_evidence_class",
                "relay_validator_authenticated_portable_proof",
                "relay_finalized_checkpoint_id",
                "relay_finalized_checkpoint_sequence",
                "relay_finalized_checkpoint_unix", "relay_confirmation_depth",
                "relay_observation_digests"}
    require_keys(body, required, optional)
    quote_body = execution["quote_request"]["body"]
    quote = execution["provider_quote"]["body"]
    mode = quote_body["mode"]
    relay_selected = mode in {"relay_exact", "sponsor_and_relay"}
    sponsorship_selected = mode in {"sponsor_only", "sponsor_and_relay"}
    if (not u16(body["schema_version"]) or body["schema_version"] != 1 or
            body["provider_agent_id"] != profile["provider_agent_id"] or
            body["network"] != quote_body["network"] or
            body["assurance_level"] != quote_body["assurance_level"]):
        raise ConformanceError("finality evidence provider or network mismatch")
    if body["stable_action_id"] != quote_body["stable_action_id"] or body["exact_request_digest"] != quote_body["exact_request_digest"]:
        raise ConformanceError("finality evidence underlying identity mismatch")
    if (body["relay_execution_request_digest"] != execution_digest(execution) or
            body["signed_transaction_digest"] != quote_body["signed_transaction_digest"] or
            body["signed_transaction_cell_hash"] != quote_body["signed_transaction_cell_hash"] or
            body["transaction_valid_until_unix"] !=
            quote_body["transaction_valid_until_unix"] or
            not positive_u64(body["transaction_valid_until_unix"])):
        raise ConformanceError("finality evidence execution or transaction mismatch")
    if not CELL_DIGEST.fullmatch(body["signed_transaction_cell_hash"]):
        raise ConformanceError("finality evidence cell hash is invalid")
    if body["source_account"] != quote_body["source_account"] or body["source_sequence"] != quote_body["source_sequence"]:
        raise ConformanceError("finality evidence source mismatch")
    if relay_selected != ("relay_finality_profile" in body) or \
            sponsorship_selected != ("sponsorship_terminal_profile" in body):
        raise ConformanceError("finality evidence profile matrix is invalid")
    if relay_selected:
        validate_finality(body["relay_finality_profile"])
        if body["relay_finality_profile"] != quote["relay_finality_profile"]:
            raise ConformanceError("relay finality profile mismatch")
        if (body["relay_finality_profile"]["terminal_evidence_class"] !=
                quote_body["relay_terminal_evidence_class"]):
            raise ConformanceError("relay finality profile class mismatch")
    if sponsorship_selected:
        validate_finality(body["sponsorship_terminal_profile"])
        if (body["sponsorship_terminal_profile"] !=
                quote["sponsorship_terminal_profile"]):
            raise ConformanceError("sponsorship terminal profile mismatch")
        if (body["sponsorship_terminal_profile"]["terminal_evidence_class"] !=
                quote_body["sponsorship_terminal_evidence_class"]):
            raise ConformanceError("sponsorship terminal profile class mismatch")

    relay_terminal_names = {
        "relay_terminal_evidence_class",
        "relay_validator_authenticated_portable_proof",
        "relay_finalized_checkpoint_id",
        "relay_finalized_checkpoint_sequence",
        "relay_finalized_checkpoint_unix",
        "relay_confirmation_depth",
        "relay_observation_digests",
    }
    has_relay_terminal = any(name in body for name in relay_terminal_names)
    if has_relay_terminal and any(
            name not in body for name in relay_terminal_names):
        raise ConformanceError("relay terminal evidence is incomplete")
    relay_success_names = {
        "submitted_transaction_hash", "source_execution_reference"}
    has_relay_success = any(name in body for name in relay_success_names)
    if has_relay_success and (not has_relay_terminal or any(
            name not in body for name in relay_success_names)):
        raise ConformanceError("relay success evidence is incomplete")
    relay_class = body.get("relay_terminal_evidence_class")
    if has_relay_terminal:
        if not relay_selected:
            raise ConformanceError(
                "relay terminal evidence exists without a selected relay profile")
        relay_profile = body["relay_finality_profile"]
        relay_observations = body["relay_observation_digests"]
        relay_authenticated = body[
            "relay_validator_authenticated_portable_proof"]
        if (not relay_selected or relay_class not in RELAY_TERMINAL_CLASSES or
                relay_class != quote_body["relay_terminal_evidence_class"] or
                not isinstance(relay_authenticated, bool) or
                (relay_class == "validator_finality") != relay_authenticated or
                body["assurance_level"] == "autonomous-decentralized" and
                relay_class != "validator_finality" or
                not isinstance(relay_observations, list) or
                relay_observations != sorted(set(relay_observations)) or
                len(relay_observations) < relay_profile["minimum_observers"] or
                len(relay_observations) > 64 or
                any(not digest(item) for item in relay_observations) or
                not u32(body["relay_confirmation_depth"]) or
                body["relay_confirmation_depth"] <
                relay_profile["minimum_confirmation_depth"] or
                not positive_u64(body["relay_finalized_checkpoint_sequence"]) or
                not identifier(body["relay_finalized_checkpoint_id"], 1024) or
                not positive_u64(body["relay_finalized_checkpoint_unix"]) or
                body["relay_finalized_checkpoint_unix"] >
                body["observed_at_unix"] + 5 * 60):
            raise ConformanceError("relay terminal evidence is invalid")
    if has_relay_success and (not identifier(
            body["submitted_transaction_hash"], 1024) or
            not identifier(body["source_execution_reference"], 1024)):
        raise ConformanceError("relay success reference is invalid")
    credits = body.get("destination_credit_references", [])
    if not isinstance(credits, list) or credits != sorted(set(credits)) or len(credits) > 64 or any(not digest(item) for item in credits):
        raise ConformanceError("destination credit set is invalid")
    if (not has_relay_success and "destination_credit_references" in body) or \
            (not u64(body["source_sequence"]) or
            not positive_u64(body["observed_at_unix"]) or
            not positive_u64(body["signing_authority_at_unix"]) or
            body["observed_at_unix"] > body["signing_authority_at_unix"] + 5 * 60):
        raise ConformanceError("finality checkpoint is invalid")
    if body["outcome"] not in OUTCOMES:
        raise ConformanceError("finality outcome is invalid")
    sponsorship_pair = (body.get("sponsorship_stable_action_id"), body.get("sponsorship_exact_request_digest"))
    has_sponsorship_identity = all(sponsorship_pair)
    if (any(sponsorship_pair) != has_sponsorship_identity or (has_sponsorship_identity and
            (not digest(sponsorship_pair[0]) or not digest(sponsorship_pair[1]))) or
            has_sponsorship_identity != positive_u64(body.get("sponsorship_valid_until_unix"))):
        raise ConformanceError("finality sponsorship action identity is invalid")
    sponsorship_absence = body.get("sponsorship_absence_observations", [])
    transaction_absence = body.get("transaction_absence_observations", [])
    has_sponsorship_absence = "sponsorship_absence_observations" in body
    has_transaction_absence = "transaction_absence_observations" in body
    has_absence = has_sponsorship_absence or has_transaction_absence
    has_transfer = bool(body.get("sponsorship_transfer_reference"))
    if body.get("sponsorship_transfer_reference") and not has_sponsorship_identity:
        raise ConformanceError("sponsorship transfer lacks its exact action identity")
    if has_transfer:
        if "sponsorship_transaction_evidence" not in body:
            raise ConformanceError("sponsorship transfer lacks exact transaction evidence")
        validate_sponsorship_transaction_evidence(
            body["sponsorship_transaction_evidence"], body, execution, registry)
    elif "sponsorship_transaction_evidence" in body:
        raise ConformanceError("sponsorship transaction evidence lacks a finalized transfer")
    if has_sponsorship_identity and not has_transfer and not has_sponsorship_absence:
        raise ConformanceError("sponsorship action identity lacks terminal evidence")
    if has_transfer and has_sponsorship_absence:
        raise ConformanceError("sponsorship evidence is both successful and absent")
    if has_absence:
        if not has_sponsorship_identity:
            raise ConformanceError("absence evidence lacks sponsorship identity")
        merged = validate_absence_observations(
            sponsorship_absence, transaction_absence, body, execution)
        if not merged:
            raise ConformanceError("relay absence evidence is empty")
    else:
        validate_absence_proof_bundle(body, [], [])

    negative_outcomes = {
        "finalized_expired", "finalized_absent", "finalized_invalidated",
        "corroborated_expired", "corroborated_absent",
        "corroborated_invalidated",
    }
    sponsorship_only_outcomes = {
        "finalized_sponsorship_only", "corroborated_sponsorship_only"}
    relay_only_outcomes = {"finalized_relay_only", "corroborated_relay_only"}

    def outcome_prefix(classes: list[str]) -> str:
        if not classes or any(item not in
                              (RELAY_TERMINAL_CLASSES |
                               SPONSORSHIP_TERMINAL_CLASSES)
                              for item in classes):
            raise ConformanceError("terminal evidence class set is invalid")
        return ("finalized_" if all(item == "validator_finality"
                                    for item in classes) else
                "corroborated_")

    sponsor_class = None
    if has_transfer:
        sponsor_class = body["sponsorship_transaction_evidence"][
            "terminal_evidence_class"]
    elif has_sponsorship_absence:
        sponsor_class = body["sponsorship_terminal_profile"][
            "terminal_evidence_class"]
    transaction_absence_class = (
        body["relay_finality_profile"]["terminal_evidence_class"]
        if has_transaction_absence else None)
    if mode == "relay_exact":
        if (has_sponsorship_identity or has_transfer or has_absence or
                "sponsorship_transaction_evidence" in body or
                body["outcome"] in {
                    "finalized_sponsorship_only",
                    "corroborated_sponsorship_only",
                    "finalized_relay_only",
                    "corroborated_relay_only",
                }):
            raise ConformanceError("relay-only evidence carries sponsorship state")
        if not has_relay_terminal:
            raise ConformanceError(
                "relay-only terminal evidence has no relay terminal result")
        expected_prefix = (
            "finalized_" if relay_class == "validator_finality" else
            "corroborated_")
        if has_relay_success:
            expected_outcome = (
                "finalized_success" if relay_class == "validator_finality" else
                "corroborated_success")
            if body["outcome"] != expected_outcome:
                raise ConformanceError(
                    "relay terminal success outcome does not match its evidence class")
        elif (body["outcome"] not in {
                "finalized_expired", "finalized_absent",
                "finalized_invalidated", "corroborated_expired",
                "corroborated_absent", "corroborated_invalidated"} or
              not body["outcome"].startswith(expected_prefix)):
            raise ConformanceError(
                "relay negative outcome does not match its terminal evidence class")
    elif mode == "sponsor_only":
        if (not has_sponsorship_identity or has_relay_terminal or
                has_relay_success or has_transaction_absence or credits):
            raise ConformanceError("sponsor-only evidence carries relay state")
        if has_transfer:
            expected = outcome_prefix([sponsor_class]) + "sponsorship_only"
        elif has_sponsorship_absence:
            expected = outcome_prefix([sponsor_class]) + "expired"
        else:
            raise ConformanceError("sponsor-only evidence has no terminal component")
        if body["outcome"] != expected:
            raise ConformanceError("sponsor-only outcome does not match evidence")
    elif mode == "sponsor_and_relay":
        if not has_sponsorship_identity:
            raise ConformanceError("combined evidence lacks sponsorship identity")
        if has_transfer and has_relay_success and not has_absence:
            expected = outcome_prefix([sponsor_class, relay_class]) + "success"
        elif (has_transfer and not has_relay_terminal and
              not has_relay_success and not has_sponsorship_absence):
            classes = [sponsor_class]
            if has_transaction_absence:
                classes.append(transaction_absence_class)
            expected = outcome_prefix(classes) + "sponsorship_only"
        elif (has_sponsorship_absence and has_relay_success and
              not has_transfer and not has_transaction_absence):
            expected = outcome_prefix([sponsor_class, relay_class]) + "relay_only"
        elif (has_sponsorship_absence and has_transaction_absence and
              not has_transfer and not has_relay_terminal and
              not has_relay_success and not credits):
            expected = outcome_prefix(
                [sponsor_class, transaction_absence_class]) + {
                    "absent": "absent",
                    "expired_without_inclusion": "expired",
                    "invalidated_without_inclusion": "invalidated",
                }[transaction_absence[0]["conclusion"]]
        else:
            raise ConformanceError("combined component evidence matrix is incomplete")
        if body["outcome"] != expected:
            raise ConformanceError("combined outcome does not match all used evidence classes")
        if (expected in sponsorship_only_outcomes and has_transaction_absence and
                body["outcome"] not in sponsorship_only_outcomes or
                expected in relay_only_outcomes and body["outcome"] not in
                relay_only_outcomes or
                expected in negative_outcomes and body["outcome"] not in
                negative_outcomes):
            raise ConformanceError("combined outcome family is invalid")

    message = signature_message(b"tos.agent-relay-finality-evidence-signature.v1\x00", body)
    if not verify_ed25519(decode_public(signed["public_key"]), message, decode_signature(signed["signature"])):
        raise ConformanceError("finality evidence signature is invalid")
    return protocol_digest("tos.agent-relay-finality-evidence.v1", body)


def terminal_evidence_references(body: dict[str, Any]) -> list[str]:
    values: list[str] = list(body.get("relay_observation_digests", []))
    sponsorship = body.get("sponsorship_transaction_evidence")
    if isinstance(sponsorship, dict):
        values.extend(sponsorship.get("observation_digests", []))
    for name in ("sponsorship_absence_observations",
                 "transaction_absence_observations"):
        values.extend(absence_reference_digest(item) for item in body.get(name, []))
    merged = sorted(set(values))
    if not merged or len(merged) != len(values) or len(merged) > 64:
        raise ConformanceError("terminal evidence reference set is invalid")
    return merged


def evidence_set_digest(values: list[str]) -> str:
    if not values or values != sorted(set(values)) or any(not digest(item) for item in values):
        raise ConformanceError("evidence reference set is invalid")
    return exact_request_digest(b"".join(item.encode("ascii") + b"\x00" for item in values))


def validate_sponsorship_credit_observation(
        value: Any, execution: dict[str, Any],
        registry: dict[str, dict[str, Any]]) -> None:
    required = {
        "schema_version", "network_digest", "agreement_payment_request",
        "agreement_payment_request_digest", "sponsorship_stable_action_id",
        "sponsorship_exact_request_digest", "provider_sponsor_source_account",
        "provider_sponsor_source_sequence", "provider_sponsor_valid_until_unix",
        "signed_top_up_transaction_digest", "signed_top_up_transaction_cell_hash",
        "sponsorship_payment_commitment_cell_hash",
        "destination_source_account", "amount", "submitted_transaction_hash",
        "source_execution_reference", "destination_credit_references",
        "evidence_profile_uri", "evidence_profile_digest", "observed_checkpoint_id",
        "observed_checkpoint_sequence", "observed_checkpoint_unix",
        "observation_digests", "observed_at_unix",
    }
    require_keys(value, required)
    request = execution["quote_request"]["body"]
    quote = execution["provider_quote"]["body"]
    payment_request = value["agreement_payment_request"]
    if (request["assurance_level"] == "autonomous-decentralized" or
            request.get("sponsorship_release_evidence_class") != "observed_unproven" or
            value["schema_version"] != 1 or
            any(not digest(value[name]) for name in (
                "network_digest", "agreement_payment_request_digest",
                "sponsorship_stable_action_id", "sponsorship_exact_request_digest",
                "signed_top_up_transaction_digest", "evidence_profile_digest")) or
            not CELL_DIGEST.fullmatch(value["signed_top_up_transaction_cell_hash"]) or
            not CELL_DIGEST.fullmatch(
                value["sponsorship_payment_commitment_cell_hash"]) or
            any(not identifier(value[name], limit) for name, limit in (
                ("provider_sponsor_source_account", 256),
                ("destination_source_account", 256),
                ("submitted_transaction_hash", 1024),
                ("source_execution_reference", 1024),
                ("observed_checkpoint_id", 1024))) or
            value["evidence_profile_uri"] != request.get("sponsorship_release_profile_uri") or
            value["evidence_profile_digest"] != request.get("sponsorship_release_profile_digest") or
            not u64(value["provider_sponsor_source_sequence"]) or
            any(not positive_u64(value[name]) for name in (
                "provider_sponsor_valid_until_unix", "observed_checkpoint_sequence",
                "observed_checkpoint_unix", "observed_at_unix")) or
            value["observed_checkpoint_unix"] > value["observed_at_unix"] + 5 * 60):
        raise ConformanceError("sponsorship credit observation shape is invalid")
    validate_amount(value["amount"], True)
    payment_bytes, _ = validate_domain_bound_payment_request(
        payment_request, request["network"], None, registry)
    for name in ("destination_credit_references", "observation_digests"):
        items = value[name]
        if (not isinstance(items, list) or not items or len(items) > 64 or
                items != sorted(set(items)) or any(not digest(item) for item in items)):
            raise ConformanceError("sponsorship credit observation set is invalid")
    expected_payment_amount = {
        "asset_namespace": quote["reserved_sponsorship"]["asset"]["asset_namespace"],
        "asset_identifier": quote["reserved_sponsorship"]["asset"]["asset_identifier"],
        "amount_atomic": quote["reserved_sponsorship"]["amount_atomic"],
        "unit": quote["reserved_sponsorship"]["asset"]["unit"],
    }
    if (value["network_digest"] != protocol_digest(
            "tos.agent-relay-network-domain.v1", request["network"]) or
            value["agreement_payment_request_digest"] != protocol_digest(
                "tos.agreement-payment-request.v1", payment_request) or
            payment_request["agreement_body_digest"] != execution["agreement_body_digest"] or
            payment_request["agreement_obligation_id"] != execution.get(
                "sponsorship_obligation_id") or
            payment_request["agent_id"] != quote["provider_agent_id"] or
            payment_request["payer_agent_id"] != quote["provider_agent_id"] or
            payment_request["payee_agent_id"] != request["requester_agent_id"] or
            payment_request["network_domain_digest"] != value["network_digest"] or
            payment_request["amount"] != expected_payment_amount or
            payment_request["destination"] != _b64(request["source_account"].encode()) or
            payment_request["settlement_adapter_uri"] != "tos.payment.direct.v1" or
            payment_request["stable_action_id"] != value["sponsorship_stable_action_id"] or
            payment_request["expires_at_unix"] != value["provider_sponsor_valid_until_unix"] or
            exact_request_digest(payment_bytes) != value["sponsorship_exact_request_digest"] or
            value["sponsorship_payment_commitment_cell_hash"] !=
            sponsorship_payment_commitment_cell_hash(
                value["agreement_payment_request_digest"],
                value["sponsorship_stable_action_id"]) or
            value["destination_source_account"] != request["source_account"] or
            value["amount"] != quote["reserved_sponsorship"]):
        raise ConformanceError("sponsorship credit observation changed its obligation")


def validate_sponsorship_transaction_evidence(
        value: Any, body: dict[str, Any], execution: dict[str, Any],
        registry: dict[str, dict[str, Any]]) -> None:
    required = {
        "schema_version", "terminal_evidence_class",
        "validator_authenticated_portable_proof", "network_digest",
        "agreement_payment_request",
        "agreement_payment_request_digest",
        "sponsorship_stable_action_id", "sponsorship_exact_request_digest",
        "provider_sponsor_source_account", "provider_sponsor_source_sequence",
        "provider_sponsor_valid_until_unix", "signed_top_up_transaction_digest",
        "signed_top_up_transaction_cell_hash",
        "sponsorship_payment_commitment_cell_hash", "destination_source_account",
        "amount", "submitted_transaction_hash", "source_execution_reference",
        "destination_credit_references", "finalized_checkpoint_id",
        "finalized_checkpoint_sequence", "finalized_checkpoint_unix",
        "confirmation_depth", "sponsorship_terminal_profile_digest",
        "observation_digests", "proof_bundle_digest",
        "observed_at_unix",
    }
    require_keys(value, required, {"proof_bundle", "portable_proof_locator"})
    request = execution["quote_request"]["body"]
    quote = execution["provider_quote"]["body"]
    payment_request = value["agreement_payment_request"]
    terminal_class = value["terminal_evidence_class"]
    authenticated_portable = value["validator_authenticated_portable_proof"]
    if (not u16(value["schema_version"]) or value["schema_version"] != 1 or
            terminal_class not in SPONSORSHIP_TERMINAL_CLASSES or
            not isinstance(authenticated_portable, bool) or
            (terminal_class == "validator_finality") != authenticated_portable or
            any(not digest(value[name]) for name in (
                "network_digest", "agreement_payment_request_digest",
                "sponsorship_stable_action_id", "sponsorship_exact_request_digest",
                "signed_top_up_transaction_digest",
                "sponsorship_terminal_profile_digest",
                "proof_bundle_digest")) or
            not CELL_DIGEST.fullmatch(value["signed_top_up_transaction_cell_hash"]) or
            not CELL_DIGEST.fullmatch(
                value["sponsorship_payment_commitment_cell_hash"]) or
            any(not identifier(value[name], limit) for name, limit in (
                ("provider_sponsor_source_account", 256),
                ("destination_source_account", 256),
                ("submitted_transaction_hash", 1024),
                ("source_execution_reference", 1024),
                ("finalized_checkpoint_id", 1024))) or
            ("portable_proof_locator" in value and
             not identifier(value["portable_proof_locator"], 1024)) or
            not u64(value["provider_sponsor_source_sequence"]) or
            not u32(value["confirmation_depth"]) or value["confirmation_depth"] == 0 or
            any(not positive_u64(value[name]) for name in (
                "provider_sponsor_valid_until_unix", "finalized_checkpoint_sequence",
                "finalized_checkpoint_unix", "observed_at_unix"))):
        raise ConformanceError("sponsorship transaction evidence shape is invalid")
    validate_amount(value["amount"], True)
    if "proof_bundle" not in value and "portable_proof_locator" not in value:
        raise ConformanceError("sponsorship transaction evidence has no retrievable proof bundle")
    if "proof_bundle" in value:
        proof_bundle = decode_base64(
            value["proof_bundle"], MAX_SPONSORSHIP_PROOF_BUNDLE_BYTES)
        if protocol_digest_canonical(
                "tos.agent-relay-sponsorship-proof-bundle.v1", proof_bundle) != \
                value["proof_bundle_digest"]:
            raise ConformanceError("sponsorship proof bundle digest was substituted")
    payment_bytes, _ = validate_domain_bound_payment_request(
        payment_request, request["network"], None, registry)
    for name in ("destination_credit_references", "observation_digests"):
        items = value[name]
        if (not isinstance(items, list) or not items or len(items) > 64 or
                items != sorted(set(items)) or any(not digest(item) for item in items)):
            raise ConformanceError("sponsorship transaction evidence set is invalid")
    expected_payment_amount = {
        "asset_namespace": quote["reserved_sponsorship"]["asset"]["asset_namespace"],
        "asset_identifier": quote["reserved_sponsorship"]["asset"]["asset_identifier"],
        "amount_atomic": quote["reserved_sponsorship"]["amount_atomic"],
        "unit": quote["reserved_sponsorship"]["asset"]["unit"],
    }
    if (value["network_digest"] != protocol_digest(
            "tos.agent-relay-network-domain.v1", request["network"]) or
            value["agreement_payment_request_digest"] != protocol_digest(
                "tos.agreement-payment-request.v1", payment_request) or
            payment_request["agreement_body_digest"] != execution["agreement_body_digest"] or
            payment_request["agreement_obligation_id"] != execution.get(
                "sponsorship_obligation_id") or
            payment_request["agent_id"] != quote["provider_agent_id"] or
            payment_request["payer_agent_id"] != quote["provider_agent_id"] or
            payment_request["payee_agent_id"] != request["requester_agent_id"] or
            payment_request["network_id"] != request["network"]["network_id"] or
            payment_request["network_domain_digest"] != value["network_digest"] or
            payment_request["amount"] != expected_payment_amount or
            payment_request["destination"] != _b64(request["source_account"].encode()) or
            payment_request["settlement_adapter_uri"] != "tos.payment.direct.v1" or
            payment_request["stable_action_id"] != value["sponsorship_stable_action_id"] or
            payment_request["expires_at_unix"] != value["provider_sponsor_valid_until_unix"] or
            exact_request_digest(payment_bytes) != value["sponsorship_exact_request_digest"] or
            value["sponsorship_payment_commitment_cell_hash"] !=
            sponsorship_payment_commitment_cell_hash(
                value["agreement_payment_request_digest"],
                value["sponsorship_stable_action_id"]) or
            value["sponsorship_stable_action_id"] != body["sponsorship_stable_action_id"] or
            value["sponsorship_exact_request_digest"] != body["sponsorship_exact_request_digest"] or
            value["provider_sponsor_valid_until_unix"] != body["sponsorship_valid_until_unix"] or
            value["destination_source_account"] != request["source_account"] or
            value["amount"] != quote.get("reserved_sponsorship") or
            value["submitted_transaction_hash"] != body["sponsorship_transfer_reference"] or
            value["sponsorship_terminal_profile_digest"] !=
            quote["sponsorship_terminal_profile"]["profile_digest"] or
            value["confirmation_depth"] <
            quote["sponsorship_terminal_profile"]["minimum_confirmation_depth"] or
            value["finalized_checkpoint_unix"] > value["observed_at_unix"] + 5 * 60):
        raise ConformanceError("sponsorship transaction evidence changed its signed obligation")
    release_class = request.get("sponsorship_release_evidence_class")
    if terminal_class != request.get("sponsorship_terminal_evidence_class"):
        raise ConformanceError(
            "sponsorship terminal evidence class was substituted")
    if terminal_class == "client_corroborated":
        if (body["assurance_level"] == "autonomous-decentralized" or
                release_class != "observed_unproven" or
                request.get("sponsorship_release_profile_uri") !=
                RPC_CORROBORATION_PROFILE_URI or
                body["sponsorship_terminal_profile"]["profile_uri"] !=
                CLIENT_CORROBORATED_TERMINAL_PROFILE_URI):
            raise ConformanceError(
                "client-corroborated terminal evidence changed its selected policy")
    elif (release_class != "validator_finality" or
          "portable_proof_locator" not in value):
        raise ConformanceError(
            "validator-finality sponsorship evidence is not portable or selected")


def validate_resolution(signed: Any, execution: dict[str, Any],
                        evidence: dict[str, Any]) -> None:
    require_keys(signed, {"body", "public_key", "signature"})
    body = signed["body"]
    required = {"schema_version", "provider_agent_id", "network", "assurance_level", "stable_action_id", "exact_request_digest",
                "relay_execution_request_digest", "state", "state_revision", "observed_at_unix", "expires_at_unix"}
    optional = {"terminal_outcome", "transaction_reference", "sponsorship_stable_action_id",
                "sponsorship_exact_request_digest", "sponsorship_valid_until_unix",
                "sponsorship_transfer_reference", "evidence_set_digest"}
    require_keys(body, required, optional)
    request = execution["quote_request"]["body"]
    if (not u16(body["schema_version"]) or body["schema_version"] != 1 or
            body["provider_agent_id"] != request["provider_agent_id"] or
            body["network"] != request["network"] or
            body["assurance_level"] != request["assurance_level"]):
        raise ConformanceError("resolution provider is invalid")
    if body["stable_action_id"] != request["stable_action_id"] or body["exact_request_digest"] != request["exact_request_digest"] or body["relay_execution_request_digest"] != execution_digest(execution):
        raise ConformanceError("resolution action binding mismatch")
    if (body["state"] not in STATES or not positive_u64(body["state_revision"]) or
            not positive_u64(body["observed_at_unix"]) or not positive_u64(body["expires_at_unix"]) or
            not body["observed_at_unix"] < body["expires_at_unix"] or
            body["expires_at_unix"] - body["observed_at_unix"] > 86400):
        raise ConformanceError("resolution state or lifetime is invalid")
    if body["state"] == "terminal":
        expected_reference = (
            evidence.get("sponsorship_transfer_reference")
            if evidence.get("outcome") in {
                "finalized_sponsorship_only",
                "corroborated_sponsorship_only",
            } else evidence.get("submitted_transaction_hash")
            if evidence.get("outcome") in {
                "finalized_success", "corroborated_success",
                "finalized_relay_only", "corroborated_relay_only",
            } else None)
        if body.get("terminal_outcome") not in OUTCOMES or \
                body.get("terminal_outcome") != evidence.get("outcome") or \
                body.get("evidence_set_digest") != evidence_set_digest(
                    terminal_evidence_references(evidence)) or \
                body.get("transaction_reference") != expected_reference:
            raise ConformanceError("terminal resolution lacks exact evidence")
    elif "terminal_outcome" in body or "evidence_set_digest" in body:
        raise ConformanceError("nonterminal resolution carries terminal evidence")
    pair = (body.get("sponsorship_stable_action_id"), body.get("sponsorship_exact_request_digest"))
    if any(pair) != all(pair) or (all(pair) and (not digest(pair[0]) or not digest(pair[1]))) or \
            all(pair) != positive_u64(body.get("sponsorship_valid_until_unix")) or (
            body.get("sponsorship_transfer_reference") and not all(pair)):
        raise ConformanceError("resolution sponsorship action identity is invalid")
    for name in ("sponsorship_stable_action_id", "sponsorship_exact_request_digest", "sponsorship_valid_until_unix",
                 "sponsorship_transfer_reference"):
        if body.get(name) != evidence.get(name):
            raise ConformanceError("resolution substituted finality evidence sponsorship identity")
    message = signature_message(b"tos.agent-relay-resolution-signature.v1\x00", body)
    if not verify_ed25519(decode_public(signed["public_key"]), message, decode_signature(signed["signature"])):
        raise ConformanceError("resolution signature is invalid")


def validate_observed_unproven_resolution(
        signed: Any, execution: dict[str, Any], observation: dict[str, Any]) -> None:
    require_keys(signed, {"body", "public_key", "signature"})
    body = signed["body"]
    required = {
        "schema_version", "provider_agent_id", "network", "assurance_level",
        "stable_action_id", "exact_request_digest", "relay_execution_request_digest",
        "state", "state_revision", "sponsorship_stable_action_id",
        "sponsorship_exact_request_digest", "sponsorship_valid_until_unix",
        "sponsorship_status", "sponsorship_observation_digest",
        "observed_at_unix", "expires_at_unix",
    }
    require_keys(body, required)
    request = execution["quote_request"]["body"]
    if (body["schema_version"] != 1 or
            body["provider_agent_id"] != request["provider_agent_id"] or
            body["network"] != request["network"] or
            body["assurance_level"] != request["assurance_level"] or
            body["assurance_level"] == "autonomous-decentralized" or
            body["stable_action_id"] != request["stable_action_id"] or
            body["exact_request_digest"] != request["exact_request_digest"] or
            body["relay_execution_request_digest"] != execution_digest(execution) or
            body["state"] not in {"prepared", "submitted", "accepted"} or
            not positive_u64(body["state_revision"]) or
            body["sponsorship_status"] != "observed_unproven" or
            body["sponsorship_observation_digest"] != protocol_digest(
                "tos.agent-relay-sponsorship-credit-observation.v1", observation) or
            body["sponsorship_stable_action_id"] != observation["sponsorship_stable_action_id"] or
            body["sponsorship_exact_request_digest"] != observation["sponsorship_exact_request_digest"] or
            body["sponsorship_valid_until_unix"] != observation["provider_sponsor_valid_until_unix"] or
            body["observed_at_unix"] != observation["observed_at_unix"] or
            not body["observed_at_unix"] < body["expires_at_unix"] or
            body["expires_at_unix"] - body["observed_at_unix"] > 86400):
        raise ConformanceError("observed-unproven resolution is invalid")
    message = signature_message(b"tos.agent-relay-resolution-signature.v1\x00", body)
    if not verify_ed25519(decode_public(signed["public_key"]), message,
                          decode_signature(signed["signature"])):
        raise ConformanceError("observed-unproven resolution signature is invalid")


def validate_bundle(models: dict[str, Any], registry: dict[str, dict[str, Any]]) -> None:
    validate_profile(models["go_service_profile"])
    validate_quote_request(models["go_signed_quote_request"], models["go_service_profile"])
    validate_provider_quote(models["go_signed_provider_quote"],
                            models["go_signed_quote_request"],
                            models["go_service_profile"])
    profile = models["service_profile"]
    request = models["signed_quote_request"]
    quote = models["signed_provider_quote"]
    execution = models["execution_request"]
    validate_profile(profile)
    validate_network_order_fixture(models["negative_network_order"])
    validate_quote_request(request, profile)
    validate_provider_quote(quote, request, profile)
    if models["transaction_identity"] != transaction_identity(request["body"]):
        raise ConformanceError("transaction identity projection was substituted")
    validate_agreement_binding(models["agreement_binding"], request, quote, profile)
    validate_execution(execution, profile, registry)
    validate_admission_request(models["admission_request"], execution)
    validate_admission_receipt(models["signed_admission_receipt"],
                               models["admission_request"], execution)
    validate_admission_route_chain([models["signed_admission_receipt"]])
    if execution["admission_receipt"] != models["signed_admission_receipt"]:
        raise ConformanceError("execution substituted its admission receipt")
    payment_bytes, _ = validate_domain_bound_payment_request(
        models["underlying_payment_request"], request["body"]["network"],
        execution["semantic_fields"], registry)
    if payment_bytes != decode_base64(execution["underlying_action_request"], MAX_ACTION_BYTES):
        raise ConformanceError("execution does not carry the exact domain-bound payment request")
    sponsorship_bytes, sponsorship_fields = validate_domain_bound_payment_request(
        models["sponsorship_payment_request"], request["body"]["network"], None, registry)
    sponsorship = models["signed_finality_evidence"]["body"]
    sponsorship_transaction = sponsorship.get("sponsorship_transaction_evidence")
    if not isinstance(sponsorship_transaction, dict):
        raise ConformanceError(
            "finality evidence lacks structured sponsorship evidence")
    if (derive_semantic_id(registry, "payment.direct", sponsorship_fields) !=
            sponsorship["sponsorship_stable_action_id"] or
            exact_request_digest(sponsorship_bytes) != sponsorship["sponsorship_exact_request_digest"] or
            sponsorship_transaction.get("agreement_payment_request_digest") !=
            protocol_digest("tos.agreement-payment-request.v1",
                            models["sponsorship_payment_request"])):
        raise ConformanceError("finality evidence substituted the sponsorship payment identity")
    changed_genesis = copy.deepcopy(request["body"]["network"])
    changed_genesis["zero_state_root_hash"] = _repeated("f")
    for name, fields in (("underlying_payment_request", execution["semantic_fields"]),
                         ("sponsorship_payment_request", sponsorship_fields)):
        try:
            validate_domain_bound_payment_request(models[name], changed_genesis, fields, registry)
        except ConformanceError:
            continue
        raise ConformanceError(f"{name} replayed across a different genesis")
    expected_call_result = {
        "quote_call": {"request": request},
        "quote_result": {"quote": quote},
        "resolve_admission_call": admission_lookup(
            models["signed_admission_receipt"]["body"]),
        "resolve_admission_result": {"receipt": models["signed_admission_receipt"]},
        "submit_result": {"resolution": models["signed_resolution"]},
        "resolve_call": {"stable_action_id": execution["authorized_action"]["stable_action_id"],
                         "exact_request_digest": execution["authorized_action"]["exact_request_digest"]},
        "resolve_result": {"resolution": models["signed_resolution"]},
        "evidence_call": {"stable_action_id": execution["authorized_action"]["stable_action_id"],
                          "exact_request_digest": execution["authorized_action"]["exact_request_digest"]},
        "evidence_result": {"evidence": models["signed_finality_evidence"]},
    }
    for name, expected in expected_call_result.items():
        if models[name] != expected:
            raise ConformanceError(f"{name} substituted its embedded protocol object")
    if models["submit_call"]["request"] != execution:
        raise ConformanceError("SubmitCall substituted the relay execution request")
    validate_submit_call(models["submit_call"], profile, registry, models["agreement_binding"])
    validate_sponsorship_credit_observation(
        models["sponsorship_credit_observation"], execution, registry)
    validate_observed_unproven_resolution(
        models["signed_observed_unproven_resolution"], execution,
        models["sponsorship_credit_observation"])
    validate_evidence(models["signed_finality_evidence"], execution, profile, registry)
    validate_resolution(models["signed_resolution"], execution,
                        models["signed_finality_evidence"]["body"])
    validate_evidence(
        models["signed_combined_partial_corroborated_evidence"],
        execution, profile, registry)
    validate_resolution(
        models["signed_combined_partial_corroborated_resolution"],
        execution,
        models["signed_combined_partial_corroborated_evidence"]["body"])
    validate_absence_proof_bundle_model(
        models["post_submit_sponsorship_only_absence_proof_bundle"], [],
        models["transaction_absence_observations"])
    validate_evidence(
        models["signed_post_submit_sponsorship_only_evidence"], execution,
        profile, registry)
    validate_resolution(
        models["signed_post_submit_sponsorship_only_resolution"], execution,
        models["signed_post_submit_sponsorship_only_evidence"]["body"])
    validate_absence_proof_bundle_model(
        models["relay_only_absence_proof_bundle"],
        models["sponsorship_absence_observations"], [])
    validate_evidence(models["signed_relay_only_evidence"], execution,
                      profile, registry)
    validate_resolution(models["signed_relay_only_resolution"], execution,
                        models["signed_relay_only_evidence"]["body"])
    if models["sponsorship_absence_observations"] != models["signed_absence_finality_evidence"]["body"]["sponsorship_absence_observations"] or \
            models["transaction_absence_observations"] != models["signed_absence_finality_evidence"]["body"]["transaction_absence_observations"]:
        raise ConformanceError("typed absence vector objects were substituted")
    for prefix in ("sponsorship", "transaction"):
        expected_references = models[f"{prefix}_absence_observations"]
        actual_references = [models[f"{prefix}_absence_observation_{index + 1}"]
                             for index in range(len(expected_references))]
        if actual_references != expected_references:
            raise ConformanceError("typed absence digest vector was substituted")
    validate_evidence(models["signed_absence_finality_evidence"], execution, profile, registry)
    validate_absence_proof_bundle_model(
        models["dual_absence_proof_bundle"],
        models["sponsorship_absence_observations"],
        models["transaction_absence_observations"])
    validate_resolution(models["signed_absence_resolution"], execution,
                        models["signed_absence_finality_evidence"]["body"])
    validate_evidence(
        models["signed_invalidated_absence_finality_evidence"],
        execution, profile, registry)
    validate_absence_proof_bundle_model(
        models["invalidated_dual_absence_proof_bundle"],
        models["sponsorship_absence_observations"],
        models["signed_invalidated_absence_finality_evidence"]["body"]
        ["transaction_absence_observations"])


def _repeated(character: str) -> str:
    return "sha256:" + character * 64


def _b64(value: bytes) -> str:
    return base64.b64encode(value).decode()


def _signed(body: dict[str, Any], seed: bytes, domain: bytes, proof_name: str = "signature") -> dict[str, Any]:
    return {
        "body": copy.deepcopy(body),
        "public_key": encode_public(seed),
        proof_name: encode_signature(seed, signature_message(domain, body)),
    }


def verify_route_chain_mutations(base: dict[str, Any], authority_seed: bytes) -> None:
    domain = b"tos.agent-relay-side-effect-admission-receipt-signature.v1\x00"
    first_body = copy.deepcopy(base["body"])
    first_body["mode"] = "relay_exact"
    first_body["assurance_level"] = "autonomous-decentralized"
    first_body["stage_mask"] = ["broadcast"]
    first_body["route_attempt"] = 1
    first_body.pop("predecessor_receipt_digest", None)
    first_body["approval_digest"] = _repeated("b")
    first = _signed(first_body, authority_seed, domain)

    successor_body = copy.deepcopy(first_body)
    successor_body["provider_agent_id"] = "agent:provider-successor"
    successor_body["service_profile_digest"] = _repeated("1")
    successor_body["provider_quote_digest"] = _repeated("2")
    successor_body["relay_execution_request_digest"] = _repeated("3")
    successor_body["authorized_action_digest"] = _repeated("4")
    successor_body["writer_fence_digest"] = _repeated("5")
    successor_body["writer_lease_id"] = "lease:successor"
    successor_body["writer_generation"] += 1
    successor_body["route_attempt"] = 2
    successor_body["predecessor_receipt_digest"] = protocol_digest(
        "tos.agent-relay-side-effect-admission-receipt.v1", first_body)
    successor_body["admission_sequence"] += 1
    successor = _signed(successor_body, authority_seed, domain)
    validate_admission_route_chain([first, successor])

    mutations = {
        "policy_revision": successor_body["policy_revision"] + 1,
        "mandate_digest": _repeated("9"),
        "approval_digest": _repeated("d"),
        "authority_id": "authority:other",
    }
    for name, replacement in mutations.items():
        mutated_body = copy.deepcopy(successor_body)
        mutated_body[name] = replacement
        mutated = _signed(mutated_body, authority_seed, domain)
        try:
            validate_admission_route_chain([first, mutated])
        except ConformanceError:
            continue
        raise ConformanceError(
            f"persisted route-head mutation {name} unexpectedly passed")


def _semantic_fields(registry: dict[str, dict[str, Any]], action_kind: str,
                     values: dict[str, Any]) -> list[dict[str, Any]]:
    fields: list[dict[str, Any]] = []
    for definition in registry[action_kind]["ordered_semantic_fields"]:
        name, field_type = definition["field_name"], definition["field_type"]
        field: dict[str, Any] = {"name": name, "type": field_type}
        field["number" if field_type == "u64" else "text"] = values[name]
        fields.append(field)
    return fields


def _domain_bound_payment_request(registry: dict[str, dict[str, Any]], network: dict[str, Any],
                                  *, owner_id: str, agent_id: str,
                                  agreement_body_digest: str, agreement_obligation_id: str,
                                  obligation_instance_id: str, payer_agent_id: str,
                                  payee_agent_id: str, amount: dict[str, Any],
                                  destination: bytes, expires_at_unix: int) -> tuple[
                                      dict[str, Any], list[dict[str, Any]], bytes]:
    network_domain_digest = protocol_digest("tos.agent-relay-network-domain.v1", network)
    asset_digest = protocol_digest("tos.agreement-payment-asset.v1", {
        "namespace": amount["asset_namespace"],
        "identifier": amount["asset_identifier"],
        "unit": amount["unit"],
    })
    destination_digest = protocol_digest("tos.agreement-payment-destination.v1", {
        "network_id": network["network_id"],
        "network_domain_digest": network_domain_digest,
        "adapter_uri": "tos.payment.direct.v1",
        "destination": _b64(destination),
    })
    fields = _semantic_fields(registry, "payment.direct", {
        "owner_id": owner_id,
        "agent_id": agent_id,
        "agreement_body_digest": agreement_body_digest,
        "obligation_instance_id": obligation_instance_id,
        "payer_id": payer_agent_id,
        "payee_id": payee_agent_id,
        "network_id": network["network_id"],
        "asset_digest": asset_digest,
        "amount_atomic": amount["amount_atomic"],
        "destination_digest": destination_digest,
    })
    request = {
        "schema_version": 3,
        "owner_id": owner_id,
        "agent_id": agent_id,
        "agreement_body_digest": agreement_body_digest,
        "agreement_obligation_id": agreement_obligation_id,
        "obligation_instance_id": obligation_instance_id,
        "payer_agent_id": payer_agent_id,
        "payee_agent_id": payee_agent_id,
        "network_id": network["network_id"],
        "network_domain_digest": network_domain_digest,
        "amount": copy.deepcopy(amount),
        "destination": _b64(destination),
        "settlement_adapter_uri": "tos.payment.direct.v1",
        "stable_action_id": derive_semantic_id(registry, "payment.direct", fields),
        "expires_at_unix": expires_at_unix,
    }
    encoded, checked_fields = validate_domain_bound_payment_request(request, network, fields, registry)
    if checked_fields != fields:
        raise ConformanceError("constructed domain-bound payment fields changed during validation")
    return request, fields, encoded


def _object(name: str, object_type: str, model: Any, domain: str | None = None,
            projection: Any | None = None) -> dict[str, Any]:
    item: dict[str, Any] = {
        "name": name,
        "object_type": object_type,
        "json_model": copy.deepcopy(model),
        "canonical_cbor_base64": _b64(bounded_canonical_cbor(model)),
    }
    if domain is not None:
        digest_model = model if projection is None else projection
        item["digest_domain"] = domain
        if projection is not None:
            item["digest_projection"] = copy.deepcopy(projection)
            item["digest_projection_cbor_base64"] = _b64(bounded_canonical_cbor(projection))
        item["digest"] = protocol_digest(domain, digest_model)
    return item


def build_vectors(registry: dict[str, dict[str, Any]]) -> dict[str, Any]:
    now = 1_800_000_000
    client_seed = b"1" * 32
    provider_seed = b"2" * 32
    authority_seed = b"3" * 32
    published_commitment_request_digest = "sha256:" + "11" * 32
    published_commitment_action_id = "sha256:" + "22" * 32
    published_commitment_representation = \
        sponsorship_payment_commitment_cell_representation(
            published_commitment_request_digest,
            published_commitment_action_id)
    published_commitment_hash = sponsorship_payment_commitment_cell_hash(
        published_commitment_request_digest, published_commitment_action_id)
    if published_commitment_hash != \
            PUBLISHED_SPONSORSHIP_PAYMENT_COMMITMENT_CELL_HASH:
        raise ConformanceError("published SPN1 cell-hash vector drifted")
    network = {
        "network_id": "tos:testnet",
        "global_id": 42,
        "zero_state_root_hash": _repeated("1"),
        "zero_state_file_hash": _repeated("2"),
        "workchain_id": 0,
    }
    rpc_corroboration_profile_descriptor = {
        "profile_uri": RPC_CORROBORATION_PROFILE_URI,
        "network_domain": copy.deepcopy(network),
        "members": [
            {"endpoint": "https://rpc-a.example/jsonRPC",
             "operator_provenance": _repeated("a")},
            {"endpoint": "https://rpc-b.example/jsonRPC",
             "operator_provenance": _repeated("b")},
            {"endpoint": "https://rpc-c.example/jsonRPC",
             "operator_provenance": _repeated("c")},
        ],
        "threshold": 2,
        "maximum_history_transactions": 1000,
        "strict_majority": True,
        "exact_submitted_message": True,
        "exact_destination_credit": True,
        "validator_finality_proven": False,
    }
    rpc_profile_json, rpc_profile_digest = tosctl_framed_json_digest(
        b"tosctl.agreement-payment-rpc-corroboration-profile.v1\x00",
        rpc_corroboration_profile_descriptor)
    absence_profile_descriptor = {
        "schema_version": 1,
        "profile_uri": TOS_RPC_ABSENCE_PROFILE_URI,
        "independent_snapshot_query": True,
        "maximum_bundle_bytes": MAX_ABSENCE_PROOF_BUNDLE_BYTES,
        "chain_side_effect": False,
    }
    absence_profile_digest = protocol_digest(
        "tos.agent-relay-absence-proof-profile.v1",
        absence_profile_descriptor)
    negative_network_order = [
        {
            "network_id": "tos:negative-order",
            "global_id": -2,
            "zero_state_root_hash": _repeated("1"),
            "zero_state_file_hash": _repeated("2"),
            "workchain_id": -2,
        },
        {
            "network_id": "tos:negative-order",
            "global_id": -2,
            "zero_state_root_hash": _repeated("1"),
            "zero_state_file_hash": _repeated("2"),
            "workchain_id": -1,
        },
        {
            "network_id": "tos:negative-order",
            "global_id": -1,
            "zero_state_root_hash": _repeated("1"),
            "zero_state_file_hash": _repeated("2"),
            "workchain_id": -2,
        },
    ]
    transaction_profile = {
        "profile_uri": "tos.signed-external-boc.v1",
        "profile_digest": _repeated("3"),
        "maximum_signed_bytes": 65536,
        "inspectable_source_sequence": True,
        "inspectable_transaction_expiry": True,
    }
    validator_finality = {
        "profile_uri": "tos.depth-quorum.v1",
        "profile_digest": _repeated("4"),
        "terminal_evidence_class": "validator_finality",
        "minimum_confirmation_depth": 2,
        "minimum_observers": 3,
        "minimum_operator_domains": 2,
        "reorg_window_seconds": 10,
        "maximum_resolution_seconds": 30,
    }
    relay_finality = {
        "profile_uri": PROVIDER_CORROBORATED_RELAY_PROFILE_URI,
        "profile_digest": _repeated("d"),
        "terminal_evidence_class": "provider_corroborated",
        "minimum_confirmation_depth": 2,
        "minimum_observers": 3,
        "minimum_operator_domains": 2,
        "reorg_window_seconds": 10,
        "maximum_resolution_seconds": 30,
    }
    sponsorship_terminal = {
        "profile_uri": CLIENT_CORROBORATED_TERMINAL_PROFILE_URI,
        "profile_digest": _repeated("f"),
        "terminal_evidence_class": "client_corroborated",
        "minimum_confirmation_depth": 2,
        "minimum_observers": 3,
        "minimum_operator_domains": 2,
        "reorg_window_seconds": 10,
        "maximum_resolution_seconds": 30,
    }
    asset = {"asset_namespace": "tos.native", "asset_identifier": "tos:testnet", "unit": "nanotos"}
    profile = {
        "schema_version": 1,
        "profile_id": "relay:provider",
        "revision": 1,
        "provider_agent_id": "agent:provider",
        "network_domains": [network],
        "supported_modes": ["relay_exact", "sponsor_and_relay"],
        "supported_assurance_levels": [
            "authorized-single-provider",
            "autonomous-decentralized",
            "trusted-local",
        ],
        "transaction_profiles": [transaction_profile],
        "finality_profiles": [validator_finality, relay_finality,
                              sponsorship_terminal],
        "fee_assets": [asset],
        "exposure_limits": [{"asset": asset, "maximum_per_request_atomic": "1000", "maximum_outstanding_atomic": "10000"}],
        "maximum_request_bytes": 65536,
        "admission_limits": {
            "maximum_quote_reservations": 64,
            "maximum_active_executions": 32,
            "maximum_active_per_requester": 8,
            "maximum_quote_requests_per_window": 256,
            "maximum_quote_requests_per_requester_window": 32,
            "quote_request_window_seconds": 60,
        },
        "endpoints": {
            "quote_url": "https://relay.example/quote",
            "submit_url": "https://relay.example/submit",
            "resolve_url": "https://relay.example/resolve",
            "evidence_url": "https://relay.example/evidence",
        },
        "policy_revision": 1,
        "created_at_unix": now - 60,
        "expires_at_unix": now + 3600,
    }
    signed_transaction = b"exact signed TOS BOC fixture"
    underlying_payment_request, semantic_fields, underlying_request = _domain_bound_payment_request(
        registry, network,
        owner_id="owner:client",
        agent_id="agent:client",
        agreement_body_digest=_repeated("5"),
        agreement_obligation_id="obligation:underlying-payment",
        obligation_instance_id=_repeated("6"),
        payer_agent_id="agent:client",
        payee_agent_id="agent:merchant",
        amount={
            "asset_namespace": asset["asset_namespace"],
            "asset_identifier": asset["asset_identifier"],
            "amount_atomic": "25",
            "unit": asset["unit"],
        },
        destination=("0:" + "2" * 64).encode(),
        expires_at_unix=now + 480,
    )
    stable_id = underlying_payment_request["stable_action_id"]
    request_body = {
        "schema_version": 1,
        "request_id": "relay-request:one",
        "requester_agent_id": "agent:client",
        "provider_agent_id": "agent:provider",
        "network": network,
        "mode": "sponsor_and_relay",
        "assurance_level": "authorized-single-provider",
        "source_account": "0:" + "1" * 64,
        "source_account_authority_digest": _repeated("0"),
        "transaction_profile_uri": transaction_profile["profile_uri"],
        "transaction_profile_digest": transaction_profile["profile_digest"],
        "underlying_action_kind": "payment.direct",
        "stable_action_id": stable_id,
        "exact_request_digest": exact_request_digest(underlying_request),
        "signed_transaction_digest": raw_digest(signed_transaction),
        "signed_transaction_cell_hash": "tvm-cell-sha256:" + "d" * 64,
        "signed_transaction_size": len(signed_transaction),
        "transaction_intent_digest": _repeated("e"),
        "source_sequence": 7,
        "transaction_valid_until_unix": now + 600,
        "requested_sponsorship": {"asset": asset, "amount_atomic": "50"},
        "sponsorship_release_evidence_class": "observed_unproven",
        "sponsorship_release_profile_uri": RPC_CORROBORATION_PROFILE_URI,
        "sponsorship_release_profile_digest": _repeated("c"),
        "relay_terminal_evidence_class": "provider_corroborated",
        "sponsorship_terminal_evidence_class": "client_corroborated",
        "maximum_service_fee": {"asset": asset, "amount_atomic": "10"},
        "maximum_network_fee_atomic": "100",
        "maximum_transaction_value_atomic": "25",
        "relay_finality_profile_uri": relay_finality["profile_uri"],
        "relay_finality_profile_digest": relay_finality["profile_digest"],
        "sponsorship_terminal_profile_uri":
            sponsorship_terminal["profile_uri"],
        "sponsorship_terminal_profile_digest":
            sponsorship_terminal["profile_digest"],
        "created_at_unix": now,
        "expires_at_unix": now + 300,
    }
    transaction_identity_body = transaction_identity(request_body)
    transaction_identity_digest = protocol_digest(
        "tos.agent-relay-transaction-identity.v1", transaction_identity_body)
    signed_request = _signed(request_body, client_seed, b"tos.agent-relay-quote-request-signature.v1\x00")
    quote_body = {
        "schema_version": 1,
        "quote_id": "relay-quote:one",
        "quote_request_digest": protocol_digest("tos.agent-relay-quote-request.v1", request_body),
        "service_profile_digest": protocol_digest("tos.agent-relay-service-profile.v1", profile),
        "provider_agent_id": "agent:provider",
        "mode": "sponsor_and_relay",
        "assurance_level": "authorized-single-provider",
        "fee_lines": [
            {"kind": "gas_sponsorship_fee", "amount": {"asset": asset, "amount_atomic": "2"}},
            {"kind": "transaction_relay_fee", "amount": {"asset": asset, "amount_atomic": "3"}},
        ],
        "reserved_sponsorship": {"asset": asset, "amount_atomic": "50"},
        "sponsorship_release_evidence_class": request_body["sponsorship_release_evidence_class"],
        "sponsorship_release_profile_uri": request_body["sponsorship_release_profile_uri"],
        "sponsorship_release_profile_digest": request_body["sponsorship_release_profile_digest"],
        "relay_terminal_evidence_class":
            request_body["relay_terminal_evidence_class"],
        "sponsorship_terminal_evidence_class":
            request_body["sponsorship_terminal_evidence_class"],
        "maximum_network_fee_atomic": "100",
        "maximum_transaction_value_atomic": "25",
        "maximum_request_bytes": 65536,
        "relay_finality_profile": relay_finality,
        "sponsorship_terminal_profile": sponsorship_terminal,
        "status_endpoint": profile["endpoints"]["resolve_url"],
        "provider_policy_revision": 1,
        "valid_from_unix": now,
        "expires_at_unix": now + 240,
    }
    signed_quote = _signed(quote_body, provider_seed, b"tos.agent-relay-provider-quote-signature.v1\x00")

    # This compact relay_exact/autonomous fixture mirrors the independently
    # implemented Go conformance fixture. The fuller sponsor-and-relay fixture
    # below remains the lifecycle and negative-mutation corpus.
    go_profile = copy.deepcopy(profile)
    go_profile["supported_modes"] = ["relay_exact"]
    go_profile["supported_assurance_levels"] = ["autonomous-decentralized"]
    go_profile["finality_profiles"] = [validator_finality]
    go_underlying_request = bytes([0xA1, 0x01, 0x02])
    go_semantic_fields = _semantic_fields(registry, "payment.direct", {
        "owner_id": "owner:client",
        "agent_id": "agent:client",
        "agreement_body_digest": _repeated("5"),
        "obligation_instance_id": _repeated("6"),
        "payer_id": "agent:client",
        "payee_id": "agent:merchant",
        "network_id": "tos:testnet",
        "asset_digest": _repeated("a"),
        "amount_atomic": "25",
        "destination_digest": _repeated("b"),
    })
    go_request_body = copy.deepcopy(request_body)
    go_request_body["mode"] = "relay_exact"
    go_request_body["assurance_level"] = "autonomous-decentralized"
    go_request_body.pop("requested_sponsorship")
    go_request_body.pop("sponsorship_release_evidence_class")
    go_request_body.pop("sponsorship_release_profile_uri")
    go_request_body.pop("sponsorship_release_profile_digest")
    go_request_body.pop("sponsorship_terminal_evidence_class")
    go_request_body.pop("sponsorship_terminal_profile_uri")
    go_request_body.pop("sponsorship_terminal_profile_digest")
    go_request_body["relay_terminal_evidence_class"] = "validator_finality"
    go_request_body["relay_finality_profile_uri"] = validator_finality["profile_uri"]
    go_request_body["relay_finality_profile_digest"] = validator_finality["profile_digest"]
    go_request_body["stable_action_id"] = derive_semantic_id(
        registry, "payment.direct", go_semantic_fields)
    go_request_body["exact_request_digest"] = exact_request_digest(
        go_underlying_request)
    go_signed_request = _signed(
        go_request_body, client_seed,
        b"tos.agent-relay-quote-request-signature.v1\x00")
    go_quote_body = copy.deepcopy(quote_body)
    go_quote_body["quote_request_digest"] = protocol_digest(
        "tos.agent-relay-quote-request.v1", go_request_body)
    go_quote_body["service_profile_digest"] = protocol_digest(
        "tos.agent-relay-service-profile.v1", go_profile)
    go_quote_body["mode"] = "relay_exact"
    go_quote_body["assurance_level"] = "autonomous-decentralized"
    go_quote_body["fee_lines"] = [
        {"kind": "transaction_relay_fee",
         "amount": {"asset": asset, "amount_atomic": "3"}},
    ]
    go_quote_body.pop("reserved_sponsorship")
    go_quote_body.pop("sponsorship_release_evidence_class")
    go_quote_body.pop("sponsorship_release_profile_uri")
    go_quote_body.pop("sponsorship_release_profile_digest")
    go_quote_body.pop("sponsorship_terminal_evidence_class")
    go_quote_body.pop("sponsorship_terminal_profile")
    go_quote_body["relay_terminal_evidence_class"] = "validator_finality"
    go_quote_body["relay_finality_profile"] = validator_finality
    go_signed_quote = _signed(
        go_quote_body, provider_seed,
        b"tos.agent-relay-provider-quote-signature.v1\x00")
    agreement_binding = {
        "schema_version": 1,
        "quote_request_digest": quote_body["quote_request_digest"],
        "provider_quote_digest": protocol_digest("tos.agent-relay-provider-quote.v1", quote_body),
        "service_profile_digest": quote_body["service_profile_digest"],
        "mode": "sponsor_and_relay",
        "assurance_level": "authorized-single-provider",
        "sponsorship_release_evidence_class": request_body["sponsorship_release_evidence_class"],
        "sponsorship_release_profile_uri": request_body["sponsorship_release_profile_uri"],
        "sponsorship_release_profile_digest": request_body["sponsorship_release_profile_digest"],
        "relay_terminal_evidence_class":
            request_body["relay_terminal_evidence_class"],
        "sponsorship_terminal_evidence_class":
            request_body["sponsorship_terminal_evidence_class"],
        "relay_finality_profile_uri":
            request_body["relay_finality_profile_uri"],
        "relay_finality_profile_digest":
            request_body["relay_finality_profile_digest"],
        "sponsorship_terminal_profile_uri":
            request_body["sponsorship_terminal_profile_uri"],
        "sponsorship_terminal_profile_digest":
            request_body["sponsorship_terminal_profile_digest"],
        "requester_agent_id": "agent:client",
        "provider_agent_id": "agent:provider",
        "stable_action_id": stable_id,
        "exact_request_digest": request_body["exact_request_digest"],
        "signed_transaction_digest": request_body["signed_transaction_digest"],
    }
    binding_bytes = bounded_canonical_cbor(agreement_binding)
    binding_b64 = _b64(binding_bytes)
    amount_50 = {"asset_namespace": asset["asset_namespace"], "asset_identifier": asset["asset_identifier"],
                 "amount_atomic": "50", "unit": asset["unit"]}
    amount_2 = {"asset_namespace": asset["asset_namespace"], "asset_identifier": asset["asset_identifier"],
                "amount_atomic": "2", "unit": asset["unit"]}
    amount_3 = {"asset_namespace": asset["asset_namespace"], "asset_identifier": asset["asset_identifier"],
                "amount_atomic": "3", "unit": asset["unit"]}
    client_subject = {"subject_kind": "agent", "subject_namespace": "tos.agent",
                      "subject_identifier": "agent:client"}
    provider_subject = {"subject_kind": "agent", "subject_namespace": "tos.agent",
                        "subject_identifier": "agent:provider"}

    def obligation(obligation_id: str, kind: str, obligor: str, beneficiary: str,
                   predicate_id: str, amount: dict[str, Any] | None = None) -> dict[str, Any]:
        result: dict[str, Any] = {
            "obligation_id": obligation_id,
            "kind": kind,
            "obligor_agent_id": obligor,
            "beneficiary_agent_id": beneficiary,
            "subject_content_type": AGREEMENT_BINDING_CONTENT_TYPE,
            "subject": binding_b64,
            "confidentiality_and_disclosure_policy": "participants",
            "cancellation_policy": "before-start",
            "dispute_policy": "evidence",
            "authorization_predicate_ids": [predicate_id],
        }
        if amount is not None:
            result["amount"] = amount
            result["settlement_adapter_uri"] = "tos.payment.direct.v1"
            result["settlement_parameters"] = _b64(b"\xa0")
        return result

    agreement_body = {
        "schema_version": 1,
        "agreement_id": "agreement:relay-service:one",
        "version": 1,
        "network_context": "tos:testnet",
        "participants": [
            {"agent_id": "agent:client", "roles": ["client"]},
            {"agent_id": "agent:provider", "roles": ["provider"]},
        ],
        "terms_content_type": AGREEMENT_BINDING_CONTENT_TYPE,
        "terms": binding_b64,
        "obligations": [
            obligation("obligation:relay", "transaction_relay", "agent:provider", "agent:client",
                       "provider-delivery"),
            obligation("obligation:relay-fee", "transaction_relay_fee", "agent:client", "agent:provider",
                       "client-fees", amount_3),
            obligation("obligation:sponsorship", "gas_sponsorship", "agent:provider", "agent:client",
                       "provider-delivery", amount_50),
            obligation("obligation:sponsorship-fee", "gas_sponsorship_fee", "agent:client", "agent:provider",
                       "client-fees", amount_2),
        ],
        "authorization_predicates": [
            {
                "predicate_id": "client-fees",
                "authority_subject": client_subject,
                "role_scope": ["client"],
                "obligation_ids": ["obligation:relay-fee", "obligation:sponsorship-fee"],
                "evidence_profile_uri": AGENT_SIGNATURE_PROFILE_URI,
                "evidence_profile_version": 1,
                "evidence_profile_digest": AGENT_SIGNATURE_PROFILE_DIGEST,
                "evidence_target_projection_digest": "",
                "expires_at_unix": now + 420,
            },
            {
                "predicate_id": "provider-delivery",
                "authority_subject": provider_subject,
                "role_scope": ["provider"],
                "obligation_ids": ["obligation:relay", "obligation:sponsorship"],
                "evidence_profile_uri": AGENT_SIGNATURE_PROFILE_URI,
                "evidence_profile_version": 1,
                "evidence_profile_digest": AGENT_SIGNATURE_PROFILE_DIGEST,
                "evidence_target_projection_digest": "",
                "expires_at_unix": now + 420,
            },
        ],
        "valid_from_unix": now,
        "expires_at_unix": now + 420,
    }
    agreement_body = prepare_agreement_targets(agreement_body)
    agreement_body_digest = protocol_digest("tos.agent-agreement-body.v1", agreement_body)

    def acceptance_evidence(subject: dict[str, Any], role: str, predicate_ids: list[str], seed: bytes) -> dict[str, Any]:
        predicate_by_id = {item["predicate_id"]: item for item in agreement_body["authorization_predicates"]}
        targets = [predicate_by_id[predicate_id]["evidence_target_projection_digest"] for predicate_id in predicate_ids]
        acceptance_body = {
            "agreement_id": agreement_body["agreement_id"],
            "agreement_version": agreement_body["version"],
            "agreement_body_digest": agreement_body_digest,
            "accepting_subject": subject,
            "accepted_roles": [role],
            "predicate_ids": predicate_ids,
            "evidence_target_projection_digests": targets,
            "expires_at_unix": now + 400,
        }
        signed_acceptance = _signed(acceptance_body, seed, b"tos.agreement-acceptance-signature.v1\x00")
        return {
            "agreement_id": agreement_body["agreement_id"],
            "agreement_version": agreement_body["version"],
            "agreement_body_digest": agreement_body_digest,
            "authority_subject": subject,
            "predicate_ids": predicate_ids,
            "evidence_profile_uri": AGENT_SIGNATURE_PROFILE_URI,
            "evidence_profile_version": 1,
            "evidence_profile_digest": AGENT_SIGNATURE_PROFILE_DIGEST,
            "evidence_target_projection_digests": targets,
            "evidence_content_type": AGREEMENT_ACCEPTANCE_CONTENT_TYPE,
            "evidence": _b64(bounded_canonical_cbor(signed_acceptance)),
        }

    agreement = {
        "body": agreement_body,
        "authorization_evidence": [
            acceptance_evidence(client_subject, "client", ["client-fees"], client_seed),
            acceptance_evidence(provider_subject, "provider", ["provider-delivery"], provider_seed),
        ],
    }
    fence_body = {
        "schema_version": 1,
        "owner_id": "owner:client",
        "agent_id": "agent:client",
        "instance_id": "instance:client",
        "lease_id": "lease:client",
        "writer_generation": 1,
        "issued_at_unix": now - 60,
        "expires_at_unix": now + 600,
        "authority_id": "authority:client",
        "scope": ["payment.direct"],
    }
    fence = _signed(fence_body, authority_seed, b"tos.writer-fence.v1\x00", "fence_proof")
    authorized_action = {
        "schema_version": 1,
        "owner_id": "owner:client",
        "agent_id": "agent:client",
        "action_kind": "payment.direct",
        "stable_action_id": stable_id,
        "exact_request_digest": request_body["exact_request_digest"],
        "writer_generation": 1,
        "writer_fence_digest": protocol_digest("tos.writer-fence-envelope.v1", fence),
        "policy_revision": 1,
        "mandate_digest": _repeated("c"),
        "expected_prior_state": "unknown",
        "expires_at_unix": now + 480,
        "authority_id": "authority:client",
        "authority_public_key": fence["public_key"],
        "authorization_proof": "",
    }
    authorized_action["authorization_proof"] = encode_signature(
        authority_seed,
        signature_message(b"tos.authorized-action-proof.v1\x00", authorized_action),
    )
    execution = {
        "schema_version": 1,
        "quote_request": signed_request,
        "provider_quote": signed_quote,
        "agreement_body_digest": agreement_body_digest,
        "agreement_expires_at_unix": now + 420,
        "relay_obligation_id": "obligation:relay",
        "sponsorship_obligation_id": "obligation:sponsorship",
        "fee_obligation_ids": ["obligation:relay-fee", "obligation:sponsorship-fee"],
        "signed_transaction_bytes": _b64(signed_transaction),
        "underlying_action_request": _b64(underlying_request),
        "semantic_fields": semantic_fields,
        "authorized_action": authorized_action,
        "writer_fence": fence,
        "created_at_unix": now,
        "expires_at_unix": now + 180,
    }
    relay_execution_digest = execution_digest(execution)
    admission_request = {
        "schema_version": 1,
        "owner_id": authorized_action["owner_id"],
        "agent_id": authorized_action["agent_id"],
        "authenticated_principal_id": "principal:openfox-client",
        "provider_agent_id": quote_body["provider_agent_id"],
        "service_profile_digest": quote_body["service_profile_digest"],
        "provider_quote_digest": protocol_digest(
            "tos.agent-relay-provider-quote.v1", quote_body),
        "network_digest": protocol_digest(
            "tos.agent-relay-network-domain.v1", network),
        "transaction_identity_digest": transaction_identity_digest,
        "mode": request_body["mode"],
        "assurance_level": request_body["assurance_level"],
        "stage_mask": relay_stage_mask(request_body["mode"]),
        "route_attempt": 1,
        "stable_action_id": authorized_action["stable_action_id"],
        "exact_request_digest": authorized_action["exact_request_digest"],
        "relay_execution_request_digest": relay_execution_digest,
        "authorized_action": authorized_action,
        "writer_fence": fence,
        "underlying_action_request": execution["underlying_action_request"],
        "semantic_fields": execution["semantic_fields"],
        "requested_start_not_after_unix": now + 30,
    }
    admission_receipt_body = {
        "schema_version": 1,
        "owner_id": admission_request["owner_id"],
        "agent_id": admission_request["agent_id"],
        "authenticated_principal_id": admission_request["authenticated_principal_id"],
        "authority_id": authorized_action["authority_id"],
        "provider_agent_id": admission_request["provider_agent_id"],
        "service_profile_digest": admission_request["service_profile_digest"],
        "provider_quote_digest": admission_request["provider_quote_digest"],
        "network_digest": admission_request["network_digest"],
        "transaction_identity_digest": admission_request["transaction_identity_digest"],
        "mode": admission_request["mode"],
        "assurance_level": admission_request["assurance_level"],
        "stage_mask": admission_request["stage_mask"],
        "route_attempt": admission_request["route_attempt"],
        "stable_action_id": admission_request["stable_action_id"],
        "exact_request_digest": admission_request["exact_request_digest"],
        "relay_execution_request_digest": relay_execution_digest,
        "authorized_action_digest": protocol_digest(
            "tos.authorized-action-envelope.v1", authorized_action),
        "writer_fence_digest": authorized_action["writer_fence_digest"],
        "writer_lease_id": fence_body["lease_id"],
        "writer_generation": fence_body["writer_generation"],
        "policy_revision": authorized_action["policy_revision"],
        "mandate_digest": authorized_action["mandate_digest"],
        "admission_sequence": 1,
        "issued_at_unix": now,
        "start_not_after_unix": admission_request["requested_start_not_after_unix"],
    }
    signed_admission_receipt = _signed(
        admission_receipt_body, authority_seed,
        b"tos.agent-relay-side-effect-admission-receipt-signature.v1\x00")
    execution["admission_receipt"] = signed_admission_receipt
    resolve_admission_call = admission_lookup(admission_receipt_body)
    resolve_admission_result = {"receipt": signed_admission_receipt}
    submit_call = {"request": execution, "agreement": agreement}
    sponsorship_valid_until_unix = now + 100
    sponsorship_payment_request, sponsorship_semantic_fields, sponsorship_action_request = \
        _domain_bound_payment_request(
            registry, network,
            owner_id="owner:provider",
            agent_id="agent:provider",
            agreement_body_digest=agreement_body_digest,
            agreement_obligation_id="obligation:sponsorship",
            obligation_instance_id=_repeated("1"),
            payer_agent_id="agent:provider",
            payee_agent_id="agent:client",
            amount=amount_50,
            destination=request_body["source_account"].encode(),
            expires_at_unix=sponsorship_valid_until_unix,
        )
    sponsorship_stable_action_id = sponsorship_payment_request["stable_action_id"]
    sponsorship_exact_request_digest = exact_request_digest(sponsorship_action_request)
    sponsorship_payment_request_digest = protocol_digest(
        "tos.agreement-payment-request.v1", sponsorship_payment_request)
    sponsorship_payment_commitment_hash = \
        sponsorship_payment_commitment_cell_hash(
            sponsorship_payment_request_digest, sponsorship_stable_action_id)
    old_agreement_payment_request = copy.deepcopy(sponsorship_payment_request)
    old_agreement_payment_request["agreement_body_digest"] = _repeated("0")
    old_agreement_payment_request_digest = protocol_digest(
        "tos.agreement-payment-request.v1", old_agreement_payment_request)
    old_agreement_commitment_hash = sponsorship_payment_commitment_cell_hash(
        old_agreement_payment_request_digest, sponsorship_stable_action_id)
    sponsorship_proof_bundle_model = {
        "schema": "tos.agent-relay-sponsorship-proof-bundle.v1",
        "terminal_evidence_class": "client_corroborated",
        "validator_authenticated_portable_proof": False,
        "agreement_payment_request_digest": sponsorship_payment_request_digest,
        "sponsorship_stable_action_id": sponsorship_stable_action_id,
        "sponsorship_payment_commitment_cell_hash":
            sponsorship_payment_commitment_hash,
        "observation_digests": [_repeated("6"), _repeated("7"), _repeated("8")],
    }
    sponsorship_proof_bundle = bounded_canonical_cbor(sponsorship_proof_bundle_model)
    sponsorship_proof_bundle_digest = protocol_digest_canonical(
        "tos.agent-relay-sponsorship-proof-bundle.v1", sponsorship_proof_bundle)
    evidence_body = {
        "schema_version": 1,
        "provider_agent_id": "agent:provider",
        "network": network,
        "assurance_level": request_body["assurance_level"],
        "stable_action_id": stable_id,
        "exact_request_digest": request_body["exact_request_digest"],
        "relay_execution_request_digest": relay_execution_digest,
        "signed_transaction_digest": request_body["signed_transaction_digest"],
        "signed_transaction_cell_hash": request_body["signed_transaction_cell_hash"],
        "transaction_valid_until_unix":
            request_body["transaction_valid_until_unix"],
        "source_account": request_body["source_account"],
        "source_sequence": 7,
        "sponsorship_stable_action_id": sponsorship_stable_action_id,
        "sponsorship_exact_request_digest": sponsorship_exact_request_digest,
        "sponsorship_valid_until_unix": sponsorship_valid_until_unix,
        "sponsorship_transfer_reference": "sponsorship:exact",
        "sponsorship_transaction_evidence": {
            "schema_version": 1,
            "terminal_evidence_class": "client_corroborated",
            "validator_authenticated_portable_proof": False,
            "network_digest": protocol_digest(
                "tos.agent-relay-network-domain.v1", network),
            "agreement_payment_request": copy.deepcopy(sponsorship_payment_request),
            "agreement_payment_request_digest": sponsorship_payment_request_digest,
            "sponsorship_stable_action_id": sponsorship_stable_action_id,
            "sponsorship_exact_request_digest": sponsorship_exact_request_digest,
            "provider_sponsor_source_account": "0:" + "3" * 64,
            "provider_sponsor_source_sequence": 11,
            "provider_sponsor_valid_until_unix": sponsorship_valid_until_unix,
            "signed_top_up_transaction_digest": _repeated("a"),
            "signed_top_up_transaction_cell_hash": "tvm-cell-sha256:" + "b" * 64,
            "sponsorship_payment_commitment_cell_hash":
                sponsorship_payment_commitment_hash,
            "destination_source_account": request_body["source_account"],
            "amount": request_body["requested_sponsorship"],
            "submitted_transaction_hash": "sponsorship:exact",
            "source_execution_reference": "sponsorship-source-execution:exact",
            "destination_credit_references": [_repeated("5")],
            "finalized_checkpoint_id": "checkpoint:100",
            "finalized_checkpoint_sequence": 100,
            "finalized_checkpoint_unix": now + 110,
            "confirmation_depth": 3,
            "sponsorship_terminal_profile_digest":
                sponsorship_terminal["profile_digest"],
            "observation_digests": [_repeated("6"), _repeated("7"), _repeated("8")],
            "proof_bundle_digest": sponsorship_proof_bundle_digest,
            "proof_bundle": _b64(sponsorship_proof_bundle),
            "observed_at_unix": now + 120,
        },
        "submitted_transaction_hash": "tx:exact",
        "source_execution_reference": "source-execution:exact",
        "sponsorship_terminal_profile": sponsorship_terminal,
        "destination_credit_references": [_repeated("c")],
        "relay_terminal_evidence_class": "provider_corroborated",
        "relay_validator_authenticated_portable_proof": False,
        "relay_finalized_checkpoint_id": "checkpoint:relay:100",
        "relay_finalized_checkpoint_sequence": 100,
        "relay_finalized_checkpoint_unix": now + 110,
        "relay_confirmation_depth": 3,
        "relay_finality_profile": relay_finality,
        "relay_observation_digests":
            [_repeated("9"), _repeated("a"), _repeated("b")],
        "outcome": "corroborated_success",
        "observed_at_unix": now + 120,
        "signing_authority_at_unix": now + 120,
    }
    signed_evidence = _signed(evidence_body, provider_seed, b"tos.agent-relay-finality-evidence-signature.v1\x00")
    partial_evidence_body = copy.deepcopy(evidence_body)
    for name in (
            "submitted_transaction_hash", "source_execution_reference",
            "destination_credit_references", "relay_terminal_evidence_class",
            "relay_validator_authenticated_portable_proof",
            "relay_finalized_checkpoint_id",
            "relay_finalized_checkpoint_sequence",
            "relay_finalized_checkpoint_unix", "relay_confirmation_depth",
            "relay_observation_digests"):
        partial_evidence_body.pop(name)
    partial_evidence_body["outcome"] = "corroborated_sponsorship_only"
    partial_evidence_body["observed_at_unix"] = now + 121
    partial_evidence_body["signing_authority_at_unix"] = now + 121
    signed_partial_evidence = _signed(
        partial_evidence_body, provider_seed,
        b"tos.agent-relay-finality-evidence-signature.v1\x00")
    credit_observation = {
        "schema_version": 1,
        "network_digest": protocol_digest(
            "tos.agent-relay-network-domain.v1", network),
        "agreement_payment_request": copy.deepcopy(sponsorship_payment_request),
        "agreement_payment_request_digest": sponsorship_payment_request_digest,
        "sponsorship_stable_action_id": sponsorship_stable_action_id,
        "sponsorship_exact_request_digest": sponsorship_exact_request_digest,
        "provider_sponsor_source_account": "0:" + "3" * 64,
        "provider_sponsor_source_sequence": 11,
        "provider_sponsor_valid_until_unix": sponsorship_valid_until_unix,
        "signed_top_up_transaction_digest": _repeated("a"),
        "signed_top_up_transaction_cell_hash": "tvm-cell-sha256:" + "b" * 64,
        "sponsorship_payment_commitment_cell_hash":
            sponsorship_payment_commitment_hash,
        "destination_source_account": request_body["source_account"],
        "amount": request_body["requested_sponsorship"],
        "submitted_transaction_hash": "sponsorship:exact",
        "source_execution_reference": "sponsorship-source-execution:exact",
        "destination_credit_references": [_repeated("5")],
        "evidence_profile_uri": RPC_CORROBORATION_PROFILE_URI,
        "evidence_profile_digest": _repeated("c"),
        "observed_checkpoint_id": "rpc-checkpoint:99",
        "observed_checkpoint_sequence": 99,
        "observed_checkpoint_unix": now + 105,
        "observation_digests": [_repeated("6"), _repeated("7"), _repeated("8")],
        "observed_at_unix": now + 110,
    }
    observed_unproven_resolution_body = {
        "schema_version": 1,
        "provider_agent_id": "agent:provider",
        "network": network,
        "assurance_level": request_body["assurance_level"],
        "stable_action_id": stable_id,
        "exact_request_digest": request_body["exact_request_digest"],
        "relay_execution_request_digest": relay_execution_digest,
        "state": "submitted",
        "state_revision": 1,
        "sponsorship_stable_action_id": sponsorship_stable_action_id,
        "sponsorship_exact_request_digest": sponsorship_exact_request_digest,
        "sponsorship_valid_until_unix": sponsorship_valid_until_unix,
        "sponsorship_status": "observed_unproven",
        "sponsorship_observation_digest": protocol_digest(
            "tos.agent-relay-sponsorship-credit-observation.v1", credit_observation),
        "observed_at_unix": credit_observation["observed_at_unix"],
        "expires_at_unix": now + 300,
    }
    signed_observed_unproven_resolution = _signed(
        observed_unproven_resolution_body, provider_seed,
        b"tos.agent-relay-resolution-signature.v1\x00")
    resolution_body = {
        "schema_version": 1,
        "provider_agent_id": "agent:provider",
        "network": network,
        "assurance_level": request_body["assurance_level"],
        "stable_action_id": stable_id,
        "exact_request_digest": request_body["exact_request_digest"],
        "relay_execution_request_digest": relay_execution_digest,
        "state": "terminal",
        "state_revision": 4,
        "terminal_outcome": "corroborated_success",
        "transaction_reference": "tx:exact",
        "sponsorship_stable_action_id": sponsorship_stable_action_id,
        "sponsorship_exact_request_digest": sponsorship_exact_request_digest,
        "sponsorship_valid_until_unix": sponsorship_valid_until_unix,
        "sponsorship_transfer_reference": "sponsorship:exact",
        "evidence_set_digest": evidence_set_digest(
            terminal_evidence_references(evidence_body)),
        "observed_at_unix": now + 130,
        "expires_at_unix": now + 1030,
    }
    signed_resolution = _signed(resolution_body, provider_seed, b"tos.agent-relay-resolution-signature.v1\x00")
    partial_resolution_body = copy.deepcopy(resolution_body)
    partial_resolution_body["terminal_outcome"] = \
        "corroborated_sponsorship_only"
    partial_resolution_body["transaction_reference"] = "sponsorship:exact"
    partial_resolution_body["evidence_set_digest"] = evidence_set_digest(
        terminal_evidence_references(partial_evidence_body))
    partial_resolution_body["observed_at_unix"] = now + 131
    partial_resolution_body["expires_at_unix"] = now + 1031
    signed_partial_resolution = _signed(
        partial_resolution_body, provider_seed,
        b"tos.agent-relay-resolution-signature.v1\x00")
    quote_call = {"request": signed_request}
    quote_result = {"quote": signed_quote}
    submit_result = {"resolution": signed_resolution}
    resolve_call = {"stable_action_id": stable_id, "exact_request_digest": request_body["exact_request_digest"]}
    resolve_result = {"resolution": signed_resolution}
    evidence_call = {"stable_action_id": stable_id, "exact_request_digest": request_body["exact_request_digest"]}
    evidence_result = {"evidence": signed_evidence}

    absence_profile_uri = TOS_RPC_ABSENCE_PROFILE_URI
    absence_observation_profile_uri = RPC_CORROBORATION_PROFILE_URI
    absence_observation_profile_digest = rpc_profile_digest
    def absence_references(kind: str, conclusion: str,
                           terminal_profile: dict[str, Any],
                           proof_characters: list[str], checkpoint_id: str,
                           checkpoint_sequence: int,
                           checkpoint_unix: int) -> list[dict[str, Any]]:
        values = []
        for index, character in enumerate(proof_characters):
            values.append({
                "schema_version": 1,
                "observation_kind": kind,
                "conclusion": conclusion,
                "provider_agent_id": "agent:provider",
                "network_digest": protocol_digest("tos.agent-relay-network-domain.v1", network),
                "relay_stable_action_id": stable_id,
                "relay_exact_request_digest": request_body["exact_request_digest"],
                "relay_execution_request_digest": relay_execution_digest,
                "sponsorship_stable_action_id": sponsorship_stable_action_id,
                "sponsorship_exact_request_digest": sponsorship_exact_request_digest,
                "sponsorship_valid_until_unix": sponsorship_valid_until_unix,
                "signed_transaction_digest": request_body["signed_transaction_digest"],
                "signed_transaction_cell_hash": request_body["signed_transaction_cell_hash"],
                "terminal_profile_uri": terminal_profile["profile_uri"],
                "terminal_profile_digest": terminal_profile["profile_digest"],
                "terminal_evidence_class":
                    terminal_profile["terminal_evidence_class"],
                "finalized_checkpoint_id": checkpoint_id,
                "finalized_checkpoint_sequence": checkpoint_sequence,
                "finalized_checkpoint_unix": checkpoint_unix,
                "observer_id": f"observer:{index + 1}",
                "operator_domain_id": f"operator:{1 if index == 0 else 2}",
                "observation_evidence_profile_uri":
                    absence_observation_profile_uri,
                "observation_evidence_profile_digest":
                    absence_observation_profile_digest,
                "observation_digest": _repeated(character),
                "observed_at_unix": checkpoint_unix,
            })
        return sorted(values, key=absence_reference_digest)

    sponsorship_absence_not_before = (
        sponsorship_valid_until_unix +
        sponsorship_terminal["reorg_window_seconds"])
    transaction_absence_not_before = (
        request_body["transaction_valid_until_unix"] +
        relay_finality["reorg_window_seconds"])
    sponsorship_absence = absence_references(
        "sponsorship_action", "expired_without_inclusion",
        sponsorship_terminal, ["0", "1", "2"],
        "checkpoint:absence:sponsorship:110", 110,
        sponsorship_absence_not_before)
    transaction_absence = absence_references(
        "client_transaction", "absent", relay_finality, ["3", "4", "5"],
        "checkpoint:absence:transaction:610", 610,
        transaction_absence_not_before)
    transaction_invalidation = absence_references(
        "client_transaction", "invalidated_without_inclusion",
        relay_finality, ["3", "4", "5"],
        "checkpoint:invalidation:transaction:200", 200, now + 200)
    sponsorship_absence_before_terminal_window = copy.deepcopy(
        sponsorship_absence)
    for reference in sponsorship_absence_before_terminal_window:
        reference["finalized_checkpoint_unix"] = \
            sponsorship_absence_not_before - 1
    sponsorship_absence_before_terminal_window.sort(
        key=absence_reference_digest)
    transaction_absence_before_terminal_window = copy.deepcopy(
        transaction_absence)
    for reference in transaction_absence_before_terminal_window:
        reference["finalized_checkpoint_unix"] = \
            transaction_absence_not_before - 1
    transaction_absence_before_terminal_window.sort(
        key=absence_reference_digest)

    def adapter_absence_payload(scope: str,
                                sponsorship_values: list[dict[str, Any]],
                                transaction_values: list[dict[str, Any]]) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "adapter_profile_uri": absence_profile_uri,
            "adapter_profile_digest": absence_profile_digest,
            "proof_scope": scope,
            "network_digest": protocol_digest(
                "tos.agent-relay-network-domain.v1", network),
            "provider_agent_id": "agent:provider",
            "agreement_payment_request_digest":
                sponsorship_payment_request_digest,
            "sponsorship_stable_action_id": sponsorship_stable_action_id,
            "sponsorship_exact_request_digest":
                sponsorship_exact_request_digest,
            "sponsorship_valid_until_unix": sponsorship_valid_until_unix,
            "provider_sponsor_source_account": "0:" + "3" * 64,
            "provider_sponsor_source_sequence": 11,
            "signed_top_up_transaction_bytes": _b64(b"fixture-top-up-boc"),
            "signed_top_up_transaction_digest": _repeated("a"),
            "signed_top_up_transaction_cell_hash":
                "tvm-cell-sha256:" + "b" * 64,
            "relay_stable_action_id": stable_id,
            "relay_exact_request_digest": request_body["exact_request_digest"],
            "relay_execution_request_digest": relay_execution_digest,
            "signed_transaction_digest":
                request_body["signed_transaction_digest"],
            "signed_transaction_cell_hash":
                request_body["signed_transaction_cell_hash"],
            "signed_transaction_source_account": request_body["source_account"],
            "signed_transaction_source_sequence": request_body["source_sequence"],
            "transaction_valid_until_unix":
                request_body["transaction_valid_until_unix"],
            "sponsorship_raw_observations": copy.deepcopy(sponsorship_values),
            "transaction_raw_observations": copy.deepcopy(transaction_values),
        }

    absence_evidence_body = {
        "schema_version": 1,
        "provider_agent_id": "agent:provider",
        "network": network,
        "assurance_level": request_body["assurance_level"],
        "stable_action_id": stable_id,
        "exact_request_digest": request_body["exact_request_digest"],
        "relay_execution_request_digest": relay_execution_digest,
        "signed_transaction_digest": request_body["signed_transaction_digest"],
        "signed_transaction_cell_hash": request_body["signed_transaction_cell_hash"],
        "transaction_valid_until_unix":
            request_body["transaction_valid_until_unix"],
        "source_account": request_body["source_account"],
        "source_sequence": 7,
        "sponsorship_stable_action_id": sponsorship_stable_action_id,
        "sponsorship_exact_request_digest": sponsorship_exact_request_digest,
        "sponsorship_valid_until_unix": sponsorship_valid_until_unix,
        "sponsorship_absence_observations": sponsorship_absence,
        "transaction_absence_observations": transaction_absence,
        "relay_finality_profile": relay_finality,
        "sponsorship_terminal_profile": sponsorship_terminal,
        "outcome": "corroborated_absent",
        "observed_at_unix": transaction_absence_not_before + 10,
        "signing_authority_at_unix": transaction_absence_not_before + 10,
    }
    dual_absence_bundle_model = attach_absence_proof_bundle(
        absence_evidence_body, sponsorship_absence, transaction_absence,
        absence_profile_uri, absence_profile_digest,
        adapter_absence_payload("dual", sponsorship_absence,
                                transaction_absence))
    signed_absence_evidence = _signed(absence_evidence_body, provider_seed,
                                      b"tos.agent-relay-finality-evidence-signature.v1\x00")
    invalidated_absence_evidence_body = copy.deepcopy(absence_evidence_body)
    invalidated_absence_evidence_body["transaction_absence_observations"] = \
        transaction_invalidation
    invalidated_absence_evidence_body["outcome"] = \
        "corroborated_invalidated"
    invalidated_absence_evidence_body["observed_at_unix"] = now + 210
    invalidated_absence_evidence_body["signing_authority_at_unix"] = now + 210
    invalidated_absence_bundle_model = attach_absence_proof_bundle(
        invalidated_absence_evidence_body, sponsorship_absence,
        transaction_invalidation, absence_profile_uri,
        absence_profile_digest,
        adapter_absence_payload("dual", sponsorship_absence,
                                transaction_invalidation))
    signed_invalidated_absence_evidence = _signed(
        invalidated_absence_evidence_body, provider_seed,
        b"tos.agent-relay-finality-evidence-signature.v1\x00")

    post_submit_sponsorship_only_evidence_body = copy.deepcopy(
        partial_evidence_body)
    post_submit_sponsorship_only_evidence_body[
        "transaction_absence_observations"] = transaction_absence
    post_submit_sponsorship_only_evidence_body["observed_at_unix"] = \
        transaction_absence_not_before + 11
    post_submit_sponsorship_only_evidence_body[
        "signing_authority_at_unix"] = transaction_absence_not_before + 11
    transaction_only_absence_bundle_model = attach_absence_proof_bundle(
        post_submit_sponsorship_only_evidence_body, [], transaction_absence,
        absence_profile_uri, absence_profile_digest,
        adapter_absence_payload("transaction_only", [], transaction_absence))
    signed_post_submit_sponsorship_only_evidence = _signed(
        post_submit_sponsorship_only_evidence_body, provider_seed,
        b"tos.agent-relay-finality-evidence-signature.v1\x00")

    relay_only_evidence_body = copy.deepcopy(evidence_body)
    relay_only_evidence_body.pop("sponsorship_transfer_reference")
    relay_only_evidence_body.pop("sponsorship_transaction_evidence")
    relay_only_evidence_body["sponsorship_absence_observations"] = \
        sponsorship_absence
    relay_only_evidence_body["outcome"] = "corroborated_relay_only"
    relay_only_evidence_body["observed_at_unix"] = \
        sponsorship_absence_not_before + 11
    relay_only_evidence_body["signing_authority_at_unix"] = \
        sponsorship_absence_not_before + 11
    sponsorship_only_absence_bundle_model = attach_absence_proof_bundle(
        relay_only_evidence_body, sponsorship_absence, [],
        absence_profile_uri, absence_profile_digest,
        adapter_absence_payload("sponsorship_only", sponsorship_absence, []))
    signed_relay_only_evidence = _signed(
        relay_only_evidence_body, provider_seed,
        b"tos.agent-relay-finality-evidence-signature.v1\x00")

    absence_resolution_body = {
        "schema_version": 1,
        "provider_agent_id": "agent:provider",
        "network": network,
        "assurance_level": request_body["assurance_level"],
        "stable_action_id": stable_id,
        "exact_request_digest": request_body["exact_request_digest"],
        "relay_execution_request_digest": relay_execution_digest,
        "state": "terminal",
        "state_revision": 4,
        "terminal_outcome": "corroborated_absent",
        "sponsorship_stable_action_id": sponsorship_stable_action_id,
        "sponsorship_exact_request_digest": sponsorship_exact_request_digest,
        "sponsorship_valid_until_unix": sponsorship_valid_until_unix,
        "evidence_set_digest": evidence_set_digest(
            terminal_evidence_references(absence_evidence_body)),
        "observed_at_unix": transaction_absence_not_before + 20,
        "expires_at_unix": transaction_absence_not_before + 920,
    }
    signed_absence_resolution = _signed(absence_resolution_body, provider_seed,
                                        b"tos.agent-relay-resolution-signature.v1\x00")

    post_submit_sponsorship_only_resolution_body = copy.deepcopy(
        partial_resolution_body)
    post_submit_sponsorship_only_resolution_body["evidence_set_digest"] = \
        evidence_set_digest(terminal_evidence_references(
            post_submit_sponsorship_only_evidence_body))
    post_submit_sponsorship_only_resolution_body["observed_at_unix"] = \
        transaction_absence_not_before + 21
    post_submit_sponsorship_only_resolution_body["expires_at_unix"] = \
        transaction_absence_not_before + 921
    signed_post_submit_sponsorship_only_resolution = _signed(
        post_submit_sponsorship_only_resolution_body, provider_seed,
        b"tos.agent-relay-resolution-signature.v1\x00")

    relay_only_resolution_body = copy.deepcopy(resolution_body)
    relay_only_resolution_body["terminal_outcome"] = \
        "corroborated_relay_only"
    relay_only_resolution_body.pop("sponsorship_transfer_reference")
    relay_only_resolution_body["evidence_set_digest"] = evidence_set_digest(
        terminal_evidence_references(relay_only_evidence_body))
    relay_only_resolution_body["observed_at_unix"] = \
        sponsorship_absence_not_before + 21
    relay_only_resolution_body["expires_at_unix"] = \
        sponsorship_absence_not_before + 921
    signed_relay_only_resolution = _signed(
        relay_only_resolution_body, provider_seed,
        b"tos.agent-relay-resolution-signature.v1\x00")

    computed_go = {
        "network": protocol_digest("tos.agent-relay-network-domain.v1", network),
        "underlying_payment_request": protocol_digest("tos.agreement-payment-request.v1",
                                                       underlying_payment_request),
        "underlying_payment_stable_id": underlying_payment_request["stable_action_id"],
        "underlying_payment_exact_request": exact_request_digest(underlying_request),
        "sponsorship_payment_request": protocol_digest("tos.agreement-payment-request.v1",
                                                        sponsorship_payment_request),
        "sponsorship_payment_stable_id": sponsorship_payment_request["stable_action_id"],
        "sponsorship_payment_exact_request": exact_request_digest(sponsorship_action_request),
        "service_profile": protocol_digest("tos.agent-relay-service-profile.v1", go_profile),
        "quote_request_body": protocol_digest("tos.agent-relay-quote-request.v1", go_request_body),
        "provider_quote_body": protocol_digest("tos.agent-relay-provider-quote.v1", go_quote_body),
        "request_public_key": go_signed_request["public_key"],
        "request_signature": go_signed_request["signature"],
        "quote_public_key": go_signed_quote["public_key"],
        "quote_signature": go_signed_quote["signature"],
    }
    if computed_go != EXPECTED_GO:
        mismatches = {key: {"computed": computed_go[key], "go": EXPECTED_GO[key]} for key in computed_go if computed_go[key] != EXPECTED_GO[key]}
        raise ConformanceError("independent fixture disagrees with Go: " + json.dumps(mismatches, sort_keys=True))

    objects = [
        _object("network", "NetworkDomainV1", network, "tos.agent-relay-network-domain.v1"),
        _object("negative_network_order", "NetworkDomainV1[]", negative_network_order),
        _object("underlying_payment_request", "AgreementPaymentRequestV3", underlying_payment_request,
                "tos.agreement-payment-request.v1"),
        _object("sponsorship_payment_request", "AgreementPaymentRequestV3", sponsorship_payment_request,
                "tos.agreement-payment-request.v1"),
        _object("go_service_profile", "RelayServiceProfileV1", go_profile,
                "tos.agent-relay-service-profile.v1"),
        _object("go_quote_request_body", "RelayQuoteRequestV1.body", go_request_body,
                "tos.agent-relay-quote-request.v1"),
        _object("go_signed_quote_request", "RelayQuoteRequestV1", go_signed_request),
        _object("go_provider_quote_body", "SignedProviderRelayQuoteV1.body", go_quote_body,
                "tos.agent-relay-provider-quote.v1"),
        _object("go_signed_provider_quote", "SignedProviderRelayQuoteV1", go_signed_quote),
        _object("service_profile", "RelayServiceProfileV1", profile, "tos.agent-relay-service-profile.v1"),
        _object("quote_request_body", "RelayQuoteRequestV1.body", request_body, "tos.agent-relay-quote-request.v1"),
        _object("signed_quote_request", "RelayQuoteRequestV1", signed_request),
        _object("provider_quote_body", "SignedProviderRelayQuoteV1.body", quote_body, "tos.agent-relay-provider-quote.v1"),
        _object("signed_provider_quote", "SignedProviderRelayQuoteV1", signed_quote),
        _object("transaction_identity", "RelayTransactionIdentityV1",
                transaction_identity_body,
                "tos.agent-relay-transaction-identity.v1"),
        _object("quote_call", "RelayQuoteCallV1", quote_call),
        _object("quote_result", "RelayQuoteResultV1", quote_result),
        _object("agreement_binding", "RelayAgreementBindingV1", agreement_binding, "tos.agent-relay-agreement-binding.v1"),
        _object("agreement_body", "AgentAgreementBodyV1", agreement_body, "tos.agent-agreement-body.v1"),
        _object("admission_request", "RelaySideEffectAdmissionRequestV1", admission_request),
        _object("admission_receipt_body", "RelaySideEffectAdmissionReceiptBodyV1",
                admission_receipt_body,
                "tos.agent-relay-side-effect-admission-receipt.v1"),
        _object("signed_admission_receipt", "SignedRelaySideEffectAdmissionReceiptV1",
                signed_admission_receipt),
        _object("resolve_admission_call", "ResolveAdmissionCallV1", resolve_admission_call),
        _object("resolve_admission_result", "ResolveAdmissionResultV1", resolve_admission_result),
        _object("execution_request", "RelayExecutionRequestV1", execution,
                "tos.agent-relay-execution-request.v1", execution_projection(execution)),
        _object("submit_call", "RelaySubmitCallV1", submit_call),
        _object("sponsorship_credit_observation", "RelaySponsorshipCreditObservationV1",
                credit_observation,
                "tos.agent-relay-sponsorship-credit-observation.v1"),
        _object("observed_unproven_resolution_body", "SignedRelayResolutionV1.body",
                observed_unproven_resolution_body,
                "tos.agent-relay-resolution.v1"),
        _object("signed_observed_unproven_resolution", "SignedRelayResolutionV1",
                signed_observed_unproven_resolution),
        _object("finality_evidence_body", "RelayFinalityEvidenceV1.body", evidence_body,
                "tos.agent-relay-finality-evidence.v1"),
        _object("signed_finality_evidence", "RelayFinalityEvidenceV1", signed_evidence),
        _object("combined_partial_corroborated_evidence_body",
                "RelayFinalityEvidenceV1.body", partial_evidence_body,
                "tos.agent-relay-finality-evidence.v1"),
        _object("signed_combined_partial_corroborated_evidence",
                "RelayFinalityEvidenceV1", signed_partial_evidence),
        _object("combined_partial_corroborated_resolution_body",
                "SignedRelayResolutionV1.body", partial_resolution_body,
                "tos.agent-relay-resolution.v1"),
        _object("signed_combined_partial_corroborated_resolution",
                "SignedRelayResolutionV1", signed_partial_resolution),
        _object("post_submit_sponsorship_only_absence_proof_bundle",
                "RelayAbsenceProofBundleV1",
                transaction_only_absence_bundle_model,
                "tos.agent-relay-absence-proof-bundle.v1"),
        _object("post_submit_sponsorship_only_evidence_body",
                "RelayFinalityEvidenceV1.body",
                post_submit_sponsorship_only_evidence_body,
                "tos.agent-relay-finality-evidence.v1"),
        _object("signed_post_submit_sponsorship_only_evidence",
                "RelayFinalityEvidenceV1",
                signed_post_submit_sponsorship_only_evidence),
        _object("post_submit_sponsorship_only_resolution_body",
                "SignedRelayResolutionV1.body",
                post_submit_sponsorship_only_resolution_body,
                "tos.agent-relay-resolution.v1"),
        _object("signed_post_submit_sponsorship_only_resolution",
                "SignedRelayResolutionV1",
                signed_post_submit_sponsorship_only_resolution),
        _object("relay_only_absence_proof_bundle",
                "RelayAbsenceProofBundleV1",
                sponsorship_only_absence_bundle_model,
                "tos.agent-relay-absence-proof-bundle.v1"),
        _object("relay_only_evidence_body", "RelayFinalityEvidenceV1.body",
                relay_only_evidence_body,
                "tos.agent-relay-finality-evidence.v1"),
        _object("signed_relay_only_evidence", "RelayFinalityEvidenceV1",
                signed_relay_only_evidence),
        _object("relay_only_resolution_body",
                "SignedRelayResolutionV1.body", relay_only_resolution_body,
                "tos.agent-relay-resolution.v1"),
        _object("signed_relay_only_resolution", "SignedRelayResolutionV1",
                signed_relay_only_resolution),
        _object("resolution_body", "SignedRelayResolutionV1.body", resolution_body,
                "tos.agent-relay-resolution.v1"),
        _object("signed_resolution", "SignedRelayResolutionV1", signed_resolution),
        _object("submit_result", "RelaySubmitResultV1", submit_result),
        _object("resolve_call", "RelayResolveCallV1", resolve_call),
        _object("resolve_result", "RelayResolveResultV1", resolve_result),
        _object("evidence_call", "RelayEvidenceCallV1", evidence_call),
        _object("evidence_result", "RelayEvidenceResultV1", evidence_result),
        _object("sponsorship_absence_observations", "RelayAbsenceObservationReferenceV1[]",
                sponsorship_absence),
        _object("transaction_absence_observations", "RelayAbsenceObservationReferenceV1[]",
                transaction_absence),
        *[_object(f"sponsorship_absence_observation_{index + 1}", "RelayAbsenceObservationReferenceV1",
                  reference, "tos.agent-relay-absence-observation-reference.v1")
          for index, reference in enumerate(sponsorship_absence)],
        *[_object(f"transaction_absence_observation_{index + 1}", "RelayAbsenceObservationReferenceV1",
                  reference, "tos.agent-relay-absence-observation-reference.v1")
          for index, reference in enumerate(transaction_absence)],
        _object("absence_finality_evidence_body", "RelayFinalityEvidenceV1.body", absence_evidence_body,
                "tos.agent-relay-finality-evidence.v1"),
        _object("dual_absence_proof_bundle", "RelayAbsenceProofBundleV1",
                dual_absence_bundle_model,
                "tos.agent-relay-absence-proof-bundle.v1"),
        _object("signed_absence_finality_evidence", "RelayFinalityEvidenceV1", signed_absence_evidence),
        _object("invalidated_absence_finality_evidence_body",
                "RelayFinalityEvidenceV1.body",
                invalidated_absence_evidence_body,
                "tos.agent-relay-finality-evidence.v1"),
        _object("signed_invalidated_absence_finality_evidence",
                "RelayFinalityEvidenceV1",
                signed_invalidated_absence_evidence),
        _object("invalidated_dual_absence_proof_bundle",
                "RelayAbsenceProofBundleV1",
                invalidated_absence_bundle_model,
                "tos.agent-relay-absence-proof-bundle.v1"),
        _object("absence_resolution_body", "SignedRelayResolutionV1.body", absence_resolution_body,
                "tos.agent-relay-resolution.v1"),
        _object("signed_absence_resolution", "SignedRelayResolutionV1", signed_absence_resolution),
    ]
    signatures = [
        {"name": "go_requester_quote_request", "body_object": "go_quote_request_body",
         "envelope_object": "go_signed_quote_request", "signature_field": "signature",
         "message_domain": "tos.agent-relay-quote-request-signature.v1\\0",
         "expected_message_hex": signature_message(
             b"tos.agent-relay-quote-request-signature.v1\x00", go_request_body).hex()},
        {"name": "go_provider_quote", "body_object": "go_provider_quote_body",
         "envelope_object": "go_signed_provider_quote", "signature_field": "signature",
         "message_domain": "tos.agent-relay-provider-quote-signature.v1\\0",
         "expected_message_hex": signature_message(
             b"tos.agent-relay-provider-quote-signature.v1\x00", go_quote_body).hex()},
        {"name": "requester_quote_request", "body_object": "quote_request_body", "envelope_object": "signed_quote_request",
         "signature_field": "signature", "message_domain": "tos.agent-relay-quote-request-signature.v1\\0",
         "expected_message_hex": signature_message(b"tos.agent-relay-quote-request-signature.v1\x00", request_body).hex()},
        {"name": "provider_quote", "body_object": "provider_quote_body", "envelope_object": "signed_provider_quote",
         "signature_field": "signature", "message_domain": "tos.agent-relay-provider-quote-signature.v1\\0",
         "expected_message_hex": signature_message(b"tos.agent-relay-provider-quote-signature.v1\x00", quote_body).hex()},
        {"name": "side_effect_admission_receipt", "body_object": "admission_receipt_body",
         "envelope_object": "signed_admission_receipt", "signature_field": "signature",
         "message_domain": "tos.agent-relay-side-effect-admission-receipt-signature.v1\\0",
         "expected_message_hex": signature_message(
             b"tos.agent-relay-side-effect-admission-receipt-signature.v1\x00",
             admission_receipt_body).hex()},
        {"name": "provider_finality_evidence", "body_object": "finality_evidence_body", "envelope_object": "signed_finality_evidence",
         "signature_field": "signature", "message_domain": "tos.agent-relay-finality-evidence-signature.v1\\0",
         "expected_message_hex": signature_message(b"tos.agent-relay-finality-evidence-signature.v1\x00", evidence_body).hex()},
        {"name": "provider_combined_partial_corroborated_evidence",
         "body_object": "combined_partial_corroborated_evidence_body",
         "envelope_object": "signed_combined_partial_corroborated_evidence",
         "signature_field": "signature",
         "message_domain": "tos.agent-relay-finality-evidence-signature.v1\\0",
         "expected_message_hex": signature_message(
             b"tos.agent-relay-finality-evidence-signature.v1\x00",
             partial_evidence_body).hex()},
        {"name": "provider_combined_partial_corroborated_resolution",
         "body_object": "combined_partial_corroborated_resolution_body",
         "envelope_object": "signed_combined_partial_corroborated_resolution",
         "signature_field": "signature",
         "message_domain": "tos.agent-relay-resolution-signature.v1\\0",
         "expected_message_hex": signature_message(
             b"tos.agent-relay-resolution-signature.v1\x00",
             partial_resolution_body).hex()},
        {"name": "provider_post_submit_sponsorship_only_evidence",
         "body_object": "post_submit_sponsorship_only_evidence_body",
         "envelope_object": "signed_post_submit_sponsorship_only_evidence",
         "signature_field": "signature",
         "message_domain": "tos.agent-relay-finality-evidence-signature.v1\\0",
         "expected_message_hex": signature_message(
             b"tos.agent-relay-finality-evidence-signature.v1\x00",
             post_submit_sponsorship_only_evidence_body).hex()},
        {"name": "provider_post_submit_sponsorship_only_resolution",
         "body_object": "post_submit_sponsorship_only_resolution_body",
         "envelope_object": "signed_post_submit_sponsorship_only_resolution",
         "signature_field": "signature",
         "message_domain": "tos.agent-relay-resolution-signature.v1\\0",
         "expected_message_hex": signature_message(
             b"tos.agent-relay-resolution-signature.v1\x00",
             post_submit_sponsorship_only_resolution_body).hex()},
        {"name": "provider_relay_only_evidence",
         "body_object": "relay_only_evidence_body",
         "envelope_object": "signed_relay_only_evidence",
         "signature_field": "signature",
         "message_domain": "tos.agent-relay-finality-evidence-signature.v1\\0",
         "expected_message_hex": signature_message(
             b"tos.agent-relay-finality-evidence-signature.v1\x00",
             relay_only_evidence_body).hex()},
        {"name": "provider_relay_only_resolution",
         "body_object": "relay_only_resolution_body",
         "envelope_object": "signed_relay_only_resolution",
         "signature_field": "signature",
         "message_domain": "tos.agent-relay-resolution-signature.v1\\0",
         "expected_message_hex": signature_message(
             b"tos.agent-relay-resolution-signature.v1\x00",
             relay_only_resolution_body).hex()},
        {"name": "provider_resolution", "body_object": "resolution_body", "envelope_object": "signed_resolution",
         "signature_field": "signature", "message_domain": "tos.agent-relay-resolution-signature.v1\\0",
         "expected_message_hex": signature_message(b"tos.agent-relay-resolution-signature.v1\x00", resolution_body).hex()},
        {"name": "provider_observed_unproven_resolution",
         "body_object": "observed_unproven_resolution_body",
         "envelope_object": "signed_observed_unproven_resolution",
         "signature_field": "signature",
         "message_domain": "tos.agent-relay-resolution-signature.v1\\0",
         "expected_message_hex": signature_message(
             b"tos.agent-relay-resolution-signature.v1\x00",
             observed_unproven_resolution_body).hex()},
        {"name": "provider_absence_finality_evidence", "body_object": "absence_finality_evidence_body",
         "envelope_object": "signed_absence_finality_evidence", "signature_field": "signature",
         "message_domain": "tos.agent-relay-finality-evidence-signature.v1\\0",
         "expected_message_hex": signature_message(b"tos.agent-relay-finality-evidence-signature.v1\x00",
                                                   absence_evidence_body).hex()},
        {"name": "provider_invalidated_absence_finality_evidence",
         "body_object": "invalidated_absence_finality_evidence_body",
         "envelope_object": "signed_invalidated_absence_finality_evidence",
         "signature_field": "signature",
         "message_domain": "tos.agent-relay-finality-evidence-signature.v1\\0",
         "expected_message_hex": signature_message(
             b"tos.agent-relay-finality-evidence-signature.v1\x00",
             invalidated_absence_evidence_body).hex()},
        {"name": "provider_absence_resolution", "body_object": "absence_resolution_body",
         "envelope_object": "signed_absence_resolution", "signature_field": "signature",
         "message_domain": "tos.agent-relay-resolution-signature.v1\\0",
         "expected_message_hex": signature_message(b"tos.agent-relay-resolution-signature.v1\x00",
                                                   absence_resolution_body).hex()},
    ]
    negative_mutations = [
        {"name": "lexical-negative-network-order", "target": "negative_network_order",
         "path": [0, "global_id"], "replacement": -1, "expected": "reject"},
        {"name": "underlying-payment-network-domain-substitution", "target": "underlying_payment_request",
         "path": ["network_domain_digest"], "replacement": _repeated("f"), "expected": "reject"},
        {"name": "sponsorship-payment-network-domain-substitution", "target": "sponsorship_payment_request",
         "path": ["network_domain_digest"], "replacement": _repeated("f"), "expected": "reject"},
        {"name": "wrong-global-id", "target": "signed_quote_request", "path": ["body", "network", "global_id"], "replacement": 43, "expected": "reject"},
        {"name": "transaction-identity-byte-digest-substitution", "target": "transaction_identity",
         "path": ["signed_transaction_digest"], "replacement": _repeated("f"),
         "expected": "reject"},
        {"name": "boolean-global-id", "target": "signed_quote_request",
         "path": ["body", "network", "global_id"], "replacement": True,
         "resign_as": "requester", "expected": "reject"},
        {"name": "boolean-source-sequence", "target": "signed_quote_request",
         "path": ["body", "source_sequence"], "replacement": False,
         "resign_as": "requester", "expected": "reject"},
        {"name": "boolean-signed-transaction-size", "target": "signed_quote_request",
         "path": ["body", "signed_transaction_size"], "replacement": True,
         "resign_as": "requester", "expected": "reject"},
        {"name": "wrong-zero-state", "target": "signed_quote_request", "path": ["body", "network", "zero_state_root_hash"], "replacement": _repeated("f"), "expected": "reject"},
        {"name": "wrong-source-authority", "target": "signed_quote_request", "path": ["body", "source_account_authority_digest"], "replacement": _repeated("1"), "expected": "reject"},
        {"name": "generic-cell-hash-domain", "target": "signed_quote_request", "path": ["body", "signed_transaction_cell_hash"], "replacement": _repeated("d"), "expected": "reject"},
        {"name": "wrong-provider", "target": "signed_quote_request", "path": ["body", "provider_agent_id"], "replacement": "agent:other", "expected": "reject"},
        {"name": "request-unsupported-assurance", "target": "signed_quote_request",
         "path": ["body", "assurance_level"], "replacement": "future-assurance",
         "resign_as": "requester", "expected": "reject"},
        {"name": "request-release-class-downgrade", "target": "signed_quote_request",
         "path": ["body", "sponsorship_release_evidence_class"],
         "replacement": "validator_finality", "resign_as": "requester", "expected": "reject"},
        {"name": "request-release-profile-owner-pin-substitution", "target": "signed_quote_request",
         "path": ["body", "sponsorship_release_profile_digest"],
         "replacement": _repeated("d"), "resign_as": "requester", "expected": "reject"},
        {"name": "observed-release-old-terminal-profile-substitution",
         "target": "signed_quote_request",
         "path": ["body", "sponsorship_terminal_profile_uri"],
         "replacement": "tos.depth-quorum.v1", "resign_as": "requester",
         "expected": "reject"},
        {"name": "request-relay-evidence-class-downgrade",
         "target": "signed_quote_request",
         "path": ["body", "relay_terminal_evidence_class"],
         "replacement": "validator_finality", "resign_as": "requester",
         "expected": "reject"},
        {"name": "request-sponsorship-terminal-class-downgrade",
         "target": "signed_quote_request",
         "path": ["body", "sponsorship_terminal_evidence_class"],
         "replacement": "validator_finality", "resign_as": "requester",
         "expected": "reject"},
        {"name": "request-mode-profile-matrix-substitution",
         "target": "signed_quote_request", "path": ["body", "mode"],
         "replacement": "relay_exact", "resign_as": "requester",
         "expected": "reject"},
        {"name": "resigned-request-before-profile", "target": "signed_quote_request", "path": ["body", "created_at_unix"], "replacement": 1799999939, "resign_as": "requester", "expected": "reject"},
        {"name": "quote-carries-bearer-bytes", "target": "signed_quote_request", "path": ["signed_transaction_bytes"], "replacement": _b64(signed_transaction), "expected": "reject"},
        {"name": "mutated-submit-signed-bytes", "target": "execution_request", "path": ["signed_transaction_bytes"], "replacement": _b64(signed_transaction + b"!"), "expected": "reject"},
        {"name": "unknown-request-field", "target": "signed_quote_request", "path": ["body", "route_id"], "replacement": "transport:forbidden", "expected": "reject"},
        {"name": "private-resolve-endpoint", "target": "service_profile", "path": ["endpoints", "resolve_url"], "replacement": "https://127.0.0.1/resolve", "expected": "reject"},
        {"name": "uninspectable-sequence", "target": "service_profile", "path": ["transaction_profiles", 0, "inspectable_source_sequence"], "replacement": False, "expected": "reject"},
        {"name": "wrong-quote-request-digest", "target": "signed_provider_quote", "path": ["body", "quote_request_digest"], "replacement": _repeated("0"), "expected": "reject"},
        {"name": "provider-quote-assurance-downgrade", "target": "signed_provider_quote",
         "path": ["body", "assurance_level"], "replacement": "trusted-local",
         "resign_as": "provider", "expected": "reject"},
        {"name": "provider-quote-release-profile-substitution", "target": "signed_provider_quote",
         "path": ["body", "sponsorship_release_profile_digest"], "replacement": _repeated("d"),
         "resign_as": "provider", "expected": "reject"},
        {"name": "wrong-fee-kind", "target": "signed_provider_quote", "path": ["body", "fee_lines", 0, "kind"], "replacement": "transaction_relay_fee", "expected": "reject"},
        {"name": "resigned-weaker-finality-threshold", "target": "signed_provider_quote", "path": ["body", "relay_finality_profile", "minimum_confirmation_depth"], "replacement": 1, "resign_as": "provider", "expected": "reject"},
        {"name": "provider-quote-relay-class-profile-substitution",
         "target": "signed_provider_quote",
         "path": ["body", "relay_finality_profile", "terminal_evidence_class"],
         "replacement": "validator_finality", "resign_as": "provider",
         "expected": "reject"},
        {"name": "provider-quote-mode-profile-matrix-substitution",
         "target": "signed_provider_quote", "path": ["body", "mode"],
         "replacement": "sponsor_only", "resign_as": "provider",
         "expected": "reject"},
        {"name": "boolean-provider-policy-revision", "target": "signed_provider_quote",
         "path": ["body", "provider_policy_revision"], "replacement": True,
         "resign_as": "provider", "expected": "reject"},
        {"name": "fee-over-maximum", "target": "signed_provider_quote", "path": ["body", "fee_lines", 0, "amount", "amount_atomic"], "replacement": "11", "expected": "reject"},
        {"name": "mutated-quote-signature", "target": "signed_provider_quote", "path": ["signature"], "replacement": "ed25519:" + "A" * 86, "expected": "reject"},
        {"name": "admission-route-substitution", "target": "admission_request",
         "path": ["provider_quote_digest"], "replacement": _repeated("f"),
         "expected": "reject"},
        {"name": "admission-transaction-identity-substitution", "target": "admission_request",
         "path": ["transaction_identity_digest"], "replacement": _repeated("f"),
         "expected": "reject"},
        {"name": "admission-assurance-downgrade", "target": "admission_request",
         "path": ["assurance_level"], "replacement": "trusted-local",
         "expected": "reject"},
        {"name": "admission-zero-route-attempt", "target": "admission_request",
         "path": ["route_attempt"], "replacement": 0, "expected": "reject"},
        {"name": "sponsorship-successor-forbidden", "target": "admission_request",
         "path": ["route_attempt"], "replacement": 2, "expected": "reject"},
        {"name": "admission-stage-expansion", "target": "admission_request",
         "path": ["stage_mask"], "replacement": ["broadcast", "sponsorship", "withdraw"],
         "expected": "reject"},
        {"name": "admission-underlying-request-substitution", "target": "admission_request",
         "path": ["underlying_action_request"], "replacement": _b64(b"different"),
         "expected": "reject"},
        {"name": "admission-receipt-principal-substitution",
         "target": "signed_admission_receipt",
         "path": ["body", "authenticated_principal_id"],
         "replacement": "principal:other", "resign_as": "authority_admission",
         "expected": "reject"},
        {"name": "admission-receipt-action-digest-substitution",
         "target": "signed_admission_receipt",
         "path": ["body", "authorized_action_digest"], "replacement": _repeated("f"),
         "resign_as": "authority_admission", "expected": "reject"},
        {"name": "admission-receipt-writer-generation-substitution",
         "target": "signed_admission_receipt",
         "path": ["body", "writer_generation"], "replacement": 2,
         "resign_as": "authority_admission", "expected": "reject"},
        {"name": "admission-receipt-assurance-downgrade",
         "target": "signed_admission_receipt",
         "path": ["body", "assurance_level"], "replacement": "trusted-local",
         "resign_as": "authority_admission", "expected": "reject"},
        {"name": "boolean-admission-sequence", "target": "signed_admission_receipt",
         "path": ["body", "admission_sequence"], "replacement": True,
         "resign_as": "authority_admission", "expected": "reject"},
        {"name": "admission-receipt-window-over-60-seconds",
         "target": "signed_admission_receipt",
         "path": ["body", "start_not_after_unix"], "replacement": now + 61,
         "resign_as": "authority_admission", "expected": "reject"},
        {"name": "admission-receipt-bad-signature", "target": "signed_admission_receipt",
         "path": ["signature"], "replacement": "ed25519:" + "A" * 86,
         "expected": "reject"},
        {"name": "resolve-admission-route-substitution", "target": "resolve_admission_call",
         "path": ["provider_quote_digest"], "replacement": _repeated("f"),
         "expected": "reject"},
        {"name": "changed-underlying-request", "target": "execution_request", "path": ["underlying_action_request"], "replacement": _b64(bytes([0xA1, 0x01, 0x03])), "expected": "reject"},
        {"name": "changed-semantic-owner", "target": "execution_request", "path": ["semantic_fields", 0, "text"], "replacement": "owner:other", "expected": "reject"},
        {"name": "stale-writer-generation", "target": "execution_request", "path": ["authorized_action", "writer_generation"], "replacement": 0, "expected": "reject"},
        {"name": "execution-after-quote", "target": "execution_request", "path": ["expires_at_unix"], "replacement": now + 241, "expected": "reject"},
        {"name": "agreement-binding-assurance-downgrade", "target": "agreement_binding",
         "path": ["assurance_level"], "replacement": "trusted-local", "expected": "reject"},
        {"name": "agreement-binding-release-profile-substitution", "target": "agreement_binding",
         "path": ["sponsorship_release_profile_digest"], "replacement": _repeated("d"),
         "expected": "reject"},
        {"name": "agreement-binding-relay-profile-substitution",
         "target": "agreement_binding",
         "path": ["relay_finality_profile_digest"],
         "replacement": _repeated("0"), "expected": "reject"},
        {"name": "agreement-binding-sponsorship-class-substitution",
         "target": "agreement_binding",
         "path": ["sponsorship_terminal_evidence_class"],
         "replacement": "validator_finality", "expected": "reject"},
        {"name": "agreement-top-level-terms-substitution", "target": "submit_call",
         "path": ["agreement", "body", "terms"], "replacement": _b64(b"different terms"), "expected": "reject"},
        {"name": "agreement-top-level-content-type-substitution", "target": "submit_call",
         "path": ["agreement", "body", "terms_content_type"], "replacement": "application/octet-stream", "expected": "reject"},
        {"name": "rpc-observation-payment-binding-substitution",
         "target": "sponsorship_credit_observation",
         "path": ["agreement_payment_request", "agreement_body_digest"],
         "replacement": _repeated("0"), "expected": "reject"},
        {"name": "rpc-observation-profile-substitution",
         "target": "sponsorship_credit_observation",
         "path": ["evidence_profile_uri"],
         "replacement": "chain-finalized.v1", "expected": "reject"},
        {"name": "rpc-observation-commitment-mutation",
         "target": "sponsorship_credit_observation",
         "path": ["sponsorship_payment_commitment_cell_hash"],
         "replacement": "tvm-cell-sha256:" + "e" * 64,
         "expected": "reject"},
        {"name": "observed-resolution-digest-substitution",
         "target": "signed_observed_unproven_resolution",
         "path": ["body", "sponsorship_observation_digest"],
         "replacement": _repeated("0"), "resign_as": "provider_resolution",
         "expected": "reject"},
        {"name": "observed-resolution-assurance-upgrade",
         "target": "signed_observed_unproven_resolution",
         "path": ["body", "assurance_level"],
         "replacement": "autonomous-decentralized", "resign_as": "provider_resolution",
         "expected": "reject"},
        {"name": "evidence-source-mismatch", "target": "signed_finality_evidence", "path": ["body", "source_sequence"], "replacement": 8, "expected": "reject"},
        {"name": "evidence-transaction-validity-substitution",
         "target": "signed_finality_evidence",
         "path": ["body", "transaction_valid_until_unix"],
         "replacement": request_body["transaction_valid_until_unix"] + 1,
         "resign_as": "provider_evidence", "expected": "reject"},
        {"name": "evidence-sponsorship-action-substitution", "target": "signed_finality_evidence",
         "path": ["body", "sponsorship_exact_request_digest"], "replacement": _repeated("0"), "expected": "reject"},
        {"name": "sponsorship-payment-request-digest-substitution", "target": "signed_finality_evidence",
         "path": ["body", "sponsorship_transaction_evidence", "agreement_payment_request_digest"],
         "replacement": _repeated("0"), "expected": "reject"},
        {"name": "sponsorship-payment-request-agreement-substitution", "target": "signed_finality_evidence",
         "path": ["body", "sponsorship_transaction_evidence", "agreement_payment_request",
                  "agreement_body_digest"],
         "replacement": _repeated("0"), "expected": "reject"},
        {"name": "sponsorship-payment-request-obligation-substitution", "target": "signed_finality_evidence",
         "path": ["body", "sponsorship_transaction_evidence", "agreement_payment_request",
                  "agreement_obligation_id"],
         "replacement": "obligation:other", "expected": "reject"},
        {"name": "sponsorship-payment-request-agent-substitution", "target": "signed_finality_evidence",
         "path": ["body", "sponsorship_transaction_evidence", "agreement_payment_request", "agent_id"],
         "replacement": "agent:other", "expected": "reject"},
        {"name": "sponsorship-terminal-class-profile-downgrade",
         "target": "signed_finality_evidence",
         "path": ["body", "sponsorship_transaction_evidence",
                  "terminal_evidence_class"],
         "replacement": "validator_finality", "resign_as": "provider_evidence",
         "expected": "reject"},
        {"name": "sponsorship-terminal-authentication-overstatement",
         "target": "signed_finality_evidence",
         "path": ["body", "sponsorship_transaction_evidence",
                  "validator_authenticated_portable_proof"],
         "replacement": True, "resign_as": "provider_evidence",
         "expected": "reject"},
        {"name": "client-corroborated-profile-downgrade",
         "target": "signed_finality_evidence",
         "path": ["body", "sponsorship_terminal_profile", "profile_uri"],
         "replacement": "tos.depth-quorum.v1",
         "resign_as": "provider_evidence", "expected": "reject"},
        {"name": "relay-provider-corroborated-profile-substitution",
         "target": "signed_finality_evidence",
         "path": ["body", "relay_finality_profile", "profile_uri"],
         "replacement": "tos.depth-quorum.v1",
         "resign_as": "provider_evidence", "expected": "reject"},
        {"name": "sponsorship-terminal-profile-digest-substitution",
         "target": "signed_finality_evidence",
         "path": ["body", "sponsorship_terminal_profile",
                  "profile_digest"],
         "replacement": _repeated("0"),
         "resign_as": "provider_evidence", "expected": "reject"},
        {"name": "nested-sponsorship-terminal-profile-digest-substitution",
         "target": "signed_finality_evidence",
         "path": ["body", "sponsorship_transaction_evidence",
                  "sponsorship_terminal_profile_digest"],
         "replacement": _repeated("0"),
         "resign_as": "provider_evidence", "expected": "reject"},
        {"name": "relay-evidence-class-authentication-overstatement",
         "target": "signed_finality_evidence",
         "path": ["body", "relay_validator_authenticated_portable_proof"],
         "replacement": True, "resign_as": "provider_evidence",
         "expected": "reject"},
        {"name": "client-corroborated-false-finalized-success",
         "target": "signed_finality_evidence", "path": ["body", "outcome"],
         "replacement": "finalized_success", "resign_as": "provider_evidence",
         "expected": "reject"},
        {"name": "terminal-sponsorship-evidence-stripped",
         "target": "signed_finality_evidence",
         "path": ["body", "sponsorship_transaction_evidence"],
         "replacement": {}, "resign_as": "provider_evidence",
         "expected": "reject"},
        {"name": "sponsorship-payment-commitment-mutation",
         "target": "signed_finality_evidence",
         "path": ["body", "sponsorship_transaction_evidence",
                  "sponsorship_payment_commitment_cell_hash"],
         "replacement": "tvm-cell-sha256:" + "e" * 64,
         "resign_as": "provider_evidence", "expected": "reject"},
        {"name": "old-agreement-top-up-replay",
         "target": "signed_finality_evidence",
         "path": ["body", "sponsorship_transaction_evidence",
                  "sponsorship_payment_commitment_cell_hash"],
         "replacement": old_agreement_commitment_hash,
         "resign_as": "provider_evidence", "expected": "reject"},
        {"name": "sponsorship-destination-substitution", "target": "signed_finality_evidence",
         "path": ["body", "sponsorship_transaction_evidence", "destination_source_account"],
         "replacement": "0:" + "f" * 64, "expected": "reject"},
        {"name": "sponsorship-top-up-byte-digest-invalid", "target": "signed_finality_evidence",
         "path": ["body", "sponsorship_transaction_evidence", "signed_top_up_transaction_digest"],
         "replacement": "tx:opaque", "expected": "reject"},
        {"name": "sponsorship-in-band-proof-substitution", "target": "signed_finality_evidence",
         "path": ["body", "sponsorship_transaction_evidence", "proof_bundle"],
         "replacement": _b64(b"\xa0"), "resign_as": "provider_evidence", "expected": "reject"},
        {"name": "insufficient-observers", "target": "signed_finality_evidence", "path": ["body", "relay_observation_digests"], "replacement": [_repeated("9"), _repeated("a")], "expected": "reject"},
        {"name": "insufficient-confirmation", "target": "signed_finality_evidence", "path": ["body", "relay_confirmation_depth"], "replacement": 1, "expected": "reject"},
        {"name": "insufficient-sponsorship-confirmation", "target": "signed_finality_evidence",
         "path": ["body", "sponsorship_transaction_evidence", "confirmation_depth"],
         "replacement": 1, "expected": "reject"},
        {"name": "zero-sponsorship-confirmation", "target": "signed_finality_evidence",
         "path": ["body", "sponsorship_transaction_evidence", "confirmation_depth"],
         "replacement": 0, "expected": "reject"},
        {"name": "boolean-confirmation-depth", "target": "signed_finality_evidence",
         "path": ["body", "relay_confirmation_depth"], "replacement": True,
         "resign_as": "provider_evidence", "expected": "reject"},
        {"name": "combined-partial-false-full-success",
         "target": "signed_combined_partial_corroborated_evidence",
         "path": ["body", "outcome"], "replacement": "corroborated_success",
         "resign_as": "provider_evidence", "expected": "reject"},
        {"name": "combined-partial-resolution-relay-reference",
         "target": "signed_combined_partial_corroborated_resolution",
         "path": ["body", "transaction_reference"],
         "replacement": "tx:exact", "resign_as": "provider_resolution",
         "expected": "reject"},
        {"name": "post-submit-sponsorship-only-missing-transaction-absence",
         "target": "signed_post_submit_sponsorship_only_evidence",
         "path": ["body", "transaction_absence_observations"],
         "replacement": [], "resign_as": "provider_evidence",
         "expected": "reject"},
        {"name": "post-submit-sponsorship-only-false-full-success",
         "target": "signed_post_submit_sponsorship_only_evidence",
         "path": ["body", "outcome"], "replacement": "corroborated_success",
         "resign_as": "provider_evidence", "expected": "reject"},
        {"name": "relay-only-missing-sponsorship-absence",
         "target": "signed_relay_only_evidence",
         "path": ["body", "sponsorship_absence_observations"],
         "replacement": [], "resign_as": "provider_evidence",
         "expected": "reject"},
        {"name": "relay-only-false-full-success",
         "target": "signed_relay_only_evidence",
         "path": ["body", "outcome"], "replacement": "corroborated_success",
         "resign_as": "provider_evidence", "expected": "reject"},
        {"name": "relay-only-resolution-sponsorship-reference",
         "target": "signed_relay_only_resolution",
         "path": ["body", "transaction_reference"],
         "replacement": "sponsorship:exact",
         "resign_as": "provider_resolution", "expected": "reject"},
        {"name": "absence-proof-bundle-digest-substitution",
         "target": "signed_absence_finality_evidence",
         "path": ["body", "absence_proof_bundle_digest"],
         "replacement": _repeated("f"), "resign_as": "provider_evidence",
         "expected": "reject"},
        {"name": "absence-proof-bundle-bytes-substitution",
         "target": "signed_absence_finality_evidence",
         "path": ["body", "absence_proof_bundle"],
         "replacement": _b64(canonical_cbor({"schema_version": 1})),
         "resign_as": "provider_evidence", "expected": "reject"},
        {"name": "absence-proof-bundle-over-128-kib",
         "target": "signed_absence_finality_evidence",
         "path": ["body", "absence_proof_bundle"],
         "replacement": _b64(b"x" * (MAX_ABSENCE_PROOF_BUNDLE_BYTES + 1)),
         "resign_as": "provider_evidence", "expected": "reject"},
        {"name": "absence-proof-bundle-scope-substitution",
         "target": "relay_only_absence_proof_bundle",
         "path": ["proof_scope"], "replacement": "dual",
         "expected": "reject"},
        {"name": "absence-proof-profile-substitution",
         "target": "relay_only_absence_proof_bundle",
         "path": ["proof_profile_uri"],
         "replacement": "tos.unknown-absence-verifier.v1",
         "expected": "reject"},
        {"name": "absence-nested-observation-profile-substitution",
         "target": "relay_only_absence_proof_bundle",
         "path": ["sponsorship_absence_observations", 0,
                  "observation_evidence_profile_uri"],
         "replacement": TOS_RPC_ABSENCE_PROFILE_URI,
         "expected": "reject"},
        {"name": "absence-mixed-nested-snapshot-digest",
         "target": "relay_only_absence_proof_bundle",
         "path": ["sponsorship_absence_observations", 0,
                  "observation_evidence_profile_digest"],
         "replacement": _repeated("f"),
         "expected": "reject"},
        {"name": "absence-proof-payload-digest-substitution",
         "target": "relay_only_absence_proof_bundle",
         "path": ["proof_payload_digest"], "replacement": _repeated("f"),
         "expected": "reject"},
        {"name": "stock-rpc-absence-false-validator-class",
         "target": "relay_only_absence_proof_bundle",
         "path": ["sponsorship_absence_observations", 0,
                  "terminal_evidence_class"],
         "replacement": "validator_finality", "expected": "reject"},
        {"name": "terminal-without-evidence", "target": "signed_resolution", "path": ["body", "evidence_set_digest"], "replacement": _repeated("0"), "expected": "reject"},
        {"name": "resolution-assurance-downgrade", "target": "signed_resolution",
         "path": ["body", "assurance_level"], "replacement": "trusted-local",
         "resign_as": "provider_resolution", "expected": "reject"},
        {"name": "boolean-resolution-revision", "target": "signed_resolution",
         "path": ["body", "state_revision"], "replacement": True,
         "resign_as": "provider_resolution", "expected": "reject"},
        {"name": "absence-missing-client-transaction-set", "target": "signed_absence_finality_evidence",
         "path": ["body", "transaction_absence_observations"], "replacement": [], "expected": "reject"},
        {"name": "absence-cross-kind-relabel", "target": "signed_absence_finality_evidence",
         "path": ["body", "transaction_absence_observations", 0, "observation_kind"],
         "replacement": "sponsorship_action", "expected": "reject"},
        {"name": "absence-sponsorship-terminal-profile-substitution",
         "target": "signed_absence_finality_evidence",
         "path": ["body", "sponsorship_absence_observations", 0,
                  "terminal_profile_uri"],
         "replacement": "tos.depth-quorum.v1", "expected": "reject"},
        {"name": "absence-relay-terminal-class-downgrade",
         "target": "signed_absence_finality_evidence",
         "path": ["body", "transaction_absence_observations", 0,
                  "terminal_evidence_class"],
         "replacement": "validator_finality", "expected": "reject"},
        {"name": "corroborated-absence-false-finalized-outcome",
         "target": "signed_absence_finality_evidence",
         "path": ["body", "outcome"], "replacement": "finalized_absent",
         "resign_as": "provider_evidence", "expected": "reject"},
        {"name": "point-in-time-sponsorship-absence", "target": "signed_absence_finality_evidence",
         "path": ["body", "sponsorship_absence_observations", 0, "conclusion"],
         "replacement": "absent", "expected": "reject"},
        {"name": "sponsorship-absence-before-expiry-and-reorg", "target": "signed_absence_finality_evidence",
         "path": ["body", "sponsorship_absence_observations"],
         "replacement": sponsorship_absence_before_terminal_window,
         "resign_as": "provider_evidence",
         "expected": "reject"},
        {"name": "client-transaction-absence-before-expiry-and-reorg",
         "target": "signed_absence_finality_evidence",
         "path": ["body", "transaction_absence_observations"],
         "replacement": transaction_absence_before_terminal_window,
         "resign_as": "provider_evidence",
         "expected": "reject"},
        {"name": "absence-sponsorship-action-substitution", "target": "signed_absence_finality_evidence",
         "path": ["body", "sponsorship_stable_action_id"], "replacement": _repeated("f"), "expected": "reject"},
        {"name": "absence-proof-reuse-across-side-effects", "target": "signed_absence_finality_evidence",
         "path": ["body", "transaction_absence_observations", 0, "observation_digest"],
         "replacement": sponsorship_absence[0]["observation_digest"], "expected": "reject"},
        {"name": "absence-resolution-identity-substitution", "target": "signed_absence_resolution",
         "path": ["body", "sponsorship_exact_request_digest"], "replacement": _repeated("e"), "expected": "reject"},
    ]
    decisions = [
        {"name": "combined-partial-client-corroborated-sponsorship",
         "operation": "terminal_outcome", "mode": "sponsor_and_relay",
         "relay_result": "none", "relay_class": "provider_corroborated",
         "sponsorship_result": "success",
         "sponsorship_class": "client_corroborated",
         "expected": "corroborated_sponsorship_only"},
        {"name": "combined-partial-validator-finalized-sponsorship",
         "operation": "terminal_outcome", "mode": "sponsor_and_relay",
         "relay_result": "none", "relay_class": "validator_finality",
         "sponsorship_result": "success",
         "sponsorship_class": "validator_finality",
         "expected": "finalized_sponsorship_only"},
        {"name": "combined-post-submit-sponsorship-only-lower-relay",
         "operation": "terminal_outcome", "mode": "sponsor_and_relay",
         "relay_result": "absent", "relay_class": "provider_corroborated",
         "sponsorship_result": "success",
         "sponsorship_class": "validator_finality",
         "expected": "corroborated_sponsorship_only"},
        {"name": "combined-post-submit-sponsorship-only-all-validator",
         "operation": "terminal_outcome", "mode": "sponsor_and_relay",
         "relay_result": "expired", "relay_class": "validator_finality",
         "sponsorship_result": "success",
         "sponsorship_class": "validator_finality",
         "expected": "finalized_sponsorship_only"},
        {"name": "combined-relay-only-lower-sponsorship-absence",
         "operation": "terminal_outcome", "mode": "sponsor_and_relay",
         "relay_result": "success", "relay_class": "validator_finality",
         "sponsorship_result": "expired",
         "sponsorship_class": "client_corroborated",
         "expected": "corroborated_relay_only"},
        {"name": "combined-relay-only-all-validator",
         "operation": "terminal_outcome", "mode": "sponsor_and_relay",
         "relay_result": "success", "relay_class": "validator_finality",
         "sponsorship_result": "expired",
         "sponsorship_class": "validator_finality",
         "expected": "finalized_relay_only"},
        {"name": "combined-whole-negative-mixed-class",
         "operation": "terminal_outcome", "mode": "sponsor_and_relay",
         "relay_result": "invalidated", "relay_class": "validator_finality",
         "sponsorship_result": "expired",
         "sponsorship_class": "client_corroborated",
         "expected": "corroborated_invalidated"},
        {"name": "combined-full-lower-sponsorship",
         "operation": "terminal_outcome", "mode": "sponsor_and_relay",
         "relay_result": "success", "relay_class": "validator_finality",
         "sponsorship_result": "success",
         "sponsorship_class": "client_corroborated",
         "expected": "corroborated_success"},
        {"name": "combined-full-lower-relay",
         "operation": "terminal_outcome", "mode": "sponsor_and_relay",
         "relay_result": "success", "relay_class": "provider_corroborated",
         "sponsorship_result": "success",
         "sponsorship_class": "validator_finality",
         "expected": "corroborated_success"},
        {"name": "combined-full-validator-finality",
         "operation": "terminal_outcome", "mode": "sponsor_and_relay",
         "relay_result": "success", "relay_class": "validator_finality",
         "sponsorship_result": "success",
         "sponsorship_class": "validator_finality",
         "expected": "finalized_success"},
        {"name": "relay-only-validator-negative",
         "operation": "terminal_outcome", "mode": "relay_exact",
         "relay_result": "absent", "relay_class": "validator_finality",
         "sponsorship_result": "none", "expected": "finalized_absent"},
        {"name": "relay-only-provider-corroborated-negative",
         "operation": "terminal_outcome", "mode": "relay_exact",
         "relay_result": "absent", "relay_class": "provider_corroborated",
         "sponsorship_result": "none", "expected": "corroborated_absent"},
        {"name": "relay-only-negative-without-evidence",
         "operation": "terminal_outcome", "mode": "relay_exact",
         "relay_result": "none", "relay_class": "validator_finality",
         "sponsorship_result": "none", "expected": "reject"},
        {"name": "credential-only-takeover", "operation": "credential_takeover", "expected": "same_execution_digest"},
        {"name": "admission-exact-recovery", "operation": "admission_recovery",
         "stored": True, "exact_lookup": True, "expected": "same_receipt"},
        {"name": "admission-route-conflict", "operation": "admission_recovery",
         "stored": True, "exact_lookup": False, "expected": "conflict"},
        {"name": "admitted-broadcast-drains-after-takeover", "operation": "admission_stage",
         "stage_mask": ["broadcast", "sponsorship"], "stage": "broadcast",
         "receipt_consumed_before_deadline": True, "writer_taken_over": True,
         "expected": "drain_exact"},
        {"name": "unadmitted-stage-blocked-after-takeover", "operation": "admission_stage",
         "stage_mask": ["sponsorship"], "stage": "broadcast",
         "receipt_consumed_before_deadline": True, "writer_taken_over": True,
         "expected": "block"},
        {"name": "late-receipt-consumption-blocked", "operation": "admission_stage",
         "stage_mask": ["broadcast"], "stage": "broadcast",
         "receipt_consumed_before_deadline": False, "writer_taken_over": False,
         "expected": "block"},
        {"name": "exact-retry", "operation": "journal_compare", "network": "same", "exact_request": "same", "signed_bytes": "same", "execution": "same", "provider": "same", "expected": "exact_retry"},
        {"name": "different-network-conflict", "operation": "journal_compare", "network": "different", "exact_request": "same", "signed_bytes": "same", "execution": "different", "provider": "same", "expected": "conflict"},
        {"name": "different-request-conflict", "operation": "journal_compare", "network": "same", "exact_request": "different", "signed_bytes": "same", "execution": "same", "provider": "same", "expected": "conflict"},
        {"name": "different-bytes-conflict", "operation": "journal_compare", "network": "same", "exact_request": "same", "signed_bytes": "different", "execution": "same", "provider": "same", "expected": "conflict"},
        {"name": "different-execution-conflict", "operation": "journal_compare", "network": "same", "exact_request": "same", "signed_bytes": "same", "execution": "different", "provider": "same", "expected": "conflict"},
        {"name": "provider-failover-keeps-original", "operation": "journal_compare", "network": "same", "exact_request": "same", "signed_bytes": "same", "execution": "different", "provider": "different", "expected": "independent_provider_route"},
        {"name": "relay-only-route-head-successor", "operation": "route_transition",
         "mode": "relay_exact", "current_attempt": 1, "candidate_attempt": 2,
         "assurance_level": "autonomous-decentralized",
         "predecessor": "current", "transaction_identity": "same",
         "stable_action": "same", "exact_request": "same", "network": "same",
         "policy_revision": "same", "mandate": "same", "approval": "same",
         "authority_domain": "same",
         "expected": "admit_successor"},
        {"name": "single-provider-route-head-successor", "operation": "route_transition",
         "mode": "relay_exact", "current_attempt": 1, "candidate_attempt": 2,
         "assurance_level": "authorized-single-provider",
         "predecessor": "current", "transaction_identity": "same",
         "stable_action": "same", "exact_request": "same", "network": "same",
         "policy_revision": "same", "mandate": "same", "approval": "same",
         "authority_domain": "same", "expected": "conflict"},
        {"name": "relay-successor-different-boc-conflict", "operation": "route_transition",
         "mode": "relay_exact", "current_attempt": 1, "candidate_attempt": 2,
         "predecessor": "current", "transaction_identity": "different",
         "stable_action": "same", "exact_request": "same", "network": "same",
         "policy_revision": "same", "mandate": "same", "approval": "same",
         "authority_domain": "same",
         "expected": "conflict"},
        {"name": "sponsorship-successor-disabled", "operation": "route_transition",
         "mode": "sponsor_and_relay", "current_attempt": 1, "candidate_attempt": 2,
         "predecessor": "current", "transaction_identity": "same",
         "stable_action": "same", "exact_request": "same", "network": "same",
         "policy_revision": "same", "mandate": "same", "approval": "same",
         "authority_domain": "same",
         "expected": "conflict"},
        {"name": "relay-successor-policy-revision-conflict", "operation": "route_transition",
         "mode": "relay_exact", "current_attempt": 1, "candidate_attempt": 2,
         "predecessor": "current", "transaction_identity": "same",
         "stable_action": "same", "exact_request": "same", "network": "same",
         "policy_revision": "different", "mandate": "same", "approval": "same",
         "authority_domain": "same", "expected": "conflict"},
        {"name": "relay-successor-mandate-conflict", "operation": "route_transition",
         "mode": "relay_exact", "current_attempt": 1, "candidate_attempt": 2,
         "predecessor": "current", "transaction_identity": "same",
         "stable_action": "same", "exact_request": "same", "network": "same",
         "policy_revision": "same", "mandate": "different", "approval": "same",
         "authority_domain": "same", "expected": "conflict"},
        {"name": "relay-successor-approval-conflict", "operation": "route_transition",
         "mode": "relay_exact", "current_attempt": 1, "candidate_attempt": 2,
         "predecessor": "current", "transaction_identity": "same",
         "stable_action": "same", "exact_request": "same", "network": "same",
         "policy_revision": "same", "mandate": "same", "approval": "different",
         "authority_domain": "same", "expected": "conflict"},
        {"name": "relay-successor-authority-domain-conflict", "operation": "route_transition",
         "mode": "relay_exact", "current_attempt": 1, "candidate_attempt": 2,
         "predecessor": "current", "transaction_identity": "same",
         "stable_action": "same", "exact_request": "same", "network": "same",
         "policy_revision": "same", "mandate": "same", "approval": "same",
         "authority_domain": "different", "expected": "conflict"},
        {"name": "ambiguous-query-before-retry", "operation": "ambiguity", "state": "submitted", "queried": True, "safe_to_rebroadcast_exact": True, "unexpired": True, "expected": "rebroadcast_exact"},
        {"name": "ambiguous-without-query", "operation": "ambiguity", "state": "submitted", "queried": False, "safe_to_rebroadcast_exact": False, "unexpired": True, "expected": "wait"},
        {"name": "stale-writer", "operation": "writer", "high_water": 2, "candidate": 1, "expected": "reject_stale"},
        {"name": "same-network-id-different-genesis", "operation": "network_authority", "network_id": "tos:testnet", "network_domain": "different", "expected": "reject_domain_replay"},
        {"name": "backdated-provider-key-without-terminal-anchor", "operation": "evidence_authority", "historical_key": "revoked", "terminal_commitment": False, "expected": "reject_production"},
        {"name": "special-purpose-endpoint-literals", "operation": "endpoint_policy",
         "endpoints": ["https://0.0.0.1/quote", "https://240.0.0.1/quote",
                       "https://[100::1]/quote", "https://[2001::1]/quote",
                       "https://[64:ff9b:1::1]/quote"], "expected": "reject_all"},
        {"name": "canonical-action-request-byte-boundary", "operation": "action_request_boundary",
         "maximum_raw_bytes": MAX_ACTION_BYTES, "maximum_base64_bytes": 256 << 10,
         "expected": "exact_boundary"},
        {"name": "combined-validator-sponsor-not-final", "operation": "sponsor_gate",
         "mode": "sponsor_and_relay", "release_class": "validator_finality",
         "sponsor_finalized": False, "observation_verified": False,
         "fresh_recheck": True, "expected": "remain_prepared"},
        {"name": "combined-validator-sponsor-final", "operation": "sponsor_gate",
         "mode": "sponsor_and_relay", "release_class": "validator_finality",
         "sponsor_finalized": True, "observation_verified": False,
         "fresh_recheck": True, "expected": "submit_exact"},
        {"name": "combined-observed-release-is-nonterminal", "operation": "sponsor_gate",
         "mode": "sponsor_and_relay", "release_class": "observed_unproven",
         "sponsor_finalized": False, "observation_verified": True,
         "fresh_recheck": True, "expected": "submit_exact_nonterminal"},
        {"name": "combined-observed-without-fresh-recheck", "operation": "sponsor_gate",
         "mode": "sponsor_and_relay", "release_class": "observed_unproven",
         "sponsor_finalized": False, "observation_verified": True,
         "fresh_recheck": False, "expected": "remain_prepared"},
        {"name": "sponsor-failover-unknown", "operation": "sponsor_failover", "prior_outcome": "unknown", "expected": "wait"},
        {"name": "sponsor-successor-after-relay-only-forbidden",
         "operation": "sponsor_failover",
         "prior_outcome": "corroborated_relay_only", "expected": "wait"},
        {"name": "sponsor-successor-after-terminal-absence-forbidden",
         "operation": "sponsor_failover",
         "prior_outcome": "finalized_absent", "expected": "wait"},
        {"name": "accepted-reorg", "operation": "state_transition", "from": "accepted", "to": "submitted", "corroborated_reorg": True, "expected": "allow"},
        {"name": "two-independent-providers", "operation": "provider_set", "providers": ["agent:provider-a", "agent:provider-b"], "operator_domains": ["operator:a", "operator:b"], "expected": "eligible"},
        {"name": "two-provider-ids-one-operator", "operation": "provider_set", "providers": ["agent:provider-a", "agent:provider-b"], "operator_domains": ["operator:a", "operator:a"], "expected": "reject_not_independent"},
        {"name": "within-rate-and-exposure", "operation": "admission_limits", "rate_remaining": 1, "exposure_after": "100", "maximum_outstanding": "100", "expected": "admit"},
        {"name": "rate-limit-exhausted", "operation": "admission_limits", "rate_remaining": 0, "exposure_after": "100", "maximum_outstanding": "100", "expected": "reject_limit"},
        {"name": "aggregate-exposure-exhausted", "operation": "admission_limits", "rate_remaining": 1, "exposure_after": "101", "maximum_outstanding": "100", "expected": "reject_limit"},
        {"name": "sponsorship-window-satisfiable", "operation": "time_window", "created_at": 100, "valid_until": 161, "maximum_resolution_seconds": 30, "safety_seconds": 30, "expected": "satisfiable"},
        {"name": "sponsorship-window-boundary-rejected", "operation": "time_window", "created_at": 100, "valid_until": 160, "maximum_resolution_seconds": 30, "safety_seconds": 30, "expected": "unsatisfiable"},
        {"name": "trusted-local-relay-ready-without-prior-campaign",
         "operation": "capability_readiness", "mode": "relay_exact",
         "assurance_level": "trusted-local", "owner_enabled": True,
         "prior_production_campaign_completed": False,
         "advertised_modes": ["relay_exact"],
         "advertised_assurance_levels": ["trusted-local"],
         "capabilities": sorted(BASE_READINESS_CAPABILITIES |
                                ASSURANCE_READINESS_CAPABILITIES["trusted-local"]),
         "provider_ids": ["agent:local-provider"],
         "operator_domains": ["operator:local"], "expected": "ready"},
        {"name": "authorized-single-provider-relay-ready-without-prior-deployment",
         "operation": "capability_readiness", "mode": "relay_exact",
         "assurance_level": "authorized-single-provider", "owner_enabled": True,
         "prior_production_deployment": False,
         "advertised_modes": ["relay_exact"],
         "advertised_assurance_levels": ["authorized-single-provider"],
         "capabilities": sorted(BASE_READINESS_CAPABILITIES |
                                ASSURANCE_READINESS_CAPABILITIES["authorized-single-provider"]),
         "provider_ids": ["agent:provider-a"],
         "operator_domains": ["operator:a"], "expected": "ready"},
        {"name": "autonomous-relay-ready-from-current-independent-capabilities",
         "operation": "capability_readiness", "mode": "relay_exact",
         "assurance_level": "autonomous-decentralized", "owner_enabled": True,
         "prior_production_campaign_completed": False,
         "advertised_modes": ["relay_exact"],
         "advertised_assurance_levels": ["autonomous-decentralized"],
         "capabilities": sorted(BASE_READINESS_CAPABILITIES |
                                ASSURANCE_READINESS_CAPABILITIES["autonomous-decentralized"] |
                                {"route_chain_recovery"}),
         "provider_ids": ["agent:provider-a", "agent:provider-b"],
         "operator_domains": ["operator:a", "operator:b"], "expected": "ready"},
        {"name": "autonomous-relay-one-operator-not-ready",
         "operation": "capability_readiness", "mode": "relay_exact",
         "assurance_level": "autonomous-decentralized", "owner_enabled": True,
         "advertised_modes": ["relay_exact"],
         "advertised_assurance_levels": ["autonomous-decentralized"],
         "capabilities": sorted(BASE_READINESS_CAPABILITIES |
                                ASSURANCE_READINESS_CAPABILITIES["autonomous-decentralized"] |
                                {"route_chain_recovery"}),
         "provider_ids": ["agent:provider-a", "agent:provider-b"],
         "operator_domains": ["operator:a", "operator:a"], "expected": "not_ready"},
        {"name": "trusted-sponsorship-ready-with-bounded-rpc-corroboration",
         "operation": "capability_readiness", "mode": "sponsor_only",
         "assurance_level": "trusted-local", "owner_enabled": True,
         "release_descriptor_pinned": True, "release_descriptor_matches_preflight": True,
         "release_snapshot_frozen": True,
         "prior_production_campaign_completed": False,
         "advertised_modes": ["sponsor_only"],
         "advertised_assurance_levels": ["trusted-local"],
         "capabilities": sorted(BASE_READINESS_CAPABILITIES |
                                ASSURANCE_READINESS_CAPABILITIES["trusted-local"] |
                                SPONSORSHIP_READINESS_CAPABILITIES |
                                {"bounded_rpc_corroboration"}),
         "provider_ids": ["agent:local-provider"],
         "operator_domains": ["operator:local"], "expected": "ready"},
        {"name": "authorized-sponsor-only-ready-with-bounded-rpc-corroboration",
         "operation": "capability_readiness", "mode": "sponsor_only",
         "assurance_level": "authorized-single-provider", "owner_enabled": True,
         "release_descriptor_pinned": True, "release_descriptor_matches_preflight": True,
         "release_snapshot_frozen": True,
         "prior_production_deployment": False,
         "advertised_modes": ["sponsor_only"],
         "advertised_assurance_levels": ["authorized-single-provider"],
         "capabilities": sorted(BASE_READINESS_CAPABILITIES |
                                ASSURANCE_READINESS_CAPABILITIES["authorized-single-provider"] |
                                SPONSORSHIP_READINESS_CAPABILITIES |
                                {"bounded_rpc_corroboration"}),
         "provider_ids": ["agent:provider-a"],
         "operator_domains": ["operator:a"], "expected": "ready"},
        {"name": "autonomous-sponsor-only-ready-with-portable-finality",
         "operation": "capability_readiness", "mode": "sponsor_only",
         "assurance_level": "autonomous-decentralized", "owner_enabled": True,
         "release_descriptor_pinned": True, "release_descriptor_matches_preflight": True,
         "release_snapshot_frozen": True,
         "prior_production_campaign_completed": False,
         "advertised_modes": ["sponsor_only"],
         "advertised_assurance_levels": ["autonomous-decentralized"],
         "capabilities": sorted(BASE_READINESS_CAPABILITIES |
                                ASSURANCE_READINESS_CAPABILITIES["autonomous-decentralized"] |
                                SPONSORSHIP_READINESS_CAPABILITIES |
                                {"portable_sponsorship_finality"}),
         "provider_ids": ["agent:provider-a", "agent:provider-b"],
         "operator_domains": ["operator:a", "operator:b"], "expected": "ready"},
        {"name": "trusted-combined-ready-with-bounded-rpc-corroboration",
         "operation": "capability_readiness", "mode": "sponsor_and_relay",
         "assurance_level": "trusted-local", "owner_enabled": True,
         "release_descriptor_pinned": True, "release_descriptor_matches_preflight": True,
         "release_snapshot_frozen": True,
         "prior_production_campaign_completed": False,
         "advertised_modes": ["sponsor_and_relay"],
         "advertised_assurance_levels": ["trusted-local"],
         "capabilities": sorted(BASE_READINESS_CAPABILITIES |
                                ASSURANCE_READINESS_CAPABILITIES["trusted-local"] |
                                SPONSORSHIP_READINESS_CAPABILITIES |
                                {"bounded_rpc_corroboration"}),
         "provider_ids": ["agent:local-provider"],
         "operator_domains": ["operator:local"], "expected": "ready"},
        {"name": "authorized-combined-ready-with-bounded-rpc-corroboration",
         "operation": "capability_readiness", "mode": "sponsor_and_relay",
         "assurance_level": "authorized-single-provider", "owner_enabled": True,
         "release_descriptor_pinned": True, "release_descriptor_matches_preflight": True,
         "release_snapshot_frozen": True,
         "prior_production_deployment": False,
         "advertised_modes": ["sponsor_and_relay"],
         "advertised_assurance_levels": ["authorized-single-provider"],
         "capabilities": sorted(BASE_READINESS_CAPABILITIES |
                                ASSURANCE_READINESS_CAPABILITIES["authorized-single-provider"] |
                                SPONSORSHIP_READINESS_CAPABILITIES |
                                {"bounded_rpc_corroboration"}),
         "provider_ids": ["agent:provider-a"],
         "operator_domains": ["operator:a"], "expected": "ready"},
        {"name": "autonomous-combined-ready-with-portable-finality",
         "operation": "capability_readiness", "mode": "sponsor_and_relay",
         "assurance_level": "autonomous-decentralized", "owner_enabled": True,
         "release_descriptor_pinned": True, "release_descriptor_matches_preflight": True,
         "release_snapshot_frozen": True,
         "prior_production_campaign_completed": False,
         "advertised_modes": ["sponsor_and_relay"],
         "advertised_assurance_levels": ["autonomous-decentralized"],
         "capabilities": sorted(BASE_READINESS_CAPABILITIES |
                                ASSURANCE_READINESS_CAPABILITIES["autonomous-decentralized"] |
                                SPONSORSHIP_READINESS_CAPABILITIES |
                                {"portable_sponsorship_finality"}),
         "provider_ids": ["agent:provider-a", "agent:provider-b"],
         "operator_domains": ["operator:a", "operator:b"], "expected": "ready"},
        {"name": "sponsorship-without-corroboration-or-finality-not-ready",
         "operation": "capability_readiness", "mode": "sponsor_only",
         "assurance_level": "trusted-local", "owner_enabled": True,
         "advertised_modes": ["sponsor_only"],
         "advertised_assurance_levels": ["trusted-local"],
         "capabilities": sorted(BASE_READINESS_CAPABILITIES |
                                ASSURANCE_READINESS_CAPABILITIES["trusted-local"] |
                                SPONSORSHIP_READINESS_CAPABILITIES),
         "provider_ids": ["agent:local-provider"],
         "operator_domains": ["operator:local"], "expected": "not_ready"},
        {"name": "autonomous-sponsorship-with-rpc-only-not-ready",
         "operation": "capability_readiness", "mode": "sponsor_and_relay",
         "assurance_level": "autonomous-decentralized", "owner_enabled": True,
         "advertised_modes": ["sponsor_and_relay"],
         "advertised_assurance_levels": ["autonomous-decentralized"],
         "capabilities": sorted(BASE_READINESS_CAPABILITIES |
                                ASSURANCE_READINESS_CAPABILITIES["autonomous-decentralized"] |
                                SPONSORSHIP_READINESS_CAPABILITIES |
                                {"bounded_rpc_corroboration"}),
         "provider_ids": ["agent:provider-a", "agent:provider-b"],
         "operator_domains": ["operator:a", "operator:b"], "expected": "not_ready"},
        {"name": "observed-release-without-terminal-finality-not-ready",
         "operation": "capability_readiness", "mode": "sponsor_and_relay",
         "assurance_level": "authorized-single-provider", "owner_enabled": True,
         "release_descriptor_pinned": True, "release_descriptor_matches_preflight": True,
         "release_snapshot_frozen": True,
         "advertised_modes": ["sponsor_and_relay"],
         "advertised_assurance_levels": ["authorized-single-provider"],
         "capabilities": sorted(BASE_READINESS_CAPABILITIES |
                                ASSURANCE_READINESS_CAPABILITIES["authorized-single-provider"] |
                                (SPONSORSHIP_READINESS_CAPABILITIES -
                                 {"terminal_sponsorship_finality_evidence"}) |
                                {"bounded_rpc_corroboration"}),
         "provider_ids": ["agent:provider-a"],
         "operator_domains": ["operator:a"], "expected": "not_ready"},
        {"name": "autonomous-with-rollbackable-action-authority-not-ready",
         "operation": "capability_readiness", "mode": "relay_exact",
         "assurance_level": "autonomous-decentralized", "owner_enabled": True,
         "advertised_modes": ["relay_exact"],
         "advertised_assurance_levels": ["autonomous-decentralized"],
         "capabilities": sorted(BASE_READINESS_CAPABILITIES |
                                (ASSURANCE_READINESS_CAPABILITIES["autonomous-decentralized"] -
                                 {"rollback_resistant_side_effect_admission"}) |
                                {"route_chain_recovery"}),
         "provider_ids": ["agent:provider-a", "agent:provider-b"],
         "operator_domains": ["operator:a", "operator:b"], "expected": "not_ready"},
        {"name": "autonomous-with-rollbackable-provider-journal-not-ready",
         "operation": "capability_readiness", "mode": "sponsor_and_relay",
         "assurance_level": "autonomous-decentralized", "owner_enabled": True,
         "release_descriptor_pinned": True, "release_descriptor_matches_preflight": True,
         "release_snapshot_frozen": True,
         "advertised_modes": ["sponsor_and_relay"],
         "advertised_assurance_levels": ["autonomous-decentralized"],
         "capabilities": sorted(BASE_READINESS_CAPABILITIES |
                                (ASSURANCE_READINESS_CAPABILITIES["autonomous-decentralized"] -
                                 {"rollback_resistant_provider_journal"}) |
                                SPONSORSHIP_READINESS_CAPABILITIES |
                                {"portable_sponsorship_finality"}),
         "provider_ids": ["agent:provider-a", "agent:provider-b"],
         "operator_domains": ["operator:a", "operator:b"], "expected": "not_ready"},
        {"name": "autonomous-with-rollbackable-route-journal-not-ready",
         "operation": "capability_readiness", "mode": "relay_exact",
         "assurance_level": "autonomous-decentralized", "owner_enabled": True,
         "advertised_modes": ["relay_exact"],
         "advertised_assurance_levels": ["autonomous-decentralized"],
         "capabilities": sorted(BASE_READINESS_CAPABILITIES |
                                (ASSURANCE_READINESS_CAPABILITIES["autonomous-decentralized"] -
                                 {"rollback_resistant_route_journal"}) |
                                {"route_chain_recovery"}),
         "provider_ids": ["agent:provider-a", "agent:provider-b"],
         "operator_domains": ["operator:a", "operator:b"], "expected": "not_ready"},
        {"name": "observed-release-config-rotated-after-preflight-not-ready",
         "operation": "capability_readiness", "mode": "sponsor_and_relay",
         "assurance_level": "authorized-single-provider", "owner_enabled": True,
         "release_descriptor_pinned": True, "release_descriptor_matches_preflight": False,
         "release_snapshot_frozen": True,
         "advertised_modes": ["sponsor_and_relay"],
         "advertised_assurance_levels": ["authorized-single-provider"],
         "capabilities": sorted(BASE_READINESS_CAPABILITIES |
                                ASSURANCE_READINESS_CAPABILITIES["authorized-single-provider"] |
                                SPONSORSHIP_READINESS_CAPABILITIES |
                                {"bounded_rpc_corroboration"}),
         "provider_ids": ["agent:provider-a"],
         "operator_domains": ["operator:a"], "expected": "not_ready"},
    ]
    return {
        "schema": "tos.agent-relay-service-conformance.v1",
        "profile_uri": "tos.agent-service.transaction-relay.v1",
        "sponsorship_payment_commitment_vector": {
            "tag_uint32": SPONSORSHIP_PAYMENT_COMMITMENT_TAG,
            "tag_hex": "53504e31",
            "agreement_payment_request_digest":
                published_commitment_request_digest,
            "stable_action_id": published_commitment_action_id,
            "cell_bit_length": 544,
            "reference_count": 0,
            "ordinary_level_zero": True,
            "cell_representation_hex":
                published_commitment_representation.hex(),
            "cell_hash": published_commitment_hash,
        },
        "rpc_corroboration_profile_vector": {
            "digest_domain": "tosctl.agreement-payment-rpc-corroboration-profile.v1\\0",
            "descriptor": rpc_corroboration_profile_descriptor,
            "compact_json_hex": rpc_profile_json.hex(),
            "digest": rpc_profile_digest,
        },
        "absence_proof_profile_vector": {
            "digest_domain": "tos.agent-relay-absence-proof-profile.v1",
            "descriptor": absence_profile_descriptor,
            "digest": absence_profile_digest,
        },
        "content_types": {
            "service_profile": "application/vnd.tos.agent-relay-service-profile.v1+cbor",
            "quote_request": "application/vnd.tos.agent-relay-quote-request.v1+cbor",
            "provider_quote": "application/vnd.tos.agent-relay-provider-quote.v1+cbor",
            "execution_request": "application/vnd.tos.agent-relay-execution-request.v1+cbor",
            "side_effect_admission_request": "application/vnd.tos.agent-relay-side-effect-admission-request.v1+cbor",
            "side_effect_admission_receipt": "application/vnd.tos.agent-relay-side-effect-admission-receipt.v1+cbor",
            "resolve_admission_call": "application/vnd.tos.agent-relay-resolve-admission-call.v1+cbor",
            "resolve_admission_result": "application/vnd.tos.agent-relay-resolve-admission-result.v1+cbor",
            "resolution": "application/vnd.tos.agent-relay-resolution.v1+cbor",
            "sponsorship_credit_observation": "application/vnd.tos.agent-relay-sponsorship-credit-observation.v1+cbor",
            "absence_proof_bundle": "application/vnd.tos.agent-relay-absence-proof-bundle.v1+cbor",
            "finality_evidence": "application/vnd.tos.agent-relay-finality-evidence.v1+cbor",
            "agreement_binding": "application/vnd.tos.agent-relay-agreement-binding.v1+cbor",
            "quote_call": "application/vnd.tos.agent-relay-quote-call.v1+cbor",
            "quote_result": "application/vnd.tos.agent-relay-quote-result.v1+cbor",
            "submit_call": "application/vnd.tos.agent-relay-submit-call.v1+cbor",
            "submit_result": "application/vnd.tos.agent-relay-submit-result.v1+cbor",
            "resolve_call": "application/vnd.tos.agent-relay-resolve-call.v1+cbor",
            "resolve_result": "application/vnd.tos.agent-relay-resolve-result.v1+cbor",
            "evidence_call": "application/vnd.tos.agent-relay-evidence-call.v1+cbor",
            "evidence_result": "application/vnd.tos.agent-relay-evidence-result.v1+cbor",
        },
        "test_keys": {
            "warning": "deterministic conformance-only seeds; never use for value",
            "requester_seed_hex": client_seed.hex(),
            "provider_seed_hex": provider_seed.hex(),
            "authority_seed_hex": authority_seed.hex(),
        },
        "objects": objects,
        "signatures": signatures,
        "negative_mutations": negative_mutations,
        "decision_vectors": decisions,
    }


def _set_path(model: Any, path: list[Any], replacement: Any) -> None:
    cursor = model
    for part in path[:-1]:
        cursor = cursor[part]
    cursor[path[-1]] = copy.deepcopy(replacement)


def evaluate_capability_readiness(item: dict[str, Any]) -> str:
    """Evaluate one mode/assurance pair from current capabilities and config.

    Deliberately absent from this decision are deployment age, transaction
    count, a production label, or prior campaign/certification history.
    """
    mode = item.get("mode")
    assurance = item.get("assurance_level")
    if mode not in MODES or assurance not in ASSURANCE_LEVELS:
        return "not_ready"
    if not item.get("owner_enabled", False):
        return "not_ready"
    if mode not in item.get("advertised_modes", []) or assurance not in item.get("advertised_assurance_levels", []):
        return "not_ready"
    capabilities = item.get("capabilities")
    if not isinstance(capabilities, list) or capabilities != sorted(set(capabilities)):
        return "not_ready"
    required = set(BASE_READINESS_CAPABILITIES)
    required.update(ASSURANCE_READINESS_CAPABILITIES[assurance])
    if mode != "relay_exact":
        if (item.get("release_descriptor_pinned") is not True or
                item.get("release_descriptor_matches_preflight") is not True or
                item.get("release_snapshot_frozen") is not True):
            return "not_ready"
        required.update(SPONSORSHIP_READINESS_CAPABILITIES)
    if not required.issubset(capabilities):
        return "not_ready"
    if mode != "relay_exact":
        if assurance == "autonomous-decentralized":
            if "portable_sponsorship_finality" not in capabilities:
                return "not_ready"
        elif not ({"bounded_rpc_corroboration", "portable_sponsorship_finality"} &
                  set(capabilities)):
            return "not_ready"
    elif (assurance == "autonomous-decentralized" and
          "route_chain_recovery" not in capabilities):
        return "not_ready"
    if assurance == "autonomous-decentralized":
        providers = item.get("provider_ids", [])
        domains = item.get("operator_domains", [])
        if (len(providers) < 2 or len(providers) != len(domains) or
                len(set(providers)) != len(providers) or
                len(set(domains)) != len(domains)):
            return "not_ready"
    return "ready"


def verify_decisions(decisions: list[dict[str, Any]], execution: dict[str, Any]) -> None:
    for item in decisions:
        operation = item["operation"]
        if operation == "terminal_outcome":
            mode = item.get("mode")
            relay_result = item.get("relay_result")
            sponsorship_result = item.get("sponsorship_result")
            relay_class = item.get("relay_class")
            sponsorship_class = item.get("sponsorship_class")
            if (mode not in MODES or
                    relay_result not in {"none", "success", "expired",
                                         "absent", "invalidated"} or
                    sponsorship_result not in {"none", "success", "expired"}):
                actual = "reject"
            elif sponsorship_result == "success":
                if sponsorship_class not in SPONSORSHIP_TERMINAL_CLASSES:
                    actual = "reject"
                elif relay_result == "success":
                    if relay_class not in RELAY_TERMINAL_CLASSES:
                        actual = "reject"
                    else:
                        actual = ("finalized_success" if
                                  relay_class == "validator_finality" and
                                  sponsorship_class == "validator_finality"
                                  else "corroborated_success")
                elif relay_result == "none":
                    actual = ("finalized_sponsorship_only" if
                              sponsorship_class == "validator_finality" else
                              "corroborated_sponsorship_only")
                elif relay_result in {"expired", "absent", "invalidated"}:
                    if relay_class not in RELAY_TERMINAL_CLASSES:
                        actual = "reject"
                    else:
                        prefix = ("finalized_" if
                                  relay_class == "validator_finality" and
                                  sponsorship_class == "validator_finality"
                                  else "corroborated_")
                        actual = prefix + "sponsorship_only"
                else:
                    actual = "reject"
            elif sponsorship_result == "expired":
                if (mode != "sponsor_and_relay" or
                        sponsorship_class not in
                        SPONSORSHIP_TERMINAL_CLASSES or
                        relay_class not in RELAY_TERMINAL_CLASSES):
                    actual = "reject"
                else:
                    prefix = ("finalized_" if
                              relay_class == "validator_finality" and
                              sponsorship_class == "validator_finality" else
                              "corroborated_")
                    if relay_result == "success":
                        actual = prefix + "relay_only"
                    elif relay_result in {"expired", "absent", "invalidated"}:
                        actual = prefix + relay_result
                    else:
                        actual = "reject"
            elif (mode == "relay_exact" and
                  relay_result in {"expired", "absent", "invalidated"} and
                  relay_class in RELAY_TERMINAL_CLASSES):
                prefix = ("finalized_" if
                          relay_class == "validator_finality" else
                          "corroborated_")
                actual = prefix + relay_result
            else:
                actual = "reject"
        elif operation == "credential_takeover":
            takeover = copy.deepcopy(execution)
            takeover["authorized_action"]["writer_generation"] += 1
            takeover["writer_fence"]["body"]["writer_generation"] += 1
            actual = "same_execution_digest" if execution_digest(takeover) == execution_digest(execution) else "changed"
        elif operation == "admission_recovery":
            if item["stored"] and item["exact_lookup"]:
                actual = "same_receipt"
            elif item["stored"]:
                actual = "conflict"
            else:
                actual = "not_found"
        elif operation == "admission_stage":
            actual = ("drain_exact" if item["receipt_consumed_before_deadline"] and
                      item["stage"] in item["stage_mask"] else "block")
        elif operation == "journal_compare":
            if item["provider"] == "different":
                actual = "independent_provider_route"
            elif item["network"] != "same" or item["exact_request"] != "same" or item["signed_bytes"] != "same" or item["execution"] != "same":
                actual = "conflict"
            else:
                actual = "exact_retry"
        elif operation == "route_transition":
            safe = (
                item["mode"] == "relay_exact" and
                item.get("assurance_level") == "autonomous-decentralized" and
                item["candidate_attempt"] == item["current_attempt"] + 1 and
                item["predecessor"] == "current" and
                item["transaction_identity"] == "same" and
                item["stable_action"] == "same" and
                item["exact_request"] == "same" and
                item["network"] == "same" and
                item["policy_revision"] == "same" and
                item["mandate"] == "same" and
                item["approval"] == "same" and
                item["authority_domain"] == "same"
            )
            actual = "admit_successor" if safe else "conflict"
        elif operation == "ambiguity":
            actual = "rebroadcast_exact" if item["state"] in {"submitted", "accepted"} and item["queried"] and item["safe_to_rebroadcast_exact"] and item["unexpired"] else "wait"
        elif operation == "writer":
            actual = "reject_stale" if item["candidate"] < item["high_water"] else "admit"
        elif operation == "network_authority":
            actual = "reject_domain_replay" if item["network_domain"] != "same" else "admit"
        elif operation == "evidence_authority":
            actual = ("reject_production" if item["historical_key"] == "revoked" and
                      not item["terminal_commitment"] else "admit")
        elif operation == "endpoint_policy":
            rejected = 0
            for endpoint in item["endpoints"]:
                try:
                    validate_endpoint(endpoint)
                except ConformanceError:
                    rejected += 1
            actual = "reject_all" if rejected == len(item["endpoints"]) else "accepted_some"
        elif operation == "action_request_boundary":
            boundary = b"x" * item["maximum_raw_bytes"]
            encoded = _b64(boundary)
            try:
                exact_request_digest(boundary)
                decode_base64(encoded, MAX_ACTION_BYTES)
            except ConformanceError:
                boundary_ok = False
            else:
                boundary_ok = True
            try:
                exact_request_digest(boundary + b"x")
            except ConformanceError:
                over_limit_rejected = True
            else:
                over_limit_rejected = False
            actual = ("exact_boundary" if len(encoded) == item["maximum_base64_bytes"] and
                      boundary_ok and over_limit_rejected else "boundary_drift")
        elif operation == "sponsor_gate":
            if item["mode"] != "sponsor_and_relay" or not item["fresh_recheck"]:
                actual = "remain_prepared"
            elif item["release_class"] == "validator_finality" and item["sponsor_finalized"]:
                actual = "submit_exact"
            elif item["release_class"] == "observed_unproven" and item["observation_verified"]:
                actual = "submit_exact_nonterminal"
            else:
                actual = "remain_prepared"
        elif operation == "sponsor_failover":
            actual = "wait"
        elif operation == "state_transition":
            actual = "allow" if item["from"] == "accepted" and item["to"] == "submitted" and item.get("corroborated_reorg") else "reject"
        elif operation == "provider_set":
            providers = item["providers"]
            domains = item["operator_domains"]
            independent = (len(providers) >= 2 and len(providers) == len(domains) and
                           len(set(providers)) == len(providers) and len(set(domains)) == len(domains))
            actual = "eligible" if independent else "reject_not_independent"
        elif operation == "admission_limits":
            within = (item["rate_remaining"] > 0 and atomic(item["exposure_after"]) and
                      atomic(item["maximum_outstanding"]) and
                      int(item["exposure_after"]) <= int(item["maximum_outstanding"]))
            actual = "admit" if within else "reject_limit"
        elif operation == "time_window":
            satisfiable = (item["created_at"] + item["maximum_resolution_seconds"] + item["safety_seconds"] <
                           item["valid_until"])
            actual = "satisfiable" if satisfiable else "unsatisfiable"
        elif operation == "capability_readiness":
            actual = evaluate_capability_readiness(item)
        else:
            raise ConformanceError(f"unknown decision operation {operation}")
        if actual != item["expected"]:
            raise ConformanceError(f"decision vector {item['name']} mismatch: {actual}")


def verify_document(path: Path, registry_path: Path) -> None:
    document = json.loads(path.read_text(encoding="utf-8"))
    if document.get("schema") != "tos.agent-relay-service-conformance.v1":
        raise ConformanceError("relay vector schema is unknown")
    registry = load_semantic_registry(registry_path)
    expected_document = build_vectors(registry)
    if document.get("sponsorship_payment_commitment_vector") != \
            expected_document["sponsorship_payment_commitment_vector"]:
        raise ConformanceError(
            "published SPN1 sponsorship commitment vector mismatch")
    expected_content_types = expected_document["content_types"]
    if document.get("content_types") != expected_content_types:
        raise ConformanceError("relay content-type registry mismatch")
    expected_rpc_profile = expected_document["rpc_corroboration_profile_vector"]
    if document.get("rpc_corroboration_profile_vector") != expected_rpc_profile:
        raise ConformanceError("RPC corroboration profile cross-language vector mismatch")
    expected_absence_profile = expected_document["absence_proof_profile_vector"]
    if document.get("absence_proof_profile_vector") != expected_absence_profile:
        raise ConformanceError("RPC absence verifier profile cross-language vector mismatch")
    objects: dict[str, dict[str, Any]] = {}
    models: dict[str, Any] = {}
    for item in document.get("objects", []):
        name = item.get("name")
        if not isinstance(name, str) or not name or name in objects:
            raise ConformanceError("vector object name is invalid or duplicate")
        model = item["json_model"]
        encoded = bounded_canonical_cbor(model)
        if _b64(encoded) != item.get("canonical_cbor_base64"):
            raise ConformanceError(f"{name}: canonical CBOR mismatch")
        if "digest_domain" in item:
            digest_model = item.get("digest_projection", model)
            if "digest_projection" in item and _b64(bounded_canonical_cbor(digest_model)) != item.get("digest_projection_cbor_base64"):
                raise ConformanceError(f"{name}: digest projection CBOR mismatch")
            if protocol_digest(item["digest_domain"], digest_model) != item.get("digest"):
                raise ConformanceError(f"{name}: digest mismatch")
        objects[name] = item
        models[name] = copy.deepcopy(model)
    required_names = {"network", "negative_network_order", "underlying_payment_request", "sponsorship_payment_request",
                      "go_service_profile", "go_quote_request_body", "go_signed_quote_request",
                      "go_provider_quote_body", "go_signed_provider_quote",
                      "service_profile", "quote_request_body", "signed_quote_request", "provider_quote_body",
                      "signed_provider_quote", "transaction_identity", "quote_call", "quote_result", "agreement_binding", "agreement_body",
                      "admission_request", "admission_receipt_body", "signed_admission_receipt",
                      "resolve_admission_call", "resolve_admission_result", "execution_request",
                      "submit_call", "sponsorship_credit_observation",
                      "observed_unproven_resolution_body", "signed_observed_unproven_resolution",
                      "submit_result", "resolve_call", "resolve_result",
                      "evidence_call", "evidence_result",
                      "finality_evidence_body", "signed_finality_evidence",
                      "combined_partial_corroborated_evidence_body",
                      "signed_combined_partial_corroborated_evidence",
                      "combined_partial_corroborated_resolution_body",
                      "signed_combined_partial_corroborated_resolution",
                      "post_submit_sponsorship_only_absence_proof_bundle",
                      "post_submit_sponsorship_only_evidence_body",
                      "signed_post_submit_sponsorship_only_evidence",
                      "post_submit_sponsorship_only_resolution_body",
                      "signed_post_submit_sponsorship_only_resolution",
                      "relay_only_absence_proof_bundle",
                      "relay_only_evidence_body", "signed_relay_only_evidence",
                      "relay_only_resolution_body", "signed_relay_only_resolution",
                      "resolution_body", "signed_resolution",
                      "sponsorship_absence_observations", "transaction_absence_observations",
                      "sponsorship_absence_observation_1", "sponsorship_absence_observation_2",
                      "sponsorship_absence_observation_3", "transaction_absence_observation_1",
                      "transaction_absence_observation_2", "transaction_absence_observation_3",
                      "absence_finality_evidence_body", "signed_absence_finality_evidence",
                      "dual_absence_proof_bundle",
                      "invalidated_absence_finality_evidence_body",
                      "signed_invalidated_absence_finality_evidence",
                      "invalidated_dual_absence_proof_bundle",
                      "absence_resolution_body", "signed_absence_resolution"}
    if set(objects) != required_names:
        raise ConformanceError("relay vector object set is incomplete")
    for signature in document.get("signatures", []):
        body = models[signature["body_object"]]
        envelope = models[signature["envelope_object"]]
        domain = signature["message_domain"].replace("\\0", "\x00").encode("ascii")
        message = signature_message(domain, body)
        if message.hex() != signature["expected_message_hex"]:
            raise ConformanceError(f"{signature['name']}: signature message mismatch")
        if not verify_ed25519(decode_public(envelope["public_key"]), message,
                              decode_signature(envelope[signature["signature_field"]])):
            raise ConformanceError(f"{signature['name']}: signature mismatch")
    validate_bundle(models, registry)
    verify_route_chain_mutations(
        models["signed_admission_receipt"],
        bytes.fromhex(document["test_keys"]["authority_seed_hex"]),
    )
    for mutation in document.get("negative_mutations", []):
        mutated = copy.deepcopy(models)
        _set_path(mutated[mutation["target"]], mutation["path"], mutation["replacement"])
        if mutation.get("resign_as") == "provider":
            envelope = mutated[mutation["target"]]
            seed = bytes.fromhex(document["test_keys"]["provider_seed_hex"])
            envelope["signature"] = encode_signature(
                seed,
                signature_message(b"tos.agent-relay-provider-quote-signature.v1\x00", envelope["body"]),
            )
        elif mutation.get("resign_as") == "requester":
            envelope = mutated[mutation["target"]]
            seed = bytes.fromhex(document["test_keys"]["requester_seed_hex"])
            envelope["signature"] = encode_signature(
                seed,
                signature_message(b"tos.agent-relay-quote-request-signature.v1\x00", envelope["body"]),
            )
        elif mutation.get("resign_as") == "provider_evidence":
            envelope = mutated[mutation["target"]]
            seed = bytes.fromhex(document["test_keys"]["provider_seed_hex"])
            envelope["signature"] = encode_signature(
                seed,
                signature_message(b"tos.agent-relay-finality-evidence-signature.v1\x00", envelope["body"]),
            )
        elif mutation.get("resign_as") == "provider_resolution":
            envelope = mutated[mutation["target"]]
            seed = bytes.fromhex(document["test_keys"]["provider_seed_hex"])
            envelope["signature"] = encode_signature(
                seed,
                signature_message(b"tos.agent-relay-resolution-signature.v1\x00", envelope["body"]),
            )
        elif mutation.get("resign_as") == "authority_admission":
            envelope = mutated[mutation["target"]]
            seed = bytes.fromhex(document["test_keys"]["authority_seed_hex"])
            envelope["signature"] = encode_signature(
                seed,
                signature_message(
                    b"tos.agent-relay-side-effect-admission-receipt-signature.v1\x00",
                    envelope["body"]),
            )
        try:
            validate_bundle(mutated, registry)
        except ConformanceError:
            continue
        raise ConformanceError(f"negative mutation {mutation['name']} unexpectedly passed")
    verify_decisions(document.get("decision_vectors", []), models["execution_request"])
    expected = expected_document
    expected_objects = {item["name"]: item for item in expected["objects"]}
    for name in ("network", "underlying_payment_request", "sponsorship_payment_request"):
        if objects[name]["digest"] != expected_objects[name]["digest"]:
            raise ConformanceError(f"{name}: Go cross-language constant mismatch")
    for name in ("service_profile", "quote_request_body", "provider_quote_body"):
        vector_name = "go_" + name
        if objects[vector_name]["digest"] != expected_objects[vector_name]["digest"]:
            raise ConformanceError(f"{vector_name}: Go cross-language constant mismatch")


def main() -> int:
    parser = argparse.ArgumentParser()
    root = Path(__file__).resolve().parents[1]
    parser.add_argument("--vectors", type=Path, default=root / "test-vectors/agent-relay-service-v1.json")
    parser.add_argument("--registry", type=Path, default=root / "schemas/semantic-action-identity-v1.json")
    parser.add_argument("--emit-vectors", action="store_true")
    parser.add_argument("--write-vectors", action="store_true")
    args = parser.parse_args()
    try:
        registry = load_semantic_registry(args.registry)
        if args.emit_vectors or args.write_vectors:
            rendered = json.dumps(build_vectors(registry), indent=2, sort_keys=False) + "\n"
            if args.write_vectors:
                args.vectors.write_text(rendered, encoding="utf-8")
            else:
                print(rendered, end="")
        else:
            verify_document(args.vectors, args.registry)
    except (ConformanceError, OSError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    if not args.emit_vectors and not args.write_vectors:
        print("PASS: independent Agent Relay Service V1 CBOR, digest, signature, binding, mutation, and recovery vectors")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
