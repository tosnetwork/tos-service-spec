# OpenFox Autonomous Earning Roadmap

**Status:** reference implementation completed through the local three-node
acceptance profile; public-testnet, cross-host, independent-operator, and
production acceptance evidence remain separate release gates

**Root architecture:**
[`TOS_AGENTIC_INTERNET_OPERATION_ARCHITECTURE_V1.md`](TOS_AGENTIC_INTERNET_OPERATION_ARCHITECTURE_V1.md)

**Intent and Agreement profile:**
[`AGENT_INTENT_EXCHANGE_V1.md`](AGENT_INTENT_EXCHANGE_V1.md)

**Semantic side-effect identity:**
[`SEMANTIC_ACTION_IDENTITY_V1.md`](SEMANTIC_ACTION_IDENTITY_V1.md)

**Trusted capability and owner control extension:**
[`AGENT_TRUSTED_CAPABILITY_AND_OWNER_CONTROL_V1.md`](AGENT_TRUSTED_CAPABILITY_AND_OWNER_CONTROL_V1.md)

**Cross-repository architecture:**
[`OPENFOX_AUTONOMOUS_EARNING_CROSS_REPOSITORY_DESIGN.md`](OPENFOX_AUTONOMOUS_EARNING_CROSS_REPOSITORY_DESIGN.md)

**OpenFox implementation plan:**
[`OPENFOX_AUTONOMOUS_EARNING_IMPLEMENTATION_PLAN.md`](OPENFOX_AUTONOMOUS_EARNING_IMPLEMENTATION_PLAN.md)

**Executable local acceptance campaign:**
[`../scripts/run-openfox-autonomous-earning-three-node.sh`](../scripts/run-openfox-autonomous-earning-three-node.sh)

### Implementation snapshot

The reference implementation now exists across all seven repositories. It
includes the independent specification verifier and frozen vectors; production
protocol codecs and authority checks; two separately implemented Carrier
stores; OpenFox discovery, evaluation, negotiation, Agreement, Portfolio,
scheduling, private handoff, Gate, execution, billing, settlement,
reconciliation, publication and learning components; Messenger typed economic
actions with sink-side fencing; executor ingress and Gate enforcement; custody
action admission; and the released TOS Paid Demand V2 escrow profile.

The local acceptance profile uses three independently queried TOS nodes and two
OpenFox economic authorities. It exercises a signed provider Intent, exact
Agreement compilation, mixed generic/native authorization, a real Native
Agent and task Capability, buyer acceptance and stablecoin funding, finalized
escrow observation, private execution admission, bounded work and delivery,
Receipt-authorized release, and exact provider-wallet credit. It also removes
one Carrier's complete database and proves recovery through the other Carrier
before and after restart.

This snapshot means the design is implemented and locally testable. It does
not collapse the stricter production gates below: a same-host three-node run
cannot prove independent operators, cross-host partition safety, public-testnet
behavior, or an external security acceptance. Those claims require their own
content-addressed evidence and do not justify weakening or bypassing a runtime
Gate.

The completed economic loop does not imply trusted autonomous capability
acquisition or a portable owner control plane. Those follow-on contracts are
defined by Agent Trusted Capability and Owner Control V1. Until its separate
phases pass, consequential self-evolution remains limited to `observe` or
quarantined `draft`, inherited executable capabilities receive no invented
trust, and Web/mobile control cannot claim shared replay-safe mutation
authority.

## 1. Purpose

This roadmap identifies the repositories and staged changes required for
OpenFox to discover economic opportunities, evaluate profitability, negotiate
with another Agent, accept an exact Agreement, perform approved work, resolve
payment, account for the result, and improve from verified evidence.

The architecture is operation-composed. It does not introduce a new protocol
interface, state machine, or contract for each profession, asset, product, or
task category. New business behavior normally enters through signed Intent
content, an optional namespaced profile, a Skill, or an execution or settlement
Adapter.

### 1.1 Normative economic lifecycle

Every implementation preserves this order, although a deployment may stop
after any read-only or non-binding step:

```text
discover bounded signed summaries
-> verify issuer, revision, admission and retrieval constraints
-> retrieve selected exact content
-> compare against fresh Inventory and Portfolio state
-> estimate feasibility, profit, risk and settlement strength
-> admit writer-fenced contact and negotiate through Messenger
-> select exact obligations, settlement Adapters and per-predicate evidence profiles
-> compile one canonical Agreement body
-> satisfy every profile-qualified authorization predicate
-> validate Adapter prerequisites and atomically reserve aggregate exposure
-> prove required prepayment or finalized escrow funding
-> accept immutable private input through the selected handoff profile
-> atomically admit one execution slot and perform bounded work
-> deliver, instantiate due obligations and resolve each selected Adapter
-> reconcile verified cost, payment, nonpayment and release evidence
-> update bounded learning, publication and pricing proposals
```

Discovery, ranking, conversation, invoices, model output and UI state are not
authorization. Settlement is fixed per value-bearing obligation before
Agreement acceptance, reservation or execution. A change to an accepted
participant, obligation, authorizer, settlement parameter, disclosure,
execution input or other authority-bearing term creates a predecessor-bound
Agreement version and repeats the applicable acceptance, admission, reservation
and Gate checks before any new irreversible effect. Timeout or missing evidence
creates an unresolved state; it never implies success, payment, cancellation or
permission to retry under a new identity.

The reference production deployment touches seven repositories when `tosctl`
and custody are part of the `tos` codebase:

1. `tos-service-spec`;
2. `tos-service-protocol`;
3. `openfox`;
4. `tos-messenger`;
5. `tos-service-gateway`;
6. `tos-ai` or another selected executor; and
7. `tos`, including custody or `tosctl` functionality.

The reference deployment makes two ownership decisions:

- `openfox` owns the Owner Economic Action Authority and aggregate Portfolio
  service. The personal profile embeds it in one local daemon and durable
  transaction store. The shared profile runs the same owner-scoped control
  plane against a strongly consistent backend reachable by every authorized
  OpenFox host. Custody independently persists its writer-generation high-water
  mark and never trusts the model process; and
- `tos-service-spec` owns a standalone conformance reference verifier that does
  not import `tos-service-protocol`, its generated code, or its canonicalization
  implementation. `tos-service-protocol` is the production SDK implementation.

If custody or `tosctl`, the shared Action Authority, the independent verifier,
the second Carrier, or the selected executor is maintained in a separate
repository, the count increases accordingly. Repository count is a deployment
result, not a protocol invariant. A smaller phase deliberately modifies fewer
repositories.

## 2. Delivery-size decision

| Outcome | Minimum repository scope | What it proves |
|---|---|---|
| protocol fixtures | `tos-service-spec`, `tos-service-protocol` | two implementations agree on exact objects, digests, errors, and recovery rules |
| read-only scout | protocol fixtures, `openfox`, one Carrier | OpenFox can safely find and evaluate signed Intents without external side effects |
| negotiated Agreement | read-only foundation, `tos-messenger`, the `openfox` Owner Economic Action Authority | Agents can contact, negotiate, and satisfy every body-bound mandatory and proposer-added authorization predicate through its frozen evidence profile without requiring chain settlement |
| trusted low-risk earning | negotiated Agreement, one executor, one selected payment Adapter if payment is promised | one bounded Agreement can be executed and honestly resolved as paid or unpaid |
| resilient public discovery | trusted foundation plus a second independent Carrier | loss of one Carrier or its database does not remove public discovery availability |
| optional TOS escrow | protocol, OpenFox, selected executor/Gate, `tos` and custody | untrusted counterparties can choose finalized funding and the released escrow lifecycle |
| continuous autonomous business | full OpenFox Portfolio, publication, scheduling, billing, recovery, and two independent Carriers | multiple engagements can operate under aggregate capacity, exposure, and failure controls |

