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
MUST be positive and no greater than `uint64`. TaskEscrow V1 requires fees to
be zero and subtotal to equal the maximum under the same exact decimal
arithmetic.

Client/display currencies are not settlement amounts. A USD or other display
price without a separately committed exchange-rate contract is not eligible
for Phase 4B-2. Implementations MUST NOT copy a USD decimal string into a TOS
amount, infer an exchange rate, truncate, round, or use floating point.

The settlement backend is exactly `tos`, settlement asset exactly `TOS`, and
the funding model is the immutable value committed by the Quote.

For ATOS-issued v1 Quotes, the gateway fee is exactly
`floor(subtotal_nanoTOS * 50 / 1000)` (5 percent), and `total_max` is the exact
integer sum of subtotal and that fee. This single floor operation occurs in
nanoTOS; no floating-point rate or later decimal rounding is permitted.

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
reservation_action_digest = sha256("TOS-PROTOCOL-CBOR\x00" ||
                                   uint16be(len("tos.task-escrow.action.v1")) ||
                                   "tos.task-escrow.action.v1" ||
                                   cbor(stable_reservation_action))
reservation_action_id = "task-action-" + hex(reservation_action_digest)
release_action_id = "task-action-" +
                    hex(sha256("tos.task-escrow.release-action.v1\x00" ||
                               escrow_id || "\x00" || release_digest || "\x00"))
```

`stable_reservation_action` is the complete JSON-model action converted to
Core Deterministic CBOR under the repository `codec.Digest` rules. Its fields
are `version`, `network`, `kind` (`deploy`), `escrow_id`, `creator`, `agent`,
optional `verifier`, `budget_nano_tos`, `funding_nano_tos`, `deadline_unix`,
`review_period`, `policy_hash`, and `permission_hash`; the permission hash is
the exact `reservation_digest`. Optional empty fields are omitted exactly as
declared by `StableTaskEscrowAction`. No reduced `(kind, escrow_id, digest)`
formula is conformant.

The same Quote cannot fund two Jobs. Reuse of a Quote, Job, escrow ID or action
identity with changed semantics is `IDEMPOTENCY_CONFLICT`.

All three pre-settlement refund actions (`cancel`, `timeout`, `reject`) carry
the frozen `release_digest` in the publisher action envelope. The contract
body continues to contain the contract-defined opcode/query ID, while the
publisher Action ID is the formula above; a journal receipt for one reason
cannot be replayed as evidence for another reason.

All committed millisecond deadlines MUST be exactly second-aligned
(`value % 1000 == 0`) before conversion to the TaskEscrow contract's integer
seconds. Non-aligned values are invalid; rounding or truncation is forbidden.

The normative fixture in `tos-protocol/pkg/escrowcommitment` has:

```text
escrow_id = esc_07dc7a9bb743b890a44312c5d6d85a8a
reservation_digest = sha256:271b8392229e741f86cbd9366f4fd35c09ce22b4a6a92f96bb7cdc68932149b5
canonical_cbor_length = 1384
reservation_action_id = task-action-34d28e46c2cecfd5af6875aaeec9620edfc095f4dc81b57782cd37cffba16aee
release_digest(CANCELED) = sha256:8a38d8920a287d1d2401285f814abb4c409a3bd866ab3a330e74df9ba1a16b1a
release_action_id = task-action-762de1e789d3f797f6bff0e6abff99d3cae158c924c7626297dd97eeefdfbc47
release_query_id = 8076693888132313379
release_expected_body_hash = tvm-cell-sha256:2a8ece876e9cfa1ef9bd9062b6c5ecbbee07bbea1ac8283fba8e5639522c80d8
```

The checked-in tests in `pkg/escrowcommitment` and `pkg/economic` construct
every field and fail on any canonical encoding, digest, Action ID, query ID,
or body-hash change; independent implementations use the same fixture values.

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

The enrollment produces a versioned `journal_binding` digest over those
immutable values. `tos-protocol` configuration pins both `journal_identity`
and `journal_binding`; readiness and every typed `action_not_found` response
carry both values. A same-network socket backed by any other journal is not an
authoritative absence source.

Before key custody is invoked, the publisher independently recomputes the
`task-action-<sha256>` identity from the complete stable action and enforces an
operator-enrolled policy containing allowed creator, Agent and verifier
addresses, allowed TaskEscrow policy/code hashes, and maximum budget/funding
nanoTOS. The tosctl configuration is read once into an unlinked immutable
descriptor; send and recovery must use the same single effective endpoint and
the same pinned genesis root/file hashes. Legacy `chain_rpc.url` and modern
`chain_rpc.urls` are merged, trimmed and deduplicated; contradictory or keyed
effective endpoint configurations fail startup.

The production tosctl-backed TaskEscrow publisher is Linux-only. Startup MUST
reject Darwin and every other unsupported platform. Its enrolled executable
MUST be owned by root, reached only through root-owned directories that are not
group- or world-writable, and executed by an unprivileged service account. The
publisher opens and revalidates the enrolled inode and digest for every call,
then executes that inherited descriptor through Linux `/proc/self/fd`; it MUST
NOT execute the previously validated pathname.

## Release

Cancellation, rejection and expiry persist a release intent before mutation.
Release is bound to the original reservation, Quote, Job, principal and reason.
It is complete only after independent observation of the canonical released,
cancelled, expired or rejected state and exact refund transition. Settled
escrows cannot release; released escrows cannot execute or return to reserved.
Ambiguous outcomes remain reconciling and never fall back to Managed.

## Successful settlement boundary

Successful provider settlement is outside the reservation/release delivery
scope of Phase 4B-2, but any existing shared Job lifecycle path MUST preserve
the Phase 4B-2 authority boundary. A Verified TaskEscrow payout/refund MUST
never be duplicated in the Managed/Blnk ledger or applied to Managed account
balances or policy allowances.

Before a Verified Job may be projected as settled, the gateway MUST validate
the exact settlement/escrow/Quote/Job/execution-Receipt tuple, settled escrow
state, configured network, exact TOS charge, refund and reserve conservation,
and a live independently observed non-zero, non-regressing finalized
checkpoint. Local cache, publisher output, a transition reference alone, or
an HTTP success response is insufficient.

Before invoking settlement, the request MUST bind the complete frozen
`VerifiedEscrowTerms`, reservation digest and finalized escrow reference. The
authority MUST re-resolve this tuple through canonical TOS observation and
compare the local projection's Quote commitment digest/reference,
reservation digest, TaskEscrow contract reference and allowed code hash. A
mismatch fails before any transaction is published.

TaskEscrow V1 does not implement an independently observable gateway payout.
Verified Quotes using it therefore require atomic `fees = 0`; the provider
payout may never include a fee represented as payable to the gateway.

The sweeper orders operations by `updated_at, escrow_id`, uses a durable cursor
or keyset pagination, bounded batches and bounded backoff, and cannot allow old
rows beyond one fixed `LIMIT` to starve indefinitely.
