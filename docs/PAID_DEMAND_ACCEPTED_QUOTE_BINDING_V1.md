# Paid-Demand Binding to the Existing Accepted Quote Rail V1

**Status:** incubation design; schema freeze, implementation, and independent
acceptance pending

**Existing-rail status:** the Native commercial rail already supports the
bounded Capability-first lifecycle from Quote Proposal through finalized
Accepted Quote, stablecoin escrow, Native Execution Gate, bounded execution,
Receipt, release or refund, and finalized settlement. This document does not
replace that rail.

**Blocking status:** paid-demand Provider Offer acceptance and execution remain
blocked until the discovery profile's D2 two-source, source-plus-database
shutdown, and independent-verifier gate passes, and until the binding extension,
Provider Offer authorization, per-Offer determinism, Provider-private admission,
proof-of-possession input delivery, exact duration/preflight/release-pipeline
profile, zero-bounce initial wallet-request proof, replay-aware semantic action
identity/recovery, fresh same-claim first-start preflight, and successor escrow
execution-deadline check in this document are frozen, implemented, and
independently verified.

## 1. Purpose

This document defines the smallest safe handoff from a selected paid-demand
Provider Offer into the existing TOS Service Accepted Quote lifecycle.

The boundary is:

```text
Paid Demand + active Mutation
  -> Provider Offer + buyer selection
  -> typed paid-demand Quote-binding extension
  -> existing Accepted Quote and escrow rail
  -> existing Native Execution Gate and bounded executor
  -> existing Receipt, release/refund, and settlement rail
```

Only the first three lines add paid-demand semantics. The final three lines are
the existing commercial rail, extended only where it must decode and enforce
the new binding. There is no second Quote, market escrow, execution authority,
Receipt, ledger, settlement protocol, or application-owned commercial truth.

The public discovery and direct response profile is defined in
[`AGENT_PAID_DEMAND_DISCOVERY_V1.md`](AGENT_PAID_DEMAND_DISCOVERY_V1.md).
The existing rail remains governed by:

- [`SETTLEMENT.md`](SETTLEMENT.md);
- [`ACCEPTED_QUOTE_TVM_V1.md`](ACCEPTED_QUOTE_TVM_V1.md);
- [`STABLECOIN_ESCROW_TVM_V1.md`](STABLECOIN_ESCROW_TVM_V1.md);
- [`NATIVE_EXECUTION_GATE_V1.md`](NATIVE_EXECUTION_GATE_V1.md);
- [`SOFTWARE_WORK_EXECUTION_V1.md`](SOFTWARE_WORK_EXECUTION_V1.md);
- [`SOFTWARE_WORK_RECEIPT_TVM_V1.md`](SOFTWARE_WORK_RECEIPT_TVM_V1.md);
- [`SAFE_HANDOFF_V1.md`](SAFE_HANDOFF_V1.md); and
- [`OPENFOX_ECONOMIC_BRIDGE_V1.md`](OPENFOX_ECONOMIC_BRIDGE_V1.md).

Where this document conflicts with an existing rail invariant, the existing
normative specification prevails until an explicit versioned extension is
approved in that specification. Implementations must not silently fork the
rail in application code.

## 2. Why a binding extension is required

The existing Capability-first rail proves that OpenFox can participate in a
narrow paid lifecycle. It already provides canonical Quote construction,
deterministic escrow, finalized funding checks, at-most-once execution,
objective Receipt processing, and finalized settlement recovery.

Paid-demand selection introduces facts that the current Accepted Quote does
not bind completely:

- buyer Agent-to-existing-escrow-wallet binding (the existing escrow terms
  already bind the exact buyer and Provider wallet addresses);
- stable Demand identity and the selected active Mutation;
- the selected Provider Offer and Provider consent;
- exact task input and source commitments;
- task-level output, validator, and evidence profiles;
- the buyer upload proof-of-possession key and Provider-selected ingress;
- Provider Offer delegation and acceptance-time revocation ordering.

Those facts cannot live only in Messenger prose, a Selection Notice, a Gateway
row, an OpenFox journal, or an opaque digest whose typed preimage is unavailable
after the market disappears. The approved solution must therefore be a
versioned extension of the existing Accepted Quote preimage and resolver
surface.

If the existing Quote schema gains a generic, reconstructible typed-extension
mechanism that satisfies every field below, this profile uses it. Otherwise the
existing Accepted Quote, escrow StateInit, resolver, Gate comparison, and safe-
handoff schemas are versioned together. The existing Receipt continues to link
transitively through the Quote commitment unless a separate review proves a
concrete schema gap. Either approach retains one commercial state machine and
one authoritative settlement rail.

Accepted Quote schema 1 has no extension slot, and its frozen decoders reject
trailing data. An implementation therefore needs an explicit Accepted Quote
schema successor (or a separately approved generic extension), a corresponding
escrow code/parser identity, and resolver, safe-handoff, and Gate support for
that version. Existing schema-1 Quotes and escrow contracts remain unchanged.
This is a versioned payload/parser integration, not an application-side digest
or a second lifecycle.

Schema 1 keeps its frozen deployment-as-acceptance rule and cannot carry this
profile. It is never reinterpreted as having the successor state below.

That successor also needs a recoverable buyer-acceptance transition. Its
deterministic StateInit starts in `pending_acceptance`; deployment alone is not
Quote acceptance. Only a versioned `accept` operation authenticated by the
exact buyer wallet committed in escrow terms may transition the contract once
to `awaiting_funding`. A third party may deploy the public StateInit first, but
cannot consume or block that transition. When the address is undeployed, the
buyer wallet may carry the same StateInit and `accept` operation in one message;
when it was predeployed, the identical operation remains valid. The finalized
`pending_acceptance -> awaiting_funding` transition is the paid-demand Quote
acceptance event. The operation names the expected Quote commitment and Offer
digest; an exact replay after acceptance is an idempotent observation of the
same state, while a different sender or commitment cannot mutate it. Ambiguous
`accept` broadcast resolves the exact escrow state before retry. Funding remains
a later transition.

## 3. Authority boundary

| Decision or fact | Authority |
|---|---|
| demand publication and current observed Mutation | signed paid-demand artifacts plus historical/current Agent authorization checks |
| Provider consent to exact work | canonical Provider Offer authorization over one typed body |
| buyer Agent publication intent and handoff context | exact signed active Demand Mutation and its `BuyerHandoffProfile` |
| buyer commercial acceptance of one exact Provider Offer | finalized versioned escrow `accept` transition authenticated to the exact bound buyer wallet |
| execution funding eligibility | later exact finalized stablecoin funding notification under the existing escrow lifecycle |
| execution admission | existing shared Native Execution Gate after decoding and comparing the extension |
| objective result | existing software-work Receipt bound to the existing Quote commitment and its current input/source/result fields |
| release, refund, and realized revenue | existing finalized escrow and wallet state |

