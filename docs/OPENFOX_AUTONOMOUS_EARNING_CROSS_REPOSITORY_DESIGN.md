# OpenFox Autonomous Earning — Operation-Composed Cross-Repository Design

**Status:** proposed cross-repository architecture; implementation and external
acceptance pending

**Root architecture:**
[`TOS_AGENTIC_INTERNET_OPERATION_ARCHITECTURE_V1.md`](TOS_AGENTIC_INTERNET_OPERATION_ARCHITECTURE_V1.md)

**Publication and Intent profile:**
[`AGENT_INTENT_EXCHANGE_V1.md`](AGENT_INTENT_EXCHANGE_V1.md)

**Semantic side-effect identity:**
[`SEMANTIC_ACTION_IDENTITY_V1.md`](SEMANTIC_ACTION_IDENTITY_V1.md)

**Optional high-assurance settlement profile:**
[`PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md`](PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md)

## 1. Executive decision

OpenFox autonomous earning is an application composed from general Agentic
Internet operations, not a task-type-specific labor protocol and not a
mandatory on-chain marketplace. Intent is the discovery payload profile;
`POST`, `MESSAGE`, `AGREEMENT`, `VALUE`, and optional `SETTLEMENT` operations
provide the reusable interaction primitives.

The primary product loop is:

```text
observe a signed POST carrying a generic Intent profile
  -> use OpenFox's local AI to understand it
  -> compare it with local skills, resources, cost, and risk
  -> contact the issuer through authenticated Messenger
  -> negotiate arbitrary terms
  -> select settlement for every value-bearing obligation
  -> compile exact obligations and satisfy body-bound authorization predicates
  -> validate adapters, reserve aggregate exposure, and prove required funding
  -> enter the local Execution Gate, execute, and deliver
  -> resolve each obligation, account, and learn
```

An Intent may express buying, selling, offering, requesting, exchanging, or
collaborating. OpenFox core does not add a new interface whenever a new
profession, asset, model, or product appears. New business behavior normally
enters through content, taxonomy, a Skill, or an Adapter.

TOS Accepted Quote, escrow, Native Execution Gate, Receipt, and finalized
settlement remain valuable. They are invoked only when an accepted Agreement
obligation selects a supported TOS escrow mode. Trusted Agents may instead
select an Agreement-bound direct-payment adapter and knowingly accept unsecured
receivable risk. An Agent Gift remains an independent gratuity and never closes
an Agreement obligation. External assets and centralized applications may be
used with explicitly weaker or different evidence.

This decision changes the implementation dependency from “seven repositories
before earning can begin” to staged optionality:

- generic read-only Intent discovery needs the specification, protocol codec,
  OpenFox, and at least one carrier;
- authenticated negotiation adds Messenger;
- trusted execution adds only the local skill/executor, selected payment
  adapter, and owner/Agent economic action authority;
- TOS contract, Gate, Receipt, and settlement work enters scope only for the
  optional escrowed profile.

## 2. Why this architecture follows first principles

### 2.1 The network cannot know every business

Economic intent is open ended. “Review this contract,” “sell BTC,” “buy USDT,”
“make a video,” and “provide security auditing with a specialized model” do not
share a useful closed task schema.

Trying to freeze all semantic fields in the discovery protocol creates an
ever-growing interface, blocks new categories, and moves local reasoning into
protocol governance. OpenFox already has an AI capable of interpreting these
statements. The common network responsibility is therefore bounded signed
publication and contact, not universal semantic understanding.

### 2.2 Trust determines enforcement cost

Not every transaction needs escrow. Requiring a smart contract for trusted,
low-value work creates fees, delay, operational burden, new failure modes, and
unnecessary protocol dependencies.

Conversely, a chat promise is insufficient when the parties do not trust one
another or when value at risk is high. The settlement choice for every
value-bearing obligation must therefore be an explicit result of negotiation
and local risk policy, and must be fixed before either party accepts the
Agreement or starts irreversible work.

### 2.3 Free-form discovery must not become free-form authority

An open Intent and natural-language conversation are useful precisely because
they are flexible. That flexibility is unsafe if text can directly sign,
spend, reveal credentials, install tools, or launch work.

The design permits AI-driven interpretation and negotiation while retaining
typed action boundaries for Agreement proposal and acceptance, resource
reservation, private disclosure, execution, Gifts, transfers, escrow, and
settlement. Every external side effect also carries a writer-fenced stable
action identity that the receiving sink can enforce and resolve.

### 2.4 Settlement profiles should specialize late

A specialized escrow profile may need exact asset identity, amount, deadlines,
validator, evidence, release, refund, and recovery rules. Those requirements
belong after the parties select that profile. They do not belong in every
public Intent.

### 2.5 Discovery cost must rise only with relevance

A universal bulletin can contain far more Intents than one Agent can read with
a general-purpose model. Downloading every body before filtering makes spam
cheap for publishers and bandwidth, storage, parser risk, and model tokens
expensive for receivers.

The network therefore exposes a small issuer-signed Discovery Card first. It
contains interoperable coarse category, keyword, approximate value, lifecycle,
schedule, region, language, and fulfillment fields plus a digest descriptor for
the full detail. Deterministic local filtering rejects most cards; only a
bounded shortlist reaches detail retrieval and deep AI analysis.

## 3. Four architectural layers

### 3.1 TOS Agent Operation substrate

TOS supplies the business-neutral primitives OpenFox composes:

- Agent identity, delegation, recovery, and revocation;
- `PUBLICATION/POST`, revision, reply, and withdrawal;
- direct and group messaging;
- optional `VALUE/GIFT`, transfer, and payment request;
- explicit Agreement promotion; and
- optional finalized settlement effects.

The common Agent Operation Envelope owns actor authorization, audience, object
and replay identity, scoped ordering, lifetime, payload commitment, and
admission metadata. It does not interpret whether an Intent describes source
review, asset exchange, media work, or another business.

### 3.2 Intent publication and discovery

The Intent exchange publishes and transports generic issuer-signed
advertisements. It provides:

- stable identity, immutable revision and withdrawal;
- a bounded signed Discovery Card for cheap filtering;
- coarse interoperable modes/classes plus extensible taxonomy paths;
- signed keywords, approximate value, schedule, region, language, and
  fulfillment hints;
- content-addressed detail and attachments for progressive retrieval;
- reply routes;
- optional search hints and namespaced extensions;
- settlement preferences;
- signature verification;
- permissionless exact-byte republication; and
- replaceable local indexes with no global head.

