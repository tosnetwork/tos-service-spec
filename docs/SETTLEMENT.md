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

## Financial Lifecycle

```text
quote
  -> tos-core.CreateEscrow(total_max)        [reserve, not settle]
  -> tos-ai.SubmitJob                        [execute]
  -> provider signs execution receipt
  -> tos-core.VerifyExecutionReceipt         [stateless, read-only check]
  -> tos-core.SettleJob                      [state change: only after verification passes]
  -> release unused escrow
  -> issue client-facing receipt
```

Verification and settlement are separate steps on purpose: `VerifyExecutionReceipt` MUST
be stateless and MUST NOT move funds by itself. `SettleJob` is the only step allowed to
change escrow/balance state, and it MUST NOT run against a receipt that has not passed
verification. A failed or missing verification blocks settlement and routes the escrowed
amount to refund/dispute handling instead.

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
  "job_id":"job_...",
  "charged":{"amount":"4.80","currency":"USD"},
  "refunded":{"amount":"0.45","currency":"USD"},
  "status":"settled",
  "created_at":"..."
}
```

## TOS Abstraction Boundary

Public default receipt: no chain details.

Advanced optional endpoint:

`GET /v1/receipts/{id}/settlement-proof`

May return TOS transaction/commitment/attestation information for users who explicitly request verifiability.

This gives ATOS both mainstream UX and cryptographic auditability.
