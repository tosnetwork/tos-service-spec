# Agent Paid Demand Discovery V1

**Status:** incubation design; schema freeze, implementation, and external
acceptance pending

**Blocking status:** D3 Provider Offer acceptance and D4 automatic commercial
action are blocked until the complete D2 gate demonstrates two Section 9.1-
independent sources, source-plus-database shutdown recovery, and a second
independent codec/verifier, and until the separate
[`PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md`](PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md)
handoff profile is frozen, implemented, and covered by independent vectors.

**Protocol:** `tos_service_v1`

## 1. Purpose

This document defines how Agents may publish, propagate, find, verify, and
respond to paid work opportunities without a central marketplace or a
canonical market database.

It deliberately separates three layers:

1. a permissionless discovery data plane for public Capability references and
   signed Paid Demand artifacts, plus direct negotiation transport for Provider
   Offers;
2. a common commerce protocol that binds one exact agreement into the existing
   Quote, escrow, execution, Receipt, and settlement rail; and
3. optional market applications that may search, rank, curate, match, support,
   or charge for their own services without becoming protocol authority.

A centralized market application may be useful and commercially successful.
It is one optional producer, carrier, index, or consumer of the same portable
artifacts, not a required intermediary. No accepted TOS-native purchase may
depend on that application or its database for verification, execution, or
settlement recovery. The D2 promotion run separately proves that public paid-
demand discovery survives loss of one qualifying source and its complete
database. A private or application-exclusive lead may disappear before
acceptance; that does not make the application protocol authority or satisfy
D2.

The product may render this system as a job board, opportunity feed, or work
square. Those are user experiences, not protocol authority. This document's
protocol boundary is a bounded signed paid-demand envelope distributed through
replaceable carriers and indexes, followed by direct Provider Offers and buyer
selection. A separate binding profile hands an accepted Offer into the existing
Accepted Quote, escrow, execution, Receipt, and settlement lifecycle.

The target interaction is:

```text
buyer Agent publishes signed paid demand
  -> public channels and independent indexes propagate it
  -> provider OpenFox instances merge, verify, match, and price locally
  -> each provider constructs one body and returns its signed Provider Offer
  -> buyer verifies and selects one Offer locally
  -> paid-demand binding profile
  -> deterministic versioned escrow starts pending acceptance
  -> bound buyer wallet finalizes the on-chain accept transition
  -> exact stablecoin funding finalizes asynchronously
  -> existing Gate, execution, Receipt, and provider settlement rail
```

This design specializes the opportunity-discovery portion of
[`OPENFOX_AUTONOMOUS_EARNING_CROSS_REPOSITORY_DESIGN.md`](OPENFOX_AUTONOMOUS_EARNING_CROSS_REPOSITORY_DESIGN.md).
The corresponding OpenFox-local package, state-machine, economics, policy,
accounting, configuration, operator-interface, and observability plan is
defined in
[`OPENFOX_AUTONOMOUS_EARNING_IMPLEMENTATION_PLAN.md`](OPENFOX_AUTONOMOUS_EARNING_IMPLEMENTATION_PLAN.md).
That plan is non-normative; this document and the cross-repository design
govern market artifacts and authority.
The exact selected-Offer handoff is governed by
[`PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md`](PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md),
which is an extension adapter to the existing commercial rail rather than a
second transaction lifecycle.
It reuses the authority boundaries in [`ARCHITECTURE.md`](ARCHITECTURE.md), the
commerce lifecycle in [`SETTLEMENT.md`](SETTLEMENT.md), client-side Gateway
composition in [`GATEWAY_FEDERATION_V1.md`](GATEWAY_FEDERATION_V1.md), and the
public-channel transport foundations in
[`AGENT_NATIVE_MESSENGER_V1.md`](AGENT_NATIVE_MESSENGER_V1.md).

## 2. Status and scope

This is an incubation design, not a frozen wire specification. It does not add
messages to `proto/tos/service/v1/native.proto`, establish digest or signature
domains, or claim that the paid-demand network is implemented. A later
specification PR must apply the product-strategy decision filter and freeze the
exact protobuf messages, bounds, encodings, vectors, and public errors before
automatic commercial action is enabled.

V1 is deliberately narrow:

- one TOS network domain per envelope;
- buyer-published fixed-price machine-checkable software work;
- public discovery metadata with bulk input bytes withheld;
- provider responses sent directly to the buyer;
- each accepted Provider Offer maps deterministically to one versioned existing
  Accepted Quote and escrow carrying the typed paid-demand binding;
- exact TOS-network stablecoin identity for the service payment;
- native TOS used separately for network fees; and
- objective completion, release, or refund under existing software-work rules.

Competitive price revision may follow the fixed-price path. Subjective work,
general arbitration, sealed-bid auctions, provider subcontracting, GPU markets,
payment channels, additional task profiles, and cross-network markets remain
outside V1 and behind their existing roadmap gates.

### 2.1 Paid-demand acquisition and handoff gaps

The surrounding repositories already implement a narrow Capability-first
commercial rail: Quote construction, deterministic escrow, exact finalized
funding checks, the Native Execution Gate, bounded software-work execution,
Receipt processing, release/refund, and finalized settlement recovery. This
profile reuses that rail.

What is not implemented end to end is the paid-demand acquisition front end and
its typed handoff into that rail. In particular, the following are missing:

1. Native protobuf messages for Paid Demand Mutation, Provider Offer,
   Selection Notice, the paid-demand Quote binding, and their query/result
   envelopes;
2. frozen content-identity, canonical encoding, digest, signature, delegation,
   expiry, and Demand Mutation domains with cross-implementation vectors;
3. a typed `paid-demand` public-channel event profile in `tos-messenger`;
4. bounded Gateway publication, withdrawal, lookup, search, mutation-
   resolution, cursor, and provenance interfaces;
5. an OpenFox multi-source synchronizer with durable per-source cursors,
   deduplication, equivocation detection, local matching, and economic policy,
   plus the D2 two-independent-source shutdown test and second independent
   codec/verifier required before commercial action;
6. a signed single-acceptance Provider Offer transport and deterministic
   one-Offer/one-existing-Quote handoff;
7. opportunity-channel topic, profile, bootstrap, subscription, and
   republication rules;
8. independent public-network evidence for Overlay, DHT, Storage, Gateway, and
   direct-offer paths;
9. a measured anti-spam and false-buyer policy that bounds provider evaluation
   cost without creating Gateway authority;
10. a compact Paid Demand Reference, informally an **Opportunity Magnet**, that
    lets an Agent retrieve the exact signed envelope from multiple independent
    carriers by content identity;
11. the versioned binding profile defined in
    [`PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md`](PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md),
    including a mutation-bound `BuyerHandoffProfile`, typed Quote-binding body,
    Provider proof, and deterministic handoff into the existing Quote;
12. market-specific bounded delegation scopes with historical and current
    authorization verification, portable finalized authority references, and
    acceptance-time revocation ordering;
13. a private-input delivery profile that never lets remote task data select a
    provider network target or credential;
14. a Provider-private, rollback-resistant writer lease/fencing and aggregate-
    exposure admission boundary spanning every shared OpenFox instance, signer
    key, mandate, runtime, unexpired Offer, and unsettled obligation without
    leaking that private state into public market artifacts.

Existing group chat, public-channel primitives, and Capability search do not
close the acquisition gaps. Conversely, existing Quote, escrow, executor,
Receipt, and settlement code must not be represented as missing: it is the
implemented transaction rail on which the binding extension is built.

## 3. Architectural decision

### 3.1 A distributed bulletin system, not one bulletin board

There is no globally privileged board, room, Gateway, indexer, moderator, or
database. A paid-demand envelope has the same identity regardless of where it
is observed. It may be carried by:

- a Messenger public opportunity channel;
- a direct Agent conversation or private room;
- a replaceable TOS Service Gateway discovery endpoint;
- another independently operated indexer;
- a content-addressed TOS Storage snapshot discovered through a public-channel
  history; or
- an owner-approved application such as FreeCity.

A carrier proves only that it served particular bytes. The envelope signature
proves only the authorized origin of those bytes. Neither fact proves that the
buyer will select an offer, that escrow is funded, that execution is
authorized, or that payment will settle.

### 3.2 Databases are allowed; database authority is not

Gateways, public-channel replicas, FreeCity, and individual OpenFox instances
may each maintain a local database for search, cursors, moderation, spam
control, and restart recovery. Those databases are disposable projections.
They may disagree, omit events, rank differently, or disappear.

No database row can:

- create or transfer an Agent or Capability;
- make a demand accepted or funded;
- select an execution signer;
- authorize provider execution;
- establish a Receipt, release, or refund outcome; or
- recognize settled provider revenue.

Finalized TOS state remains the sole canonical authority for those facts.

### 3.3 Do not put the public market feed on-chain

Task advertisements, search impressions, offer revisions, and unsuccessful
bids are frequent, short-lived, privacy-sensitive, and mostly non-winning.
Putting them all in consensus would add cost, latency, spam, permanent data,
and privacy leakage without strengthening the winning commercial commitment.

TOS finality begins to control one accepted Offer when the deterministic
versioned escrow finalizes its buyer-wallet-authenticated
`pending_acceptance -> awaiting_funding` transition. Deployment alone creates
no acceptance. Execution remains blocked until the later asynchronous
stablecoin funding notification is also finalized and exact. For this
successor, `accept_by == Quote.expires_at` gates only the accept transition;
after acceptance, funding is eligible when the handling transaction's contract
time satisfies `now <= funding_deadline`, without reapplying that acceptance
cutoff. Later finality observation does not change either transaction-time
predicate. Schema 1 retains its frozen funding rule. Bulk task inputs, outputs,
conversation history, and evidence remain off-chain and are bound by immutable
digests where required.

