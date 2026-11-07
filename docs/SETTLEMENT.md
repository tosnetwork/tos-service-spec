# Native Quote, Execution, and Settlement Model

Prepared, submitted, ambiguous, rejected and finalized settlement facts may be
published as immutable, profile-qualified observations under
[`Agent Operation and Outcome Event V1`](AGENT_OPERATION_OUTCOME_EVENT_V1.md).
That evidence layer cannot authorize a transfer, replace finality, or change
the Quote, custody, Receipt, refund, and dispute rules in this document.

## Delivery scope

This document defines the target economic model. The first implementation is
limited to machine-checkable software work settled in native TOS on the Service
Actor contract ([`SERVICE_ACTOR_TVM_V1.md`](SERVICE_ACTOR_TVM_V1.md), binding
rules in [`SERVICE_ACTOR_SETTLEMENT_DESIGN.md`](SERVICE_ACTOR_SETTLEMENT_DESIGN.md)),
objective release or refund, and narrowly bounded dispute evidence.
Stablecoin pricing, additional TOS-network assets, subjective work,
generalized arbitration, and high-frequency payment channels require later
roadmap gates. Stablecoin pricing in particular waits for a token integration
that reports payout outcomes.

## Quote Proposal

A gateway may construct `QuoteProposalV1` after resolving a Capability version
and the Service Actor its manifest names. The proposal binds:

- Capability ID and exact version;
- provider Agent ID;
- manifest digest;
- transport binding digest;
- the actor address and code hash;
- the actor's policy version, `terms_hash`, exact price and non-refundable
  storage fee in nanoTOS;
- the attestor key id; and
- a buyer-side expiry.

`proposal_id` is gateway-local correlation data. A proposal can be discarded,
replaced, or compared with proposals from other gateways. It does not authorize
payment or execution, and every rail field must equal finalized actor state and
the manifest before a buyer uses it.

## Accepted Quote

The client verifies the proposal against finalized state and converts it into
the Accepted Quote cell of [`ACCEPTED_QUOTE_TVM_V1.md`](ACCEPTED_QUOTE_TVM_V1.md).
The deterministic Accepted Quote commitment binds network and all commercial and
execution fields except the gateway-local proposal ID. The attestor key is not
chosen by the client: it is the key the manifest pins (D5).

The buyer commits to the Quote through the `request_hash` of one Service Actor
`call` that also carries the quoted `terms_hash` and the payment. An Accepted
Quote exists for that request only after the `call` transaction is finalized
and checked. Its chain reference includes workchain, account, logical time,
transaction hash, contract code hash, finalized checkpoint, and the request ID
from the call's request snapshot message.

## Amounts

Amounts are unsigned nanoTOS encoded as canonical base-10 text:

```text
0 | [1-9][0-9]*
```

No sign, decimal point, exponent, whitespace, locale formatting, or leading
zero is allowed. Arithmetic uses checked integers below `2^120`, the bound of
the contract's Coins fields. A price is non-zero.

Gateways cannot represent an off-chain balance, bridged claim on another
network, or private ledger entry as settlement under this specification.

## Custody

The Service Actor holds each admitted request's price and storage fee from the
`call` until the request resolves. State transitions are contract-defined:

- `call` admits a request only under the quoted `terms_hash` and stores a
  snapshot of the policy and attestor; it emits that snapshot in the call
  transaction;
- `respond` by the owner with the snapshotted attestor's ML-DSA-44 signature
  over the SRP2 statement, before `response_deadline`, credits the price and
  storage fee to the provider's revenue;
- after `response_deadline` anyone may `expire` the request; the caller may
  then `claim_refund` the price before `refund_claim_deadline`;
- at or after `refund_claim_deadline` anyone may sweep an unanswered request;
  the sweep returns the price to the caller and pays the sweeper a bounded
  cleanup bounty out of the storage fee.

Respond and expire partition time exactly at `response_deadline`. A request
resolves once. Gateway accounting is a projection of finalized actor
transactions; a gateway callback is not settlement authority.

## Execution

Execution begins only after the `call` is finalized and the request is
verified pending under the quoted `terms_hash` and `request_hash`. The dispatch
envelope binds Quote commitment, Capability version, manifest, endpoint,
attestor key id, input digest, idempotency identity, the actor and request ID,
and `response_deadline`. The provider must reserve enough time before
`response_deadline` for execution, Receipt construction, attestor signing, and
inclusion of the `respond`; after the deadline only a refund is possible.

A routing change is valid only if it remains within the endpoint and attestor
committed by the Accepted Quote. Otherwise the client must accept a new Quote.

## Receipt

A successful receipt binds:

- Accepted Quote and execution identity;
- Capability and version;
- input digest;
- result and artifact digests;
- charged amount, equal to the price;
- provider Agent;
- completion time; and
- any evidence commitment required by the Quote.

For the software-work profile, the Receipt also binds repository or source
reference, toolchain or sandbox image digest, operation descriptor, exit status,
test or scan report digest, and reproducible artifact digest where applicable.

The attestor signs the SRP2 statement whose `response_hash` is the Receipt cell
hash ([`SOFTWARE_WORK_RECEIPT_TVM_V1.md`](SOFTWARE_WORK_RECEIPT_TVM_V1.md)).
Bulk outputs and evidence remain off-chain and are checked by digest.

## Settlement

The contract verifies the owner sender, the request's pending state and
deadline, and the snapshotted attestor's signature over SRP2. It does not decode
the Receipt: the exit status, charge and digests are enforced by attestor
custody, which refuses to sign a Receipt that is not releasable under the
manifest (D9). A buyer holding a signed non-conforming Receipt has off-chain
evidence of misbehaviour, not an on-chain remedy.

`respond` sends no value: the release is a credit to the provider's revenue,
which the owner later withdraws. A refund or sweep pays the caller directly.
The terminal outcome is derived from the actor's finalized transaction history
(responded, refunded, or swept), never from a gateway.

## Disputes

The dispute policy is fixed by contract code: an attested response before the
deadline pays; otherwise the price returns to the caller. A dispute refers to
the Quote, the request snapshot, the Receipt or failure evidence, and the exact
challenged amount, and it has no on-chain effect in this profile.

Subjective quality judgments and generalized marketplace arbitration are outside
scope.

## Asset roles

Native TOS pays contract execution, Registry operations, relaying, protocol
security costs, and, in the current domain, the provider service itself. Wallets
and accounting views must show the service price, the non-refundable storage
fee, and network fees separately.

## Invariants

1. Proposal creation moves no funds.
2. Only a finalized `call` under the quoted `terms_hash` creates canonical
   purchase terms for a request.
3. Execution cannot silently change bound version, endpoint, or attestor.
4. Each request resolves exactly once: its price goes either to provider
   revenue on an attested response or back to the caller.
5. The storage fee is never refunded; the Quote discloses it.
6. Gateway balances and histories are rebuildable from finalized chain state.
7. An ambiguous settlement request is resolved from chain state before retry.
