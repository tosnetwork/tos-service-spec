# OpenFox Agent Gifts V1

**Status:** incubation design; not implemented and not payment-acceptance
evidence

**Related specifications:**

- [`OPENFOX_AUTONOMOUS_MESSENGER_ECONOMY_PLAN.md`](OPENFOX_AUTONOMOUS_MESSENGER_ECONOMY_PLAN.md)
- [`OPENFOX_ECONOMIC_BRIDGE_V1.md`](OPENFOX_ECONOMIC_BRIDGE_V1.md)
- [`AGENT_NATIVE_MESSENGER_V1.md`](AGENT_NATIVE_MESSENGER_V1.md)
- [`STABLECOIN_ESCROW_TVM_V1.md`](STABLECOIN_ESCROW_TVM_V1.md)
- [`SETTLEMENT.md`](SETTLEMENT.md)
- [`AUTH.md`](AUTH.md)

## 1. Product decision

OpenFox-to-OpenFox ordinary messaging, first contact and private-room chat do
not require payment. A gift (the product presentation may call it a red packet)
is an optional, explicitly authorized economic action carried alongside chat.

V1 supports one narrowly defined product:

> One sender Agent offers one fixed amount of one allowlisted stablecoin to one
> canonical recipient Agent. The recipient may claim it before expiry; after
> expiry the sender may recover it. Finalized chain state, never chat text,
> determines the economic outcome.

V1 does not support group packets, random shares, first-come allocation,
split claims, tips paid directly from model output, or an unrestricted
autonomous-spend mode. Those features require separate profiles and acceptance
evidence.

The word `Gift` is used in protocol identifiers. “Red packet” is presentation
metadata and has no separate identity, payment or settlement semantics.

## 2. Why this is not an ordinary message

A chat Event can be retried, delayed, delivered through multiple Relays or
observed after a process restart. A stablecoin transfer cannot safely inherit
those delivery semantics. In particular:

- message delivery does not prove that funds were locked;
- a displayed amount does not prove the asset or amount on chain;
- retrying a send must not create a second funding transaction;
- receiving the same Event twice must not permit two claims;
- an expired offer must not race into both claim and refund;
- `.tos` reassignment must not change the recipient; and
- model output must not select a wallet, signing key or contract address.

Messenger therefore carries an authenticated reference and human-readable
display hint. The Gift contract and finalized wallet-transfer chain own money.

## 3. Normative authority boundaries

### 3.1 Identity

- The sender and recipient are canonical AgentIDs.
- A `.tos` input is resolved once through the normal finalized name path before
  gift preparation. Alias text may be retained only as display metadata.
- A later name transfer cannot retarget a prepared, funded, claimed or refunded
  Gift.
- Messaging EndpointID, DeviceID, SessionID and room membership are not payment
  identities.
- V1 uses a dedicated Gift claim key authorized for the recipient Agent. It
  does not reuse an Endpoint, Device, MLS or model-provider key.

### 3.2 Funds

- Only finalized Gift-vault and stablecoin-wallet state establishes funded,
  claimed or refunded status.
- A Messenger Event, Gateway response, model statement, local projection or
  transaction-submission result is never terminal economic evidence.
- The software-work Quote, escrow, Receipt and Settler profiles are not reused.
  A Gift buys no Capability and proves no execution.
- V1 supports one deployment-allowlisted stablecoin contract per configured
  network. Native-coin and multi-asset gifts are later profiles.
- Gas funding is an operator deployment responsibility and is not deducted
  silently from the displayed Gift amount.

### 3.3 Authorization and custody

- Gift sending is disabled by default.
- Funding requires an exact owner policy or owner-signed mandate binding the
  recipient AgentID, asset, maximum amount, expiry, count and time window.
- The AgentLoop may propose a recipient, amount and message. It cannot create
  the authorization, alter resolved authority or sign a transaction.
- `tosctl` or an equivalently hardened custody process owns wallet signing.
  OpenFox and `tos-messengerd` do not receive chain private keys.
- Claim signing is performed by a recipient-owned Gift claimant process. The
  model never receives the claim private key.

## 4. Recipient Gift profile

