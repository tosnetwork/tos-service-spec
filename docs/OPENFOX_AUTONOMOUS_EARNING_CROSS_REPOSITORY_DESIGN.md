# OpenFox Autonomous Earning — Cross-Repository Design

**Status:** incubation design; implementation and external acceptance pending

**Blocking status:** read-only discovery may proceed after its minimal schema
freeze, but Provider Offer acceptance, paid execution, and automatic commercial
action remain blocked until the D2 multi-source/independent-verifier gate, the
complete mutation-bound buyer acceptance context, bilateral typed accepted-work
authorization, portable market-delegation proofs, Provider-wide fenced
admission, per-Offer single acceptance, contract-enforced demand-wide one-
Provider selection, and proof-of-possession private-input delivery are
implemented.

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
- [`AGENT_ECONOMY_METRICS_V1.md`](AGENT_ECONOMY_METRICS_V1.md)
- [`ROADMAP.md`](ROADMAP.md)

For paid-demand artifact construction, verification, distribution gates,
bilateral acceptance, private Provider admission, and recovery invariants,
[`AGENT_PAID_DEMAND_DISCOVERY_V1.md`](AGENT_PAID_DEMAND_DISCOVERY_V1.md) is the
specialized governing design and prevails over any abbreviated summary here.
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
accepted-work extension to Quote, escrow, Execution Gate, Receipt, and safe
handoff before any paid execution; this is not left to an application journal.

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
- typed accepted-work convergence binding Demand, Offer, buyer, input,
  evidence, reconstructible buyer acceptance, and reconstructible Provider
  Offer authorization into finalized commercial state;
- per-Offer single acceptance, demand-wide one-Provider selection, and
  deterministic Quote/escrow derivation;
- buyer-push private-input delivery to a Provider-bound ingress;
- competitive pricing and offer revision without allowing model prose to
  authorize a commitment;
- private portfolio and runtime-capacity reservation after canonical body/action
  construction and before Provider authorization;
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
active Demand Mutation + Provider fields + durable Offer identity
  -> unsigned typed AcceptedWorkBody
  -> Provider authorization creates one Provider Offer
  -> buyer authorization completes AcceptedWorkTerms
  -> exact buyer wallet atomically consumes the Demand Acceptance Key
  -> finalized Accepted Quote and funded escrow embedding those terms
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

## 4. Repository ownership

| Repository | Must own | Must not own |
|---|---|---|
| `tos-service-spec` | normative Demand Mutation, market delegation, Provider Offer, AcceptedWorkTerms, private-input, task/execution/validator/evidence schemas when approved; bounds; canonical encodings; authority/state-machine invariants; vectors; acceptance contract | runtime schedules, private policy, private credentials, mutable market indexes |
| `tos-service-protocol` | generated types; canonical encoders/digests; signature and finalized-state verification; negotiation, Accepted Quote, provider, Receipt, settlement, and recovery SDKs; conformance helpers | opportunity ranking, model planning, operator portfolio policy, custody secrets |
| `tos-service-gateway` | bounded searchable projection of non-expired demand; cursors; federation; rate limits; authenticated publish/withdraw/relay transport; explicit provenance and freshness | canonical task acceptance, buyer solvency truth, ranking authority, custody, provider execution, settlement truth |
| `openfox` | durable earning coordinator; source federation; verifier orchestration; skill/capacity matching; economics; pricing strategy; deterministic policy; owner-private process lock; Provider writer-lease client/recovery; Offer/later-bid journal; execution orchestration; local P&L; operator explanation and control | protocol codecs, chain truth, raw chain keys, task-selected authority, unrestricted tool execution |
| `tos-ai` | implementation/operation of spec-defined task, execution, validator, evidence and private-input profiles; deterministic estimates; durable body-bound runtime capacity leases; bounded executors; metering; artifacts; execution replay protection | freezing normative profiles, market authority, economic policy, wallet custody, final settlement recognition |
| `tos-messenger` | paid-demand public-channel and direct-offer profiles; authenticated Agent conversations; replay-safe transport; verification/synchronization/persistence integration over TOS networking; device/session custody | generic DHT/Overlay/RLDP/Storage primitives, market ranking, Quote/escrow authority, execution authority, wallet authority from prose |
| `tos` / contracts | generic DHT/Overlay/ADNL/RLDP/Storage primitives; canonical Agent delegation; demand-wide first-finalized acceptance key; accepted-work/Quote, escrow, Receipt, dispute, transfer, and final settlement transitions | task search, bid ranking, private cost models, OpenFox objectives, execution planning |
| `tosctl` or equivalent custody boundary | Provider-wide exclusive writer lease; rollback-resistant generation and issuance ledger; unresolved Demand-tuple and aggregate-exposure admission across shared instances/keys/mandates/runtimes; stable-action conflict/replay handling; semantic confirmation; delegated signing; broadcast; ambiguous-submit resolution; revocation integration | opportunity selection, model prompts, execution or accounting policy; public market-artifact fields for private admission state |
| `doc` | ecosystem-level product explanation synchronized after the design is accepted | normative schemas, implementation status without evidence, runtime behavior |