### 3.4 Two discovery lanes, one commercial rail

The ecosystem supports two complementary acquisition lanes:

```text
Capability-first / offering-first
  Provider publishes a versioned Capability
  -> buyer discovers it and constructs the existing Quote
  -> existing Accepted Quote and escrow rail

Demand-first
  buyer publishes a Paid Demand Mutation
  -> Provider returns one signed Provider Offer
  -> paid-demand Quote-binding profile
  -> the same existing Accepted Quote and escrow rail
```

The first lane is the protocol equivalent of a machine-readable service
catalog. The second is the distributed bulletin path defined by this document.
A user interface may call a Capability projection an `offering`, but V1 does
not introduce a second mutable Offering identity or a platform-owned catalog.
Both lanes converge before funding and reuse one commercial state machine.
They retain their schema-appropriate acceptance rule: the frozen schema-1
Capability-first escrow uses finalized deployment as acceptance, while the
paid-demand successor uses `pending_acceptance` followed by the bound buyer
wallet's versioned `accept` operation. Neither schema is reinterpreted as the
other. The paid-demand D2 source-independence gate applies to commercial action
originating from the new public Demand-first path and does not redefine the
existing Capability-first rail's own acceptance status.

Centralized markets may provide managed matching between the lanes, sponsored
placement, recommendations, customer support, KYC, moderation, or manual
dispute services. Permissionless carriers may merely relay exact signed bytes.
Neither class can create acceptance, funding, execution authority, a Receipt,
or settlement. A market's private matching result is not a globally selected
Provider.

## 4. Terms

### Paid Demand

A buyer-originated signed envelope advertising one bounded request for paid
work. It is a pre-acceptance negotiation artifact, not a purchase.

### Demand Mutation

One immutable element in a buyer-authored sequence covering both active
revisions and terminal withdrawal. Every element commits the immediately prior
mutation digest.

### Active Revision

A `DemandMutation` whose kind publishes or supersedes the complete currently
active Paid Demand terms.

### Buyer Handoff Profile

The canonical buyer Agent-to-existing-rail and upload context embedded in every
Active Revision. It fixes the signed Demand authorization context, portable
authority-reference digest, exact settlement wallet already represented by the
existing escrow terms, and dedicated upload proof-of-possession key before any
Provider signs. Transport prose cannot complete or replace it.

### Terminal Withdrawal

A `DemandMutation` whose kind permanently closes the demand for new offers.
V1 does not permit reopening after terminal withdrawal. It cannot cancel an
already finalized Accepted Quote or erase previously distributed bytes.

### Provider Offer

A provider-originated signed response binding one active Demand Mutation to an
exact provider, Capability version, execution profile, price, delivery interval,
and expiry. V1 fixes `max_acceptances = 1`. It is not an Accepted Quote.

### Paid-demand Quote binding profile

The separate versioned adapter that binds one exact Demand Mutation, Provider
Offer authorization, buyer wallet acceptance, and task commitments into one
deterministic instance of the existing Accepted Quote and escrow rail. It is
not a second transaction lifecycle and does not create a demand-wide winner.

### Selection Notice

A buyer-originated non-canonical notice that one Offer is expected to be
converted into an Accepted Quote. It does not prove Quote acceptance, funding,
or that no other Provider Offer will be accepted.

### Opportunity Carrier

A public channel, direct Messenger path, Gateway, indexer, or application API
that transports or indexes immutable market artifacts.

### Opportunity Index

A replaceable local projection used for filtering and search. Its coverage,
freshness, ranking, and moderation are non-canonical.

### Work Square

An application view over locally observed demand, offers, and finalized
commerce. It is not a protocol object.

### Market Application

An optional commercial application, including a UUMIT-like managed labor
market, that may publish, ingest, search, rank, curate, match, or support
portable commerce artifacts. Its accounts, listings, rankings, chat history,
separate service fees, moderation, and customer-service decisions are
application state. A fee deducted from, split from, or routed through TOS
settlement requires an exact pre-acceptance term in a supported Quote/escrow
profile; objective V1 has no platform-fee recipient or payout split. The
application is never a required source of Agent identity, acceptance,
execution, or settlement truth.

## 5. Authority matrix

| Fact | Authority | Non-authoritative observations |
|---|---|---|
| buyer Agent identity and live controller policy | finalized TOS Agent state | display name, channel profile, Gateway account |
| exact paid-demand bytes and historical origin | signature, delegation, generation/policy digest, and portable finalized issuance-authority verification under the market signing profile | channel author label, TLS origin, index row, bare checkpoint number |
| buyer pre-Offer handoff and upload context | exact `BuyerHandoffProfile` inside the signed active Demand Mutation plus historical/current Demand authorization verification | Messenger prose, Selection Notice, Gateway field, Provider guess |
| locally offer-eligible demand observation | verified observed Demand Mutation chain, current live Agent/delegation eligibility, source coverage, and freshness | another observer's “open” badge, any claim of a globally complete head |
| provider identity and Capability/version | finalized TOS Agent and Capability state | offer text, local skill name, Gateway metadata |
| offer origin | candidate offer signature under the approved signing profile | Messenger prose, index ranking |
| buyer selection before acceptance | negotiation input only | Selection Notice, conversation statement |
| one accepted Provider Offer | finalized versioned escrow `pending_acceptance -> awaiting_funding` transition authenticated to the bound buyer wallet and carrying the exact existing Accepted Quote and reconstructible binding extension | deployment alone, Selection Notice, buyer signature alone, Provider Offer, Gateway status, or a local “winner” label |
| execution and payment eligibility | exact finalized escrow funding plus the Accepted Quote and binding extension | Quote deployment alone, funding broadcast, demand, opaque Offer digest, Selection Notice, or Gateway acknowledgement |
| execution admission | shared Native Execution Gate over finalized state | task status, delivery ACK, model output |
| successful result commitment | canonical signed Receipt under accepted terms | process exit, chat message, artifact URL |
| provider revenue | finalized exact provider-wallet credit | quoted price, release intent, dashboard balance |
| search rank, recommendation, curation, KYC, support, or sponsored placement | market-application policy only | any claim that the application decision is protocol acceptance, execution, or settlement authority |

## 6. Candidate paid-demand object model

The following object model identifies the information a future schema must
express. Field names and canonical encoding remain unfrozen until the Native
protobuf specification PR.

### 6.1 Identity and mutation sequence

Each Paid Demand carries:

- exact protocol and paid-demand profile version;
- complete TOS network domain;
- buyer Agent ID;
- buyer-generated nonzero demand nonce;
- positive mutation sequence;
- previous-mutation digest, zero only for sequence one;
- mutation kind exactly `active_revision` or `terminal_withdrawal`;
- creation and publication-expiry times;
- stable idempotency identity outside model control; and
- a signature authorization that can be checked against the buyer's relevant
  finalized Agent policy or approved delegation.

The future canonical demand identity must commit to network, buyer, and nonce.
The mutation digest commits every byte, including sequence, predecessor, kind,
authorization context, and either the complete active terms or terminal target.
Reusing one sequence position with different content is equivocation. Exact
byte replay is idempotent.

An observer never combines fields from two mutations. Sequence `N+1` is
eligible only when its predecessor equals the verified sequence `N` digest.
`terminal_withdrawal` contains no replacement active terms, permanently closes
the sequence, and rejects every later descendant. A broken, missing, or forked
mutation chain is not actionable and does not authorize guessing the current
state.

Every `active_revision` contains exactly one complete
`BuyerHandoffProfile` defined in Sections 6.3 and 6.6. A
`terminal_withdrawal` contains no replacement handoff or upload profile.

### 6.2 Task profile and requirements

Each demand carries bounded structured requirements:

- task-profile identifier and version;
- human-readable summary treated as untrusted display text;
- required Capability predicates;
- input media type and immutable input commitment;
- required output media types;
- objective validator and evidence-profile identifiers;
- execution resource class and maximum completion duration in positive integer
  seconds;
- input-delivery, execution-admission, and execution-completion constraints plus
  any earlier Offer-acceptance deadline;
- accepted transport profiles; and
- objective dispute-policy/refund profile compatible with the selected
  software-work profile; V1 permits only successful release or full timeout
  refund and has no dispute state.

Capability predicates are exact structured filters, not natural-language
authority. A free-form description may improve discovery but cannot change the
input commitment, success rule, resource limit, evidence obligation, or
commercial terms.

Bulk source archives, prompts, credentials, private repository URLs, personal
data, and secret acceptance tests are not published in the public envelope.
The envelope commits to the required bytes and bounds, never a provider-fetch
URL or buyer credential. Disclosure uses the buyer-push profile in
[`PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md`](PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md)
only after the existing Accepted Quote and exact escrow funding are finalized.

### 6.3 Commercial terms

Each V1 demand carries:

- a complete `BuyerHandoffProfile` containing the buyer Agent ID, equal to the
  envelope buyer, exact settlement-wallet commitment, buyer Agent generation
  and controller-policy digest, exact Demand-publication delegation, typed
  delegation bounds and owner-mandate digests, authorization validity interval,
  canonical proof/profile version and signature encoding, portable finalized
  issuance-authority reference digest, and a dedicated upload proof-of-
  possession public key/key ID, proof algorithm/profile version, and input-
  delivery validity bounds;
- exact TOS-network asset identity;
- fixed provider-service payment in unsigned atomic units;
- explicit statement of who pays network and protocol fees;
- Offer-acceptance, funding, input-delivery, execution-admission,
  execution-completion, and refund deadline constraints, plus the minimum
  nonzero release-pipeline margin required by the selected profile;
- an optional buyer-local desired Provider count that is negotiation metadata,
  not global acceptance authority;
