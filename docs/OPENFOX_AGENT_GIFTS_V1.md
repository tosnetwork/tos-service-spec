# OpenFox Direct Signed Agent Gifts V1

**Status:** incubation design; not implemented and not payment-acceptance evidence

**Privacy class:** E2EE-private before broadcast; relationship-minimizing on a transparent chain; amount confidentiality and transaction anonymity are not claimed

**Supported V1 assets:** native TOS and one deployment-allowlisted TOS-network stablecoin, one asset per Gift

**Related specifications:**

- [`OPENFOX_AUTONOMOUS_MESSENGER_ECONOMY_PLAN.md`](OPENFOX_AUTONOMOUS_MESSENGER_ECONOMY_PLAN.md)
- [`OPENFOX_ECONOMIC_BRIDGE_V1.md`](OPENFOX_ECONOMIC_BRIDGE_V1.md)
- [`AGENT_NATIVE_MESSENGER_V1.md`](AGENT_NATIVE_MESSENGER_V1.md)
- [`DNS_ALIAS_V1.md`](DNS_ALIAS_V1.md)
- [`SETTLEMENT.md`](SETTLEMENT.md)
- [`AUTH.md`](AUTH.md)

## 1. Product decision

OpenFox-to-OpenFox ordinary messaging, first contact, and private-room chat remain free. A Gift — presented to a user as a gift or red packet — is an optional, explicitly authorized economic action carried inside an existing end-to-end encrypted conversation.

V1 supports one narrow product:

> One sender Agent prepares one fixed-amount, time-limited, sender-wallet-signed external-message BOC that authorizes one exact transfer of either native TOS or one allowlisted TOS-network stablecoin to one recipient-controlled destination. The recipient receives the exact BOC over E2EE Messenger and may broadcast those unchanged bytes before expiry. Finalized destination credit, never chat text or a submission acknowledgement, determines whether the Gift was paid.

V1 deliberately creates **no per-Gift Vault, escrow contract, claim contract, refund contract, or on-chain Gift registry**.

The signed BOC is a time-limited digital cheque:

- the sender has authorized exact payment semantics;
- anyone holding the BOC may relay it, but cannot redirect its payment;
- funds are not locked when the BOC is sent;
- sender wallet state, balance, or sequence changes may invalidate it before broadcast;
- expiry leaves the funds in the sender-controlled wallet, so no refund transaction is needed; and
- only finalized transfer evidence establishes payment.

The UI MUST NOT describe an unbroadcast Signed Gift as “funded,” “locked,” “guaranteed,” “received,” or “already paid.”

V1 does not support one Gift containing multiple assets, group packets, random shares, first-come allocation, split claims, public Gift discovery, high-load parallel redemption, or unrestricted autonomous spending. A future guaranteed or group Gift profile may lock funds, but that is outside this document.

Allowing native TOS as a Gift asset does **not** make native TOS a provider-service price or settlement asset under the software-work commercial profile. A Gift is a non-purchase transfer and carries no Capability, Quote, execution, Receipt, or provider-settlement semantics.

`Gift` is the architectural term. “Red packet” is presentation metadata and has no separate identity, payment, or settlement semantics.

## 2. Why a signed BOC is the V1 primitive

OpenFox Messenger already provides authenticated E2EE delivery, durable retries, device identity, and replay-resistant application events. The payment primitive should add only what Messenger cannot provide: a sender-wallet authorization that a recipient can submit to TOS without learning a signing key.

A conforming Signed Gift BOC contains one standard wallet-signed external request whose immutable action list authorizes exactly one permitted transfer profile:

```text
NativeTOSGiftV1
or
TOSStablecoinGiftV1
```

Both profiles use the same outer sender-wallet signature, network binding, sequence, validity window, exact action count, and no-hidden-action rule. They differ only in the single internal action:

```text
NativeTOSGiftV1:
  sender Gift wallet
    -> exact native TOS internal transfer
    -> recipient destination owner wallet

TOSStablecoinGiftV1:
  sender Gift wallet
    -> exact internal call to sender stablecoin wallet
    -> standard stablecoin transfer
    -> recipient destination stablecoin wallet
```

The recipient cannot alter any signed bit, including:

- asset kind;
- native TOS or stablecoin identity;
- amount;
- destination;
- sender wallet;
- validity window;
- wallet sequence;
- action count;
- stablecoin transfer query identity where applicable;
- send mode, bounce policy, attached native value, response destination, or payload rules; or
- any other signed field.

If an attacker obtains the BOC, the attacker can at most relay it early. The exact transfer still pays the signed destination. This is materially different from a bearer secret that pays whoever presents it.