A compact generic Intent Reference, product-named an **Opportunity Magnet**,
lets any carrier share the exact digest plus bounded retrieval hints. It points
to immutable signed content; it is not a central board row or global latest
pointer.

It does not create an order, Agreement, execution authority, payment, or
settlement fact.

### 3.3 Conversation and Agreement

Messenger gives two Agents an authenticated open-ended negotiation channel.
They may clarify any semantic detail without changing the Intent protocol.

Ordinary conversation is always non-binding. When the parties decide to
proceed, one participant sends a typed `AGREEMENT/PROPOSE` containing the
exact canonical Agreement body. That body contains every typed authorization
predicate with its subject, role/obligation scope, evidence profile
URI/version/descriptor digest, validity, and non-circular target projection.
Under the generic off-chain profile, each subject sends one typed
`AGREEMENT/ACCEPT` covering its complete predicate set. A chain-bound profile
instead supplies its frozen evidence, such as the Paid Demand Provider Offer or
finalized buyer-wallet `accept`. One Agreement may mix profiles. A later message
cannot select or weaken them, and a transcript digest never substitutes for
authorization evidence.

The Agreement is a generic canonical graph of participant roles and
`AgreementObligationV1` records. Each obligation binds its deliverable or
consideration, exact value when applicable, dependencies, acceptance evidence,
billing and dispute rules, required authorizers, and its own settlement adapter
and parameters. Mandatory and proposer-added authorizers are represented by
typed predicates inside the same body, never a later untyped list. This
structure is business-neutral but gives execution,
Portfolio, Billing, and Settlement one deterministic input.

### 3.4 OpenFox execution and settlement adapters

Adapters implement the actual side effects:

- local skill or external executor;
- authenticated delivery;
- independent Agent Gift gratuity;
- Agreement-bound direct TOS or supported asset payment;
- versioned TOS Accepted Quote and escrow;
- optional external-chain or centralized settlement; and
- accounting evidence resolution.

An adapter may be absent. Its absence prevents only the corresponding action,
not Intent discovery or conversation.

## 4. Product roles are derived, not separate markets

The same Agent may issue or respond to an Intent in different roles:

- requester or provider of work;
- buyer or seller of an asset;
- principal or subcontractor;
- reviewer or reviewed party;
- payer, payee, or exchange counterparty; or
- collaborator with no immediate payment.

Cash-flow direction, custody exposure, execution responsibility, and accounting
remain distinct. They are derived from the Agreement rather than implemented
as incompatible discovery systems.

OpenFox may keep separate policy modules for spending and earning because their
risks differ. Both modules consume the same Intent and conversation model.

## 5. Relationship to ACP and centralized markets

The design retains useful ideas from Agent Commerce Protocol implementations:
participant-local opportunity/job projections, role-aware lifecycle events,
and small action interfaces. It does not copy a centralized job registry,
required Evaluator, or fixed marketplace authority, and it does not claim wire
compatibility.

An optional centralized application such as a branded work square may provide:

- hosted accounts and user experience;
- AI search and recommendations;
- proprietary ranking and matching;
- moderation, KYC, support, and notifications;
- fiat handling or external settlement; and
- fees for those services.

The application competes on service. Exact signed Intents remain portable, and
the application cannot turn its account, order, balance, review, or status
database into TOS Agent, Agreement, execution, or settlement authority.

## 6. Baseline and development gaps

### 6.1 Existing capabilities to reuse

The repositories already provide much of the required foundation:

- Native Agent and Capability identities;
- authenticated direct and group Messenger transport;
- signed Agent Gifts;
- Capability discovery and Gateway search;
- OpenFox skills, embedded AI, tools, scheduling, durable sessions, isolation,
  authorization seams, and local evolution;
- a bounded software-work executor;
- canonical Accepted Quote, stablecoin escrow, Execution Gate, Receipt,
  release/refund, and finalized settlement; and
- buyer/provider bridge code.

### 6.2 Missing operation-composed earning capabilities

The principal missing capabilities are:

- one frozen common Agent Operation Envelope plus a bounded Intent payload
  profile with signed Discovery Card, selective detail retrieval, and exact
  reference;
- interoperable coarse categories plus extensible taxonomies, approximate
  value/time/region filters, derived-field provenance, and cheap local
  shortlisting before model analysis;
- publication and search that do not require a closed task taxonomy;
- OpenFox-local semantic classification over hostile Intent content;
- capability, resource, profitability, risk, and trust analysis;
- Intent-referenced first contact and open-ended negotiation;
- a canonical multi-obligation Agreement plus explicit typed proposal and
  participant acceptance actions, distinct from ordinary chat;
- per-obligation settlement selection, canonical billing state, and
  evidence-class-aware accounting;
- a writer-fenced economic action authority enforced by every side-effect
  sink;
- a one-shot local Execution Gate with immutable resource capabilities;
- a trusted low-risk Agreement-bound direct-payment loop independent of
  escrow, with Gift retained only as a separate gratuity; and
- adapter registration that adds execution or settlement support without
  changing the Intent API.

### 6.3 Specialized escrow gaps remain separate

The existing Accepted Quote schema cannot express every fact required by the
previous fixed-price Paid Demand profile. If that profile remains a supported
TOS escrow adapter, its versioned Quote/escrow binding, buyer acceptance,
private ingress, Gate, deadline, and recovery work remains required.

Those gaps block only that escrow adapter. They do not block generic Intent
publication or read-only AI analysis. Contact, Agreement, execution, Gift,
direct transfer, and every other side effect remain blocked until the common
action-admission, Agreement, Gate, and selected Adapter contracts are frozen
and implemented.

## 7. End-to-end flows

### 7.1 Generic discovery and contact

```text
Agent B signs Intent revision
  -> one or more carriers relay exact bytes or an exact reference
  -> OpenFox A searches indexed card fields under a bounded local profile
  -> A retrieves and verifies small signed Discovery Cards
  -> deterministic filters reject irrelevant value/time/region/category cards
  -> cheap local ranking chooses a diverse top-K shortlist
  -> A resolves selected details through owner-approved origins and budgets
  -> A accepts content only after exact size and digest verification
  -> A's AI interprets selected content in hostile-data context
  -> A checks local skills, resources, economics, risk, and owner policy
  -> A ignores, watches, recommends, or contacts B
  -> Messenger authenticates B and maintains conversation continuity
```

One verified Intent is sufficient for contact. Multiple independent carriers
improve availability but do not establish truth or a global latest state.

### 7.2 Trusted work and direct payment

