# OpenFox Direct Signed Agent Gifts V1

**Status:** V1 product flow and canonical encodings frozen; G0-G2 local
implementation and compositional acceptance complete; independent G3
deployment acceptance pending

**Privacy class:** E2EE-private before broadcast; transparent after broadcast

**Supported V1 asset:** native TOS only

**Related specifications:**

- [`TOS_AGENTIC_INTERNET_OPERATION_ARCHITECTURE_V1.md`](TOS_AGENTIC_INTERNET_OPERATION_ARCHITECTURE_V1.md)
- [`OPENFOX_AUTONOMOUS_MESSENGER_ECONOMY_PLAN.md`](OPENFOX_AUTONOMOUS_MESSENGER_ECONOMY_PLAN.md)
- [`OPENFOX_ECONOMIC_BRIDGE_V1.md`](OPENFOX_ECONOMIC_BRIDGE_V1.md)
- [`AGENT_NATIVE_MESSENGER_V1.md`](AGENT_NATIVE_MESSENGER_V1.md)
- [`DNS_ALIAS_V1.md`](DNS_ALIAS_V1.md)
- [`AUTH.md`](AUTH.md)
- [`OPENFOX_AGENT_GIFTS_V1_FIRST_PRINCIPLES.md`](OPENFOX_AGENT_GIFTS_V1_FIRST_PRINCIPLES.md)

## 1. Product decision

An OpenFox Agent may send another OpenFox Agent one optional, fixed-amount,
time-limited native TOS Gift inside an existing authenticated end-to-end
encrypted conversation.

V1 uses the smallest useful protocol:

1. sender Agent A asks recipient Agent B for a native TOS address;
2. B returns one address inside their authenticated E2EE conversation;
3. A obtains owner authorization and its deployed Agent Account signs one
   exact, time-limited generic native-send external-message BOC transferring
   native TOS to that address;
4. A sends the exact signed BOC to B through E2EE Messenger;
5. B verifies and submits those unchanged bytes to a TOS node; and
6. only finalized destination credit establishes payment.

The signed BOC is a time-limited digital cheque. Anyone holding it may submit
it, but no holder can change the signed amount or destination.

V1 creates no Receiver Profile, Gift delegation, receive ticket, ticket-signing
key, Gift Vault, escrow, claim contract, refund contract, or on-chain Gift
registry.

V1 also excludes stablecoins, first-contact Gifts, public Gift discovery,
private-room Gifts, group packets, random or equal shares, split claims,
high-load parallel redemption, and sender-noncancellable guaranteed funding.
Each requires a separate versioned profile.

Ordinary OpenFox messaging remains free and usable when Gift support is
disabled or no wallet is configured. A Gift is a non-purchase transfer. It has
no Capability, Quote, software execution, Receipt, or provider-settlement
semantics.

`Gift` is the architectural term. “Red packet” is presentation metadata only.

## 2. Honest guarantees and limitations

### 2.1 What the signed BOC guarantees

Before submitting a conforming BOC, B can verify that it:

- was signed by A's pinned Agent Account controller;
- is valid only for the intended TOS network and Agent Account identity;
- uses one exact Agent Account sequence number;
- expires at one exact signed `valid_until` time;
- contains exactly one permitted native TOS send action;
- sends exactly `amount_atomic` to B's previously returned address;
- pays Agent Account execution and forwarding fees separately from the Gift amount;
- contains no second action, plugin mutation, StateInit, memo, comment, Gift
  marker, AgentID, alias, room ID, or arbitrary payload; and
- can be accepted at most once under the Agent Account sequence rules.

### 2.2 What is not guaranteed before finalization

Funds are not locked when A sends the BOC to B. Before successful execution:

- A may no longer have enough native TOS for the amount plus fees;
- the signed Agent Account sequence may be consumed by a cancellation or
  another account action;
- the BOC may expire before inclusion;
- node submission may fail or remain ambiguous; and
- a transaction observed before finality may still disappear.

The UI MUST NOT describe an unfinalized Gift as “funded,” “locked,”
“guaranteed,” “received,” “claimed,” or “paid.”

Only `finalized-paid` means that B received value. Other allowed states are:

```text
address-requested
address-received
owner-authorization-required
owner-authorized
boc-signed
offer-delivered
currently-executable
currently-unexecutable
broadcast-submitted
expired-unpaid
invalidated-unpaid
insufficient-funds
finality-unknown
```

