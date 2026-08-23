# OpenFox Autonomous Earning — Cross-Repository Design

**Status:** incubation design; implementation and external acceptance pending

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
- [`AGENT_ECONOMY_METRICS_V1.md`](AGENT_ECONOMY_METRICS_V1.md)
- [`ROADMAP.md`](ROADMAP.md)

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
5. `tos-ai` for typed execution profiles, capacity, reservations, isolation,
   metering, validation evidence, and result production;
6. `tos-messenger` where authenticated negotiation, owner approval, or direct
   buyer/provider delivery uses Messenger; and
7. `tos` and custody tooling only when existing Agent delegation, escrow,
   Receipt, or settlement contracts cannot express the accepted commercial
   lifecycle safely.

The first useful slice should avoid a chain change. Open paid-demand listings,
bids, and negotiation messages can remain bounded, signed, non-canonical
pre-acceptance artifacts. The winning agreement becomes authoritative only
through the existing finalized Accepted Quote and escrow. A chain or protobuf
extension is justified only after the existing lifecycle cannot express a
required shared fact and the roadmap decision filter approves it.

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

- discovery of buyer-published paid demand, rather than only provider
  Capabilities that OpenFox may purchase;
- independent verification and deduplication of task revisions from multiple
  sources;
- typed matching between task requirements, installed skills, available
  capacity, credentials, legal policy, and evidence capability;
- exact-asset revenue, cost, risk, locked-capital, and expected-profit models;
- portfolio-level exposure, concurrency, counterparty, and loss limits;
- deterministic bid/claim authority and idempotent negotiation journals;
- competitive pricing and offer revision without allowing model prose to
  authorize a commitment;
- capacity reservation between acceptance and execution;
- multiple bounded execution profiles beyond the current pinned software-work
  profile;
- task-specific validation, evidence generation, result submission, dispute,
  and recovery adapters;
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
- real fee, latency, failure, refund, dispute, and utilization observations;
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
selected terms
  -> finalized Accepted Quote and escrow
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
| Market action | request/accept Quote | advertise, bid, claim, or offer Quote |
| Execution role | buyer/client | provider/worker |
| Terminal accounting | expense or purchased asset | settled revenue and allocated cost |

They may share finalized resolvers, canonical codecs, custody clients, event
infrastructure, and accounting primitives. They must not share a permissive
policy decision merely because the same owner operates both roles.

## 4. Repository ownership

| Repository | Must own | Must not own |
|---|---|---|
| `tos-service-spec` | normative market-envelope schemas when approved; bounds; canonical encodings; authority and state-machine invariants; compatibility rules; frozen positive and negative vectors; cross-repository acceptance contract | runtime schedules, private policy, private credentials, mutable market indexes |
| `tos-service-protocol` | generated types; canonical encoders/digests; signature and finalized-state verification; negotiation, Accepted Quote, provider, Receipt, settlement, and recovery SDKs; conformance helpers | opportunity ranking, model planning, operator portfolio policy, custody secrets |
| `tos-service-gateway` | bounded searchable projection of non-expired demand; cursors; federation; rate limits; authenticated publish/withdraw/relay transport; explicit provenance and freshness | canonical task acceptance, buyer solvency truth, ranking authority, custody, provider execution, settlement truth |
| `openfox` | durable earning coordinator; source federation; verifier orchestration; skill/capacity matching; economics; pricing strategy; deterministic policy; bid/claim journal; execution orchestration; local P&L; operator explanation and control | protocol codecs, chain truth, raw chain keys, task-selected authority, unrestricted tool execution |
| `tos-ai` | versioned task/execution profiles; deterministic estimates; capacity and reservation interface; bounded executors; metering; validators; evidence and artifact production; execution replay protection | market authority, economic policy, wallet custody, final settlement recognition |
| `tos-messenger` | authenticated Agent conversations, replay-safe structured negotiation transport, direct approval delivery, and device/session custody where Messenger is selected | market ranking, Quote/escrow authority, execution authority, wallet authority from prose |
| `tos` / contracts | canonical Agent delegation, Accepted Quote, escrow, Receipt, dispute, transfer, and final settlement transitions that truly require shared authority | task search, bid ranking, private cost models, OpenFox objectives, execution planning |
| `tosctl` or equivalent custody boundary | semantic confirmation, delegated signing, fee/balance ceilings, broadcast, ambiguous-submit resolution, revocation integration | opportunity selection, model prompts, execution or accounting policy |
| `doc` | ecosystem-level product explanation synchronized after the design is accepted | normative schemas, implementation status without evidence, runtime behavior |

