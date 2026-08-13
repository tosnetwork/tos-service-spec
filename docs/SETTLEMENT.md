# Native Quote, Execution, and Settlement Model

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

## Escrow

Escrow creation references the Accepted Quote commitment and locks no more than
its maximum price in the selected asset. State transitions are contract-defined
and idempotent. Gateway accounting is a projection of finalized escrow and
settlement transactions.

At minimum, the lifecycle distinguishes funded, accepted for execution,
released to provider, refunded to buyer, disputed, and resolved. Impossible or
ambiguous simultaneous terminal outcomes are rejected by contract state.

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

The authorized execution signer signs the canonical receipt. Bulk outputs and
evidence remain off-chain and are checked by digest.

## Settlement

Settlement verifies Accepted Quote, escrow, receipt signature, signer
authorization, immutable version, amount bounds, and prior state. It then
performs one terminal economic transition. Replaying the identical settlement
is idempotent; conflicting receipt or amount data is rejected.

## Disputes

The Accepted Quote commits to dispute terms before execution. A dispute refers
to the Quote, escrow, receipt or failure evidence, and exact challenged amount.
Resolution authority and allowed outcomes come from the committed policy, not
from the gateway that routed the job.

## Invariants

1. Proposal creation moves no funds.
2. Only finalized acceptance creates canonical purchase terms.
3. Execution cannot silently change bound version, endpoint, or signer.
4. Total release plus refund never exceeds funded escrow.
5. One escrow reaches one consistent terminal outcome.
6. Gateway balances and histories are rebuildable from finalized chain state.
7. Ambiguous submission is resolved from chain state before retry.