This is the user-visible status vocabulary after a Gift has been offered.
Section 9 additionally names private orchestration and recipient-observation
states that are never presented as payment claims.

`finalized-paid`, `expired-unpaid`, and `invalidated-unpaid` are terminal.
Every other state is non-terminal. In particular, `insufficient-funds` and
`currently-unexecutable` may return to executable after a top-up or reversible
policy change; custody retains the original sequence claim. Controller rotation
is different: it consumes a sequence and becomes finalized invalidation.

## 3. Identity and address authority

### 3.1 Agent identity

A and B are canonical AgentIDs in private orchestration state. A `.tos` alias
is resolved once through finalized state before the Gift flow starts. Later
alias reassignment cannot retarget the conversation, address response, signed
BOC, payment record, or audit record.

EndpointID, DeviceID, SessionID, Relay identity, display name, and alias text
are not payment identities.

### 3.2 Existing authenticated conversation

V1 permits Gift address exchange only inside an already established direct
conversation whose sender and recipient AgentIDs are authenticated by the
existing Messenger identity, delegation, device, session, and replay
protections.

V1 introduces no new Gift-specific Agent delegation. The existing Messenger
authorization chain establishes who sent an E2EE application event; it does not
sign a wallet transaction and cannot move funds.

First-contact Gift requests are not supported. A public Agent profile, Gateway
result, Relay envelope, push notification, or unverified message cannot supply
a Gift destination.

### 3.3 Address authority

B authorizes the destination for one Gift intent by returning it in an
authenticated E2EE `GiftAddressResponseV1`. This is a conversational payment
instruction, not proof of wallet-key ownership and not permission to spend A's
funds.

A MUST NOT infer the address from alias records, profile text, model output,
previous Gifts, Gateways, Relays, push providers, indexers, or on-chain
transactions. A's owner confirmation displays the exact returned address
before signing.

Operators requiring independent destination-key ownership proof or portable
recipient authorization must use a later profile. V1 does not claim those
properties.

## 4. E2EE address exchange

### 4.1 Address request

A generates a fresh random 256-bit `gift_intent_id` outside the model and sends:

```text
GiftAddressRequestV1 {
  network
  gift_intent_id
  sender_agent_id
  recipient_agent_id
  sender_agent_account
  asset_kind = native_tos
  amount_atomic
  requested_valid_until
}
```

The request is accepted only when the E2EE sender is A, the local recipient is
B, the direct conversation is live, the network is supported, the amount and
validity window satisfy local policy, and the intent ID has not been reused
with different semantics.

`amount_atomic` uses positive canonical unsigned base-10 text:

```text
[1-9][0-9]*
```

No sign, decimal point, exponent, whitespace, locale formatting, or leading
zero is allowed.

### 4.2 Address response

B's local custody or wallet boundary selects a native TOS destination and
returns:

```text
GiftAddressResponseV1 {
  network
  gift_intent_id
  request_digest
  sender_agent_id
  recipient_agent_id
  asset_kind = native_tos
  amount_atomic
  destination_address
  response_not_after
}
```

The response is authenticated by the existing E2EE Messenger session. It has
no additional ticket signature and refers to no Receiver Profile or Gift
delegation.

The full request digest prevents moving an address between intents. Exact
duplicate responses are idempotent. Reusing one intent ID with another network,
participant, sender Agent Account, amount, address, or expiry is a conflict.

B may return a fresh address to reduce simple linkage, but V1 neither requires
one nor claims anonymity. A must authorize and sign before
`response_not_after`, which cannot be later than `requested_valid_until`.
The signed BOC's `valid_until` MUST NOT be later than either bound.

## 5. Sender authorization and custody

Gift sending is disabled by default. Before signing, A's owner policy or
explicit confirmation binds:

- network and canonical recipient AgentID;
- sender Agent Account and its owner wallet;
- exact or maximum native TOS amount;
- B's exact returned destination;
- validity-window bounds;
- Gift count and rolling native TOS amount limits;
- native TOS fee reserve;
- maximum concurrent active Gifts; and
- whether model-assisted intent parsing is allowed.

The confirmation independently renders recipient, network, amount, exact
destination, sender Agent Account, owner wallet, controller key ID, current
sequence, `valid_until`, fee reserve,
request/response digests, the fact that funds are not locked, and the ways the
BOC may expire or become invalid.

