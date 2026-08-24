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
> advertises bounded services, schedules a portfolio of obligations, and learns
> from verified outcomes.

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

The same coordinator also runs a bounded supply loop:

```text
Capability Inventory + verified cost/outcome evidence
  -> AI proposes service Intent and price range
  -> deterministic publication and exposure policy
  -> writer-fenced publish/revise/withdraw action
  -> customer contact enters the same negotiation and Agreement path
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
| Local execution authorization | No common OpenFox Gate binds every Skill plan to exact files, domains, credentials, resources, disclosure, policy, approval, writer fence, and expiry. |
| Autonomous supply | No durable loop safely publishes, reprices, revises, or withdraws OpenFox's own service Intents. |
| Portfolio scheduling and subcontracting | Concurrency limits do not yet define deadline-, priority-, dependency- and exposure-aware scheduling or separate downstream Agreements. |
| Milestone and periodic billing | No generic obligation sequence reconciles invoices, installments, partial payments, accumulated balances, and bounded recurring mandates. |
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

pkg/publication/
  manager.go          # draft -> authorize -> publish/reply/revise/withdraw
  pricing.go          # bounded price and capacity proposals
  policy.go           # audience, rate, disclosure and revision limits
  store.go            # exact publication chains and Carrier observations

pkg/negotiation/
  conversation.go     # Intent-referenced Messenger coordination
  proposal.go         # non-binding proposals
  compiler.go         # conversation -> exact generic Agreement candidate
  agreement.go        # exact Agreement versions and authorization state
  store.go            # durable conversation/Agreement projection

pkg/business/
  inventory.go        # current Skills, models, tools, credentials and capacity
  economics.go        # explainable expected profit, ROI, trust and risk
  portfolio.go        # atomic reservations and aggregate exposure limits
  ledger.go           # evidence-class-aware P&L, receivables and reconciliation
  scheduler.go        # deadline-, priority- and exposure-aware work ordering
  billing.go          # invoices, milestones and periodic payment obligations

pkg/skilladapter/
  skill.go            # generic bounded Skill interface
  registry.go         # owner-approved installed Skills
  gate.go             # local execution authorization for every Skill
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
    SubscribeCards(
        ctx context.Context,
        filter CardFilter,
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

Subscriptions are resumable bounded acquisition, not an unbounded push channel.
Each batch advances a source-local cursor and is subject to the same byte, card,
issuer, topic, retry, and verification budgets as search.

Search returns exact bounded signed cards or exact references plus provenance;
any derived labels or rank are separate attributed fields. Detail, attachment
manifest, and selected attachments reuse one explicit content fetch and must
match their signed size and digest. Search may be
lexical, taxonomy-, value-, time-, region-, language-, embedding-, room-, or
application-based. A source's filtering or ranking never becomes OpenFox's
decision or issuer authority.

### 6.2 Publication manager and pricing policy

```go
type IntentPublisher interface {
    Draft(
        ctx context.Context,
        inventory InventorySnapshot,
        portfolio PortfolioSnapshot,
        request PublicationRequest,
    ) (IntentDraft, error)
    Publish(
        ctx context.Context,
        fence WriterFence,
        action AuthorizedPublicationAction,
    ) (PublicationResult, error)
    Reply(
        ctx context.Context,
        fence WriterFence,
        action AuthorizedReplyAction,
    ) (PublicationResult, error)
    Revise(
        ctx context.Context,
        fence WriterFence,
        action AuthorizedPublicationAction,
    ) (PublicationResult, error)
    Withdraw(
        ctx context.Context,
        fence WriterFence,
        action AuthorizedWithdrawalAction,
    ) (PublicationResult, error)
}
```

The AI may propose service descriptions, capability hints, audience, price
ranges, availability, and expiry from the current inventory and verified cost
history. Deterministic publication policy enforces minimum margin, maximum
discount, exposure, disclosure, active-post, revision, reply, Carrier, and
per-period limits. Custody signs only the final authorized Agent Operation.

A public offer advertises availability; it does not reserve all advertised
capacity or create an Agreement. Before contact or commitment, OpenFox refreshes
inventory, price, schedule, and portfolio state. Material price, capability,
audience, schedule, or detail changes create a new signed revision. Automatic
refresh cannot conceal a worse price or rewrite an earlier issuer assertion.

### 6.3 Capability inventory

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

### 6.4 Conversation transport

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

### 6.5 Generic Agreement compiler

```go
type AgreementCompiler interface {
    Compile(
        ctx context.Context,
        conversation ConversationSnapshot,
        intentRefs []IntentRef,
        proposedTerms ProposedTerms,
    ) (AgreementCandidate, error)
    Validate(
        ctx context.Context,
        candidate AgreementCandidate,
        inventory InventorySnapshot,
        portfolio PortfolioSnapshot,
    ) (AgreementValidation, error)
}
```

Compilation converts a bounded conversation and selected attachments into one
exact candidate that binds participants, referenced publications, terms and
attachment digests, deliverables, consideration, schedule, acceptance evidence,
confidentiality, cancellation, dispute and billing terms, settlement mode, and
expiry. Business-specific meaning remains in exact terms or namespaced
extensions. The compiler cannot sign, reserve, execute, or settle; those remain
separate authorized actions.

### 6.6 Economic evaluator

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

### 6.7 Skill adapter

```go
type Skill interface {
    DescribeCapabilities(ctx context.Context) (SkillDescriptor, error)
    Estimate(
        ctx context.Context,
        input CandidateInput,
        inventory InventorySnapshot,
    ) (Feasibility, error)
    Plan(
        ctx context.Context,
        agreement Agreement,
        inventory InventorySnapshot,
    ) (ExecutionPlan, error)
    Execute(
        ctx context.Context,
        authorization ExecutionAuthorization,
        plan ExecutionPlan,
        input Input,
    ) (Outcome, error)
    ProduceEvidence(ctx context.Context, outcome Outcome) (ExecutionEvidence, error)
}
```

Fulfillment means performing the locally controlled obligation: running a
Skill, delivering an artifact, releasing a good, providing compute, or taking
one side of an asset exchange. Adapter-specific behavior is selected from the
local registry and Agreement content, not from a new business-category API.

### 6.8 Local Execution Gate

```go
type ExecutionGate interface {
    Authorize(
        ctx context.Context,
        fence WriterFence,
        agreement Agreement,
        plan ExecutionPlan,
        reservation Reservation,
        policyRevision PolicyRevision,
    ) (ExecutionAuthorization, error)
    RevalidateAtLaunch(
        ctx context.Context,
        authorization ExecutionAuthorization,
    ) error
}
```

This is OpenFox's local gate for every Skill, not the optional TOS Native
Execution Gate used by an escrow profile. Its authorization binds exact
Agreement, plan and input digests; Skill and model versions; sandbox; allowed
files and directories; network domains and destinations; task-scoped credential
handles; CPU, memory, storage, accelerator, token, time and spend budgets;
allowed disclosures and uploads; destructive-operation flags; reservation;
writer fencing generation; owner approval evidence; policy revision; and
expiry.

The executor receives handles scoped to the exact Skill, task, domain and
destination rather than long-lived custody or general credentials. It rejects a
stale writer, expired authorization, plan mutation, additional network target,
unapproved upload, or destructive side effect. A successful Gate decision does
not prove correct work or authorize payment.

### 6.9 Engagement scheduler

```go
type EngagementScheduler interface {
    Schedule(
        ctx context.Context,
        inventory InventorySnapshot,
        portfolio PortfolioSnapshot,
        engagements []SchedulableEngagement,
    ) (ScheduleDecision, error)
}
```

Scheduling considers Agreement deadlines, expected profit, risk, priority,
resource compatibility, setup cost, fairness, dependencies, cancellation cost,
and settlement exposure. It may delay or recommend rejection, but it cannot
invent capacity, exceed reservations, or preempt irreversible work. Every
dispatch still requires the current writer fence and a fresh Execution Gate
authorization.

### 6.10 Settlement adapter

```go
type SettlementAdapter interface {
    Prepare(
        ctx context.Context,
        agreement Agreement,
        obligation SettlementObligation,
    ) (PreparedSettlement, error)
    Request(ctx context.Context, action AuthorizedAction) (Attempt, error)
    Resolve(ctx context.Context, reference SettlementRef) (SettlementEvidence, error)
}
```

Adapters expose a shared operational shape but preserve their own guarantees.
No generic method claims that all external settlement is atomic or finalized.
`SettlementObligation` identifies an exact deposit, milestone, installment,
period, final balance, refund, or other Agreement-bound obligation. Each request
has its own stable action ID and evidence; a schedule is not unlimited recurring
payment authority.

### 6.11 Portfolio ledger and writer fencing

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

The AI chooses among installed adapters and proposes an exact `ExecutionPlan`.
The Portfolio Ledger reserves its worst-case resources and exposure before the
local Execution Gate evaluates it. The selected adapter receives only:

- exact Agreement and plan;
- explicitly disclosed input;
- approved tools, credentials, models, destinations, and resource limits;
- cancellation/deadline policy; and
- output/delivery requirements.

Remote text cannot widen that envelope. If no safe adapter exists, OpenFox asks
for owner intervention, renegotiates, or declines.

Immediately before launch, the Gate revalidates the current writer generation,
Agreement and plan digests, reservation, policy revision, credential handles,
destinations, approval evidence, and expiry. Plan mutation or a lost reservation
requires a new authorization; retry does not reuse an authorization whose
one-shot effects may already have occurred.

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

### 11.5 Milestones, invoices, and periodic settlement

An Agreement may contain exact billing terms for a deposit, milestones,
installments, usage periods, a final balance, or an accumulated low-value
balance. OpenFox projects each due item as a separate `Invoice` or payment
obligation with Agreement digest, sequence, asset, amount, due time, payer,
payee, settlement adapter, stable action ID, and evidence state.

Periodic terms authorize only the bounded schedule and maximum aggregate amount
in the Agreement or a separate mandate. They do not let the model invent a new
charge. A cumulative execution Receipt is valid only when the selected profile
defines how exact completed units and payment are bound; otherwise OpenFox keeps
separate execution evidence and payment requests. Partial payment never settles
unpaid obligations implicitly.

## 12. Accounting

The ledger distinguishes evidence classes and never equates quoted value with
revenue.

Candidate accounts include:

- estimated consideration;
- expected unsecured Gift;
- Agreement value;
- issued and received invoices by obligation sequence;
- milestone, installment, and accumulated-balance receivables;
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
invoice or obligation sequence, settlement evidence, outstanding balance, and
variance.

## 13. Continuous operation and learning

The coordinator periodically:

1. resumes unresolved source cursors, conversations, Agreements, work, and
   settlements;
2. retrieves new Intents under bounded AI-selected queries;
3. recomputes capability, capacity, economics, and trust;
4. sends permitted messages or requests owner review;
5. advances authorized Agreements;
6. reconciles payment evidence; and
7. schedules eligible Engagements within reserved capacity;
8. reviews active service publications against current costs, capacity, and
   expiry;
9. publishes, revises, or withdraws only policy-authorized service Intents; and
10. emits bounded learning records.

Learning may adjust:

- source/topic/search preference;
- semantic classifiers and embeddings;
- effort, cost, acceptance, delivery, and payment estimates;
- negotiation strategy;
- price-floor, quote-range, and publication-timing proposals;
- counterparty trust recommendations;
- settlement-mode recommendations; and
- proposed skill or adapter improvements.

Learning cannot automatically add a source with new disclosure risk, install a
skill or adapter, authorize a credential, increase budgets, weaken sandboxing,
change settlement evidence, or erase adverse outcomes. A learned pricing or
publication change is a proposal that still passes deterministic margin,
exposure, disclosure, rate, signing, and writer-fencing policy.

OpenFox may use the same Intent loop in the opposite economic direction to find
a customer, supplier, or subcontractor. A subcontract creates a separate exact
Agreement, reservation, disclosure decision, and settlement obligation. The
upstream Agreement does not delegate private input, owner credentials, payment
authority, or deadline changes to the subcontractor, and downstream failure
remains part of the principal's portfolio exposure.

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
  publication:
    enabled: false
    max_active_service_intents: 5
    max_new_posts_per_day: 2
    max_revisions_per_post_per_day: 3
    max_public_replies_per_day: 10
    minimum_ttl_seconds: 3600
    maximum_ttl_seconds: 604800
    pricing:
      minimum_expected_margin_bps: 3000
      maximum_discount_bps: 1000
      maximum_revision_change_bps: 2500
  contact:
    enabled: false
    max_first_contacts_per_day: 10
    max_replies_per_day: 50
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
  execution_gate:
    require_fresh_writer_fence: true
    require_exact_plan_digest: true
    deny_unlisted_network_destinations: true
    deny_unlisted_credential_handles: true
    destructive_actions_require_owner_approval: true
  scheduling:
    max_dispatches_per_cycle: 2
    irreversible_work_is_not_preemptible: true
    deadline_miss_requires_replan_or_owner_review: true
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
openfox earning publications list
openfox earning publication inspect <operation-ref>
openfox earning schedule show
openfox earning search <text>
openfox earning opportunity inspect <operation-ref>
openfox earning explain <operation-ref>
openfox earning inventory show
openfox earning portfolio show
openfox earning writer status
openfox earning conversations
openfox earning agreement inspect <agreement-id>
openfox earning engagement list
openfox earning billing obligations <agreement-id>
openfox earning accounting summary
openfox earning settlement inspect <agreement-id>
openfox earning reconcile --dry-run
```

