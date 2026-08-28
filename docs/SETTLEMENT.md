# Native Quote, Execution, and Settlement Model

Prepared, submitted, ambiguous, rejected and finalized settlement facts may be
published as immutable, profile-qualified observations under
[`Agent Operation and Outcome Event V1`](AGENT_OPERATION_OUTCOME_EVENT_V1.md).
That evidence layer cannot authorize a transfer, replace finality, or change
the Quote, escrow, Receipt, refund, and dispute rules in this document.

## Delivery scope

This document defines the target economic model. The first implementation is
limited to machine-checkable software work, one supported stablecoin issued on
TOS Network, native TOS network fees, objective release or refund, and narrowly
bounded dispute evidence. Additional TOS-network assets, subjective work,
generalized arbitration, and high-frequency payment channels require later
roadmap gates.

## Quote Proposal

A gateway may construct `QuoteProposalV1` after resolving a Capability version.
The proposal binds:

- Capability ID and exact version;
- provider Agent ID;
- manifest digest;
- transport binding digest;
- maximum price and asset;
- escrow terms digest;
- dispute policy digest; and
- expiry.

`proposal_id` is gateway-local correlation data. A proposal can be discarded,
replaced, or compared with proposals from other gateways. It does not authorize
payment or execution.

## Accepted Quote

The client validates terms and chooses an execution-signer authorization. The
deterministic Accepted Quote commitment binds network and all commercial and
execution fields except the gateway-local proposal ID. The client submits the
commitment in a TOS transaction.

An Accepted Quote exists only after the transaction is finalized and checked.
Its chain reference includes workchain, account, logical time, transaction
hash, contract code hash, and finalized checkpoint.

## Amounts

Money uses an asset identifier and unsigned atomic amount encoded as canonical
base-10 text:

```text
0 | [1-9][0-9]*
```

No sign, decimal point, exponent, whitespace, locale formatting, or leading
zero is allowed. Arithmetic uses checked integers with asset-specific bounds.

The typed `asset` identity contains the wc=0 master account ID, master code
hash, wallet code hash, and decimals on the same TOS network as the Accepted
Quote. Resolution verifies every value and active status from finalized TOS
state. A ticker such as `USD` or `USDT` is display metadata and is never a
canonical asset identifier. Gateways cannot represent an off-chain balance,
bridged claim on another network, or private ledger entry as settlement under
this specification.

## Escrow

Escrow creation references the Accepted Quote commitment and locks no more than
its maximum price in the selected asset. State transitions are contract-
defined. Exact replay cannot create another wallet request while escrow is
pending or terminal. After an authenticated bounce restores `funded`, frozen
schema 1 may accept an old public request again because it retains no consumed-
query history; resolver-level idempotency groups that transition under the same
semantic action. Gateway accounting is a projection of finalized escrow and
settlement transactions.

The first escrow contract distinguishes `awaiting_funding`, `funded`,
`release_pending`, and `refund_pending`, plus the chain-derived economic
outcomes released or refunded. `accepted_for_execution`, `result_ready`,
and any future `evaluating` label are Gate or SDK projections, not V1 escrow
states. Mutually exclusive pending states prevent a second economic transfer
request. The finalized resolver derives the terminal outcome from the exact
stablecoin wallet transaction chain; a gateway callback or the standard
wallet's unbound `excesses` message is not settlement authority.

For the first release, escrow supports fixed-price release before the committed
refund boundary and timeout refund at or after it. The Execution Gate must
reserve the schema-dispatched worst case. For the paid-demand successor, that
means the exact committed preflight-to-start delay, effective runtime derived
no greater than the manifest limit, and a nonzero margin for bounded objective
validation; evidence/report and Receipt construction; query-specific signing;
initial release inclusion; and definitive downstream acceptance of that initial
wallet request without bounce, strictly before the refund boundary, with a
fresh same-claim preflight before first process start. Frozen escrow V1 forgets
the pending query on bounce, so a public old release/refund attempt may be
permissionlessly replayed from `funded`; distinct queries do not create a finite
contract-enforced retry bound. Automatic execution therefore requires a proven
zero-bounce initial release path, otherwise it remains disabled. A separately
versioned settlement-critical successor may preserve the valid pre-cutoff
semantic release action or consumed-query generation across bounces; that is
outside current V1. Merely starting before the refund time is unsafe. A
downstream accepted transfer may finalize provider
credit later because `release_pending` already blocks refund; the bound
establishes release priority, not terminal payout latency. A binding Evaluator,
disputed state, fee split, or challenge flow
requires a separately versioned Quote and escrow profile with an explicit
timeout fallback. It cannot be added by a general-purpose arbitration callback
or by reinterpreting V1 state.

For the first lifecycle, escrow deployment embeds the complete Accepted Quote
cell in StateInit. Its finalized deployment transaction is the canonical Quote
acceptance transaction. This does not reintroduce an Action Anchor: the escrow
exists because it has continuing custody and settlement behavior.

## Execution

Execution begins only after the Accepted Quote and required escrow state are
finalized. The dispatch envelope binds Quote commitment, Capability version,
manifest, endpoint, authorized signer, input digest, idempotency identity, and
deadline.

A routing change is valid only if it remains within the endpoint and signer set
committed by the Accepted Quote. Otherwise the client must accept a new Quote.

## Receipt

A successful receipt binds:

- Accepted Quote and execution identity;
- Capability and version;
- input digest;
- result and artifact digests;
- measured usage used for pricing;
- charged atomic amount;
- provider Agent and execution signer;
- completion time; and
- any evidence commitment required by the Quote.

For the software-work profile, the Receipt also binds repository or source
reference, toolchain or sandbox image digest, operation descriptor, exit status,
test or scan report digest, and reproducible artifact digest where applicable.

The authorized execution signer signs the canonical receipt. Bulk outputs and
evidence remain off-chain and are checked by digest.

## Settlement

Settlement verifies Accepted Quote, escrow, receipt signature, signer
authorization, immutable version, amount bounds, and prior state. It then
records one pending transfer intent and asks the bound stablecoin wallet to
perform the economic transition. While escrow remains pending or reaches a
terminal outcome, replay or conflicting receipt/amount data cannot create
another transfer request. Frozen schema 1 clears the pending query if that
wallet request authentically bounces, however, so an old public release/refund
attempt may recreate the same semantic action from restored `funded` and race a
new operator attempt. The resolver groups those attempts; automatic policy does
not retry after bounce and requires a proven zero-bounce initial release path.
The terminal projection requires finalized wallet transaction evidence.

## Disputes

The Accepted Quote commits to dispute terms before execution. A dispute refers
to the Quote, escrow, receipt or failure evidence, and exact challenged amount.
Resolution authority and allowed outcomes come from the committed policy, not
from the gateway that routed the job.

Initial-release disputes are narrow exceptions around objective software-work
evidence. Subjective quality judgments and generalized marketplace arbitration
are outside scope.

## Asset roles

Native TOS pays contract execution, Registry operations, relaying, and protocol
security costs. The provider service is denominated in the exact TOS-network
stablecoin selected by the Accepted Quote. Wallets and accounting views must
show stablecoin service payment and native TOS fees separately.

## Invariants

1. Proposal creation moves no funds.
2. Only finalized acceptance creates canonical purchase terms.
3. Execution cannot silently change bound version, endpoint, or signer.
4. Total release plus refund never exceeds funded escrow.
5. One escrow creates at most one terminal economic transfer, and its outcome
   is derived from finalized wallet transaction evidence.
6. Gateway balances and histories are rebuildable from finalized chain state.
7. An ambiguous settlement request is resolved from chain state before retry.