Any canonical field or digest addition starts in
`proto/tos/service/v1/native.proto` in this repository. Implementations must not
create a competing JSON, database, or application schema and later treat it as
protocol authority.

## 5. End-to-end architecture

```text
buyer / task issuer
  -> publish bounded paid-demand envelope
  -> one or more replaceable Gateways index the envelope

OpenFox earning scout
  -> federated cursor reads
  -> signature, expiry, revision, provenance, and bound checks
  -> direct finalized Agent/Capability/network verification
  -> typed skill + evidence + capacity match
  -> integer economics + portfolio exposure calculation
  -> deterministic mandate decision

OpenFox provider
  -> bid / claim / Quote response through protocol or Messenger adapter
  -> resolve ambiguity before any retry
  -> buyer selects terms
  -> finalized Accepted Quote + funded escrow

tos-ai execution boundary
  -> reserve capacity
  -> Native Execution Gate claims the exact paid execution
  -> execute approved profile once
  -> validate output and produce immutable evidence

protocol + custody boundary
  -> submit canonical Receipt / settlement intent once
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

### 6.1 Why a demand profile is needed

Current Capability search answers “what can I buy?” It does not answer “which
buyer currently wants work that I can profitably perform?” A provider earning
loop therefore needs a paid-demand discovery profile.

The initial profile should support fixed-price, objectively verifiable
software work. Competitive bidding is added after fixed-price claiming works
end to end. General job boards, subjective arbitration, subcontracting, GPU
markets, and cross-chain payments remain later profiles.

### 6.2 Pre-acceptance artifacts

The design requires the following conceptual artifacts. Their exact fields and
canonical encoding are not frozen by this document:

- **Paid Demand** — buyer identity, revision, task-profile ID, input/evidence
  commitments, required Capability predicates, exact asset, payment ceiling or
  fixed price, deadlines, dispute profile, publication expiry, and signature;
- **Provider Offer** — demand revision, provider Agent and Capability/version,
  exact price, delivery window, execution/evidence profile, offer expiry,
  idempotency identity, and signature;
- **Selection Notice** — buyer's non-canonical notice of a selected offer and
  the terms expected in the Accepted Quote; and
- **Withdrawal/Supersession** — a signed replacement relation for one issuer's
  prior demand or offer revision.

These artifacts are hostile, replayable Internet inputs. A valid signature
proves origin only. It does not prove funding, solvency, availability, quality,
selection, or payment.

Before an implementation PR adds these messages or services, the specification
PR must decide whether they belong in the sole Native protobuf schema. If they
do, it must define bounds, canonical ordering, digest domains, signatures,
revision rules, rejection behavior, retry semantics, and frozen vectors first.

### 6.3 Discovery semantics

A Gateway may index, rank, filter, paginate, relay, and expire demand. Every
result includes source Gateway, observation time, issuer, revision, envelope
digest, and cursor provenance. A Gateway must not claim that a listing is:

- accepted or funded;
- still available merely because it has not expired locally;
- profitable for a particular provider;
- authorized for execution; or
- guaranteed to settle.

OpenFox deduplicates identical envelope digests across Gateways, rejects
conflicting reuse of an issuer/revision identity, and retains source
provenance. Before bidding it verifies the signature and finalized issuer Agent
state. Before execution it ignores the listing and verifies the finalized
Accepted Quote and escrow through the existing Native Execution Gate.

### 6.4 Bid and claim safety

Every bid, claim, revision, withdrawal, and submission has an
OpenFox-generated durable action identity outside model control. Exact replay
is idempotent. Reuse of an identity for different content is a conflict.

An ambiguous network result never causes a blind retry. The coordinator first
queries the destination, negotiation peer, or finalized TOS state appropriate
to the action. If no authoritative resolution operation exists, the action is
marked ambiguous and requires operator review or safe expiry.

## 7. OpenFox earning control plane

### 7.1 Runtime modes

The earning runtime has explicit modes:

1. `off` — no polling or commercial action;
2. `observe` — discover, verify, match, estimate, and report only;
3. `recommend` — prepare a structured bid or claim for owner approval;
4. `policy-gated` — automatically bid or claim only within an exact active
   mandate; and
5. `drain` — accept no new work, finish or safely unwind existing obligations.

`policy-gated` is not unrestricted autonomy. The default is `off`; activation
requires an owner mandate and production readiness checks.

### 7.2 Durable local state

The earning coordinator maintains a non-authoritative projection such as:

```text
DISCOVERED
  -> VERIFIED
  -> MATCHED
  -> SCORED
  -> POLICY_REVIEW
  -> BIDDING | CLAIMING
  -> ACCEPTED
  -> RESERVED
  -> EXECUTING
  -> VALIDATING
  -> SUBMITTING
  -> SUBMITTED
  -> SETTLING
  -> SETTLED