The design avoids a per-Gift contract and its public fingerprint. If the recipient never broadcasts the BOC, no Gift-specific chain object or transaction exists. If the recipient broadcasts it successfully, chain observers see an ordinary native TOS transfer or ordinary stablecoin transfer, not a dedicated Gift-vault lifecycle.

## 3. Asset model

### 3.1 Exactly one typed asset

Each Gift binds exactly one canonical asset union:

```text
GiftAssetV1 =
  NativeTOSAssetV1
  | TOSStablecoinAssetV1
```

A ticker such as `TOS`, `USD`, or `USDT` is display metadata and is never sufficient authority.

All amounts use unsigned canonical base-10 atomic-unit text:

```text
0 | [1-9][0-9]*
```

No sign, decimal point, exponent, whitespace, locale formatting, or leading zero is allowed. Human formatting is derived from verified decimals and never signed as authority.

### 3.2 Native TOS asset

```text
NativeTOSAssetV1 {
  network
  kind = native_tos
  atomic_unit = network-defined native TOS smallest unit
}
```

The network tuple identifies native TOS unambiguously. No master contract or ticker is accepted as a substitute.

For a native TOS Gift:

- the sender Gift wallet is the source of both the Gift amount and execution fees;
- the recipient destination is an exact recipient-controlled owner wallet;
- the one internal transfer carries exactly `amount_atomic` as recipient value;
- the selected send mode MUST pay execution and forwarding fees separately from the Gift amount;
- the message body, StateInit, comment, memo, Gift tag, and arbitrary payload are absent; and
- finalized recipient native TOS credit establishes payment.

The frozen native transfer profile must prove in the TVM emulator that the recipient receives exactly `amount_atomic`, while gas and forwarding costs are charged separately to the sender Gift wallet.

### 3.3 TOS-network stablecoin asset

```text
TOSStablecoinAssetV1 {
  network
  kind = tos_stablecoin
  master_account
  master_code_hash
  wallet_code_hash
  decimals
}
```

Every field is verified from finalized TOS state. The asset is not identified by ticker.

For a stablecoin Gift:

- the sender Gift wallet controls the exact derived sender stablecoin wallet;
- the recipient ticket binds an exact recipient owner wallet and exact derived recipient stablecoin wallet;
- both destination wallets are active and code-pinned before ticket issuance in V1;
- the signed action calls the exact sender stablecoin wallet with one canonical transfer body;
- the transfer amount equals `amount_atomic`;
- custom payload and forward payload are absent;
- forward native TOS amount, response destination, bounce behavior, attached value, and send mode are fixed by the frozen profile; and
- finalized recipient stablecoin-wallet credit under the exact master establishes payment.

### 3.4 No cross-asset substitution

Changing any of the following creates another Gift intent and invalidates the receive ticket:

- `native_tos` to `tos_stablecoin` or the reverse;
- stablecoin master, master code hash, wallet code hash, or decimals;
- amount;
- source wallet;
- destination wallet;
- transfer profile; or
- network.

A native TOS Gift MUST NOT be parsed as a stablecoin Gift with a missing master. A stablecoin Gift MUST NOT be represented as a native transfer plus a memo.

### 3.5 Separate policy and accounting buckets

Owner policy maintains distinct rolling limits for:

```text
native TOS Gift principal
stablecoin Gift principal per exact asset
native TOS fee reserve
```

Native TOS fees are never silently included in or deducted from a stablecoin Gift amount. For a native TOS Gift, the UI separately displays:

```text
Gift amount
estimated/max fee reserve
total sender-wallet balance required
```

## 4. Honest guarantees and limitations

### 4.1 Guaranteed by a valid signed BOC

Before broadcast, a recipient can verify that the BOC:

- was signed by the pinned sender wallet;
- is valid only on the intended TOS network;
- expires at the exact signed time;
- uses the exact expected wallet sequence;
- contains exactly one permitted action;
- selects exactly one supported Gift asset profile;
- names the exact amount and destination;
- contains no hidden second transfer, plugin/extension action, deployment, StateInit, comment, memo, or model-selected route;
- can be relayed without modifying or re-signing; and
- cannot execute twice under the accepted wallet replay rules.

For native TOS, the verifier proves exact recipient value and separate fee payment.

For a stablecoin, the verifier proves exact master, sender/recipient asset wallets, transfer body, amount, and no custom payload.

### 4.2 Not guaranteed before finalization

A Signed Gift is not pre-funded. Before successful execution:

- the sender may spend or move the relevant asset;
- a native TOS Gift wallet may no longer cover amount plus fees;
- a sender stablecoin wallet may no longer cover the stablecoin amount;
- the sender Gift wallet may lack native TOS fee reserve;
- another transaction may consume the signed wallet sequence;
- the sender may explicitly invalidate the pending Gift;
- the relevant wallet or asset contract may become unavailable or invalid under finalized state;
- the BOC may expire before inclusion; and
- submission may remain ambiguous until finalized state is resolved.