Before funding, the sender resolves a finalized, network-bound Gift receiver
profile for the canonical recipient AgentID:

```text
GiftReceiverProfileV1 {
  network
  recipient_agent_id
  claim_public_key
  supported_asset_contracts[]
  not_before
  expires_at
  generation
  profile_digest
}
```

The profile is signed or committed through the existing Agent controller
hierarchy. Resolution verifies the Agent lifecycle, network tuple, controller
authority, validity window and monotonically advancing generation.

The claim key is a narrowly scoped public key. It may authorize only a claim
over the exact Gift ID, vault, recipient AgentID, destination stablecoin wallet,
nonce and expiry. It cannot authorize Messenger sessions, Agent mutations,
Capability actions or general wallet transfers.

Rotation affects only Gifts prepared after the new finalized profile is
resolved. An existing funded Gift remains bound to the claim key committed in
its immutable terms. Revocation policy must be explicit: V1 does not silently
replace that key. A future recovery profile may add an owner-authorized timeout
path without changing already finalized outcomes.

If no valid profile exists, the operation fails before authorization or
funding. OpenFox must not ask the model to invent a payout address.

## 5. Canonical Gift identity and immutable terms

The sender runtime creates a cryptographically random 256-bit `gift_intent_id`
outside the model. After recipient/profile resolution, the canonical terms bind
at least:

```text
network tuple
gift_intent_id
sender_agent_id
recipient_agent_id
recipient_claim_public_key
stablecoin master contract
amount in indivisible units
claim expiry
refund destination authority
Gift-vault code hash and version
```

`GiftID` is a domain-separated digest of the canonical terms. The deterministic
vault address is derived through the pinned contract deployment rules and is
verified before funding.

The human greeting, emoji, color and `.tos` alias are not part of payment
authority. If presentation text is committed for audit, it uses a separate
bounded display digest so changing it cannot change the recipient or amount.

The durable sender idempotency key is the exact `GiftID`. Reusing one
`gift_intent_id` with different canonical terms is a conflict, not another
Gift. Retrying exact terms resumes the existing record and cannot fund twice.

## 6. On-chain Gift vault

V1 requires a dedicated Gift vault contract. The software-work escrow MUST NOT
be repurposed: its Quote, Capability, Receipt, dispute and provider semantics do
not describe a gift.

The vault commits the immutable terms and accepts exactly the required
stablecoin amount through the standard authenticated transfer-notification
path. Direct wallet credit, an unverified token notification, wrong asset,
wrong amount, wrong vault code or surplus funding fails closed under the
contract's specified recovery rules.

The vault exposes two mutually exclusive terminal paths:

1. `claim`: before expiry, verify the dedicated recipient claim signature and
   request transfer of the exact amount to the signed destination wallet; or
2. `refund`: after expiry, authorize the pinned sender refund authority and
   request transfer of the exact amount to the refund destination.

Claim and refund serialize through one contract state. At most one terminal
economic transfer request may exist. As with the stablecoin escrow, initiating
an asynchronous wallet transfer is not terminal success. The vault becomes
`claimed` or `refunded` only after the exact authenticated wallet callback or
other profile-defined finalized confirmation. Bounce and ambiguous-transfer
states remain nonterminal and recoverable without issuing a second economic
transfer.

## 7. Durable lifecycle

OpenFox keeps a non-authoritative orchestration projection. The chain/vault
record remains authoritative:

```text
draft
  -> recipient-verified
  -> policy-authorized
  -> vault-prepared
  -> funding-submitted
  -> funded
  -> offer-announced
  -> claim-submitted -> claim-transfer-pending -> claimed
  -> refund-submitted -> refund-transfer-pending -> refunded
```

Before `funded`, a rejected or expired local attempt may become
`terminal-failed` without an economic outcome. After funding, local failures
are never collapsed into failure: the record remains resumable until finalized
chain state proves `claimed` or `refunded`.

Each transition is fsynced before its next external side effect. On restart,
the coordinator queries finalized vault/wallet state before retrying an
ambiguous mutation. A transaction hash is useful evidence but not a state
transition by itself.

