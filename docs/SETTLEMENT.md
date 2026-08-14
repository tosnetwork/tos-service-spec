# Native Quote, Execution, and Settlement Model

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
its maximum price in the selected asset. State transitions are contract-defined
and idempotent. Gateway accounting is a projection of finalized escrow and
settlement transactions.

At minimum, the lifecycle distinguishes funded, accepted for execution,
release pending, refund pending, and the chain-derived economic outcomes
released or refunded. Mutually exclusive pending states prevent a second
economic transfer request. The finalized resolver derives the terminal outcome
from the exact stablecoin wallet transaction chain; a gateway callback or the
standard wallet's unbound `excesses` message is not settlement authority.

For the first release, escrow supports fixed-price release and timeout refund.
A disputed state is added only if a concrete software-work failure cannot be
decided from committed objective evidence. It must not require a
general-purpose arbitration platform.

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
records one replay-blocking transfer intent and asks the bound stablecoin wallet
to perform the economic transition. The terminal projection requires finalized
wallet transaction evidence. Replaying or conflicting receipt or amount data
cannot create another transfer request.

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
7. Ambiguous submission is resolved from chain state before retry.
