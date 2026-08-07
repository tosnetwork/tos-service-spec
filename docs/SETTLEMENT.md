# ATOS Settlement Model v0.2

## 1. Principle

**Clients buy capabilities. They should not be forced to become blockchain users.**

ATOS exposes one stable commercial abstraction while allowing the transaction to resolve to one of three concrete trust modes:

```text
managed
verified
native
```

`auto` is a pre-quote policy value only. It MUST resolve to a concrete mode before a Quote is issued.

The key invariant is:

> **The Quote locks the economic terms, the concrete trust mode, and the proof/settlement guarantees before commitment.**

No implementation may silently downgrade those guarantees after the Quote is accepted.

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
Signed Execution Receipt
        |
ATOS managed settlement
```

TOS anchoring is optional.

### 4.2 Verified Mode

Verified Mode keeps the managed UX but requires TOS-backed economic and proof checkpoints according to the selected proof profile.

Minimum paid-job lifecycle:

```text
Quote issued with trust_mode=verified
        |
Quote/terms commitment -> TOS
        |
TOS-backed escrow reservation
        |
Provider / tos-ai executes off-chain
        |
Provider signs Execution Receipt
        |
Receipt commitment + verification -> tos-core / TOS
        |
TOS-backed settlement
        |
Settlement proof + Proof-of-Service evidence
```

The gateway may fund, sponsor, custody, or abstract the TOS-side transaction on behalf of the client where operationally and legally supported. The user still does not need to handle chain mechanics directly.

### 4.3 Native Mode

Native Mode provides the same minimum cryptographic/economic guarantees as Verified Mode, but `atos.im` is not a required authority or transaction intermediary.

A compatible gateway or client can resolve the capability and verify the resulting economic/proof state through TOS-compatible infrastructure.

Native settlement MUST NOT depend on an `atos.im` database record as the canonical source of ownership, Quote commitment, escrow state, receipt proof, or final settlement state.

## 5. What "On-Chain" Means

ATOS does not write prompts, private files, raw model outputs, or bulk artifacts to TOS merely because the user selected `verified` or `native`.

Instead, the protocol commits the economically/trust-relevant facts.

Typical required commitments for Verified/Native paid execution:

- provider identity / capability ownership;
- capability version/manifest commitment;
- quote/terms commitment;
- escrow state;
- signed Execution Receipt commitment;
- output/artifact commitment where applicable;
- usage commitment for metered billing;
- settlement state;
- dispute outcome commitment if disputed;
- Proof-of-Service evidence.

Implementations MAY batch or aggregate commitments as long as an independent verifier can prove inclusion, ordering where relevant, and finality against TOS Network.

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

## 7. Reservation / Escrow Model

Paid, financially committing work SHOULD reserve the maximum authorized amount before provider execution unless the Quote explicitly defines another safe settlement model.

Free capabilities do not require an escrow.

### 7.1 Common logical object

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
- Verified/Native: `backend = tos` or a protocol-defined TOS-backed backend.

### 7.2 States

```text
reserved -> settled
reserved -> released
reserved -> disputed -> settled
reserved -> disputed -> released
```

`reserved` and `disputed` are non-terminal.

Every reservation MUST eventually reach `settled` or `released`. A reservation left indefinitely after expiry is an implementation bug.

For metered/per-unit pricing, `settled` does not imply the full reserved maximum was charged. The unused amount is released/refunded.

## 8. Reservation vs Settlement

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
  -> provider signs Execution Receipt
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
  -> provider signs Execution Receipt
  -> tos-core.VerifyExecutionReceipt   [side-effect-free verification]
       |-- fail ------------------------------> no settlement; release/dispute path
       |-- pass
       v
  -> tos-core.SettleJob               [state mutation]
  -> release unused reserve
  -> persist/return network-verifiable Receipt
  -> emit Proof-of-Service evidence
```

`VerifyExecutionReceipt` MUST be side-effect-free with respect to balances/escrow state. It MAY read identity, ownership, key, Quote commitment, manifest, and network state. "Verification" does not imply "no reads"; it means verification itself does not move value.

`SettleJob` is the operation that changes settlement state and MUST NOT run against a receipt that has not satisfied the selected proof profile.

## 9. Execution Receipt

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
  "provider_signature":"...",
  "network_proof_ref":"tos:...",
  "created_at":"..."
}
```

Sensitive input/output payloads are not embedded merely for verification. Commitments are preferred.

### Receipt arithmetic invariant

For a reservation-backed final receipt:

```text
charged + refunded = originally reserved amount
```

where all three amounts are expressed in the same client accounting currency and include fees consistently according to the Quote.

Provider payout accounting may use a different settlement asset and is reconciled separately.

## 10. Proof Profiles

A proof profile defines the exact guarantees that a gateway means when it returns `trust_mode=verified` or `trust_mode=native`.

Initial protocol target:

```text
tos_verified_v1
```

At minimum it should cover:

- provider identity/capability ownership proof;
- capability version/manifest commitment;
- quote/terms commitment;
- reservation/escrow proof for paid committed work;
- provider-signed Execution Receipt;
- receipt inclusion/verification proof;
- settlement proof;
- Proof-of-Service evidence reference.

Native Mode additionally requires federation-safe canonical resolution as defined by the Architecture specification.

A gateway MUST NOT invent a weaker local meaning for a standard proof-profile name.

## 11. Cancellation

Cancellation before a billable receipt exists normally releases the full reserve.

If partial billable work is allowed, the Quote/terms MUST define the cancellation charging rule and the provider must produce a receipt for the billable portion.

After Quote issuance, cancellation MUST preserve the original concrete `trust_mode`. A Verified/Native cancellation/refund transition is itself handled through the corresponding TOS-backed economic path where required by the proof profile.

## 12. Expiry

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

## 13. Disputes

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

## 14. No Silent Downgrade

After Quote issuance, the selected mode is part of the commercial contract.

Forbidden without a new Quote:

```text
verified -> managed
native   -> managed
native   -> verified
```

If TOS settlement, proof production, capability anchoring, or required network infrastructure becomes unavailable, the call MUST fail, wait within its SLA, or require a new Quote.

The gateway MUST NOT "helpfully" complete the job under a weaker trust mode.

## 15. TOS Abstraction Boundary

Ordinary clients should see stable commercial/proof objects, not blockchain internals.

Default receipt may include:

```json
{
  "trust_mode":"verified",
  "proof_status":"verified",
  "network_proof_ref":"tos:..."
}
```

Advanced proof retrieval:

```text
GET /v1/receipts/{id}/settlement-proof
GET /v1/receipts/{id}/execution-proof
```

These endpoints may return protocol-defined commitments, attestations, inclusion proofs, transaction references, or other TOS proof data.

Normal MCP responses MUST NOT require clients to reason about validator IDs, gas units, contract addresses, or chain topology.

## 16. Settlement Invariants

1. `auto` is request-only; committed economic objects use a concrete mode.
2. Quote mode and proof profile are immutable after issuance.
3. No silent downgrade is allowed.
4. Managed settlement may remain centralized.
5. Verified/Native paid work uses the TOS-backed guarantees of the selected proof profile.
6. Bulk/private payloads remain off-chain; commitments carry the trust facts.
7. Verification is side-effect-free; settlement is the value-moving state transition.
8. Reservation expiry cannot leave funds locked indefinitely.
9. Dispute policy is committed at Quote time.
10. Client currency and provider payout asset may differ without changing the trust-mode contract.