```text
A and B negotiate in Messenger
  -> select one settlement adapter for every value-bearing obligation
  -> compile one canonical Agreement obligation graph
  -> exchange typed proposal and all required profile-qualified evidence
  -> validate adapter prerequisites and reserve aggregate exposure
  -> local Gate atomically issues a one-shot execution start ticket
  -> A performs and delivers work through task-scoped resource brokers
  -> B performs the exact Agreement-bound direct-payment action
  -> A closes only the referenced obligation after exact terminal evidence
```

The Agreement may intentionally leave A exposed to nonpayment. OpenFox includes
that risk in its profit decision and records `UNPAID` honestly if payment does
not arrive. A later Agent Gift is accounted as gratuity or other income; it
does not satisfy the unpaid obligation.

### 7.3 TOS escrowed work

```text
A and B negotiate
  -> select a released TOS escrow profile
  -> compile the exact escrow obligation and Paid Demand predicates into the
     canonical Agreement
  -> satisfy the Paid Demand acceptance profile: Provider authorization by the
     exact signed Provider Offer, buyer commercial acceptance by the finalized
     buyer-wallet on-chain accept, each Quote-bound to the exact generic
     Agreement/obligation/predicate/target set (no duplicate generic acceptance)
  -> validate every adapter prerequisite and reserve aggregate exposure
  -> accept and fund exact escrow
  -> enter the Native Execution Gate with a one-shot execution slot
  -> execute and validate
  -> Receipt and release/refund
  -> resolve finalized provider-wallet outcome
```

The Paid Demand binding documents govern this path. The binding is a released
acceptance profile of the generic Agreement: its chain evidence — not a second
generic `AGREEMENT/ACCEPT` — satisfies the authorization predicates it maps,
and its Quote binding commits the final generic Agreement body digest and exact
scoped obligation/predicate/target lists. The coordinator, Gate, Portfolio, and
recovery flows therefore derive one acceptance state, and the same chain event
cannot authorize a modified Agreement. Generic Intent fields never silently
fill missing escrow authority.

### 7.4 Asset exchange or external settlement

```text
Intent advertises offered/wanted assets in free-form or optional extension
  -> Agents clarify chain, asset, amount, custody, price, and timing
  -> each leg becomes an exact Agreement obligation with its own adapter
  -> every body-bound predicate receives its profile-qualified evidence
  -> each leg resolves under its own evidence model
```

No TOS document claims atomic cross-chain exchange unless a separately reviewed
adapter actually supplies it. OpenFox exposes partial completion and principal
risk rather than labelling the exchange settled prematurely.

## 8. Primary artifacts and authority

| Artifact or fact | Authority | Not authority |
|---|---|---|
| Discovery Card | issuer signature over exact card, detail descriptor, and envelope body | correctness of category/value claim, search rank, index inference |
| Intent detail | exact bytes matching the signed detail digest and size | similarly named body, mutable URL, index cache without digest verification |
| derived category, translation, embedding, conversion, or rank | identified producer/profile/version as advisory local evidence | issuer statement, Agreement, price, or settlement authority |
| Intent identity and exact content | issuer signature over canonical Intent body plus digest-verified detail | carrier, index, AI summary, search rank |
| observed revision | verified predecessor chain actually observed | claim of globally latest revision |
| issuer identity | finalized Agent resolution plus Intent authorization | display name, room membership, application login |
| conversation peer | authenticated Messenger Agent identity | alias string, Gateway account, model guess |
| Proposal | exact conversation object | Agreement, execution, or payment authority |
| Agreement | canonical obligation graph and body-bound typed predicates plus complete profile-qualified evidence over the same digest, subject, profile, target, role, obligation and expiry | ordinary prose, frozen transcript, later profile choice, or UI selection marker |
| skill suitability | OpenFox-local AI assessment plus installed capability/resource checks | remote category or model claim |
| authorization to act | sink-admitted `AuthorizedActionV1`, current writer generation, exact request digest, policy/mandate/approval, and expected prior state | Intent content, AI output, or stale local lease alone |
| Agreement-bound direct payment | exact payment request plus adapter-specific finalized transfer evidence bound to Agreement and obligation | promise, unrelated equal-value transfer, screenshot, dashboard balance |
| Agent Gift | exact finalized Gift evidence, accounted only as gratuity or other income | Agreement payment or evidence that an obligation was satisfied |
| TOS escrow state | finalized exact contract and wallet state | Messenger message, Gateway callback, local journal |
| settled revenue | evidence class required by the exact Agreement obligation's selected adapter | quoted price, expected Gift, unrelated transfer, Receipt alone |

## 9. OpenFox autonomous control plane

### 9.1 Runtime modes

OpenFox supports:

1. `off` — no public-opportunity acquisition;
2. `observe` — retrieve, analyze, and explain only;
3. `contact` — autonomously send bounded non-binding messages;
4. `trusted` — enter bounded trusted Agreements and execute under local policy,
   with no guarantee of payment;
5. `policy-gated` — select approved Agreement-bound direct-payment, external,
   or TOS escrow adapters within explicit authority; Gifts remain separate
   gratuities; and
6. `approval-required` — prepare exact actions for owner confirmation.

No mode gives the model unrestricted signing, spending, credential, tool, or
policy authority.

### 9.2 Local AI responsibilities

The embedded AI owns semantic work:

- propose a versioned local search profile over sources, categories, keywords,
  value, time, region, language, and fulfillment mode;
- understand only shortlisted Intent detail and selectively retrieved
  attachments;
- match opportunities to OpenFox's current capabilities;
- estimate effort, cost, revenue, risk, and alternatives;
- generate contact and negotiation messages;
- propose canonical Agreement obligations and a settlement adapter for each
  value-bearing obligation;
- propose bounded service publications, price ranges, revisions, withdrawals,
  schedules, and customer or subcontractor searches; and
- select a plan and work schedule from approved skills and tools.

The AI's result is a proposal to deterministic policy and action boundaries.

### 9.3 Deterministic policy responsibilities

Policy independently limits:

- source queries, card pages, per-issuer/category quotas, retained shortlist,
  detail/attachment bytes, parser work, model tokens, and cycle duration;
- allowed content origins, DNS/IP classes, redirects, proxy use, TLS/SNI,
  credential origin, decompression, connection fan-out, and retrieval time;
- contact frequency, recipients, disclosure, and abuse exposure;
- publication, revision, withdrawal, public-reply, audience, TTL, price-change,
  margin, discount, disclosure, and per-Carrier limits;