The recipient displays only honest states:

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

### 4.3 Cancellation semantics

V1 uses a dedicated sender Gift wallet so normal payments do not accidentally invalidate a pending Gift. A wallet has at most one active Signed Gift at a time, regardless of asset kind.

The sender may explicitly cancel an unredeemed Gift by consuming that wallet sequence through a separately owner-authorized standard-wallet action. Cancellation is not secret revocation: the recipient detects it from finalized wallet state and displays `invalidated-unpaid`.

A deployment that allows unrelated wallet actions while a Gift is active is non-conforming.

## 5. Privacy objective and honest limits

### 5.1 Protected by design

A conforming implementation minimizes disclosure:

- `.tos` aliases and AgentIDs exist only in E2EE and owner-private state;
- the exact signed BOC is delivered only inside E2EE application data;
- the chain receives no Gift-specific contract, Gift registry, Gift opcode, Gift memo, alias, greeting, room ID, conversation ID, EndpointID, DeviceID, or AgentID;
- native TOS transfers carry no Gift body, comment, tag, or StateInit;
- stablecoin transfers carry only the frozen ordinary transfer body and no Gift tag or model-controlled payload;
- the recipient may use a fresh active destination wallet for one Gift;
- the sender uses a dedicated Gift wallet rather than a publicly advertised Agent wallet where operationally possible;
- Relays, Gateways, push services, and model providers receive no custody keys;
- push notifications are content-free;
- public APIs do not expose “list Gifts by Agent” indexes; and
- either participant may selectively disclose an audit bundle without making the relationship public by default.

### 5.2 Not hidden

TOS and the supported assets are transparent. After execution, an observer may see or infer:

For native TOS:

- sender Gift wallet;
- recipient destination wallet;
- exact amount;
- transaction/message timing;
- wallet sequence and validity window;
- sender-wallet funding history; and
- destination reuse or later consolidation.

For a stablecoin:

- sender owner wallet and sender stablecoin wallet;
- recipient owner/stablecoin wallet;
- stablecoin master;
- exact amount;
- timing;
- wallet sequence and validity window;
- sender Gift-wallet/stablecoin funding history; and
- recipient wallet reuse or consolidation.

A reusable sender Gift wallet links its successful transfers. A reusable destination links incoming transfers. Fresh wallets reduce simple linkage but do not provide shielded anonymity, because activation, funding, and consolidation may reconnect the graph.

V1 is **E2EE-private before broadcast and relationship-minimizing after broadcast**, not amount-confidential, shielded, or anonymous.

### 5.3 Adversaries considered

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

It does not protect a party from compromise of its own wallet/custody process or endpoint. Sender and recipient necessarily know the counterparty.

## 6. Authority and custody boundaries

### 6.1 Identity

- Sender and recipient are canonical AgentIDs in private orchestration state.
- A `.tos` input is resolved once through the finalized alias path before preparation.
- Alias text is optional display metadata only.
- A later alias transfer cannot retarget a receive ticket, BOC, payment, policy record, or audit bundle.
- EndpointID, DeviceID, SessionID, Relay identity, room membership, and display name are not payment identities.
- Neither AgentID nor alias is placed in the signed wallet message or asset-transfer payload.

### 6.2 Funds and finality

- Native TOS payment is established only by finalized exact destination credit from the signed sender-wallet action.
- Stablecoin payment is established only by finalized exact recipient stablecoin-wallet credit under the signed transfer chain.
- Messenger delivery, ReadAck, ApplicationAck, node submission response, transaction hash, local projection, or model statement is not terminal payment evidence.
- The software-work Quote, escrow, Receipt, and settlement profiles are not reused. A Gift buys no Capability and proves no execution.
- Supporting native TOS Gifts does not change the commercial profile's rule that provider service prices use supported TOS-network stablecoins.

### 6.3 Owner authorization

Gift sending is disabled by default.

Signing requires an exact owner policy or owner-signed mandate binding at least:

- network;
- sender Gift wallet or approved wallet pool;
- exact typed Gift asset;
- recipient canonical AgentID or owner-approved allowlist digest;
- exact or maximum amount;
- exact validity-window bounds;
- Gift count and rolling cumulative amount per asset;
- maximum concurrent active Gifts;
- whether a fresh destination is required; and
- whether model-assisted intent parsing is allowed.

Owner confirmation binds the receive-ticket digest and exact unsigned transfer semantics, not a model summary or `.tos` string.

### 6.4 Custody

