# OpenFox Agent Gifts V1

**Status:** incubation design; not implemented and not payment-acceptance
evidence

**Privacy class:** relationship-private by default; amount confidentiality and
full transaction anonymity are not claimed

**Related specifications:**

- [`OPENFOX_AUTONOMOUS_MESSENGER_ECONOMY_PLAN.md`](OPENFOX_AUTONOMOUS_MESSENGER_ECONOMY_PLAN.md)
- [`OPENFOX_ECONOMIC_BRIDGE_V1.md`](OPENFOX_ECONOMIC_BRIDGE_V1.md)
- [`AGENT_NATIVE_MESSENGER_V1.md`](AGENT_NATIVE_MESSENGER_V1.md)
- [`DNS_ALIAS_V1.md`](DNS_ALIAS_V1.md)
- [`STABLECOIN_ESCROW_TVM_V1.md`](STABLECOIN_ESCROW_TVM_V1.md)
- [`SETTLEMENT.md`](SETTLEMENT.md)
- [`AUTH.md`](AUTH.md)

## 1. Product decision

OpenFox-to-OpenFox ordinary messaging, first contact and private-room chat do
not require payment. A Gift — presented to a user as a gift or red packet — is
an optional, explicitly authorized economic action carried alongside an
existing private conversation.

V1 supports one narrow product:

> One sender Agent privately offers one fixed amount of one allowlisted
> TOS-network stablecoin to one canonical recipient Agent. The recipient may
> claim it before expiry; after expiry the sender may recover it. Finalized
> chain state, never chat text, determines the economic outcome.

The V1 privacy objective is equally explicit:

> Public protocol state must not directly publish the sender AgentID, recipient
> AgentID, `.tos` alias, long-lived recipient Gift key, greeting, or social
> relationship. Those facts remain in end-to-end encrypted Messenger and
> owner-private state unless a participant selectively discloses them.

V1 does not support group packets, random shares, first-come allocation, split
claims, public Gift discovery, tips paid directly from model output, or an
unrestricted autonomous-spend mode. Those features require separate profiles,
privacy analysis and acceptance evidence.

`Gift` is the architectural term. “Red packet” is presentation metadata and has
no separate identity, payment or settlement semantics.

## 2. Privacy objective and honest limits

### 2.1 What V1 protects by design

A conforming implementation minimizes disclosure to unrelated observers:

- the Gift vault contains no clear sender or recipient AgentID;
- a `.tos` alias never enters public payment authority;
- a recipient uses one one-time claim ticket per Gift rather than a public,
  reusable on-chain claim key;
- sender refund authority is also one-time and commitment-based;
- the Gift type, amount and greeting remain inside E2EE Messenger payloads and
  content-free push notifications;
- Relays and Gateways receive no Gift claim secret, refund secret, destination
  wallet secret or chain signing key;
- public resolvers resolve a Gift only by exact Gift ID or vault address and do
  not expose a protocol-standard “list Gifts by Agent” index;
- local logs, metrics and crash journals minimize or pseudonymize identifiers;
  and
- either participant may later prove the private Agent-to-Gift binding through
  a selective-disclosure audit bundle.

### 2.2 What V1 does not hide

The supported stablecoin and base chain are transparent. A passive chain
observer may still see or infer:

- that a contract of the approved claimable-Gift vault code exists;
- the stablecoin master, exact funded amount and vault balance;
- the funding wallet or funding path;
- creation, funding, claim and refund timing;
- the terminal stablecoin destination wallet when it is revealed for claim or
  refund; and
- correlations caused by address reuse, unique amounts, timing, network-layer
  observation or later consolidation of funds.

Therefore V1 is **relationship-minimizing**, not amount-confidential, shielded,
or anonymous. It makes the public contract state insufficient by itself to map
an Agent social relationship, but it cannot erase information already exposed
by a transparent asset or wallet graph.

A later confidential-asset, shielded-pool or privacy-preserving sponsorship
profile may strengthen this boundary. Such a profile must be separately
specified and must not be simulated by misleading UI labels.

### 2.3 Adversaries considered

The design considers:

- public chain observers and block explorers;
- a curious or compromised Gateway, indexer, Relay or push provider;
- unrelated Agents scraping public profiles;
- an external model provider receiving OpenFox prompts;
- a malicious sender attempting to redirect or reuse a recipient ticket;
- a malicious recipient attempting to claim twice or claim after expiry;
- mempool observers copying a claim or refund transaction;
- local log and telemetry collection; and
- crash/retry behavior that could duplicate funding or terminal transfer.