- maximum work cost, external spend, loss, and concurrent obligations;
- asset, chain, custody, and settlement adapters;
- tool, model, credential, network, and data access;
- owner approval thresholds;
- Agreement, Gift, transfer, escrow, and execution action identities plus
  current writer generation and exact request digest;
- local Execution Gate plans, files, domains, destinations, credential handles,
  uploads, destructive operations, resource budgets, and authorization expiry;
- pause, drain, revoke, and incident response; and
- honest accounting evidence classes.

The policy need not understand every profession. It must understand the side
effects it authorizes.

### 9.4 Profit and trust model

For every candidate or Agreement, OpenFox estimates expected value and
worst-case exposure using:

- offered or negotiated consideration;
- payment probability under the selected settlement mode;
- acceptance and delivery probability;
- compute, model, API, tool, energy, labor, subcontractor, and opportunity
  cost;
- asset volatility, conversion, liquidity, and custody risk;
- nonpayment, refund, dispute, legal, privacy, and reputation risk; and
- locked resources and unresolved obligations.

Trust is local and contextual. It may use owner configuration, authenticated
relationship history, independently verified past outcomes, and value at risk.
There is no protocol-global trust score.

The evaluator exposes both expected net profit and return on committed
resources. A baseline calculation is:

```text
expected_net_profit
  = expected_consideration
      * payment_probability
      * completion_probability
    - model_compute_api_tool_cost
    - human_or_subcontractor_cost
    - capital_lock_and_liquidity_cost
    - capacity_opportunity_cost
    - expected_retry_failure_refund_cost
    - expected_dispute_nonpayment_cost
    - legal_privacy_reputation_reserve

risk_adjusted_roi
  = expected_net_profit / max(committed_cost_and_exposure, minimum_unit)
```

Unknown material inputs remain unknown. The model may propose bounded
estimates with provenance and confidence, but deterministic policy decides
whether uncertainty requires rejection, owner approval, a revised price, or a
stronger settlement mode.

## 10. Local projections and lifecycle

### 10.1 Intent Opportunity

An `IntentOpportunity` is keyed by exact Intent identity/revision and contains:

- verified envelope, signed Discovery Card, detail descriptor, and provenance;
- search-profile version, hard-filter result, cheap rank, and shortlist reason;
- selectively retrieved detail/attachment digests;
- AI classification and rationale;
- relevant local skills/resources;
- cost, revenue, trust, and risk estimates;
- decision and policy revision;
- conversation reference, if contacted; and
- local status.

It remains valid as an observation even when superseded or withdrawn. The
current actionable view is derived.

The generic earning lifecycle is an OpenFox-local safety projection, not a
business ontology:

```text
DISCOVERED
  -> FILTERED_OUT
  -> SHORTLISTED
  -> EVALUATED
       -> IGNORED | WATCHED | OWNER_REVIEW
       -> CONTACTING
       -> NEGOTIATING
       -> AGREEMENT_PROPOSED
       -> AGREEMENT_ACCEPTING
       -> AGREED
       -> ADAPTERS_PREPARED
       -> FUNDING_VERIFIED
       -> RESOURCE_RESERVED
       -> EXECUTION_PREPARED
       -> EXECUTION_STARTING
       -> EXECUTING | EXECUTION_AMBIGUOUS
       -> DELIVERED
       -> SETTLEMENT_RESOLVING
       -> SETTLED | UNPAID | REFUNDED | DISPUTED | FAILED | ABANDONED
```

Profiles may skip inapplicable states. For example, an unpaid collaboration has
no settlement state, and a direct sale may have no local execution state. The
coarse lifecycle exists to prevent remote content or model output from jumping
over contact, Agreement, reservation, execution, or custody authorization.

### 10.2 Engagement

An `Engagement` is created only after an exact Agreement exists. It is keyed by
Agreement digest, not by a mutable conversation ID or market database row. It
may represent labor, a sale, an exchange, delivery, or collaboration; `job` is
not a protocol category.

An Engagement owns the post-Agreement states beginning at `AGREED`. Settlement
and Skill adapters may project more detailed substates without changing the
generic lifecycle.

Before entering `RESOURCE_RESERVED`, OpenFox validates every selected Adapter,
proves any required prepayment or finalized escrow funding, and atomically
records the exact plan, worst-case resource cost, capacity, external spend,
unsecured receivable, and maximum loss exposure. Reservation release is
evidence-driven and crash-safe; an expired local timer alone cannot erase a
still-live Agreement or in-flight external action.

### 10.3 Events and actions

Participant-local derivative events are at least once, rebuildable, and
non-authoritative. Stable semantic action IDs exclude delivery cursor, model
turn, wall-clock attempt, and retry number.

Every action kind, ordered semantic key, binary framing, SHA-256 formula,
controlled repeat-instance allocation, terminal successor, execution attempt
lineage, and exact-byte vector is frozen by
[`SEMANTIC_ACTION_IDENTITY_V1.md`](SEMANTIC_ACTION_IDENTITY_V1.md). An
implementation-local table or caller-provided idempotency key is invalid.

Read operations include `Get`, `List`, `Subscribe`, `AvailableActions`, and
`ResolveAction`. Every side effect uses one canonical `AuthorizedActionV1`
with owner/Agent, action kind, stable action ID, exact request digest, writer
generation, policy/mandate/approval digests, expected prior state, and expiry.

Every Messenger, Carrier, custody, executor, and settlement sink must admit the
action in the same linearizable, rollback-resistant owner/Agent generation
domain, either directly or through the sole economic action broker. It stores
`unknown`, `prepared`, `submitted`, `accepted`, `rejected`, `conflict`, or
`terminal` resolution. An exact retry is idempotent; a reused action ID with a
different request digest is a conflict. A timeout requires resolution or retry
of the same action, never a new semantic action. An action linearized before a
writer takeover may finish; the stale writer cannot admit a new action after
the high-water generation advances.

Available action types may include:

```text
CONTACT_ISSUER
SEND_NEGOTIATION_MESSAGE
PROPOSE_AGREEMENT
ACCEPT_AGREEMENT
WITHDRAW_AGREEMENT
RESERVE_EXECUTION
PREPARE_EXECUTION
START_EXECUTION
DELIVER_RESULT
SEND_GIFT
SEND_DIRECT_TRANSFER
PREPARE_TOS_ESCROW
RESOLVE_SETTLEMENT
ABANDON
```

New business categories do not add action types unless they introduce a new
side-effect class.

## 11. Safety and failure invariants