The minimum read-only product normally involves four repositories. A useful
trusted earning loop normally involves five or six. The reference production
architecture normally involves seven, subject to the ownership choices above.

## 3. Repository change matrix

| Repository or component | Requirement | Required changes | Must not become |
|---|---|---|---|
| `tos-service-spec` | always | freeze Intent, Agreement, body-bound authorization predicates, evidence profiles, semantic action identity registry, obligation, action, retrieval, private handoff, operation admission, billing, scheduling, Gate, authority, bounds, errors, vectors, and an implementation-independent reference verifier | an industry-specific workflow catalog |
| `tos-service-protocol` | always | production canonical codecs, signatures, predicate/evidence verification, registry-derived deterministic IDs, admission and handoff helpers, references, clients, Adapter interfaces, and recovery vectors | a profitability engine or market database |
| `openfox` | always for the product | discovery, Inventory, AI assessment, economics, negotiation, Agreement coordination, Owner Economic Action Authority, transactional Portfolio, Gate, publication/pricing, scheduling, operations, accounting, and learning | custody, chain finality, or unrestricted model authority |
| `tos-messenger` | required for Agent negotiation; optionally one Carrier | Intent-referenced contact, typed Agreement and private-handoff control events, action admission, deduplication, resolution, exact-object transport, replay-safe delivery, and the complete bounded Carrier profile when enabled | Agreement, execution, settlement, or global-market truth derived from chat or room state |
| `tos-service-gateway` | required when Gateway is a Carrier; normally one of two production paths | bounded publish/search/subscribe, source-local cursor, operation admission, provenance, selective retrieval, idempotent status, and controlled writer admission | a global market head, winner, solvency oracle, or authoritative order database |
| `tos-ai` or another executor | required when selected by an Agreement | receiver-selected private ingress when applicable, immutable resource capabilities, task-scoped effect broker, one-shot runner, evidence, and crash/takeover behavior | settlement selector, policy authority, credential owner, or remote-selected fetcher |
| `tos` and custody/`tosctl` | required for TOS identity/value effects or escrow | writer-generation high-water, action admission, signing, broadcast, recovery, direct-payment evidence, and optional Quote/escrow/Receipt support | search, ranking, profitability logic, or category-specific commerce contracts |
| optional market applications | independently optional | user experience, hosted search, ranking, moderation, support, KYC, fiat, and proprietary services | Agent, Agreement, execution, or settlement authority |

## 4. `tos-service-spec` roadmap

The specification repository owns the portable contract. Documentation alone
does not complete this phase. It must freeze wire-level definitions and
conformance artifacts for:

- the common Agent Operation Envelope and operation profile boundaries;
- `AgentIntentV1`, signed Discovery Card, revision, withdrawal, and reference;
- publisher fields versus separately attributed Carrier- or index-derived
  fields;
- bounded detail and attachment descriptors;
- operation admission descriptors, short-lived proof/challenge profiles,
  resource vectors, and bindings to actor, opcode, audience, declared size,
  Carrier and expiry;
- `ContentRetrievalPolicyV1`, including origin, SSRF, DNS, redirect, TLS/SNI,
  proxy, credential-origin, connection, byte, decompression, and time policy;
- a business-neutral private-content handoff contract binding Agreement,
  obligation, sender, receiver, exact content, encryption, proof of possession,
  ingress, bounds, retention, action identity, acknowledgement and recovery;
- `AgentAgreementBodyV1` and its canonical participant and obligation graph;
- `AgreementObligationV1`, including dependencies, value, billing, evidence,
  disclosure, cancellation, dispute, references to specification-derived
  mandatory and proposer-added authorization predicates, and one settlement
  Adapter for each value-bearing obligation;
- canonical `AgreementAuthoritySubjectV1` and
  `AgreementAuthorizationPredicateV1` records inside the Agreement body,
  binding subject, role/obligation scope, evidence profile
  URI/version/descriptor digest, validity and target projection;
- the non-circular Agreement-core, authorization-policy and per-predicate target
  projection formulas, with the final body digest covering every target;
- `AgreementAcceptanceProfileV1` and
  `AgreementAuthorizationEvidenceV1`, supporting mixed profiles while
  preventing a later profile choice, weaker substitute, partial union, or
  cross-Agreement replay;
- the V1 Agent-signature, authority-signature and optional Paid Demand Quote
  evidence-profile descriptors, eligible subject kinds, grouping rules and
  immutable descriptor-digest fixtures;
- typed `AGREEMENT/PROPOSE`, `AGREEMENT/ACCEPT`, and
  `AGREEMENT/WITHDRAW` actions;
- the per-action-kind `SemanticActionIdentityV1` registry in
  [`SEMANTIC_ACTION_IDENTITY_V1.md`](SEMANTIC_ACTION_IDENTITY_V1.md),
  including recoverable repeat-instance allocation, schedule/dependency
  transitions, generic post-start executor effects, and private-content
  deletion,
  `WriterFenceV1`, `AuthorizedActionV1`, and `ActionResolutionV1`;
- `BillingTermsV1` and `SettlementObligationV1`, including Agreement and
  obligation identity, kind, sequence, predecessor, payer, payee, asset,
  canonical amount, due/not-before/expiry, finite recurrence, aggregate cap,
  paid-to-date, Adapter, mandate, action identity, exact evidence references,
  and durable `pending`, `partially-paid`, `paid`, `overdue`, `cancelled`,
  `disputed`, and `written-off` states;
- durable scheduling and subcontract dependency records;
- unique execution slots, atomic start, one-shot start tickets, and
  ambiguous-start recovery; and
- canonical encoding, domain separation, deterministic identity, bounds,
  unknown-extension behavior, error classes, time-validation rules, and exact
  test vectors. Time rules define maximum accepted future skew, durable
  monotonic observation, expiry after clock rollback, and use of finalized
  chain time only where a selected chain profile makes it authoritative.

Exit criteria:

1. semantically unrelated Intents use the same core schema;
2. the standalone specification verifier and the production SDK reproduce every
   required digest and ID without sharing canonicalization code;
3. malformed authority, duplicate identifiers, cycles, conflicting bytes, and
   unknown required extensions fail closed; and
4. no side-effect phase depends on prose that has not been frozen into a typed
   object or explicit implementation policy.

## 5. `tos-service-protocol` roadmap

The protocol SDK implements the shared mechanics so that individual products
do not create incompatible versions. It must provide:

- canonical encode/decode for Agent Operations, Intents, Agreements,
  authorization predicates/evidence, Authorized Actions, payment requests, and settlement
  obligations;
- exact signature, delegation, expiry, audience, revision, and predecessor
  verification;
- identity, delegation, key-rotation and revocation verification without
  transferring earlier authority to a new device or alias by inference;
- time, expiry and maximum-skew verification that cannot revive an already
  observed expired object after process restart or host-clock rollback;
- deterministic object, action, obligation-instance, and request digests;
- duplicate, conflict, equivocation, fork, and unknown-extension handling;
- mandatory-predicate derivation; non-circular target recomputation; immutable
  profile descriptor resolution; and mixed-profile Agreement evidence
  verification, including one complete generic evidence object per
  body/version/subject and no union of partial subsets;
- exact implementation of the released `SemanticActionIdentityV1` binary
  framing, SHA-256 formula, ordered entry table, controlled repeat-instance,
  terminal-successor, execution-lineage and exact-byte vectors, excluding
  retry, transport, wall time and writer generation;