Mutating commands require local authorization and stable action IDs:

```text
openfox earning contact <operation-ref>
openfox earning profile regenerate
openfox earning publication draft <template>
openfox earning publication publish <draft-id>
openfox earning publication reply <operation-ref>
openfox earning publication revise <operation-ref>
openfox earning publication withdraw <operation-ref>
openfox earning agreement propose <conversation-id>
openfox earning agreement accept <agreement-id>
openfox earning engagement authorize <agreement-id>
openfox earning schedule recompute
openfox earning settlement request <agreement-id> <obligation-id>
openfox earning reconcile --apply
openfox earning writer takeover
openfox earning pause [source|publication|contact|scheduler|skill|adapter|all]
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
- publication drafts, posts, revisions, withdrawals, audience, price changes,
  active-post age, Carrier propagation, and publication-rate rejections;
- Proposals and Agreements by settlement mode;
- engagements accepted, fulfilled, failed, abandoned, and unpaid;
- expected versus actual cost and duration;
- scheduler decisions, deadline risk, preemption rejection, queue age, and
  capacity utilization;
- Execution Gate approvals and denials by policy reason, excluding secrets;
- invoices, installments, accumulated balances, partial payments, and overdue
  obligations;
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
  language rules, capability-hint identifiers, canonical decimal value hints,
  schedule ordering, and all card/detail/attachment bounds;
- decide whether existing opportunity storage can represent generic exact
  operation and Intent identity or needs `pkg/opportunity`;
- build semantically varied fixtures; and
- keep every external action disabled.

Exit: two independent codecs/verifiers agree on the common operation and Intent
payload, unrelated goods, services, and asset exchange require no new core
opcode or fields, and a second implementation filters signed cards without
retrieving detail.

### Phase 1 — read-only Intent scout

- implement bounded card search and subscription, exact verification, and
  source-local cursors;
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
- compile exact generic Agreement candidates from bounded conversation and
  selected content without granting signing authority;
- ensure ordinary chat is non-binding; and
- recover ambiguous send and restart without duplicate Agreement actions.

Exit: two fresh Agents negotiate changed terms and freeze one exact Agreement
without chain settlement.

### Phase 3 — trusted low-risk work

- enable one reviewed local skill or executor;
- reserve resources and worst-case cost;
- construct an exact plan and pass the local Execution Gate before launch;
- execute, schedule, and deliver under one trusted Agreement;
- record nonpayment exposure;
- optionally request/receive an existing Agent Gift or direct transfer; and
- reconcile paid or unpaid outcome.

Exit: one real low-value job completes without invoking Accepted Quote or
escrow. Nonpayment must be handled as a valid adverse business outcome.

### Phase 4 — policy-gated settlement adapters

- add a common adapter registry;
- enable Agent Gift and supported direct-transfer modes;
- project deposits, milestones, installments, periodic obligations, invoices,
  partial payments, and outstanding balances without recurring implicit
  authority;
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
- publish, revise, and withdraw bounded service Intents under owner policy;
- propose dynamic price ranges from verified cost and outcome evidence while
  enforcing deterministic margin, discount, exposure, and revision limits;
- schedule multiple Agreements without exceeding reservations or deadlines;
- use the same Intent loop to find customers, suppliers, and subcontractors
  under separate Agreement, disclosure, reservation, and settlement boundaries;
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
- search and subscription by mode, class, taxonomy, keyword, optional
  capability hint, value range, lifecycle/schedule, fulfillment, region, and
  language without eager detail retrieval;
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

### Publication and pricing

- AI-proposed service card, capability hints, price range, schedule, audience,
  detail, and expiry rejected or clamped by deterministic policy;
- stale inventory, cost, capacity, portfolio, policy revision, or writer fence;
- post, revision, public-reply, active-post, per-Carrier, disclosure, TTL,
  minimum-margin, maximum-discount, and maximum-price-change limits;
- duplicate or ambiguous publish, partial Carrier propagation, retry, crash,
  revision conflict, expiry, and withdrawal;
- a public offer never treated as reserved capacity or an Agreement; and
- earlier signed prices and claims remain visible after automatic repricing.

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
- changed Agreement, plan, input, Skill/model version, policy revision,
  reservation, writer fence, approval evidence, or authorization expiry;
- unlisted file, directory, domain, destination, credential handle, upload,
  network route, destructive action, or resource use;
- restart before and after first execution start;
- bounded failure, cancellation, delivery retry, and duplicate prevention; and
- result delivered without falsely claiming payment.

### Scheduling and subcontracting

- concurrent deadline, priority, dependency, resource, and exposure conflicts;
- starvation, unsafe preemption, lost reservation, stale queue item, and
  irreversible work;
- scheduler output unable to bypass writer fencing or the Execution Gate;
- subcontractor unavailable, late, unpaid, malicious, or requesting upstream
  private input; and
- upstream and downstream Agreements, evidence, reservations, and settlement
  remaining distinct under retry and failure.

### Settlement

- trusted work paid and unpaid;
- Gift/direct transfer wrong destination, amount, asset, replay, and ambiguity;
- external evidence labelled below TOS finality;
- unsupported adapter and owner-approval enforcement;
- duplicate, skipped, reordered, partial, overdue, cancelled, or over-limit
  milestone and periodic obligations;
- a billing schedule unable to create unlimited recurring payment authority;
- cumulative execution evidence not treated as payment without a profile that
  binds both;
- TOS escrow profile's complete independent adversarial matrix; and
- no adapter state substituting for another mode's evidence.

### Accounting and learning

- quoted value never counted as revenue;
- expected Gift remains unsecured;
- exact promotion by evidence class;
- invoices, installments, partial payments, accumulated balances, and overdue
  obligations reconcile by exact sequence and stable action ID;
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
   coarse direction/class, keywords, optional namespaced capability hints,
   explicit value state, lifecycle, and digest-bound detail descriptor;
3. OpenFox builds a fresh, evidence-backed Capability Inventory covering its
   current Skills, models, tools, credentials, wallets, assets, capacity,
   reservations, obligations, costs, and relevant verified outcomes;
4. OpenFox's embedded AI proposes a versioned bounded search profile from that
   inventory, and deterministic owner policy clamps it;
5. card search or subscription and deterministic filters cover category,
   keyword, optional capability hint, approximate value, time, fulfillment,
   region, and language without retrieving every Intent detail;
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
17. one owner-approved bounded Skill produces an exact plan, and a local
    Execution Gate binds its Agreement, input, Skill/model versions, sandbox,
    resources, files, network, credentials, disclosures, writer fence, policy,
    approval and expiry before launch;
18. that Skill executes and delivers without exceeding its authorization;
19. one trusted low-risk run records either verified Gift/direct payment or an
   honest unpaid outcome;
20. the Portfolio Ledger reconciles actual cost and settlement evidence
    without calling expected value revenue;
21. restart, writer takeover, and exact retry create no duplicate contact,
    Agreement, execution, Gift, transfer, or settlement action;
22. pause and drain work at source, publication, contact, scheduler, Skill,
    adapter, and global scope;
23. the entire MVP works with TOS escrow support disabled; and
24. if TOS escrow is demonstrated, it separately passes every specialized
    profile gate.

Two independent carriers are required before claiming resilient decentralized
public availability. They are not required before first contact about one
verified signed Intent.

Continuous autonomous business is a later acceptance claim. It additionally
requires:

1. OpenFox publishes, revises, and withdraws its own service Intents under
   exact writer-fenced actions and bounded posting, reply, audience, disclosure,
   TTL, active-post, and Carrier policy;
2. dynamic pricing uses current cost, capacity, risk and verified outcome
   evidence while deterministic policy enforces margin, discount, exposure and
   revision-change limits;
3. multiple Engagements are scheduled without deadline, reservation, priority,
   preemption, or aggregate-exposure violations;
4. every invoice, milestone, installment, period and accumulated balance has a
   distinct Agreement-bound obligation, stable action ID and evidence state;
5. customer, supplier and subcontractor searches reuse the same Intent profile,
   while each resulting relationship has a separate Agreement, disclosure,
   reservation, execution and settlement boundary;
6. losing one Carrier does not prevent already replicated publications from
   being discovered, resolved, revised through another Carrier, or withdrawn
   directly with the issuer; and
7. verified results improve measured matching, pricing or profitability without
   automatically expanding authority or hiding adverse outcomes.

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
13. Which publication audiences, posting/reply limits, price-change bounds and
    owner approvals are safe for the first autonomous service offer?
14. Which credential broker and sandbox enforce exact Skill/task/domain/
    destination handles for the local Execution Gate?
15. Which scheduling and subcontracting policy governs deadlines, preemption,
    downstream disclosure and aggregate failure exposure?
16. Which settlement adapters support milestones or bounded periodic
    obligations, and what exact evidence closes each obligation?

Until these decisions are frozen and tested, OpenFox may implement the
read-only scout. Autonomous publication, contact, Agreement, scheduling,
execution, billing, Gift, transfer, escrow, and external settlement must be
enabled one bounded phase at a time.