A Provider Offer is not an Accepted Quote. A Demand signature is not commercial
acceptance or payment. A Selection Notice is not selection authority. A buyer-
side preference to choose only one Provider is not a global chain invariant.
Provider-private capacity state is not public acceptance authority. Finalized
TOS state remains the only commercial authority after handoff.

### 3.1 Job-scoped truth and the ACP alignment boundary

The useful ACP principle is a small, deterministic Job lifecycle with explicit
roles and a distinct result-submission boundary. It applies to one exact
purchase after its parties and terms are bound. Pre-acceptance Demand and Offer
rows are participant-local Opportunity projections, not Jobs, and this model
does not imply one source of truth for the global opportunity feed.
This deliberately differs from ERC-8183, where a Job exists in `Open` before
funding and may initially have no Provider. TOS terminalizes the immutable-key
Opportunity row with an `accepted_job_ref` and creates a separate Commerce Job
row only after a schema-valid Accepted Quote fixes the parties and terms; it
does not rekey the Opportunity row.

For TOS, the exact Accepted Quote and escrow become the job-scoped commercial
authority only under their schema-appropriate acceptance rule. Before that
point, carriers and market applications expose incomplete observations. After
that point, the Quote, escrow, Gate claim, Receipt, and finalized wallet
transactions reconstruct one purchase without the discovery source.

SDKs may expose the coarse projection defined in
[`OPENFOX_AUTONOMOUS_EARNING_CROSS_REPOSITORY_DESIGN.md`](OPENFOX_AUTONOMOUS_EARNING_CROSS_REPOSITORY_DESIGN.md):

```text
QUOTE_ACCEPTED -> UNFUNDED_EXPIRED
QUOTE_ACCEPTED -> FUNDED -> EXECUTING -> RESULT_READY
  -> SETTLEMENT_REQUESTING -> SETTLEMENT_PENDING -> RELEASED
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
```

That projection is a read model, not an additional ledger. Objective software-
work V1 does not add an ACP-style on-chain `Submitted` escrow state. Its
`RESULT_READY` projection means only that the canonical Receipt and query-
independent semantic release template/digest have been constructed.
`SETTLEMENT_REQUESTING` records or resolves the one idempotent semantic release
action and its query-specific signed intent attempt. Only a finalized resolver proving
the escrow is `release_pending` creates `SETTLEMENT_PENDING`, V1's closest
analogue to ACP `Submitted`; the Receipt remains evidence, and only finalized
escrow and wallet state establish release, refund, and revenue.

Once a release action is recorded or broadcast, the refund clock alone cannot
authorize a different economic action. The exact release must first resolve as
not accepted, including an authenticated initial bounce where applicable, and
finalized escrow must again be `funded` at or after the refund boundary.
Otherwise recovery remains
`AMBIGUOUS(origin=SETTLEMENT_REQUESTING, SAME_ACTION_ONLY)`. An authenticated
initial bounce of a refund request leaves only that same semantic refund action.
Honest tooling may propose a new lower-level query/attempt, but escrow V1 does
not retain consumed queries: any public old attempt may win a permissionless
replay race. The resolver groups all old/new queries under the semantic action;
automatic paid-demand policy does not retry after bounce.

### 3.2 Evaluation and safe extension boundary

V1 has no general Evaluator role. It accepts only the frozen objective
validator/evidence and successful-release/full-timeout-refund profile. A
subjective model, buyer acknowledgement, market badge, or third-party opinion
cannot call release merely by being labelled an evaluator.

A future Evaluator-enabled successor must freeze an `EvaluationPolicyProfile`
before either party accepts. That profile must bind at least:

- Evaluator Agent, Capability/version/manifest, signer or immutable verifier
  contract code hash, and whether the buyer is also the Evaluator;
- objective versus subjective decision class, evidence schema, evidence digest
  and availability/retention commitment;
- decision encoding and reason commitment, evaluation deadline, and complete
  fee tuple: exact asset, source, recipient, deduction time, maximum amount, and
  funds-conservation rule;
- one static Evaluator key, a precommitted M-of-N quorum, or an objective
  precommitted rotation set/schedule; conflict rules; and no post-acceptance
  administrator replacement;
- timeout fallback that anyone may trigger when the Evaluator is unavailable,
  challenge/appeal policy, and the exact terminal transitions each one-shot
  decision may authorize; and
- domain-separated bindings to network, Quote, escrow, task, result, profile
  version, and replay identity.

An Evaluator is an explicitly trusted oracle for any fact not proven by the
committed verifier. A signature proves who decided, not that a subjective
deliverable is correct. High-value subjective profiles therefore require a
separately reviewed quorum, stake or other accountability model, challenge
path, and liveness analysis. They are outside V1.

ACP-style extensibility is adopted only as frozen typed profiles, not as an
arbitrary application callback. Any future commercial extension must be
versioned, reconstructible, and committed in the Accepted Quote. Where it
invokes executable contract logic, it must bind the exact contract address,
immutable code hash, configuration, proxy/upgrade status, and every settlement-
critical external dependency before acceptance. Its permissions, states,
assets, fee flows and conservation, external calls, gas/resource bounds, and
failure behavior must be enumerated. It must be one-shot where it decides a
terminal outcome, must not be upgradeable for an accepted purchase, reach
escrow funds outside its declared transition, change economic terms, or block
the permissionless bounded timeout-refund escape path. A platform administrator
or central Hook allowlist is not transaction authority; participants may apply
stricter local trust policies without changing protocol validity.

## 4. Typed handoff objects

### 4.1 `BuyerHandoffProfile`

Every active Demand Mutation contains the complete buyer-to-rail context needed
before a Provider signs:

- buyer Agent identity and signed Demand authorization context;
- the exact buyer wallet already represented by the existing typed escrow terms;
- Agent generation, controller-policy/delegation digest, proof profile, portable
  issuance-authority reference, and validity bounds for the Demand;
- the dedicated upload proof-of-possession key/profile and validity bounds; and
- the accepted existing Quote, escrow, task, and private-input profile versions.

The signed Demand Mutation authenticates this profile. V1 does not add a
post-Offer `accepted-work.accept` Agent signature. Buyer commercial acceptance
is the versioned escrow's on-chain `accept` transition authenticated to the
exact bound buyer wallet, and funding is the later exact stablecoin
notification. The wallet transaction authorization stays outside StateInit
identity. This removes a second buyer-controlled signature byte string from
Quote/StateInit identity and keeps a predeployment from consuming acceptance.

### 4.2 `PaidDemandQuoteBindingBodyV1`

