# OpenFox Direct Signed Agent Gifts V1

**Status:** incubation design; not implemented and not payment-acceptance evidence

**Privacy class:** E2EE-private before broadcast; relationship-minimizing on a transparent chain; amount confidentiality and transaction anonymity are not claimed

**Related specifications:**

- [`OPENFOX_AUTONOMOUS_MESSENGER_ECONOMY_PLAN.md`](OPENFOX_AUTONOMOUS_MESSENGER_ECONOMY_PLAN.md)
- [`OPENFOX_ECONOMIC_BRIDGE_V1.md`](OPENFOX_ECONOMIC_BRIDGE_V1.md)
- [`AGENT_NATIVE_MESSENGER_V1.md`](AGENT_NATIVE_MESSENGER_V1.md)
- [`DNS_ALIAS_V1.md`](DNS_ALIAS_V1.md)
- [`SETTLEMENT.md`](SETTLEMENT.md)
- [`AUTH.md`](AUTH.md)

## 1. Product decision

OpenFox-to-OpenFox ordinary messaging, first contact and private-room chat remain free. A Gift — presented to a user as a gift or red packet — is an optional, explicitly authorized economic action carried inside an existing end-to-end encrypted conversation.

V1 supports one narrow product:

> One sender Agent prepares one fixed-amount, time-limited, sender-wallet-signed external-message BOC that authorizes one exact transfer of one allowlisted TOS-network stablecoin to one recipient-controlled destination. The recipient receives the exact BOC over E2EE Messenger and may broadcast those unchanged bytes before expiry. Finalized recipient-wallet credit, never chat text or submission acknowledgement, determines whether the Gift was paid.

V1 deliberately creates **no per-Gift Vault, escrow contract, claim contract, refund contract, or on-chain Gift registry**.

The signed BOC is best understood as a time-limited digital cheque:

- the sender has authorized exact payment semantics;
- anyone holding the BOC may relay it, but cannot redirect its payment;
- funds are not locked when the BOC is sent;
- sender wallet state, balance, or sequence changes may invalidate it before broadcast;
- expiry leaves the funds in the sender wallet, so no refund transaction is needed; and
- only finalized stablecoin transfer evidence establishes payment.

The UI MUST NOT describe an unbroadcast Signed Gift as “funded,” “locked,” “guaranteed,” “received,” or “already paid.”

V1 does not support group packets, random shares, first-come allocation, split claims, public Gift discovery, native-coin Gifts, multiple assets in one Gift, high-load parallel redemption, or unrestricted autonomous spending. A future guaranteed or group Gift profile may lock funds, but that is not part of this document.

`Gift` is the architectural term. “Red packet” is presentation metadata and has no separate identity, payment, or settlement semantics.

## 2. Why a signed BOC is the V1 primitive

OpenFox Messenger already provides authenticated E2EE delivery, durable retries, device identity, and replay-resistant application events. The payment primitive should therefore add only what Messenger cannot provide: a sender-wallet authorization that a recipient can submit to TOS without learning a signing key.

A conforming Signed Gift BOC contains a standard wallet-signed external request whose immutable actions authorize exactly one bounded stablecoin transfer. The signature covers the network, wallet identity, sequence, validity window, action list, stablecoin transfer body, destination, amount, and gas/send-mode fields.

The recipient cannot alter:

- stablecoin master or wallet;
- amount;
- destination owner or destination stablecoin wallet;
- sender wallet;
- validity window;
- wallet sequence;
- internal action count;
- transfer query identity;
- forward value or payload; or
- any other signed bit.

If an attacker obtains the BOC, the attacker can at most relay it early. The exact transfer still pays the signed destination. This is materially different from a bearer secret that pays whoever presents it.

The design avoids a per-Gift contract and its public fingerprint. If the recipient never broadcasts the BOC, no Gift-specific chain object or transaction exists. If the recipient broadcasts it successfully, chain observers see an ordinary stablecoin transfer rather than a dedicated Gift-vault lifecycle.

## 3. Honest guarantees and limitations

### 3.1 Guaranteed by a valid signed BOC

Before broadcast, a recipient can verify that the BOC:

- was signed by the pinned sender wallet;
- is valid only on the intended TOS network;
- expires at the exact signed time;
- uses the exact expected wallet sequence;
- contains exactly one permitted stablecoin-transfer action;
- names the exact stablecoin and amount;
- pays only the recipient-approved destination;
- contains no hidden second transfer, plugin action, deployment action, or model-selected route;
- can be relayed without modifying or re-signing; and
- cannot execute twice under the accepted wallet replay rules.

### 3.2 Not guaranteed before finalization

A Signed Gift is not pre-funded. Before successful execution:

- the sender may spend or move the stablecoin;
- the sender wallet may lack sufficient native TOS for gas;
- another transaction may consume the signed wallet sequence;
- the sender may explicitly invalidate the pending Gift;
- the sender or stablecoin wallet may become unavailable or invalid under finalized state;
- the BOC may expire before inclusion; and
- network submission may remain ambiguous until finalized state is resolved.

Therefore a recipient sees one of these honest states:

```text
signed
delivered
verification-pending
currently-executable
broadcast-submitted
finalized-paid
expired-unpaid
invalidated-unpaid
insufficient-funds
finality-unknown
```

No state before `finalized-paid` means that value has been received.

### 3.3 Cancellation semantics

V1 uses a dedicated sender Gift wallet so normal payments do not accidentally invalidate a pending Gift. The wallet has at most one active Signed Gift at a time.

The sender may explicitly cancel an unredeemed Gift by consuming that wallet sequence through a separately authorized standard wallet action. Cancellation is not secret revocation: the recipient detects it from finalized wallet sequence/state and displays `invalidated-unpaid`.

A deployment that allows unrelated transactions from the same sender Gift wallet while a Gift is active is non-conforming.

## 4. Privacy objective and honest limits

### 4.1 What V1 protects

A conforming implementation minimizes disclosure as follows:

- `.tos` aliases and AgentIDs exist only in E2EE and owner-private state;
- the exact signed BOC is delivered only inside E2EE application data;
- the chain receives no Gift-specific contract, Gift registry, Gift opcode, Gift memo, alias, greeting, room ID, conversation ID, EndpointID, DeviceID, or AgentID;
- the standard stablecoin transfer has no Gift tag or model-controlled forward payload;
- the recipient may use a fresh destination owner wallet and derived stablecoin wallet for one Gift;
- the sender uses a dedicated Gift wallet rather than a publicly advertised Agent wallet where operationally possible;
- Relays, Gateways, push services, and model providers receive no custody keys;
- push notifications are content-free;
- public APIs do not expose “list Gifts by Agent” indexes; and
- either participant may selectively disclose an audit bundle without making the relationship public by default.

### 4.2 What V1 does not hide

TOS and the selected stablecoin are transparent. Once the BOC executes, a chain observer may see or infer:

- sender wallet and sender stablecoin wallet;
- recipient owner/stablecoin wallet;
- stablecoin master;
- exact amount;
- transaction and message timing;
- wallet sequence and signed validity window;
- funding history of a dedicated Gift wallet;
- destination-wallet reuse;
- later consolidation of received funds; and
- network-layer or timing correlation.

A reusable sender Gift wallet links its successful transfers to one another. A reusable recipient destination links incoming transfers to one another. Fresh wallets reduce simple linkage but do not provide shielded anonymity, because funding and consolidation paths may reconnect the graph.

V1 is therefore **E2EE-private before broadcast and relationship-minimizing after broadcast**, not amount-confidential, shielded, or anonymous.

### 4.3 Adversaries considered

The design considers:

- curious or compromised Relays, Gateways, push providers, and indexers;
- public chain and mempool observers;
- an external model provider receiving user prompts;
- an attacker copying an encrypted payload after endpoint compromise;
- a malicious sender constructing hidden actions or misleading display text;
- a malicious recipient altering or replaying a BOC;
- crash/retry behavior causing duplicate signing or broadcast;
- local logs, traces, crash dumps, analytics, and support bundles; and
- alias reassignment after Gift preparation.

It does not protect a party from compromise of its own wallet/custody process or endpoint. Sender and recipient necessarily know the counterparty with whom they communicate.

## 5. Authority and custody boundaries

### 5.1 Identity