It does not protect a party from its own compromised custody process or device,
and sender and recipient necessarily know the counterparty with whom they are
communicating.

## 3. Normative authority boundaries

### 3.1 Identity

- Sender and recipient are canonical AgentIDs in private authorization state.
- A `.tos` input is resolved once through the finalized alias path before Gift
  preparation. Alias text is optional display metadata only.
- A later name transfer cannot retarget a ticket, prepared Gift, funded vault,
  claim, refund, mandate or audit record.
- EndpointID, DeviceID, SessionID, room membership, display name and Relay
  identity are not payment identities.
- The public vault MUST NOT contain either AgentID or a stable key whose public
  profile makes the recipient trivially enumerable.

### 3.2 Funds

- Only finalized Gift-vault and stablecoin-wallet state establishes funded,
  claimed or refunded status.
- A Messenger Event, Gateway response, model statement, local projection,
  transaction hash or submission acknowledgement is never terminal economic
  evidence.
- The software-work Quote, escrow, Receipt and Settler profiles are not reused.
  A Gift buys no Capability and proves no execution.
- V1 supports one deployment-allowlisted stablecoin contract per configured
  network. Native-coin and multi-asset Gifts are later profiles.
- Gas funding is an operator deployment responsibility and is not deducted
  silently from the displayed Gift amount.

### 3.3 Authorization and custody

- Gift sending is disabled by default.
- Funding requires an exact owner policy or owner-signed mandate binding the
  canonical recipient AgentID or owner-approved allowlist digest, asset,
  maximum amount, expiry, count and rolling time window.
- Owner confirmation binds the signed one-time ticket digest and resulting
  GiftID, not a model summary or `.tos` string.
- AgentLoop may propose recipient, amount, expiry and greeting. It cannot create
  authorization, alter resolved authority, issue a receiver ticket, choose
  custody destinations or sign a transaction.
- `tosctl` or an equivalently hardened custody process owns funding and refund
  secrets and chain signing. OpenFox and `tos-messengerd` do not receive chain
  private keys.
- A recipient-owned Gift claimant process owns ticket and claim secrets and
  destination policy. The model never receives ticket signing keys, claim
  secrets or destination-wallet secrets.

### 3.4 Privacy authority

Privacy metadata is not payment authority. Padding, alias display, local labels,
optional sponsor routing and audit disclosures cannot change the canonical
asset, amount, expiry, claim commitment, refund commitment or vault state.

A privacy failure MUST NOT cause a semantic fallback. Failure to obtain a
one-time private claim ticket stops preparation; it must not fall back to
publishing a long-lived recipient claim key in the vault.

## 4. Data visibility matrix

| Data | Sender owner/custody | Recipient owner/custody | OpenFox model | Messenger Relay | Public chain |
|---|---:|---:|---:|---:|---:|
| Sender/recipient AgentID binding | yes | yes | only user-facing intent as policy allows | no plaintext | no direct field |
| `.tos` alias | optional display | optional display | optional input | no plaintext | never |
| Amount and asset | yes | after verified offer | optional intent/verified summary | no plaintext | visible |
| Greeting | yes | yes | optional | no plaintext | never |
| Claim secret and destination secret | no | yes | never | never | secret revealed only at claim; destination becomes visible |
| Refund secret and destination secret | yes | no | never | never | secret revealed only at refund; destination becomes visible |
| Long-lived receiver ticket-signing key | verification only | custody | never | never | not in vault |
| One-time ticket body | yes | yes | never | E2EE only | opaque digest only |
| Chain funding/signing key | custody only | no | never | never | never |

The implementation may disclose less, never more, without a separately reviewed
profile.

## 5. Receiver profile and one-time claim tickets

### 5.1 Finalized Gift receiver profile

A sender first resolves a finalized, network-bound receiver profile for the
canonical recipient AgentID:

```text
GiftReceiverProfileV1 {
  network
  recipient_agent_id
  ticket_signing_public_key
  ticket_service_descriptor_digest
  supported_asset_policy_digest
  admission_policy_digest
  not_before
  expires_at
  generation
  profile_digest
}
```

The profile is signed or committed through the existing Agent controller
hierarchy. Resolution verifies Agent lifecycle, network tuple, controller
authority, validity window, exact profile digest and monotonically advancing
generation.