- `tosctl` or an equivalently hardened sender custody process chooses the Gift wallet, reads finalized sequence/state, builds the exact asset-specific action, signs the external message, and returns only the exact signed BOC plus non-secret verification metadata.
- OpenFox and `tos-messengerd` never receive sender chain private keys.
- Recipient custody chooses and controls the destination wallet(s) and signs the one-time receive ticket.
- The model never receives a wallet key, ticket-signing key, unsigned wallet action, signed BOC bytes, private destination metadata, or raw transaction body.
- The recipient broadcasts the exact signed bytes; it never rebuilds, edits, or re-signs them.

## 7. Receiver profile and one-time receive ticket

### 7.1 Finalized receiver profile

A sender resolves a finalized, network-bound receiver profile:

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

### 7.2 Ticket request

Sender custody chooses an active dedicated Gift wallet, reads finalized state, and creates fresh random 256-bit `gift_intent_id`.

OpenFox sends an E2EE request:

```text
GiftReceiveRequestV1 {
  network
  gift_intent_id
  sender_agent_id
  recipient_agent_id
  sender_gift_wallet
  sender_wallet_profile_digest
  sender_wallet_seqno
  asset
  amount_atomic
  valid_until
  payment_profile_digest
  optional_stablecoin_transfer_query_id
  receiver_profile_generation
}
```

`optional_stablecoin_transfer_query_id` MUST be present for a stablecoin Gift and MUST be absent for a native TOS Gift. The canonical union has distinct encodings; an omitted field cannot change asset kind.

The request is allowed only for:

- an existing approved contact;
- a recipient-issued one-time Gift invite; or
- an explicitly enabled and rate-limited first-contact Gift policy.

A public profile scrape alone is not enough to force a recipient to issue destination tickets.

### 7.3 Receive ticket

Recipient custody selects an asset-specific destination route.

For native TOS:

```text
NativeTOSDestinationV1 {
  active_destination_owner_wallet
  destination_wallet_code_hash
}
```

For a stablecoin:

```text
TOSStablecoinDestinationV1 {
  active_destination_owner_wallet
  destination_owner_wallet_code_hash
  derived_destination_stablecoin_wallet
  destination_stablecoin_wallet_code_hash
}
```

For the strongest privacy mode, custody creates and activates a fresh destination before ticket issuance. A reusable destination is permitted only when policy allows it and the UI warns that successful Gifts become publicly linkable.

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
  asset
  amount_atomic
  valid_until
  payment_profile_digest
  optional_stablecoin_transfer_query_id
  destination
  receiver_profile_generation
  ticket_not_after
}

ticket_body_digest =
  H(ticket-domain || canonical GiftReceiveTicketBodyV1)

ticket_signature =
  Sign(ticket-signature-domain || ticket_body_digest)
```

`ticket_id` is a fresh random 256-bit value generated outside the model.

The ticket body and signature are never published by default. Sender custody verifies the signature against the finalized receiver profile before owner authorization or signing.

### 7.4 Ticket lifecycle

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

One ticket is reserved for one exact intent and sender wallet sequence. Changing sender, recipient, wallet, sequence, asset, amount, expiry, payment profile, stablecoin transfer query, or destination invalidates it.

A ticket may be released after timeout only after finalized checks show that no successful transfer matching it occurred. Ambiguous state remains reserved until resolved.

## 8. Signed Gift BOC profile

### 8.1 Approved sender wallet

V1 uses one pinned standard sender-wallet code hash and canonical signed-external-message profile. It MUST provide:

- TOS network/global-ID anti-replay binding;
- exact wallet/subwallet identity;
- signed `valid_until`;
- strict sequence replay protection;
- a signed, bounded action list; and
- deterministic parsing sufficient to reject hidden actions.

The first implementation candidate is the TOS Wallet V5 signed-external profile. G0 freezes the exact code hash, external-message encoding, action encoding, and vectors. Supporting multiple sender-wallet versions under one V1 identifier is prohibited.

The sender wallet MUST already be active in finalized state. V1 does not combine wallet deployment and Gift execution in one BOC.

### 8.2 Dedicated sender Gift wallet

A conforming deployment uses a dedicated sender Gift wallet or bounded pool.

For each wallet:

- at most one Signed Gift is active, regardless of asset;
- no unrelated payment or plugin/extension mutation is allowed while active;
- sufficient native TOS fee reserve is maintained;
- any stablecoin source wallet is derived and verified;
- current sequence and relevant balances are resolved before signing; and
- exact retry returns the same durable signed BOC.

High-load/query-ID wallets and parallel outstanding Gifts are later profiles.

### 8.3 Common outer action rule

The signed external request contains exactly one permitted wallet send action, no extra references, no trailing data, and no action-list ambiguity.

The action MUST match exactly one of the following profiles.

### 8.4 Native TOS action profile

The single action sends one ordinary internal message directly to the ticket-approved active destination owner wallet.

It binds:

```text
destination_owner_wallet
amount_atomic
bounce_policy
send_mode
message_value
body_absent
state_init_absent
```

The frozen profile requires:

- `message_value == amount_atomic`;
- fees are paid separately by the sender Gift wallet;
- body is empty;
- StateInit is absent;
- no comment, memo, Gift tag, AgentID, alias, or forward payload exists;
- send mode and bounce policy are fixed, not caller-selected; and
- emulator vectors prove exact recipient credit.

A native TOS action addressed to a stablecoin wallet, contract supplied by the model, or non-ticket destination is rejected.

### 8.5 Stablecoin action profile

The single action sends one internal message to the exact sender stablecoin wallet derived from the approved master and sender Gift wallet.

The canonical stablecoin transfer body binds:

```text
transfer_query_id
amount_atomic
destination_owner_wallet
response_destination
custom_payload_absent
forward_tos_amount
forward_payload_absent
```

The frozen profile fixes:

- exact sender stablecoin wallet;
- exact recipient stablecoin wallet derivation;
- standard transfer constructor;
- attached native value;
- bounce flags;
- send mode;
- response destination;
- forward native TOS amount; and
- empty custom/forward payload rules.

### 8.6 Common refusals

V1 rejects:

- more than one action;
- action kind inconsistent with the typed asset;
- plugin/extension install or removal;
- contract deployment;
- arbitrary code/data StateInit;
- unknown action constructors;
- comments, memos, aliases, AgentIDs, room IDs, or Gift tags;
- custom or forward payload;
- caller-selected send modes outside the selected profile;
- a destination or amount not matching the receive ticket; and
- a BOC whose asset-specific semantics cannot be fully reconstructed.

### 8.7 Signed Gift identity

After signing:

```text
SignedGiftID =
  H(signed-gift-domain || exact_signed_boc_bytes)
