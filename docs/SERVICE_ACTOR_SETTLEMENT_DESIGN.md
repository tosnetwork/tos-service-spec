# Service Actor Settlement Binding (design)

**Status:** decided 2026-11-07 (owner: D1-D10 as recommended). The decisions of
section 8 are taken; the normative contract surface they produce is
[`SERVICE_ACTOR_TVM_V1.md`](SERVICE_ACTOR_TVM_V1.md), and the in-place
specification edits are in the documents section 10 lists. The contract change
is implemented on tos branch `feat/service-actor-pq` at `1a469f6e2` (not merged,
not deployed). The gates in section 9 are still open: no code identity or
vector exists yet for the changed contract.

**Owner decision it implements (2026-11-06):** the current-domain
`tos_service_v1` end-to-end acceptance settles on the Service Actor contract
(native TOS, attestor-signed `respond`, timeout refund). Stablecoin escrow v2 is
not the rail; it was removed from tos main and is guarded against by
`scripts/check-no-legacy-escrow.py`. Existing objects (Capability, manifest,
Quote Proposal, Accepted Quote, Receipt, discovery) are reused; this document
binds them to the Service Actor and lists the gaps. It introduces no new
catalog, SDK, custody or authority path.

**Sources pinned.** `SA:N` is line `N` of `crypto/smartcont/service-actor-code.fc`
on tos main `c17d3fca5`, the contract before the change; `SAP:N` is line `N` of
the same file at `1a469f6e2`, the changed contract. Where the two differ,
`SAP` and `SERVICE_ACTOR_TVM_V1.md` govern. `SD:N` is
`crypto/smartcont/signing-domain.fc`. `RS:N`
is `tosctl/src/node-control/contracts/src/service_actor.rs`. `CMD:N` is
`tosctl/src/node-control/commands/src/commands/nodectl/service_actor_cmd.rs`.
`SBX` is `tosctl/src/node-control/contracts/tests/service_actor_sandbox.rs`.
Spec references are to `tos-service-spec` main `80739a8`.

## 1. What the contract enforces

| Operation | Who | Effect | Source |
|---|---|---|---|
| `call` | caller allowed by `open_access` or `authorized_caller` | admits one request, assigns `request_id = next_request_id`, snapshots policy and attestor key | SA:508-597 |
| `respond` | owner sender **and**, if the request snapshotted an attestor, a valid attestor signature | deletes the request; credits `price + storage_fee` to owner revenue | SA:599-636 |
| `expire` | anyone, in `[response_deadline, refund_claim_deadline)` | moves the request to the refund set | SA:638-665 |
| `claim_refund` | the original caller only, before `refund_claim_deadline` | pays `price` to a caller-chosen destination | SA:667-703 |
| `sweep_expired_request` | anyone, at or after `refund_claim_deadline` | deletes a pending or refundable entry; pays the price to the caller and the cleanup bounty to the sweeper; credits `storage_fee - cleanup_bounty` to owner revenue (D3) | SAP:792-889 |
| `update_policy` | owner | replaces price, fees, SLA, window, access, rate limit, `metadata_hash`, `proof_scheme_hash`; `policy_version + 1` | SA:793-835 |
| `rotate_attestor_key` / `revoke_attestor` | owner | sets or clears the current attestor; pending requests unaffected | SAP:935-963 |
| `withdraw_revenue` | owner | pays at most the revenue not needed to back live entries and the 1 TOS reserve, always to the owner address | SA:863-894 |

Bounced messages are ignored (SA:490). All coin arithmetic is checked
(SA:122-132). Payment is native TOS: `msg_value` must cover `price_per_call`,
then `storage_fee`, then a 0.2 TOS execution allowance whose unused part is
returned (SA:533-538, SA:165, SA:586-588).

## 2. Binding a Capability version to a Service Actor

### 2.1 Identities

| Identity | Authority | Source |
|---|---|---|
| Agent ID, controller policy | Native Registry Agent state | `NATIVE_REGISTRY_STATE_MACHINES.md` §2 |
| Capability ID, owner Agent ID, version string, manifest digest, revocation bit | Native Registry Capability state | same, §4 |
| actor address `A = wc:cell_hash(StateInit)` | deterministic from the deploy StateInit | RS:228-236 |
| actor code hash | account state | — |
| owner address `O` (a wallet) | actor data, fixed for life | SA:14, SA:296; no owner-change op exists (SA:71-79) |
| attestor key `K` (ML-DSA-44 stored key and its key id) | actor data; snapshotted per request | SAP:20-21, SAP:653-656 |
| `metadata_hash`, `proof_scheme_hash` | actor policy; owner-set | SA:20, SA:806-807 |

### 2.2 Who may deploy and own an actor

Anyone may deploy an actor with any owner, any `metadata_hash` and any attestor:
the StateInit is caller-supplied and only re-checked at `call` for policy bounds
and for a consistent attestor encoding (SAP:582-608). An actor's own claim to serve a Capability is therefore
unauthenticated. The owner wallet is not an Agent controller and the Agent policy
has no authority over the actor.

