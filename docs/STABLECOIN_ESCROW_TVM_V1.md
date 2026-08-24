# Native Stablecoin Escrow TVM V1

## Purpose and authority

This contract is the canonical custody boundary for one Accepted Quote. Its
StateInit embeds the complete Accepted Quote cell. The finalized deployment
transaction is the Quote acceptance event, and finalized typed contract state
is the sole authority for funding and settlement. Gateways, relayers, local
journals, and portable CBOR are projections only.

The escrow accepts only the exact stablecoin issued on TOS Network that is
bound by the Accepted Quote. Native TOS attached to messages pays execution and
storage fees; it is never counted as service payment.

An escrow must not be deployed as a canonical acceptance event until its
funding, release, refund, asynchronous token-transfer recovery, emulator test,
and resolver matrices are complete. A pre-funded shell would have a different
code hash and address from the finished contract and therefore cannot be
treated as an upgradeable milestone.

## StateInit data

```text
escrow_data$_ magic:uint32=0x4e455331 schema:uint16=1 status:uint8
  quote_commitment:uint256 escrow_terms_digest:uint256
  execution_authorization_digest:uint256
  ^accepted_quote ^escrow_terms ^execution_authorization ^runtime
  = NativeEscrowDataV1;

escrow_terms$_ magic:uint32=0x4e455431 schema:uint16=1
  buyer:MsgAddressInt provider:MsgAddressInt
  funding_deadline:uint64 refund_available_at:uint64
  = NativeEscrowTermsV1;

execution_authorization$_ magic:uint32=0x4e454131 schema:uint16=1
  signer_ed25519_public_key:uint256 = NativeEscrowAuthorizationV1;

escrow_runtime$_ magic:uint32=0x4e455231 schema:uint16=1
  funded_atomic_amount:uint128 settled_atomic_amount:uint128
  receipt_commitment:uint256 pending_query_id:uint64
  ^asset_route ^transport_binding ^dispute_policy
  = NativeEscrowRuntimeV1;

asset_route$_ magic:uint32=0x4e455031 schema:uint16=1
  stablecoin_master:MsgAddressInt wallet_code_hash:uint256 ^wallet_code
  = NativeEscrowAssetRouteV1;
```

All addresses are canonical `addr_std` values. V1 uses wc=0 for the bound
stablecoin master and wallets. The deadlines are Unix seconds,
`funding_deadline > 0`, and `refund_available_at > funding_deadline`. Atomic
amount fields occupy 128 bits, but valid values are bounded below `2^120` to
match the stablecoin wallet's canonical `Coins` encoding.

The initial state is `awaiting_funding`; funded and settled amounts, the
Receipt commitment, and pending query ID are zero. The full Quote, terms,
authorization, and runtime cells are stored by reference. The route embeds the
exact stablecoin wallet code preimage. The escrow derives its wallet at runtime
from `my_address()`, the master, and that code; storing the derived address in
StateInit would create an invalid circular address dependency. The root digests
must equal their actual cell hashes. In addition:

- `quote_commitment` equals `cell_hash(accepted_quote)`;
- `escrow_terms_digest` equals both `cell_hash(escrow_terms)` and the digest in
  the Accepted Quote economic cell; and
- `execution_authorization_digest` equals both
  `cell_hash(execution_authorization)` and the digest in the Accepted Quote
  authority cell; and
- the route master and wallet code hash equal the Accepted Quote asset, while
  `cell_hash(wallet_code)` equals the route wallet code hash; and
- `cell_hash(transport_binding)` and `cell_hash(dispute_policy)` equal the
  corresponding Accepted Quote digests and both cells satisfy their frozen V1
  schemas.

Opaque placeholder digests are therefore not deployable. The exact buyer,
provider payout address, deadlines, and execution signing key have public,
typed preimages.

The ordinary TVM StateInit encoding is:

```text
split_depth:none special:none code:(just ^code) data:(just ^escrow_data)
library:none
```

The escrow address is `workchain:cell_hash(StateInit)`. Its identity is bound
to the complete terms and implementation code, not assigned by a gateway.

## Lifecycle

V1 reserves these typed states:

```text
0 awaiting_funding
1 funded
2 release_pending
3 refund_pending
```

V1 has no on-chain `accepted_for_execution`, `submitted`, `evaluating`, or
`approved` state. Execution admission and result submission may appear in
rebuildable provider or SDK projections, but they cannot delay, redirect, or
replace these contract transitions.

The two pending states are mutually exclusive and block another economic
transfer request while pending. Only an authenticated bounce of the initial
request from the escrow's own wallet restores `funded`; otherwise the pending
state cannot be retried or replaced. TOS-network stablecoin transfer is
asynchronous, so
the escrow may not claim a terminal outcome merely because it sent a transfer
request to its token wallet. Standard-wallet `excesses` messages commit only to
a caller-selected query ID; they do not bind the transferred asset amount or
source and are therefore non-authoritative. The contract deliberately ignores
them. A resolver derives the terminal `released` or `refunded` outcome only
from the finalized escrow-to-wallet transaction chain and exact wallet balance
changes. An ambiguous downstream outcome remains pending without authorizing a
second economic transfer.