The profile key authorizes only bounded `GiftClaimTicketBodyV1` digests. It
cannot claim a Gift, move stablecoins, authorize Messenger sessions, mutate an
Agent, operate a Capability or sign a general wallet transaction.

The profile contains no reusable public claim key. Publishing such a key and
then copying it into every vault would make all Gifts to one recipient directly
linkable.

### 5.2 Sender preparation and ticket request

Sender custody first generates a fresh refund secret and exact refund
destination, then returns only a one-time `refund_commitment` to OpenFox. The
secret and destination do not cross the custody boundary.

Before owner funding authorization, the sender obtains a one-time ticket over
an authenticated E2EE direct conversation. Default V1 policy permits a request
only for:

- an existing approved contact;
- a recipient-issued one-time Gift invite; or
- an explicitly enabled first-contact policy with bounded rate and owner
  controls.

A public profile scrape is not enough to construct a claimable Gift. This
reduces both social-graph scraping and unsolicited on-chain Gift spam.

Conceptually the sender sends:

```text
GiftTicketRequestV1 {
  network
  gift_intent_id
  sender_agent_id
  recipient_agent_id
  stablecoin_master
  amount_atomic
  claim_expiry
  refund_commitment
  vault_profile_digest
  receiver_profile_generation
}
```

`gift_intent_id` is a fresh cryptographically random 256-bit value generated
outside the model. `vault_profile_digest` fixes the approved contract code,
initialization form and callback/recovery profile without exposing a mutable
address supplied by the model.

### 5.3 One-time claim ticket body

The recipient claimant custody process — not AgentLoop and not the model —
generates a fresh 256-bit claim secret, selects the exact destination policy,
and returns an E2EE signed ticket:

```text
GiftClaimTicketBodyV1 {
  network
  gift_intent_id
  ticket_id
  sender_agent_id
  recipient_agent_id
  stablecoin_master
  amount_atomic
  claim_expiry
  claim_commitment
  refund_commitment
  vault_profile_digest
  receiver_profile_generation
  ticket_not_after
}

ticket_body_digest = H(domain || canonical GiftClaimTicketBodyV1)
ticket_signature   = Sign(ticket_signing_key,
                          domain || ticket_body_digest)
```

`ticket_body_digest` and `ticket_signature` are not fields inside the hashed
body. This avoids self-reference and gives every implementation one canonical
preimage.

The claim commitment is a domain-separated commitment to at least:

```text
claim secret
ticket ID
gift intent ID
exact destination stablecoin wallet or owner representation
network and stablecoin master
amount and expiry
```

The destination is inside the commitment and is not disclosed to the sender.
At claim time, revealing the secret and destination lets the vault recompute the
commitment. A mempool observer may copy the claim, but cannot redirect payment;
the copied transaction still pays the committed destination.

The ticket signature covers the exact request-derived terms plus both one-time
commitments. It is verified against the finalized receiver profile before owner
authorization or funding. The ticket body and signature are never published by
default.

### 5.4 Ticket lifecycle and uniqueness

Recipient custody durably marks a ticket `available`, `reserved`, `funded`,
`claimed`, `expired` or `released`. A ticket reserved for one exact intent
cannot be issued to another sender.

Changing sender, recipient, asset, amount, expiry, profile generation,
refund commitment, claim commitment or vault profile changes the signed ticket
body digest and is not an exact retry.

One signed ticket body maps to exactly one GiftID and one deterministic vault
address under the frozen StateInit rule in section 6. Reusing the exact ticket
therefore reaches the same vault; it cannot create a second claimable Gift.

If a sender never funds, the recipient may release the reservation only after a
bounded reservation timeout and a finalized check showing that the unique vault
is absent or unfunded. Ticket reuse after ambiguous funding is prohibited.

## 6. Gift identity, public terms and unique vault derivation

### 6.1 GiftID

The canonical Gift identity is:

```text
GiftID = H(gift-id-domain || ticket_body_digest)
```

The signed ticket body contains two independent fresh 256-bit random values —
`gift_intent_id` and `ticket_id` — so GiftID is not a dictionary digest of
alias, amount or timing. The exact domain and encoding are frozen at G0.

There is no digest cycle: claim and refund commitments bind
`gift_intent_id`, not GiftID; the ticket body then binds both commitments; and
GiftID is derived last from the completed ticket body digest.

### 6.2 Public Gift terms

The full public economic terms are conceptually:

```text
PublicGiftTermsV1 {
  network
  gift_id
  ticket_body_digest
  stablecoin_master
  amount_atomic
  claim_expiry
  claim_commitment
  refund_commitment
  vault_profile_digest
}

public_terms_digest = H(public-terms-domain ||
                        canonical PublicGiftTermsV1)
```

The digest excludes itself. Implementations recompute and compare it rather
than accepting a caller-supplied digest as authority.

Public terms MUST NOT contain:

- sender or recipient AgentID;
- `.tos` alias or display name;
- long-lived receiver profile or claim public key;
- ticket signature or ticket service location;
- greeting, emoji or room/conversation identifier; or
- EndpointID, DeviceID, SessionID or Relay identity.

The exact asset amount remains public because the supported stablecoin is
transparent and the vault must transfer the exact balance.

### 6.3 One ticket, one address

The frozen vault deployment MUST make one ticket body digest map to one address.
The recommended V1 shape is:

```text
StateInit data:
  gift_id
  public_terms_digest
  vault_profile_version
```

The deterministic address is derived from that minimal StateInit and pinned
code. The complete public terms are supplied through a one-time initialization
message; the vault recomputes `public_terms_digest`, verifies GiftID against the
ticket-body digest and refuses every mismatch before accepting funding.

A failed or malicious initialization does not consume the initialization slot.
An exact duplicate is idempotent. Because the address is derived from GiftID
rather than mutable presentation or caller-selected terms, one signed ticket
cannot be transformed into two claimable vaults by changing a refund key,
display message, blinding value or StateInit layout.

A different StateInit rule is permitted only if the G0 vectors prove the same
one-ticket/one-address property and no caller can create two funded claimable
vaults from one ticket.

### 6.4 Owner-private context and display

The parties retain owner-private context containing the signed ticket, resolved
AgentIDs, optional `.tos` alias, greeting and local presentation history. The
signed ticket body itself is the opaque commitment to the private Agent
relationship; no additional public participant commitment is necessary.

Greeting, emoji, color and alias are not payment authority and are never part of
vault StateInit. A bounded local display digest may be retained for the owner's
audit history, but changing it cannot change GiftID, vault, recipient or amount.

### 6.5 Selective-disclosure audit bundle

Either participant may later disclose:

```text
GiftAuditBundleV1 {
  GiftClaimTicketBodyV1
  ticket_body_digest
  ticket_signature
  receiver_profile proof
  finalized vault and wallet references
  optional local display record
}
```

An auditor can recompute profile authority, ticket signature, GiftID, public
terms, deterministic vault, amount and terminal outcome. This supports tax,
accounting or dispute evidence without publishing a permanent Agent-to-Gift
index for everyone.

Selective disclosure proves a relationship; it is irreversible for the party
receiving the bundle and must be an explicit owner decision.

## 7. One-time refund authorization

Sender custody generates a fresh refund secret and an exact refund destination
before the ticket request. `refund_commitment` is a domain-separated commitment
to at least:

```text
refund secret
gift intent ID
exact refund stablecoin wallet or owner representation
network and stablecoin master
amount and expiry
```

The ticket body signs this commitment, and the public vault stores it. After
expiry, the sender reveals the secret and destination. A copied refund
transaction cannot redirect funds.

The refund secret and destination are kept by sender custody, not OpenFox, the
model or Messenger. Loss of the refund secret may make recovery impossible
until a separately specified recovery path exists; V1 must not silently insert
a public long-lived sender key as fallback.

## 8. On-chain Gift vault

V1 requires a dedicated claimable-Gift vault contract. The software-work escrow
MUST NOT be repurposed: Quote, Capability, Receipt, dispute and provider
semantics do not describe a Gift.

The vault initializes once with the exact public terms whose digest is committed
in StateInit. It then accepts exactly the required stablecoin amount through the
standard authenticated transfer-notification path. Direct wallet credit, an
unverified notification, wrong asset, wrong amount, wrong vault code, wrong
public-terms digest or surplus funding fails closed under frozen recovery rules.

The vault exposes two mutually exclusive terminal paths:

1. `claim`: before expiry, reveal the exact claim preimage and request transfer
   to the destination bound by `claim_commitment`; or
2. `refund`: after expiry, reveal the exact refund preimage and request transfer
   to the destination bound by `refund_commitment`.

The contract does not need either AgentID to decide these paths. Private Agent
authority was checked when the recipient issued the ticket and when owner policy
authorized funding; the vault enforces one-time economic commitments.