- Sender and recipient are canonical AgentIDs in private orchestration state.
- A `.tos` input is resolved once through the finalized alias path before preparation.
- Alias text is optional display metadata only.
- A later alias transfer cannot retarget a receive ticket, BOC, payment, policy record, or audit bundle.
- EndpointID, DeviceID, SessionID, Relay identity, room membership, and display name are not payment identities.
- Neither AgentID nor alias is placed in the signed wallet message or stablecoin-transfer payload.

### 5.2 Funds

- Only finalized sender-wallet/stablecoin-wallet and recipient-wallet transaction state determines whether payment occurred.
- Messenger delivery, ReadAck, ApplicationAck, node submission response, transaction hash, local projection, or model statement is not terminal payment evidence.
- The software-work Quote, escrow, Receipt, and settlement profiles are not reused. A Gift buys no Capability and proves no execution.
- V1 supports exactly one deployment-allowlisted TOS-network stablecoin master per configured network.
- Native TOS is used only for wallet and message fees and is not silently deducted from the displayed stablecoin amount.

### 5.3 Owner authorization

Gift sending is disabled by default.

Signing requires an exact owner policy or owner-signed mandate that binds at least:

- network;
- sender Gift wallet or approved wallet pool;
- stablecoin master;
- recipient canonical AgentID or owner-approved allowlist digest;
- exact or maximum amount;
- exact validity window bounds;
- Gift count and rolling cumulative amount;
- maximum concurrent active Gifts;
- whether a fresh recipient destination is required; and
- whether model-assisted intent parsing is allowed.

Owner confirmation binds the receive-ticket digest and exact unsigned transfer semantics, not a model summary or `.tos` string.

### 5.4 Custody

- `tosctl` or an equivalently hardened sender custody process chooses the Gift wallet, reads finalized sequence/state, builds the exact action, signs the external message, and returns only the exact signed BOC plus non-secret verification metadata.
- OpenFox and `tos-messengerd` never receive sender chain private keys.
- Recipient custody chooses and controls the destination wallet and signs the one-time receive ticket.
- The model never receives a wallet key, ticket-signing key, unsigned wallet action, signed BOC bytes, private destination metadata, or raw transaction body.
- The recipient broadcasts the exact signed bytes; it never rebuilds, edits, or re-signs them.

## 6. Receiver profile and one-time receive ticket

### 6.1 Finalized receiver profile

A sender resolves a finalized, network-bound receiver profile for the recipient AgentID:

```text
GiftReceiverProfileV1 {
  network
  recipient_agent_id
  ticket_signing_public_key
  supported_asset_policy_digest
  admission_policy_digest
  not_before
  expires_at
  generation
  profile_digest
}
```

The profile is authorized through the existing Agent controller hierarchy. Resolution verifies Agent lifecycle, network tuple, controller authority, validity window, exact profile digest, and monotonically advancing generation.

The ticket-signing key authorizes only bounded `GiftReceiveTicketBodyV1` digests. It cannot move funds, claim general wallet authority, authorize Messenger sessions, mutate an Agent, or operate a Capability.

### 6.2 Ticket request

Sender custody first chooses an active dedicated Gift wallet and reads its finalized state. It then creates a fresh cryptographically random 256-bit `gift_intent_id` and `transfer_query_id`.

OpenFox sends an E2EE request conceptually shaped as:

```text
GiftReceiveRequestV1 {
  network
  gift_intent_id
  sender_agent_id
  recipient_agent_id
  sender_gift_wallet
  sender_wallet_profile_digest
  sender_wallet_seqno
  stablecoin_master
  amount_atomic
  valid_until
  transfer_query_id
  transfer_profile_digest
  receiver_profile_generation
}
```

The request is allowed only for:

- an existing approved contact;
- a recipient-issued one-time Gift invite; or
- an explicitly enabled and rate-limited first-contact Gift policy.

A public profile scrape alone is not enough to force a recipient to issue destination tickets.

### 6.3 Receive ticket

Recipient custody chooses a destination owner wallet and verifies or derives the exact corresponding stablecoin wallet under the approved stablecoin master and code hashes.

For the strongest V1 privacy mode, custody creates a fresh destination for this Gift. A reusable destination is permitted only when policy allows it and the UI warns that successful Gifts become publicly linkable.

Recipient custody returns an E2EE ticket:

```text
GiftReceiveTicketBodyV1 {
  network
  gift_intent_id
  ticket_id
  sender_agent_id
  recipient_agent_id
  sender_gift_wallet
  sender_wallet_profile_digest
  sender_wallet_seqno
  stablecoin_master
  amount_atomic
  valid_until
  transfer_query_id
  transfer_profile_digest
  destination_owner_wallet
  destination_stablecoin_wallet
  receiver_profile_generation
  ticket_not_after
}

ticket_body_digest =
  H(ticket-domain || canonical GiftReceiveTicketBodyV1)

ticket_signature =
  Sign(ticket-signature-domain || ticket_body_digest)
```

`ticket_id` is a fresh random 256-bit value generated outside the model.

The ticket body and signature are never published by default. The sender verifies the signature against the finalized receiver profile before owner authorization or signing.

### 6.4 Ticket lifecycle

Recipient custody durably tracks:

```text
available
reserved
boc-observed
broadcast-submitted
finalized-paid
expired
invalidated
released
```

One ticket is reserved for one exact intent and sender wallet sequence. Changing sender, recipient, wallet, sequence, asset, amount, expiry, transfer query, transfer profile, or destination invalidates the ticket.

A ticket may be released after its timeout only after finalized checks show that no successful transfer matching the ticket occurred. Ambiguous state remains reserved until resolved.

## 7. Signed Gift BOC profile

### 7.1 Approved sender wallet profile

V1 uses one pinned standard sender-wallet code hash and canonical signed-external-message profile. The selected wallet profile MUST provide:

- TOS network/global-ID anti-replay binding;
- exact wallet/subwallet identity;
- a signed `valid_until`;
- strict sequence replay protection;
- a signed, bounded action list; and
- deterministic parsing sufficient to reject hidden actions.

The first implementation candidate is the TOS Wallet V5 signed-external profile. G0 must freeze the exact code hash, external-message encoding, action encoding, and vectors before implementation acceptance. Supporting multiple wallet versions under one V1 identifier is prohibited.

The sender wallet MUST already be active in finalized state. V1 does not combine wallet deployment and Gift execution in one BOC.

### 7.2 Dedicated sender Gift wallet

A conforming deployment uses a dedicated sender Gift wallet or a bounded pool of such wallets.

For each wallet:

- at most one Signed Gift is active;
- no unrelated payment or plugin/extension mutation is allowed while active;
- sufficient native TOS fee reserve is maintained;
- the exact stablecoin wallet is derived and verified;
- current sequence and balances are resolved before signing; and
- an exact retry returns the same durable signed BOC.

This restriction prevents ordinary wallet activity from silently consuming the Gift sequence. High-load/query-ID wallets and parallel outstanding Gifts are later profiles.

### 7.3 Exact action shape

The signed external message contains exactly one permitted wallet send action.

That action sends one internal message to the sender's exact stablecoin wallet. The stablecoin transfer body binds at least:

```text
transfer_query_id
amount_atomic
destination_owner_wallet
response_destination
custom_payload_absent
forward_tos_amount
forward_payload_absent
```

The exact sender stablecoin wallet, recipient stablecoin wallet derivation, message value, bounce flags, send mode, response destination, forward amount, and empty-payload rules are frozen by `transfer_profile_digest`.

V1 rejects:

- more than one action;
- native-coin value transfer to the recipient;
- plugin/extension install or removal;
- contract deployment;
- arbitrary code/data StateInit;
- unknown action constructors;
- custom or forward payload;
- comments, memos, aliases, AgentIDs, room IDs, or Gift tags;
- unbounded forwarding value;
- caller-selected send modes outside the profile; and
- a destination or amount not matching the receive ticket.

### 7.4 Canonical Signed Gift identity

After signing:

```text
SignedGiftID =
  H(signed-gift-domain || exact_signed_boc_bytes)
```

The exact signed BOC bytes are immutable. They are the only bytes that may be broadcast.

The SignedGiftID is an owner-private/Messenger correlation identifier. It is not inserted into the stablecoin transfer payload and is not a new chain object.

The sender journal binds:

```text
gift_intent_id
ticket_body_digest
unsigned_transfer_digest
exact_signed_boc_digest
SignedGiftID
```

Reusing one `gift_intent_id` with different semantics is a conflict. Retrying exact semantics returns the same BOC and cannot sign another sequence slot.