- `WriterFenceV1` proof, owner/Agent/scope/expiry and authority-confirmed
  acquire/takeover verification, plus mandate and approval content resolution;
- Intent Reference and Carrier client helpers;
- operation admission proof/challenge verification and resource-accounting
  helpers without requiring one universal fee or stake mechanism;
- private-content handoff encode/verify, exact retry, conflicting-upload, status
  and accepted-content-record helpers;
- `ContentResolver`, publication, conversation, execution, Portfolio, and
  settlement Adapter interfaces where portability is required;
- `ResolveAction` and obligation-resolution helpers; and
- conformance fixtures consumable by every repository.

OpenFox, Messenger, Gateway, and custody must reuse this implementation or
prove byte-for-byte compatibility. They must not independently reinterpret the
canonical schemas.

The second verifier lives under a standalone conformance package in
`tos-service-spec`. It uses a separately maintained implementation language or
toolchain, imports neither the production SDK nor generated production codec
code, and consumes only frozen schemas and byte fixtures. Its CI compares
success values and exact failure classes against `tos-service-protocol`. If
these independence requirements cannot be met in that repository, the verifier
moves to a separately named repository and the repository count is updated
before Phase 0 exits.

## 6. `openfox` roadmap

OpenFox owns local reasoning and autonomous-business safety. It requires the
largest implementation effort.

### 6.1 Capability Inventory

Build an owner-scoped snapshot covering:

- installed Skills, models, and tools;
- credential capabilities and revocation generations;
- wallets, assets, and supported settlement Adapters;
- CPU, memory, storage, accelerator, model-token, API, time, and concurrency
  capacity;
- existing reservations and obligations;
- verified unit-cost and outcome evidence; and
- snapshot creation, expiry, source generation, Portfolio revision, policy
  revision, consistency token, and per-item authority evidence.

Informational contact may use a configured wider freshness window. Agreement,
reservation, settlement preparation, publication pricing, and execution must
revalidate the Inventory at the same consistency barrier used to admit the
side effect.

### 6.2 Opportunity Collector and staged filtering

Implement:

- bounded search and subscription over one or more Carriers;
- source-local cursors, exact deduplication, replay, restart, and provenance;
- signature and observed revision-chain verification before model analysis;
- deterministic filters over mode, class, taxonomy, keyword, approximate
  value, time, region, language, fulfillment, issuer, and local policy;
- issuer/category/value diversity quotas and a bounded exploration bucket;
- cheap ranking followed by a bounded top-K shortlist;
- source-specific query minimization so a Carrier never receives the complete
  Skill Inventory, credential list, Portfolio, exact profit threshold, or full
  search profile;
- owner-visible retention and sharing policy for queries, embeddings,
  translations, derived profiles, and remote model calls;
- optional broad batching, local indexing, query rotation, or a released
  privacy-relay profile when the owner selects that threat model;
- content retrieval only through `ContentRetrievalPolicyV1`; and
- exact size and digest validation before selected detail reaches the model.

### 6.3 AI assessment and Economic Evaluator

The embedded AI may interpret hostile free-form content, propose queries,
classify opportunities, identify relevant Skills, estimate work, generate
questions, propose prices, and suggest a plan. Deterministic code must
independently calculate or clamp:

- revenue and payment probability;
- completion and acceptance probability;
- compute, model, API, tool, energy, labor, and subcontractor cost;
- capital lock, opportunity cost, liquidity, volatility, and custody risk;
- retry, failure, refund, dispute, privacy, legal, and reputation reserves;
- expected net profit, risk-adjusted ROI, and worst-case exposure; and
- rejection, owner-review, contact, and settlement-strength thresholds.

Every cross-asset estimate records an owner-approved valuation source, quote
asset, observation time, expiry, confidence or spread, liquidity, slippage,
fees and worst-case conversion assumption. Valuation is advisory evidence for
local admission and accounting, never authority to alter the Agreement's exact
asset or amount. Stale, unavailable or materially conflicting valuation leaves
profit unknown and blocks autonomous commitment under a fail-closed policy.

Unknown material inputs remain unknown. Model output cannot select credentials,
signing keys, policy changes, unrestricted tools, hidden routes, execution, or
payment.

### 6.4 Negotiation and Agreement coordination

Implement:

- bounded Intent-referenced first contact;
- disclosure, frequency, recipient, abuse, and owner-policy controls;
- natural-language negotiation through authenticated Messenger;
- V2 non-authorizing Intent applications carrying an optional complete generic
  Agreement proposal graph for all Intent modes, with issuer-side exact-subject,
  value, time, participant, predicate and Adapter validation;
- owner-configured public settlement parameters in supply Intents so an
  applicant can compile an exact destination/profile without inferring it from
  prose; secrets and credentials are forbidden from this field;
- compilation of one canonical multi-obligation Agreement body;
- deterministic derivation of each obligation's mandatory typed predicates:
  always its obligor, plus the payer/custody principal for value, the refunding
  principal for a refund, and the authority owner for disclosed private data,
  credentials or capabilities; proposer additions become stricter canonical
  predicates rather than an untyped parallel list;
- settlement Adapter and exact parameters for every value-bearing obligation
  before acceptance;
- body binding of each predicate's subject, profile
  URI/version/descriptor digest, role/obligation scope, validity and recomputed
  target projection, followed by satisfaction with matching evidence; generic
  predicates use typed acceptance while chain-bound predicates use their exact
  mapped evidence without duplicate generic acceptance;
- typed proposal, applicable generic acceptance, withdrawal, predecessor,
  expiry, and conflict handling, with exactly one complete generic evidence
  object per `(body_digest, version, subject)` rather than unioned subsets; and
- recovery of ambiguous sends through the same action ID and request digest.

Ordinary chat, a model-generated acceptance phrase, a UI state, a read receipt,
or a frozen transcript cannot create Agreement authority.

### 6.5 Owner Economic Action Authority

Every publication, contact, Agreement action, reservation, schedule transition,
Gate transition, disclosure, upload, credential issue, delivery, payment,
settlement, release, and applied reconciliation must carry one exact
`AuthorizedActionV1`.

The V1 reference implementation lives in `openfox`. For a personal single-host
deployment, the OpenFox owner daemon embeds the authority in one durable
transactional service with an exclusive process lock. For a shared or
multi-host deployment, the same package runs as an owner-operated control-plane
service against a strongly consistent backend reachable by all authorized
OpenFox hosts. Model and worker processes cannot access its signing identity or
storage directly. Both profiles must provide:

- monotonically increasing writer generation;
- rollback-resistant generation high-water state advanced only by an
  authority-confirmed acquire or takeover;
- an authority-issued `WriterFenceV1` proof binding owner, Agent, instance,
  lease, generation, issue/expiry, authority and action scope; a bare or merely
  larger generation integer carries no authority;
- stable action ID derived by the registered per-kind semantic formula and
  exact request digest admission; retry, transport, time and writer fields are
  forbidden identity inputs;
- expected-prior-state validation;
- resolution and validation of mandate and approval content, scope, revision
  and expiry rather than digest comparison alone;
- idempotent exact retry and conflicting-request rejection;
- durable `unknown`, `prepared`, `submitted`, `accepted`, `rejected`,
  `conflict`, and `terminal` resolution; and
- query-before-retry recovery after timeout, crash, partition, or takeover.

Lease validation uses the authority's durable monotonic lease state and the
sink's released skew policy. Restoring a backup, restarting a process or
rolling back a host clock cannot make a superseded or previously expired fence
current again.