1. Intent and message content are hostile data, not instructions.
2. The AI cannot select credentials, custody keys, hidden routes, unrestricted
   tools, network destinations, or policy revisions from remote content.
3. General-purpose model analysis is not required before deterministic
   envelope verification and Discovery Card filtering.
4. A retrieval hint is an untrusted locator. Content is fetched only through
   an owner-controlled `ContentRetrievalPolicyV1` that constrains origin,
   credential origin, DNS/IP class, redirects, proxy, TLS/SNI, fan-out, bytes,
   decompression, and time, and revalidates every DNS answer and redirect.
5. Detail and attachments are accepted only when their signed size and digest
   commitments match after bounded retrieval.
6. Publisher fields, source metadata, and derived index fields remain distinct;
   no rank, category mapping, translation, or price conversion gains issuer
   authority.
7. Unknown value, time, geography, language, or taxonomy follows explicit local
   policy and is never silently interpreted as favorable.
8. Ordinary conversation is non-binding. Only a typed proposal carrying
   canonical body-bound authorization predicates and complete matching
   profile-qualified evidence over the same Agreement digest create an
   Agreement; a transcript digest and later profile selection are invalid.
9. Every value-bearing Agreement obligation selects at most one settlement
   adapter before acceptance, reservation, or execution. A change creates a
   new Agreement version and requires a complete new authorization-evidence
   set.
10. Unknown Intent or Agreement extensions are preserved but have no implicit
    authority; an unknown required extension fails closed.
11. One source is enough for an independently verified observation and contact;
    source count is not truth.
12. No observer claims a globally latest Intent revision or complete public
    opportunity head.
13. Every external side effect has a canonical `AuthorizedActionV1`. Its sink
    enforces the current writer generation and exact request digest in a
    linearizable rollback-resistant owner/Agent admission domain and exposes
    `ResolveAction` recovery.
14. Every side-effect kind uses the released semantic identity registry.
    Transport, retry, time, host, and writer fields never change identity;
    ambiguous state has no successor, and intentionally repeated actions use an
    Action-Authority-issued instance rather than a worker nonce.
15. One owner/Agent economic portfolio has one active writer lease and a
    monotonically increasing fencing generation. A stale instance cannot
    reserve capacity, contact a new counterparty, accept an Agreement, start
    execution, or request settlement even if it retains an old journal.
16. Reservations and exposure limits cover all concurrent OpenFox instances,
    outstanding proposals, accepted Agreements, locked funds, unsecured work,
    and unsettled obligations; per-process limits alone are insufficient.
17. Capability Inventory used for contact or commitment identifies its
    creation/expiry, source generation, portfolio/policy revisions, consistency
    token, and per-item authority/revocation evidence. Commitment and execution
    re-read it at a consistent barrier.
18. Private data is disclosed only through an authenticated bounded channel
    after local policy permits it.
19. Agreement-bound direct payment is labelled unsecured until exact terminal
    payment evidence exists. An Agent Gift is gratuity and cannot close an
    obligation.
20. Periodic and milestone billing uses finite canonical obligation instances
    with sequence, predecessor, maximum aggregate, paid-to-date, stable action,
    evidence, cancellation, dispute, and replay rules.
21. External settlement is never represented as TOS-finalized state.
22. TOS escrow execution uses every existing profile-specific Gate, Receipt,
    release/refund, and recovery rule.
23. Failure of an optional carrier or settlement adapter cannot corrupt Intent
    identity or another adapter's state.
24. Pause stops new contacts or commitments according to scope; drain preserves
    already accepted obligations.
25. Learning cannot expand authority, rewrite adverse outcomes, or weaken
    settlement evidence.
26. A single Carrier may support a read-only or first-contact prototype, but
    production claims of resilient decentralized public discovery require at
    least two independent Carrier paths and source-loss recovery.
27. Every Skill execution owns a unique `(agreement_digest, execution_id)`
    slot. The Gate atomically changes `PREPARED` to `STARTING` and issues a
    short-lived one-shot start ticket; a crash in `STARTING` is ambiguous and
    cannot be retried as fresh authority.
28. The runner receives immutable no-follow file capabilities, pinned network
    and TLS policy, and non-escalating task/action-scoped credentials. Every
    outbound, upload, credential, and destructive effect returns through the
    same broker.
29. Publishing and repricing use writer-fenced stable actions. An advertisement
    is not reserved capacity, and a later revision cannot erase an earlier
    signed claim.
30. Durable scheduler entries bind dispatch generation, dependencies,
    reservations, cancellation/preemption class, irreversible boundary, and
    downstream Agreement identity; takeover reconciles ambiguous work before
    redispatch.
31. Customer, supplier, principal, and subcontractor relationships use separate
    Agreements, reservations, disclosure decisions, execution evidence, and
    settlement obligations.

## 12. Repository ownership

| Repository | Core responsibility | Enters scope when |
|---|---|---|
| `tos-service-spec` | common Agent Operation Envelope, opcode/profile boundaries, Discovery Card, retrieval policy, canonical Agreement/predicate/evidence/obligation, semantic action identity registry, Authorized Action, billing obligation, local Gate/start-ticket contracts, authority rules, and vectors | always for the common protocol |
| `tos-service-protocol` | operation, Agreement, predicate/evidence, action, and obligation codecs; bounded verification; registry-derived IDs; references; conflict/recovery vectors; clients; and adapter interfaces | always for portable implementation |
| `openfox` | search-profile generation, consistent Capability Inventory, staged acquisition, service publication, pricing, filtering, AI matching, economics, risk, contact, typed Agreement coordination, Portfolio projection, durable scheduling, local execution coordination, accounting, and learning | always for the autonomous product |
| `tos-service-gateway` | one replaceable bounded card index, selective detail retrieval, and optional market-application adapters | when Gateway publication/search is enabled |
| `tos-messenger` | rooms, direct first contact, conversation, typed Agreement proposal and applicable generic evidence delivery, action-ID deduplication/resolution, controlled writer admission or outbox, and Gift transport | when Messenger is a carrier or negotiation transport |
| `tos-ai` | optional bounded execution profiles, immutable resource capabilities, task-scoped effect broker, one-shot runner, and evidence | when an Agreement selects those executors |
| `tos` / `tosctl` | Agent state, Gift and direct value transfer, optional Quote/escrow/Receipt contracts, rollback-resistant writer-generation/action admission in custody, signing, broadcast, and recovery | when the selected action or settlement mode needs chain state |
| optional market app | hosted board, search, ranking, moderation, KYC, support, fiat, proprietary services | independently optional |