The Provider constructs one unsigned canonical binding body from the exact
active Demand Mutation, its `BuyerHandoffProfile`, one preallocated durable
Offer identity, and Provider-selected execution terms. It fixes every semantic
fact that must remain identical through Offer authorization, Quote construction,
execution admission, and settlement recovery.

It includes at least:

- complete network domain and paid-demand Quote-binding profile version;
- the exact `BuyerHandoffProfile`;
- stable Demand identity, terminal-safe active Mutation sequence, and exact
  Mutation digest;
- Provider Offer identity and `max_acceptances = 1`;
- Provider Agent, Capability ID/version, and manifest digest;
- exact Provider `provider-offer.sign` key, delegation/mandate digests,
  validity bounds, proof profile, and portable authority-reference digest;
- task profile/version and operation descriptor;
- exact input digest, source digest, media type, and byte/file bounds;
- required output, validator, and evidence profiles;
- Provider-selected transport, private-input ingress, ingress-attestation key,
  and execution-signer commitments;
- exact TOS-network asset and Provider price in atomic units;
- exact positive `effective_max_completion_duration_seconds` and
  `max_preflight_to_start_delay_seconds`, plus exact positive
  `acceptance_to_funding_margin_seconds` and
  `funding_to_input_margin_seconds`, and
  `input_to_admission_margin_seconds`;
- `accept_by`, `funding_deadline`, `input_delivery_deadline`,
  `execution_admission_deadline`, `execution_deadline`,
  `refund_available_at`, and a strictly positive
  `release_pipeline_margin_seconds`; and
- equality commitments to every existing typed Quote/escrow preimage:
  network, Provider Agent, Capability/version/manifest, transport, Quote
  `expires_at`, asset/amount, buyer/Provider wallets, funding/refund deadlines,
  execution signer, and objective release/timeout-refund profile encoded by the
  existing dispute-policy cell; V1 has no dispute state.

Repeated values are equality constraints, never second authorities. Existing
Quote and escrow fields remain authoritative for their native meanings.
`accept_by` must equal the successor Quote's `expires_at` and the deterministic
escrow's acceptance cutoff; the bound-wallet `accept` operation rejects at or
after that time. For this successor version, `expires_at` is an acceptance-only
cutoff: it is checked only while the escrow is `pending_acceptance`. After the
authenticated `accept` transition finalizes `awaiting_funding`, the exact
stablecoin funding notification may be accepted in a transaction whose escrow
contract time satisfies `now <= funding_deadline`, even when that contract time
is later than `expires_at`; the transaction may be observed as finalized after
the cutoff. Resolver observation or finality wall time MUST NOT substitute for
the contract time, and the funding handler MUST NOT reapply the acceptance-only
cutoff. Funding while `pending_acceptance` remains invalid. Schema 1 retains its
frozen rule that an `awaiting_funding` notification satisfy both its
`funding_deadline` and Quote `expires_at` cutoffs.

#### Deadline safety and settlement slack

The body must leave enough time to start and finish the bounded execution and
have its release request accepted before the escrow refund boundary. Let:

```text
manifest_limit_seconds = ceil(manifest.limits.wall_clock_millis / 1000)

effective_max_completion_duration_seconds
  = min(exact signed Mutation maximum_completion_duration_seconds,
        manifest_limit_seconds)
```

That exact Mutation was active when the Offer and acceptance were authorized;
after acceptance, a later Mutation, withdrawal, or observed feed head has no
authority to tighten or relax this purchase. The execution profile freezes the
derivation and rounding. The body commits the exact result; the Gate recomputes
it from the transitively committed Mutation and manifest,
and the runner enforces it even when it is narrower than the manifest ceiling.
`max_preflight_to_start_delay_seconds` is the exact committed maximum queue/
handoff delay between one fresh Gate start preflight and first process start. It
is a receipt-validity bound, not an admission-to-start SLA: repeated refresh
while durably `prepared` may make total time since the original Gate claim
larger, while the fresh execution/refund deadline checks remain authoritative.
Checked arithmetic must prove a feasible schedule at admission:

```text
acceptance_to_funding_margin_seconds > 0
funding_to_input_margin_seconds > 0
input_to_admission_margin_seconds > 0
accept_by + acceptance_to_funding_margin_seconds
  <= funding_deadline
funding_deadline + funding_to_input_margin_seconds
  <= input_delivery_deadline
input_delivery_deadline + input_to_admission_margin_seconds
  <= execution_admission_deadline
execution_admission_deadline + max_preflight_to_start_delay_seconds
  + effective_max_completion_duration_seconds
  <= execution_deadline
execution_deadline + release_pipeline_margin_seconds
  < refund_available_at
```

The released profile freezes both pre-input pipeline bounds and their exact
step compositions. `acceptance_to_funding_margin_seconds` covers the worst-case
interval from a latest-valid `accept` handling transaction through finalized
acceptance observation, conforming buyer funding construction/broadcast, and
acceptance of the exact stablecoin notification by escrow.
`funding_to_input_margin_seconds` covers the worst-case interval from a latest-
valid funding handling transaction through finalized funded observation,
challenge issuance, bounded buyer upload, verification, and atomic durable
input acceptance. `input_to_admission_margin_seconds` covers record
verification, immutable-byte reopening/digest confirmation, current finalized
authority resolution, and atomic Gate claim publication after a latest-valid
input acceptance. A buyer that does not begin a conforming next step promptly
may still miss its deadline; these margins prove that the protocol path is
feasible, not that an inactive buyer is extended. If any complete bound is
absent, automatic paid-demand action remains blocked.

`input_delivery_deadline` applies to the ingress operation that durably accepts
and binds the exact bytes, not to a later Gate admission. Before consuming the
challenge, ingress obtains an `input_accept_time_upper_bound` under the same
Quote-bound conservative clock profile used by the Gate. One atomic durable
operation must consume the challenge, bind the immutable bytes, and commit a
signed `InputAcceptanceRecordV1` proving:

```text
input_accept_time_upper_bound <= input_delivery_deadline
```

The record binds the Quote, escrow, execution and upload action IDs, input and
source digests, challenge, exact ingress-attestation key/profile, clock-profile
digest and evidence/checkpoint, monotonic ingress journal sequence/head, and
accepted byte bounds. The challenge expiry cannot exceed
`input_delivery_deadline`. Equality is valid. Backdated clock evidence, a
checkpoint or journal high-water-mark regression, missing durable bytes, or an
unavailable bound is invalid and blocks admission. Once that record is valid,
the Gate may admit the same input after `input_delivery_deadline` provided its
separate `admission_time_upper_bound <= execution_admission_deadline` and slack
checks pass; it MUST NOT compare the later admission time to the delivery
deadline.

`release_pipeline_margin_seconds` covers the bounded post-run pipeline:
objective validation; evidence/report and Receipt construction; query-specific
intent signing; release broadcast/inclusion; and definitive downstream
acceptance of the initial escrow-to-wallet request without bounce. It is not
task-runner work time.

