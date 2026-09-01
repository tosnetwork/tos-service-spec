#!/usr/bin/env python3
"""Independent verifier for Agent Operation and Outcome Event V1 vectors."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import struct
from pathlib import Path


# Minimal independent RFC 8032 verifier. It intentionally has no dependency on
# the Go implementation or a platform crypto package, so the release corpus
# catches shared codec/signature-message mistakes in hermetic CI.
ED_Q = 2**255 - 19
ED_L = 2**252 + 27742317777372353535851937790883648493
ED_D = (-121665 * pow(121666, ED_Q - 2, ED_Q)) % ED_Q
ED_I = pow(2, (ED_Q - 1) // 4, ED_Q)


def ed_xrecover(y: int, sign: int) -> int:
    xx = ((y * y - 1) * pow(ED_D * y * y + 1, ED_Q - 2, ED_Q)) % ED_Q
    x = pow(xx, (ED_Q + 3) // 8, ED_Q)
    if (x * x - xx) % ED_Q:
        x = (x * ED_I) % ED_Q
    if (x * x - xx) % ED_Q:
        raise ValueError("invalid Ed25519 point")
    if x & 1 != sign:
        x = ED_Q - x
    return x


def ed_decode(raw: bytes) -> tuple[int, int]:
    if len(raw) != 32:
        raise ValueError("invalid Ed25519 point length")
    encoded = int.from_bytes(raw, "little")
    y, sign = encoded & ((1 << 255) - 1), encoded >> 255
    if y >= ED_Q:
        raise ValueError("non-canonical Ed25519 point")
    point = (ed_xrecover(y, sign), y)
    x, y = point
    if (-x * x + y * y - 1 - ED_D * x * x * y * y) % ED_Q:
        raise ValueError("off-curve Ed25519 point")
    return point


def ed_add(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    x1, y1 = left
    x2, y2 = right
    product = ED_D * x1 * x2 * y1 * y2 % ED_Q
    return ((x1 * y2 + x2 * y1) * pow(1 + product, ED_Q - 2, ED_Q) % ED_Q,
            (y1 * y2 + x1 * x2) * pow(1 - product, ED_Q - 2, ED_Q) % ED_Q)


def ed_scalar(point: tuple[int, int], scalar: int) -> tuple[int, int]:
    output = (0, 1)
    while scalar:
        if scalar & 1:
            output = ed_add(output, point)
        point = ed_add(point, point)
        scalar >>= 1
    return output


ED_BASE = (ed_xrecover(4 * pow(5, ED_Q - 2, ED_Q) % ED_Q, 0), 4 * pow(5, ED_Q - 2, ED_Q) % ED_Q)

OBJECT_SCHEMA_DEFINITIONS = {
    "evidence_manifest": "OutcomeEvidenceManifestV1",
    "authority_time_material": "OutcomeAuthorityProofMaterialV1",
    "issuer_qualification_material": "OutcomeAuthorityProofMaterialV1",
    "artifact_bundle": "OperationOutcomeArtifactBundleV1",
    "pinned_operation_authority": "PinnedAgentOperationAuthorityProofV1",
    "terminal_disposition": "TerminalDispositionV1",
    "event_body": "OperationOutcomeEventBodyV1",
    "operation_body": "AgentOperationBodyV1",
    "operation_envelope": "AgentOperationEnvelopeV1",
    "carrier_request": "OperationCarrierRequestV1",
    "private_request": "OperationPrivateRequestV1",
    "journal_append_request": "OperationJournalAppendAdmissionRequestV1",
    "submission_receipt": "OperationSubmissionReceiptV1",
    "economic_perimeter": "EconomicPerimeterV1",
    "revenue_recognition": "RevenueRecognitionV1",
    "asset_conversion": "AssetConversionEvidenceV1",
    "forecast": "OutcomeForecastV1",
    "calibration_report": "CalibrationReportV1",
    "financial_report": "FinancialReportV1",
    "censoring": "OutcomeCensoringV1",
    "evidence_availability": "EvidenceAvailabilityObservationV1",
    "gate_execution": "GateExecutionObservationV1",
    "carrier_receipt": "CarrierReceiptObservationV1",
    "cost_genesis": "CostObservationPayloadV1",
    "cost_contra": "CostObservationPayloadV1",
    "gift_transfer": "TransferObservationV1",
    "agreement_payment": "TransferObservationV1",
    "tos_escrow_transfer": "TOSEscrowObservationV1",
    "audience_policy": "AudiencePolicyV1",
    "encrypted_evidence": "OutcomeEncryptedEvidenceV1",
    "disclosure_projection": "OutcomeDisclosureProjectionV1",
    "cohort_membership_proof": "OutcomeCohortMembershipProofV1",
    "learning_dataset": "LearningDatasetManifestV1",
    "skill_promotion": "SkillPromotionDecisionV1",
}

EXPECTED_NEGATIVE_MUTATIONS = {
    "caller-selected-operation-id",
    "event-payload-substitution",
    "envelope-signature-substitution",
    "unsorted-evidence",
    "cross-issuer-content-deduplication",
    "publication-action-reused-across-carriers",
    "private-send-reused-after-membership-epoch-change",
    "genesis-cost-with-original-reference",
    "contra-cost-without-original-reference",
    "contra-cost-with-malformed-original-reference",
}


def verify_ed25519(public_key: bytes, message: bytes, signature: bytes) -> bool:
    if len(public_key) != 32 or len(signature) != 64:
        return False
    try:
        authority = ed_decode(public_key)
        r_point = ed_decode(signature[:32])
    except ValueError:
        return False
    scalar = int.from_bytes(signature[32:], "little")
    if scalar >= ED_L or authority == (0, 1) or r_point == (0, 1) or \
            ed_scalar(authority, ED_L) != (0, 1) or ed_scalar(r_point, ED_L) != (0, 1):
        return False
    challenge = int.from_bytes(hashlib.sha512(signature[:32] + public_key + message).digest(), "little") % ED_L
    return ed_scalar(ED_BASE, scalar) == ed_add(r_point, ed_scalar(authority, challenge))


def decode_unpadded_urlsafe(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def verify_schema_model(value, rule: dict, schema: dict, path: str) -> None:
    """Validate the corpus against the dependency-free JSON Schema subset it uses."""
    if "$ref" in rule:
        prefix = "#/$defs/"
        reference = rule["$ref"]
        if not reference.startswith(prefix) or reference[len(prefix):] not in schema["$defs"]:
            raise ValueError(f"{path}: unresolved local schema reference")
        verify_schema_model(value, schema["$defs"][reference[len(prefix):]], schema, path)
    if "oneOf" in rule:
        matches = 0
        for candidate in rule["oneOf"]:
            try:
                verify_schema_model(value, candidate, schema, path)
                matches += 1
            except ValueError:
                pass
        if matches != 1:
            raise ValueError(f"{path}: expected one schema match, got {matches}")
    for index, candidate in enumerate(rule.get("allOf", [])):
        if not isinstance(candidate, dict):
            raise ValueError(f"{path}: allOf[{index}] is not a schema")
        verify_schema_model(value, candidate, schema, f"{path}:allOf[{index}]")
    if "if" in rule:
        condition = rule["if"]
        if not isinstance(condition, dict):
            raise ValueError(f"{path}: if is not a schema")
        try:
            verify_schema_model(value, condition, schema, f"{path}:if")
            branch = "then"
        except ValueError:
            branch = "else"
        if branch in rule:
            selected = rule[branch]
            if not isinstance(selected, dict):
                raise ValueError(f"{path}: {branch} is not a schema")
            verify_schema_model(value, selected, schema, f"{path}:{branch}")
    if "const" in rule and value != rule["const"]:
        raise ValueError(f"{path}: const mismatch")
    if "enum" in rule and value not in rule["enum"]:
        raise ValueError(f"{path}: enum mismatch")
    kind = rule.get("type")
    if kind == "object":
        if not isinstance(value, dict):
            raise ValueError(f"{path}: expected object")
    elif kind == "array":
        if not isinstance(value, list):
            raise ValueError(f"{path}: expected array")
        if len(value) < rule.get("minItems", 0) or len(value) > rule.get("maxItems", 2**63 - 1):
            raise ValueError(f"{path}: array cardinality is out of range")
        for index, member in enumerate(value):
            verify_schema_model(member, rule["items"], schema, f"{path}[{index}]")
    elif kind == "string":
        if not isinstance(value, str):
            raise ValueError(f"{path}: expected string")
        if len(value) < rule.get("minLength", 0) or len(value) > rule.get("maxLength", 2**63 - 1):
            raise ValueError(f"{path}: string length is out of range")
        if "pattern" in rule and re.fullmatch(rule["pattern"], value) is None:
            raise ValueError(f"{path}: string pattern mismatch")
    elif kind == "integer":
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError(f"{path}: expected integer")
        if value < rule.get("minimum", -(2**1024)) or value > rule.get("maximum", 2**1024):
            raise ValueError(f"{path}: integer is out of range")
    if isinstance(value, dict):
        missing = set(rule.get("required", [])) - set(value)
        if missing:
            raise ValueError(f"{path}: missing fields {sorted(missing)}")
        properties = rule.get("properties", {})
        if rule.get("additionalProperties") is False and not set(value) <= set(properties):
            raise ValueError(f"{path}: unknown fields {sorted(set(value) - set(properties))}")
        for name, member in value.items():
            if name in properties:
                verify_schema_model(member, properties[name], schema, f"{path}.{name}")


def require_schema_rejection(value, rule: dict, schema: dict, name: str) -> None:
    try:
        verify_schema_model(value, rule, schema, name)
    except ValueError:
        return
    raise ValueError(f"{name}: negative schema mutation was accepted")


def verify_schema_document(schema: dict) -> None:
    definitions = schema.get("$defs")
    if not isinstance(definitions, dict):
        raise ValueError("schema has no definitions")
    seen_refs: set[str] = set()

    def collect(node) -> None:
        if isinstance(node, dict):
            if "$ref" in node:
                seen_refs.add(node["$ref"])
            for member in node.values():
                collect(member)
        elif isinstance(node, list):
            for member in node:
                collect(member)

    collect(schema)
    unresolved = sorted(reference for reference in seen_refs
                        if not reference.startswith("#/$defs/") or reference.removeprefix("#/$defs/") not in definitions)
    if unresolved:
        raise ValueError(f"unresolved schema references: {unresolved}")
    roots = {entry.get("$ref", "").removeprefix("#/$defs/") for entry in schema.get("oneOf", [])}
    missing_roots = set(OBJECT_SCHEMA_DEFINITIONS.values()) - roots
    if missing_roots:
        raise ValueError(f"fixture schemas are not top-level roots: {sorted(missing_roots)}")


def cbor_head(major: int, value: int) -> bytes:
    if value < 24:
        return bytes([(major << 5) | value])
    if value <= 0xFF:
        return bytes([(major << 5) | 24, value])
    if value <= 0xFFFF:
        return bytes([(major << 5) | 25]) + struct.pack(">H", value)
    if value <= 0xFFFFFFFF:
        return bytes([(major << 5) | 26]) + struct.pack(">I", value)
    if value <= 0xFFFFFFFFFFFFFFFF:
        return bytes([(major << 5) | 27]) + struct.pack(">Q", value)
    raise ValueError("CBOR integer exceeds u64")


def canonical_cbor(value, depth: int = 0) -> bytes:
    if depth > 16:
        raise ValueError("CBOR nesting exceeds V1 bound")
    if value is None:
        return b"\xf6"
    if value is False:
        return b"\xf4"
    if value is True:
        return b"\xf5"
    if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
        return cbor_head(0, value)
    if isinstance(value, str):
        raw = value.encode("utf-8")
        return cbor_head(3, len(raw)) + raw
    if isinstance(value, list):
        return cbor_head(4, len(value)) + b"".join(canonical_cbor(item, depth + 1) for item in value)
    if isinstance(value, dict) and all(isinstance(key, str) for key in value):
        pairs = [(canonical_cbor(key, depth + 1), canonical_cbor(item, depth + 1)) for key, item in value.items()]
        pairs.sort(key=lambda pair: (len(pair[0]), pair[0]))
        return cbor_head(5, len(pairs)) + b"".join(key + item for key, item in pairs)
    raise ValueError("value is outside the V1 JSON/CBOR data model")


def protocol_digest(domain: str, canonical: bytes) -> str:
    raw = b"TOS-PROTOCOL-CBOR\x00" + struct.pack(">H", len(domain.encode())) + domain.encode() + canonical
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def lp16(value: bytes) -> bytes:
    if not value or len(value) > 0xFFFF:
        raise ValueError("invalid lp16 value")
    return struct.pack(">H", len(value)) + value


def lp32(value: bytes) -> bytes:
    if not value or len(value) > 1 << 20:
        raise ValueError("invalid lp32 value")
    return struct.pack(">I", len(value)) + value


def semantic_value(field_type: str, value: dict) -> bytes:
    if value.get("type") != field_type:
        raise ValueError("semantic field type mismatch")
    if field_type == "u64":
        number = value.get("number")
        if not isinstance(number, int) or isinstance(number, bool) or number < 0 or number > 0xFFFFFFFFFFFFFFFF or "text" in value:
            raise ValueError("invalid u64 semantic value")
        return struct.pack(">Q", number)
    text = value.get("text")
    if not isinstance(text, str) or not text or "number" in value:
        raise ValueError("invalid text semantic value")
    if field_type == "digest32":
        if len(text) != 71 or not text.startswith("sha256:"):
            raise ValueError("invalid digest semantic value")
        return bytes.fromhex(text[7:])
    return text.encode()


def verify_action(vector: dict, entry: dict) -> None:
    kind = vector["action_kind"]
    fields = vector["fields"]
    definitions = entry["ordered_semantic_fields"]
    if len(fields) != len(definitions):
        raise ValueError(f"{kind}: field count mismatch")
    output = bytearray(b"TOS-SAI\x00")
    output += struct.pack(">HH", entry["registry_version"], entry["entry_version"])
    output += lp16(entry["domain_tag"].encode()) + lp16(kind.encode()) + struct.pack(">H", len(definitions))
    for value, definition in zip(fields, definitions, strict=True):
        if value.get("name") != definition["field_name"]:
            raise ValueError(f"{kind}: non-canonical field order")
        output += lp16(definition["field_name"].encode())
        output += lp32(semantic_value(definition["field_type"], value))
    if bytes(output).hex() != vector["preimage_hex"]:
        raise ValueError(f"{kind}: preimage mismatch")
    if "sha256:" + hashlib.sha256(output).hexdigest() != vector["stable_action_id"]:
        raise ValueError(f"{kind}: stable Action ID mismatch")


def verify_fixture_signatures(objects: dict[str, dict]) -> None:
    envelope = objects["operation_envelope"]
    authority = envelope["authorization"]
    public_key = bytes.fromhex(authority["public_key"].removeprefix("ed25519:"))
    signature = decode_unpadded_urlsafe(authority["signature"].removeprefix("ed25519:"))
    body = canonical_cbor(envelope["body"])
    domain = b"tos.agent-operation-signature.v1"
    message = b"TOS-AGENT-OPERATION\x00" + struct.pack(">I", len(domain)) + domain + struct.pack(">I", len(body)) + body
    if not verify_ed25519(public_key, message, signature):
        raise ValueError("Agent Operation fixture signature mismatch")
    mutated = bytearray(signature)
    mutated[0] ^= 1
    if verify_ed25519(public_key, message, bytes(mutated)):
        raise ValueError("Agent Operation signature mutation was accepted")

    receipt = dict(objects["submission_receipt"])
    receipt_proof = base64.b64decode(receipt["sink_proof"], validate=True)
    receipt["sink_proof"] = None
    receipt_message = b"tos.operation-submission-receipt.v1\x00" + canonical_cbor(receipt)
    if not verify_ed25519(public_key, receipt_message, receipt_proof):
        raise ValueError("submission Receipt fixture signature mismatch")
    mutated = bytearray(receipt_proof)
    mutated[-1] ^= 1
    if verify_ed25519(public_key, receipt_message, bytes(mutated)):
        raise ValueError("submission Receipt signature mutation was accepted")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument("--vectors", type=Path, default=root / "test-vectors/agent-operation-outcome-event-v1.json")
    parser.add_argument("--registry", type=Path, default=root / "schemas/semantic-action-identity-v1.json")
    parser.add_argument("--schema", type=Path, default=root / "schemas/agent-operation-outcome-event-v1.json")
    args = parser.parse_args()
    vectors = json.loads(args.vectors.read_text(encoding="utf-8"))
    registry_doc = json.loads(args.registry.read_text(encoding="utf-8"))
    schema = json.loads(args.schema.read_text(encoding="utf-8"))
    verify_schema_document(schema)
    registry = {entry["action_kind"]: entry for entry in registry_doc["entries"]}
    if vectors.get("schema") != "tos.operation-outcome-conformance.v1":
        raise ValueError("unexpected vector schema")
    names: set[str] = set()
    object_models: dict[str, dict] = {}
    for item in vectors.get("objects", []):
        if item["name"] in names:
            raise ValueError("duplicate object vector")
        names.add(item["name"])
        object_models[item["name"]] = item["json_model"]
        definition = OBJECT_SCHEMA_DEFINITIONS.get(item["name"])
        if definition is None:
            raise ValueError(f"{item['name']}: no schema definition mapping")
        verify_schema_model(item["json_model"], schema["$defs"][definition], schema, item["name"])
        verify_schema_model(item["json_model"], schema, schema, item["name"] + ":root")
        canonical = base64.b64decode(item["canonical_cbor_base64"], validate=True)
        # Independently reproduce deterministic CBOR from the public JSON
        # model; digest-only checking would not catch a shared encoder bug.
        if canonical_cbor(item["json_model"]) != canonical:
            raise ValueError(f"{item['name']}: canonical CBOR mismatch")
        if protocol_digest(item["digest_domain"], canonical) != item["digest"]:
            raise ValueError(f"{item['name']}: digest mismatch")
    required = {
        "evidence_manifest", "authority_time_material", "issuer_qualification_material",
        "artifact_bundle", "pinned_operation_authority", "terminal_disposition",
        "event_body", "operation_body", "operation_envelope", "carrier_request", "private_request", "journal_append_request", "submission_receipt",
        "economic_perimeter", "revenue_recognition", "asset_conversion", "forecast",
        "calibration_report", "financial_report", "censoring", "evidence_availability",
        "gate_execution", "carrier_receipt", "cost_genesis", "cost_contra", "gift_transfer", "agreement_payment", "tos_escrow_transfer",
        "audience_policy", "encrypted_evidence", "disclosure_projection", "learning_dataset", "skill_promotion",
        "cohort_membership_proof",
    }
    if names != required:
        raise ValueError("object vector coverage mismatch")
    empty_cost_ref = {"network_id": "", "actor_agent_id": "", "operation_id": "", "operation_envelope_digest": ""}
    if object_models["cost_genesis"]["cost_class"] == "contra" or \
            object_models["cost_genesis"]["original_cost_assertion_ref"] != empty_cost_ref:
        raise ValueError("genesis cost incorrectly claims correction lineage")
    contra = object_models["cost_contra"]
    if contra["cost_class"] != "contra" or contra["original_cost_assertion_ref"] == empty_cost_ref:
        raise ValueError("contra cost lacks correction lineage")
    cost_schema = schema["$defs"]["CostObservationPayloadV1"]
    genesis_with_original = dict(object_models["cost_genesis"])
    genesis_with_original["original_cost_assertion_ref"] = dict(contra["original_cost_assertion_ref"])
    contra_without_original = dict(contra)
    contra_without_original["original_cost_assertion_ref"] = dict(empty_cost_ref)
    contra_with_malformed_original = dict(contra)
    malformed_ref = dict(contra["original_cost_assertion_ref"])
    malformed_ref["operation_id"] = "operation:malformed"
    contra_with_malformed_original["original_cost_assertion_ref"] = malformed_ref
    for mutation_name, mutation in {
        "genesis-cost-with-original-reference": genesis_with_original,
        "contra-cost-without-original-reference": contra_without_original,
        "contra-cost-with-malformed-original-reference": contra_with_malformed_original,
    }.items():
        require_schema_rejection(mutation, cost_schema, schema, mutation_name)
    verify_fixture_signatures(object_models)
    kinds: set[str] = set()
    for action in vectors.get("semantic_actions", []):
        kind = action["action_kind"]
        if kind in kinds or kind not in registry:
            raise ValueError("unknown or duplicate Action vector")
        kinds.add(kind)
        verify_action(action, registry[kind])
    if kinds != {"operation.journal.append", "operation.publish", "operation.private-send"}:
        raise ValueError("Action vector coverage mismatch")
    negative_mutations = vectors.get("negative_mutations")
    if not isinstance(negative_mutations, list) or any(not isinstance(name, str) for name in negative_mutations):
        raise ValueError("negative mutation matrix is not a string list")
    mutation_names = set(negative_mutations)
    if len(mutation_names) != len(negative_mutations):
        raise ValueError("negative mutation matrix contains duplicates")
    if mutation_names != EXPECTED_NEGATIVE_MUTATIONS:
        missing = sorted(EXPECTED_NEGATIVE_MUTATIONS - mutation_names)
        unexpected = sorted(mutation_names - EXPECTED_NEGATIVE_MUTATIONS)
        raise ValueError(f"negative mutation matrix mismatch: missing={missing}, unexpected={unexpected}")
    print(f"PASS: {len(names)} objects, {len(kinds)} Actions, {len(vectors['negative_mutations'])} negative mutations")


if __name__ == "__main__":
    main()