The Action Authority and Portfolio admission share one serializable transaction
or an explicitly frozen atomic commit protocol. The transaction advances the
writer high-water mark, admits the exact action, checks aggregate exposure, and
creates or changes its reservation together. A reservation cannot succeed
without its action, and an action that changes exposure cannot succeed without
the matching Portfolio transition. Messenger, Carrier, executor, credential,
and payment sinks either query this authority at admission or are reachable
only through a broker whose credentials the authority exclusively controls.
Every `AuthorizedActionV1` binds the verified fence through
`writer_fence_digest`; each sink verifies proof, scope and expiry and never
advances high-water from an ordinary action carrying a future integer.
Authority or backend loss blocks new actions; it never falls back to a worker
journal or per-process Portfolio.

### 6.6 Portfolio Ledger

Atomically reserve and reconcile:

- compute and execution capacity;
- external spend and locked capital;
- unsecured receivable and maximum nonpayment loss;
- refund, dispute, and subcontract exposure;
- per-counterparty and aggregate owner exposure; and
- pending contact, proposal, accepted Agreement, execution, delivery, billing,
  and unsettled-obligation state.

Per-process limits are insufficient. A stale writer must not reserve or release
resources after takeover.

### 6.7 Local Execution Gate

Implement:

- a unique `(agent_id, agreement_digest, execution_id)` slot;
- `execution_id` derived from the exact `execution.slot` entry over Agreement,
  execution-bearing obligation, canonical plan/input identity, authority-
  allocated attempt index and predecessor terminal-resolution digest; attempt
  zero uses the zero predecessor, ambiguous state has no successor, and only a
  permitted terminal failure can atomically allocate index `n+1`;
- `PREPARED -> STARTING` as the atomic execution linearization point;
- a short-lived, one-shot `start_not_after` ticket;
- durable `AMBIGUOUS_START` after a crash during start;
- immutable no-follow file and directory capabilities bound to file identity
  and, where required, exact digest;
- pinned scheme, host, IP class, port, TLS/SNI/certificate, redirect, proxy, and
  retry rules;
- non-escalating credentials bound to action, Skill, task, domain, and
  destination;
- task-broker mediation for every outbound connection, upload, credential use,
  value transfer, and destructive action after process start;
- a registered `executor.effect` or more specific action kind for every
  externally visible or destructive tool/API effect, with the exact
  plan-effect ID, profile, target, operation and semantic key frozen by the
  Gate-approved plan; and
- explicit drain or kill policy when writer authority is superseded.

A successful Gate decision authorizes only bounded execution. It does not prove
correct work or authorize payment.

### 6.8 Durable scheduling and subcontracting

Implement durable schedule and dependency records containing:

- the exact Agreement body and execution-obligation identity for every entry;
- writer and dispatch generations;
- deadlines, priority, resource and exposure reservations;
- dependency identity and type;
- a `blocking` or `informational` dependency class;
- cancellation and preemption class;
- irreversible boundary;
- downstream Agreement and obligation identity;
- failure-propagation and disclosure policy; and
- evidence-driven release and accounting updates.

New entries use `EngagementScheduleEntryV2`. A migrated V1 entry without an
exact execution-obligation identity remains readable but is conservatively
held for reconciliation; migration never guesses that identity from an opaque
execution digest.

Takeover must reconcile dispatched, starting, running, and ambiguous entries
before replacement work is admitted. Cancelling an upstream Agreement cannot
silently cancel or grant authority over a downstream Agreement.

All blocking cross-Agreement dependencies for one owner form a versioned
acyclic graph. Edge cycle check and insertion occur in the same linearized
Action/Portfolio transaction as schedule admission, preventing concurrent
`A -> B` and `B -> A` insertion. Informational edges never block dispatch.
Cancellation, timeout, or terminal failure removes blocking edges under the
recorded propagation policy so recovery cannot deadlock the schedule.
Entry mutations use `schedule.entry.transition`; dependency insertion and
removal use `schedule.dependency.transition`. Unknown or implementation-local
scheduler action kinds fail closed.

### 6.9 Settlement, accounting, and learning

Implement a common Adapter registry and distinguish:

- explicitly unpaid work;
- Agreement-bound direct payment;
- external settlement with an explicit evidence class;
- optional TOS escrow; and
- Agent Gift as independent gratuity or other income.

A Gift cannot close an Agreement obligation. Only evidence bound to the exact
Agreement, obligation instance, payer, payee, asset, amount, destination, and
payment request can close a direct-payment obligation.

The billing engine deterministically materializes only the finite instances
authorized by `BillingTermsV1`. Each instance binds its Agreement, obligation,
sequence and predecessor; enforces not-before, due, expiry and cumulative cap;
and allocates partial payment by the released rule. Duplicate materialization
is idempotent. A skipped sequence, changed amount or destination, extension of
recurrence, or increase of the aggregate cap requires a newly accepted
Agreement version. Cancellation, dispute, payment and timeout races resolve
from exact ordered evidence, and restart or takeover reconstructs the same
paid-to-date and outstanding balance before another payment action is admitted.

Accounting must preserve quoted value, accepted obligation value, reserved
exposure, actual cost, partial payment, overdue balance, nonpayment, refund,
dispute, write-off, gratuity, and settled revenue. Learning may improve search,
matching, cost estimation, pricing, negotiation, and local risk estimates only
from verified evidence. It cannot enlarge authority or erase adverse outcomes.

### 6.10 Autonomous supply publication and pricing

Implement a dedicated publication manager with typed `Draft`, `Publish`,
`Reply`, `Revise`, `Withdraw`, and `ResolveAction` operations. The AI may propose
service content, taxonomy, capability hints, audience, price range,
availability, and expiry. Deterministic owner policy must enforce:

- current Inventory, verified unit cost, minimum expected margin, maximum
  discount, and maximum price-change bounds;
- audience, disclosure, TTL, active-publication, reply, revision, per-Carrier,
  and per-period limits;
- exact `AuthorizedActionV1`, verified `WriterFenceV1`, request digest, signing
  purpose, and idempotent Carrier status recovery;
- acquisition of the selected Carrier's short-lived admission challenge and
  proof before publication; any postage, fee, bond, or other economic exposure
  is a separate exact Authorized Action admitted by the aggregate Portfolio;
- withdrawal or owner review when capacity, credential, Skill, cost, policy, or
  price evidence becomes stale or materially changes; and
- preservation of every earlier signed revision and honest visibility of worse
  terms.

A publication advertises possible availability. It is not an Agreement and
does not reserve every advertised unit of capacity. OpenFox refreshes Inventory,
price, schedule, and Portfolio before contact or commitment. Autonomous supply
uses the same Intent, Agreement, Gate, settlement, and accounting path as an
opportunity found elsewhere.

### 6.11 Private content handoff

Implement a business-neutral `PrivateContentHandoffAdapter` for private source,
data, artifacts, and results required by an accepted Agreement. A handoff binds:

- Agreement and obligation identifiers, sender, receiver, direction, purpose,
  action identity, expiry, and accepted transport profile;
- exact content or manifest digest, media type, file count, canonical path,
  compressed and expanded byte bounds, and encryption parameters;
- a receiver-selected ingress or an owner-approved origin that remote content
  cannot replace;
- a short-lived single-purpose challenge and sender proof of possession;
- authenticated encryption or an equivalent released private-transport
  profile, with no ambient credentials or bearer-only authority;
- atomic durable acceptance of immutable bytes, acknowledgement, retention,
  deletion, and evidence references; and
- exact retry, concurrent upload, conflicting bytes, timeout, status query,
  crash, and takeover behavior.