The bounce transition clears `pending_query_id`; schema 1 retains no consumed-
query set or settlement generation. Therefore, after a bounce restores
`funded`, any previously public valid release or refund message may be
permissionlessly replayed with its old query ID and may win the next valid
transition. Distinct query IDs are client hygiene, not contract replay
protection. The resolver groups every such old/new attempt under its unchanged
semantic release or refund action and follows finalized transaction order and
the currently stored pending query. A consumed-query or generation guarantee
requires a successor escrow schema and code hash.

Funding must arrive through the standard stablecoin transfer-notification path
from the exactly derived escrow wallet. The notification must identify the
exact buyer and asset, be accepted in a handling transaction whose contract
time is at or before both the funding deadline and the schema-1 Quote
`expires_at` cutoff, and equal the Quote amount. Equivalently, schema 1 requires
`now <= min(funding_deadline, Quote.expires_at)`. The transaction may be
observed as finalized later; resolver observation time is not the deadline
input. Direct native TOS value is not funding. A successor schema may version-
dispatch a different funding predicate, but it does not reinterpret this
frozen schema-1 rule.

Release requires the canonical Receipt, an Ed25519 signature from the committed
execution signer over a domain-separated settlement intent, an exact-price
charge equal to the funded balance and Quote amount, and the exact prior state.
The contract accepts that release only from `funded` while its current time is
strictly less than `refund_available_at`. Refund is accepted only from `funded`
at or after `refund_available_at` under the committed objective timeout rule.
Finalized transaction ordering resolves a boundary race: the first valid
transition changes the state, and the mutually exclusive pending state rejects
the other action. An off-chain submission timestamp cannot reserve priority.

The V1 contract attaches exactly `0.1 TOS` to the outbound request sent to its
stablecoin wallet. This fixed upper bound covers the wallet-to-wallet transfer
and return-message processing under the frozen testnet fee schedule.
It is protocol overhead, never part of the stablecoin price. A deployment must
revalidate this bound against the target network fee configuration; an
insufficient outbound budget aborts or bounces without authorizing a second
economic transfer.

V1 deliberately has one stablecoin transfer leg per terminal transition:
successful work releases the complete fixed price to the provider; timeout
refunds the complete fixed price to the buyer. Supporting a partial charge plus
change would require two asynchronous transfers that cannot be made atomic by
the standard wallet-owner callback. That feature is outside V1.

Contract and resolver vectors must cover an authenticated bounce followed by
old-query permissionless replay, old/new attempt races for both release and
refund, repeated bounce/replay fee consumption, and exact attribution of the
one accepted pending transition. No vector may assume the new query wins.

An ACP-style `submitted -> evaluator decision -> settlement` lifecycle, an
Evaluator fee split, or any extension allowed to decide release/refund requires
a separately versioned escrow schema, code hash, resolver, deadline/fallback
analysis, and conformance suite. It cannot be introduced as an application
callback or by reinterpreting these four states. Any successor must preserve a
bounded refund escape path that an unavailable Evaluator cannot block.

## Resolver requirements

A typed resolver reads finalized account state and fails closed unless it can
verify:

1. the expected network, account address, and escrow code hash;
2. the exact cell layouts with no trailing bits or references;
3. all root-to-reference and Quote-to-preimage digest links;
4. the finalized Capability version, manifest, non-revocation, and owner;
5. the stablecoin master identity, wallet code hash, decimals, and derived
   escrow wallet from finalized chain state;
6. lifecycle invariants and the fixed-price rule
   `settled == funded == Quote amount` for release;
7. for a derived terminal outcome, the exact finalized transaction chain from
   the escrow through its derived wallet to the derived recipient wallet, with
   the expected amount and resulting balance changes; and
8. the finalized transaction references and checkpoint.

A missing account, unfinalized state, unknown status, mismatched hash, malformed
address, impossible amount, or ambiguous asynchronous transfer is an error,
not an empty or successful result.

`get_escrow_wallet` exposes the address derived from the committed master and
wallet-code preimage. Resolvers must independently reproduce it rather than
accepting the getter as authority.

## Acceptance evidence

Before the first public-testnet deployment, independent implementations must
reproduce the StateInit and address from a frozen vector. The TVM emulator
matrix must cover correct funding, fixed-price release, full refund,
replay, wrong wallet/master/buyer, overfunding, early and late messages,
forged Receipt/signature, release immediately before and at the refund boundary,
conflicting release/refund ordering, bounced transfers,
forged `excesses`, crash/restart resolution, malformed cells, and
native-TOS/stablecoin accounting separation.