Any canonical field or digest addition starts in
`proto/tos/service/v1/native.proto` in this repository. Implementations must not
create a competing JSON, database, or application schema and later treat it as
protocol authority.

## 5. End-to-end architecture

```text
buyer / task issuer
  -> publish bounded Demand Mutation
  -> one or more replaceable Gateways index the envelope

OpenFox earning scout
  -> federated cursor reads
  -> historical signature + current delegation authorization eligibility
  -> observed mutation-chain integrity, source freshness, provenance, and bounds
  -> never claim an off-chain globally complete mutation head
  -> direct finalized Agent/Capability/network verification
  -> typed skill + evidence + capacity match
  -> integer economics + portfolio exposure calculation
  -> deterministic mandate decision

OpenFox provider
  -> load the active Mutation's complete buyer authorization context
  -> choose one durable Offer identity and Provider terms
  -> construct one unsigned typed AcceptedWorkBody
  -> reserve private capacity and pass Provider-wide admission
  -> sign that body to create one single-acceptance Provider Offer
  -> resolve ambiguity before any retry
  -> buyer selects the Offer and signs the same unique typed AcceptedWorkBody
  -> complete AcceptedWorkTerms carries both proofs
  -> finalized extended Accepted Quote + funded escrow

private input boundary
  -> buyer pushes committed bytes to Offer-bound Provider ingress
  -> ingress verifies buyer proof of possession, challenge, digests, media and
     archive bounds

tos-ai execution boundary
  -> Native Execution Gate compares every finalized accepted-work field
  -> Gate claims the exact paid execution once
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

The transport-neutral paid-demand envelope, public-channel carriage,
DHT/Overlay/Storage boundary, replaceable indexing, federated discovery,
direct Provider Offer, abuse controls, and work-square projection are defined
in [`AGENT_PAID_DEMAND_DISCOVERY_V1.md`](AGENT_PAID_DEMAND_DISCOVERY_V1.md).
This section retains only the cross-repository earning-control-plane summary.

### 6.1 Why a demand profile is needed

Current Capability search answers “what can I buy?” It does not answer “which
buyer currently wants work that I can profitably perform?” A provider earning
loop therefore needs a paid-demand discovery profile.

The initial profile should support fixed-price, objectively verifiable
software work. Competitive bidding is added after fixed-price offering works
end to end. General job boards, subjective arbitration, subcontracting, GPU
markets, and cross-chain payments remain later profiles.

### 6.2 Pre-acceptance artifacts

The design requires the following conceptual artifacts. Their exact fields and
canonical encoding are not frozen by this document:

- **Demand Mutation** — buyer identity, monotonic sequence, predecessor, kind
  (`active_revision` or `terminal_withdrawal`), task/input/evidence terms,
  exact asset, deadlines, and one complete `BuyerAcceptanceProfile` that fixes
  the buyer settlement wallet, exact `accepted-work.accept` key, constrained
  delegation/proof/authority reference, and upload proof-of-possession key before
  any Provider signature, plus expiry and signature;
- **Provider Offer** — the Provider first combines the exact active Mutation,
  preallocated Offer identity, and Provider-owned terms into one unsigned typed
  `AcceptedWorkBody`; its `provider-offer.sign` authorization over that body
  creates the Offer. The body fixes active Mutation digest, buyer context,
  provider Agent and Capability/version, exact price, delivery window,
  execution/evidence/private-input profiles, `max_acceptances=1`, and expiry;
  private writer-generation, reservation, runtime-lease, and admission-ledger
  data never enter these public bytes;
- **Selection Notice** — buyer's non-canonical notice of a selected offer and
  the terms expected in the Accepted Quote; and
- **AcceptedWorkTerms** — a typed unsigned accepted-work body plus
  reconstructible buyer `accepted-work.accept` and Provider
  `provider-offer.sign` authorization proofs, committed by the unique Accepted
  Quote and escrow. The body fixes the exact single delegated Ed25519 key and
  proof profile, validity bounds, and canonical portable authority-reference
  digest for each side, so alternate authorized keys, threshold subsets, proof
  paths, or wrappers cannot create another Quote. Each signature also binds
  the digest of its canonical proof context. The full Provider Offer digest is
  derived from the unsigned body plus Provider proof and is never contained in
  its own signed body. An Offer digest alone is not Provider consent.

These artifacts are hostile, replayable Internet inputs. A valid signature
proves origin only. It does not prove funding, solvency, availability, quality,
selection, or payment.

Messenger, Selection Notice, Gateway, or index data cannot complete or rotate a
missing buyer context. Such a change requires a successor active Demand Mutation
and a newly constructed and authorized Provider Offer.

Before an implementation PR adds these messages or services, the specification
PR must place their canonical representations in the sole Native protobuf
schema and define bounds, canonical ordering, digest domains, purpose-limited
market delegation, Demand Mutation rules, rejection behavior, retry semantics,
and frozen vectors first.

### 6.3 Discovery semantics

A Gateway may index, rank, filter, paginate, relay, and expire demand. Every
result includes source Gateway, observation time, issuer, mutation sequence,
mutation digest, envelope
digest, and cursor provenance. A Gateway must not claim that a listing is:

- accepted or funded;
- still available merely because it has not expired locally;
- profitable for a particular provider;
- authorized for execution; or
- guaranteed to settle.

OpenFox deduplicates identical envelope digests across Gateways, rejects
conflicting reuse of a buyer/demand/mutation sequence, and retains source
provenance. Before offering it verifies historical signing authorization,
fresh current Agent/delegation eligibility, and the integrity/freshness of the
exact observed mutation chain. Because no canonical feed head exists, it does
not claim that no unseen successor, withdrawal, or fork exists. Before
execution it ignores the listing and verifies the complete bilateral finalized
AcceptedWorkTerms, Quote, and escrow through the extended Native Execution
Gate.

A known terminal withdrawal or fork fails closed before Offer signing. Absence
of one is only source-bounded evidence. Final acceptance instead relies on the
Provider authorizing the exact accepted-work body, the buyer separately
authorizing that body, and the committed buyer wallet atomically consuming the
stable Demand Acceptance Key while finalizing/funding the exact Quote and escrow.
Globally enforceable pre-acceptance cancellation would require a canonical
on-chain demand head and is deliberately outside this profile.

### 6.4 Provider Offer and later-bid safety

Every mutation, Offer, Selection Notice, input delivery, and submission has an
OpenFox-generated durable action identity outside model control. Exact replay
is idempotent. Reuse of an identity for different content is a conflict.

An ambiguous network result never causes a blind retry. The coordinator first
queries the destination, negotiation peer, or finalized TOS state appropriate
to the action. If no authoritative resolution operation exists, the action is
marked ambiguous and requires operator review or safe expiry.

One preallocated Provider Offer identity is buyer-specific and fixes
`max_acceptances=1`. Together with the exact Mutation and Provider terms it
determines one unsigned accepted-work body, Quote commitment, and escrow
StateInit. The Provider authorization over that body creates the signed Offer;
selection adds a distinct buyer Agent authorization, while the exact
buyer wallet atomically consumes the stable Demand Acceptance Key while it
authorizes/funds the finalized Quote transaction. The first finalized
compare-and-set selects one Provider across every Offer and Mutation under the
Demand identity; exact replay returns that winner and a competing acceptance
conflicts. OpenFox atomically reserves capacity before signing and converts or
releases that reservation only after resolving the deterministic escrow. Private input is
buyer-pushed with proof of possession to the Provider ingress bound by the
Offer and accepted terms; remote task content never selects a Provider fetch
target or credential.

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

- capacity is privately reserved before Provider authorization and converted
  only after the unique bilateral acceptance and funded escrow finalize;
- after Provider authorization, withdrawal, expiry, or local cancellation enters
  a resolving state and retains exposure until deterministic acceptance absence
  is proved;
- every ambiguous state preserves its origin phase, operation, and stable action
  ID, and only its phase-specific resolver may advance or compensate it; and
- execution, submission, Receipt, dispute, and settlement recovery cannot
  regress to `ACCEPTED`, reopen a terminal state, or repeat an economic action.

No local transition creates a protocol fact. From acceptance onward, the
record stores immutable references to the typed accepted-work body, both
bilateral authorization proofs, unique Quote commitment, escrow address,
execution identity, Receipt, and finalized checkpoints. On disagreement,
verified chain state wins and the local projection is rebuilt or quarantined.

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
- concurrent accepted, executing, and disputed tasks;
- resource-class capacity and reservation headroom;
- counterparty and task-profile concentration;
- unresolved bids, submissions, settlement intents, and receivables;
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
the complete finalized `AcceptedWorkTerms`, Accepted Quote, and escrow. A
mismatch causes rejection or a new Offer, not silent substitution. Reservations
convert to accepted obligations on unique Quote/escrow finality. Before Provider
authorization they may compensate on a verified terminal path; after Provider
authorization they remain held through withdrawal/expiry/cancellation
resolution and release only after the acceptance deadline plus deterministic
proof that no valid acceptance can still finalize.

### 8.2 Execution admission

Every transport must reach the shared Native Execution Gate after its mandatory
accepted-work extension is implemented. The extended Gate independently decodes
the finalized `AcceptedWorkTerms` and verifies the Accepted Quote, funded
escrow, buyer authorization, exact buyer-wallet acceptance, Provider Offer
authorization, the body-derived Demand Acceptance Key and its exact finalized
winner, portable issuance references and acceptance-time revocation ordering,
Demand Mutation, provider, Capability/version, manifest, execution signer,
transport binding, input/source, validator/evidence, asset/amount, and deadlines
before atomically claiming the execution slot. The current narrower Gate is
reusable infrastructure, not sufficient admission for paid D3 work.

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
15. An Offer identity or digest alone is not Provider consent. Finalized paid
    execution requires both Agent-level authorizations over the same typed body
    plus the exact buyer-wallet acceptance transaction.
16. The accepted-work body fixes one delegated Ed25519 key, canonical proof
    context, portable authority-reference digest, validity bounds, and encoding
    per side; authorization-proof choice cannot change the unique Quote or
    escrow identity.
17. Every active Demand Mutation fixes the complete buyer acceptance and upload
    context before Provider authorization; chat, selection, Gateway, or index
    data cannot complete or rotate it.
18. No commercial phase or MVP may pass on one source: D2 requires at least two
    independently operated and implemented carriers/indexes, source-plus-store
    shutdown recovery, and an independent codec/verifier.
19. Every Provider signature passes a rollback-resistant Provider-wide writer
    fence and aggregate admission boundary spanning all shared instances, keys,
    mandates, runtimes, unexpired Offers, and unsettled obligations. That private
    state is not copied into public market artifacts.
20. Per-Offer `max_acceptances=1` is supplemented by one contract-enforced
    Demand Acceptance Key. Its first finalized atomic consumption binds the
    exact winning Mutation, Offer, terms, Quote, escrow, and buyer-wallet funding
    across all competing Providers and Demand revisions.

## 10. Cross-repository interfaces

The implementation must stabilize these interfaces before enabling automatic
commercial action:

| Interface | Producer | Consumer | Required semantics |
|---|---|---|---|
| demand discovery page | Gateway | OpenFox | bounded cursor, provenance, expiry, signed envelope, explicit non-authority |
| demand verification | protocol SDK | OpenFox | canonical digest/signature checks plus finalized Agent/network resolution; observed-chain integrity without global-head claims |
| skill descriptor | OpenFox skill registry / `tos-ai` profile catalog | OpenFox matcher | versioned exact compatibility and operator approval |
| estimate | `tos-ai` | OpenFox economics | fixed-point/integer bounds, version, validity, resource class |
| capacity reservation | `tos-ai` | OpenFox coordinator | durable Offer/body-bound, expiring, idempotent reserve/convert/release; ambiguous acceptance retains capacity |
| Demand Mutation / Offer | protocol/Messenger adapter | OpenFox | market-purpose authorization, sequence/single-acceptance, exact action, idempotency, ambiguity resolution |
| mandate decision | OpenFox deterministic policy | custody adapter | exact action digest, limits, mandate version, expiry |
| Provider-private admission | custody adapter | OpenFox coordinator | exclusive writer lease, rollback-resistant fencing high-water mark, stable-action replay, unresolved-tuple and aggregate exposure across every shared signer/runtime; atomic record before signature release |
| accepted-work convergence | protocol + TOS contracts | Gate/custody/OpenFox | unsigned typed body plus reconstructible buyer/Provider authorization proofs embedded in unique Quote/escrow; exact buyer-wallet finality |
| demand-wide acceptance | TOS Accepted Quote/escrow contract | buyer, Providers, Gate, recovery clients | deterministic key from stable Demand identity; first-finalized atomic compare-and-set records exact Mutation/Offer/terms/Quote/escrow and funding; exact replay or conflict resolution |
| private-input push | Provider ingress | buyer + `tos-ai` | Offer-bound endpoint/challenge, buyer upload proof of possession, exact committed bytes, idempotent status resolution, no Provider pull |
| execution admission | Native Execution Gate | `tos-ai` runner | verify both authorizations/revocation ordering, compare every finalized accepted-work field, and admit one shared claim |
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
- freeze bounded Demand Mutation with complete `BuyerAcceptanceProfile` and
  single-acceptance Provider Offer artifacts in Native protobuf;
- freeze market delegation scopes/static bounds, portable historical authority,
  current authorization eligibility, acceptance-time revocation ordering,
  signatures, sequences, terminal withdrawal, the non-canonical-head boundary,
  digests, ordering, errors, retry behavior, and vectors;
- freeze the field-level binding sufficiency matrix, typed AcceptedWorkBody,
  bilateral authorization proofs, complete AcceptedWorkTerms, unique Quote/
  escrow derivation, shared Demand Acceptance Key, and Execution Gate
  comparisons;
- freeze Provider-private writer-fencing, rollback-resistant issuance,
  aggregate-admission, and recovery invariants without adding private state to
  public artifacts;
- define spec-owned task, execution, validator, evidence, and private-input
  profiles plus implementation-owned skill and estimate versioning;
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
- create one typed AcceptedWorkBody, Provider authorization, buyer acceptance
  authorization, and unique extended Accepted Quote/escrow whose funding
  atomically consumes the shared Demand Acceptance Key;
- race a synthetic competing Provider Offer and Mutation revision to prove one
  first-finalized demand-wide winner before product-level competitive bidding;
- push exact private input through the Offer-bound proof-of-possession Provider
  ingress;
- make the Native Execution Gate verify both authorizations and compare every
  finalized accepted-work field;
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

S1  tos-service-spec: AcceptedWorkBody/bilateral authorization/Demand Acceptance Key/
    private-input vectors + Provider-private fencing/admission invariants
 |
 +-> C1  tos: demand-wide acceptance CAS + extended Quote/escrow typed body/proofs
 +-> P1  tos-service-protocol: accepted-work resolver/SDK/safe handoff
 +-> E1  execution Gate: compare every finalized accepted-work field
 +-> A1  tos-ai: private ingress + exact executor/validator/evidence mapping
 +-> F1  custody: exclusive writer lease + rollback-resistant generation/issuance
          + unresolved-tuple and Provider-wide aggregate admission

S1 + C1 + P1 + E1 + A1 + F1 + D1/D2 acceptance
  -> O1: guarded single-acceptance Provider Offer
  -> E2E testnet fixed-price acceptance
  -> production mandate and external evidence
  -> competitive bidding and additional profiles
```