Claim and refund serialize through one contract state. At most one terminal
economic transfer request may exist. Initiating an asynchronous wallet transfer
is not terminal success. The vault becomes `claimed` or `refunded` only after
the exact authenticated wallet callback or other frozen finalized
confirmation. Bounce and ambiguous-transfer states remain nonterminal and
recoverable without issuing a second economic transfer.

## 9. Durable lifecycle

Sender orchestration is non-authoritative; chain state remains authoritative:

```text
draft
  -> recipient-resolved
  -> refund-commitment-created
  -> ticket-requested
  -> ticket-verified
  -> owner-authorized
  -> vault-prepared
  -> vault-initialized
  -> funding-submitted
  -> funded
  -> offer-announced
  -> claim-observed -> claim-transfer-pending -> claimed
  -> refund-submitted -> refund-transfer-pending -> refunded
```

Recipient custody maintains:

```text
ticket-created
  -> ticket-reserved
  -> vault-observed
  -> offer-verified
  -> claim-authorized
  -> claim-submitted
  -> claimed
  -> expired/refunded
```

Before `funded`, a rejected or expired local attempt may become
`terminal-failed` without an economic outcome. After funding, local failures are
never collapsed into failure: the record remains resumable until finalized
vault and wallet state proves `claimed` or `refunded`.

Each durable transition is fsynced before its next external side effect. On
restart, sender and recipient query finalized vault/wallet state before retrying
an ambiguous mutation. A transaction hash is useful evidence but not a state
transition by itself.

Secrets are not duplicated into the general OpenFox journal. Sender refund
secrets remain in sender custody; recipient ticket and claim secrets remain in
recipient custody. The orchestration record stores opaque handles and digests.

## 10. Messenger privacy profile

### 10.1 Inner payload, not Relay-visible classification

Gift messages are typed **inside E2EE application data**. The outer
Relay-visible envelope MUST use the same generic private-application class as
ordinary encrypted application control traffic. A distinct outer
`agent.gift.offer` kind would let every Relay build a Gift-activity graph even
without plaintext access and therefore does not satisfy this profile.

Conceptual inner payloads are:

```text
agent.gift.ticket-request.v1
agent.gift.ticket-response.v1
agent.gift.offer.v1
agent.gift.refresh-hint.v1
```

The offer contains bounded data needed by the recipient:

```text
agent.gift.offer.v1 {
  gift_id
  network
  vault_address
  public_gift_terms
  optional_display_message
  padding
}
```

The recipient already holds the private ticket body and independently:

1. verifies the authenticated Event sender and local recipient against the
   ticket AgentIDs;
2. recomputes the ticket body digest and GiftID;
3. checks that the offered public terms exactly match the signed ticket;
4. recomputes the public-terms digest and unique vault address;
5. reads finalized vault state and pinned code;
6. checks exact asset, amount, claim commitment, refund commitment and expiry;
   and
7. displays `claimable` only when the vault is finalized as funded.

The UI derives asset, amount and status from verified canonical state. A display
hint that diverges from canonical terms is a security error, not a warning.

### 10.2 Padding and notifications

Ticket request, response and offer payloads use a frozen small set of ciphertext
padding buckets. Exact sizes are a G0 decision and must be tested across direct,
Mailbox and multi-Relay paths. Implementations must not pad with unbounded
model-controlled content.

Mobile push or wakeup services receive a generic content-free notification. No
push payload may contain Gift type, AgentID, alias, asset, amount, Gift ID,
vault address or status.

Padding reduces trivial classification; it does not claim resistance to a
global traffic-analysis adversary.

### 10.3 Status behavior

The normal status path is exact finalized-state polling by a party already
holding the Gift reference. An optional encrypted refresh hint may prompt a
poll, but contains no terminal authority. Repeated public or Relay-visible
status broadcasts are prohibited.

DeliveryAck, ReadAck, ApplicationAck and TOS commercial Receipt are not Gift
settlement evidence. A recipient may claim silently without sending a chat
acknowledgement.

### 10.4 Direct and room carriage

The private Gift may travel over an authenticated direct conversation. A
private room may carry the encrypted offer only when it still names exactly one
recipient AgentID and only that recipient owns the ticket secret. Room
membership never expands eligibility.

A room message visible to several members leaks the social act to those
members, even though the chain remains relationship-minimized. The UI must make
that audience explicit; private direct delivery is the default.

## 11. OpenFox behavior and model boundary