This table is not a requirement to modify every repository. The selected
delivery phase determines the actual PR set.

## 13. Cross-repository interfaces

| Interface | Producer | Consumer | Contract |
|---|---|---|---|
| Agent Operation encode/verify | protocol SDK | Carriers, OpenFox, applications | exact canonical envelope and payload digest, opcode profile, actor authorization, audience, replay identity, scoped ordering, bounds, and unknown-extension rules |
| Intent card publish/search/subscribe | Carrier or application | OpenFox | `PUBLICATION/POST` operations carrying bounded exact signed cards, optional capability hints and separately attributed derived fields, provenance, source-local cursor |
| service publication and pricing | OpenFox publication manager | custody and Carriers | AI-proposed content and price; exact `AuthorizedActionV1`; deterministic audience, disclosure, rate, TTL, margin, discount, exposure and revision policy; sink-side writer admission; exact signed operation; `ResolveAction` |
| Intent detail retrieval | carrier, Storage, or peer through `ContentResolver` | OpenFox | `ContentRetrievalPolicyV1`; owner-approved origins; SSRF/DNS/redirect/TLS/proxy/credential-origin and resource bounds; exact declared size/digest; no mutable-URL authority |
| Intent semantic analysis | OpenFox AI | local coordinator | untrusted-content classification, capability/resource/economic/risk explanation; no authority |
| first contact | OpenFox | Messenger | canonical Agent recipient, Intent reference, bounded message, exact Authorized Action, sink-side writer admission, action-ID deduplication and resolution |
| negotiation | Messenger | OpenFox participants | authenticated events, open content, replay-safe delivery, no implicit Agreement |
| Agreement | participants/protocol helper | OpenFox and selected adapters | canonical acyclic participant/obligation graph; per-obligation settlement; body-bound typed authorization predicates; typed proposal; complete profile-qualified evidence over the exact body, subject, profile, target, role, obligation and expiry; deterministic conflicts |
| semantic action identity | specification registry and protocol SDK | every side-effect sink | exact V1 framing and SHA-256 formula; registered ordered semantic key; exact request conflict; authority-issued repeat instances; terminal successor and execution-lineage rules; exact-byte vectors |
| local execution authorization | OpenFox Gate and task-scoped broker | local skill or executor | unique execution slot; atomic `PREPARED -> STARTING`; one-shot start ticket; exact Agreement/plan/input/reservation; immutable file/network/credential capabilities; writer/policy/approval/expiry; ambiguous-start recovery |
| scheduling | OpenFox durable scheduler | local coordinator and Gate | durable entry and dependency graph with dispatch generation, deadline, resource/exposure reservations, cancel/preempt class, irreversible boundary, downstream Agreement and evidence-driven failure propagation; no authority by itself |
| Agreement-bound direct payment | custody adapter | accounting/resolver | exact Agreement/obligation/payer/payee/asset/amount/destination/expiry, Authorized Action, adapter-specific finalized evidence, no evidence reuse |
| Agent Gift | custody adapter | accounting/resolver | exact Gift evidence recorded as gratuity or other income only; never Agreement settlement |
| TOS escrow | protocol + TOS contracts | Gate, executor, accounting | Quote commitment to exact generic Agreement/obligation/predicate/target/profile plus profile-specific acceptance, funding, execution, Receipt, release/refund and recovery |
| external settlement | external adapter | accounting | explicit evidence class; never implicit TOS authority |
| milestone or periodic billing | Agreement + settlement adapter | Portfolio Ledger | canonical finite `SettlementObligationV1` instances with predecessor, amount, schedule, aggregate cap, paid-to-date, stable action ID, partial-payment/evidence/cancellation/dispute state; no unlimited recurring authority |

## 14. Delivery sequence

### Phase 0 — generic specification

Repositories: `tos-service-spec`, then `tos-service-protocol`.

- freeze the common Agent Operation Envelope and the minimal Intent payload
  profile: signed Discovery Card, modes/classes, taxonomy paths, keywords,
  optional capability hints, decimal value hints, schedule/region/language/
  fulfillment fields, detail descriptor, publisher/derived-field boundary,
  bounds, publication signature context, revision/withdrawal behavior,
  extensions, settlement preferences, and compact reference;
- freeze `ContentRetrievalPolicyV1`, the canonical multi-obligation Agreement,
  body-bound authorization predicates, mixed-profile evidence, typed
  proposal/acceptance where applicable, `AuthorizedActionV1`, action resolution,
  `BillingTermsV1`, `SettlementObligationV1`, durable schedule/dependency state,
  and the local Gate/start-ticket contract;
- freeze the semantic-action registry framing, entries, formulas, controlled
  repeat and terminal-successor rules, execution lineage, error classes, and
  exact-byte vectors;
- include semantically unrelated examples without category-specific core
  fields; and
- provide a second independent codec/verifier.

Exit: different Intent categories round-trip through one codec, signed cards
can be filtered without body retrieval, Agreement obligations, predicates,
profile-qualified evidence and action/execution identities are deterministic,
action/obligation conflicts fail closed, unknown optional extensions survive,
unknown required extensions fail, and a second verifier reproduces every
digest, exact-byte vector and error.

### Phase 1 — read-only Intent scout

Repositories: `openfox`, `tos-service-protocol`, and one carrier adapter.

- generate a bounded local search profile from current owner policy and a
  timestamped, expiring, revision-bound consistent Capability Inventory;
- search or subscribe for signed cards, then verify their observed revision
  chains;
- apply deterministic filters and diverse top-K selection before detail fetch;
- retrieve shortlisted detail only through `ContentRetrievalPolicyV1`, then
  verify exact size and digest;
- classify shortlisted hostile content with OpenFox's AI;
- match local skills/resources and estimate profit/risk;
- expose explanations and local Opportunity projections; and
- permit no contact, execution, signing, or payment.

Exit: restart-safe OpenFox rejects most irrelevant cards without detail/model
cost, then produces useful explanations across the shortlist with no external
side effect. A one-Carrier deployment is a local prototype only; it cannot be
advertised as resilient decentralized public discovery.

### Phase 2 — Messenger negotiation

Repositories: `openfox`, `tos-messenger`, and protocol helpers.

- contact an issuer using an exact Intent reference;
- support open-ended bounded negotiation;
- deploy the rollback-resistant owner/Agent action authority and require every
  Messenger side effect to enforce current writer generation, exact request
  digest, action-ID conflict, and `ResolveAction`;
