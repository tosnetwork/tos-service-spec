# OpenFox Direct Signed Agent Gifts V1

**Status:** V1 product flow frozen; canonical encodings, implementation, and
acceptance evidence pending

**Privacy class:** E2EE-private before broadcast; transparent after broadcast

**Supported V1 asset:** native TOS only

**Related specifications:**

- [`OPENFOX_AUTONOMOUS_MESSENGER_ECONOMY_PLAN.md`](OPENFOX_AUTONOMOUS_MESSENGER_ECONOMY_PLAN.md)
- [`OPENFOX_ECONOMIC_BRIDGE_V1.md`](OPENFOX_ECONOMIC_BRIDGE_V1.md)
- [`AGENT_NATIVE_MESSENGER_V1.md`](AGENT_NATIVE_MESSENGER_V1.md)
- [`DNS_ALIAS_V1.md`](DNS_ALIAS_V1.md)
- [`AUTH.md`](AUTH.md)

## 1. Product decision

An OpenFox Agent may send another OpenFox Agent one optional, fixed-amount,
time-limited native TOS Gift inside an existing authenticated end-to-end
encrypted conversation.

V1 uses the smallest useful protocol:

1. sender Agent A asks recipient Agent B for a native TOS address;
2. B returns one address inside their authenticated E2EE conversation;
3. A obtains owner authorization and signs one exact, time-limited standard
   wallet external-message BOC transferring native TOS to that address;
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

- was signed by A's pinned Gift wallet;
- is valid only for the intended TOS network and wallet identity;
- uses one exact wallet sequence number;
- expires at one exact signed `valid_until` time;
- contains exactly one permitted native TOS send action;
- sends exactly `amount_atomic` to B's previously returned address;
- pays wallet execution and forwarding fees separately from the Gift amount;
- contains no second action, plugin mutation, StateInit, memo, comment, Gift
  marker, AgentID, alias, room ID, or arbitrary payload; and
- can execute at most once under the approved wallet sequence rules.

### 2.2 What is not guaranteed before finalization

Funds are not locked when A sends the BOC to B. Before successful execution:

- A may no longer have enough native TOS for the amount plus fees;
- the signed wallet sequence may be consumed by a cancellation or another
  wallet action;
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
boc-signed
offer-delivered
currently-executable
broadcast-submitted
expired-unpaid
invalidated-unpaid
insufficient-funds
finality-unknown
```

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
participant, amount, address, or expiry is a conflict.

B may return a fresh address to reduce simple linkage, but V1 neither requires
one nor claims anonymity. A must authorize and sign before
`response_not_after`, which cannot be later than `requested_valid_until`.

## 5. Sender authorization and custody

Gift sending is disabled by default. Before signing, A's owner policy or
explicit confirmation binds:

- network and canonical recipient AgentID;
- sender Gift wallet;
- exact or maximum native TOS amount;
- B's exact returned destination;
- validity-window bounds;
- Gift count and rolling native TOS amount limits;
- native TOS fee reserve;
- maximum concurrent active Gifts; and
- whether model-assisted intent parsing is allowed.

The confirmation independently renders recipient, network, amount, exact
destination, sender wallet, current sequence, `valid_until`, fee reserve,
request/response digests, the fact that funds are not locked, and the ways the
BOC may expire or become invalid.

OpenFox and the model never receive a wallet private key or unsigned wallet
request. `tosctl` or an equivalently hardened custody process reads finalized
wallet state, builds the exact action, signs it, durably persists the exact BOC,
and returns only bounded status to OpenFox.

## 6. Signed Gift BOC profile

### 6.1 Approved sender wallet

V1 uses one pinned standard sender-wallet code hash and one canonical
signed-external-message profile. The first implementation candidate is TOS
Wallet V5.

G0 freezes the exact wallet code hash, network/global-ID and wallet-ID encoding,
external-message constructor, BOC serialization, signed validity and sequence,
action encoding, signature preimage, and positive/negative vectors. Multiple
wallet versions cannot share the same V1 profile identifier.

The wallet must already be active in finalized state. V1 does not combine
wallet deployment and Gift execution.

### 6.2 Dedicated Gift wallet

A conforming deployment uses a dedicated Gift wallet or bounded pool. Each
wallet has at most one active signed Gift. While active, the deployment prevents
unrelated payments and plugin or extension mutation from that wallet.

Before signing, custody resolves the exact finalized wallet identity, code hash,
sequence, native TOS balance, Gift amount, maximum fee reserve, and absence of
another active Gift.

Exact retry returns the same durable BOC. A changed request, response, address,
amount, sequence, validity time, action, or BOC is a conflict.

### 6.3 One-action native TOS transfer

The signed request contains exactly one send action whose internal message
binds:

```text
destination_address
amount_atomic
message_value = amount_atomic
fixed_send_mode
fixed_bounce_policy
body_absent
state_init_absent
```

The frozen mode pays wallet execution and forwarding fees separately from Gift
principal. Emulator vectors define and prove the exact finalized
destination-credit predicate.

V1 rejects zero or excessive amounts, multiple or unknown actions, another
destination or amount, caller-selected mode or bounce policy, fees deducted
from principal, any body or payload, StateInit, deployment, plugin mutation,
hidden references, trailing data, and any BOC whose complete semantics cannot
be reconstructed.

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
wallet, network, amount, destination, sequence, and validity from the BOC and
its durable address-exchange record.

Before broadcast, B verifies:

1. the E2EE participants are canonical A and B;
2. request and response digests match B's durable record;
3. BOC digest and `SignedGiftID` are canonical;
4. the external message targets a sender wallet using the approved Gift-wallet
   profile;
5. wallet address, code hash, wallet ID, and network/global ID match;
6. sequence equals the latest finalized sender-wallet sequence;
7. `valid_until` is in bounds with sufficient inclusion margin;
8. A's wallet signature over the exact request is valid;
9. there is exactly one permitted action and no hidden data;
10. destination equals the address B returned for this intent;
11. amount equals the request, response, and BOC;
12. body and StateInit are absent;
13. fees are separate from principal; and
14. latest finalized balance covers amount plus fee reserve.

A readiness observation is not a guarantee that state remains unchanged.

B submits the exact original BOC to one or more TOS nodes. B never rebuilds,
edits, or re-signs it. Repeated submission is permitted while finality is
unresolved; wallet sequence rules allow at most one successful execution.
Submission acknowledgement, mempool observation, or a transaction hash is not
payment evidence.

## 8. Finality, expiry, and cancellation

`finalized-paid` requires a finalized transaction chain linking:

```text
exact signed external BOC
  -> successful execution by A's exact Gift wallet and sequence
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
non-Gift sequence consumption and no matching destination credit.

## 9. Crash safety and idempotency

Sender lifecycle:

```text
draft -> recipient-resolved -> address-requested -> address-received
      -> owner-authorized -> boc-signed -> offer-delivered
      -> finalized-paid | expired-unpaid | invalidated-unpaid | finality-unknown
```

Recipient lifecycle:

```text
address-request-observed -> address-response-sent -> signed-offer-observed
                         -> verified -> broadcast-submitted
                         -> finalized-paid | expired-unpaid
                          | invalidated-unpaid | finality-unknown
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

After execution, observers may see A's Gift wallet, B's destination, exact
amount, timing, sequence, validity window, funding history, reuse, and later
consolidation. Fresh wallets reduce simple linkage but do not provide anonymity.
V1 claims neither amount confidentiality nor transaction anonymity.

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
  finalized sender-wallet execution reference
  finalized destination-credit reference
  optional owner authorization record
}
```

It proves conversation provenance, B's returned address, A's wallet signature,
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
- wrong network, wallet identity, code, sequence, validity, or signature fails;
- multiple actions, hidden data, plugin mutation, deployment, StateInit,
  unknown action, memo, comment, tag, or payload fail;