The released paid-demand execution/settlement profile freezes the worst-case
elapsed seconds and upper-bound composition for each step, network-time and
finality assumptions, plus its permitted margin range and conformance vectors;
the body commits the exact total, which may be larger than the profile minimum.
The Gate must use that committed value, never silently replace it with the
minimum.

Frozen escrow V1 clears `pending_query_id` when a wallet request bounces and
retains no consumed-query history or settlement generation. Any public old
release/refund message can then be permissionlessly replayed from `funded` and
race an honest new-query attempt. Thus no finite nonzero-bounce attempt budget
is a V1 contract invariant, and distinct query IDs do not repair the bound.
Before automatic paid-demand execution, the released profile must prove and
test a zero-bounce initial release path under the exact wallet code/state,
attached value, balance, fee, and network assumptions. If it cannot, the margin
proves only initial request inclusion, not payout priority, and automatic
paid-demand execution remains blocked. Any unexpected authenticated bounce
enters resolver/operator recovery; it never authorizes a blind automatic retry.
The same replay fact applies to timeout-refund attempts, although every valid
refund still pays only the committed buyer.

A priority-preserving escrow that records the valid pre-cutoff semantic release
action or a monotonic settlement generation/consumed-query set across bounces is
a different settlement-critical Quote/escrow successor. It requires its own
code identity, states, resolver, recovery analysis, vectors, and review; it
cannot be used to satisfy this V1 profile. Even with a proven zero-bounce path,
this profile does not promise the time of final provider-wallet credit: once a
downstream transfer is accepted and escrow remains `release_pending`, refund
stays blocked while the resolver waits for the terminal transaction chain.

The Native Execution Gate rechecks both the committed admission deadline and
the remaining worst-case slack when it admits a claim:

```text
admission_time_upper_bound
  + max_preflight_to_start_delay_seconds
  + effective_max_completion_duration_seconds
  + release_pipeline_margin_seconds
  < refund_available_at
```

Overflow, an unresolved profile, a missing/invalid/late
`InputAcceptanceRecordV1`, an expired admission deadline, or insufficient slack
rejects admission. A valid on-time input record remains valid for a later Gate
claim through the admission deadline. Immediately before first process start,
the runner must obtain a fresh preflight over the same Gate claim and verify:

```text
start_preflight_time_upper_bound
  + max_preflight_to_start_delay_seconds
  + effective_max_completion_duration_seconds
  <= execution_deadline

start_preflight_time_upper_bound
  + max_preflight_to_start_delay_seconds
  + effective_max_completion_duration_seconds
  + release_pipeline_margin_seconds
  < refund_available_at
```

That preflight and every safe refresh repeat the Gate's complete finalized
authority verification at coherent fresh monotonic checkpoints. Each attempt
first quorum-resolves a finalized network anchor within the released maximum
age and head-lag bounds, proves every escrow/Registry/Agent/Capability
observation at or through that anchor with required cross-shard order, and binds
the anchor/proof digest into the ticket. A monotonic old checkpoint is not
freshness. The checks include exact escrow and Registry code identities, funded
escrow state and Accepted Quote, provider Agent non-tombstone state, and
Capability ownership, exact unrevoked version, and manifest digest. It is not a
funding-only check. A post-admission escrow
transition, Agent tombstone, Capability transfer/revocation, code substitution,
checkpoint regression, fork conflict, or other authority divergence already
finalized in the preflight checkpoint set prevents first start. The fresh
preflight receipt is the linearization point for a bounded start-authority
ticket. It binds the checked `start_not_after` derived by adding the committed
preflight-to-start delay to the conservative preflight time upper bound, and
freezes exactly that verified snapshot only through that instant. A change
finalized after the checkpoint does not retroactively invalidate a start inside
the ticket; the original Gate claim freezes no authority.

The runner atomically binds the ticket on `prepared -> starting` and makes its
first runtime call only while the conservative process-start time upper bound
is no later than `start_not_after`. Otherwise the same claim is preflighted
again only while the runner is durably `prepared` and has proven that no runtime
side effect was possible; the refresh sees newer finalized revocation state.
After the atomic `prepared -> starting` transition, uncertainty is execution
ambiguity and is never refreshed or re-admitted as another execution.

A successful Receipt for this successor must record
`completed_at <= execution_deadline`. The versioned successor escrow must decode
the bound deadline and reject release when that condition fails; relying on the
Provider's Receipt builder alone would not enforce a buyer term. The escrow must
also accept the release request while `now < refund_available_at`; otherwise
only the committed timeout-refund path remains. Schema-1 escrow semantics remain
unchanged. This is deterministic liveness budgeting, not an Evaluator or
discretionary quality decision.

The contract comparison enforces the signed timestamp field, not wall-clock
truth by itself. The successor profile therefore treats the Quote-bound
execution signer as an explicit time attestor and binds its custody policy to
the same Gate claim, runner journal, conservative clock interval, and immutable
completion record. A signer that can authorize an arbitrary or backdated
`completed_at` is ineligible for automatic paid-demand execution.

The body fixes semantic fields but does not alone derive the final Quote or
StateInit. The complete canonical Provider Offer, including its one exact proof,
plus the existing typed rail preimages determine those bytes. Provider-private
writer generations and reservation/admission identifiers never appear in the
public body or proof.

### 4.3 `ProviderOfferV1` and Quote binding

The Provider authorizes the body once:

```text
paid_demand_binding_body_digest
  = H(body-domain || canonical PaidDemandQuoteBindingBodyV1)

provider_offer_authorization
  = canonical ProviderProofContext
      || Sign_provider(provider-domain || paid_demand_binding_body_digest
                       || H(canonical ProviderProofContext))

provider_offer_digest
  = H(offer-domain || canonical PaidDemandQuoteBindingBodyV1
      || canonical provider_offer_authorization)

PaidDemandQuoteBindingV1
  = PaidDemandQuoteBindingBodyV1
  + canonical provider_offer_authorization
```

`ProviderOfferV1` is the body plus that exact Provider proof.
`PaidDemandQuoteBindingV1` is the same exact-byte object carried by the
versioned existing Accepted Quote. It is a Quote extension payload, not separate
accepted state.

By signing, the Provider authorizes those exact bytes to be embedded and
disclosed in this deterministic Quote/StateInit. Because anyone holding the
Offer can predeploy `pending_acceptance`, selected or predeployed Offers may
become publicly observable before the buyer acts. This is not authorization to
index the Offer as general public discovery inventory; an unused losing Offer
remains direct/private unless separately disclosed under a publication profile.

The exact Provider proof bytes are part of one exact Provider Offer identity.
A different valid signature over the same body is a different, conflicting
Offer, not a second encoding of the same Offer. The buyer cannot substitute or
re-wrap the proof while preserving Offer identity.

