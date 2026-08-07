# ATOS Settlement Model

## Principle

**Clients buy capabilities. They should not be forced to become blockchain users.**

ATOS exposes a stable commercial abstraction while TOS Network can perform internal machine settlement.

## External Accounting

Recommended client-facing unit for MVP: **ATOS Credits**, denominated transparently in a fiat reference currency (initially USD).

Examples:

- `1 ATOS Credit = USD 1 accounting value` (recommended for clarity), or
- show USD directly and keep credits entirely internal.

Avoid making the consumer reason about TOS token volatility.

## Provider Settlement

Provider preferences may include:

- TOS
- supported stablecoin
- fiat payout where legally/operationally available
- ATOS Credits retained on platform

Provider payout policy is separate from client pricing.

## Escrow

An escrow is the reservation that sits between "client agreed to a price" and "provider
actually got paid." ATOS never moves client funds straight to a provider on invocation —
it always reserves first, so a failed or disputed job can be refunded without a clawback.

### Object

```json
{
  "escrow_id": "esc_...",
  "quote_id": "q_...",
  "principal_id": "prn_...",
  "provider_id": "agt_...",
  "capability_id": "cap_...",
  "reserved": {"amount": "5.25", "currency": "USD"},
  "status": "reserved",
  "created_at": "...",
  "expires_at": "...",
  "settled_at": null
}
```

### States

```text
reserved -> settled            (VerifyExecutionReceipt passed, SettleJob ran)
reserved -> released           (job never completed: canceled, quote/job expired, provider rejected)
reserved -> disputed -> settled   (dispute resolved in provider's favor, in whole or in part)
reserved -> disputed -> released  (dispute resolved in client's favor)
```

`reserved` and `disputed` are the only non-terminal states. Every escrow MUST reach
`settled` or `released` — an escrow with no terminal state after its expiry window is a
bug, not a valid resting state, because it silently locks client funds.

A `settled` escrow MAY still carry a `refunded` remainder (see Receipt below) when actual
usage was less than `reserved` — full settlement of the reserved amount is only correct
for `fixed`/`per_use` pricing; `metered`/`per_unit` capabilities almost always settle for
less than they reserved.

### Reservation vs. Settlement

Reservation (`CreateEscrow`) and settlement (`SettleJob`) are deliberately two different
calls, both idempotent under the invocation's `idempotency_key`:

- `CreateEscrow` only checks and holds funds. It does not know whether the job will
  succeed.
- `SettleJob` only runs once a signed execution receipt has passed
  `VerifyExecutionReceipt` (see Financial Lifecycle below). It never runs speculatively.

This mirrors a simple reserve-then-release-on-completion pattern common to escrow-style
marketplaces: money is locked at commit time, not paid out until the buyer's side of the
bargain (a verifiable delivered result) exists. ATOS's variant replaces manual "client
clicks confirm" acceptance with a signed, machine-verifiable receipt, so it can settle
without a human in the loop.

### Expiry

Every escrow inherits its quote's `expires_at` plus a bounded grace window for
in-flight jobs (recommended default: `min(job SLA timeout, 24h)`). On expiry with no
settlement:

1. the escrow auto-transitions to `released`;
2. the full reserved amount returns to the client's available balance;
3. any late-arriving receipt for that job is rejected with `settlement_failed` and
   surfaced to provider dispute tooling rather than silently retried.

A provider that consistently misses this window is a reputation signal
(`tos-core.UpdateReputationEvidence`), not a billing exception.

### Disputes

Either party may open a dispute against a `reserved` or freshly `settled` escrow within
a bounded window (recommended default: 72h after `settled_at`/expiry). Opening a dispute:

- freezes the escrow in `disputed` (blocks further release/settlement until resolved);
- does not itself reverse a completed settlement — reversal only happens if the dispute
  resolves in the client's favor, at which point resolution issues a corrective
  `SettleJob`/refund, never a raw balance edit;
- always produces an updated `Receipt` reflecting the final `charged`/`refunded` split.

Dispute adjudication logic (rules, evidence, arbitration) is intentionally out of scope
for this document — this section only defines the escrow state machine's dispute
transitions, not who decides them.

## Financial Lifecycle

```text
quote
  -> tos-core.CreateEscrow(total_max)        [reserve, not settle]  --> escrow: reserved
  -> tos-ai.SubmitJob                        [execute]
  -> provider signs execution receipt
  -> tos-core.VerifyExecutionReceipt         [stateless, read-only check]
       |-- fails / missing --------------------------> escrow stays reserved -> expires -> released
       |-- passes
       v
  -> tos-core.SettleJob                      [state change: only after verification passes]
                                                        --> escrow: settled
  -> release unused escrow                             --> refunded portion credited back
  -> issue client-facing receipt
```

Verification and settlement are separate steps on purpose: `VerifyExecutionReceipt` MUST
be stateless and MUST NOT move funds by itself. `SettleJob` is the only step allowed to
change escrow/balance state, and it MUST NOT run against a receipt that has not passed
verification. A failed or missing verification blocks settlement and routes the escrowed
amount to refund/dispute handling instead.

Cancellation (`atos_cancel_job`) before any receipt exists follows the same right-hand
branch: escrow releases in full, no settlement ever runs.

## Quote Object

A quote is immutable and time limited.

Required fields:

- `quote_id`
- `capability_id`
- `capability_version`
- `price.subtotal`
- `price.fees`
- `price.total_max`
- `currency`
- `expires_at`
- `terms_hash`

## Receipt

```json
{
  "receipt_id":"rcpt_...",
  "quote_id":"q_...",
  "escrow_id":"esc_...",
  "job_id":"job_...",
  "charged":{"amount":"4.80","currency":"USD"},
  "refunded":{"amount":"0.45","currency":"USD"},
  "status":"settled",
  "created_at":"..."
}
```

`status` mirrors the escrow's terminal state plus dispute outcomes:
`settled` | `released` | `disputed` | `settled_after_dispute` | `released_after_dispute`.
`charged + refunded` MUST always equal the escrow's original `reserved` amount — this is
an invariant clients can check without trusting the server's arithmetic.

## TOS Abstraction Boundary

Public default receipt: no chain details.

Advanced optional endpoint:

`GET /v1/receipts/{id}/settlement-proof`

May return TOS transaction/commitment/attestation information for users who explicitly request verifiability.

This gives ATOS both mainstream UX and cryptographic auditability.
