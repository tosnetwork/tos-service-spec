# Agent Paid Demand Discovery V1

**Status:** incubation design; schema freeze, implementation, and external
acceptance pending

**Blocking status:** D3 Provider Offer acceptance and D4 automatic commercial
action are blocked until the complete D2 gate demonstrates two Section 9.1-
independent sources, source-plus-database shutdown recovery, and a second
independent codec/verifier, and until the P0/P1 prerequisites in Sections 11.4
through 11.6 are frozen, implemented, and covered by independent vectors.

**Protocol:** `tos_service_v1`

## 1. Purpose

This document defines how Agents may publish, propagate, find, verify, and
respond to paid work opportunities without a central marketplace or a
canonical market database.

The product may render this system as a job board, opportunity feed, or work
square. Those are user experiences, not protocol authority. The protocol
boundary is a bounded signed paid-demand envelope distributed through
replaceable carriers and indexes, followed by an extended finalized Accepted
Quote, escrow, execution, Receipt, and settlement lifecycle.

The target interaction is:

```text
buyer Agent publishes signed paid demand
  -> public channels and independent indexes propagate it
  -> provider OpenFox instances merge, verify, match, and price locally
  -> each provider constructs one body and returns its signed Provider Offer
  -> buyer selects one Offer and authorizes the same body
  -> buyer wallet atomically consumes the Demand Acceptance Key
  -> finalized Accepted Quote and funded escrow for the one winner
  -> bound execution, Receipt, and finalized provider credit
```

This design specializes the opportunity-discovery portion of
[`OPENFOX_AUTONOMOUS_EARNING_CROSS_REPOSITORY_DESIGN.md`](OPENFOX_AUTONOMOUS_EARNING_CROSS_REPOSITORY_DESIGN.md).
The corresponding OpenFox-local package, state-machine, economics, policy,
accounting, configuration, operator-interface, and observability plan is
defined in
[`OPENFOX_AUTONOMOUS_EARNING_IMPLEMENTATION_PLAN.md`](OPENFOX_AUTONOMOUS_EARNING_IMPLEMENTATION_PLAN.md).
That plan is non-normative; this document and the cross-repository design
govern market artifacts and authority.
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
- one selected provider and one extended Accepted Quote/escrow lifecycle that
  binds typed accepted work terms;
- exact TOS-network stablecoin identity for the service payment;
- native TOS used separately for network fees; and
- objective completion, release, or refund under existing software-work rules.

Competitive price revision may follow the fixed-price path. Subjective work,
general arbitration, sealed-bid auctions, provider subcontracting, GPU markets,
payment channels, additional task profiles, and cross-network markets remain
outside V1 and behind their existing roadmap gates.

### 2.1 Current implementation gaps

The surrounding repositories contain reusable identity, public-channel,
discovery, execution, and settlement foundations, but the paid-demand network
defined here is not implemented end to end. In particular, the following are
missing:

1. Native protobuf messages for Paid Demand Mutation, Provider Offer,
   Selection Notice, accepted work terms, and their query/result envelopes;
2. frozen content-identity, canonical encoding, digest, signature, delegation,
   expiry, and Demand Mutation domains with cross-implementation vectors;
3. a typed `paid-demand` public-channel event profile in `tos-messenger`;
4. bounded Gateway publication, withdrawal, lookup, search, mutation-
   resolution, cursor, and provenance interfaces;
5. an OpenFox multi-source synchronizer with durable per-source cursors,
   deduplication, equivocation detection, local matching, and economic policy,
   plus the D2 two-independent-source shutdown test and second independent
   codec/verifier required before commercial action;
6. a signed single-acceptance Provider Offer transport, deterministic
   Quote/escrow derivation, and safe buyer-selection handoff;
7. opportunity-channel topic, profile, bootstrap, subscription, and
   republication rules;
8. independent public-network evidence for Overlay, DHT, Storage, Gateway, and
   direct-offer paths;
9. a measured anti-spam and false-buyer policy that bounds provider evaluation
   cost without creating Gateway authority;
10. a compact Paid Demand Reference, informally an **Opportunity Magnet**, that
    lets an Agent retrieve the exact signed envelope from multiple independent
    carriers by content identity;
11. a complete mutation-bound `BuyerAcceptanceProfile` fixed before Provider
    signing, plus a typed accepted-work body and reconstructible buyer-acceptance
    and provider-offer authorization proofs binding buyer Agent/wallet/key,
    Demand Mutation, Provider Offer, upload key, input/source, task/evidence
    profiles, and delivery/refund conditions into the finalized Quote and
    escrow;
12. market-specific bounded delegation scopes with historical and current
    authorization verification, portable finalized authority references, and
    acceptance-time revocation ordering;
13. a private-input delivery profile that never lets remote task data select a
    provider network target or credential;
14. a Provider-private, rollback-resistant writer lease/fencing and aggregate-
    exposure admission boundary spanning every shared OpenFox instance, signer
    key, mandate, runtime, unexpired Offer, and unsettled obligation without
    leaking that private state into public market artifacts; and
15. a deterministic contract-enforced Demand Acceptance Key whose first
    finalized atomic consumption selects one Provider across every competing
    Offer and Mutation of the V1 Demand.

Existing group chat, public-channel primitives, Capability search, Quote,
escrow, executor, Receipt, and settlement code must not be represented as
closing these gaps. They are dependencies on which this profile can be built.

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
- establish a Receipt or dispute outcome; or
- recognize settled provider revenue.

Finalized TOS state remains the sole canonical authority for those facts.

### 3.3 Do not put the public market feed on-chain

Task advertisements, search impressions, offer revisions, and unsuccessful
bids are frequent, short-lived, privacy-sensitive, and mostly non-winning.
Putting them all in consensus would add cost, latency, spam, permanent data,
and privacy leakage without strengthening the winning commercial commitment.

TOS finality begins to control the opportunity only when the selected exact
terms become an Accepted Quote and funded escrow. Bulk task inputs, outputs,
conversation history, and evidence remain off-chain and are bound by immutable
digests where required.

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

### Buyer Acceptance Profile

