# OpenFox Autonomous Earning — Cross-Repository Design

**Status:** incubation design; implementation and external acceptance pending

**Blocking status:** read-only discovery may proceed after its minimal schema
freeze, but paid-demand-sourced Provider Offer acceptance, execution, and
automatic commercial action remain blocked until the D2 multi-source/
independent-verifier gate, complete mutation-bound `BuyerHandoffProfile`, typed
Quote-binding body and Provider proof, portable market-delegation proofs,
Provider-wide fenced admission, per-Offer deterministic acceptance, and proof-
of-possession private-input delivery, strict deadline/release-pipeline
enforcement, a zero-bounce initial wallet-request proof with replay-aware
recovery, and fresh same-claim runner-start preflight are implemented. The
existing Capability-first commercial rail remains available under its own
acceptance status and schema-1 rules.

**Protocol:** `tos_service_v1`

**Product goal:** an owner-controlled Agent that continuously finds diverse
profitable tasks, competes for work, executes accepted work through approved
skills and capacity, proves delivery, receives payment, and keeps operating
without exceeding deterministic safety, budget, or authority limits.

This document defines the cross-repository delivery boundary for that goal. It
does not freeze a new wire surface, open the roadmap Expansion Gate, claim that
competitive task markets already exist, or replace any authority in the
current Accepted Quote, escrow, Receipt, and settlement lifecycle.

Related specifications:

- [`PRODUCT_STRATEGY.md`](PRODUCT_STRATEGY.md)
- [`ARCHITECTURE.md`](ARCHITECTURE.md)
- [`SETTLEMENT.md`](SETTLEMENT.md)
- [`SOFTWARE_WORK_EXECUTION_V1.md`](SOFTWARE_WORK_EXECUTION_V1.md)
- [`NATIVE_EXECUTION_GATE_V1.md`](NATIVE_EXECUTION_GATE_V1.md)
- [`OPENFOX_ECONOMIC_BRIDGE_V1.md`](OPENFOX_ECONOMIC_BRIDGE_V1.md)
- [`OPENFOX_AUTONOMOUS_MESSENGER_ECONOMY_PLAN.md`](OPENFOX_AUTONOMOUS_MESSENGER_ECONOMY_PLAN.md)
- [`AGENT_PAID_DEMAND_DISCOVERY_V1.md`](AGENT_PAID_DEMAND_DISCOVERY_V1.md)
- [`PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md`](PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md)
- [`AGENT_ECONOMY_METRICS_V1.md`](AGENT_ECONOMY_METRICS_V1.md)
- [`ROADMAP.md`](ROADMAP.md)

External design influences:

