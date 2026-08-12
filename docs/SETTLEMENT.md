# ATOS Settlement Model v0.2

## 1. Principle

**Clients buy capabilities. They should not be forced to become blockchain users.**

ATOS exposes one stable commercial abstraction while allowing the transaction to resolve to one of three concrete trust modes:

```text
managed
verified
native
```

`auto` is a pre-Quote policy value only. It MUST resolve to a concrete mode before a Quote is issued.

The key invariant is:

> **The Quote locks the economic terms, the concrete trust mode, and the proof/settlement guarantees before commitment.**

No implementation may silently downgrade those guarantees after the Quote is accepted.

Normative proof profiles are defined in `docs/PROOF_PROFILES.md`.

## 2. Client-Facing Accounting

Recommended client-facing accounting for the managed product remains fiat-referenced ATOS Credits or direct fiat display.

Examples:

- `1 ATOS Credit = USD 1 accounting value`; or
- display USD directly and keep credits internal.

The client-facing denomination does not have to equal the provider settlement asset.

A client can therefore see:

```text
USD 5.25
```

while the provider ultimately receives TOS, a supported stable asset, fiat payout, or retained ATOS Credits according to provider policy and the selected trust mode.

Consumers MUST NOT be required to reason about TOS token volatility, gas, validator topology, or wallet derivation merely to buy a capability.

## 3. Requested Mode vs Resolved Mode

Request-time field:

```text
requested_trust_mode = managed | verified | native | auto
```

Committed transaction field:

```text
trust_mode = managed | verified | native
```

The following objects MUST carry only a resolved concrete `trust_mode`:

- Quote;
- Invocation;
- Job;
- Escrow/reservation;
- Execution Receipt;
- settlement record.

A Quote MAY additionally retain `requested_trust_mode` for auditability.

`auto` MUST NOT appear as the final mode of any committed economic object.

## 4. Mode-Specific Settlement Guarantees

### 4.1 Managed Mode

Managed Mode may use the ATOS gateway's own ledger, payment processor, or internal reservation system.

```text
Client balance / payment method
        |
ATOS managed reserve
        |
Provider executes
        |
Authorized signer creates Execution Receipt
        |
ATOS managed settlement
```

TOS anchoring is optional.

### 4.2 Verified Mode

Verified Mode keeps the managed UX but requires TOS-backed economic and proof checkpoints using `tos_verified_v1` or a stronger compatible profile.

Minimum paid-job lifecycle:

```text
Quote issued with trust_mode=verified
        |
Quote/terms commitment -> TOS
        |
TOS-backed enforceable escrow reservation
        |
Provider / tos-ai executes off-chain
        |
Authorized execution signer signs Receipt
        |
Signer authority + Receipt commitment verified -> tos-core / TOS
        |
TOS-backed settlement
        |
Settlement proof + Proof-of-Service evidence
```

The gateway may fund, sponsor, custody, or abstract the TOS-side transaction on behalf of the client where operationally and legally supported. The user still does not need to handle chain mechanics directly.

### 4.3 Native Mode

Native Mode uses `tos_native_v1` or a stronger compatible profile.

It includes the Verified economic/proof guarantees and additionally requires gateway-independent canonical identity/capability resolution and proof verification.

Native settlement MUST NOT depend on an `atos.im` database record as the canonical source of ownership, Quote commitment, escrow state, receipt proof, or final settlement state.

## 5. What "On-Chain" Means

ATOS does not write prompts, private files, raw model outputs, or bulk artifacts to TOS merely because the user selected `verified` or `native`.

Instead, the protocol commits the economically/trust-relevant facts.

Typical required commitments for Verified/Native paid execution:

- provider identity / capability ownership;
- capability version/manifest commitment;
- quote/terms commitment;
- escrow state;
- authorized execution signer identity/authorization;
- signed Execution Receipt commitment;
- output/artifact commitment where applicable;
- usage commitment for metered billing;
- settlement state;
- dispute outcome commitment if disputed;
- Proof-of-Service evidence.

Implementations MAY batch or aggregate proof/evidence commitments as long as an independent verifier can prove inclusion, ordering where relevant, and finality against TOS Network.

**Economic state is stricter.** A hash/Merkle root of a private centralized balance database is not sufficient to claim TOS-backed escrow or settlement. The value-moving reservation/release/settlement state required by a Verified/Native proof profile must be economically enforceable through the TOS-backed economic mechanism.