The canonical buyer-side authorization and upload context embedded in every
Active Revision. It fixes the exact `accepted-work.accept` key, delegation and
proof commitments, portable authority-reference digest, settlement wallet,
and dedicated upload proof-of-possession key before any Provider signs.
Transport prose cannot complete or replace it.

### Terminal Withdrawal

A `DemandMutation` whose kind permanently closes the demand for new offers.
V1 does not permit reopening after terminal withdrawal. It cannot cancel an
already finalized Accepted Quote or erase previously distributed bytes.

### Provider Offer

A provider-originated signed response binding one active Demand Mutation to an
exact provider, Capability version, execution profile, price, delivery interval,
and expiry. V1 fixes `max_acceptances = 1`. It is not an Accepted Quote.

### Demand Acceptance Key

The deterministic TOS contract key shared by every Mutation and Provider Offer
under one stable Demand identity. V1 atomically consumes this key at most once
when the buyer wallet finalizes an Accepted Quote, thereby selecting one
Provider across all competing Offers and all revisions of that Demand. It is
accepted-work authority, not a global market head or marketplace database.

### Selection Notice

A buyer-originated non-canonical notice that one offer is expected to be
converted into an Accepted Quote. It does not prove acceptance or funding.

### Opportunity Carrier

A public channel, direct Messenger path, Gateway, indexer, or application API
that transports or indexes immutable market artifacts.

### Opportunity Index

A replaceable local projection used for filtering and search. Its coverage,
freshness, ranking, and moderation are non-canonical.

### Work Square

An application view over locally observed demand, offers, and finalized
commerce. It is not a protocol object.

## 5. Authority matrix

| Fact | Authority | Non-authoritative observations |
|---|---|---|
| buyer Agent identity and live controller policy | finalized TOS Agent state | display name, channel profile, Gateway account |
| exact paid-demand bytes and historical origin | signature, delegation, generation/policy digest, and portable finalized issuance-authority verification under the market signing profile | channel author label, TLS origin, index row, bare checkpoint number |
| buyer pre-Offer acceptance and upload context | exact `BuyerAcceptanceProfile` inside the signed active Demand Mutation plus historical/current delegation verification | Messenger prose, Selection Notice, Gateway field, Provider guess |
| locally offer-eligible demand observation | verified observed Demand Mutation chain, current live Agent/delegation eligibility, source coverage, and freshness | another observer's “open” badge, any claim of a globally complete head |
| provider identity and Capability/version | finalized TOS Agent and Capability state | offer text, local skill name, Gateway metadata |
| offer origin | candidate offer signature under the approved signing profile | Messenger prose, index ranking |
| buyer selection before acceptance | negotiation input only | Selection Notice, conversation statement |
| one selected Provider for a V1 Demand | first finalized atomic consumption of the Demand Acceptance Key, recording the exact Mutation, Offer, accepted-work terms, Quote, and escrow | Selection Notice, buyer signature alone, Provider Offer, Gateway status, or per-Offer `max_acceptances` |
| accepted work terms and execution authority | finalized Accepted Quote and escrow containing the reconstructible typed accepted-work body, buyer acceptance authorization, provider offer authorization, and exact buyer-wallet acceptance transaction | demand, opaque Offer digest, Selection Notice, or Gateway acknowledgement |
| execution admission | shared Native Execution Gate over finalized state | task status, delivery ACK, model output |
| successful result commitment | canonical signed Receipt under accepted terms | process exit, chat message, artifact URL |
| provider revenue | finalized exact provider-wallet credit | quoted price, release intent, dashboard balance |

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
`BuyerAcceptanceProfile` defined in Sections 6.3 and 6.6. A
`terminal_withdrawal` contains no replacement acceptance or upload profile.

### 6.2 Task profile and requirements

Each demand carries bounded structured requirements:

- task-profile identifier and version;
- human-readable summary treated as untrusted display text;
- required Capability predicates;
- input media type and immutable input commitment;
- required output media types;
- objective validator and evidence-profile identifiers;
- execution resource class and maximum completion duration;
- delivery deadline and any earlier offer deadline;
- accepted transport profiles; and
- dispute/refund profile compatible with the selected software-work profile.

Capability predicates are exact structured filters, not natural-language
authority. A free-form description may improve discovery but cannot change the
input commitment, success rule, resource limit, evidence obligation, or
commercial terms.

Bulk source archives, prompts, credentials, private repository URLs, personal
data, and secret acceptance tests are not published in the public envelope.
The envelope commits to the required bytes and bounds, never a provider-fetch
URL or buyer credential. Disclosure uses the buyer-push profile in Section
11.6 only after finalized acceptance and funding.

### 6.3 Commercial terms

Each V1 demand carries:

- a complete `BuyerAcceptanceProfile` containing the buyer Agent ID, equal to
  the envelope buyer, exact settlement-wallet commitment, exact
  `accepted-work.accept` delegated Ed25519 public key/key ID, buyer Agent
  generation and controller-policy digest, exact delegation, typed delegation-
  bounds and owner-mandate digests, authorization validity interval, canonical
  proof/profile version and signature encoding, portable finalized issuance-
  authority reference digest, and a dedicated upload proof-of-possession public
  key/key ID, proof algorithm/profile version, and input-delivery validity
  bounds;
- exact TOS-network asset identity;
- fixed provider-service payment in unsigned atomic units;
- explicit statement of who pays network and protocol fees;
- offer deadline, execution deadline, and refund deadline constraints;
- V1 `max_selected_providers = 1`, enforced by one Demand Acceptance Key shared
  across every Mutation and Offer under the stable Demand identity;
- Accepted Quote and escrow profile requirements;
- required provider Capability/version and execution-signer bindings; and
- any objective cancellation or dispute inputs allowed by the selected
  existing profile.

The dedicated upload key has no wallet, Agent-control, market-signing,
settlement, or read authority. It proves possession only when pushing the one
input already committed by the accepted terms.

A ticker, exchange-rate estimate, Gateway balance, external-chain token, or
custodial credit is not a valid asset identity. Monetary authorization uses
checked integer atomic units. A later UI may display converted estimates but
they never change signed terms.