The finalized buyer-wallet-authenticated `accept` transition on the
deterministic escrow carrying this exact binding is buyer commercial
acceptance. No additional buyer Agent signature is required or embedded. Exact
stablecoin funding remains a later existing-rail transition.

## 5. Construction and handoff sequence

The only valid fixed-price handoff sequence is:

1. Resolve and verify the exact active Demand Mutation, mutation history,
   `BuyerHandoffProfile`, authority references, expiry, and observed fork
   evidence under the discovery profile.
2. Preallocate one durable Provider Offer identity and construct the complete
   canonical `PaidDemandQuoteBindingBodyV1` without signatures.
3. Derive the stable body digest and semantic action ID.
4. Reserve owner-private portfolio exposure and obtain the exact runtime
   capacity lease for that body.
5. Pass Provider-wide custody admission, then create the Provider authorization
   and signed Provider Offer.
6. Deliver the exact signed Offer bytes through an ambiguity-resolving response
   transport.
7. The buyer verifies the exact Provider Offer and selects it locally. A
   Selection Notice is optional and non-authoritative.
8. The deterministic escrow StateInit embeds the versioned Accepted Quote,
   complete `PaidDemandQuoteBindingV1`, exact buyer wallet, and
   `pending_acceptance` state. Deployment creates no Accepted Quote authority
   and may safely occur before the buyer acts.
9. The exact bound buyer wallet sends the versioned `accept` operation. The
   contract authenticates the sender and transitions once from
   `pending_acceptance` to `awaiting_funding`; wrong senders cannot consume or
   disable that transition. Finality of this state transition is Quote
   acceptance.
10. The buyer funds that exact escrow through the existing asynchronous
   stablecoin transfer-notification path. A broadcast acknowledgement is not
   funding; the Provider waits for exact finalized funded state. The profile's
   acceptance-to-funding margin makes this ordered path feasible after a
   latest-valid acceptance.
11. Finalized resolution returns the existing Accepted Quote and escrow state
    plus the complete typed binding and Provider proof without a market
    database.
12. The existing Native Execution Gate verifies its normal Capability, Quote,
    escrow, signer, and replay invariants and additionally compares every
    paid-demand binding field.
13. The existing bounded executor, objective Receipt, release/refund, and
    settlement paths continue under their governing specifications.

No step may construct a second Quote or escrow identity from a different nonce,
wallet, proof wrapper, input, deadline, transport, or application journal field.
Retries reuse the same canonical bytes and stable semantic action identity.

## 6. Binding sufficiency matrix

| Fact | Pre-acceptance artifact | Existing-rail accepted authority | Enforcement |
|---|---|---|---|
| display summary, topics, hints, rank | Demand/index only | none | local presentation only |
| buyer Agent-to-wallet context and upload key | active Demand Mutation | exact body plus finalized versioned escrow `accept` transition authenticated to the bound wallet | authority resolver, escrow, ingress |
| Demand identity/sequence/digest | Demand Mutation | body provenance link, not a claim of a global feed head | resolver and Gate compare exact values |
| Quote acceptance for one Offer | exact Offer identity, body, and Provider proof | finalized `pending_acceptance -> awaiting_funding` transition authenticated to the bound buyer wallet | versioned escrow and resolver |
| execution funding eligibility | existing Quote | later exact finalized funded escrow state | existing resolver and Gate |
| Provider Offer identity and consent | Provider Offer | body Offer identity plus Provider proof | resolver, Gate, private admission journal |
| Provider Capability/version/manifest | Demand predicate and Offer | body plus existing Quote/Registry fields | existing finalized Registry checks |
| task profile and operation | Demand and Offer | body | spec-defined executor mapping |
| input/source commitments and bounds | Demand and Offer | body plus later signed provider-private `InputAcceptanceRecordV1` execution evidence | ingress and Gate; the record is not commercial authority |
| pre-input/execution/release-pipeline slack | Demand maximum, bound manifest, and Offer | exact pre-input margins, derived duration, preflight delay, and release-pipeline margin in body | resolver, ingress, Gate admission, fresh runner-start preflight, runner, and successor escrow deadline check |
| output, validator, evidence | Demand and Offer | body transitively committed by the existing Quote | validator; existing Receipt remains bound through Quote commitment and its existing fields |
| transport, ingress/attestation, execution signer | Offer | body | transport, ingress, Gate |
| asset, amount, deadlines, objective release/timeout refund | Demand and Offer | body plus existing Quote/escrow fields | custody, escrow, Gate, settlement |
| Provider consent and buyer commercial acceptance | Provider Offer plus signed Demand context | exact Provider proof plus finalized buyer-wallet-authenticated `accept` transition | resolver and Gate |
| Selection Notice | negotiation only | none | correlation only |
| skill internals, cost, margin, model rank | none | none | owner-private OpenFox policy |
| source coverage or moderation | index observation only | none | local discovery policy |

Existing rail fields are reused as follows:

| Semantic value | Existing authoritative preimage |
|---|---|
| network | Accepted Quote `network_domain` |
| Provider Agent, Capability/version, manifest | Quote identity/version cells |
| endpoint, transport security, request bound | typed Native transport binding |
| Offer acceptance cutoff | Quote version `expires_at`, equal to `accept_by` |
| funding cutoff after accepted transition | successor `funding_deadline`; the acceptance-only `expires_at` is not reapplied |
| asset and fixed Offer price | Quote economic asset and maximum amount; the fixed-price escrow requires that exact amount |
| buyer/Provider wallets and funding/refund deadlines | typed existing escrow terms |
| execution signer | Quote authority and escrow execution authorization |
| objective release/refund mode | existing Native objective dispute-policy cell |

The paid-demand successor reuses the existing custody rail and its funded,
release-pending, refund-pending, release, refund, and finalized-wallet recovery
semantics. It adds version-dispatched predicates: the
`pending_acceptance -> awaiting_funding` buyer-wallet transition; exact paid-
demand funding rule that rejects funding before acceptance and, after
acceptance, checks `funding_deadline` without reapplying `expires_at`; exact
paid-demand body/proof, deadline, duration, start-preflight, and slack checks at
the Gate; and the successor release-time execution-deadline predicate. Schema 1
remains byte-for-byte valid under its frozen acceptance, funding, and release
rules and is not reinterpreted for this paid-demand path.

The extension binds buyer Agent-to-wallet context, Demand/Mutation/Offer
provenance, Provider Offer proof, task/input/source and
output/validator/evidence commitments required before first claim, upload
proof-of-possession/ingress context, and the versioned deadline/slack fields.

No field may have two inconsistent authoritative sources. Every execution input
must trace to the finalized existing Quote and its reconstructible extension.

## 7. Per-Offer single acceptance and multi-Offer semantics

