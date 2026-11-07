# Service Actor TVM V1

**Status:** normative layout of the Service Actor contract **after** the
changes decided on 2026-11-07 (`SERVICE_ACTOR_SETTLEMENT_DESIGN.md` section 8:
D1 ML-DSA-44 attestor, D3 sweep returns the price to the caller, D10 request
snapshot message). The contract on tos main does not implement these changes
yet.

**Pending, not invented here:** the changed contract source, its released
code BOC, code hash and release manifest, and every test vector (`terms_hash`,
SRP2 domain hash, request snapshot, key id, signatures). Until the contract
change lands with a release manifest and vectors generated from it, no code
identity is conforming and this document carries no hash. Clients must refuse
an actor whose code hash they cannot pin to a published release
(`SERVICE_ACTOR_SETTLEMENT_DESIGN.md` section 2.4 step 3).

**Sources.** `SA:N` is line `N` of `crypto/smartcont/service-actor-code.fc` on
tos main `c17d3fca5`, the current Ed25519 contract this document changes. Every
layout or rule not marked **changed** is the one at the cited lines. Design
references (`design §N`) are to `SERVICE_ACTOR_SETTLEMENT_DESIGN.md`.

## 1. Role

A Service Actor sells per-call access in native TOS. One actor serves one
(Capability, version) at a time (design §2.3). Its authority boundary:

- `call` admits a request, pays nothing out, and commits the caller to the
  quoted `terms_hash` (SA:557, SA:569);
- `respond` releases a request's price and storage fee to owner revenue only
  when the owner sends it **and** the request's snapshotted attestor signed the
  SRP2 statement (section 6);
- an unanswered request returns its price to the caller, through
  `claim_refund` within the claim window or through `sweep_expired_request`
  after it (D3);
- the contract never decodes a Receipt; release conditions beyond the signed
  `response_hash` are attestor custody policy (D9, design §4).

The actor and every key it holds live in workchain 0 only; the contract
refuses to run elsewhere (design §6.2).

## 2. Constants

Unchanged from SA:120-181:

| Name | Value |
|---|---|
| `MAX_COINS` (exclusive) | `2^120` |
| `MINIMUM_CLEANUP_BOUNTY` / `MAXIMUM_CLEANUP_BOUNTY` | 0.1 TOS / 1 TOS |
| `MINIMUM_STORAGE_FEE` | 0.1 TOS; `storage_fee >= MINIMUM_STORAGE_FEE + cleanup_bounty` |
| `MINIMUM_OPERATING_RESERVE` | 1 TOS |
| `ADMISSION_GAS_ALLOWANCE` / `PAYOUT_GAS_ALLOWANCE` | 0.2 TOS each, unused value returned |
| `response_sla`, `refund_claim_window` | 3,600 to 2,592,000 seconds each |
| `MAX_LIVE_GLOBAL` / `MAX_LIVE_PER_CALLER` | 100,000 / 1,000 |

The 0.2 TOS allowances must be re-measured on the changed contract (design §9);
a change of value is a contract change with its own release.

## 3. Post-quantum key material

