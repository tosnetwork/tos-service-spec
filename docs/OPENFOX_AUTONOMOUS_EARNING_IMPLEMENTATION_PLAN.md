# OpenFox Autonomous Earning — Operation-Composed Implementation Plan

## Status

- Document type: OpenFox application design and delivery plan
- Status: proposed; implementation and acceptance pending
- Target repository: `tosnetwork/openfox`
- Root architecture:
  [`TOS_AGENTIC_INTERNET_OPERATION_ARCHITECTURE_V1.md`](TOS_AGENTIC_INTERNET_OPERATION_ARCHITECTURE_V1.md)
- Primary specification:
  [`AGENT_INTENT_EXCHANGE_V1.md`](AGENT_INTENT_EXCHANGE_V1.md)
- Semantic side-effect identity:
  [`SEMANTIC_ACTION_IDENTITY_V1.md`](SEMANTIC_ACTION_IDENTITY_V1.md)
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
> resources, estimates profit and risk, negotiates exact obligations and their
> settlement adapters with other Agents, satisfies profile-qualified
> authorization predicates, performs
> agreed work through approved skills, advertises bounded services, schedules a
> portfolio of obligations, and learns from verified outcomes.

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
  -> Settlement Selector chooses an adapter for each value-bearing obligation
  -> Agreement Compiler freezes exact obligations and authorization predicates
  -> validate adapter prerequisites
  -> Portfolio Ledger atomically reserves aggregate resources and exposure
  -> prove required prepayment or finalized escrow funding
  -> Skill/Execution Gate performs and delivers approved work
  -> resolve each obligation through its selected adapter
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
| Optional settlement | No common adapter boundary selects Agreement-bound direct transfer, TOS escrow, or external settlement per obligation without changing the Intent or Agreement objects. |
| Generic execution dispatch | The passive provider path is pinned to a narrow software profile rather than a locally selected approved skill. |
| Local execution authorization | No common OpenFox Gate binds every Skill plan to exact files, domains, credentials, resources, disclosure, policy, approval, writer fence, and expiry. |
| Autonomous supply | No durable loop safely publishes, reprices, revises, or withdraws OpenFox's own service Intents. |
| Portfolio scheduling and subcontracting | Concurrency limits do not yet define deadline-, priority-, dependency- and exposure-aware scheduling or separate downstream Agreements. |
| Milestone and periodic billing | No generic obligation sequence reconciles invoices, installments, partial payments, accumulated balances, and bounded recurring mandates. |
| Business accounting | Gift gratuity, unsecured receivable, external payment, escrowed receivable, cost, nonpayment, and settled revenue are not reconciled under evidence classes. |
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

### 4.5 Select settlement after negotiation and before acceptance

Settlement is chosen after negotiation:

- `none` for explicitly unpaid collaboration, which may later receive an
  unrelated Gift gratuity;
- `agreement-direct-transfer` for simple Agreement-bound payment without
  escrow, including intentionally unsecured post-delivery payment;
- `tos-escrow` for a supported high-assurance TOS profile;
- `external` for explicitly non-TOS systems.

No settlement mode is a prerequisite for discovering or discussing an Intent.
Every value-bearing obligation selects and validates its mode before the
Agreement is accepted and before dependent reservation or execution.

### 4.6 Preserve strict optional profiles

When `tos-escrow` is selected, OpenFox must satisfy the complete Quote,
escrow, Gate, execution, Receipt, release/refund, custody, and recovery profile.
Generic chat or an Intent digest cannot fill missing authority.

The complexity of an untrusted escrowed purchase remains inside that adapter.
It does not infect trusted or conversational paths.

### 4.7 Make side effects durable and idempotent

Every contact, Agreement action, reservation, execution, delivery, Gift,
transfer, escrow, and settlement-resolution operation has a stable semantic
action ID derived under the released `SemanticActionIdentityV1` registry: one
frozen, domain-separated digest formula per action kind over the complete
semantic key of exact participant and object identity plus terms. Any writer —
including a retry path or a takeover writer — recomputes the identical ID for
the same semantic side effect.

Retry attempt, source cursor, model turn, wall time, transport session, and
writer generation are forbidden identity inputs and do not create new economic
identities.

The normative registry is not implementation-local. Exact V1 framing, SHA-256
formulas, ordered fields for every action kind, authority-issued repeatable
instances, terminal successors, execution lineage, and exact-byte vectors are
defined by
[`SEMANTIC_ACTION_IDENTITY_V1.md`](SEMANTIC_ACTION_IDENTITY_V1.md). OpenFox
generates code or data tables from that registry and refuses unknown or locally
modified entries.

## 5. Proposed package boundary

The package layout is illustrative. Existing packages should be reused when
their semantics match exactly.

```text
pkg/earning/
  coordinator.go      # observe -> evaluate -> negotiate -> agree -> prepare -> execute -> resolve
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
  gift.go             # gratuity/other-income integration; not settlement
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
}

type ContentResolver interface {
    ResolveContent(
        ctx context.Context,
        descriptor ContentDescriptor,
        policy ContentRetrievalPolicyV1,
        budget RetrievalBudget,
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
manifest, and selected attachments go through a configured `ContentResolver`
and the generic retrieval security profile before they must match their signed
size and digest. A raw `retrieval_hint` is never passed to a general HTTP client
or model-selected tool. Search may be
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
        action AuthorizedActionV1,
    ) (PublicationResult, error)
    Reply(
        ctx context.Context,
        action AuthorizedActionV1,
    ) (PublicationResult, error)
    Revise(
        ctx context.Context,
        action AuthorizedActionV1,
    ) (PublicationResult, error)
    Withdraw(
        ctx context.Context,
        action AuthorizedActionV1,
    ) (PublicationResult, error)
    ResolveAction(
        ctx context.Context,
        actionID ActionID,
        requestDigest Digest,
    ) (ActionResolution, error)
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
    Snapshot(
        ctx context.Context,
        owner OwnerID,
        agent AgentID,
        barrier ConsistencyBarrier,
    ) (InventorySnapshot, error)
}

type InventorySnapshot struct {
    Revision       uint64
    CreatedAt      Timestamp
    ExpiresAt      Timestamp
    SourceGeneration uint64
    PortfolioRevision uint64
    PolicyRevision PolicyRevision
    ConsistencyToken Digest
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

type InventoryItemState struct {
    ItemID               ItemID
    AuthorityDigest      Digest
    State                AvailabilityState
    ExpiresAt            Timestamp
    RevocationGeneration uint64
    EvidenceRefs         []EvidenceRef
}
```