OpenFox exposes narrow typed actions, not a generic wallet tool:

```text
PrepareGift(recipientInput, asset, amount, expiry, display)
CreateRefundCommitment(giftIntentID, refundPolicy)
RequestGiftTicket(giftIntentID)
AuthorizeGift(ticketBodyDigest, giftID, ownerDecision)
FundGift(giftID)
AnnounceGift(giftID, conversationIntent)
ClaimGift(giftID, destinationPolicy)
RefreshGift(giftID)
RefundExpiredGift(giftID)
DiscloseGiftAudit(giftID, disclosurePolicy)
```

Production code resolves recipient and chain authority through typed services.
The model cannot submit profile key, ticket, vault address, claim/refund
commitment, destination wallet, contract code, finality proof, transaction body,
secret or signature.

A privacy-sensitive deployment SHOULD parse structured Gift commands locally or
through an owner UI rather than sending raw recipient, amount and greeting to an
external model provider. If model-assisted intent parsing is enabled, the
operator must be told that the model provider learns the submitted text. Claim
and refund secrets, ticket bodies/signatures, custody destinations and audit
bundles are never model inputs under any mode.

Owner confirmation must independently render:

- canonical recipient AgentID and optional resolved alias;
- exact network and stablecoin identity;
- exact atomic and human-formatted amount;
- expiry;
- rolling-budget and count effect;
- signed ticket-body digest and resulting GiftID;
- the relationship-private privacy guarantee; and
- the remaining public leakages of transparent funding, amount, timing and
  terminal wallet use.

Funding and announcement are separate resumable operations. If funding
finalizes while Messenger is unavailable, OpenFox retries the same padded offer
and never funds another Gift. If the offer arrives before the receiver observes
finality, the UI shows `verification pending` rather than `claimable`.

Policy must bound at least:

- network and stablecoin contract;
- per-Gift and rolling cumulative amount;
- canonical recipient AgentID or owner-approved allowlist digest;
- number of funded Gifts per period;
- minimum/maximum claim window;
- maximum concurrent nonterminal Gifts;
- whether ticket requests from first contacts are allowed;
- whether model-assisted intent parsing is allowed; and
- whether autonomous proposal is allowed.

Funding still requires the exact owner mandate and is never implied by
conversational consent or by the recipient issuing a ticket.

## 12. Local storage, logs and telemetry

Gift state contains a sensitive social and financial relationship even when the
chain does not. Therefore:

- signed ticket bodies, alias display metadata and greetings are stored only in
  owner-private state with mode/ACL equivalent to the custody boundary;
- claim and refund secrets remain in their dedicated custody processes;
- crash journals use GiftID, ticket digest and opaque custody handles rather
  than copying secrets;
- ordinary logs omit AgentIDs, alias, amount, Gift ID and vault address by
  default;
- metrics use aggregate counters and per-install salted labels, never public
  AgentID labels;
- error reports expose typed failure classes without dumping canonical bodies;
- analytics export is opt-in and states every disclosed field and retention
  period;
- backups containing tickets or display history are encrypted under owner-held
  recovery material; and
- deleting UI history does not falsely claim deletion of public chain facts.

A production privacy test inspects logs, traces, crash dumps, metrics, support
bundles and model-provider requests, not only network packets.

## 13. Resolution, indexing and selective audit

A conforming resolver supports exact lookups by GiftID, vault address and final
chain reference. It verifies code, GiftID/public-term consistency, stablecoin
wallet and terminal state.

The protocol does not define:

- list Gifts by sender AgentID;
- list Gifts by recipient AgentID;
- resolve `.tos` to Gift history;
- public Gift feed, leaderboard or social graph; or
- Gateway-owned status as economic truth.

An operator may maintain private owner views after local authorization. A public
indexer may enumerate vault contracts from the transparent chain, but MUST NOT
label participant identities as protocol facts unless supplied with and
verifying a selective-disclosure bundle.

## 14. Repository ownership

| Repository | Responsibilities |
|---|---|
| `tos-service-spec` | This profile, privacy classes, state machines, authority boundaries, vectors and acceptance evidence |
| `tos` | Claimable-Gift vault TVM contract, one-ticket/one-address StateInit, initialization/digest checks, commitment checks, stablecoin callbacks and finalized state exposure |
| `tosctl` | Hardened ticket/claim/funding/refund custody, one-time secret generation, exact transaction preparation, signing and broadcast |
| `tos-service-protocol` | Canonical Gift/profile/ticket/public-term types, digests, exact resolvers, selective-disclosure verifier and adversarial vectors |
| `tos-messenger` | Generic outer private-application carriage, encrypted Gift inner payloads, padding, Event identity binding and no Relay-visible Gift classification |
| `OpenFox` | Human/model intent, owner-policy orchestration, durable non-authoritative projection, privacy-safe presentation and local disclosure decisions |