Encodings are identical to the Native Registry's canonical chains
(`NATIVE_REGISTRY_TVM_V1.md`, "Policy and signature cells", as amended for
ML-DSA-44 by tosnetwork/tos-service-spec#61):

```text
stored_key       = len:uint32(=1312) ^chain = StoredKeyV1;
stored_signature = len:uint32(=2420) ^chain = StoredSignatureV1;
```

- `chain` is canonical: byte-aligned ordinary cells, each full cell holding
  exactly 127 bytes and exactly one continuation reference, and a final cell
  holding 1 to 127 bytes and no reference; the total equals `len`. Library and
  other exotic cells are refused at the wrapper and at every chain cell.
- Key id: `SHA-256("TOS-PQ-CONSENSUS-KEY-v1" || 0x01 0x00 || public_key)` over
  the 1,312 raw key bytes, as `NATIVE_IDENTIFIERS_V1.md` "Controller key ID"
  defines it. Text form: `mldsa44:<64 lowercase hex key id>`.
- Signatures are Pure ML-DSA-44 (FIPS 204, no pre-hash, no external mu) checked
  with `PQCHECKSIG_MLDSA44` (TVM global version 16).
- Context string for every Service Actor attestor signature:
  `TOS-SERVICE-ACTOR-RESPOND-V1` (28 ASCII bytes). It differs from the registry
  context `TOS-NATIVE-REGISTRY`, so a signature made for one role cannot be
  read as the other even under one key.
- ML-DSA-44 signing may be randomized. A response is identified by its request
  and `response_hash`, never by signature bytes; vectors freeze signatures as
  data.

There is no Ed25519 attestor. The owner and caller wallets are ordinary wallets
and are outside this suite (design §6.2).

## 4. Persistent data

### 4.1 Root, policy and accounting

Root, accounting and dictionaries are unchanged (SA:13-27, SA:294-390):

```text
service_actor_data$_ owner:MsgAddress active:uint1 next_request_id:uint64
  pending_count:uint32 live_count:uint32
  ^policy ^accounting ^dicts = ServiceActorDataV1;

policy$_ policy_version:uint32 price_per_call:Coins storage_fee:Coins
  cleanup_bounty:Coins response_sla:uint32 refund_claim_window:uint32
  open_access:uint1 has_authorized_caller:uint1 authorized_caller:MsgAddress
  rate_limit_per_day:uint32 ^policy_commitments = ServiceActorPolicyV1;

accounting$_ withdrawable_revenue:Coins locked_storage_fees:Coins
  pending_liability:Coins refundable_liability:Coins call_day:uint32
  calls_today:uint32 = ServiceActorAccountingV1;

dicts$_ pending_requests:(HashmapE 64 ^PendingRequest)
  refunds:(HashmapE 64 ^Refund) caller_live_counts:(HashmapE 256 uint32)
  = ServiceActorDictsV1;
```

**Changed** (D1): the policy commitments cell.

```text
policy_commitments$_ metadata_hash:uint256 proof_scheme_hash:uint256
  attestor_key_id:uint256 attestor_key:(Maybe ^StoredKeyV1)
  = ServiceActorPolicyCommitmentsV1;
```

`has_attestor` is the `Maybe` bit: there is no separate flag, so a flag set
without a key, or a key without the flag, is not representable. With no
attestor, `attestor_key_id = 0`. With an attestor, `attestor_key_id` is the key
id of the referenced stored key. The contract establishes that equality when it
admits a key (`rotate_attestor_key`, section 7.8); it does not re-derive it.

A deploy StateInit is caller-supplied and is not admitted by the contract
(SA:510-517 apply the same reasoning to policy bounds). A conforming provider
deploys with no attestor and installs one with `rotate_attestor_key`.
Admission-time verification recomputes the key id from the stored key in the
current policy and refuses a mismatch or a non-canonical chain (design §2.4
step 5); otherwise every `respond` under that key fails and the requests can
only be refunded.

### 4.2 Pending request

**Changed** (D1): the commitments cell snapshots the attestor by reference.

```text
pending_request$_ caller:MsgAddressInt price:Coins storage_fee:Coins
  cleanup_bounty:Coins response_deadline:uint64 refund_claim_deadline:uint64
  policy_version:uint32 ^pending_commitments = PendingRequestV1;

pending_commitments$_ request_hash:uint256 terms_hash:uint256
  attestor_key_id:uint256 attestor_key:(Maybe ^StoredKeyV1)
  = PendingCommitmentsV1;
```

At `call` the contract copies `attestor_key_id` and the **same** stored-key
cell reference from the current policy. Cells are deduplicated by hash, so
storage grows per distinct live key, not per request, and an old key stays
stored only while a request snapshotted under it is live (design §6.2).
`respond` uses only the snapshot (SA:606, SA:618-620).

### 4.3 Refund

Unchanged (SA:46-48, SA:436-456):

```text
refund$_ caller:MsgAddressInt price:Coins storage_fee:Coins
  cleanup_bounty:Coins refund_claim_deadline:uint64 = RefundV1;
```

## 5. `terms_hash`

Layout unchanged (SA:241-264); the attestor field carries the key id (D1):

```text
terms_hash = cell_hash(terms)
terms$_ policy_version:uint32 price_per_call:Coins storage_fee:Coins
  cleanup_bounty:Coins response_sla:uint32 refund_claim_window:uint32
  ^terms_tail = ServiceActorTermsV1;
terms_tail$_ metadata_hash:uint256 proof_scheme_hash:uint256
  has_attestor:uint1 attestor_key_id:uint256 = ServiceActorTermsTailV1;
```

`has_attestor` is the policy's `Maybe` bit; `attestor_key_id` is zero when it
is clear. Admission gates (`open_access`, `authorized_caller`,
`rate_limit_per_day`) are excluded (SA:229-235). For the software-work profile
`metadata_hash` and `proof_scheme_hash` are fixed by design §2.3 (`NSM1` and
`SHA-256("tos.service.service-actor.receipt.software-work-v1")`).

## 6. Response statement (SRP2)

Unchanged preimage (SA:134-135, SA:274-290; `signing-domain.fc` SD:14-21):

```text
srp2$_ tag:uint32=0x53525032 global_id:int32 actor_wc:int8 actor_addr:uint256
  request_id:uint64 request_hash:uint256 response_hash:uint256
  ^srp2_tail = ServiceResponseStatementV2;
srp2_tail$_ caller:MsgAddressInt terms_hash:uint256 price:Coins
  response_deadline:uint64 refund_claim_deadline:uint64 = ServiceResponseTailV2;
response_domain_hash = cell_hash(srp2)
```

`global_id` is ConfigParam 19 (`GLOBALID`); the actor address is the
contract's own address. **Changed** (D1): the attestor signs the 32 raw bytes of
`response_domain_hash` with ML-DSA-44 under the context of section 3, and the
contract verifies with `PQCHECKSIG_MLDSA44` against the request's snapshotted
stored key. For the software-work profile `response_hash` is
`cell_hash(SoftwareWorkReceiptV1)` (`SOFTWARE_WORK_RECEIPT_TVM_V1.md`).

## 7. Inbound messages

Every body starts with `op:uint32 query_id:uint64`. Bounced messages and empty
bodies are ignored (SA:490, SA:495). Unknown ops fail with 1910. Every message
is refused if its body has trailing bits or references.

### 7.1 `call`

Unchanged body (SA:51, SA:508-597):

```text
call#53564301 query_id:uint64 request_hash:uint256 expected_terms_hash:uint256
```

Checks, in order: active (1901), policy bounds (1903-1906), admission (1923),
payment `price`, then `storage_fee` (1902), execution allowance (1929),
capacity (1907, 1908), id overflow (1909), daily rate limit (1924), terms match
(1926), backing of existing obligations plus reserve (1928).

Effect: stores the pending request (section 4.2), increments counters and
liabilities, reserves all preexisting backing plus `price + storage_fee`,
**emits the request snapshot message (section 8.1, changed by D10)**, and
returns the unused value to the caller with mode 128.

`request_hash` is stored opaquely; conforming clients refuse a zero value and
never reuse one (design §3.1, §3.2).

### 7.2 `respond`

**Changed** (D1) signature encoding:

```text
respond#53564302 query_id:uint64 request_id:uint64 response_hash:uint256
  signature:(attestor snapshotted ? ^StoredSignatureV1 : nothing)
```

Checks: sender is the owner (1900); request pending (1913);
`now < response_deadline` (1912); when the request snapshotted an attestor,
exactly one reference holding a canonical stored signature that verifies over
SRP2 (section 6) against the snapshotted key, otherwise 1911. With no
snapshotted attestor the body has no reference. A malformed signature wrapper
or chain is refused before any state changes; whether it surfaces as 1911 or as
the instruction's own exit is fixed by the contract change and its sandbox
tests. The weak-key check of the Ed25519 contract (SA:618, exit 1925) does not
exist for ML-DSA-44 keys.

Effect, unchanged (SA:624-634): deletes the request; credits
`price + storage_fee` to `withdrawable_revenue`; releases the storage-fee lock
and the pending liability. No message is sent.

### 7.3 `expire`

Unchanged (SA:55, SA:638-665): permissionless,
`response_deadline <= now < refund_claim_deadline` (1914, 1915); moves the
request to the refund set; capacity is not released.

### 7.4 `claim_refund`

Unchanged (SA:56-57, SA:667-703):

```text
claim_refund#53564304 query_id:uint64 request_id:uint64 destination:MsgAddressInt
```

Only the original caller (1918), before `refund_claim_deadline` (1916), with the
refund present (1917), backing for this price and every other obligation
(1921), and at least `PAYOUT_GAS_ALLOWANCE` attached (1929). Pays `price` to
`destination` and the change to the sender; credits `storage_fee` to owner
revenue (D4: the storage fee is non-refundable).

### 7.5 `sweep_expired_request`

Body unchanged (SA:58). **Changed** (D3) payout:

- permissionless; the request is pending or refundable (1920) and
  `now >= refund_claim_deadline` (1919);
- backing after paying `cleanup_bounty` **and** `price` must cover every other
  entry's price and storage lock plus `MINIMUM_OPERATING_RESERVE` (1921);
  at least `PAYOUT_GAS_ALLOWANCE` attached (1929);
- deletes the entry and releases its liability, storage lock and capacity;
- pays `price` to the request's **caller** (not a chosen destination);
- pays `cleanup_bounty` to the sweeper and returns the change to the sweeper;
- credits only `storage_fee - cleanup_bounty` to owner revenue.

Every swept entry is unanswered (a responded request no longer exists), so a
sweep always returns the price to the caller. The reserve is
`backing - price - cleanup_bounty`; both payouts are sent with mode 1 and no
ignore-errors flag, so either all sends and the state commit or the
transaction rolls back (SA:216-227). A failed delivery to the caller after the
action phase is not restored (SA:743-747).

### 7.6 `update_policy`

Unchanged (SA:59-63, SA:793-835). It cannot change the attestor; it bumps
`policy_version`.

### 7.7 `revoke_attestor`

```text
revoke_attestor#53564308 query_id:uint64
```

Owner only (1900). **Changed** (D1): clears the attestor entirely
(`attestor_key_id = 0`, no key reference). Pending requests keep their
snapshot (SA:851-861). `terms_hash` changes, so outstanding quotes fail with
1926.

### 7.8 `rotate_attestor_key`

**Changed** (D1):

```text
rotate_attestor_key#53564307 query_id:uint64 new_attestor_key_id:uint256
  ^StoredKeyV1 ^StoredSignatureV1
```

Owner only (1900). The key is admitted once, mirroring the registry's
admission rule (`NATIVE_REGISTRY_PQ_DESIGN.md` §4.2(2)):

1. the stored-key wrapper is an ordinary cell, `len = 1312`, exactly one
   reference, no trailing data (1925);
2. a possession signature by the new key verifies, under the section 3
   context, over the 32 raw bytes of
   `cell_hash("SRK1":uint32 global_id:int32 actor_wc:int8 actor_addr:uint256 new_attestor_key_id:uint256)`,
   built with the same signing-domain prefix as SRP2 (1911);
3. the key id derived from the verified chain equals `new_attestor_key_id`
   (1925).

Then the policy holds that id and key. Pending requests keep their snapshot.
`terms_hash` changes, so outstanding quotes fail with 1926; `policy_version` is
not bumped (SA:837-849). Under D5 a conforming buyer accepts a new key only
after a new Capability version names it in manifest key 21.

### 7.9 `withdraw_revenue`

Unchanged (SA:66, SA:863-894): owner only; pays at most the revenue not needed
to back live entries and the reserve, always to the owner address.

## 8. Outbound messages

### 8.1 Request snapshot (new, D10)

A successful `call` emits exactly one external out-message:
`ext_out_msg_info` with `dest = addr_none`, no `init`, and the body by
reference:

```text
request_snapshot$_ magic:uint32=0x53415331 schema:uint16=1
  request_id:uint64 caller:MsgAddressInt price:Coins storage_fee:Coins
  cleanup_bounty:Coins response_deadline:uint64 refund_claim_deadline:uint64
  policy_version:uint32 ^request_snapshot_terms
  = ServiceActorRequestSnapshotV1;                 -- at most 911 bits

request_snapshot_terms$_ request_hash:uint256 terms_hash:uint256
  response_sla:uint32 refund_claim_window:uint32
  has_attestor:uint1 attestor_key_id:uint256
  = ServiceActorRequestSnapshotTermsV1;            -- 833 bits
```

`magic` is ASCII `SAS1`. Every value equals the stored pending request and the
policy at admission; `has_attestor` and `attestor_key_id` equal the snapshot's
`Maybe` bit and id. The stored key itself is not emitted. The message is sent
after the reserve and before the mode-128 change transfer, and its forward fee
is paid from the caller's execution allowance, never from retained backing.

Resolvers read the snapshot only from the finalized `call` transaction and
verify an existing request against it (design §2.4 steps 6-9). It carries the
policy fields that `terms_hash` covers, so `terms_hash` can be recomputed with
the prescribed `metadata_hash`, `proof_scheme_hash` and attestor without
reading account state.

### 8.2 Value transfers

Unchanged (SA:183-227): `send_value` builds a non-bounceable internal message
(`0x10` flags) with an empty body. Payouts use mode 1; change uses mode 128 after
a `raw_reserve` of the backing that must stay.

## 9. Exit codes

From SA:81-114; meanings changed by this document are marked.

| Code | Name | Raised by |
|---:|---|---|
| 1900 | `not_owner` | `respond`, `update_policy`, `rotate_attestor_key`, `revoke_attestor`, `withdraw_revenue` |
| 1901 | `inactive` | `call` |
| 1902 | `insufficient_payment` | `call` |
| 1903 | `invalid_response_sla` | `call`, `update_policy` |
| 1904 | `invalid_refund_claim_window` | `call`, `update_policy` |
| 1905 | `invalid_cleanup_bounty` | `call`, `update_policy` |
| 1906 | `insufficient_storage_fee` | `call`, `update_policy` |
| 1907 | `capacity_exceeded_global` | `call` |
| 1908 | `capacity_exceeded_caller` | `call` |
| 1909 | `request_id_overflow` | `call` |
| 1910 | `unknown_op` | any |
| 1911 | `bad_response_signature` | `respond`; **also** a failed possession signature in `rotate_attestor_key` |
| 1912 | `response_window_closed` | `respond` |
| 1913 | `request_not_pending` | `respond`, `expire` |
| 1914 | `expire_too_early` | `expire` |
| 1915 | `expire_too_late` | `expire` |
| 1916 | `refund_claim_expired` | `claim_refund` |
| 1917 | `refund_not_found` | `claim_refund` |
| 1918 | `not_refund_caller` | `claim_refund` |
| 1919 | `sweep_too_early` | `sweep_expired_request` |
| 1920 | `request_not_live` | `sweep_expired_request` |
| 1921 | `insufficient_balance` | `claim_refund`, `sweep_expired_request` (now also covering the caller's price) |
| 1922 | `insufficient_revenue` | `withdraw_revenue` |
| 1923 | `not_authorized` | `call` |
| 1924 | `rate_limited` | `call` |
| 1925 | **changed:** `bad_attestor_key` (was `weak_attestor`) | `rotate_attestor_key`: malformed stored-key wrapper or key-id mismatch |
| 1926 | `terms_mismatch` | `call` |
| 1927 | `amount_range` | any coin arithmetic on supplied state |
| 1928 | `operating_reserve_unfunded` | `call` |
| 1929 | `insufficient_execution_payment` | `call`, `claim_refund`, `sweep_expired_request`, `withdraw_revenue` |

## 10. Getters

Convenience only; resolvers decode the account data exactly (design §2.4
step 3). **Changed** (D1): `get_service_data` (SA:901-915) and `get_request`
(SA:917-929) return `attestor_key_id` where they returned `attestor_pubkey`,
and `has_attestor` is derived from the key reference. `get_refund`,
`get_pending_count`, `get_live_count` and `get_caller_live_count` are unchanged.

## 11. Invariants

1. Coins arithmetic is checked below `2^120`; liabilities never go negative
   (SA:116-132).
2. Balance covers `pending_liability + refundable_liability +
   locked_storage_fees + MINIMUM_OPERATING_RESERVE` after every admission,
   sweep and withdrawal; a refund may consume the reserve but no other
   customer's backing (SA:203-214, SA:683-687).
3. A request resolves exactly once: respond (price to owner revenue), refund
   (price to the caller's destination) or sweep (price to the caller). The
   storage fee is never refunded; on sweep its bounty part goes to the sweeper.
4. A request's attestor, terms and deadlines are fixed at `call`; no owner
   action changes them.
5. With an attestor snapshotted, no `respond` succeeds without both the owner
   sender and a valid ML-DSA-44 signature by the snapshotted key over SRP2.
6. Every successful `call` emits exactly one request snapshot message that
   equals the stored request.

## 12. Gates before this layout is frozen

Listed in design §9: sandbox on both VMs, the adversarial cases, gas and size
(including the `respond` and `rotate_attestor_key` owner-wallet external
messages within 65,535 bytes), vectors generated from contract execution, the
resolver, live-chain lifecycles and an independent security review. None is
met for the changed contract as of 2026-11-07.