```

Terminal or side states include `REJECTED`, `EXPIRED`, `WITHDRAWN`,
`CANCELLED`, `FAILED`, `AMBIGUOUS`, `REFUNDED`, and `DISPUTED`.

No local transition creates a protocol fact. From acceptance onward, the
record stores immutable references to the existing Quote commitment, escrow
address, execution identity, Receipt, and finalized checkpoints. On
disagreement, verified chain state wins and the local projection is rebuilt or
quarantined.

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
  - dispute_and_refund_reserve
  - capacity_opportunity_cost

worst_case_exposure
  = external_spend
  + non_refundable_execution_cost
  + locked_capital
  + dispute_or_penalty_reserve
```

The actual implementation represents probabilities as bounded fixed-point
integers with specified rounding toward the conservative outcome. Every input
records its source, freshness, confidence class, and maximum validity period.
Missing or stale required cost inputs fail closed for automatic bidding.

A policy decision is one of `reject`, `recommend`, `approval-required`,
`auto-bid`, or `auto-claim`. It commits the exact assumptions, price, fee cap,
expiry, execution profile, capacity reservation, and mandate version used.

### 7.5 Portfolio policy

Per-task profit is insufficient. The coordinator also enforces atomic claims
over:

- total and per-asset worst-case exposure;
- daily and rolling-window external spend and realized loss;
- concurrent accepted, executing, and disputed tasks;
- resource-class capacity and reservation headroom;
- counterparty and task-profile concentration;
- unresolved bids, submissions, settlement intents, and receivables;
- native TOS fee reserve; and
- mandatory liquidity and emergency-unwind reserves.

Two concurrent tasks cannot both consume the same remaining budget or
capacity. Policy evaluation and reservation are one atomic local transaction.

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
- hide losses, refunds, disputes, or unresolved exposure; or
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
the finalized Accepted Quote. A mismatch causes rejection or a new Quote, not
silent substitution. Reservations expire or are released on every terminal
path.

### 8.2 Execution admission

Every transport reaches the existing shared Native Execution Gate. The Gate
independently verifies the finalized Accepted Quote, funded escrow, provider,
Capability/version, manifest, execution signer, transport binding, input, and
deadlines before atomically claiming the execution slot.

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
- **contracted receivable** — finalized Accepted Quote/funded escrow, still not
  earned cash;
- **submitted receivable** — result or Receipt submitted, still unresolved;
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
3. Model or task text cannot directly authorize bid, claim, execution,
   credential use, Receipt, or settlement.
4. Gateway data is a discovery hint, never canonical authority.
5. Every candidate is network-bound, revision-bound, digest-bound, and
   provenance-bearing.
6. Every external side effect has a durable idempotency identity before it is
   attempted.
7. Ambiguous mutation results are resolved before retry; otherwise they remain
   visibly ambiguous.
8. Exact asset identity and checked integer arithmetic are mandatory.
9. Policy and capacity claims are atomic across concurrent opportunities.
10. Acceptance precedes execution; objective validation precedes a successful
    Receipt; finalized provider credit precedes revenue recognition.
11. Task-selected tools, code, models, credentials, endpoints, or network
    exceptions are forbidden.
12. Self-learning cannot expand authority or erase adverse outcomes.
13. Pause stops new commitments; drain preserves safe handling of accepted
    obligations; revoke prevents new signatures and triggers reconciliation.
14. Restart rebuilds commercial truth from durable journals and independently
    verified finalized state.

## 10. Cross-repository interfaces

The implementation must stabilize these interfaces before enabling automatic
commercial action:

| Interface | Producer | Consumer | Required semantics |
|---|---|---|---|
| demand discovery page | Gateway | OpenFox | bounded cursor, provenance, expiry, signed envelope, explicit non-authority |
| demand verification | protocol SDK | OpenFox | canonical digest/signature checks plus finalized Agent/network resolution |
| skill descriptor | OpenFox skill registry / `tos-ai` profile catalog | OpenFox matcher | versioned exact compatibility and operator approval |
| estimate | `tos-ai` | OpenFox economics | fixed-point/integer bounds, version, validity, resource class |
| capacity reservation | `tos-ai` | OpenFox coordinator | atomic, expiring, idempotent reserve/release |
| bid/claim mutation | protocol/Messenger adapter | OpenFox | signed exact action, idempotency, ambiguous-result resolution |
| mandate decision | OpenFox deterministic policy | custody adapter | exact action digest, limits, mandate version, expiry |
| execution admission | Native Execution Gate | `tos-ai` runner | finalized purchase verification and at-most-once shared claim |
| outcome/evidence | `tos-ai` | protocol provider SDK | immutable digests, typed validator result, bounded metadata |
| Receipt/settlement resolution | protocol SDK | OpenFox accounting | quorum-finalized escrow and wallet outcome |
| strategy observation | OpenFox accounting | learning/ranking | evidence references, immutable adverse outcomes, no authority |

Interfaces return typed public errors with retry dispositions. Transport
timeouts cannot be flattened into generic retryable errors.

## 11. Delivery sequence

### Phase 0 — specification and truth model

Repositories: `tos-service-spec` first, then `tos-service-protocol`.

- decide the first fixed-price paid-demand profile;
- perform the product-strategy decision filter;
- define bounded pre-acceptance artifacts and whether they enter Native
  protobuf;
- freeze signatures, revisions, digests, ordering, errors, retry behavior, and
  vectors if a protocol surface is approved;
- define task-profile, skill-profile, evidence-profile, and estimate versioning;
- freeze the authority matrix and state ownership; and
- provide an independent parser/vector implementation.

Exit: two implementations reject the same malformed, replayed, conflicting,
expired, wrong-network, and over-bound artifacts.

### Phase 1 — read-only earning scout

Repositories: `tos-service-gateway`, `tos-service-protocol`, `openfox`.

- publish and federate synthetic fixed-price demand;
- add bounded cursors and withdrawal/supersession;
- verify candidates independently in OpenFox;
- add typed skill matching and integer economics;
- persist explanations and counterfactual rejection reasons; and
- permit no bid, claim, execution, signature, or spend.

Exit: restart-safe observe mode produces identical decisions from a frozen
candidate/cost/policy corpus and no external mutation is possible.

### Phase 2 — guarded testnet fixed-price worker

Repositories: `openfox`, `tos-ai`, `tos-service-protocol`, custody tooling;
Gateway changes only where the approved profile requires them.

- add recommend mode and owner-approved claim;
- add atomic capacity reservation and portfolio exposure claims;
- reuse the existing software-work execution and evidence profile;
- create the Accepted Quote and escrow through existing canonical paths;
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

### Phase 4 — competitive bidding and multiple skills

Repositories: specification and protocol first for any new profile, followed
by Gateway, OpenFox, and `tos-ai` implementations.

- add bounded offer revision and buyer selection;
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
S0  tos-service-spec: approve profile, invariants, schema decision, vectors
 |
 +-> P0  tos-service-protocol: codecs, verifier, SDK, errors
 |    |
 |    +-> G0  tos-service-gateway: bounded demand publication/search
 |    |
 |    +-> O0  openfox: observe-only scout, matcher, economics, journal
 |
 +-> A0  tos-ai: profile descriptors, estimate, capacity reservation

P0 + G0 + O0 + A0
  -> O1/custody: recommend mode and delegated exact claim
  -> E2E testnet fixed-price acceptance
  -> production mandate and external evidence
  -> competitive bidding and additional profiles