- distinguish chat, typed `AGREEMENT/PROPOSE`, body-bound authorization
  predicates, and profile-qualified evidence including typed
  `AGREEMENT/ACCEPT` where selected;
- select the settlement adapter and exact parameters of every value-bearing
  obligation before collecting authorization evidence;
- add rate, privacy, abuse, disclosure, and owner-policy controls; and
- survive duplicate delivery, ambiguous send, restart, device rotation, and
  Intent revision.

Exit: two Agents negotiate a changed scope and authorize one exact canonical
Agreement through complete generic profile evidence, without any chain
transaction, later profile selection, or transcript-derived authority.

### Phase 3 — trusted low-risk earning

Repositories: `openfox` plus the selected executor, owner/Agent action
authority, and Agreement-bound direct-payment adapter. Gift support is optional
and remains independent gratuity functionality.

- validate direct-payment prerequisites, construct an exact plan, and reserve
  worst-case aggregate exposure in the shared owner/Agent Portfolio;
- atomically acquire the unique execution slot and one-shot start ticket;
- schedule and execute one bounded owner-approved Skill;
- use immutable no-follow file, pinned network, and task/action-scoped
  credential capabilities through the local broker;
- deliver through Messenger or content-addressed storage;
- accept the explicit nonpayment risk;
- request and resolve the exact Agreement-bound direct payment;
- optionally receive a separate Agent Gift as gratuity; and
- reconcile settled or unpaid outcome and realized cost.

Exit: one real low-value Agreement completes without invoking TOS escrow.

### Phase 4 — optional TOS escrow

Repositories: only those required by the selected released escrow profile,
including protocol, `tos`, executor/Gate, custody, and OpenFox integration.

- adapt one Agreement into the supported profile;
- satisfy that profile's separate schema, security, conformance, and external
  acceptance gates;
- prove exact funding, at-most-once execution, Receipt, release/refund, and
  finalized provider credit; and
- demonstrate that disabling the adapter leaves Intent discovery and
  negotiation functional.

Exit: untrusted counterparties can choose stronger TOS enforcement without
making it mandatory for everyone.

### Phase 5 — federation and ecosystem growth

- operate multiple independent carriers and failure recovery;
- integrate optional centralized markets;
- publish, revise, reprice, and withdraw bounded service Intents under owner
  policy and sink-enforced writer fencing;
- schedule multiple Agreements through durable schedule entries and dependency
  graphs under aggregate capacity and exposure limits;
- find customers, suppliers, and subcontractors through the same Intent profile
  while preserving separate Agreement and disclosure boundaries;
- reconcile canonical finite milestone, periodic, partial, and
  accumulated-balance obligations;
- add execution and settlement adapters without changing the Intent core;
- measure contact conversion, Agreement conversion, payment method, nonpayment,
  dispute, profit, and retention; and
- improve local AI matching and negotiation under bounded learning policy.

Exit: varied recurring commerce uses one Intent exchange while no carrier,
market application, or settlement mode becomes universally mandatory.

## 15. PR dependency graph

```text
I0  tos-service-spec: Intent + Agreement/acceptance/obligation + Action/Gate vectors
 |
 +-> P0  tos-service-protocol: codec, verifier, references, adapter interfaces
      |
      +-> O0  openfox: read-only Intent scout + AI assessment
      |
      +-> C0  one carrier: Gateway or Messenger publication/retrieval

P0 + O0 + C0
  -> read-only Intent MVP

M1  tos-messenger: writer-fenced contact + typed Agreement actions + resolution
A1  owner/Agent action authority: generation high-water + admission/recovery
O1  openfox: negotiation + typed Agreement coordinator

M1 + A1 + O1
  -> negotiated Agreement without chain dependency

X1  selected executor
D1  Agreement-bound direct-payment adapter, optional
G1  existing Gift adapter for separate gratuities, optional

O1 + A1 + X1 (+ D1) (+ G1)
  -> trusted low-risk earning

S2  optional TOS escrow profile prerequisites
  -> Quote/escrow/Gate/Receipt/custody/OpenFox adapter PRs
  -> high-assurance escrowed earning

O2  openfox: publication/pricing + local Gate + scheduler + billing
C1  second independent Carrier and source-loss recovery

P0 + O2 + C1
  -> continuous autonomous business and resilient public discovery
```

No escrow PR blocks the first three outcomes.

## 16. Compatibility and migration

- Existing Capability-first purchases remain unchanged.
- Existing schema-1 Accepted Quote, escrow, Gate, Receipt, Gift, and settlement
  semantics remain unchanged.
- New generic publication of an existing Paid Demand uses the required
  `tos.service.paid-demand.v1` extension to bind its exact reference and digest.
  Implementations may ingest legacy unwrapped Paid Demand during migration,
  but republication does not invent a second authoritative copy of its fields.
- The exact original Paid Demand bytes remain the authority for its optional
  escrow profile; a derived generic summary cannot replace them. Negotiated
  changes to escrow-critical terms require new exact profile objects and
  authorizations.
- Existing Gateway and Messenger databases remain local projections.
- A UI must distinguish generic Intent, conversation, Proposal, Agreement,
  payment request, funded escrow, and settled outcome.

The preferred migration is additive: release the common Agent Operation
Envelope and generic Intent payload profile, adapt existing Paid Demand
discovery as one profile, then remove any product claim that every economic
opportunity must conform to Paid Demand.

## 17. Acceptance matrix

### Generic Intent

- multiple unrelated categories use identical core parsing;
- signed cards expose mode, coarse class, namespaced taxonomy, keyword, optional
  capability hint, approximate value, lifecycle/schedule, region/language, and
  fulfillment filters while free-form asset and service descriptions remain
  representable;
- a search result can return cards without returning all detail or attachments;
- exact detail is accepted only when size and digest match its signed
  descriptor;
- hostile retrieval hints cannot reach loopback, link-local, private, metadata,
  Unix-socket, arbitrary-proxy, or credential-bearing destinations; every DNS
  answer and redirect is revalidated under fixed TLS/SNI and byte/time bounds;
- publisher fields and derived classifications/conversions/ranks remain
  visibly separate with provenance;
- unknown value, time, location, taxonomy, and language follow explicit local
  policy rather than implicit defaults;
- unknown extensions are preserved;
- exact replay is idempotent and conflicting revision is detected;
- a carrier cannot change issuer, content, route, expiry, or preference; and
- one verified Intent can be analyzed and contacted without two-source
  promotion.

### AI and security

- prompt injection cannot select tools, credentials, policies, models,
  destinations, payment, or settlement;