The binding review has already proven that the current Accepted Quote/escrow
does not express all required accepted-work facts, so C1 is mandatory before
paid D3 execution. Messenger receives a PR only for public-channel and selected
negotiation/approval transport integration; generic DHT/Overlay/RLDP/Storage
primitives remain in `tos`, and OpenFox must also work through a non-Messenger
protocol adapter.

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
  but paid-demand execution requires an explicitly versioned accepted-work
  extension. Pre-acceptance market data cannot reinterpret an old Quote as if
  it carried the new bindings.

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
- typed AcceptedWorkBody, non-circular bilateral authorization proofs, complete
  AcceptedWorkTerms, and deterministic Quote/escrow reproduction;
- shared Demand Acceptance Key derivation across Mutations/Offers, atomic
  funding and first-finalized winner update, exact replay, conflicting winner,
  and resolver recovery;
- explicit body → Provider proof/Offer digest → buyer proof → terms digest
  reproduction with rejection of every circular digest dependency;
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

### OpenFox

- deterministic replay of discovery, matching, economics, and policy;
- recommend/approval records with no canonical body, reservation, custody, or
  signature effect; exact one-shot proposal binding without persistent mode
  increase;
- concurrent budget and capacity races;
- Provider Offer/later-bid crash at every journal transition;
- Offer single-acceptance and capacity reserve/convert/release races;
- competing Provider/Mutation acceptance races under one Demand Acceptance Key;
- same-host duplicate writer, partitioned stale generation, aggregate exposure,
  rollback-resistant issuance restore, and full-exposure fail-closed recovery;