```

Only the exact signed BOC bytes may be broadcast.

SignedGiftID is owner-private/Messenger correlation data. It is not inserted into a native TOS message, stablecoin body, or chain object.

The sender journal binds:

```text
gift_intent_id
ticket_body_digest
asset
unsigned_transfer_digest
exact_signed_boc_digest
SignedGiftID
```

Reusing one `gift_intent_id` with changed semantics is a conflict. Exact retry returns the same BOC.

## 9. Recipient verification and broadcast

Before presenting a Gift as currently executable, recipient custody verifies:

### 9.1 Common checks

1. E2EE Event sender is the ticket's canonical sender AgentID.
2. Local recipient is the ticket's canonical recipient AgentID.
3. Receiver profile and ticket signature are finalized, live, and network-correct.
4. Exact BOC digest and SignedGiftID are canonical.
5. BOC uses the approved sender-wallet code/profile and signed-external constructor.
6. Network/global ID, wallet ID, sender wallet address, and code hash match.
7. Signed sequence equals the ticket and latest finalized sender-wallet sequence.
8. `valid_until` equals the ticket, is in bounds, and has sufficient inclusion margin.
9. Signature over the exact wallet request is valid.
10. There is exactly one permitted send action and no hidden refs or trailing data.
11. Typed asset, amount, payment profile, and destination match the ticket.
12. Sender Gift wallet has required native TOS fee reserve.
13. No finalized destination credit matching this Signed Gift already exists.

### 9.2 Native TOS checks

14. Action destination equals the ticket's active destination owner wallet.
15. Internal message value equals exact `amount_atomic`.
16. Send mode pays fees separately from the Gift amount.
17. Body and StateInit are absent.
18. Finalized sender Gift wallet native balance is at least Gift amount plus frozen fee reserve.

### 9.3 Stablecoin checks

14. Action targets the exact derived sender stablecoin wallet.
15. Transfer body matches exact asset, amount, query ID, destination, response address, gas, and empty-payload rules.
16. Recipient stablecoin wallet derives exactly from the ticket destination and approved code.
17. Finalized sender stablecoin balance covers the amount.
18. Finalized sender Gift wallet native TOS balance covers the frozen execution/forward fee reserve.

A current sequence and balance check is a readiness observation, not a guarantee that state remains unchanged before inclusion.

To redeem, recipient custody submits the exact original BOC to one or more configured TOS nodes. It never reconstructs a wallet request.

Repeated submission of the same BOC is permitted while finality is unresolved. The wallet sequence rule permits at most one successful execution. A submission error or transaction hash does not establish payment.

`finalized-paid` requires:

```text
native_tos:
  finalized exact native TOS destination credit

tos_stablecoin:
  finalized exact recipient stablecoin-wallet credit