The recipient projection has `observed`, `claim-authorized`,
`claim-submitted`, `claimed`, `expired` and `refunded` views. It never marks a
Gift claimed merely because it submitted a claim or sent a chat acknowledgement.

## 8. Messenger profile

Messenger carries an encrypted authenticated payload conceptually shaped as:

```text
agent.gift.offer.v1 {
  gift_id
  network
  vault_address
  sender_agent_id
  recipient_agent_id
  asset_display
  amount_display
  expires_at
  optional_display_message
}
```

The receiver independently:

1. binds the Event sender and recipient to the payload AgentIDs;
2. derives or verifies the expected Gift vault address and pinned code;
3. reads finalized vault state;
4. checks the exact canonical asset, amount, claim key and expiry; and
5. displays `claimable` only when the vault is finalized as funded.

`asset_display`, `amount_display` and status messages are hints. Divergence
from canonical chain terms is a security error, not a UI warning.

Optional `agent.gift.status.v1` Events may prompt refresh after claim or refund,
but carry no economic authority. Delivery acknowledgement, ReadAck and TOS
commercial Receipt are not Gift settlement evidence.

The offer may travel over an existing direct conversation or private room, but
V1 always names exactly one recipient AgentID. Room membership never expands
claim eligibility.

## 9. OpenFox behavior

OpenFox exposes narrow owner/runtime actions rather than a generic wallet tool:

```text
PrepareGift(recipientInput, asset, amount, expiry, display)
AuthorizeGift(giftID, ownerDecision)
FundGift(giftID)
AnnounceGift(giftID, conversationIntent)
ClaimGift(giftID, destinationPolicy)
RefreshGift(giftID)
RefundExpiredGift(giftID)
```

Production code resolves recipient and chain authority through typed services.
The model cannot submit vault address, claim key, wallet address, contract code,
finality proof, transaction body or signature. A destination wallet used for a
claim comes from recipient custody policy and is covered by the exact claim
signature.

Funding and announcement are separate resumable operations. If funding
finalizes but Messenger is unavailable, OpenFox keeps retrying the same
announcement; it does not fund another Gift. If announcement arrives before a
receiver observes finality, the UI shows verification pending rather than
claimable.

Policy must bound at least:

- network and stablecoin contract;
- per-Gift and rolling total amount;
- recipient AgentID or an explicit recipient class;
- number of funded Gifts per period;
- minimum/maximum claim window;
- maximum concurrent nonterminal Gifts; and
- whether autonomous proposal is allowed. Funding still requires the stated
  mandate and is never implied by conversational consent.

## 10. Repository ownership

| Repository | Responsibilities |
|---|---|
| `tos-service-spec` | This profile, state machines, authority boundaries, vectors and acceptance evidence |
| `tos` | Gift-vault TVM contract, deterministic address/state rules, stablecoin callbacks and finalized state exposure |
| `tosctl` | Hardened wallet/claim custody, exact transaction preparation, signing and broadcast |
| `tos-service-protocol` | Canonical Gift/profile types, digests, resolvers, strict clients and adversarial vectors |
| `tos-messenger` | Authenticated encrypted Gift offer/status payload carriage and Event identity binding only |
| `OpenFox` | User/model intent, owner-policy orchestration, durable non-authoritative projection and presentation |

`tos-service-gateway` is not required for direct gifts. If it later indexes Gift
activity, results are discovery hints only. `tos-ai` is not required because a
Gift has no software execution or commercial Receipt.

## 11. Threat model and required refusal cases

Implementations must test at least:

- `.tos` reassignment after preparation does not change the recipient AgentID;
- wrong network, Agent, profile generation, claim key, asset, amount, expiry,
  vault code or deterministic address fails before funding or display;
- model-selected Endpoint, Session, vault, claim key, wallet or transaction
  fields are unrepresentable or rejected;
- exact funding retry cannot create a second vault or transfer;
- duplicate/multi-Relay offer delivery cannot create a second claim;
- claim-key substitution and claim to an unsigned wallet fail;
- claim after expiry and refund before expiry fail;
- concurrent claim/refund produces exactly one terminal path;
- bounced or ambiguous stablecoin callbacks remain recoverable and cannot
  issue a second economic transfer;