- restart with accepted, executing, submitted, disputed, and settling work;
- pause, drain, mandate expiry, custody revocation, and emergency stop;
- hostile task prompt and tool/credential/network escalation attempts;
- stale estimates, cost spikes, fee exhaustion, and settlement delay; and
- learning data that includes losses and attempts to expand authority.

### Execution and settlement

- profile-to-runtime mapping and sandbox conformance;
- buyer-push private ingress and hostile URL/credential/archive/challenge inputs;
- stolen bearer challenge, wrong buyer upload proof-of-possession key,
  concurrent/conflicting upload, exact retry, ambiguous ACK, and status
  resolution;
- reservation expiry and accepted-profile mismatch;
- Execution Gate comparison against every AcceptedWorkTerms field;
- cross-transport duplicate execution reaching one shared claim;
- validator failure despite process success;
- evidence tampering, Receipt signer mismatch, refund race, and dispute path;
- provider-wallet credit checked through independent endpoints; and
- exact reconciliation after Gateway, OpenFox, worker, or custody restart.

### External acceptance

At least five independently controlled roles participate: buyer, provider, two
qualifying source operators, and an independent verifier/resolver. Each claimed
independent source records
operator/signing identity, host/process/store, network path, upstream carrier,
implementation/codec dependency, and failure domain. Evidence also records
repository commits, network domain, Agent and Capability/version, Demand
Mutation/Offer/AcceptedWorkBody/authorization-proof digests, Quote commitment,
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
   its complete mutation-bound `BuyerAcceptanceProfile`, with no global market-
   head claim or Messenger/Gateway completion;