V1 Provider Offers are buyer-specific and single-use. One exact Demand Mutation,
buyer Agent/wallet, Provider terms, binding body, and exact Provider proof
determine one `PaidDemandQuoteBindingV1`, one existing Quote commitment, and one
existing escrow StateInit/address.

The existing rail has no cross-escrow atomic selection primitive. For the
versioned paid-demand successor, deterministic deployment creates only
`pending_acceptance`; the bound buyer wallet's finalized `accept` transition
creates Quote acceptance, and stablecoin funding arrives later through an
asynchronous transfer notification. This profile therefore does not claim that
one on-chain operation can select a demand-wide winner and fund the escrow
atomically.

After Quote acceptance but before funding, the Provider retains the obligation
and capacity through the funding deadline. The successor accepts the exact
notification in any handling transaction whose contract time satisfies
`now <= funding_deadline`, including after the acceptance-only `expires_at`;
later finality observation does not make a timely transaction late. It rejects
funding before the accepted transition and any handling transaction after the
funding deadline. If finalized resolution then proves that no exact funding
notification can still become authoritative, OpenFox may project
`unfunded_expired` and release capacity. No money was accepted, so this is not a
refund or a new escrow terminal state, and execution never begins.

`max_acceptances = 1` means one exact Provider Offer can derive only one Quote
commitment and one escrow address. Exact retry resolves that same identity; a
buyer-selected nonce, wallet, proof wrapper, or other variant cannot create a
second purchase from the Offer.

Different Provider Offers for the same Demand remain independent commercial
offers. If a buyer finalizes and funds more than one, every exact funded Quote
is independently valid and every Provider may perform the work. The buyer's
custody policy and local journal may enforce an owner preference such as
"accept one Provider", but that preference is not global authority and cannot
invalidate another finalized funded Quote.

A future auction or exclusive-work profile may add a dedicated coordinator
contract with a demand-wide compare-and-set. That is a separate protocol and
contract change, not part of this minimal binding extension. Until then, user
interfaces must say `selected locally` or `accepted and funded`; they must not
claim `unique global winner`.

## 8. Provider-private reservation and admission

Before Provider authorization, OpenFox atomically reserves local portfolio
exposure and obtains a runtime lease bound to Provider scope, stable action ID,
Offer identity, body digest, Demand/Mutation, resources, exact-asset exposure,
expiry, and `max_acceptances = 1`.

One local reservation is insufficient when several OpenFox instances, signer
keys, mandates, or runtimes share a Provider identity. Every production
`provider-offer.sign` path therefore passes through one Provider-private
admission authority, normally inside purpose-limited custody. It maintains:

- an exclusive writer lease with Provider scope, instance identity, expiry,
  and monotonically increasing fencing generation;
- a rollback-resistant generation high-water mark and authorization issuance
  ledger in one linearizable persistence domain;
- every signed/unexpired Offer and accepted/unsettled obligation;
- aggregate exact-asset exposure and runtime capacity;
- one unresolved Offer constraint for each `(provider scope, demand identity,
  active Mutation digest)` tuple; and
- stable semantic action IDs, canonical request digests, signatures,
  dispositions, and deterministic Quote/escrow resolution results.

Lease acquire, renewal, and takeover use compare-and-swap. Takeover increments
the fencing generation before a new writer may sign. Custody atomically rejects
an expired or stale generation, conflicting body/action, missing runtime lease,
unresolved tuple conflict, or aggregate policy violation. It commits the
high-water mark, admission result, signature result, and exposure before
returning signature bytes. Exact retry returns the recorded result. Writer
generation and retry attempt are private audit fields and never alter public
canonical bytes.

A replacement writer inherits unresolved Offers and obligations. A partitioned
old writer cannot sign with its stale generation. Even a single-process
deployment holds an operating-system lock on the canonical private state
directory for the daemon lifetime and still uses custody-side fencing.

After restore or migration, custody must prove that its generation high-water
mark and complete issuance ledger are at least as recent as every authorization
it emitted. If it cannot, it disables affected Offer keys and mandates. Recovery
requires finalized revocation or rotation, reservation of the old mandate's
maximum possible exposure/capacity, and resolution of every known on-chain
obligation. Because no global Offer source exists and an unknown deterministic
escrow address cannot be scanned, external observations cannot prove the
escaped-Offer set complete. Fresh signing remains blocked until all protocol-
and mandate-bounded Offer-acceptance, funding, obligation, and refund
windows have elapsed after finalized revocation and all known Quotes/escrows are
resolved. A copied subset, a claimed exhaustive index, or an incremented stale
counter is insufficient.

This ledger prevents Provider overcommitment. It is not a public market
database, transaction authority, or settlement authority.

## 9. Private input delivery

V1 uses buyer push to a Provider-selected, Offer-bound ingress. A Provider never
fetches a URL, host, repository, object store, or credential selected by remote
Demand text, buyer messages, model output, or task content.

The active Demand Mutation binds the buyer upload proof-of-possession key and
profile in `BuyerHandoffProfile`. The Offer and body copy that exact value;
the finalized extension also binds the Provider-selected ingress, TLS identity,
ingress-attestation key, and conservative clock profile. The upload key and
ingress-attestation key have no wallet, Agent-control, or market-signing power.

Only after the existing Quote and escrow are finalized and exactly funded:

1. the Provider issues a short-lived single-task challenge outside model/task
   content, bound to Quote, escrow, execution ID, input/source digests, bounds,
   expiry no later than `input_delivery_deadline`, stable upload action ID, and
   buyer upload key;
2. the buyer signs the canonical request/body digest and pushes the committed
   bytes to the bound ingress;
3. ingress authenticates Quote, escrow, proof of possession, Provider/TLS
   identity, challenge scope, expiry, operation, and body; bearer-only access is
   insufficient;
4. ingress checks ciphertext/plaintext digest as applicable, media type,
   compressed and decompressed sizes, file count, canonical paths, and archive
   rules;
5. under the bound conservative clock profile, one atomic durable operation
   consumes the challenge, binds the accepted immutable bytes to the existing
   Gate claim fields, and commits the signed `InputAcceptanceRecordV1` with
   `input_accept_time_upper_bound <= input_delivery_deadline`; and
6. the ingress maps the immutable bytes and exact acceptance-record digest into
   an existing task-admitting transport and the shared Native Execution Gate
   before the bounded executor. It creates no pre-Gate execution slot.

Exact retry returns the same delivery receipt. Conflicting bytes, proof,
identity, or concurrent claimant fail without replacement. Ambiguous delivery
uses a bounded status query before retry. Credentials and private source never
enter public artifacts, Opportunity Magnets, model context, Receipt, logs, or
evidence. Redirects, arbitrary DNS, proxies, credential forwarding, buyer-
selected egress, and pull fallback are forbidden.

