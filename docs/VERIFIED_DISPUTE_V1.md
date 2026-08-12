# Verified TaskEscrow Dispute v1

## 1. Scope and authority

This contract freezes the dispute window and terminal adjudication used by
`trust_mode=verified` and `tos_verified_v1`. TOS TaskEscrow state is the sole
economic authority. ATOS review records and PostgreSQL rows are durable
projections and workflow intents; they cannot prove that a dispute opened or
that funds moved.

Managed earnings, Blnk balances, Managed account credits and payout holds MUST
NOT be used for a Verified dispute.

## 2. Lifecycle

```text
finalized execution Receipt
 -> durable result-operation intent
 -> TaskEscrow accept + result commitment
 -> independent result_submitted observation
 -> durable review_pending Job projection

requester opens before observed review_deadline
 -> durable dispute-open intent
 -> TaskEscrow dispute(dispute_digest)
 -> independent disputed observation
 -> durable opened projection

reviewer resolves
 -> durable immutable outcome intent
 -> TaskEscrow resolve(dispute_digest, provider_payout)
 -> independent settled observation
 -> durable Receipt/dispute/Job projection
 -> portable dispute_resolution proof

no dispute before review_deadline
 -> ordinary provider settlement recovery
```

Provider settlement MUST NOT be published before the observed contract review
deadline. A local clock or caller-supplied deadline is not authority. The
review deadline is read from finalized TaskEscrow state and is bound to the
original result transition.

## 3. Canonical commitments

Both values use RFC 8949 Core Deterministic CBOR through the repository's
`codec.Digest` discipline. Strings are UTF-8, timestamps are UTC Unix
milliseconds, digests are lowercase `sha256:<64 hex>`, and money is an unsigned
base-10 atomic TOS integer. Unknown fields are rejected recursively.

### Open tuple

Domain separator: `tos.atos.verified-dispute-open.v1`.

Required fields in canonical order/model:

```text
version, network_id, gateway_domain,
dispute_id, escrow_id, job_id, quote_id, receipt_id,
principal_id, provider_id, capability_id, capability_version,
quote_commitment_digest, reservation_digest, receipt_digest,
dispute_policy_digest, reason_code, evidence_digests,
opened_unix_millis
```

`evidence_digests` is a sorted, duplicate-free array of content digests. It
never contains private evidence bytes, mutable URLs, credentials or Artifact
database IDs. The resulting digest is `dispute_digest` and is the exact
non-zero hash passed to TaskEscrow `dispute`.

### Resolution tuple

Domain separator: `tos.atos.verified-dispute-resolution.v1`.

```text
version, network_id, gateway_domain,
dispute_id, escrow_id, job_id, quote_id, receipt_id,
dispute_digest, outcome, reviewer_principal_id,
reserved_atomic, provider_payout_atomic, requester_refund_atomic,
resolved_unix_millis
```

`outcome` is `principal`, `provider`, or `rejected`. Principal outcome requires
provider payout zero and full requester refund. Provider or rejected outcome
uses the already-verified Receipt charge and refunds the remainder. In all
cases payout plus refund equals the original reservation exactly.

The resolution digest is audit evidence. The chain action remains bound to the
same immutable `dispute_digest`, payout, TaskEscrow contract and deterministic
complete stable action. An outcome cannot be changed under the same dispute ID.

## 4. Authorization and binding

- Only the Job's authenticated requester may open the dispute.
- A requester or provider party cannot review or resolve it.
- Reviewer identity comes from the authenticated `disputes:review` principal.
- Caller fields are equality assertions, never selectors for network, Quote,
  Job, Receipt, provider, Capability, escrow, policy, amount or contract.
- Opening re-resolves the exact Quote, Receipt, reservation, signer and current
  result-submitted TaskEscrow state before mutation.
- Resolution re-resolves the same disputed TaskEscrow and immutable dispute
  digest before mutation.

## 5. Durability and recovery

Open and resolution use monotonic durable checkpoints (the current ATOS wire
names are shown here):

```text
verified_open_pending -> verified_disputed
verified_resolution_pending -> verified_resolved
```

Completed is terminal. Stale writers cannot regress it. Recovery reconstructs
the deterministic complete action without a cached transaction reference and
performs read-only publisher journal resolution plus independent quorum chain
observation. Typed absence, generic 404, pending journal state, malformed
response, timeout, transport failure and local cache miss all fail closed and
never authorize a second terminal mutation after chain state is disputed or
settled.

## 6. Portable outcome

A `dispute_resolution` proof binds:

- the open `dispute_digest`;
- resolution digest and outcome;
- original Quote, reservation and execution Receipt;
- immutable TaskEscrow contract reference and code hash;
- dispute and resolution transaction references with non-zero checkpoints;
- exact payout/refund conservation;
- the same Proof-of-Service and signer evidence as provider settlement.

The verifier resolves the terminal dispute action read-only. An ATOS dispute
row or terminal Receipt alone is not proof.

## 7. Normative digest vectors

The normative fixture uses network `tos-test`, domain `atos.im`, IDs suffixed
`-1`, capability version `1.0.0`, Quote/reservation/Receipt digests filled with
bytes `0x11`/`0x22`/`0x33`, policy bytes `0x44`, evidence bytes `0x55` and
`0x66`, reason `OUTPUT_MISMATCH`, and open time `1800000000123`.

```text
dispute_digest = sha256:143021614f8f6c93619a50f1a352937403c33d89a7dfd1c1cf1444f42ae486b8
```

The principal resolution uses reviewer `reviewer-1`, reserve `1000` nanoTOS,
provider payout `0`, requester refund `1000`, and time `1800000100123`:

```text
resolution_digest = sha256:bf86f1a0e42166185db786ff2c1dc5ffc5a60cb17e95a27160800ac0febb399b
```

Reversing evidence input order MUST produce the same open digest. Duplicate
evidence digests, unknown protobuf fields, zero/non-SHA-256 digests, malformed
amounts, and changed tuple fields MUST be rejected or change the digest as
applicable.