4. typed skill/capacity matching and reproducible exact-asset economics under a
   narrow owner mandate;
5. same-host process exclusion plus rollback-resistant Provider-wide writer
   fencing, unresolved-tuple and aggregate-exposure admission across every
   shared instance, key, mandate, runtime, unexpired Offer, and obligation;
6. one privately reserved, idempotent, buyer-specific, single-acceptance
   Provider Offer whose Provider and buyer authorize the same deterministic
   `AcceptedWorkBody`, followed by the exact buyer-wallet-funded unique Quote and
   escrow atomically recorded as the first and only winner under the stable
   Demand Acceptance Key across competing Providers and revisions;
7. private input admitted only through the Mutation- and Offer-bound proof-of-
   possession buyer-push ingress;
8. one Native Execution Gate admission, bounded execution, objective validation,
   immutable evidence, Receipt submission, and independently resolved finalized
   provider credit;
9. restart, takeover, duplicate, ambiguity, withdrawal/finality race, dispute,
   refund, and stale-writer tests without duplicate work or excess exposure;
10. append-only realized P&L reconciliation, explanation, owner pause/revoke/
    drain controls, and recovery without a Gateway, market database, or local
    journal becoming settlement authority.

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
2. What exact encoding freezes the purpose-limited market delegation/static
   bounds, portable historical authority proof, Demand Mutation sequence,
   terminal withdrawal, explicit non-canonical-head boundary, and issuance/
   acceptance-time authorization rules selected by the focused discovery
   design?