Ingress storage is owner-private but not an unverified timestamp oracle. The
Gate verifies the record signature, bound clock evidence/checkpoint, monotonic
journal high-water mark, exact immutable-byte availability and digest, and the
deadline comparison. A storage restore or local wall-clock rollback blocks all
affected admissions until reconciliation proves the retained record and high-
water marks. Admission after the delivery deadline is legal only for a record
that already proves timely atomic acceptance; a newly backdated receipt is not
recovery.

## 10. Existing Gate, Receipt, and recovery integration

The Native Execution Gate retains its existing authority, five schema-1 core
claim fields, and at-most-once record keyed by `(Quote commitment, escrow
address)`. Quote-version dispatch adds the exact
`input_acceptance_record_digest` to the paid-demand claim and every admitting
transport while leaving that shared slot key unchanged. Exact replay is
idempotent; an omitted or different record digest conflicts. The versioned
paid-demand profile also adds field-by-field checks over the signed Demand
Mutation, Provider Offer proof, authority bounds, acceptance-time revocation
ordering, the exact buyer-wallet-authenticated escrow `accept` transition,
task/input/source, validation/evidence, transport, signer, amount, and
deadlines. The Gate may record execution identity on first claim; it cannot
choose a missing expected value or create a second admission slot. It
additionally verifies the exact
`InputAcceptanceRecordV1` and immutable accepted bytes: the record's conservative
accept-time upper bound, clock evidence, ingress signature, journal high-water
mark, and every identity/digest must match the binding and prove delivery no
later than `input_delivery_deadline`. A later Gate claim is compared separately
to `execution_admission_deadline`.

The existing software-work Receipt remains the objective result and release
input. Its existing Quote commitment transitively binds the versioned paid-
demand payload, and its current schema already binds input/source and objective
result fields. This profile does not require a second Receipt field unless a
separate concrete binding-sufficiency review proves one is missing.

After Quote finality, public-feed state is irrelevant to recovery. Existing
safe handoff and finalized escrow/wallet resolution must reconstruct the Quote,
typed extension, signed Demand context, Provider proof, Receipt,
release/refund, and settlement
without a Gateway, Messenger database, market index, OpenFox journal, or
Provider-private admission ledger.

## 11. Repository ownership

| Repository or component | Extension responsibility |
|---|---|
| `tos-service-spec` | paid-demand Quote-binding fields, proof contexts, private-input profile, mappings into existing rail schemas, vectors, and invariants |
| `tos-service-protocol` | canonical construction/verification, deterministic handoff into the existing Quote builder, finalized resolver output, Gate comparisons, reuse of the existing Receipt binding, and safe-handoff helpers |
| `tos` | versioned existing Accepted Quote/escrow representation; no market database or new selection coordinator in this profile |
| `openfox` | body proposal, private reservations, custody admission client, Offer orchestration, and recovery; no custody or settlement authority |
| `tos-ai` | Offer-bound capacity lease, private ingress profile, existing bounded execution, validation, evidence, and artifacts |
| custody tools | Provider-wide writer fencing, aggregate admission, exact semantic confirmation, purpose-limited signing, and rollback-safe issuance history |
| `tos-messenger` and Gateways | exact-byte Offer/selection transport only; no accepted-state authority |

No repository may implement an application-private paid-demand transaction
and later present it as the canonical TOS Service rail.

## 12. Conformance and adversarial tests

The extension requires frozen positive vectors and mutations for:

- complete body, signed Demand context, and Provider proof context/signature;
- acyclic digest and deterministic existing Quote/StateInit reproduction in two
  independent implementations;
- wrong Demand, Mutation, Offer, Agent, buyer wallet, `accept` sender,
  Capability, input/source, task,
  validator/evidence, transport, signer, asset/amount, or deadline;
- invalid deadline ordering, zero/below-profile/substituted acceptance-to-
  funding, funding-to-input, input-to-admission, or release-pipeline margin;
  effective-duration mismatch or round-down, arithmetic overflow,
  exact-boundary Gate rejection, insufficient remaining slack, queue/restart
  delay while `prepared`, fresh same-claim preflight, atomic
  `prepared -> starting`, crash ambiguity after that boundary, clock-skew
  rejection, escrow/Agent/Capability/code or finalized-checkpoint change
  between admission and preflight; an adverse change finalized at/before the
  final preflight checkpoint versus only after that checkpoint; start inside
  and after the bounded `start_not_after` ticket; monotonic-but-stale finality
  anchor, excess anchor age/head lag, endpoint disagreement, or missing cross-
  shard proof; late Receipt/release; and understated validation, wallet-request,
  zero-bounce/replay-resolution, attached-value, or fee bounds; arbitrary or
  backdated completion time and a signer detached from the Gate/runner record;
- missing, detached, wrong-body, wrong-scope, expired, or revoked proofs;
- later Demand successor or withdrawal, including a lower/higher duration,
  attempting to deny or relax the exact already accepted Mutation binding;
- alternate otherwise authorized key, threshold subset, proof path/wrapper,
  portable authority reference, or non-canonical signature;
- buyer context or upload key differing from the active Mutation;
- public bytes containing Provider-private fencing or reservation data;
- opaque digest without reconstructible typed body and Provider proof;
- two Quotes/escrows from one Offer and any buyer-controlled construction
  variance;
- third-party predeployment followed by successful bound-wallet acceptance;
  rejection of a wrong-sender `accept`, duplicate/conflicting `accept`, funding
  before acceptance, and acceptance at or after its deadline; successful
  successor funding at `accept_by + 1` after an earlier accepted transition and
  at `funding_deadline`, plus rejection at `funding_deadline + 1`; schema-1
  vectors continue to enforce both its Quote-expiry and funding-deadline
  cutoffs; delayed acceptance and funding finality at every committed pre-input
  pipeline boundary, and rejection when either complete pipeline bound is too
  small or unavailable;
- deterministic one-Offer/one-Quote reproduction; independent acceptance of two
  different Provider Offers; and rejection of a second Quote identity derived
  from one Offer;
- Provider writer takeover, stale generation, aggregate exposure overflow,
  storage rollback, incomplete restore, and escaped-signature recovery;
- private-input bearer theft, wrong proof key, concurrent overwrite, exact
  retry, conflicting body, ambiguous acknowledgement, and status recovery; and
  input acceptance exactly at `input_delivery_deadline`, rejection one second
  after it, on-time durable input admitted later but no later than
  `execution_admission_deadline`, including the full committed input-to-
  admission margin; backdated or rolled-back clock/journal evidence, wrong
  ingress-attestation key, missing accepted bytes, and use of Gate admission/
  observation time as the input-delivery timestamp;