The complete buyer acceptance and upload context is part of every
`active_revision` canonical preimage. The `paid-demand.publish` signature
authenticates that commitment but does not itself accept later work; the named
`accepted-work.accept` key must separately authorize the exact
`AcceptedWorkBody`, and the named upload key must separately prove possession
for the bound private-input request.

A Provider constructs the candidate `AcceptedWorkBody` only from this exact
mutation-bound context plus Provider-selected fields. It never guesses a live
buyer delegation and never obtains a key, proof profile, authority reference,
wallet, or upload key from a Selection Notice, ordinary Messenger content, or
Gateway metadata. An active mutation missing any required context is
display-only and cannot receive a Provider Offer.

Changing the buyer acceptance key, delegation/mandate, proof profile,
authority-reference digest, settlement wallet, or upload proof-of-possession
key for future Offers requires a new complete `active_revision` with the next
sequence and exact predecessor. Revocation or expiry before Quote finality
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
accepted-work.accept
```

`active_revision` requires `paid-demand.publish`; `terminal_withdrawal`
requires `paid-demand.withdraw`; a Provider Offer requires
`provider-offer.sign`; and the buyer's final Agent-level approval of selected
terms requires `accepted-work.accept`. Cross-purpose substitution is invalid.
The exact buyer settlement wallet separately authorizes and funds the finalized
Quote transaction; the market or accepted-work delegation never becomes a
wallet key.

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
accepted-work/Quote/escrow code profiles, and owner-mandate digest. A verifier
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
`BuyerAcceptanceProfile`: the `accepted-work.accept` delegation, typed bounds,
validity, proof profile, and portable authority-reference digest must be
historically authentic and currently eligible before Provider reservation or
signing. The complete portable proof may be embedded or retrieved by content
identity, but failure to resolve it or reproduce its committed digest fails
closed. Messenger, Selection Notice, Gateway, index, and local-journal fields
cannot complete, normalize, or rotate the profile.

A Provider Offer becomes non-actionable before Quote finality if its provider
Agent, signing delegation, Capability/version, manifest, or reserved capacity
authorization is revoked, transferred, expired, or otherwise no longer valid.
The accepted-work resolver and Native Execution Gate prove from finalized
history that both market authorizations were valid at the Quote acceptance
checkpoint and that the acceptance transaction occurred no later than the
Offer deadline. Revocation finalized before acceptance invalidates the paid-
demand Quote even if an escrow account was deployed; revocation finalized only
after acceptance does not rewrite the finalized Quote. If the resolver cannot
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
attempts, and retains every local, Provider-private, and runtime reservation.
The Provider resolves the Demand Acceptance Key and its own deterministic Quote/
escrow at an adequate finalized checkpoint. A valid finalized acceptance of its
Offer converges to accepted work regardless of event arrival order; finalized
selection of a competing Offer makes this Offer non-acceptable. Only after the
Offer deadline and deterministic proof that neither its acceptance nor an
unresolved winner can still finalize may the Provider mark the Offer withdrawn/
expired and release once. After Accepted Quote finality, Demand withdrawal is
evidence only; cancellation requires the authoritative accepted-work/escrow
flow.

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
Provider signs the exact accepted-work body, the buyer supplies a distinct
accepted-work authorization, and the committed buyer wallet finalizes and
funds that body on-chain. A contradictory terminal withdrawal or head assertion
is durable buyer-equivocation evidence and causes refusal when known before
finality, but it cannot invalidate an already finalized bilateral Quote.
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
input delivery uses only the Offer-bound buyer-push profile in Section 11.6 and
retains its own authorization and retention rules.

### 8.5 Direct Messenger and private rooms

Direct conversations and private rooms may carry:

- invitation-only Paid Demand;
- provider questions;
- Provider Offers;
- Selection Notices;
- owner approvals; and
- accepted-work progress or result transport.

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

The response transport may be direct Messenger or a bounded Gateway relay. It
must preserve the exact signed offer bytes and must not become selection
authority.

### 11.2 Candidate offer contents

A Provider Offer binds at least:

- exact demand identity and active Demand Mutation digest;
- the stable Demand Acceptance Key and V1 `max_selected_providers = 1`;
- the complete mutation-bound `BuyerAcceptanceProfile`, including buyer Agent,
  settlement wallet, acceptance key/proof context, and upload proof-of-
  possession key/profile, without any Provider guess or post-Offer buyer choice;
- provider Agent ID;
- Capability ID and exact active version;
- manifest, task, input/source, execution, validator, evidence, private-input
  delivery, dispute, and refund commitments;
- fixed exact-asset price;
- delivery interval and offer expiry;
- `max_acceptances = 1`;
- one complete deterministic canonical `AcceptedWorkBody` with no buyer-
  substitutable commercial or execution field;
- provider-generated durable offer identity;
- reply or Quote-construction transport hint; and
- a reconstructible `provider-offer.sign` authorization over the exact
  `accepted_work_body_digest`, including the constrained delegation, owner-
  mandate digest, and portable finalized authority reference.

OpenFox may use a model to propose price or explanatory prose. Its deterministic
earning policy authorizes the exact structured offer, price floor, fee ceiling,
expiry, capacity reservation, and mandate version before signing.

Before reservation and signing, the Provider re-verifies the exact mutation-
bound `BuyerAcceptanceProfile` and requires the Offer-acceptance deadline to be
no later than the buyer acceptance delegation validity bound and every private-
input deadline to fit the committed upload-key validity. No buyer-side field
remains selectable after Provider authorization.

Exact replay of one offer identity is idempotent. Conflicting reuse is rejected
and retained as evidence. An ambiguous send is resolved through a defined
query or direct peer acknowledgement before retry; if no reliable resolution
exists it remains ambiguous until safe expiry or owner review.

### 11.3 Selection

The buyer may compare offers locally and send a Selection Notice. No provider
executes or recognizes revenue from that notice. The selected provider checks
that the later Accepted Quote exactly reproduces the required demand/offer
terms and binds the correct provider, Capability version, manifest, endpoint,
execution signer, buyer Agent/wallet, input/source, task/validator/evidence
profiles, asset, amount, deadlines, private-input delivery, and dispute/refund
profile.

Selection also creates a distinct `accepted-work.accept` authorization by the
buyer Agent over the same exact typed accepted-work body. This authorization is
not a Selection Notice and cannot move funds. The committed buyer settlement
wallet separately authorizes the finalized Quote/escrow deployment and exact
funding transaction, which atomically consumes the Demand Acceptance Key if it
is still empty. Both Agent-level bilateral authorization proofs, that demand-
wide selection result, and the wallet acceptance must be reconstructible from
finalized accepted state. A Selection Notice or buyer signature alone cannot
reserve or consume the key.

The buyer authorization key, proof context, settlement wallet, and upload
proof-of-possession key must exactly equal the values already committed by the
selected active Demand Mutation and copied into the Provider-authorized body.
A Selection Notice or acceptance using a different value is invalid; changing
the context requires a new Demand Mutation and a new Provider Offer.

The current Accepted Quote does not bind all of those facts. D3 therefore
requires the canonical extension in Section 11.4; this is a confirmed blocking
gap, not a conditional possibility. An index, Selection Notice, Messenger
message, Gateway acknowledgement, or OpenFox journal must not fill it as hidden
authority.

### 11.4 Canonical accepted-work convergence

From the exact active Demand Mutation, its mutation-bound buyer context, one
preallocated durable Offer identity, and Provider-selected fields, the Provider
first constructs one typed `AcceptedWorkBody` without signatures. The Provider
authorization over that body creates the signed Provider Offer. The buyer may
then select that Offer and authorize the same body; adding that buyer proof
completes the reconstructible `AcceptedWorkTerms`. The exact message and TVM
layout remain schema-freeze work, but the body must include:

- complete network domain and accepted-work profile version;
- the exact canonical `BuyerAcceptanceProfile` copied from the active Demand
  Mutation, including buyer Agent, settlement wallet, acceptance key,
  delegation/bounds/mandate, proof profile, authority-reference digest, and
  upload proof-of-possession key/profile;
- demand identity, terminal-safe active mutation sequence, and mutation digest;
- the deterministic Demand Acceptance Key derived from the stable Demand
  identity and V1 `max_selected_providers = 1`;
- Provider Offer identity with `max_acceptances = 1`; the full signed Offer
  digest is derived outside the body as specified below and is never an input
  to its own signing preimage;
- provider Agent, Capability ID/version, and manifest digest;
- exact Provider `provider-offer.sign` key ID, delegation/mandate digests,
  authorization validity bounds, authorization-proof profile, and canonical
  portable issuance-authority reference digest;
- task profile/version and operation descriptor;
- exact input digest, source digest, media type, and byte/file bounds;
- required output, validator, and evidence profiles;
- provider-selected transport, private-input push, and execution-signer
  commitments;
- exact TOS-network asset and provider-service atomic amount;
- offer acceptance, input-delivery, work-delivery, Receipt, and refund
  deadlines under one defined ordering;
- escrow and objective dispute/refund terms; and
- every field needed to deterministically derive the unique Quote commitment,
  escrow StateInit, demand-wide acceptance operation, and execution admission
  identity.

The digest construction is explicitly acyclic:

```text
accepted_work_body_digest
  = H(body-domain || canonical AcceptedWorkBody)