Every Skill, model, tool, credential, wallet, asset, capacity, and cost entry
includes `InventoryItemState`. The snapshot is local, versioned, owner-scoped,
and consistent with the named writer, portfolio, and policy barrier. Remote
content cannot add a Skill, mark a credential available, change a cost, or
release a reservation.

An informational contact policy may accept a longer configured freshness
window. Agreement validation, reservation, publication pricing, settlement
preparation, and Gate authorization require a new non-expired snapshot under
the same admission barrier. If heterogeneous sources cannot produce one atomic
snapshot, the final admission transaction revalidates every referenced item,
revocation generation, portfolio revision, and consistency token before it
linearizes the action. A mismatch restarts evaluation; it never falls back to a
stale estimate.

### 6.4 Conversation transport

```go
type ConversationTransport interface {
    EnsureDirect(
        ctx context.Context,
        action AuthorizedActionV1,
        issuer AgentID,
    ) (Conversation, error)
    Send(
        ctx context.Context,
        conversation ConversationID,
        action AuthorizedActionV1,
        message Message,
    ) (SendResult, error)
    Subscribe(ctx context.Context, cursor Cursor, limit uint32) (MessageBatch, error)
    ResolveAction(
        ctx context.Context,
        actionID ActionID,
        requestDigest Digest,
    ) (ActionResolution, error)
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
        proposedBody AgentAgreementBodyV1,
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
attachment digests and a canonical graph of `AgreementObligationV1` records.
Each obligation binds its obligor, beneficiary, dependencies, subject,
deliverables or consideration, exact asset and amount when applicable, schedule,
acceptance evidence, confidentiality, cancellation, dispute and billing terms,
settlement adapter, authorization-predicate references, and expiry. The
compiler derives each mandatory typed predicate from semantics — always the
obligor; the payer or custody principal for a value transfer; the refunding
custody principal for a refund; and the authority owner for private data,
credential, key, or capability disclosure. Proposer-added authorizers become
additional canonical predicates and can only strengthen the body.

Every predicate freezes subject kind/namespace/id, role and obligation scope,
evidence profile URI/version/descriptor digest, validity, and the target
projection digest derived from the Agreement core and complete authorization-
policy digest under the non-circular formula in
`AGENT_INTENT_EXCHANGE_V1.md`. The final body digest
covers all recomputed targets. Business-specific meaning remains in exact terms
or namespaced extensions. The compiler rejects duplicate or missing predicates,
cycles, wrong scope, profile substitution, projection mismatch, ambiguous value,
missing Adapter fields, omitted mandatory subjects, or any body that lets the
proposer authorize another subject. It cannot sign, reserve, execute, or settle;
those remain separate authorized actions.

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
        ticket StartTicket,
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
    PrepareExecution(
        ctx context.Context,
        action AuthorizedActionV1,
        agreement Agreement,
        plan ExecutionPlan,
        reservation Reservation,
        policyRevision PolicyRevision,
    ) (PreparedExecution, error)
    StartExecution(
        ctx context.Context,
        action AuthorizedActionV1,
        prepared PreparedExecution,
    ) (StartTicket, error)
    ResolveExecution(
        ctx context.Context,
        slot ExecutionSlotID,
    ) (ExecutionResolution, error)
}
```

This is OpenFox's local gate for every Skill, not the optional TOS Native
Execution Gate used by an escrow profile. `PreparedExecution` binds exact
Agreement, plan and input digests; Skill and model versions; sandbox; allowed
files and directories; network domains and destinations; task-scoped credential
handles; CPU, memory, storage, accelerator, token, time and spend budgets;
allowed disclosures and uploads; destructive-operation flags; reservation;
writer fencing generation; owner approval evidence; policy revision; and
expiry.

The Gate creates one unique execution slot for `(agent_id,
agreement_body_digest, execution_id)`. `execution_id` is not chosen by the
runner, model, or retry path. It uses the exact `execution.slot` registry entry
over owner, Agent, Agreement body digest, execution-bearing obligation,
canonical plan, accepted input manifest, authority-allocated attempt index, and
predecessor terminal-resolution digest. Attempt zero uses index zero and the
zero digest. Timeout, crash, partition, lease loss, and `AMBIGUOUS_START` are
nonterminal and recompute the identical slot. Only a permitted durable
`FAILED`, `CANCELLED`, or `KILLED` result can atomically allocate index `n+1`
with that predecessor resolution; `SUCCEEDED` has no replacement.
`PrepareExecution` may create only
`PREPARED`. `StartExecution` is the single linearization point: under the action
admission transaction it revalidates writer high-water, Agreement, plan, input,
reservation, policy, credentials and approval, then atomically moves
`PREPARED -> STARTING` and returns a short-lived `start_not_after` one-shot
ticket. The runner consumes that ticket once and records `RUNNING`; a crash in
`STARTING` becomes `AMBIGUOUS_START` and must be reconciled, never automatically
re-authorized. Terminal states are `SUCCEEDED`, `FAILED`, `CANCELLED`, or
`KILLED`. A new writer cannot create another slot for the same exact
execution, because it derives the same `execution_id`.

File access uses pre-opened no-follow directory/file capabilities bound to
stable file identity and, where immutability is required, exact content digest.
Path re-resolution, symlink traversal, rename substitution, device files, and
mount escape fail closed. Network access is mediated for every connection by a
task broker that binds allowed scheme, hostname, resolved IP class, port, TLS
SNI/certificate policy, proxy, redirect and retry rules. DNS and redirects are
rechecked at each hop. Credential capabilities are immutable, purpose-limited,
bound to action, Skill, task, domain and destination, and cannot be exchanged
for a broader ambient token.