- Gate field substitution and cross-transport replay; and
- evaluator, fee, extension-profile, contract-address, or code-hash
  substitution; fee-asset/source/recipient/conservation mismatch; administrator
  signer replacement; mutable proxy/configuration/dependency closure; arbitrary
  callback injection; post-acceptance upgrade; repeated decision; and any
  extension attempt to block or redirect the committed timeout refund; and
- authenticated release/refund bounce followed by permissionless replay of an
  old signed/query-specific attempt, concurrent old/new query races, repeated
  replay/fee consumption, resolver grouping under one semantic action, and
  rejection of an automatic profile without a proven zero-bounce initial
  release path; and
- restart before and after reservation, Offer delivery, predeployment, the
  buyer-wallet `accept` transition, Quote finality, reservation conversion,
  input admission, Gate claim, Receipt, and settlement.

Existing rail conformance tests remain mandatory and must pass unchanged except
where an explicitly versioned vector is added. Passing the paid-demand extension
tests cannot waive any existing Quote, escrow, Gate, execution, Receipt, refund,
safe-handoff, or settlement invariant.

## 13. Acceptance criteria

The paid-demand binding is accepted only when:

1. the existing commercial rail is identified by exact released versions and
   its current conformance suite remains green;
2. two independent implementations reproduce every extension digest, Provider
   proof, existing Quote commitment, and escrow StateInit;
3. the selected body, signed Demand context, and Provider proof are
   reconstructible from finalized state without market infrastructure;
4. one Offer cannot yield two Quotes or escrows, while separately accepted and
   funded Provider Offers remain independently valid under the existing rail;
5. third-party predeployment cannot create acceptance or block the exact bound
   buyer wallet from completing the one canonical `accept` transition; after
   that transition, successor funding uses contract time
   `now <= funding_deadline` without reapplying `expires_at`, while pre-
   acceptance or late-contract-time funding is rejected, finality observation
   time is ignored for the deadline, and schema-1 funding semantics remain
   unchanged;
6. Provider-private fencing prevents stale or partitioned writers and aggregate
   overcommitment without entering public canonical bytes;
7. private input reaches only the bound proof-of-possession ingress after exact
   finalized funding, and one signed monotonic `InputAcceptanceRecordV1` proves
   atomic durable acceptance under the bound conservative clock profile no
   later than `input_delivery_deadline` without preventing a separately timely
   later Gate admission;
8. the existing Gate rejects every extension-field substitution and executes
   each exact funded Quote at most once, only while its committed admission
   deadline/start delay, effective duration, and release-pipeline slack fit
   strictly before the refund boundary; the committed acceptance-to-funding,
   funding-to-input, and input-to-admission margins prove a complete feasible
   pre-execution pipeline; and every first-start preflight uses a current-quorum
   finality anchor within frozen age/head-lag bounds rather than a merely
   monotonic old checkpoint;
9. the successor escrow rejects release when the bound Receipt completion time
   exceeds `execution_deadline`, while the existing Receipt/release/refund and
   finalized provider-credit paths remain authoritative; and
10. crash recovery at every handoff boundary creates no duplicate commercial
    action.

Until these criteria are met, discovery and local simulation may proceed, but
paid-demand-sourced Provider Offer acceptance and automatic execution remain
disabled. The existing Capability-first commercial rail is unaffected.
Passing this binding profile is necessary but not sufficient for commercial
use: the complete D2 gate in
[`AGENT_PAID_DEMAND_DISCOVERY_V1.md`](AGENT_PAID_DEMAND_DISCOVERY_V1.md)
must also pass.

## 14. Explicit non-goals

This profile does not create:

- a second Quote, escrow, Execution Gate, Receipt, ledger, or settlement state
  machine;
- an application database that can declare accepted work or payment;
- a globally authoritative market head, index, or order book;
- a globally unique Provider winner or atomic cross-escrow selection contract;
- a built-in subjective Evaluator, platform-selected arbiter, mandatory market
  commission, or administrator-controlled fee schedule;
- an arbitrary or upgradeable Hook that can alter an accepted purchase or
  block its timeout-refund path;
- natural-language authority for work, signatures, execution, or payment;
- public storage of private task input or Provider-private admission state;
- a replacement for existing Capability, custody, objective refund, or safe-
  handoff rules; or
- proof that a task is profitable, lawful, safe, or successfully completed
  merely because its Offer or Quote is valid.

## 15. Open schema decisions

Before implementation, the specification PR must freeze:

1. the exact `PaidDemandQuoteBindingBodyV1` and Provider proof protobuf fields,
   bounds, canonical ordering, digest domains, and positive/negative vectors;
2. the Accepted Quote successor or generic typed-extension mechanism, including
   unknown-version and trailing-data behavior while schema 1 remains unchanged;
3. the corresponding escrow StateInit/code identity, deterministic address
   derivation for one exact Provider Offer, initial `pending_acceptance` state,
   buyer-wallet-authenticated `accept` message and transition, wrong-sender and
   duplicate behavior, acceptance deadline, predeployment recovery, funding
   rejection before acceptance, and version-dispatched post-acceptance funding
   predicate through `funding_deadline` without reapplying `expires_at`, plus
   release-time enforcement of the bound `execution_deadline` while schema 1
   retains its frozen dual-cutoff funding and release rules;
4. resolver, safe-handoff, and Native Execution Gate immutable version-dispatch
   tuple from network/Quote schema/binding profile to exact Quote parser, escrow
   parser/code hash, Gate claim-extension parser/predicate set, and field-by-
   field comparison rules, with no retry/preflight redispatch;
5. historical Provider delegation proof, current eligibility, revocation/
   expiry ordering at Quote acceptance, and canonical proof representation;
6. the buyer-push challenge, proof-of-possession, encryption, retention, status,
   ingress-attestation key, atomic `InputAcceptanceRecordV1`, conservative
   clock evidence, rollback-resistant journal high-water mark, and existing
   Gate-claim mapping;
7. the complete deadline fields and strict checked ordering, effective-duration
   derivation/enforcement, maximum preflight-to-start delay and fresh preflight,
   conservative network-time upper-bound rule including the distinct input-
   acceptance and Gate-admission comparisons, exact nonzero acceptance-to-
   funding, funding-to-input, input-to-admission, and release-pipeline margins
   with complete step bounds, zero-bounce initial-wallet-request proof,
   permissionless old-query replay/resolver rule, exact wallet/attached-value/
   fee assumptions, finalized
   anchor max-age/max-head-lag and current-quorum/cross-shard proof rules,
   bounded start-ticket linearization, execution-signer time-attestation custody
   rule, and boundary vectors; and
8. the Provider-private fencing/admission interface and rollback-safe recovery
   evidence required before custody can release a signature.

None of these decisions may introduce a second settlement lifecycle or claim
demand-wide exclusivity without a separately specified coordinator contract.