OpenFox and the model never receive an owner or controller private key or an
unsigned account request. `tosctl` custody is the sole local authority for the
Agent Account address and controller. It reads finalized account state, claims
the sequence in the journal shared by every controller action, builds the exact
action, signs it, durably persists the exact BOC, and returns only bounded
status to OpenFox. Raw-hash and unjournaled controller signing are unavailable.

## 6. Signed Gift BOC profile

### 6.1 Approved sender Agent Account

V1 uses the one pinned TOS Agent Account code hash and its canonical generic
`agent_native_send` signed-external-message profile. The pre-release Agent
Account interface is replaced in place; there is no Wallet V5R1 Gift sender,
legacy Agent Account parser, dual-version deployment, or migration mode.

G0 freezes the exact Agent Account code hash, minimum TVM/global version 4,
TVM `GLOBALID` check,
external-message constructor, BOC serialization, signed validity, controller epoch and sequence,
generic operation encoding, account-address-bound signature preimage, fixed
send mode and positive/negative vectors. `agent_task_send` also gains the
global-ID field but is never accepted as a Gift action.

The Agent Account must already be active in finalized state and must match the
owner-private `tosctl agent wallet` profile's owner, controller, policy, and
address. V1 does not combine account creation, deployment, migration, funding,
or recovery with Gift execution. The underlying Wallet V5R1 remains the account's
owner/recovery wallet and is not a separate Gift balance.

The frozen implementation constants are:

```text
Agent Account code hash:
  tvm-cell-sha256:e1f436e4cc26b88cad0b06f804380eda7d715c7499d789f85ac83e6f60b4b679
minimum TVM/global version: 4
agent_task_send opcode:    0x41475003
agent_native_send opcode:  0x41475004
agent_cancel_seqno opcode: 0x41475005
maximum signed action value: 281474976710655 nanoTOS (2^48 - 1)
controller-signature domain SHA-256:
  ede715a9852fbba2c3c234ed0d27329ae34d6263a82cfb6215da87c91683b471
```

The final account data includes an immutable, nonzero random
`deployment_id:uint256`, generated by `tosctl` at account creation. Finalized
readers bind every prepared Gift to that exact value. The supported
`tosctl agent-account deploy --new-generation` replacement flow refuses an
active or frozen predecessor, requires outstanding controller signatures to
have expired, retires their custody records, and durably
assigns a new deployment ID/address after owner confirmation but before
broadcast. Operators must not redeploy identical StateInit: no contract can
distinguish that act from restoration of the old generation, and custody's
durable high-water mark deliberately fails closed on the resulting
epoch/sequence rollback.

The controller signature preimage binds that domain hash, signed global ID,
Agent Account workchain and 256-bit address, and exact payload cell hash. The
external payload is rejected unless its global ID equals TVM `GLOBALID` and its
`controller_epoch:uint64` equals finalized account state.
Every controller action must also satisfy
`now < valid_until <= now + default_task_timeout`; the stored timeout is an
on-chain upper bound, not merely a custody default. An owner controller-key
rotation increments both `controller_epoch` and `seqno`, permanently
invalidating every outstanding controller signature, including future-sequence
signatures made by a key that is later restored.

The native `max_per_tx` and `daily_limit` meter native TOS message value only.
The generic `agent_task_send` body can invoke other contracts and does not
measure tokenized or contract-internal assets. Operators must therefore keep
such assets out of this account unless the invoked contract independently
enforces policy. Gift V1 never emits `agent_task_send` and supports native TOS
only.

### 6.2 One active Agent Account action

One Agent Account is the Agent's sole automatic-spending account. Custody uses
one process-independent deployment-generation/epoch/sequence journal shared by Gift and non-Gift controller
actions. It permits at most one active primary signed action for the current
sequence, plus at most one separately owner-authorized cancellation racing that
same action. While unresolved, unrelated controller spending is blocked.

Before signing, custody resolves the exact finalized account identity, pinned
code hash, deployment ID, owner, controller, controller epoch, policy, sequence, native TOS balance, Gift amount,
maximum fee reserve, and absence of another primary action.

Exact retry returns the same durable BOC. A changed request, response, address,
amount, sequence, validity time, action, or BOC is a conflict.

### 6.3 One-action native TOS transfer