provider_offer_authorization
  = canonical ProviderProofContext
      || Sign_provider(provider-domain || accepted_work_body_digest
                       || H(canonical ProviderProofContext))

provider_offer_digest
  = H(offer-domain || canonical AcceptedWorkBody
      || canonical provider_offer_authorization)

buyer_acceptance_authorization
  = canonical BuyerProofContext
      || Sign_buyer(buyer-domain || accepted_work_body_digest
                    || H(canonical BuyerProofContext))

accepted_work_terms_digest
  = H(terms-domain || canonical AcceptedWorkBody
      || canonical provider_offer_authorization
      || canonical buyer_acceptance_authorization)
```

The full Provider Offer digest is derived only after its proof exists and is
not stored inside `AcceptedWorkBody`. The buyer verifies the unique Provider
proof before signing the same body digest. Each canonical proof context
includes signer identity, constrained delegation/mandate digest, validity
bounds, proof profile, and the exact portable finalized authority reference
needed to verify issuance and acceptance-time revocation ordering. Its reference
digest and every other context value must equal the values already committed by
`AcceptedWorkBody`; a verifier rejects a substituted, equivalent, or additional
proof wrapper. Provider-private writer generations, reservations, capacity
leases, and admission-ledger references are deliberately absent from the public
Offer, body, and proof context: outside resolvers cannot validate that private
state, and takeover must not change canonical accepted-work bytes. Demand
Mutation and derived Provider Offer digests remain immutable provenance links;
neither an opaque Offer digest nor buyer-authored terms alone prove Provider
consent.

`BuyerProofContext` must reproduce the exact mutation-bound
`BuyerAcceptanceProfile` and portable authority-reference digest. A different
otherwise authorized buyer key, delegation, proof path/wrapper, wallet, or
upload key is not equivalent and requires a successor active Demand Mutation
plus a newly authorized Provider Offer/body.

The body fixes both exact delegated signing keys, proof profiles, authority-
reference digests, and validity bounds before the Provider and buyer sign. V1
accepts one canonical Ed25519 signature per named key and one canonical proof
context per side, not an alternate authorized key, threshold subset, proof
path, or wrapper. This prevents authorization-proof choice from changing
`AcceptedWorkTerms`, Quote commitment, or escrow address for the same Provider
Offer. If either named key rotates or is revoked before acceptance, the Offer
expires as non-actionable and a new active Demand Mutation or Provider Offer,
as applicable, plus a new body is required. Buyer acceptance or upload context
cannot be supplied or replaced after the Provider signature.

The Accepted Quote commits the typed body and both authorization proofs, and
escrow StateInit embeds them or an equivalent fully typed representation from
which every field and signing preimage is reconstructed. The finalized Quote
transaction and funding path must originate from the exact buyer settlement
wallet committed by the body and must be the winner recorded under the Demand
Acceptance Key. An opaque Demand/Offer digest, detached
signature, or terms body without both proofs is insufficient. Finalized
resolution returns the complete accepted work terms and bilateral proofs
without a Gateway, Messenger database, market index, or OpenFox journal.

The Native Execution Gate must decode those finalized terms and compare the
incoming execution claim field by field, including buyer/provider identities,
Demand Mutation, Offer, task profile, input/source commitments, validator and
evidence profiles, transport, signer, asset/amount, and deadlines. The first
local claim may record execution identity, but it cannot choose the expected
input or source. The Gate also resolves the body-derived Demand Acceptance Key
and rejects any terms that are not its exact finalized winner.

Before claiming execution, the Gate also verifies both domain-separated
signatures, every delegation/mandate bound, the finalized buyer-wallet
acceptance transaction, the Offer-acceptance deadline, and the ordering of
Quote finality against delegation revocation. A fabricated Offer digest or a
signature that was valid only after its authority was revoked never reaches the
runner.

Receipt construction, settlement verification, portable safe handoff, and
independent history resolution use the same accepted-work body and bilateral
proofs. No later layer may substitute a second value for a fact already bound
there.

#### Binding sufficiency matrix

| Fact | Pre-acceptance artifact | Final accepted authority | Execution/local use |
|---|---|---|---|
| display summary, topics, source hints, index rank | Demand/index only | none | local discovery/presentation only |
| buyer Agent, settlement wallet, acceptance key/proof context, and upload proof-of-possession key | Demand Mutation | exact values in `AcceptedWorkBody` + buyer acceptance proof + finalized wallet transaction | verify issuance and acceptance-time authority; wallet funds exact Quote; ingress checks the mutation-bound upload key |
| Demand identity/sequence/digest | Demand Mutation | `AcceptedWorkBody` as provenance link, not global-head proof | Gate compares exact values and recorded fork evidence |
| demand-wide selection of one Provider | stable Demand identity and fixed V1 limit | first finalized atomic Demand Acceptance Key consumption recording exact Mutation, Offer, terms, Quote, and escrow | Gate checks that the accepted terms equal the recorded winner; competing Offers cannot execute |
| Provider Offer identity/derived digest/single acceptance | Provider Offer | Offer identity in `AcceptedWorkBody` + Provider signature proof; full Offer digest derived outside the body; deterministic Quote/escrow | Gate verifies Provider consent and reservation journal compares exact values |
| provider Agent, Capability/version, manifest | Demand predicate + Offer | `AcceptedWorkTerms` + existing Quote/Registry checks | Gate freshly verifies finalized Registry state |
| task profile/version and operation | Demand + Offer | `AcceptedWorkTerms` | spec-defined executor mapping |
| input/source commitments and bounds | Demand + Offer | `AcceptedWorkTerms` | Gate compares; ingress verifies bytes before execution |
| validator/evidence/output profiles | Demand + Offer | `AcceptedWorkTerms` | validator and Receipt use exact profiles |
| transport, Provider-selected private-input ingress, execution signer | Offer plus mutation-bound buyer upload key | `AcceptedWorkTerms` | transport, ingress, and Gate enforce exact commitments |
| asset, amount, deadlines, dispute/refund | Demand + Offer | `AcceptedWorkTerms` + escrow | custody, Gate, Receipt, settlement enforce |
| bilateral accepted-work authorization | buyer acceptance + Provider Offer | both typed signature proofs in `AcceptedWorkTerms` plus buyer-wallet finality | Gate verifies signing preimages, bounds, expiry, and revocation ordering |
| Selection Notice | negotiation only | none | correlation/presentation only |
| skill implementation, internal cost, margin, model rank | none | none | owner-private OpenFox policy only |
| source coverage, moderation, availability estimate | index observation only | none | local discovery policy only |

Schema work must extend this matrix down to every field. No field may have two
inconsistent authoritative sources, and every accepted execution input must
trace to finalized typed terms.

### 11.5 Single acceptance and capacity consumption

V1 Provider Offers are buyer-specific and single-use. The exact Demand
Mutation, buyer Agent/wallet, provider terms, bilaterally authorized accepted-
work body, and Offer identity determine one `AcceptedWorkTerms`, one Quote
commitment, and one escrow StateInit/address.
The buyer cannot vary a nonce, wallet, input, deadline, amount, signer,
transport, evidence rule, market-authorization key/proof, or other accepted
field to derive a second valid purchase from the same Offer.

Per-Offer `max_acceptances=1` is not demand-wide selection. Every Mutation and
Offer under one V1 Demand instead shares:

```text
demand_acceptance_key
  = H(demand-accept-domain || network-domain || canonical demand identity)