Public Intent processing never fetches or executes private input. The local
Gate receives only the immutable accepted-content record and matching bytes
after Agreement, disclosure, Inventory, Portfolio, writer, and policy checks.
Private content, keys, plaintext, and unrestricted URLs never enter public
cards, model prompts, receipts, metrics, or logs. A TOS escrow profile may
replace this generic Adapter with a stricter profile, but cannot weaken these
boundaries.

The reference trusted path assigns canonical challenge, authorization,
acknowledgement, and status messages to `tos-messenger`; the selected executor,
or `openfox` for an in-process Skill, owns the receiver-selected bulk ingress
and immutable accepted-content store. `tos-service-protocol` supplies the shared
codec and verifier. A different Storage Adapter may replace the byte transport
only after satisfying the same contract and cannot become Agreement authority.

### 6.12 Operational safety and rollout

Implement explicit runtime modes:

1. `off` — no earning acquisition;
2. `observe` — read, verify, assess, and explain only;
3. `contact` — bounded non-binding contact;
4. `trusted` — bounded accepted Agreements and unsecured execution;
5. `policy-gated` — approved payment or escrow Adapters; and
6. `approval-required` — prepare exact actions for the owner.

Every fresh installation and schema migration defaults to `off` or `observe`.
Publication, contact, Agreement, scheduler, execution, billing, Gift, transfer,
external settlement, and escrow each have separate default-off feature gates.
Operators receive authenticated commands for status, inspection, owner-approved
writer takeover, scoped pause, drain, resume, and reconciliation. Reconciliation
is split into read-only `--dry-run` and writer-fenced, audited, crash-recoverable
`--apply`.

A paused scope creates no new action in that scope. Drain preserves already
accepted obligations while preventing new commitments. Takeover increments the
writer generation and reconciles every ambiguous action, reservation,
execution, billing, and settlement state before new work. A release must define
rollback, data migration, credential revocation, emergency stop, and safe
downgrade behavior; inability to represent a newer authoritative object blocks
the downgrade rather than discarding it.

### 6.13 Observability and release evidence

Expose bounded metrics and audit records for acquisition budgets, admission
proofs, verification failures, filtering, model cost, publication, contact,
Agreement, writer state, actions, reservations, execution, scheduling, billing,
payment, nonpayment, disputes, write-offs, recovery, and unresolved-state age.

Logs and metrics exclude custody secrets, credentials, private input, complete
confidential messages, unrestricted model context, and plaintext deliverables.
Retention and deletion are owner-visible and profile-specific. Every mutating
operator action records the actor, exact action/request digest, writer
generation, policy/mandate/approval references, prior state, result, and
evidence without copying secrets.

The repository produces a reproducible acceptance manifest containing exact
commits, configuration, schema/vector versions, build artifacts, platform,
operator/store identity, test interval, commands, results, and exclusions. Unit,
fuzz, race, crash, partition, stale-writer, resource-exhaustion, hostile-content,
private-handoff, real-Adapter, and platform build/test results remain separately
labelled; mocks never substitute for production evidence.

## 7. `tos-messenger` roadmap

### 7.1 Negotiation transport

Messenger is the authenticated negotiation transport. It must add or expose:

- first contact bound to canonical issuer Agent identity and an exact Intent
  Reference;
- typed `AGREEMENT/PROPOSE` and `AGREEMENT/WITHDRAW` event delivery, plus
  `AGREEMENT/ACCEPT` when a body-bound predicate selects typed off-chain
  evidence;
- exact Agreement body and digest transport;
- typed private-handoff challenge, authorization, acknowledgement, status and
  deletion events without placing bulk plaintext in public or model context;
- `AuthorizedActionV1` admission for every side-effecting send;
- `WriterFenceV1` proof/scope/expiry and high-water enforcement directly at the
  outbox, or exclusive access through the owner Economic Action Authority;
- stable action-ID deduplication, request-digest conflict detection, durable
  resolution, and `ResolveAction`;
- duplicate, ambiguous-send, restart, replay, and device-rotation recovery;
- explicit UI and event separation among message, Proposal, Agreement,
  delivery, Gift, payment request, and settlement evidence; and
- existing secure room, direct-message, and Gift transport without converting
  chat or Gift into commercial authority.

Messenger databases remain participant-local projections. They are not a
global Agreement, market, execution, or payment database.

### 7.2 Optional Messenger Carrier profile

Messenger may count as a first or second Carrier only when it implements the
complete released Carrier contract rather than merely carrying links in chat.
The profile must provide:

- bounded exact-byte Intent publication, revision, withdrawal, republication,
  and reference resolution in explicitly configured public rooms or channels;
- signed Discovery Card search or bounded history subscription without eager
  detail or attachment delivery;
- room- and source-local cursors, epochs, retention bounds, pagination,
  provenance, and restart recovery;
- exact digest deduplication, issuer/revision conflict evidence, source-local
  availability, and no claim of a globally latest head;
- selective content-addressed detail resolution under the generic retrieval
  policy;
- membership/role checks where required, sender and room quotas, block lists,
  admission proof or inbox/publication resource policy, and
  resource-exhaustion telemetry; and
- `AuthorizedActionV1`, writer-fence proof and high-water enforcement,
  registered semantic publication identity, request-digest conflict,
  idempotent exact retry, and status resolution.

If Messenger does not release this profile, it remains the negotiation
transport and cannot satisfy Phase 1 or the second-Carrier production gate. The
roadmap must then name another independent Carrier implementation.

## 8. `tos-service-gateway` and Carrier roadmap

Gateway is one replaceable Carrier implementation. When selected, it must
provide:

- bounded exact-byte Intent publication, revision, withdrawal, and retrieval;
- signed Discovery Card search and subscription without eagerly returning all
  detail or attachments;
- source-local cursors, pagination, rate limits, quotas, and provenance;
- explicit separation of issuer-signed fields from Gateway-derived category,
  translation, conversion, embedding, moderation, and rank;
- selective detail and attachment retrieval through the generic retrieval
  policy;
- stable action-ID idempotency, request-digest conflict, status resolution, and
  writer-fenced publication admission; and
- rebuildable local indexes without a global latest head or globally complete
  cursor.

### 8.1 Operation admission and spam resistance

Every Carrier publishes a bounded admission profile for each accepted operation
family. Admission policy may use contacts, room membership, inbox tickets,
postage, unsolicited quotas, proof of work, fees, refundable bonds, local
relationship state, or another released challenge. No single mechanism is
mandatory for every Carrier, but an accepted proof is short lived and binds the
actor, opcode, audience, declared size/resource vector, Carrier identity,
challenge, and expiry.

A Carrier that selects a TOS-denominated fee or bond uses existing custody and
value-transfer primitives where their semantics fit. It adds `tos` contract
work only when a separately reviewed generic admission primitive is genuinely
missing; admission policy alone does not justify an industry-specific contract.

Gateway and Messenger reject an invalid, expired, replayed, undersized, or
wrong-Carrier proof before expensive body retrieval, parsing, indexing, or model
work. They enforce per-actor, origin, topic, audience, room, and Carrier-path
budgets; strict envelope, nesting, field, attachment, revision, and lifetime
bounds; content addressing; exact-byte deduplication; quarantine and block
policy; and bounded retention. Paid placement or moderation may affect local
visibility but never changes Intent validity or Agreement authority.

OpenFox additionally applies receiver-local source, issuer, category,
value-band, query, byte, parser, model-token, and wall-clock budgets. Carrier
admission and local filtering are complementary: sender cost and resource
admission protect the propagation layer, while local quotas protect each
receiver against valid-but-irrelevant or deceptive content.

