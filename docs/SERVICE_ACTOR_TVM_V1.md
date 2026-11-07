# Service Actor TVM V1

**Status:** normative layout of the Service Actor contract with the changes
decided on 2026-11-07 (`SERVICE_ACTOR_SETTLEMENT_DESIGN.md` section 8: D1
ML-DSA-44 attestor, D3 sweep returns the price to the caller, D10 request
snapshot message). Implemented and merged on tos main (tosnetwork/tos#429,
`fc5e7723e`). Released by the reproducible release manifest
`crypto/smartcont/tos-service-actor-v1.release.json` (tosnetwork/tos#430).
Deployed on the public testnet (global_id 2) by the public Gate D/E run; it is
not deployed on any mainnet.

**Code identity.** The release manifest is the authority; these values are
copied from it:

```text
code hash   tvm-cell-sha256:0594f9a5743440f9c5f63913ab790c0ea6f4fd5c627d9962d63e09428e42aa0c
BOC sha256  sha256:21f1ea22576fce66ec3b218513adf037710b078ea12a8d84929eda970d62d5a8
BOC size    4,590 bytes
tos commit  fc5e7723e5dfb04890902abdd456aa41b4655a10
compiler    FunC v0.4.6 (392bc162e)
```

Clients pin this code hash and refuse an actor with any other code
(`SERVICE_ACTOR_SETTLEMENT_DESIGN.md` section 2.4 step 3). Changing the
contract requires a new release manifest and new vectors.

**Vectors.** Cross-language conformance vectors come from executing the
release code. They are tos
`tosctl/src/node-control/contracts/tests/fixtures/service_actor/conformance-vectors.json`
(sandbox test `conformance_vectors_come_from_contract_execution`), reproduced
byte for byte in tos-service-protocol
`pkg/nativecore/testdata/service-actor-conformance-vectors.json`. They cover the
deployed and after-admission data, the call body, the terms cell and
`terms_hash`, the request snapshot, the SRP2 respond domain and an attestor
signature over it.

**Sources.** `SA:N` is line `N` of `crypto/smartcont/service-actor-code.fc` at
tos `4c62edcae`. The contract sources are byte-identical at the release commit
`fc5e7723e` and on main. `PB:N` is `crypto/smartcont/pq-bytes.fc` and `SD:N` is
`crypto/smartcont/signing-domain.fc` at the same commit. `RS` is
`tosctl/src/node-control/contracts/src/service_actor.rs` and `SBX` is
`tosctl/src/node-control/contracts/tests/service_actor_sandbox.rs`. Design
references (`design §N`) are to `SERVICE_ACTOR_SETTLEMENT_DESIGN.md`.

## 1. Role

A Service Actor sells per-call access in native TOS. One actor serves one
(Capability, version) at a time (design §2.3). Its authority boundary:

- `call` admits a request, pays nothing out but the caller's change, and
  commits the caller to the quoted `terms_hash` (SA:576-678, SA:648);
- `respond` releases a request's price and storage fee to owner revenue only
  when the owner sends it **and**, if the request snapshotted an attestor, that
  attestor signed the SRP2 statement (section 6);
- an unanswered request returns its price to the caller, through
  `claim_refund` within the claim window or through `sweep_expired_request`
  after it (D3);
- the contract never decodes a Receipt; release conditions beyond the signed
  `response_hash` are attestor custody policy (D9, design §4).

This profile settles only through an actor on workchain 0: conforming clients
refuse an actor, Quote or manifest naming any other workchain
(`ACCEPTED_QUOTE_TVM_V1.md`, manifest key 21). The contract itself does not
check its workchain.

## 2. Constants

SA:133, SA:171-203:

| Name | Value |
|---|---|
| `MAX_COINS` (exclusive) | `2^120` |
| `MINIMUM_CLEANUP_BOUNTY` / `MAXIMUM_CLEANUP_BOUNTY` | 0.1 TOS / 1 TOS |
| `MINIMUM_STORAGE_FEE` | 0.1 TOS; `storage_fee >= MINIMUM_STORAGE_FEE + cleanup_bounty` |
| `MINIMUM_OPERATING_RESERVE` | 1 TOS |
| `ADMISSION_GAS_ALLOWANCE` / `PAYOUT_GAS_ALLOWANCE` | 0.2 TOS each, unused value returned |
| `response_sla`, `refund_claim_window` | 3,600 to 2,592,000 seconds each |
| `MAX_LIVE_GLOBAL` / `MAX_LIVE_PER_CALLER` | 100,000 / 1,000 |

The 0.2 TOS allowances must be confirmed by the gas gates on the changed
contract (design §9); a change of value is a contract change with its own
release.

## 3. Post-quantum key material

Encodings are the shared canonical chains of `pq-bytes.fc`, identical to the
Native Registry's (`NATIVE_REGISTRY_TVM_V1.md`, "Policy and signature cells",
as amended for ML-DSA-44 by tosnetwork/tos-service-spec#61):

```text
stored_key       = len:uint32(=1312) ^chain = StoredKeyV1;
stored_signature = len:uint32(=2420) ^chain = StoredSignatureV1;
```

- The wrapper holds exactly `len` and one reference (PB:88-97, PB:104-113).
  `chain` is canonical: byte-aligned ordinary cells, each non-final cell
  holding exactly 127 bytes and exactly one continuation reference, and a
  final cell holding 1 to 127 bytes and no reference; the total equals `len`
  (PB:63-84). Library and other exotic cells are refused at the wrapper and at
  every chain cell (PB:42-46).
- Refusals: a declared length other than 1,312 (key) or 2,420 (signature) exits
  62 (`pq::error::key_length`); an exotic cell or a non-canonical chain exits
  63 (`pq::error::malformed_key`); a wrapper without its reference or with
  trailing data fails with the TVM cell-underflow exit 9 (PB:18-20, PB:88-113).
- Key id: `SHA-256("TOS-PQ-CONSENSUS-KEY-v1" || 0x01 0x00 || public_key)` over
  the 1,312 raw key bytes (`pq::key_id`, PB:120-128), as
  `NATIVE_IDENTIFIERS_V1.md` "Controller key ID" defines it. Text form:
  `mldsa44:<64 lowercase hex key id>`. `pq::key_id` first validates the stored
  key as above.
- Signatures are Pure ML-DSA-44 (FIPS 204, no pre-hash, no external mu) checked
  with `PQCHECKSIG_MLDSA44` (TVM global version 16).
- Context string for every Service Actor attestor signature:
  `TOS-SERVICE-ACTOR-RESPOND-V1` (28 ASCII bytes; SA:702, RS
  `SERVICE_ACTOR_RESPOND_CONTEXT`). It differs from the registry context
  `TOS-NATIVE-REGISTRY`, so a signature made for one role cannot be read as
  the other even under one key.
- ML-DSA-44 signing may be randomized. A response is identified by its request
  and `response_hash`, never by signature bytes; vectors freeze signatures as
  data.

There is no Ed25519 attestor. The owner and caller wallets are ordinary wallets
and are outside this suite (design §6.2).

## 4. Persistent data

### 4.1 Root, policy and accounting

SA:13-27, SA:321-419:

```text
service_actor_data$_ owner:MsgAddress active:uint1 next_request_id:uint64
  pending_count:uint32 live_count:uint32
  ^policy ^accounting ^dicts = ServiceActorDataV1;

policy$_ policy_version:uint32 price_per_call:Coins storage_fee:Coins
  cleanup_bounty:Coins response_sla:uint32 refund_claim_window:uint32
  open_access:uint1 has_authorized_caller:uint1 authorized_caller:MsgAddress
  rate_limit_per_day:uint32 ^policy_commitments = ServiceActorPolicyV1;

policy_commitments$_ metadata_hash:uint256 proof_scheme_hash:uint256
  has_attestor:uint1 attestor_key_id:uint256
  attestor_key:(Maybe ^StoredKeyV1) = ServiceActorPolicyCommitmentsV1;

accounting$_ withdrawable_revenue:Coins locked_storage_fees:Coins
  pending_liability:Coins refundable_liability:Coins call_day:uint32
  calls_today:uint32 = ServiceActorAccountingV1;

dicts$_ pending_requests:(HashmapE 64 ^PendingRequest)
  refunds:(HashmapE 64 ^Refund) caller_live_counts:(HashmapE 256 uint32)
  = ServiceActorDictsV1;
```

"No attestor" has one encoding: `has_attestor = 0`, `attestor_key_id = 0`, no
key reference. With an attestor, `has_attestor = 1`, the key reference is
present and `attestor_key_id = pq::key_id` of it. `rotate_attestor_key` and
`revoke_attestor` only ever write these two encodings (sections 7.7, 7.8).

A deploy StateInit is deployer-controlled and passes through no admission
code, so `call` re-checks the commitments on every admission before reading
the body (SA:595-604): with `has_attestor = 1` it refuses an absent key (1925),
a key that is not a canonical stored key (62 or 63) and a key whose derived id
differs from `attestor_key_id` (1925); with `has_attestor = 0` it refuses a
present key or a non-zero `attestor_key_id` (1925). An actor deployed with an
inconsistent attestor therefore admits no request. The RS `build_data` writes
the canonical encoding for a deploy with or without an attestor.

### 4.2 Pending request

SA:40-44, SA:423-476:

```text
pending_request$_ caller:MsgAddressInt price:Coins storage_fee:Coins
  cleanup_bounty:Coins response_deadline:uint64 refund_claim_deadline:uint64
  policy_version:uint32 ^pending_commitments = PendingRequestV1;

pending_commitments$_ request_hash:uint256 terms_hash:uint256
  has_attestor:uint1 attestor_key_id:uint256
  attestor_key:(Maybe ^StoredKeyV1) = PendingCommitmentsV1;
```

At `call` the contract copies `has_attestor`, `attestor_key_id` and, only when
`has_attestor = 1`, the **same** stored-key cell reference from the current
policy (SA:650-653). Cells are deduplicated by hash, so storage grows per
distinct live key, not per request, and an old key stays stored only while a
request snapshotted under it is live (design §6.2). `respond` uses only the
snapshot (SA:685-705).

### 4.3 Refund

SA:50-52, SA:504-524:

```text
refund$_ caller:MsgAddressInt price:Coins storage_fee:Coins
  cleanup_bounty:Coins refund_claim_deadline:uint64 = RefundV1;
```

## 5. `terms_hash`

`terms_cell`, SA:263-291; RS `terms_hash_of_data` / `terms_hash_of_init`:

```text
terms_hash = cell_hash(terms)
terms$_ policy_version:uint32 price_per_call:Coins storage_fee:Coins
  cleanup_bounty:Coins response_sla:uint32 refund_claim_window:uint32
  ^terms_tail = ServiceActorTermsV1;
terms_tail$_ metadata_hash:uint256 proof_scheme_hash:uint256
  has_attestor:uint1 attestor_key_id:uint256 = ServiceActorTermsTailV1;
```

`attestor_key_id` is written as zero when `has_attestor = 0` (SA:275).
Admission gates (`open_access`, `authorized_caller`, `rate_limit_per_day`) are
excluded (SA:29-38, SA:255-261). For the software-work profile `metadata_hash`
and `proof_scheme_hash` are fixed by design §2.3 (`NSM1` and
`SHA-256("tos.service.service-actor.receipt.software-work-v1")`). `call` builds
this cell once, compares its hash with `expected_terms_hash`, stores the hash
and emits the cell itself in the request snapshot (SA:641-648, section 8.1).

## 6. Response statement (SRP2)

SA:147-148, SA:301-317; `begin_signing_domain` SD:12-21:

```text
srp2$_ tag:uint32=0x53525032 global_id:int32 actor_wc:int8 actor_addr:uint256
  request_id:uint64 request_hash:uint256 response_hash:uint256
  ^srp2_tail = ServiceResponseStatementV2;
srp2_tail$_ caller:MsgAddressInt terms_hash:uint256 price:Coins
  response_deadline:uint64 refund_claim_deadline:uint64 = ServiceResponseTailV2;
response_domain_hash = cell_hash(srp2)
```

`global_id` is ConfigParam 19 (`GLOBALID`); the actor address is the
contract's own address. Every other field is in the request snapshot
(section 8.1: `terms_hash` is the hash of its terms cell and `price` is that
cell's `price_per_call`), except `response_hash`, which the `respond` body
carries. The attestor signs the 32 raw bytes of `response_domain_hash` with
ML-DSA-44 under the context of section 3, and the contract verifies with
`PQCHECKSIG_MLDSA44` against the request's snapshotted stored key
(SA:696-704; RS `sign_service_response` / `verify_service_response`). For the
software-work profile `response_hash` is `cell_hash(SoftwareWorkReceiptV1)`
(`SOFTWARE_WORK_RECEIPT_TVM_V1.md`).

## 7. Inbound messages

SA:54-71 list every inbound body. Every body starts with `op:uint32
query_id:uint64`. Bounced messages and empty bodies are ignored (SA:558,
SA:563). Unknown ops fail with 1910 (SA:996). Every handler ends its body parse
with `end_parse`, so trailing bits or references fail with the TVM
cell-underflow exit 9, as does a missing field.

### 7.1 `call`

SA:55-56, SA:576-678:

```text
call#53564301 query_id:uint64 request_hash:uint256 expected_terms_hash:uint256
```

Checks, in order: active (1901); policy bounds (1903-1906); the attestor
commitments of section 4.1 (1925, or 62/63 for a non-canonical stored key);
admission (1923); payment covering `price_per_call`, then `storage_fee` (1902);
execution allowance (1929); capacity (1907, 1908); id overflow (1909); daily
rate limit (1924); body parse; terms match (1926); backing of existing
obligations plus reserve (1928). Coin sums past `2^120` fail with 1927.

Effect: stores the pending request (section 4.2) under
`request_id = next_request_id`, increments the counters, liabilities and storage
lock, reserves all preexisting backing plus `price + storage_fee`, emits the
request snapshot (section 8.1), and returns the unused value to the caller with
mode 128 (SA:650-676).

`request_hash` is stored opaquely; conforming clients refuse a zero value and
never reuse one (design §3.1, §3.2).

### 7.2 `respond`

SA:57-59, SA:680-720:

```text
respond#53564302 query_id:uint64 request_id:uint64 response_hash:uint256
  signature:(snapshot has_attestor ? ^StoredSignatureV1 : nothing)
```

Checks, in order: sender is the owner (1900); request pending (1913);
`now < response_deadline` (1912). Then, when the request snapshotted an
attestor: a missing signature reference fails with 9; the stored signature is
validated as section 3 states (62 for a length other than 2,420, 63 for an
exotic cell or non-canonical chain, 9 for a malformed wrapper); a signature
that does not verify over SRP2 (section 6) under the snapshotted key fails
with 1911. When the request snapshotted no attestor, a signature reference is
trailing data and fails with 9. Every refusal leaves state unchanged. The
sandbox pins 62 (SBX `malformed_attestor_keys_and_signatures_are_refused`) and
1911 (SBX `attestor_signature_cannot_be_replayed_across_requests`,
`a_response_signed_for_another_network_is_refused`); the unsigned `respond` to
an attested request is pinned only as aborted (SBX
`attestor_signed_respond_matches_the_compiled_bytecode`).

Effect (SA:708-718): deletes the request; credits `price + storage_fee` to
`withdrawable_revenue`; releases the storage-fee lock, the pending liability and
the request's capacity. No message is sent.

### 7.3 `expire`

SA:60, SA:722-749:

```text
expire#53564303 query_id:uint64 request_id:uint64
```

The body ends after `request_id`; trailing bits or references are refused (9).
Permissionless; the request is pending (1913) and
`response_deadline <= now < refund_claim_deadline` (1914, 1915); moves the
request to the refund set and its price from pending to refundable liability;
capacity is not released.

### 7.4 `claim_refund`

SA:61-62, SA:751-787:

```text
claim_refund#53564304 query_id:uint64 request_id:uint64 destination:MsgAddressInt
```

Checks, in order: refund present (1917); sender is the original caller (1918);
`now < refund_claim_deadline` (1916); backing for this price and every other
entry's price and storage lock, the operating reserve not required (1921); at
least `PAYOUT_GAS_ALLOWANCE` attached (1929). Effect: deletes the refund and
releases its capacity; reserves `backing - price`, pays `price` to
`destination` (mode 1) and the change to the sender (mode 128); credits
`storage_fee` to owner revenue (D4: the storage fee is non-refundable).

### 7.5 `sweep_expired_request`

SA:63, SA:789-887 (D3):

```text
sweep_expired_request#53564305 query_id:uint64 request_id:uint64
```

The body ends after `request_id`; trailing bits or references are refused (9).

- permissionless; the request is pending or refundable (1920) and
  `now >= refund_claim_deadline` (1919);
- with `backing` the balance minus this message's value: `backing` must cover
  `cleanup_bounty`, then `price`, then every other entry's price and storage
  lock, subtracted one at a time (1921). The operating reserve is not required
  (SA:853-854): the swept price is a customer's principal and, as in a refund,
  ranks ahead of the reserve, so a rent-eroded reserve never strands it (SBX
  `solvency_sweep_pays_principal_before_the_operating_reserve`). At least
  `PAYOUT_GAS_ALLOWANCE` attached (1929);
- deletes the entry and releases its liability, storage lock and capacity;
- credits `storage_fee - cleanup_bounty` to owner revenue (SA:868-869);
- `raw_reserve(backing - cleanup_bounty - price)` (`remaining_after_payouts`,
  SA:243-245, SA:871), then sends `price` to the request's **caller** (mode 1,
  if non-zero), then `cleanup_bounty` to the sweeper (mode 1, if non-zero),
  then the change to the sweeper (mode 128) (SA:872-878).

Every swept entry is unanswered (a responded request no longer exists), so a
sweep always returns the price to the caller. The sends carry no
ignore-errors flag, so either all sends and the state commit or the
transaction rolls back. The value transfers are non-bounceable (section 8.2):
a failed delivery to the caller after the action phase does not restore the
entry.

### 7.6 `update_policy`

SA:64-68, SA:889-931:

```text
update_policy#53564306 query_id:uint64
  price_per_call:Coins storage_fee:Coins cleanup_bounty:Coins
  response_sla:uint32 refund_claim_window:uint32
  active:uint1 open_access:uint1 has_authorized_caller:uint1
  authorized_caller:MsgAddress rate_limit_per_day:uint32
  ^[ metadata_hash:uint256 proof_scheme_hash:uint256 ]
```

Fields are read in exactly this order; the referenced cell and the body both
end after their last field, and trailing bits or references are refused (9).
`authorized_caller` is always present: when `has_authorized_caller = 0` it is a
filler that admission never compares (section 7.1), and clients write the owner
address there. `rate_limit_per_day = 0` means unlimited.

Owner only (1900); bounds as `call` (1903-1906); replaces
price, fees, SLA, window, `active`, access, rate limit, `metadata_hash` and
`proof_scheme_hash`, and sets `policy_version + 1`. It cannot change the
attestor.

### 7.7 `revoke_attestor`

SA:70, SA:949-961:

```text
revoke_attestor#53564308 query_id:uint64
```

Owner only (1900). Writes `has_attestor = 0`, `attestor_key_id = 0` and no key
reference. Pending requests keep their snapshot (SBX
`revoke_attestor_is_never_frozen_by_a_pending_request`). If an attestor was
set, `terms_hash` changes, so outstanding quotes fail with 1926;
`policy_version` is not bumped.

### 7.8 `rotate_attestor_key`

SA:69, SA:933-947:

```text
rotate_attestor_key#53564307 query_id:uint64 attestor_key:^StoredKeyV1
```

Owner only (1900). The contract derives the key id with `pq::key_id`, which
first validates the stored key (section 3: 62, 63, or 9), and writes
`has_attestor = 1`, that id and the key reference. A refusal leaves state
unchanged (SBX `malformed_attestor_keys_and_signatures_are_refused`). There is
no key-id field and no possession signature: a key the owner does not control
cannot produce SRP2 signatures, so a wrong key only makes `respond` impossible
for requests admitted under it, and those requests refund to their callers;
nothing can be taken. Pending requests keep their snapshot. Unless the new key
is the one already set, `terms_hash` changes, so outstanding quotes fail with
1926; `policy_version` is not bumped. Under D5 a conforming buyer accepts a new
key only after a new Capability version names it in manifest key 21.

### 7.9 `withdraw_revenue`

SA:71, SA:963-994:

```text
withdraw_revenue#53564309 query_id:uint64 amount:Coins
```

Owner only (1900); `backing` must cover pending and refundable liability, the
storage lock and `MINIMUM_OPERATING_RESERVE`, and `amount` must not exceed the
lesser of `withdrawable_revenue` and the remainder (1922, including a zero
amount when the obligations are not covered); at least `PAYOUT_GAS_ALLOWANCE`
attached (1929). Pays `amount` to the owner address (mode 1) and the change to
the sender (mode 128).

## 8. Outbound messages

### 8.1 Request snapshot (D10)

SA:73-78, SA:151, SA:478-502, SA:667-668. A successful `call` emits exactly one
external out-message, built as `ext_out_msg_info` with `src = addr_none`,
`dest = addr_none`, no `init`, and the body by reference, sent with mode 1. The
action phase replaces the source with the actor's own address, so in the
finalized transaction the message has `src` = the actor and `dest = addr_none`;
a resolver requires exactly that:

```text
request_snapshot#53415231 request_id:uint64 caller:MsgAddressInt
  request_hash:uint256 response_deadline:uint64 refund_claim_deadline:uint64
  terms:^ServiceActorTermsV1 = ServiceActorRequestSnapshotV1;
```

The tag is ASCII `SAR1` (RS `SERVICE_ACTOR_REQUEST_SNAPSHOT_TAG`). There is no
schema field. `terms` is the exact `terms_hash` preimage of section 5, the same
cell `call` hashed: its cell hash is the request's `terms_hash`, and it carries
`policy_version`, `price_per_call` (the request's price), `storage_fee`,
`cleanup_bounty`, `response_sla`, `refund_claim_window`, `metadata_hash`,
`proof_scheme_hash`, `has_attestor` and `attestor_key_id` (zero when
`has_attestor = 0`). Every value equals the stored pending request; `caller` is
the `call` sender, `response_deadline = now + response_sla` and
`refund_claim_deadline = response_deadline + refund_claim_window` at the `call`
(SA:639-640). The stored key is not emitted. The message is sent after the
reserve and before the mode-128 change transfer, so its forward fee is paid
from the caller's attached value, never from retained backing.

A conforming decoder (RS `decode_request_snapshot`) takes `terms_hash` as the
cell hash of `terms` and refuses any other tag, a missing field, trailing bits
or references in any of the three cells, `has_attestor = 1` with a zero key
id, `has_attestor = 0` with a non-zero key id, and
`response_deadline + refund_claim_window != refund_claim_deadline` (checked
addition).

Resolvers read the snapshot only from the finalized `call` transaction and
verify an existing request against it (design §2.4 steps 5-9). It opens
`terms_hash` without reading account state, and with the actor address,
`global_id` and the `respond` body's `response_hash` it supplies every SRP2
input.

### 8.2 Value transfers

SA:205-214, SA:247-253: `send_value` builds a non-bounceable internal message
(`0x10` flags) with an empty body. Payouts use mode 1; change uses mode 128
after a `raw_reserve` of the backing that must stay.

## 9. Exit codes

SA:94-128 and PB:18-20.

| Code | Name | Raised by |
|---:|---|---|
| 9 | TVM cell underflow | any handler: missing field, trailing data; `respond` without the required signature reference or with an unexpected one; malformed stored-key or stored-signature wrapper |
| 62 | `pq::error::key_length` | `rotate_attestor_key` (key length not 1,312); `respond` (signature length not 2,420); `call` (deploy key) |
| 63 | `pq::error::malformed_key` | `rotate_attestor_key`, `respond`, `call`: exotic cell or non-canonical chain |
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
| 1911 | `bad_response_signature` | `respond` |
| 1912 | `response_window_closed` | `respond` |
| 1913 | `request_not_pending` | `respond`, `expire`; getter `get_request_attestor_key` |
| 1914 | `expire_too_early` | `expire` |
| 1915 | `expire_too_late` | `expire` |
| 1916 | `refund_claim_expired` | `claim_refund` |
| 1917 | `refund_not_found` | `claim_refund` |
| 1918 | `not_refund_caller` | `claim_refund` |
| 1919 | `sweep_too_early` | `sweep_expired_request` |
| 1920 | `request_not_live` | `sweep_expired_request` |
| 1921 | `insufficient_balance` | `claim_refund`, `sweep_expired_request` |
| 1922 | `insufficient_revenue` | `withdraw_revenue` |
| 1923 | `not_authorized` | `call` |
| 1924 | `rate_limited` | `call` |
| 1925 | `bad_attestor_key` | `call`: attestor commitments inconsistent (section 4.1) |
| 1926 | `terms_mismatch` | `call` |
| 1927 | `amount_range` | any coin arithmetic on supplied state |
| 1928 | `operating_reserve_unfunded` | `call` |
| 1929 | `insufficient_execution_payment` | `call`, `claim_refund`, `sweep_expired_request`, `withdraw_revenue` |

Exit 61 (`pq::error::algorithm`) is unreachable: the contract passes only the
ML-DSA-44 suite.

## 10. Getters

SA:1001-1071. Convenience only; resolvers decode the account data exactly
(design §2.4 step 3).

| Getter | Returns |
|---|---|
| `get_service_data()` | `owner, active, policy_version, price_per_call, storage_fee, cleanup_bounty, response_sla, refund_claim_window, open_access, has_authorized_caller, authorized_caller, rate_limit_per_day, metadata_hash, proof_scheme_hash, has_attestor, attestor_key_id, next_request_id, pending_count, live_count, withdrawable_revenue, locked_storage_fees, pending_liability, refundable_liability, call_day, calls_today` |
| `get_request(request_id)` | `found, caller, price, storage_fee, cleanup_bounty, response_deadline, refund_claim_deadline, policy_version, request_hash, terms_hash, has_attestor, attestor_key_id`; all zero and a null caller when not pending |
| `get_refund(request_id)` | `found, caller, price, storage_fee, cleanup_bounty, refund_claim_deadline`; all zero and a null caller when absent |
| `get_attestor_key()` | the policy's stored key cell, or null when there is no attestor (`load_state` is `impure`, so the key it loads is kept; SA:321, SA:1043-1046) |
| `get_request_attestor_key(request_id)` | the pending request's snapshotted stored key cell, or null; fails with 1913 when the request is not pending |
| `get_pending_count()` | `pending_count` |
| `get_live_count()` | `live_count` |
| `get_caller_live_count(caller)` | live entries of `caller` |

## 11. Invariants

1. Coins arithmetic is checked below `2^120`; liabilities never go negative
   (SA:133-145).
2. Balance covers `pending_liability + refundable_liability +
   locked_storage_fees + MINIMUM_OPERATING_RESERVE` after every admission and
   withdrawal. A refund or a sweep may consume the reserve, but no other
   customer's price or storage backing (SA:227-236, SA:770-771, SA:853-854).
3. A request resolves exactly once: respond (price to owner revenue), refund
   (price to the caller's destination) or sweep (price to the caller). The
   storage fee is never refunded; on sweep its bounty part goes to the sweeper.
4. A request's attestor, terms and deadlines are fixed at `call`; no owner
   action changes them.
5. With an attestor snapshotted, no `respond` succeeds without both the owner
   sender and a valid ML-DSA-44 signature by the snapshotted key over SRP2.
6. The policy and every pending request hold the single "no attestor" encoding
   or a key whose derived id equals the stored id.
7. Every successful `call` emits exactly one request snapshot message that
   equals the stored request, and whose terms cell hashes to the stored
   `terms_hash`.

## 12. Gates before this layout is frozen

Listed in design §9: sandbox on both VMs, the adversarial cases, gas and size
(including the `respond` and `rotate_attestor_key` owner-wallet external
messages within 65,535 bytes), vectors generated from contract execution, the
resolver, live-chain lifecycles and an independent security review. Sandbox
tests exist on the implementing branch (SBX at `4c62edcae`); none of the gates
has been accepted as of 2026-11-07.