The signed request contains exactly one send action whose internal message
binds:

```text
destination_address
amount_atomic
message_value = amount_atomic
fixed_send_mode = 3 (pay fees separately, ignore action error)
fixed_bounce_policy
body_absent = inline-empty body branch
state_init_absent
```

The fixed bounce policy is non-bouncing. Owner confirmation must treat the
exact destination as irreversible: an uninitialized or failing recipient
contract does not return principal to the Agent Account.

The frozen mode pays account execution and forwarding fees separately from Gift
principal. Its ignore-action-error bit ensures that an accepted but
insufficient output consumes the sequence rather than allowing repeated
recipient-triggered gas charges. Such a finalized execution without exact
destination credit is `invalidated-unpaid`; the attempted amount is
conservatively committed to the account's `spent_today` even though no output
credit occurred. Emulator vectors define and prove the exact finalized
destination-credit predicate.

V1 rejects zero or excessive amounts, `agent_task_send`, multiple or unknown
actions, another destination or amount, caller-selected mode or bounce policy,
fees deducted from principal, any non-empty or referenced body, StateInit,
deployment, hidden references, trailing data, and any BOC whose complete
semantics cannot be reconstructed.

An exact signed BOC is bounded to 56 KiB, reserving deterministic space for
the canonical offer fields and up to 4 KiB of padding. Every complete Gift
application object remains within Messenger's 64 KiB application-data bound.

### 6.4 Signed Gift identity

```text
SignedGiftID =
  H(signed-gift-domain || exact_signed_boc_bytes)
```

Only the exact signed bytes may be submitted. The private sender journal binds:

```text
gift_intent_id
address_request_digest
address_response_digest
owner_authorization_digest
unsigned_transfer_digest
exact_signed_boc_digest
SignedGiftID
```

`SignedGiftID` is not inserted into the on-chain message.

## 7. Signed offer, verification, and broadcast

A sends inside generic E2EE application data:

```text
GiftSignedBOCOfferV1 {
  gift_intent_id
  address_request_digest
  address_response_digest
  signed_gift_id
  exact_signed_boc
  optional_display_message
  padding
}
```

The display message has no payment authority. B derives the authoritative
Agent Account, network, amount, destination, sequence, and validity from the BOC
and its durable address-exchange record.

Before broadcast, B verifies:

1. the E2EE participants are canonical A and B;
2. request and response digests match B's durable record;
3. BOC digest and `SignedGiftID` are canonical;
4. the external message targets the exact sender Agent Account in the request
   using the pinned code/profile;
5. account address, code hash, deployment ID, owner, controller, controller epoch, and signed network/global ID
   match finalized state and the connected chain's actual `GLOBALID`;
6. sequence equals the latest finalized Agent Account sequence;
7. `valid_until` is in bounds with sufficient inclusion margin;
8. A's Agent Account controller signature is valid over the frozen domain tag,
   signed network/global ID, exact account address, and exact canonical payload
   hash; the global ID also remains inside that payload;
9. there is exactly one permitted action and no hidden data;
10. destination equals the address B returned for this intent;
11. amount equals the request, response, and BOC;
12. body and StateInit are absent;
13. fees are separate from principal; and
14. latest finalized balance covers amount plus fee reserve.

A readiness observation is not a guarantee that state remains unchanged.

B submits the exact original BOC to one or more TOS nodes. B never rebuilds,
edits, or re-signs it. Repeated submission is permitted while finality is
unresolved; the first accepted execution consumes the account sequence even if
its mode-3 output action fails, and later duplicates fail before charging
accepted-message gas.
Submission acknowledgement, mempool observation, or a transaction hash is not
payment evidence.

## 8. Finality, expiry, and cancellation

`finalized-paid` requires a finalized transaction chain linking:

```text
exact signed external BOC
  -> accepted execution by A's exact Agent Account and sequence
  -> its one permitted internal message
  -> exact native TOS credit to B's returned destination
```

A balance snapshot alone is insufficient because unrelated transfers may have
changed the same account.

Local wall-clock expiry is not terminal evidence. `expired-unpaid` requires a
finalized checkpoint whose chain time is later than `valid_until`, plus absence
of successful execution and matching destination credit. Ambiguity remains
`finality-unknown`; no replacement is signed while the original may execute.
Expiry requires no refund because funds were never locked.