## 6. Quote Object

A Quote is immutable and time-limited.

Required fields:

- `quote_id`;
- `capability_id`;
- `capability_version`;
- `provider_id`;
- `requested_trust_mode`;
- resolved `trust_mode`;
- `proof_profile` when required;
- `price.subtotal`;
- `price.fees`;
- `price.total_max`;
- `price.currency`;
- settlement descriptor;
- proof descriptor;
- `expires_at`;
- `terms_hash`;
- `dispute_policy_hash` or equivalent immutable reference.

Example:

```json
{
  "quote_id":"q_...",
  "capability_id":"cap_...",
  "capability_version":"1.2.0",
  "provider_id":"agt_...",
  "requested_trust_mode":"auto",
  "trust_mode":"verified",
  "proof_profile":"tos_verified_v1",
  "price": {
    "subtotal":"5.00",
    "fees":"0.25",
    "total_max":"5.25",
    "currency":"USD"
  },
  "settlement": {
    "backend":"tos",
    "escrow":true,
    "funding_model":"gateway_sponsored",
    "client_asset":"USD",
    "provider_asset":"TOS"
  },
  "proof": {
    "quote_commitment":true,
    "execution_receipt":true,
    "settlement_proof":true,
    "proof_of_service":true
  },
  "expires_at":"2026-08-07T05:10:00Z",
  "terms_hash":"sha256:...",
  "dispute_policy_hash":"sha256:..."
}
```

For `verified` and `native`, the Quote MUST NOT be returned unless the implementation can currently satisfy the selected proof profile and settlement path.

## 7. Funding Model vs Settlement Guarantee

Walletless UX and TOS-backed settlement are compatible, but they are not the same thing.

A settlement descriptor MAY identify a funding model such as:

```text
managed_balance
client_tos
client_supported_asset
gateway_sponsored
external_sponsor
```

Examples:

- Managed: client pays ATOS Credits; ATOS reserves/settles internally.
- Verified: client pays USD/credits; gateway sponsors an enforceable TOS-side escrow corresponding to the Quote.
- Native: client or a replaceable sponsor funds the TOS-backed escrow; canonical trade state remains verifiable without `atos.im`.

If a Native client uses a gateway-local fiat balance, that fiat account remains gateway-local. The Native guarantee applies to the ATOS/TOS trade contract and proof state, not to making every off-chain fiat account portable.

## 8. Reservation / Escrow Model

Verified TaskEscrow reservation and pre-settlement release are normatively
defined in `VERIFIED_TASK_ESCROW_V1.md`. In particular, Phase 4B-2 uses exact
nanoTOS committed by a TOS-priced Quote; a display/client currency is never
implicitly converted to native TOS.

Paid, financially committing work SHOULD reserve the maximum authorized amount before provider execution unless the Quote explicitly defines another safe settlement model.

Free capabilities do not require an escrow.

### 8.1 Common logical object

```json
{
  "escrow_id":"esc_...",
  "quote_id":"q_...",
  "principal_id":"prn_...",
  "provider_id":"agt_...",
  "capability_id":"cap_...",
  "trust_mode":"verified",
  "backend":"tos",
  "reserved":{"amount":"5.25","currency":"USD"},
  "status":"reserved",
  "proof_ref":"tos:...",
  "created_at":"...",
  "expires_at":"...",
  "settled_at":null
}
```

The logical object is stable across modes even though its backend differs.

- Managed: `backend = atos_managed` or another managed backend.
- Verified/Native: `backend = tos` or a protocol-defined TOS-backed backend satisfying the proof profile.

### 8.2 States

```text
reserved -> settled
reserved -> released
reserved -> disputed -> settled
reserved -> disputed -> released
```

`reserved` and `disputed` are non-terminal.

Every reservation MUST eventually reach `settled` or `released`. A reservation left indefinitely after expiry is an implementation bug.

For metered/per-unit pricing, `settled` does not imply the full reserved maximum was charged. The unused amount is released/refunded.

## 9. Reservation vs Settlement

Reservation and settlement are deliberately separate operations.

Conceptually:

```text
Reserve(quote.total_max)
Execute
VerifyReceipt
Settle(actual_charge)
Release(unused_reserve)
```

In Managed Mode these may map to internal ATOS billing functions.

In Verified/Native Mode they map to `tos-core` trust/economic operations and TOS-backed state.