- Accepted Quote and escrow profile requirements;
- required provider Capability/version and execution-signer bindings; and
- the objective release and timeout-refund inputs allowed by the selected
  existing profile.

The dedicated upload key has no wallet, Agent-control, market-signing,
settlement, or read authority. It proves possession only when pushing the one
input already committed by the accepted terms.

A ticker, exchange-rate estimate, Gateway balance, external-chain token, or
custodial credit is not a valid asset identity. Monetary authorization uses
checked integer atomic units. A later UI may display converted estimates but
they never change signed terms.

The complete buyer handoff and upload context is part of every
`active_revision` canonical preimage. The `paid-demand.publish` signature
authenticates that commitment but does not itself accept later work. Buyer
commercial acceptance is the exact finalized versioned escrow `accept`
transition authenticated to the bound settlement wallet; the named upload key
separately proves possession for the bound private-input request.

A Provider constructs the candidate `PaidDemandQuoteBindingBodyV1` only from this exact
mutation-bound context plus Provider-selected fields. It never guesses a live
buyer delegation and never obtains a key, proof profile, authority reference,
wallet, or upload key from a Selection Notice, ordinary Messenger content, or
Gateway metadata. An active mutation missing any required context is
display-only and cannot receive a Provider Offer.

Changing the Demand delegation/mandate, proof profile, authority-reference
digest, settlement wallet, or upload proof-of-possession key for future Offers
requires a new complete `active_revision` with the next sequence and exact
predecessor. Revocation or expiry before Accepted Quote finality
makes an Offer bound to the old context non-actionable; a buyer cannot repair or
replace that context after the Provider signs.

### 6.4 Routing and discovery hints

An envelope may carry bounded non-authoritative hints for:

- topic identifiers;
- languages or regions relevant to delivery;
- preferred direct negotiation method;
- reply-to Agent or delegated Messenger identity;
- content-addressed public supporting material; and
- optional index categories.

Topic, channel, Gateway, hostname, alias, and reply route are never Agent,
Capability, acceptance, or payment authority. The accepting flow must rebind
the selected provider and execution route through the existing Quote rules.

### 6.5 Anti-abuse commitment

The profile reserves a bounded anti-abuse section. V1 must select at most one
minimal mechanism justified by measurements, such as:

- finalized live buyer Agent plus per-Agent publication rate limits;
- an owner-approved issuer allow-list;
- a small TOS fee or refundable demand bond under a separately specified
  contract profile; or
- a verifiable funded-intent commitment that reveals no more than necessary.

No implementation may invent a Gateway balance, private reputation score, or
unverifiable “verified buyer” badge as universal authority. A bond, if later
approved, reduces spam but does not prove that a task is safe, profitable, or
guaranteed to settle.

### 6.6 Market authorization profile

V1 uses purpose-limited online delegations rather than Agent-control,
Capability-control, recovery, wallet, or settlement keys. The target scopes
are distinct and non-interchangeable:

```text
paid-demand.publish
paid-demand.withdraw
provider-offer.sign
```

`active_revision` requires `paid-demand.publish`; `terminal_withdrawal`
requires `paid-demand.withdraw`; a Provider Offer requires
`provider-offer.sign`. Cross-purpose substitution is invalid. The signed Demand
Mutation authenticates the buyer Agent's handoff context; the exact buyer
settlement wallet separately authorizes the versioned escrow `accept`
operation, whose finalized `pending_acceptance -> awaiting_funding` transition
creates the Accepted Quote, and later supplies the exact asynchronous stablecoin
funding. Permissionless deployment alone creates no acceptance, and a market
delegation never becomes a wallet key.

Each V1 market artifact is signed by one exact delegated Ed25519 key named in
its canonical preimage. Weighted controller keys authorize or revoke the
delegation; they do not form variable per-artifact threshold-signature subsets.
The signing key, delegation digest, signature profile, and canonical Ed25519
signature encoding are unique inputs. An otherwise authorized alternate key,
different valid threshold subset, or different proof ordering is not an
equivalent encoding of the same artifact.

The `provider-offer.sign` delegation is not merely a purpose bit. Its typed
bounds commit at least the allowed Provider Agent and Capability/profile set,
asset and minimum-price/fee bounds, maximum resource and Offer lifetime,
paid-demand-binding/Quote/escrow code profiles, and owner-mandate digest. A verifier
checks every static bound against the Offer. Dynamic capacity and stricter
price-floor decisions remain in the Provider's
atomic owner-policy boundary, but a compromised online Offer key cannot use an
otherwise valid delegation outside its frozen profile, asset, lifetime, or
contract bounds.

The exact scope encoding remains a schema-freeze item, but every signed market
artifact commits:

- complete network domain and protocol/profile version;
- signer public-key identity and exact market scope;
- Agent ID, Agent generation, and controller-policy digest;
- delegation digest and delegation validity interval, when delegated;
- a portable finalized issuance-authority reference and issuance time under
  the frozen clock rule;
- artifact identity, sequence, predecessor, content digest, and expiry; and
- a domain-separated signature over the complete canonical preimage.

A bare checkpoint height or timestamp is not an authority proof. The portable
reference names the complete network and Registry identity, Agent object,
generation, controller-policy and delegation digests, typed state hash,
transaction hash, contract code hash, and finalized checkpoint. Schema freeze
must select either a historical finalized-state resolver or a self-contained
proof format that independently reproduces those facts after policy rotation;
a Gateway cache or issuer-supplied JSON assertion is insufficient.

Verification has three separate results:

1. **historical authenticity** proves that the signing key and scope were
   authorized by the referenced finalized Agent generation, policy/delegation,
   and issuance checkpoint; and
2. **current authorization eligibility** freshly proves, before expensive offer
   evaluation and again at Quote acceptance, that the Agent is live, the
   relevant market delegation remains active and unrevoked, and the artifact
   has not expired; and
3. **observed mutation eligibility** proves the integrity and non-terminal,
   non-forked status of the exact mutation chain available through the
   verifier's recorded sources and freshness window. It does not prove that no
   unseen successor, terminal withdrawal, or conflicting branch exists.

Historical bytes remain attributable after normal rotation or later
revocation, but they cease to authorize a new offer or Quote when the current
authorization-eligibility check fails. A recovered or rotated current
controller may issue the next mutation, including terminal withdrawal, only
through the same monotonic sequence and immediate predecessor. It cannot
rewrite history.

For an active Demand Mutation, verification also resolves and checks its exact
`BuyerHandoffProfile`: the Demand-publication delegation, typed bounds,
validity, proof profile, and portable authority-reference digest must be
historically authentic and currently eligible before Provider reservation or
signing. The complete portable proof may be embedded or retrieved by content
identity, but failure to resolve it or reproduce its committed digest fails
closed. Messenger, Selection Notice, Gateway, index, and local-journal fields
cannot complete, normalize, or rotate the profile.

A Provider Offer becomes non-actionable before Quote finality if its provider
Agent, signing delegation, Capability/version, manifest, or reserved capacity
authorization is revoked, transferred, expired, or otherwise no longer valid.
The paid-demand binding resolver and Native Execution Gate prove from finalized
history that the signed Demand and Provider Offer authorizations were valid at
the Quote-acceptance checkpoint and that the buyer-wallet-authenticated escrow
`accept` transition's containing transaction had contract time strictly before
the Offer deadline; finality may be observed later. Revocation finalized before
that transition makes the attempt invalid; revocation finalized only after
acceptance does not rewrite the finalized Quote. If the resolver cannot
establish a strict finalized order, including a same-checkpoint or cross-shard
race, it fails closed. Existing Capability, execution-signer, escrow, and
settlement revocation rules continue to apply.

## 7. Withdrawal, supersession, and expiry

A signed market artifact is immutable. Lifecycle is represented by additional
artifacts and local projection, not by mutating an index row as if it were a
shared object.

Revision and Withdrawal share one sequence:

```text
unknown
  -> active(sequence 1)
  -> active(sequence 2)
  -> ...
  -> terminal-withdrawn(sequence N)
```

The following rules apply:

1. Every mutation increments sequence by exactly one and commits the exact
   immediately prior mutation digest.
2. `active_revision` carries the complete new active terms; it does not patch
   fields from an older revision.
3. `terminal_withdrawal` names the same demand identity and predecessor,
   permanently ends the chain, and carries no replacement active terms.
4. V1 forbids reopen or any descendant after terminal withdrawal.
5. A conforming observer that has verified terminal withdrawal marks the demand
   ineligible for new offers. It does not claim that every delayed or offline
   carrier has received the mutation.
6. A conforming observer that has verified withdrawal or expiry refuses a new
   Offer or Quote-preparation action under this profile. Absence of such an
   observation does not prove that no unseen withdrawal exists, and no feed
   artifact can undo an already finalized Accepted Quote.
7. Expiry is evaluated under the future profile's bounded clock/freshness rule;
   a carrier's wall clock is not shared commercial authority.
8. If two different otherwise valid artifacts claim the same sequence, every
   descendant is quarantined as equivocation. Arrival order, carrier count, and
   index ranking never choose a branch. Only a later separately specified
   on-chain or owner recovery profile could resolve such a fork; V1 has none.
9. A late mutation is applied only after its complete predecessor chain is
   verified. An observer that saw sequence N+1 before N reports incomplete,
   not open.
10. Missing history causes an incomplete projection, not a fabricated chain.
11. Moderation may hide an event locally without altering its digest, signature,
    origin, or availability through another carrier.

