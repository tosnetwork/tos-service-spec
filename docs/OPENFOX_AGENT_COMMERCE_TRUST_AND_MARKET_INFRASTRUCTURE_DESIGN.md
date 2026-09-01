# OpenFox Agent Commerce Trust and Market Infrastructure — Post-Experiment Delta Design

**Status:** proposed incubation design; capability reconciliation and validation
plan only

**Normative effect:** none. This document does not release a wire object,
schema, contract state, settlement rail, conformance profile, or roadmap gate.
Where it conflicts with an existing V1 specification, the existing V1
specification controls.

**Source experiment:** [Eight-Agent Generic Intent Social Earning
Report](https://github.com/tosnetwork/openfox/blob/b18ddaba8b7b2d508ce6e9bc99aa09a4107c4ee2/docs/operations/eight-agent-generic-intent-social-earning-report.md),
executed on 2026-08-31. The pinned report is product evidence, not protocol
conformance evidence.

**Review record:** [Codex Review
Report](OPENFOX_AGENT_COMMERCE_TRUST_AND_MARKET_INFRASTRUCTURE_DESIGN_REVIEW_REPORT.md)

**Implementation record:** [Local Implementation
Checkpoint](OPENFOX_AGENT_COMMERCE_TRUST_AND_MARKET_INFRASTRUCTURE_IMPLEMENTATION.md)

**Controlling references:**

- [Product Strategy](PRODUCT_STRATEGY.md)
- [System Architecture](ARCHITECTURE.md)
- [Implementation Roadmap](ROADMAP.md)
- [Agent Intent Exchange V1](AGENT_INTENT_EXCHANGE_V1.md)
- [Native Quote, Execution, and Settlement Model](SETTLEMENT.md)
- [Semantic Action Identity V1](SEMANTIC_ACTION_IDENTITY_V1.md)
- [Agent Operation and Outcome Event V1](AGENT_OPERATION_OUTCOME_EVENT_V1.md)
- [Agent Economy Metrics V1](AGENT_ECONOMY_METRICS_V1.md)
- [Agent Trusted Capability and Owner Control
  V1](AGENT_TRUSTED_CAPABILITY_AND_OWNER_CONTROL_V1.md)
- [OpenFox Autonomous Earning Implementation
  Plan](OPENFOX_AUTONOMOUS_EARNING_IMPLEMENTATION_PLAN.md)

## 1. Executive decision

The experiment does not justify another generic market protocol. TOS already
has the business-neutral Intent, authenticated application, versioned
Agreement, obligation DAG, billing, settlement-obligation, stable-action, and
Outcome Event foundations needed to represent most recommendations.

The adopted program is therefore a post-experiment delta:

1. exercise real multi-round negotiation by reusing Application V2 and
   predecessor-bound Agreement proposals;
2. operationalize existing Outcome Event evidence as a portable bounded view
   and compute counterparty outcome-risk locally;
3. connect real model, tool, API, storage, network, and chain-fee producers to
   existing cost semantics;
4. validate objective staged settlement by composing current fixed-price
   escrows before proposing a new contract; and
5. repeat the market experiment across independent owners, hosts, and
   Carriers with adverse outcomes and recovery.

No new interface is created for source review, localization, security audit,
BTC, USDT, model access, or any other trade category. Business meaning remains
Intent and Agreement content interpreted by each Agent's AI. Deterministic
authority remains in the selected released profiles and local Owner policy.

## 2. Precedence, classification, and evidence limits

This document uses five classifications:

| Class | Meaning |
|---|---|
| `REUSE` | A released or implementation-candidate capability already expresses the requirement. Do not duplicate it. |
| `VALIDATE` | The design exists, but implementation, deployment, cross-host, adverse-path, or external acceptance evidence is missing. |
| `CANDIDATE` | A portable semantic gap may remain. It needs a separately versioned specification, schema, verifier, vectors, and review before it is shared authority. |
| `LOCAL` | OpenFox AI reasoning, policy, orchestration, projection, ranking, or user experience; it is not portable authority. |
| `DEFERRED` | A generalized expansion or non-goal that remains behind the current product and roadmap gates. |

The precedence order is:

```text
root architecture + Product Strategy + ROADMAP
  -> released or candidate V1 profiles and their schemas/vectors
  -> this non-normative incubation design
  -> experiment reports and local projections
```

The three-hour run demonstrated one generic bulletin, AI screening, four
direct native-TOS payments, and rational declines among eight same-host
runtimes. It did not exercise escrow, Gift, counter-offers, Agreement
supersession, milestones, refunds, disputes, independent operators, hostile
publishers, actual model invoices, or external revenue. Declines had several
recorded causes; the experiment does not prove that missing reputation caused
all of them.

## 3. Existing-capability and conflict audit

| Requested surface | Existing authority or capability | Conflict found in the earlier draft | Decision |
|---|---|---|---|
| Generic supply and demand | Intent modes already include `REQUEST`, `OFFER`, `BUY`, `SELL`, `EXCHANGE`, and `COLLABORATE`, with signed revisions, ranges, expiry, and arbitrary content | Treating buyer demand or heterogeneous work as a missing API would duplicate Intent V1 | `REUSE`; add no business-specific endpoint or schema |
| First contact | Authenticated `INTENT/APPLICATION` V1/V2 already references the exact Intent; V2 may carry a complete proposed Agreement body | A new generic offer message would create parallel non-authorizing proposal semantics | `REUSE` and `VALIDATE` |
| Multi-round negotiation | Natural-language negotiation is supported; changed terms use exact Agreement versions and predecessor digests; `AGREEMENT/PROPOSE`, accept, and withdraw are typed | A standalone `CounterOffer` wire object would overlap Agreement proposal/version authority and Messenger's older incubation labels | `VALIDATE` reuse first; a new portable object is `CANDIDATE` only after an ambiguity is demonstrated |
| Milestones and staged obligations | `AgreementObligationV1`, dependencies, acceptance evidence, cancellation/dispute policy, `BillingTermsV1`, and `SettlementObligationV1` already express milestone, deposit, installment, periodic, refund, and mixed-adapter graphs | A second milestone Agreement or global commerce state machine would duplicate existing authority | `REUSE`; OpenFox may keep only a derived local projection |
| Aggregate loss and capacity | The autonomous earning plan and Semantic Action Identity registry already require atomic Portfolio reservation, Writer Fence admission, stable actions, and recovery | Presenting exposure reservation as a new protocol primitive obscures an existing safety invariant | `REUSE` and add adapter-integration tests |
| Current Paid Demand escrow | Escrow V1 has `awaiting_funding`, `funded`, `release_pending`, and `refund_pending`, with derived full release/refund outcomes for one fixed-price objective job | The earlier draft added partial funding, buyer acceptance, revision, `disputed`, split remedy, adjudication, and fee states that V1 does not have | Preserve V1. Test multiple independent escrows; any richer contract is separately versioned `CANDIDATE` work |
| Escrow asset | The current commercial profile settles one exact supported stablecoin issued on TOS Network; native TOS pays network fees | A native-TOS 4/1.5 escrow test would claim support that the current profile does not define | Use one exact TOS-network stablecoin for escrow tests and account for native-TOS Gas separately |
| Acceptance and dispute evidence | Agreement obligations already bind acceptance requirements and dispute policy; Outcome Events can observe acceptance, rejection, rework, dispute, refund, and ambiguity | An Outcome observation or local state was at risk of becoming release authority | `REUSE` as evidence; prove the selected settlement profile separately authorizes every custody transition |
| Portable history | Outcome Event V1 already defines immutable negative and positive observations, event sets, evidence manifests, disclosure projections, completeness/cohort checkpoints, conflicts, and economic perimeters | A new dossier/reputation wire layer would duplicate Outcome Event and risk a global score | `REUSE`; define a bounded product view and local counterparty outcome-risk only |
| Cost and profit evidence | Outcome Event V1 already distinguishes declared ceiling, estimate, usage measured, payable invoiced, cash finalized, allocated, contra, penalty, write-off, and cost categories | A campaign-specific cost schema would fork economic meanings | `REUSE`; implement actual evidence producers and reports |
| Agent Economy Metrics | The separate metrics document is a narrow finalized stablecoin-escrow aggregate and remains not implemented | Using it for native-TOS direct payments, Gift, external settlement, Owner P&L, or model cost would broaden its meaning | Keep it separate; use Outcome evidence and Owner-local reports for this experiment |
| Executable-capability trust | Trusted Capability and Owner Control defines artifact Admission, Promotion, Use Binding, and formal campaigns; coordinated implementation surfaces exist but the profile and Gates S/M are not released or passed | Calling counterparty commerce history “trusted capability” could imply execution authority | Use `counterparty outcome-risk`; it can never admit or promote executable bytes |
| Action recovery | Semantic Action Identity V1 already supplies stable identities, exact-request binding, terminal successors, and query-before-retry behavior | New per-workflow idempotency rules could conflict with the shared registry | `REUSE`; add missing action kinds only through the registry process |
| Multi-host market evidence | Existing campaigns and Gates D--G already separate local integration, independent acceptance, recurring paid demand, and expansion | Calling one multi-host run production or market acceptance would bypass gates | `VALIDATE` without changing gate order or status |
| General reputation and arbitration | Product Strategy keeps global reputation, universal marketplace semantics, and generalized subjective arbitration outside the initial wedge | Making either one a protocol prerequisite would broaden and reorder the product | `LOCAL` counterparty outcome-risk; generalized arbitration is `DEFERRED` |

### 3.1 Maturity qualification

“Existing” does not mean “production accepted.” Intent V1 and Semantic Action
Identity V1 are release candidates with local conformance and external
acceptance pending. Outcome Event V1 is an implementation candidate whose
public publication is default-off and whose independent-operator availability
gate has not passed. Agent Economy Metrics remains not implemented. Trusted
Capability and Owner Control remains a design candidate: coordinated
implementation surfaces and local verification exist, but its formal Phase 0,
Gate S, Gate M, physical-client, independent-operation, and external campaign
evidence have not passed.

The structural commerce schema includes `SettlementObligationV1`, but the
`SettlementObligationStateV1` projection described by Intent V1 is not a chain
escrow state and is not a substitute for the selected adapter's canonical
state and finality. A consumer must advertise only the exact codec, verifier,
projection, and deployment maturity it has actually passed.

## 4. Adopted post-experiment requirements

### 4.1 Multi-round negotiation by reuse

OpenFox should first implement the following flow without a new shared wire
object:

```text
signed Intent
  -> authenticated Application V2 or non-authorizing conversation
  -> complete candidate Agreement body
  -> typed AGREEMENT/PROPOSE
  -> changed terms produce a new predecessor-bound Agreement body
  -> exact current body receives all required authorization evidence
  -> selected adapters are prepared
```

The first validation cohort must include:

- one price counter-offer;
- one reduced-scope-for-lower-price proposal;
- one buyer demand Intent that receives multiple independent applications;
- one explicit withdrawal or rejection that creates no Agreement, reservation,
  execution, or payment; and
- stale, expired, forked, tampered, and replayed proposals that fail closed.

There is no global authoritative “latest proposal head” in the current model.
An implementation must reject a body it has verified as expired or withdrawn
and must stop when its retained lineage is forked or inconsistent. It must not
infer global supersession from message arrival order. If the product needs a
cross-implementation proof that exactly one proposal head is current, that is
a separate candidate profile and not an implied property of Agreement V1.

OpenFox may render local labels such as `proposal` and `counterproposal`, but
those labels do not authorize anything and are not portable object names. A
new negotiation profile is justified only if two independent implementations
cannot reconstruct proposal lineage, current complete terms, expiry, and
withdrawal using the existing Agreement-version model. That failure must be
recorded as a concrete reuse proof before a `CANDIDATE` specification starts.

### 4.2 Counterparty outcome-risk without a global score

The portable input is existing Outcome Event evidence, not a new reputation
record. A bounded commerce-history view should select and verify existing:

- operation and outcome events, including adverse and ambiguous outcomes;
- Agreement, obligation, action, execution, payment, refund, and finality
  references;
- `OutcomeEventSetV1`, artifact manifests or bundles, and disclosure
  projections;
- completeness, cohort, conflict, correction, expiry, and economic-perimeter
  information; and
- available controller, funder, host, Carrier, campaign, and counterparty
  concentration evidence.

OpenFox then computes buyer-payment, provider-delivery, and service-capability
outcome-risk projections under an explicit local Owner-policy revision. A local score
may assist pricing or adapter recommendation, but it cannot authorize an
Agreement, enable a disabled adapter, increase a budget, release funds, or
become a canonical property of an Agent or `.tos` name.

“Counterparty outcome-risk” in this document is not Capability Admission,
Promotion Authority, or Capability Use Binding from the Trusted Capability and
Owner Control profile. A favorable commerce history cannot admit executable
bytes, bypass Gate S or Gate M, widen permissions, or authorize execution.

Missing denominators and selectively disclosed history remain `unknown`.
Several Carrier copies of the same exact event are idempotently deduplicated;
distinct issuers' assertions about one subject are retained as distinct
evidence and may conflict. A cohort checkpoint proves completeness only for
its exact admission authority, scope, and cut. Expiry affects freshness and
propagation, not the validity of an earlier signature. Signatures prove who
asserted a fact, not that work quality was good or counterparties were
independent. Public export must pass the existing declassification and privacy
rules; private deliverables and low-entropy commercial facts are not exposed
merely to improve outcome-risk estimates.

This is primarily `VALIDATE` and `LOCAL`. A new portable dossier object is not
approved by this design. If the existing event set, artifact bundle, and
disclosure projection cannot carry one exact bounded view, the failed reuse
case must identify the missing field and authority before `CANDIDATE` work.

### 4.3 Real cost and economic reporting

OpenFox should emit or ingest evidence for actual model usage, API and tool
charges, compute, storage, network, native-TOS Gas, stablecoin settlement
fees, subcontractor cost, rework, dispute handling, penalty, write-off, and
separate refund transfers when
such evidence exists. Each record must bind the applicable Agent, execution,
Agreement or obligation, asset, accounting perimeter, source, and evidence
class defined by Outcome Event V1.

Reports must keep these values distinct:

| Value | Required interpretation |
|---|---|
| Declared ceiling or loss cap | Owner authority bound, not a cost |
| Estimate or reserve | Forward-looking risk input, not realized cash |
| Usage measured | Metered quantity, not automatically an invoice |
| Payable invoiced | Authenticated payable, not finalized payment |
| Cash finalized | Evidence-qualified transfer or fee |
| Allocated | Policy-derived accounting entry, visibly labeled |
| Unknown | Projection state when required evidence is absent; not an Outcome cost-class token and never silently zero |

Different assets are not summed without explicit conversion evidence.
Closed-campaign transfers, related-party revenue, external revenue, seller
unit margin, buyer expenditure, and whole-Agent cash flow remain separate.
Buying a capability is not realized return until evidence links it to later
revenue under the stated accounting policy.

As a regression fixture, the source experiment should reproduce 9.2 native
TOS internal seller gross receipts, 9.2 native TOS buyer spend, zero
intra-perimeter transfer net, the
reported 1.4 native TOS conservative reserve, and projected closed-economy net
of -1.4 native TOS. Actual model/tool cost and external profit remain unknown
or absent unless new evidence supports them.

### 4.4 Objective staged settlement by composition first

The experiment exposed a practical problem: a buyer with a 1.5-unit current
loss cap could not accept a 4-unit unsecured job. The first test should not
solve this by inventing generalized arbitration. It should test whether the
current fixed-price Paid Demand rail can be composed as several independently
authorized objective jobs:

```text
parent generic Agreement
  -> milestone obligation 1 -> existing Quote/escrow instance 1
  -> milestone obligation 2 -> existing Quote/escrow instance 2
  -> milestone obligation 3 -> existing Quote/escrow instance 3

fund instance N only after the exact predecessor evidence permits N
```

The display fixture is 4.0 units of one exact supported TOS-network stablecoin,
split into 1.2, 1.4, and 1.4 units. Implementations use canonical atomic
amounts and the exact asset identifier, not these decimal display strings.
At every authenticated snapshot, the sum of finalized locked value and all
submitted, ambiguous, or reserved funding exposure for the buyer must not
exceed 1.5 units of that same asset. Native TOS Gas is accounted separately
and cannot be disguised as stablecoin exposure.

The 1.5-unit rule is a fixture for one Owner policy, not a protocol constant or
a universal definition of buyer/provider loss. Portfolio policy separately
tracks locked capital, unsecured receivables, execution cost, refund/dispute
reserves, and maximum loss. For each escrow contribution, same-asset release,
refund, and any profile-defined same-asset deduction must not exceed that exact
contribution; native-TOS fees never enter that stablecoin conservation sum.

Each milestone instance retains the current V1 behavior:

- its own Accepted Quote, fixed amount, objective manifest and Receipt;
- full funding before execution admission for that instance;
- full release on the profile-qualified objective success path; or
- full timeout refund under the current contract rules.

A revision that requires another execution is a new execution obligation and
new Quote/escrow/Gate slot under current semantics. A successfully executed
`(quote_commitment, escrow_address)` slot is not reopened by a local
`revision_requested` label.

The composition must not imply partial funding inside one escrow, partial
release, buyer-selected post-delivery acceptance, revision re-execution under
one Quote, a chain `disputed` state, fee split, adjudicator callback, or
subjective quality enforcement. Those semantics are absent from escrow V1.

The current escrow's deadline boundaries, chain time, finality, and bounce
behavior remain exact profile rules; OpenFox must not replace them with one
generic timeout. After an authenticated wallet-request bounce, escrow V1 may
return to `funded` and may accept an old public release/refund request again.
Recovery must therefore prove that no second terminal economic payout occurs
and must account for any additional native-TOS fee; it must not claim that a
replayed request can never create another wallet request.

The reuse trial may still fail. Examples include an inability to bind several
Quotes safely to one parent Agreement, an unacceptable atomicity gap between
milestones, a Quote/manifest model that cannot express the objective slice, or
fees and recovery complexity that defeat the product outcome. Only a recorded
failure of the composition permits a separately versioned staged-settlement
proposal. Such a proposal must define a new Quote binding and contract,
canonical state and amounts, custody authority, time source, conservation,
idempotency, recovery, schema, resolver, errors, positive and negative vectors,
and independent security review. It must not reinterpret V1.

General subjective arbitration, arbitrary split remedies, and a universal
quality oracle remain `DEFERRED`. An Agreement may describe a dispute policy,
and Outcome Events may observe a dispute, but neither fact grants the current
escrow a custody transition it does not implement.

## 5. Keep four state namespaces separate

There is no single authoritative “commerce state machine.” Implementations
must retain the source namespace and authority of every state:

| Namespace | Examples | Authority and use |
|---|---|---|
| Chain escrow V1 | `awaiting_funding`, `funded`, `release_pending`, `refund_pending`, derived released/refunded outcomes | Finalized contract and stablecoin-wallet state; custody authority |
| Agreement and obligation projection | proposed/authorized Agreement versions; settlement obligation `pending`, `partially_paid`, `paid`, `overdue`, `cancelled`, `disputed`, `written_off` | Typed Agreement evidence plus adapter-qualified payment evidence; business obligation accounting, not contract state |
| Semantic action resolution | admitted, submitted, ambiguous, succeeded, failed, terminal successor | Side-effect idempotency, Writer Fence takeover, reservation retention, and query-before-retry recovery |
| Outcome observation | attempt, rejection, rework, dispute, refund, cost, unknown, conflict, correction | Immutable evidence and local projections; never action or custody authority |

A local OpenFox UI may combine these into one view only if it preserves each
qualified source and does not invent a transition. In particular:

- `SettlementObligationStateV1.disputed` does not mean escrow V1 has a
  `disputed` contract state;
- `DELIVERED` or `ACCEPTED` in a workflow view does not authorize release;
- an Outcome Event saying `refunded` does not replace finalized refund
  resolution; and
- an ambiguous funding action retains its atomic Portfolio reservation until
  the same stable action resolves conclusively.

## 6. Authority and safety invariants

Every implementation slice must preserve:

1. Intent, Application, and ordinary conversation are non-authorizing.
2. Changed terms require a new exact predecessor-bound Agreement body and all
   profile-qualified authorization evidence required by that body.
3. An AI may recommend; deterministic policy and typed authority decide.
4. Every external side effect uses the registered stable semantic action,
   exact request digest, current Writer Fence, durable admission, and
   query-before-retry recovery.
5. Aggregate spend, resource, and exposure admission is atomic across every
   Agent and writer sharing one Owner authority.
6. Submitted or ambiguous custody actions retain worst-case exposure through
   crash, Carrier loss, endpoint disagreement, and takeover.
7. One payment or outcome evidence item cannot satisfy two obligations by
   heuristic allocation or be counted twice through several Carriers.
8. Gift is an independent gratuity and never silently settles an Agreement
   obligation.
9. Adapter evidence never claims stronger finality, asset identity, quality,
   privacy, or enforcement than that adapter provides.
10. Private content is hostile input and cannot become prompt, tool, wallet,
    credential, execution, or disclosure authority.

## 7. Non-gating delta work packages and roadmap mapping

These work packages organize implementation; they are not gates, campaign
numbers, or evidence thresholds. They do not reorder Gates D--G, replace the
formal Campaigns 1--6 in the Trusted Capability and Owner Control profile, or
open the locked expansion gate. Formal status and acceptance use only the
current controlling ROADMAP and campaign specifications; a smaller diagnostic
run receives no credit toward their stronger thresholds.

### Work package A — reconciliation and fixtures

- map every experiment request to `REUSE`, `VALIDATE`, `CANDIDATE`, `LOCAL`, or
  `DEFERRED`;
- retain pinned experiment evidence and add deterministic fixtures without
  claiming protocol acceptance;
- add no new shared schema; and
- keep current Gift, direct payment, external settlement, and Paid Demand
  meanings unchanged.

**Diagnostic completion:** no duplicate Intent, Agreement, milestone, Outcome,
cost, reputation, or escrow authority is introduced.

### Work package B — negotiation and cost shadow mode

- exercise counter-offers and Agreement supersession using existing objects;
- record stale, forked, expired, withdrawn, and rejected alternatives;
- connect real cost producers in observe-only mode; and
- verify that rejected or prose-only terms create no side effect.

**Diagnostic completion:** the Section 4.1 negotiation cohort and the
experiment accounting fixture pass without a new portable message.

### Work package C — Outcome evidence and counterparty outcome-risk

- export, import, and independently verify bounded existing Outcome Event
  sets, bundles, and disclosure projections;
- build separate buyer, provider, and service-capability local projections;
- exercise corrections, incomplete cohorts, conflicts, concentration, expiry,
  and privacy; and
- keep outcome-risk advisory and non-authoritative.

**Diagnostic completion:** two independent hosts verify the same evidence
identically while local policy may produce different explainable
recommendations.

### Work package D — current escrow composition

- implement or validate one existing fixed-price escrow per objective
  milestone;
- fund sequentially under the existing aggregate Portfolio reservation;
- test release, timeout refund, replay, crash, bounce, stale writer, ambiguous
  finality, and Carrier loss for every instance; and
- document any concrete reuse failure before proposing a new profile.

**Diagnostic completion:** the 4.0/1.5 stablecoin fixture preserves the current
escrow contract semantics, exact-asset conservation, and exposure bound in
every state. A test that prefunds all 4.0 units must fail local admission even
if each individual escrow would otherwise be valid.

### Work package E — independent multi-host diagnostic

- satisfy the host, Owner, Agent, Carrier, failure-domain, sample, and
  independence requirements of the controlling formal campaign when making a
  formal claim; a focused diagnostic may use fewer samples only when labeled
  non-gating;
- run several market rounds with malicious Intent content, prompt injection,
  signature mutation, replay, related-party clusters, nondelivery, payment
  refusal, endpoint loss, clock skew, network partition, and validator
  disagreement; and
- exercise only settlement paths whose current profile and Owner policy permit
  them.

**Diagnostic completion:** zero unauthorized payments, zero duplicate
execution or transfer, zero aggregate-exposure breach, deterministic recovery,
explicit unknowns and conflicts, and no forced trade. Rational decline is a
successful result.

This result is operational evidence for the exercised profiles only. It is not
public-network decentralization, recurring paid demand, Gate F acceptance, or
permission to implement locked expansions.

## 8. Repository ownership

| Repository or component | Delta responsibility |
|---|---|
| `tos-service-spec` | Own this reconciliation; freeze a genuinely missing portable profile only after a recorded reuse failure and normal versioning/review |
| `tos-service-protocol` | Reuse canonical codecs/verifiers; provide portable helpers and projections only for released or candidate profiles |
| `tos` and `tosctl` | Keep escrow V1 unchanged; implement a future version only after its separate specification, gate, and security review |
| `tos-messenger` | Carry authenticated conversation and existing typed commerce objects; do not create commercial truth from delivery or read state |
| `openfox` | AI reasoning, demand drafting, Owner policy, orchestration, Portfolio admission, local negotiation/outcome-risk/accounting projections, meters, UX, and campaigns |
| Carriers and Gateways | Bounded transport, indexes, provenance, availability, and optional ranking; never Agreement, trust, acceptance, or settlement authority |
| Independent operators | Cross-implementation verification, adverse-path execution, evidence retention, and external acceptance |

The full experimental report remains in OpenFox because it is operational
evidence. This cross-repository delta belongs here because it reconciles shared
protocol and settlement boundaries. OpenFox should link to released profiles
instead of maintaining a second normative copy.

## 9. Required validation matrix

| Area | Positive validation | Mandatory negative and recovery validation |
|---|---|---|
| Intent and negotiation | demand with several applications; price counter; scope reduction; current Agreement authorization | prose-only acceptance, stale/expired/forked version, wrong predecessor, mutation, replay, withdrawal, aggregate-capacity overflow |
| Agreement milestones | obligation DAG with sequential objective slices and exact adapter per payment | dependency skip, predecessor rewrite, wrong acceptance profile, one evidence item allocated twice |
| Existing escrow composition | independent fund/release and timeout-refund cycles; rolling exposure within cap | all-at-once prefunding, wrong asset/payee/Quote, partial funding assumption, split/dispute transition, bounce, ambiguous finality, duplicate request, stale writer |
| Portfolio and actions | atomic reservation, exact replay, terminal successor, restart recovery | concurrent overflow, reservation leak, new ID after ambiguity, same ID with different request |
| Outcome evidence | positive, adverse, ambiguous, corrected, explicitly incomplete, privacy-scoped bundles | forged issuer, wrong Agreement or party, conflicting repeat identity, same event through several Carriers, success-only reliability claim, missing denominator, private-data leak |
| Counterparty outcome-risk | distinct buyer/provider/service-capability views with explainable policy revision | projection authorizes action or executable-capability admission, `.tos` name treated as proof, missing evidence treated as success, global-score claim |
| Economics | actual meter/invoice/finality evidence, per-asset ledger, source fixture | reserve reported as cash, unknown reported as zero, related-party transfer reported as external revenue, unproven purchase reported as ROI |
| Multi-host | independent hosts/owners/Carriers, repeated rounds, removal and reconstruction | partition, clock skew, hostile Intent, prompt injection, endpoint loss, nondelivery, refusal, evidence omission |

Deterministic codec, verifier, race, fuzz, crash-restart, canonical-vector, and
independent-implementation tests remain required at each boundary where they
apply. A long-running social experiment does not replace them.

## 10. Deferred work and decision triggers

The following are not approved implementation work by this document:

- a universal `CounterOffer` object;
- a new portable reputation record or global score;
- a generalized multi-slot escrow contract;
- subjective buyer-quality enforcement in escrow;
- partial release/refund, split fees, adjudicator callbacks, appeals, or a
  chain `disputed` state;
- cross-asset or cross-network accounting without exact conversion evidence;
  or
- expansion ahead of recurring paid-demand acceptance.

A deferred item becomes a candidate only when its owner records:

1. the exact existing profile and composition that were attempted;
2. a reproducible case that existing semantics cannot express safely;
3. the smallest missing portable authority or evidence boundary;
4. compatibility, privacy, recovery, and failure consequences;
5. why a local OpenFox policy or projection is insufficient; and
6. the governing roadmap gate and measurable customer outcome.

## 11. Completion claim

This document is complete when the classification, authority boundaries,
conflict dispositions, and tests survive independent review. Work-package
completion requires the code and evidence named by that package. No package may
claim a new wire profile, escrow feature, production acceptance, recurring
demand, or roadmap-gate completion unless its controlling specification and
ROADMAP independently record that fact.