A may cancel by broadcasting a separately owner-authorized action consuming the
same sequence. Cancellation races with B's BOC: whichever valid request executes
first wins. `invalidated-unpaid` is terminal only after finalized state proves a
non-Gift sequence consumption or output-action failure and no matching
destination credit. Controller rotation consumes a sequence and therefore
permanently invalidates the Gift once finalized. Policy tightening without
sequence consumption is reversible and only produces non-terminal
`currently-unexecutable`; the original claim remains reserved because policy
loosening may re-enable the BOC before expiry.

## 9. Crash safety and idempotency

Sender lifecycle:

```text
draft -> recipient-resolved -> address-requested -> address-received
      -> owner-authorization-required -> owner-authorized -> boc-signed
      -> offer-delivered -> currently-executable | insufficient-funds
                         | currently-unexecutable | broadcast-submitted
                         | finality-unknown
      -> finalized-paid | expired-unpaid | invalidated-unpaid
```

Recipient lifecycle:

```text
address-request-observed -> address-response-sent -> signed-offer-observed
                         -> verified -> broadcast-submitted
                         -> currently-executable | insufficient-funds
                          | currently-unexecutable | finality-unknown
                         -> finalized-paid | expired-unpaid
                          | invalidated-unpaid
```

Each transition is fsynced before the next external side effect. Restart uses
the exact canonical request/response, exact BOC bytes, and digests. A never
signs another BOC while the original may execute; B resubmits only the exact
original bytes.

## 10. Privacy and Messenger carriage

Requests, responses, and offers exist only inside E2EE application data. The
Relay-visible envelope uses the existing generic private-application class and
frozen padding buckets. Push notifications are content-free.

The chain receives no Gift contract, registry, opcode, memo, greeting, AgentID,
alias, conversation ID, EndpointID, DeviceID, or room ID.

After execution, observers may see A's Agent Account, B's destination, exact
amount, timing, sequence, validity window, funding history, reuse, and later
consolidation. Because the same account performs Agent tasks and Gifts, every
Gift is linkable to A's operating history; B learns that primary account,
balance, and policy before submission. V1 deliberately chooses coherent custody
over unlinkability and claims neither relationship privacy, amount
confidentiality, nor transaction anonymity.

## 11. OpenFox and model boundary

OpenFox exposes narrow operations:

```text
PrepareGift(recipientInput, amount, expiry, display)
RequestGiftAddress(giftIntentID)
AuthorizeGift(addressResponseDigest, unsignedTransferDigest, ownerDecision)
SignGiftBOC(giftIntentID)
SendSignedGift(signedGiftID)
VerifySignedGift(signedGiftID)
BroadcastSignedGift(signedGiftID)
RefreshSignedGift(signedGiftID)
CancelSignedGift(signedGiftID, ownerDecision)
```

The model may propose recipient text, amount, expiry, and greeting. It cannot
provide or alter canonical AgentID, authenticated conversation identity, B's
address response, wallet, network, sequence, unsigned request, BOC, fee fields,
signature, or finality evidence.

The exact address response, BOC, wallet data, and custody material are never
model input. Model-assisted parsing requires an operator warning that submitted
recipient text, amount, expiry, and greeting leave the local privacy boundary.

## 12. Logs, metrics, and audit

General logs, traces, crash dumps, analytics, and support bundles MUST NOT
contain raw address exchanges, exact BOCs, aliases, full AgentIDs, destination
addresses, amounts, private display text, or owner authorization material.

Metrics expose aggregate counts only, without participant, wallet,
`SignedGiftID`, amount, or destination labels.

An explicit private audit export may contain:

```text
SignedGiftAuditBundleV1 {
  authenticated Messenger Event references
  canonical address request and response
  exact signed BOC
  SignedGiftID
  finalized sender-Agent-Account execution reference
  finalized destination-credit reference
  optional owner authorization record
}
```

It proves conversation provenance, B's returned address, A's Agent Account
controller signature,
transfer semantics, and outcome. It does not prove B owns the destination key
unless B separately discloses such proof. Selective disclosure irreversibly
reveals relationship information and requires explicit owner action.

No public API provides Gift lists, feeds, leaderboards, or social-payment
graphs.

## 13. Required refusal tests

Implementations test at least:

- alias reassignment cannot retarget an active Gift;
- unestablished, unauthenticated, room, Relay, Gateway, push, model, or stale
  address input fails;
