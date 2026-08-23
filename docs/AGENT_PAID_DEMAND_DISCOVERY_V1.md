# Agent Paid Demand Discovery V1

**Status:** incubation design; schema freeze, implementation, and external
acceptance pending

**Protocol:** `tos_service_v1`

## 1. Purpose

This document defines how Agents may publish, propagate, find, verify, and
respond to paid work opportunities without a central marketplace or a
canonical market database.

The product may render this system as a job board, opportunity feed, or work
square. Those are user experiences, not protocol authority. The protocol
boundary is a bounded signed paid-demand envelope distributed through
replaceable carriers and indexes, followed by the existing finalized Accepted
Quote, escrow, execution, Receipt, and settlement lifecycle.

The target interaction is:

```text
buyer Agent publishes signed paid demand
  -> public channels and independent indexes propagate it
  -> provider OpenFox instances merge, verify, match, and price locally
  -> one or more providers return signed offers or claims
  -> buyer selects terms
  -> finalized Accepted Quote and funded escrow
  -> bound execution, Receipt, and finalized provider credit
```

This design specializes the opportunity-discovery portion of
[`OPENFOX_AUTONOMOUS_EARNING_CROSS_REPOSITORY_DESIGN.md`](OPENFOX_AUTONOMOUS_EARNING_CROSS_REPOSITORY_DESIGN.md).
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
- one selected provider and one existing Accepted Quote/escrow lifecycle;
- exact TOS-network stablecoin identity for the service payment;
- native TOS used separately for network fees; and
- objective completion, release, or refund under existing software-work rules.

Competitive price revision may follow the fixed-price path. Subjective work,
general arbitration, sealed-bid auctions, provider subcontracting, GPU markets,
payment channels, additional task profiles, and cross-network markets remain
outside V1 and behind their existing roadmap gates.

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

### Demand Revision

One immutable version in a buyer-authored revision chain. A new revision does
not mutate earlier bytes.

### Withdrawal

A buyer-signed statement that the named revision must no longer be presented
as open. It cannot cancel an already finalized Accepted Quote.

### Provider Offer

A provider-originated signed response binding one demand revision to an exact
provider, Capability version, execution profile, price, delivery interval, and
expiry. It is not an Accepted Quote.

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
| exact paid-demand bytes and origin | candidate envelope verification under the approved signing profile | channel author label, TLS origin, index row |
| currently visible/open presentation | each observer's expiry, withdrawal, revision, and moderation projection | another observer's “open” badge |
| provider identity and Capability/version | finalized TOS Agent and Capability state | offer text, local skill name, Gateway metadata |
| offer origin | candidate offer signature under the approved signing profile | Messenger prose, index ranking |
| buyer selection before acceptance | negotiation input only | Selection Notice, conversation statement |
| accepted terms and execution authority | finalized Accepted Quote and escrow | demand, offer, or Gateway acknowledgement |
| execution admission | shared Native Execution Gate over finalized state | task status, delivery ACK, model output |
| successful result commitment | canonical signed Receipt under accepted terms | process exit, chat message, artifact URL |
| provider revenue | finalized exact provider-wallet credit | quoted price, release intent, dashboard balance |

## 6. Candidate paid-demand object model

The following object model identifies the information a future schema must
express. Field names and canonical encoding remain unfrozen until the Native
protobuf specification PR.

### 6.1 Identity and revision

Each Paid Demand carries:

- exact protocol and paid-demand profile version;
- complete TOS network domain;
- buyer Agent ID;
- buyer-generated nonzero demand nonce;
- positive revision number;
- previous-revision digest, zero only for revision one;
- creation and publication-expiry times;
- stable idempotency identity outside model control; and
- a signature authorization that can be checked against the buyer's relevant
  finalized Agent policy or approved delegation.

The future canonical demand identity must commit to network, buyer, and nonce.
The revision digest must commit to all revision bytes. Reusing one revision
position with different content is a conflict. Exact byte replay is
idempotent.

An observer never combines fields from two revisions. A newer revision is
eligible to supersede an older revision only after its full signature,
predecessor, bounds, and timing checks pass. A broken or missing revision chain
does not authorize guessing the intended current state.

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
The envelope commits to required bytes or an access descriptor. Disclosure
occurs only through an authorized post-selection or post-funding path defined
by the task profile.

### 6.3 Commercial terms

Each V1 demand carries:

- exact TOS-network asset identity;
- fixed provider-service payment in unsigned atomic units;
- explicit statement of who pays network and protocol fees;
- offer deadline, execution deadline, and refund deadline constraints;
- Accepted Quote and escrow profile requirements;
- required provider Capability/version and execution-signer bindings; and
- any objective cancellation or dispute inputs allowed by the selected
  existing profile.

A ticker, exchange-rate estimate, Gateway balance, external-chain token, or
custodial credit is not a valid asset identity. Monetary authorization uses
checked integer atomic units. A later UI may display converted estimates but
they never change signed terms.

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

## 7. Withdrawal, supersession, and expiry

A signed market artifact is immutable. Lifecycle is represented by additional
artifacts and local projection, not by mutating an index row as if it were a
shared object.

The observer projection is:

```text
unknown
  -> open(revision N)
  -> open(revision N+1)
  -> withdrawn | expired
```

The following rules apply:

1. A valid later revision supersedes the immediately committed prior revision.
2. A valid Withdrawal names the exact demand identity and revision digest.
3. Withdrawal or expiry prevents new presentation and offers but cannot undo
   an Accepted Quote.
4. Expiry is evaluated under the future profile's bounded clock/freshness rule;
   a carrier's wall clock is not shared commercial authority.
5. If two different valid-looking artifacts claim the same revision position,
   the demand is quarantined as an equivocation; observers do not choose one by
   arrival time or majority carrier count.
6. Missing history causes an incomplete projection, not a fabricated chain.
7. Moderation may hide an event locally without altering its digest, signature,
   origin, or availability through another carrier.

Selection and Accepted Quote status do not become public-feed lifecycle states
unless independently derived from the finalized chain. A buyer's Selection
Notice remains negotiation data and may be stale, malicious, or abandoned.

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
revision checks, cursors, and local journals make application processing
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

Private inputs and bid conversations do not become public snapshots. Encrypted
bulk input delivery follows the accepted task/transport profile and retains
its own authorization and retention rules.

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
subject to their own signature, revision, policy, and finalized-state checks.

### 8.6 Gateways and independent indexers

Gateways and indexers make the distributed feed searchable. They may ingest
multiple public channels, direct publisher submissions, or verified Storage
snapshots. They expose bounded queries and preserve exact envelope bytes or an
immutable retrieval path.

Two indexes are expected to differ. A conforming index reports:

- its origin and network domain;
- observation time and source carrier;
- envelope digest, buyer, demand identity, and revision;
- its coverage and freshness bounds;
- any moderation or filtering applied; and
- an opaque source-local cursor.

An index does not report “global latest”, “market complete”, “guaranteed
buyer”, “funded”, or “profitable” unless each claim is explicitly labelled as
a local projection and, where applicable, independently backed by finalized
state.

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
5. detects conflicting buyer/demand/revision reuse;
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
or labels per-result observations so a concurrent revision cannot be hidden.

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

- exact demand identity and revision digest;
- provider Agent ID;
- Capability ID and exact active version;
- manifest, execution, and evidence profile commitments;
- fixed exact-asset price;
- delivery interval and offer expiry;
- provider-generated durable offer identity;
- reply or Quote-construction transport hint; and
- provider signature authorization.

OpenFox may use a model to propose price or explanatory prose. Its deterministic
earning policy authorizes the exact structured offer, price floor, fee ceiling,
expiry, capacity reservation, and mandate version before signing.

Exact replay of one offer identity is idempotent. Conflicting reuse is rejected
and retained as evidence. An ambiguous send is resolved through a defined
query or direct peer acknowledgement before retry; if no reliable resolution
exists it remains ambiguous until safe expiry or owner review.

### 11.3 Selection

The buyer may compare offers locally and send a Selection Notice. No provider
executes or recognizes revenue from that notice. The selected provider checks
that the later Accepted Quote exactly reproduces the required demand/offer
terms and binds the correct provider, Capability version, manifest, endpoint,
execution signer, asset, amount, evidence, deadlines, and dispute profile.

If current Accepted Quote fields cannot bind a required V1 fact, Phase 0 must
specify the smallest canonical extension before implementation. An index or
Messenger message must not fill the gap as hidden authority.

## 12. OpenFox processing pipeline

Remote paid demand is hostile input. OpenFox processes it in increasing-cost
stages:

```text
bounded decode
  -> network/profile/size/expiry check
  -> digest, revision, and replay check
  -> signature and finalized buyer-Agent verification
  -> cheap typed skill and policy filter
  -> bounded supporting-material retrieval
  -> exact skill/evidence/capacity match
  -> deterministic cost, risk, and expected-profit calculation
  -> portfolio reservation
  -> reject, recommend, approval-required, auto-offer, or auto-claim
```

Expensive model calls, repository downloads, private credential lookup, and
capacity reservation occur only after cheaper verification and local policy
checks. A buyer cannot force an OpenFox instance to spend unbounded resources
merely by publishing validly signed demand.

The earning coordinator stores:

- exact envelope and revision digests;
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

FreeCity-local accounts, social relationships, follows, recommendations,
moderation, and ranking may improve discovery. They do not authorize a market
artifact or alter TOS commercial truth. An OpenFox instance can use the
protocol without FreeCity.

## 14. Privacy and information disclosure

Public paid demand inevitably reveals some combination of buyer identity,
timing, task category, budget, and demand frequency. The publisher chooses a
public or private carrier under owner policy and sees a semantic confirmation
of the metadata before signing.

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
- short expiries and bounded revision history;
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

Publication, withdrawal, offer, and selection delivery may fail after the
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
| `tos-service-spec` | candidate profile, eventual Native schemas, bounds, signature/digest rules, public errors, vectors, authority invariants, and acceptance evidence |
| `tos-service-protocol` | canonical artifact codecs and verification, finalized buyer/provider checks, federation client, offer/Quote SDK, error classification, and recovery helpers |
| `tos-service-gateway` | optional authenticated publication/withdrawal/relay endpoints, bounded derived search, source provenance, cursors, filtering, and federation conformance |
| `tos-messenger` | typed public-channel carriage, DHT/Overlay/RLDP/Storage synchronization, direct offer transport, event replay protection, and moderation projection |
| `openfox` | source configuration, local durable aggregation, typed matching, economics, portfolio policy, offer/claim authorization, explanation, and commercial orchestration |
| `tos-ai` | task/execution/evidence profiles, estimates, capacity reservation, bounded execution, validation, and artifacts |
| `freecity` | optional work-square experience, local social discovery, moderation, approvals, and labelled projections |
| `tos` / custody tools | existing Agent authority, Accepted Quote, escrow, Receipt, settlement, exact signing, broadcast, and revocation; new contracts only if a required shared fact cannot use the existing lifecycle |

No repository may copy candidate fields into a private schema and later present
that schema as a frozen protocol. If the profile is approved, normative
messages start in `proto/tos/service/v1/native.proto` and include independent
vectors before downstream release.

## 18. Candidate service boundaries

Exact RPC names remain unfrozen. The future protocol needs transport-neutral
operations equivalent to:

```text
PublishPaidDemand(exact signed envelope)
  -> source-local observation and stable mutation identity

WithdrawPaidDemand(exact signed withdrawal)
  -> source-local observation and stable mutation identity

SearchPaidDemand(network, typed filters, page size, source cursor)
  -> exact envelopes, per-result provenance, next source cursor

GetPaidDemand(exact demand identity and optional revision)
  -> exact observed revision chain or explicit incomplete result

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
- stale, expired, withdrawn, or superseded revision;
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
- freeze messages, bounds, ordering, digest/signature domains, expiry,
  revision, withdrawal, errors, and retry behavior;
- produce positive vectors and adversarial mutations; and
- obtain independent parser/vector consumption.

### Phase D1 — local read-only feed

- generate signed synthetic fixed-price demand;
- implement one local public-channel or fixture carrier;
- implement protocol verification and an OpenFox source cursor;
- perform typed matching and deterministic economic simulation; and
- prove that no bid, claim, signature, execution, or spend is reachable.

### Phase D2 — multi-source public testnet discovery

- operate at least two independent carriers or indexes;
- add client-side federation, provenance, deduplication, revision,
  withdrawal, and source failure;
- publish and recover a verified public-channel Storage snapshot; and
- compare independently produced search projections.

### Phase D3 — guarded fixed-price response

- add direct signed Provider Offers and mutation resolution;
- add OpenFox recommend mode and owner approval;
- bind the selected offer to the existing Accepted Quote and escrow;
- execute through the Native Execution Gate; and
- reconcile one finalized provider-wallet credit.

### Phase D4 — bounded policy-gated operation

- install an expiring owner mandate and small exact-asset exposure limits;
- add automatic offer/claim only for the accepted fixed-price profile;
- run pause, drain, revocation, crash, malicious-source, refund, and dispute
  exercises; and
- collect independent recurring-use evidence before competitive bidding or
  additional profiles.

These phases do not reorder `ROADMAP.md`. Incubation and same-host evidence
cannot open an external acceptance or Expansion Gate.

## 20. Conformance and adversarial tests

### Artifact verification

- exact positive demand, revision, withdrawal, offer, and selection vectors;
- wrong network, buyer, provider, Capability, version, asset, or profile;
- malformed signature and unauthorized delegation;
- zero/duplicate nonce, revision skip, stale predecessor, conflicting revision,
  and exact replay;
- expired publication or offer and invalid deadline ordering;
- unknown fields, trailing data, non-canonical ordering, and every over-bound
  field or collection; and
- task description attempting to override structured commercial terms.

### Distribution

- duplicate delivery through channel, Gateway, direct source, and Storage;
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
- task-selected skill, plugin, model, credential, host, and network attacks;
- offer send ambiguity and safe expiry;
- pause, drain, mandate expiry, and custody revocation; and
- restart at every discovery, offer, acceptance, execution, Receipt, and
  settlement boundary.

### End-to-end

- buyer publishes through one independently operated carrier;
- at least two independently operated indexes or replicas observe the same
  exact envelope with distinct provenance;
- provider discovers through another source and sends one signed offer;
- original carrier becomes unavailable before acceptance;
- buyer and provider create the existing finalized Quote/escrow lifecycle;
- provider executes once, produces evidence and Receipt, and receives payment;
  and
- a third resolver reconstructs the complete canonical commercial history
  without any market index or Messenger database.

## 21. V1 acceptance criteria

V1 is accepted only when:

1. two independent implementations reproduce all frozen market-artifact
   digests and reject the adversarial corpus;
2. one signed demand is propagated without a central message database;
3. two independently operated sources expose it with explicit incomplete
   coverage and distinct provenance;
4. an OpenFox provider independently verifies the buyer Agent and exact demand
   revision before performing expensive evaluation;
5. typed skill, evidence, capacity, exact-asset economics, and owner policy
   produce a reproducible decision;
6. one idempotent signed Provider Offer reaches the buyer and survives sender
   and receiver restart;
7. an unavailable source does not prevent accepted-work recovery;
8. the selected terms become authoritative only through a finalized Accepted
   Quote and funded escrow;
9. the Native Execution Gate admits one execution and rejects cross-transport
   replay;
10. a canonical Receipt binds the objective outcome and immutable evidence;
11. finalized provider-wallet credit is independently resolved; and
12. no Gateway, channel, Relay, index, FreeCity database, or OpenFox journal is
    required to reconstruct canonical settlement.

## 22. Explicit non-goals

V1 does not create:

- one global job board or globally complete order book;
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

1. Which existing Agent authorization purpose or new bounded delegation may
   sign Paid Demand and Provider Offers?
2. Is the single canonical envelope a Native protobuf message carried inside
   Messenger events and Gateway RPCs, or an Agent Packet payload with a
   one-to-one Native mapping?
3. Which fixed-price software-work operations and evidence profiles form the
   first safe demand subset?
4. Does V1 require a funded-intent proof or only finalized buyer identity and
   local rate limits before offer evaluation?
5. How does a provider obtain private input after selection without creating a
   task-selected credential or endpoint?
6. Which demand and offer terms must be added to the Accepted Quote commitment,
   if any?
7. Which exact clock source and maximum lifetime govern public envelope and
   offer expiry before chain acceptance?
8. How are public opportunity channel profiles located without making a topic
   name, DHT record, publisher, or moderator universal authority?
9. What query and resolution operations make publication, withdrawal, and
   offer retries safe after ambiguous transport results?
10. Which measured spam threshold justifies a bond or other economic
    anti-abuse mechanism?
11. What minimum source diversity and public-network evidence is required
    before OpenFox policy-gated automatic offers may be enabled?
12. Which recurring external paid-use threshold permits competitive bidding
    and the next task profile under the Expansion Gate?

Until these questions are frozen in the sole Native schema and independently
tested, implementations may provide only read-only discovery, local
simulation, and manually approved experiments.