```

Both must link to the exact signed sender-wallet execution under the selected resolver.

## 10. Durable lifecycle and recovery

### 10.1 Sender lifecycle

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

The sender never signs a replacement BOC for the same intent while the original may still execute. It resolves finalized wallet sequence, relevant asset balances, destination credit, and transaction history before deciding that a BOC is expired or invalidated.

### 10.2 Recipient lifecycle

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

Restart resumes from exact BOC bytes and digests. Payment is never inferred from chat acknowledgement, local send result, or mempool observation.

### 10.3 Expiry and cancellation

Expiry requires no refund because funds never left the sender-controlled wallet.

Explicit sender cancellation consumes or invalidates the dedicated wallet sequence under owner authorization. The recipient detects this from finalized state. Cancellation cannot transform the BOC into another payment.

If a BOC expires or is invalidated, the destination ticket is not immediately reusable. Recipient custody first completes the frozen absence/nonpayment reconciliation rules for the selected asset.

## 11. Messenger privacy profile

### 11.1 Inner typed payloads

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
  asset_display_hint
  exact_signed_boc
  optional_display_message
  padding
}
```

`asset_display_hint` is non-authoritative. The receiver derives asset and amount from the verified BOC and ticket.

The exact BOC and ticket are never exposed to a Relay, push provider, Gateway, model provider, or public status API.

### 11.2 Padding and push

Receive request, ticket, and signed-offer payloads use a frozen small set of ciphertext padding buckets. Padding is generated by the Messenger boundary, not the model.

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

### 11.3 Status

The normal status path is finalized-state polling by a participant already holding the private record. An optional encrypted refresh hint may prompt polling but carries no terminal authority.

DeliveryAck, ReadAck, ApplicationAck, and TOS commercial Receipt are not Gift-payment evidence. A recipient may broadcast and receive funds without sending a chat acknowledgement.

### 11.4 Direct and room carriage

Direct E2EE conversation is the default.

A private room may carry a signed offer only when:

- the private ticket names exactly one recipient;
- only that recipient receives or can decrypt the BOC payload; and
- the UI makes any room-visible social disclosure explicit.

Room membership never grants redemption authority. A room-wide copy of the exact BOC would let other members trigger early broadcast, even though they could not redirect payment, and is prohibited by default.

## 12. OpenFox behavior and model boundary

OpenFox exposes narrow typed actions:

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

The model may propose recipient, typed asset, amount, expiry, and greeting. It cannot provide or alter:

- canonical AgentID after resolution;
- sender Gift wallet;
- wallet code or sequence;
- receive ticket or ticket signature;
- destination wallet;
- stablecoin wallet derivation;
- asset identity after verification;
- payment profile;
- stablecoin transfer query ID;
- unsigned wallet request;
- signed BOC;
- send mode, bounce, attached value, or gas fields;
- finality evidence;
- transaction bytes; or
- wallet signature.

A privacy-sensitive deployment SHOULD parse structured Gift commands locally or through an owner UI. If model-assisted intent parsing is enabled, the operator must be warned that the model provider learns submitted recipient text, asset, amount, expiry, and greeting.

Owner confirmation independently renders:

- canonical recipient AgentID and optional alias;
- exact network;
- exact asset kind and, for a stablecoin, full contract identity;
- exact atomic and human-formatted amount;
- destination privacy mode;
- sender Gift wallet and current sequence;
- `valid_until`;
- ticket-body and unsigned-transfer digests;
- rolling budget/count effect for this exact asset;
- fee reserve separately from Gift principal;
- the fact that funds are **not locked**;
- the ways the BOC may become invalid; and
- transparent-chain leakage after successful broadcast.

The BOC itself and custody material are never model input.

## 13. Local data, logs, and telemetry

General logs MUST NOT contain:

- raw receive tickets;
- exact signed BOC bytes;
- aliases;
- full AgentIDs;
- destination wallet addresses;
- Gift amount;
- private display message; or
- owner authorization material.

Operational logs may use per-installation salted labels and bounded error codes. Typed errors must not dump canonical bodies, refs, signatures, or BOCs.

Metrics may expose only aggregate counts:

```text
gift_prepare_total
gift_signed_total
gift_broadcast_total
gift_finalized_total
gift_expired_total
gift_invalidated_total
gift_verification_failure_total
```

Metrics must not use public AgentID, wallet, SignedGiftID, alias, asset, or amount labels.

Crash dumps, traces, analytics exports, support bundles, and backups are part of the privacy boundary. Analytics is opt-in and documents exact fields, retention, and deletion. Owner-private records are encrypted at rest by owner-held recovery material where supported.

Deleting local UI history does not erase finalized chain transactions, and the UI must not imply otherwise.