- request/response intent, participant, network, amount, digest, or destination
  substitution fails;
- wrong network, Agent Account identity, code, owner, controller, controller epoch, sequence,
  validity, or signature fails;
- multiple actions, hidden data, plugin mutation, deployment, StateInit,
  unknown action, memo, comment, tag, or payload fail;
- wrong amount, destination, mode, bounce policy, or fee behavior fails;
- insufficient balance plus fee reserve is not executable;
- mode-3 output failure consumes sequence, emits no credit, and conservatively
  counts the attempted amount against the on-chain daily limit;
- supported account replacement creates a fresh deployment ID/address; prohibited identical-StateInit redeployment and any controller/sequence rollback fail closed in custody and recipient resolution;
- duplicate delivery and node submission create at most one payment;
- changed bytes under one `SignedGiftID` fail;
- local time alone cannot produce `expired-unpaid`;
- cancellation races remain nonterminal until finalized resolution;
- controller rotation consumes sequence and permanently invalidates outstanding
  BOCs; policy tightening without sequence consumption remains nonterminal;
- ambiguous submission resolves finalized state before replacement or terminal
  reporting;
- crash recovery returns the same BOC and does not sign twice;
- node and chat acknowledgements cannot mark payment;
- external services cannot authorize spending; and
- diagnostics exclude prohibited data.

Every object is bounded, versioned, canonically encoded, domain-separated where
hashed, and rejects unknown fields and trailing data.

The canonical schema and digest-domain strings are frozen as:

```text
tos.agent-gift.address-request.v1
tos.agent-gift.address-response.v1
tos.agent-gift.signed-boc-offer.v1
tos.agent-gift.owner-authorization.v1
tos.agent-gift.owner-cancellation.v1
tos.agent-gift.unsigned-transfer.v1
tos.agent-gift.exact-signed-boc.v1
tos.agent-gift.signed-gift.v1
```

OpenFox exposes separate owner-private Unix sockets to the model and runtime.
The model principal can only start a Gift with recipient, amount, expiry and
greeting, then read a redacted lifecycle view. Canonical address-exchange
bytes, exact BOCs, Agent IDs, addresses, digests, custody actions, broadcast,
cancellation and finality refresh are runtime-only operations; the local API
never returns those private authority values to the model principal.

## 14. Repository ownership

| Repository | Responsibilities |
|---|---|
| `tos-service-spec` | This profile, canonical objects, BOC profile, vectors, negative corpus, and acceptance evidence |
| `tos` | The single Agent Account contract and native TOS semantics; no Gift contract is added |
| `tosctl` | Agent Account custody/journal, exact BOC construction/signing, verification, and raw-byte broadcast |
| `tos-service-protocol` | Canonical Gift types, wallet/BOC parser, finalized resolver, and adversarial vectors |
| `tos-messenger` | Authenticated E2EE address request/response and signed-offer carriage |
| `OpenFox` | Intent, owner-policy orchestration, durable state, and honest presentation |

`tos-service-gateway` and `tos-ai` are not required. Any Gateway projection is
non-authoritative and must not expose a standard Agent Gift graph.

## 15. Implementation sequence

### G0 — freeze profiles and vectors

- freeze request, response, offer, IDs, digests, and encodings;
- pin the one Agent Account code/profile, minimum TVM/global version 4, and exact
  signed-message/action encoding;
- freeze mode, bounce policy, fee reserve, and destination-credit predicate;
- publish positive and negative vectors;
- prove builder/parser equivalence in two implementations; and
- obtain wallet, Messenger, custody, privacy, and cross-repository review.

### G1 — read-only verification

- implement strict Gift and BOC parsing;
- implement finalized Agent Account execution and destination-credit resolution;
- implement observe-only OpenFox rendering;
- prove prohibited data does not reach model, diagnostics, Relay metadata, or
  push; and
- do not enable signing or broadcast.

### G2 — owner-authorized local Gifts

- implement one-active-primary-action custody shared by every Agent Account controller operation;
- implement E2EE address exchange and signed-offer delivery;
- implement owner authorization and rolling native TOS controls; and
- prove signing, broadcast, finalization, expiry, cancellation, insufficient
  funds, ambiguous submission, duplicate submission, and restart.

### G3 — independent acceptance

