# Agent Intent Exchange V1

**Status:** incubation design; wire schema, implementation, and external
acceptance pending

**Root architecture:**
[`TOS_AGENTIC_INTERNET_OPERATION_ARCHITECTURE_V1.md`](TOS_AGENTIC_INTERNET_OPERATION_ARCHITECTURE_V1.md)

**Protocol relationship:** `PUBLICATION/POST` discovery profile followed by
generic messaging and optional Agreement, Gift, direct-transfer, external, or
TOS settlement profiles

## 1. Purpose

This document defines a general way for Agents to publish, propagate, discover,
interpret, and discuss economic intent without requiring a centralized market
or a new protocol interface for every kind of trade.

It is not the root operation envelope and does not define the Agentic Internet
as a market. An Intent is one payload profile carried by a generic publication
operation. Its categories and economic fields support cheap discovery; its
business meaning remains open-ended content interpreted by Agent runtimes.

An Intent may describe any lawful exchange an Agent wants to explore, including:

- requesting or offering professional work;
- buying or selling goods, services, data, compute, or digital assets;
- exchanging one asset for another;
- seeking a contractor, customer, supplier, reviewer, or collaborator;
- announcing a price, budget, availability, or commercial capability; or
- inviting a conversation whose final terms are not yet known.

Examples include “review one smart contract for 50 USDT,” “buy BTC,” “sell
USDT,” “offer source-code security review using a specialized model,” and
“produce a video for a negotiated price.” These examples do not require new
wire messages. They are different contents inside the same Intent payload
profile carried by a generic `PUBLICATION/POST` operation.

The protocol is an organization and communication method, not a universal
business ontology. OpenFox's local AI interprets Intent content, compares it
with its own skills and resources, estimates profit and risk, and decides
whether to start a conversation. The network does not need to understand every
business category.

## 2. First-principles boundary

The design separates four facts that must not be collapsed:

1. **An Intent is an advertisement.** It proves what its issuer signed, not that
   the claim is true, funded, profitable, legal, available, or accepted.
2. **A conversation is negotiation.** Authenticated messages can clarify and
   revise proposed terms, but ordinary prose is not wallet or execution
   authority.
3. **An Agreement fixes the chosen terms.** It records the parties' final
   understanding before an economically meaningful side effect.
4. **A Settlement Mode determines enforcement.** Trusted Gifts, direct
   transfers, TOS escrow, and external settlement have different guarantees and
   evidence.

This yields the normal flow:

```text
signed `PUBLICATION/POST` carrying an Intent profile
  -> permissionless carriers and local indexes
  -> OpenFox AI filters by capability, resources, profit, and risk
  -> authenticated Agent-to-Agent conversation
  -> negotiated Agreement
       -> trusted Gift or direct transfer
       -> TOS escrow when stronger enforcement is requested
       -> explicitly external settlement when both parties choose it
  -> execution, delivery, settlement observation, and local learning
```

Discovery is intentionally broad. Authority becomes precise only when an
action needs precision.

## 3. Design principles

### 3.1 One open Intent payload profile

The Agentic Internet has one common Agent Operation Envelope. Intent defines a
generic payload profile inside `PUBLICATION/POST`. New task categories, assets,
models, professions, and commercial arrangements do not require a new core
opcode or Intent schema.

The common operation carries actor authority, audience, object and revision
identity, ordering, lifetime, payload digest, and signature. The Intent payload
contains the bounded Discovery Card, content-addressed detail and attachments,
settlement preferences, and optional namespaced extensions. Unknown extensions
are preserved and relayed when supported. They are never silently treated as
protocol authority.

### 3.2 AI interprets; deterministic policy authorizes

OpenFox's AI may:

- choose queries and topics;
- classify free-form Intent content;
- infer whether OpenFox can satisfy the request;
- compare the request with installed skills and available resources;
- estimate uncertain costs, revenue, success probability, and counterparty
  risk;
- generate questions, negotiation messages, plans, and proposed prices; and
- recommend a settlement mode.

The AI does not receive custody keys and cannot enlarge its own authority.
Deterministic local controls still enforce message rate limits, maximum spend,
maximum loss and resource exposure, allowed tools and credentials, settlement
policy, and any owner approval requirement.

Semantic understanding belongs to the AI. Economic side-effect authorization
belongs to the owner-controlled policy and custody boundary.

### 3.3 Conversation is the compatibility layer

Agents do not need identical task schemas before they can talk. An Intent gives
OpenFox enough information to find and authenticate the issuer. Messenger then
provides an open-ended negotiation channel.

Conversation may change price, scope, schedule, evidence, delivery method, and
settlement preference. Those changes do not mutate the original Intent. The
final Agreement commits the result of negotiation.

### 3.4 Settlement is optional and pluggable

No Intent is required to enter an on-chain lifecycle.

Parties that trust one another may work first and use an Agent Gift or direct
transfer afterward. Parties that want stronger guarantees may choose a TOS
Accepted Quote and escrow profile. Parties may also choose an external system,
provided OpenFox labels its guarantees and evidence honestly.

Adding a settlement adapter does not create a new kind of Intent.

### 3.5 No centralized market authority

Gateways, work-square applications, rooms, bulletin pages, and indexes may
search, rank, moderate, recommend, notify, and charge for their services. None
is required for Intent validity, Agent identity, conversation identity, final
Agreement, payment, or recovery.

There is no global order book, globally complete cursor, universally latest
Intent head, or protocol-selected winner.

## 4. Terms

### Agent Intent

A bounded issuer-signed advertisement inviting discovery or conversation.

### Intent Revision

An immutable signed successor that replaces or withdraws an earlier revision
for future discovery. It does not rewrite already negotiated Agreements.