Conformance includes Sybil issuance, keyword/category stuffing, rapid revision,
duplicate publication, admission-proof replay, wrong audience/size/Carrier,
challenge expiry, oversized compressed and expanded content, parser bombs,
resource exhaustion, block/quarantine, and recovery after a Carrier restart.

One Carrier is sufficient for development, read-only observation, and contact
about one independently verified Intent. A claim of resilient decentralized
public discovery requires at least two Carrier paths with independent
implementations, operators, stores, upstreams, and failure domains. The
acceptance campaign must remove one complete Carrier database and still
rediscover and resolve already replicated signed content through the other.

## 9. `tos-ai` or selected executor roadmap

An executor enters scope only when an accepted Agreement selects it. It must:

- consume the exact Agreement, plan, input, resource capabilities, and one-shot
  start ticket;
- start one execution slot at most once;
- run inside the selected sandbox and resource budget;
- receive only immutable file, network, credential, disclosure, upload, and
  destructive-operation capabilities;
- when acting as the private-content receiver, expose only the receiver-selected
  ingress, authenticate the exact handoff challenge and sender proof, atomically
  commit the immutable accepted-content record, and resolve exact retry or
  conflict without allowing a remote-selected fetch target;
- request every post-start external effect through the task-scoped broker;
- journal start, running, checkpoint, outcome, and evidence state;
- obey writer-loss drain or kill policy; and
- produce bounded execution and delivery evidence.

The executor cannot select payment, expand permissions, obtain custody keys,
reinterpret ordinary conversation as an Agreement, or mark itself paid.

If the first trusted task uses an existing local OpenFox Skill, a separate
`tos-ai` change may be deferred. The same Gate, capability, broker, and
at-most-once rules still apply inside OpenFox.

## 10. `tos`, custody, and `tosctl` roadmap

### 10.1 Common custody admission

Custody must persist and enforce:

- owner/Agent writer-generation high-water state advanced only by
  authority-confirmed acquire or takeover;
- verified `WriterFenceV1` proof, scope and expiry;
- registered semantic action ID and exact request digest;
- policy, mandate, approval, expiry, and expected-prior-state checks;
- aggregate spend and locked-capital limits;
- prepared, signed, broadcast, accepted, rejected, conflict, and terminal
  resolution; and
- query-before-retry recovery without producing a replacement economic action.

Private signing keys remain in custody. OpenFox and its model receive only
purpose-limited action results and evidence.

### 10.2 Agreement-bound direct payment

The direct-payment Adapter must bind:

- Agreement body digest;
- Agreement obligation and runtime obligation-instance identifiers;
- payer and payee;
- asset and exact atomic or canonical decimal amount;
- destination and network;
- Adapter profile and parameters;
- stable action identity and expiry; and
- exact finalized transfer evidence.

The same transfer evidence cannot satisfy two payment requests. An unrelated
transfer with the same payer, payee, asset, and amount cannot be heuristically
used to close the obligation.

This work normally belongs in custody or `tosctl`. It does not necessarily
require a new chain contract.

### 10.3 Agent Gift

Keep the existing Gift semantics unchanged. Gift is a non-purchase transfer and
may be recorded as gratuity or other income. It does not bind an Agreement,
invoice, deliverable, Quote, Receipt, or payment obligation and therefore cannot
close one.

### 10.4 Optional TOS escrow

Only an Agreement obligation that explicitly selects a released TOS escrow
profile activates this scope. The selected profile must provide:

- deterministic Agreement-to-Accepted-Quote binding;
- body-bound Paid Demand predicates mapping Provider authorization to the exact
  signed Provider Offer and buyer commercial acceptance to the finalized bound-
  wallet on-chain `accept`, with no duplicate generic acceptance required or
  accepted for those predicates;
- Quote commitment to the exact generic Agreement body digest, scoped
  obligation IDs, predicate IDs, target projection digests and immutable Paid
  Demand profile descriptor, with equality verification against both generic
  and native terms;
- complete specification-derived mandatory and additional authorization;
- exact asset, amount, destination, and contract configuration;
- finalized escrow funding before dependent execution;
- the released proof-of-possession private-input ingress, immutable acceptance
  record, retention, deadline, clock, status, and recovery profile;
- Native Execution Gate admission;
- at-most-once bounded execution;
- Receipt and validator or release evidence;
- release, refund, dispute, timeout, and recovery; and
- independently resolved finalized provider-wallet credit.

No new contract is added merely because a new profession or product appears.
Only a genuinely new enforcement primitive may justify a separately reviewed
generic contract or Adapter.

## 11. Compatibility and migration

Migration is additive and preserves existing authority:

- existing Capability-first purchases remain valid and do not become generic
  Intent Agreements retroactively;
- existing Accepted Quote, escrow, Native Gate, Receipt, Gift, and settlement
  semantics remain unchanged;
- an existing Paid Demand may be advertised through a generic Intent only by a
  released extension that binds the exact original bytes, reference, and
  digest; a derived summary never replaces its profile authority;
- changed escrow-critical terms create the new exact specialized objects and
  authorizations required by that profile;
- existing Gateway and Messenger databases remain local projections and may be
  rebuilt from retained signed bytes; migration cannot promote their local
  rows into global Intent or Agreement authority;
- schema negotiation records supported required and optional extensions,
  rejects unknown required semantics, and round-trips unknown optional bytes;
- OpenFox database migration preserves action IDs, writer generations,
  reservations, Agreement/obligation evidence, paid-to-date, adverse outcomes,
  and unresolved ambiguity; and
- downgrade is allowed only when every authoritative object and safety state
  remains representable. Otherwise the older binary starts read-only or refuses
  the affected profile.

Every repository supplies forward/backward fixture tests and a rollback plan.
Mixed-version tests cover publication, Messenger delivery, Agreement acceptance,
Action resolution, private handoff, direct payment, billing, and optional
escrow without weakening the newest required authority checks.

## 12. Delivery phases

### Phase 0 — schema and conformance foundation

Repositories:

- `tos-service-spec`;
- `tos-service-protocol`.

Deliver:

- all canonical objects, body-bound Agreement predicates, mixed-profile
  evidence, non-circular targets, semantic-action registry entries and
  exact-byte vectors, operation-admission and private-handoff profiles, bounds,
  IDs, signatures, errors, and recovery vectors;
- semantically unrelated fixtures; and
- the standalone `tos-service-spec` reference verifier plus the production
  `tos-service-protocol` codec/verifier.

Exit only when the two code-independent implementations agree on success and
exact failure classes, admission/handoff attack vectors fail closed, and the
acceptance manifest records both implementations and toolchains.

### Phase 1 — read-only Intent scout

Repositories:

- Phase 0 repositories;
- `openfox`;
- one complete Carrier profile, initially `tos-service-gateway` or the released
  Messenger Carrier profile.

Deliver bounded discovery, consistent Inventory, deterministic filtering,
query minimization, selective safe retrieval, operation-admission/resource
telemetry, hostile-content AI analysis, capability matching, profit/risk
explanations, persistence, and read-only UI/CLI. Publication, contact,
Agreement, execution, and payment remain disabled by separate default-off
feature gates.

### Phase 2 — authenticated negotiation

Repositories:

- `openfox`;
- `tos-messenger`;
- `tos-service-protocol`;
- the `openfox` Owner Economic Action Authority and transactional Portfolio
  implementation.

Deliver proof-carrying writer-fenced contact, registry-derived semantic action
IDs, typed Agreement proposal/withdrawal and applicable off-chain evidence,
mandatory-predicate derivation, body-bound profile/target validation,
Action/Portfolio atomic admission, duplicate and ambiguous-send recovery,
owner-approved takeover, pause/drain, and non-binding ordinary conversation.

