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
not regress. The first successfully observed package freezes those checkpoint
values and its canonical bytes permanently. On replay, a verifier or producer
must re-observe the same reference at a checkpoint greater than or equal to the
frozen value; a later, higher chain head does not create a second package or
change its digest. V1 digests use SHA-256 only.

```text
package
  version, canonicalization, network_id, gateway_domain
  principal_id, requester_agent_id, requester_identity_ref, requester_identity
  provider_id, provider_agent_id, provider_identity_ref, provider_identity
  capability, quote, escrow, outcome
  signer_authorization (conditional), receipt (conditional)
  proof_of_service (conditional)

capability
  capability_id, capability_version, manifest_digest
  ownership_digest, ownership_ref

`ownership_digest` is the exact authority commitment digest for the frozen
Capability ownership tuple and is distinct from the nested manifest content
digest. Fresh-replica lookup uses `(capability_id@version, ownership_digest,
ownership_ref)`; substituting the manifest digest is invalid.

requester_identity / provider_identity
  agent_id, canonical_uri, controllers (exactly one canonical TOS address)
  assurance (non-empty and not self_asserted), identity_ref

The binding reference and Agent identity reference are distinct canonical
facts. Both are live-resolved. The identity tuple supplies the creator/agent
controller addresses to TaskEscrow observation only as equality assertions.
This permits a fresh protocol replica with an empty local bbolt file to verify
the complete contract tuple; neither the package nor a local projection may
select a different controller.

Identity live resolution recomputes `tos.atos.agent-identity.v2` from exactly
the four identity fields above. Principal-binding live resolution recomputes
`tos.atos.principal-binding.v2` from `principal_id` and `agent_id`. Both use
the RFC 8949 digest construction in §2. Mutable timestamps/references,
`public_attributes` and RPC transport/idempotency context are forbidden from
these commitment inputs. This is the normative empty-replica recovery identity.

quote
  quote_id, commitment_digest, commitment_ref, terms_digest
  trust_mode="verified", proof_profile="tos_verified_v1"
  settlement_backend="tos", settlement_asset="TOS", asset_decimals=9
  subtotal_atomic, fees_atomic, total_max_atomic
  acceptance_deadline_unix_nanos, quote_expiry_unix_nanos
  execution_deadline_unix_nanos, underlying_service_quote_ref
  dispute_policy_digest, canonical_cbor

escrow
  escrow_id, job_id, contract_ref, contract_code_hash
  reservation_digest, reservation_ref, reserved_atomic
  escrow_deadline_unix_nanos, funding_model, canonical_cbor

`contract_code_hash` uses the canonical lower-case
`tvm-cell-sha256:<64 lowercase hexadecimal digits>` representation. It is a
TVM code-cell identity and MUST NOT be rewritten as a generic `sha256:`
content digest.

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
  content_digest, canonical_cbor, retrieval_ref (optional)
```

`kind` is `provider_settlement`, `requester_release`, or
`dispute_resolution`. Release fields occur only for requester release; dispute
fields only for dispute resolution. `charged_atomic + refunded_atomic` equals
`reserved_atomic`. TaskEscrow v1 requires zero Quote fees. A provider
settlement may charge zero and refund the full reserve.

`signer_authorization`, `receipt`, and `proof_of_service` are mandatory for
provider settlement and dispute resolution. A requester release before
execution MUST omit all three: inventing execution evidence for a task that
did not run is forbidden. Such a release has zero charge and refunds the full
reservation. A release after execution is not representable as
`requester_release`; it requires the applicable dispute outcome.

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

Every field repeated outside canonical Quote, reservation or Receipt bytes is
an equality assertion. The verifier compares requester Agent identity, all
three monetary values, every deadline, service Quote reference, signer IDs and
algorithm, and both Receipt timestamps. It also requires
`subtotal_atomic + fees_atomic = total_max_atomic = reserved_atomic`.
`started_unix_millis` and `completed_unix_millis` are part of the signed
Receipt commitment; neither is presentation metadata.

A requester release is exactly zero charge and a full refund of the reserved
amount. A dispute package carries the canonical resolution CBOR and a distinct
finalized `dispute-resolution` commitment reference. That commitment binds the
dispute and reservation identities, reviewer, outcome, allocation and frozen
resolution time. The TaskEscrow terminal reference remains separately bound to
the actual contract transition.

Signer revocation is a deterministic
`tos.atos.execution-signer-revocation.v2` tuple keyed by authorization ID.
The canonical `revoked_unix_millis` is the independently observed exact
transaction `utime` of that finalized commitment, not the later observation
high-water time. Verifiers MUST query this tuple even when
the protocol replica has no local signer row. It invalidates an execution only
when effective at or before Receipt completion; later rotation/revocation does
not invalidate historical proofs. Missing canonical absence, finality or block
time fails closed. Principal bindings follow the equivalent
`tos.atos.principal-binding-revocation.v2` rule keyed by the exact historical
principal/agent/binding-digest tuple; an old binding anchor alone never proves
current ACTIVE state.

`quote.canonical_cbor` and `escrow.canonical_cbor` are respectively the exact
Phase 4B-1 Quote and Phase 4B-2 reservation values. The verifier recomputes
their domain digests locally and compares every repeated tuple field.
Proof-of-Service resolution is a live canonical tuple lookup; an ATOS or
protocol-local evidence row is not authority.

`proof_of_service.canonical_cbor` is the RFC 8949 deterministic encoding of
the complete authority tuple under domain separator
`tos.atos.proof-of-service.v1`. `evidence_digest` is the domain-separated
SHA-256 digest of that exact value. `content_digest` is the nested evidence
content digest; it is not interchangeable with the authority digest. The
tuple binds evidence and Receipt IDs, provider, Capability ID/version,
result, latency, exact settlement atomic amount and asset, dispute fields,
UTC Unix-millisecond observation time and optional AIPoW attribution.
Language-native JSON and deterministic protobuf are transport formats and
MUST NOT replace these canonical bytes.

Normative minimal Proof-of-Service vector:

```text
evidence_id = pos_receipt-1
receipt_id = receipt-1
provider_id = provider-1
capability_id = capability-1
capability_version = 1.2.3
result = EXECUTION_RESULT_SUCCESS
latency_millis = 42
settlement_volume = { asset: TOS, atomic_amount: 700 }
content_digest = sha256:1111111111111111111111111111111111111111111111111111111111111111
observed_unix_millis = 1800000000123
evidence_digest = sha256:039eb30e9a6af1d33a8cc49f4b6c2dc5446572da1fa59d7e33d2af87eba4cb64
```

The reference CLI's `--protocol-url` observer uses only public read-only
tos-protocol RPCs. Those RPCs live-resolve principal bindings, Capability
ownership, Quote/Receipt/PoS commitments, and TaskEscrow reservation and
terminal state. The observer has no ATOS database or mutation/publisher
dependency.

The outcome reference is the independently observed transaction that produced
the current terminal TaskEscrow state. It is distinct from the immutable
contract reference and cannot be supplied solely from an ATOS Receipt row.
For `requester_release`, live observation is bound to the package's release
digest and reason, and resolves the deterministic terminal ActionID without a
mutation. Verification of reservation/contract references against an already
released contract performs the same release-tuple assertion; a terminal local
projection is never sufficient.

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
network, checkpoint and terminal-outcome mutations. Every negative vector is
executable: `operation` is an RFC 6901 path-bound `replace` over the decoded
package model with a typed replacement value; `expected_code` and
`expected_field` are the mandatory verifier result after canonical
re-encoding. A name without an operation and expected result is not a
conformance vector.
