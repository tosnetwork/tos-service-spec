# Software-Work Receipt TVM V1

## Canonical role

A Receipt commits to one completed execution under one Accepted Quote. The
Receipt cell itself is evidence, not payment authority. Release additionally
requires the execution signer selected by the Accepted Quote to sign the exact
escrow settlement intent. Finalized escrow state remains the sole settlement
authority.

The first profile is intentionally fixed-price: the Receipt charge must equal
the Quote amount and the complete funded balance. A lower charge plus change
would require two non-atomic stablecoin transfers and is not supported in V1.

## Receipt cell

```text
receipt$_ magic:uint32=0x4e575231 schema:uint16=1
  completed_at:uint64 exit_code:int32
  ^binding ^outcome ^evidence ^economic = SoftwareWorkReceiptV1;

binding$_ quote_commitment:uint256 execution_id:uint256
  input_digest:uint256 = ReceiptBindingV1;

outcome$_ result_digest:uint256 artifact_digest:uint256
  report_digest:uint256 = ReceiptOutcomeV1;

evidence$_ source_digest:uint256 toolchain_digest:uint256
  sandbox_digest:uint256 = ReceiptEvidenceV1;

economic$_ charged_atomic_amount:uint128 provider_agent_id:uint256
  = ReceiptEconomicV1;
```

Every digest and identifier is non-zero. `completed_at` is a Unix timestamp,
`exit_code` must be zero for release, and the unsigned charge must be positive
and below `2^120`.
The Quote commitment transitively binds the Capability ID, immutable version,
manifest, endpoint, asset, provider, signer authorization, terms, and expiry.
Bulk output, reports, source, and artifacts remain content-addressed off-chain.

## Settlement intent and message

The execution signer signs the TVM representation hash of:

```text
settlement_intent$_ magic:uint32=0x4e534931 schema:uint16=1
  query_id:uint64 charged_atomic_amount:uint128
  escrow:MsgAddressInt quote_commitment:uint256 receipt_commitment:uint256
  = EscrowSettlementIntentV1;
```

The release message is:

```text
release$_ op:uint32=0x4e450001 query_id:uint64 signature:bits512
  ^receipt = EscrowReleaseV1;
```

The contract reconstructs the intent from its own address and stored Quote,
checks Ed25519 over `cell_hash(settlement_intent)`, validates the complete
Receipt, requires `charged == funded == Quote amount`, and enters
`release_pending`. Replays or a different query ID, Receipt, amount, escrow,
Quote, or signer fail before another transfer request can be created.

The timeout refund message is:

```text
refund$_ op:uint32=0x4e450002 query_id:uint64 = EscrowRefundV1;
```

Anyone may trigger it only from `funded` after `refund_available_at`; the sole
destination is the committed buyer. Both release and refund enter a permanent
pending state that blocks replay. A bounce of the initial request to the
escrow's own wallet restores `funded`. Standard-wallet `excesses` is not a
payment proof because it binds neither amount nor source. The finalized
resolver derives the terminal economic outcome from the exact wallet
transaction chain; an ambiguous downstream outcome remains pending and is
never blindly replayed.