The authorizing link must come from the Capability side: the manifest is
published under the owner Agent's live Capability-control policy, so a manifest
that names the actor is the owner Agent's statement that this actor settles this
version. The actor's `metadata_hash` is the reverse link, a consistency check
that the actor is currently configured for exactly that version.

### 2.3 Binding objects (proposed)

Forward link, in the manifest (decision D5/D6): a new map key `21 settlement`:

```text
settlement = { 1: rail = "tos.service.service-actor.v1",
               2: actor workchain (0), 3: actor account id (32 bytes),
               4: actor code hash (32 bytes), 5: attestor key text form }
```

Key 18 `execution_signer_authorization` becomes the digest of the attestor key
text form (`mldsa44:<key id>` under D1, section 6). Key 20 `supported_assets`
must be able to express native TOS (gap, D6).

Reverse link, in the actor:

```text
metadata_hash = cell_hash(service_actor_metadata)
service_actor_metadata$_ magic:uint32="NSM1" schema:uint16=1
  capability_id:uint256 provider_agent_id:uint256
  ^network_domain ^service_actor_version = ServiceActorMetadataV1;   -- 560 bits
service_actor_version$_ capability_version_sha256:uint256
  manifest_digest:uint256 = ServiceActorVersionV1;                  -- 512 bits
proof_scheme_hash = SHA-256("tos.service.service-actor.receipt.software-work-v1")
```

`network_domain` is the existing `NetworkDomainV1` cell of
`ACCEPTED_QUOTE_TVM_V1.md` (768 bits). The four 256-bit identities and the
48-bit header (1,072 bits) do not fit one 1,023-bit cell, so the version pair
moves into a referenced cell. Because `terms_hash` includes `metadata_hash` and
`proof_scheme_hash` (SA:250-251), every admitted request commits to the exact
network, Capability version, manifest and Receipt scheme.

**Ordering, no circularity.** The address depends only on the initial StateInit
(RS:228-236). The provider (1) deploys the actor with `metadata_hash = 0`,
(2) registers or adds the Capability version whose manifest names `A`, then
(3) sends `update_policy` with the real `metadata_hash`. Serving a new version
repeats (2) and (3) against the same `A`. One actor serves one (Capability,
version) at a time; requests admitted under the previous `metadata_hash` keep
their snapshotted `terms_hash` (SA:571-574). `RS:218` deploys with `active = 1`,
so a deploy-then-configure window exists; no buyer's quoted `terms_hash` can
match it, but an inactive deploy option is a tooling gap (section 7).

### 2.4 Verification from finalized state alone

Every read below is taken at one quorum-finalized checkpoint (atomic-read rule
in `CLAUDE.md`). Nothing is supplied by a gateway. There are two procedures:
admission-time verification checks the actor's **current** policy before a
`call`; existing-request verification checks a request against **its own
snapshot**, because a later rotation or `update_policy` changes the current
policy but not admitted requests (SA:571-574, SA:604-620).

**Common: identity and actor equality.** `terms_hash` hashes neither the actor
address nor its owner (SA:241-264): an identical policy deployed at another
address yields the same `terms_hash`, and a matching `call` there would be
admitted. The verifier therefore requires, and otherwise refuses:

1. the Capability is not tombstoned, the version is present and not revoked
   (admission only; see below), the owner Agent is not tombstoned; the manifest
   bytes match the version's `manifest_digest`;