### Managed lifecycle

```text
quote
  -> billing.Reserve(total_max)
  -> tos-ai/provider execution
  -> authorized execution signer signs Receipt
  -> gateway verifies receipt/policy
  -> billing.Settle(actual_charge)
  -> release unused reserve
  -> issue Receipt
```

### Verified/Native lifecycle

```text
quote + terms commitment
  -> tos-core.CreateEscrow(total_max)
  -> tos-ai/provider execution
  -> authorized execution signer signs Receipt
  -> tos-core.VerifyExecutionReceipt   [side-effect-free verification]
       |-- fail ------------------------------> no settlement; release/dispute path
       |-- pass
       v
  -> tos-core.SettleJob               [state mutation]
  -> release unused reserve
  -> persist/return network-verifiable Receipt
  -> emit Proof-of-Service evidence
```

`VerifyExecutionReceipt` MUST verify signer authorization as well as receipt integrity and Quote/capability binding.

It MUST be side-effect-free with respect to balances/escrow state. It MAY read identity, ownership, signer authorization, Quote commitment, manifest, and network state.

`SettleJob` is the operation that changes settlement state and MUST NOT run against a receipt that has not satisfied the selected proof profile.

For `trust_mode=verified`, the finalized TOS TaskEscrow transition is the
only mutable financial authority. ATOS MUST NOT mirror the provider payout,
gateway fee or principal refund into a Managed/Blnk escrow, balance or spend
policy. Managed financial legs apply only to `trust_mode=managed`.

TaskEscrow V1 has only provider and requester payout legs; it has no canonical
gateway-fee recipient. Therefore a Verified Quote using TaskEscrow V1 MUST
freeze `fees = 0`, and `total_max` MUST equal `subtotal`. A gateway MUST reject
a non-zero Verified fee at Quote commitment and escrow construction. A future
contract version may enable fees only after its three-party payout tuple and
independent observation rules are separately frozen.

A successful Verified `SettleJob` response MUST bind the exact settlement,
escrow, Quote, Job and verified execution Receipt identities; exact charged
amount and asset; and a refund such that `charged + refunded == reserved` in
integer atomic TOS. Its settlement reference MUST carry the configured
network, `finalized=true` and a non-zero, non-regressing independently
observed checkpoint. The returned escrow MUST be the same canonical
TaskEscrow in the settled state. ATOS MUST validate this complete response
before persisting a settled projection or marking proof status settled.

`actual_charge` and the provider payout MAY be zero for a successful
metered/per-unit Job. TaskEscrow V1 natively permits `payout=0`; in that case
the provider receives zero, the requester receives the complete reserved
budget, and the independently observed contract state is still `settled`
with zero budget/balance. Zero-charge settlement uses the same deterministic
action identity, finality checks and crash-safe replay as non-zero settlement.

Before mutation, `SettleJob` MUST carry the same full `expected_terms`,
`expected_reservation_digest`, and `expected_escrow_ref` assertions used by
release. The authority MUST resolve that tuple live and compare it to its
local projection before selecting a contract address. Missing, stale,
regressed or mismatched canonical state fails closed before publication.

## 10. Execution Receipt

The Execution Receipt is both a billing input and an ATOS trust primitive.

Example:

```json
{
  "receipt_id":"rcpt_...",
  "quote_id":"q_...",
  "escrow_id":"esc_...",
  "job_id":"job_...",
  "provider_id":"agt_...",
  "capability_id":"cap_...",
  "capability_version":"1.2.0",
  "trust_mode":"verified",
  "proof_profile":"tos_verified_v1",
  "input_commitment":"sha256:...",
  "output_commitment":"sha256:...",
  "usage_commitment":"sha256:...",
  "charged":{"amount":"4.80","currency":"USD"},
  "refunded":{"amount":"0.45","currency":"USD"},
  "status":"settled",
  "execution_signer_id":"sig_...",
  "signer_authorization_ref":"tos:...",
  "signature":"...",
  "network_proof_ref":"tos:...",
  "created_at":"..."
}
```

Sensitive input/output payloads are not embedded merely for verification. Commitments are preferred.

The `provider_id` identifies the economic/service provider. `execution_signer_id` identifies the key/runtime that actually attested the execution. Verified/Native proof must establish that the signer was authorized for this provider/capability/version at the relevant time.

### Receipt arithmetic invariant

For a reservation-backed final receipt:

```text
charged + refunded = originally reserved amount
```

where all three amounts are expressed in the same client accounting currency and include fees consistently according to the Quote.

Provider payout accounting may use a different settlement asset and is reconciled separately.

## 11. Proof Profiles

Initial standard profiles:

```text
tos_verified_v1
tos_native_v1
```

`tos_verified_v1` defines the minimum TOS-backed transaction guarantees for Verified Mode.

`tos_native_v1` extends those guarantees with gateway-independent canonical resolution/federation requirements for Native Mode.

See `docs/PROOF_PROFILES.md` for the normative guarantee sets, signer-authorization rules, batching constraints, and verification package.

A gateway MUST NOT invent a weaker local meaning for a standard proof-profile name.

## 12. Cancellation

Cancellation before a billable receipt exists normally releases the full reserve.

If partial billable work is allowed, the Quote/terms MUST define the cancellation charging rule and the authorized execution signer must produce a receipt for the billable portion.

After Quote issuance, cancellation MUST preserve the original concrete `trust_mode`. A Verified/Native cancellation/refund transition is handled through the corresponding TOS-backed economic path where required by the proof profile.

## 13. Expiry

Every reservation inherits the Quote expiry plus a bounded grace window for in-flight work.

Recommended default:

```text
min(job SLA timeout, 24h)
```

On expiry with no valid settlement:

1. release the reserved amount;
2. restore client available balance according to the settlement backend;
3. reject late settlement unless dispute/recovery policy explicitly permits it;
4. record provider lateness as reputation/Proof-of-Service evidence where appropriate.

A gateway MUST NOT bypass an expired Verified/Native escrow by settling the job through a Managed backend.

## 14. Disputes

The Quote MUST commit to the applicable dispute policy before execution.

The policy should identify or commit to:

- dispute window;
- evidence rules;
- resolver/arbitration mechanism;
- refund/partial-settlement semantics;
- proof/anchoring requirements for the outcome.

Either party may open a dispute when allowed by that policy.

For Verified/Native, the final dispute outcome and corrective settlement/refund MUST be reflected in TOS-backed proof state according to the proof profile. A raw administrator balance edit is not a valid final protocol outcome.

The dispute resolver itself may be centralized, federated, contractual, committee-based, or eventually decentralized; its mechanism is a separate policy concern. The critical protocol requirement is that the resolver/policy is known at Quote time and the final economic transition is auditable.

## 15. No Silent Downgrade

After Quote issuance, the selected mode is part of the commercial contract.

Forbidden without a new Quote:

```text
verified -> managed
native   -> managed
native   -> verified
```

If TOS settlement, proof production, capability anchoring, signer authorization, or required network infrastructure becomes unavailable, the call MUST fail, wait within its SLA, or require a new Quote.

The gateway MUST NOT "helpfully" complete the job under a weaker trust mode.

## 16. TOS Abstraction Boundary

Ordinary clients should see stable commercial/proof objects, not blockchain internals.

Default receipt may include:

```json
{
  "trust_mode":"verified",
  "proof_profile":"tos_verified_v1",
  "proof_status":"verified",
  "network_proof_ref":"tos:..."
}
```

Advanced proof retrieval:

```text
GET /v1/receipts/{id}/settlement-proof
GET /v1/receipts/{id}/execution-proof
```

These endpoints may return protocol-defined commitments, attestations, inclusion proofs, transaction references, signer authorization proofs, or other TOS proof data.

Normal MCP responses MUST NOT require clients to reason about validator IDs, gas units, contract addresses, or chain topology.

## 17. Settlement Invariants

1. `auto` is request-only; committed economic objects use a concrete mode.
2. Quote mode and proof profile are immutable after issuance.
3. No silent downgrade is allowed.
4. Managed settlement may remain centralized.
5. Verified uses `tos_verified_v1` or stronger; Native uses `tos_native_v1` or stronger.
6. TOS-backed escrow/settlement must be economically enforceable; a hash of a private ledger is insufficient.
7. Bulk/private payloads remain off-chain; commitments carry the trust facts.
8. Execution Receipts are signed by an authorized execution signer, not necessarily the provider root key.
9. Verification is side-effect-free; settlement is the value-moving state transition.
10. Reservation expiry cannot leave funds locked indefinitely.
11. Dispute policy is committed at Quote time.
12. Client currency and provider payout asset may differ without changing the trust-mode contract.