## 8. Recipient verification and broadcast

Before presenting a Gift as currently executable, recipient custody independently verifies all of the following:

1. E2EE Event sender is the ticket's canonical sender AgentID.
2. Local recipient is the ticket's canonical recipient AgentID.
3. Receiver profile and ticket signature are finalized, live, and network-correct.
4. Exact BOC digest and SignedGiftID are canonical.
5. BOC contains the approved wallet code/profile and signed-external constructor.
6. Network/global ID, wallet ID, sender wallet address, and code hash match.
7. Signed sequence equals the ticket and the latest finalized sender-wallet sequence.
8. `valid_until` equals the ticket, is in bounds, and has sufficient inclusion margin.
9. Signature over the exact wallet request is valid.
10. There is exactly one permitted send action and no hidden refs or trailing data.
11. The action targets the exact sender stablecoin wallet derived from the approved master and sender owner wallet.
12. Stablecoin transfer body is canonical and matches amount, query ID, destination, response address, gas, and empty-payload rules.
13. Recipient stablecoin wallet derives exactly from the ticket destination and approved code.
14. Finalized sender stablecoin balance is at least the transfer amount.
15. Sender wallet has the minimum native TOS fee reserve required by the frozen profile.
16. No finalized recipient credit matching this Signed Gift already exists.

A current sequence and balance check is a readiness observation, not a guarantee that state will remain unchanged before inclusion.

To redeem, recipient custody submits the exact original BOC to one or more configured TOS nodes. It does not reconstruct a wallet request.

Repeated submission of the same BOC is permitted while finality is unresolved. The wallet's sequence rule ensures at most one successful execution. A submission error or transaction hash does not establish payment.

`finalized-paid` requires independently verified finalized stablecoin credit to the exact destination, linked to the exact sender transfer and amount under the selected stablecoin resolver.

## 9. Durable lifecycle and recovery

### 9.1 Sender lifecycle

```text
draft
  -> recipient-resolved
  -> gift-wallet-selected
  -> ticket-requested
  -> ticket-verified
  -> owner-authorized
  -> boc-signed
  -> offer-delivered
  -> finalized-paid

boc-signed / offer-delivered
  -> expired-unpaid
  -> invalidated-unpaid
  -> finality-unknown
```

Each transition is fsynced before the next external side effect.

The sender never signs a replacement BOC for the same intent while the original may still execute. It resolves finalized wallet sequence, sender stablecoin balance, recipient credit, and transaction history before deciding that a BOC is expired or invalidated.

### 9.2 Recipient lifecycle

```text
ticket-created
  -> ticket-reserved
  -> signed-offer-observed
  -> verified
  -> broadcast-submitted
  -> finalized-paid

verified / broadcast-submitted
  -> expired-unpaid
  -> invalidated-unpaid
  -> finality-unknown
```

A process restart resumes from exact BOC bytes and digests. The recipient never marks payment from a chat acknowledgement, local send result, or mempool observation.

### 9.3 Cancellation and expiry

Expiry requires no refund path because funds never left the sender wallet.

Explicit sender cancellation consumes or otherwise invalidates the dedicated wallet sequence under owner authorization. The recipient detects this from finalized state. Cancellation cannot transform the BOC into another payment.

If a BOC expires or is invalidated, the destination ticket is not immediately reusable. Recipient custody first completes the frozen absence/nonpayment reconciliation rules.

## 10. Messenger privacy profile

### 10.1 Inner typed payloads

Gift messages are typed only inside E2EE application data. The Relay-visible outer envelope uses the same generic private-application class as other encrypted control traffic.

Conceptual inner payloads are:

```text
agent.gift.receive-request.v1
agent.gift.receive-ticket.v1
agent.gift.signed-offer.v1
agent.gift.refresh-hint.v1
```

The signed offer contains:

```text
SignedGiftOfferV1 {
  signed_gift_id
  ticket_body_digest
  exact_signed_boc
  optional_display_message
  padding
}
```

The exact BOC and ticket are never exposed to a Relay, push provider, Gateway, model provider, or public status API.

### 10.2 Padding and push

Receive request, ticket, and signed-offer payloads use a frozen small set of ciphertext padding buckets. Padding data is generated by the Messenger boundary, not the model.

Push notifications are content-free wakeups. They contain no:

- Gift type;
- alias or AgentID;
- asset or amount;
- SignedGiftID;
- BOC digest or bytes;
- wallet address;
- expiry; or
- payment status.

Padding reduces trivial classification but does not claim resistance to a global traffic-analysis adversary.

### 10.3 Status

The normal status path is finalized-state polling by a participant already holding the private record. An optional encrypted refresh hint may prompt polling but carries no terminal authority.

DeliveryAck, ReadAck, ApplicationAck, and TOS commercial Receipt are not Gift-payment evidence. A recipient may broadcast and receive funds without sending a chat acknowledgement.

### 10.4 Direct and room carriage

Direct E2EE conversation is the default.

A private room may carry a signed offer only when:

- the inner offer names exactly one recipient through the private ticket;
- only that recipient receives or can decrypt the BOC payload; and
- the UI makes any room-visible social disclosure explicit.

Ordinary room membership never grants redemption authority. A public or room-wide copy of the exact BOC would allow other members to trigger early broadcast, even though they could not redirect payment, and is therefore prohibited by default.

## 11. OpenFox behavior and model boundary

OpenFox exposes narrow typed actions rather than a generic wallet tool:

```text
PrepareGift(recipientInput, asset, amount, expiry, display)
SelectGiftWallet(giftIntentID)
RequestGiftReceiveTicket(giftIntentID)
AuthorizeGift(ticketBodyDigest, unsignedTransferDigest, ownerDecision)
SignGiftBOC(giftIntentID)
SendSignedGift(signedGiftID, conversationIntent)
VerifySignedGift(signedGiftID)
BroadcastSignedGift(signedGiftID)
RefreshSignedGift(signedGiftID)
CancelSignedGift(signedGiftID, ownerDecision)
DiscloseSignedGiftAudit(signedGiftID, disclosurePolicy)
```

The model may propose recipient, amount, expiry, and greeting. It cannot provide or alter:

- canonical AgentID after resolution;
- sender Gift wallet;
- wallet code or sequence;
- receive ticket or ticket signature;
- destination wallet;
- stablecoin wallet derivation;
- transfer query ID or transfer profile;
- unsigned wallet request;
- signed BOC;
- send mode or gas fields;
- finality evidence;
- transaction bytes; or
- wallet signature.

A privacy-sensitive deployment SHOULD parse structured Gift commands locally or through an owner UI. If model-assisted intent parsing is enabled, the operator must be warned that the model provider learns submitted recipient text, amount, expiry, and greeting.

Owner confirmation independently renders:

- canonical recipient AgentID and optional alias;
- exact network and stablecoin identity;
- exact atomic and human-formatted amount;
- destination privacy mode;
- sender Gift wallet and current sequence;
- `valid_until`;
- ticket-body and unsigned-transfer digests;
- rolling budget/count effect;
- the fact that funds are **not locked**;
- the ways the BOC may become invalid; and
- transparent-chain leakage after successful broadcast.

The BOC itself and custody material are never model input under any mode.

## 12. Local data, logs, and telemetry

General logs MUST NOT contain:

- raw receive tickets;
- exact signed BOC bytes;
- aliases;
- full AgentIDs;
- destination wallet addresses;
- stablecoin amount;
- private display message; or
- owner authorization material.

Operational logs may use per-installation salted labels and bounded error codes. Typed errors must not dump canonical bodies, refs, signatures, or BOCs.

Metrics may expose aggregate counts such as:

```text
gift_prepare_total
gift_signed_total
gift_broadcast_total
gift_finalized_total
gift_expired_total
gift_invalidated_total
gift_verification_failure_total
```

Metrics must not use public AgentID, wallet, SignedGiftID, alias, or amount labels.

Crash dumps, traces, analytics exports, support bundles, and backups are part of the privacy boundary. Analytics is opt-in and documents exact fields, retention, and deletion. Owner-private records are encrypted at rest by owner-held recovery material where the deployment supports it.

Deleting local UI history does not erase finalized chain transactions and the UI must not imply otherwise.

## 13. Selective-disclosure audit

Either participant may explicitly export:

```text
SignedGiftAuditBundleV1 {
  authenticated Messenger Event reference
  GiftReceiveTicketBodyV1
  ticket_body_digest
  ticket_signature
  exact_signed_boc
  SignedGiftID
  finalized sender-wallet reference
  finalized stablecoin transfer references
  finalized recipient-credit reference
  optional local display record
}
```

An auditor can verify:

- alias-to-Agent resolution at preparation time where disclosed;
- receiver profile and ticket authority;
- BOC signature and exact semantics;
- sender wallet sequence and validity;
- amount and destination;
- broadcast/finalization outcome; and
- whether payment occurred once.

Selective disclosure irreversibly reveals relationship information to the recipient of the bundle and requires an explicit owner decision.

No standard public API may provide:

```text
list Gifts by sender AgentID
list Gifts by recipient AgentID
list Gifts by alias
public Gift feed
Gift leaderboard
public social-payment graph
```

## 14. Threat model and required refusal cases

Implementations must test at least:

- `.tos` reassignment after preparation does not change canonical recipient AgentID;
- wrong network/global ID, wallet ID, wallet code, wallet address, or stablecoin master fails;
- expired, zero, excessive, or policy-invalid validity windows fail;
- stale, future, substituted, or already-consumed wallet sequence fails;
- invalid wallet signature fails;
- multiple actions or hidden refs fail;
- plugin/extension mutation, deployment, native transfer, or unknown action fails;
- wrong sender stablecoin wallet or destination wallet derivation fails;
- wrong asset, amount, query ID, response destination, gas, mode, or payload fails;
- a model-selected wallet, sequence, destination, BOC, or transaction is unrepresentable or rejected;
- ticket substitution or destination substitution fails;
- exact BOC replay creates at most one successful transfer;
- changed BOC bytes under the same SignedGiftID fail;
- recipient broadcast after expiry fails without moving funds;
- unrelated sender-wallet use while active is prevented;
- explicit cancellation invalidates but does not redirect payment;
- insufficient stablecoin or native fee reserve is displayed as not executable;
- duplicate/multi-Relay delivery does not create a second signature or second payment;
- local journal rollback or cross-network replay fails closed;
- node submission acknowledgement cannot mark payment;
- ambiguous submission resolves finalized state before retry;
- external model, Gateway, Relay, or push provider cannot authorize signing; and
- logs, metrics, and support bundles do not expose prohibited data.

All amounts use indivisible integer units under the exact stablecoin contract. Floating point is prohibited. Every typed object is bounded, versioned, domain-separated, and rejects unknown fields unless a frozen compatibility rule says otherwise.

## 15. Repository ownership

| Repository | Responsibilities |
|---|---|
| `tos-service-spec` | This profile, authority boundaries, canonical preimages, vectors, negative corpus, and acceptance evidence |
| `tos` | Existing wallet and stablecoin execution semantics; no per-Gift contract is added by V1 |
| `tosctl` | Sender Gift-wallet custody, receive-ticket custody helpers, exact BOC construction/signing, strict BOC verification, and raw-byte broadcast |
| `tos-service-protocol` | Canonical receiver profile/ticket types, wallet/stablecoin resolvers, strict BOC parser/verifier, finalized payment resolver, and adversarial vectors |
| `tos-messenger` | Authenticated E2EE receive-request, receive-ticket, signed-offer, and refresh-hint carriage; generic outer classification and padding |
| `OpenFox` | User/model intent, owner-policy orchestration, durable non-authoritative state, honest presentation, and selective disclosure |

`tos-service-gateway` is not required. If it later indexes wallet transfers, those projections are non-authoritative and MUST NOT expose a standard Agent Gift graph.

`tos-ai` is not required because a Gift has no software execution or commercial Receipt.

## 16. Group and guaranteed Gifts — deferred

V1 is one sender, one recipient, one fixed amount, one signed wallet BOC, and one standard wallet sequence.

The following require separate versioned profiles:

- multiple simultaneous Gifts from one wallet;
- high-load/query-ID wallet semantics;
- funds locked before recipient action;
- sender-noncancellable guaranteed Gifts;
- automatic expiry refund after locked funding;
- group/equal-share Gifts;
- group/random-share Gifts;
- first-come allocation;
- split claims; and
- confidential/shielded amounts.

A future guaranteed profile may use a locked-fund mechanism, but no such mechanism or per-Gift Vault is specified here.