2. one actor address everywhere: manifest key 21 actor `=` the Quote's
   `rail.actor` `=` the destination of the `call` (before sending: the message
   the buyer builds; afterwards: the finalized `call` transaction's account).
   The owner is fixed per address (SA:71-79), so address equality also fixes the
   owner;
3. one code hash everywhere: the account's code hash `=` manifest key 21 code
   hash `=` the Quote's `rail.actor_code_hash` `=` the pinned Service Actor
   release hash (no release manifest publishes one today; gap, section 7); the
   account is on workchain 0 and its data cell decodes exactly as
   `SERVICE_ACTOR_TVM_V1.md` section 4 (SAP:13-27, SAP:319-364), not only through the getter;
4. one attestor key everywhere: manifest key 21 (and key 18) `=` the Quote's
   `authority.attestor_key_id`.

A mismatch in 2-4 is a verification error, never an empty or partial result.
The buyer must not build or sign the `call`, and a resolver must not attribute
the request to the Capability.

**Admission-time verification (before `call`).** Additionally:

5. current state: `active = 1`, `has_attestor = 1`, and the current
   `attestor_key_id` equals step 4. `call` refuses with 1925 a policy whose
   stored key is absent or derives a different id (SAP:599-608), so the decoded
   id names the stored key; a verifier may also recompute it from the key
   (`get_attestor_key` or the decoded data);
6. current `metadata_hash` equals `NSM1` recomputed from step 1 and the network;
   `proof_scheme_hash` equals the section 2.3 value;
7. policy bounds (SA:518-526) and admission: `open_access = 1` or
   `authorized_caller` equals the buyer wallet (SA:529-530);
8. `terms_hash` computed from the decoded current policy (SAP:266-289) equals the
   Quote's `rail.terms_hash`, and the Quote's `policy_version`, `price` and
   `storage_fee` equal the decoded ones.

Capacity and the daily rate limit (SA:539-554) can still refuse the call; they
are not part of the terms.

**Existing-request verification (after `call`).** Steps 1-4, except that a
version revoked after the `call` does not invalidate the request (revocation
does not touch the actor). Then, instead of steps 5-8:

5. locate the finalized `call` transaction (section 3.2); its caller is the
   buyer and its inbound body carries the buyer's `request_hash` and the
   Quote's `terms_hash`;
6. read the request snapshot from that transaction alone (D10): the
   successful `call` emits exactly one external out-message whose body is the
   `ServiceActorRequestSnapshotV1` cell of `SERVICE_ACTOR_TVM_V1.md` section
   8.1 (tag `SAR1`). It is decoded exactly (tag, bit lengths, references,
   exhaustion, attestor encoding, deadline order); zero or more than one such
   message, or a trailing field, is a verification error. Its `request_id` is
   the request's identity. Its caller equals the `call` sender and the buyer,
   its `request_hash` equals the inbound body, and its price equals the
   Quote. No account state is read, so the result is the same in **every**
   request state and does not depend on block packing: a `call` and a
   `respond` in one block, which leave no queryable state holding the entry,
   verify like any other pair;
7. the snapshot has `has_attestor = 1` and its attestor key id equals the step
   4 key, the one the manifest and the Quote name and admission verified. This
   is the check that matters after an owner action: a rotation from K1 to K2
   without a new manifest gives later requests the snapshot K2, and a
   `revoke_attestor` clears the attestor, so later requests snapshot
   `has_attestor = 0` and `respond` then needs no signature at all
   (SAP:694-708). Both are refused here, whatever the request state;
8. the snapshot's `terms_hash` equals the inbound `expected_terms_hash` and the
   Quote's `rail.terms_hash`. `terms_hash` is not recomputed from the snapshot,
   which does not carry the policy fields it covers: the request's commitment
   to the quoted `policy_version`, `storage_fee`, `metadata_hash`,
   `proof_scheme_hash` and attestor is the Quote's `terms_hash`, which
   admission-time verification (steps 5-8 above) checked against the decoded
   policy before the `call` (gap, section 7). The deadlines are the
   snapshot's;
9. the outcome: pending, or from transaction history (section 5.1). A
   `respond` is the finalized successful `respond` transaction for the
   snapshot's `request_id`: the contract verified the signature against the
   snapshotted key whose id step 7 checked, over SRP2 (section 4), whose
   inputs are the snapshot, the actor address, `global_id` and the `respond`
   body's `response_hash`. A resolver that re-verifies the signature takes the
   stored key from the finalized transaction that installed it (the
   `rotate_attestor_key` body or the deploy StateInit) or, while the request
   is pending, from `get_request_attestor_key`, recomputes its key id and
   requires it to equal step 7. A refund or sweep is checked against the
   transaction and the snapshot.

The current attestor, `metadata_hash` and policy are never consulted for an
existing request; only its snapshot message and the attestor admission verified
are.

## 3. Quote Proposal, Accepted Quote and `call`

### 3.1 Commitments

The Quote Proposal (`native.proto` `QuoteProposalV1`, lines 329-340) stays
gateway-local. The client converts it into an Accepted Quote cell for this rail
(D2):

```text
accepted_quote$_ magic:uint32=0x4e415131 schema:uint16=<D2>
  ^network_domain ^identity ^rail ^authority
identity  = capability_id provider_agent_id ^(capability_version_sha256
            manifest_digest transport_binding_digest expires_at:uint64
            ^capability_version_snake)                -- unchanged from V1
rail      = actor:MsgAddressInt actor_code_hash:uint256 policy_version:uint32
            ^rail_terms                                 -- 555 bits
rail_terms = terms_hash:uint256 price:Coins storage_fee:Coins   -- <= 504 bits
authority = attestor_key_id:uint256
quote_commitment = cell_hash(accepted_quote)
```

In one cell the rail would be 267 (standard address) + 256 + 256 + 32 + 2 x 124
(Coins, 4-bit length plus up to 120 bits) = 1,059 bits. It is split rather than
given a narrower amount bound: the contract accepts any Coins value below
`2^120` (SA:120-132), and a smaller Quote bound would either refuse policies the
contract admits or need a second bound kept in step with it.

The request commitment carried by `call`:

```text
request_hash = cell_hash(service_request)
service_request$_ magic:uint32="NSR1" schema:uint16=1
  quote_commitment:uint256 execution_id:uint256 input_digest:uint256
```

The contract stores `request_hash` opaquely and does not require it to be
non-zero (SA:556, SA:571-574); conforming clients must refuse a zero value.

### 3.2 What the buyer commits to at `call`

- `expected_terms_hash`, which must equal the actor's current `terms_hash` or
  the call fails with 1926 before any state moves (SA:557, SA:563-569; test
  `a_call_quoted_under_one_policy_is_refused_under_another`, SBX:1850);
- `request_hash`, binding the Accepted Quote, execution identity and input;
- the sender address, which becomes `caller` and the only refund claimant
  (SA:572, SA:675);
- attached value at least `price + storage_fee + 0.2 TOS` (SA:533-538).

The finalized `call` transaction is the acceptance event. It stores both
deadlines computed from chain time: `response_deadline = now + response_sla`,
`refund_claim_deadline = response_deadline + refund_claim_window`
(SAP:643-644). The assigned `request_id` is emitted in the request snapshot
message of the `call` transaction (D10, SAP:670-671; section 2.4 step 6). A
buyer must
still never reuse a `request_hash`, so that one `request_hash` names one request.

`tosctl agent service send --operation call` defaults `expected_terms_hash` to
the actor's live terms (CMD:1147-1152). That default re-reads the terms the call
is meant to pin; buyer tooling must always pass the quoted value.

### 3.3 Field reconciliation

| Accepted Quote V1 / Paid Demand field | Service Actor counterpart |
|---|---|
| `network_domain` | none in `terms_hash`; SRP2 binds `GLOBALID` and the actor address (SD:14-21); the proposed `metadata_hash` binds the domain |
| `capability_id`, `provider_agent_id`, version, `manifest_digest` | `metadata_hash` (section 2.3) |
| `transport_binding_digest` | none on chain; manifest key 17 and `quote_commitment` |
| `expires_at` | **none**: `call` has no acceptance deadline; a quote is usable while the terms are unchanged (D7) |
| `escrow_terms_digest` | `terms_hash` (SA:241-264) |
| `dispute_policy_digest` | fixed by contract code: attested response pays, otherwise timeout refund |
| `asset` (wc=0 stablecoin identity) | **none**: native TOS only (D8) |
| `maximum_atomic_amount` | exact `price_per_call`; plus a non-refundable `storage_fee` (SA:698, SA:779) |
| `execution_signer_authorization` | attestor key in `terms_hash` (SA:252-253) |
| buyer wallet (escrow terms) | not quoted; bound at `call` as `caller` |
| `accept_by`, `funding_deadline` | none: acceptance and funding are one transaction |
| `execution_deadline`, `refund_available_at` | `response_deadline`, relative to the call, not absolute at quote time |
| Provider Offer digest | none |
| — | `refund_claim_deadline`: new, no Quote counterpart; after it the refund right lapses (section 5) |

Admission gates (`open_access`, `authorized_caller`, `rate_limit_per_day`) are
deliberately outside `terms_hash` and the response domain (SA:29-38,
SA:230-235).

## 4. `respond`, the SRP2 domain and the Receipt

The attestor signs `cell_hash` of (SA:274-290, SD:14-21):

```text
"SRP2":uint32 global_id:int32 actor_wc:int8 actor_addr:uint256
request_id:uint64 request_hash:uint256 response_hash:uint256
^[ caller:MsgAddressInt terms_hash:uint256 price:Coins
   response_deadline:uint64 refund_claim_deadline:uint64 ]
```

A signature for one network, actor, request, caller, policy, price or deadline
cannot authorize another (tests SBX:1065, SBX:1809). It does not bind
`query_id`, completion time or any Receipt field except through
`response_hash`.

`respond` requires the owner as sender (SA:600) and, when the request
snapshotted an attestor, the snapshotted key's signature (SA:610-621). With
`has_attestor = 0` the owner alone can take the price; this profile therefore
requires `has_attestor = 1`, which the buyer verifies through `terms_hash`.

**Binding the Receipt.** `response_hash = cell_hash(SoftwareWorkReceiptV1)` of
`SOFTWARE_WORK_RECEIPT_TVM_V1.md`, with `quote_commitment`, `execution_id` and
`input_digest` equal to the `service_request` preimage, `charged_atomic_amount =
price` (nanoTOS), and `provider_agent_id` equal to the quoted provider. The
Receipt section "Settlement intent and message" is replaced by SRP2 for this
rail.

**What the contract cannot check.** `respond` sees only `response_hash`. It does
not decode the Receipt, so `exit_code = 0`, `completed_at`, the charge, and every
digest are unchecked on chain; any attested response credits `price +
storage_fee` (SA:631-633). Escrow v2 required `exit_code == 0` and the charge on
chain. On this rail those become attestor custody policy: the attestor signer
must refuse to sign a Receipt that is not releasable under the manifest. A
buyer holding a signed non-conforming Receipt has off-chain evidence of
misbehaviour, not an on-chain remedy.

**What a signed Receipt proves.** That the bound attestor key attested the bound
digests, charge and completion for this request on this actor and network. It
does not prove computation correctness, payout delivery, wall-clock truth of
`completed_at`, usefulness, or that the work ran once.

**Resolution.** `response_hash` and the signature exist only in the finalized
`respond` transaction's inbound body; state keeps neither, and afterwards
`get_request` returns not found (SA:917-923). A resolver therefore needs the
actor's finalized transaction history, not only its state.

## 5. Refund, timeout and sweep

### 5.1 Buyer-visible states

| State | Predicate at a finalized checkpoint | Buyer action |
|---|---|---|
| refused | `call` aborted with an exit code; no entry | none (bounceable call returns value minus fees) |
| pending | `get_request(id)` found, `now < response_deadline` | wait |
| overdue | `get_request(id)` found, `response_deadline <= now < refund_claim_deadline` | `expire` (anyone) |
| refundable | `get_refund(id)` found, `now < refund_claim_deadline` | `claim_refund` with at least 0.2 TOS (SA:688) |
| lapsed | either entry found, `now >= refund_claim_deadline` | none; anyone may sweep |
| responded | terminal: finalized `respond` transaction for `id` | verify Receipt (section 4) |
| refunded | terminal: finalized `claim_refund` transaction | — |
| swept | terminal: finalized `sweep_expired_request` transaction | none; the price was paid to the caller |

`respond` (`now < response_deadline`, SA:607) and `expire`
(`response_deadline <= now`, SA:649) partition time exactly (SBX:863, SBX:885).
Terminal states are only distinguishable from the transaction history.

### 5.2 Economics a buyer must be told before `call`

- On refund the buyer receives `price` only; `storage_fee` goes to owner revenue
  even when the provider never answered (SA:698).
- A refund takes two transactions inside `refund_claim_window` (at least one
  hour, SA:175): `expire`, then `claim_refund` from the caller address.
- After `refund_claim_deadline` a sweep pays the price to the **caller** and
  the bounty to the sweeper, and credits `storage_fee - cleanup_bounty` to the
  owner (D3, SAP:870-880). A buyer offline for the whole window still gets the
  price back, from whoever sweeps; the storage fee is not refunded.
- `claim_refund` sends to any destination (SA:669); a failed delivery is not
  restored (SA:743-747, SBX:1307).

### 5.3 Failure cases

- `call` refusals leave state unchanged: inactive 1901, policy bounds
  1903-1906, capacity 1907-1908, id overflow 1909, not authorized 1923, rate
  limit 1924, terms mismatch 1926, reserve unfunded 1928, allowance 1929
  (SA:81-114).
- `call` also refuses an inconsistent attestor encoding in a deploy StateInit
  (1925, or 62/63 for a non-canonical stored key; SAP:599-608).
- `respond`: not owner 1900, not pending 1913, window closed 1912, missing
  signature reference 9, malformed stored signature 62/63, failed verification
  1911 (`SERVICE_ACTOR_TVM_V1.md` section 7.2). A key the owner installed but
  does not control makes every `respond` for requests snapshotted under it
  fail, so those requests can only be refunded.
- `claim_refund` against an under-backed actor fails with 1921 and keeps the
  claim (SA:677-687); if under-backing lasts past the deadline the claim lapses.
  Rent can erode backing once the operator reserve is exhausted (SA:156-158).
- `expire` does not release capacity (SA:655-656, SBX:1395).
- A fork that keeps the same `GLOBALID` is outside what SRP2 distinguishes
  (SD:9-10).

## 6. Attestor key suite

### 6.1 Snapshot, rotation and revocation

`call` copies `has_attestor`, the key id and the stored-key reference into the
request (SAP:653-656); `respond` uses only the copy (SAP:694-708).
`rotate_attestor_key` and `revoke_attestor` change only future calls
(SAP:935-963; SBX
`update_policy_and_attestor_rotation_never_alter_already_snapshotted_requests`,
`revoke_attestor_is_never_frozen_by_a_pending_request`). They do not bump
`policy_version`, but `terms_hash` covers the bit and the key id
(SAP:266-289), so every outstanding quote fails with 1926 afterwards.
`update_policy` cannot change the attestor (SAP:926-931).

Consequences: a lost attestor key turns pending requests into refunds; a
compromised attestor key alone cannot respond (owner sender required, SA:600);
a compromised owner wallet alone cannot respond to attested requests, but can
withdraw revenue to itself, change policy and rotate the attestor for new calls
(buyers who pin the manifest key refuse those, D5). Revocation is not an
emergency stop for pending requests; the stop is the owner not responding.

### 6.2 ML-DSA-44 options

Measured by a shape probe, not the contract (tos `test/pq-service-actor-gas`
`b39fdba8a`, `pq_service_actor_gas_sandbox.rs`, context
`TOS-SERVICE-ACTOR-RESPOND`; Rust VM equal to the C++ engine):

| | Ed25519 today | A: stored key, snapshot by reference | B: key id snapshot, key in `respond` |
|---|---|---|---|
| `respond` gas | 7,574 | 12,870 | 14,248 |
| `respond` body | 121 B | 2,545 B | 3,897 B |
| storage | inline 256-bit key | +12 cells per distinct live key; per-request unchanged | unchanged |
| key check | weak-key test | admitted once at rotation | id derived per `respond` |

Common to both: one suite, no Ed25519 attestor (as the registry PQ design §3.1);
key id and text form `mldsa44:<id>` as in that design §3.2; the
`terms_hash` attestor field carries the key id, so its layout is unchanged;
the SRP2 preimage is unchanged and ML-DSA-44 signs its 32 raw hash bytes under
the context above; signatures may be randomized, so a response is identified by
`response_hash` and the request, never by signature bytes; workchain 0 only
(a client rule: the contract does not check its workchain).

**Recommendation: A.** `respond` runs once per paid call; A saves 1,378 gas and
1,352 bytes on every one, while its storage cost is per distinct live key, and
an old key stays referenced only while requests snapshotted under it are live.
Admitting the key once at rotation mirrors registry rule §4.2(2). B is simpler
state and needs no admission code at rotation. Owner decision D1.

**As implemented** (`1a469f6e2`, `SERVICE_ACTOR_TVM_V1.md` sections 4.1, 7.8):
`rotate_attestor_key` carries only `query_id` and the stored key; the contract
validates the canonical stored key and derives the key id itself
(`pq::key_id`). There is no possession signature: a key the owner does not
control cannot produce SRP2 signatures, so a wrong key only makes `respond`
impossible and the requests admitted under it refund to their callers;
nothing can be taken. Because a deploy StateInit bypasses rotation, `call`
re-derives the key id on every admission and refuses an inconsistent
attestor encoding (1925). The shape probe's figures above are not measurements
of this contract.

The owner and buyer wallets remain Ed25519 until a post-quantum wallet is
released for `tosctl`; under a forging adversary the two-key rule still
protects pending requests, but revenue and future-call policy do not.

## 7. Gaps in the implementation repositories

Pointers for follow-up changes; no code is written here.

| Repository | File | Gap |
|---|---|---|
| tos | RS:18, RS:159-160 | the BOC is embedded and deserialized there, but no release manifest publishes its code hash for clients to pin; needed by 2.4 step 3 |
| tos | CMD:1147-1152 | `call` defaults `expected_terms_hash` to live state |
| tos | RS:218 | deploy is always `active = 1`; add an inactive deploy for 2.3 |
| tos | service-actor-code.fc | ML-DSA-44 attestor (D1), sweep to the caller (D3), request snapshot carrying `request_id` (D10) and the `call` attestor-encoding check: implemented on `feat/service-actor-pq` at `1a469f6e2`, not merged, not deployed |
| tos | SAP:476-506 | the request snapshot omits `cleanup_bounty` (and `storage_fee`, `policy_version`, the policy commitments), so a resolver that did not run admission-time verification cannot open `terms_hash` from the `call` transaction; section 2.4 step 8 relies on the Quote's `terms_hash` |
| spec | see section 10 | Accepted Quote, escrow v2, settlement, Receipt, manifest, execution gate (slot key `(quote_commitment, escrow_address)` becomes `(quote_commitment, actor, request_id)`), strategy §9, roadmap Gate D |
| spec | `native.proto` 315-349 | `MoneyV1.asset` is stablecoin-only; `QuoteProposalV1` has no actor or `terms_hash`; `AcceptedQuoteV1` |
| spec | `test-vectors/` | `NSM1`, `NSR1`, Accepted Quote, `terms_hash`, SRP2, from contract execution |
| protocol | `pkg/nativecore/quote.go`, `internal/referencecodec/quote.go` | rail cell instead of asset and escrow terms |
| protocol | `pkg/nativecore/receipt.go`, `escrow.go`, `escrow_v2.go` | settlement intent and release/refund bodies give way to an SRP2 builder and `call`/`expire`/`claim_refund` bodies |
| protocol | `pkg/toschain/escrow.go` | actor resolver: code hash, exact decode, request/refund lookup, transaction-derived outcomes |
| protocol | `pkg/executiongate/gate.go` | `PaidDemandEscrowResolver` and the funded-escrow predicate become "request pending under the quoted `terms_hash` and `request_hash`" |
| protocol | `pkg/buyersdk/buyer.go`, `tosctl_sender.go`, `journal.go` | native-TOS `call` with the quoted terms; journal `expire`/`claim_refund` duties and deadlines |
| protocol | `pkg/quoteprovider/provider.go`, `pkg/quoteexchange/package.go` | proposals from finalized actor state; `terms_hash` instead of escrow terms |
| protocol | `pkg/providersdk/provider.go` | manifest key 21; deploy, register, `update_policy` sequencing |
| protocol | `pkg/economic`, `cmd/native-receipt-release` | inputs from actor transactions (`pkg/paiddemand` stays escrow-bound, out of scope) |
| gateway | `internal/nativegateway/server.go`, `internal/quotesource` | Quote Proposal contents only; no authority |
| tos-ai | `pkg/a2aadapter/adapter.go`, `pkg/mcpadapter/adapter.go` | carry `(actor, request_id)` instead of `EscrowAddress`; settler submits `respond`; attestor signing keeps the Receipt document's two-stage custody (emit the 32-byte SRP2 hash, verify the signature before building `respond`); `pkg/softwarework` unchanged |
| openfox | `pkg/servicebridge/interfaces.go`, `buyer.go`, `provider.go`, `nativeimpl/purchase_coordinator.go`, `nativeimpl/tosctl_runner.go` | `call` instead of fund (`ResolveEscrow`, `SignAndFundEscrow`); new buyer duty to `expire` and `claim_refund` before `refund_claim_deadline` (`pkg/earning/paid_demand_*` stays escrow-bound) |

## 8. Owner decisions (taken 2026-11-07)

The owner took every decision as recommended on 2026-11-07. Each entry keeps
the options that were weighed and records the one taken.

- **D1 Attestor suite.** (A) stored ML-DSA-44 key snapshotted by reference;
  (B) key id snapshot, key carried in `respond`; (C) keep Ed25519.
  *Recommend A* (section 6.2). C contradicts the 2026-11-06 PQ priority.
  **Taken: A.**
- **D2 Accepted Quote cell.** (a) replace schema 1 in place with the rail cell
  of 3.1 and retire schema 2 with escrow v2; (b) add a new schema beside them.
  *Recommend (a)*: pre-launch, no backward compatibility, and no escrow remains
  on tos main to accept schema 1 or 2. **Taken: (a).**
- **D3 Sweep of an unanswered request.** (a) keep: price to owner revenue
  (SA:779); (b) change the contract to return the price to the caller on sweep,
  bounty still from `storage_fee`. *Recommend (b)* while the contract changes
  for D1: under (a) a provider earns from a buyer's inattention.
  **Taken: (b).**
- **D4 Storage fee on provider failure.** (a) keep it non-refundable (SA:698);
  (b) refund `storage_fee - cleanup_bounty` on `claim_refund`. *Recommend (a)*,
  disclosed in the Quote: it pays for the entry the buyer created.
  **Taken: (a).**
- **D5 Attestor key pinning.** (a) the manifest pins the key (rotation needs a
  new Capability version under Agent policy); (b) actor state only (owner
  wallet rotates alone). *Recommend (a)*: otherwise an owner-wallet
  compromise also rotates the attestation authority. **Taken: (a).**
- **D6 Manifest.** (a) edit `SOFTWARE_WORK_MANIFEST_V1.md` in place (key 21,
  key 18 meaning, native TOS in key 20, refund condition); (b) a new manifest
  version. *Recommend (a)*, same reason as D2. **Taken: (a).**
- **D7 Quote expiry.** (a) buyer-side only: refuse to call after `expires_at`;
  (b) add an acceptance deadline to `call`. *Recommend (a)*: `terms_hash` already
  makes a stale quote fail closed, and expiry protects only the buyer.
  **Taken: (a).**
- **D8 Settlement asset.** (a) native TOS for current-domain acceptance, and
  amend `PRODUCT_STRATEGY.md` §9 and `SETTLEMENT.md`; stablecoin pricing waits
  for a token integration that reports payout outcomes. (b) block acceptance on
  stablecoin support. *Recommend (a)*. **Taken: (a).**
- **D9 Release condition.** (a) attestor custody refuses non-releasable
  Receipts, off-chain; (b) carry and decode the Receipt in `respond`.
  *Recommend (a)* for this profile; (b) costs gas and body size per call and
  still proves only what the attestor signed. **Taken: (a).**
- **D10 Historical request snapshot.** Existing-request verification
  (section 2.4, steps 6-8) needs the request entry the `call` wrote, but chain
  queries return account state per block, not per transaction, and a
  transaction carries only the old and new account hashes; when `call` and
  `respond` execute in the same block, no queryable state holds the entry.
  Options: (a) the contract emits the request snapshot (request ID, caller,
  `request_hash`, `terms_hash`, price, attestor flag and key or key id) as an
  external out-message at `call`, which a resolver reads from the finalized
  `call` transaction and which also closes the missing `request_id` event of
  section 7; (b) resolvers replay the `call` transaction from the authenticated
  preceding account state and check the resulting state hash against the
  transaction; (c) restrict historical verification to pending requests and
  treat terminal outcomes as unverifiable by Capability. *Recommend (a)*: one
  bounded log message per call, independent of block packing, and the only
  option a light client can check without re-executing the contract. Raised by
  the third non-author review round. **Taken: (a)**; section 2.4 steps 6-9
  use the snapshot message.

## 9. Verification before freeze

- **Sandbox, both VMs.** Every case in `service_actor_sandbox.rs` re-run on the
  changed contract, and the gas test transactions replayed in the C++ engine
  with identical gas, exit code, actions, messages, balance, data and code
  (`scripts/replay-token-bridge-trace.py`), as for the registry.
- **Adversarial cases.** Wrong ML-DSA context; a cross-role signature (same key,
  registry or consensus context); response signed by the rotated-out key for a
  new request and by the new key for an old request; stored key whose id does
  not match; library or exotic cells for the key wrapper and chain cells;
  malformed lengths and trailing data; two randomized signatures for one
  response giving one transition; Ed25519-shaped key and signature refused;
  a deploy StateInit with an attestor key whose id differs, or with a key or
  key id but `has_attestor = 0`, admitting no request (1925); an actor outside
  workchain 0 refused by the client verifier; actor substitution (an identical policy at a
  second address, so equal `terms_hash`, refused by 2.4 step 2 before `call`
  and never attributed afterwards); a Quote whose code hash or attestor key
  differs from the manifest or account (steps 3-4); existing-request
  verification after `rotate_attestor_key`, `revoke_attestor` and
  `update_policy`, still accepting the request by its snapshot while
  admission-time verification refuses new quotes; rotation from K1 to K2
  without a manifest update, then a new request answered under K2, refused by
  2.4 step 7 while pending and after `respond`; `revoke_attestor`, then a new
  request answered with no signature, refused by step 7 in every state; a
  snapshot whose `terms_hash` differs from the Quote's, refused by step 8;
  `call` with a zero `request_hash` (client
  refusal) and with a duplicate `request_hash`; `call` after manifest
  revocation (accepted by the contract, refused by the buyer verifier); quote
  stale by `update_policy`, rotation and revocation each refused with 1926; and,
  under D3 (b), sweep pays the caller and preserves every other entry.
- **Gas and size.** `call`, `respond`, `rotate_attestor_key`, `claim_refund` and
  sweep at capacity with sparse ids and wide coins on both VMs (as SBX:3117,
  SBX:3152), within the 0.2 TOS allowances (SA:165-166); the real owner-wallet
  external message for `respond` and rotation built by
  `tosctl wallet send --build-only` within 65,535 bytes.
- **Vectors.** `NSM1`, `NSR1`, the D2 Accepted Quote cell, `terms_hash`, SRP2
  domain hash, key id, and signatures over the exact 32 raw bytes, produced
  from contract execution and reproduced by the tos Rust builders,
  `nativecore` and the independent reference codec.
- **Resolver.** Both procedures of section 2.4, kept separate: admission-time
  verification against current policy, and existing-request verification
  against the request snapshot (`has_attestor = 1`, the admitted attestor key,
  the quoted `terms_hash`, in every request state) and transaction
  history, never against the
  current attestor, `metadata_hash` or terms. Every state of 5.1 derived from
  finalized state and transactions at one checkpoint, three endpoints, quorum
  two, with no gateway input; an actor, code-hash or attestor mismatch, a
  missing account or an ambiguous outcome is an error, never empty.
- **Live chain.** On a v16 local network, one lifecycle per terminal state
  (responded, refunded, swept) from deploy through Receipt, reconstructed
  by a second resolver; then the same on the public testnet with an external
  buyer, independent provider and independent resolver (`ROADMAP.md` Gate D).
- **Review.** Independent security review of the changed contract and protocol.

| Gate | Status (2026-11-07) |
|---|---|
| Sandbox, current Ed25519 contract | Met for that contract (SBX, 3,275 lines); not for the changed one |
| Changed contract | Implemented on `feat/service-actor-pq` at `1a469f6e2` with its sandbox tests (SBX, 3,603 lines); not merged, not deployed, no gate accepted |
| ML-DSA-44 cost | Probe only (`b39fdba8a`); not yet measured on the changed contract |
| Everything else above | Open |

## 10. Contradictions found

1. `STABLECOIN_ESCROW_TVM_V2.md` calls escrow v2 "the only stablecoin escrow
   code that conforming tooling builds, deploys, resolves, or settles against";
   tos main removed it and `scripts/check-no-legacy-escrow.py` fails if it
   returns.
2. `ACCEPTED_QUOTE_TVM_V1.md` and `SETTLEMENT.md` make an escrow `accept` or
   deployment the acceptance event and a wc=0 stablecoin the only asset;
   escrow v2 says native TOS "is never counted as service payment". The Service
   Actor accepts and pays in native TOS in one `call` (SA:533-538).
3. `SOFTWARE_WORK_MANIFEST_V1.md` key 20 admits only stablecoins, and key 16
   allows only `not-started-before-deadline`; the actor refunds on no response,
   whether or not work started, and only within the claim window.
4. `SOFTWARE_WORK_RECEIPT_TVM_V1.md` requires `exit_code = 0` and
   `charged == funded == Quote amount` checked by the contract, and an
   `EscrowSettlementIntentV2` signature; the actor checks neither and verifies
   SRP2 (SA:610-621, SA:631-633).
5. `SETTLEMENT.md` and the V1 dispute policy promise a full refund after the
   timeout; the actor refunds `price` but keeps `storage_fee` (SA:698) and
   forfeits the price to the owner after the window (SA:779); D3 changes the
   sweep to pay the caller (SAP:874-876).
6. `PRODUCT_STRATEGY.md` §9 and §15 denominate services and evidence targets in
   TOS-network stablecoins; the chosen rail is native TOS.
7. `ROADMAP.md` Gate D lists stablecoin escrow, release and refund as delivered
   items; they describe a rail no longer on tos main.
8. `NATIVE_REGISTRY_STATE_MACHINES.md` §3 on main still specifies 1-20 Ed25519
   controllers and `NATIVE_REGISTRY_TVM_V1.md` pins code hash `600f2fda…`; tos
   main `c17d3fca5` is ML-DSA-44 with at most 8 (draft #61 not merged).
9. No spec document describes the Service Actor; the contract header cites an
   external design document instead (SA:6).
