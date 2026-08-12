# `tos_verified_v1` portable proof package

Status: frozen for Phase 4C.

## 1. Purpose and authority

`tos_verified_v1` is a self-describing immutable evidence package for one
completed Verified ATOS transaction. It is a projection of already-authorized
TOS facts. Producing or verifying it never mutates a Quote, Job, Receipt, or
TaskEscrow.

An ATOS database row, publisher journal entry, HTTP response, transaction hash,
or caller-supplied finality flag is not canonical evidence. A verifier MUST
recompute every digest and resolve every required reference through a
read-only, quorum-backed TOS observer. Transport failure, malformed data,
unsupported endpoints, cache misses and ordinary HTTP 404 are
`AUTHORITY_UNAVAILABLE`, never authoritative absence and never permission to
publish.

## 2. Encoding and identity

The package/version identifier is `tos_verified_v1`; canonicalization is
`rfc8949_core_deterministic_cbor`; the digest domain is
`tos.atos.portable-proof.v1`.

Canonical bytes are RFC 8949 Core Deterministic CBOR over the exact JSON data
model in §3. JSON names are exact; maps contain only named fields; optional
fields are omitted, not null; arrays preserve specified order. Floating point,
CBOR tags, indefinite lengths and unknown fields are forbidden. Times are UTC
Unix nanoseconds. Monetary amounts are unsigned base-10 atomic-unit strings
with no sign, decimal point, exponent, or leading zero except `0`.

```text
digest = sha256("TOS-PROTOCOL-CBOR" || 0x00 ||
                uint16be(len(domain)) || domain || canonical_cbor(package))
package_id = "proof_" || first_32_hex(digest)
```

Digests render as lowercase `sha256:<64 hex>`. Neither digest nor package ID is
embedded in the canonical value.

## 3. Required wire model

Every field is required unless marked optional. References are exact objects
`{network, reference, finalized_checkpoint}`. Checkpoints are nonzero and may
not regress. V1 digests use SHA-256 only.

```text
package
  version, canonicalization, network_id, gateway_domain
  principal_id, requester_agent_id, provider_id
  capability, quote, escrow, signer_authorization, receipt
  outcome, proof_of_service

capability
  capability_id, capability_version, manifest_digest, ownership_ref

quote
  quote_id, commitment_digest, commitment_ref, terms_digest
  trust_mode="verified", proof_profile="tos_verified_v1"
  settlement_backend="tos", settlement_asset="TOS", asset_decimals=9
  subtotal_atomic, fees_atomic, total_max_atomic
  acceptance_deadline_unix_nanos, quote_expiry_unix_nanos
  execution_deadline_unix_nanos, underlying_service_quote_ref
  dispute_policy_digest

escrow
  escrow_id, job_id, contract_ref, contract_code_hash
  reservation_digest, reservation_ref, reserved_atomic
  escrow_deadline_unix_nanos, funding_model

signer_authorization
  authorization_id, execution_signer_id, authorization_ref
  signature_algorithm="ed25519", signer_public_key (32 raw bytes)
  valid_from_unix_nanos, valid_until_unix_nanos

receipt
  receipt_id, receipt_digest, receipt_ref, result
  input_commitment, output_commitment, usage_commitment
  started_unix_nanos, completed_unix_nanos
  charged_atomic, signature_algorithm="ed25519", signature (64 raw bytes)
  canonical_cbor (the exact `tos.atos.execution-receipt.v2` signed value)

outcome
  kind, outcome_ref, charged_atomic, refunded_atomic
  release_digest (optional), reason_code (optional)
  dispute_digest (optional), dispute_outcome (optional)

proof_of_service
  evidence_id, evidence_digest, evidence_ref
  content_digest, retrieval_ref (optional)
```

`kind` is `provider_settlement`, `requester_release`, or
`dispute_resolution`. Release fields occur only for requester release; dispute
fields only for dispute resolution. `charged_atomic + refunded_atomic` equals
`reserved_atomic`. TaskEscrow v1 requires zero Quote fees. A provider
settlement may charge zero and refund the full reserve.

`funding_model` is the exact Phase 4B-2 value committed in
`VerifiedEscrowTerms` (for example `gateway_sponsored`); it is never inferred
or rewritten as the name of the TaskEscrow contract version.

`receipt.canonical_cbor` is the explicit field-level Execution Receipt DTO
defined by `tos.atos.execution-receipt.v2`. `receipt_digest` is its domain
digest and Ed25519 signs the 32 raw digest bytes. The package repeats selected
receipt tuple fields so verifiers can compare them to the signed DTO and the
surrounding Quote/escrow without accepting an opaque blob. This replaces
deterministic protobuf as the normative Receipt signature representation;
protobuf is transport only.

## 4. Verification algorithm

A verifier MUST:

1. decode exact canonical CBOR under bounded byte/depth/collection limits;
2. reject unknown fields, unsupported semantics, malformed digests, times and
   atomic amounts;
3. recompute package, Quote, reservation, Receipt, release/dispute and
   Proof-of-Service digests;
4. bind every reference and nested tuple to one network/domain, principal,
   provider, Capability version, Quote, Job and escrow;
5. live-resolve identity, ownership/manifest, Quote, reservation, Receipt,
   outcome and Proof-of-Service references through the read-only observer;
6. resolve signer authorization at Receipt completion, comparing exact key,
   Capability version, reference and validity interval and rejecting rotation
   or revocation effective at/before execution;
7. verify the Ed25519 Receipt signature locally;
8. match terminal TaskEscrow state, charge/refund and outcome type to the
   original contract and reservation;
9. require nonzero, sufficiently final, non-regressing checkpoints.

Verification time is observation metadata only and cannot be caller-selected
to make an invalid signer valid.

## 5. Privacy

Packages contain commitments, not private task inputs/outputs, proposals,
credentials, signing commands, journal internals, secrets, or bulk artifacts.
Optional `retrieval_ref` is authorization-gated and its content is untrusted
until it matches `content_digest`. Mutable URLs never replace a digest or
finalized reference.

## 6. Errors and compatibility

Structured codes are `MALFORMED_PACKAGE`, `UNSUPPORTED_VERSION`,
`UNSUPPORTED_SEMANTICS`, `DIGEST_MISMATCH`, `TUPLE_MISMATCH`,
`NETWORK_MISMATCH`, `DOMAIN_MISMATCH`, `SIGNER_UNAUTHORIZED`,
`SIGNATURE_INVALID`, `FINALITY_INVALID`, `FINALITY_REGRESSION`,
`AUTHORITY_UNAVAILABLE`, `EVIDENCE_NOT_FOUND`, `OUTCOME_INVALID`, and
`PRIVACY_VIOLATION`. Failures are ordered by wire traversal. Version matching
is exact; no guessing or downgrade is permitted. V1 has no extension map and
rejects every unknown field.

## 7. Production and recovery

ATOS persists a monotonic operation:

```text
intent_persisted -> reconciling -> canonical_observed
                 -> projection_persisted -> completed
```

`completed` is terminal. The semantic identity is `(network_id,
gateway_domain, quote_id, job_id, escrow_id, receipt_id, terminal outcome
reference)`. Exact replay is byte-identical. Changed semantics under the same
identity is `IDEMPOTENCY_CONFLICT`. Recovery after any local failure is
read-only; proof production never retries a chain mutation.

Normative positive and negative vectors live in
`test-vectors/tos_verified_v1.json` and freeze canonical CBOR, digest, signer,
network, checkpoint and terminal-outcome mutations.