### Phase 3 — trusted low-risk earning

Repositories:

- Phase 2 repositories;
- one selected local or remote executor;
- one private-content handoff transport/ingress;
- custody and one Agreement-bound payment Adapter when payment is promised.

Deliver one real bounded Agreement, aggregate Portfolio reservation, required
prepayment or finalized funding, authenticated private input, immutable accepted
bytes, one-shot Gate execution, bounded delivery, exact payment resolution or
honest nonpayment, dry-run/applied reconciliation, realized-cost accounting,
and separate Gift-gratuity accounting. Only the required feature gates are
enabled; emergency pause and drain remain operational.

### Phase 4 — settlement and billing adapters

Repositories depend on the selected Adapters.

Deliver at least two settlement choices through the same Agreement path,
canonical finite deposit/milestone/installment/periodic/refund obligations,
partial-payment allocation, cancellation/dispute state, and evidence-driven
recovery. Mixed-version and migration fixtures preserve earlier payment and
Gift semantics. Disabling any Adapter must not disable discovery or
negotiation.

### Phase 5 — optional untrusted TOS escrow

Repositories:

- `openfox`;
- `tos-service-protocol`;
- `tos` and custody/`tosctl`;
- the selected executor and Native Gate implementation.

Deliver the complete released escrow profile and its separate security,
proof-of-possession private ingress, conformance, public-testnet, recovery, and
external-acceptance evidence. This phase does not block the trusted
direct-payment loop.

### Phase 6 — resilient continuous autonomous business

Repositories:

- all required runtime repositories above;
- a second independent Carrier implementation and deployment.

Deliver autonomous service publication and repricing, durable multi-engagement
scheduling, subcontract dependencies, canonical recurring billing, aggregate
cross-host Portfolio safety, source-loss recovery, Adapter failure recovery,
operation-level spam/resource admission, query privacy, mixed-version recovery,
operator controls, observability, reproducible acceptance manifests, and
bounded learning from verified outcomes.

## 13. Dependency graph

```text
S0  tos-service-spec: canonical objects, admission/handoff, bounds, and vectors
 |
 +-> R0  tos-service-spec: code-independent reference verifier
 |
 +-> P0  tos-service-protocol: production codec, verifier, IDs, clients, helpers
      |
      +-> O0  openfox: read-only collector, Inventory, AI, and economics
      |
      +-> C0  first complete Carrier: admission, publication, retrieval, recovery

S0 + R0 + P0 + O0 + C0
  -> read-only Intent scout

M1  tos-messenger: writer-fenced contact and profile-qualified Agreement actions
A1  openfox owner control plane: Action + Portfolio atomic admission/recovery
O1  openfox: negotiation, Agreement, and operational controls

P0 + M1 + A1 + O1
  -> profile-authorized Agreement

X1  selected executor with local Gate and task-scoped broker
H1  selected private-content handoff transport and ingress
D1  selected Agreement-bound payment Adapter and custody, when required

A1 + O1 + H1 + X1 (+ D1)
  -> trusted low-risk earning

E1  optional TOS Quote/escrow/Receipt/custody profile
  -> high-assurance untrusted earning

O2  OpenFox publication/pricing, scheduler, billing, operations, evidence
C1  second independent Carrier with admission and source-loss recovery

P0 + A1 + O2 + C0 + C1
  -> continuous autonomous business and resilient public discovery
```

## 14. Cross-repository acceptance campaign

No production or continuous-autonomous-business claim is permitted until the
cross-repository campaign is complete. Each runtime repository owns its local
machine-readable test and operational evidence. `openfox` assembles
content-addressed references into the campaign manifest but cannot rewrite a
Carrier, Messenger, executor, custody, chain, or Adapter result. Missing or
unverifiable required evidence blocks the claim.

The campaign records exact repository commits, configurations, build artifacts,
operators, stores, time windows, and exclusions, and demonstrates:

1. the standalone specification verifier and production SDK share no
   canonicalization implementation and produce identical canonical results and
   exact failure classes;
2. invalid, expired, replayed, undersized, wrong-audience, wrong-opcode, or
   wrong-Carrier admission proofs fail before expensive retrieval, indexing, or
   model work, and Sybil/flood/resource-exhaustion campaigns remain bounded;
3. hostile retrieval hints cannot reach loopback, link-local, private,
   metadata, arbitrary-proxy, credential-bearing, or rebound destinations;
4. Carrier queries reveal only configured minimum fields, never complete
   Inventory, credentials, Portfolio, profit thresholds, or the full search
   profile, and derived-data retention follows owner-visible policy;
5. ordinary chat, transcript text, model output, Gift, invoice, or payment
   request cannot create Agreement or execution authority;
6. every specification-derived mandatory and proposer-added authorization
   predicate is frozen inside the canonical body with typed subject,
   profile URI/version/descriptor digest, role/obligation scope, validity and
   recomputed target projection, then satisfied over that same final Agreement
   by matching evidence; mixed profiles converge, later profile selection and
   partial unions fail, generic evidence cannot replace required chain evidence,
   and chain evidence needs no duplicate generic acceptance;
7. settlement is selected per obligation and aggregate exposure is reserved
   before funding or execution; cross-asset economics retain reproducible,
   fresh valuation, spread, liquidity, fee and worst-case conversion evidence,
   and unknown or conflicting material valuation blocks autonomous commitment;
8. Action and Portfolio admission are atomic; every semantic side effect and
   execution attempt reproduces the normative registry's exact framing,
   ordered key, SHA-256 identity and vectors independent of retry, transport,
   time or writer; same-ID/different-request conflicts, ambiguous successors,
   destination omission, takeover, terminal lineage, and authority-issued
   intentional repeats fail or succeed exactly as specified; a lost repeat-
   allocation response resolves by the same request digest without consuming a
   second sequence, and scheduler/dependency transitions, post-start executor
   effects and private-content deletion cannot use caller-selected IDs;
   every sink verifies the authority-issued `WriterFenceV1`, resolved mandate
   and approval content, and two processes or hosts cannot bypass generation,
   aggregate exposure, or custody limits;
9. forged, expired, replayed, wrong-owner, wrong-scope, future-integer or
   non-authority-confirmed fences fail, and stale writers cannot publish,
   contact, accept, reserve, execute, settle,
   reconcile, compensate, or release after takeover; restart, backup restore,
   excess clock skew or host-clock rollback cannot revive an expired or
   superseded authorization;
10. ambiguous publication, send, upload, signing, broadcast, start, billing,
    and settlement states recover by querying the same stable action, never by
    inventing a replacement or allocating a terminal successor;
11. private handoff authenticates sender, receiver, Agreement, obligation,
    challenge, content, encryption, bounds, ingress, expiry and accepted bytes;
    bearer theft, remote-selected fetch, conflicting or concurrent upload,
    archive/path abuse, status ambiguity, retention and deletion failures fail
    closed;
12. symlink replacement, rename substitution, DNS rebinding, redirect, proxy,
    TLS, credential-scope, upload, and post-start network attacks fail closed;
13. periodic and milestone obligations reconstruct exact sequence, cap,
    paid-to-date, outstanding, cancellation, dispute, and evidence state across
    crash and takeover;
14. blocking cross-Agreement dependency cycle checks and edge insertion are
    atomic under concurrent writers, informational edges never block, and
    upstream cancellation or failure cannot implicitly grant, copy, or cancel
    downstream authority, private data, execution evidence, or payment state;
15. Gift is never consumed as Agreement payment evidence;
16. fresh installs and migrations start with side effects disabled; scoped
    pause, drain, resume, emergency stop, writer takeover, reconciliation
    dry-run/apply, rollback and blocked unsafe downgrade behave deterministically;