For Provider-side projection, a verified terminal withdrawal observed before a
Provider signature exists may stop preparation and release local reservations
idempotently. From the moment a Provider Offer is authorized, the signature may
have escaped even if local send state is absent. A withdrawal, expiry, reject,
failure, or cancellation signal therefore enters
`WITHDRAWAL_OBSERVED`/`CANCELLATION_RESOLVING`, stops new send and execution
attempts only while the Offer is not yet accepted, and retains every local,
Provider-private, and runtime reservation. The Provider resolves its own
deterministic Quote/escrow identity at an adequate finalized checkpoint. A
valid finalized acceptance of its Offer converges to accepted work regardless
of event arrival order. A competing Offer has no authority over this Quote.
Only after the Offer deadline and deterministic proof that this exact escrow's
buyer-wallet `accept` transition cannot still finalize may the Provider mark the
Offer withdrawn or expired and release once. After Accepted Quote finality,
Demand withdrawal is evidence only and cannot cancel the purchase. The current
objective V1 rail then permits only successful release or timeout refund; an
accepted-but-unfunded local obligation may expire only after finalized
resolution proves that funding can no longer become authoritative. Execution
remains gated on exact finalized funding.

Selection and Accepted Quote status do not become public-feed lifecycle states
unless independently derived from the finalized chain. A buyer's Selection
Notice remains negotiation data and may be stale, malicious, or abandoned.

Expiry and terminal withdrawal are eligibility semantics, not deletion or a
right-to-be-forgotten mechanism. Public-channel, index, cache, or Storage
copies may persist indefinitely. Publishing confirmation must state that
public bytes cannot be guaranteed deleted; sensitive demand defaults to direct
or private carriers.

### 7.1 Mutation integrity is provable; global head completeness is not

A verifier can prove signatures, predecessor links, forks among observed
mutations, and the meaning of an observed terminal withdrawal. Because the feed
has no canonical database or on-chain head, it cannot prove that an apparently
active mutation is the globally latest mutation or that no other carrier holds
an unseen successor, withdrawal, or equivocation.

Every `active` presentation is therefore qualified as “latest verified through
sources S at freshness bound T.” Before signing an Offer, OpenFox refreshes all
owner-required sources and may request a direct buyer-signed head assertion,
but the assertion remains provenance and equivocation evidence rather than
consensus. A known terminal withdrawal or fork fails closed; absence is only a
bounded risk input.

Final commercial authority does not depend on proving a global feed head. The
Provider signs the exact Quote-binding body, and the committed buyer wallet
finalizes the versioned deterministic escrow's `accept` transition carrying
that Offer and later funds it through the existing stablecoin path. A
contradictory terminal withdrawal or head assertion is durable buyer-
equivocation evidence and causes refusal when known before finality, but it
cannot invalidate an already finalized Accepted Quote.
Making withdrawal globally enforceable before acceptance would require a
canonical on-chain demand-head/nonce object; V1 deliberately does not add one.

## 8. Distribution architecture

### 8.1 Public opportunity channels

Messenger public channels are the preferred decentralized real-time carrier
for open demand. They provide signed events, Overlay propagation,
content-addressed history, gap repair, bounded moderation, DHT-based peer
discovery, and TOS Storage history snapshots.

Paid Demand is a typed public-channel event profile. General chat text that
looks like a job advertisement is not silently parsed into a Paid Demand. A
channel may carry the full bounded envelope or an immutable digest plus a
strict content-addressed retrieval reference.

Opportunity channels are topic-scoped rather than one global firehose. A
future profile may define examples such as software testing, static analysis,
or reproducible builds, but topic names are discovery hints. They do not define
task semantics or authorization.

Public-channel publisher and moderator roles control what one channel replica
accepts and presents. They cannot rewrite a valid demand, mark it funded, pick
a winner, or prevent the same bytes from being distributed through another
channel.

### 8.2 DHT

DHT records store short-lived signed locators and content digests. They do not
store paid-demand history, search indexes, bids, Accepted Quotes, or settlement
state.

For public opportunity channels, DHT may help locate:

- current channel peers;
- a signed channel profile;
- verified history-head hints; and
- content-addressed Storage snapshot hints.

A DHT value is a routing hint. The client still verifies channel authority,
event signatures, history links, envelope bytes, network domain, and expiry.

### 8.3 Overlay and RLDP

Overlay distributes public-channel events among participating replicas. RLDP
may transfer bounded history segments and referenced public objects. Network
delivery may be duplicated, reordered, delayed, or incomplete; event identity,
mutation-chain checks, cursors, and local journals make application processing
idempotent.

Overlay membership is not opportunity authority. Seeing an event from many
peers does not make it true or selected. A malicious peer cannot alter signed
bytes without detection but may omit, replay, flood, or delay them; clients
therefore enforce independent source, byte, event, pending-work, and time
budgets.

### 8.4 TOS Storage

TOS Storage may carry deterministic public-channel history snapshots or
bounded public supporting material. Snapshot bytes are content addressed and
reverified before import. Storage availability, a BagID hint, or a successful
download does not prove opportunity validity or freshness.

Private inputs and bid conversations do not become public snapshots. V1 bulk
input delivery uses only the Offer-bound buyer-push profile in
[`PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md`](PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md)
and retains its own authorization and retention rules.

### 8.5 Direct Messenger and private rooms

Direct conversations and private rooms may carry:

- invitation-only Paid Demand;
- provider questions;
- Provider Offers;
- Selection Notices;
- owner approvals; and
- selected-work progress or result transport.

Messenger authenticates the conversation and event origin. Prose still has no
wallet, bid, execution, or settlement authority. Typed market artifacts remain
subject to their own signature, Demand Mutation, policy, and finalized-state
checks.

### 8.6 Gateways and independent indexers

Gateways and indexers make the distributed feed searchable. They may ingest
multiple public channels, direct publisher submissions, or verified Storage
snapshots. They expose bounded queries and preserve exact envelope bytes or an
immutable retrieval path.

Two indexes are expected to differ. A conforming index reports:

- its origin and network domain;
- observation time and source carrier;
- envelope digest, buyer, demand identity, mutation sequence, and mutation
  digest;
- its coverage and freshness bounds;
- any moderation or filtering applied; and
- an opaque source-local cursor.

An index does not report “global latest”, “market complete”, “guaranteed
buyer”, “funded”, or “profitable” unless each claim is explicitly labelled as
a local projection and, where applicable, independently backed by finalized
state.

### 8.7 Paid Demand Reference (“Opportunity Magnet”)

The protocol needs a compact, copyable reference analogous in purpose to a
magnet link: it identifies one immutable Paid Demand envelope and supplies
optional places from which the exact bytes may be retrieved. The normative
name is **Paid Demand Reference**. “Opportunity Magnet” is a product nickname,
not a second schema or authority path.

A future canonical reference has a small mandatory core:

- exact `tos_service_v1` protocol and reference-profile version;
- complete TOS network domain or its unambiguous approved compact encoding;
- paid-demand envelope media/schema identifier; and
- exact content digest of the complete canonical signed Paid Demand envelope.

It may also contain bounded optional hints:

- expected buyer Agent ID for early filtering, which must match the retrieved
  and verified envelope;
- public opportunity-channel profile or immutable channel identifier;
- one or more owner-policy-eligible Gateway origins;
- a content-addressed TOS Storage object or verified channel-snapshot hint;
- a direct publisher or replica retrieval hint; and
- a human-readable label excluded from all identity and authorization
  decisions.

The mandatory core identifies the same demand regardless of which optional
hints are present or in which application the reference is displayed. Hints
are availability inputs only. They cannot alter the digest, buyer, mutation,
task, price, deadline, signature, selection, Quote, or settlement. A Gateway,
channel, DHT record, Storage Bag, hostname, or display label found in a
reference is never trusted merely because the reference was received through
an authenticated conversation.

The exact URI grammar is deliberately not frozen here. A future compact form
may be rendered conceptually as:

```text
tos-demand:<network>:<paid-demand-digest>?source-hints...
```

Implementations must not ship that illustrative spelling as a de facto wire
format. The schema-freeze PR must specify character encoding, normalization,
maximum total length, duplicate/unknown parameter handling, canonical display,
QR representation if any, and downgrade-safe parser behavior.

#### Resolution algorithm

Given a Paid Demand Reference, an OpenFox resolver:

1. parses and bounds the reference without contacting a network;
2. matches the complete network domain and schema to owner policy;
3. checks its content-addressed local cache;
4. selects only configured and policy-approved hints and default sources;
5. queries eligible public channels, Gateways, Storage, and direct replicas in
   bounded local policy order or bounded parallelism;
6. accepts bytes only when the complete canonical envelope digest equals the
   mandatory reference digest;
7. verifies the envelope schema, historical signature/delegation context,
   current buyer Agent/delegation eligibility, the exact observed Demand
   Mutation chain through the referenced mutation, timing, source freshness,
   and task/commercial bounds without claiming that no unseen successor exists;
8. records each successful and failed source observation as provenance;
9. stores the exact verified bytes under the digest; and
10. submits the verified candidate to OpenFox matching and economics, never
    directly to bidding or execution.

The first valid exact envelope is sufficient for content retrieval; agreement
among sources is not consensus. A malformed or mismatching source is isolated.
If every source fails, resolution returns unavailable and does not use an
unverified label, stale cache beyond policy, or similar-looking demand.

#### Mutation successor and terminal-withdrawal behavior

An Opportunity Magnet identifies one immutable mutation, not a mutable “latest
job” row. After resolving it, a client may follow only the single verified
successor chain under Section 7. A reference to sequence N does not silently
retarget to sequence N+1, and it never proves that the named mutation is still
actionable, selected, funded, or payable.

A UI may offer an explicit “resolve current verified mutation” operation. That
operation returns both the originally referenced digest and the verified
Demand Mutation chain so the identity change remains visible.