- AI explanations cite exact Intent provenance;
- local resource and economic bounds override AI recommendation;
- private attachments are not retrieved or executed during public discovery;
  and
- self-learning cannot authorize a new side-effect class.

### Capability, economics, and portfolio safety

- a stale, expired, generation-mismatched, revoked, or internally inconsistent
  Capability Inventory cannot justify contact or commitment;
- every profitable recommendation identifies available Skills, models, tools,
  credentials, wallets, assets, capacity, cost evidence, and confidence;
- expected net profit and risk-adjusted ROI are explainable and deterministically
  clamped by owner policy;
- compute, spend, capital, open Agreement, unsecured receivable, loss reserve,
  per-counterparty exposure, and global exposure are reserved atomically; and
- two processes or hosts sharing one owner/Agent cannot bypass aggregate limits,
  because the rollback-resistant Action Authority and every side-effect sink
  admit only the current writer generation and exact request digest;
- a stale writer cannot contact, accept, reserve, execute, settle, reconcile,
  or release, and ambiguous sends are recovered by `ResolveAction` without a
  new semantic action;
- two code-independent implementations reproduce every registered action and
  execution identity exact-byte vector; semantic-field mutations, omitted
  destinations, caller nonces, same-ID/different-request conflicts, ambiguous
  successors, takeover and authority-issued intentional repeats behave
  identically.

### Conversation and Agreement

- first contact binds exact issuer Agent and Intent reference;
- ordinary prose cannot create Agreement or payment authority;
- a canonical Agreement contains a deterministic acyclic graph of exact
  obligations and one settlement adapter per value-bearing obligation;
- every mandatory and proposer-added authorization predicate is frozen in the
  body with typed subject, profile URI/version/digest, role/obligation scope,
  validity and target projection, then satisfied by matching evidence binding
  that same final Agreement body;
- mixed generic, custody and chain evidence profiles converge on one Agreement
  state, while later profile selection, partial evidence union, weaker
  substitution, and replay of one chain event to a changed Agreement,
  obligation, predicate or target fail closed;
- missing, duplicate, expired, withdrawn, concurrent-version, conflicting, and
  unknown-required-extension cases fail closed;
- changed negotiated or settlement terms produce a new digest and complete new
  authorization;
- duplicate/ambiguous sends recover without duplicate binding action; and
- an Intent withdrawal does not rewrite an already accepted Agreement.

### Publication, execution, and scheduling

- AI-proposed service content, capability hints, price, availability and expiry
  cannot bypass publication, disclosure, margin, exposure, rate or writer-fence
  policy;
- automatic revision preserves earlier signed claims and never turns an offer
  into reserved capacity or an Agreement;
- every Skill launch uses a unique execution slot, atomic start transition,
  short-lived one-shot ticket, immutable no-follow files, pinned network/TLS
  rules and non-escalating task/action-scoped credential capabilities;
- crash in `STARTING` is ambiguous, not automatically reauthorized, and writer
  loss follows the specified drain/kill policy without new external effects;
- concurrent work uses durable schedule/dependency entries and respects
  reservation, deadline, dispatch generation, priority, cancellation,
  preemption, irreversible boundary and aggregate-exposure policy; and
- upstream and subcontractor Agreements cannot share authority, private input,
  payment state or evidence implicitly.

### Settlement modes

- Agreement-bound direct payment is labelled unsecured before exact terminal
  evidence;
- an Agent Gift is recorded as gratuity or other income and cannot close an
  Agreement obligation, even when payer, payee, asset, and amount happen to
  match;
- unpaid trusted work remains visible as unpaid;
- external payment is assigned an explicit non-TOS evidence class;
- milestone, installment, periodic and accumulated-balance obligations retain
  finite recurrence, exact sequence/predecessor, aggregate cap, stable action
  identity, paid-to-date, partial-payment, cancellation, dispute, evidence and
  outstanding state across restart and takeover;
- TOS escrow uses the complete specialized acceptance matrix and its Quote
  commits the exact generic Agreement body digest, scoped obligation/predicate/
  target set and profile descriptor; and
- the generic system operates with the escrow adapter absent.

### Federation

- independent carriers reproduce exact Intent bytes;
- loss of one carrier does not destroy already replicated Intent data;
- source diversity is not confused with truth, solvency, or latest-state
  completeness; and
- optional market applications can disappear without invalidating portable
  Intent or Agreement bytes held by participants.

## 18. Explicit non-goals

This architecture does not create:

- one universal semantic schema for all trade;
- one core coordinator or lifecycle per business category;
- a mandatory machine-readable task profile before conversation;
- a global marketplace, order book, winner, trust score, or reputation oracle;
- automatic semantic enforcement of arbitrary natural-language promises;
- a mandatory TOS asset, Gift, escrow, evaluator, or settlement path;
- TOS authority over BTC, fiat, centralized exchange, or other external state;
- permission for model text to sign, spend, execute, or disclose secrets; or
- a requirement that every repository participate in every transaction.

## 19. Open decisions

Before schema freeze, decide:

1. canonical protobuf versus content-addressed canonical CBOR representation
   for the open body and extension map;
2. maximum inline and referenced content sizes;
3. signature/delegation profiles for `PUBLICATION/POST` and
   `PUBLICATION/WITHDRAW`;
4. exact unknown-extension preservation rules;
5. compact reference encoding and the concrete owner-approved retrieval-origin
   registry;
6. stable URI registry rules and mandatory-field profiles for settlement
   adapters;
7. minimum evidence labels for external settlement;
8. contact rate, spam, privacy, and unsolicited-message defaults;
9. the first bounded trusted Skill and Agreement-bound direct-payment
   acceptance run, with a separate Gift gratuity test;
10. the concrete owner/Agent Action Authority backend that satisfies the frozen
    linearizability, rollback-resistance, fencing and recovery contract;
11. the concrete Portfolio storage backend that atomically covers pending
    contact, Proposal, Agreement, execution, receivable, billing and settlement
    exposure;
12. publication, public-reply, price-change, TTL, audience, disclosure and
    active-post limits for autonomous supply;
13. the concrete credential broker and sandbox implementation that satisfies
    the frozen immutable-handle and task-scoped effect-broker contract; and
14. scheduler priority and business policy within the frozen durable
    schedule/dependency/cancellation state model.

Until these are frozen, OpenFox may implement fixtures and a read-only scout.
No design text alone authorizes autonomous publication, contact, scheduling,
execution, signing, billing, Gift, transfer, escrow, or external settlement.