- wrong amount, destination, mode, bounce policy, or fee behavior fails;
- insufficient balance plus fee reserve is not executable;
- duplicate delivery and node submission create at most one payment;
- changed bytes under one `SignedGiftID` fail;
- local time alone cannot produce `expired-unpaid`;
- cancellation races remain nonterminal until finalized resolution;
- ambiguous submission resolves finalized state before replacement or terminal
  reporting;
- crash recovery returns the same BOC and does not sign twice;
- node and chat acknowledgements cannot mark payment;
- external services cannot authorize spending; and
- diagnostics exclude prohibited data.

Every object is bounded, versioned, canonically encoded, domain-separated where
hashed, and rejects unknown fields unless a frozen compatibility rule permits
them.

## 14. Repository ownership

| Repository | Responsibilities |
|---|---|
| `tos-service-spec` | This profile, canonical objects, BOC profile, vectors, negative corpus, and acceptance evidence |
| `tos` | Standard-wallet and native TOS semantics; no Gift contract is added |
| `tosctl` | Gift-wallet custody, exact BOC construction/signing, verification, and raw-byte broadcast |
| `tos-service-protocol` | Canonical Gift types, wallet/BOC parser, finalized resolver, and adversarial vectors |
| `tos-messenger` | Authenticated E2EE address request/response and signed-offer carriage |
| `OpenFox` | Intent, owner-policy orchestration, durable state, and honest presentation |

`tos-service-gateway` and `tos-ai` are not required. Any Gateway projection is
non-authoritative and must not expose a standard Agent Gift graph.

## 15. Implementation sequence

### G0 — freeze profiles and vectors

- freeze request, response, offer, IDs, digests, and encodings;
- pin one wallet code/profile and exact signed-message/action encoding;
- freeze mode, bounce policy, fee reserve, and destination-credit predicate;
- publish positive and negative vectors;
- prove builder/parser equivalence in two implementations; and
- obtain wallet, Messenger, custody, privacy, and cross-repository review.

### G1 — read-only verification

- implement strict Gift and BOC parsing;
- implement finalized wallet execution and destination-credit resolution;
- implement observe-only OpenFox rendering;
- prove prohibited data does not reach model, diagnostics, Relay metadata, or
  push; and
- do not enable signing or broadcast.

### G2 — owner-authorized local Gifts

- implement one-active-Gift custody;
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
6. signs one exact single-action time-limited wallet BOC;
7. delivers only that immutable BOC through E2EE Messenger;
8. lets B independently verify and submit the exact bytes;
9. transfers the exact amount if A's wallet state still permits execution;
10. creates no Gift contract or Gift-specific chain payload;
11. reports payment only from finalized destination credit; and
12. honestly reports expiry, invalidation, insufficient funds, or unknown
    finality as unpaid or unresolved.

## 17. Non-negotiable invariants

1. **V1 has no Receiver Profile, Gift delegation, receive ticket, or ticket-signing key.**
2. **V1 supports native TOS only.**
3. **B's destination comes only from an authenticated direct E2EE response for the exact Gift intent.**
4. **A's owner policy and Gift wallet are the only spending authorities.**
5. **The exact signed BOC is payment authorization; chat text is not.**
6. **The BOC contains one native TOS transfer and no hidden action or payload.**
7. **B may submit but cannot redirect or modify payment.**
8. **Funds are not locked before execution, and the UI states this plainly.**
9. **Only finalized exact destination credit establishes payment.**
10. **Local time, submission, transaction hash, or chat acknowledgement is not terminal evidence.**
11. **One dedicated Gift wallet has at most one active signed Gift.**
12. **AgentIDs and aliases never enter the on-chain transfer payload.**
13. **Wallet, destination, BOC, sequence, fees, signature, and finality never come from model output.**
14. **Fees cannot reduce the signed Gift principal.**
15. **Exact BOC retries are idempotent; changed bytes are a conflict.**
16. **V1 does not claim guaranteed funding, destination-key ownership proof, anonymity, or amount confidentiality.**
17. **Gift support does not change the software-work commercial asset model.**
18. **Stablecoin, first-contact, room, guaranteed, group, and high-load Gifts require later profiles.**