- Virtuals Protocol's
  [Agent Commerce Protocol research page](https://app.virtuals.io/research/agent-commerce-protocol)
  and
  [2025 paper](https://s3.ap-southeast-1.amazonaws.com/virtualprotocolcdn/Agent_Commerce_Protocol_Virtuals_0759d11d1d.pdf),
  for explicit client/requester, Provider, and Evaluator roles, agreement
  proofs, and a job-scoped commercial lifecycle in that earlier ACP iteration;
- the current
  [ACP concepts and architecture](https://whitepaper.virtuals.io/acp/acp-concepts-terminologies-and-architecture),
  as a distinct later iteration, for event-driven Agent integration, typed
  requirements, and extensibility; their wire objects are not combined here;
  and
- draft [ERC-8183](https://eips.ethereum.org/EIPS/eip-8183), for a minimal
  escrowed Job, explicit submission commitment, required Evaluator-gated
  completion with an optional attestation reason, expiry refund, and provider-
  later/bidding composition.

These are design inputs, not inherited authority or wire compatibility. This
architecture intentionally does not inherit Virtuals-hosted Registry, search,
chat, event, account, ranking, platform-fee, administrator, or upgrade
dependencies. ERC-8183 remains a draft and its single Evaluator is an explicit
oracle, not proof that a subjective deliverable is correct.
The linked materials were reviewed on 2026-08-24. Later ACP or ERC revisions do
not silently change this design; adoption requires an explicit TOS profile and
compatibility/security review.

For paid-demand publication, verification, distribution, Provider Offers, and
local buyer selection,
[`AGENT_PAID_DEMAND_DISCOVERY_V1.md`](AGENT_PAID_DEMAND_DISCOVERY_V1.md) is the
specialized governing design. For the versioned handoff from one exact Offer
into the existing Accepted Quote rail, private input, and commercial recovery,
[`PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md`](PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md)
governs. Both prevail over any abbreviated summary here.
The OpenFox-local projection and operator behavior are expanded in
[`OPENFOX_AUTONOMOUS_EARNING_IMPLEMENTATION_PLAN.md`](OPENFOX_AUTONOMOUS_EARNING_IMPLEMENTATION_PLAN.md);
this document does not define an alternate signing order, state machine, or MVP
gate.

## 1. Executive decision

This outcome is not an `OpenFox`-only change.

OpenFox owns the autonomous business loop, but it must consume independently
verifiable market, execution, authorization, and settlement boundaries owned
by other repositories. Implementing every missing piece inside OpenFox would
create a private marketplace, duplicate protocol codecs, blur custody, and make
earnings depend on an application database rather than finalized TOS state.

The minimum architecture spans:

1. `tos-service-spec` for normative schemas, invariants, state ownership, and
   frozen conformance vectors;
2. `tos-service-protocol` for canonical construction, verification, clients,
   provider SDKs, and portable recovery;
3. `tos-service-gateway` for replaceable demand discovery and negotiation
   transport;
4. `openfox` for opportunity acquisition, matching, economics, deterministic
   policy, orchestration, local accounting, and operator controls;
5. `tos-ai` for implementation of spec-defined execution profiles, capacity,
   reservations, isolation, metering, validation evidence, and result
   production;
6. `tos-messenger` where authenticated negotiation, owner approval, or direct
   buyer/provider delivery uses Messenger; and
7. `tos` for generic networking primitives and canonical Agent, Accepted
   Quote, escrow, Receipt, and settlement contracts, plus custody tooling for
   purpose-limited signing, Provider-wide writer fencing/admission, and
   broadcast.

The D1/D2 read-only discovery slices avoid a chain change. Open paid-demand
listings and propagation remain bounded, signed, non-canonical pre-acceptance
artifacts. The binding sufficiency review has established that the current
Accepted Quote cannot express all facts required for D3: it omits buyer Agent,
Demand Mutation, Provider Offer, task input/source, and task-level
validator/evidence terms. D3 therefore requires a typed, reconstructible
versioned binding in the existing Accepted Quote, corresponding escrow parser/
code identity, a recoverable `pending_acceptance` state and bound-wallet
`accept` transition, resolver, Native Execution Gate comparison, and safe
handoff before paid-demand-sourced execution. The extra state prevents a third-
party deployment of the public deterministic StateInit from consuming buyer
acceptance. The existing Receipt remains bound
transitively through its Quote commitment and current input/source/result
fields unless a separate review proves a concrete gap. No application journal
or parallel settlement state may supply the missing authority.

## 2. Current baseline and exact gaps

### 2.1 What already exists

The current repositories already provide much of the commercial spine:

- finalized Agent and Capability identity and version resolution;
- derived Capability discovery;
- Quote Proposal construction and complete-preimage validation;
- finalized Accepted Quote and stablecoin escrow;
- a provider-side shared Native Execution Gate;
- bounded machine-checkable software execution in `tos-ai`;
- canonical software-work Receipt construction and objective release/refund;
- finalized provider-wallet settlement verification;
- OpenFox buyer/provider integration, policy-gated purchasing, skills, an
  AgentLoop, event provenance, isolation, schedules, and local evolution
  mechanisms; and
- economic metrics derived from authenticated terminal settlement records.

These pieces prove that OpenFox can participate in a paid lifecycle. They do
not yet form a general autonomous earning business.

### 2.2 Development gaps

The following are missing product or engineering capabilities, not deployment
configuration:

- proactive discovery of buyer-published paid demand in addition to existing
  Capability-first provider sales and Capabilities that OpenFox may purchase;
- independent verification and deduplication of Demand Mutation chains from
  multiple sources;
- typed matching between task requirements, installed skills, available
  capacity, credentials, legal policy, and evidence capability;
- exact-asset revenue, cost, risk, locked-capital, and expected-profit models;
- portfolio-level exposure, concurrency, counterparty, and loss limits;
- deterministic Provider Offer/later-bid authority and idempotent negotiation
  journals;
- purpose-limited market delegation with portable historical authority,
  current authorization-eligibility, and acceptance-time revocation-ordering
  verification;
- typed Quote-binding convergence connecting signed Demand context, Provider
  Offer authorization, buyer Agent-to-wallet context, task input/evidence, and
  the buyer-wallet-authenticated versioned escrow `accept` transition into
  finalized commercial state;
- deterministic one-Offer/one-existing-Quote derivation, without claiming
  demand-wide exclusivity across independently funded Offers;
- buyer-push private-input delivery to a Provider-bound ingress;
- competitive pricing and offer revision without allowing model prose to
  authorize a commitment;
- private portfolio and runtime-capacity reservation after canonical body/action
  construction and before Provider authorization;
- multiple bounded execution profiles beyond the current pinned software-work
  profile;
- task-specific validation, evidence generation, result submission, objective
  refund, and recovery adapters;
- finalized revenue attribution, cost allocation, realized P&L, receivables,
  and unresolved-exposure accounting inside OpenFox; and
- a continuous operating loop that can restart, pause, drain, revoke, and
  explain every economic action.

### 2.3 Deployment and acceptance gaps

The following do not primarily require a new product architecture, but remain
necessary before production autonomy may be claimed:

- independent buyer, provider, resolver, and Gateway operators;
- recurring public-network paid demand and useful Capability supply;
- production custody, delegated limits, recovery, revocation, monitoring, and
  accounting procedures;
- real fee, latency, failure, refund, and utilization observations;
- public conformance evidence across independent implementations;
- production capacity and credential provisioning for each enabled skill; and
- the external Gate D through Gate G evidence required by `ROADMAP.md`.

No deployment setting can manufacture the missing discovery, bidding,
economics, portfolio policy, or generalized execution code. Conversely, code
completion cannot manufacture independent demand, production custody, or gate
acceptance.

## 3. Product and authority boundaries

### 3.1 Owner-controlled autonomy

“Autonomous” means that an owner may install a bounded mandate under which the
Agent can repeat previously authorized classes of action without asking for
each instance. It does not mean that the Agent can expand its own authority.

An owner mandate fixes at least:

- exact TOS network domain;
- earning Agent and allowed execution identities;
- allowed task and execution profiles;
- allowed assets and minimum revenue or profit rules;
- maximum bid, fee, external-spend, locked-capital, and loss exposure;
- per-task, counterparty, rolling-window, and concurrent-work limits;
- allowed skill, model, endpoint, credential, and network profiles;
- approval thresholds and expiration;
- custody signer or delegated authorization identity; and
- pause, drain, revoke, and emergency-stop behavior.

OpenFox and model output may propose a task interpretation, plan, price, or bid
text. A deterministic policy gate must authorize the exact structured action.
Neither a task description nor a conversation signature creates wallet,
execution, credential, or settlement authority.

### 3.2 Existing canonical lifecycle remains authoritative

Pre-acceptance market objects are negotiation inputs:

```text
paid-demand listing -> bid/offer -> negotiation -> buyer selection
```

They do not prove funding, acceptance, execution authority, successful work,
or payment. The authority transition remains:

```text
active Demand Mutation + Provider fields + durable Offer identity
  -> unsigned typed PaidDemandQuoteBindingBodyV1
  -> Provider authorization creates one Provider Offer
  -> buyer verifies and selects the exact Offer locally
  -> deterministic versioned escrow starts in pending_acceptance
     and carries the versioned Quote
  -> bound buyer wallet finalizes its on-chain accept transition
  -> later exact stablecoin notification creates funded state
  -> Native Execution Gate
  -> bound execution and evidence
  -> canonical Receipt
  -> finalized release or refund
  -> independently resolved provider-wallet outcome
```

Finalized TOS state wins over every OpenFox journal, Gateway index, Messenger
conversation, provider database, local metric, and model conclusion.

### 3.3 Buying and earning are separate control planes

OpenFox's current opportunity coordinator evaluates Capabilities that OpenFox
may buy. Autonomous earning evaluates demand for work that OpenFox may sell.
They must remain separate even when one Agent uses both:

| Concern | Buying | Earning |
|---|---|---|
| Cash-flow direction | outbound funding | inbound provider revenue |
| Primary exposure | spend and refund risk | delivery cost, penalties, and locked capacity |
| Market action | request/accept Quote | advertise demand response, send Provider Offer, or later bid |
| Execution role | buyer/client | provider/worker |
| Terminal accounting | expense or purchased asset | settled revenue and allocated cost |

They may share finalized resolvers, canonical codecs, custody clients, event
infrastructure, and accounting primitives. They must not share a permissive
policy decision merely because the same owner operates both roles.

### 3.4 Protocol, participant, and market application are separate

The target architecture has three independent product layers:

| Layer | Responsibility | Must not become |
|---|---|---|
| permissionless discovery data plane | carry and index public Capability references and signed Demand Mutations through public channels, Storage, DHT, Gateways, and independent indexes; carry buyer-specific Provider Offers only through approved direct negotiation transports | a globally complete order book or acceptance authority |
| TOS commerce protocol | bind exact parties and terms into the existing Accepted Quote, escrow, Gate, execution, Receipt, release/refund, and finalized settlement lifecycle | a search engine, ranking service, customer-support desk, or centrally operated labor market |
| optional market applications | provide listings, managed matching, recommendations, curation, moderation, KYC, fiat workflows, support, advisory/manual dispute services, and application-specific fees | a required market-operated identity directory, hosted catalog, event source, evaluator, or settlement database |

An UUMIT-like centralized market may offer a strong user experience and operate
its own private database. It participates by emitting, carrying, or consuming
portable protocol artifacts and by directing the parties to the same TOS
commercial rail. OpenFox may use it as one source under local policy, but must
not require it, treat its ranking as proof, or lose accepted commercial history
when it disappears.

A Provider Offer is portable and independently verifiable. Its signature
authorizes exact inclusion in the deterministic Quote/StateInit, so a selected
or predeployed Offer may become publicly observable before buyer acceptance.
That does not authorize an index to republish it as general discovery inventory;
losing Offers remain direct/private unless separately disclosed. Public-
inventory publication requires a separate profile and both parties' explicit
authorization. Finalized Native Registry state for Agent and Capability accounts
remains canonical protocol authority; no market-operated directory or account
system may replace it.

This boundary lets centralized markets compete on operations and service while
TOS remains neutral infrastructure. A market may charge a separate membership,
matching, support, or fiat-service fee under its own disclosed terms. Any fee
deducted from, split from, or routed through TOS settlement requires a supported
pre-acceptance Quote/escrow profile. Objective V1 has no platform-fee recipient
or payout split, and a market database cannot change an accepted price,
evaluator, or payout. No canonical TOS Work Square or market operator is
required.

### 3.5 ACP-derived opportunity and Commerce Job projections

ACP demonstrates that Agent developers benefit from a small role-aware Job
model even when the underlying verification and recovery logic is complex. An
OpenFox instance or SDK may expose that convenience through two participant-
local, rebuildable read models. TOS does not require a hosted event server,
globally meaningful cursor, or canonical opportunity feed.
Unlike ERC-8183, whose Job exists in `Open` before funding and may initially
have no Provider, a TOS Commerce Job begins only after one schema-valid Accepted
Quote fixes both parties and terms. This is a deliberate semantic divergence,
not an ERC state alias.

For the Demand-first lane, pre-acceptance discovery remains this Opportunity
projection:

```text
OBSERVED -> OFFER_PREPARED -> OFFERED -> QUOTE_ACCEPTED

OBSERVED | OFFER_PREPARED
  -> WITHDRAWN | EXPIRED | REJECTED

OFFERED
  -> WITHDRAWAL_OBSERVED -> CANCELLATION_RESOLVING
  -> CANCELLATION_RESOLVING(expiry_observed)

CANCELLATION_RESOLVING
  -> QUOTE_ACCEPTED | WITHDRAWN | EXPIRED

Any non-terminal pre-acceptance state
  -> AMBIGUOUS(origin_state, operation, action_id)
```

The Capability-first lane keeps its existing finalized Capability/version and
complete-preimage Quote-Proposal projection. It has no Demand Mutation or
Provider Offer key and must not be forced into the state machine above. The two
lanes converge only at their schema-valid Accepted Quote.

The Commerce Job starts only when one exact Quote becomes accepted under its
schema-specific rule:

```text
QUOTE_ACCEPTED
  |-> UNFUNDED_EXPIRED
  `-> FUNDED
       -> EXECUTING
       -> RESULT_READY
       -> SETTLEMENT_REQUESTING
       -> SETTLEMENT_PENDING
       -> RELEASED

Any state from FUNDED through RESULT_READY
  -> REFUND_RESOLVING -> REFUNDED

SETTLEMENT_REQUESTING
  -> REFUND_RESOLVING(only after exact release action is resolved as not
       accepted and finalized escrow is funded at/after refund)

SETTLEMENT_PENDING
  -> SETTLEMENT_REQUESTING(bounce recovery before refund; operator/resolver
       only; SAME_ACTION_ONLY; old_or_new_query_may_win)
  | REFUND_RESOLVING(bounce recovery at/after refund after release is
       impossible; operator/resolver only)

REFUND_RESOLVING
  -> REFUND_RESOLVING(bounce recovery; operator/resolver only;
       same action; old_or_new_query_may_win)

Any non-terminal state
  -> AMBIGUOUS(origin_state, operation, action_id)
  -> that operation's legal predecessor or successor
```

Before acceptance, identity is the network plus exact Demand/Mutation and, when
present, exact Provider Offer digest. Different Offers are never merged. Quote
acceptance terminalizes that immutable-key Opportunity row with an
`accepted_job_ref` and creates a separate Commerce Job row keyed by
`(quote_commitment, escrow_address)`. Neither row is rekeyed. A local Job ID is
correlation only and cannot replace either key; one derivative event names one
immutable projection key. The local log emits linked `opportunity_accepted` and
`commerce_job_created` events rather than one event that changes key.

Each row carries its evidence class and exact underlying Demand, Offer, Quote,
escrow, Gate claim, Receipt, action, transaction, and finalized-checkpoint
references. The projection can be deleted and rebuilt from the participant's
durable journal plus independently verified artifacts and resolvers without
changing commercial truth. `AMBIGUOUS` is a recovery overlay, never a terminal
commercial outcome. Once an Offer is authorized, a withdrawal or expiry is
terminal only after `CANCELLATION_RESOLVING` proves that no concurrent accepted
Quote exists; an observation alone cannot release the reservation.

The journal may be bounded only through verified compaction. An atomically
durable reducer snapshot must bind its schema version, journal-head digest,
last local sequence, source/resolver checkpoints, and every unresolved action,
artifact, evidence, and authority reference needed for replay. Compaction keeps
that snapshot and all referenced immutable objects before deleting its covered
prefix; restart verifies the head and replays the retained tail. Without those
records, the implementation must report retention-limited history rather than
claim deterministic rebuildability.

The OpenFox implementation retains detailed internal states for reservation,
writer fencing, input ingress, execution, accounting, and crash recovery. These
coarse projections give SDKs, CLIs, models, and operators a stable advisory
surface. Role and verified state constrain which actions may be proposed;
deterministic policy, custody, the Gate, and finalized state still authorize
every effect.

ACP's authoritative `Submitted` transition is not copied into objective
software-work V1. `RESULT_READY` means only that the Provider has durably
constructed the canonical Receipt and query-independent semantic release
template and digest. `SETTLEMENT_REQUESTING` covers the unique semantic release
action, its exact query-specific signed intent attempt, and ambiguity
resolution. Only a finalized resolver proving the exact escrow is
`release_pending` creates `SETTLEMENT_PENDING`; that is V1's closest analogue to
ACP `Submitted`, but it already begins objective payment transfer rather than
waiting for an Evaluator. A future Evaluator-enabled profile requires a new
versioned on-chain `submitted_pending_evaluation` state. V1 does not reinterpret
the frozen schema-1 escrow or create a second settlement rail.

Once `SETTLEMENT_REQUESTING` records or broadcasts a release action, arrival of
the refund time alone cannot switch to refund. The exact action must first be
resolved as not accepted, including an authenticated initial bounce when
applicable, and finalized escrow must again be `funded` at or after the refund
boundary. Otherwise the projection remains
`AMBIGUOUS(origin=SETTLEMENT_REQUESTING, SAME_ACTION_ONLY)`.

After bounce, frozen escrow V1 forgets the pending query, so any public old
release/refund attempt can be permissionlessly replayed from `funded` and race
an honest new attempt. All such queries remain children of the same semantic
action; distinct client query IDs are not contract replay protection, and
automatic paid-demand recovery does not retry after bounce.

### 3.6 Deadline-safe execution and extension classes

ACP makes submission explicit; TOS must also prove that a Provider admitted
early enough to reach that boundary before the objective refund becomes
available. The paid-demand successor therefore commits acceptance, funding,
input-delivery, execution-admission, execution-completion, refund, and nonzero
release-pipeline-margin values. It also commits the exact effective duration,
deterministically derived as the minimum of the exact signed Mutation's maximum
and rounded-up manifest limit and enforced by the runner, plus the maximum
preflight-to-start delay. A later Mutation, withdrawal, or feed head cannot
alter an accepted purchase. Exact positive
`acceptance_to_funding_margin_seconds` covers latest-valid
acceptance through its finality observation and exact funding-notification
acceptance; `funding_to_input_margin_seconds` covers latest-valid funding
through finality observation, challenge/upload/verification, and atomic durable
input acceptance; and `input_to_admission_margin_seconds` covers record and byte
verification, current finalized authority resolution, and atomic Gate claim
publication after latest-valid input acceptance. Checked arithmetic requires
each complete pipeline to fit before its next deadline. Checked ordering must
also reserve the execution duration and delay plus bounded
objective validation; evidence/report and Receipt construction; query-specific
signing and initial release inclusion; and definitive downstream acceptance of
the initial wallet request without bounce, strictly before the refund boundary.
Frozen escrow V1 clears pending-query history on bounce, so old public attempts
can be replayed without a finite contract-enforced attempt bound. Automatic V1
therefore requires a proven zero-bounce initial release path. A future
settlement-critical successor may instead preserve valid pre-cutoff release
priority or a consumed-query generation across bounces, but it is not the V1
paid-demand binding. The Native Execution
Gate recalculates the remaining slack at admission and fails closed when it is
insufficient. The runner obtains a fresh same-claim preflight immediately before
first process start so queue, crash, or restart delay cannot consume the budget
silently. Every preflight also repeats the Gate's complete finalized authority
verification at coherent fresh monotonic checkpoints. It first current-quorum
resolves a finalized network anchor within frozen maximum age/head-lag bounds,
then proves escrow/Registry code, funded state and exact Quote, Agent non-
tombstone state, and Capability ownership/exact unrevoked version/manifest at
or through that anchor with required cross-shard order. Merely repeating an old
checkpoint is invalid. The fresh preflight is the linearization point for one
bounded start-authority ticket over that exact snapshot and anchor. An adverse
change finalized at or before the checkpoint blocks the ticket; one finalized
only afterward is non-retroactive while the runner starts no later than the
ticket's checked `start_not_after`. The original admission freezes nothing. It
may refresh only while durably `prepared` with no possible runtime side effect;
an expired ticket forces a complete recheck, and
uncertainty after the atomic `prepared -> starting` transition is execution
ambiguity, not permission to retry. A Receipt or local
`RESULT_READY` timestamp never extends the escrow deadline.
This proves release priority, not terminal payout latency: once the downstream
wallet request is accepted, `release_pending` blocks refund while finalized
credit resolution may complete later. If the target network cannot prove a
zero-bounce initial request, automatic V1 paid-demand execution stays blocked. A
priority-preserving alternative requires another Quote/escrow version and
review.

The private ingress atomically consumes the challenge, binds the immutable
bytes, and signs `InputAcceptanceRecordV1` under the Quote-bound ingress-
attestation key. The record binds conservative clock evidence and monotonic
journal high-water marks and proves
`input_accept_time_upper_bound <= input_delivery_deadline`. This is distinct
from the Gate's later
`admission_time_upper_bound <= execution_admission_deadline`; a timely durable
input may be admitted after its delivery deadline, but a new or backdated input
record may not be created then.

Extensibility is divided by authority rather than marketed as a generic Hook:

| Extension class | Examples | Required treatment |
|---|---|---|
| binding-only | additional portable provenance or display commitments | typed and versioned; cannot alter execution, custody, or settlement |
| execution-critical | a new input, validator, evidence, or runtime profile | committed before acceptance and explicitly understood by the resolver and shared Gate |
| settlement-critical | Evaluator decision, fee split, partial payment, challenge, or alternate refund rule | new Quote/escrow version and code hash, explicit transitions and deadlines, resolver and recovery support, independent conformance review |

An Evaluator that can cause or block payment is a settlement-critical oracle,
even when its interface looks like an application callback. Its identity or
quorum, evidence commitment, fee, decision schema, deadline, replacement,
challenge, and unavailable-Evaluator fallback must be fixed before acceptance.
Objective V1 contains no such authority; market reviews and buyer feedback are
advisory artifacts only.

## 4. Repository ownership

| Repository or component | Must own | Must not own |
|---|---|---|
| `tos-service-spec` | normative Demand Mutation, market delegation, Provider Offer, `PaidDemandQuoteBindingV1`, private-input, task/execution/validator/evidence schemas when approved; bounds; canonical encodings; authority/state-machine invariants; vectors; acceptance contract | runtime schedules, private policy, private credentials, mutable market indexes |
| `tos-service-protocol` | generated types; canonical encoders/digests; signature and finalized-state verification; negotiation, Accepted Quote, provider, Receipt, settlement, and recovery SDKs; conformance helpers | opportunity ranking, model planning, operator portfolio policy, custody secrets |
| `tos-service-gateway` | bounded searchable projection of non-expired demand; cursors; federation; rate limits; authenticated publish/withdraw/relay transport; explicit provenance and freshness; optional market-application adapter boundary with application-local metadata | canonical task acceptance, buyer solvency truth, ranking authority, custody, provider execution, settlement truth; platform account or order state presented as TOS authority |
| optional market application | branded work square, centralized accounts, managed matching, proprietary ranking, moderation, KYC, support, notification, fiat, and exact-byte protocol relay services | TOS Agent/Capability identity from login state; canonical acceptance, funding, Gate admission, Receipt, or settlement authority; satisfaction of source independence through correlated replicas |
| `openfox` | durable earning coordinator; source federation; verifier orchestration; skill/capacity matching; economics; pricing strategy; deterministic policy; owner-private process lock; Provider writer-lease client/recovery; Offer/later-bid journal; execution orchestration; local P&L; operator explanation and control | protocol codecs, chain truth, raw chain keys, task-selected authority, unrestricted tool execution |
| `tos-ai` | implementation/operation of spec-defined task, execution, validator, evidence and private-input profiles; deterministic estimates; durable body-bound runtime capacity leases; bounded executors; metering; artifacts; execution replay protection | freezing normative profiles, market authority, economic policy, wallet custody, final settlement recognition |
| `tos-messenger` | paid-demand public-channel and direct-offer profiles; authenticated Agent conversations; replay-safe transport; verification/synchronization/persistence integration over TOS networking; device/session custody | generic DHT/Overlay/RLDP/Storage primitives, market ranking, Quote/escrow authority, execution authority, wallet authority from prose |
| `tos` / contracts | generic DHT/Overlay/ADNL/RLDP/Storage primitives; canonical Agent delegation; existing Accepted Quote, escrow, Receipt, objective release/refund, transfer, and final settlement transitions; versioned Quote/escrow parser support for the paid-demand binding | task search, bid ranking, private cost models, OpenFox objectives, execution planning, demand-wide winner selection in V1 |
| `tosctl` or equivalent custody boundary | Provider-wide exclusive writer lease; rollback-resistant generation and issuance ledger; unresolved Demand-tuple and aggregate-exposure admission across shared instances/keys/mandates/runtimes; stable-action conflict/replay handling; semantic confirmation; delegated signing; broadcast; ambiguous-submit resolution; revocation integration | opportunity selection, model prompts, execution or accounting policy; public market-artifact fields for private admission state |
| `doc` | ecosystem-level product explanation synchronized after the design is accepted | normative schemas, implementation status without evidence, runtime behavior |

Any canonical field or digest addition starts in
`proto/tos/service/v1/native.proto` in this repository. Implementations must not
create a competing JSON, database, or application schema and later treat it as
protocol authority.

## 5. End-to-end architecture

```text
Demand-first entry
  buyer publishes a bounded Demand Mutation
  -> permissionless carriers and optional market-application Gateways
  -> OpenFox federates, verifies, matches, prices, and returns one Provider Offer
  -> paid-demand binding and schema-successor acceptance

Capability-first / offering-first entry
  Provider publishes a finalized Capability/version and immutable manifest
  -> replaceable Gateway or optional market application presents it
  -> buyer obtains and verifies a complete-preimage Quote Proposal
  -> frozen schema-appropriate Capability-first acceptance

Both lanes
  -> exact Accepted Quote and deterministic escrow under the lane's schema
  -> exact finalized stablecoin funding
  -> the same Native Execution Gate, bounded execution, Receipt, and settlement

OpenFox demand-first earning scout
  -> federated cursor reads
  -> historical signature + current delegation authorization eligibility
  -> observed mutation-chain integrity, source freshness, provenance, and bounds
  -> never claim an off-chain globally complete mutation head
  -> direct finalized Agent/Capability/network verification
  -> typed skill + evidence + capacity match
  -> integer economics + portfolio exposure calculation
  -> deterministic mandate decision

OpenFox provider
  -> load the active Mutation's complete BuyerHandoffProfile
  -> choose one durable Offer identity and Provider terms
  -> construct one unsigned typed PaidDemandQuoteBindingBodyV1
  -> reserve private capacity and pass Provider-wide admission
  -> sign that body to create one single-acceptance Provider Offer
  -> resolve ambiguity before any retry
  -> buyer verifies and selects the exact Offer locally
  -> deterministic escrow may be deployed only into pending_acceptance
  -> bound buyer wallet finalizes the accept transition carrying the binding
  -> later exact stablecoin notification creates funded state

private input boundary
  -> buyer pushes committed bytes to Offer-bound Provider ingress
  -> ingress verifies buyer proof of possession, challenge, digests, media and
     archive bounds
  -> one atomic InputAcceptanceRecordV1 binds immutable bytes and proves the
     conservative input-accept upper bound met the delivery deadline

tos-ai execution boundary
  -> existing Native Execution Gate validates every paid-demand binding field
  -> Gate claims the existing (Quote commitment, escrow address) slot once
  -> execute approved profile once
  -> validate output and produce immutable evidence

protocol + custody boundary
  -> request one semantic Receipt release action with attempt-level recovery
  -> resolve finalized escrow and provider-wallet state

OpenFox accounting
  -> recognize revenue only from finalized provider credit
  -> allocate measured and reserved costs
  -> update realized P&L and bounded strategy observations
  -> release capacity and continue, pause, or escalate
```

Every arrow crossing a repository boundary uses a typed interface with bounded
inputs, a stable idempotency identity, explicit network domain, explicit asset
identity where monetary, and an error disposition that states whether retry is
safe, forbidden, or requires authoritative resolution first.

## 6. Market negotiation profile

The transport-neutral paid-demand envelope, public-channel carriage,
DHT/Overlay/Storage boundary, replaceable indexing, federated discovery,
direct Provider Offer, abuse controls, and work-square projection are defined
in [`AGENT_PAID_DEMAND_DISCOVERY_V1.md`](AGENT_PAID_DEMAND_DISCOVERY_V1.md).
This section retains only the cross-repository earning-control-plane summary.

### 6.1 Why a demand profile is needed

Current Capability discovery lets buyers find a Provider's published
Capability and can produce Provider revenue through the existing Capability-
first rail. It does not answer the complementary question, “which buyer
currently wants work that I can profitably perform?” The paid-demand profile
adds proactive buyer-demand acquisition; it does not replace Capability-first
sales.

The initial profile should support fixed-price, objectively verifiable
software work. Competitive bidding is added after fixed-price offering works
end to end. General job boards, subjective arbitration, subcontracting, GPU
markets, and cross-chain payments remain later profiles.

### 6.2 Pre-acceptance artifacts

The design requires the following conceptual artifacts. Their exact fields and
canonical encoding are not frozen by this document:

- **Demand Mutation** — buyer identity, monotonic sequence, predecessor, kind
  (`active_revision` or `terminal_withdrawal`), task/input/evidence terms,
  exact asset, deadlines, and one complete `BuyerHandoffProfile`. That profile
  fixes signed Demand authorization context, the exact settlement wallet already
  represented by existing escrow terms, portable authority reference, and
  upload proof-of-possession key before any Provider signature.
- **Provider Offer** — the Provider combines the exact active Mutation,
  preallocated Offer identity, and Provider-owned terms into one unsigned
  `PaidDemandQuoteBindingBodyV1`. Its `provider-offer.sign` proof creates the
  exact Offer. The body fixes Provider/Capability, price, task/input/evidence,
  transport/private-input and ingress-attestation profile, pre-input and
  execution/release timing margins, existing-rail equality commitments,
  `max_acceptances = 1`, and expiry. Private writer/reservation data never
  enters public bytes.
- **Selection Notice** — optional non-canonical buyer notice of a locally
  selected Offer. It proves neither Accepted Quote finality, funding, nor global
  exclusivity.
- **PaidDemandQuoteBindingV1** — the exact body plus Provider proof, carried by a
  versioned existing Accepted Quote. It is an extension payload, not separate
  accepted state. The signed Demand establishes buyer Agent handoff context;
  permissionless deployment creates only `pending_acceptance`; the finalized
  escrow `accept` transition authenticated to the bound buyer wallet is
  commercial acceptance; later exact stablecoin notification is funding.

The exact Provider proof bytes are part of one exact Provider Offer identity.
A different valid signature over the same body is a different conflicting
Offer, not an alternate encoding that can silently derive another escrow. V1
adds no post-Offer buyer Agent signature to Quote/StateInit identity.

These artifacts are hostile, replayable Internet inputs. A valid signature
proves origin only. It does not prove funding, solvency, availability, quality,
selection, or payment. Messenger, Selection Notice, Gateway, or index data
cannot complete or rotate a missing buyer context; that requires a successor
active Demand Mutation and newly authorized Provider Offer.

The complete field mapping, Quote schema-version boundary, Provider admission,
private-input adapter, and existing-rail integration are governed by
[`PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md`](PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md).

### 6.3 Discovery semantics

A Gateway may index, rank, filter, paginate, relay, and expire demand. Every
result includes source Gateway, observation time, issuer, Mutation sequence and
digest, envelope digest, and cursor provenance. A Gateway must not claim that a
listing is accepted, funded, profitable, execution-authorized, or guaranteed to
settle.

OpenFox deduplicates identical envelope digests across Gateways, rejects
conflicting reuse of one buyer/demand/Mutation sequence, and retains source
provenance. Before offering it verifies historical signing authorization,
current Agent/delegation eligibility, and the integrity/freshness of the exact
observed Mutation chain. It never claims that no unseen successor, withdrawal,
or fork exists.

Before execution it ignores listing and Selection Notice state. It resolves the
versioned binding from the existing finalized Accepted Quote, separately proves
the exact funded escrow state, and enters the existing Native Execution Gate.

A known terminal withdrawal or fork fails closed before Offer signing. Absence
of one is only source-bounded evidence. Final acceptance relies on the signed
Demand context, exact Provider proof, and finalized escrow `accept` transition
authenticated to the bound buyer wallet. Permissionless deployment creates no
acceptance. Funding is the later existing stablecoin transition. Globally
enforceable pre-acceptance cancellation or exclusive Provider selection would
require a separate on-chain coordinator and is outside V1.

### 6.4 Provider Offer and later-bid safety

Every Mutation, Offer, Selection Notice, and input-delivery action has an
OpenFox-generated durable semantic identity outside model control. Exact replay
is idempotent; reuse for different content is a conflict.

An ambiguous network result never causes a blind retry. The coordinator first
queries the destination, peer, or exact deterministic escrow appropriate to the
action. If no reliable resolution operation exists, it remains ambiguous until
operator review or safe expiry.

One exact buyer-specific Provider Offer fixes `max_acceptances = 1` and maps to
one deterministic existing Quote commitment and escrow address. The buyer
cannot vary wallet, nonce, proof wrapper, input, deadline, or transport while
preserving that Offer identity. Different Provider Offers remain independent:
if the buyer finalizes and funds two, both are valid purchases. Buyer custody may
enforce a local preference to accept one, but no UI or protocol component calls
that a global winner.

OpenFox reserves capacity before signing and converts the reservation when the
Offer-specific Accepted Quote finalizes. The accepted-but-unfunded obligation
then follows the successor's version-dispatched funding predicate: the exact
notification is eligible in a handling transaction whose contract time is
`now <= funding_deadline`, and the acceptance-only
`accept_by == Quote.expires_at` cutoff is not reapplied after
`pending_acceptance -> awaiting_funding`. Funding before acceptance or after
the funding deadline is rejected; later finality observation does not change
the handling transaction's deadline result. Schema 1 keeps its frozen dual-
cutoff funding rule. If no funds were accepted, there is nothing to refund.
Execution begins only after exact funded finality, after which successful
release or objective timeout refund applies. An unaccepted Offer releases only
after its deadline and deterministic resolution of its exact escrow `accept`
transition.

Private input is buyer-pushed with proof of possession to the Provider ingress
bound by the Offer and then mapped into an existing task transport and shared
Gate claim. Remote task content never selects a Provider fetch target,
credential, or execution authority.

## 7. OpenFox earning control plane

### 7.1 Runtime modes

The earning runtime has authority modes ordered by maximum permission:

1. `off` — no polling or commercial action;
2. `observe` — discover, verify, match, estimate, and report only;
3. `recommend` — prepare an unsigned structured Provider Offer proposal or
   later-bid intent for owner approval, without canonical market body bytes or a
   custody/signature call; and
4. `policy-gated` — authorize a V1 Provider Offer, or a later frozen bid profile,
   only within exact policy, reservation, approval, and active-mandate limits.

`drain` is a separate admission state, not an authority mode. It accepts no new
work and may finish or safely unwind only obligations already accepted under the
current authority ceiling; entering it from a lower mode grants no execution or
signing power.

`policy-gated` is not unrestricted autonomy. The default is `off`; activation
requires an owner mandate and production readiness checks. The owner or a safety
control may downgrade authority at any time.

`recommend` never signs merely because a proposal is viewed or marked approved.
A distinct locally authenticated one-shot owner action may authorize one exact
proposal digest without changing the persistent mode. It must revalidate current
authority and terms and use the same body construction, reservation, fencing,
custody, and audit path as `policy-gated`; it grants no authority for a later
Offer.

### 7.2 Durable local state

The earning coordinator maintains the non-authoritative durable projection
defined in the
[`OPENFOX_AUTONOMOUS_EARNING_IMPLEMENTATION_PLAN.md`](OPENFOX_AUTONOMOUS_EARNING_IMPLEMENTATION_PLAN.md#durable-task-state-machine).
This overview does not define a shorter competing state machine. In particular:

- capacity is privately reserved before Provider authorization, converts to an
  accepted-awaiting-funding obligation after Offer-specific Quote finality, and
  becomes executable only after exact escrow funding finality;
- after Provider authorization, withdrawal, expiry, or local cancellation enters
  a resolving state and retains exposure until deterministic acceptance absence
  is proved;
- every ambiguous state preserves its origin phase, operation, and stable action
  ID, and only its phase-specific resolver may advance or compensate it; and
- execution, submission, Receipt, objective refund, and settlement recovery
  cannot regress to an earlier execution-eligible state, reopen a terminal
  state, or repeat an economic action.

No local transition creates a protocol fact. From acceptance onward, the
record stores immutable references to the paid-demand Quote-binding body,
Provider Offer proof, deterministic Offer-specific Quote commitment, escrow
address, separate funding state, execution identity, Receipt, and finalized
checkpoints. On disagreement, verified chain state wins and the local
projection is rebuilt or quarantined.

### 7.3 Typed skill matching

An installed skill declares a versioned descriptor:

- accepted task-profile IDs and versions;
- required input and output media types;
- required execution profile and resource classes;
- deterministic or bounded estimator support;
- allowed tools, models, credentials, hosts, and data classifications;
- validation and evidence profile produced;
- maximum duration and resource bounds; and
- code/artifact digest and operator approval status.

Free-form semantic similarity may rank candidates but cannot establish
eligibility. Eligibility requires an exact compatible descriptor, available
approved capacity, valid credentials, and a validator capable of producing the
evidence promised by the commercial terms.

Task content cannot install a skill, enable a plugin, select an MCP server,
choose a model, request a credential, change an allow-list, add network access,
or weaken isolation.

### 7.4 Economics

All monetary arithmetic uses exact asset identity and checked integer atomic
units. Values of different assets are never added without an owner-approved,
time-bounded conversion input that is recorded as non-canonical risk data.
Floating point is forbidden for authorization.

For one candidate, OpenFox computes at least:

```text
expected_revenue
  = offered_payment
  * conservative_success_probability
  * conservative_acceptance_probability
  * conservative_settlement_probability

expected_net_profit
  = expected_revenue
  - compute_and_energy_cost
  - model_api_tool_and_credential_cost
  - subcontractor_cost
  - network_bid_and_settlement_fees
  - retry_and_failure_allowance
  - failure_and_timeout_refund_reserve
  - capacity_opportunity_cost

worst_case_exposure
  = external_spend
  + non_refundable_execution_cost
  + locked_capital
  + refund_or_penalty_reserve
```

The actual implementation represents probabilities as bounded fixed-point
integers with specified rounding toward the conservative outcome. Every input
records its source, freshness, confidence class, and maximum validity period.
Missing or stale required cost inputs fail closed for every automatic
commercial action, including V1 Provider Offers and later bidding.

A V1 policy decision is one of `reject`, `recommend`, `approval-required`, or
`auto-offer`. A later frozen bidding profile may add `auto-bid`; unilateral
`auto-claim` remains disabled. The decision commits the exact assumptions,
price, fee cap, expiry, execution profile, proposed capacity/exposure
requirements, and mandate version used. An actual reservation identity is added
only on the exact owner one-shot or policy-gated path after canonical body
construction; reject/recommend/approval-required records have none.

### 7.5 Portfolio policy

Per-task profit is insufficient. The coordinator also enforces atomic reservations
over:

- total and per-asset worst-case exposure;
- daily and rolling-window external spend and realized loss;
- concurrent accepted, executing, and refund-resolving tasks;
- resource-class capacity and reservation headroom;
- counterparty and task-profile concentration;
- unresolved bids, result-ready records, settlement intents, and receivables;
- native TOS fee reserve; and
- mandatory liquidity and emergency-unwind reserves.

Two concurrent tasks cannot both consume the same remaining budget or capacity.
A local policy/reservation transaction protects one OpenFox process only and is
insufficient across processes, hosts, partitions, shared signer keys, mandates,
or runtimes. Before every Provider signature, the runtime capacity authority
must grant the exact body-bound lease and custody must enforce the current
Provider-wide writer fence, unresolved tuple, and aggregate exposure across the
entire Provider scope.

### 7.6 Continuous improvement boundary

OpenFox may learn non-authoritative strategy observations from verified
history, including estimate error, utilization, bid acceptance, execution
success, settlement latency, refunds, and realized margin. Such observations
may affect ranking or propose new policy.

Self-learning must never automatically:

- increase a budget, authority, credential, host, tool, or network allow-list;
- install or approve executable code;
- lower evidence or isolation requirements;
- convert unfinalized revenue into success labels;
- hide losses, refunds, or unresolved exposure; or
- publish a strategy change without versioning and rollback.

Promotion of a learned strategy requires offline replay, holdout evaluation,
adversarial tests, owner approval, a bounded canary, and a reversible version.

## 8. Execution, evidence, and settlement

### 8.1 Capacity and reservation

`tos-ai` exposes a local, authenticated, typed capacity interface. OpenFox may
ask for an estimate and request a bounded reservation. The response identifies
the execution profile, resource class, estimate version, validity deadline,
and reservation identity; it does not authorize chain or market actions.

After commercial acceptance, OpenFox must reconcile the reserved profile with
the complete finalized `PaidDemandQuoteBindingV1`, Accepted Quote, and escrow. A
mismatch causes rejection or a new Offer, not silent substitution. Reservations
never convert on permissionless deployment; they convert to accepted-awaiting-
funding obligations only on the Offer-specific bound-wallet `accept` transition
and Quote finality. Before Provider
authorization they may compensate on a verified terminal path; after Provider
authorization they remain held through withdrawal/expiry/cancellation
resolution and release only after the acceptance deadline plus deterministic
proof that no valid acceptance can still finalize.

### 8.2 Execution admission

Every transport must reach the existing shared Native Execution Gate after its
paid-demand binding parser is implemented. The Gate retains its current
`(Quote commitment, escrow address)` slot and independently verifies the
versioned binding, Accepted Quote, exact funded escrow, signed Demand context,
the buyer-wallet-authenticated escrow `accept` transition, Provider Offer
authorization, portable issuance references and acceptance-time revocation
ordering, Demand Mutation, Provider,
Capability/version, manifest, execution signer, transport binding,
input/source, validator/evidence, asset/amount, and deadlines. The current Gate
also verifies the exact signed `InputAcceptanceRecordV1`, immutable accepted
bytes, ingress-attestation key, conservative clock evidence/checkpoint, and
monotonic ingress journal high-water marks. Timely input acceptance and later
Gate admission use distinct deadline comparisons. The Gate is reusable
infrastructure; D3 adds binding validation rather than a second execution
authority.

The executor receives only provider-approved configuration. Remote tasks and
model output cannot select images, commands, environment variables, host
mounts, identities, runtime sockets, network exceptions, or resource limits.

### 8.3 Validation and evidence

Each task profile pairs execution with a validator and evidence profile. A
successful process exit is not sufficient unless the accepted terms define it
as the objective success rule. Validators operate over immutable inputs,
outputs, reports, artifacts, and recorded execution metadata.

Bulk evidence remains off-chain and content addressed. The Receipt binds the
exact digests and authorized execution signer. If promised evidence cannot be
generated or verified, OpenFox must not submit a successful Receipt.

### 8.4 Revenue recognition and P&L

OpenFox distinguishes:

- **quoted revenue** — non-authoritative offer value;
- **accepted-unfunded commitment** — finalized Accepted Quote awaiting exact
  funding, not a receivable or execution permission;
- **contracted receivable** — finalized exact funded escrow, still not earned
  cash;
- **settlement-requested receivable** — the exact release action is recorded or
  pending, still unresolved;
- **settled provider receipt** — authenticated finalized provider-wallet
  credit; and
- **realized profit** — settled provider receipt minus attributable recorded
  cost under one declared accounting policy.

Only finalized provider-wallet credit is recognized as settled revenue. A
Gateway callback, model statement, task status, Receipt signature alone,
release intent, escrow's unverified terminal flag, or wallet display cache is
insufficient.

Accounting retains exact asset separation. It reports native TOS fees apart
from stablecoin service receipts and never labels protocol metrics as audited
revenue, profit, or taxable income.

## 9. Security and failure invariants

1. OpenFox never stores or reconstructs an owner root key.
2. Signing occurs through a purpose-limited, revocable custody boundary.
3. Model or task text cannot directly authorize a Provider Offer, later bid, execution,
   credential use, Receipt, or settlement.
4. Gateway data is a discovery hint, never canonical authority.
5. Every candidate is network-bound, mutation-sequence-bound, digest-bound, and
   provenance-bearing; an observed active mutation never proves a globally
   complete off-chain feed head.
6. Every external side effect has a durable idempotency identity before it is
   attempted.
7. Ambiguous mutation results are resolved before retry; otherwise they remain
   visibly ambiguous.
8. Exact asset identity and checked integer arithmetic are mandatory.
9. Policy reservations and Provider-wide capacity/exposure admission are atomic
   across concurrent opportunities.
10. Acceptance precedes execution; objective validation precedes a successful
    Receipt; finalized provider credit precedes revenue recognition.
11. Task-selected tools, code, models, credentials, endpoints, or network
    exceptions are forbidden.
12. Self-learning cannot expand authority or erase adverse outcomes.
13. Pause stops new commitments; drain preserves safe handling of accepted
    obligations; revoke prevents new signatures and triggers reconciliation.
14. Restart rebuilds commercial truth from durable journals and independently
    verified finalized state.
15. An Offer identity or digest alone is not Provider consent. Every paid-
    demand Quote carries the exact Provider-authorized binding body and proof;
    permissionless deployment creates only `pending_acceptance`, and buyer
    commercial acceptance is the finalized escrow `accept` transition
    authenticated to the wallet fixed by the active Demand Mutation.
16. One exact Provider Offer maps to one deterministic versioned Accepted Quote
    and escrow identity. Alternate proof wrappers, encodings, or StateInit
    inputs cannot create another identity for that same Offer.
17. Every active Demand Mutation fixes the complete buyer handoff and upload
    context before Provider authorization; chat, selection, Gateway, or index
    data cannot complete or rotate it.
18. No public Demand-first D3/D4 phase or paid-demand MVP may be enabled until
    the system-level D2 promotion gate has passed: at least two independently
    operated and implemented sources, source-plus-store shutdown recovery, and
    an independent codec/verifier. This does not redefine the Capability-first
    rail or require every later private opportunity to appear in two sources.
19. Every Provider signature passes a rollback-resistant Provider-wide writer
    fence and aggregate admission boundary spanning all shared instances, keys,
    mandates, runtimes, unexpired Offers, and unsettled obligations. That private
    state is not copied into public market artifacts.
20. Permissionless escrow deployment, buyer-wallet Quote acceptance, and
    stablecoin funding are three separate events in the versioned existing
    rail. Different Provider Offers accepted or funded by the buyer are
    independent purchases; V1 does not claim a demand-wide winner or add a
    coordinator contract that would make that claim true.
21. The Gate admits no execution unless the committed admission deadline and
    complete pre-input pipelines, worst-case start delay, effective runtime,
    and exact release-pipeline margin fit their committed boundaries. A fresh
    same-claim start preflight covers queue/restart delay only while durably
    `prepared` and repeats every escrow, Quote, Registry, Agent, Capability,
    code-identity, and finalized-checkpoint authority check. That final
    checkpoint linearizes a bounded ticket through `start_not_after`; original
    admission freezes nothing, and uncertainty after `prepared -> starting` is
    execution ambiguity. Result readiness cannot extend the refund boundary.

## 10. Cross-repository interfaces

The implementation must stabilize these interfaces before enabling automatic
commercial action:

| Interface | Producer | Consumer | Required semantics |
|---|---|---|---|
| Capability-first acquisition | Registry plus Gateway/provider Quote service | buyer and Provider coordinator | finalized Capability/version and immutable manifest, complete-preimage Quote Proposal, frozen schema-appropriate acceptance; catalog rank, availability, SLA, and price displays remain non-authoritative until bound |
| demand discovery page | Gateway | OpenFox | bounded cursor, provenance, expiry, signed envelope, explicit non-authority |
| optional market-application source | centralized market application | OpenFox source adapter | exact signed artifact bytes or an explicitly application-local lead; provenance, bounded query, local-status namespace, and no substitution of account, order, balance, or support state for TOS authority; a local lead is display-only until converted into and independently verified as the exact artifact required by its origin lane |
| demand verification | protocol SDK | OpenFox | canonical digest/signature checks plus finalized Agent/network resolution; observed-chain integrity without global-head claims |
| skill descriptor | OpenFox skill registry / `tos-ai` profile catalog | OpenFox matcher | versioned exact compatibility and operator approval |
| estimate | `tos-ai` | OpenFox economics | fixed-point/integer bounds, version, validity, resource class |
| capacity reservation | `tos-ai` | OpenFox coordinator | durable Offer/body-bound, expiring, idempotent reserve/convert/release; ambiguous acceptance retains capacity |
| Demand Mutation / Offer | protocol/Messenger adapter | OpenFox | market-purpose authorization, sequence/single-acceptance, exact action, idempotency, ambiguity resolution |
| mandate decision | OpenFox deterministic policy | custody adapter | exact action digest, limits, mandate version, expiry |
| Provider-private admission | custody adapter | OpenFox coordinator | exclusive writer lease, rollback-resistant fencing high-water mark, stable-action replay, unresolved-tuple and aggregate exposure across every shared signer/runtime; atomic record before signature release |
| paid-demand Quote binding | protocol + TOS contracts | Gate/custody/OpenFox | exact Provider-authorized binding body embedded in a versioned existing Accepted Quote/escrow; one deterministic Quote per exact Offer; permissionless `pending_acceptance` deployment plus one buyer-wallet-authenticated `accept` transition |
| escrow funding | existing stablecoin escrow contract | buyer, Provider, Gate, recovery clients | asynchronous exact-asset funding after Quote acceptance; idempotent finalized-state resolution without a demand-wide winner claim |
| private-input push | Provider ingress | buyer + `tos-ai` | Offer-bound endpoint/challenge, buyer upload proof of possession, exact committed bytes, and one signed monotonic `InputAcceptanceRecordV1` under the bound ingress-attestation/clock profile; distinct delivery and later admission deadlines; idempotent status resolution; no Provider pull |
| execution admission and first-start preflight | Native Execution Gate | `tos-ai` runner | preserve the five schema-1 claim fields and shared slot; for the paid successor, every adapter also carries exact `input_acceptance_record_digest`, whose omission/substitution conflicts; verify that record, immutable bytes, binding, Provider authorization, and complete pre-execution margins; compare every finalized Quote/escrow field, require funding, exact duration/preflight/release-pipeline values and strict refund slack; before first start and every safe refresh, repeat complete authority checks at fresh coherent checkpoints and issue one bounded ticket through `start_not_after` |
| outcome/evidence | `tos-ai` | protocol provider SDK | immutable digests, typed validator result, bounded metadata |
| Opportunity and Commerce Job projections | durable participant journal plus protocol/source/runtime/custody resolvers | OpenFox SDK, CLI, and UI | participant-local rebuildable read models with evidence classes and role/state-gated advisory actions; derivative events are at least once and have no signing, execution, or settlement authority |
| Receipt/settlement resolution | protocol SDK | OpenFox accounting | quorum-finalized escrow and wallet outcome |
| future evaluation profile | versioned Quote/escrow profile plus evaluator Capability or contract | buyer, Provider, evaluator, resolver | static evaluator/quorum/rotation set, evidence/availability, one-shot decision schema, complete fee asset/source/recipient/conservation tuple, deadlines, challenge, immutable dependency closure, and permissionless unavailable-Evaluator refund fixed before acceptance; absent from objective V1 |
| strategy observation | OpenFox accounting | learning/ranking | evidence references, immutable adverse outcomes, no authority |

Interfaces return typed public errors with retry dispositions. Transport
timeouts cannot be flattened into generic retryable errors.

## 11. Delivery sequence

### Phase 0 — specification and truth model

Repositories: `tos-service-spec` first, then `tos-service-protocol`.

- decide the first fixed-price paid-demand profile;
- perform the product-strategy decision filter;
- freeze bounded Demand Mutation with complete `BuyerHandoffProfile` and
  single-acceptance Provider Offer artifacts in Native protobuf;
- freeze market delegation scopes/static bounds, portable historical authority,
  current authorization eligibility, acceptance-time revocation ordering,
  signatures, sequences, terminal withdrawal, the non-canonical-head boundary,
  digests, ordering, errors, retry behavior, and vectors;
- freeze the field-level paid-demand binding matrix, Provider authorization,
  versioned Accepted Quote/escrow mapping, one-Offer/one-Quote derivation,
  asynchronous funding transition, and the existing Gate's immutable mapping
  from network/Quote schema/binding profile to exact Quote/escrow parsers,
  escrow code hash, claim extension, and predicate set;
- freeze complete deadline ordering, effective-duration derivation/enforcement,
  preflight-to-start delay and fresh preflight, conservative network-time
  bounds, exact nonzero acceptance-to-funding, funding-to-input, input-to-
  admission, and release-pipeline margins with complete step bounds, strict
  refund inequality, zero-bounce initial-wallet-request proof and permissionless
  old-query replay/resolver rules, exact wallet/attached-value/fee assumptions,
  execution-signer time-attestation custody, finalized-anchor age/head-lag
  bounds, current-quorum/cross-shard proof rules, bounded start-ticket
  linearization, and boundary vectors;
- freeze Provider-private writer-fencing, rollback-resistant issuance,
  aggregate-admission, and recovery invariants without adding private state to
  public artifacts;
- define spec-owned task, execution, validator, evidence, and private-input
  profiles, including signed `InputAcceptanceRecordV1`, ingress attestation,
  conservative clock evidence, monotonic journal recovery, and the separate
  delivery/admission comparisons, plus implementation-owned skill and estimate
  versioning;
- freeze the authority matrix and state ownership; and
- provide an independent parser/vector implementation.

Exit: two implementations reject the same malformed, replayed, conflicting,
expired, wrong-network, and over-bound artifacts.

### Phase 1 — read-only earning scout

Repositories: `tos-service-gateway`, `tos-service-protocol`, `openfox`.

- publish and federate synthetic fixed-price demand;
- add bounded cursors and the active/terminal Demand Mutation chain;
- verify candidates independently in OpenFox;
- add typed skill matching and integer economics;
- expose bounded rebuildable Opportunity and role-aware Commerce Job projections
  plus a participant-local resumable derivative event stream with stable reason
  codes;
- persist explanations and counterfactual rejection reasons; and
- permit no Provider Offer, custody/market signing request, execution, or spend.

Exit: restart-safe observe mode produces identical decisions from a frozen
candidate/cost/policy corpus and no external mutation is possible.

### Phase 2 — guarded testnet fixed-price worker

Repositories: `openfox`, `tos-ai`, `tos-service-protocol`, custody tooling;
Gateway changes only where the approved profile requires them. This phase is
blocked until specification, protocol, TOS contract/escrow, Execution Gate,
private-ingress, Provider-wide fencing/admission, and independent-vector
prerequisites are complete. It also requires the complete D2 evidence in the
specialized paid-demand design: two independent sources, original-source plus
database shutdown recovery, and a second independent codec/verifier.

- keep recommend mode proposal-only, and add a distinct exact one-shot owner-
  authorization path for a single-acceptance Provider Offer without widening
  the persistent mode;
- add the owner-private process lock and rollback-resistant Provider-wide writer
  fence, unresolved-tuple, and aggregate-exposure admission;
- add atomic capacity reservation/convert/release and portfolio exposure
  reservations;
- implement the spec-defined software-work execution, validator, evidence, and
  private-input profiles;
- create one `PaidDemandQuoteBindingBodyV1` plus Provider authorization and map
  it into one versioned existing Accepted Quote/escrow;
- permit permissionless deployment only into `pending_acceptance`, finalize the
  exact buyer wallet's `accept` transition, then observe the later asynchronous
  stablecoin funding transition before execution admission;
- race duplicate encodings of one exact Offer to prove one deterministic Quote,
  and separately prove that distinct buyer-accepted Offers remain independent
  purchases without a global-winner claim;
- push exact private input through the Offer-bound proof-of-possession Provider
  ingress;
- make the Native Execution Gate verify the Provider-authorized binding and
  compare every finalized paid-demand Quote/escrow field, including the
  exact effective duration, preflight-to-start delay and admission deadline,
  strict settlement slack, and fresh same-claim preflight before first process
  start;
- execute and submit exactly once; and
- reconcile final provider credit, costs, and realized P&L.

Exit: one fresh public-testnet task completes from demand discovery through
independently resolved provider credit, including crash recovery at every side
effect boundary.

### Phase 3 — bounded production vertical

Repositories: all operationally involved repositories.

- install production custody and a narrow expiring mandate;
- enable one objective task profile, exact asset, and small exposure ceiling;
- add monitoring, drain, revoke, incident, and accounting export procedures;
- run independent buyer, provider, Gateway, and verifier operators; and
- measure cost-estimate error, margin, settlement latency, refunds, and
  unresolved exposure.

Exit: recurring paid use meets the existing roadmap gates. Code or same-host
tests alone cannot satisfy this phase.

### Phase 4 — competitive multi-offer selection and multiple skills

Repositories: specification and protocol first for any new profile, followed
by Gateway, OpenFox, and `tos-ai` implementations.

- add competitive multi-provider Offer revision and selection; Phase 2 already
  contains one buyer selecting one fixed single-acceptance Offer;
- add pricing strategies behind deterministic floors and exposure limits;
- onboard additional machine-checkable profiles one at a time;
- add canary strategy evaluation and rollback; and
- consider batch settlement or subcontracting only after the Expansion Gate
  permits them.

Exit: multiple independently operated providers compete without any Gateway
becoming market authority, and every winning task remains portable through the
same finalized lifecycle.

## 12. PR dependency graph

The intended order is:

```text
S0  tos-service-spec: Demand Mutation, delegation, discovery, vectors
 |
 +-> P0  tos-service-protocol: codecs, verifier, SDK, errors
 |    |
 |    +-> G0  tos-service-gateway: bounded demand publication/search
 |    |
 |    +-> O0  openfox: observe-only scout, matcher, economics, journal
 |
 +-> A0  tos-ai: implement spec profiles, estimate, capacity reservation

P0 + G0 + O0 + A0
  -> D1/D2 read-only discovery evidence only

S1  tos-service-spec: paid-demand Quote-binding body/Provider authorization/
    private-input vectors + Provider-private fencing/admission invariants
 |
 +-> C1  tos: versioned Quote/escrow parser and code identity + pending/accept state
 +-> P1  tos-service-protocol: binding resolver/SDK/safe handoff
 +-> E1  execution Gate: compare every finalized paid-demand binding field
 +-> A1  tos-ai: private ingress + exact executor/validator/evidence mapping
 +-> F1  custody: exclusive writer lease + rollback-resistant generation/issuance
          + unresolved-tuple and Provider-wide aggregate admission

S1 + C1 + P1 + E1 + A1 + F1 + D1/D2 acceptance
  -> O1: guarded single-acceptance Provider Offer
  -> E2E testnet fixed-price acceptance
  -> production mandate and external evidence
  -> competitive bidding and additional profiles
```

The binding review has already proven that schema-1 Accepted Quote/escrow bytes
do not express all required paid-demand facts, so C1 is mandatory before paid
D3 execution. This is a versioned integration into the existing commercial
rail, not a second lifecycle. Messenger receives a PR only for public-channel
and selected negotiation/approval transport integration; generic DHT/Overlay/
RLDP/Storage primitives remain in `tos`, and OpenFox must also work through a
non-Messenger protocol adapter.

Every implementation PR records the specification commit it implements. No
downstream repository may freeze incompatible fields while the specification
decision is unresolved.

## 13. Compatibility and migration

- The sole protocol identifier remains `tos_service_v1` unless an approved
  breaking specification change explicitly resets it.
- New messages use new bounded protobuf fields or services; they do not create
  an alternate JSON authority path.
- Gateway indexes are disposable and rebuildable. Cursor invalidation is
  explicit and never changes object identity.
- OpenFox journals carry schema version, network domain, object digests, and
  migration code. Unknown versions fail closed.
- Skill, execution, estimate, evidence, and accounting policies are versioned
  independently and recorded on each decision.
- Removing a frozen field reserves its protobuf number. Digest changes require
  new domains and frozen positive and negative vectors.
- Existing Quote/escrow/Receipt semantics remain the compatibility baseline,
  but paid-demand execution requires an explicitly versioned paid-demand Quote-
  binding extension. Schema 1 keeps deployment-as-acceptance; only the successor
  has recoverable `pending_acceptance` and bound-wallet `accept`. Pre-acceptance
  market data cannot reinterpret an old Quote as if it carried the new bindings.

## 14. Test and evidence matrix

### Specification and protocol

- canonical positive vectors and independently produced digests;
- wrong network, signer, market purpose, Agent generation/policy/delegation,
  mutation sequence/predecessor/kind, ordering, digest, and expiry;
- oversized strings, repeated fields, pages, artifacts, and retry windows;
- exact replay versus conflicting identity reuse;
- unknown schema/profile versions and trailing data;
- integer overflow, asset mismatch, and conservative rounding;
- ambiguous mutation resolution;
- typed `PaidDemandQuoteBindingBodyV1`, exact Provider proof, and deterministic
  versioned Quote/escrow reproduction for one exact Offer;
- separate permissionless `pending_acceptance` deployment, finalized bound-
  wallet `accept`, and asynchronous exact-asset funding, including front-run,
  replay, ambiguity, resolver recovery, latest-valid transaction times, delayed
  finality, and exact committed acceptance-to-funding/funding-to-input margins;
- rejection of alternate signatures, proof wrappers, field encodings, or
  StateInit inputs that attempt to map one exact Offer to multiple Quotes;
- independent validity of two distinct buyer-accepted Provider Offers, with no
  false demand-wide winner claim;
- alternate authorized key, threshold-signature subset, portable authority
  reference/proof path, proof wrapper/ordering, and non-canonical Ed25519
  encoding for one otherwise identical body;
- buyer, Demand, Offer, input/source, validator/evidence, deadline, signer,
  asset, and private-input-profile swap vectors; and
- current authorization eligibility and Quote-acceptance ordering after
  rotation, recovery, delegation revocation, Capability transfer/revocation,
  and Offer expiry;
- unseen successor/withdrawal simulation proving that observed mutation
  eligibility is never reported as a globally complete head.

### Gateway and federation

- two independently controlled Gateways return the same envelope digest with
  distinct provenance and failure domains;
- stale, terminal-withdrawn, superseded, duplicate, incomplete, and forked
  mutation chains;
- cursor expiry/restart without lost or duplicated authoritative action;
- Gateway outage and malicious ranking; and
- rebuild from retained envelopes without creating acceptance facts.

### Optional market applications

- application login, order, balance, `accepted`, `funded`, `completed`, support,
  and ranking fields cannot substitute for TOS Agent/wallet authority or advance
  protocol evidence;
- regions, mirrors, and API endpoints sharing one application account/order
  database count as one source, not D2 independence;
- an application-local lead is display-only until exact artifact conversion and
  independent verification;
- deleting or moderating an application row cannot create withdrawal,
  cancellation, refund, or settlement; and
- after acceptance, Quote, escrow, Receipt, and settlement reconstruction works
  after the application's complete database is deleted.

### OpenFox

- deterministic replay of discovery, matching, economics, and policy;
- recommend/approval records with no canonical body, reservation, custody, or
  signature effect; exact one-shot proposal binding without persistent mode
  increase;
- concurrent budget and capacity races;
- Provider Offer/later-bid crash at every journal transition;
- Offer single-acceptance and capacity reserve/convert/release races;
- duplicate-encoding races for one exact Offer and independent acceptance of
  different Provider Offers;
- same-host duplicate writer, partitioned stale generation, aggregate exposure,
  rollback-resistant issuance restore, and full-exposure fail-closed recovery;
- restart with accepted, executing, result-ready, settlement-requesting,
  refund-resolving, and settlement-pending work;
- duplicate, reorder, resume, and rebuild Commerce Job events without changing
  projected evidence or exposing an action forbidden to the caller's role;
- pause, drain, mandate expiry, custody revocation, and emergency stop;
- hostile task prompt and tool/credential/network escalation attempts;
- stale estimates, cost spikes, fee exhaustion, and settlement delay; and
- learning data that includes losses and attempts to expand authority.

### Execution and settlement

- profile-to-runtime mapping and sandbox conformance;
- buyer-push private ingress and hostile URL/credential/archive/challenge inputs;
- stolen bearer challenge, wrong buyer upload proof-of-possession key,
  concurrent/conflicting upload, exact retry, ambiguous ACK, and status
  resolution; signed `InputAcceptanceRecordV1` at and after the delivery
  boundary; on-time input admitted later through the admission boundary; wrong
  ingress-attestation key; missing bytes; backdated clock evidence; journal/
  checkpoint rollback; and admission-time substitution;
- reservation expiry and accepted-profile mismatch;
- Execution Gate comparison against every paid-demand binding and existing
  funded-escrow field;
- zero/substituted pre-input or release-pipeline margin, duration round-down,
  exact-boundary rejection, late admission, queue delay and restart while
  `prepared`, fresh same-claim preflight, atomic `prepared -> starting`, crash
  ambiguity after that boundary, monotonic-but-stale finality anchor, excessive
  anchor age/head lag, unavailable/disagreeing current quorum, missing cross-
  shard order proof, clock rollback/skew, overflow, understated finality/upload/
  Gate-claim/validation/wallet-request time, inability to prove zero-bounce,
  old-query permissionless release/refund replay, concurrent old/new attempts,
  replay fee consumption or incorrect semantic-action grouping, and a late
  result/settlement request that attempts to outrank timeout refund;
- arbitrary/backdated Receipt completion time and execution signer detached from
  the Gate claim, runner journal, or conservative clock interval;
- successor escrow rejection of a Receipt completed after the bound execution
  deadline, even when the Provider signer authorizes it before refund;
- cross-transport duplicate execution reaching one shared claim;
- validator failure despite process success;
- evidence tampering, Receipt signer mismatch, and objective timeout-refund
  race;
- provider-wallet credit checked through independent endpoints; and
- exact reconciliation after Gateway, OpenFox, worker, or custody restart.

### External acceptance

At least five independently controlled roles participate: buyer, provider, two
qualifying source operators, and an independent verifier/resolver. Each claimed
independent source records
operator/signing identity, host/process/store, network path, upstream carrier,
implementation/codec dependency, and failure domain. Evidence also records
repository commits, network domain, Agent and Capability/version, Demand
Mutation/Offer/binding-body/Provider-proof digests, Quote commitment,
escrow, private-input profile, execution, artifact and Receipt digests,
settlement transaction, provider-wallet delta, exact costs, unresolved items,
and signed role declarations. Credentials and private keys are forbidden in
evidence bundles.

## 15. MVP acceptance criteria

The first autonomous-earning MVP is accepted only when every V1 criterion in
[`AGENT_PAID_DEMAND_DISCOVERY_V1.md`](AGENT_PAID_DEMAND_DISCOVERY_V1.md#21-v1-acceptance-criteria)
and every OpenFox-specific criterion in
[`OPENFOX_AUTONOMOUS_EARNING_IMPLEMENTATION_PLAN.md`](OPENFOX_AUTONOMOUS_EARNING_IMPLEMENTATION_PLAN.md#mvp-acceptance-criteria)
is demonstrated. The cross-repository evidence must therefore include at least:

1. discovery of the same exact Demand Mutation through at least two sources
   satisfying operator, implementation, upstream, storage, path, and failure-
   domain independence;
2. continued discovery and exact reference resolution after the original source
   and its complete database stop, plus frozen-vector verification by a second
   independent codec/verifier;
3. historical and current authorization verification of one active Mutation and
   its complete mutation-bound `BuyerHandoffProfile`, with no global market-
   head claim or Messenger/Gateway completion;
4. typed skill/capacity matching and reproducible exact-asset economics under a
   narrow owner mandate;
5. same-host process exclusion plus rollback-resistant Provider-wide writer
   fencing, unresolved-tuple and aggregate-exposure admission across every
   shared instance, key, mandate, runtime, unexpired Offer, and obligation;
6. one privately reserved, idempotent, buyer-specific Provider Offer whose
   Provider authorizes the exact `PaidDemandQuoteBindingBodyV1`, followed by
   permissionless deterministic versioned escrow deployment into
   `pending_acceptance`, the bound buyer wallet's finalized `accept` transition,
   and a later finalized exact-asset funding transition; the evidence proves a
   wrong-sender predeployment cannot consume acceptance, one exact Offer cannot
   create multiple Quotes, and no global-winner claim is made;
7. private input admitted only through the Mutation- and Offer-bound proof-of-
   possession buyer-push ingress, with one atomic signed
   `InputAcceptanceRecordV1` proving timely durable byte acceptance under the
   bound clock/journal profile and a separate later Gate-admission comparison;
8. one Native Execution Gate admission, bounded execution, objective validation,
   immutable evidence, Receipt submission, and independently resolved finalized
   provider credit, with the exact start delay, effective duration, and release-
   pipeline margin proven to fit strictly before the refund boundary at
   admission and fresh first-start preflight;
9. restart, takeover, duplicate, ambiguity, withdrawal/finality race, objective
   timeout-refund, and stale-writer tests without duplicate work or excess
   exposure;
10. append-only realized P&L reconciliation, explanation, owner pause/revoke/
    drain controls, and recovery without a Gateway, market database, or local
    journal becoming settlement authority;
11. deterministic rebuild of the same Opportunity and role-aware Commerce Job
    projections from durable records/resolvers and resumption of their local
    derivative event cursor, with advisory actions and stable reason codes
    unable to bypass policy, custody, funding, Gate, or finalized-state checks.

Passing this MVP does not prove a broad autonomous economy, general task
competence, production profitability, legal compliance, or roadmap gate
acceptance.

## 16. Explicit non-goals

The initial implementation does not include:

- unrestricted autonomous custody or self-issued mandates;
- a Gateway-owned task ledger, balance, reputation score, or settlement truth;
- prohibiting optional centralized market applications or proprietary market
  user experiences;
- making any market application a required discovery, identity, acceptance,
  execution, evaluation, or settlement intermediary;
- treating application-local orders, credits, rankings, fees, support outcomes,
  disputes, or reputation as TOS protocol state;
- a protocol-mandated platform commission or administrator-controlled fee
  change for an accepted purchase;
- universal subjective work or generalized arbitration;
- task-installed code, skills, plugins, credentials, models, or network access;
- cross-chain or custodial settlement assets;
- automatic subcontracting or recursive Agent supply chains;
- speculative trading, token-price strategies, or capital management;
- automatic policy expansion through self-learning;
- claims of profit based on quotes, unfinalized Receipts, or token valuation;
- broad marketplace work before the fixed-price software profile demonstrates
  recurring external paid use; or
- chain changes made only to improve discovery or ranking convenience.

## 17. Open decisions for the first specification PR

1. Is the initial paid-demand envelope a Native protobuf message, a signed
   Agent Packet payload profile, or both with one canonical digest source?
2. What exact encoding freezes the purpose-limited market delegation/static
   bounds, portable historical authority proof, Demand Mutation sequence,
   terminal withdrawal, explicit non-canonical-head boundary, and issuance/
   acceptance-time authorization rules selected by the focused discovery
   design?
3. Which buyer proof, deposit, or anti-spam mechanism is sufficient before an
   earning Agent spends material resources evaluating demand?
4. What exact `PaidDemandQuoteBindingBodyV1`, Provider proof, versioned Accepted
   Quote/TVM schema, escrow StateInit/code identity, `pending_acceptance` state,
   bound-wallet `accept` operation, resolver, existing Gate comparison, and
   safe-handoff encodings implement the mandatory binding matrix without
   changing the existing Receipt lifecycle?
5. What exact per-Offer StateInit derivation, parser-version dispatch, finalized
   Quote query, wrong-sender predeployment recovery, acceptance deadline,
   asynchronous funding resolution, replay/conflict handling, and recovery
   semantics guarantee one Quote identity for one exact Offer while treating
   different accepted Offers as independent purchases?
6. What exact ingress/challenge, buyer upload proof-of-possession, status,
   encryption, retention, ingress-attestation, `InputAcceptanceRecordV1`,
   conservative clock evidence, and monotonic journal profile implements buyer-
   push private input without Provider pull, task-selected endpoints, bearer-
   only authority, credential proxying, or a backdated delivery claim?
7. What exact deadline fields, effective-duration derivation/enforcement,
   preflight-to-start bound and fresh preflight, network-time upper-bound rule,
   clock-skew/finality assumptions, exact nonzero pre-input and release-pipeline
   margins with complete step compositions, separate input-delivery/Gate-
   admission comparisons, strict refund inequality, zero-bounce initial-wallet-
   request proof, permissionless old-query replay/resolver rules, wallet/
   attached-value/fee assumptions, execution-signer time-attestation custody,
   and boundary vectors make execution safe before timeout refund?
8. Which software-work subset is safe for the first autonomous Offer, and what
   maximum cost/exposure bounds apply?
9. Which cost sources are reproducible enough for automatic authorization, and
   which remain owner-configured conservative ceilings?
10. What operation resolves an ambiguous mutation, Offer, input delivery, result
   submission, and settlement intent for each supported transport?
11. How are legal restrictions and operator-specific compliance represented as
   local policy without making a Gateway a universal authority?
12. What exact operator/host/store/upstream/implementation diversity is required
    for independent-source acceptance?
13. What external recurring-use threshold permits competitive multi-offer
    bidding and the next task profile under the existing Expansion Gate?

Until these decisions are frozen and tested, OpenFox may implement only the
read-only scout and local simulations; D2 may test propagation without Offers.
Provider Offers, paid execution, automatic commercial action, later bidding,
and production operation must not be inferred from the presence of this design
document.