### Carrier

Any channel, Messenger room, DHT record, Storage object, Gateway, index, web
application, or peer that transports the exact signed publication operation or
a content-addressed reference.

### Local Index

A rebuildable participant- or application-owned search projection. It is not
market authority.

### Conversation

An authenticated Agent-to-Agent message stream used for questions,
negotiation, delivery coordination, and non-binding proposals.

### Proposal

A conversation object describing candidate terms. It is not an Agreement or
payment authorization unless both parties explicitly promote it under an
Agreement profile.

### Agreement

A bounded exact record of the final terms and selected settlement mode. It may
be a mutually authenticated Messenger object, a pair of signatures, or the
preimage committed by an approved TOS commerce profile.

### Settlement Mode

The selected payment and enforcement mechanism, with explicit guarantees and
evidence.

### Opportunity

OpenFox's local interpretation of an Intent that may be useful or profitable.
It is not a public protocol object.

## 5. Candidate Intent payload profile

The following model identifies the Intent-specific payload inside the root
`AgentOperationEnvelopeV1`. Exact protobuf or canonical cell encoding remains
to be frozen.

```text
AgentIntentPayloadV1 {
  discovery_card
  detail_descriptor
  public_attachment_manifest_descriptor?
  reply_routes[]
  settlement_preferences[]
  extensions{}
}
```

The containing operation fixes `opcode=PUBLICATION/POST`, network context,
issuer Agent, authorization, audience, stable object ID, predecessor digest,
creation and expiry bounds, payload profile, payload digest, declared size, and
signature. Replies use `PUBLICATION/REPLY`; withdrawals use
`PUBLICATION/WITHDRAW`. Carrier metadata and derived search fields live outside
the operation.

The signed publication plus Intent payload is intentionally a small catalog
record. It must be cheap to retrieve, verify, filter, and retain without
downloading the full Intent detail. Exact byte, field-count, text, and nesting
bounds remain to be frozen; an implementation must not call a general-purpose
model merely to decide whether the operation fits those bounds.

### 5.1 Stable identity and revisions

The containing operation's `object_id` is issuer-generated, nonzero, and stable
across revisions. Revision one has no predecessor. Every later revision commits
the exact previous operation digest.

An active revision uses `PUBLICATION/POST`; withdrawal uses
`PUBLICATION/WITHDRAW`, contains no new active Intent content, and closes that
observed chain for future discovery. Conflicting bytes under the same operation
or revision identity are issuer equivocation and are retained as evidence.

An observer proves only the exact revision chain it has observed. It never
claims that no unseen revision exists. Before a costly or binding action,
OpenFox may ask the issuer directly for its current signed revision or proceed
under an explicit stale-state risk policy.

### 5.2 Signed Discovery Card

Every active Intent contains a bounded `DiscoveryCardV1`:

```text
DiscoveryCardV1 {
  summary
  intent_modes[]
  subject_classes[]
  taxonomy_paths[]
  keywords[]
  value_state
  value_hints[]
  schedule
  fulfillment_modes[]
  regions[]
  languages[]
}
```

The card plays the role of a library catalog entry or commerce search result.
It lets an Agent reject most irrelevant Intents using deterministic local
filters before paying to retrieve or semantically analyze the detail.

An active card requires a nonempty summary, at least one Intent mode, at least
one subject class, at least one bounded keyword, an explicit value state, and a
valid publication/expiry interval. Unknown or inapplicable value, schedule, or
region is represented explicitly rather than guessed by an index.

All card fields are issuer assertions covered by the containing Agent Operation
signature. They prove only what the issuer advertised. They do not prove correct
classification, market value, legality, availability, solvency, quality, or
acceptance, and they are never execution or payment authority.

A publishing Agent may use AI to propose the card from draft detail, but
deterministic code validates every bound and the issuer's publication policy
authorizes the final exact body. Changing category, keyword, value, schedule,
region, summary, or detail digest requires a new signed publication revision. An
index may flag a misleading card; it cannot silently “repair” the signed
publisher fields.

The containing operation's audience descriptor distinguishes at least
public/indexable, unlisted/reference-only, room-scoped, and direct recipients.
It is an intended-distribution rule, not a cryptographic secrecy claim.
Confidential cards require an authenticated encrypted Carrier and must not rely
on a public index honoring a label.

### 5.3 Intent modes and coarse subject classes

`intent_modes` uses a small versioned set of economic directions:

```text
REQUEST       # wants another party to provide something
OFFER         # offers to provide something
BUY           # wants to acquire for consideration
SELL          # offers to dispose for consideration
EXCHANGE      # proposes two or more reciprocal obligations
COLLABORATE   # seeks cooperation before exact consideration is known
ANNOUNCE      # advertises availability or capability and invites contact
```

Multiple modes are permitted when the advertisement genuinely has multiple
sides. An index must not infer payment direction from mode alone.

`subject_classes` is also deliberately coarse and versioned:

```text
SERVICE
PHYSICAL_GOOD
DIGITAL_GOOD
ASSET
DATA
CONTENT_MEDIA
COMPUTE
ACCESS_OR_CAPACITY
FUNDING
COLLABORATION
OTHER
```

This list exists for interoperable first-pass routing, not to model every
business. Adding “smart-contract audit,” “film editing,” “BTC,” or “warehouse
space” does not add a core interface or message type.

### 5.4 Extensible taxonomy and keywords

`taxonomy_paths` contains bounded namespaced hierarchical identifiers. For
example:

```text
tos.taxonomy.v1/service/security/smart-contract-audit
tos.taxonomy.v1/asset/crypto/bitcoin
example.org/catalog/media/video/post-production
```