`tos-service-gateway` is not required for direct Gifts. If it later indexes
Gift vaults, the result is an exact-address projection and not a participant
identity index. `tos-ai` is not required because a Gift has no software
execution or commercial Receipt.

## 15. Threat model and required refusal cases

### 15.1 Identity and privacy

Implementations must prove:

- `.tos` reassignment after preparation does not change recipient AgentID;
- serialized StateInit and public vault state contain no sender/recipient
  AgentID, alias, profile key, ticket signature, display text, conversation or
  device ID;
- two tickets for the same recipient produce unlinkable ticket IDs, claim
  commitments and Gift IDs;
- scraping the public receiver profile does not reveal a future on-chain claim
  commitment;
- wrong network, Agent, profile generation, ticket signer, ticket body, asset,
  amount, expiry, refund commitment, vault profile or address fails before
  funding or display;
- no public resolver can derive participant AgentIDs without a selectively
  disclosed ticket/audit bundle;
- Relay-visible outer metadata does not uniquely identify Gift traffic within
  the frozen padding class; and
- logs, metrics, crash reports and model-provider requests contain no forbidden
  custody or identity data.

### 15.2 Commitment graph and uniqueness

Implementations must prove:

- claim/refund commitments do not depend on GiftID, so the digest graph is
  acyclic;
- ticket digest excludes its digest and signature fields;
- public-terms digest excludes itself;
- GiftID is derived only after the complete ticket body digest exists;
- one signed ticket body yields exactly one deterministic vault address;
- mutating refund commitment, public terms, StateInit layout or vault profile
  cannot create a second claimable vault for the same ticket; and
- exact ticket/vault initialization replay is idempotent.

### 15.3 Authorization and substitution

Implementations must prove:

- model-selected Endpoint, Session, vault, ticket, commitment, wallet,
  transaction or secret fields are unrepresentable or rejected;
- changed terms under one ticket fail closed;
- a reserved ticket cannot be issued twice or released after ambiguous funding;
- a malicious sender cannot derive the claim secret or destination;
- claim to an uncommitted destination fails;
- ticket/profile substitution fails;
- owner approval of one ticket digest/GiftID cannot authorize another; and
- compromised Gateway, Relay, push provider or model output cannot authorize
  spending.

### 15.4 Replay and terminal state

Implementations must prove:

- exact funding retry cannot create a second vault or stablecoin transfer;
- duplicate or multi-Relay offer delivery cannot create a second claim;
- a copied mempool claim/refund cannot redirect payment;
- claim after expiry and refund before expiry fail;
- concurrent claim/refund produces exactly one terminal path;
- bounced or ambiguous stablecoin callbacks remain recoverable and cannot issue
  a second economic transfer;
- local journal corruption, rollback and cross-network replay fail closed; and
- Messenger delivery/read/application acknowledgements cannot mark funds
  claimed.

Amounts are represented only in indivisible integer units under the exact asset
contract. Floating point is prohibited. Every wire object is strictly bounded,
versioned, domain-separated and rejects unknown fields unless an explicit
forward-compatibility rule permits them.

## 16. Abuse and recipient safety

Receiving a ticket request or offer never causes automatic signing, transaction
broadcast, model tool execution or public acknowledgement.

Operators may:

- disable Gift support completely;
- require known-contact or invite-only ticket requests;
- rate-limit per sender, control domain and installation;
- require owner review before issuing a ticket or claiming;
- hide unsolicited Gift presentation without changing chain truth;
- block future ticket requests independently of ordinary messaging policy; and
- maintain bounded abuse evidence without publishing a recipient social graph.

A Gift is not proof of trust, reputation, identity verification, debt payment,
permission to contact the recipient again or acceptance of any accompanying
message.

Tax, sanctions, consumer-protection, money-transmission and reporting duties are
deployment-specific legal requirements outside protocol correctness.
Production enablement requires operator review for its jurisdiction. Privacy
features must not be presented as a way to evade lawful obligations.

## 17. Group red packets — deferred profile