Every upload, new outbound connection, credential use, value transfer, or
destructive operation passes through the same task broker after process start;
the runner cannot rely only on a preflight check. If writer generation is
superseded while running, the default is `DRAIN_NO_NEW_EFFECTS`: pure local
computation may checkpoint, but the broker denies every new external or
destructive effect. Owner policy may choose immediate kill for a profile known
to be safely killable. Existing effects already linearized before takeover may
finish and are reconciled by their action IDs. A successful Gate decision does
not prove correct work or authorize payment.

### 6.9 Engagement scheduler

```go
type EngagementScheduler interface {
    Propose(
        ctx context.Context,
        inventory InventorySnapshot,
        portfolio PortfolioSnapshot,
        engagements []SchedulableEngagement,
    ) (ScheduleDecision, error)
    Admit(
        ctx context.Context,
        action AuthorizedActionV1,
        entry EngagementScheduleEntryV1,
    ) (EngagementScheduleEntryV1, error)
    RequestTransition(
        ctx context.Context,
        action AuthorizedActionV1,
        entryID ScheduleEntryID,
        expectedRevision uint64,
        target ScheduleState,
    ) (EngagementScheduleEntryV1, error)
    ResolveEntry(
        ctx context.Context,
        entryID ScheduleEntryID,
    ) (EngagementScheduleEntryV1, error)
}
```

Scheduling considers Agreement deadlines, expected profit, risk, priority,
resource compatibility, setup cost, fairness, dependencies, cancellation cost,
and settlement exposure. It may delay or recommend rejection, but it cannot
invent capacity, exceed reservations, or preempt irreversible work. Every
admission, dispatch, cancellation, or preemption transition requires an exact
`AuthorizedActionV1`; dispatch also requires a fresh Execution Gate
authorization. `Propose` has no authority by itself.

The durable scheduler projection is:

```text
EngagementScheduleEntryV1 {
  schedule_entry_id
  agreement_body_digest
  execution_id
  writer_generation
  dispatch_generation
  state                    # queued, reserved, dispatched, starting, running,
                           # preempt_requested, cancel_requested, ambiguous,
                           # completed, failed, cancelled
  priority
  not_before
  deadline
  reservation_digest
  resource_and_exposure_digest
  dependency_ids[]
  cancel_class
  preempt_class
  irreversible_boundary
  downstream_agreement_digests[]
  state_revision
  evidence_refs[]
}

PortfolioDependencyV1 {
  dependency_id
  upstream_agreement_digest
  upstream_obligation_id
  downstream_agreement_digest
  downstream_obligation_id
  dependency_type
  dependency_class         # blocking | informational
  failure_propagation_policy
  disclosure_policy_digest
  reserved_loss_exposure
}
```

For each owner Portfolio, the `blocking` cross-Agreement dependencies form one
versioned graph that must remain acyclic, exactly as obligations must inside a
single Agreement. Admitting a new blocking edge — or a schedule entry carrying
`dependency_ids` — is itself an `AuthorizedActionV1` whose cycle check and
insertion execute inside the same linearized Portfolio admission transaction,
so two writers cannot concurrently admit `A depends on B` and `B depends on
A`. An edge that would create a cycle is rejected before any reservation or
risk reserve is taken. `informational` edges never block dispatch and are
excluded from the cycle rule. Recovery and takeover revalidate acyclicity
before dispatching, and cancellation, timeout, or failure of an Agreement
removes its blocking edges under the recorded propagation policy so dependent
entries resolve instead of deadlocking.

Only an `AuthorizedActionV1` with the current writer generation can linearize a
dispatch, cancellation, or preemption transition. A takeover increments
`dispatch_generation`, reconstructs durable entries, and reconciles
`dispatched`, `starting`, `running`, and `ambiguous` entries before dispatching
replacement work. Crossing an irreversible boundary disables automatic
preemption. Cancellation of an upstream Agreement does not silently cancel a
downstream Agreement; its accepted cancellation policy and dependency event are
applied separately.

A downstream completion, failure, delay, dispute, cancellation, or payment
event atomically updates the dependency projection, deadline risk, reserved
loss, refund exposure, and Portfolio evidence before a new scheduling decision.
It never copies private input, authority, execution evidence, or settlement
state between Agreements.

### 6.10 Settlement adapter

```go
type SettlementAdapter interface {
    Prepare(
        ctx context.Context,
        agreement Agreement,
        obligation SettlementObligationV1,
    ) (PreparedSettlement, error)
    Request(ctx context.Context, action AuthorizedActionV1) (Attempt, error)
    Resolve(ctx context.Context, reference SettlementRef) (SettlementEvidence, error)
    ResolveAction(
        ctx context.Context,
        actionID ActionID,
        requestDigest Digest,
    ) (ActionResolution, error)
}
```

Adapters expose a shared operational shape but preserve their own guarantees.
No generic method claims that all external settlement is atomic or finalized.
`SettlementObligationV1` is the canonical projection defined by the Intent
specification. It identifies an exact deposit, milestone, installment, period,
final balance, refund, or other Agreement-bound obligation and state. Each
request has its own stable action ID and evidence; a schedule is not unlimited
recurring payment authority.

### 6.11 Portfolio ledger and writer fencing

```go
type PortfolioLedger interface {
    Snapshot(ctx context.Context, owner OwnerID, agent AgentID) (PortfolioSnapshot, error)
    Reserve(ctx context.Context, action AuthorizedActionV1, reservation Reservation) (ReservationResult, error)
    ApplyEvidence(ctx context.Context, action AuthorizedActionV1, evidence Evidence) error
    Reconcile(ctx context.Context, action AuthorizedActionV1, scope ReconcileScope, apply bool) (ReconcileResult, error)
}

type WriterLease interface {
    Acquire(ctx context.Context, owner OwnerID, agent AgentID, instance InstanceID) (WriterFence, error)
    Renew(ctx context.Context, fence WriterFence) (WriterFence, error)
    Release(ctx context.Context, fence WriterFence) error
}
```

`WriterFence` is the typed lease proof:

```text
WriterFenceV1 {
  owner_id
  agent_id
  instance_id
  lease_id
  writer_generation
  issued_at
  expires_at
  authority_id
  scope
  fence_proof              # authority-issued unforgeable MAC or signature
}
```

`writer_generation` increases monotonically per owner/Agent, but a bare
integer carries no authority: a fence is valid only while its `fence_proof`
verifies as issued by the owner's Action Authority over every field above, is
unexpired, and covers the scope of the attempted action. A process mutex is
required even for single-process deployments but does not replace
cross-process or cross-host fencing.

### 6.12 Unified economic action admission

Every externally visible or exposure-changing side effect uses the same frozen
authorization envelope:

```text
AuthorizedActionV1 {
  owner_id
  agent_id
  action_kind
  stable_action_id
  exact_request_digest
  writer_generation
  writer_fence_digest
  policy_revision
  mandate_digest
  approval_digest?
  expected_prior_state
  expires_at
}

ActionResolutionV1 {
  stable_action_id
  exact_request_digest
  state                    # unknown, prepared, submitted, accepted,
                           # rejected, conflict, terminal
  sink_reference?
  evidence_refs[]
  state_revision
}
```

Publication, public reply, contact, Proposal, Agreement acceptance, reservation,
schedule dispatch, Gate preparation/start, delivery, disclosure, upload,
credential issuance, Gift, transfer, escrow, billing, settlement, reservation
release, and applied reconciliation each use an appropriate `action_kind`.
Typed wrappers may add fields but must embed the exact common envelope.

`stable_action_id` for every kind is derived under the frozen
`SemanticActionIdentityV1` registry described in §4.7, so no caller, model, or
retry path can mint a fresh identity for an existing semantic side effect.

For each owner/Agent, every sink either participates directly in one
linearizable, rollback-resistant action-admission domain or is reachable only
through a broker that does. Admission atomically:

1. verifies the `WriterFenceV1` referenced by `writer_fence_digest` — proof,
   owner/Agent binding, scope, and expiry — and on a shared endpoint binds the
   authenticated caller principal to that fence; a bare or forged generation
   integer is rejected regardless of its value;
2. rejects a fence generation lower than the stored high-water generation;
3. advances the high-water generation only when the lease authority has
   confirmed a completed acquire or takeover for that owner/Agent, never from
   a future integer carried by an ordinary action request;
4. resolves and validates mandate and approval content, scope, revision, and
   expiry — digest comparison alone is insufficient;
5. creates `(stable_action_id, exact_request_digest)` once against the expected
   prior state; and
6. returns the durable existing resolution for an exact retry or `conflict` for
   the same ID with different bytes.

Messenger outboxes, custody, Carrier publishers, credential brokers, local
executors, Portfolio storage, and settlement adapters must enforce this rule.
If an external system cannot enforce fencing, its credential is held only by
the fenced broker; stale processes have no alternate session, token, key, or
network route that can create the economic side effect directly.

Timeout or crash recovery calls `ResolveAction(stable_action_id,
exact_request_digest)`. `unknown` may retry the same exact action under policy;
`prepared`, `submitted`, or `accepted` is ambiguous or in progress and never
creates a new semantic action. An action linearized before a writer loses its
lease may reach its defined terminal state. After the high-water generation
advances, that writer cannot linearize a new action, including a release or
compensating action.

V1 defines two deployment profiles. `personal-single-host` uses one local
Owner Economic Action Authority with an exclusive process lock and durable
transactional store; every side-effect credential and outbox is owned by that
authority, not worker processes. `shared-multi-host` uses one owner-operated
strongly consistent Action Authority endpoint shared by all hosts, while
custody independently persists and rejects lower generations. The endpoint is
not a global market database: it stores only one owner's private safety state.
Loss of the authority stops new actions; it never falls back to per-process
journals. A backend is eligible only after linearizability, crash, rollback,
partition, stale-client, and custody-high-water conformance tests.

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
- recommended response and settlement adapter for each value-bearing
  obligation; and
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

- exact participants and roles;
- referenced Intent revisions;
- bounded exact terms and content-addressed attachments;
- a canonical acyclic graph of exact `AgreementObligationV1` records;
- per-obligation obligor, beneficiary, dependencies, subject, asset/amount,
  schedule, evidence, disclosure, cancellation, dispute, billing and settlement
  parameters;
- selected execution/delivery assumptions; and
- validity, predecessor, complete body-bound authorization predicates, and
  profile-qualified evidence state.

Conversation text and transcript digests remain evidence only. OpenFox sends a
typed `AGREEMENT/PROPOSE` action. Each canonical predicate already selects its
released evidence profile URI/version/descriptor digest. Generic off-chain
predicates use one typed `AGREEMENT/ACCEPT` per subject over that subject's
complete predicate and target set. A chain-bound Paid Demand predicate instead
uses its exact signed Provider Offer or finalized buyer-wallet on-chain
`accept`; its Quote binding commits the final generic Agreement body digest and
scoped obligation/predicate/target lists. It neither requires nor accepts
duplicate generic evidence. Mixed-profile obligations share one Agreement
without a later message selecting or weakening a profile. No local projection
becomes `AGREED` until every body-bound predicate has matching evidence.

### 7.5 Engagement

An `Engagement` is the local durable projection of one exact Agreement. It is
not limited to labor and may represent a service, sale, exchange, delivery, or
collaboration.