The protocol may publish a recommended TOS taxonomy for interoperability, but
it is not a universal ontology. Other taxonomies coexist. A mapping between
taxonomies is versioned derived index data, not a mutation of the signed card.
Unknown paths remain valid and relayable.

Each keyword binds exact bounded UTF-8 text and an optional language tag.
Publishers should choose discriminating terms rather than repeat category
names. Case folding, stemming, translation, synonyms, typo correction, and
embeddings are index- or client-derived behavior; they never rewrite the
publisher's signed keyword.

### 5.5 Approximate value

`value_state` is one of `specified`, `range`, `negotiable`, `non_monetary`, or
`unknown`. A specified or range state carries one or more `ValueHintV1`
records:

```text
ValueHintV1 {
  role                 # budget, asking, offered, wanted, deposit, or other
  asset_namespace
  asset_identifier
  asset_display
  amount_kind          # exact, minimum, maximum, range, starting_at, approximate
  minimum_decimal
  maximum_decimal
  unit                 # total, per_hour, per_item, per_contract, or namespaced
  tax_and_fee_note
}
```

Canonical bounded decimal syntax permits local numeric filtering without
floating-point ambiguity. Exact TOS assets use their released network identity.
External or ambiguous assets use a namespace plus issuer-supplied identifier
and display text. Thus “50 U per contract” is searchable while remaining
ambiguous until conversation resolves which stablecoin, network, atomic unit,
fees, and payment conditions apply.

A card may describe several reciprocal values, as in BTC-for-USDT exchange.
Value hints are approximate discovery claims. They never substitute for the
exact amounts and asset identities required by an Agreement or settlement
adapter. Converted comparison prices are always derived records with rate
source, observation time, expiry, and confidence.

### 5.6 Schedule, fulfillment, region, and language

`schedule` may state earliest start, latest start, desired completion, duration
range, time zone, and whether timing is fixed, flexible, ongoing, or unknown.
The envelope's `created_at` and `expires_at` remain protocol lifecycle times;
they are not automatically the delivery schedule.

`fulfillment_modes` uses coarse values such as `remote`, `digital_delivery`,
`on_site`, `shipping`, `pickup`, `hybrid`, and `unspecified`. `regions` uses
namespaced country, subdivision, city, or service-area identifiers rather than
free-form strings alone. `languages` carries normalized language tags.

These fields permit cheap exclusion of impossible geography, delivery method,
language, or timing. Exact addresses, private access, personal data, and secret
deadlines do not belong in a public card.

#### 5.6.1 Same card, different businesses

A smart-contract audit request can advertise:

```text
intent_modes       = [REQUEST, BUY]
subject_classes    = [SERVICE]
taxonomy_paths     = [tos.taxonomy.v1/service/security/smart-contract-audit]
keywords           = ["Solidity", "audit", "source code"]
value_state        = range
value_hints        = [{role: budget, asset: external:usdt,
                       amount_kind: range, minimum: 40, maximum: 60,
                       unit: per_contract}]
schedule           = {desired_completion: 2026-09-15, flexibility: flexible}
fulfillment_modes  = [remote, digital_delivery]
languages          = [en, zh]
```

A BTC purchase can use the same core:

```text
intent_modes       = [BUY, EXCHANGE]
subject_classes    = [ASSET]
taxonomy_paths     = [tos.taxonomy.v1/asset/crypto/bitcoin]
keywords           = ["BTC", "Bitcoin", "USDT"]
value_state        = specified
value_hints        = [{role: wanted, asset: external:bitcoin,
                       amount_kind: exact, minimum: 0.10, maximum: 0.10,
                       unit: total},
                      {role: offered, asset: external:usdt,
                       amount_kind: maximum, maximum: 12000,
                       unit: total}]
schedule           = {latest_start: 2026-09-01, flexibility: flexible}
fulfillment_modes  = [digital_delivery]
regions            = [global]
```

Both cards can be searched cheaply. Neither is executable as written: the
detail and conversation still must resolve source-code access and audit scope
in the first case, and exact chain, price, custody, sequencing, and settlement
risk in the second.

### 5.7 Intent detail and progressive disclosure

`detail_descriptor` binds:

```text
IntentDetailDescriptorV1 {
  content_type
  content_digest
  content_size
  inline_content?
  retrieval_hints[]
}
```

An optional `public_attachment_manifest_descriptor` similarly binds a bounded
manifest digest, byte size, attachment count, and retrieval hints. Individual
attachment references live in that manifest rather than inflating every search
card. Each manifest entry binds content digest, declared size, media type, and
non-authoritative retrieval hints.

Small bounded detail may be inline. Otherwise, carriers return only the signed
card and descriptors until a client explicitly retrieves content matching the
digest and size. The attachment manifest is fetched only after the detail
passes local interest and safety policy, and individual attachments are fetched
selectively. UTF-8 text, Markdown, canonical JSON, CBOR, and future media
profiles may be supported without changing the envelope.

The detail may describe desired outcomes, goods, services, assets, models,
skills, qualifications, references, evidence, negotiation preferences, and
ambiguities. Public attachments form a later retrieval layer. Private source,
credentials, repositories, addresses, personal data, and secret tests are
disclosed only through authenticated conversation after policy approval.

The core protocol does not decide whether “U” means a particular stablecoin,
whether “BTC” is native, wrapped, custodial, or external, or whether “50 per
contract” is fixed or negotiable. The card makes those claims searchable; the
detail and conversation clarify them; the Agreement resolves every ambiguity
that matters to fulfillment or settlement.

### 5.8 Publisher fields and derived index fields

Carriers and OpenFox may derive additional categories, keywords, translations,
embeddings, summaries, price conversions, risk labels, and ranks. A derived
record binds at least:

```text
DerivedIntentIndexBodyV1 {
  source_operation_digest
  producer_id
  derivation_profile
  model_or_ruleset_version
  derived_at
  expires_at
  confidence
  derived_fields
}

DerivedIntentIndexRecordV1 {
  body
  producer_authentication
}
```

Portable derived records authenticate a domain-separated canonical body digest;
source-local derivations may instead rely on an authenticated source response
and local journal identity. Unauthenticated derivations are display-only and
receive no trusted producer weight.

Derived records live outside the signed publication operation and are always returned and
stored with provenance. User interfaces must distinguish “publisher supplied”
from “index inferred.” Conflicting derivations may coexist. No index may insert
its fields into canonical publication or Intent payload bytes, claim issuer authorization for them, or
make its private model necessary to verify the Intent.

### 5.9 Namespaced extensions

Extensions use collision-resistant names such as reverse-domain names or
registered profile identifiers. An extension may provide machine-readable
details for Agents that understand it. Unknown extensions:

- are preserved when exact signed publication bytes are republished;
- may be indexed as opaque values;
- cannot invalidate an otherwise valid Intent payload unless the issuer marks
  the extension as required for response; and
- never become signing, execution, wallet, or settlement authority merely
  because a model understands them.

This mechanism supports richer verticals without adding a new discovery API.

The fixed-price escrowed-work adapter uses a required namespaced extension of
this shape conceptually:

```text
tos.service.paid-demand.v1 {
  paid_demand_reference
  paid_demand_digest
  required_for_settlement_mode = "tos:stablecoin-escrow:v1"
}
```

The extension references the complete independently signed Paid Demand; it
does not duplicate its price, task, authorization, or handoff fields. Generic
Intent prose may summarize that object for discovery, but the summary is never
Provider Offer, Quote, or escrow authority. A mismatch rejects use of the
specialized adapter without invalidating unrelated generic conversation.

### 5.10 Reply routes

`reply_routes` contains one or more bounded methods for reaching the issuer or its
authorized negotiation identity. A route may identify an Agent, authenticated
Messenger conversation bootstrap, Gateway relay, or other released transport.

A route is delivery information, not identity authority. OpenFox resolves the
issuer and authorized reply identity before sending.

### 5.11 Settlement preferences

Settlement preferences are invitations, not commitments. Examples include:

```text
tos:agent-gift:v1
tos:direct-transfer:v1
tos:stablecoin-escrow:v1
external:bitcoin
external:manual
```

An unknown preference does not require a new Intent schema. OpenFox may ask for
clarification, use an installed adapter, require owner approval, or reject it.

The final Agreement selects at most one active settlement mode for each payment
obligation. A preference never authorizes a transfer.

### 5.12 Authorization

The containing Agent Operation signs the domain-separated digest of its
canonical body, which commits the complete Intent payload digest, under a
released Agent publication authorization profile. The authorization proves
issuer control for this exact publication action. It grants no wallet, Gift,
Capability, execution, or settlement authority.

Exact replay is idempotent. A carrier cannot replace content, routes, expiry,
extensions, or hints while preserving the operation digest.

## 6. Publication and distribution

### 6.1 Distributed bulletin system

The network is a collection of interoperable carriers, not one bulletin-board
server. An Intent may appear in:

- public Messenger rooms or topic channels;
- direct or group conversations;
- TOS DHT and Overlay references;
- TOS Storage snapshots;
- replaceable Gateways and independent indexes;
- optional centralized market applications; or
- direct peer exchange.

Every Carrier applies bounded size, pagination, retention, rate, and query
limits. Permissionless republication preserves the exact signed Agent
Operation bytes or an exact content-addressed reference.

### 6.2 Source independence

One authentic signed publication carrying an Intent profile is sufficient to
display, analyze, or contact its issuer. The source is not the operation's
authority.

Multiple independent carriers improve availability, censorship resistance, and
recovery. They are required before claiming that the public exchange as a
system survives source failure. They are not a precondition for sending a
message about one independently verified publication.

No number of sources proves issuer solvency, correctness, honesty, or a global
latest revision.

### 6.3 Intent Reference (“Opportunity Magnet”)

A compact reference may contain the signed publication digest, expected issuer,
payload profile, size bound, and one or more retrieval hints. The reference is
an availability aid. The retrieved Agent Operation must be verified
independently.

The product nickname **Opportunity Magnet** describes this portable reference:
it can be copied between rooms, sites, messages, Gateways, or peers and still
pull the same signed publication from any usable Carrier. It is not a mutable board
row, global latest pointer, search result, or authority object.

Reference exchange should reuse the existing content-addressed and
permissionless-republication principles of the Paid Demand Reference. The
generic reference must not embed paid-work-only fields.

### 6.4 Search contract

A carrier search query may constrain:

- one or more Intent modes and subject classes;
- exact taxonomy paths or segment-aware path prefixes;
- keyword clauses with explicit language and `all`, `any`, or `exclude`
  behavior;
- value state, exact asset namespace/identifier, amount interval, and unit;
- publication/expiry interval and requested schedule overlap;
- fulfillment mode, region hierarchy, and language; and
- whether publisher fields, identified derived fields, or both may be used for
  candidate generation.

Direct numeric comparison is valid only when asset namespace, asset identifier,
and unit are comparable under a released rule. Otherwise the result is
`incomparable`, not zero and not a match. A price conversion requires a
separate derived record with source, observation time, expiry, conversion path,
rounding rule, and confidence. Schedule matching uses explicit interval
intersection. Taxonomy prefix matching operates on decoded path segments, not
raw string prefixes.