Group Gifts must additionally define an immutable MLS membership snapshot, private eligibility proof, per-recipient replay protection, share bounds, remainder rules, and manipulation-resistant randomness. Relay order, local clock, model output, and block timestamp alone are not random allocation authority.

## 17. Implementation sequence

### G0 — profile and vectors

- select and pin one sender wallet code hash/profile;
- freeze receiver profile and ticket canonical encodings;
- freeze exact signed-external-message and stablecoin-transfer encodings;
- freeze send mode, gas, response destination, forward amount, and empty-payload rules;
- freeze SignedGiftID and all domain separators;
- publish positive vectors and a cross-implementation negative corpus;
- prove exact BOC parser/build equivalence in two implementations; and
- obtain wallet, custody, privacy, and cross-repository security review.

### G1 — read-only verification

- implement strict profile/ticket/BOC parsing;
- implement finalized sender wallet, stablecoin wallet, and recipient credit resolution;
- implement OpenFox observe-only rendering against injected fixtures;
- prove no prohibited fields reach model, logs, metrics, Relay outer metadata, or push;
- do not enable signing or broadcast.

### G2 — owner-authorized local Signed Gift

- implement dedicated Gift-wallet custody and one-active-Gift enforcement;
- implement recipient ticket custody and optional fresh destination creation;
- implement exact owner authorization and rolling budget/count controls;
- implement E2EE request/ticket/offer carriage;
- prove sign, delayed delivery, broadcast, finalization, expiry, cancellation, insufficient funds, sequence invalidation, and full-process restart on a local validator network.

### G3 — independent acceptance

- separate sender, recipient, resolver, Messenger, and validator operators;
- one fresh Signed Gift executes successfully;
- one fresh Signed Gift expires without any transfer;
- one fresh Signed Gift is explicitly invalidated;
- ambiguous submission and node failure are recovered from finalized state;
- an independent verifier reconstructs ticket, BOC, wallet sequence, exact transfer, and recipient credit;
- privacy review confirms no AgentID/alias/Gift marker in chain payload or Relay-visible outer type; and
- configs, binaries, wallet code hashes, vectors, checkpoints, and repository commits are published in a signed evidence bundle.

## 18. Acceptance criterion

V1 is complete only when an operator can say:

```text
“Send 10 units to alice.tos as a time-limited Gift.”
```

and the implementation:

1. resolves `alice.tos` once to a canonical AgentID;
2. selects one dedicated sender Gift wallet with no other active Gift;
3. obtains a recipient-signed one-time destination ticket over E2EE;
4. obtains exact owner authorization;
5. constructs and signs one exact time-limited standard-wallet BOC;
6. delivers only that immutable BOC inside generic E2EE application data;
7. lets the recipient independently verify and broadcast the exact bytes;
8. transfers only to the ticket-approved destination if sender wallet state still permits execution;
9. creates no per-Gift contract and no on-chain trace if never broadcast;
10. reports payment only from finalized recipient stablecoin credit; and
11. honestly reports expiry, cancellation, sequence invalidation, or insufficient funds as unpaid.

Ordinary OpenFox messaging remains usable with Gift support disabled and with no wallet configured.

## 19. Non-negotiable invariants

1. **No per-Gift Vault, escrow, claim contract, refund contract, or Gift registry exists in V1.**
2. **The exact signed BOC is the payment authorization; Messenger text is not.**
3. **The BOC contains one permitted stablecoin transfer and no hidden action.**
4. **The recipient may relay but cannot redirect or modify the payment.**
5. **Funds are not locked before execution, and the UI states this plainly.**
6. **Only finalized recipient stablecoin credit establishes payment.**
7. **Expiry causes no refund because no transfer occurred.**
8. **One dedicated sender Gift wallet has at most one active Signed Gift.**
9. **AgentIDs and `.tos` aliases never enter the on-chain transfer payload.**
10. **The outer Relay-visible message class does not reveal Gift activity.**
11. **Wallet, destination, BOC, sequence, gas, and signature authority never come from model output.**
12. **Exact BOC retries are idempotent; changed bytes are a conflict.**
13. **Transparent-chain leakage is disclosed honestly; V1 does not claim anonymity or amount confidentiality.**
14. **A later guaranteed or group Gift profile cannot silently change these semantics under the V1 identifier.**