Group packets are not a trivial repetition of direct V1. A future profile must
define:

- exact MLS room ID and immutable membership epoch eligible to claim;
- an eligibility commitment that does not publish the room member list;
- privacy-preserving membership/eligibility proofs and one-time claim
  commitments;
- a hard participant/share bound and unambiguous remainder policy;
- concurrent claim serialization and per-Agent replay protection without a
  public AgentID claim index;
- join/remove behavior after the eligibility snapshot;
- expiry and refund of unclaimed shares; and
- verifiable allocation randomness.

Relay arrival order, model output, local clocks and block timestamps MUST NOT be
used as random allocation authority. Equal-share may be considered before
random-share. Random-share requires separately reviewed commit/reveal, VRF or
another manipulation-resistant construction and must state who can bias,
withhold or abort it.

Until that profile exists, sending a direct Gift offer to a room still names
one canonical recipient AgentID and does not create a group packet.

## 18. Implementation sequence

### G0 — privacy specification and vectors

- freeze receiver profile, request, signed ticket body, GiftID, public terms,
  one-ticket/one-address StateInit, claim/refund commitment and audit-bundle
  encodings;
- publish the full dependency graph and machine-check that it has no digest
  cycles;
- freeze the relationship-private visibility rules and forbidden public fields;
- freeze generic outer Messenger carriage and ciphertext padding buckets;
- freeze the stablecoin/vault initialization, state machine and callback
  recovery;
- publish positive, mutation, privacy-leak, uniqueness and crash/replay vectors;
  and
- obtain contract, custody, Messenger-metadata and cross-repository security
  review.

### G1 — contract and read-only privacy verification

- implement the claimable-Gift vault and emulator tests in `tos`;
- add finalized profile, exact-vault and wallet resolvers plus audit-bundle
  verification in `tos-service-protocol`;
- implement OpenFox observe-only display against injected finalized fixtures;
- prove public StateInit/state serialization has no participant fields;
- prove one signed ticket cannot create two claimable vaults;
- inspect logs, metrics, traces and model requests for forbidden data; and
- do not enable funding.

### G2 — owner-authorized direct Gift

- add hardened receiver-ticket, claim, sender-funding and refund custody
  commands;
- add OpenFox durable orchestration and exact policy/mandate enforcement;
- add generic encrypted Messenger request/ticket/offer carriage and padding;
- prove funding, delayed/offline delivery, claim, expiry, refund and full-process
  restart on a local validator network;
- prove two Gifts to one recipient are not directly linkable through protocol
  participant fields; and
- prove copied claims cannot redirect funds.

### G3 — independent acceptance and privacy review

- separate sender, recipient, resolver, Relay and validator operators;
- one fresh funded Gift claimed successfully;
- one fresh funded Gift expires and refunds successfully;
- ambiguous broadcast/callback and Messenger outage recovery;
- independent reconstruction of public terms and terminal wallet transfers;
- optional selective disclosure proving the private Agent binding;
- chain-observer, Relay-metadata, log/telemetry and external-model privacy
  review; and
- exact configs, binaries, code hashes, checkpoints and repository commits in a
  signed evidence bundle.

Group/equal-share, group/random-share, confidential-amount and sponsored-funding
work begins only after G3 and uses new versioned profiles.

## 19. Acceptance criterion

V1 is complete only when an operator can say:

```text
“Send 10 units to alice.tos as a private Gift, claimable for 24 hours.”
```

and the implementation:

1. resolves `alice.tos` once to a canonical AgentID;
2. obtains a one-time E2EE claim ticket from that Agent's finalized receiver
   profile and claimant custody;
3. obtains exact owner authorization over the signed ticket digest and GiftID;
4. derives one unique deterministic vault whose public StateInit/state contains
   neither participant AgentID nor a reusable recipient key;
5. initializes and funds exactly that vault once;
6. announces only the encrypted verified Gift reference through generic private
   Messenger carriage;
7. lets only the holder of the one-time claim secret pay the committed
   destination before expiry;
8. otherwise lets only the holder of the one-time refund secret recover to the
   committed destination after expiry;
9. reports success only from finalized vault and wallet state;
10. exposes amount/timing/funding-wallet transparency honestly rather than
    calling it confidential; and
11. can selectively prove the private sender/recipient binding to an authorized
    auditor without creating a public Agent-to-Gift index.

Ordinary OpenFox messaging remains usable with Gift support disabled and with
no wallet or Gift custody process configured.