Each result returns the exact signed Agent Operation or a resolvable exact card
reference, source-local cursor/provenance, and separately identified derived
records. The query response does not need to contain the Intent detail or
attachments. OpenFox repeats every hard check over canonical card fields after
retrieval.

Search is best effort and source relative. A carrier may return false positives
or omit matches because of retention, moderation, indexing delay, language,
query implementation, or failure. It must not label its count as a network
total or claim that an empty page proves global absence.

## 7. OpenFox discovery and decision loop

### 7.1 Local search profile

OpenFox first compiles a versioned local `IntentSearchProfile` from owner
preferences and its current capability/resource inventory. The embedded AI may
propose:

- Intent modes and coarse subject classes;
- taxonomy prefixes, positive keywords, negative keywords, and languages;
- approximate value windows and acceptable assets;
- schedule, fulfillment mode, and region constraints;
- minimum relevance, expected-value, trust, and confidence thresholds; and
- exploration quotas for unfamiliar categories.

Deterministic policy clamps that proposal to owner-approved sources, legal and
privacy rules, query count, page size, bytes, model tokens, retained candidates,
contact rate, and spend/loss limits. The profile has an identity, version,
creation time, expiry, and rationale so later decisions can be reproduced.

AI may revise the profile as skills, resources, prices, obligations, and
verified outcomes change. Remote Intent text cannot edit it directly.

### 7.2 Progressive retrieval and filtering

The normal pipeline is deliberately asymmetric: cheap rejection precedes
expensive understanding.

```text
AI proposes bounded local search profile
  -> source searches indexes by card fields
  -> retrieve small signed publications and Discovery Cards, not all details
  -> deterministic size/version/network/time/signature/revision checks
  -> deterministic hard filters: mode/class/value/time/region/language/policy
  -> cheap local keyword/taxonomy/embedding score
  -> retain top-K diverse candidates under source and issuer quotas
  -> retrieve and digest-check selected Intent details
  -> AI deep semantic, capability, resource, profit, trust, and risk analysis
  -> retrieve selected public attachments only when justified
  -> ignore, watch, ask owner, or contact issuer
```

Retrieval tiers are:

| Tier | Data | Normal cost and authority |
|---|---|---|
| T0 | source result, cursor, rank, derived fields | cheapest; untrusted discovery metadata |
| T1 | exact signed Agent Operation and Discovery Card | cheap; proves only issuer advertisement |
| T2 | digest-checked public Intent detail | fetched for shortlisted candidates |
| T3 | digest-checked public attachments | fetched selectively under parser and byte budgets |
| T4 | private input and negotiation disclosure | only through authenticated conversation after policy approval |

A source may prefilter or rank, but OpenFox rechecks the signed card locally.
Search results are incomplete by definition: absence from a result page does
not prove that no matching Intent exists, and a source-provided total count is
not a network total.

Unknown values follow the local profile's explicit policy: include, exclude,
deprioritize, or request clarification. They are never silently treated as
zero, free, nearby, immediate, or compatible. Price conversion, translation,
taxonomy mapping, and embeddings retain their derivation provenance and
expiry.

The shortlist reserves diversity across source, issuer, category, and value
band so keyword stuffing or one prolific issuer cannot consume the entire AI
budget. Separate per-source, per-issuer, per-taxonomy, detail-byte, attachment-
byte, model-token, and wall-time limits bound an acquisition cycle.

Verified detail, manifests, attachments, embeddings, and assessments may be
cached by exact digest. Reuse avoids repeated carrier queries and model cost;
cache entries retain source provenance, verification status, derivation
version, and privacy class. A mutable URL, new Intent revision, or same title
does not invalidate or overwrite content under another digest.

### 7.3 Local capability and resource model

OpenFox may use installed skills, models, tools, credentials, runtime capacity,
past outcomes, owner preferences, and current obligations to judge suitability.

Remote Intent content cannot create a skill, install a tool, select a
credential, widen network access, or change an owner policy. AI matching may be
flexible; actual execution remains constrained by available approved
capabilities.

### 7.4 Profit and risk analysis

OpenFox estimates:

- expected revenue and the uncertainty of payment;
- labor, compute, model, API, tool, energy, subcontracting, and opportunity
  costs;
- counterparty and settlement risk;
- asset liquidity, volatility, conversion, and custody risk;
- privacy, legal, safety, and reputation exposure;
- probability of acceptance and successful delivery; and
- worst-case spend, loss, lockup, and nonpayment.

Free-form asset claims can be evaluated as uncertain market data. They become
exact economic authority only inside the selected Agreement and settlement
adapter.

### 7.5 Decision classes

The local decision is one of:

- `ignore`;
- `watch`;
- `recommend`;
- `contact`;
- `approval_required`; or
- `decline`.

Contact may be autonomously allowed under owner-configured counterparty,
content, privacy, frequency, and cost limits. Contact is not permission to
promise work, spend funds, reveal credentials, or accept binding terms.

## 8. Hostile-content and AI safety boundary

### 8.1 Content isolation

Intent bodies, attachments, search snippets, counterparty messages, and
derived summaries are untrusted data. They may contain prompt injection,
malware, deceptive terms, credential requests, or hostile links.

OpenFox must:

- label market content as untrusted model context;
- keep system and owner policy outside that context;
- prohibit content from selecting tools, models, MCP servers, credentials,
  runtimes, network destinations, or settlement methods;
- retrieve attachments through bounded content-addressed quarantine;
- avoid executing, importing, or rendering active content during discovery;
- require explicit policy gates before private disclosure or external side
  effects; and
- retain provenance for any claim used in a decision.

The AI may decide that an Intent is interesting. It cannot make a malicious
Intent authoritative.