```

`tos` receives a contract PR only if Phase 0 proves that a new shared
authoritative fact cannot safely remain pre-acceptance negotiation data or be
expressed by the existing Accepted Quote/escrow/Receipt lifecycle. Messenger
receives a PR only for selected negotiation or approval transport; OpenFox must
also work through a non-Messenger protocol adapter.

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
- Existing Accepted Quote, escrow, Receipt, and settlement objects remain the
  compatibility anchor. Pre-acceptance market data cannot reinterpret them.

## 14. Test and evidence matrix

### Specification and protocol

- canonical positive vectors and independently produced digests;
- wrong network, signer, issuer, revision, ordering, digest, and expiry;
- oversized strings, repeated fields, pages, artifacts, and retry windows;
- exact replay versus conflicting identity reuse;
- unknown schema/profile versions and trailing data;
- integer overflow, asset mismatch, and conservative rounding; and
- ambiguous mutation resolution.

### Gateway and federation

- two Gateways return the same envelope digest with distinct provenance;
- stale, withdrawn, superseded, duplicate, and conflicting listings;
- cursor expiry/restart without lost or duplicated authoritative action;
- Gateway outage and malicious ranking; and
- rebuild from retained envelopes without creating acceptance facts.

### OpenFox

- deterministic replay of discovery, matching, economics, and policy;
- concurrent budget and capacity races;
- bid/claim crash at every journal transition;
- restart with accepted, executing, submitted, disputed, and settling work;
- pause, drain, mandate expiry, custody revocation, and emergency stop;
- hostile task prompt and tool/credential/network escalation attempts;
- stale estimates, cost spikes, fee exhaustion, and settlement delay; and
- learning data that includes losses and attempts to expand authority.

### Execution and settlement

- profile-to-runtime mapping and sandbox conformance;
- reservation expiry and accepted-profile mismatch;
- cross-transport duplicate execution reaching one shared claim;
- validator failure despite process success;
- evidence tampering, Receipt signer mismatch, refund race, and dispute path;
- provider-wallet credit checked through independent endpoints; and
- exact reconciliation after Gateway, OpenFox, worker, or custody restart.

### External acceptance

At least four independently controlled roles participate: buyer, provider,
Gateway, and verifier/resolver. Evidence records repository commits, network
domain, Agent and Capability/version, demand/offer digests, Quote commitment,
escrow, execution, artifact and Receipt digests, settlement transaction,
provider-wallet delta, exact costs, unresolved items, and signed role
declarations. Credentials and private keys are forbidden in evidence bundles.

## 15. MVP acceptance criteria

The first autonomous-earning MVP is accepted only when one OpenFox instance,
under a narrow owner mandate, can:

1. discover an open fixed-price software-work task from a replaceable Gateway;
2. verify its bounded signed envelope and issuer against the exact network;
3. match it to an installed approved skill and available `tos-ai` profile;
4. reproduce a conservative exact-asset profit and exposure decision;
5. prepare and obtain authorization for one idempotent claim;
6. verify the finalized Accepted Quote and funded escrow;
7. reserve capacity and execute once through the Native Execution Gate;
8. validate the result and produce immutable bound evidence;
9. submit the canonical Receipt or objective failure path once;
10. resolve finalized escrow and provider-wallet state independently;
11. recognize settled revenue and realized P&L without mixing assets;
12. restart safely at every phase without duplicate work or settlement;
13. explain why it acted, rejected, paused, or escalated; and
14. stop accepting work immediately when paused or revoked while safely
    draining already accepted obligations.

Passing this MVP does not prove a broad autonomous economy, general task
competence, production profitability, legal compliance, or roadmap gate
acceptance.

## 16. Explicit non-goals

The initial implementation does not include:

- unrestricted autonomous custody or self-issued mandates;
- a Gateway-owned task ledger, balance, reputation score, or settlement truth;
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
2. Does fixed-price claiming require a provider-signed offer, or can the buyer
   construct the existing Quote from a signed claim response?
3. Which buyer proof, deposit, or anti-spam mechanism is sufficient before an
   earning Agent spends material resources evaluating demand?
4. Which exact fields must the Accepted Quote bind for buyer-published inputs,
   evidence rules, cancellation, and delivery deadline?
5. Can current escrow express every required cancellation and objective
   failure outcome without a contract change?
6. Which software-work subset is safe for the first autonomous claim, and what
   maximum cost/exposure bounds apply?
7. Which cost sources are reproducible enough for automatic authorization, and
   which remain owner-configured conservative ceilings?
8. What operation resolves an ambiguous bid, claim, withdrawal, result
   submission, and settlement intent for each supported transport?
9. How are legal restrictions and operator-specific compliance represented as
   local policy without making a Gateway a universal authority?
10. What external recurring-use threshold permits competitive bidding and the
    next task profile under the existing Expansion Gate?

Until these decisions are frozen and tested, OpenFox may implement only the
read-only scout and local simulations. Automatic bids, claims, or production
execution must not be inferred from the presence of this design document.
