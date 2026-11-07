# Software-Work Receipt TVM V1

## Canonical role

A Receipt commits to one completed execution under one Accepted Quote. The
Receipt cell itself is evidence, not payment authority. Release on the Service
Actor rail ([`SERVICE_ACTOR_TVM_V1.md`](SERVICE_ACTOR_TVM_V1.md)) requires the
attestor key that the manifest pins and the request snapshotted to sign the
SRP2 statement whose `response_hash` is this Receipt's cell hash, and the actor
owner to submit it as `respond`. Finalized Service Actor transactions remain
the sole settlement authority.

The first profile is intentionally fixed-price: the Receipt charge equals the
quoted price, the request's snapshotted `price_per_call` in nanoTOS.

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
and below `2^120`. For the Service Actor rail, `quote_commitment`,
`execution_id` and `input_digest` equal the request's `ServiceRequestV1`
preimage, `charged_atomic_amount` equals the price, and `provider_agent_id`
equals the quoted provider.
The Quote commitment transitively binds the Capability ID, immutable version,
manifest, endpoint, actor, terms, attestor, provider, and expiry.
Bulk output, reports, source, and artifacts remain content-addressed off-chain.

The contract does not decode the Receipt. It does not check `exit_code`,
`completed_at`, the charge, or any digest; any attested response before
`response_deadline` releases the price. These conditions are enforced by
attestor custody (D9): the attestor signer must refuse to sign SRP2 for a
Receipt that is not releasable under the manifest, including a non-zero exit
code, a charge other than the price, a binding that differs from the request,
or `completed_at` after the request's `response_deadline`. The timestamp
remains signed evidence; it does not extend the response deadline or reserve a
settlement position.

That comparison does not independently prove wall-clock truth. The successor
profile makes the manifest-pinned attestor the explicit time attestor and
requires its custody policy to sign only an immutable completion record bound to
the same Gate claim, runner journal, and conservative clock interval. An
arbitrary or backdated timestamp, or a signer detached from those records, is
not releasable under that profile.

## Response statement and message

The attestor signs the Service Actor response statement SRP2
([`SERVICE_ACTOR_TVM_V1.md`](SERVICE_ACTOR_TVM_V1.md) section 6), which binds
`GLOBALID`, the actor address, the request ID, `request_hash`,
`response_hash = cell_hash(receipt)`, the caller, `terms_hash`, the price and
both deadlines. Pure ML-DSA-44 signs the 32 raw bytes of the SRP2 hash under the
context `TOS-SERVICE-ACTOR-RESPOND-V1`. A signature for one network, actor,
request, caller, policy, price or deadline cannot authorize another.

The owner submits:

```text
respond#53564302 query_id:uint64 request_id:uint64 response_hash:uint256
  ^StoredSignatureV1
```

The contract verifies the signature against the key the request snapshotted at
`call`, before `response_deadline`, and deletes the request; a second
`respond` for the same request fails because the request is no longer pending.
ML-DSA-44 signatures may be randomized, so a response is identified by its
request and `response_hash`, never by signature bytes. `response_hash` and the
signature exist only in the finalized `respond` transaction's inbound body; a
resolver reads them from the actor's transaction history.

Provider tooling must preserve the attestor custody boundary. It first emits the
32-byte SRP2 hash as the signing payload together with the Receipt and request
snapshot it covers, accepts only a signature response that repeats the exact
payload and the manifest-pinned key id, verifies ML-DSA-44 locally under the
context above, and only then constructs `respond`. The custody service checks
the Receipt against the manifest before signing. Receipt tooling must never
accept a mnemonic, private seed, or test-identity fixture as an operational
signing input.

No refund message names the Receipt. If no attested `respond` lands before
`response_deadline`, the request is refunded to the caller through `expire` and
`claim_refund` or a sweep (`SERVICE_ACTOR_TVM_V1.md` section 7).

The Receipt contains no Evaluator identity, score, approval, fee, or challenge
authority. A market, buyer, or third party may publish a separately signed
advisory assessment, but software-work V1 must ignore it for release and refund.
A binding evaluation step requires a new Quote and settlement profile; it
cannot be smuggled into `report_digest`, `evidence`, or the attestor key.