17. autonomous publication obeys current Inventory, margin, exposure,
    disclosure, audience, TTL, active-post, revision and rate bounds, preserves
    earlier signed revisions, and never treats advertised capacity as reserved;
18. mixed-version nodes preserve existing Capability, Accepted Quote, Gift,
    Receipt, escrow and Paid Demand authority without creating a second source
    of truth;
19. metrics, audit records and acceptance bundles are complete enough to
    reproduce decisions and failures while excluding credentials, custody
    secrets, private content and confidential model context;
20. identity delegation, key rotation, device rotation, alias changes and
    revocation preserve prior evidence without granting the replacement
    identity undeclared economic, disclosure or custody authority;
21. deleting one complete Carrier database still permits discovery and
    resolution through a separately implemented and operated Carrier;
22. real Carrier, Messenger, executor, handoff, custody and payment Adapter
    failures are demonstrated in addition to unit, fuzz, race, crash, partition
    and platform tests; and
23. the TOS escrow acceptance profile recognizes the exact Provider Offer and
    finalized bound-wallet chain evidence only for the Quote-committed generic
    Agreement body, scoped obligation IDs, predicate IDs, target projections and
    profile descriptor; cross-Agreement/profile replay and weaker substitutes
    fail, while disabling TOS escrow leaves generic discovery, negotiation,
    trusted execution, private handoff, and supported direct payment operational.

Mocks and same-process happy paths are useful unit tests but are insufficient
for cross-host, custody, Carrier-independence, or production claims.

The reference source-loss campaign is
[`../scripts/run-independent-carrier-source-loss.sh`](../scripts/run-independent-carrier-source-loss.sh).
It compiles and starts the standalone Gateway and Messenger Carrier processes,
publishes one exact signed Intent through both independent admission/action
stores, verifies both copies, stops the Gateway Carrier and removes its entire
active database, then verifies the exact digest through the Messenger Carrier
both before and after a Messenger restart. It retains all logs and removed
store bytes in the named acceptance artifact directory for independent review.

The complete local campaign is
[`../scripts/run-openfox-autonomous-earning-three-node.sh`](../scripts/run-openfox-autonomous-earning-three-node.sh).
It first checks that all three configured TOS JSON-RPC endpoints are live, runs
the independent codec verifier and the security-critical repository suites,
proves the frozen escrow build and sandbox behavior, executes the independent
Carrier source-loss campaign, and finally runs the real two-Agent Paid Demand
V2 lifecycle against the three nodes. Its private artifact directory contains
per-stage logs and a manifest of exact repository commits, worktree state,
endpoints, completion time and result. The manifest deliberately excludes
vault material and private keys.

The controlled three-seller execution and local-network settlement campaign is
recorded in
[`OPENFOX_THREE_AGENT_EARNING_PILOT_REPORT.md`](OPENFOX_THREE_AGENT_EARNING_PILOT_REPORT.md).
That report preserves the narrower acceptance boundary between a successful
seller pilot and a production claim of unattended customer acquisition.

## 15. Explicit non-goals

This roadmap does not require:

- a new opcode, API, state machine, or contract for each trade category;
- a universal business taxonomy or universal task schema;
- a central marketplace, order book, global latest head, winner, or trust
  score;
- a mandatory TOS asset, escrow profile, Evaluator, Receipt, or market
  application;
- one universal stake, fee, bond, proof-of-work algorithm, or global reputation
  mechanism for every operation family;
- one global clock, exchange-rate oracle or valuation authority;
- reinterpreting Gift as purchase or Agreement settlement;
- allowing remote Intent content or model output to choose credentials,
  signing, execution, disclosure, or payment;
- TOS authority over external chains, fiat, custodial dashboards, or market
  databases; or
- modifying every repository before a smaller read-only or trusted phase can
  be implemented and honestly described.

## 16. Immediate implementation order

The recommended first PR sequence is:

1. `tos-service-spec`: freeze the Phase 0 wire objects, body-bound authorization
   predicates and evidence profiles, non-circular Agreement targets, the
   semantic action registry and exact-byte vectors, operation admission, private
   handoff, authority, recovery and conformance vectors;
2. `tos-service-spec`: implement the standalone code-independent reference
   verifier and record its language/toolchain boundary;
3. `tos-service-protocol`: implement the production canonical codec/verifier,
   Agreement predicate/evidence validation, registry-derived action/execution
   IDs, clients, admission/handoff helpers and cross-verifier fixtures;
4. `openfox`: implement read-only Inventory, privacy-preserving Collector,
   filtering, retrieval, economics, persistence, observability and operator
   explanations under default-off side-effect gates;
5. one complete Carrier: implement admission, bounded signed-card
   publish/search/subscribe, selective content retrieval, cursors, provenance,
   resource telemetry and recovery;
6. `openfox`: implement the personal and shared Owner Economic Action Authority
   plus transactionally coupled aggregate Portfolio, registered semantic action
   IDs, proof-carrying writer fences, resolved mandate/approval validation and
   atomic blocking-dependency cycle admission;
7. `tos-messenger`: implement writer-fenced contact, typed Agreement actions,
   profile-qualified acceptance evidence transport, `ResolveAction`, and the
   optional complete Messenger Carrier profile if it will count as a Carrier;
8. `openfox` plus one handoff transport and executor: implement authenticated
   private content, aggregate reservation, one-shot local Gate, delivery,
   pause/drain/takeover/reconciliation and honest unpaid accounting;
9. custody: implement one Agreement-bound direct-payment Adapter, independent
   writer-generation enforcement and exact evidence resolution;
10. add canonical billing, mixed-version migration and a second settlement
    Adapter;
11. implement autonomous publication and pricing with stale-evidence withdrawal,
    rate, margin, exposure, disclosure, TTL and revision controls;
12. add the optional TOS escrow Adapter only after its specialized private
    ingress and independent security gates pass; and
13. add the second independently implemented and operated Carrier, durable
    multi-engagement scheduling, subcontract recovery, failure injection,
    reproducible acceptance manifests and bounded learning before claiming
    continuous autonomous business.

The follow-on trusted-capability and owner-control sequence is:

14. `tos-service-spec`: freeze executable-artifact identity, permission,
    requirement, sourcing decision, evaluation, admission, revocation,
    promotion, capability-use, report, projection, device-session and owner-
    command objects, plus their registries, errors, vectors, a code-independent
    standalone reference verifier, and Gate S/M profiles;
15. `tos-service-protocol`: implement the production codec/verifier and a
    cross-verifier CI job that reproduces every identity and failure class
    against the independent `tos-service-spec` verifier;
16. `openfox`: enforce the consequential-use safety ceiling, build the
    append-only Inventory, reuse-first coordinator, quarantine, admission,
    promotion and revocation path, then pass Gate S;
17. `openfox`: add deterministic accounting/report queries, the four maintained
    report Skills, and the durable owner projection;
18. `openfox` server and `openfox/web`, followed by future
    `tosnetwork/openfox-ios` and `tosnetwork/openfox-android` repositories:
    release read-only projection convergence, then the shared replay-safe owner
    command path and Gate M; these two mobile repositories are additional to
    the seven-repository earning-loop count; and
19. treat the existing local campaign runs as diagnostic input, then rerun
    formal Campaigns 1--4, cross-host Campaign 5, and arm's-length Campaign 6
    after Gates S/M, without promoting a campaign result into authority.

This order preserves a useful result at every phase while keeping all economic
side effects disabled until their exact authority, fencing, recovery, and
evidence contracts are implemented and tested.