- operate A, B, Messenger, resolver, and validators independently;
- execute one fresh native TOS Gift;
- expire and cancel separate fresh Gifts;
- recover ambiguous submission and process restart;
- independently reconstruct the address response, BOC, sequence, transfer, and
  destination credit; and
- publish signed configs, binaries, code hashes, vectors, checkpoints, and
  repository commits.

### Local implementation evidence (2026-08-23)

The completed local evidence establishes G0-G2 without treating fixtures as
live-chain results:

- Rust sandbox tests execute the pinned Agent Account code and cover native
  payment, expiry, cancellation, controller rotation, policy and mode-3 output
  failure. Rust fixtures and the independent Go parser agree on the exact BOC
  profile and code hash.
- An isolated local validator run uses a Wallet V5R1 owner and the deployed
  Agent Account sender. It proves exact payment and destination credit,
  duplicate submission at most once, cancellation winning the shared sequence,
  finalized expiry without execution, generic task send, policy update,
  controller rotation, owner recovery send, and validator restart/catch-up.
- Protocol tests cover strict canonical request/response/offer decoding,
  adversarial BOCs, finalized sender transaction linkage, the one exact output,
  exact recipient credit, and bounded-history uncertainty.
- Two independently established Messenger daemons carry all three exact Gift
  application byte strings in both directions over authenticated direct E2EE;
  first-contact, room, unauthenticated, rendered, and Gift-specific outer
  metadata paths are refused.
- OpenFox cross-repository tests consume the Rust BOC fixture and canonical Go
  exchange objects, execute owner authorization, durable send/receive,
  verification and broadcast seams, then recover both roles as
  `finalized-paid`. Separate crash, ambiguous submission, cancellation and
  exact-byte retry tests cover failure recovery.

This is compositional executable acceptance, not G3. The remaining external
condition is an independently operated environment with at least three pinned
validator/read endpoints and two deployed Agent identities running the full
A/B/Messenger/resolver process topology. The host also needs the system
`libolm` development headers before the unrelated Matrix-enabled OpenFox root
test set can build; Gift packages and the native implementation do not depend
on that missing header.

## 16. Acceptance criterion

V1 is complete only when an operator can say:

```text
“Send 10 TOS to alice.tos as a time-limited Gift.”
```

and the implementation:

1. resolves `alice.tos` once to canonical Agent B;
2. uses an existing authenticated direct E2EE conversation;
3. asks B for a native TOS address;
4. receives one intent-bound authenticated address response;
5. obtains A's exact owner authorization;
6. signs one exact single-action time-limited Agent Account BOC;
7. delivers only that immutable BOC through E2EE Messenger;
8. lets B independently verify and submit the exact bytes;
9. transfers the exact amount if A's Agent Account state still permits execution;
10. creates no Gift contract or Gift-specific chain payload;
11. reports payment only from finalized destination credit; and
12. honestly reports expiry, invalidation, insufficient funds, or unknown
    finality as unpaid or unresolved.

## 17. Non-negotiable invariants

1. **V1 has no Receiver Profile, Gift delegation, receive ticket, or ticket-signing key.**
2. **V1 supports native TOS only.**
3. **B's destination comes only from an authenticated direct E2EE response for the exact Gift intent.**
4. **A's owner policy and Agent Account controller are the only spending authorities.**
5. **The exact signed BOC is payment authorization; chat text is not.**
6. **The BOC contains one native TOS transfer and no hidden action or payload.**
7. **B may submit but cannot redirect or modify payment.**
8. **Funds are not locked before execution, and the UI states this plainly.**
9. **Only finalized exact destination credit establishes payment.**
10. **Local time, submission, transaction hash, or chat acknowledgement is not terminal evidence.**
11. **The one Agent Account custody journal permits at most one active primary signed action per sequence, plus one separately owner-authorized cancellation.**
12. **AgentIDs and aliases never enter the on-chain transfer payload.**
13. **Agent Account, destination, BOC, sequence, fees, signature, and finality never come from model output.**
14. **Fees cannot reduce the signed Gift principal.**
15. **Exact BOC retries are idempotent; changed bytes are a conflict.**
16. **V1 does not claim guaranteed funding, destination-key ownership proof, anonymity, or amount confidentiality.**
17. **Gift support does not change the software-work commercial asset model.**
18. **Stablecoin, first-contact, room, guaranteed, group, and high-load Gifts require later profiles.**
