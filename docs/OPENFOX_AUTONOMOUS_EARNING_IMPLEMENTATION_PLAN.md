# OpenFox Autonomous Earning — Operation-Composed Implementation Plan

## Status

- Document type: OpenFox application design and delivery plan
- Status: proposed; implementation and acceptance pending
- Target repository: `tosnetwork/openfox`
- Root architecture:
  [`TOS_AGENTIC_INTERNET_OPERATION_ARCHITECTURE_V1.md`](TOS_AGENTIC_INTERNET_OPERATION_ARCHITECTURE_V1.md)
- Primary specification:
  [`AGENT_INTENT_EXCHANGE_V1.md`](AGENT_INTENT_EXCHANGE_V1.md)
- Cross-repository design:
  [`OPENFOX_AUTONOMOUS_EARNING_CROSS_REPOSITORY_DESIGN.md`](OPENFOX_AUTONOMOUS_EARNING_CROSS_REPOSITORY_DESIGN.md)
- Optional TOS escrow profile:
  [`PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md`](PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md)
- Historical source baseline: OpenFox PR
  [#13](https://github.com/tosnetwork/openfox/pull/13), commit
  `d4d5e165831ace2e1e01e04f9fc17e90853814ef`

This plan replaces the assumption that all earning opportunities are typed
fixed-price software jobs. OpenFox composes general Agent Operations: it
discovers `PUBLICATION/POST` operations carrying an Intent profile, uses its
embedded AI to understand arbitrary opportunities, contacts the issuer through
Messenger, promotes negotiated terms into an explicit Agreement, dispatches an
approved Skill, and selects a settlement adapter according to capability,
trust, risk, and owner policy.

No implementation claim may rely only on the historical source baseline. The
current OpenFox repository must be re-audited at the commit selected for work.

## 1. Product outcome

Build OpenFox into:

> An owner-controlled Agent that continuously discovers arbitrary economic
> intent, identifies opportunities compatible with its current abilities and
> resources, estimates profit and risk, negotiates with other Agents, performs
> agreed work through approved skills, selects an appropriate payment method,
> and learns from verified outcomes.

The primary loop and component boundary are:

```text
Capability Inventory
  -> bounded Search Profile
  -> Opportunity Collector verifies Agent Operations and signed Intent cards
  -> deterministic card filters and diverse shortlist
  -> selective detail retrieval and hostile-content AI analysis
  -> Economic Evaluator computes feasibility, profit, ROI, trust, and risk
  -> ignore, watch, request owner review, or contact issuer
  -> Negotiation Manager uses authenticated Messenger
  -> freeze exact Agreement
  -> Portfolio Ledger atomically reserves resources and exposure
  -> Skill/Execution Gate performs and delivers approved work
  -> Settlement Selector chooses none/Gift/direct/TOS escrow/external adapter
  -> Portfolio Ledger reconciles evidence and bounded learning records
  -> repeat
```

OpenFox is not a centralized market. It may consume centralized market leads,
but it reuses portable Agent identity, Intent, conversation, Agreement, and
settlement evidence wherever those are available.

## 2. What the baseline already provides

The historical PR #13 baseline and related repositories contained useful
building blocks:

- embedded AI planning, tools, skills, routing, scheduled work, durable
  sessions, event provenance, isolation, and bounded self-evolution;
- a buyer-facing Capability opportunity service;
- a passive provider path for one bounded software-work profile;
- action-authorization seams for spending, keys, tools, and configuration;
- Native Agent/Capability resolution, Quote, escrow, Receipt, and settlement
  bridge code;
- direct Messenger conversations and rooms; and
- direct signed Agent Gifts.

Those components prove isolated capabilities. They do not yet prove the
generic autonomous business loop in this plan.

## 3. Development gaps

| Required behavior | Gap to close |
|---|---|
| Generic Intent acquisition | Existing discovery is centered on Capability listings or specialized Paid Demand, not arbitrary signed economic content. |
| Cheap catalog filtering | The prior generic draft did not separate a small signed category/keyword/value/time card from full detail, causing avoidable bandwidth, parser, and model cost. |
| AI semantic selection | No unified loop lets the embedded AI choose what Intent information to retrieve and interpret across unrelated categories. |
| Local capability/resource judgment | Skills, models, credentials, runtime capacity, and policy are not combined into one current feasibility view. |
| Profit and trust analysis | No generic model covers cost, payment probability, asset risk, trust, nonpayment, and settlement choice. |
| Intent-referenced contact | No complete coordinator turns a verified Intent into bounded authenticated first contact. |
| Open negotiation | Existing earning design over-specializes Provider Offers and forbids general natural-language negotiation in the production path. |
| Generic Agreement | No exact object cleanly separates ordinary chat from the final terms that authorize work or payment. |
| Optional settlement | No common adapter boundary selects trusted Gift, direct transfer, TOS escrow, or external settlement without changing the Intent or Agreement objects. |
| Generic execution dispatch | The passive provider path is pinned to a narrow software profile rather than a locally selected approved skill. |
| Business accounting | Expected Gift, unsecured receivable, external payment, escrowed receivable, cost, nonpayment, and settled revenue are not reconciled under evidence classes. |
| Continuous operation | Pause, drain, restart, contact limits, unresolved Agreements, settlement recovery, and learning are not integrated into one durable loop. |

## 4. Architectural decisions

### 4.1 Use one operation-composed earning coordinator

Create a generic earning control plane over the Agent Operation layer. Do not
create separate discovery APIs or coordinator state machines for smart-contract
review, asset exchange, video work, data collection, or each future Skill.

Buying, selling, requesting, offering, and exchanging share acquisition,
verification, AI analysis, contact, and negotiation. Spending policy and
earning policy remain distinct local checks because their cash-flow and loss
risks differ.

### 4.2 Make the embedded AI the semantic engine

The AI decides what content is relevant and what it means. It may classify
unstructured Intent text, infer missing questions, match local abilities,
generate a plan, estimate uncertainty, and negotiate.

The protocol does not require exact task categories or I/O schemas before
contact. Optional extensions and local indexes improve efficiency but are not
validity requirements.

### 4.3 Keep remote text outside the authority boundary

Intent and conversation text can influence reasoning but cannot directly:

- sign or accept an Agreement;
- promise bounded resources or spend;
- select credentials, wallet keys, custody devices, hidden routes, or network
  exceptions;
- install or modify skills, tools, MCP servers, plugins, or models;
- disclose private data;
- start an executor;
- send a Gift or transfer; or
- deploy, fund, release, or refund escrow.

Each side effect uses a separate typed local action under deterministic policy.

### 4.4 Permit autonomous conversation

OpenFox may autonomously send non-binding messages when owner policy permits
the recipient, topic, disclosure, frequency, model cost, and abuse exposure.

The system must not treat ordinary natural-language acceptance phrases as an
Agreement. The AI may propose terms; a dedicated Agreement action freezes and
authorizes them.

### 4.5 Select settlement late

Settlement is chosen after negotiation:

- `trusted-gift` for low-risk relationships willing to accept nonpayment risk;
- `direct-transfer` for simple payment without escrow;
- `tos-escrow` for a supported high-assurance TOS profile;
- `external` for explicitly non-TOS systems; or
- `none` for unpaid collaboration.

No settlement mode is a prerequisite for discovering or discussing an Intent.

### 4.6 Preserve strict optional profiles

When `tos-escrow` is selected, OpenFox must satisfy the complete Quote,
escrow, Gate, execution, Receipt, release/refund, custody, and recovery profile.
Generic chat or an Intent digest cannot fill missing authority.

The complexity of an untrusted escrowed purchase remains inside that adapter.
It does not infect trusted or conversational paths.

### 4.7 Make side effects durable and idempotent

Every contact, Agreement action, reservation, execution, delivery, Gift,
transfer, escrow, and settlement-resolution operation has a stable semantic
action ID derived from exact participant and object identity plus action kind
and terms.

Retry attempt, source cursor, model turn, wall time, and transport session do
not create new economic identities.

## 5. Proposed package boundary

The package layout is illustrative. Existing packages should be reused when
their semantics match exactly.

```text
pkg/earning/
  coordinator.go      # observe -> evaluate -> negotiate -> execute -> settle
  lifecycle.go        # generic economic safety states, not business categories
  actions.go          # typed semantic actions and idempotent action IDs
  writer_lease.go     # owner/Agent single-writer lease and fencing generation
  store.go            # restart-safe journal, recovery, pause and drain

pkg/opportunity/
  operation.go        # verified Agent Operation and Intent payload projection
  collector.go        # bounded multi-Carrier acquisition and exact deduplication
  card.go             # signed Discovery Card and publisher fields
  detail.go           # selective detail/manifest/attachment retrieval
  taxonomy.go         # coarse classes and namespaced taxonomy helpers
  search_profile.go   # AI proposal plus deterministic policy clamp
  shortlist.go        # hard filters, cheap rank, diversity and quotas
  model.go            # verified observation and Opportunity projection
  reference.go        # generic Intent Reference / Opportunity Magnet
  source.go           # bounded Carrier interface
  verify.go           # operation, signature, revision, provenance
  policy.go           # contact and candidate-side deterministic limits

pkg/negotiation/
  conversation.go     # Intent-referenced Messenger coordination
  proposal.go         # non-binding proposals
  agreement.go        # exact Agreement versions and authorization state
  store.go            # durable conversation/Agreement projection

pkg/business/
  inventory.go        # current Skills, models, tools, credentials and capacity
  economics.go        # explainable expected profit, ROI, trust and risk
  portfolio.go        # atomic reservations and aggregate exposure limits
  ledger.go           # evidence-class-aware P&L, receivables and reconciliation

pkg/skilladapter/
  skill.go            # generic bounded Skill interface
  registry.go         # owner-approved installed Skills
  delivery.go         # authenticated result/artifact delivery

pkg/settlementadapter/
  adapter.go          # common prepare/authorize/submit/resolve boundary
  gift.go             # existing Agent Gift integration
  direct.go           # supported direct transfers
  tosescrow.go        # optional Accepted Quote/escrow profile
  external.go         # explicit non-TOS evidence integration
```

Do not duplicate protocol codecs in OpenFox. `tos-service-protocol` owns exact
Agent Operation, Intent payload, Agreement, Gift, Quote, Receipt, and settlement
encodings.

## 6. Small integration surfaces

The common architecture needs coarse business-neutral boundaries rather than
one interface per trade type.

### 6.1 Opportunity collection and source adapters

```go
type OpportunitySource interface {
    SearchCards(
        ctx context.Context,
        query CardQuery,
        cursor Cursor,
        limit uint32,
    ) (OperationBatch, error)
    ResolveOperation(
        ctx context.Context,
        ref OperationRef,
    ) (VerifiedAgentOperation, error)
    FetchContent(
        ctx context.Context,
        descriptor ContentDescriptor,
    ) (ExactContent, error)
}
```

The Opportunity Collector owns bounded polling, source-local cursors, exact
deduplication, retry, and source provenance across these adapters. It never
converts Carrier rank or availability into truth, latest-state, solvency, or
profitability authority.

Search returns exact bounded signed cards or exact references plus provenance;
any derived labels or rank are separate attributed fields. Detail, attachment
manifest, and selected attachments reuse one explicit content fetch and must
match their signed size and digest. Search may be
lexical, taxonomy-, value-, time-, region-, language-, embedding-, room-, or
application-based. A source's filtering or ranking never becomes OpenFox's
decision or issuer authority.

### 6.2 Capability inventory

```go
type CapabilityInventory interface {
    Snapshot(ctx context.Context, owner OwnerID, agent AgentID) (InventorySnapshot, error)
}

type InventorySnapshot struct {
    Revision       uint64
    Skills         []SkillDescriptor
    Models         []ModelDescriptor
    Tools          []ToolDescriptor
    Credentials    []CredentialDescriptor
    Wallets        []WalletDescriptor
    Assets         []AssetDescriptor
    Capacity       ResourceCapacity
    Reservations   []ResourceReservation
    Obligations    []Obligation
    CostEvidence   []UnitCostEvidence
    OutcomeHistory []SkillOutcomeSummary
}
```

The snapshot is local, versioned, and owner-scoped. Remote content cannot add a
Skill, mark a credential available, change a cost, or release a reservation.

### 6.3 Conversation transport

```go
type ConversationTransport interface {
    EnsureDirect(ctx context.Context, issuer AgentID) (Conversation, error)
    Send(ctx context.Context, conversation ConversationID, actionID ActionID, message Message) (SendResult, error)
    Subscribe(ctx context.Context, cursor Cursor, limit uint32) (MessageBatch, error)
}
```

OpenFox supplies the canonical Agent recipient, Intent reference, and semantic
message. Messenger owns routes, sessions, devices, encryption, replay, and
delivery.

### 6.4 Economic evaluator

```go
type EconomicEvaluator interface {
    Evaluate(
        ctx context.Context,
        opportunity VerifiedOpportunity,
        inventory InventorySnapshot,
        portfolio PortfolioSnapshot,
    ) (EconomicAssessment, error)
}
```

The assessment records revenue, cost, payment and completion probabilities,
capital lock, opportunity cost, loss reserves, expected net profit,
risk-adjusted ROI, worst-case exposure, evidence provenance, confidence, and
unknown material inputs. AI may propose estimates; deterministic policy applies
minimum profit, ROI, confidence, capacity, asset, legal, and risk thresholds.

### 6.5 Skill adapter

```go
type Skill interface {
    DescribeCapabilities(ctx context.Context) (SkillDescriptor, error)
    Assess(
        ctx context.Context,
        agreement Agreement,
        inventory InventorySnapshot,
    ) (Feasibility, error)
    Reserve(ctx context.Context, actionID ActionID, plan Plan) (Lease, error)
    Execute(ctx context.Context, lease Lease, input Input) (Outcome, error)
    ProduceEvidence(ctx context.Context, outcome Outcome) (ExecutionEvidence, error)
}
```

Fulfillment means performing the locally controlled obligation: running a
Skill, delivering an artifact, releasing a good, providing compute, or taking
one side of an asset exchange. Adapter-specific behavior is selected from the
local registry and Agreement content, not from a new business-category API.

### 6.6 Settlement adapter

```go
type SettlementAdapter interface {
    Prepare(ctx context.Context, agreement Agreement) (PreparedSettlement, error)
    Request(ctx context.Context, action AuthorizedAction) (Attempt, error)
    Resolve(ctx context.Context, reference SettlementRef) (SettlementEvidence, error)
}
```

Adapters expose a shared operational shape but preserve their own guarantees.
No generic method claims that all external settlement is atomic or finalized.

### 6.7 Portfolio ledger and writer fencing

```go
type PortfolioLedger interface {
    Snapshot(ctx context.Context, owner OwnerID, agent AgentID) (PortfolioSnapshot, error)
    Reserve(ctx context.Context, fence WriterFence, reservation Reservation) (ReservationResult, error)
    ApplyEvidence(ctx context.Context, fence WriterFence, actionID ActionID, evidence Evidence) error
    Reconcile(ctx context.Context, fence WriterFence, scope ReconcileScope, apply bool) (ReconcileResult, error)
}

type WriterLease interface {
    Acquire(ctx context.Context, owner OwnerID, agent AgentID, instance InstanceID) (WriterFence, error)
    Renew(ctx context.Context, fence WriterFence) (WriterFence, error)
    Release(ctx context.Context, fence WriterFence) error
}
```

`WriterFence` contains a monotonically increasing generation. Every operation
that creates contact, commitment, reservation, execution, delivery, or
settlement exposure carries the current generation. Local storage and custody
reject stale generations. A process mutex is required even for single-process
deployments but does not replace cross-process or cross-host fencing.

## 7. Domain model

### 7.1 Verified Intent observation

The local record contains:

- exact `PUBLICATION/POST` Agent Operation digest, canonical Intent payload,
  signed Discovery Card, and reference;
- issuer Agent and authorization evidence;
- observed revision/predecessor/withdrawal state;
- source, cursor, retrieval time, and provenance;
- publisher card fields separated from every source/derived index field;
- local search-profile version, hard-filter result, cheap score, diversity
  bucket, and shortlist reason;
- detail and attachment-manifest descriptors, retrieved/verified state, and
  selected attachment metadata;
- settlement preferences and unknown extensions;
- verification result and ambiguity; and
- no claim of globally latest state.

### 7.2 AI assessment

The AI assessment is versioned local evidence containing:

- signed-card interpretation, retrieved-detail classification, and summary;
- publisher-versus-derived discrepancies and remaining ambiguity;
- inferred offered and wanted value;
- questions and ambiguities;
- relevant installed skills, models, tools, credentials, and capacity;
- proposed plan and work units;
- revenue, cost, probability, trust, asset, legal, privacy, and safety
  assumptions;
- recommended response and settlement mode; and
- exact model/profile and prompt-policy revision used.

The assessment is not a signature or commitment.

### 7.3 Opportunity projection

```text
IntentOpportunity {
  exact_operation_key
  issuer_agent_id
  observation_evidence
  assessment_digest
  economic_estimate_digest
  policy_decision
  conversation_ref?
  current_status
}
```

`exact_operation_key` is stable. Later revisions create new exact observations and
update the current actionable view without erasing history.

The pre-contact retrieval projection is explicit:

```text
CARD_OBSERVED
  -> CARD_REJECTED
  -> CARD_SHORTLISTED
       -> DETAIL_FETCHING
       -> DETAIL_UNAVAILABLE | DETAIL_INVALID | DETAIL_VERIFIED
            -> ASSESSED
            -> ATTACHMENT_REVIEWING
            -> IGNORED | WATCHED | RECOMMENDED | CONTACT_READY
```

Retry from `DETAIL_UNAVAILABLE` reuses the same descriptor and budgeted action
identity. A changed digest is a new Intent revision, not a retry result.

### 7.4 Proposal and Agreement

A Proposal contains candidate terms and remains non-binding. An Agreement
contains:

- exact participants;
- referenced Intent revisions;
- bounded exact terms and content-addressed attachments;
- selected execution/delivery assumptions;
- selected settlement mode and adapter parameters;
- validity and cancellation terms; and
- required authorizations.

For trusted mode, the accepted record may be an authenticated conversation
agreement. For higher risk, both Agent authorities or the selected TOS profile
must authorize it.

### 7.5 Engagement

An `Engagement` is the local durable projection of one exact Agreement. It is
not limited to labor and may represent a service, sale, exchange, delivery, or
collaboration.

```text
AGREED
  -> PREPARING
  -> READY
  -> EXECUTING
  -> DELIVERING
  -> DELIVERED
  -> SETTLEMENT_RESOLVING
  -> SETTLED | UNPAID | REFUNDED | FAILED | ABANDONED
```

Adapter-specific substates are nested observations, not new generic business
categories.

### 7.6 Complete economic lifecycle

The coordinator exposes one business-neutral safety lifecycle:

```text
DISCOVERED
  -> FILTERED_OUT
  -> SHORTLISTED
  -> EVALUATED
       -> IGNORED | WATCHED | OWNER_REVIEW
       -> CONTACTING
       -> NEGOTIATING
       -> AGREEMENT_PROPOSED
       -> AGREED
       -> RESOURCE_RESERVED
       -> EXECUTING
       -> DELIVERED
       -> SETTLEMENT_RESOLVING
       -> SETTLED | UNPAID | REFUNDED | DISPUTED | FAILED | ABANDONED
```

The lifecycle is not a task schema. Profiles may skip states that do not apply,
but no external side effect may skip its required policy, authorization,
reservation, custody, or evidence boundary. Every transition records the
expected prior revision, current writer-fence generation, stable action ID,
policy revision, and triggering evidence.

## 8. Discovery and AI processing

### 8.1 Versioned local search profile

The owner configures broad boundaries: allowed sources, maximum cost, privacy,
legal restrictions, contact limits, and excluded content. From OpenFox's
current installed skills, models, resources, obligations, owner preferences,
and verified outcomes, the embedded AI proposes an `IntentSearchProfile`:

```text
IntentSearchProfile {
  profile_id
  version
  created_at
  expires_at
  source_scopes[]
  intent_modes[]
  subject_classes[]
  taxonomy_prefixes[]
  positive_keywords[]
  negative_keywords[]
  accepted_value_rules[]
  schedule_rules[]
  fulfillment_modes[]
  regions[]
  languages[]
  unknown_field_policy{}
  exploration_policy
  budget_policy
  rationale_digest
}
```

Deterministic owner policy validates and clamps this proposal before it is used.
The AI can decide that smart-contract review, BTC purchase, video editing, or a
new inferred niche is worth searching without adding an Intent API. It cannot
add a source, remove an exclusion, widen geography/data rules, or raise a
budget beyond configured authority.

### 8.2 Verification before interpretation

Before detail retrieval or expensive AI analysis, deterministic code checks
the small envelope's size, encoding, network context, lifecycle times, digest,
signature, revision links, exact replay, and known conflicts. It also validates
card field counts, enums, taxonomy syntax, keyword/language bounds, canonical
decimals, amount range ordering, schedule ordering, and descriptor size.

A valid envelope means only that the named issuer authorized those exact
bytes. It does not prove truth, legality, solvency, quality, or payment.

### 8.3 Card filtering, ranking, and staged retrieval

For each verified card, deterministic hard filters first apply mode, coarse
class, required/forbidden taxonomy and keywords, value-state and amount window,
asset support, lifecycle/schedule overlap, fulfillment mode, region/language,
issuer/source policy, and explicit unknown-field rules.

Passing cards receive a cheap local score using bounded rules, lexical match,
or local embeddings. Source rank and derived fields may contribute only with
their provenance and configured weight. The coordinator selects a top-K set
with per-source, per-issuer, per-category, and per-value-band caps plus a small
exploration quota. Keyword repetition cannot increase the score without bound.

Only the shortlist's detail is retrieved. The source must return exactly the
declared bytes; size or digest mismatch quarantines that observation. Deep AI
analysis then decides whether selected public attachments justify their
additional byte, parser, and model-token cost. Private inputs remain
unavailable at this stage.

The local content-addressed cache deduplicates verified detail, manifests,
attachments, embeddings, and assessments by exact digest plus derivation
version. It retains provenance and privacy class. It never overwrites one
digest because a mutable URL, title, or later Intent revision looks similar.

Budget accounting is separate for:

- card queries, pages, bytes, verification time, and retained observations;
- detail fetch count and bytes;
- attachment fetch count, bytes, archive expansion, and parser work;
- embedding and general-model tokens/cost; and
- source, issuer, taxonomy, and cycle wall-clock quotas.

The journal records why a card was rejected, shortlisted, fetched, or left
unfetched. Restart cannot accidentally bypass an earlier tier or spend the same
cycle budget twice.

### 8.4 Hostile-content context

Intent and message content enter the model as quoted untrusted data under a
fixed instruction boundary. Remote content cannot:

- override system or owner instructions;
- call a tool directly;
- choose a credential, model, plugin, MCP server, route, or runtime;
- request hidden data;
- install code; or
- invoke an action or settlement adapter.

Detail and attachments are presented to the model as separate quoted untrusted
objects. Attachments are retrieved through content-addressed quarantine with
media, size, archive, parser, and active-content limits.

### 8.5 Capability and resource assessment

OpenFox builds a current local inventory of:

- installed and owner-approved skills;
- available embedded and external models;
- allowed tools, APIs, credentials, and destinations;
- runtime CPU, memory, disk, accelerator, token, and concurrency capacity;
- legal/privacy/data constraints;
- existing reservations and obligations; and
- historical quality and cost evidence.

The AI performs flexible matching. Deterministic code confirms that every
selected side effect fits the current inventory and owner policy.

### 8.6 Economics and trust

Use exact integers for any value that reaches a supported payment adapter.
Discovery estimates may represent ambiguous or external assets, but must retain
asset description, source, timestamp, confidence, conversion assumptions, and
expiry.

```text
expected value
  = expected consideration * payment probability * delivery probability
    - compute/model/API/tool/labor/subcontractor cost
    - asset conversion and custody risk
    - expected retry, failure, refund, and nonpayment cost
    - privacy/legal/reputation reserve
    - capacity opportunity cost

worst-case exposure
  = committed spend
    + non-refundable work cost
    + asset/custody exposure
    + unresolved obligations
    + maximum nonpayment loss

risk-adjusted ROI
  = expected value / max(committed cost and exposure, minimum unit)
```

Unknown material values require owner approval or rejection. A model estimate
cannot silently become an exact price or probability.

Automatic contact may use a lower informational threshold than automatic
Agreement or execution. Commitment requires all configured minimum profit,
ROI, confidence, capacity, liquidity, settlement, counterparty, and maximum-loss
rules to pass against a fresh inventory and portfolio snapshot.

## 9. Contact and negotiation

### 9.1 Contact policy

Autonomous contact may be enabled separately from economic commitment. Policy
limits:

- allowed issuers, relationship tiers, rooms, topics, regions, and data
  classes;
- maximum messages and model/API cost per period;
- maximum unsolicited first contacts and retry count;
- disclosure templates and forbidden private information;
- impersonation, scam, abuse, and legal checks; and
- quiet hours, pause, and owner-review thresholds.

### 9.2 First-contact message

The message binds:

- exact Intent ID and revision/digest;
- sender and intended issuer Agent IDs;
- stable contact action ID;
- non-binding semantic content; and
- optional capability or portfolio references chosen by OpenFox.

It does not include custody secrets, private task input, or an execution promise.

### 9.3 Negotiation behavior

The AI may ask questions, explain ability, negotiate price and schedule,
propose alternative settlement, and decline. Each turn has bounded tokens,
attachments, tool access, disclosure, and time.

The coordinator records unresolved semantic questions. It does not infer exact
asset, amount, chain, destination, scope, delivery, or release terms when those
matter to an action.

### 9.4 Agreement promotion

When both sides appear ready, OpenFox constructs an exact Proposal from the
conversation. The model explains the Proposal; deterministic code validates
participants, terms digest, settlement adapter, resources, policy, and
authorization requirements.

Promoting the Proposal to Agreement is a distinct action. Changed terms require
a new version. Ordinary chat cannot trigger promotion.

## 10. Execution and delivery

### 10.1 Reservation

Before work begins, OpenFox reserves the exact plan's resources and worst-case
cost. Reservation is keyed by Agreement and stable action ID. Concurrent
instances cannot exceed shared local or custody-enforced exposure. Reservation
requires the current owner/Agent writer-fence generation and atomically checks:

- CPU, memory, disk, accelerator, token, API, time, and concurrency capacity;
- external spend and locked capital;
- outstanding Offers and accepted Agreements;
- delivered-but-unpaid and other unsecured receivables;
- dispute, refund, and maximum-loss reserves; and
- per-counterparty and aggregate portfolio limits.

A stale writer cannot reserve or release resources. Lease expiry initiates
reconciliation; it does not by itself prove that external work or settlement
stopped.

Trusted mode may intentionally accept unsecured payment risk, but it cannot
ignore execution cost or resource limits.

### 10.2 Skill dispatch

The AI chooses among installed adapters. The selected adapter receives only:

- exact Agreement and plan;
- explicitly disclosed input;
- approved tools, credentials, models, destinations, and resource limits;
- cancellation/deadline policy; and
- output/delivery requirements.

Remote text cannot widen that envelope. If no safe adapter exists, OpenFox asks
for owner intervention, renegotiates, or declines.

### 10.3 Delivery

Delivery may use Messenger, content-addressed storage, an authenticated
endpoint, or the selected escrow profile. The delivery record binds exact
Agreement, execution, result, artifact, timestamp, and adapter evidence.

A delivery acknowledgement is not payment unless the settlement mode defines
it as such.

## 11. Settlement adapters

### 11.1 Trusted Gift

OpenFox may perform work before payment when local trust and value-at-risk
policy permit it. After delivery, it can request or wait for an Agent Gift.

The Gift action remains distinct from Agreement and delivery. Expected Gift is
an unsecured expectation. Settled revenue requires finalized destination
credit under the Gift profile.

### 11.2 Direct transfer

The adapter prepares one exact transfer request with asset, amount,
destination, expiry, and replay identity. It may support payment before, during,
or after work.

It does not claim escrow protection or prove work quality.

### 11.3 TOS escrow

The adapter is disabled unless the Agreement fits a released TOS profile. It
uses `tos-service-protocol` for canonical construction and verification and
delegates signing to custody.

The fixed-price machine-checkable Paid Demand profile retains its complete
`BuyerHandoffProfile`, Provider authorization, versioned Quote/escrow,
private-input, Execution Gate, deadline, Receipt, release/refund, bounce, and
recovery requirements. These are adapter requirements, not generic Intent
requirements.

### 11.4 External settlement

External adapters must declare:

- system and asset identity;
- custody and counterparty assumptions;
- evidence source and confidence class;
- finality or reversibility model;
- partial-completion and retry behavior; and
- what OpenFox cannot independently prove.

An unsupported external mode remains conversation-only or approval-required.

## 12. Accounting

The ledger distinguishes evidence classes and never equates quoted value with
revenue.

Candidate accounts include:

- estimated consideration;
- expected unsecured Gift;
- Agreement value;
- prepaid direct transfer;
- escrow-funded receivable;
- external declared receivable;
- incurred compute/model/API/tool/labor cost;
- reserved capacity and locked funds;
- delivered-but-unpaid work;
- settled revenue;
- refund, write-off, and nonpayment loss; and
- asset conversion gain or loss.

Settlement promotion rules:

| Mode | Settled evidence |
|---|---|
| trusted Gift | exact finalized destination credit |
| supported direct TOS transfer | exact finalized destination credit |
| TOS escrow | independently resolved finalized provider-wallet credit |
| external adapter | adapter's declared evidence class; never labelled TOS-finalized |
| no payment | no revenue |

The journal records original estimate, revised Agreement estimate, actual cost,
settlement evidence, and variance.

## 13. Continuous operation and learning

The coordinator periodically:

1. resumes unresolved source cursors, conversations, Agreements, work, and
   settlements;
2. retrieves new Intents under bounded AI-selected queries;
3. recomputes capability, capacity, economics, and trust;
4. sends permitted messages or requests owner review;
5. advances authorized Agreements;
6. reconciles payment evidence; and
7. emits bounded learning records.

Learning may adjust:

- source/topic/search preference;
- semantic classifiers and embeddings;
- effort, cost, acceptance, delivery, and payment estimates;
- negotiation strategy;
- counterparty trust recommendations;
- settlement-mode recommendations; and
- proposed skill or adapter improvements.

Learning cannot automatically add a source with new disclosure risk, install a
skill or adapter, authorize a credential, increase budgets, weaken sandboxing,
change settlement evidence, or erase adverse outcomes.

## 14. Configuration sketch

```yaml
earning:
  mode: observe                  # off | observe | contact | trusted | policy-gated
  writer_lease:
    backend: owner-scoped-durable-store
    ttl_seconds: 30
    renew_seconds: 10
    require_custody_fence: true
  sources:
    - id: public-intents
      adapter: gateway
      max_cards_per_page: 100
    - id: messenger-work-room
      adapter: messenger-room
      max_cards_per_page: 100
  search_profile:
    ai_proposals_enabled: true
    subject_classes: [service, asset, digital_good]
    taxonomy_prefixes:
      - tos.taxonomy.v1/service/security
    positive_keywords: [audit, review, smart-contract]
    negative_keywords: []
    value_states: [specified, range, negotiable]
    unknown_value: deprioritize       # include | exclude | deprioritize
    unknown_schedule: include
    unknown_region: include
    languages: [en, zh]
    exploration_percent: 10
  acquisition:
    max_queries_per_cycle: 20
    max_card_bytes_per_cycle: 1048576
    max_detail_fetches_per_cycle: 40
    max_detail_bytes_per_cycle: 8388608
    max_attachment_fetches_per_cycle: 8
    max_attachment_bytes_per_cycle: 16777216
    max_model_tokens_per_cycle: 50000
    max_candidates_retained: 1000
    shortlist_size: 40
    max_shortlist_per_issuer: 3
    max_shortlist_per_taxonomy: 12
  contact:
    enabled: false
    max_first_contacts_per_day: 10
    max_messages_per_conversation: 30
    owner_approval_above_disclosure_class: internal
  business:
    max_concurrent_agreements: 2
    max_unsecured_cost_atomic: "0"
    maximum_external_spend_atomic: "0"
    maximum_total_exposure_atomic: "0"
    minimum_expected_profit_atomic: "0"
    minimum_risk_adjusted_roi_bps: 3000
    minimum_assessment_confidence_bps: 8000
    minimum_expected_margin_bps: 3000
  settlement:
    allowed:
      - trusted-gift
      - tos-escrow
    default_for_unknown_counterparty: tos-escrow
    external_requires_owner_approval: true
```

Configuration is owner policy. Intent content cannot edit it.

## 15. Operator interface

Read-only commands:

```text
openfox earning sources
openfox earning profile show
openfox earning search <text>
openfox earning opportunity inspect <operation-ref>
openfox earning explain <operation-ref>
openfox earning inventory show
openfox earning portfolio show
openfox earning writer status
openfox earning conversations
openfox earning agreement inspect <agreement-id>
openfox earning engagement list
openfox earning accounting summary
openfox earning settlement inspect <agreement-id>
openfox earning reconcile --dry-run
```

Mutating commands require local authorization and stable action IDs:

```text
openfox earning contact <operation-ref>
openfox earning profile regenerate
openfox earning agreement propose <conversation-id>
openfox earning agreement accept <agreement-id>
openfox earning engagement authorize <agreement-id>
openfox earning settlement request <agreement-id>
openfox earning reconcile --apply
openfox earning writer takeover
openfox earning pause [source|contact|skill|adapter|all]
openfox earning drain
openfox earning resume
```

`writer takeover` requires explicit owner authorization, increments the fencing
generation, invalidates the prior writer, and forces reconciliation before new
economic actions. `reconcile --dry-run` is read-only; `--apply` uses a stable
action ID, audit record, writer fence, and crash recovery.

The UI must distinguish AI suggestion, non-binding message, Proposal,
Agreement, fulfillment authorization, delivery, expected payment, payment
request, and settled revenue.

## 16. Observability

Metrics include:

- card queries/pages/bytes, cards verified, expired, withdrawn, conflicting,
  filtered, shortlisted, and rejected by reason;
- shortlist diversity by source, issuer, class, taxonomy, and value band;
- detail/attachment fetch count, bytes, cache hit, digest mismatch, parser cost,
  and skipped-budget reason;
- search-profile version, changes, query coverage, unknown-field decisions, and
  exploration share;
- AI classifications, model cost, and decision explanations;
- capability/resource matches and rejection reasons;
- contacts, replies, conversation turns, and abuse/rate-limit events;
- Proposals and Agreements by settlement mode;
- engagements accepted, fulfilled, failed, abandoned, and unpaid;
- expected versus actual cost and duration;
- Gifts, direct payments, escrow settlements, refunds, and external evidence;
- gross revenue, cost, realized net income, nonpayment, and write-off;
- source, skill, model, counterparty, asset, and settlement-adapter performance;
  and
- pause, drain, recovery, and unresolved-action age.

Logs never contain custody secrets, private input, full confidential messages,
or unrestricted model context.

## 17. Delivery plan

### Phase 0 — current-source audit and protocol fixtures

- re-audit the selected OpenFox commit;
- freeze the common Agent Operation Envelope plus the Intent payload, signed
  Discovery Card, detail descriptor, publisher/derived-field boundary, query,
  and Agreement vectors in `tos-service-spec` and `tos-service-protocol`;
- freeze coarse modes/classes, taxonomy and region identifier syntax, keyword/
  language rules, canonical decimal value hints, schedule ordering, and all
  card/detail/attachment bounds;
- decide whether existing opportunity storage can represent generic exact
  operation and Intent identity or needs `pkg/opportunity`;
- build semantically varied fixtures; and
- keep every external action disabled.

Exit: two independent codecs/verifiers agree on the common operation and Intent
payload, unrelated goods, services, and asset exchange require no new core
opcode or fields, and a second implementation filters signed cards without
retrieving detail.

### Phase 1 — read-only Intent scout

- implement bounded card search, exact verification, and source-local cursors;
- compile versioned AI-proposed search profiles under deterministic owner
  policy;
- implement hard card filters, cheap local scoring, issuer/category/value
  diversity quotas, and a bounded exploration bucket;
- retrieve and digest-check only shortlisted detail and separately approved
  public attachments;
- add hostile-content isolation;
- expose the local capability/resource inventory;
- let the embedded AI choose bounded queries and classify Intents;
- calculate explainable economics and trust/risk estimates;
- persist Opportunity projections and cursors; and
- expose read-only CLI/UI.

Exit: seven days of restart-safe observation across varied Intent categories;
most irrelevant cards are rejected without detail or general-model cost, all
detail fetches are explainable and bounded, and no message or economic side
effect occurs. A one-Carrier run is explicitly a local prototype and cannot be
advertised as resilient decentralized public discovery.

### Phase 2 — authenticated contact and negotiation

- add Intent-referenced first contact through existing Messenger;
- enable bounded open-ended conversation;
- add contact/disclosure/abuse policies;
- implement Proposal and Agreement versioning;
- ensure ordinary chat is non-binding; and
- recover ambiguous send and restart without duplicate Agreement actions.

Exit: two fresh Agents negotiate changed terms and freeze one exact Agreement
without chain settlement.

### Phase 3 — trusted low-risk work

- enable one reviewed local skill or executor;
- reserve resources and worst-case cost;
- execute and deliver under one trusted Agreement;
- record nonpayment exposure;
- optionally request/receive an existing Agent Gift or direct transfer; and
- reconcile paid or unpaid outcome.

Exit: one real low-value job completes without invoking Accepted Quote or
escrow. Nonpayment must be handled as a valid adverse business outcome.

### Phase 4 — policy-gated settlement adapters

- add a common adapter registry;
- enable Agent Gift and supported direct-transfer modes;
- add external adapters only with explicit evidence labels and owner approval;
- optionally integrate the released TOS escrow profile; and
- prove disabling any adapter does not disable discovery or negotiation.

Exit: the same Intent/Agreement path selects at least two settlement modes
without category-specific core code.

### Phase 5 — optional untrusted TOS escrow

This phase is required only for Agents that select the Paid Demand TOS escrow
profile.

- satisfy its independent specification, contract, Gate, custody, ingress,
  execution, Receipt, settlement, and recovery prerequisites;
- adapt one Agreement without treating conversation text as missing authority;
- complete one public-testnet fixed-price task; and
- independently resolve provider-wallet credit.

Exit: the high-assurance path works as an optional adapter and cannot weaken or
be confused with trusted modes.

### Phase 6 — federation and bounded improvement

- add independent carriers and source-failure recovery;
- integrate optional centralized markets as leads;
- add new skills and settlement adapters without changing Intent core;
- calibrate estimates from verified outcomes; and
- add canary learning changes with review and rollback.

Exit: recurring varied commerce improves measured matching or profitability
without expanding authority automatically. Production public-discovery claims
additionally require at least two independently operated Carrier paths and
successful recovery after one Carrier and its complete database are removed.

## 18. Test strategy

### Agent Operations, Intent, and sources

- exact common Agent Operation codec, payload binding, signature, replay, and
  profile vectors;
- unrelated content categories under one envelope and common Discovery Card;
- required card fields, field-count/text bounds, canonical decimals, amount
  ordering, schedule ordering, taxonomy/region syntax, and language tags;
- search by mode, class, taxonomy, keyword, value range, lifecycle/schedule,
  fulfillment, region, and language without eager detail retrieval;
- explicit include/exclude/deprioritize behavior for unknown value, schedule,
  region, language, and taxonomy;
- publisher fields separated from derived translation, taxonomy mapping,
  embedding, price conversion, risk label, and rank provenance;
- detail size/digest mismatch, mutable retrieval URL, unavailable detail, and
  attachment-budget exhaustion;
- keyword stuffing, one-issuer flooding, one-category starvation, source-rank
  manipulation, and diversity/exploration quota enforcement;
- source adapter receives only the projected query, not credentials, full skill
  inventory, portfolio, or exact local profitability threshold;
- unknown required and optional extension behavior;
- exact replay, conflicting revision, withdrawal, expiry, and stale observation;
- malformed sizes, references, routes, hints, and content types;
- source cursor replay, loss, corruption, and independent-source divergence;
  and
- one-source verified contact without a false global-head claim.

### Capability, economics, portfolio, and writer fencing

- stale, missing, or internally inconsistent capability inventory;
- unavailable model, Skill, tool, credential, wallet, asset, or capacity;
- deterministic profit and risk-adjusted ROI calculations around threshold
  boundaries, unknown costs, uncertain payment, and adverse outcomes;
- atomic reservation and release of compute, spend, capital, receivables, loss
  allowance, counterparty exposure, and total portfolio exposure;
- two local processes and two hosts competing for the same owner/Agent writer
  lease;
- an expired or superseded fencing generation unable to contact, propose,
  agree, reserve, execute, settle, reconcile with changes, or release another
  writer's reservation; and
- crash, lease expiry, takeover, journal replay, and evidence-driven
  reconciliation without duplicate economic actions.

### AI and hostile content

- prompt injection requesting tools, keys, routes, policy changes, private data,
  payment, or model replacement;
- malicious attachments, archives, links, active content, and oversized input;
- incorrect semantic classification and uncertainty propagation;
- capability/resource mismatch despite model confidence;
- missing cost and asset data;
- external asset ambiguity; and
- deterministic policy override of an unsafe AI recommendation.

### Conversation and Agreement

- wrong issuer, alias transfer, device rotation, session retry, duplicate and
  ambiguous send;
- excessive unsolicited contact and disclosure;
- model message containing “accept” without Agreement action;
- changed terms under reused Agreement identity;
- concurrent Proposals and stale acceptance;
- Intent withdrawal before and after Agreement; and
- crash at every negotiation and authorization boundary.

### Execution

- unavailable skill/model/tool/credential;
- resource overcommit across concurrent Agreements;
- task-selected credential or destination;
- restart before and after first execution start;
- bounded failure, cancellation, delivery retry, and duplicate prevention; and
- result delivered without falsely claiming payment.

### Settlement

- trusted work paid and unpaid;
- Gift/direct transfer wrong destination, amount, asset, replay, and ambiguity;
- external evidence labelled below TOS finality;
- unsupported adapter and owner-approval enforcement;
- TOS escrow profile's complete independent adversarial matrix; and
- no adapter state substituting for another mode's evidence.

### Accounting and learning

- quoted value never counted as revenue;
- expected Gift remains unsecured;
- exact promotion by evidence class;
- cost and nonpayment write-off;
- crash/replay-safe reconciliation;
- adverse outcomes retained; and
- learning cannot change budgets, skills, adapters, credentials, or authority.

## 19. MVP acceptance criteria

The generic autonomous-earning MVP is accepted only when:

1. the same common Agent Operation envelope and Intent payload profile
   represent at least five unrelated economic intents, including a service
   request, service offering, asset buy, asset sale, and open collaboration;
2. each active Intent exposes a bounded signed Discovery Card containing a
   coarse direction/class, keywords, explicit value state, lifecycle, and
   digest-bound detail descriptor;
3. OpenFox builds a fresh, evidence-backed Capability Inventory covering its
   current Skills, models, tools, credentials, wallets, assets, capacity,
   reservations, obligations, costs, and relevant verified outcomes;
4. OpenFox's embedded AI proposes a versioned bounded search profile from that
   inventory, and deterministic owner policy clamps it;
5. card queries and deterministic filters cover category/keyword, approximate
   value, time, fulfillment, region, and language without retrieving every
   Intent detail;
6. publisher claims and derived classifications, translations, conversions,
   embeddings, and ranks remain visibly separate and provenance-bound;
7. hard filters plus diversity quotas reject irrelevant/flooding cards before
   general-model analysis, while an explicit exploration quota avoids a fully
   closed recommendation loop;
8. only shortlisted detail and approved attachments are fetched, each under
   separate budgets and exact digest/size verification;
9. OpenFox explains search-profile, rejection, shortlist, detail-fetch,
   semantic, capability, resource, profit, and risk decisions;
10. the Economic Evaluator calculates explainable expected net profit and
    risk-adjusted ROI, and deterministic thresholds reject opportunities whose
    costs, payment probability, downside, or confidence are unacceptable;
11. hostile content cannot control tools, credentials, models, routes, policies,
   execution, disclosure, or payment;
12. OpenFox A contacts OpenFox B through authenticated Messenger using an exact
   Intent reference;
13. A and B negotiate natural-language terms and produce a separate exact
   Agreement;
14. ordinary messages cannot create an Agreement or economic side effect;
15. one active writer lease and fencing generation governs all economic
    actions for the owner/Agent, including across multiple processes or hosts;
16. compute, spend, capital, receivable risk, and counterparty/global exposure
    are atomically reserved before commitment, and aggregate portfolio limits
    cannot be bypassed by concurrent opportunities;
17. one owner-approved bounded skill executes and delivers under that
    Agreement;
18. one trusted low-risk run records either verified Gift/direct payment or an
   honest unpaid outcome;
19. the Portfolio Ledger reconciles actual cost and settlement evidence
    without calling expected value revenue;
20. restart, writer takeover, and exact retry create no duplicate contact,
    Agreement, execution, Gift, transfer, or settlement action;
21. pause and drain work at source, contact, skill, adapter, and global scope;
22. the entire MVP works with TOS escrow support disabled; and
23. if TOS escrow is demonstrated, it separately passes every specialized
    profile gate.

Two independent carriers are required before claiming resilient decentralized
public availability. They are not required before first contact about one
verified signed Intent.

## 20. Non-goals

The implementation does not require:

- a universal business taxonomy;
- one interface per task or asset type;
- one core coordinator or lifecycle per business category;
- a task profile before conversation;
- a central market database or global winner;
- mandatory TOS escrow, stablecoin, Evaluator, or Receipt;
- automatic enforcement of arbitrary natural-language work;
- unrestricted model access to custody, credentials, tools, or network;
- TOS settlement claims for BTC, fiat, or external systems; or
- modifying every related repository before OpenFox can perform trusted work.

## 21. Open decisions

1. Should the first generic Carrier be a Messenger public room, a Gateway
   search endpoint, or both behind one `OpportunitySource` interface?
2. What exact owner policy permits autonomous first contact?
3. What minimum Agreement fields are required for trusted work?
4. Which existing OpenFox skill is safe and useful for the first low-value
   trusted run?
5. Should trusted Agreement acceptance require both Agent signatures or a
   mutually authenticated Messenger transcript digest?
6. Which Gift or direct-transfer adapter should be demonstrated first?
7. How should external asset descriptions and price observations be normalized
   locally without becoming protocol authority?
8. What retention and disclosure defaults apply to public Intent and private
   negotiation content?
9. Which evidence class permits counterparty trust calibration?
10. When does value at risk require owner approval or TOS escrow?
11. Which durable store and custody boundary enforce owner/Agent writer fencing
    across processes and hosts?
12. Which reservation dimensions and evidence release each class of aggregate
    portfolio exposure?

Until these decisions are frozen and tested, OpenFox may implement the
read-only scout. Autonomous contact, Agreement, execution, Gift, transfer,
escrow, and external settlement must be enabled one bounded phase at a time.