“Current verified” is source-relative under Section 7.1. It never means global
latest, and a resolver must expose the source set and freshness bound used.

#### Permissionless republication

Any Agent, channel replica, Gateway, indexer, or application may re-serve the
unchanged signed envelope or share another Paid Demand Reference to its digest.
Republication requires no new buyer signature because it creates no new
semantic claim. A republisher may attach new source and display hints, but it
must not alter the mandatory core or represent itself as the buyer.

Indexes deduplicate by exact envelope digest while retaining all source
provenance. Republishing the same bytes improves availability only; it does not
increase authenticity, ranking, buyer solvency, selection probability, or
commercial authority.

#### Security and privacy

- References contain no credentials, bearer tokens, private repository URLs,
  session material, private host paths, or decryption keys.
- Network hints pass the same SSRF, DNS, redirect, TLS, proxy, byte, time, and
  credential-origin policy as direct discovery.
- Clients never contact every untrusted hint automatically; owner policy
  selects eligible carriers and bounds fan-out.
- A reference digest verifies content integrity, not buyer solvency, task
  safety, profitability, availability, or payment.
- Copying a public reference may leak buyer, topic, timing, or commercial
  metadata even when bulk inputs remain private.
- Unknown or unsupported algorithms, schemas, networks, or reference versions
  fail closed without a “best effort” legacy parser.

## 9. Federated discovery

An OpenFox instance configures multiple owner-approved sources. Sources may be
public-channel replicas, Gateway search endpoints, direct contacts, or local
application feeds.

For each source, OpenFox maintains an independent durable cursor and source
health record. It does not convert multiple source cursors into a fictional
global cursor. On each bounded cycle it:

1. requests no more than the configured page/event/byte/time budget;
2. validates the entire source response shape;
3. verifies each envelope before making it eligible;
4. deduplicates exact envelope digests across sources;
5. detects conflicting buyer/demand/mutation-sequence reuse;
6. updates the source cursor only after durable local application;
7. retains every source observation used for provenance; and
8. applies local task, skill, cost, counterparty, and policy filters.

The union of sources is incomplete by definition. Seeing the same envelope
through several sources improves availability but does not create consensus or
increase its commercial authority. One source's malformed page invalidates
that page; it does not poison valid independent sources.

Presentation ordering is local. A client may sort by estimated profit,
deadline, task match, source freshness, counterparty policy, or owner
preference. Ranking inputs and model summaries are recorded as
non-authoritative. Another client may produce a different correct ordering.

### 9.1 Source and implementation independence

Two origins are not independent merely because they use different hostnames.
Acceptance evidence records, for every claimed independent source:

- legal/operator organization and signing identity;
- host, process, and persistent-store identity;
- network path and deployment failure domain;
- upstream public channel, replica, Gateway, or Storage dependency;
- implementation repository, commit, build, and codec dependency; and
- exact observation interval and source-local cursor/checkpoint.

Sources that share one private database, process, host, operator key, upstream
carrier, or single failure domain are labelled correlated. They may improve
read throughput but do not satisfy independent-source acceptance.
Multiple regions, API hostnames, mirrors, or replicas of one managed market
still count as one source when they depend on that market's account system,
private order database, or administrative availability.

At least one acceptance run stops one source and its complete database while a
separately operated source continues reference resolution and discovery. The
second vector implementation independently consumes frozen bytes and does not
call the first implementation's canonical codec or verifier library.

## 10. Discovery query boundary

The future search interface must be bounded and transport-neutral. Candidate
query dimensions include:

- task-profile identifier and version;
- required Capability predicate;
- exact asset identity;
- minimum fixed payment;
- offer and execution deadline window;
- maximum input/output size classes;
- evidence profile;
- buyer Agent allow/deny policy; and
- source-local cursor and page size.

Free-form text may be accepted as a local convenience query, but Gateway match
scores and embeddings are never task compatibility or profitability proof.
OpenFox must rerun typed matching and economics locally over the exact verified
envelope.

A search response must not copy separately locked mutable reads into one
apparently atomic result. The index either takes one consistent local snapshot
or labels per-result observations so a concurrent mutation cannot be hidden.

## 11. Provider Offers and selection

### 11.1 Response path

V1 Provider Offers are returned directly to the reply identity authorized by
the Paid Demand. They are not required to be broadcast to the public channel.
This limits strategy leakage, front-running, spam amplification, and permanent
publication of losing offers.

An Offer remains portable and independently verifiable by its intended parties.
Signing authorizes its exact bytes to be embedded in the deterministic Quote/
StateInit for this purchase, so a selected or predeployed Offer may become
publicly observable even before buyer acceptance. It does not authorize the
Offer to be indexed or republished as general discovery inventory. Losing
Offers remain direct/private unless separately disclosed. A publication profile
plus explicit buyer and Provider authorization is required for public inventory.

The response transport may be direct Messenger or a bounded Gateway relay. It
must preserve the exact signed offer bytes and must not become selection
authority.

### 11.2 Candidate offer contents

A Provider Offer binds at least:

- exact demand identity and active Demand Mutation digest;
- the complete mutation-bound `BuyerHandoffProfile`, including buyer Agent,
  settlement wallet, signed Demand proof context, and upload proof-of-possession
  key/profile, without any Provider guess or post-Offer buyer choice;
- provider Agent ID;
- Capability ID and exact active version;
- manifest, task, input/source, execution, validator, evidence, private-input
  delivery, objective release, and timeout-refund commitments;
- fixed exact-asset price;
- exact acceptance, funding, input-delivery, execution-admission,
  execution-completion, and refund deadlines plus the nonzero
  release-pipeline margin satisfying the checked ordering in the paid-demand
  Quote-binding profile;
- `max_acceptances = 1`;
- one complete deterministic canonical `PaidDemandQuoteBindingBodyV1` with no buyer-
  substitutable commercial or execution field;
- provider-generated durable offer identity;
- reply or Quote-construction transport hint; and
- a reconstructible `provider-offer.sign` authorization over the exact
  `paid_demand_binding_body_digest`, including the constrained delegation, owner-
  mandate digest, and portable finalized authority reference.

OpenFox may use a model to propose price or explanatory prose. Its deterministic
earning policy authorizes the exact structured offer, price floor, fee ceiling,
expiry, capacity reservation, and mandate version before signing.

Before reservation and signing, the Provider re-verifies the exact mutation-
bound `BuyerHandoffProfile` and requires the Offer-acceptance deadline to be no
later than the signed Demand authorization validity bound and every private-
input deadline to fit the committed upload-key validity. It also proves that
the complete acceptance-to-funding, funding-to-input, and input-to-admission
pipeline margins fit their next deadlines, and that the bound maximum
completion duration, preflight-to-start delay, and release-pipeline margin fit
before the refund boundary. No buyer-side field remains selectable after
Provider authorization.

Exact replay of one offer identity is idempotent. Conflicting reuse is rejected
and retained as evidence. An ambiguous send is resolved through a defined
query or direct peer acknowledgement before retry; if no reliable resolution
exists it remains ambiguous until safe expiry or owner review.

### 11.3 Selection

The buyer may compare Offers locally and send a Selection Notice. No Provider
executes or recognizes revenue from that notice, and the notice does not prove
that another Offer was not also selected. The selected Provider checks that the
later Accepted Quote exactly reproduces the required demand/offer
terms and binds the correct provider, Capability version, manifest, endpoint,
execution signer, buyer Agent/wallet, input/source, task/validator/evidence
profiles, asset, amount, deadlines, private-input delivery, objective release,
and timeout-refund profile.

The buyer verifies the Provider proof over the exact binding body. The committed
buyer settlement wallet then authorizes the versioned escrow `accept` operation.
The contract transitions once from `pending_acceptance` to `awaiting_funding`,
creating the Accepted Quote, and the resolver later verifies its exact
stablecoin funding. The successor rejects funding before that transition; once
accepted, the funding handler applies contract-time
`now <= funding_deadline` without reapplying the acceptance-only Quote expiry.
Permissionless predeployment cannot consume or block that transition. The
signed Demand context, Provider Offer proof, and wallet acceptance must be
reconstructible from finalized accepted state. A Selection Notice, Demand
signature, or deployment alone proves neither Quote acceptance nor funding.

The buyer Agent, Demand proof context, settlement wallet, and upload proof-of-
possession key must exactly equal the values already committed by the selected
active Demand Mutation and copied into the Provider-authorized body. A
Selection Notice or acceptance using a different value is invalid; changing
the context requires a new Demand Mutation and a new Provider Offer.

The current Accepted Quote does not bind all of those facts. D3 therefore
requires the versioned adapter in
[`PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md`](PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md).
An index, Selection Notice, Messenger message, Gateway acknowledgement, or
OpenFox journal must not fill the gap as hidden authority.

### 11.4 Handoff to the existing commercial rail

This discovery profile stops at one exact signed Provider Offer and optional
local Selection Notice. Buyer commercial acceptance occurs only through the
bound wallet's finalized `accept` transition on the deterministic versioned
escrow. The governing handoff is
[`PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md`](PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md).

That profile defines `PaidDemandQuoteBindingBodyV1`, the Provider proof, and the
versioned payload committed by the existing Accepted Quote. These objects are
an adapter into the existing rail; they do not create a second Quote, escrow,
Execution Gate, Receipt, ledger, or settlement state machine.

One Provider Offer deterministically maps to one existing Quote commitment and
escrow address. Deployment creates only `pending_acceptance`; the bound buyer
wallet's finalized `accept` transition is Quote acceptance. Exact stablecoin
funding arrives later through the existing asynchronous transfer-notification
path, and no Provider executes before that funded state is finalized.

