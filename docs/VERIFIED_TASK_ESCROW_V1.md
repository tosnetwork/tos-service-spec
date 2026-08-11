# Verified TaskEscrow Reservation and Release v1

## Status and scope

This document freezes Phase 4B-2. It covers reservation, read-only recovery,
and pre-settlement release for `trust_mode=verified`. Receipt commitment and
successful provider settlement remain out of scope.

```text
finalized Quote commitment -> intent_persisted -> reconciling
  -> authority_reserved -> projection_persisted -> completed

cancel/reject/expiry -> release_intent_persisted -> release_reconciling
  -> authority_released -> release_projection_persisted -> release_completed
```

Completed checkpoints are terminal and monotonic. ATOS rows, protocol caches,
publisher receipts and transaction hashes are projections, never canonical
proof of contract state or finality.

## Monetary contract

An executable `tos_verified_v1` Quote MUST price and commit its maximum in
native TOS with `asset_decimals=9`. `VerifiedEscrowTerms.reserve.asset` is
`TOS`; `atomic_amount` is the exact unsigned base-10 nanoTOS integer and MUST
equal the Quote maximum converted using exactly nine decimal places. The value
MUST be positive and no greater than `uint64`. Subtotal plus fees MUST equal
the maximum under the same exact decimal arithmetic.

Client/display currencies are not settlement amounts. A USD or other display
price without a separately committed exchange-rate contract is not eligible
for Phase 4B-2. Implementations MUST NOT copy a USD decimal string into a TOS
amount, infer an exchange rate, truncate, round, or use floating point.

The settlement backend is exactly `tos`, settlement asset exactly `TOS`, and
the funding model is the immutable value committed by the Quote.

## Canonical terms and digest

`VerifiedEscrowTerms` in `settlement.proto` is mandatory. Version is
`atos_verified_task_escrow_v1`; canonicalization is
`rfc8949_core_deterministic_cbor`. Unknown protobuf fields are rejected
recursively before conversion.

The canonical CBOR map uses the protobuf field names as UTF-8 text keys and
includes every field, including empty optional references as empty strings.
Integers use their shortest RFC 8949 representation; maps use deterministic
key ordering; floats and protobuf wire bytes are forbidden. Digests are:

```text
reservation_digest = sha256("tos.atos.verified-task-escrow.v1\x00" || cbor(terms))
release_digest = sha256("tos.atos.verified-task-escrow-release.v1\x00" ||
                        cbor({reservation_digest, escrow_id, job_id,
                              quote_id, reason_code}))
```

Deterministic identities are:

```text
escrow_id = "esc_" + hex(sha256("tos.atos.verified-task-escrow-id.v1\x00" ||
                                 network || "\x00" || domain || "\x00" ||
                                 quote_id || "\x00" || job_id))[0:32]
reservation_action_id = sha256("tos.task-escrow.action.v1\x00" ||
                                "reserve\x00" || escrow_id || "\x00" ||
                                reservation_digest)
release_action_id = sha256("tos.task-escrow.action.v1\x00" ||
                            "release\x00" || escrow_id || "\x00" ||
                            release_digest)
```

The same Quote cannot fund two Jobs. Reuse of a Quote, Job, escrow ID or action
identity with changed semantics is `IDEMPOTENCY_CONFLICT`.

The normative fixture in `tos-protocol/pkg/escrowcommitment` has:

```text
escrow_id = esc_07dc7a9bb743b890a44312c5d6d85a8a
reservation_digest = sha256:271b8392229e741f86cbd9366f4fd35c09ce22b4a6a92f96bb7cdc68932149b5
canonical_cbor_length = 1384
```

The checked-in test constructs every field and fails on any canonical encoding
or digest change; independent implementations use the same fixture values.

## Authority and live validation

Before reservation, the server live-resolves the exact Phase 4B-1 Quote
commitment and compares every term: network/domain, identities, Capability and
version, manifest/ownership, signer authorization, mode/profile, arithmetic,
backend/asset/funding model, deadlines, service Quote and dispute policy.
The Quote reference must be finalized at a non-zero, non-regressing checkpoint.

After any publisher result, the configured independent quorum observes the
canonical TaskEscrow code hash, address, full state, balance, transaction and
checkpoint. The code hash must be in the immutable startup allowlist. A
reservation is usable only when the state is open or accepted as allowed by
the configured execution policy, the exact budget is funded, and the canonical
tuple matches. Every replay, `GetEscrow`, reconciliation, and Job execution
gate repeats this live observation. Unavailability, reorganization, zero or
regressed checkpoint, and mismatches fail closed.

## Recovery and authoritative absence

Recovery first performs a read-only lookup by the deterministic action and
semantic tuple, even when no contract/reference was saved locally. It MUST NOT
publish to discover prior success. Local cache/database absence is not absence.

Mutation replay is permitted only after a versioned authenticated publisher
journal response, bound to the exact Action ID and journal identity, explicitly
states `action_not_found`. Generic 404, unsupported route, malformed response,
schema mismatch, wrong action, pending/unknown intent, timeout, transport or
journal failure are ambiguous and remain reconciling. A bounded history search
cannot establish absence.

The publisher persists and fsyncs pending intent before broadcast. Production
startup requires explicit journal enrollment and pins journal identity/schema,
network/genesis, endpoint set, wallet, contract/service policy, code hashes,
action encoding and send/recovery backend capabilities. Missing or replaced
enrolled state fails closed. Mutable path check/use is forbidden.

## Release

Cancellation, rejection and expiry persist a release intent before mutation.
Release is bound to the original reservation, Quote, Job, principal and reason.
It is complete only after independent observation of the canonical released,
cancelled, expired or rejected state and exact refund transition. Settled
escrows cannot release; released escrows cannot execute or return to reserved.
Ambiguous outcomes remain reconciling and never fall back to Managed.

The sweeper orders operations by `updated_at, escrow_id`, uses a durable cursor
or keyset pagination, bounded batches and bounded backoff, and cannot allow old
rows beyond one fixed `LIMIT` to starve indefinitely.
