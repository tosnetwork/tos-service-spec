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
Where a typed Quote successor commits an execution deadline, its Gate and
Receipt builder must additionally prove `completed_at <= execution_deadline`,
and that successor escrow must decode the bound deadline and enforce the same
comparison before accepting release. Provider-side tooling alone cannot enforce
a buyer term. Schema-1 escrow has no such field and retains its frozen rule.
The timestamp remains signed evidence; it does not extend the escrow cutoff or
reserve a settlement position.

That comparison does not independently prove wall-clock truth. The successor
profile makes the Quote-bound execution signer the explicit time attestor and
requires its custody policy to sign only an immutable completion record bound to
the same Gate claim, runner journal, and conservative clock interval. An
arbitrary or backdated timestamp, or a signer detached from those records, is
not releasable under that profile.

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

The retry-stable semantic release template is the domain-separated tuple of
escrow, Quote commitment, Receipt commitment, and charged amount; it excludes
`query_id`, signature bytes, local revision/cursor/time, and transport-attempt
metadata. A stable release action ID commits to that template. Each protocol
attempt then selects one `query_id`, constructs the exact
`EscrowSettlementIntentV1`, and obtains its exact signature. An ambiguous
broadcast reuses those same bytes until resolved. After an authenticated bounce
restores `funded`, operator-controlled recovery tooling may create a new query-
specific intent and signature under the unchanged semantic release action, but
automatic policy does not retry and query distinctness is not a V1 contract
invariant.

The contract reconstructs the intent from its own address and stored Quote,
checks Ed25519 over `cell_hash(settlement_intent)`, validates the complete
Receipt, requires `charged == funded == Quote amount`, and enters
`release_pending`. While pending, any replay or different request fails before
another transfer request can be created. An authenticated bounce clears
`pending_query_id` and restores `funded` without retaining consumed-query
history. Consequently, any previously public valid release message—including
the same query ID and signature—may be permissionlessly replayed and accepted
again if the other `funded` and deadline predicates still hold. The resolver
must group old and new query-specific attempts under the one semantic release
action and use finalized transaction order/pending state to identify the
attempt actually accepted; it must not report an old-query replay as a new
commercial action or an impossible contract conflict.

Provider tooling must preserve the execution-signing custody boundary. It
first emits `cell_hash(settlement_intent)` as a 32-byte signing payload, accepts
only a signature response that repeats the exact payload and Quote-bound public
key, verifies Ed25519 locally, and only then constructs the release message.
Receipt tooling must never accept a mnemonic, private seed, or test-identity
fixture as an operational signing input.

The timeout refund message is:

```text
refund$_ op:uint32=0x4e450002 query_id:uint64 = EscrowRefundV1;
```

The retry-stable semantic refund template binds the domain, escrow, Quote
commitment, committed buyer, and objective refund rule, but excludes `query_id`
and attempt metadata. An ambiguous refund broadcast reuses one exact attempt;
after an authenticated bounce restores `funded`, operator-controlled recovery
tooling may use a new query ID under the unchanged semantic refund action, while
automatic policy does not retry. The contract does not enforce freshness or
retain old refund query IDs, so a prior public refund message may also be
permissionlessly replayed after the bounce.

Anyone may trigger it only from `funded` at or after `refund_available_at`;
the sole destination is the committed buyer. Both release and refund enter a
pending state that blocks another request while pending. Only an authenticated
bounce of the initial request from the escrow's own wallet restores `funded`;
otherwise the request cannot be retried or replaced. Standard-wallet `excesses`
is not a payment proof because it binds neither amount nor source. The finalized
resolver derives the terminal economic outcome from the exact wallet transaction
chain; an ambiguous downstream outcome remains pending and is never blindly
replayed.

Conformance tests must race old-query replay against a newly generated release
attempt after bounce and do the same for refund. They must prove that only the
first valid `funded -> *_pending` transaction takes effect, every observed query
is grouped under the unchanged semantic action, and no resolver or client
mistakes off-chain distinct-query policy for replay protection. A stronger
consumed-query or settlement-generation invariant requires a new escrow schema.

The Receipt contains no Evaluator identity, score, approval, fee, or challenge
authority. A market, buyer, or third party may publish a separately signed
advisory assessment, but software-work V1 must ignore it for release and refund.
A binding evaluation step requires a new Quote/escrow profile; it cannot be
smuggled into `report_digest`, `evidence`, or the execution-signing key.