Different Provider Offers remain independent. A buyer-local policy may prefer
one Provider, but V1 has no chain-wide winner or atomic cross-escrow selection
primitive. If the buyer accepts and funds two different Offers, both purchases
are valid. A future exclusive auction would require a separately specified
coordinator contract and is outside this profile.

### 11.5 Provider Offer reservation and admission

Provider Offer issuance remains inside this discovery and negotiation boundary.
Before signing, OpenFox:

1. preallocates one durable Offer identity and complete canonical body;
2. derives one stable body digest and semantic action ID;
3. atomically reserves local portfolio exposure;
4. obtains a runtime capacity lease for the same body; and
5. passes Provider-wide purpose-limited custody admission before receiving the
   Provider signature.

Production custody covers every OpenFox instance, signer key, mandate, and
runtime sharing the Provider scope. It uses an exclusive expiring writer lease,
monotonic fencing generation, rollback-resistant high-water/issuance ledger,
unresolved-Offer tracking, and aggregate exposure/capacity admission. Exact
retry returns the recorded signature; stale writers and conflicting bodies fail
closed. Provider-private generations and reservation identifiers never enter
public Offer or body bytes.

A replacement writer inherits unresolved Offers. After an Offer expires,
OpenFox releases its reservations only after resolving that Offer's one
deterministic escrow identity and proving that its buyer-wallet `accept`
transition cannot still finalize.
If Quote acceptance already finalized, the obligation follows the existing
funding deadline, execution, objective refund, and settlement rail. Full recovery and
rollback requirements are defined in the binding profile.

### 11.6 Private input boundary

Discovery artifacts contain only bounded input commitments and never a buyer-
selected fetch URL or credential. Private bytes move only after the existing
Accepted Quote and exact escrow funding are finalized, using the Offer-bound
buyer-push and proof-of-possession profile in
[`PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md`](PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md).

The upload path authenticates and binds immutable bytes to the one
`(Quote commitment, escrow address)` execution slot. It grants no acceptance,
wallet, or execution authority; the existing Native Execution Gate remains the
sole execution-admission boundary.

## 12. OpenFox processing pipeline

Remote paid demand is hostile input. OpenFox processes it in increasing-cost
stages:

```text
bounded decode
  -> network/profile/size/expiry check
  -> digest, Demand Mutation chain, and replay check
  -> historical signature/delegation verification
  -> current buyer-Agent/delegation authorization-eligibility check
  -> observed mutation-chain integrity, source-freshness, and fork check
  -> cheap typed skill and policy filter
  -> bounded supporting-material retrieval
  -> exact skill/evidence/capacity match
  -> deterministic cost, risk, and expected-profit calculation
  -> reject, recommend, approval-required, or policy-gated auto-offer intent
  -> exact owner one-shot or policy-gated path only:
     acquire process lock + Provider writer lease
  -> preallocate durable Offer ID + construct canonical Quote-binding body
  -> derive body digest + stable semantic action ID
  -> private portfolio reservation + runtime capacity lease
  -> Provider-wide custody admission + Provider authorization
```

Expensive model calls, bounded public supporting-material downloads, and
capacity estimation occur only after cheaper verification and local policy
checks. `reject` creates no commercial state. `recommend` or
`approval-required` may retain a bounded, expiring unsigned structured proposal
for explanation, but creates no canonical market body, Provider Offer, durable
portfolio/runtime reservation, custody admission, or signature. After approval,
OpenFox re-reads
authority and terms, but the approval record alone still grants no signing call
or persistent mode increase. Only a separately authenticated exact one-shot
Offer authorization, or an already active policy-gated mandate, may enter the
body-before-reservation sequence above. The one-shot path authorizes only the
revalidated proposal digest and does not enable later Offers. Private input and
upload challenges do not enter discovery evaluation. A buyer cannot force an
OpenFox instance to spend unbounded resources merely by publishing validly
signed demand.

The earning coordinator stores:

- exact observed Demand Mutation chain and digests, source/freshness bounds, and
  any head assertion or equivocation evidence;
- every source observation used;
- verification and finalized-checkpoint references;
- skill, estimator, cost, risk, policy, and mandate versions;
- rejection reasons or authorized structured offer;
- idempotency and ambiguous-send state;
- any later Quote, escrow, execution, Receipt, and settlement references; and
- terminal revenue and cost reconciliation.

Discovery observations never share the buyer-side opportunity coordinator's
spending authority. Buying and earning remain separate control planes.

## 13. Work-square application boundary

FreeCity, OpenFox UI, a UUMIT-like managed market, or another application may
render:

- recently observed work;
- tasks matching the local Agent's approved skills;
- estimated net profit and worst-case exposure;
- fixed-price versus offer-required opportunities;
- expiring, withdrawn, or superseded listings;
- offers awaiting a buyer response;
- accepted and executing work;
- result-ready and settlement-pending receivables; and
- independently finalized earnings.

Every item displays its evidence class, such as:

```text
channel-observed
gateway-observed
signature-verified
buyer-agent-finalized
offer-sent
selection-noticed
accepted-quote-finalized
escrow-funded-finalized
receipt-verified
provider-credit-finalized
```

The UI must not collapse these labels into one “verified job” or “earned”
state. It also reports source coverage, last synchronization time, local
filters, hidden/moderated events, and unresolved conflicts.

The UI renders `expired`, `terminal-withdrawn`, `locally-hidden`, and
`unavailable` separately. It must never label any of them `deleted` or “removed
from the network,” because public replicas may retain the immutable bytes.

FreeCity-local accounts, social relationships, follows, recommendations,
moderation, and ranking may improve discovery. They do not authorize a market
artifact or alter TOS commercial truth. An OpenFox instance can use the
protocol without FreeCity.

The same rule applies to every market application. It may operate a centralized
database, choose whom it serves, charge an explicitly disclosed application
fee, provide fiat or compliance workflows, or offer human support. Those are
valuable application services. A private lead may exist only inside that
application before acceptance and may disappear with it. Once an application
participates in a TOS-native accepted purchase, however, the exact signed
artifacts and finalized transaction must remain independently verifiable and
recoverable without its account or order database. A separate membership or
matching fee remains under the application's disclosed terms. Any deduction,
split, or routing through TOS settlement requires a supported pre-acceptance
Quote/escrow profile; objective V1 pays the fixed full amount only to the
Provider, and a database-side fee schedule cannot mutate that obligation.

No TOS-operated canonical Work Square is required for protocol conformance.
Reference applications and Gateways exist to demonstrate interoperability and
may compete with independent markets, but they have no privileged namespace,
ranking, listing, or matching authority.

## 14. Privacy and information disclosure

Public paid demand inevitably reveals some combination of buyer identity,
timing, task category, budget, and demand frequency. The publisher chooses a
public or private carrier under owner policy and sees a semantic confirmation
of the metadata before signing. That confirmation explicitly states that
public publication, caching, republication, and content-addressed Storage may
be permanent: expiry, terminal withdrawal, moderation, and deletion requests
cannot guarantee erasure by third parties. Sensitive demand defaults to direct
or private carriers.

V1 minimizes public data:

- publish digests and bounded descriptors instead of bulk input;
- keep private repository access and credentials outside the envelope;
- deliver sensitive input only to the selected provider under the accepted
  transport policy;
- send Provider Offers directly rather than broadcasting losing prices;
- use short bounded publication and offer expiries;
- avoid public model traces, private cost estimates, or portfolio state; and
- never include keys, bearer tokens, session material, or private host paths.

Encryption protects content in transit but not all metadata. DHT, Overlay,
Gateway, Storage, and Messenger operators may observe timing, volume, peer, or
topic information according to their transport positions. Production profiles
must document those exposures rather than claim anonymity.

## 15. Abuse and market-integrity controls

The system assumes malicious publishers, carriers, providers, and content.
Minimum controls include:

- strict byte, field, nesting, page, pending-candidate, and time bounds;
- exact network and profile allow-lists;
- finalized buyer Agent verification before expensive evaluation;
- per-source and per-buyer quotas and circuit breakers;
- short expiries and bounded Demand Mutation history;
- digest deduplication and equivocation quarantine;
- local topic, buyer, task, asset, and risk policies;
- content retrieval only through approved, size-bound, digest-checked paths;
- no task-selected tool, plugin, model, credential, endpoint, or network access;
- no automatic execution before finalized Quote and escrow verification;
- no revenue recognition before finalized provider credit; and
- durable adverse evidence that self-learning cannot erase.

Spam policy is local and plural. One channel may moderate an event and another
may carry it. No moderator becomes universal truth. OpenFox can use multiple
sources while applying one owner policy consistently.

Sybil resistance cannot be solved by signatures alone because an attacker may
control many valid Agent identities. The first implementation must measure
spam and evaluation costs before choosing fees, bonds, proof of work,
reputation inputs, or issuer admission. Any later mechanism must remain
explicitly scoped and cannot become a parallel identity or settlement system.

## 16. Failure and recovery

### Source failure

An unavailable channel replica, Gateway, indexer, DHT peer, or Storage provider
removes only that source. Other configured sources continue within their own
bounds. If all sources fail, discovery becomes unavailable; it does not fall
back to stale or unverified data.

### Cursor and history failure

Each source cursor advances only after the exact observed artifacts and local
application state are durably committed. Cursor corruption, history gaps,
forks, invalid snapshots, and stale completions fail closed. Recovery resumes
from the last verified source-specific checkpoint and deduplicates by immutable
event and envelope identity.

### Ambiguous market mutation

Demand Mutation, Offer, and Selection Notice delivery may fail after the
remote side has accepted bytes. Each mutation requires a stable action identity
and a resolution operation or acknowledgement rule. A timeout alone does not
authorize replay. Unresolvable ambiguity remains visible until expiry or owner
intervention.

### Acceptance and settlement failure