```text
AGREED
  -> SETTLEMENT_PREPARING
  -> READY_TO_RESERVE
  -> RESOURCE_RESERVED
  -> FUNDING_REQUIRED | UNSECURED_APPROVED | READY
  -> FUNDED | READY
  -> EXECUTION_PREPARED
  -> EXECUTION_STARTING
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
       -> AGREEMENT_ACCEPTING
       -> AGREED
       -> SETTLEMENT_PREPARING
       -> READY_TO_RESERVE
       -> RESOURCE_RESERVED
       -> FUNDING_REQUIRED | UNSECURED_APPROVED | READY
       -> FUNDED | READY
       -> EXECUTION_PREPARED
       -> EXECUTION_STARTING | EXECUTION_AMBIGUOUS
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
conversation. The model explains it; deterministic code validates the canonical
obligation graph, participants, terms and attachment digests, exact values,
dependencies, billing, per-obligation settlement adapters, resources, policy,
and the complete body-bound authorization-predicate set. It recomputes the
Agreement core digest, full authorization-policy digest, every target projection
and final body digest before any evidence is requested.

Sending `AGREEMENT/PROPOSE` and, where a predicate selects generic typed
evidence, each `AGREEMENT/ACCEPT` are distinct writer-fenced
`AuthorizedActionV1` operations. Every evidence object repeats the exact body
digest, version, subject, profile/version, predicate IDs and target projections.
One generic accepting subject covers its complete predicate set in one object;
partial subsets are not unioned. Changed terms require a new predecessor-bound
version and a complete new profile-qualified evidence set. Ordinary chat, a
transcript digest, a model phrase, read receipt, or stale evidence cannot trigger
promotion. Ambiguous sends are resolved by action ID and request digest before
retry.

## 10. Execution and delivery

### 10.1 Agreement and settlement admission

Execution is ineligible until every body-bound authorization predicate of the
exact `AgentAgreementBodyV1` is satisfied by evidence matching its frozen
subject, profile/version, obligation/role scope, target projection, validity,
and body digest. The coordinator prepares each selected
settlement adapter, validates its exact parameters and prerequisites, and
recomputes economics and worst-case exposure using that adapter's payment,
funding, reversibility, fee, delay, dispute, and nonpayment model.

An obligation requiring prepayment must have accepted finalized payment
evidence before dependent work begins. A TOS escrow obligation must have its
profile-required finalized funding and all Gate prerequisites. An unsecured
direct-payment obligation explicitly reserves nonpayment exposure. Work with no
payment obligation records no receivable; a possible later Gift is not a
settlement prerequisite. Changing settlement adapter, payer, payee, asset,
amount, destination, sequence, funding rule, or release condition requires a
new Agreement version and complete profile-qualified authorization evidence
before a dependent irreversible action.

Adapter validation is read-only and does not move value. The aggregate
Portfolio reservation linearizes first. Only after that reservation succeeds
may custody admit the exact prepayment or escrow-funding action; dependent work
remains blocked until the required finalized funding evidence is resolved.

### 10.2 Reservation

Before work begins, OpenFox reserves the exact plan's resources and worst-case
cost. Reservation is keyed by Agreement and stable action ID. Concurrent
instances cannot exceed shared local or custody-enforced exposure. Reservation
requires the current `AuthorizedActionV1`; the linearizable owner/Agent
Portfolio admission transaction validates its writer generation, policy,
request digest, expected prior state and fresh consistency barrier while it
atomically checks:

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

### 10.3 Skill planning, Gate, and dispatch

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

The Gate prepares the exact slot, then atomically revalidates and moves it to
`STARTING` when issuing the one-shot start ticket. Plan mutation, lost
reservation, stale writer, changed resource identity, or expired policy requires
a new preparation. `STARTING` ambiguity is resolved from the execution journal;
it is never treated as permission to start again.

### 10.4 Delivery

Delivery may use Messenger, content-addressed storage, an authenticated
endpoint, or the selected escrow profile. The delivery record binds exact
Agreement, execution, result, artifact, timestamp, and adapter evidence.

A delivery acknowledgement is not payment unless the settlement mode defines
it as such.

## 11. Settlement adapters

### 11.1 Agent Gift gratuity

OpenFox may perform explicitly unpaid trusted work and later receive an Agent
Gift. Gift V1 remains a non-purchase transfer: it is recorded as gratuity or
other income and cannot close an Agreement obligation, invoice, milestone, or
receivable. A chat reference or matching amount is not a payment binding.

If the parties promise compensation, the Agreement uses an Agreement-bound
direct, external, or escrow adapter. OpenFox never records an “expected Gift” as
a debt or settled Agreement revenue.

### 11.2 Agreement-bound direct transfer

The adapter prepares one exact `AgreementPaymentRequestV1` containing Agreement
digest, obligation ID, payer, payee, asset, amount, destination, adapter, expiry,
and stable action identity. It may support payment before, during, or after work
when the accepted obligation permits that timing.

It does not claim escrow protection or prove work quality. It closes only the
exact obligation whose payment-request digest is bound by independently
resolved transfer evidence; the same evidence cannot close another obligation.

### 11.3 TOS escrow

The adapter is disabled unless the Agreement fits a released TOS profile. It
uses `tos-service-protocol` for canonical construction and verification and
delegates signing to custody.

The fixed-price machine-checkable Paid Demand profile retains its complete
`BuyerHandoffProfile`, Provider authorization, versioned Quote/escrow,
private-input, Execution Gate, deadline, Receipt, release/refund, bounce, and
recovery requirements. These are adapter requirements, not generic Intent
requirements.

Before the Provider signs, OpenFox finalizes the generic Agreement body and its
Paid Demand-scoped authorization predicates. `PaidDemandQuoteBindingBodyV1`
commits the exact `agreement_body_digest`, obligation IDs, predicate IDs, target
projection digests, and profile version. The resolver verifies equality in both
the generic Agreement and native Quote/escrow projections. One chain `accept`
cannot authorize another Agreement or a changed delivery, disclosure,
cancellation, profile, subject, or scope.

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

An accepted `AgreementObligationV1` contains exact `BillingTermsV1`. OpenFox
deterministically projects each due item into the canonical
`SettlementObligationV1` and `SettlementObligationStateV1` defined by the Intent
specification. Deposit, milestone, installment, usage period, final balance,
refund, and accumulated balance share the same sequence, predecessor, amount,
aggregate-cap, adapter, stable-action and evidence rules.

Periodic expansion requires exact start, interval, finite count, end and maximum
aggregate amount. Modification requires a newly profile-authorized Agreement
version and does not rewrite already due or paid instances. Partial payment is
applied only to the exact payment-request digest for one instance; duplicate
evidence is idempotent and conflicting allocation fails closed. Cancellation,
due-time and payment races follow the accepted policy and durable state revision.

A cumulative execution Receipt is valid only when the selected profile defines
how exact completed units and payment are bound; otherwise OpenFox keeps
separate execution evidence and payment requests. No invoice, schedule, model
output, or prior transfer creates unlimited recurring authority.

## 12. Accounting

The ledger distinguishes evidence classes and never equates quoted value with
revenue.

Candidate accounts include:

- estimated consideration;
- Agreement value;
- finalized Gift gratuity or other income, never an Agreement receivable;
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
| Agent Gift | exact finalized destination credit proves gratuity only; closes no Agreement obligation |
| Agreement-bound direct TOS transfer | exact payment-request digest plus independently resolved exact finalized transfer evidence |
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
  action_admission:
    backend: owner-scoped-linearizable-store
    rollback_resistant_generation: true
    require_sink_or_broker_enforcement: true
    resolve_before_retry: true
  inventory:
    max_contact_age_seconds: 300
    max_commitment_age_seconds: 30
    require_portfolio_policy_consistency_barrier: true
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
  content_retrieval:
    allowed_resolver_profiles: [configured-carrier, configured-storage, public-https]
    deny_loopback_linklocal_private_metadata: true
    recheck_dns_and_redirects: true
    allow_ambient_proxy: false
    allow_url_credentials: false
    require_tls_hostname_sni_certificate_binding: true
    max_redirects: 3
    max_connections_per_object: 4
    max_header_bytes: 65536
    max_expanded_bytes_per_object: 8388608
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
    atomic_prepared_to_starting: true
    start_ticket_ttl_seconds: 10
    ambiguous_start_requires_reconcile: true
    writer_loss_policy: drain-no-new-effects
    no_follow_file_capabilities: true
    recheck_dns_redirect_tls_each_connection: true
    deny_unlisted_network_destinations: true
    deny_unlisted_credential_handles: true
    destructive_actions_require_owner_approval: true
  scheduling:
    max_dispatches_per_cycle: 2
    irreversible_work_is_not_preemptible: true
    deadline_miss_requires_replan_or_owner_review: true
  settlement:
    allowed:
      - agreement-direct-transfer
      - tos-escrow
    default_for_unknown_counterparty: tos-escrow
    external_requires_owner_approval: true
  gratuity:
    accept_agent_gifts: true
    never_close_agreement_obligation: true
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
openfox earning inventory consistency
openfox earning portfolio show
openfox earning writer status
openfox earning action inspect <action-id> <request-digest>
openfox earning conversations
openfox earning agreement inspect <agreement-id>
openfox earning engagement list
openfox earning execution inspect <execution-slot-id>
openfox earning schedule entries
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
- Proposals, Agreements, and obligations by selected settlement adapter;
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
  content retrieval policy, canonical Agreement/obligation/acceptance,
  `AuthorizedActionV1`, settlement-obligation state, local Gate/start-ticket,
  scheduler/dependency, and recovery vectors in `tos-service-spec` and
  `tos-service-protocol`;
- freeze coarse modes/classes, taxonomy and region identifier syntax, keyword/
  language rules, capability-hint identifiers, canonical decimal value hints,
  schedule ordering, and all card/detail/attachment bounds;
- decide whether existing opportunity storage can represent generic exact
  operation and Intent identity or needs `pkg/opportunity`;
- build semantically varied fixtures; and
- keep every external action disabled.

Exit: two independent codecs/verifiers agree on the common operation and Intent
payload plus Agreement, obligation, acceptance, action and billing objects;
unrelated goods, services, and asset exchange require no new core opcode or
fields; and a second implementation filters signed cards without retrieving
detail. No side-effect phase starts before this exit is met.

### Phase 1 — read-only Intent scout

- implement bounded card search and subscription, exact verification, and
  source-local cursors;
- compile versioned AI-proposed search profiles under deterministic owner
  policy;
- implement hard card filters, cheap local scoring, issuer/category/value
  diversity quotas, and a bounded exploration bucket;
- retrieve through the generic SSRF/DNS/redirect/TLS/proxy/credential policy,
  then digest-check only shortlisted detail and separately approved public
  attachments;
- add hostile-content isolation;
- expose freshness-, authority-, revocation- and consistency-bound local
  capability/resource inventory;
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

- deploy the linearizable writer-generation and `AuthorizedActionV1` admission
  domain for Messenger and Agreement actions;
- add Intent-referenced first contact through existing Messenger;
- enable bounded open-ended conversation;
- add contact/disclosure/abuse policies;
- implement typed Proposal, body-bound authorization predicates,
  profile-qualified evidence, withdrawal and versioning;
- compile exact generic Agreement candidates from bounded conversation and
  selected content without granting signing authority;
- ensure ordinary chat is non-binding; and
- recover ambiguous send and restart without duplicate Agreement actions.

Exit: two fresh Agents negotiate changed terms, emit generic typed evidence for
one canonical multi-obligation Agreement, reject profile/target substitution,
and recover ambiguous sends through `ResolveAction` without chain settlement or
transcript inference.

### Phase 3 — trusted low-risk work

- enable one reviewed local skill or executor;
- select and validate settlement for each value-bearing obligation;
- reserve resources, worst-case cost, capital and exact unsecured nonpayment
  exposure in the linearizable Portfolio;
- then satisfy required prepayment or finalized funding evidence;
- construct an exact plan and pass the local Execution Gate's one-shot atomic
  start before launch;
- execute, schedule, and deliver under one trusted Agreement;
- record nonpayment exposure;
- optionally request/receive one Agreement-bound direct transfer, or separately
  observe an unrelated Agent Gift gratuity; and
- reconcile paid or unpaid outcome.

Exit: one real low-value job completes without invoking Accepted Quote or
escrow. Nonpayment must be handled as a valid adverse business outcome.

### Phase 4 — policy-gated settlement adapters

- add a common adapter registry;
- enable Agreement-bound direct-transfer modes and separate Gift-gratuity
  accounting;
- project deposits, milestones, installments, periodic obligations, invoices,
  partial payments, cancellation races, conflicts, finite aggregate caps, and
  outstanding balances from canonical state without recurring implicit
  authority;
- add external adapters only with explicit evidence labels and owner approval;
- optionally integrate the released TOS escrow profile; and
- prove disabling any adapter does not disable discovery or negotiation.

Exit: the same Intent/Agreement path selects at least two settlement adapters
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
- URL user information, loopback, link-local, private and metadata addresses,
  alternative IP encodings, DNS rebinding, redirects across origin/address
  class, TLS/SNI mismatch, proxy and credential capture, oversized headers,
  connection fan-out, compression bombs, timeout and retry amplification;
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

- expired snapshot, stale source generation, mismatched portfolio/policy
  revision or consistency token, revoked item generation, and internally
  inconsistent capability inventory;
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

### Authorized actions and sink admission

- every publication, contact, Proposal, acceptance, reservation, dispatch,
  Gate, credential, disclosure, delivery, payment, settlement, release and
  reconciliation sink receiving the exact common action envelope;
- lower, equal and higher writer generations against a rollback-resistant
  high-water mark;
- a forged or replayed fence proof, a future generation without an
  authority-confirmed acquire or takeover, a wrong-owner or out-of-scope
  fence, an expired or stolen lease proof, a rolled-back authority store, and
  a partitioned stale client unable to advance the high-water or admit
  actions;
- mandate or approval digests resolving to changed, out-of-scope, superseded,
  or expired content rejected despite matching digests;
- a timeout, crash, or takeover retry deriving the identical semantic action
  ID, and any attempt to express the same payment, publication, or execution
  under a new ID — including a changed destination wrapper — rejected as a
  distinct unauthorized action;
- exact retry, same action ID with different request digest, wrong expected
  prior state, expired policy/mandate/approval and stale journal;
- `unknown`, `prepared`, `submitted`, `accepted`, `rejected`, `conflict` and
  terminal recovery through `ResolveAction`;
- an action admitted before takeover completing, while the old writer cannot
  admit a new message, compensation, release or retry afterward; and
- external sinks without native fencing accessible only through a broker whose
  scoped credential and network route are unavailable to stale processes.

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
- transcript digest or local UI projection without profile-qualified evidence;
- multi-party and multi-obligation service, deposit/final balance, milestone,
  asset-exchange and refund fixtures using one canonical schema;
- duplicate obligation IDs, missing participant, dependency cycle, ambiguous
  asset/amount, missing adapter field, unknown required extension, and unknown
  optional-extension round trip;
- evidence for wrong body, version, subject, profile/version, role, predicate,
  target projection, obligation set or expiry;
- a proposer omitting the obligor from an obligation's authorizer coverage,
  self-authorizing an obligation that binds another party, substituting the
  payer or custody principal, or omitting the owner of disclosed private data;
- one accepting Agent emitting obligation-subset acceptances that only union
  to coverage, and equivocating bytes under one acceptance identity;
- a chain-accepted Paid Demand Agreement with no generic `AGREEMENT/ACCEPT`
  recognized as accepted, a generic acceptance without the profile's finalized
  chain `accept` never treated as accepted, and a wrong-wallet, wrong-Quote,
  wrong-obligation, wrong-predicate, wrong-target, wrong-profile, or wrong-body
  chain acceptance rejected;
- one finalized Paid Demand chain `accept` replayed against a modified generic
  Agreement, and mixed generic/direct/TOS evidence profiles within one
  Agreement, producing identical accepted state in independent verifiers;
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
- atomic `PREPARED -> STARTING`, one-shot ticket consumption, crash before and
  after start linearization, and `AMBIGUOUS_START` recovery;
- `execution_id` re-derivation: a timeout or takeover recomputing the
  identical slot identity, a runner- or model-chosen novel execution ID
  rejected, and a replacement attempt admitted only through recorded terminal
  lineage;
- every released semantic-action registry entry reproduced from exact-byte
  vectors; mutation of each required field, omitted destination/recipient,
  wrapper substitution, unknown version, caller nonce, same ID/different
  request, ambiguous successor, takeover, and authority-controlled intentional
  repeat cases;
- writer takeover before prepare, between prepare and start, while starting,
  and while running under drain-no-new-effects and kill policies;
- symlink, rename, inode/device/mount substitution, file-digest change, DNS
  rebinding, redirect, proxy, TLS/SNI change, and credential-scope substitution;
- every post-start upload, connection, credential use and destructive action
  rechecked by the task broker;
- bounded failure, cancellation, delivery retry, and duplicate prevention; and
- result delivered without falsely claiming payment.

### Scheduling and subcontracting

- concurrent deadline, priority, dependency, resource, and exposure conflicts;
- starvation, unsafe preemption, lost reservation, stale queue item, and
  irreversible work;
- scheduler output unable to bypass writer fencing or the Execution Gate;
- durable dispatch generation and takeover reconciliation for queued,
  dispatched, starting, running and ambiguous entries;
- concurrent admission of mutually blocking cross-Agreement dependencies,
  cycle formation across subcontract chains, cycle revalidation after restart
  and takeover, and cancellation or timeout removing blocking edges so blocked
  entries resolve;
- upstream cancellation racing downstream irreversible work under independent
  cancellation policies;
- subcontractor unavailable, late, unpaid, malicious, or requesting upstream
  private input; and
- upstream and downstream Agreements, evidence, reservations, and settlement
  remaining distinct under retry and failure.

### Settlement

- trusted work paid and unpaid;
- Gift with a matching conversation, amount or destination unable to close any
  Agreement obligation;
- Agreement-bound direct transfer wrong Agreement, obligation, payer, payee,
  destination, amount, asset, request digest, replay, evidence reuse, or
  ambiguity;
- external evidence labelled below TOS finality;
- unsupported adapter and owner-approval enforcement;
- duplicate, skipped, reordered, partial, overdue, cancelled, or over-limit
  milestone and periodic obligations;
- sequence/predecessor conflict, recurrence without finite count/end/cap,
  concurrent cancellation/payment, partial-payment allocation, evidence reuse,
  Agreement revision after incurred debt, and restart reconstruction;
- a billing schedule unable to create unlimited recurring payment authority;
- cumulative execution evidence not treated as payment without a profile that
  binds both;
- TOS escrow profile's complete independent adversarial matrix; and
- no adapter state substituting for another mode's evidence.

### Accounting and learning

- quoted value never counted as revenue;
- Gift is gratuity/other income and never a receivable or Agreement payment;
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
3. OpenFox builds a fresh, evidence-backed Capability Inventory with created/
   expiry times, source generation, portfolio and policy revisions, consistency
   token, and per-item authority, state, expiry, revocation generation and
   evidence for Skills, models, tools, credentials, wallets, assets, capacity,
   reservations, obligations, costs, and outcomes;
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
8. only shortlisted detail and approved attachments are fetched through a
   configured resolver under SSRF, DNS, redirect, TLS, proxy, credential-origin,
   connection, compressed/expanded-byte and timeout policy, then accepted under
   separate budgets and exact digest/size verification;
9. OpenFox explains search-profile, rejection, shortlist, detail-fetch,
   semantic, capability, resource, profit, and risk decisions;
10. the Economic Evaluator calculates explainable expected net profit and
    risk-adjusted ROI, and deterministic thresholds reject opportunities whose
    costs, payment probability, downside, or confidence are unacceptable;
11. hostile content cannot control tools, credentials, models, routes, policies,
   execution, disclosure, or payment;
12. OpenFox A contacts OpenFox B through authenticated Messenger using an exact
    Intent reference and `AuthorizedActionV1` admitted by the current writer;
13. A and B negotiate natural-language terms that compile into one canonical
    acyclic Agreement body with unambiguous participants and multi-obligation
    deliverable, payment, exchange, billing, evidence, cancellation, dispute,
    disclosure and per-obligation settlement fields;
14. every mandatory and proposer-added canonical predicate freezes its typed
    subject, profile/version/descriptor digest, role/obligation scope, validity
    and recomputed target projection, and matching profile-qualified evidence
    binds the same final body before `AGREED`; mixed profiles converge and chain
    evidence cannot replay to another Agreement;
15. ordinary messages, transcript digests, model phrases, UI projections,
    Gifts, invoices and payment requests cannot create an Agreement or economic
    side effect;
16. one active writer lease and rollback-resistant fencing high-water governs
    all economic actions for the owner/Agent across multiple processes or hosts;
17. every side-effect sink receives the same action ID, request digest,
    verified writer fence, resolved policy, mandate and approval content,
    expected state and expiry, persists conflict-safe resolution, and supports
    query-before-retry; all action kinds and execution attempts reproduce the
    normative registry's exact-byte vectors, controlled repeat allocation and
    terminal-successor rules;
18. compute, spend, capital, receivable risk, and counterparty/global exposure
    are atomically reserved before commitment, and aggregate portfolio limits
    cannot be bypassed by concurrent opportunities;
19. every value-bearing obligation selects its settlement adapter and validates
    exact prerequisites before reservation or execution, and escrow-dependent
    work proves finalized funding first;
20. one owner-approved bounded Skill produces an exact plan, and a local Gate
    creates a unique execution slot binding Agreement, input, Skill/model,
    sandbox, immutable files, mediated network, scoped credentials, disclosure,
    reservation, writer, policy, approval and expiry;
21. atomic `PREPARED -> STARTING`, a short-lived one-shot ticket, durable
    `AMBIGUOUS_START`, and post-start task brokers prevent duplicate start and
    file/network/credential TOCTOU through crash or takeover;
22. that Skill executes and delivers without exceeding its authorization;
23. one trusted low-risk run records either an Agreement-bound direct payment,
    an honest unpaid receivable, or explicitly unpaid work; a finalized Gift is
    separate gratuity and closes no obligation;
24. canonical billing state reconstructs sequence, predecessor, finite
    recurrence, aggregate cap, partial payment, cancellation, conflict and
    evidence without heuristic allocation;
25. the Portfolio Ledger reconciles actual cost and settlement evidence
    without calling expected value revenue;
26. restart, writer takeover, and exact retry create no duplicate contact,
    Agreement, execution, Gift, transfer, or settlement action;
27. pause and drain work at source, publication, contact, scheduler, Skill,
    adapter, and global scope;
28. the entire MVP works with TOS escrow support disabled; and
29. if TOS escrow is demonstrated, it separately passes every specialized
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
3. multiple Engagements use durable schedule entries, dispatch generations and
   dependency records, and survive cancellation, ambiguous start, takeover and
   downstream failure without deadline, reservation, priority, unsafe
   preemption, irreversible-work or aggregate-exposure violations;
4. every invoice, milestone, installment, period and accumulated balance has a
   distinct Agreement-bound obligation, finite sequence/cap, stable action ID,
   conflict rule, partial-payment allocation and evidence state;
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
3. Which existing OpenFox Skill is safe and useful for the first low-value
   trusted run?
4. Which Agreement-bound direct-payment adapter should be demonstrated first,
   and should Gift gratuity be demonstrated separately?
5. How should external asset descriptions and price observations be normalized
   locally without becoming protocol authority?
6. What retention and disclosure defaults apply to public Intent and private
   negotiation content?
7. Which evidence class permits counterparty trust calibration?
8. When does value at risk require owner approval or TOS escrow?
9. Which concrete backend is the first released implementation of the
   single-host and shared multi-host Action Authority conformance profiles?
10. Which reservation dimensions and evidence release each class of aggregate
    portfolio exposure?
11. Which publication audiences, posting/reply limits, price-change bounds and
    owner approvals are safe for the first autonomous service offer?
12. Which credential broker and sandbox implementation satisfies the frozen
    immutable-handle and task-scoped effect-broker contract for exact
    Skill/task/domain/destination scopes?
13. Which released settlement adapter first implements the canonical finite
    milestone or periodic obligation profile?

Until these decisions are frozen and tested, OpenFox may implement the
read-only scout. Autonomous publication, contact, Agreement, scheduling,
execution, billing, Gift, transfer, escrow, and external settlement must be
enabled one bounded phase at a time.
