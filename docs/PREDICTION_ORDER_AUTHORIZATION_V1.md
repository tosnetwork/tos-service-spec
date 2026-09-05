# Prediction Order Authorization V1

Status: release candidate. This profile is additive and does not change any
previously released TOS Service object or semantic-action entry.

## 1. Security boundary

An OpenFox Intent, Operation, Agreement, Carrier publication, or local approval
is not executable order authority. A TOS PredictionMarket V1 contract accepts
only a canonical order authorized by the account's currently registered
trading key and epoch.

The signer signs the raw 32 bytes of `order_digest`. It does not sign JSON,
hexadecimal text, `order_cell_hash`, or a second hash of `order_digest`.

## 2. Primitive encodings

All integers are unsigned big-endian bit strings unless declared signed.
Addresses use canonical `addr_std` serialization and are restricted to
workchains `-1` and `0`. Every cell is an ordinary level-zero TVM cell. A
decoder consumes every bit and reference and rejects alternate tree shapes.

```text
prediction_market_binding$_
  market_address:MsgAddressInt
  market_config_hash:uint256 = PredictionMarketBindingV1;

prediction_owner_binding$_
  owner_address:MsgAddressInt
  counterparty_present:Bool
  optional_counterparty:(counterparty_present ? MsgAddressInt : ())
  = PredictionOwnerBindingV1;

prediction_order#504f5231
  schema_version:uint16
  global_id:int32
  workchain_id:int8
  key_epoch:uint32
  nonce:uint64
  salt:uint256
  quantity_lots:uint64
  min_fill_lots:uint64
  limit_price_tick:uint16
  valid_after:uint64
  valid_until:uint64
  action:uint8
  outcome:uint8
  liquidity_role:uint8
  allow_partial:Bool
  market:^PredictionMarketBindingV1
  owner:^PredictionOwnerBindingV1
  = PredictionOrderV1;
```

The enum values are:

```text
action: BUY=0, SELL=1
outcome: YES=0, NO=1
liquidity_role: MAKER=0, TAKER=1
```

`schema_version` is `1`. `market_config_hash`, `salt`, quantities, and minimum
fill are nonzero. `0 < limit_price_tick < 10000`, and
`valid_after < valid_until`. An order outcome cannot be `INVALID`.

## 3. Authorization digest

```text
prediction_order_authority_binding$_
  market_address:MsgAddressInt
  market_config_hash:uint256
  order_cell_hash:uint256 = PredictionOrderAuthorityBindingV1;

prediction_order_authorization#504f4131
  schema_version:uint16
  domain_hash:uint256
  global_id:int32
  workchain_id:int8
  contract_code_version:uint16
  binding:^PredictionOrderAuthorityBindingV1
  = PredictionOrderAuthorizationV1;
```

`domain_hash = SHA256("TOS_PREDICTION_ORDER_V1")` and
`contract_code_version = 1`. The market address, network domain and config hash
are copied from the decoded order; callers cannot supply them independently.

```text
order_cell_hash = cell_hash(PredictionOrderV1)
order_digest = cell_hash(PredictionOrderAuthorizationV1)
```

## 4. Signed transport

```text
prediction_signature$_ signature:bits512 = PredictionSignatureV1;

signed_prediction_order#50534f31
  schema_version:uint16
  trading_public_key:bits256
  order:^PredictionOrderV1
  signature:^PredictionSignatureV1
  = SignedPredictionOrderV1;
```

The signature is PureEd25519 over the raw `order_digest`. Decoders require an
exactly 512-bit signature cell with no references. Public keys must be a
canonical compressed Edwards25519 point and must not equal any of the eight
canonical encodings of the curve's 8-torsion subgroup. This application rule
is stricter than the TOS v14 VM's zero/identity footgun check and must be
identical in SDK, Agent Account, and PredictionMarket code.

The signed wrapper and order DAG together use at most six cells and depth
three. Network admission may impose a smaller byte envelope but never a larger
cell/depth allowance.

## 5. Replay and execution rules

The on-chain replay key is `(owner_address, key_epoch, nonce)`. Its first fill
or exact cancellation binds it to one `order_digest`; the same nonce with a
different digest is rejected. Rotation invalidates older epochs and
`raise_nonce_floor(n)` invalidates nonces below `n`.

The validity window is half-open:

```text
valid_after <= contract_now < valid_until <= trade_close
```

`allow_partial=false` requires the entire remaining quantity. Otherwise every
non-final fill and remainder is at least
`max(market.min_fill_lots, order.min_fill_lots)`.

The contract rejects self-trades, counterparty mismatches, two makers, two
takers, and all pairs outside the three collateral-conserving combinations in
`PREDICTION_MARKET_V1.md`.

## 6. Conformance

`test-vectors/prediction-market-v1.json` freezes canonical BOCs, cell hashes,
the authorization digest, Ed25519 key/signature, malformed trailing-data
vectors, and domain separation. `scripts/prediction-market-reference.py`
independently parses ordinary BOCs, recomputes TVM representation hashes and
verifies the RFC 8032 signature.