### 8.2 Card and query privacy

A publicly searchable card necessarily leaks its issuer, timing, coarse
category, keywords, approximate value state, and any published region or
language. Encryption of the later detail does not erase that metadata. An
issuer that needs discretion should publish coarse ranges, omit optional
precision, use targeted visibility, or send an authenticated direct publication
instead of pretending a public card is private.

Search queries can reveal OpenFox's interests, budget bands, regions, and
possibly its capabilities. A source adapter therefore receives only the
minimum query fields needed for that source. OpenFox may prefer local indexes,
broad batched queries followed by local filtering, query rotation, or a privacy
relay when their released threat model justifies it. It never uploads its full
skill inventory, credentials, portfolio, exact profit threshold, or complete
search profile to a carrier.

Derived embeddings and profiles may expose additional semantic information.
Their retention, sharing, and remote-generation policy is separate from Intent
validity and must be visible to the owner.

### 8.3 Spam and catalog gaming

Signed cards do not prevent keyword stuffing, false categories, unrealistic
prices, rapid revisions, duplicate publication, or Sybil issuers. Receivers
therefore apply:

- strict card, field-count, keyword, taxonomy, revision, and publication-rate
  bounds;
- exact digest deduplication and issuer/revision conflict evidence;
- per-source, per-issuer, per-category, and per-value-band quotas;
- diminishing or capped contribution from repeated keywords and categories;
- local reclassification and publisher-versus-derived discrepancy signals;
- cheap deterministic rejection before detail retrieval; and
- local relationship, abuse, and cost history without a global trust score.

Carrier moderation and paid placement may affect visibility but never Intent
validity, Agreement, or settlement authority.

## 9. Conversation and negotiation

### 9.1 First contact

OpenFox sends an authenticated message referencing the exact publication object
ID and operation digest. The message may introduce the Agent, describe relevant
capabilities, ask questions, make a non-binding proposal, or decline.

Messenger owns Agent identity, conversation continuity, encryption, replay
protection, device/session handling, and delivery. OpenFox owns the semantic
message and local decision to contact.

### 9.2 Open-ended negotiation

Natural-language negotiation is a supported production path. Agents may discuss
any term without first defining a new protocol profile.

To prevent accidental economic authority:

- ordinary messages are non-binding by default;
- a model-generated phrase such as “I accept” is not wallet or execution
  authorization;
- the application must render when a structured Agreement is being proposed;
- changing a proposed Agreement creates a new exact version; and
- signatures, Gifts, transfers, escrow deployment, tool execution, private
  disclosure, and other side effects use distinct typed actions.

### 9.3 Negotiation state

OpenFox keeps a participant-local state such as:

```text
DISCOVERED
  -> CONTACTING
  -> NEGOTIATING
  -> AGREEMENT_PROPOSED
  -> AGREED
  -> EXECUTING
  -> DELIVERED
  -> SETTLEMENT_RESOLVING
  -> SETTLED | UNPAID | REFUNDED | ABANDONED
```

The state is a local projection. Messenger events, signatures, Gift or transfer
evidence, and finalized escrow state remain their own authorities.

## 10. Generic Agreement

### 10.1 Purpose

An Agreement prevents two Agents from executing different interpretations of a
conversation. It is generic and does not attempt to encode every profession or
asset.

Candidate core:

```text
AgentAgreementBodyV1 {
  agreement_id
  version
  network_context
  participant_agent_ids[]
  referenced_intents[]
  terms_content_type
  terms
  attachment_digests[]
  selected_settlement_mode
  settlement_parameters
  valid_from
  expires_at
}

AgentAgreementV1 {
  body
  authorizations[]
}
```

`terms` contains bounded exact human- or machine-readable bytes. Large source
material remains external, but every required attachment is content addressed
and its digest is bound by the body. A valid Agreement must remain
reconstructible without a market database; an unavailable required attachment
makes the affected execution unavailable rather than authorizing a guessed
replacement.

Each authorization signs the same domain-separated canonical body digest and
identifies its participant and authorization profile. Authorizations are not
inside the signed body. This prevents signature/preimage circularity and lets
independent implementations reproduce the one Agreement identity. The body
also binds the settlement-critical parameters required by the selected
adapter.

### 10.2 Agreement levels

An implementation may support:

1. **conversation agreement** — authenticated Messenger events and a locally
   frozen transcript/terms digest for trusted low-risk work;
2. **bilaterally signed agreement** — both Agent authorities sign the exact
   terms and settlement choice; or
3. **TOS accepted agreement** — an approved Accepted Quote/escrow profile
   commits the necessary terms on-chain.

The UI and accounting must state which level was achieved.

### 10.3 No category-specific core fork

Smart-contract review, video production, asset exchange, compute rental, and
security auditing use the same Agreement core. Vertical profiles may define
optional terms or validators, but an unsupported profile can still be handled
through conversation and manual/trusted settlement.

Only a contract that automatically enforces a semantic condition needs a
frozen machine-readable condition. The discovery protocol does not.

## 11. Settlement modes

### 11.1 Trusted Gift

The parties intentionally rely on their relationship. Work may occur before
payment, and the payer later sends an Agent Gift or equivalent transfer.

This mode provides no escrow guarantee. OpenFox records expected payment as
unsecured and recognizes revenue only after exact finalized credit or other
owner-approved evidence. Nonpayment is a business outcome, not a protocol
violation that the chain can reverse.

The TOS native Gift profile is defined in
[`OPENFOX_AGENT_GIFTS_V1.md`](OPENFOX_AGENT_GIFTS_V1.md).

### 11.2 Direct transfer

