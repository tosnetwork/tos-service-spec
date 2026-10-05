# Native Stablecoin Escrow TVM V2

**Status:** experimental; deployable only for non-production use (see
[Deployment restriction](#deployment-restriction)).

**Released code:** `tos-service-stablecoin-escrow-v2`, code hash
`tvm-cell-sha256:d6d53a11bcda151b2e7d6b4b2f275eeadea8eb9b66496c24b0b7c54453d6d209`.
This is the only stablecoin escrow code that conforming tooling builds,
deploys, resolves, or settles against. Escrow version 1 was retired on
2026-10-05; its storage layout, settlement intent, and deployment-as-acceptance
rule are not part of this protocol.

## Purpose and authority

The escrow is the canonical custody boundary for one Accepted Quote of the
Paid Demand profile ([`PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md`](PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md)).
Its StateInit embeds the complete Accepted Quote cell (schema 2). Deployment is
not acceptance: the deterministic account starts in `pending_acceptance`, and
only the bound buyer wallet may accept the Quote before `accept_by`. Funding is
a separate later transition. Finalized typed contract state is the sole
authority for acceptance, funding, and settlement; gateways, relayers, local
journals, and portable CBOR are projections only.

The escrow accepts only the exact stablecoin issued on TOS Network that the
Accepted Quote binds. Native TOS attached to messages pays execution and
storage fees; it is never counted as service payment.

## StateInit data

```text
escrow_data$_ magic:uint32=0x4e455331 version:uint16=2 status:uint8
  quote_commitment:uint256 escrow_terms_digest:uint256
  execution_authorization_digest:uint256
  ^accepted_quote ^escrow_terms ^execution_authorization ^runtime
  = NativeEscrowDataV2;

escrow_terms$_ magic:uint32=0x4e455431 version:uint16=1
  buyer:MsgAddressInt provider:MsgAddressInt
  funding_deadline:uint64 refund_available_at:uint64
  = NativeEscrowTermsV1;

execution_authorization$_ magic:uint32=0x4e454131 version:uint16=1
  signer_ed25519_public_key:uint256 = NativeEscrowAuthorizationV1;

escrow_runtime$_ magic:uint32=0x4e455231 version:uint16=2
  funded_atomic_amount:uint128 settled_atomic_amount:uint128
  receipt_commitment:uint256 pending_query_id:uint64 accepted_at:uint64
  ^asset_route ^transport_binding ^dispute_policy
  = NativeEscrowRuntimeV2;

asset_route$_ magic:uint32=0x4e455031 version:uint16=2
  stablecoin_master:MsgAddressInt wallet_code_hash:uint256 ^wallet_code
  = NativeEscrowAssetRouteV2;
```

The terms and execution-authorization cells keep version 1 inside the v2
contract; they are not escrow version 1. `accepted_quote` is an Accepted Quote
of schema 2 whose authority cell carries the Paid Demand extension.

All addresses are canonical `addr_std` values on workchain 0, and the escrow
itself must be on workchain 0. The contract refuses data that does not satisfy:

- every root digest equals the hash of the referenced cell, and the Accepted
  Quote binds the same escrow-terms, authorization, transport-binding, and
  dispute-policy digests;
- `funding_deadline > 0` and `refund_available_at > funding_deadline`;
- `accept_by == Quote.expires_at`, `accept_by <= funding_deadline <
  execution_deadline < refund_available_at`;
- the execution signer key is non-zero and not a small-order or non-canonical
  Ed25519 point (exit code 2411);
- the route master and wallet-code hash equal the Quote asset, and
  `cell_hash(wallet_code)` equals the route hash;
- the Quote amount is a canonical decimal below `2^120`.

The initial state is `pending_acceptance` with every runtime amount, the
Receipt commitment, the pending query ID, and `accepted_at` zero. The escrow
derives its own stablecoin wallet at run time from `my_address()`, the master,
and the wallet code, with the wallet data `status:uint4=0 balance:Coins=0
owner master`; `get_escrow_wallet` returns that address, and resolvers must
reproduce it independently rather than trust the getter.

The escrow address is `0:cell_hash(StateInit)` for the ordinary StateInit
`split_depth:none special:none code:(just ^code) data:(just ^escrow_data)
library:none`.

## Lifecycle

```text
0 pending_acceptance
1 awaiting_funding
2 funded
3 release_pending
4 refund_pending
```

### Accept

```text
accept$_ op:uint32=0x4e450003 query_id:uint64 quote_commitment:uint256
  provider_offer_digest:uint256 = EscrowAcceptV2;
```

Accepted only from the committed buyer address, with a non-zero query ID and
the exact Quote commitment and Provider Offer digest (otherwise exit 2409), and
only while `now < accept_by` (exit 2405). It records `accepted_at = now` and
enters `awaiting_funding`. An exact replay after acceptance is a no-op.

### Fund

Funding arrives only as a stablecoin `transfer_notification` (`0x7362d09c`)
from the escrow's own derived wallet, while `awaiting_funding`, from the
committed buyer, at or before `funding_deadline`, for exactly the Quote amount.
It sets `funded_atomic_amount` and enters `funded`. The notification handler
never throws: a notification that does not fund is answered by returning the
jettons to the funder (query ID 0, reason `0xffffffa1`), and a notification from
any wallet other than the derived one asks that wallet to return them (reason
`0xffffffa2`), so jettons credited through a differently laid out wallet are
not orphaned. Native TOS is never funding.

### Release

```text
release$_ op:uint32=0x4e450001 query_id:uint64 signature:bits512
  ^receipt = EscrowReleaseV2;
```

The Receipt is the software-work Receipt cell of
[`SOFTWARE_WORK_RECEIPT_TVM_V1.md`](SOFTWARE_WORK_RECEIPT_TVM_V1.md), bound to
this Quote, with `exit_code == 0`, `0 < completed_at <= execution_deadline`,
`completed_at <= now`, `completed_at < refund_available_at`, a charge equal to
the Quote amount, and the Quote's provider Agent. The signature is Ed25519 by
the committed execution signer over `cell_hash(settlement_intent)`:

```text
settlement_intent$_ magic:uint32=0x4e534931 version:uint16=2
  global_id:int32 query_id:uint64 charged_atomic_amount:uint128
  escrow:MsgAddressInt ^settlement_hashes = EscrowSettlementIntentV2;

settlement_hashes$_ quote_commitment:uint256 receipt_commitment:uint256
  = EscrowSettlementHashesV2;
```

`global_id` is the network's ConfigParam 19, which the contract reads with
`GLOBALID`: a signature made for one network does not settle on another. A
version 1 intent (no network, hashes inline) is refused with exit 2407.

From `funded`, and only while `now <= execution_deadline` and
`now < refund_available_at`, a valid release enters `release_pending`, records
the charge, Receipt commitment, and query ID, and sends one stablecoin transfer
of the charge to the committed provider. While `release_pending`, the identical
release is a no-op and any other is refused.

### Refund

```text
refund$_ op:uint32=0x4e450002 query_id:uint64 = EscrowRefundV2;
```

From `funded`, at or after `refund_available_at`, any sender may trigger the
objective timeout refund with a non-zero query ID; it enters `refund_pending`
and sends the funded amount to the committed buyer. While `refund_pending`,
the identical refund is a no-op.

### Settlement funding and bounce

Each settlement transfer attaches exactly `0.1 TOS`, paid from the escrow's
balance, after reserving a `0.05 TOS` storage floor. A release or refund is
refused (exit 2410) unless the balance covers that payout budget, the
configuration-derived compute and forward fees, and the floor. A bounce of the
settlement request from the escrow's own wallet whose query ID equals the
pending one restores `funded` with zero settled amount, Receipt commitment, and
query ID. The contract retains no consumed-query history, so after such a
bounce a previously public valid release or refund may be replayed; resolvers
attribute attempts by finalized transaction order and the stored pending query.
`excesses` messages are ignored and prove nothing.

### Known limitation (accepted risk)

If the recipient's wallet refuses a payout (for example, a wallet the
stablecoin administrator has locked for incoming transfers), the jettons bounce
into the escrow's own wallet and are re-credited there without telling the
escrow. The escrow stays `release_pending` or `refund_pending` and no operation
moves those funds. With the issuer's unchanged wallet the escrow cannot
distinguish this from a delivered payout followed by unrelated jettons, so any
retry could pay twice. Funds can be stranded indefinitely.

## Deployment restriction

Because of that limitation, escrow v2 is deployable only on local or test
networks with test assets. Every deployment tool must refuse to deploy it
unless the operator explicitly acknowledges a non-production test deployment,
must check that acknowledgment before preparing and again before broadcasting,
and must record it in the deployment evidence (`"non_production": true`).
Production support requires a new integration in which the token's wallet
reports each payout's outcome to the escrow in an authenticated,
request-specific, replay-safe way.

## Errors

| Exit code | Meaning |
|---|---|
| 2400 | malformed or unknown message |
| 2401 | invalid stored state or transition from the wrong status |
| 2402 | wrong wallet |
| 2403 | wrong buyer |
| 2404 | wrong amount |
| 2405 | deadline violated |
| 2406 | invalid Receipt |
| 2407 | settlement signature does not verify over the version 2 intent |
| 2408 | unauthenticated bounce |
| 2409 | invalid acceptance |
| 2410 | balance does not cover the settlement budget |
| 2411 | weak execution-signer key |

## Getters

- `get_escrow_state` returns `(status, funded, settled, receipt_commitment,
  pending_query_id, accepted_at)`;
- `get_escrow_cells` returns `(accepted_quote, escrow_terms,
  execution_authorization, runtime)`;
- `get_escrow_wallet` returns the derived stablecoin wallet address.

## Resolver requirements

A typed resolver reads finalized account state and fails closed unless it
verifies the released code hash, the exact v2 cell layouts with no trailing
bits or references, every digest link, the status-specific runtime invariants,
the derived wallet, and the finalized transaction reference and checkpoint. A
terminal released or refunded outcome is derived only from the finalized
escrow-to-wallet-to-recipient transaction chain. A missing account, unknown
status or version, mismatched hash, or ambiguous asynchronous transfer is an
error, not an empty or successful result.

## Conformance vectors

Cross-language vectors are produced by running the released contract in the
TOS sandbox on an escrow built by the Go codec
(`scripts/generate-escrow-v2-vectors.sh` in tos-service-protocol). They record
the data cell the contract writes after accept, fund, release, and refund, its
getter answers, the settlement intent it accepted a signature over, and the
exit codes for a version 1 intent (2407), an intent for another network (2407),
and version 1 data (2401).