- local journal corruption, rollback and cross-network replay fail closed;
- Messenger delivery/read acknowledgements cannot mark funds claimed; and
- compromised Gateway, Relay or model output cannot authorize spending.

Amounts are represented only in indivisible integer units under the exact
asset contract. Floating-point values are prohibited. Every wire object is
strictly bounded, versioned, domain-separated and rejects unknown fields where
forward-compatibility rules do not explicitly permit them.

## 12. Privacy and abuse

V1 does not claim confidential amounts or anonymous participants. Public chain
state may expose the vault, asset, amount, timing and committed identities or
keys. Messenger encryption only protects the offer while transported.

Receiving an offer never causes automatic signing, transaction broadcast or
model tool execution. Operators may block unsolicited Gift presentation,
enforce known-contact/invite admission, rate-limit verification and hide spam
without changing chain truth. A Gift is not proof of trust, reputation or
permission to contact the recipient again.

Tax, sanctions, consumer-protection, money-transmission and reporting duties
are deployment-specific legal requirements and are outside protocol
correctness. Production enablement requires an operator review for its
jurisdiction.

## 13. Group red packets — deferred profile

Group packets are not a trivial repetition of V1. A future profile must define:

- the exact MLS room ID and immutable membership epoch eligible to claim;
- privacy-preserving eligibility proofs and dedicated claim keys;
- a hard participant/share bound and unambiguous remainder policy;
- concurrent claim serialization and per-Agent replay protection;
- join/remove behavior after the eligibility snapshot;
- expiry and refund of unclaimed shares; and
- verifiable allocation randomness.

Relay arrival order, model output, local clocks and block timestamps MUST NOT be
used as “random” allocation authority. An equal-share profile can be considered
before a random-share profile. A random profile requires a separately reviewed
commit/reveal, VRF or other manipulation-resistant construction and must state
who can bias or abort it.

Until that profile exists, sending one direct Gift Event to a room does not
create a group packet. It still names one canonical recipient AgentID.

## 14. Implementation sequence

### G0 — specification and vectors

- freeze canonical terms, GiftID, profile digest and claim-signing preimages;
- freeze the stablecoin/vault state machine and callback recovery;
- publish positive and adversarial vectors; and
- obtain contract, custody and cross-repository security review.

### G1 — contract and read-only verification

- implement the Gift vault and emulator tests in `tos`;
- add finalized profile/vault/wallet resolvers in `tos-service-protocol`;
- implement OpenFox observe-only display against injected finalized fixtures;
- do not enable funding.

### G2 — owner-authorized direct Gift

- add hardened sender and claimant custody commands;
- add OpenFox durable orchestration and exact policy/mandate enforcement;
- add Messenger offer/status payloads;
- prove funding, delayed delivery, claim, expiry, refund and full-process
  restart on a local validator network.

### G3 — independent acceptance

- separate sender, recipient, resolver and validator operators;
- one fresh funded Gift claimed successfully;
- one fresh funded Gift expires and refunds successfully;
- ambiguous broadcast/callback and Messenger outage recovery;
- independently reconstructed canonical terms and terminal wallet transfers;
  and
- exact configs, binaries, code hashes, checkpoints and repository commits in
  a signed evidence bundle.

Group/equal-share and group/random-share work begins only after G3 and uses a
new versioned specification.

## 15. Acceptance criterion

V1 is complete only when an operator can say:

```text
“Send 10 units to alice.tos as a gift, claimable for 24 hours.”
```

and the implementation:

1. resolves `alice.tos` once to a canonical AgentID;
2. verifies that Agent's finalized Gift receiver profile;
3. obtains exact owner authorization and external custody signature;
4. funds exactly one deterministic Gift vault;
5. announces only the verified Gift reference through Messenger;
6. lets only the pinned recipient claim before expiry;
7. otherwise lets only the sender refund after expiry; and
8. reports success only from finalized vault and wallet state.

Ordinary OpenFox messaging remains usable with Gift support disabled and with
no wallet configured.