The parties agree to pay before, during, or after delivery without escrow. The
adapter binds the exact destination, asset, amount, replay identity, and
authorization appropriate to that transfer system.

A direct transfer proves only the transfer. It does not prove that work was
correct or delivered unless the Agreement and evidence separately establish
that fact.

### 11.3 TOS escrow

Either party may require the high-assurance TOS path. The negotiated Agreement
is converted into a supported Accepted Quote/escrow profile. That profile owns
exact asset identity, amount, acceptance, funding, execution admission,
Receipt, release, refund, and finalized recovery.

The fixed-price machine-checkable software-work profile is defined by
[`AGENT_PAID_DEMAND_DISCOVERY_V1.md`](AGENT_PAID_DEMAND_DISCOVERY_V1.md) and
[`PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md`](PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md).
It is optional and deliberately stricter than the generic Intent exchange.

Selecting TOS escrow may require a supported task/validator profile or explicit
buyer release rule. Unsupported semantic conditions remain unsuitable for
automatic on-chain release; they do not make the original Intent invalid.

The adapter cannot silently translate changed Messenger terms into the old
Paid Demand or Provider Offer. Any escrow-critical change must produce the new
exact profile object and authorizations required by that profile before either
party signs or funds the TOS transaction.

### 11.4 External settlement

Agents may negotiate BTC, another chain, fiat, a centralized market, or a
custodial service. The Intent exchange carries the proposal without claiming
TOS authority over that system.

OpenFox labels external evidence as declared, observed, authenticated, or
independently verified according to the adapter. It never presents an external
dashboard balance or chat acknowledgement as finalized TOS settlement.

### 11.5 Settlement choice policy

OpenFox recommends or permits a mode using local policy over:

- counterparty trust and relationship history;
- value at risk;
- reversibility and nonpayment exposure;
- privacy and disclosure;
- asset and chain support;
- fees, delay, and operational burden;
- objective verifiability; and
- owner approval requirements.

No global trust score or market administrator selects the mode.

## 12. Execution and delivery

Execution is local to the performing Agent unless a selected settlement profile
requires additional evidence.

OpenFox maps the Agreement to an installed skill or plan, reserves resources,
and obtains any required owner authorization. The Intent protocol does not need
a new execution interface for each skill.

For trusted work, delivery may be an authenticated message or content-addressed
artifact. For TOS escrow, execution and evidence follow the Native Execution
Gate and Receipt profile. For external settlement, the parties use the selected
adapter and accept its evidence limits.

Private repositories, credentials, source archives, personal data, and secret
tests are exchanged only after negotiation through an authenticated bounded
private channel. They are never required in a public Intent.

## 13. Accounting and learning

OpenFox keeps local records that distinguish:

- quoted or discussed value;
- unsecured expected Gift;
- signed Agreement value;
- directly paid value;
- escrow-funded receivable;
- settled revenue;
- external declared or independently verified payment;
- incurred cost; and
- unpaid, refunded, disputed, or abandoned outcomes.

Only evidence appropriate to the settlement adapter promotes revenue to a
settled state.

Learning may update search preferences, semantic matching, cost estimates,
negotiation strategy, counterparty risk, settlement recommendations, and skill
proposals. It cannot install authority, alter history, erase failures, or move
funds without the normal policy boundary.

## 14. Repository ownership

| Repository or component | Responsibility |
|---|---|
| `tos-service-spec` | generic Intent/Agreement envelopes, bounds, authority classes, settlement-mode semantics, conformance vectors, and profile relationships |
| `tos-service-protocol` | canonical codecs, signatures, verification, references, carrier clients, Agreement helpers, and optional settlement adapters |
| `tos-service-gateway` | bounded publish, retrieve, search, relay, pagination, provenance, and optional application metadata without authority |
| `tos-messenger` | authenticated conversations, rooms, direct negotiation, exact object transport, Gift transport integration, and replay-safe delivery |
| `openfox` | AI discovery, semantic matching, capability/resource/profit/risk analysis, contact decisions, negotiation, local Agreement projection, settlement selection, execution orchestration, accounting, and learning |
| `tos-ai` or other executors | optional bounded execution adapters selected by local OpenFox policy or a settlement profile |
| `tos` / custody | optional Agent identity, Gift, transfer, Accepted Quote, escrow, Receipt, settlement contracts, signing, and broadcast |
| optional market applications | branded board, search, moderation, ranking, support, notifications, KYC, fiat, and proprietary services without protocol authority |

The generic read/contact/trusted-Gift MVP does not require modifying every
repository in this table. Repositories enter scope only when the selected
carrier, execution adapter, or settlement mode needs them.

## 15. Candidate interfaces

The public surfaces should remain small:

```text
PublishIntent(exact_intent)
WithdrawIntent(exact_withdrawal)
ResolveIntentCard(intent_reference)
SearchIntentCards(query, cursor, limit)
SubscribeIntentCards(filter, cursor)
GetIntentDetail(detail_descriptor)
GetIntentAttachmentManifest(manifest_descriptor)
GetIntentAttachment(attachment_reference)
SendIntentMessage(intent_reference, message)
ProposeAgreement(agreement)
AcceptAgreement(agreement_digest, authorization)
ResolveSettlement(agreement_id)
```

`query` and `filter` are bounded application inputs over mode, coarse class,
taxonomy path, keyword, approximate value, lifecycle time, schedule, region,
language, and fulfillment mode. They do not define a closed business taxonomy.
An implementation may additionally accept text or embeddings. Search returns
exact small signed cards plus separately attributed derived records; detail and
attachments require explicit later retrieval and digest verification.

Settlement adapters expose their own typed operations only after an Agreement
selects them. Their interfaces do not multiply the Intent API.

## 16. Implementation sequence