3. Which buyer proof, deposit, or anti-spam mechanism is sufficient before an
   earning Agent spends material resources evaluating demand?
4. What exact AcceptedWorkBody, non-circular buyer/Provider authorization
   proofs, complete AcceptedWorkTerms, Quote/TVM, escrow StateInit, resolver,
   Execution Gate, Receipt, and safe-handoff encodings implement the mandatory
   binding matrix?
5. What exact contract/state owner, Demand Acceptance Key derivation, TVM layout,
   atomic buyer-wallet funding/winner update, per-Offer enforcement, exact-
   replay/conflict resolver, finalized query, and recovery semantics guarantee
   one accepted Provider across every Offer and Mutation of a stable Demand?
6. What exact ingress/challenge, buyer upload proof-of-possession, status,
   encryption, and retention profile implements buyer-push private input
   without Provider pull, task-selected endpoints, bearer-only authority, or
   credential proxying?
7. Which software-work subset is safe for the first autonomous Offer, and what
   maximum cost/exposure bounds apply?
8. Which cost sources are reproducible enough for automatic authorization, and
   which remain owner-configured conservative ceilings?
9. What operation resolves an ambiguous mutation, Offer, input delivery, result
   submission, and settlement intent for each supported transport?
10. How are legal restrictions and operator-specific compliance represented as
   local policy without making a Gateway a universal authority?
11. What exact operator/host/store/upstream/implementation diversity is required
    for independent-source acceptance?
12. What external recurring-use threshold permits competitive multi-offer
    bidding and the next task profile under the existing Expansion Gate?

Until these decisions are frozen and tested, OpenFox may implement only the
read-only scout and local simulations; D2 may test propagation without Offers.
Provider Offers, paid execution, automatic commercial action, later bidding,
and production operation must not be inferred from the presence of this design
document.