```

The extended Accepted Quote/escrow acceptance operation atomically requires
that key to be empty, verifies the exact body, both authorization proofs and
buyer-wallet funding, and records the winning active Mutation digest, Provider
Offer identity and derived digest, `accepted_work_terms_digest`, Quote
commitment, and escrow identity. Exact replay returns the recorded winner; a
different Offer, Mutation, body, terms, Quote, or escrow conflicts. The operation
must not expose an intermediate state in which the key is consumed without the
exact funded Quote/escrow or vice versa.

This first-finalized compare-and-set is the authoritative selection among all
Provider Offers and all revisions of the stable Demand. It does not assert a
global off-chain Demand head. A buyer that legitimately wants multiple Providers
publishes distinct Demand identities; no local journal, Selection Notice,
signature count, or Gateway row may emulate a quantity greater than one.

Before signing, OpenFox chooses one durable Provider Offer identity, constructs
the canonical body, derives one stable semantic action ID, atomically reserves
local portfolio exposure, and has the selected runtime durably grant the quoted
capacity lease. Each private reservation binds Provider scope, stable action ID,
durable Offer identity, exact `accepted_work_body_digest`, exact Demand identity
and active Mutation digest, resource or exact-asset exposure terms, expiry, and
`max_acceptances=1`. The Provider-private admission authority described below
records those private reservations and the resulting authorization under the
same body digest and Offer identity. Neither the writer fencing generation nor a
private reservation/lease identifier or commitment is copied into the public
Offer, `AcceptedWorkBody`, or proof context.

On observing the unique Quote finality, OpenFox and the runtime atomically or
through the defined idempotent saga convert their reservations to an accepted
obligation. Offer expiry without Quote finality releases them only after
deterministic acceptance resolution; ambiguous acceptance retains them while
resolving the escrow.

Local reservation and one runtime lease do not protect a Provider Agent or
owner mandate shared by multiple OpenFox instances. Every production
`provider-offer.sign` path therefore passes through one Provider-private
admission authority covering the Provider Agent, every key/mandate that may
sign for it, and all configured runtimes. This authority is normally enforced
inside purpose-limited custody and durably maintains:

- one exclusive writer lease containing Provider scope, instance identity,
  authority-clock expiry, and a monotonically increasing fencing generation;
- a rollback-resistant generation high-water mark and Provider-authorization
  issuance ledger in one linearizable persistence domain;
- every signed and unexpired Provider Offer, accepted or unsettled obligation,
  exact-asset aggregate exposure, and runtime capacity commitment;
- one unresolved Offer constraint for each exact `(provider scope, demand
  identity, active mutation digest)` tuple in V1; and
- stable semantic action identities, canonical request digests, signatures,
  dispositions, and deterministic Quote/escrow resolution results.

Lease acquire, renew, and takeover use compare-and-swap. Custody imposes a
protocol maximum lease TTL; owner configuration may narrow but never extend it.
Takeover increments the generation before a new coordinator can sign. Every sign request carries
the current lease token/generation, stable semantic action ID, durable Offer
identity, exact `accepted_work_body_digest`, and references to the matching
private local-portfolio and runtime-capacity records. Custody atomically rejects
a missing, expired, or stale generation, a conflicting body for an existing
action or demand tuple, a missing runtime lease, or any aggregate
exposure/mandate violation. Before any signature bytes leave custody, custody
commits the generation high-water mark, private admission decision, canonical
authorization result, and resulting aggregate exposure in the rollback-
resistant linearizable domain. The generation used is retained only in that
private audit record. Exact retry returns the recorded result. Retry attempt
number and writer generation are audit fields, never inputs that create a new
semantic action identity or alter canonical market bytes.

A replacement writer inherits all unresolved Offers and obligations. It cannot
release them until Offer expiry plus deterministic Quote/escrow resolution, and
a partitioned old writer cannot continue signing with its stale generation.
Even a declared single-process deployment holds an operating-system process
lock on its canonical owner-private state directory for the daemon lifetime and
uses the custody-side expiring writer generation; a PID file alone is not a
lock, and a host-local lock is not cross-host fencing.

After restore or migration, custody must prove that the generation high-water
mark and complete issuance ledger are at least as recent as every generation and
authorization it has emitted. If it cannot, it disables every affected
`provider-offer.sign` key and mandate before serving another lease or signature.
Recovery requires finalized revocation or rotation of that authority, reserves
the old mandate's full possible exact-asset exposure and capacity ceiling, and
blocks every affected Provider/owner scope from fresh signing. The block remains
until either an authoritative exhaustive issuance-and-acceptance source proves
the complete escaped-signature set and every resulting obligation is resolved,
or all protocol- and mandate-bounded maximum Offer-acceptance, obligation,
dispute, and refund windows have elapsed after finalized revocation and the
deterministic Quote/escrow scan is clear. Copied or externally observed subsets
are not proof of completeness. Merely restoring an older snapshot, incrementing
its local counter, rotating without those exposure controls, or changing
configuration cannot recover authority. Loss, rollback, or ambiguous migration
therefore fails closed without making a stale generation current again.

This ledger is Provider-private safety state, not a public market database and
not acceptance or settlement authority. It prevents the Provider from
overcommitting itself; finalized TOS state remains authoritative for accepted
work and settlement.

The finalized terms and Gate reject a second Quote/escrow identity, two
concurrent acceptances, cross-transport replay, or any Offer-field
substitution. Local reservation is necessary for honest capacity planning but
is not the only replay defense. Provider-scope fencing and aggregate admission
are required even though `max_acceptances=1` limits each individual Offer. An
Offer identity or digest without the exact Provider signature proof is never a
reservation or acceptance authority.

### 11.6 Private input delivery V1

V1 selects **buyer push to a Provider-selected, Offer-bound ingress**. A
provider never fetches a URL, host, repository, object store, or credential
chosen by the Demand, buyer message, model, or task content.

The active Demand Mutation binds the dedicated buyer upload proof-of-possession
key/profile in its `BuyerAcceptanceProfile`. The Provider Offer and
`AcceptedWorkBody` copy that exact value, and finalized `AcceptedWorkTerms`
preserve it while also binding the Provider-selected ingress profile and
endpoint/TLS identity. The upload key has no wallet, Agent-control, or market-
signing authority. A challenge repeats the bound key identity for correlation
only and cannot choose or rotate it; a different key or profile conflicts.
Only after finalized Quote and funded escrow:

1. the provider may issue a short-lived, single-task upload challenge outside
   the model and task content, bound to Quote, escrow, input digest, byte/file
   bounds, expiry, stable upload action identity, and buyer upload public key;
2. the buyer signs the canonical request/body digest with that upload key and
   pushes the exact committed bytes to the bound ingress;
3. the ingress authenticates Quote, escrow, buyer proof of possession,
   provider/TLS identity, challenge scope, expiry, operation, and body before
   accepting bytes; a bearer token alone is insufficient;
4. it checks ciphertext/plaintext digest as applicable, media type, compressed
   bytes, decompressed bytes, file count, canonical paths, and archive rules;
5. it durably binds one accepted input to the unique Quote/execution slot; and
6. only verified immutable bytes enter the Native Execution Gate and bounded
   executor.

Challenge consumption and the input record are one atomic durable operation.
Exact retry returns the same input-delivery receipt; a different body,
signature, action identity, or concurrent claimant conflicts without replacing
the accepted bytes. An ambiguous response is resolved by a bounded status
operation keyed by the stable upload action identity before retry.

Upload secrets, credentials, and private source never enter the public
envelope, Opportunity Magnet, model context, artifact, Receipt, logs, or
evidence bundle. Owner-private recovery state may retain only the challenge
digest, action identity, attempt disposition, and non-secret delivery receipt,
not bearer material. Redirects, proxies, arbitrary DNS, provider-side
credential forwarding, buyer-selected egress, and pull fallback are forbidden.
Challenge expiry, revocation, retry, retention, deletion request, and crash
recovery are typed profile behavior. A deletion acknowledgement proves only
the named operator's local observation and never cryptographic erasure.

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
  -> preallocate durable Offer ID + construct canonical AcceptedWorkBody
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

FreeCity, OpenFox UI, or another application may render:

- recently observed work;
- tasks matching the local Agent's approved skills;
- estimated net profit and worst-case exposure;
- fixed-price versus offer-required opportunities;
- expiring, withdrawn, or superseded listings;
- offers awaiting a buyer response;
- accepted and executing work;
- submitted receivables; and
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
The provider resumes from exact owner-held preimages and journals plus
finalized TOS state. Gateway, channel, conversation, and work-square loss must
not prevent execution admission, Receipt checking, refund, settlement, or
independent reconstruction.

## 17. Repository ownership

| Repository | Responsibility |
|---|---|
| `tos-service-spec` | candidate profile; eventual Native Demand Mutation, Offer, market delegation, AcceptedWorkTerms, private-input, task/execution/validator/evidence schemas; bounds; signatures/digests; public errors; vectors; authority invariants; acceptance evidence |
| `tos-service-protocol` | canonical artifact codecs and verification, finalized buyer/provider checks, federation client, offer/Quote SDK, error classification, and recovery helpers |
| `tos-service-gateway` | optional authenticated Demand Mutation/relay endpoints, bounded derived search, source provenance, cursors, filtering, and federation conformance |
| `tos` | generic DHT, Overlay, ADNL/RLDP, Storage, Agent, demand-wide acceptance-key, Accepted Quote, escrow, Receipt, and settlement primitives/contracts; no market search or ranking |
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

ResolveDemandAcceptance(deterministic Demand Acceptance Key,
                        finalized checkpoint)
  -> empty | accepted(exact Mutation, Offer, terms, Quote, escrow, funding)
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
- retryable source unavailability;
- ambiguous mutation requiring resolution before retry;
- already-consumed Demand Acceptance Key with the exact prior winner; and
- conflicting attempt to consume a Demand Acceptance Key with different
  Mutation, Offer, terms, Quote, escrow, or funding.

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
- freeze the mutation-bound `BuyerAcceptanceProfile`, binding sufficiency
  matrix, typed `AcceptedWorkBody`, bilateral authorization proofs, complete
  `AcceptedWorkTerms`, deterministic Quote/escrow derivation, single-acceptance
  rule, demand-wide acceptance-key derivation/atomic consumption, proof-of-
  possession private-input push profile, required Execution Gate comparisons,
  and the separate Provider-private fencing/admission invariants;
- produce positive vectors and adversarial mutations; and
- obtain independent parser/vector consumption.

### Phase D1 — local read-only feed

- generate signed synthetic fixed-price demand;
- implement one local public-channel or fixture carrier;
- resolve one Paid Demand Reference from a local cache and at least two
  independently configured fixture carriers;
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
- permit no Provider Offer, Selection Notice acceptance, Quote, execution, or
  automatic commercial authorization.

### Phase D3 — guarded fixed-price response

- begin only after the complete D2 two-source, source-plus-database shutdown,
  and independent-codec/verifier gate, and after the market delegation, Demand
  Mutation/non-canonical-head boundary, mutation-bound
  `BuyerAcceptanceProfile`, bilateral
  `AcceptedWorkTerms` authorizations, Provider-wide writer fencing and
  aggregate admission, demand-wide single-provider acceptance, Accepted Quote/
  escrow, Execution Gate, per-Offer single-acceptance, and proof-of-possession
  private-input profiles have frozen vectors and implementations;
- add direct signed single-acceptance Provider Offers and mutation resolution;
- add proposal-only OpenFox recommend mode plus a distinct exact one-shot owner-
  authorization path that does not widen the persistent mode;
- construct the unique extended Accepted Quote and escrow from the typed
  accepted-work body and bilateral proofs;
- push private input only through the Offer-bound proof-of-possession Provider
  ingress;
- execute through the Native Execution Gate; and
- reconcile one finalized provider-wallet credit.

### Phase D4 — bounded policy-gated operation

- install an expiring owner mandate and small exact-asset exposure limits;
- add automatic Provider Offer only for the accepted fixed-price profile;
- run pause, drain, revocation, crash, malicious-source, refund, and dispute
  exercises; and
- collect independent recurring-use evidence before competitive bidding or
  additional profiles.

These phases do not reorder `ROADMAP.md`. Incubation and same-host evidence
cannot open an external acceptance or Expansion Gate. D3 and D4 remain blocked
until every prerequisite named above is complete; D1/D2 evidence cannot be
used to infer executable commercial safety.

## 20. Conformance and adversarial tests

### Artifact verification

- exact positive active/terminal Demand Mutation, market delegation,
  mutation-bound `BuyerAcceptanceProfile`, single-acceptance Provider Offer,
  buyer accepted-work authorization, bilateral AcceptedWorkTerms, Demand
  Acceptance Key, Quote/escrow, private-input, and selection vectors;
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
- missing, malformed, unauthorized, expired, or unresolvable buyer acceptance
  profile; Messenger, Selection Notice, Gateway, or index completion of a
  missing field; successor-profile substitution into an old Offer; and
  acceptance-key or upload-key rotation/substitution after Provider signing.

### Accepted-work convergence

- demand, offer, buyer Agent/wallet, input, source, task profile, validator,
  evidence, transport, signer, asset/amount, and deadline swap mutations;
- absent, forged, detached, circular, wrong-body, wrong-scope, or revoked buyer
  acceptance and Provider Offer authorization proofs;
- body containing its own Provider Offer/AcceptedWorkTerms digest or any other
  circular digest/signature dependency;
- alternate otherwise authorized key, threshold-signature subset, portable
  authority reference/proof path, proof wrapper/order, or non-canonical Ed25519
  signature encoding for the same Offer/body;
- buyer acceptance key/delegation/proof/reference or upload key that differs
  from the selected active Demand Mutation;
- public Offer, body, or proof bytes containing Provider-private writer
  generation, reservation, capacity-lease, or admission-ledger fields;
- opaque accepted-work digest without its reconstructible typed body and
  bilateral proofs;
- two concurrent Quotes or escrows from one Offer and any buyer-controlled
  Quote-construction variance;
- simultaneous acceptance of different Provider Offers and different active
  Mutations under one stable Demand Acceptance Key, including exact replay,
  conflicting winner, atomic funding/key-consumption rollback, and recovery in
  both finality orders;
- exact deterministic Quote/StateInit reproduction in two implementations;
- Execution Gate claim mismatch against every accepted-work field;
- safe-handoff and Receipt reconstruction without market databases; and
- crash before/after reservation, Offer send, Quote observation, reservation
  conversion, ingress admission, Gate claim, Receipt, and settlement.

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
- malicious buyer URL, DNS, redirect, proxy, metadata address, credential,
  archive, compression, media-type, digest, challenge, and retention inputs;
- stolen bearer challenge, wrong upload proof-of-possession key, concurrent
  upload, exact retry, conflicting body, crash-before-receipt, ambiguous ACK,
  and status-resolution inputs;
- pause, drain, mandate expiry, and custody revocation;
- reconciliation dry-run with an unchanged state digest; canonical plan
  recomputation and digest binding; authorized, unauthorized, stale-plan,
  conflicting-action, exact-resume, journal-head-CAS, and crash-after-intent
  reconciliation apply; and
- restart at every discovery, offer, acceptance, execution, Receipt, and
  settlement boundary.

### End-to-end

- buyer publishes through one independently operated carrier;
- at least two independently operated indexes or replicas observe the same
  exact envelope with distinct provenance;
- provider discovers through another source and sends one signed offer;
- original carrier becomes unavailable before acceptance;
- buyer and provider authorize the same canonical `AcceptedWorkBody`, including
  its exact portable authority-reference digests;
- the canonical Provider Offer authorization and buyer acceptance authorization
  are attached to that body to form the complete `AcceptedWorkTerms`;
- a second Provider supplies a competing independently valid Offer, and
  concurrent buyer acceptance attempts prove that the exact committed wallet
  atomically funds only the first finalized Quote/escrow while the shared Demand
  Acceptance Key rejects the other;
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
   `BuyerAcceptanceProfile`, before performing expensive evaluation;
6. typed skill, evidence, capacity, exact-asset economics, and owner policy
   produce a reproducible decision;
7. one idempotent, single-acceptance signed Provider Offer reaches the buyer,
   reserves capacity atomically, passes Provider-wide writer fencing,
   unresolved-tuple and aggregate-exposure admission across every shared
   key/mandate/instance, and survives sender and receiver restart;
8. same-host process locking rejects a second writable OpenFox, custody rejects
   a stale or partitioned writer generation, and a replacement writer inherits
   every unresolved Offer before it may sign;
9. an unavailable source does not prevent accepted-work recovery;
10. the complete typed `AcceptedWorkBody`, mutation-bound buyer acceptance and
   upload profile, buyer acceptance authorization,
   Provider Offer authorization, portable authority references, and exact
   buyer-wallet acceptance are reconstructible from the finalized Accepted
   Quote and funded escrow without a market database;
11. the same Provider-authorized body cannot create a second Quote/escrow;
    concurrent Offers from different Providers or Demand revisions yield exactly
    one atomically funded winner under the shared Demand Acceptance Key; and its
    private input arrives only through the bound proof-of-possession buyer-push
    ingress;
12. the Native Execution Gate verifies both bilateral authorizations and their
    revocation ordering, compares every accepted-work field, admits one
    execution, and rejects field substitution and cross-transport replay;
13. a canonical Receipt binds the objective outcome and immutable evidence;
14. finalized provider-wallet credit is independently resolved; and
15. no Gateway, channel, Relay, index, FreeCity database, OpenFox journal, or
    Provider-private admission ledger is
    required to reconstruct canonical settlement.

## 22. Explicit non-goals

V1 does not create:

- one global job board or globally complete order book;
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
- a new stablecoin, external-chain asset, or Gateway ledger;
- policy or authority expansion through OpenFox self-learning; or
- production or roadmap acceptance from design, local tests, or same-host
  operation.

## 23. Open decisions before schema freeze

The architecture review closes five directional questions: V1 uses one
monotonic Demand Mutation chain with terminal withdrawal, separate
purpose-limited market delegations, single-acceptance Provider Offers with
typed accepted-work convergence, a contract-enforced demand-wide first-finalized
selection key, and buyer push to a Provider-bound private input ingress. Schema
freeze must still decide the exact encodings and bounds:

1. Is the single canonical envelope a Native protobuf message carried inside
   Messenger events and Gateway RPCs, or an Agent Packet payload with a
   one-to-one Native mapping?
2. Which exact numeric purpose bits/scopes, single delegated Ed25519 key,
   canonical signature/proof encoding, delegation schema and static bounds,
   portable historical authority proof, policy/generation
   commitment, checkpoint proof, lifetime, and revocation lookup encode
   `paid-demand.publish`, `paid-demand.withdraw`, and
   `provider-offer.sign`, and `accepted-work.accept`?
3. Which fixed-price software-work operations and spec-defined execution,
   validator, and evidence profiles form the first safe demand subset?
4. Does V1 require a funded-intent proof or only finalized buyer identity and
   local rate limits before offer evaluation?
5. What exact `AcceptedWorkBody`, buyer/provider authorization proofs,
   `AcceptedWorkTerms` protobuf and TVM cells, Quote schema version, escrow
   StateInit, resolver response, Receipt binding, and safe-handoff
   representation freeze the Section 11.4 matrix without circular signing?
6. What exact contract/state owner, key derivation, TVM layout, atomic buyer-
   wallet funding and winner update, per-Offer check, exact-replay/conflict
   resolver, finalized-checkpoint query, and recovery semantics freeze the
   shared Demand Acceptance Key across every Provider Offer and Mutation?
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