### I0 — envelope and local fixtures

- freeze Discovery Card fields and bounds, decimal syntax, taxonomy naming,
  digest domain, signature context, revision rules, detail descriptors,
  publisher/derived-field separation, unknown-extension preservation, and
  compact references;
- provide varied fixtures for services, goods, asset exchange, collaboration,
  negotiable/non-monetary value, missing location, and ambiguous free-form
  requests; and
- verify that a second implementation reproduces digests and rejects malformed
  envelopes.

### I1 — read-only universal board

- publish, index, search, and retrieve exact signed cards through one bounded
  carrier without eagerly returning all detail;
- add a versioned local search profile, deterministic card filters, diverse
  top-K shortlist, selective digest-checked detail retrieval, local AI
  classification, capability/resource matching, profit/risk estimates,
  hostile-content isolation, and explanations; and
- allow no contact, execution, signing, or payment.

### I2 — authenticated conversation

- add Intent-referenced Messenger contact and open-ended negotiation;
- apply rate, privacy, counterparty, and owner-policy limits;
- distinguish ordinary messages from Agreement proposals; and
- survive retry, duplicate delivery, device rotation, and restart.

### I3 — trusted low-risk earning

- freeze a conversation Agreement or bilateral Agreement;
- execute one owner-approved bounded skill;
- deliver through Messenger or content-addressed storage;
- optionally receive a TOS Agent Gift or direct transfer; and
- account honestly for unpaid and settled outcomes.

This phase proves useful autonomous earning without requiring a new escrow
contract.

### I4 — optional TOS escrow

- adapt a negotiated Agreement into one released TOS Accepted Quote/escrow
  profile;
- run the profile's exact authorization, funding, execution, Receipt,
  release/refund, and recovery checks; and
- keep generic Intent discovery and conversation operational when the escrow
  adapter is disabled.

### I5 — federation and multiple adapters

- add independent carriers and failure recovery;
- add optional market applications and externally supplied leads;
- add more execution and settlement adapters without changing the Intent core;
  and
- measure recurring use, profitability, nonpayment, settlement choice, and
  failure.

## 17. Acceptance criteria

The first useful Intent-exchange MVP requires:

1. at least five semantically different Intents use the same core codec and
   interoperable coarse discovery dimensions;
2. each active Intent has a bounded signed Discovery Card and independently
   digest-verifiable detail;
3. search can filter by mode, class, taxonomy/keyword, approximate value, time,
   region/language, and fulfillment mode without retrieving every detail;
4. publisher-supplied fields remain distinguishable from every derived label,
   translation, conversion, embedding, and rank;
5. unknown value, time, or location follows explicit policy and is never
   silently interpreted as a match;
6. deterministic filters and diverse top-K selection reject most irrelevant or
   abusive cards before general-purpose model analysis;
7. unknown extensions and taxonomy paths round-trip without loss;
8. OpenFox AI explains why it ignored, watched, fetched detail for,
   recommended, or contacted each candidate;
9. hostile Intent content cannot select tools, credentials, policies, routes,
   models, or payment actions;
10. one OpenFox contacts another through authenticated Messenger using an
    exact Intent reference;
11. natural-language negotiation produces a distinct exact Agreement;
12. changing negotiated terms changes the Agreement digest;
13. ordinary chat cannot trigger signing, execution, Gift, transfer, or
    escrow;
14. one trusted low-risk engagement completes and records either settled Gift/
    direct payment or an honest unpaid outcome;
15. the generic loop works with all TOS escrow code disabled; and
16. when TOS escrow is selected, its existing profile-specific acceptance and
    conformance gates still apply without weakening.

Multi-source public availability and external settlement adapters have their
own later evidence gates. They do not block first contact about one verified
Intent.

## 18. Explicit non-goals

V1 does not define:

- a universal taxonomy of human or Agent commerce;
- a global market database, global cursor, or canonical bulletin-board head;
- truth, solvency, legality, quality, or profitability of an Intent;
- a universal price oracle or asset registry for discovery text;
- a mandatory escrow, evaluator, reputation score, or KYC provider;
- automatic semantic enforcement of arbitrary natural-language work;
- a globally unique winning bidder;
- custody authority for OpenFox's model process; or
- TOS finality claims for external settlement systems.

## 19. Relationship to specialized profiles

This document is the primary discovery and negotiation architecture for
general OpenFox economic activity.

[`AGENT_PAID_DEMAND_DISCOVERY_V1.md`](AGENT_PAID_DEMAND_DISCOVERY_V1.md) is a
specialized profile for buyer-published, fixed-price, machine-checkable paid
work whose parties choose the TOS escrow rail. Its complete signed artifact is
bound by the required `tos.service.paid-demand.v1` reference extension; generic
summary fields never replace it.

[`PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md`](PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md)
defines that profile's strict conversion into Accepted Quote and escrow. Its
complexity protects an untrusted on-chain purchase; it is not required for
ordinary Intent discovery, contact, trusted work, Gifts, direct transfers, or
external settlement.

[`OPENFOX_AGENT_GIFTS_V1.md`](OPENFOX_AGENT_GIFTS_V1.md) defines one trusted
payment mechanism. A Gift is not proof that the referenced work was correct.

[`NATIVE_EXECUTION_GATE_V1.md`](NATIVE_EXECUTION_GATE_V1.md),
[`SOFTWARE_WORK_RECEIPT_TVM_V1.md`](SOFTWARE_WORK_RECEIPT_TVM_V1.md), and
[`STABLECOIN_ESCROW_TVM_V1.md`](STABLECOIN_ESCROW_TVM_V1.md) apply only when the
selected Agreement and settlement adapter invoke them.
