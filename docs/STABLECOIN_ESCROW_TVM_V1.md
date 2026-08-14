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
  escrow_asset_wallet:MsgAddressInt funded_atomic_amount:uint128
  settled_atomic_amount:uint128 receipt_commitment:uint256
  = NativeEscrowRuntimeV1;
```

All addresses are canonical `addr_std` values. V1 uses wc=0 for the bound
stablecoin master and wallets. The deadlines are Unix seconds,
`funding_deadline > 0`, and `refund_available_at > funding_deadline`. Atomic
amounts are unsigned and bounded to 128 bits.

The initial state is `awaiting_funding`; funded and settled amounts and the
Receipt commitment are zero. The full Quote, terms, authorization, and runtime
cells are stored by reference. The three root digests must equal their actual
cell hashes. In addition:

- `quote_commitment` equals `cell_hash(accepted_quote)`;
- `escrow_terms_digest` equals both `cell_hash(escrow_terms)` and the digest in
  the Accepted Quote economic cell; and
- `execution_authorization_digest` equals both
  `cell_hash(execution_authorization)` and the digest in the Accepted Quote
  authority cell.

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
4 released
5 refunded
```

`released` and `refunded` are mutually exclusive terminal states. Pending
states are required because TOS-network stablecoin transfer is asynchronous.
The escrow may not claim a terminal outcome merely because it sent a transfer
request to its token wallet. It finalizes only from the expected wallet path
after success is proven; bounce or ambiguous outcomes remain recoverable
without authorizing a second economic transfer.

Funding must arrive through the standard stablecoin transfer-notification path
from the exact escrow wallet bound in StateInit. The notification must identify
the exact buyer and asset, arrive before the funding deadline, and credit no
more than the Quote maximum. Direct native TOS value is not funding.

Release requires the canonical Receipt, an Ed25519 signature from the committed
execution signer over a domain-separated settlement intent, an amount no
greater than the funded balance or Quote maximum, and the exact prior state.
Refund is available only under the committed objective rule, including the
timeout path after `refund_available_at`. One transition may split a funded
amount into provider release plus buyer refund, but their sum must equal the
funded amount and both outbound transfers must be accounted for before the
terminal state is finalized.

## Resolver requirements

A typed resolver reads finalized account state and fails closed unless it can
verify:

1. the expected network, account address, and escrow code hash;
2. the exact cell layouts with no trailing bits or references;
3. all root-to-reference and Quote-to-preimage digest links;
4. the finalized Capability version, manifest, non-revocation, and owner;
5. the stablecoin master identity, wallet code hash, decimals, and derived
   escrow wallet from finalized chain state;
6. lifecycle invariants and `settled <= funded <= Quote maximum`; and
7. the finalized transaction reference and checkpoint.

A missing account, unfinalized state, unknown status, mismatched hash, malformed
address, impossible amount, or ambiguous asynchronous transfer is an error,
not an empty or successful result.

## Acceptance evidence

Before the first public-testnet deployment, independent implementations must
reproduce the StateInit and address from a frozen vector. The TVM emulator
matrix must cover correct funding, release, partial-charge refund, full refund,
replay, wrong wallet/master/buyer, overfunding, early and late messages,
forged Receipt/signature, conflicting terminal actions, bounced transfers,
crash/restart resolution, malformed cells, and native-TOS/stablecoin accounting
separation.