After Accepted Quote finality, public-feed state is irrelevant to recovery.
Quote acceptance, later asynchronous funding, execution, Receipt, refund, and
settlement recovery follow
[`PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md`](PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md)
and the existing commercial specifications. Gateway, channel, conversation,
and work-square loss must not prevent independent reconstruction.

## 17. Repository ownership

| Repository | Responsibility |
|---|---|
| `tos-service-spec` | Paid Demand/Mutation, Provider Offer, market delegation, carrier/query schemas, bounds, signatures/digests, public errors, vectors, and discovery acceptance evidence; the separate binding profile owns the existing-rail adapter |
| `tos-service-protocol` | canonical artifact codecs and verification, finalized buyer/provider checks, federation client, offer/Quote SDK, error classification, and recovery helpers |
| `tos-service-gateway` | optional authenticated Demand Mutation/relay endpoints, bounded derived search, source provenance, cursors, filtering, and federation conformance |
| `tos` | generic DHT, Overlay, ADNL/RLDP, Storage, Agent, and the existing Accepted Quote, escrow, Receipt, and settlement primitives/contracts; no market search, ranking, or demand-wide selection contract in V1 |
| `tos-messenger` | paid-demand public-channel profile, verification, synchronization and persistence integration over TOS networking primitives; direct offer transport; event replay protection; moderation projection |
| `openfox` | source configuration, local durable aggregation, typed matching, economics, portfolio policy, owner-private process lock, Provider writer-lease client/recovery, Provider Offer/later-bid authorization, explanation, and commercial orchestration |
| `tos-ai` | implementation and operation of spec-defined task/execution/validator/evidence/private-input profiles, estimates, durable Offer-bound runtime capacity leases, bounded execution, validation, and artifacts |
| `freecity` | optional work-square experience, local social discovery, moderation, approvals, and labelled projections |
| custody tools | Provider-wide exclusive writer lease/fencing generation, durable unresolved-Offer/obligation and aggregate-exposure admission ledger, stable-action replay/conflict handling, exact market/Quote semantic confirmation, delegated signing, broadcast, ambiguous-submit resolution, and revocation without exposing keys to OpenFox |

No repository may copy candidate fields into a private schema and later present
that schema as a frozen protocol. If the profile is approved, normative
messages start in `proto/tos/service/v1/native.proto` and include independent
vectors before downstream release.

## 18. Candidate service boundaries

Exact RPC names remain unfrozen. The future protocol needs transport-neutral
operations equivalent to:

```text
PublishDemandMutation(exact signed mutation)
  -> source-local observation and stable mutation identity

SearchPaidDemand(network, typed filters, page size, source cursor)
  -> exact envelopes, per-result provenance, next source cursor

GetDemandMutations(exact demand identity, optional sequence range)
  -> exact observed mutation chain or explicit incomplete/forked result

ResolvePaidDemandReference(exact compact reference, local source policy)
  -> exact verified envelope, mutation status, and per-source provenance

SubmitProviderOffer(exact signed offer)
  -> peer/source acknowledgement with ambiguity-resolution identity

ResolveMarketMutation(stable mutation identity)
  -> unknown | durably observed(exact digest) | conflict(exact digests)
```

Public-channel carriage may implement publish and synchronize without a
Gateway RPC. Direct Messenger may implement offer delivery without a Gateway.
All carriers map to the same eventual artifact schema and verification rules.

Errors distinguish at least:

- permanent invalid input;
- unsupported profile or network;
- unauthorized publisher;
- stale, expired, terminal-withdrawn, superseded, incomplete, or forked
  mutation chain;
- exact replay;
- conflicting identity reuse or equivocation;
- bounded resource exhaustion;
- retryable source unavailability; and
- ambiguous mutation requiring resolution before retry.

## 19. Implementation sequence

### Phase D0 — specification freeze decision

- confirm that paid-demand discovery advances the initial software-work
  commercial lifecycle and measurable market usage;
- select the fixed-price task subset and anti-abuse rule;
- decide the one canonical artifact source: Native protobuf, an Agent Packet
  payload profile mapped into Native protobuf, or another approved single
  representation;
- freeze the Paid Demand Reference mandatory core, optional hint grammar,
  content-digest algorithm, URI/QR encoding, resolver behavior, and bounds;
- freeze Demand Mutation sequence/terminal/fork rules, the explicit
  non-canonical-head boundary, market scopes, portable historical authority
  proofs, acceptance-time revocation ordering, messages, bounds, ordering,
  digest/signature domains, expiry, errors, and retry behavior;
- freeze the mutation-bound `BuyerHandoffProfile`, per-Offer deterministic
  identity, and Provider-private fencing/admission invariants here, while the
  separate binding profile freezes the typed body, Provider proof, versioned
  existing Quote/escrow handoff, proof-of-possession private-input push, and
  existing Gate comparisons;
- produce positive vectors and adversarial mutations; and
- obtain independent parser/vector consumption.

### Phase D1 — local read-only feed

- generate signed synthetic fixed-price demand;
- implement one local public-channel or fixture carrier;
- resolve one Paid Demand Reference from that carrier and a restartable local
  cache;
- implement protocol verification and an OpenFox source cursor;
- perform typed matching and deterministic economic simulation; and
- prove that no Provider Offer, custody/market signing request, execution, or
  spend is reachable.

### Phase D2 — multi-source public testnet discovery

- operate at least two independent carriers or indexes;
- add client-side federation, provenance, deduplication, Demand Mutation,
  terminal withdrawal, equivocation, and source failure;
- exchange one compact Paid Demand Reference out of band, retrieve the exact
  envelope after its first source stops, and retain all provenance;
- publish and recover a verified public-channel Storage snapshot;
- compare independently produced search projections under the Section 9.1
  operator/implementation/failure-domain evidence rules;
- permit no Provider Offer, Selection Notice, Quote construction, execution, or
  automatic commercial authorization.

### Phase D3 — guarded fixed-price response

- begin only after the complete D2 two-source, source-plus-database shutdown,
  and independent-codec/verifier gate, and after the market delegation, Demand
  Mutation/non-canonical-head boundary, mutation-bound `BuyerHandoffProfile`,
  Provider Offer authorization, Provider-wide writer fencing and
  aggregate admission, deterministic per-Offer existing Quote/escrow handoff,
  existing Execution Gate integration, per-Offer single-acceptance, and proof-
  of-possession private-input profiles—including `InputAcceptanceRecordV1` and
  complete acceptance-to-funding, funding-to-input, and input-to-admission
  margins—have frozen vectors and implementations;
- add direct signed single-acceptance Provider Offers and mutation resolution;
- add proposal-only OpenFox recommend mode plus a distinct exact one-shot owner-
  authorization path that does not widen the persistent mode;
- construct the one Offer-specific versioned existing Accepted Quote and escrow
  from the typed Quote-binding body and Provider proof;
- permit permissionless deterministic predeployment only into
  `pending_acceptance`; distinguish finalized Quote acceptance by the bound
  buyer wallet's `accept` transition from the later exact asynchronous
  stablecoin funding state;
- push private input only through the Offer-bound proof-of-possession Provider
  ingress, whose atomic signed acceptance record proves the separate delivery
  deadline before later Gate admission;
- execute through the Native Execution Gate; and
- reconcile one finalized provider-wallet credit.

### Phase D4 — bounded policy-gated operation

- install an expiring owner mandate and small exact-asset exposure limits;
- add automatic Provider Offer only for the accepted fixed-price profile;
- run pause, drain, revocation, crash, malicious-source, objective release, and
  timeout-refund exercises; and
- collect independent recurring-use evidence before competitive bidding or
  additional profiles.

These phases do not reorder `ROADMAP.md`. Incubation and same-host evidence
cannot open an external acceptance or Expansion Gate. D3 and D4 remain blocked
until every prerequisite named above is complete; D1/D2 evidence cannot be
used to infer executable commercial safety.

## 20. Conformance and adversarial tests

### Artifact verification

- exact positive active/terminal Demand Mutation, market delegation,
  mutation-bound `BuyerHandoffProfile`, single-acceptance Provider Offer,
  and non-authoritative Selection Notice vectors;
- exact positive Paid Demand Reference parse/render vectors with and without
  optional source hints;
- wrong network, buyer, provider, Capability, version, asset, or profile;
- malformed signature, wrong market purpose, cross-purpose substitution,
  over-scoped/expired delegation,
  wrong Agent generation/policy digest/checkpoint, rotation, recovery, and
  revocation, including ambiguous same-checkpoint/cross-shard acceptance order;
- zero/duplicate nonce, mutation sequence skip, stale predecessor, active
  descendant after terminal withdrawal, fork/equivocation, late arrival, and
  exact replay;
- expired publication or offer and invalid deadline ordering;
- unknown fields, trailing data, non-canonical ordering, and every over-bound
  field or collection;
- malformed URI encoding, duplicate/unknown parameters, unsupported digest,
  ambiguous network, oversized hints, hint substitution, and mandatory-core
  mutation;
- task description attempting to override structured commercial terms;
- missing, malformed, unauthorized, expired, or unresolvable buyer handoff
  profile; Messenger, Selection Notice, Gateway, or index completion of a
  missing field; successor-profile substitution into an old Offer; and
  Demand-proof or upload-key rotation/substitution after Provider signing.

### Existing-rail binding

Canonical body/proof construction, one-Offer/one-Quote derivation, separate
Quote-acceptance and funding finality, private-input delivery, existing Gate
integration, and commercial recovery are tested under
[`PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md`](PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md).
This discovery suite must consume those frozen vectors but does not redefine
their transaction semantics.

### Distribution

- duplicate delivery through channel, Gateway, direct source, and Storage;
- one Paid Demand Reference resolving to the same exact envelope through each
  supported carrier independently;