## 14. Selective-disclosure audit

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
  asset-specific finalized transfer references
  finalized destination-credit reference
  optional local display record
}
```

An auditor can verify:

- alias-to-Agent resolution at preparation time where disclosed;
- receiver profile and ticket authority;
- BOC signature and exact asset-specific semantics;
- sender wallet sequence and validity;
- amount and destination;
- broadcast/finalization outcome; and
- whether payment occurred once.

Selective disclosure irreversibly reveals relationship information to the audit recipient and requires explicit owner decision.

No standard public API may provide:

```text
list Gifts by sender AgentID
list Gifts by recipient AgentID
list Gifts by alias
public Gift feed
Gift leaderboard
public social-payment graph
```

## 15. Threat model and required refusal cases

Implementations must test at least:

### 15.1 Common refusals

- `.tos` reassignment after preparation does not change canonical recipient AgentID;
- wrong network/global ID, wallet ID, wallet code, or wallet address fails;
- expired, zero, excessive, or policy-invalid validity windows fail;
- stale, future, substituted, or already-consumed wallet sequence fails;
- invalid wallet signature fails;
- multiple actions or hidden refs fail;
- plugin/extension mutation, deployment, StateInit, unknown action, comment, memo, or Gift tag fails;
- typed asset/action mismatch fails;
- wrong amount, destination, mode, bounce, attached value, or payload fails;
- model-selected wallet, sequence, destination, BOC, or transaction is unrepresentable or rejected;
- ticket or destination substitution fails;
- exact BOC replay creates at most one successful transfer;
- changed BOC bytes under the same SignedGiftID fail;
- broadcast after expiry fails without moving funds;
- unrelated sender-wallet use while active is prevented;
- explicit cancellation invalidates but cannot redirect payment;
- duplicate/multi-Relay delivery does not create a second signature or payment;
- local journal rollback or cross-network replay fails closed;
- node acknowledgement cannot mark payment;
- ambiguous submission resolves finalized state before retry;
- external model, Gateway, Relay, or push provider cannot authorize signing; and
- logs, metrics, and support bundles do not expose prohibited data.

### 15.2 Native TOS refusals

- a native action with any body or StateInit fails;
- a native action whose recipient receives less than exact Gift principal fails;
- a send mode that deducts fees from Gift principal fails;
- destination is not the ticket-approved active owner wallet fails;
- native balance below Gift amount plus fee reserve is not executable; and
- a native TOS action masquerading as a stablecoin Gift fails.

### 15.3 Stablecoin refusals

- wrong master, master code hash, wallet code hash, or decimals fails;
- wrong sender stablecoin wallet or destination stablecoin derivation fails;
- wrong transfer constructor or query ID fails;
- custom/forward payload or unapproved forward amount fails;
- stablecoin balance below amount is not executable;
- native fee reserve below frozen requirement is not executable; and
- a stablecoin transfer represented as a native TOS Gift fails.

Every typed object is bounded, versioned, domain-separated, and rejects unknown fields unless a frozen compatibility rule says otherwise.

## 16. Repository ownership

| Repository | Responsibilities |
|---|---|
| `tos-service-spec` | This profile, authority boundaries, typed asset union, canonical preimages, vectors, negative corpus, and acceptance evidence |
| `tos` | Existing standard-wallet, native TOS transfer, and stablecoin execution semantics; no per-Gift contract is added by V1 |
| `tosctl` | Sender Gift-wallet custody, receive-ticket custody helpers, exact asset-specific BOC construction/signing, strict verification, and raw-byte broadcast |
| `tos-service-protocol` | Canonical receiver profile/ticket/asset types, wallet/native/stablecoin resolvers, strict BOC parser/verifier, finalized payment resolver, and adversarial vectors |
| `tos-messenger` | Authenticated E2EE receive-request, receive-ticket, signed-offer, and refresh-hint carriage; generic outer classification and padding |
| `OpenFox` | User/model intent, owner-policy orchestration, durable non-authoritative state, honest presentation, and selective disclosure |

`tos-service-gateway` is not required. If it later indexes transfers, projections are non-authoritative and MUST NOT expose a standard Agent Gift graph.

`tos-ai` is not required because a Gift has no software execution or commercial Receipt.

## 17. Deferred profiles

V1 is one sender, one recipient, one fixed amount, one typed asset, one signed wallet BOC, and one standard-wallet sequence.

Separate versioned profiles are required for:

- multiple assets in one Gift;
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

A future guaranteed profile may use a locked-fund mechanism, but no per-Gift Vault is specified here.

Group Gifts must additionally define an immutable MLS membership snapshot, private eligibility proof, per-recipient replay protection, share bounds, remainder rules, and manipulation-resistant randomness. Relay order, local clock, model output, and block timestamp alone are not random allocation authority.

## 18. Implementation sequence

### G0 — profiles and vectors

- select and pin one sender-wallet code hash/profile;
- freeze receiver profile, typed asset union, and ticket encodings;
- freeze exact signed-external-message encoding;
- freeze native TOS internal-transfer profile;
- freeze stablecoin transfer profile;
- freeze send modes, bounce policy, fee reserves, attached values, response destination, and empty-payload rules;
- freeze SignedGiftID and domain separators;
- publish positive vectors for both assets;
- publish a cross-asset substitution and hidden-action negative corpus;
- prove BOC parser/build equivalence in two implementations; and
- obtain wallet, custody, privacy, and cross-repository security review.

### G1 — read-only verification

- implement strict profile/ticket/asset/BOC parsing;
- implement finalized sender wallet and native TOS destination-credit resolution;
- implement finalized sender/recipient stablecoin wallet resolution;
- implement OpenFox observe-only rendering against injected fixtures;
- prove no prohibited fields reach model, logs, metrics, Relay outer metadata, or push;
- do not enable signing or broadcast.

### G2 — owner-authorized local Signed Gifts

- implement dedicated Gift-wallet custody and one-active-Gift enforcement;
- implement recipient ticket custody and optional fresh active destinations;
- implement exact owner authorization and per-asset rolling controls;
- implement E2EE request/ticket/offer carriage;
- prove native TOS sign, delivery, broadcast, finalization, expiry, cancellation, insufficient funds, and restart;
- prove stablecoin sign, delivery, broadcast, finalization, expiry, cancellation, insufficient funds, and restart; and
- prove one asset cannot be substituted for the other.

### G3 — independent acceptance

- separate sender, recipient, resolver, Messenger, and validator operators;
- one fresh native TOS Signed Gift executes successfully;
- one fresh stablecoin Signed Gift executes successfully;
- one fresh Signed Gift expires without transfer;
- one fresh Signed Gift is explicitly invalidated;
- ambiguous submission and node failure are recovered from finalized state;
- an independent verifier reconstructs ticket, BOC, wallet sequence, exact asset transfer, and destination credit;
- privacy review confirms no AgentID/alias/Gift marker in chain payload or Relay-visible outer type; and
- configs, binaries, wallet/asset code hashes, vectors, checkpoints, and repository commits are published in a signed evidence bundle.

## 19. Acceptance criterion

V1 is complete only when an operator can say either:

```text
“Send 10 TOS to alice.tos as a time-limited Gift.”
```

or:

```text
“Send 10 tUSDT to alice.tos as a time-limited Gift.”
```

and the implementation:

1. resolves `alice.tos` once to a canonical AgentID;
2. selects one dedicated sender Gift wallet with no other active Gift;
3. resolves the exact typed asset;
4. obtains a recipient-signed one-time destination ticket over E2EE;
5. obtains exact owner authorization;
6. constructs and signs one exact time-limited standard-wallet BOC under the correct native or stablecoin profile;
7. delivers only that immutable BOC inside generic E2EE application data;
8. lets the recipient independently verify and broadcast the exact bytes;
9. transfers only the exact selected asset and amount to the ticket-approved destination if sender state still permits execution;
10. creates no per-Gift contract and no chain trace if never broadcast;
11. reports payment only from finalized asset-specific destination credit; and
12. honestly reports expiry, cancellation, sequence invalidation, or insufficient funds as unpaid.

Ordinary OpenFox messaging remains usable with Gift support disabled and with no wallet configured.

## 20. Non-negotiable invariants

1. **No per-Gift Vault, escrow, claim contract, refund contract, or Gift registry exists in V1.**
2. **The exact signed BOC is payment authorization; Messenger text is not.**
3. **Each Gift binds exactly one typed asset: native TOS or one exact allowlisted TOS-network stablecoin.**
4. **The BOC contains one permitted asset-specific transfer and no hidden action.**
5. **The recipient may relay but cannot redirect or modify payment.**
6. **Funds are not locked before execution, and the UI states this plainly.**
7. **Only finalized asset-specific destination credit establishes payment.**
8. **Expiry causes no refund because no transfer occurred.**
9. **One dedicated sender Gift wallet has at most one active Signed Gift.**
10. **AgentIDs and `.tos` aliases never enter the on-chain transfer payload.**
11. **The Relay-visible outer message class does not reveal Gift activity.**
12. **Wallet, destination, BOC, sequence, asset, gas, and signature authority never come from model output.**
13. **Native TOS principal and fees are distinct; fees cannot reduce the signed Gift amount.**
14. **Stablecoin identity is exact contract identity, never ticker text.**
15. **Exact BOC retries are idempotent; changed bytes are a conflict.**
16. **Transparent-chain leakage is disclosed honestly; V1 does not claim anonymity or amount confidentiality.**
17. **Supporting native TOS Gifts does not alter the software-work commercial asset model.**
18. **A later guaranteed, high-load, multi-asset, or group Gift profile cannot silently change V1 semantics.**