- dead, malicious, mismatching, private-network, redirecting, and
  credential-capturing reference hints;
- malicious peer omission, replay, flood, delay, and altered bytes;
- DHT locator substitution and Storage snapshot mismatch;
- incomplete history, forked head, cursor corruption, and restart;
- one unavailable or malicious index among valid independent sources;
- deterministic local deduplication with retained provenance; and
- moderation hide/restore without semantic mutation.

### OpenFox

- cheap checks precede expensive evaluation;
- source, buyer, candidate, bytes, model-call, and wall-time budgets;
- exact skill/evidence/capacity mismatch rejection;
- stale cost estimate and integer overflow refusal;
- simultaneous candidates cannot double-claim budget or capacity;
- two local writers for one state directory, two partitioned cross-host writers,
  stale fencing generation after takeover, two signer keys/mandates sharing one
  Provider scope, aggregate exposure overflow across different Offers, and
  loss/rollback/ambiguous migration of the Provider admission ledger;
- restore of a snapshot below the generation/issuance high-water mark, custody
  TTL above its protocol cap, signing-key disablement, authority
  revocation/rotation, and conservative outstanding-Offer resolution;
- task-selected skill, plugin, model, credential, host, and network attacks;
- offer send ambiguity and safe expiry;
- atomic Offer capacity reserve/convert/release and simultaneous acceptance;
- withdrawal, expiry, reject, failure, or cancellation racing Quote finality in
  both observation orders, including restart in `CANCELLATION_RESOLVING` and a
  post-acceptance Demand withdrawal that cannot undo the obligation;
- pause, drain, mandate expiry, and custody revocation;
- restart at every discovery, evaluation, Offer reservation/signing, delivery,
  selection-notice, and Quote-resolution boundary; and
- consumption of the separate binding profile's frozen private-input, Gate,
  Receipt, and recovery vectors without redefining them here.

### Optional market applications

- application `accepted`, `funded`, `completed`, balance, order, ranking, and
  support fields cannot advance a protocol evidence class;
- application login cannot substitute for a finalized TOS Agent, wallet,
  delegation, or Provider proof;
- regions, mirrors, or API endpoints sharing one application account/order
  database count as one D2 source;
- application removal cannot create a Demand terminal withdrawal, cancellation,
  refund, or settlement outcome;
- an application-local lead remains display-only until converted into and
  independently verified as the exact artifact required by its origin lane; and
- after acceptance, deletion of the application database does not prevent
  Quote, escrow, Receipt, or settlement reconstruction.

### End-to-end

- buyer publishes into at least two source paths satisfying every Section 9.1
  operator, implementation, upstream, store, network-path, and failure-domain
  independence requirement;
- the two independent sources expose the same exact envelope with distinct
  provenance and explicitly incomplete coverage;
- provider discovers through one of those qualified paths and sends one signed
  offer;
- one qualified source path and its complete persistent store become unavailable
  before acceptance while the other still resolves and exposes the exact bytes;
- a paired lane test keeps Capability-first schema-1 deployment acceptance and
  Demand-first successor bound-wallet acceptance distinct, without
  reinterpretation;
- the Provider authorizes one canonical `PaidDemandQuoteBindingBodyV1`, including
  its exact portable authority-reference digest;
- a second Provider supplies a competing independently valid Offer, and the
  buyer selects one locally without claiming a global winner;
- the selected exact Offer deterministically produces one existing escrow;
  third-party predeployment creates no authority, the bound buyer wallet's
  finalized `accept` transition creates the Accepted Quote, and later exact
  stablecoin funding creates execution eligibility;
- buyer pushes the exact private input to the Offer-bound provider ingress;
- provider executes once, produces evidence and Receipt, and receives payment;
  and
- a third resolver reconstructs the complete canonical commercial history
  without any market index or Messenger database.

## 21. V1 acceptance criteria

V1 is accepted only when:

1. two independent implementations reproduce all frozen market-artifact
   digests and reject the adversarial corpus;
2. one signed demand is propagated without a central message database;
3. one compact Paid Demand Reference retrieves the same exact signed envelope
   after its original source disappears;
4. two sources satisfying Section 9.1 operator, implementation, upstream, and
   failure-domain independence expose it with explicit incomplete coverage and
   distinct provenance;
5. an OpenFox provider verifies historical authorization, current Agent/
   delegation eligibility, and the integrity/freshness of the exact observed
   active Demand Mutation while explicitly not claiming a globally complete
   feed head, and verifies the complete mutation-bound
   `BuyerHandoffProfile`, before performing expensive evaluation;
6. typed skill, evidence, capacity, exact-asset economics, and owner policy
   produce a reproducible decision;
7. one idempotent, single-acceptance signed Provider Offer reaches the buyer,
   reserves capacity atomically, passes Provider-wide writer fencing,
   unresolved-tuple and aggregate-exposure admission across every shared
   key/mandate/instance, and survives sender and receiver restart;
8. same-host process locking rejects a second writable OpenFox, custody rejects
   a stale or partitioned writer generation, and a replacement writer inherits
   every unresolved Offer before it may sign;
9. every acceptance criterion in
   [`PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md`](PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md)
   passes, including one Offer-specific Quote/escrow identity, separate Quote-
   acceptance and funding finality, Offer-bound input, existing Gate admission,
   Receipt/release/refund reuse, and finalized provider credit; and
10. no Gateway, channel, Relay, index, FreeCity database, OpenFox journal, or
    Provider-private admission ledger is required to reconstruct the existing
    canonical settlement.

## 22. Explicit non-goals

V1 does not create:

- one global job board or globally complete order book;
- one required market-operated Agent directory, hosted service catalog, market
  operator, or hosted search/chat/event backend; finalized Native Registry state
  for Agent and Capability accounts remains canonical protocol authority;
- a protocol-mandated market commission, platform treasury, sponsored rank, or
  centrally selected Provider;
- a mutable location-dependent job identity or authoritative source-hint
  registry;
- consensus over search results, ranking, moderation, availability, or profit;
- a Gateway-controlled buyer identity, balance, acceptance, or reputation;
- natural-language authorization for offers, execution, or payment;
- public storage of bulk private task input or losing Provider Offers;
- automatic parsing of ordinary chat into commercial artifacts;
- universal subjective-work arbitration;
- automatic subcontracting, recursive tasks, or provider composition;
- an on-chain transaction for every advertisement or offer;
- a globally unique Provider winner or cross-escrow selection contract;
- a new stablecoin, external-chain asset, or Gateway ledger;
- policy or authority expansion through OpenFox self-learning; or
- production or roadmap acceptance from design, local tests, or same-host
  operation.

## 23. Open decisions before schema freeze

The architecture review closes four directional questions: V1 uses one
monotonic Demand Mutation chain with terminal withdrawal, separate
purpose-limited market delegations, single-acceptance Provider Offers with
typed Quote-binding convergence, and buyer push to a Provider-bound private
input ingress. V1 deliberately adds neither a post-Offer buyer Agent signature
nor a demand-wide selection contract: the versioned escrow's bound-buyer-wallet
`accept` transition is commercial acceptance, permissionless deployment alone
is not, and different funded Offers are independent purchases. Schema freeze
must still decide the exact encodings and bounds:

1. Is the single canonical envelope a Native protobuf message carried inside
   Messenger events and Gateway RPCs, or an Agent Packet payload with a
   one-to-one Native mapping?
2. Which exact numeric purpose bits/scopes, single delegated Ed25519 key,
   canonical signature/proof encoding, delegation schema and static bounds,
   portable historical authority proof, policy/generation
   commitment, checkpoint proof, lifetime, and revocation lookup encode
   `paid-demand.publish`, `paid-demand.withdraw`, and
   `provider-offer.sign`?
3. Which fixed-price software-work operations and spec-defined execution,
   validator, and evidence profiles form the first safe demand subset?
4. Does V1 require a funded-intent proof or only finalized buyer identity and
   local rate limits before offer evaluation?
5. What exact `PaidDemandQuoteBindingBodyV1`, Provider proof,
   `PaidDemandQuoteBindingV1`, Accepted Quote schema successor, escrow
   StateInit/code identity, resolver response, Gate mapping, and safe-handoff
   representation freeze the separate binding matrix without circular signing
   or duplicating existing Receipt authority?
6. Which exact compatibility and rollout rules allow the versioned binding
   while leaving all schema-1 Accepted Quotes and escrows unchanged?
7. What provider ingress authentication, buyer upload proof-of-possession key,
   challenge/status format, encryption, maximum bytes/files, retention,
   revocation, acknowledgement, and recovery rules freeze the buyer-push
   private-input profile?
8. Which exact clock source and maximum lifetime govern Demand Mutation and
   Offer expiry before chain acceptance?
9. How are public opportunity channel profiles located without making a topic
   name, DHT record, publisher, or moderator universal authority?
10. Which digest algorithm, URI grammar, compact network encoding, maximum hint
    count, default-source behavior, and optional QR representation define the
    Paid Demand Reference?
11. What query and resolution operations make publication, terminal
    withdrawal, Offer delivery, result submission, and settlement retries safe
    after ambiguous transport results?
12. Which measured spam threshold justifies a bond or other economic
    anti-abuse mechanism?
13. What minimum independently controlled source diversity and public-network
    evidence is required before OpenFox policy-gated automatic offers may be
    enabled?
14. Which recurring external paid-use threshold permits competitive
    multi-offer bidding and the next task profile under the Expansion Gate?

Until these questions are frozen in the sole Native schema and independently
tested, implementations may provide only read-only discovery and local
simulation. D2 may exercise public-testnet propagation without Provider
Offers. D3/D4 commercial actions remain prohibited.
