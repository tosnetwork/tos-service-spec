<!-- markdownlint-disable MD013 -->

# Decentralized Agent Guarantor Service V1

**Status:** pre-freeze application-profile design. No implementation may
advertise conformance until the schemas, exact-byte vectors, independent
reference verifier, production codec, authority integration, and applicable
Adapter tests defined by this document have been released.
This is an incubation design under the `ROADMAP.md` expansion gate: it neither
opens nor reorders Gates D--G and is not acceptance evidence for the first
software-work commercial lifecycle or the root Agentic Internet operation gate.

**Profile URI:** `tos.agent-service.guarantor.v1`

**Issue:** [tos-service-spec #56](https://github.com/tosnetwork/tos-service-spec/issues/56)

**Implementation evidence:**
[Agent Guarantor V1 implementation report](AGENT_GUARANTOR_SERVICE_V1_IMPLEMENTATION_REPORT.md).
The report is non-normative and does not change the pre-freeze status or open
an assurance tuple by itself.

**Composes:**
[Agent Intent Exchange V1](AGENT_INTENT_EXCHANGE_V1.md),
[Semantic Action Identity V1](SEMANTIC_ACTION_IDENTITY_V1.md),
[OpenFox Autonomous Earning Implementation Plan](OPENFOX_AUTONOMOUS_EARNING_IMPLEMENTATION_PLAN.md),
[Agent Operation and Outcome Event V1](AGENT_OPERATION_OUTCOME_EVENT_V1.md),
and the settlement Adapter selected by each value-bearing obligation. Outcome
events can preserve offer, activation, claim, decision, payout and failure
evidence; they cannot create coverage or enlarge the guarantor's liability.

**Proposed media types:**

| Object | Media type |
| --- | --- |
| service profile | `application/vnd.tos.service.agent-guarantor-service-profile.v1+cbor` |
| quote request | `application/vnd.tos.service.agent-guarantor-quote-request.v1+cbor` |
| firm coverage offer | `application/vnd.tos.service.agent-guarantor-firm-offer.v1+cbor` |
| firm-offer Agreement evidence | `application/vnd.tos.service.agent-guarantor-firm-offer-agreement-evidence.v1+cbor` |
| Provider exposure admission receipt | `application/vnd.tos.service.agent-guarantor-exposure-receipt.v1+cbor` |
| offer non-acceptance evidence | `application/vnd.tos.service.agent-guarantor-offer-non-acceptance.v1+cbor` |
| pre-acceptance exposure release receipt | `application/vnd.tos.service.agent-guarantor-pre-acceptance-release-receipt.v1+cbor` |
| coverage acceptance request | `application/vnd.tos.service.agent-guarantor-acceptance-request.v1+cbor` |
| coverage acceptance receipt | `application/vnd.tos.service.agent-guarantor-acceptance-receipt.v1+cbor` |
| coverage activation evidence | `application/vnd.tos.service.agent-guarantor-activation-evidence.v1+cbor` |
| coverage non-activation evidence | `application/vnd.tos.service.agent-guarantor-non-activation-evidence.v1+cbor` |
| coverage cancellation request | `application/vnd.tos.service.agent-guarantor-cancellation-request.v1+cbor` |
| coverage cancellation receipt | `application/vnd.tos.service.agent-guarantor-cancellation-receipt.v1+cbor` |
| collateral control evidence | `application/vnd.tos.service.agent-guarantor-collateral-control-evidence.v1+cbor` |
| collateral evidence | `application/vnd.tos.service.agent-guarantor-collateral-evidence.v1+cbor` |
| claim | `application/vnd.tos.service.agent-guarantor-claim.v1+cbor` |
| claim-submission ingress action | `application/vnd.tos.service.agent-guarantor-claim-ingress-action.v1+cbor` |
| claim-submission ingress receipt | `application/vnd.tos.service.agent-guarantor-claim-ingress-receipt.v1+cbor` |
| claim admission receipt | `application/vnd.tos.service.agent-guarantor-claim-admission.v1+cbor` |
| claim-filing close receipt | `application/vnd.tos.service.agent-guarantor-claim-filing-close.v1+cbor` |
| claim decision | `application/vnd.tos.service.agent-guarantor-claim-decision.v1+cbor` |
| claim-decision admission receipt | `application/vnd.tos.service.agent-guarantor-claim-decision-admission.v1+cbor` |
| claim-decision application receipt | `application/vnd.tos.service.agent-guarantor-decision-application.v1+cbor` |
| claim-state transition receipt | `application/vnd.tos.service.agent-guarantor-claim-state-transition.v1+cbor` |
| terminal claim-set evidence | `application/vnd.tos.service.agent-guarantor-terminal-claim-set.v1+cbor` |
| exposure release receipt | `application/vnd.tos.service.agent-guarantor-exposure-release-receipt.v1+cbor` |
| coverage resolution | `application/vnd.tos.service.agent-guarantor-resolution.v1+cbor` |
| generic commerce profile event | `application/vnd.tos.service.commerce-profile-event.v1+cbor` |

The keywords MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT,
RECOMMENDED, NOT RECOMMENDED, MAY, and OPTIONAL are interpreted as BCP 14.

## 1. Purpose

This document defines an optional, decentralized service profile through which
an Agent can assume a bounded contingent payment obligation for exact
obligations in another Agreement. It lets Agents discover Guarantors, request
and compare bounded quotes, authorize one exact coverage Agreement, prove any
required collateral, submit and decide claims, pay approved amounts exactly
once, and release remaining exposure after every relevant window and claim has
resolved.

The profile is a specialized composition over generic Agent operations. It is
not a new root operation, a global Guarantor registry, a canonical market head,
a solvency oracle, a claims court, or an industry-specific chain opcode.

The technical term `coverage` in this document means only the bounded
contingent obligation encoded and authorized by this profile. It does not, by
itself, establish legal insurance, surety, licensing, jurisdiction, consumer
protection, capital adequacy, or enforceability. Parties and implementations
remain responsible for applicable law and for accurately describing the
assurance their selected Adapter provides.

## 2. Empirical design input from the eight-Agent campaign (non-normative)

This section records the measured design input explicitly required for this
profile. It is not a history of superseded drafts. Conformance depends only on
the normative objects, rules, and gates in the remaining sections, not on the
campaign result.

This profile was proposed during the real-time, three-hour
[Eight-Agent Market Campaign](https://github.com/tosnetwork/openfox/blob/df75c91a72ddca4c3106cec0014c1baae4a464fe/docs/operations/eight-agent-market-campaign-report.md)
on 2026-08-25. Eight logically isolated OpenFox identities used two local
Intent Carrier processes and a local three-validator TOS network to discover,
authorize, execute, and settle generic work. The campaign is development
evidence, not evidence of public-network decentralization, independent
operator failure domains, external profit, or a deployed guarantee service.

The `guarantor-analyst` participant offered the advisory capability
`agreement-risk-analysis` through a subscription-backed AI runtime. It sold
three risk-analysis engagements at 350,000 nanoTOS each and produced one
reviewed, non-authoritative `Agreement risk` procedural skill. One declassified
engagement cited by Issue #56 has the following evidence:

| Field | Observed value |
| --- | --- |
| Capability | `agreement-risk-analysis` |
| Seller role | `guarantor-analyst` |
| Agreement digest | `sha256:65e5bd007b78da7c5cc67c7ce2f96ac7881f5d88367910c92264339b4a34acf0` |
| Execution outcome digest | `sha256:8730cc5f9f49163cbd1e9e4677c9dfefa85588b3730e6c446dd7f65c5d0ab51a` |
| Finalized payment transaction | `sha256:602a29e9f4a0ccfcf73a7b128eee185c0751b7a3e47243da0c8fce030ec0fe7e` |
| Payment | 350,000 nanoTOS |

The engagement demonstrated that an Agent can sell Agreement-risk analysis.
It did not transfer risk, issue coverage, prove guarantee capacity, lock
collateral, adjudicate a claim, or pay a covered loss. The analysis found that
the tested direct-postpaid Agreement lacked pre-funding, conditional custody,
objective acceptance, an adjudication forum, and independently verifiable
guarantee capacity. It recommended bounded collateralized guarantees or escrow
before unsecured execution.

That difference between advice and enforceable responsibility is the
motivating gap. An Agent seeking actual third-party coverage still needs an
interoperable way to discover a Guarantor, request and compare a bounded quote,
bind the promise to one exact Agreement and obligation set, verify any required
collateral, submit and decide claims, pay approved amounts exactly once, and
recover ambiguous outcomes. Without a common profile, implementations would
invent incompatible private messages or depend on a centralized Guarantor
database.

The campaign boundaries remain material:

- the eight identities were logical runtimes in one campaign process;
- the two Carrier processes shared one host and operator;
- the three validators were local test-network processes;
- all payments occurred inside a closed economy; and
- the learned risk skill was guidance and conveyed no authority, credential,
  capital, or spending permission.

The campaign therefore motivates this design but does not count as Guarantor
conformance or production acceptance.

### 2.1 Ten Issue #56 design commitments

The earlier cross-repository discussion is preserved here as ten normative
commitments rather than as a separate business-specific workflow:

1. publish Guarantor supply through ordinary signed Intents, never a privileged
   registry or market database;
2. bind every quote and coverage promise to exact parties, an underlying
   Agreement digest, and covered obligation IDs;
3. reserve the full worst-case Provider exposure before signing a one-use firm
   offer;
4. make effective acceptance a linearized transition that cannot race expiry
   or exposure release;
5. distinguish unsecured promises, profile-qualified Adapter-attested
   collateral, and
   independently enforceable collateral without overstating any level;
6. admit typed, authenticated, replay-safe claims through an Agreement-selected
   authority and immutable evidence manifest;
7. bind each decision to the selected authority, quorum, evidence, policy,
   revision, challenge, and fallback profile;
8. materialize finite payout obligations and apply payout, cancellation,
   collateral release, and recovery with stable semantic action identities;
9. place canonical objects and verification in the specification and protocol,
   autonomy and private exposure in OpenFox, generic transport in Messenger,
   discovery in existing Carriers, and only optional application collateral in
   TOS; and
10. block conformance claims until independent codecs, exact vectors, crash and
    race tests, source-loss recovery, Adapter evidence, and pinned acceptance
    artifacts pass.

## 3. First-principles model

A Guarantor service is:

> a third party's canonical, bounded, condition-triggered obligation to pay a
> named beneficiary for a selected failure or loss associated with exact
> obligations in an already identified underlying Agreement.

It is not merely an opinion about risk. It is also not identical to escrow.
Escrow holds assets for an already specified transfer lifecycle. A Guarantor
assumes contingent liability that may be unsecured, supported by attested
collateral, or independently enforceable through a selected Adapter.

The protocol separates these facts:

1. a signed supply Intent proves what the Provider advertised, not solvency;
2. a quote request asks for terms but authorizes no coverage or payment;
3. a firm offer is a bounded commercial commitment backed by a Provider-private
   exposure reservation, but it does not prove collateral or activate coverage;
4. the coverage Agreement records exact terms and body-bound authorizers;
5. linearized acceptance decides whether a firm offer was consumed before its
   cutoff;
6. activation requires every selected premium, collateral, and underlying-
   Agreement prerequisite;
7. a claim is an assertion, not a decision;
8. a profile-qualified decision authorizes a bounded payout schedule, not the
   transfer itself;
9. settlement terminal evidence proves an exact payout; and
10. collateral release requires terminal coverage, claim, payout, and Adapter
    evidence rather than Provider silence or local time alone.

## 4. Roles

| Role | Responsibility | Not implied by the role |
| --- | --- | --- |
| Risk Analyst | estimates or explains risk | coverage, collateral, decision, or payout authority |
| Guarantor | assumes the bounded contingent payout obligation | solvency or independent enforcement |
| Covered Party | obtains coverage and commonly pays the fee | automatic beneficiary or claimant authority |
| Beneficiary | receives an approved payout | authority to decide its own claim |
| Claimant | submits a typed claim and evidence | proof that the claim is valid |
| Decision Authority | applies the Agreement-selected claim profile | objective truth beyond that profile |
| Collateral Principal | owns or controls assets to be locked | authority to release them outside accepted terms |
| Collateral Custodian or Adapter | proves and applies lock, payout, and release transitions | authority to reinterpret claim evidence |
| Settlement Adapter | proves the terminal transfer outcome it specifies | claim validity or general solvency |

One Agent MAY hold several roles only when each role, subject, scope, and
evidence profile is separately bound. A service name, Carrier record, model
output, reputation score, or conversation transcript never assigns a role.

A Guarantor whose Agent identity is also an obligor of any covered obligation
in the underlying Agreement is not a third party and MUST NOT issue a conforming
Guarantor V1 offer for that obligation. It may describe a self-guarantee through
an ordinary generic Agreement, but cannot label it with this service profile or
any of its three assurance levels. The Guarantor service's `provider_agent_id`
normally is the Guarantor and is not the comparison target. Reinsurance or a
downstream guarantee is a separate Agreement and does not weaken the primary
Guarantor's obligation unless the beneficiary authorizes a new Agreement
version.

This is a deterministic rejection rule, not a missing classification field.
Before quote authorization, offer issuance, Agreement authorization, and
activation, the verifier resolves the complete underlying
`AgentAgreementBodyV1`, resolves every `covered_obligation_id`, derives each
obligor's canonical Agent ID from that body, and requires that set not to contain
`guarantor_agent_id`. A missing Agreement, missing obligation, non-Agent obligor
without a released subject-to-Agent resolver, unresolved alias, or equality at
any covered obligation fails closed. No caller-provided `third_party` or
`self_guaranteed` token can override this derivation.

## 5. Goals, non-goals, and invariants

### 5.1 Goals

The V1 profile provides:

- permissionless publication and multi-Carrier discovery;
- bounded, targeted, non-transferable firm offers;
- exact linkage to one underlying Agreement and obligation set;
- body-bound mixed authorization profiles;
- reserve-before-offer aggregate exposure control;
- explicit unsecured, attested-collateral, and independently enforceable
  assurance;
- typed claim submission and decision authority;
- finite, deterministic partial-payout materialization;
- query-before-retry recovery for every external side effect;
- exact accounting for fees, exposure, collateral, claims, payouts, defaults,
  and release; and
- capability-based enablement without a global production-readiness flag.

### 5.2 Non-goals

V1 does not define or operate:

- a TOS-owned Guarantor;
- a global list of Guarantors, policies, coverage, claims, or solvency;
- a canonical ranking, reputation, capacity, or price feed;
- legal or regulatory status;
- a universal loss ontology or industry-specific workflow;
- an AI claims judge with implicit authority;
- mandatory collateral or mandatory on-chain settlement;
- cross-asset collateral valuation or an implicit price oracle;
- automatic discovery of undisclosed coverage held with other Guarantors;
- automatic sponsorship failover after a payout may have been attempted; or
- a new consensus rule, VM-wide opcode, or transaction type.

### 5.3 Safety invariants

1. Critical authority, amount, asset, party, time, evidence, destination, and
   Adapter facts are canonical fields, not prose.
2. The full worst-case offer exposure is reserved before a firm offer is
   signed.
3. A firm offer is targeted, has `max_acceptances = 1`, and is accepted only by
   one linearizable admission domain or an exact selected contract transition.
4. No acceptance, claim, decision, payout, or release is inferred from chat,
   HTTP status, Provider timeout, Carrier absence, or AI output.
5. Same stable action ID plus different exact request bytes is `conflict` and
   never overwrites the admitted record.
6. `unknown`, `submitted`, or `ambiguous` never means absent and never permits a
   new semantic payout or collateral release.
7. Every payout is bound to the coverage Agreement, coverage obligation,
   claim, terminal decision, payout sequence, amount, asset, payer, beneficiary,
   destination, and Adapter.
8. Cumulative approved and paid amounts never exceed the accepted aggregate
   cap; arithmetic is checked and never floating point.
9. An open or ambiguous claim, decision, payout, challenge, or Adapter action
   blocks collateral and exposure release.
10. Carrier metadata, a self-issued exposure receipt, and historical balance
    evidence never prove solvency or current collateral.
11. An unaccepted reservation is released only through a fenced non-acceptance
    proof from the same admission domain; it never requires or fabricates a
    claim set.
12. `independently-enforceable` always has exclusive, same-asset, offline-
    executable beneficiary capacity for the full aggregate cap.
13. For an `independently-enforceable` tuple, removing the Guarantor's complete
    technical-control closure leaves coverage activation and non-activation,
    claim ingress, admission, revision, non-decision transitions, filing close,
    terminal decision, decision application, coverage cancellation, coverage
    closure, and payout quorums satisfiable through direct authenticated Adapter
    routes. Lower assurance
    levels make no such control-deletion claim and may use the bound Guarantor
    lifecycle authority exactly as disclosed by their selected profile.

## 6. End-to-end lifecycle

The normal lifecycle is:

```text
Guarantor publishes an ordinary signed OFFER/SERVICE Intent
  -> clients merge and verify results from configured Carriers
  -> local AI and deterministic owner policy evaluate the profile
  -> Covered Party sends a signed, targeted quote request
  -> parties negotiate exact machine terms
  -> compile and freeze the coverage Agreement body
  -> Provider authority atomically reserves worst-case exposure
  -> Guarantor signs a firm offer bound one-way to the Agreement body
  -> all other body-bound authorization predicates are satisfied
  -> Covered Party submits exact acceptance before accept_by
  -> Provider authority or selected contract atomically admits acceptance
  -> verify underlying Agreement, premium, and collateral prerequisites
  -> activate coverage
  -> accept typed claims during the accepted filing window
  -> atomically freeze the filing high-water at the cutoff
  -> selected Decision Authority authorizes each decision
  -> independent decision admission orders it in the claim log
  -> resolve any challenge and close against the admitted decision
  -> decision application deterministically materializes finite payout obligations
  -> pay and resolve each payout through its selected settlement Adapter
  -> authorize the terminal claim set and enter release_pending
  -> dispose of residual collateral using that exact terminal set
  -> release Provider exposure
  -> admit final coverage resolution and terminal state
  -> update evidence-bound accounting and learning
```

Settlement selection, evidence profiles, collateral requirements, and the
maximum exposure are frozen before any coverage becomes active. Changing one
requires a predecessor-linked Agreement version and complete authorization;
it never silently rewrites an active version or an already occurred loss.

### 6.1 Example without a business-specific interface

Suppose Agent A hires Agent B to review source code for 50 units of an asset.
Agent C offers a performance guarantee for a fee of 2 units and an aggregate
cap of 50 units. The coverage Agreement binds the exact A-B Agreement, B's
delivery obligation, the accepted evidence and decision profiles, A as
beneficiary, C as Guarantor, the fee, claim windows, exclusions, and payout
Adapter. If B completes, C earns the fee and no payout occurs. If a valid claim
is approved, C pays the exact approved amount up to the cap.

The same objects can express a buyer-payment guarantee, refund guarantee,
milestone guarantee, subcontract guarantee, or bounded storage, compute, and
service-availability guarantee. Those are different signed terms, not new root
opcodes or Guarantor APIs.

## 7. Decentralized discovery

### 7.1 Supply Intent

A Guarantor publishes an ordinary `AgentIntentPayloadV1`; this profile adds no
Discovery Card field. The exact mapping is:

| Existing Intent field | Guarantor V1 mapping |
| --- | --- |
| `discovery_card.summary` | short bounded statement that contingent-payment coverage is offered |
| `intent_modes[]` | exactly `[OFFER]` for the supply Intent |
| `subject_classes[]` | contains `SERVICE`; `FUNDING` is added only when the same signed detail genuinely offers funding rather than merely describing contingent liability |
| `taxonomy_paths[]` | one or more open paths for coarse coverage categories, for example `tos.taxonomy.v1/service/risk/guarantee`; unknown paths remain valid |
| `keywords[]` | bounded public terms for benefit kind, assurance class, or other issuer-asserted search concepts; exact profile IDs do not hide here |
| `capability_hints[]` | exactly `{relation: offered, capability_namespace: "tos.agent-service", capability_identifier: "guarantor"}`; a version constraint is present only when its syntax has been released by the generic Intent schema |
| `value_state` and `value_hints[]` | `range` or `negotiable`; fee uses role `asking`, while an approximate coverage cap uses role `other` and a namespaced coverage-cap unit; each carries the existing asset namespace/identifier fields |
| `schedule` | coarse availability and maximum duration only; signed quote and coverage cutoffs remain in detail/Agreement objects |
| `fulfillment_modes[]` | normally `remote` and `digital_delivery` |
| `regions[]`, `languages[]` | only normalized public service-area and language values |
| `detail_descriptor` | exact Guarantor service-profile media type, digest, byte size, and bounded inline bytes or untrusted retrieval hints |
| `reply_routes[]` | authenticated Messenger or another owner-approved route under the generic Intent rules |
| `settlement_preferences[]` | optional coarse supported choices; never collateral, solvency, or payment evidence |

Coverage categories may become taxonomy paths; benefit and assurance labels may
be keywords; fee and coverage ranges may become existing value hints. Exact
claim, evidence, collateral, jurisdiction-policy, Adapter, quote-lifetime, and
assurance-profile identifiers live only in the content-addressed
`GuarantorServiceProfileV1` detail. Neither Carrier-derived fields nor a
Guarantor-specific card extension is issuer-signed core metadata.

It MUST NOT contain private underlying Agreements, claim evidence, credentials,
customer lists, private portfolio exposure, or unredacted policy material.

### 7.2 Carrier authority boundary

Carriers store, propagate, filter, and rank immutable signed objects. They do
not determine global latest state, solvency, collateral, coverage activation,
claim validity, payout, or release. A rank or capacity hint is advisory even
when signed by the Provider.

No global Guarantor database exists. Each OpenFox merges source-local results,
verifies issuer lineage and signatures, deduplicates immutable bytes, and keeps
its own local evaluation. Existing coverage remains reconstructible from its
Agreement, authorization evidence (including the complete Firm Offer with its
signed-Intent/service-profile lineage artifact), claim objects, and Adapter evidence
after every Carrier copy is removed.

An implementation may offer a lower-assurance single-Carrier discovery path,
but it may claim resilient decentralized public discovery only after two
independent Carrier implementations, operators, stores, upstreams, and failure
domains pass the source-loss test in section 31.3.

### 7.3 Progressive retrieval and anti-abuse

Clients filter the small signed card before fetching detail. Detail and public
attachments are content addressed and subject to the generic retrieval policy:

- retrieval hints are candidates, never authority;
- only owner-approved Carrier or storage origins are reachable;
- loopback, link-local, private-network, Unix-socket, arbitrary-proxy, and
  credential-forwarding targets are rejected unless an explicit local profile
  authorizes the exact endpoint;
- DNS and every redirect are revalidated;
- TLS identity, SNI, credential origin, connection count, fan-out, time,
  compressed bytes, and decoded bytes are bounded; and
- invalid signatures, digest mismatch, size mismatch, and unavailable required
  content fail closed.

Carriers and quote endpoints apply existing signed-operation admission,
publisher budgets, rate limits, local reputation, duplicate suppression, and
bounded storage. None of these controls becomes semantic authority.

## 8. Assurance levels

One service profile MAY advertise several assurance levels. One exact level is
selected per coverage Agreement.

| Assurance | Required statement | What it does not prove |
| --- | --- | --- |
| `unsecured-signed` | the Guarantor signed a bounded contingent promise and maintains the required private reservation | collateral, independent payout, legal enforceability, or solvency |
| `collateral-attested` | an Agreement-selected profile-qualified Adapter proves an exact, current, coverage-bound collateral allocation | Adapter/custodian independence, exclusive full-cap capacity, Guarantor-control deletion, direct claimant execution, claim validity, or payout without the Guarantor and selected control subjects |
| `independently-enforceable` | selected Adapters have finalized, exclusive, same-asset capacity for the full aggregate payout cap and preserve claim admission, filing close, decision, and payout without any Guarantor-controlled subject | correctness beyond the bound decision profile, market-wide solvency, or legal status |

`collateral-attested` describes evidence quality, not operator independence.
Its canonical `CollateralControlDisclosureV1` states the Adapter operators,
custodian controller roots, and whether Guarantor control is declared, shared,
third-party controlled, or undetermined. The value in coverage terms is byte-
identical to the authenticated service-profile entry. It is a Provider
disclosure, not proof by itself. A `third_party_control_asserted` selection
always requires the exact current `AuthorizedCollateralControlEvidenceV1`
described below; callers cannot waive that evidence while retaining the token.
Every relationship remains valid for this level if owner policy accepts it,
but none proves
`independently-enforceable`. Only the full current control-resolution and
Guarantor-control-deletion test can do that. User interfaces disclose the exact
relationship and evidence class without converting it into a global trust
score.

An implementation MUST report readiness per exact capability tuple:

```text
network domain
profile version and digest
coverage asset
fee asset
benefit kind
claim evidence profile
decision profile
collateral profile
payout Adapter profile
assurance level
owner policy revision
```

Missing dependencies block only that tuple. Deployment age, transaction count,
campaign volume, or external certification is not a protocol readiness input.
The runtime must nevertheless fail closed when a current verifier, authority,
custody, collateral, settlement, or recovery dependency is absent or stale.

V1 collateralized assurance uses the same asset and canonical atomic unit as
the coverage payout. Cross-asset collateral requires a future profile that
binds an oracle, observation time, conversion rule, haircuts, and recovery
semantics; it cannot be enabled by prose or local price lookup.

An `independently-enforceable` tuple is valid only when its selected Adapter
proves an exclusive position whose beneficiary-available capacity is at least
`maximum_aggregate_payout` for the entire accepted liability window. Adapter,
network, execution, recovery, or transfer costs MUST be funded separately and
MUST NOT reduce that capacity. The Adapter's accepted execution profile must
be able to consume the position from the Agreement-selected terminal decision
and claim high-water without a fresh Guarantor signature, process, credential,
or availability assumption. The position remains subject to the same payout-
versus-release compare-and-swap domain. A partial reserve, revocable debit
permission, Guarantor-controlled wallet, stale balance proof, or capacity that
depends on the Guarantor being online is at most `collateral-attested`. Loss of
any of these properties blocks or downgrades only a newly authorized coverage
version; an implementation MUST NOT continue advertising the stronger tuple.

Independence includes action admission, not only asset custody. Every required
stage uses the exact Agreement-bound `GuarantorStageActionAuthorityV1` entry.
Its Action Authority, Writer-Fence issuer and validator, generation high-water,
action-resolution store, and admission-state domain must remain directly
reachable and satisfiable after deleting the Guarantor control closure. A
Guarantor-owned Writer Fence in front of an otherwise independent vault is
therefore only `collateral-attested`.

## 9. Canonical encoding, digests, signatures, and bounds

The released structural schema is
[`schemas/agent-guarantor-service-v1.json`](../schemas/agent-guarantor-service-v1.json).
It is deterministically generated from the closed object and mutation type
registries in `tos-service-protocol`; wire
objects use RFC 8949 Core Deterministic CBOR with text map keys. Integers use
the shortest representation. Indefinite values, floats, tags, duplicate keys,
invalid UTF-8, noncanonical Base64, unknown fields, and alternate spellings
fail closed.

Collections declared as sets are sorted by their released canonical key and
reject duplicates. Ordered claim, decision, payout, and predecessor sequences
retain order and reject gaps or forks.

Wire `kind` and `state` values are exact lower-case ASCII tokens. State-machine
diagrams render the same values in upper case only for readability; an
implementation lowercases no input and rejects upper-case or alternate wire
spellings.

The common digest formula is:

```text
Digest(domain, value) = "sha256:" || lower_hex(SHA-256(
  "TOS-PROTOCOL-CBOR\0" ||
  uint16_big_endian(len(domain)) || domain || canonical_cbor(value)))
```

The service profile URI uses the registered `tos.agent-service.*` discovery
namespace. Every media type, digest domain, envelope domain, signature domain,
and verifier identifier introduced by this document uses the current
`tos.service.*` protocol namespace and is valid only under wire protocol
`tos_service_v1`. No pre-migration spelling or compatibility alias is accepted.
References to already released generic Agreement, Semantic Action, taxonomy,
and evidence-set identifiers retain their exact released bytes; this profile
does not silently rename another specification's domain.

Proposed digest domains are:

| Value | Domain |
| --- | --- |
| `GuarantorServiceProfileV1` | `tos.service.agent-guarantor-service-profile.v1` |
| `GuarantorServiceProfileArtifactV1` | `tos.service.agent-guarantor-service-profile-artifact.v1` |
| `GuarantorCollateralProfileV1` | `tos.service.agent-guarantor-collateral-profile.v1` |
| `CollateralTransitionProfileV1` | `tos.service.agent-guarantor-collateral-transition-profile.v1` |
| `CollateralControlDisclosureV1` | `tos.service.agent-guarantor-collateral-control-disclosure.v1` |
| collateral-control evidence body | `tos.service.agent-guarantor-collateral-control-evidence.v1` |
| `CollateralAuthorizationBindingV1` | `tos.service.agent-guarantor-collateral-authorization-binding.v1` |
| `CollateralTransitionBindingV1` | `tos.service.agent-guarantor-collateral-transition-binding.v1` |
| `GuarantorClaimProfileV1` | `tos.service.agent-guarantor-claim-profile.v1` |
| `DeterministicFallbackReasonRuleV1` | `tos.service.agent-guarantor-fallback-reason-rule.v1` |
| quote-request body | `tos.service.agent-guarantor-quote-request.v1` |
| `RequestedCoverageTermsV1` | `tos.service.agent-guarantor-requested-coverage-terms.v1` |
| `GuarantorCoverageTermsV1` | `tos.service.agent-guarantor-coverage-terms.v1` |
| `CoverageCancellationPolicyV1` | `tos.service.agent-guarantor-cancellation-policy.v1` |
| coverage identity preimage | `tos.service.agent-guarantor-coverage-id.v1` |
| `PayoutDestinationV1` | `tos.service.agent-guarantor-payout-destination.v1` |
| `CoverageEndCommitmentV1` | `tos.service.agent-guarantor-coverage-end-commitment.v1` |
| `GuarantorStageOperationBindingV1` | `tos.service.agent-guarantor-stage-operation-binding.v1` |
| `GuarantorStageActionAuthorityBindingV1` | `tos.service.agent-guarantor-stage-action-authority-binding.v1` |
| `GuarantorOperationalIndependenceTermsV1` | `tos.service.agent-guarantor-operational-independence-terms.v1` |
| `GuarantorObjectVerifierRegistryV1` | `tos.service.agent-guarantor-object-verifier-registry.v1` |
| `GuarantorMutationVerifierRegistryV1` | `tos.service.agent-guarantor-mutation-verifier-registry.v1` |
| `AuthorityAdmissionEligibilityProofV1` | `tos.service.agent-guarantor-authority-admission-eligibility-proof.v1` |
| `AuthorityAdmissionEligibilityProofSetV1` | `tos.service.agent-guarantor-authority-admission-eligibility-proof-set.v1` |
| `GuarantorFirmOfferAgreementEvidenceV1` | `tos.service.agent-guarantor-firm-offer-agreement-evidence.v1` |
| `GuarantorAgreementAuthorizationEvidenceSetV1` | `tos.service.agent-guarantor-agreement-authorization-evidence-set.v1` |
| `CanonicalGuarantorEvidenceSetV1` | `tos.service.agent-guarantor-evidence-set.v1` |
| `MaterializedPayoutObligationSetV1` | `tos.service.agent-guarantor-payout-obligation-set.v1` |
| `ClaimPayoutLineV1` | `tos.service.agent-guarantor-payout-line.v1` |
| `MaterializedPayoutLineV1` | `tos.service.agent-guarantor-materialized-payout-line.v1` |
| `ProfileQualifiedSettlementParametersV1` | `tos.service.agent-guarantor-settlement-parameters.v1` |
| payout-obligation instance identity | `tos.service.agent-guarantor-payout-instance.v1` |
| `TerminalPayoutEvidenceSetV1` | `tos.service.agent-guarantor-terminal-payout-evidence-set.v1` |
| `CoverageTerminalPayoutEvidenceSetV1` | `tos.service.agent-guarantor-coverage-terminal-payout-evidence-set.v1` |
| `PortableStageActionAdmissionBodyV1` | `tos.service.agent-guarantor-stage-action-admission.v1` |
| `PortableStageActionAdmissionEvidenceV1` | `tos.service.agent-guarantor-stage-action-admission-evidence.v1` |
| `AuthorizedGuarantorPayoutExecutionEvidenceV1` | `tos.service.agent-guarantor-payout-execution-evidence.v1` |
| `GuarantorAgreementPaymentActionBodyV1` | `tos.service.agent-guarantor-agreement-payment-action.v1` |
| exposure-admission descriptor | `tos.service.agent-guarantor-exposure-admission.v1` |
| reservation identity | `tos.service.agent-guarantor-reservation-id.v1` |
| exposure receipt body | `tos.service.agent-guarantor-exposure-receipt.v1` |
| firm-offer body | `tos.service.agent-guarantor-firm-offer.v1` |
| firm-offer issuance terms | `tos.service.agent-guarantor-firm-offer-issuance-terms.v1` |
| `FirmOfferRecipientSetV1` | `tos.service.agent-guarantor-firm-offer-recipient-set.v1` |
| `ProviderExposureReservationScopeV1` | `tos.service.agent-guarantor-reservation-scope.v1` |
| offer non-acceptance body | `tos.service.agent-guarantor-offer-non-acceptance.v1` |
| pre-acceptance release receipt body | `tos.service.agent-guarantor-pre-acceptance-release-receipt.v1` |
| pre-acceptance release evidence projection | `tos.service.agent-guarantor-pre-acceptance-release-evidence-projection.v1` |
| acceptance-request body | `tos.service.agent-guarantor-acceptance-request.v1` |
| acceptance-receipt body | `tos.service.agent-guarantor-acceptance-receipt.v1` |
| activation-evidence body | `tos.service.agent-guarantor-activation-evidence.v1` |
| non-activation-evidence body | `tos.service.agent-guarantor-non-activation-evidence.v1` |
| `ActivationAdmissionCutProofV1` | `tos.service.agent-guarantor-activation-cut-proof.v1` |
| `ActivationPrerequisiteFailureRuleV1` | `tos.service.agent-guarantor-activation-prerequisite-failure-rule.v1` |
| `CoverageNonActivationReasonRuleV1` | `tos.service.agent-guarantor-non-activation-reason-rule.v1` |
| `TerminalPrerequisiteFailureEvidenceV1` | `tos.service.agent-guarantor-terminal-prerequisite-failure-evidence.v1` |
| `PreActivationMutualCancellationBodyV1` | `tos.service.agent-guarantor-pre-activation-mutual-cancellation.v1` |
| `CoverageNonActivationReasonEvidenceV1` | `tos.service.agent-guarantor-non-activation-reason-evidence.v1` |
| `CoverageNonActivationActionBodyV1` | `tos.service.agent-guarantor-non-activation-action.v1` |
| coverage-cancellation request body | `tos.service.agent-guarantor-cancellation-request.v1` |
| coverage-cancellation receipt body | `tos.service.agent-guarantor-cancellation-receipt.v1` |
| collateral evidence body | `tos.service.agent-guarantor-collateral-evidence.v1` |
| `CollateralPositionStateV1` | `tos.service.agent-guarantor-collateral-position-state.v1` |
| `CollateralAdapterRequestV1` | `tos.service.agent-guarantor-collateral-adapter-request.v1` |
| `CollateralAdapterEvidenceV1` | `tos.service.agent-guarantor-collateral-adapter-evidence.v1` |
| `CollateralTransitionActionBodyV1` | `tos.service.agent-guarantor-collateral-transition-action.v1` |
| `CollateralPayoutPaymentEvidenceProjectionV1` | `tos.service.agent-guarantor-collateral-payout-payment-evidence.v1` |
| claim-evidence manifest | `tos.service.agent-guarantor-claim-evidence-manifest.v1` |
| `OtherRecoveryDeclarationV1` | `tos.service.agent-guarantor-other-recovery-declaration.v1` |
| `TriggeredObligationSetV1` | `tos.service.agent-guarantor-triggered-obligation-set.v1` |
| claim identity preimage | `tos.service.agent-guarantor-claim-id.v1` |
| claim body | `tos.service.agent-guarantor-claim.v1` |
| claim-submission ingress action body | `tos.service.agent-guarantor-claim-ingress-action.v1` |
| claim-submission ingress receipt body | `tos.service.agent-guarantor-claim-ingress-receipt.v1` |
| `ClaimIngressAdmissionCutProofV1` | `tos.service.agent-guarantor-claim-ingress-cut-proof.v1` |
| `ClaimSubmissionAuthorityInstanceEffectV1` | `tos.service.agent-guarantor-claim-submission-authority-instance-effect.v1` |
| claim-submission action body | `tos.service.agent-guarantor-claim-submission-action.v1` |
| claim-admission body | `tos.service.agent-guarantor-claim-admission.v1` |
| `ClaimRevisionAdmissionLeafV1` | `tos.service.agent-guarantor-claim-revision-admission-leaf.v1` |
| claim-revision log root step | `tos.service.agent-guarantor-claim-revision-log-root.v1` |
| claim-filing close receipt body | `tos.service.agent-guarantor-claim-filing-close.v1` |
| claim-decision body | `tos.service.agent-guarantor-claim-decision.v1` |
| `ClaimDecisionPolicyApplicationV1` | `tos.service.agent-guarantor-claim-decision-policy-application.v1` |
| `DeterministicFallbackAggregateProjectionV1` | `tos.service.agent-guarantor-fallback-aggregate-projection.v1` |
| `ClaimDecisionReasonV1` | `tos.service.agent-guarantor-claim-decision-reason.v1` |
| `ClaimRevisionEpochExpectationV1` | `tos.service.agent-guarantor-claim-revision-epoch-expectation.v1` |
| `ClaimDecisionSourceHeadV1` | `tos.service.agent-guarantor-claim-decision-source-head.v1` |
| `AuthorizedDecisionAdmissionIdentityV1` | `tos.service.agent-guarantor-authorized-decision-admission-identity.v1` |
| `DeterministicFallbackAdmissionIdentityV1` | `tos.service.agent-guarantor-fallback-admission-identity.v1` |
| claim-decision admission receipt body | `tos.service.agent-guarantor-claim-decision-admission.v1` |
| decision-application token | `tos.service.agent-guarantor-decision-application-token.v1` |
| decision-application token identity | `tos.service.agent-guarantor-decision-application-token-id.v1` |
| claim-decision application receipt body | `tos.service.agent-guarantor-decision-application.v1` |
| claim-state transition receipt body | `tos.service.agent-guarantor-claim-state-transition.v1` |
| `ClaimTerminalResolutionRefSetV1` | `tos.service.agent-guarantor-claim-resolution-set.v1` |
| terminal claim set | `tos.service.agent-guarantor-terminal-claim-set.v1` |
| coverage-closure evidence context | `tos.service.agent-guarantor-coverage-closure-context.v1` |
| `ExposureDispositionComputationV1` | `tos.service.agent-guarantor-exposure-disposition.v1` |
| exposure-release receipt body | `tos.service.agent-guarantor-exposure-release-receipt.v1` |
| coverage-resolution body | `tos.service.agent-guarantor-resolution.v1` |
| transition-evidence projection | `tos.service.agent-guarantor-transition-evidence-projection.v1` |
| exposure-release evidence projection | `tos.service.agent-guarantor-exposure-release-evidence-projection.v1` |

Complete-envelope digest domains are:

| Envelope | Domain |
| --- | --- |
| `AuthorizedCoverageQuoteRequestV1` | `tos.service.agent-guarantor-quote-request-envelope.v1` |
| `AuthorizedProviderExposureAdmissionReceiptV1` | `tos.service.agent-guarantor-exposure-receipt-envelope.v1` |
| `AuthorizedFirmCoverageOfferV1` | `tos.service.agent-guarantor-firm-offer-envelope.v1` |
| `AuthorizedOfferNonAcceptanceEvidenceV1` | `tos.service.agent-guarantor-offer-non-acceptance-envelope.v1` |
| `AuthorizedPreAcceptanceExposureReleaseReceiptV1` | `tos.service.agent-guarantor-pre-acceptance-release-receipt-envelope.v1` |
| `AuthorizedCoverageAcceptanceRequestV1` | `tos.service.agent-guarantor-acceptance-request-envelope.v1` |
| `AuthorizedCoverageAcceptanceReceiptV1` | `tos.service.agent-guarantor-acceptance-receipt-envelope.v1` |
| `AuthorizedCoverageActivationEvidenceV1` | `tos.service.agent-guarantor-activation-evidence-envelope.v1` |
| `AuthorizedCoverageNonActivationEvidenceV1` | `tos.service.agent-guarantor-non-activation-evidence-envelope.v1` |
| `AuthorizedCoverageCancellationRequestV1` | `tos.service.agent-guarantor-cancellation-request-envelope.v1` |
| `AuthorizedCoverageCancellationReceiptV1` | `tos.service.agent-guarantor-cancellation-receipt-envelope.v1` |
| `AuthorizedCollateralControlEvidenceV1` | `tos.service.agent-guarantor-collateral-control-evidence-envelope.v1` |
| `AuthorizedCoverageClaimV1` | `tos.service.agent-guarantor-claim-envelope.v1` |
| `AuthorizedClaimSubmissionIngressReceiptV1` | `tos.service.agent-guarantor-claim-ingress-receipt-envelope.v1` |
| `AuthorizedClaimAdmissionReceiptV1` | `tos.service.agent-guarantor-claim-admission-envelope.v1` |
| `AuthorizedClaimFilingCloseReceiptV1` | `tos.service.agent-guarantor-claim-filing-close-envelope.v1` |
| `AuthorizedClaimDecisionV1` | `tos.service.agent-guarantor-claim-decision-envelope.v1` |
| `AuthorizedClaimDecisionAdmissionReceiptV1` | `tos.service.agent-guarantor-claim-decision-admission-envelope.v1` |
| `AuthorizedClaimDecisionApplicationReceiptV1` | `tos.service.agent-guarantor-decision-application-envelope.v1` |
| `AuthorizedClaimStateTransitionReceiptV1` | `tos.service.agent-guarantor-claim-state-transition-envelope.v1` |
| `AuthorizedCollateralEvidenceV1` | `tos.service.agent-guarantor-collateral-evidence-envelope.v1` |
| `AuthorizedTerminalClaimSetEvidenceV1` | `tos.service.agent-guarantor-terminal-claim-set-evidence.v1` |
| `AuthorizedExposureReleaseReceiptV1` | `tos.service.agent-guarantor-exposure-release-receipt-envelope.v1` |
| `AuthorizedCoverageResolutionV1` | `tos.service.agent-guarantor-resolution-envelope.v1` |

References to an authorized object commit its complete canonical envelope under a
released envelope-digest domain; they do not commit only its unsigned body.
References whose names end in `_body_digest` deliberately commit only the
named canonical body. This distinction prevents a verifier from substituting a
different key, authorization proof, or wrapper around equal body bytes.

When an `Authorized*V1` envelope selects the native Ed25519 Agent profile, its
authorization evidence signs the complete canonical authorization statement,
not only the business body:

```text
NativeObjectAuthorizationStatementV1 {
  schema_version                    # 1
  authority_subject
  profile_uri
  profile_version
  profile_digest
  authorized_object_kind
  authorized_body_digest
  validation_time_unix
}

message = SHA-256(
  signature_domain || "\0" ||
  uint32_big_endian(len(canonical_authorization_statement)) ||
  canonical_authorization_statement)
```

| Object envelope | Native Agent signature domain |
| --- | --- |
| `AuthorizedCoverageQuoteRequestV1` | `tos.service.agent-guarantor-quote-request-signature.v1` |
| `AuthorizedProviderExposureAdmissionReceiptV1` | `tos.service.agent-guarantor-exposure-receipt-signature.v1` |
| `AuthorizedFirmCoverageOfferV1` | `tos.service.agent-guarantor-firm-offer-signature.v1` |
| `AuthorizedOfferNonAcceptanceEvidenceV1` | `tos.service.agent-guarantor-offer-non-acceptance-signature.v1` |
| `AuthorizedPreAcceptanceExposureReleaseReceiptV1` | `tos.service.agent-guarantor-pre-acceptance-release-receipt-signature.v1` |
| `AuthorizedCoverageAcceptanceRequestV1` | `tos.service.agent-guarantor-acceptance-request-signature.v1` |
| `AuthorizedCoverageAcceptanceReceiptV1` | `tos.service.agent-guarantor-acceptance-receipt-signature.v1` |
| `AuthorizedCoverageActivationEvidenceV1` | `tos.service.agent-guarantor-activation-evidence-signature.v1` |
| `AuthorizedCoverageNonActivationEvidenceV1` | `tos.service.agent-guarantor-non-activation-evidence-signature.v1` |
| `AuthorizedCoverageCancellationRequestV1` | `tos.service.agent-guarantor-cancellation-request-signature.v1` |
| `AuthorizedCoverageCancellationReceiptV1` | `tos.service.agent-guarantor-cancellation-receipt-signature.v1` |
| `AuthorizedCollateralControlEvidenceV1` | `tos.service.agent-guarantor-collateral-control-evidence-signature.v1` |
| `AuthorizedCoverageClaimV1` | `tos.service.agent-guarantor-claim-signature.v1` |
| `AuthorizedClaimSubmissionIngressReceiptV1` | `tos.service.agent-guarantor-claim-ingress-receipt-signature.v1` |
| `AuthorizedClaimAdmissionReceiptV1` | `tos.service.agent-guarantor-claim-admission-signature.v1` |
| `AuthorizedClaimFilingCloseReceiptV1` | `tos.service.agent-guarantor-claim-filing-close-signature.v1` |
| `AuthorizedClaimDecisionV1` | `tos.service.agent-guarantor-claim-decision-signature.v1` |
| `AuthorizedClaimDecisionAdmissionReceiptV1` | `tos.service.agent-guarantor-claim-decision-admission-signature.v1` |
| `AuthorizedClaimDecisionApplicationReceiptV1` | `tos.service.agent-guarantor-decision-application-signature.v1` |
| `AuthorizedClaimStateTransitionReceiptV1` | `tos.service.agent-guarantor-claim-state-transition-signature.v1` |
| `AuthorizedCollateralEvidenceV1` | `tos.service.agent-guarantor-collateral-evidence-signature.v1` |
| `AuthorizedTerminalClaimSetEvidenceV1` | `tos.service.agent-guarantor-terminal-claim-set-signature.v1` |
| `AuthorizedExposureReleaseReceiptV1` | `tos.service.agent-guarantor-exposure-release-receipt-signature.v1` |
| `AuthorizedCoverageResolutionV1` | `tos.service.agent-guarantor-resolution-signature.v1` |
| `PortableStageActionAdmissionEvidenceV1` | `tos.service.agent-guarantor-stage-action-admission-signature.v1` |

The verifier first recomputes the canonical body digest and then requires every
statement field to equal the containing
`ProfileQualifiedObjectAuthorizationV1`. Replacing the subject, profile,
object kind, body digest, or validation time therefore invalidates the native
signature. For a pre-admission assertion, `validation_time_unix` is the
body-defined creation or decision time and proves only that the signer was
eligible when it signed. It never proves that the signer remains eligible when
the assertion is later admitted. For an authority-produced receipt,
`validation_time_unix` is the trusted admission, release, or resolution time
selected by the released result profile.

Within native Ed25519 evidence, public keys use `ed25519:` followed by 64
lowercase hexadecimal characters. Signatures use `ed25519:` followed by
unpadded RFC 4648 URL-safe Base64.
Uppercase hex, padded Base64, aliases, replaceable wrapper paths, or signatures
over noncanonical bytes fail closed.

### 9.1 Signer authority resolution

A `public_key` carried by native authorization evidence is key material, not
authority. Before
accepting a signature, a verifier resolves the exact named signing subject and
proves that the key was authorized for the object kind, network or authority
domain, role, and validation time. The required bindings are:

| Object envelope | Named signing subject or authority |
| --- | --- |
| quote request | `requester_agent_id` |
| firm offer | `guarantor_agent_id` |
| acceptance request | `accepting_subject` |
| coverage cancellation request | the selected cancellation-policy branch's `permitted_requester_subjects[]`, authorization profile, and exact quorum rule |
| coverage cancellation receipt | the Agreement-selected lifecycle authority, or the exact single `coverage_cancellation` independent-stage Action Authority for `independently-enforceable` |
| claim | `claimant_subject` |
| claim-submission ingress receipt | the Agreement-selected claim-ingress authority, or the exact single `claim_submission_ingress` independent-stage Action Authority for `independently-enforceable` |
| claim decision | the Agreement-selected `decision_authority_subjects[]` and exact quorum rule |
| claim-filing close receipt | the Agreement-selected claim-admission authority subjects and exact quorum rule |
| claim-decision admission receipt | the Agreement-selected decision-admission authority subjects and exact quorum rule |
| collateral control evidence | the selected disclosure's `disclosure_authority_subjects[]` and exact quorum rule |
| collateral evidence | the selected collateral profile's custody or independent-execution subjects and exact quorum rule |
| offer non-acceptance evidence | `lifecycle_authority_id` from the exact service profile under the Agreement terms' `acceptance_authority_profile` |
| terminal claim set | the Agreement-selected claim-admission authority subjects and exact quorum rule |
| exposure, pre-acceptance release, acceptance, activation, claim-admission, decision-application, claim-state-transition, post-acceptance exposure-release, or coverage-resolution evidence | the exact `authority_id` and its role bound by the accepted Agreement, firm offer, or service profile |

Agent keys use the released historical Agent-authority resolver. Authority,
custody, wallet, contract, quorum, or non-Ed25519 subjects use the exact
profile-qualified authorization evidence selected by the Agreement; they
cannot be represented by placing an arbitrary Ed25519 key in native evidence.
The verifier checks key epoch, delegation scope and history, revocation order,
validity interval, profile digest, and subject-to-participant relationship at
the authorized object's signed validation time. Current-key lookup alone is
insufficient for historical evidence, and a self-issued key-binding statement
is insufficient for every subject.

Historical signature validity is necessary but never sufficient to create a
new side effect. At the linearized admission checkpoint for a quote issuance,
acceptance, claim, cancellation, decision, collateral transition, payout, or
other mutation, the sink MUST resolve every newly presented authorization
subject and exact key or principal against fresh finalized authority state at
the sink-generated admission time. A body timestamp, local receipt time,
caller-supplied resolver head, or proof finalized only before that checkpoint
cannot satisfy this rule. The sink atomically admits the mutation and freezes
an exact `AuthorityAdmissionEligibilityProofSetV1`; its entries bind the input
envelope and body, required scope, resolver profile, finalized state revision
and root, finality evidence, admission domain/sequence, and admission time.
Every entry has `eligibility_state = eligible`; an absent, revoked, expired,
wrong-scope, non-final, stale, or conflicting result fails closed.

The proof set is sorted by input-envelope digest, authority subject, and
authority-key/principal digest and rejects duplicates. Its admission action,
domain, sequence, and time must equal the mutation receipt. Its digest is
`Digest("tos.service.agent-guarantor-authority-admission-eligibility-proof-set.v1",
proof_set)`. The V1 result schemas that first admit quote-request, acceptance,
claim, cancellation, decision, activation-prerequisite, claim-transition, or
collateral authorization explicitly carry that digest and exact proof set.
A selected generic payment or settlement Adapter MUST likewise include it in
the released terminal evidence wrapper and its `ActionResolutionV1` whenever it
first admits a payer, custody, or execution authorization; the Guarantor
profile cannot weaken that Adapter rule. A new mutation that first acts on
signed input must version its result schema to carry the same proof. Already
admitted immutable inputs are resolved
through their original durable result and proof set rather than re-admitted;
later revocation does not rewrite a completed action. If no such durable result
exists, a signature created or backdated before revocation cannot be admitted
after revocation. Recovery retains and verifies the frozen proof and never
substitutes a current-key lookup.

The envelope's complete profile-qualified authority evidence is part of the
complete envelope digest. A correct signature from an unauthorized, expired, revoked,
wrong-role, wrong-domain, or wrong-profile key fails closed. These checks apply
equally when an object arrives through Messenger, a direct endpoint, a Carrier,
an Adapter callback, or local recovery.

The V1 schema freezes at least these limits:

- complete canonical object or event envelope: 1 MiB;
- inline service-profile detail: 64 KiB;
- complete `GuarantorServiceProfileArtifactV1` revision lineage: 512 KiB;
- terms or policy descriptor collection: 256 KiB;
- profile lifetime: 90 days;
- firm-offer lifetime: 15 minutes;
- evidence descriptors per claim: 128;
- in-band proof bytes: 256 KiB;
- claim and payout lines: bounded by the Agreement's finite `maximum_claims`
  and schema caps; and
- every identifier, URI, digest, count, time calculation, and decoded byte
  length has an explicit schema bound.

Large or private evidence remains content addressed and out of band. Declared
size does not authorize retrieval; retrieval and model-ingress budgets are
separate and stricter.

## 10. Common profile types

The pseudocode below names canonical fields. The JSON Schema, Go types, and
independent verifier must reproduce the same presence, ordering, bounds, and
failure rules.

Unless a field is explicitly suffixed `_digest`, `_id`, `_subject`, or
`_subjects`, a field whose name ends in `_profile` is an exact `ProfileRefV1`.
A plural `*_profiles[]` is a bounded canonical set of exact `ProfileRefV1`
values unless its schema explicitly declares another typed entry, as section
11 does for claim and collateral subprofiles. Display strings and bare URIs
never satisfy these fields.

```text
ProfileRefV1 {
  profile_uri
  profile_version
  profile_digest
}

PolicyRefV1 {
  content_type
  content_digest
  content_size
}

ImmutableEvidenceDescriptorV1 {
  content_type
  content_digest
  content_size
  retrieval_policy_digest
}

AssetIdentityV1 {
  asset_namespace
  asset_identifier
  unit
}

AtomicAmountV1 {
  asset
  amount_atomic
}

AtomicAmountRangeV1 {
  minimum
  maximum
}

ClaimContinuationBudgetEntryV1 {
  profile_state_key
  challenge_rounds_remaining
  nonterminal_rounds_remaining
  required_reserved_decision_admission_slots
  required_reserved_claim_state_transition_slots
  maximum_remaining_decision_path_seconds
  maximum_remaining_closure_seconds
}

DeterministicClaimTerminalFallbackV1 {
  schema_version
  fallback_profile
  fallback_authority_subjects[]
  fallback_quorum_rule
  eligible_source_states[]             # exact set: initial_reviewing,
                                       # evidence_required, disputed,
                                       # reviewing_after_challenge,
                                       # reviewing_after_nonterminal_response
  trigger_deadline_rules[] {
    source_state
    deadline_source                    # claim_review_cutoff,
                                       # resolution_due_at_unix, or
                                       # successor_decision_due_at_unix
  }
  evidence_snapshot_rule                # exactly current_portable_claim_history in V1
  outcome_rule                          # deny_zero or accepted_benefit_calculation
  aggregate_cap_projection_rule         # not_applicable_deny_zero or
                                         # remaining-aggregate-min.v1
  reason_rules[]                         # exact DeterministicFallbackReasonRuleV1 set
  payout_line_derivation_rule           # exact accepted payout-template projection
  authorization_mode                    # exactly agreement_granted_deterministic_admission
  final_round_rule                      # exactly challenge_window_then_close
}

DeterministicFallbackReasonRuleV1 {
  outcome_case                          # deny_zero, no_eligible_benefit,
                                        # aggregate_exhausted,
                                        # aggregate_limited, or full_benefit
  result                                # exact derived decision result
  reason_code                           # exact decision-profile registry token
  applicable_policy_clause_ids[]        # exact canonical Agreement subset
  evidence_predicate_selection_rule     # exactly all_decision_evidence_predicates
}

ClaimClosureCapacityV1 {
  maximum_claims
  maximum_claim_ingress_actions
  maximum_claim_revisions_per_claim       # includes the initial claim
  maximum_decision_admissions_per_claim   # includes every permitted continuation and fallback
  maximum_claim_state_transitions_per_claim # includes every permitted response, challenge, and close
  maximum_challenge_rounds_per_claim
  maximum_nonterminal_rounds_per_claim
  maximum_payout_lines_per_claim
  maximum_admitted_claim_envelope_bytes
  maximum_claim_ingress_receipt_envelope_bytes
  maximum_claim_ingress_cut_proof_bytes
  maximum_acceptance_request_envelope_bytes
  maximum_acceptance_receipt_envelope_bytes
  maximum_activation_evidence_envelope_bytes
  maximum_non_activation_evidence_envelope_bytes
  maximum_cancellation_receipt_envelope_bytes
  maximum_claim_filing_close_receipt_envelope_bytes
  maximum_terminal_claim_set_envelope_bytes
  maximum_exposure_release_request_bytes
  maximum_exposure_release_receipt_bytes
  maximum_coverage_resolution_request_bytes
  maximum_coverage_resolution_envelope_bytes
  computed_worst_case_acceptance_request_envelope_bytes
  computed_worst_case_acceptance_receipt_envelope_bytes
  computed_worst_case_activation_evidence_envelope_bytes
  computed_worst_case_non_activation_evidence_envelope_bytes
  computed_worst_case_cancellation_receipt_envelope_bytes
  computed_worst_case_claim_filing_close_receipt_envelope_bytes
  computed_worst_case_terminal_claim_set_bytes
  computed_worst_case_exposure_release_request_bytes
  computed_worst_case_exposure_release_receipt_bytes
  computed_worst_case_coverage_resolution_request_bytes
  computed_worst_case_coverage_resolution_envelope_bytes
  continuation_budget_profile
  continuation_budget_entries[]           # exact ClaimContinuationBudgetEntryV1 set
  terminal_fallback                       # exact DeterministicClaimTerminalFallbackV1
}

PayoutDestinationV1 {
  schema_version
  settlement_adapter_profile
  beneficiary_subject
  asset
  network_or_system_digest
  destination_encoding
  destination_bytes                  # bounded byte string
  routing_parameters                 # bounded canonical byte string
}

PayoutDestinationBindingV1 {
  mode                               # exactly agreement_fixed in V1
  destination_authorization_predicate_id
  payout_destination                 # exact PayoutDestinationV1
}

CoverageEndCommitmentV1 {
  schema_version
  coverage_agreement_body_digest
  coverage_obligation_id
  coverage_state_domain_digest
  end_branch                         # scheduled, accepted_cancellation,
                                     # or never_activated
  incident_eligibility_ends_at_unix?
  coverage_end_evidence_digest?
}

CollateralControlDisclosureV1 {
  schema_version
  custody_adapter_profile
  adapter_operator_subjects[]
  custodian_controller_root_subjects[]
  declared_guarantor_control_relationship # guarantor_controlled,
                                           # shared_control,
                                           # third_party_control_asserted,
                                           # or control_undetermined
  control_resolution_profile?
  disclosure_evidence_profile?
  disclosure_authority_subjects[]?
  disclosure_authority_quorum_rule?
  maximum_disclosure_evidence_age_seconds?
}

CollateralControlEvidenceBodyV1 {
  schema_version
  coverage_agreement_body_digest
  collateral_obligation_id
  selected_collateral_profile_digest
  collateral_control_disclosure_digest
  custody_adapter_profile
  adapter_operator_subjects[]
  custodian_controller_root_subjects[]
  declared_guarantor_control_relationship # exactly third_party_control_asserted
  observed_at_unix
  expires_at_unix
}

AuthorizedCollateralControlEvidenceV1 {
  body
  authorizations[]
}

GuarantorStageOperationResultBindingV1 {
  role
  canonical_type
  digest_or_envelope_domain
  cardinality                       # exactly_one or profile_selected
  presence_rule                     # exactly accepted_effect_v1
}

GuarantorStageOperationBindingV1 {
  schema_version                       # exactly 1
  stage
  operation_registry_profile           # exact ProfileRefV1
  operation_id
  action_kind
  operation_purpose
  semantic_action_registry_version     # exactly 1
  semantic_action_entry_version        # exactly 1
  request_schema_version
  request_type
  request_body_profile_id
  maximum_request_bytes                # positive and no more than 1,048,576
  result_components[]
  required_context_types[]
  semantic_field_derivation_profile_id
  transition_validator_profile_id
  materializer_profile_id
  adapter_route_profile_source       # coverage_operation_adapter_profile,
                                     # claim_operation_adapter_profile,
                                     # selected_payout_adapter_profile, or
                                     # exposure_operation_adapter_profile
  adapter_operation
  cas_domain_source                  # released closed enum in section 11
  stage_derivation_profile_id
}

GuarantorStageActionAuthorityV1 {
  stage                              # one exact required-independent-stage value
  operation_binding                  # exact GuarantorStageOperationBindingV1
  operation_binding_digest
  action_owner_id                    # exact owner_id in the semantic-action key
  action_agent_id                    # exact agent_id in the semantic-action key
  action_authority_id                # exact AuthorizedActionV1 authority_id
  writer_fence_domain_id
  writer_fence_authority_id           # equals action_authority_id
  writer_generation_high_water_profile
  action_resolution_profile
  admission_state_domain_digest
}

GuarantorStageActionAuthorityBindingV1 {
  schema_version
  authority_domain_digest
  stages[]                           # exact GuarantorStageActionAuthorityV1 set
}

PortableStageActionAdmissionBodyV1 {
  schema_version                       # exactly 1
  stage
  operation_id
  operation_binding_digest
  admitted_at_unix
  canonical_request_digest
  authorized_action_digest
  writer_fence_digest
  admission_state                       # exactly accepted
  admission_state_revision
}

PortableStageActionAdmissionEvidenceV1 {
  body
  canonical_request_content_type
  canonical_request                    # exact bounded canonical request bytes
  authorized_action                    # exact canonical AuthorizedActionV1
  writer_fence                         # exact canonical WriterFenceV1
  action_admission_authorization       # exact scalar Action Authority authorization
}

GuarantorOperationalIndependenceTermsV1 {
  schema_version
  authority_control_resolution_profile
  coverage_operation_adapter_profile
  claim_operation_adapter_profile
  exposure_operation_adapter_profile
  required_independent_stages[]      # exact V1 set: coverage_activation,
                                     # coverage_non_activation,
                                     # claim_submission_ingress,
                                     # initial_claim_admission,
                                     # claim_revision_admission,
                                     # claim_state_transition, filing_close,
                                     # terminal_decision,
                                     # decision_application, payout_execution,
                                     # coverage_cancellation, coverage_closure,
                                     # post_acceptance_exposure_release,
                                     # coverage_resolution
  guarantor_control_root_subjects[]
  stage_action_authority_binding_digest # exact Agreement sibling binding
  authority_change_policy            # exact PolicyRefV1
  maximum_control_evidence_age_seconds
}

ProfileQualifiedObjectAuthorizationV1 {
  authority_subject
  profile_uri
  profile_version
  profile_digest
  authorized_object_kind
  authorized_body_digest
  validation_time_unix
  evidence_content_type
  evidence
}

NativeEd25519AgentAuthorizationEvidenceV1 {
  public_key
  signature
  historical_authority_proof
}

AuthorityAdmissionEligibilityProofV1 {
  schema_version
  input_authorized_envelope_digest
  authority_subject
  authority_key_or_principal_digest
  authorized_object_kind
  authorized_body_digest
  required_scope_digest
  authority_resolver_profile          # exact ProfileRefV1
  finalized_authority_state_revision
  finalized_authority_state_root
  resolver_finality_evidence          # exact profile-qualified evidence
  admission_domain_id
  admission_sequence
  admission_time_unix
  eligibility_state                   # eligible
}

AuthorityAdmissionEligibilityProofSetV1 {
  schema_version
  admitted_action_digest
  admission_domain_id
  admission_sequence
  admission_time_unix
  entries[]
}

CanonicalGuarantorEvidenceItemV1 {
  content_type
  evidence_profile_digest
  evidence_envelope_digest
  representation                     # inline or content_addressed
  canonical_envelope_bytes?          # bounded CBOR byte string
  immutable_descriptor?
}

CanonicalGuarantorEvidenceSetV1 {
  schema_version
  purpose
  context_digest
  items[]
}
```

`CollateralControlDisclosureV1` has a closed presence matrix. For
`third_party_control_asserted`, `control_resolution_profile`,
`disclosure_evidence_profile`, nonempty sorted
`disclosure_authority_subjects[]`, a satisfiable
`disclosure_authority_quorum_rule`, and a positive bounded
`maximum_disclosure_evidence_age_seconds` are all required; they are all
absent for the other three relationship tokens. The authorized control-
evidence body copies the selected disclosure's Adapter profile, operator set,
controller-root set, and relationship byte-for-byte. Its disclosure digest is
`Digest("tos.service.agent-guarantor-collateral-control-disclosure.v1",
collateral_control_disclosure)`, and its complete envelope is authorized by
exactly the disclosure authority subjects and quorum under the selected
evidence profile.

`expires_at_unix` is exactly `observed_at_unix +
maximum_disclosure_evidence_age_seconds`, with checked arithmetic. Verification
requires `observed_at_unix <= validation_time_unix <= expires_at_unix`. It
resolves the exact subject/key authority from finalized history at both
`observed_at_unix` and the signed `validation_time_unix` and requires that
authority to remain continuously valid throughout the inclusive interval; a
revocation followed by reauthorization does not bridge the gap. The mutation
sink then performs the independent fresh admission-time authority check in
section 9.1. Stale, future-dated, revoked-at-signature, differently controlled,
or differently profiled evidence is rejected. This
object proves only the current disclosed controller-root relationship for this
Agreement and collateral obligation. It is neither collateral allocation
evidence nor a substitute for the control-resolution and Guarantor-control-
deletion proof required by `independently-enforceable`.

The operational binding digest is exactly:

```text
stage_action_authority_binding_digest = Digest(
  "tos.service.agent-guarantor-stage-action-authority-binding.v1",
  stage_action_authority_binding)
```

The binding is immutable for one coverage Agreement version. Changing any
stage, identifier, authority, quorum, fence domain, high-water, resolver, or
admission domain requires a new coverage terms and Agreement version before
any affected side effect. Runtime failover changes only the current generation
inside a bound fence domain; it does not rewrite the binding.

`amount_atomic` is a canonical unsigned base-10 integer. Leading zeroes are
forbidden except for exact zero where a field permits it. Asset identity,
network domain, wrapper or token contract identity, unit, decimals profile,
and any memo or tag that changes the beneficiary must be committed by the
selected Adapter.

Every `Authorized*V1` envelope carries a canonical
`authorizations[]` set of `ProfileQualifiedObjectAuthorizationV1`. The owning
body, accepted Agreement, or referenced service profile freezes the eligible
subject, profile URI/version/digest, scope, quorum, and validation-time rule
before evidence is attached. The envelope cannot select a weaker profile after
the body digest exists. `authorized_object_kind` and `authorized_body_digest`
MUST equal the containing envelope's released kind and recomputed canonical
body digest. Native Agent authorization uses the corresponding
object-specific signature domain in section 9 and embeds
`NativeEd25519AgentAuthorizationEvidenceV1`; contract, wallet, custody, quorum,
or other profiles embed their released evidence instead.

Authorization elements sort by complete canonical encoded bytes and reject
duplicate subjects, duplicated quorum domains, conflicting bytes under one
profile evidence identity, missing required subjects, and extraneous evidence.
The complete envelope digest covers the set. Thus native Ed25519 signatures and
non-Ed25519 Adapter evidence have one tagged wire boundary without treating a
public key as self-authorizing.

`CanonicalGuarantorEvidenceSetV1.items[]` is sorted by content type, profile
digest, then envelope digest, and rejects duplicates. Its digest uses
`tos.service.agent-guarantor-evidence-set.v1`. The `purpose` and `context_digest` bind
the set to one fee prerequisite, claim payout, collateral transition, terminal
claim cut, or resolution; the same evidence cannot be reinterpreted under a
different purpose. A set commitment never proves its members by itself: the
containing envelope carries the exact bounded objects or immutable
content-addressed descriptors, and the verifier resolves and verifies every
member before relying on the set digest.

Exactly one of `canonical_envelope_bytes` and `immutable_descriptor` is
present according to `representation`. Inline bytes MUST be the exact bounded
canonical envelope whose released complete-envelope digest equals
`evidence_envelope_digest`. A content-addressed descriptor MUST reproduce that
same content type, digest, and exact size after retrieval under its fixed
policy. Bare digests, mutable locators, or Provider-private database keys are
invalid evidence carriage.

Policy references bind immutable bytes. Human-readable policy text may explain
terms, but any clause that changes authority, eligibility, amount, asset,
deadline, evidence, decision, destination, cancellation, or payout must also
have a canonical machine field or profile digest.

### 10.1 Closure-capacity invariant

V1 deliberately emits one portable `AuthorizedTerminalClaimSetEvidenceV1`
and then carries that object once through exposure release and final coverage
resolution. An Agreement must therefore prove before authorization that every
history it permits fits not only the terminal envelope but every mandatory
downstream wrapper. `ClaimClosureCapacityV1` is not a usage estimate. It is a
canonical ex-ante bound selected in the coverage terms, bounded by the signed
claim-profile entry and the request, and recomputed by every verifier.
`maximum_claims` is byte-for-byte equal to the coverage terms' top-level value.
Each of the fourteen closure-path ceilings in the selected
`GuarantorClaimProfileV1` is positive and is an upper bound on the
byte-identically named ceiling in `ClaimClosureCapacityV1`:
`maximum_admitted_claim_envelope_bytes`,
`maximum_claim_ingress_receipt_envelope_bytes`,
`maximum_claim_ingress_cut_proof_bytes`,
`maximum_acceptance_request_envelope_bytes`,
`maximum_acceptance_receipt_envelope_bytes`,
`maximum_activation_evidence_envelope_bytes`,
`maximum_non_activation_evidence_envelope_bytes`,
`maximum_cancellation_receipt_envelope_bytes`,
`maximum_claim_filing_close_receipt_envelope_bytes`,
`maximum_terminal_claim_set_envelope_bytes`,
`maximum_exposure_release_request_bytes`,
`maximum_exposure_release_receipt_bytes`,
`maximum_coverage_resolution_request_bytes`, and
`maximum_coverage_resolution_envelope_bytes`. A missing profile field, a
capacity field greater than its corresponding profile field, or comparison
against a differently named or locally inferred limit is invalid before offer
reservation.
Every maximum count except the two negotiated round maxima is a positive
checked integer; either round maximum may be zero. Remaining-capacity entries
may reach zero only in a terminal profile state. Each complete-object, ingress-
cut, or request ceiling is no more than 1,048,576 canonical bytes.
Checked multiplication requires `maximum_claim_ingress_actions >=
maximum_claims * maximum_claim_revisions_per_claim`, so every valid maximum
history has an ingress slot before any allowance for terminally rejected
attempts.

The released schema publishes an exact numeric maximum-canonical-CBOR-size
table for every component embedded by section 19.6. The normative computation
constructs the complete maximum-size, semantically valid
`AuthorizedTerminalClaimSetEvidenceV1`, canonically encodes it, and measures
the resulting byte string:

```text
maximum_acceptance_request_envelope =
  BuildMaximumAuthorizedCoverageAcceptanceRequestV1(
    exact selected service-profile artifact,
    exact firm offer and Agreement authorization set,
    maximum_profile_permitted_acceptance_authorizations)

maximum_acceptance_receipt_envelope =
  BuildMaximumAuthorizedCoverageAcceptanceReceiptV1(
    maximum_acceptance_request_envelope,
    maximum_profile_permitted_acceptance_receipt_authorizations)

maximum_activation_evidence_envelope =
  BuildMaximumAuthorizedCoverageActivationEvidenceV1(
    maximum_acceptance_receipt_envelope,
    maximum_profile_permitted_activation_prerequisite_evidence,
    maximum_stage_action_admission_evidence,
    maximum_profile_permitted_activation_authorizations)

maximum_non_activation_evidence_envelope =
  BuildMaximumAuthorizedCoverageNonActivationEvidenceV1(
    maximum_acceptance_receipt_envelope,
    maximum_profile_permitted_activation_cut,
    maximum_profile_permitted_non_activation_evidence,
    maximum_stage_action_admission_evidence,
    maximum_profile_permitted_non_activation_authorizations)

maximum_cancellation_receipt_envelope =
  BuildMaximumAuthorizedCoverageCancellationReceiptV1(
    maximum_profile_permitted_cancellation_request,
    maximum_stage_action_admission_evidence,
    maximum_profile_permitted_cancellation_authorizations)

maximum_claim_filing_close_receipt_envelope = max_encoded_size(
  BuildMaximumAuthorizedClaimFilingCloseReceiptV1(
    branch = normal,
    maximum_activation_evidence_envelope,
    maximum_cancellation_receipt_envelope,
    maximum_claim_ingress_cut_proof_bytes,
    maximum_stage_action_admission_evidence),
  BuildMaximumAuthorizedClaimFilingCloseReceiptV1(
    branch = never_activated,
    maximum_non_activation_evidence_envelope,
    maximum_claim_ingress_cut_proof_bytes,
    maximum_stage_action_admission_evidence))

computed_worst_case_acceptance_request_envelope_bytes =
  len(canonical_cbor(maximum_acceptance_request_envelope))
computed_worst_case_acceptance_receipt_envelope_bytes =
  len(canonical_cbor(maximum_acceptance_receipt_envelope))
computed_worst_case_activation_evidence_envelope_bytes =
  len(canonical_cbor(maximum_activation_evidence_envelope))
computed_worst_case_non_activation_evidence_envelope_bytes =
  len(canonical_cbor(maximum_non_activation_evidence_envelope))
computed_worst_case_cancellation_receipt_envelope_bytes =
  len(canonical_cbor(maximum_cancellation_receipt_envelope))
computed_worst_case_claim_filing_close_receipt_envelope_bytes =
  len(canonical_cbor(maximum_claim_filing_close_receipt_envelope))

per_claim_history_elements_max =
    fixed ClaimTerminalResolutionBundleV1 overhead excluding resolution_ref
  + maximum_claim_revisions_per_claim
      * max ClaimAdmissionReceiptProofV1 size, including the exact ingress
        receipt and immutable complete-receipt descriptor
  + maximum_decision_admissions_per_claim
      * max ClaimDecisionAdmissionReceiptProofV1 size
  + maximum_claim_state_transitions_per_claim
      * max AuthorizedClaimStateTransitionReceiptV1 size
  + max AuthorizedClaimDecisionV1 size
  + max DecisionApplicationReceiptProofV1 size
  + max MaterializedPayoutObligationSetV1 size at
      maximum_payout_lines_per_claim
  + max terminal payout-evidence-set size at
      maximum_payout_lines_per_claim

maximum_terminal_claim_set_envelope =
  BuildMaximumAuthorizedTerminalClaimSetEvidenceV1(
    maximum_claim_filing_close_receipt_envelope,
    maximum_claims,
    maximum_claim_ingress_actions,
    maximum_claim_revisions_per_claim,
    maximum_decision_admissions_per_claim,
    maximum_claim_state_transitions_per_claim,
    maximum_payout_lines_per_claim,
    maximum_admitted_claim_envelope_bytes,
    maximum_claim_ingress_receipt_envelope_bytes,
    maximum_claim_ingress_cut_proof_bytes,
    maximum_stage_action_admission_evidence)

computed_worst_case_terminal_claim_set_bytes =
  len(canonical_cbor(maximum_terminal_claim_set_envelope))

maximum_terminal_payout_index =
  BuildMaximumCoverageTerminalPayoutEvidenceSetV1(
    maximum_terminal_claim_set_envelope)

maximum_exposure_release_request =
  BuildMaximumExposureReleaseActionBodyV1(
    maximum_terminal_claim_set_envelope,
    maximum_terminal_payout_index,
    maximum_profile_permitted_collateral_disposition,
    maximum_profile_permitted_authorization_context)

maximum_exposure_release_receipt =
  BuildMaximumAuthorizedExposureReleaseReceiptV1(
    maximum_terminal_claim_set_envelope,
    maximum_terminal_payout_index,
    maximum_profile_permitted_collateral_disposition,
    maximum_profile_permitted_release_authorizations,
    maximum_stage_action_admission_evidence)

maximum_coverage_resolution_request =
  BuildMaximumCoverageResolutionActionBodyV1(
    maximum_exposure_release_receipt)

maximum_coverage_resolution_envelope =
  BuildMaximumAuthorizedCoverageResolutionV1(
    maximum_exposure_release_receipt,
    maximum_profile_permitted_resolution_authorizations,
    maximum_stage_action_admission_evidence)

computed_worst_case_exposure_release_request_bytes =
  len(canonical_cbor(maximum_exposure_release_request))
computed_worst_case_exposure_release_receipt_bytes =
  len(canonical_cbor(maximum_exposure_release_receipt))
computed_worst_case_coverage_resolution_request_bytes =
  len(canonical_cbor(maximum_coverage_resolution_request))
computed_worst_case_coverage_resolution_envelope_bytes =
  len(canonical_cbor(maximum_coverage_resolution_envelope))
```

These builders start from the exact selected service-profile lineage, firm
offer, Agreement bytes, authorization-profile cardinalities, evidence limits,
and stage-operation request ceilings known before issuance. Every stage result
is measured with its complete `PortableStageActionAdmissionEvidenceV1`,
including the duplicated canonical request bytes where the result also embeds
objects carried by that request. The filing-close maximum is the greater of the
largest semantically valid normal branch (activation plus optional accepted
cancellation) and never-activated branch; an impossible mixture is not counted
as though it were valid. The terminal builder embeds that complete maximum
filing-close receipt, and every later builder embeds its actual predecessor
wrapper at every canonical path. Thus an inner object being under 1 MiB is
never, by itself, proof that its mandatory parent is encodable.

For a profile that permits collateral-backed payout, the “max terminal payout-
evidence-set” term physically includes, for every maximum-size line, the exact
generic `AgreementPaymentEvidenceV1`, its
`CollateralPayoutPaymentEvidenceProjectionV1`, and the complete matching
`AuthorizedCollateralEvidenceV1` carried as the second evidence-set item. The
builder also includes the composite request/result component references at
their actual nested paths. Counting only one side of the atomic payout, or only
the collateral-envelope digest, is invalid.

The builder serializes three byte-identical copies of
`ClaimTerminalResolutionRefV1` per claim: one inside the bundle, one in
`TerminalClaimSetBodyV1.claim_resolutions[]`, and one in
`ClaimTerminalResolutionRefSetV1.refs[]`. An equivalent audit decomposition is
`maximum_claims * (3 * max_ref_size + per_claim_history_elements_max)`, plus
the exact enclosing maps, arrays, evidence, and authorization objects. That
decomposition is explanatory only; the full-object measurement is normative.
Omitting or changing any of the three copies is a conformance failure.

The builders account for each canonical map key and each aggregate array header
exactly once at its actual maximum length, including the header changes at 24,
256, and larger canonical-CBOR boundaries. Per-element size constants exclude
their enclosing aggregate-array headers. Bounded authorizations, recursively
embedded objects, and wrapper overhead are measured as physically serialized;
declared payload sizes or compressed sizes are never substituted. The schema
release gate must turn every symbolic `max` above into fixed generated objects
and integers and publish boundary vectors. The aggregate payout index carries
only the per-bundle payout-set digests defined in section 16.2; it never repeats
the full payout sets already inside the terminal bundles. The release receipt
then carries the terminal envelope and index once, and each resolution wrapper
carries that release receipt once.

The generated maximum ingress receipt physically contains one maximum admitted
claim envelope plus its receipt body, fresh eligibility-proof set, and receipt
authorization quorum. The maximum filing-close receipt physically contains one
`ClaimIngressAdmissionCutProofV1` with up to
`maximum_claim_ingress_actions` contiguous entries. Those bytes are then
counted once at every actual nested path through the terminal set and downstream
wrappers. Every maximum stage result contains its exact maximum-size
`PortableStageActionAdmissionEvidenceV1`, including canonical request,
`AuthorizedActionV1`, and `WriterFenceV1`. Each compact receipt proof counts its
full projected body, authorization quorum, stage-authority seal, and immutable
descriptor at its actual path; the descriptor's declared complete-receipt size
is also checked against the corresponding negotiated ceiling. A calculator
that omits a proof field, counts only the claim, or treats an unsigned digest as
a receipt is invalid.

Every recomputed integer must equal its corresponding
`computed_worst_case_*_bytes` field and be no larger than its corresponding
`maximum_*_bytes` field or the global 1 MiB ceiling. The accepted terminal-set
ceiling is therefore no greater than the smallest residual capacity left by
the terminal envelope, exposure-release request, exposure-release receipt,
coverage-resolution request, and coverage-resolution envelope builders after
their other maximum permitted fields and authorizations are serialized. This
minimum is calculated by constructing the complete objects, not by subtracting
estimated overhead. A profile, request, offer, or Agreement for which any one
inequality fails is invalid before exposure is reserved. Consequently a
history that remains within all admitted count and size slots cannot become
unreleasable merely because an outer wrapper has no remaining bytes.

The counts include terminal records. The exact
`continuation_budget_profile` deterministically derives one canonical entry for
every reachable cross-product of claim state, decision-log state, challenge
state, and remaining profile cycle count. Each entry states the decision and
transition slots that must remain reserved to preserve every
continuation still permitted by the Agreement, the maximum decision-path
duration to reach a terminal claim, and the maximum total duration through
payout and Adapter recovery. These reserved-slot values are therefore the
maximum record consumption of the remaining permitted paths, not the shortest
fallback path. The supplied entry set must equal that derived complete state
table; an omitted state, duplicate key, caller-reduced reserve, or caller-
shortened duration is invalid.

At minimum, the generated table reserves these records, where `r` is the
number of challenge admissions still permitted and `n` is the number of
nonterminal response rounds still permitted. Durable receipts store the
monotonically increasing used counters; `r` and `n` are derived by checked
subtraction from the Agreement maxima and therefore decrease monotonically. A
selected profile with extra states may reserve more, never less:

| Target profile state | Required spare decision slots | Required spare transition slots |
| --- | ---: | ---: |
| initial reviewing before any decision `(r,n)` | `1 + n + r` | `n + r + 1` |
| challengeable candidate `(r)` | `r` | `r + 1` |
| reviewing after challenge admission `(r)` | `r + 1` | `r + 1` |
| `evidence_required` or `disputed` `(r,n)`, `n > 0` | `n + r` | `n + r + 1` |
| reviewing after nonterminal response `(r,n)` | `n + r + 1` | `n + r + 1` |
| terminal close admitted | `0` | `0` |

One exercised challenge round is exactly one `challenge_admission` transition
followed by one successor decision. A post-challenge successor is restricted
in V1 to `approved`, `partially_approved`, or `denied`; only its final
unchallenged candidate receives one `challenge_close` transition. One
nonterminal round is either (a) one `nonterminal_response_admission` transition
followed by a successor decision or (b) one deterministic terminal-fallback
decision admitted directly at the response deadline. The fallback is a
decision admission, not a state-transition receipt, and its result must be a
challengeable candidate; it cannot recursively return `evidence_required` or
`disputed`. The final `+1` in every applicable transition count is the
challenge close.

There is deliberately no reachable `evidence_required` or `disputed` entry
with `n = 0`. Admission of either result requires at least one remaining
nonterminal round in the same CAS. The round may then be consumed by a
response transition plus successor or by the direct deterministic fallback.
This rule also applies to an initial decision;
`maximum_nonterminal_rounds_per_claim = 0` therefore permits only a
challengeable candidate as decision sequence 1.

Each round is counted from the complete portable decision and transition logs;
it cannot be reset by a revision, takeover, or restored journal. Unknown or
ambiguous admission preserves the predecessor's entire continuation budget and
blocks another semantic admission until resolution. Array-header growth at
canonical-CBOR boundaries and recursive copies embedded by receipts are part
of the generated maximum object, not assumed constant overhead.

For the base V1 profile, let `I` be the accepted initial-review duration, `C`
the accepted challenge duration, `N` the accepted nonterminal-resolution
duration, and `S` the accepted post-challenge successor-decision duration. A
nonterminal response transition inherits the existing absolute response
deadline; it does not start another `N`. The generated state table uses these
checked upper bounds before adding the accepted payout and Adapter-recovery
windows:

```text
initial_reviewing(r, n) = I + n * N + (r + 1) * C + r * S
challengeable_candidate(r) = (r + 1) * C + r * S
reviewing_after_challenge(r) = S + (r + 1) * C + r * S
evidence_required_or_disputed(r, n) = n * N + (r + 1) * C + r * S
reviewing_after_nonterminal_response(r, n) =
    (n + 1) * N + (r + 1) * C + r * S
```

The last row uses `N` as the canonical ex-ante upper bound for the already
running response window. At runtime the inherited receipt cutoff supplies the
actual, never-later successor deadline; it does not change the signed table or
create fresh time.

The selected continuation profile may define stricter processing bounds but
cannot omit a reachable state or shorten this base requirement. Checked
subtraction from `terminal_resolution_deadline_unix` yields the exact latest
admission time for each state/round pair; underflow invalidates the proposed
coverage terms.

Before admitting a claim revision, decision, challenge, evidence response,
dispute, timeout fallback, state transition, or payout materialization, the
same CAS computes the target profile state. After charging the proposed record,
the unused decision and transition slots must be at least that target state's
two required reserves, and checked addition must prove:

```text
admitted_at_unix
  + target_state.maximum_remaining_closure_seconds
  <= terminal_resolution_deadline_unix
  <= coverage_agreement.expires_at
```

This time inequality governs normal-case admission. The exact
`late_recovery_terminal_fallback` branch is exempt only from the ordinary
deadline. Its filing close and fallback admission must be no later than the
Agreement-derived `late_ingress_recovery_deadline_unix`, and its complete
continuation, payout, and Adapter-recovery path must be no later than
`late_recovery_terminal_deadline_unix`. It still consumes the pre-reserved
count/byte continuation entry, uses the frozen benefit and aggregate rules, and
follows every state CAS. If a
settlement or collateral resource has expired or become unavailable by then,
the selected Adapter must emit its exact terminal default/impaired evidence so
the claim and coverage can still close; absence or timeout is not fabricated as
payment.

A challengeable approval, partial approval, or denial therefore cannot consume
the last successor-decision slot. Challenge admission retains the slots for its
successor decision and terminal close. A nonterminal evidence or dispute step
retains either its response transition plus successor decision or its direct
terminal-fallback decision, followed by the final challenge-close path. The
rule also produces backward-derived latest-admission
cutoffs: a claim revision or nonterminal action arriving too late is rejected
before it can invalidate the already closable head.

The exact `terminal_fallback` object is mandatory. It is selected from the
signed claim profile, bound byte-for-byte by the Agreement, and exhaustively
maps initial reviewing, `evidence_required`, `disputed`, and both reviewing
branches to their admitted cutoff sources. Its outcome rule is either canonical
zero denial or the accepted benefit-calculation profile applied to the current
portable claim/evidence history. Only the accepted-benefit branch applies the
mandatory aggregate-cap projection using the exact current coverage-state
revision; the accepted payout
template derives every payout line. No caller, model, signer, or runtime may
choose another result, amount, evidence cut, cap snapshot, or line.

`deny_zero` always derives `result = denied`, canonical zero approved amount,
no payout lines, `aggregate_cap_projection_rule =
not_applicable_deny_zero`, and no aggregate projection. Its policy application
uses canonical zero `full_eligible_benefit_amount` and the canonical empty byte
string for `policy_input_projection`; these values mean “benefit calculation
deliberately not evaluated by the Agreement's forced-denial rule,” not a claim
that compensable loss was zero. `accepted_benefit_calculation` requires
`aggregate_cap_projection_rule = remaining-aggregate-min.v1` and is a released total
function over the exact current authorized claim and complete admitted
evidence/revision cut under the Agreement's benefit profile and per-claim caps.
It first returns `gross_fallback_amount`. The closed V1
`remaining-aggregate-min.v1` projection is then evaluated inside the same
decision-admission CAS:

```text
reclaimable_prior_amount =
  prior_pending_application_token.reserved_approved_amount
  if that exact token belongs to this claim and is replaced by this admission
  else 0

remaining_aggregate_capacity =
  maximum_aggregate_payout
  - cumulative_applied_approved_amount
  - aggregate_pending_decision_reserve_before
  + reclaimable_prior_amount

fallback_approved_amount =
  min(gross_fallback_amount, remaining_aggregate_capacity)
```

All arithmetic is checked in the coverage asset and is derived from the exact
rollback-resistant state read by the admission authority in its linearized
transaction; the fallback request names no coverage revision or aggregate
operand. Zero `fallback_approved_amount` derives `denied`; a
positive value equal to the full eligible claim derives `approved`; every
other positive value derives `partially_approved`. The reason and policy-application
digests commit whether aggregate exhaustion constrained the result. Thus an
already exhausted aggregate cap deterministically closes a later valid claim
as a challengeable zero denial instead of leaving it inadmissible. The payout
template deterministically partitions the final amount. Invalid or
unavailable input that claim admission was required to reject cannot be
introduced later. Every selectable benefit, aggregate, and line-derivation
profile is a released total function over schema-bounded operands, and
Agreement validation proves every checked arithmetic bound. A profile with a
reachable error, unknown value, unavailable input, overflow, optional external
lookup, partial function, or implementation-local error branch is invalid
before Agreement authorization. A worker crash or faulty implementation emits
no alternate decision or `deny_zero`; recovery resolves the same stable action
and another conforming executor derives the one specified output. `deny_zero`
is used only when it is the Agreement's selected `outcome_rule`.

`reason_rules[]` is sorted by the five `outcome_case` ordinals and contains
exactly one row for each case, even when `outcome_rule = deny_zero` makes four
rows unreachable. Each reason code exists exactly once in the Agreement-
selected decision-profile registry for its row's result; each clause ID exists
exactly once in the accepted Agreement. Runtime derivation selects one row:

```text
deny_zero                    -> deny_zero
gross_fallback_amount = 0    -> no_eligible_benefit
gross_fallback_amount > 0 and remaining_aggregate_capacity = 0
                             -> aggregate_exhausted
0 < fallback_approved_amount < gross_fallback_amount
                             -> aggregate_limited
fallback_approved_amount = gross_fallback_amount > 0
                             -> full_benefit
```

The selected row fixes `ClaimDecisionReasonV1.reason_code` and
`applicable_policy_clause_ids[]` byte-for-byte. Its result equals both the
reason object and `ClaimDecisionBodyV1.result`.
`ClaimDecisionPolicyApplicationV1.applicable_policy_clause_ids[]` equals that
same row exactly for a fallback; it cannot add another otherwise valid clause.
For `accepted_benefit_calculation`, the selected total benefit profile derives
one canonical `policy_input_projection`, full eligible amount, and evidence-set
digest from the frozen portable history. For `deny_zero`, their exact special
values are the empty/zero form above. Thus the fallback authority supplies no
free policy byte, clause membership, or eligibility operand.
`evidence_predicate_ids[]` is the sorted unique set of every predicate ID from
the exact `decision_evidence_set` used by the policy application—empty only
when that set has no predicates. No authority, caller, or codec may choose a
subset, alternate registered reason, or different clause list for an otherwise
identical fallback state.

Both arrays are canonical sets. Every released source state occurs exactly once
in each. The only V1 mappings are `initial_reviewing -> claim_review_cutoff`,
`evidence_required -> resolution_due_at_unix`, `disputed ->
resolution_due_at_unix`, and each reviewing branch ->
`successor_decision_due_at_unix`; a missing, duplicate, overlapping, unknown,
or different mapping invalidates the claim profile.

`authorization_mode = agreement_granted_deterministic_admission` means the
Agreement grants the bound admission authority an irrevocable, purpose-limited
capability to materialize and admit those exact bytes when the trigger proof is
valid. Any Agreement-authorized claimant or beneficiary may invoke that route;
it requires no new discretionary Guarantor signature after Agreement
authorization. Elapsed time alone is never terminal evidence: the request
embeds the current portable state and admitted cutoff proof, and the fallback
decision still passes ordinary decision admission, aggregate-cap CAS, challenge
close, payout, and recovery. For `independently-enforceable`, its quorum,
Action Authority, Writer Fence, resolver, and direct route pass the Guarantor-
control-deletion test. A profile without a deterministic terminal fallback is
not a valid Guarantor V1 claim profile.

Claim admission rejects an envelope over
`maximum_admitted_claim_envelope_bytes`; claim revision, decision, transition,
and payout materialization reject their next item before admission when its
count, continuation, time, or encoded-size bound would be exceeded. A rejected
or duplicate action consumes no slot; an admitted ambiguous action retains its
slot until exact resolution. These checks and the corresponding log revision
advance occur in one CAS. Consequently every valid history admitted under the
Agreement has both encoding and continuation capacity. V1 has no paging
fallback and never drops, summarizes, or fetches an admitted record from
mutable state to fit the limit; a future paged format requires a new profile
version.

## 11. Service profile

```text
CollateralTransitionProfileV1 {
  transition_kind
  successor_derivation_profile       # exact deterministic sink-side profile
  adapter_profile
  adapter_request_content_type
  adapter_request_profile
  maximum_adapter_request_bytes
  adapter_evidence_content_type
  adapter_evidence_profile
  authorization_subject_source       # custodian or independent_execution_quorum
  custodian_authorization_binding?    # exact CollateralAuthorizationBindingV1
  permitted_prior_states[]
  permitted_resulting_states[]
  prerequisite_evidence_roles[]
  authorized_claim_decision_binding   # forbidden or terminal_decision_required
  payout_destination_binding          # forbidden or agreement_destination_required
}

CollateralAuthorizationBindingV1 {
  authorization_profile             # exact ProfileRefV1
  authorization_subjects[]          # nonempty canonical set
  authorization_quorum_rule
}

CollateralTransitionBindingV1 {
  transition_profile_digest
  transition_profile                  # exact CollateralTransitionProfileV1
  authorization_binding               # exact CollateralAuthorizationBindingV1
}

GuarantorCollateralProfileV1 {
  profile_id
  profile_version
  predecessor_profile_digest?
  assurance_level
  asset
  custody_adapter_profile
  collateral_control_disclosure      # exact CollateralControlDisclosureV1
  transition_profiles[]               # exact CollateralTransitionProfileV1 set
  independent_execution_profile?
  independent_execution_authority_subjects[]
  independent_execution_quorum_rule?
  compatible_claim_profile_digests[]
  exclusive_allocation_required
  minimum_collateralization_ppm
  maximum_evidence_age_seconds
}

GuarantorClaimProfileV1 {
  profile_id
  profile_version
  predecessor_profile_digest?
  trigger_profile
  evidence_profile
  claimant_authorization_profiles[]
  ingress_profile
  ingress_authority_subjects[]
  ingress_authority_quorum_rule
  admission_profile
  admission_authority_subjects[]
  admission_quorum_rule
  independent_claim_operation_profile?
  decision_admission_profile
  decision_admission_authority_subjects[]
  decision_admission_quorum_rule
  decision_profile
  dispute_profile?
  maximum_claims
  maximum_claim_ingress_actions
  maximum_claim_revisions_per_claim
  maximum_decision_admissions_per_claim
  maximum_claim_state_transitions_per_claim
  maximum_challenge_rounds_per_claim
  maximum_nonterminal_rounds_per_claim
  maximum_payout_lines_per_claim
  maximum_admitted_claim_envelope_bytes
  maximum_claim_ingress_receipt_envelope_bytes
  maximum_claim_ingress_cut_proof_bytes
  maximum_acceptance_request_envelope_bytes
  maximum_acceptance_receipt_envelope_bytes
  maximum_activation_evidence_envelope_bytes
  maximum_non_activation_evidence_envelope_bytes
  maximum_cancellation_receipt_envelope_bytes
  maximum_claim_filing_close_receipt_envelope_bytes
  maximum_terminal_claim_set_envelope_bytes
  maximum_exposure_release_request_bytes
  maximum_exposure_release_receipt_bytes
  maximum_coverage_resolution_request_bytes
  maximum_coverage_resolution_envelope_bytes
  continuation_budget_profile
  permitted_terminal_fallbacks[]          # exact DeterministicClaimTerminalFallbackV1 set
  maximum_evidence_items
  maximum_evidence_bytes
  review_deadline_seconds
  maximum_nonterminal_resolution_window_seconds
  maximum_successor_decision_window_seconds
  maximum_claim_ingress_resolution_grace_seconds
  maximum_late_ingress_recovery_window_seconds
  payout_deadline_seconds
}

GuarantorServiceProfileV1 {
  schema_version
  profile_id
  revision
  predecessor_profile_digest?
  provider_agent_id
  authority_domain_digest
  coverage_capabilities[] {
    category
    benefit_kinds[]                 # fixed_benefit or indemnity
    supported_underlying_profiles[]
    supported_claim_profiles[]
    supported_assets[]
    coverage_ranges[]
    fee_ranges[]
    maximum_coverage_seconds
    maximum_claim_window_seconds
    jurisdiction_policy
  }
  collateral_profiles[]              # exact GuarantorCollateralProfileV1 values
  claim_profiles[]                   # exact GuarantorClaimProfileV1 values
  payout_adapter_profiles[]
  admission_limits {
    maximum_quote_reservations
    maximum_active_coverages
    maximum_active_claims
    maximum_active_per_covered_party
    maximum_activation_attempts_per_coverage
    maximum_quote_requests_per_window
    quote_request_window_seconds
    maximum_acceptance_processing_grace_seconds
  }
  endpoints {
    quote_route
    acceptance_route
    claim_route
    resolve_route
    evidence_route
  }
  exposure_authority_id
  exposure_authorization_profile
  lifecycle_authority_id
  lifecycle_authorization_profile
  policy_revision
  created_at_unix
  expires_at_unix
  required_extensions[]
  optional_extensions[]
}

GuarantorServiceProfileRevisionArtifactV1 {
  schema_version
  service_intent_operation_digest
  service_intent_operation           # exact signed AgentOperationEnvelopeV1
  intent_payload                     # exact AgentIntentPayloadV1
  service_profile                    # exact GuarantorServiceProfileV1
}

GuarantorServiceProfileArtifactV1 {
  schema_version
  selected_service_intent_operation_digest
  selected_service_profile_digest
  revisions[]                        # complete oldest-to-selected lineage; 1..64,
                                     # cumulatively no more than 512 KiB
}
```

For this profile, the Intent detail descriptor's content type identifies the
canonical `GuarantorServiceProfileV1` bytes directly. Each revision artifact
recomputes the root operation digest and authorization, Intent payload digest,
detail descriptor content digest and size, and service-profile digest. All
links must match. `revisions[]` is bounded, contiguous, and starts at the
profile's version 1; every later operation and profile names the exact previous
digests, issuer, profile ID, and authority domain. The selected digests equal
the final array entry. Gaps, forks, duplicate revisions, Carrier metadata, and
a predecessor available only by locator fail closed. The artifact is not a new
authority wrapper; it retains the original signed publication lineage and exact
authenticated detail bytes so verification does not depend on a Carrier or
mutable Provider endpoint. Before a next revision would exceed either 64
entries or the 512 KiB canonical artifact limit, the Provider must publish a
new profile ID and Intent. A revision that crosses either bound is not a
selectable continuation and cannot issue a firm offer. The lineage selected by
an existing firm offer is never truncated. The 512 KiB cap leaves at least 512
KiB inside the 1 MiB complete-object ceiling for the offer, exposure receipt,
authorizations, and wrapper overhead; every complete wrapper must still satisfy
its own stricter encoded-size bound. The cap is exactly
`len(canonical_cbor(GuarantorServiceProfileArtifactV1))`, including array and
object overhead—not a sum of declared detail sizes. Compression, a locator, or
omitting an earlier revision cannot change the measured object.
Its canonical digest uses
`tos.service.agent-guarantor-service-profile-artifact.v1`.

The 512 KiB lineage ceiling is an upper bound, not permission to create an
unusable offer. Before issuance, the authority uses the released maximum-size
table for the Agreement's authorization profiles to prove that the final firm
offer, single-carriage acceptance request, acceptance receipt, activation, and
non-activation wrappers can each remain below 1 MiB. It then executes the full
section 10.1 closure-capacity builders through filing close, terminal claim set,
exposure release, and coverage resolution; every computed value must equal the
request/offer terms and fit both its claim-profile ceiling and every containing
wrapper. This is a hard pre-reservation and pre-signature condition, not a
deployment test. A smaller effective lineage limit is derived when any later
mandatory wrapper or other required evidence needs more space. The
same complete offer or Agreement-evidence set is never embedded twice in one
wrapper merely to satisfy two projection roles.

Each nested profile has a canonical identity independent of array position:

```text
collateral_profile_digest = Digest(
  "tos.service.agent-guarantor-collateral-profile.v1",
  exact GuarantorCollateralProfileV1)

claim_profile_digest = Digest(
  "tos.service.agent-guarantor-claim-profile.v1",
  exact GuarantorClaimProfileV1)
```

The arrays sort by those digests and reject duplicate IDs, digests, or
conflicting versions. `profile_version` is a checked positive `u64`. Version 1
has no predecessor. For version `n > 1`, `predecessor_profile_digest` is
required and resolves to the exact version `n - 1` entry in the authenticated
predecessor service-profile lineage with the same `provider_agent_id`,
`authority_domain_digest`, and `profile_id`. An entry cannot cite a Carrier
copy, unrelated service profile, fork, skipped version, or same-version body.
Every request and accepted terms object selects a profile by its exact digest,
not by array index, display name, or an unversioned URI. The verifier locates
exactly one matching entry in the signed service profile and applies every
limit and external `ProfileRefV1` in that entry. No match or multiple matches
fails closed.

`coverage_capabilities[].supported_claim_profiles[]` lists external claim-
semantics `ProfileRefV1` values for coarse discovery. It is not a selector for
the nested `claim_profiles[]` entries. Selection always uses
`selected_claim_profile_digest`; the chosen entry's trigger, evidence,
admission, and decision references must also be compatible with the advertised
capability.

For a `collateral-attested` entry, all three `independent_execution_*` fields
are absent or empty and `exclusive_allocation_required` is exactly true. Its
`minimum_collateralization_ppm` is a positive `u64` and may be below
`1_000_000`, but the resulting claimed allocation is still exclusive to one
Agreement-bound position and must meet that advertised ratio. For an
`independently-enforceable` entry, the profile is present, the subject set is
nonempty, the quorum rule is satisfiable, exclusive allocation is true, and
`minimum_collateralization_ppm >= 1_000_000`. An
`unsecured-signed` selection has no collateral-profile digest. These presence
rules are canonical; permissive decoding or silently inferred defaults are
invalid.

Every collateral entry carries one canonical control disclosure whose Adapter
profile equals `custody_adapter_profile`; its operator and controller sets are
sorted, duplicate-free, and nonempty where the declared relationship requires
them. `third_party_control_asserted` requires the control-resolution and
disclosure-evidence profiles, nonempty disclosure-authority subjects, a
satisfiable quorum, and a positive freshness limit. Other relationship
tokens forbid fields they do not use. `CollateralTermsV1` copies this object
byte-for-byte from the selected entry. A changed, omitted, stale, or locally
inferred disclosure invalidates activation; the disclosure itself never
satisfies the stronger control-deletion proof.

A claim-profile entry offered for `independently-enforceable` use also has a
present `independent_claim_operation_profile`. That profile defines a direct,
authenticated Adapter path for initial claim admission, revision admission,
the three closed V1 claim-state transitions, decision admission and
application, filing close, and terminal coverage closure without routing
through a Guarantor process. The operational terms separately bind a coverage-
operation Adapter for activation, non-activation resolution, and active-
coverage cancellation and final coverage resolution, an exposure-operation
Adapter for post-acceptance exposure release, plus the selected payout Adapter
for execution. The independent-execution fields are absent for entries that
make no such claim; the exact operation Adapter ProfileRefs and stage binding
in the coverage terms remain mandatory at every level and honestly identify
Provider-controlled lower-assurance routes. Compatibility
between a claim and collateral entry is explicit: the selected claim-profile
digest must occur exactly once in the selected collateral entry's canonical
`compatible_claim_profile_digests[]` set. Capability compatibility and the
selected assurance level must also verify. None of these relations is inferred
at runtime.

The coverage terms embed exactly one
`GuarantorStageActionAuthorityBindingV1`. Its digest is
`stage_action_authority_binding_digest`; a separately fetched or locally
selected binding is invalid. At independently enforceable assurance, the
operational-independence terms commit that exact digest. `stages[]` is sorted
by the released stage enum and contains
exactly one entry for each of the fourteen required stages, with no unknown or
duplicate stage. For an action at a bound stage, the registry's `owner_id` and
`agent_id` are exactly `action_owner_id` and `action_agent_id` from that entry;
the requester, transport, Guarantor, and takeover worker cannot choose or
derive alternatives. `AuthorizedActionV1` must name those same identifiers and
be admitted by the entry's Action Authority. Its `WriterFenceV1` must be issued
and checked in the named fence domain against the named rollback-resistant
generation high-water.

Guarantor V1 deliberately constrains each stage's action admission to the
already released `AuthorizedActionV1` authority model. No selectable
action-authorization or fence-authorization profile exists in this binding;
both authority-ID fields are byte-identical and equal, at admission time, to
the one `authority_id`, public key, and authorization proof carried by
`AuthorizedActionV1` and the same issuer/key carried by `WriterFenceV1`. A
contract, threshold group, quorum, separate action signer and fence issuer, or
profile-qualified non-Ed25519 proof cannot be projected into those scalar
fields in V1. Supporting one requires a separately versioned generic action
envelope and new Agreement, operation-binding, schema, registry, and exact-byte
vectors; it cannot be enabled by interpreting these fields differently.

The authority-control resolution proof expands every Guarantor control root
transitively and rejects a stage when its single action/Writer-Fence authority,
generation-high-water control, action-resolution control, or admission-state
control lies in that closure. It separately removes the closure from each
claim-operation, decision, collateral-execution, and payout evidence quorum.
Every remaining business-evidence quorum must still be satisfiable, and the
single action authority and every route must remain directly reachable and able
to resolve an ambiguous action without a Guarantor endpoint or credential.
Sharing one independent
Adapter domain across stages is allowed only when every stage entry names that
same immutable domain explicitly. An omitted binding, caller-selected owner,
Guarantor-issued fence, unfenced direct endpoint, or control-deletion failure
invalidates `independently-enforceable`.

This is a typed verifier contract, not a Boolean assertion. The selected
authority-control Adapter receives the exact profile, stage, stage-authority
binding, operation-Adapter profile, Guarantor control-root set, finalized state
root and revision, observation time, and finality evidence. It returns one
`AuthorityControlResolutionResultV1` containing the stage, exact binding
digest, exact operation-Adapter profile, finalized root and revision, sorted
transitive-controller closure, and these seven affirmative deletion tests:
Guarantor roots deleted; action authority, Writer Fence, generation high-water,
action resolver, admission domain, and operation route each survived deletion.
Every returned field is compared to the Agreement-bound input. A missing typed
verifier, opaque signed statement, mismatched closure, remaining direct or
transitive Guarantor controller, or any false survival result fails closed.

Presence of fourteen stage entries is not sufficient. Every
`GuarantorStageActionAuthorityV1` embeds one exact
`GuarantorStageOperationBindingV1`; its digest is
`Digest("tos.service.agent-guarantor-stage-operation-binding.v1",
operation_binding)`, equals `operation_binding_digest`, and its `stage` equals
the containing entry. Each binding is byte-for-byte equal to the applicable row
below after resolving the Agreement-selected profile and payout request form.
Every operation also returns one generic `ActionResolutionV1`; the result column
lists the additional exact result component. The sink derives the stage from
the canonical request and current predecessor state. A caller-supplied stage,
route, result type, or CAS domain is ignored and causes a conflict when carried
as a disagreeing duplicate.

For every Guarantor-specific row, `operation_registry_profile` is this exact
`ProfileRefV1`:

```text
profile_uri:
  tos.service.agent-guarantor-mutation-verifier-registry.v1
profile_version:
  1
profile_digest:
  Digest(
    "tos.service.agent-guarantor-mutation-verifier-registry.v1",
    canonical GuarantorMutationVerifierRegistryV1)
```

The ProfileRef already commits registry version and bytes; a duplicate version
or digest field is forbidden. `operation_id`, all handler-profile fields,
`result_components[]`, and the canonical empty `required_context_types[]` are
copied byte-for-byte from the matching immutable section 23.2 entry. The
Semantic Action registry and entry versions are both 1. Each payout stage uses
the Guarantor mutation-registry operation matching its Agreement-selected
direct, external, or collateral-backed request form, while its `action_kind`
and semantic fields resolve the exact released generic payment or settlement
identity entry. The Guarantor operation adds only the mandatory result-wrapper
profile carrying underlying terminal payment evidence and portable stage
admission. A URI-only match, an unwrapped generic payment result, or registry
digests/versions that do not contain both the bound Guarantor operation and
generic Semantic Action entry fails closed.

The fourteen stage tokens, their canonical array ordinals, and their exact
derivation-profile IDs are closed; implementations perform no textual token
transformation:

| Ordinal | Stage token | Exact `stage_derivation_profile_id` |
| ---: | --- | --- |
| 1 | `coverage_activation` | `tos.service.agent-guarantor.stage.coverage-activation.v1` |
| 2 | `coverage_non_activation` | `tos.service.agent-guarantor.stage.coverage-non-activation.v1` |
| 3 | `claim_submission_ingress` | `tos.service.agent-guarantor.stage.claim-submission-ingress.v1` |
| 4 | `initial_claim_admission` | `tos.service.agent-guarantor.stage.initial-claim-admission.v1` |
| 5 | `claim_revision_admission` | `tos.service.agent-guarantor.stage.claim-revision-admission.v1` |
| 6 | `claim_state_transition` | `tos.service.agent-guarantor.stage.claim-state-transition.v1` |
| 7 | `filing_close` | `tos.service.agent-guarantor.stage.filing-close.v1` |
| 8 | `terminal_decision` | `tos.service.agent-guarantor.stage.terminal-decision.v1` |
| 9 | `decision_application` | `tos.service.agent-guarantor.stage.decision-application.v1` |
| 10 | `payout_execution` | `tos.service.agent-guarantor.stage.payout-execution.v1` |
| 11 | `coverage_cancellation` | `tos.service.agent-guarantor.stage.coverage-cancellation.v1` |
| 12 | `coverage_closure` | `tos.service.agent-guarantor.stage.coverage-closure.v1` |
| 13 | `post_acceptance_exposure_release` | `tos.service.agent-guarantor.stage.post-acceptance-exposure-release.v1` |
| 14 | `coverage_resolution` | `tos.service.agent-guarantor.stage.coverage-resolution.v1` |

Both `required_independent_stages[]` and
`GuarantorStageActionAuthorityBindingV1.stages[]` use this ordinal order. An
underscore-form ID, inferred kebab-case alias, lexical reordering, unknown
stage, omission, or duplicate is invalid.

| Required stage | Action kind / purpose | Canonical request | Exact result besides `ActionResolutionV1` | Adapter route | CAS-domain source |
| --- | --- | --- | --- | --- | --- |
| `coverage_activation` | `conditional.obligation.transition` / `coverage-activation` | `CoverageActivationActionBodyV1` | `AuthorizedCoverageActivationEvidenceV1` under the activation-evidence envelope domain | `coverage_operation_adapter_profile.ActivateCoverage` | `coverage_state_domain` |
| `coverage_non_activation` | `conditional.obligation.transition` / `coverage-non-activation` | `CoverageNonActivationActionBodyV1` | `AuthorizedCoverageNonActivationEvidenceV1` under the non-activation-evidence envelope domain | `coverage_operation_adapter_profile.ResolveNonActivation` | `coverage_state_domain` |
| `claim_submission_ingress` | `conditional.claim.ingress` / `claim-submission-ingress` | `ClaimSubmissionIngressActionBodyV1` | `AuthorizedClaimSubmissionIngressReceiptV1` under the claim-ingress-receipt envelope domain | `claim_operation_adapter_profile.IngestClaim` | `claim_ingress_state_domain` |
| `initial_claim_admission` | `conditional.claim.submit` / `claim-admission` | `ClaimSubmissionActionBodyV1` whose nested claim is revision 1 with no predecessor | `AuthorizedClaimAdmissionReceiptV1` under the claim-admission envelope domain | `claim_operation_adapter_profile.AdmitClaim` | `coverage_state_domain` |
| `claim_revision_admission` | `conditional.claim.submit` / `claim-admission` | `ClaimSubmissionActionBodyV1` whose nested claim is revision greater than 1 with the exact predecessor | `AuthorizedClaimAdmissionReceiptV1` under the claim-admission envelope domain | `claim_operation_adapter_profile.AdmitClaim` | `coverage_state_domain` |
| `claim_state_transition` | `conditional.claim.transition` / `claim-state-transition` | `ClaimStateTransitionActionBodyV1` | `AuthorizedClaimStateTransitionReceiptV1` under the claim-state-transition envelope domain | `claim_operation_adapter_profile.TransitionClaim` | `claim_state_domain` |
| `filing_close` | `conditional.claim-filing.close` / `claim-filing-close` | `ClaimFilingCloseActionBodyV1` | `AuthorizedClaimFilingCloseReceiptV1` under the claim-filing-close envelope domain | `claim_operation_adapter_profile.CloseClaimFiling` | `coverage_state_domain` |
| `terminal_decision` | `conditional.claim-decision.admit` / `claim-decision-admission` | `ClaimDecisionAdmissionActionBodyV1` | on accepted admission, `AuthorizedClaimDecisionAdmissionReceiptV1` under the claim-decision-admission envelope domain | `claim_operation_adapter_profile.AdmitDecision` | `coverage_state_domain` |
| `decision_application` | `conditional.claim.decide` / `claim-decision-application` | `ClaimDecisionApplicationActionBodyV1` | `MaterializedPayoutObligationSetV1` and `AuthorizedClaimDecisionApplicationReceiptV1` under their released domains | `claim_operation_adapter_profile.ApplyDecision` | `coverage_state_domain` |
| `payout_execution` | the Agreement-selected `payment.direct` / `guarantor-payout` purpose for V1, `payment.domain-bound` / `guarantor-payout` purpose for V3, `settlement.external` / `guarantor-payout` purpose for V2, or `settlement.external` / `collateral-backed-payout` purpose | exact `GuarantorAgreementPaymentActionBodyV1` carrying the selected V1/V2/V3 request form, or exact `CollateralBackedAgreementPaymentActionBodyV1` | exact `AuthorizedGuarantorPayoutExecutionEvidenceV1`; its payment evidence uses the selected settlement-evidence profile and the collateral-backed form also carries exact `AuthorizedCollateralEvidenceV1` | `selected_payout_adapter_profile.SubmitPayment` or its exact `SubmitCollateralBackedPayment` composite route | `settlement_adapter_state_domain`, which is one atomic settlement-plus-position domain for the composite route |
| `coverage_cancellation` | `conditional.obligation.transition` / `coverage-cancellation` | `CoverageCancellationActionBodyV1` | `AuthorizedCoverageCancellationReceiptV1` under the cancellation-receipt envelope domain | `coverage_operation_adapter_profile.CancelCoverage` | `coverage_state_domain` |
| `coverage_closure` | `conditional.obligation.transition` / `coverage-closure` | `CoverageClosureActionBodyV1` | `AuthorizedTerminalClaimSetEvidenceV1` under the terminal-claim-set envelope domain | `claim_operation_adapter_profile.BeginClosure` | `coverage_state_domain` |
| `post_acceptance_exposure_release` | `portfolio.release` / `post-acceptance` | `ExposureReleaseActionBodyV1` | `AuthorizedExposureReleaseReceiptV1` under the exposure-release-receipt envelope domain | `exposure_operation_adapter_profile.ReleaseExposure` | `portfolio_exposure_state_domain` |
| `coverage_resolution` | `conditional.obligation.transition` / `coverage-resolution` | `CoverageResolutionActionBodyV1` | `AuthorizedCoverageResolutionV1` under the coverage-resolution envelope domain | `coverage_operation_adapter_profile.ResolveCoverage` | `coverage_state_domain` |

`coverage_state_domain` means exact equality with
`GuarantorCoverageTermsV1.coverage_state_domain_digest`. The other four domain
tokens select the Agreement-bound claim-ingress, per-claim, settlement-Adapter,
or exposure-Adapter state namespace and deterministic object key defined by the
named route; the resulting concrete digest equals the stage entry's
`admission_state_domain_digest`. The selected route profile equals the source
field named by the row. The `payout_execution` binding freezes one exact action
kind, request schema, Adapter profile, evidence profile, and state domain for
the payout obligation; it is not a runtime choice between the alternatives in
the table.

The only V1 `adapter_route_profile_source` tokens are the four values shown in
the schema. The only `cas_domain_source` tokens are
`coverage_state_domain`, `claim_ingress_state_domain`, `claim_state_domain`,
`settlement_adapter_state_domain`, and `portfolio_exposure_state_domain`; the
only `adapter_operation` tokens are the method names in the table. These are
closed wire enums, not display strings or implementation method lookup.
Unknown, case-folded, inferred, or aliased values fail canonical decoding.

Every stage result component uses the closed `accepted_effect_v1` presence
rule. `unknown`, `prepared`, `submitted`, `rejected`, and `conflict` carry zero
components. `accepted` carries the exact table cardinality and durably freezes
those component bytes. A terminal positive resolution carries the same exact
component vector and its `evidence_refs[]` commits the component digests in
registry order. If an accepted revision existed, terminal retains its bytes
unchanged; a sink may instead atomically commit the effect and terminal evidence
in one first durable terminal revision, but only with that complete verified
vector. A terminal negative resolution has zero components. New, changed,
missing, reordered, or unreferenced terminal-positive components are invalid.
An `accepted` result does not by itself
prove external finality where the selected stage requires a later terminal
Adapter result; downstream use applies that stage's evidence rule. In
particular, ordinary decision capacity rejection does not manufacture an
admission receipt.

Every positive result for one of the fourteen independent stages carries
exactly one embedded `PortableStageActionAdmissionEvidenceV1`. For all rows
except `payout_execution`, it is the field
`stage_action_admission_evidence` in the authorized result envelope named by
the table. Payout execution uses the wrapper defined in section 16.2. The
portable evidence's stage, operation ID, operation-binding digest, request
content type, and request bytes equal the immutable stage binding and the exact
request admitted by the sink. Its request length is positive, no greater than
that binding's `maximum_request_bytes`, and no greater than 1,048,576 bytes.
The verifier canonical-decodes and re-encodes those bytes as the bound request
type; recomputes its exact-request digest, semantic fields, stable action ID,
expected prior state, and Action digest; verifies the complete scalar
`AuthorizedActionV1` and `WriterFenceV1`; and requires their owner, Agent,
authority/key, scope, generation, validity, and proofs to match both the stage
binding and admission time. `admission_state` is exactly `accepted` and its
positive revision is the rollback-resistant action-admission revision. The one
`action_admission_authorization` is a native Ed25519 authorization by the exact
scalar Action Authority over
`Digest("tos.service.agent-guarantor-stage-action-admission.v1", body)` at
`admitted_at_unix`; it proves the Action/Fence high-water admission independently
of the business-evidence quorum. The body deliberately excludes the resulting
business component and `ActionResolutionV1`, so it is constructible before the
outer envelope is hashed and introduces no digest cycle. The later accepted or
terminal-positive `ActionResolutionV1` still commits the outer result component
under the mutation registry and must match the same stable ID and request
digest. At `accepted` its state revision equals the admission revision; a later
terminal-positive revision is greater, preserves the accepted component bytes,
and cites their digest in the registry order. The action/fence evidence is part of the complete
result-envelope digest and survives deletion of the sink resolver, Adapter
database, Provider, and Guarantor. A digest-only pointer, separately fetched
credential, mutable locator, second request path, or business-evidence quorum
without this independent action layer is invalid.

The field is required at all three assurance levels. For the two lower levels,
the verifier resolves the exact stage entry from the Agreement-embedded
`stage_action_authority_binding`, validates its canonical operation against the
immutable section 23 mutation-registry entry, and checks the bound service-
profile lifecycle/exposure authority or selected payout Adapter; there is no
claim of Guarantor-control deletion. For
`independently-enforceable`, those bytes must additionally equal the exact
binding committed by the operational-independence terms and pass its deletion
test. Omission is never
encoded as a lower-assurance shortcut.

The admission authorization's object kind is exactly
`stage-action-admission`, its authorized body digest is the recomputed body
digest, its validation time equals `admitted_at_unix`, and its native signature
domain is
`tos.service.agent-guarantor-stage-action-admission-signature.v1`. Its subject,
public key, and proof equal the immutable stage's scalar Action Authority; a
business-decision signer, Writer-Fence proof alone, threshold projection, or
second authorization profile cannot satisfy it. The complete evidence digest
uses `tos.service.agent-guarantor-stage-action-admission-evidence.v1`.

Initial versus revision admission is derived only from the claim nested in the
exact ingress receipt. Every decision admission, including a nonterminal row,
uses the `terminal_decision` stage binding; that name promises that the same
independent route can eventually admit the Agreement-fixed deterministic
terminal path, not that every intermediate result is terminal. Claim ingress
is separately durable and resolvable from admission, and its exact receipt is
consumed through one canonical path by the matching admission. Generic payment
execution validates `payout_execution` before the selected Adapter may submit
value. Exposure release and final resolution have their own stages and cannot
reuse `coverage_closure`, so an independent `BeginClosure` cannot hide a
Guarantor-controlled finalizer. An unused entry, implicit stage reuse, one
action standing in for two stages, or an omitted direct endpoint fails the
control-deletion test.

The profile is authenticated by the containing signed Intent and exact detail
descriptor. It is not separately self-signed. A verifier checks that the Intent
issuer equals `provider_agent_id`, the detail digest and size match, the
capability hint names this profile, revision lineage is valid, and the profile
and Intent validity windows overlap.

Published ranges are admission ceilings and discovery hints. They do not prove
available capacity. A Provider MAY refuse a request for a stricter local
reason, but it MUST NOT sign a firm offer outside the published or owner-policy
bounds.

## 12. Quote request and negotiated terms

```text
RequestedCoverageTermsV1 {
  schema_version
  coverage_category
  benefit_kind
  coverage_asset
  requested_aggregate_payout
  requested_per_claim
  deductible_range?
  coinsurance_ppm_range?
  maximum_claims
  requested_closure_capacity             # exact ClaimClosureCapacityV1 bounds and fallback
  requested_coverage_starts_at_unix
  requested_coverage_ends_at_unix
  requested_claim_filing_ends_at_unix
  maximum_review_deadline_seconds
  maximum_challenge_window_seconds
  maximum_nonterminal_resolution_window_seconds
  maximum_successor_decision_window_seconds
  maximum_payout_deadline_seconds
  maximum_adapter_recovery_window_seconds
  maximum_claim_ingress_resolution_grace_seconds
  maximum_late_ingress_recovery_window_seconds
  maximum_terminal_resolution_deadline_unix
  maximum_late_recovery_terminal_deadline_unix
  claim_trigger_profile
  claim_evidence_profile
  claimant_authorization_profiles[]
  claim_ingress_profile
  claim_ingress_authority_subjects[]
  claim_ingress_authority_quorum_rule
  claim_admission_profile
  decision_admission_profile
  decision_profile
  requested_decision_authority_subjects[]
  requested_decision_quorum_rule
  selected_assurance_level
  selected_claim_profile_digest
  selected_collateral_profile_digest?
  operational_independence_requirements? # exact GuarantorOperationalIndependenceTermsV1
  selected_payout_adapter_profile
  payout_destination_constraints
  exclusions_constraints
  cancellation_constraints
  requested_non_activation_reason_rules[]
  dispute_constraints
  default_constraints
  required_extensions[]
  optional_extensions[]
}

CoverageQuoteRequestBodyV1 {
  schema_version
  request_id
  service_intent_digest
  service_profile_digest
  requester_agent_id
  guarantor_agent_id
  covered_party_agent_id
  beneficiary_agent_id
  claimant_subjects[]
  underlying_agreement_body_digest
  covered_obligation_ids[]
  requested_terms_digest
  maximum_fee
  selected_assurance_level
  selected_claim_profile_digest
  selected_decision_profile
  selected_collateral_profile_digest?
  selected_payout_adapter_profile
  private_input_manifest_digest?
  created_at_unix
  expires_at_unix
  required_extensions[]
  optional_extensions[]
}

AuthorizedCoverageQuoteRequestV1 {
  body
  requested_terms
  authorizations[]
}
```

The verifier recomputes `requested_terms_digest` from the exact embedded
`RequestedCoverageTermsV1` under
`tos.service.agent-guarantor-requested-coverage-terms.v1`. Replacing the terms with a
locator, prose summary, Carrier copy, or digest-only unavailable object is
invalid. Repeated selected profiles and maxima in the request body are equality
constraints; any mismatch fails closed. The requester's Agent authorization is
the fixed native Agent profile for V1 and is resolved as required by section
9.1.

`selected_claim_profile_digest` and, when present,
`selected_collateral_profile_digest` each resolve to exactly one canonical
entry in the signed `GuarantorServiceProfileV1`. The request's trigger,
evidence, authority, decision, limit, assurance, asset, and Adapter selections
must be permitted by those exact entries. The final coverage terms repeat both
digests and the fully negotiated effective fields; they may narrow advertised
ranges but cannot change an entry's profile identities or exceed its limits.
`selected_assurance_level` is byte-identical in requested terms, quote request,
final coverage terms, reservation scope, firm offer projection, and activation
evidence; it is never inferred from the presence of collateral fields.
An absent collateral digest is valid only for `unsecured-signed`.
For `independently-enforceable`, the request and final coverage terms carry the
same exact `GuarantorOperationalIndependenceTermsV1`; an offer cannot weaken,
replace, or omit its roots, stages, routes, control resolver, immutable binding,
change policy, or freshness bound. Both lower levels omit the object.

The final `nonterminal_resolution_window_seconds` is positive, no greater than
the request's `maximum_nonterminal_resolution_window_seconds`, no greater than
the selected claim profile's corresponding maximum, and no greater than
`review_deadline_seconds`. A nonterminal decision must repeat that exact
duration; neither its authority nor transport may shorten it after Agreement
authorization.
The final `successor_decision_window_seconds` is likewise positive and no
greater than both request and selected-profile maxima. These are respectively
the exact `N` and `S` used by section 10.1. A nonterminal response inherits its
already running `resolution_due_at_unix` and therefore does not restart this or
any other window.

`selected_payout_adapter_profile` is an exact `ProfileRefV1`, not a URI. It is
byte-identical in `RequestedCoverageTermsV1`,
`CoverageQuoteRequestBodyV1`, and `GuarantorCoverageTermsV1`, resolves to one
entry in the signed service profile's `payout_adapter_profiles[]`, and equals
both `payout_destination_binding.payout_destination.settlement_adapter_profile`
and `payout_template.settlement_adapter_profile`. URI equality alone,
profile-version/digest substitution, or a destination using another Adapter
fails before offer issuance.

The nested `payout_template` is also validated as an exact capacity projection,
not merely as an Adapter selector. Agreement validation requires:

```text
payout_template.first_sequence = 1
payout_template.asset = coverage_asset
payout_template.maximum_per_instance = maximum_per_claim
payout_template.maximum_aggregate_amount = maximum_aggregate_payout
payout_template.maximum_instances = checked_mul(
  maximum_claims,
  claim_closure_capacity.maximum_payout_lines_per_claim)
```

The payer is the Guarantor, the payee is the beneficiary, the destination is
the Agreement-fixed payout destination, and the condition and authorized-
decision profiles are the exact selected Guarantor terminal-decision profiles.
The template's `agreement_obligation_id` equals the exact separate
`guarantor.payout.template` obligation ID named by the firm offer; it never
equals or substitutes the `guarantor.coverage` obligation ID. Its Adapter
ProfileRef, parameters digest, cancellation policy, and dispute policy equal
the corresponding enclosing coverage terms. A smaller value could strand a valid admitted claim; a
larger or shifted value could authorize an obligation outside the accepted
coverage. Therefore no inequality, non-one starting sequence, or
implementation-local default is valid. Checked multiplication overflow rejects
the Agreement before any authorization or reservation.

The request is targeted to one Guarantor and one proposed set of parties. It
authorizes only the request. It is not Agreement acceptance, a fee payment,
coverage activation, disclosure authority, or permission to move collateral.

Private underwriting inputs use the authenticated, bounded private-content
handoff profile. Only exact content digests and manifests enter the request.
Secrets, source archives, personal data, and claim attachments do not enter a
Carrier, public Intent, ordinary log, or model context without a separately
authorized disclosure action.

### 12.1 Coverage terms

```text
GuarantorCoverageTermsV1 {
  schema_version
  coverage_id
  coverage_version
  predecessor_terms_digest?
  service_profile_digest
  quote_request_digest
  guarantor_agent_id
  covered_party_agent_id
  beneficiary_agent_id
  permitted_claimant_subjects[]
  underlying_agreement_body_digest
  covered_obligation_ids[]
  coverage_category
  benefit_kind                      # fixed_benefit or indemnity
  selected_assurance_level
  coverage_asset
  maximum_aggregate_payout
  maximum_per_claim
  deductible?
  coinsurance_ppm?
  benefit_calculation_profile
  maximum_claims
  claim_closure_capacity                  # exact ClaimClosureCapacityV1 bounds and fallback
  coverage_starts_at_unix
  coverage_ends_at_unix
  claim_filing_ends_at_unix
  claim_ingress_resolution_grace_seconds
  late_ingress_recovery_window_seconds
  coverage_state_domain_digest            # one Agreement-bound revision/CAS domain
  review_deadline_seconds
  challenge_window_seconds
  nonterminal_resolution_window_seconds
  successor_decision_window_seconds
  payout_deadline_seconds
  adapter_recovery_window_seconds
  terminal_resolution_deadline_unix       # exact normal-case hard effect target
  late_ingress_recovery_deadline_unix     # latest late filing-close/fallback admission
  late_recovery_terminal_deadline_unix    # exact contingency hard effect target
  acceptance_processing_grace_seconds
  exclusions_policy
  cancellation_policy                 # exact CoverageCancellationPolicyV1
  non_activation_reason_rules[]       # exact closed CoverageNonActivationReasonRuleV1 set
  dispute_policy
  default_policy
  other_coverage_policy
  payout_destination_binding
  coverage_layer_id
  layer_priority
  layer_share_ppm
  selected_claim_profile_digest
  selected_collateral_profile_digest?
  selected_payout_adapter_profile
  coverage_operation_adapter_profile
  claim_operation_adapter_profile
  exposure_operation_adapter_profile
  stage_action_authority_binding       # exact GuarantorStageActionAuthorityBindingV1
  operational_independence_terms?        # exact GuarantorOperationalIndependenceTermsV1
  claim_trigger_profile
  claim_evidence_profile
  claimant_authorization_profiles[]
  claim_ingress_profile
  claim_ingress_authority_subjects[]
  claim_ingress_authority_quorum_rule
  claim_admission_profile
  claim_admission_authority_subjects[]
  claim_admission_quorum_rule
  acceptance_authority_profile
  lifecycle_authorization_profile
  decision_admission_profile
  decision_admission_authority_subjects[]
  decision_admission_quorum_rule
  decision_profile
  decision_authority_subjects[]
  decision_quorum_rule
  payout_template
  premium_obligation_ids[]
  collateral_obligation_id?
  collateral_terms?
  required_extensions[]
  optional_extensions[]
}
```

The following closed rule set is part of the canonical coverage terms and
therefore of the Agreement body before any party authorizes it:

```text
ActivationPrerequisiteFailureRuleV1 {
  prerequisite_id
  terminal_failure_evidence_profile       # exact ProfileRefV1
  terminal_failure_authority_subjects[]   # canonical nonempty set
  terminal_failure_quorum_rule
  permitted_terminal_failure_outcomes[]   # closed, nonempty enum set
}

CoverageNonActivationReasonRuleV1 {
  reason                                  # prerequisite_failed,
                                          # activation_window_expired,
                                          # mutually_cancelled
  evidence_mode                           # terminal_prerequisite_failure,
                                          # cutoff_only, unanimous_typed_cancel
  prerequisite_failure_rules[]            # exact canonical set or empty
  cancellation_authorization_predicate_ids[] # exact canonical set or empty
}
```

Exactly one rule exists for each of the three V1 reasons and no unknown reason
is accepted. `prerequisite_failed` uses
`terminal_prerequisite_failure`, has one failure rule for every Agreement-
defined activation prerequisite that can fail terminally, and has no
cancellation predicates. `activation_window_expired` uses `cutoff_only` and
both arrays are empty. `mutually_cancelled` uses `unanimous_typed_cancel`, has
no prerequisite rules, and names the complete, nonempty set of Agreement-body
authorization predicates for the Guarantor, covered party, beneficiary when
distinct, fee payer, and collateral principal when their rights or assets are
affected. A predicate may coalesce identical subjects but cannot omit a role.
Each named predicate fixes the evidence profile, authority subject, role scope,
validity bounds, and the requirement that its later evidence authorize the
exact cancellation-request digest. The requested and final rule sets are byte-
identical; an offer may reject a request but cannot silently weaken a rule.

The quote request's `maximum_fee` is an exact `AtomicAmountV1`, not a display
estimate. `premium_obligation_ids[]` is a canonical sorted unique set and equals
the complete set of `guarantor.fee` obligations in the proposed coverage
Agreement. Each named obligation has a fixed, finite atomic amount in exactly
the same `AssetIdentityV1` as `maximum_fee`, names exactly the request's
`covered_party_agent_id` as obligor, names exactly the request's
`guarantor_agent_id` as beneficiary, and is dependency-bound to this exact
coverage obligation. V1 deliberately forbids alternate premium payers and fee
recipients because the quote request has no separate authority surface for
them; support for either role requires a new request/profile version that binds
the exact subjects and their authorization predicates. Installments may use
several IDs, but each
amount is fixed before Agreement authorization. Variable, unbounded, foreign-
asset, or dynamically recurring premium obligations are invalid in V1.

Every verifier computes with checked same-asset addition:

```text
total_coverage_fee = sum(
  agreement.obligation[id].amount_atomic
  for id in premium_obligation_ids)

total_coverage_fee.amount_atomic <= maximum_fee.amount_atomic
```

An empty set yields canonical zero. The Agreement MUST NOT make activation,
continued coverage, claim admission, decision, payout, or release depend on any
other value transfer to the Guarantor or a Guarantor-controlled fee recipient;
such a transfer is an omitted premium and invalidates the mapping. A genuinely
independent Decision Authority review fee is a separate obligation and cannot
be made a hidden condition of the Guarantor's coverage service. The firm-offer
verifier derives the IDs and amounts from its exact embedded Agreement and
quote request, recomputes the sum, and rejects an omitted, duplicated,
substituted, excess, or asset-mismatched fee before authorizing the offer.

`coverage_state_domain_digest` is an immutable Agreement field, not a runtime
locator or a Provider-local database name. It is the exact Adapter- or
authority-profile-defined state-domain digest whose rollback-resistant revision
orders activation, non-activation, initial and revision claim admission, filing
close, decision admission and application, active cancellation, terminal-set
construction, and final coverage resolution. Every operation that compares or
advances `coverage_revision` MUST use this one domain. For lower assurance, the
claim-admission and lifecycle authority profiles both resolve it. For
`independently-enforceable`, the `admission_state_domain_digest` in the
`coverage_activation`, `coverage_non_activation`, `initial_claim_admission`,
`claim_revision_admission`, `filing_close`, `terminal_decision`,
`decision_application`, `coverage_cancellation`, and `coverage_closure` stage
entries, plus the `coverage_resolution` stage entry, MUST all equal it. A
deployment cannot advertise that assurance when
any one of those entries names a different state head, even if its local
revision happens to have the same integer value.

`stage_action_authority_binding` is mandatory at every assurance level and is
the sole portable source for all fourteen stage operation bindings, Action
Authorities, Writer-Fence domains and authorities, generation-high-water
profiles, action-resolution profiles, and admission-state domains. Its stage
set, ordinals, operation-registry entries, request maxima, result bindings, and
CAS-domain derivations pass sections 10, 11, and 23 before Agreement
authorization. The three operation Adapter ProfileRefs in the coverage terms
are also mandatory and supply the exact route-profile sources named by those
stage entries. Under `unsecured-signed` and `collateral-attested`, the service-
profile lifecycle authority supplies coverage and claim stage action authority,
the exposure authority supplies exposure release, and the selected settlement
Adapter supplies payout execution; the binding records their exact keys and
domains without claiming control independence. A service-profile revision,
Provider-local database, or runtime route cannot replace those Agreement bytes.

For `independently-enforceable`, the operational-independence terms' three
Adapter ProfileRefs are byte-identical to the sibling coverage-term fields and
its `stage_action_authority_binding_digest` equals the canonical digest of that
sibling binding. The control-deletion, independent quorum, and direct-route
rules then strengthen the same binding rather than creating a second stage set.
For both lower levels the operational-independence object is absent, but the
stage binding is not. Every portable result therefore remains independently
constructible and verifiable at its honestly selected assurance level.

The durable record also has exactly one canonical `CoverageEndCommitmentV1`.
Its digest is
`Digest("tos.service.agent-guarantor-coverage-end-commitment.v1", commitment)`.
For active coverage, `end_branch = scheduled`, the incident cutoff equals the
Agreement's immutable `coverage_ends_at_unix`, and end evidence is absent. An
admitted cancellation replaces that value once with
`accepted_cancellation`, its exact admitted effective time, and the complete
authorized cancellation-receipt envelope digest. Confirmed non-activation uses
`never_activated`, omits the incident cutoff, and binds the complete authorized
non-activation envelope. Presence rules are closed. The scheduled branch may
change only to `accepted_cancellation` before its strict cutoff; the other two
branches are immutable. A filing-close receipt later derives the display and
closure reason `normal_expiry` from a still-scheduled commitment, but does not
rewrite that commitment or create a scheduled-expiry action.

`claim_closure_capacity` is required and its `maximum_claims` equals the
top-level field. Every selected count and byte ceiling is no greater than both
the authenticated `GuarantorClaimProfileV1` entry and the request's
`requested_closure_capacity`; changing one requires a new Agreement version.
The request and final terms are each verified as complete, self-consistent
capacity objects: every `computed_worst_case_*_bytes` value is independently
recomputed from that object's own maxima and MUST NOT be copied from the other
object. Their continuation entries have the same canonical state keys. Final
required slot counts and durations are derived from the final round counts and
exact timing windows and are no greater than their corresponding requested
maxima; equality is required wherever the final terms did not tighten an input.
The final `continuation_budget_profile` equals the selected claim-profile
entry, and its exact `terminal_fallback` is byte-identical to the requested
fallback and occurs exactly once in that entry's permitted set. The fallback
rule, subjects, quorum, and deterministic authorization mode are therefore
fixed before Agreement authorization. The final ordinary and late-recovery
deadlines are deterministically derived under section 12.2 from Agreement
expiry, the selected bounded late-recovery window and, when present, collateral
lock/reorg terms. They must be no later than their corresponding request maxima
and cannot be moved by a later signer or runtime. Request fields are only
authorized upper bounds, not final runtime deadlines. Request validation proves
that the requested timing windows and closure capacity fit beneath both
ceilings. Final-terms validation recomputes the exact deadlines and MUST NOT
copy request ceilings as asserted derived facts.
The verifier performs the section 10.1 worst-case computation before accepting
the terms. A Provider cannot promise a larger claim history and later reject a
conforming claim merely because closure storage was under-provisioned.

`claim_ingress_profile`, its authority subjects and quorum are byte-identical
to the selected authenticated `GuarantorClaimProfileV1` and to the request's
accepted constraints; a Provider cannot replace them in final terms.
`claim_ingress_resolution_grace_seconds` is positive and no greater than both
the request and selected profile maxima. Initial ingress is closed at
`claim_filing_ends_at_unix`, but actions sequenced no later than that cutoff
receive this full bounded interval to resolve ingress and admission. Every
accepted claim-admission receipt must have `admitted_at_unix` no later than the
checked sum of cutoff plus grace; an action that has not linearized by that
instant may later resolve only as a terminal rejection for admission purposes.

Filing close normally linearizes after the zero-pending ingress cut and no later
than that checked grace endpoint. If any timely ingress is still unknown,
prepared, submitted, accepted-but-unresolved, or otherwise ambiguous at the
endpoint, close remains blocked and the coverage records a liveness/default
condition. Elapsed time is not an empty-cut proof. After every such action is
resolved, the same filing-close route MUST permit a late close using the exact
final ingress log, but only through the Agreement's
`late_ingress_recovery_deadline_unix`. An action still unresolved at that hard
cutoff resolves as the claim-ingress profile's deterministic terminal rejection
for claim-admission purposes; it cannot later create an admitted claim. That
cutoff transaction freezes the final cut and prevents value from remaining
reserved indefinitely. Late close cannot reset a review window, extend incident
eligibility, rewrite either hard deadline, or pretend the ordinary deadline was
met; it only enters the pre-reserved contingency path. The Agreement grants the
filing-close authority this bounded recovery-only capability. A late recovery
is reported as an operational breach and may finish after the ordinary target,
but never after `late_recovery_terminal_deadline_unix`.

A late close also opens exactly one recovery-only terminalization route for
each admitted claim that is not already terminal:
`late_recovery_terminal_fallback`. The path uses the Agreement-selected total
deterministic fallback function over the exact frozen portable claim/evidence
head and may produce only a challengeable approval, partial approval, or zero
denial. It cannot request more evidence, open another revision epoch, admit a
new claim, change an incident cutoff, or use model/provider discretion. The
ordinary challenge, decision-application, payout/default, collateral,
exposure-release, and coverage-resolution state machines then run to completion
with their fixed relative durations even though the normal-case terminal target
has been missed.

This narrow recovery route becomes eligible only from the exact late filing-
close receipt and has the hard admission and completion cutoffs in section
12.2. Each concrete `AuthorizedActionV1` has a current authority expiry no later
than its applicable stage cutoff; an expired-but-unadmitted envelope may be
reauthorized with a current fence while preserving the same semantic action ID
and exact request bytes, but never after that cutoff. Once admitted, ambiguity
resolves only that action. The recovery route cannot be used when filing closed
on time or to extend an otherwise ordinary claim. At the outer hard-effect
deadline, any unresolved Adapter operation produces its Agreement-selected
terminal default/impaired evidence and the state machines close without
fabricating payment. Thus an outage is observable and authority is finite,
while a timely accepted claim retains the exact bounded contingency path for
which collateral and exposure were reserved.

For `independently-enforceable`, `operational_independence_terms` is required;
for both lower levels it is absent. Its `required_independent_stages[]` is
exactly the fourteen-stage V1 set shown in section 10. Its coverage-operation
Adapter profile is directly callable for activation, non-activation resolution,
cancellation, and final coverage resolution; its claim-operation Adapter
profile equals the selected claim profile's independent operation profile. Its
exposure-operation Adapter is directly callable for post-acceptance exposure
release and is independent of the Guarantor control closure. Its immutable
stage binding authorizes that Adapter to treat the exact signed exposure-
admission receipt plus the exact activation/terminal evidence as the immutable
genesis of a reservation-scoped release record. The Adapter keys that record by
reservation ID and receipt digest, admits at most one final release, and needs no Provider-private
portfolio credential or co-signature. The Provider may reconcile its private
accounting later; that accounting is not authority for the independent release
receipt.
`claim_state_transition`
includes exactly `nonterminal_response_admission`, `challenge_admission`, and
`challenge_close` in V1. The
`guarantor_control_root_subjects[]` set is not caller selectable: the verifier
derives the complete roots from `guarantor_agent_id`, the offer-bound service
profile's exposure and lifecycle authorities, and every custody or Adapter
subject whose released authority resolver identifies one of those roots as a
controller. Exact equality is required.

At Agreement authorization and activation, the selected control-resolution
profile computes the transitive technical-control closure of those roots at one
atomic evidence snapshot. Each required stage's scalar Action/Writer-Fence
authority must lie outside that closure. Separately remove every subject in the
closure from the claim-activation, non-activation, claim-ingress,
admission/revision, non-decision transition, filing-close, terminal-decision,
decision-application, cancellation, closure, and payout-execution business-
evidence quorums. Every remaining quorum must still be satisfiable and
must retain a direct authenticated Adapter route. The immutable authority-
binding digest commits the scalar action authorities, business-evidence
subjects and quorums, routes, Adapter configuration, and the beneficiary's
fixed destination. During the liability window, an
authority change is admissible only under the bound change policy and only when
the same deletion test still passes; it cannot add a Guarantor veto. This is a
technical authority-independence claim, not proof of legal, economic, or
beneficial-owner independence.

V1 supports only an Agreement-fixed payout destination. The exact
`PayoutDestinationV1` is inside the coverage Agreement's canonical terms and
its `destination_authorization_predicate_id` names a body-bound beneficiary,
wallet, or custody predicate that authorizes those exact bytes. The Guarantor,
Claimant, Decision Authority, Carrier, model, or settlement Adapter cannot
replace it. Every claim, payout line, materialized settlement obligation, and
Adapter request MUST reproduce its digest, beneficiary, asset, system, routing
parameters, and raw destination bytes. Changing the destination requires a new
coverage Agreement version authorized before activation; it is forbidden after
any claim or payout action for that version is prepared, admitted, submitted,
accepted, or ambiguous.
The `payout_template.payout_destination_binding` is byte-for-byte equal to the
top-level coverage-terms binding; duplication with conflicting bytes is
invalid.

`coverage_id` is issuer scoped and is derived before the coverage Agreement is
hashed. The exact V1 derivation is:

```text
coverage_id = Digest("tos.service.agent-guarantor-coverage-id.v1", {
  guarantor_agent_id,
  quote_request_digest
})
```

Version 1 has no predecessor. A later version retains `coverage_id`, increments
`coverage_version` by one, and binds the predecessor terms and Agreement body
digests. A revision is a full replacement for future authority; it never
rewrites an event, fee, claim, decision, or payment already governed by a prior
version.

`fixed_benefit` pays the accepted amount when the trigger predicate is
satisfied. `indemnity` also applies the accepted loss-measurement, deductible,
coinsurance, other-coverage, recovery, layer, and aggregate rules. Implementers
must not substitute one benefit kind for the other.

The terms do not contain the final coverage Agreement digest, authorization
target digests, firm-offer digest or signature, exposure receipt, writer
generation, or terminal collateral evidence. Excluding them is required for
the one-way, digest-cycle-safe construction in section 14.

The claim-admission profile selects the only authority domain that may assign a
claim admission sequence, close the filing window, and attest the complete
claim set. `unsecured-signed` MAY select the Guarantor's rollback-resistant
lifecycle authority. A collateral or independently enforceable tuple MUST use
an admission profile that the selected Collateral Adapter can verify and whose
release transition is ordered against that same claim high-water. A Provider
signature over a private list cannot be promoted to independently enforceable
completeness.

The decision-admission profile and authority/quorum tuple resolves exactly from
the selected claim-profile entry and is copied byte-for-byte into the coverage
terms. It is distinct from the merits `decision_profile`: the latter authorizes
the decision body, while the former linearizes that body into the claim log.
For `independently-enforceable`, the resulting decision-admission receipt must
independently satisfy that selected profile, subject set, and quorum after the
Guarantor control-deletion test. The mutation that admits it separately uses
the immutable `terminal_decision` stage's scalar Ed25519 Action Authority and
Writer Fence from `GuarantorStageActionAuthorityV1`. These are different
typed authorization layers and are never compared for byte equality or
substituted for one another; both must independently pass control deletion. The
portable decision-admission receipt embeds the complete scalar Action and Fence
envelopes, rather than relying on their authority's mutable resolver for later
verification.

For `independently-enforceable`, verification alone is insufficient: the
selected claim operation Adapter must itself admit authorized initial claims
and revisions and freeze the filing high-water through the Guarantor-control-
deleted quorum. The Guarantor lifecycle authority may be a redundant member but
cannot be necessary for any transition.

The same Adapter validates the immutable per-stage Action Authority binding
before admission. It obtains the current Writer Fence from the selected
independent fence domain, checks its generation high-water in the same
linearizable boundary as the stage mutation, and persists the action
resolution under the bound resolution profile. A Guarantor fence or local
OpenFox process lock cannot satisfy this rule.

### 12.2 Time-window satisfiability

All additions use checked unsigned arithmetic; overflow is invalid. V1 forbids
retroactive activation and requires these exact inequalities:

```text
quote_request.created_at_unix
  <= offer.valid_from_unix
  < accept_by_unix
  < accept_by_unix + acceptance_processing_grace_seconds
  <= reservation_expires_at_unix
  <= offer.expires_at_unix
  <= quote_request.expires_at_unix
  <= coverage_starts_at_unix

agreement.valid_from
  <= activated_at_unix
  <= coverage_starts_at_unix
  < coverage_ends_at_unix
  <= claim_filing_ends_at_unix

claim_filing_ends_at_unix
  + claim_ingress_resolution_grace_seconds
  + review_deadline_seconds
  + challenge_window_seconds
  + payout_deadline_seconds
  + adapter_recovery_window_seconds
  <= agreement.expires_at
```

The last inequality is only a one-round lower bound. The selected continuation
table supplies the stronger exact bound for all negotiated challenge and
nonterminal rounds. Scheduling starts from one Agreement-fixed outer hard-
effect anchor and reserves a distinct, bounded contingency lane for a timely
ingress whose admission remains ambiguous through the ordinary grace period.
The ordinary lane cannot consume that reserve:

```text
hard_effect_deadline =
  if unsecured:
    agreement.expires_at
  otherwise:
    min(agreement.expires_at,
        checked_sub(collateral_terms.lock_until_unix,
                    collateral_terms.reorg_window_seconds))

late_recovery_terminal_deadline_unix = hard_effect_deadline

late_recovery_candidate_closure_seconds =
  continuation_budget[challengeable_candidate,
                      maximum_challenge_rounds_per_claim,
                      0].maximum_remaining_closure_seconds

late_ingress_recovery_deadline_unix = checked_sub(
  late_recovery_terminal_deadline_unix,
  late_recovery_candidate_closure_seconds)

terminal_resolution_deadline_unix = checked_sub(
  late_ingress_recovery_deadline_unix,
  late_ingress_recovery_window_seconds)

latest_payout_terminal_at =
  checked_sub(terminal_resolution_deadline_unix,
              adapter_recovery_window_seconds)

latest_terminal_claim_close_at =
  checked_sub(latest_payout_terminal_at,
              payout_deadline_seconds)

latest_admission_at(state, challenge_rounds_remaining,
                    nonterminal_rounds_remaining) =
  checked_sub(latest_terminal_claim_close_at,
              continuation_budget[state, rounds].maximum_remaining_decision_path_seconds)
```

The three derived absolute deadlines must equal their fields in the accepted
coverage terms. `terminal_resolution_deadline_unix` is no later than the
request's `maximum_terminal_resolution_deadline_unix`,
`late_recovery_terminal_deadline_unix` is no later than the request's
`maximum_late_recovery_terminal_deadline_unix`, and none is a caller-selected
later timestamp. `late_ingress_recovery_window_seconds` is positive and no
greater than both the request and selected claim-profile maxima. The selected
claim profile must permit `late_recovery_terminal_fallback`; otherwise all
three late-recovery fields are forbidden and the ordinary deadline equals
`hard_effect_deadline`. The
continuation entry's `maximum_remaining_closure_seconds` includes its decision
path plus payout and Adapter-recovery windows, while
`maximum_remaining_decision_path_seconds` is exactly the formula in section
10.1 before those two windows. The two fields must differ by the checked sum of
the accepted payout and Adapter-recovery windows. The equivalent direct check
is the section 10.1 inequality. The worst-case initial schedule also requires:

```text
latest_possible_claim_review_cutoff =
  claim_filing_ends_at_unix
  + claim_ingress_resolution_grace_seconds
  + review_deadline_seconds

latest_possible_claim_admission_at =
  claim_filing_ends_at_unix
  + claim_ingress_resolution_grace_seconds

latest_possible_claim_admission_at
  <= latest_admission_at(initial_reviewing,
                         maximum_challenge_rounds_per_claim,
                         maximum_nonterminal_rounds_per_claim)

terminal_resolution_deadline_unix
  < late_ingress_recovery_deadline_unix
  < late_recovery_terminal_deadline_unix
```

The `initial_reviewing` entry already includes `review_deadline_seconds`, so the
last comparison starts at the latest possible post-ingress-grace claim
admission and does not add that duration twice. An ingress sequenced by the
filing cutoff may consume the entire accepted grace interval; no verifier may
replace `latest_possible_claim_admission_at` with the filing cutoff. For each
admitted claim, its portable, immutable cutoff is derived independently:

```text
claim_review_cutoff =
  checked_add(initial_claim_admission_receipt.body.admitted_at_unix,
              review_deadline_seconds)

claim_review_cutoff <= latest_possible_claim_review_cutoff
```

A revision, retry, Writer takeover, or later receipt cannot reset or extend
this claim-relative cutoff.

For collateralized coverage, additionally:

```text
collateral_terms.lock_by_unix <= coverage_starts_at_unix
late_recovery_terminal_deadline_unix + collateral_terms.reorg_window_seconds
  <= collateral_terms.release_not_before_unix
collateral_terms.release_not_before_unix <= collateral_terms.lock_until_unix
late_recovery_terminal_deadline_unix
  + collateral_terms.reorg_window_seconds
  <= collateral_terms.lock_until_unix
collateral_terms.lock_until_unix <= agreement.expires_at
```

Every subtraction and multiplication is checked; underflow, overflow, a
missing state/round entry, or a zero-time ordering ambiguity invalidates the
request before a firm offer. `release_not_before_unix` is only an earliest-
release guard and never contributes processing time.

The quote request's requested windows satisfy the corresponding order, and a
firm offer may only tighten them within requester maxima. Before acceptance and
again before activation, the authority verifies that current time, Agreement,
authorization-evidence expiry, fee and collateral prerequisites, reservation,
and selected Adapter resolution bounds still fit the complete schedule.
Activation after `coverage_starts_at_unix`, or a prerequisite that cannot be
terminal by that time, fails closed and requires a newly authorized Agreement;
it never silently shortens coverage. An incident is eligible only when its
profile proves `coverage_starts_at_unix <= occurred_at_unix <=
coverage_ends_at_unix`. The initial `conditional.claim.ingress` action must be
durably sequenced no later than `claim_filing_ends_at_unix`; the corresponding
claim-admission action may linearize no later than
`checked_add(claim_filing_ends_at_unix,
claim_ingress_resolution_grace_seconds)`, but only from that timely ingress and
within the same frozen ingress cut. A claim first sequenced after the filing
cutoff is invalid, while a timely ingress is not invalid merely because ingress
resolution or claim admission uses the accepted grace interval.

## 13. Generic Agreement mapping

The coverage contract is a separate generic `AgentAgreementBodyV1` that
references an already identified underlying Agreement. Its
`agreement_id` equals `coverage_id`, and its `version` equals
`coverage_version`.

A typical obligation DAG contains:

| Obligation kind | Obligors and purpose | Value semantics |
| --- | --- | --- |
| `guarantor.coverage` | Guarantor owes the bounded contingent service to the beneficiary | non-current-value; subject is exact `GuarantorCoverageTermsV1` |
| `guarantor.fee` | fee payer pays the Guarantor | ordinary fixed value-bearing obligation |
| `guarantor.collateral.lock` | collateral principal locks an exact position | specialized Adapter transition, not a payout |
| `guarantor.claim.review` | selected Decision Authority reviews admitted claims | service obligation; any review fee is separate |
| `guarantor.payout.template` | Guarantor exposes the finite conditional settlement template | non-current-value until a terminal decision materializes exact lines |
| `guarantor.collateral.release` | Adapter returns eligible residual collateral | specialized terminal transition |

The open `kind` token and canonical subject bytes in the generic Agreement
already support these namespaced kinds. V1 does not add an industry enum to the
core Agreement schema.

Every obligation references body-bound `AgreementAuthorizationPredicateV1`
records. The deterministic mandatory set includes, as applicable:

- the Guarantor Agent for coverage and payout-template obligations;
- the covered party and fee payer;
- the beneficiary when its claim, disclosure, cancellation, challenge, or
  other-coverage duties are material;
- each custody, wallet, collateral, key, capability, or data authority whose
  assets or protected resources may move;
- every Decision Authority accepting a review role; and
- any stricter owner-required authorizer.

The Guarantor predicate selects
`tos.service.agreement.evidence.guarantor-firm-offer.v1`. Other predicates MAY select
generic Agent signatures, custody authorization, external evidence, or a
released contract profile. Evidence profiles are selected per predicate and
cannot be chosen after the body digest is fixed.

The firm-offer evidence profile is frozen as:

```text
profile_uri:     tos.service.agreement.evidence.guarantor-firm-offer.v1
profile_version: 1
content_type:    application/vnd.tos.service.agent-guarantor-firm-offer-agreement-evidence.v1+cbor
group_rule:      complete-subject-profile-group
target_rule:     agreement-predicate-target-v1
verifier:        tos.service.agent-guarantor.verify.firm-offer-agreement-evidence.v1
```

The canonical descriptor and its digest are released in the conformance corpus.

```text
GuarantorFirmOfferAgreementEvidenceV1 {
  schema_version
  evidence_profile                  # exact ProfileRefV1
  agreement_body_digest
  guarantor_agent_id
  satisfied_predicate_targets[] {
    predicate_id
    target_projection_digest
  }
  authorized_firm_offer_envelope_digest
  authorized_firm_offer             # complete AuthorizedFirmCoverageOfferV1
}
```

`evidence_profile.profile_uri` is exactly
`tos.service.agreement.evidence.guarantor-firm-offer.v1`; its released version and
digest must equal the Agreement predicate and the `guarantor_evidence_profile`
inside the offer. The evidence subject is exactly the Agreement's Guarantor
Agent. The predicate-target pairs are sorted by predicate ID then target digest,
reject duplicate predicates and targets, and must equal the complete Guarantor-
authorized predicate group—neither a subset nor a superset.
The verifier recomputes the complete embedded firm-offer envelope digest,
checks its one-way Agreement, receipt, subject, profile, and target bindings,
then projects this object into the generic `AgreementAuthorizationEvidenceV1`
profile-evidence field. No codec may substitute an unsigned offer body, a
signature alone, or a locally invented projection.

Ordinary chat, a locally frozen transcript, a UI click without typed evidence,
a model-generated phrase, and a Carrier acknowledgement never satisfy an
Agreement predicate.

Coverage acceptance and activation use the following Guarantor-profile-local
canonical carrier of released business-neutral evidence rather than an
implementation-local hash of wrappers. The wrapper is owned and versioned by
this profile; it does not add a generic Agreement wire type:

```text
GuarantorAgreementAuthorizationEvidenceSetV1 {
  schema_version
  agreement_id
  agreement_version
  agreement_body_digest
  evidence[]                         # complete AgreementAuthorizationEvidenceV1 objects
}

complete_authorization_evidence_set_digest
  = Digest(
      "tos.service.agent-guarantor-agreement-authorization-evidence-set.v1",
      GuarantorAgreementAuthorizationEvidenceSetV1)
```

`evidence[]` is a set sorted by each element's complete canonical encoded bytes
and rejects byte duplicates. The verifier also derives each element's semantic
identity from its body-bound authority subject, profile URI/version/digest,
predicate set, and target-projection set. Two different elements under one
semantic identity are conflicting evidence, not two votes. The set must name
the same Agreement body and version, satisfy every mandatory predicate exactly
under its frozen grouping rule, contain no out-of-scope predicate or target,
and reproduce each selected profile descriptor. Unknown or unsupported
evidence cannot be counted merely because its bytes are present.

The digest covers complete evidence objects, including their authorization
proofs. Rewrapping, changing a key or proof path, adding an otherwise unused
object, or changing canonical order therefore cannot preserve the digest. An
underlying Agreement and the coverage Agreement use distinct set objects and
body digests even when they happen to have the same participants.

## 14. Reserve-before-offer and digest-cycle-safe firm offer

### 14.1 Construction order

Implementations use this exact dependency direction:

```text
authorized quote request and negotiated terms
  -> canonical GuarantorCoverageTermsV1
  -> generic coverage Agreement core and authorization policy
  -> recompute body-bound predicate target projections
  -> final coverage Agreement body digest
  -> recoverably allocate one authority_instance_id / offer_id
  -> one Provider-authority operation atomically reserves exposure,
     creates the admission receipt, constructs the final offer body,
     and authorizes the firm offer
  -> remaining Agreement authorization evidence
```

The Agreement body MUST NOT commit the firm-offer body, signature, binding
digest, or exposure receipt. The firm offer commits the already final Agreement
body in one direction. This preserves one unique Agreement without a hash
cycle.

`offer_id` is exactly the recoverably allocated `authority_instance_id` from
Semantic Action Identity V1. The allocation's canonical effect descriptor
commits the requester, final Agreement and terms digests, recipient set,
reservation scope, maximum exposure, offer validity schedule, and all proposed
offer fields, with fixed zero placeholders only for the authority-generated
offer ID, reservation ID, and exposure receipt. A caller UUID,
wall time, transport ID, random nonce, or a second allocation after an ambiguous
result is invalid. An intentionally new counteroffer requires a separately
authorized quote request and a new V1 offer allocation; it cannot revise or
replace the original authority instance. The portfolio therefore reserves both
offers until each reaches its own terminal acceptance-or-close result.

### 14.2 Exposure admission

```text
FirmOfferRecipientSetV1 {
  schema_version
  requester_agent_id
  guarantor_agent_id
  covered_party_agent_id
  beneficiary_agent_id
  claimant_subjects[]
  acceptance_subjects[]
}

ProviderExposureReservationScopeV1 {
  schema_version
  owner_id
  guarantor_agent_id
  coverage_agreement_body_digest
  coverage_obligation_id
  coverage_asset
  maximum_aggregate_payout
  selected_assurance_level
  policy_bucket_digest
  correlation_bucket_digest
  default_liability_disposition      # charge_off or retain
  reservation_expires_at_unix
}

FirmOfferAuthorityInstanceEffectV1 {
  schema_version
  guarantor_agent_id
  authorized_quote_request_envelope_digest
  coverage_agreement_body_digest
  coverage_terms_digest
  recipient_set                       # exact FirmOfferRecipientSetV1
  recipient_set_digest
  reservation_scope                   # exact ProviderExposureReservationScopeV1
  reservation_scope_digest
  reserved_exposure
  preallocation_offer_template       # exact body with three zero placeholders
}

FirmOfferIssuanceActionBodyV1 {
  schema_version
  authority_instance_id
  authority_instance_record
  authority_instance_effect          # exact FirmOfferAuthorityInstanceEffectV1
  authorized_quote_request            # exact AuthorizedCoverageQuoteRequestV1
  service_profile_artifact             # exact GuarantorServiceProfileArtifactV1
  unsigned_offer_template
  exposure_admission_descriptor
  expected_portfolio_revision
}

ProviderExposureAdmissionDescriptorV1 {
  schema_version
  guarantor_agent_id
  service_profile_digest
  quote_request_digest
  coverage_id
  coverage_version
  coverage_agreement_body_digest
  coverage_terms_digest
  reservation_scope                   # exact ProviderExposureReservationScopeV1
  reservation_scope_digest
  reserved_exposure
  collateral_credit
  policy_bucket_digest
  correlation_bucket_digest
  base_portfolio_revision
  reservation_expires_at_unix
}

ProviderExposureAdmissionReceiptBodyV1 {
  schema_version
  authority_id
  guarantor_agent_id
  descriptor_digest
  authorized_action_digest
  reservation_id
  stable_action_id
  exact_request_digest
  writer_generation
  writer_fence_digest
  base_portfolio_revision
  admitted_portfolio_revision
  reserved_exposure
  state                              # reserved
  admitted_at_unix
  expires_at_unix
  authority_admission_eligibility_proof_set_digest
}

AuthorizedProviderExposureAdmissionReceiptV1 {
  body
  descriptor
  authority_admission_eligibility_proof_set
  authorizations[]
}
```

The exposure admission is also the quote request's economic-admission
checkpoint. The authority re-resolves every newly presented requester and
Agreement authorization against fresh finalized authority state at
`admitted_at_unix` and freezes the exact section 9.1 proof set in the receipt.
A historically valid request whose signer was revoked before this checkpoint
cannot reserve exposure or produce a firm offer.

`FirmOfferAuthorityInstanceEffectV1` is the exact
`canonical_effect_body` supplied to the released recoverable authority-instance
allocator; its content type, bounds, and every field above are mandatory. The
allocation request separately supplies mandate, owner approval where required,
and terminal predecessor under Semantic Action Identity V1. The returned
instance ID is the only valid `offer_id` and MUST match the issuance body's
`authority_instance_id` and exact allocation record.

The two allocation digests are not caller-controlled knobs:

```text
recipient_set_digest = Digest(
  "tos.service.agent-guarantor-firm-offer-recipient-set.v1",
  recipient_set)

reservation_scope_digest = Digest(
  "tos.service.agent-guarantor-reservation-scope.v1",
  reservation_scope)
```

The authority derives the recipient set from the exact quote request, final
Agreement participants/predicates, and permitted claimant/acceptance subjects.
Both subject arrays are canonical sorted sets and reject duplicates or a subject
not authorized by those objects. It derives the reservation scope from the
current owner, final terms, exact coverage obligation, asset/cap, assurance,
portfolio policy/correlation buckets, the owner policy's exact default-
liability disposition, and bounded reservation schedule. The disposition is a
closed `charge_off` or `retain` token and cannot be deferred to release time. The
effect, descriptor, unsigned template, and later offer carry or deterministically
project the same values. The descriptor's embedded reservation scope is byte-
identical to the effect's. Missing source objects, alternate wrappers, digest-
only inputs, or a changed field conflict before authority-instance allocation.

The preallocation template is canonical `FirmCoverageOfferBodyV1` with
`offer_id`, `reservation_id`, and `exposure_receipt_digest` set to their
respective all-zero placeholders. The issuance template is derived by replacing
`offer_id` with the allocated authority instance, deriving `reservation_id`
from that instance and the exact descriptor as specified below, and leaving the
exposure digest zero.
The authority verifies byte equality after those prescribed substitutions; its
quote, Agreement, terms, recipients, scope, and exposure must also equal the
corresponding embedded objects. This order avoids deriving the allocation ID
from bytes that already contain that ID.

`unsigned_offer_template` is the exact canonical `FirmCoverageOfferBodyV1`
with `offer_id = authority_instance_id` and
`exposure_receipt_digest = sha256:` followed by 64 zeroes. The zero digest is a
construction placeholder and is never valid in a delivered or authorized firm
offer. `exposure_admission_descriptor` is the complete canonical descriptor,
not its digest. The exact action-request digest is computed over this whole
`FirmOfferIssuanceActionBodyV1`; the Action and Writer Fence are outside it.
The embedded service-profile artifact must pass section 11 and match every
service Intent/profile field in the request, effect, descriptor, and template;
the output envelope carries those byte-identical artifact bytes.

The purpose-limited Provider authority performs this operation in one
serializable admission boundary: validate the current Writer Fence and policy,
reserve exposure, create and authorize the receipt, replace the placeholder by
the receipt envelope digest, construct and authorize the final firm offer, and
persist the complete terminal action result before returning either object. If
custody signing is a separate process, it participates through a prepared
operation keyed by the same stable action and exact request, enforces the same
writer-generation high-water, and cannot sign after cancellation or takeover.
Exposure remains reserved while signing is prepared, unknown, or ambiguous.
A coordinator that merely holds an Agent key is not permitted to bypass this
boundary or sign a firm offer directly.

`descriptor` is the exact canonical
`ProviderExposureAdmissionDescriptorV1`. A verifier recomputes
`descriptor_digest`, requires equality with the authorized receipt body, and then
checks the descriptor's Agreement, terms, amount, asset, portfolio base
revision, and reservation horizon against the firm offer. The receipt's
`expires_at_unix` is exactly the descriptor's
`reservation_expires_at_unix`. A digest without the
descriptor bytes or an immutable content-addressed descriptor is not
verifiable and cannot support a firm offer.

The owner/provider authority validates the current Writer Fence, policy,
mandate, asset bucket, counterparty, correlated exposure, outstanding offers,
active coverage, claims, and ambiguous actions in one linearized transaction.
It persists the stable action and exact request before authorizing a signature.

The reservation identity is deterministic and cannot be caller selected:

```text
reservation_id = Digest("tos.service.agent-guarantor-reservation-id.v1", {
  guarantor_agent_id,
  authority_instance_id,
  descriptor_digest
})
```

The authority derives it inside the issuance transaction; exact recovery must
return the same ID and receipt.

The full maximum aggregate payout remains reserved until exact terminal rules
allow a reduction. Eligible finalized same-asset collateral MAY reduce the
owner's net unsecured exposure but never the beneficiary-facing aggregate cap.

The receipt proves that the Guarantor's configured authority claimed to admit
the reservation. It is not proof that public assets exist, that the private
ledger cannot be restored from an old snapshot, or that a payout will occur.
`writer_generation` and `writer_fence_digest` are audit facts in the receipt;
they never enter public coverage terms or semantic identity. A takeover keeps
already admitted offers and reservations valid and blocks the stale writer
from creating new actions.

### 14.3 Firm offer

```text
FirmCoverageOfferBodyV1 {
  schema_version
  offer_id                            # exact authority_instance_id
  offer_version                       # exactly 1 in V1
  predecessor_offer_digest?           # forbidden in V1
  quote_request_digest
  service_intent_digest
  service_profile_digest
  coverage_id
  coverage_version
  guarantor_agent_id
  covered_party_agent_id
  beneficiary_agent_id
  underlying_agreement_body_digest
  covered_obligation_ids[]
  coverage_terms_digest
  coverage_agreement_body_digest
  coverage_obligation_id
  premium_obligation_ids[]
  collateral_obligation_id?
  payout_template_obligation_id
  guarantor_predicate_targets[] {
    predicate_id
    target_projection_digest
  }
  guarantor_evidence_profile          # exact ProfileRefV1
  exposure_receipt_digest
  reservation_id
  max_acceptances                    # exactly 1
  valid_from_unix
  accept_by_unix
  acceptance_processing_grace_seconds
  withdrawal_policy                   # exactly forbidden in V1
  expires_at_unix
  required_extensions[]
  optional_extensions[]
}

AuthorizedFirmCoverageOfferV1 {
  body
  authorizations[]
  exposure_receipt
  authorized_quote_request
  service_profile_artifact
}
```

V1 firm offers are irrevocable until their signed acceptance cutoff:
`withdrawal_policy` is the closed token `forbidden`. The Provider may decline
to issue an offer or let an issued offer expire, but no later policy, mandate,
message, Intent revision, key rotation, or local state can withdraw or shorten
it. A revocable indication of interest is ordinary negotiation content and is
not an `AuthorizedFirmCoverageOfferV1`. Any future conditional-withdrawal
profile requires a new offer version that signs its exact predicates, cutoff,
race order, and evidence; it cannot reinterpret V1.

The verifier recomputes the complete embedded
`AuthorizedProviderExposureAdmissionReceiptV1` envelope digest, requires it to
equal `exposure_receipt_digest`, verifies its profile-qualified authorization,
and rejects a receipt whose descriptor, authority, expiry, reservation, or
Agreement binding differs from the offer. A digest-only receipt is not a valid
firm offer.

The embedded `GuarantorServiceProfileArtifactV1` is mandatory. Its signed
lineage head's operation digest equals `service_intent_digest`; its selected
profile digest equals `service_profile_digest`; and its Provider, authorities, policy revision,
capabilities, nested profile identities, validity window, and endpoints are the
exact values used to verify the offer and exposure receipt. It is retained in
the Firm Offer Agreement evidence after acceptance. Later claim, decision,
release, and recovery verification resolves the historical profile from that
accepted evidence rather than querying the original Carrier. A digest-only
profile reference, mutable URL, or locally cached decoded structure is not
portable recovery evidence.

The envelope also embeds the exact `AuthorizedCoverageQuoteRequestV1` named by
the body. A verifier recomputes its complete envelope digest, requester
authorization, requested terms, maxima, selected profiles, parties, underlying
Agreement, and service-Intent/profile references before checking the offer.
The issuance action's quote request and the output copy are byte-identical. A
digest-only request or Provider-private request record is not portable firm-
offer evidence.

The offer is targeted and non-transferable. It satisfies only the exact
Guarantor predicate IDs and target projections listed by the final Agreement.
It cannot authorize the covered party, beneficiary, wallet, custodian,
collateral principal, data owner, or Decision Authority.

V1 deliberately has no in-place firm-offer revision protocol:
`offer_version` is exactly `1` and `predecessor_offer_digest` is absent. A
counteroffer or any second economic offer uses a newly authorized quote request,
a new `offer_id`/authority instance, a new exposure admission, and a new
reservation. Conversation metadata MAY reference an earlier offer for user
experience, but that reference has no revision, replacement, cancellation, or
authorization effect. The earlier offer remains live until its own acceptance
or section 14.4 close wins. A later schema may introduce a bounded portable
offer-lineage object; a V1 verifier rejects version zero, version greater than
one, or any predecessor field. A lost send response resolves the original
action and does not permit a price, term, recipient, or offer-ID mutation.

The exposure reservation is part of offer validity. Its
`reservation_expires_at_unix` MUST be no earlier than
`accept_by_unix + acceptance_processing_grace_seconds`, and the grace MUST be
positive, within the published service-profile maximum, and identical to the
accepted coverage terms. An offer whose receipt or reservation ends sooner is
invalid. The offer itself MUST NOT expire before the reservation horizon.

### 14.4 Pre-acceptance non-acceptance proof and exposure release

An unaccepted reservation is released through a different evidence path from
an accepted coverage. It cannot manufacture terminal claims or reuse the
post-acceptance release body from section 19.

```text
OfferNonAcceptanceEvidenceBodyV1 {
  schema_version
  authority_id
  guarantor_agent_id
  authority_instance_id
  reservation_id
  exposure_receipt_digest
  authorized_firm_offer_envelope_digest
  release_reason                       # exactly expired in V1
  issuance_action_resolution_digest
  acceptance_admission_log_id
  acceptance_admission_high_water
  acceptance_admission_log_root
  acceptance_cutoff_unix
  sequenced_by_cutoff_count
  terminal_rejected_count
  accepted_count                       # exactly 0
  pending_or_ambiguous_count            # exactly 0
  expected_reservation_revision
  prior_offer_state_revision
  resolved_offer_state_revision
  authorized_action_digest
  stable_action_id
  exact_request_digest
  writer_generation
  writer_fence_digest
  resolved_at_unix
}

AuthorizedOfferNonAcceptanceEvidenceV1 {
  body
  authorized_firm_offer                 # exact issued offer
  issuance_action_resolution
  authorizations[]
}

OfferNonAcceptanceResolutionActionBodyV1 {
  schema_version
  authority_instance_id
  authorized_firm_offer
  issuance_action_resolution
  release_reason
  acceptance_cutoff_unix
  expected_reservation_revision
  expected_offer_state_revision
  target_offer_state_revision
}

PreAcceptanceExposureReleaseEvidenceProjectionV1 {
  schema_version
  authority_instance_id
  reservation_id
  exposure_receipt_digest
  authorized_firm_offer_envelope_digest
  release_reason
  non_acceptance_evidence_digest
}

PreAcceptanceExposureReleaseActionBodyV1 {
  schema_version
  release_variant                       # exactly pre_acceptance
  authorized_non_acceptance_evidence
  release_evidence_projection
  expected_portfolio_revision
  target_portfolio_revision
  expected_reserved_exposure
}

PreAcceptanceExposureReleaseReceiptBodyV1 {
  schema_version
  authority_id
  guarantor_agent_id
  authority_instance_id
  reservation_id
  exposure_receipt_digest
  authorized_firm_offer_envelope_digest
  release_reason
  non_acceptance_evidence_digest
  release_evidence_projection_digest
  authorized_action_digest
  stable_action_id
  exact_request_digest
  writer_generation
  writer_fence_digest
  base_portfolio_revision
  released_portfolio_revision
  released_exposure
  remaining_reserved_exposure          # exactly 0
  state                                # released_unaccepted
  released_at_unix
}

AuthorizedPreAcceptanceExposureReleaseReceiptV1 {
  body
  authorized_non_acceptance_evidence
  release_evidence_projection
  authorizations[]
}
```

The offer-acceptance admission authority creates non-acceptance evidence in
the same linearized domain that could admit acceptance. Its `authority_id`
equals the exact service profile's `lifecycle_authority_id`, and its evidence
uses the final Agreement terms' `acceptance_authority_profile`. It freezes the
complete admission log through the stated high-water and proves that every request
sequenced by `acceptance_cutoff_unix` is terminally rejected, with no accepted,
pending, unknown, or ambiguous request. The exact issuance `ActionResolution`
is embedded and verified; a digest, timer, empty inbox, or Provider-local query
result is insufficient. The authority executes one
`commercial.quote.close` action, atomically freezes the log, wins the offer-
state compare-and-swap, persists the action resolution, and authorizes this
evidence. `resolved_offer_state_revision` and the close request's target are
exactly the prior or expected revision plus one; all action and Writer Fence
fields must match the admitted action. Timeout recovery resolves or retries
only that stable action.

The presence and time matrix is exact:

| Reason | Firm offer | Close authorization | Additional rule |
| --- | --- | --- | --- |
| `expired` | required | signed offer expiry rule and current Writer Fence | the cutoff is `accept_by_unix`; all by-cutoff requests are resolved and release is no earlier than `reservation_expires_at_unix` |

This path carries the complete `authorized_firm_offer` and obtains the exposure
receipt only through that offer. A second direct receipt is forbidden.
`ResolveNonAcceptanceExposureSourceV1(evidence)` returns exactly one verified
`AuthorizedProviderExposureAdmissionReceiptV1` and its required verified offer,
requires all body digests and the issuance resolution to match that path, and
rejects absent, duplicated, body-only, or conflicting carriage.

For an issued offer, `sequenced_by_cutoff_count = terminal_rejected_count`,
`accepted_count = 0`, and `pending_or_ambiguous_count = 0`. Any unknown send,
unresolved admission, stale log root, or mismatched reservation keeps the
exposure reserved.

Failure before a complete firm offer is authorized is not a non-acceptance
branch. `FirmOfferIssuanceActionBodyV1` has one atomic positive result containing
both the exposure receipt and firm offer. If any signing participant refuses or
permanently fails before that result commits, the issuance action becomes a
generic terminal negative result with zero profile components and atomically
unwinds its private `RESERVED_UNSIGNED` portfolio reservation. Any receipt
signature produced during preparation is inadmissible without the same action's
accepted positive result and cannot support an Agreement or release action. An
unknown or ambiguous issuance result keeps the private reservation and must be
resolved under the same stable action; it cannot be converted into `expired` or
a new offer.

The exposure authority consumes
`PreAcceptanceExposureReleaseActionBodyV1` under the existing
`portfolio.release` identity. It recomputes the projection from the exact
embedded non-acceptance envelope and its resolved source path, requires the
non-acceptance body's expected reservation
revision to equal the currently reserved record, requires
`target_portfolio_revision = expected_portfolio_revision + 1`, atomically
writes the action resolution and
decrements exactly `expected_reserved_exposure`, and returns the permanent
authorized receipt. The receipt is the only interoperable proof that an issued,
unaccepted offer's reservation was released. A terminal-negative issuance has
no portable exposure component and uses only the atomic private unwind above.
The receipt cannot close an accepted coverage or
authorize collateral release. The release action and receipt carry the
non-acceptance envelope exactly once and contain no second receipt or offer
copy; every downstream verifier uses the same resolver.

## 15. Linearized acceptance and activation

### 15.1 Why generic off-chain authorization delivery is insufficient

A covered party may sign before `accept_by_unix` but deliver after the
Guarantor believes the offer expired and releases exposure. Local timestamps
or message arrival order cannot safely choose a winner. Acceptance, expiry,
and reservation release therefore share one Provider-side
linearization domain, unless an exact selected contract Adapter provides that
ordering.

### 15.2 Acceptance request and receipt

```text
CoverageAcceptanceRequestBodyV1 {
  schema_version
  coverage_agreement_body_digest
  authorized_firm_offer_envelope_digest
  complete_authorization_evidence_set_digest
  accepting_subject
  submission_authorization_profile
  created_at_unix
  expires_at_unix
}

AuthorizedCoverageAcceptanceRequestV1 {
  body
  coverage_agreement_body
  authorization_evidence_set
  authorizations[]
}

CoverageAcceptanceReceiptBodyV1 {
  schema_version
  authority_id
  coverage_agreement_body_digest
  authorized_firm_offer_envelope_digest
  complete_authorization_evidence_set_digest
  reservation_id
  transition_evidence_projection_digest
  prior_reservation_revision
  prior_offer_state_revision
  accepted_offer_state_revision
  admitted_coverage_revision
  prior_claim_filing_state             # exactly uninitialized
  accepted_claim_filing_state          # exactly not_open
  prior_claim_filing_state_revision    # exactly 0
  accepted_claim_filing_state_revision # exactly 1
  authorized_action_digest
  stable_action_id
  exact_request_digest
  writer_generation
  writer_fence_digest
  received_at_unix
  accepted_at_unix
  state                              # accepted
  authority_admission_eligibility_proof_set_digest
}

AuthorizedCoverageAcceptanceReceiptV1 {
  body
  authorized_acceptance_request
  transition_evidence_projection
  authority_admission_eligibility_proof_set
  authorizations[]
}
```

`authorization_evidence_set` is an
`GuarantorAgreementAuthorizationEvidenceSetV1` whose recomputed digest MUST
equal `complete_authorization_evidence_set_digest`; the acceptance-request
authorization therefore commits the exact set without embedding it in the body.
An omitted, added, duplicate, reordered, or wrapper-substituted evidence object
invalidates the request.
The envelope embeds the exact coverage Agreement body and requires its digest,
participants, predicates, obligation IDs, and terms to match the body and every
evidence element. Its authorization set contains exactly one
`GuarantorFirmOfferAgreementEvidenceV1` satisfying the Guarantor predicate; that
object's complete embedded firm offer is the sole canonical offer-carriage path
for acceptance and all wrappers that embed the acceptance request.
`submission_authorization_profile` is frozen in the body and must be permitted
by the Agreement for `accepting_subject`; it cannot be selected by inspecting
which proof happened to arrive.

The authority admits acceptance only when:

- the complete authorized request was durably received and sequenced by the
  admission authority under its clock with
  `created_at_unix <= received_at_unix <= accept_by_unix`;
- `received_at_unix <= accepted_at_unix <= min(request.expires_at_unix,
  checked_add(accept_by_unix, acceptance_processing_grace_seconds),
  exposure_receipt.expires_at_unix, offer.expires_at_unix,
  quote_request.expires_at_unix)`; all bounds are inclusive and resolved from
  the offer's single canonical carriage path;
- `created_at_unix <= expires_at_unix`, and request creation is no earlier than
  the accepted offer's `valid_from_unix`; request expiry never extends any
  offer, quote-request, reservation, or processing-grace boundary;
- the firm offer, receipt, Agreement body, predicates, and all authorization
  evidence verify exactly;
- the accepting subject and every newly presented Agreement-authorization
  principal remain eligible in fresh finalized authority state at
  `accepted_at_unix`, and the exact section 9.1 proof set is frozen in the
  receipt;
- `max_acceptances = 1` has not been consumed;
- the reservation remains live and matches the admitted portfolio revision;
- the current writer and action authorization are valid; and
- the same offer has no conflicting accepted Agreement or request.

A request sequenced by `accept_by_unix` but not linearized by its own
`expires_at_unix` is terminally rejected. If the exact action outcome is pending
or ambiguous at that boundary, the authority resolves that same action and
returns its stored pre-expiry result if one exists; it never manufactures a new
post-expiry acceptance or extends consent because the offer grace remains open.

Acceptance and expiry consume the same offer-state revision. The
acceptance action's `expected_offer_state_revision` must equal the current
issued offer revision and `target_offer_state_revision` is its checked
successor. In the same serializable transaction the authority advances that
revision to `accepted`, consumes the one-use reservation, advances the coverage
revision, and creates the deterministic claim-filing state key from
`uninitialized` revision `0` to `not_open` revision `1`. The receipt records all
four filing-state values and they equal the action fields. A pre-existing state,
another revision, or a receipt that omits this initialization is invalid. The
coverage, offer, reservation, filing-state, and action writes commit in the same
serializable transaction. A concurrent close can therefore win the same CAS or
lose it, but cannot produce terminal non-acceptance evidence alongside a valid
acceptance receipt.

The Provider-side admission action is carried separately in an
`AuthorizedActionV1`; neither its stable action ID nor its exact request digest
is embedded in the acceptance-request bytes from which that request digest is
computed. The exact action request binds the complete authorized acceptance
envelope, expected reservation and offer revisions, target coverage revision,
and the exact `uninitialized/0 -> not_open/1` claim-filing CAS.
The receipt envelope embeds that byte-identical acceptance request and
transition projection. The authority and every later verifier extract the firm
offer from the request's one Guarantor Agreement-evidence element, recompute its
complete-envelope digest, and require equality with the receipt body and
projection. A second top-level offer copy is forbidden. This single-carriage
rule lets a verifier reproduce acceptance without a Provider acceptance
database while avoiding a maximum-size service-profile lineage twice.

The same request is idempotent. Same action ID with different bytes is
`conflict`. A timeout remains `unknown` and is resolved through the same action.
Expiry may release the reservation only after this admission
domain proves that no concurrent acceptance was admitted. Provider silence,
message absence, or quote expiry alone is insufficient. The proof and release
must use the canonical section 14.4 objects and the same reservation revision.

During `acceptance_processing_grace_seconds`, no new acceptance may enter after
the signed cutoff, but release remains blocked while every request durably
sequenced by the cutoff is admitted or terminally rejected. The admission must
finish by `reservation_expires_at_unix`; otherwise the offer enters
`AMBIGUOUS`, retains exposure, and requires recovery rather than release.

### 15.3 Activation

Acceptance creates a coverage commitment but does not necessarily activate it.
Activation requires:

- the exact underlying Agreement is complete and authorized;
- every covered obligation exists and is in an eligible state;
- the coverage Agreement has complete profile-qualified authorization;
- the firm offer and acceptance receipt verify;
- any up-front fee prerequisite has terminal evidence;
- the selected collateral profile has current, finalized, exclusive lock
  evidence;
- when its exact control disclosure is `third_party_control_asserted`, the
  activation carries current profile-qualified collateral-control evidence;
- an `independently-enforceable` selection proves full same-asset beneficiary
  capacity and the complete Guarantor-control-deleted claim-to-payout path;
- the coverage start and remaining validity windows are satisfiable; and
- for lower assurance, the current Provider portfolio still preserves the
  accepted exposure; for `independently-enforceable`, the accepted exposure
  receipt plus current full-capacity collateral and operational-independence
  evidence are sufficient and Provider-private portfolio availability cannot
  veto activation.

```text
CoverageActivationEvidenceBodyV1 {
  schema_version
  authority_id
  coverage_agreement_body_digest
  coverage_obligation_id
  coverage_state_domain_digest
  authorization_evidence_set_digest
  underlying_agreement_body_digest
  underlying_authorization_evidence_set_digest
  authorized_firm_offer_envelope_digest
  acceptance_receipt_digest
  exposure_receipt_digest
  fee_prerequisite_evidence_set_digest?
  collateral_evidence_set_digest?
  collateral_control_evidence_digest?
  operational_independence_evidence_set_digest?
  selected_assurance_level
  selected_claim_profile_digest
  selected_collateral_profile_digest?
  transition_evidence_projection_digest
  authorized_action_digest
  stable_action_id
  exact_request_digest
  writer_generation
  writer_fence_digest
  prior_coverage_revision
  activated_coverage_revision
  prior_claim_filing_state             # exactly not_open
  activated_claim_filing_state         # exactly open
  prior_claim_filing_state_revision
  activated_claim_filing_state_revision
  resulting_coverage_end_commitment_digest
  activated_at_unix
  coverage_ends_at_unix
  authority_admission_eligibility_proof_set_digest
}

AuthorizedCoverageActivationEvidenceV1 {
  body
  stage_action_admission_evidence     # exact PortableStageActionAdmissionEvidenceV1
  underlying_agreement_body
  authorized_acceptance_receipt
  coverage_end_commitment            # exact scheduled CoverageEndCommitmentV1
  underlying_authorization_evidence_set
  fee_prerequisite_evidence_set?
  collateral_evidence_set?
  collateral_control_evidence?
  operational_independence_evidence_set?
  transition_evidence_projection
  authority_admission_eligibility_proof_set
  authorizations[]
}

ActivationAdmissionCutProofV1 {
  schema_version
  coverage_agreement_body_digest
  activation_admission_log_id
  activation_cutoff_unix
  admission_high_water
  admission_log_root
  entries[]                           # exact GuarantorAdmissionLogEntryV1 prefix
  accepted_count
  pending_or_ambiguous_count
}

GuarantorAdmissionLogEntryV1 {
  sequence                            # contiguous, starts at 1
  stable_action_id
  exact_request_digest
  received_at_unix                   # authority receipt time; monotonic
  log_root_after
  resolution                         # exact ActionResolutionV1
}

TerminalPrerequisiteFailureEvidenceV1 {
  prerequisite_id
  failure_outcome
  terminal_failure_evidence_profile       # exact Agreement-rule ProfileRefV1
  terminal_failure_evidence               # complete immutable evidence envelope
  terminal_failure_authorizations[]       # exact profile-qualified quorum
}

PreActivationMutualCancellationBodyV1 {
  schema_version
  coverage_agreement_body_digest
  coverage_obligation_id
  authorized_firm_offer_envelope_digest
  acceptance_receipt_digest
  activation_cutoff_unix
  expected_coverage_revision
  cancellation_nonce
  created_at_unix
  expires_at_unix
}

CoverageNonActivationReasonEvidenceV1 {
  schema_version
  coverage_agreement_body_digest
  coverage_obligation_id
  reason
  activation_admission_cut_proof_digest
  prerequisite_failure_evidence[]?        # canonical nonempty set
  mutual_cancellation_body?               # exact canonical body
  mutual_cancellation_authorization_evidence[]? # exact predicate-qualified set
}

CoverageNonActivationEvidenceBodyV1 {
  schema_version
  authority_id
  coverage_agreement_body_digest
  coverage_obligation_id
  coverage_state_domain_digest
  authorized_firm_offer_envelope_digest
  acceptance_receipt_digest
  exposure_receipt_digest
  reason                              # prerequisite_failed,
                                      # activation_window_expired,
                                      # mutually_cancelled
  activation_cutoff_unix
  activation_admission_log_id
  activation_admission_high_water
  activation_admission_log_root
  pending_activation_action_count     # exactly 0
  activation_admission_cut_proof_digest
  non_activation_reason_evidence_digest
  fee_resolution_evidence_set_digest?
  collateral_non_activation_evidence_set_digest?
  transition_evidence_projection_digest
  authorized_action_digest
  stable_action_id
  exact_request_digest
  writer_generation
  writer_fence_digest
  prior_coverage_revision
  resolved_coverage_revision
  prior_claim_filing_state             # exactly not_open
  resulting_claim_filing_state         # exactly not_open
  prior_claim_filing_state_revision
  resulting_claim_filing_state_revision # equals prior; no filing mutation
  resolved_at_unix
  authority_admission_eligibility_proof_set_digest
}

AuthorizedCoverageNonActivationEvidenceV1 {
  body
  stage_action_admission_evidence     # exact PortableStageActionAdmissionEvidenceV1
  authorized_acceptance_receipt
  activation_admission_cut_proof
  non_activation_reason_evidence
  fee_resolution_evidence_set?
  collateral_non_activation_evidence_set?
  transition_evidence_projection
  authority_admission_eligibility_proof_set
  authorizations[]
}
```

An activation wrapper is a recoverable aggregation, not a substitute for the
underlying evidence. A verifier recomputes every present set digest against the
body, checks that each Agreement set names its respective Agreement, and
independently resolves and verifies each selected profile and terminal evidence
object or immutable descriptor. The fee set uses purpose
`coverage-activation-fee` and the coverage Agreement body as context. The
collateral set uses purpose `coverage-activation-collateral`, contains the exact
Adapter-authorized collateral envelope, and uses the coverage obligation and
position binding as context. A bare transaction hash, body-only collateral
digest, mutable locator, or Provider-private record cannot activate coverage.
For non-activation, it additionally recomputes
`non_activation_reason_evidence_digest` under
`tos.service.agent-guarantor-non-activation-reason-evidence.v1`, requires the
embedded structured object to match the exact Agreement rule and reason, and
applies the exhaustive matrix below. A generic evidence-set digest or lifecycle
authority assertion cannot substitute for that object.

The activation envelope embeds the exact underlying Agreement body and
authorized acceptance receipt. The latter already carries the exact coverage
Agreement and, through its acceptance request's Guarantor Agreement evidence,
the sole complete firm offer. The verifier follows that canonical path and
recomputes every body/envelope digest named by the activation body; the firm
offer supplies the exact exposure receipt and authenticated service-profile
lineage. Duplicate top-level copies of either the coverage Agreement or firm
offer are forbidden. A fresh verifier needs no Carrier, Provider endpoint, or
private activation database.
It also recomputes the embedded transition projection, requires its digest to
equal `transition_evidence_projection_digest`, and verifies that the projection
contains exactly the prerequisite roles released in section 20.1.
The activation or non-activation authority re-resolves every newly admitted
prerequisite, collateral-control, and operational-independence signer against
fresh finalized authority state at its authority-generated result time and
freezes the exact section 9.1 eligibility proof set. Evidence signed before a
revocation but first presented afterward cannot activate coverage or prove the
opposite branch.

Both branches mutate the Agreement's exact `coverage_state_domain_digest`.
Activation requires the action's `target_coverage_end_commitment` to be the
cycle-free `scheduled` commitment derived from the exact Agreement; the result
embeds it and commits its digest. Non-activation stores the
`never_activated` commitment only after the complete non-activation envelope is
available, using that envelope digest as end evidence. As with cancellation,
the result body cannot recursively contain its own complete-envelope digest.
The activation/non-activation CAS, evidence envelope, durable coverage record,
and every later claim or close operation must agree on the same domain and
commitment branch.

The same transaction also verifies the claim-filing state initialized by the
exact acceptance receipt. Activation requires `not_open` at the receipt's
revision, advances that revision by exactly one, and records the atomic
`not_open -> open` transition in both its action and evidence body. Only that
accepted activation transition permits initial claim ingress. Non-activation
requires the same `not_open` state and revision but preserves both byte-for-byte;
its action and evidence body record equal prior/resulting values. It cannot
open, freeze, or silently advance claim filing. The later `never_activated`
filing-close mutation consumes that preserved revision and advances it once to
`frozen`. These rules let an offline verifier derive every filing-state
predecessor from the acceptance, activation or non-activation, and filing-close
envelopes without consulting a Provider database.

The activation body's selected claim and collateral profile digests exactly
equal the coverage terms and resolve again against the offer-bound service
profile. For `unsecured-signed`, the collateral digest and collateral evidence
set are absent. For both collateral levels they are present; for
`independently-enforceable`, the evidence additionally proves the full-capacity
and offline-execution invariants in sections 8 and 18.

The control-evidence field and digest are present if and only if the selected
collateral profile's byte-identical disclosure uses
`third_party_control_asserted`; they are forbidden for every other relationship
token. The verifier applies the closed disclosure matrix from section 10,
checks the complete control-evidence envelope and historical quorum, recomputes
its digest under
`tos.service.agent-guarantor-collateral-control-evidence-envelope.v1`, and
requires its Agreement, collateral obligation, selected profile, disclosure,
Adapter, operators, and controller roots to equal the activation inputs. The
evidence must still be current at `activated_at_unix`. A profile cannot retain
the third-party label by omitting stale evidence, substituting a local
observation, or downgrading the token after Agreement authorization.

For `independently-enforceable`, the operational-independence evidence set is
also required and uses purpose `coverage-operational-independence` with the
coverage Agreement body as context. It carries the exact Adapter authority
configuration and control-resolution proofs needed to reproduce the deletion
test in section 12.1 within `maximum_control_evidence_age_seconds`. Both lower
levels omit it. The selected claim/collateral Adapter rechecks the immutable
binding, every stage's Action Authority and Writer-Fence configuration, and the
deletion test at initial claim admission, every revision, filing
close, every non-decision transition (including challenge admission and close),
terminal decision, decision application, payout, coverage cancellation, and
coverage closure. A Guarantor outage cannot
force traffic through a Guarantor endpoint, prevent the remaining quorum from
acting, or authorize residual release.

For that assurance, activation uses the exact `coverage_activation` stage and
non-activation resolution uses the distinct `coverage_non_activation` stage.
Both entries name the same immutable activation-log/admission-state domain but
have their own Action Authority, Writer Fence, generation high-water, and
resolution binding. The Agreement-bound coverage-operation Adapter exposes
both canonical actions directly after Guarantor control deletion. It derives
the accepted exposure and Agreement from portable envelopes, freezes and
verifies every by-cutoff activation resolution, and never queries a Guarantor-
private database to decide either branch. Reusing one stage entry for the other
or maintaining two activation heads is invalid.

Acceptance is a real commitment but is not active coverage. Every activation
attempt is admitted or rejected in the same revisioned authority domain and
append-only activation log. At the activation cutoff—exactly
`coverage_starts_at_unix`—the authority first resolves every attempt durably
sequenced by the cutoff. It may authorize non-activation evidence only when no
activation was accepted, no activation action is pending or ambiguous, the
frozen high-water and root verify, and the selected reason has exact profile-
qualified evidence. Provider silence, a local timer, an absent prerequisite,
or an unknown attempt is insufficient and leaves coverage ambiguous with
exposure reserved.

`ActivationAdmissionCutProofV1` is canonical and complete through its stated
high-water. Its `entries[]` are contiguous and ordered; each entry carries the
exact durable `ActionResolutionV1` plus the sequence, authority receipt time,
stable identity, exact request digest, and resulting prefix root needed by an
offline verifier. The verifier recomputes the log root and both
counts. Non-activation requires `accepted_count = 0` and
`pending_or_ambiguous_count = 0`; the proof's fields must exactly equal the
redundant log fields in `CoverageNonActivationEvidenceBodyV1`, and its canonical
digest must equal `activation_admission_cut_proof_digest`. For lower assurance,
the selected lifecycle authority's authorization states exactly that limited
assurance. An `independently-enforceable` selection additionally requires the
Adapter-verifiable cut and control-deletion guarantees promised by its profile.
A signed root and zero count without the exact entries and selected verifier are
not portable evidence of absence.

The empty root and each successor root use the released domain
`tos.service.agent-guarantor-admission-log-root.v1`. The empty value commits
`(activation_admission_log_id, sequence = 0)`; each successor commits the prior
root and the entry's domain ID, sequence, stable action ID, exact request
digest, and receipt time. An implementation-private root domain is not valid
portable evidence.

The non-activation reason matrix is exhaustive and normative:

| Reason | Required reason evidence | Authorization and quorum | Forbidden evidence |
| --- | --- | --- | --- |
| `prerequisite_failed` | A canonical nonempty `prerequisite_failure_evidence[]`; every element names one Agreement rule, carries the complete terminal-failure envelope, and has an outcome in that rule's permitted set | Each element independently satisfies exactly the rule's evidence profile, authority-subject set, and quorum; at least one terminal failure is required and unknown, pending, absent, or merely expired evidence is not failure | mutual-cancellation body/evidence |
| `activation_window_expired` | The exact zero-acceptance `ActivationAdmissionCutProofV1`; the reason object repeats only its digest and contains neither optional branch | The portable `coverage_non_activation` stage action/fence admission at `resolved_at_unix >= activation_cutoff_unix` is the authority; no discretionary lifecycle signature may replace the cut | prerequisite failures and mutual-cancellation body/evidence |
| `mutually_cancelled` | Exact `PreActivationMutualCancellationBodyV1` plus a complete canonical authorization-evidence set | Every Agreement rule's `cancellation_authorization_predicate_ids[]` is satisfied exactly once against the same cancellation-body digest; all required subjects consent, irrespective of a smaller ordinary quorum | prerequisite failures; ordinary chat, transcript hashes, unilateral cancellation, or model-generated assent |

For `prerequisite_failed`, duplicate prerequisite IDs, evidence for an ID absent
from the selected Agreement rule, a body-only digest, or two competing outcomes
fail closed. The evidence need not list still-pending prerequisites because one
terminal failure makes activation impossible, but it cannot characterize them
as failed. For `mutually_cancelled`, the cancellation body is valid only before
the activation cutoff, has
`created_at_unix <= authorization.validation_time <= expires_at_unix <=
activation_cutoff_unix`, and binds the exact acceptance receipt and expected
coverage revision. Its nonce prevents a prior cancellation from being replayed
against another accepted coverage. For every row, the reason in the structured
evidence, action projection, result body, and Agreement rule is byte-identical.
The canonical reason-evidence object and every nested envelope must fit the
Agreement's non-activation closure-capacity maximum.

The non-activation envelope derives the exact coverage Agreement and firm offer
from its embedded acceptance receipt's single canonical carriage path,
acceptance receipt, cut proof, and all prerequisite/fee/collateral sets named by
its body. Every digest, acceptance/reservation binding, cutoff, reason, and
revision is recomputed. Those objects are inputs to the canonical non-activation
action before its request and action identities are derived; the result cannot
load or replace them after admission. Its embedded projection is byte-identical
to the action projection and recomputes the body's
`transition_evidence_projection_digest`.

When collateral was provisionally locked, the non-activation wrapper's
`collateral_non_activation_evidence_set` uses purpose
`coverage-collateral-non-activation`. It proves that activation did not consume
the position, freezes the current position state, and establishes which later
release transition is eligible. It is not collateral-release evidence and does
not move or unlock the position.

`NOT_ACTIVATED_CONFIRMED` proves that the accepted version never became active.
It leaves claim filing in `NOT_OPEN`; no incident or claim is eligible. The
separate `never_activated` filing-close mutation in section 17.3 must consume
the exact non-activation envelope, atomically move `NOT_OPEN` to `FROZEN`, and
create the canonical zero-high-water, empty-log
`AuthorizedClaimFilingCloseReceiptV1`. Non-activation evidence alone is not a
filing-close receipt and cannot perform or pre-empt that CAS.
Fee refund or retention follows the accepted Agreement policy. Collateral
unlock occurs only after the signed zero-claim terminal set through the later
Adapter transition. Provider exposure release follows those dispositions and
the ordinary rollback-resistant release receipt. Only final coverage resolution
then records `closed_not_activated`. That terminal state is distinct from
cancellation of active coverage, Guarantor default, exhaustion, and ordinary
expiry.

### 15.4 Active-coverage cancellation

Cancellation is a typed, revisioned coverage mutation. A chat message, model
statement, local policy decision, or cancellation object presented only during
final closure cannot end incident eligibility.

```text
CoverageCancellationPolicyV1 {
  schema_version
  policy_id
  branches[] {
    cancellation_branch
    permitted_requester_subjects[]
    request_authorization_profile
    request_authorization_quorum_rule
    evidence_profile?
    earliest_after_activation_seconds
    maximum_admission_delay_seconds
  }
}

CoverageCancellationRequestBodyV1 {
  schema_version
  coverage_agreement_body_digest
  coverage_obligation_id
  cancellation_policy_digest
  cancellation_branch
  requester_subject
  effective_not_before_unix
  effective_not_after_unix
  cancellation_evidence_set_digest?
  created_at_unix
  expires_at_unix
}

AuthorizedCoverageCancellationRequestV1 {
  body
  coverage_agreement_body
  cancellation_evidence_set?
  authorizations[]
}

CoverageCancellationReceiptBodyV1 {
  schema_version
  authority_id
  coverage_agreement_body_digest
  coverage_obligation_id
  coverage_state_domain_digest
  prior_coverage_end_commitment_digest
  authorized_cancellation_request_digest
  cancellation_policy_digest
  cancellation_branch
  effective_at_unix
  incident_eligibility_ends_at_unix
  claim_filing_ends_at_unix
  transition_evidence_projection_digest
  authorized_action_digest
  stable_action_id
  exact_request_digest
  writer_generation
  writer_fence_digest
  prior_coverage_revision
  ended_coverage_revision
  state                              # exactly coverage_ended
  admitted_at_unix
  authority_admission_eligibility_proof_set_digest
}

AuthorizedCoverageCancellationReceiptV1 {
  body
  stage_action_admission_evidence     # exact PortableStageActionAdmissionEvidenceV1
  authorized_cancellation_request
  transition_evidence_projection
  authority_admission_eligibility_proof_set
  authorizations[]
}
```

`GuarantorCoverageTermsV1.cancellation_policy` is the exact canonical policy,
not prose or a mutable locator. Its digest is computed under
`tos.service.agent-guarantor-cancellation-policy.v1`. Branches form a sorted,
unique, nonempty set. A branch deterministically fixes eligible requester
subjects, exact authorization profile and quorum, optional evidence profile,
and timing bounds. The request embeds the exact Agreement and, when required,
an evidence set with purpose `coverage-cancellation` and context equal to the
Agreement body digest. The verifier recomputes every digest and rejects a
branch, subject, profile, quorum, or evidence set not fixed by that policy.
`authorized_cancellation_request_digest` is the complete request-envelope
digest under `tos.service.agent-guarantor-cancellation-request-envelope.v1`.
The receipt embeds that byte-identical request, derives the sole complete
Agreement through `authorized_cancellation_request.coverage_agreement_body`,
recomputes the transition projection, and is authorized at `admitted_at_unix`
by the selected lifecycle or independent-stage authority. The action and
receipt forbid a second Agreement copy. A body digest, signature alone, or
request rewrapped with different authorization evidence is invalid.
Every cancellation-request subject is also re-resolved against fresh finalized
authority state at `admitted_at_unix`; the receipt's exact section 9.1 proof set
must cover every newly admitted authorization and match the receipt action,
domain, sequence, and time.

Let `activated_at_unix` be read from the exact current authorized activation
evidence. The authority computes, with checked addition:

```text
earliest_branch_admission_unix =
  activated_at_unix + branch.earliest_after_activation_seconds

latest_branch_admission_unix =
  request.created_at_unix + branch.maximum_admission_delay_seconds
```

Admission is allowed only from `active`, strictly before the scheduled
`coverage_ends_at_unix`, and when all of the following hold:

```text
activated_at_unix <= created_at_unix <= admitted_at_unix
effective_not_before_unix <= effective_not_after_unix <= expires_at_unix
max(created_at_unix,
    earliest_branch_admission_unix,
    effective_not_before_unix)
  <= admitted_at_unix
  <= min(latest_branch_admission_unix,
         effective_not_after_unix,
         expires_at_unix)
```

Overflow, an inverted interval, a request created before activation, admission
after the creation-relative delay, or admission before the activation-relative
earliest time fails closed. Thus the same policy and request bytes have one
timing interpretation across implementations. The authority sets
`effective_at_unix = admitted_at_unix` and
`incident_eligibility_ends_at_unix = min(coverage_ends_at_unix,
effective_at_unix)`. V1 never backdates cancellation. The original
`claim_filing_ends_at_unix` remains unchanged so accrued incidents can still be
filed and resolved.
The action's exact expected end commitment must be the current `scheduled`
value for the same Agreement, obligation, and
`coverage_state_domain_digest`; its cutoff equals the Agreement schedule and
its evidence field is absent. The receipt copies that domain digest and prior
commitment digest. A cancellation request cannot select another domain or
present an already shortened commitment.

The cancellation action and claim admission compare the same coverage
revision. The winner advances it once; an unknown result must be resolved, and
a stale loser must re-read and revalidate before a permitted terminal
successor. After cancellation wins, an
initial claim is eligible only when its authenticated
`occurred_at_unix <= incident_eligibility_ends_at_unix` and the original filing
cutoff remains open. Later incidents fail. Cancellation does not freeze claim
filing, erase an accrued claim, decide a claim, release collateral or exposure,
or enter final `cancelled`. A prepared or unknown action projects locally as
`cancellation_resolving`; a successfully admitted receipt moves coverage to
`coverage_ended`, while accrued obligations continue through final closure.

The durable coverage projection records
`incident_eligibility_ends_at_unix`, `coverage_end_reason`, and
`coverage_end_evidence_digest`. For this path they are the admitted effective
time, `accepted_cancellation`, and complete cancellation-receipt envelope
digest. Only after the complete receipt envelope and its authorization exist
does the authority construct the resulting `CoverageEndCommitmentV1` from those
values and store it atomically with the receipt and ended revision. The receipt
cannot contain its own complete-envelope digest; this one-way construction is
intentional and avoids a digest cycle. Every later coverage-revision mutation
must carry or derive that exact commitment and preserve it byte-for-byte.

Scheduled expiry is deliberately not another mutation or authority statement
in V1. Incident eligibility already ends at the immutable
`coverage_ends_at_unix` in the authorized Agreement, whether or not any process
is online. A local projection may display that the scheduled cutoff passed, but
it cannot create a receipt, advance the coverage revision, release value, or
compete with a claim. Normal-expiry closure is authorized only after the exact
filing-close receipt exists; the closure authority derives `normal_expiry`
from the embedded Agreement, activation evidence, scheduled cutoff, its own
linearization time, and the absence of an accepted cancellation. This avoids a
second clock-driven state head while retaining portable, profile-qualified
closure evidence. Cancellation admitted before the strict cutoff remains the
end branch; at or after the cutoff a new cancellation is invalid.

For lower assurance, the Agreement-selected lifecycle authority admits and
authorizes the receipt. For `independently-enforceable`, the exact
`coverage_cancellation` stage Action Authority, Writer Fence, high-water,
resolver, and direct Adapter route perform the same mutation without the
Guarantor. The receipt remains historical evidence even if keys rotate later.

## 16. Conditional settlement template

### 16.1 Required generic extension

The current generic `AgreementObligationV1.amount` and `BillingTermsV1`
describe a fixed accepted value obligation. Materializing
`maximum_aggregate_payout` through those fields would incorrectly make the
maximum possible loss immediately payable.

V1 therefore introduces a profile-qualified generic template:

```text
ProfileQualifiedSettlementParametersV1 {
  schema_version
  settlement_adapter_profile          # exact ProfileRefV1
  payout_destination_digest
  adapter_parameters                   # bounded canonical bytes
}

ConditionalSettlementTemplateV1 {
  template_id
  agreement_obligation_id
  condition_profile
  authorized_decision_profile
  payer_agent_id
  payee_agent_id
  asset
  maximum_per_instance
  maximum_aggregate_amount
  maximum_instances
  first_sequence
  settlement_adapter_profile          # exact ProfileRefV1
  settlement_parameters               # exact ProfileQualifiedSettlementParametersV1
  settlement_parameters_digest
  payout_destination_binding
  materialization_domain
  cancellation_policy_digest
  dispute_policy_digest
}
```

The template is the canonical subject of the non-current-value
`guarantor.payout.template` obligation. It is not a `payment` obligation and
does not produce a `SettlementObligationV1` at Agreement acceptance. A small
generic Agreement rule and verifier extension must state that only a terminal
object satisfying `condition_profile` and `authorized_decision_profile` may
materialize finite instances.

The current released generic `SettlementObligationV1` carries
`settlement_adapter_uri`, not a full `ProfileRefV1`; this profile does not
reinterpret or silently change those bytes. The template's exact settlement
parameters are hashed under
`tos.service.agent-guarantor-settlement-parameters.v1`, repeat the same
ProfileRef and Agreement-fixed destination, and satisfy
`settlement_parameters_digest`. A materialized generic obligation sets its
`settlement_adapter_uri` to exactly
`settlement_adapter_profile.profile_uri` and copies that digest. Version and
profile digest remain authoritative from the accepted template. Adapter
dispatch receives the complete ProfileRef and exact parameter bytes from the
Agreement plus materialization set; URI-only dispatch is invalid. The same URI
with another version or profile digest is a conflict. A future generic native
ProfileRef field requires a versioned generic schema and vectors rather than an
in-place V1 reinterpretation.

### 16.2 Deterministic payout lines

A terminal approving decision contains a finite, decision-local schedule. It
does not choose coverage-global payout sequence numbers: those numbers depend
on which concurrently admitted terminal decision wins the later application
CAS and therefore cannot be known safely when the Decision Authority signs.

```text
ClaimPayoutLineV1 {
  decision_line_index
  amount
  payout_destination_digest
  not_before_after_terminal_close_seconds
  due_after_terminal_close_seconds
  expires_after_terminal_close_seconds
}
```

`decision_line_index` starts at 1, is contiguous within the exact decision, and
orders `payout_lines[]`. The line digest is computed under
`tos.service.agent-guarantor-payout-line.v1`. Duplicate, missing, zero,
reordered, or noncontiguous indexes are invalid. The Decision Authority signs
the amount, destination, and relative time bounds. It cannot sign absolute
payout times because decision admission and the later terminal challenge close
have not yet linearized. The three offsets are canonical unsigned seconds and
must satisfy:

```text
0 <= not_before_after_terminal_close_seconds
  <= due_after_terminal_close_seconds
  <= expires_after_terminal_close_seconds
due_after_terminal_close_seconds <= payout_deadline_seconds
expires_after_terminal_close_seconds = checked_add(
  due_after_terminal_close_seconds,
  adapter_recovery_window_seconds)
```

The accepted payout template deterministically supplies those offsets. A
Decision Authority may not shorten, extend, or convert them to wall-clock
timestamps.

The application transaction constructs exactly one materialized line for each
decision-local line:

```text
MaterializedPayoutLineV1 {
  payout_sequence
  predecessor_materialized_payout_line_digest?
  claim_decision_body_digest
  terminal_claim_state_transition_receipt_digest
  decision_line_index
  claim_payout_line                  # exact ClaimPayoutLineV1
  not_before_unix
  due_at_unix
  expires_at_unix
  obligation_instance_id
}
```

`payout_sequence` starts at 1 and is contiguous across the entire coverage
obligation. The first-ever materialized line omits
`predecessor_materialized_payout_line_digest`; every later line commits the
digest of the immediately preceding `MaterializedPayoutLineV1` under
`tos.service.agent-guarantor-materialized-payout-line.v1`. A decision with
multiple lines chains them in decision-line order. Two equal-amount lines
remain distinct through their decision digest, local index, and global
sequence. The application authority derives the absolute values only from the
exact terminal `challenge_close` receipt embedded by the decision-application
action:

```text
not_before_unix = checked_add(
  terminal_close_receipt.body.transitioned_at_unix,
  claim_payout_line.not_before_after_terminal_close_seconds)
due_at_unix = checked_add(
  terminal_close_receipt.body.transitioned_at_unix,
  claim_payout_line.due_after_terminal_close_seconds)
expires_at_unix = checked_add(
  terminal_close_receipt.body.transitioned_at_unix,
  claim_payout_line.expires_after_terminal_close_seconds)
```

For an ordinary decision lineage, all three values must be no later than the
Agreement's `terminal_resolution_deadline_unix`. For a lineage whose first
post-late-close decision is exactly `late_recovery_terminal_fallback`, the
materializer instead requires all three values to be no later than
`late_recovery_terminal_deadline_unix`; the exact authorized decision chain and
filing-close receipt make that branch mechanically distinguishable. No other
path may use the contingency deadline. Overflow or insufficient remaining time
rejects the earlier decision admission under the applicable continuation-
budget rule, not the already terminal close. For each materialized line:

```text
obligation_instance_id = Digest("tos.service.agent-guarantor-payout-instance.v1", {
  coverage_agreement_body_digest,
  payout_template_obligation_id,
  claim_decision_body_digest,
  terminal_claim_state_transition_receipt_digest,
  decision_line_index,
  claim_payout_line_digest,
  not_before_unix,
  due_at_unix,
  expires_at_unix,
  payout_sequence,
  predecessor_materialized_payout_line_digest_or_zero
})
```

The materializer verifies:

- the accepted coverage Agreement and template;
- the admitted claim and unbroken claim revision chain;
- terminal profile-qualified decision authority;
- the exact terminal `challenge_close` receipt, its transition time, and the
  checked relative-to-absolute time derivation above;
- contiguous decision-local line indexes and application-assigned global payout
  sequences;
- exact asset, payer, payee, destination, and Adapter;
- exact equality of `first_sequence`, per-instance, aggregate, and instance-
  count template limits with the accepted coverage terms under section 12.1;
- `sum(payout_lines) = approved_amount`;
- per-claim, maximum-instance, maximum-claim-count, and aggregate caps;
- prior approved and paid totals using checked arbitrary-precision arithmetic;
- no duplicate decision, line, evidence, or obligation instance; and
- the expected coverage and claim revisions in one atomic admission.

It then produces ordinary `SettlementObligationV1` instances. Actual payment
reuses `payment.direct`, `settlement.external`, or another released Adapter;
terminal payment evidence is applied through existing settlement resolution.
A Claim Decision is never payout evidence.

The output is carried canonically as:

```text
MaterializedPayoutObligationSetV1 {
  schema_version
  coverage_agreement_body_digest
  payout_template_obligation_id
  authorized_claim_decision_digest
  terminal_claim_state_transition_receipt_digest
  materialization_state              # materialized or not_applicable
  first_payout_sequence?
  last_payout_sequence?
  materialized_lines[]               # complete MaterializedPayoutLineV1 objects
  obligations[]                      # complete SettlementObligationV1 objects
}

TerminalPayoutEvidenceSetV1 {
  schema_version
  coverage_agreement_body_digest
  claim_id
  authorized_claim_decision_digest
  materialized_payout_obligation_set_digest
  disposition                       # resolved, defaulted, or not_applicable
  approved_amount
  paid_amount
  defaulted_amount
  outstanding_amount                 # exactly zero in this terminal object
  payout_execution_evidence[]        # complete sequence-ordered AuthorizedGuarantorPayoutExecutionEvidenceV1 set
  terminal_settlement_evidence_set   # exact CanonicalGuarantorEvidenceSetV1
}

AuthorizedGuarantorPayoutExecutionEvidenceV1 {
  schema_version
  obligation_instance_id
  stage_action_admission_evidence    # exact PortableStageActionAdmissionEvidenceV1
  agreement_payment_evidence         # exact AgreementPaymentEvidenceV1
  collateral_evidence?               # exact only for the collateral-backed composite
}

GuarantorAgreementPaymentActionBodyV1 {
  schema_version
  payment_request                    # tagged exact AgreementPaymentRequestV1, V2, or V3
  settlement_obligation              # exact Materialized SettlementObligationV1
  materialized_payout_obligation_set # exact containing set
}

CoverageTerminalPayoutEvidenceEntryV1 {
  claim_admission_sequence
  terminal_payout_evidence_set_digest # digest of the exact set in the matching terminal bundle
}

CoverageTerminalPayoutEvidenceSetV1 {
  schema_version
  coverage_agreement_body_digest
  authorized_terminal_claim_set_evidence_digest
  entries[]                          # ordered by admission sequence
}
```

For unsecured and non-payout-collateral paths, the selected settlement Adapter
admits `GuarantorAgreementPaymentActionBodyV1` through the Agreement-bound
`payout_execution` stage. `payment.direct` accepts only the released V1 direct
request form, `payment.domain-bound` accepts only V3, and ordinary
`settlement.external` accepts only V2. The
payment request, obligation, containing materialized set, Agreement, decision,
sequence, payer, beneficiary, asset, amount, destination, Adapter, stable ID,
and time bounds must agree exactly. The accepted mutation atomically emits one
`AuthorizedGuarantorPayoutExecutionEvidenceV1` containing the exact generic
payment evidence and the stage Action/Fence evidence; `collateral_evidence` is
absent. A generic payment result emitted outside this profile operation cannot
close a Guarantor payout merely because its economic fields happen to match.
The collateral-backed composite in section 18.1.1 uses its distinct request and
requires the collateral field.

`materialized_lines[]` and `obligations[]` have equal length and one-to-one
order. Each generic obligation copies its matching line's global
`payout_sequence` into `sequence`, uses the prior materialized line's
`obligation_instance_id` as `predecessor_instance_id` when a predecessor
exists, and copies the exact decision-authorized amount, destination, and time
policy while setting its `not_before`, `due`, and `expires` fields to the three
materialized absolute values. The signed relative offsets remain in the
matching materialized line and the exact terminal-close digest binds their
origin. The set rejects an omitted, duplicate, reordered, foreign, or
conflicting line or instance. Its digest uses
`tos.service.agent-guarantor-payout-obligation-set.v1`. A terminal claim-set reference
therefore commits the exact materialized obligations rather than an
implementation-local list hash.

`payout_execution_evidence[]` has exactly one entry for each materialized
payout obligation, in payout-sequence order, and is empty only for
`not_applicable`. Each wrapper resolves the same obligation instance, request,
stable action, amount, destination, Adapter profile, and terminal transfer
evidence as its matching entry in `terminal_settlement_evidence_set`. The
collateral-backed form also embeds the byte-identical collateral evidence from
the atomic composite result; every other form forbids it. The wrapper's stage
evidence is exactly `payout_execution` and makes Action/Fence admission
portable without changing or weakening the generic payment-evidence schema.
A missing wrapper, an extra wrapper, a different ordering, or reuse across two
obligation instances is invalid.

A terminal denial is explicit rather than represented by a missing digest or a
fabricated zero-value payment. Its obligation set uses
`materialization_state = not_applicable`, omits both sequence fields, and has
`obligations = []`; because it binds the exact authorized denial, it has a
claim-specific digest. Its `TerminalPayoutEvidenceSetV1` uses
`disposition = not_applicable`, binds that exact empty obligation set, sets all
four amount fields to canonical zero, and has
an exact claim-context terminal-settlement evidence set with `items = []`. An
approval uses `materialized`, both sequence fields, and at least one obligation;
its `approved_amount` equals the exact obligation-set sum and always satisfies
`approved_amount = paid_amount + defaulted_amount + outstanding_amount` under
checked same-asset arithmetic. A terminal object requires
`outstanding_amount = 0`. `resolved` requires `paid_amount = approved_amount` and
`defaulted_amount = 0`. `defaulted` requires `defaulted_amount > 0` and exact
Agreement-selected terminal default evidence for every unpaid portion; a
timeout or locally written-off invoice is not such evidence. Every obligation
must have exactly one profile-qualified paid or default terminal disposition.
`evidence_required` and `disputed` cannot produce either terminal object.
The nested evidence set always uses purpose `claim-terminal-payment` and the
materialized obligation-set digest as context; its inline objects or immutable
descriptors must resolve every materialized obligation exactly once.

The coverage aggregate is a digest index, not a second carriage of those
objects. For every contiguous claim admission sequence, its entry digest is
exactly
`Digest("tos.service.agent-guarantor-terminal-payout-evidence-set.v1",
matching_bundle.terminal_payout_evidence_set)`, where the matching bundle is in
the bound `AuthorizedTerminalClaimSetEvidenceV1`. The aggregate verifier first
verifies that terminal envelope, derives all entries in sequence order, and
requires byte equality with the aggregate. A missing bundle, repeated full
payout set, reordered digest, foreign claim, or equal digest supplied without
the bound terminal envelope fails closed. This preserves one physical copy of
each potentially large terminal payout set while retaining portable
verification after every mutable database is removed.

## 17. Claims and decisions

### 17.1 Evidence manifest and claim

```text
ClaimEvidenceDescriptorV1 {
  predicate_id
  evidence_profile
  content_type
  content_digest
  content_size
  disclosure_policy_digest
}

ClaimEvidenceManifestV1 {
  schema_version
  items[]
  total_declared_bytes
}

TriggeredObligationSetV1 {
  schema_version
  underlying_agreement_body_digest
  obligation_ids[]                    # nonempty canonical set
}

OtherRecoveryItemV1 {
  recovery_item_id
  source_kind                         # guarantee, insurance, escrow, refund,
                                      # restitution, legal_recovery, or other
  source_subject
  related_instrument_digest?
  recovery_status                     # pending, receivable, received, denied,
                                      # waived, or exhausted
  amount_received                     # exact AtomicAmountV1
  amount_receivable                   # exact AtomicAmountV1
  evidence_predicate_ids[]            # canonical references into the manifest
}

OtherRecoveryDeclarationV1 {
  schema_version
  coverage_agreement_body_digest
  coverage_obligation_id
  underlying_agreement_body_digest
  claim_revision
  beneficiary_agent_id
  incident_key_digest
  coverage_asset
  recovery_items[]                    # canonical sorted unique set; may be empty
  declared_at_unix
}

CoverageClaimBodyV1 {
  schema_version
  claim_id
  claim_revision
  predecessor_claim_digest?
  coverage_agreement_body_digest
  coverage_obligation_id
  underlying_agreement_body_digest
  triggered_obligation_set            # exact TriggeredObligationSetV1
  claimant_subject
  claimant_authorization_profile
  beneficiary_agent_id
  incident_key_digest
  occurred_at_unix
  claimed_amount
  evidence_manifest_digest
  other_recovery_declaration_digest
  payout_destination_digest
  created_at_unix
  expires_at_unix
}

AuthorizedCoverageClaimV1 {
  body
  evidence_manifest
  other_recovery_declaration
  authorizations[]
}

ClaimSubmissionIngressActionBodyV1 {
  schema_version
  authorized_claim                   # exact AuthorizedCoverageClaimV1
  target_ingress_state               # exactly received
}

ClaimSubmissionIngressReceiptBodyV1 {
  schema_version
  authority_id
  coverage_agreement_body_digest
  coverage_obligation_id
  claim_id
  claim_revision
  ingress_kind                       # initial or revision, derived from claim
  claim_body_digest
  authorized_claim_envelope_digest
  ingress_state_domain_digest
  claim_ingress_log_id
  claim_ingress_sequence
  prior_claim_ingress_log_root
  admitted_claim_ingress_log_root
  ingress_slot_revision              # exactly 1
  state                              # exactly received
  authorized_action_digest
  stable_action_id
  exact_request_digest
  writer_generation
  writer_fence_digest
  received_at_unix
  authority_admission_eligibility_proof_set_digest
}

AuthorizedClaimSubmissionIngressReceiptV1 {
  body
  stage_action_admission_evidence     # exact PortableStageActionAdmissionEvidenceV1
  authorized_claim                   # sole complete claim carriage
  authority_admission_eligibility_proof_set
  authorizations[]
}

ClaimIngressResolutionEntryV1 {
  claim_ingress_sequence
  received_at_unix                   # exact log-leaf time required to
                                     # recompute the portable ingress root
  ingress_action_resolution          # exact terminal ActionResolutionV1
  claim_ingress_receipt_digest?
  resolution_kind                    # ingress_rejected, claim_admitted,
                                     # or claim_rejected
  claim_admission_action_resolution?
  claim_admission_receipt_digest?
}

ClaimIngressAdmissionCutProofV1 {
  schema_version
  coverage_agreement_body_digest
  coverage_obligation_id
  cut_kind                           # initial_filing or decision_snapshot
  claim_id?                          # required only for decision_snapshot
  revision_epoch?                    # required only for decision_snapshot
  prior_epoch_state_revision?        # required only for decision_snapshot
  frozen_epoch_state_revision?       # prior + 1 on freeze; unchanged only for
                                      # a late-recovery challenge successor
  claim_ingress_log_id
  ingress_cutoff_unix                # filing cutoff, or authority freeze time
  admission_high_water
  admission_log_root
  entries[]                          # exact contiguous selected ingress-log cut
  admitted_claim_count
  rejected_ingress_or_claim_count
  pending_or_ambiguous_count         # exactly 0
}

ClaimSubmissionAuthorityInstanceEffectV1 {
  schema_version
  authorized_claim_ingress_receipt   # exact ingress receipt; resolves the claim
  authorized_coverage_activation_evidence # sole path to accepted coverage Agreement
  authorized_coverage_cancellation_receipt? # exact current early-end evidence
  expected_coverage_end_commitment   # exact CoverageEndCommitmentV1
  expected_coverage_revision
}

ClaimSubmissionActionBodyV1 {
  schema_version
  authority_instance_id
  authority_instance_record
  authority_instance_effect          # exact ClaimSubmissionAuthorityInstanceEffectV1
}
```

The authorized claim body is an assertion and contains no action identity or
digest of bytes that contain that identity. Before business admission, the
claim passes the separately recoverable `conditional.claim.ingress` mutation.
The ingress sink derives Agreement, obligation, claim ID, revision, and body
digest from `authorized_claim`; it creates one absent-to-`received` slot in the
stage's exact ingress state domain and returns the authorized receipt above.
The stable ingress identity omits authorization-wrapper bytes, so the same
claim ID and revision with another body or wrapper conflicts through the exact
request digest instead of creating another inbox item. The receipt proves only
durable authenticated receipt; it does not prove incident eligibility, consume
a claim sequence, or make the Claimant currently eligible at later admission.
At `received_at_unix`, the ingress authority nevertheless re-resolves every
newly presented Claimant authorization against finalized authority state and
freezes the exact section 9.1 eligibility-proof set in the receipt. Admission
performs the same check again at its later cut; neither proof substitutes for
the other.

The later claim-admission action is nevertheless context-free and portable.
Its authority-instance effect embeds the exact authorized activation envelope;
the verifier follows its acceptance receipt to the sole canonical coverage
`AgentAgreementBodyV1`, complete Agreement authorization evidence, firm offer,
service-profile lineage, claim/cap/timing rules, covered obligations, and payout
destination. `authorized_coverage_cancellation_receipt` is present if and only
if the current end commitment is `accepted_cancellation`, is absent for the
scheduled branch, and is forbidden for `never_activated`. The action recomputes
the exact current `CoverageEndCommitmentV1` and expected coverage revision from
those envelopes. Thus section 23 may keep `required_context_types[]` empty:
after loss of Provider or sink state, a verifier still has every immutable
commercial input; only the current CAS head is queried. A body-only Agreement,
digest-only activation, omitted cancellation receipt, second Agreement copy,
or wrapper substitution fails. Closure-capacity builders include these nested
complete envelopes in every maximum claim-admission request and downstream
copy.

The ingress sink derives `ingress_kind = initial` exactly for revision 1 with no
predecessor and `revision` otherwise. Initial ingress uses the one Agreement-
bound coverage ingress log; revision ingress uses the deterministic per-claim
child log. Each successful ingress appends one never-reused sequence and root
step in the same CAS as the receipt slot. All logs share the stage's bounded
state namespace, and the aggregate sequenced action count cannot exceed
`maximum_claim_ingress_actions`. A request beyond the bound is rejected before
sequencing and cannot create a receipt or hidden pending item.

At filing cutoff the ingress authority freezes the exact initial-ingress
high-water and root in `ClaimIngressAdmissionCutProofV1`. Every sequence through
that cut carries a terminal ingress `ActionResolutionV1`; every successful
ingress receipt additionally has exactly one terminal claim-admission action
and is either admitted with its exact receipt or terminally rejected. Pending
or ambiguous count must be zero. Thus a timely initial claim cannot be hidden
behind delayed admission, while a post-cutoff initial ingress is ineligible. An
already admitted claim may still use its bounded revision-ingress child log
during the Agreement-authorized evidence/review window; terminal claim-set
verification requires every such receipt to be consumed or terminally rejected.
The cut proof is bounded by `maximum_claim_ingress_cut_proof_bytes` and the
complete ingress receipt, including its sole claim and authorization proofs, by
`maximum_claim_ingress_receipt_envelope_bytes`.

An ingress slot has the closed states `absent -> prepared -> received`,
`rejected`, or `ambiguous`; `ambiguous` may resolve only to the terminal result
of that same stable action and exact request. The authority chooses
`received_at_unix` and requires `created_at_unix <= received_at_unix <=
expires_at_unix`. Exact retry returns the byte-identical receipt, different
bytes under the stable ID conflict, and takeover queries the bound resolver
before any retry. A prepared or ambiguous initial ingress sequenced no later
than the filing cutoff blocks the ingress cut and therefore filing close. Local
queue absence, Messenger acknowledgement, timeout, or writer loss cannot reject
or omit it.

The complete canonical `ClaimSubmissionAuthorityInstanceEffectV1` is the
ID-free `canonical_effect_body` supplied to the released recoverable authority-
instance allocator. It embeds that exact ingress receipt, not another claim
copy. The exact authorized claim envelope is resolved only through the receipt;
the expected coverage revision and exact current coverage-end commitment are
the remaining known inputs to `allocation_request_digest`. The returned
`authority_instance_id` is then inserted only into
`ClaimSubmissionActionBodyV1`, together with the exact allocation record and
unchanged effect. The authority record's effect digest MUST equal the
recomputed effect digest, and its purpose MUST be
`conditional.claim.submit`.

The submission side effect is authorized separately:
`conditional.claim.submit` derives its stable action ID from the released
semantic fields including the allocated `authority_instance_id` and
`claim_body_digest`, while `exact_request_digest` is computed over the
canonical `ClaimSubmissionActionBodyV1`. The surrounding `AuthorizedActionV1`,
Writer Fence, transport metadata, retry counters, and resulting admission
receipt are not part of those action-body bytes. This dependency direction is
acyclic and constructible:

```text
canonical claim body
  -> claim body digest
  -> resolved claimant authorization and authorized-envelope digest
  -> canonical claim-ingress action and stable action ID
  -> authorized claim-ingress receipt
  -> ID-free claim-submission authority-instance effect
  -> recoverable allocation request and authority_instance_id
  -> canonical claim-submission action body
  -> exact request digest and stable action ID
  -> Authorized Action and delivery
```

The admission sink derives the Agreement, obligation, claim-body digest, and
complete authorized-claim envelope digest only from the effect's embedded
ingress receipt. It verifies that receipt's action, request, stage binding,
state-domain, authority, and sole embedded claim before allocation. It derives
the authority instance only from the verified allocation record; the caller
cannot supply disagreeing duplicates. The stable semantic key uses these
derived fields, while the exact request commits the allocation record, complete
manifest, destination binding, and authorization set.

An implementation MUST reject a claim body containing `authority_instance_id`,
`stable_action_id`, `exact_request_digest`, an admission receipt, or another
value derived from the claim body's own digest. It MUST also reject an
allocation effect containing either the allocated ID, allocation record, or a
second direct claim copy. Exact ingress resubmission resolves the same ingress
action and receipt. Exact admission resubmission preserves that receipt,
allocation request, allocated ID, action ID, request bytes, and claim bytes. A
revised claim has its own predecessor-linked body, ingress action and receipt,
then separately allocated and admitted submission action; it is not a retry of
the earlier revision.

The envelope carries the exact canonical `ClaimEvidenceManifestV1` and
`OtherRecoveryDeclarationV1`; the verifier recomputes
`evidence_manifest_digest` and `other_recovery_declaration_digest` under
`tos.service.agent-guarantor-claim-evidence-manifest.v1` and
`tos.service.agent-guarantor-other-recovery-declaration.v1` respectively before
admitting the claim. The recovery declaration repeats and must equal the claim
body's coverage Agreement, coverage obligation, underlying Agreement, claim
revision, beneficiary, incident key, and the Agreement's coverage asset.
`declared_at_unix <= created_at_unix`; a later update requires a normal
predecessor-linked claim revision rather than mutable side data.

`ClaimEvidenceManifestV1.items[]` is sorted by unique `predicate_id`, contains
no more than the selected claim profile's `maximum_evidence_items`, and every
descriptor resolves one predicate permitted by that profile and the triggering
obligation. `total_declared_bytes` is not a claimant estimate: the verifier
recomputes it as the checked unsigned sum of every `items[].content_size`,
requires exact equality, and requires the result to be no greater than
`maximum_evidence_bytes`. Each content object must reproduce its descriptor's
exact digest and size under the bounded retrieval policy before it is used.
Overflow, an empty required manifest, a duplicate predicate, a zero or
unbounded size where the evidence profile forbids it, count or byte excess, or
a declared total different from the recomputed sum fails before claim ingress
admission. The maximum counts logical evidence items once; transport wrappers,
chunk requests, redirects, retries, and compressed bytes cannot create a second
budget or replace the descriptor's uncompressed canonical content size.

`recovery_items[]` is sorted by unique `recovery_item_id`, is bounded by the
selected claim profile's `maximum_evidence_items`, and every amount is a
nonnegative atomic amount in exactly `coverage_asset`. Each evidence predicate
ID resolves exactly once in the embedded manifest; duplicate or foreign
references fail. `pending`, `denied`, and `waived` require both amounts to be
zero; `receivable` requires zero received and positive receivable;
`received` requires positive received and zero receivable; and `exhausted`
requires zero receivable while permitting a nonnegative historical received
amount. Checked addition is used for every policy aggregate. An empty array is
the one canonical
declaration of no known other recovery; a missing object, null, prose, or a
digest-only unavailable declaration is invalid. For indemnity coverage, the
Agreement-selected `other_coverage_policy` and benefit-calculation profile
consume this exact declaration. For fixed-benefit coverage they define whether
it is informational or affects coordination, but the declaration remains
mandatory. The signed declaration proves what the Claimant asserted, not that
undisclosed recovery does not exist; omission and misrepresentation remedies
come only from the accepted policy and evidence process, never from a global
coverage database.

Manifest entries describe separately authorized, bounded evidence handoffs and
do not make their private content public or inline. A digest-only unavailable
manifest cannot be admitted.

The accepted trigger profile deterministically projects one real-world or
protocol event into `incident_key_digest`; it binds every event coordinate that
changes claim identity and forbids claimant-selected randomness. The covered
obligation IDs are carried in one exact `TriggeredObligationSetV1`.
`obligation_ids[]` is nonempty, sorted by canonical ID bytes, duplicate-free,
and a subset of the accepted coverage terms' `covered_obligation_ids[]`; its
Agreement digest equals both the claim and coverage terms. Its digest is
exactly:

```text
triggered_obligation_set_digest = Digest(
  "tos.service.agent-guarantor-triggered-obligation-set.v1",
  triggered_obligation_set)
```

The set is embedded in the signed claim body, so two codecs cannot choose a
different wrapper, order, or implicit Agreement. Claim identity is exactly:

```text
claim_id = Digest("tos.service.agent-guarantor-claim-id.v1", {
  coverage_agreement_body_digest,
  coverage_obligation_id,
  incident_key_digest,
  beneficiary_agent_id,
  triggered_obligation_set_digest
})
```

The authority-allocated instance distinguishes the authorized submission side
effect but is absent from both the claim body and claim identity. The Action
Authority permits another instance for the same `claim_id` only for the exact
next predecessor-linked claim revision under the Agreement's revision policy;
it cannot allocate a second initial submission for the same incident.
Retrying through another transport or taking over the writer resolves the
original allocation request and cannot create a second claim. A caller-chosen
UUID or nonconforming incident projection is invalid. Supplemental evidence
retains `claim_id`, increments `claim_revision`, and binds the exact
predecessor; it does not create a second claim for the same incident.

The Claimant authorization proves only that the subject submitted the assertion.
It does not prove occurrence time, loss, evidence truth, coverage eligibility,
decision, or payout.

`claimant_authorization_profile` MUST be one of the exact profiles accepted by
the coverage terms for that typed Claimant and must resolve the Claimant-to-
participant relationship. The authorization envelope cannot select a profile
that is absent from the body or use an Agent signature as a substitute for a
required wallet, custody, contract, or quorum profile.

`payout_destination_digest` MUST equal the exact Agreement-fixed
`PayoutDestinationV1` digest. The Claimant supplies no replacement destination,
and the claim envelope carries no destination locator. The verifier already has
the raw bounded destination bytes from the accepted coverage Agreement and
passes those exact bytes to materialization and the selected Adapter.

### 17.2 Claim admission

The Agreement-selected claim admission authority admits a claim through a
stable action and returns an authorized receipt. It may be the Guarantor-side
lifecycle authority at a lower assurance level; for
`independently-enforceable` it is the Guarantor-control-deleted Adapter quorum
defined in section 12.1:

```text
ClaimAdmissionReceiptBodyV1 {
  schema_version
  authority_id
  coverage_agreement_body_digest
  coverage_obligation_id
  claim_id
  authorized_claim_envelope_digest
  claim_submission_ingress_receipt_digest
  authority_instance_id
  authority_instance_allocation_request_digest
  authorized_action_digest
  stable_action_id
  exact_request_digest
  prior_coverage_revision
  admitted_coverage_revision
  prior_coverage_end_commitment_digest
  resulting_coverage_end_commitment_digest
  prior_claim_revision
  admitted_claim_revision
  admission_kind                     # initial or revision
  claim_admission_log_id
  claim_admission_sequence
  initial_claim_admission_receipt_digest?
  claim_revision_log_id
  claim_revision_admission_sequence
  predecessor_revision_admission_receipt_digest?
  prior_claim_admission_log_root
  admitted_claim_admission_log_root
  prior_claim_revision_log_root
  admitted_claim_revision_log_root
  writer_generation
  writer_fence_digest
  admitted_at_unix
  authority_admission_eligibility_proof_set_digest
}

ClaimRevisionAdmissionLeafV1 {
  claim_id
  claim_revision_admission_sequence
  authorized_claim_envelope_digest
  predecessor_revision_admission_receipt_digest?
}

AuthorizedClaimAdmissionReceiptV1 {
  body
  stage_action_admission_evidence     # exact PortableStageActionAdmissionEvidenceV1
  authorized_claim_ingress_receipt   # sole path to exact admitted claim
  coverage_end_commitment            # exact preserved CoverageEndCommitmentV1
  authority_instance_record          # exact released allocation record
  authority_admission_eligibility_proof_set
  authorizations[]
}
```

The receipt resolver reconstructs the exact ID-free
`ClaimSubmissionAuthorityInstanceEffectV1` from
`authorized_claim_ingress_receipt`, the embedded `coverage_end_commitment`, and
`prior_coverage_revision`, verifies the ingress action and receipt, verifies the
allocation record and its allocation-request digest, and requires its allocated
ID to equal the receipt and the registered semantic action. Both commitment
digests in the receipt equal the recomputed embedded commitment digest. It
requires `claim_submission_ingress_receipt_digest` to equal the complete nested
receipt-envelope digest and rejects a missing, alternate, duplicated, or second
claim/allocation path.

Admission verifies claimant authority both historically at the signed claim
time and against the exact fresh authority-admission cut in section 9.1,
filing window, covered obligation,
incident and claim uniqueness, evidence descriptors, amount bounds, state,
Writer Fence, and aggregate claim-count policy. Claim admission and coverage
cancellation compare and update the same coverage revision. One wins; the loser
resolves or conflicts rather than guessing from message order. Scheduled expiry
has no mutation to race: the authority evaluates the claim's authenticated
incident time against the immutable inclusive Agreement interval and evaluates
submission against the filing cutoff. An accrued incident remains admissible
after the scheduled coverage end until filing closes.

For an initial claim, the embedded ingress receipt's `received_at_unix` must be
no later than `claim_filing_ends_at_unix`, and this admission's
`admitted_at_unix` must be no later than
`checked_add(claim_filing_ends_at_unix,
claim_ingress_resolution_grace_seconds)`. These are independent checks: timely
ingress does not authorize late claim admission. If a prepared or ambiguous
admission first attempts to linearize after the grace endpoint, it resolves as
a terminal rejection with no claim-log or coverage mutation. Late recovery may
return an already stored receipt whose `admitted_at_unix` was within the bound,
but cannot mint a backdated receipt.

For an initial claim, checked time ordering is exactly
`coverage_starts_at_unix <= occurred_at_unix <= created_at_unix <=
admitted_at_unix <= expires_at_unix`, and `occurred_at_unix` is no later than
the current `CoverageEndCommitmentV1.incident_eligibility_ends_at_unix`.
Therefore a claim that wins the CAS before cancellation is already accrued at
that linearization point; a claimant cannot reserve a future incident and then
carry it across a later cancellation. Every supplemental revision preserves
`claim_id`, `incident_key_digest`, `occurred_at_unix`, beneficiary, and triggered
obligation set byte-for-byte, has a later or equal `created_at_unix`, and is
checked against the same preserved end commitment. A future-dated incident,
backdated revision, or change to an incident coordinate fails before consuming
a claim or closure-capacity slot.

Initial and revision admission read the exact Agreement-bound
`coverage_state_domain_digest` and compare the embedded end commitment in the
same CAS as the coverage revision and claim-log roots. They advance the
coverage revision but preserve the end commitment byte-for-byte. After accepted
cancellation, no claim admission or revision may restore `active`, lengthen the
incident cutoff, replace the reason or evidence, or return to the scheduled
branch.

The same admission transaction enforces `claim_closure_capacity`. It measures
the complete authorized claim envelope, checks the per-claim revision count,
and durably charges the corresponding worst-case bundle allowance before
advancing either log. Later decision, state-transition, and payout admissions
consume only their pre-reserved bounded slots. A rejected or exact duplicate
action consumes no new capacity; an ambiguous admitted action retains its slot
until exact resolution. Restoring an older journal, changing writers, or
deleting a Carrier cannot restore a consumed slot. No admitted initial claim or
revision may make the section 19.6 envelope exceed the Agreement-bound byte
ceiling.

The coverage-level admission log counts distinct claims, not revisions. For an
`initial` admission, claim revision is 1, the prior revision is zero, revision
predecessors are absent, and the authority atomically allocates the next never-
reused contiguous `claim_admission_sequence`. It creates the per-claim
`claim_revision_log_id` at sequence 1. For a `revision`, the receipt retains the
original claim ID, coverage-level sequence, revision-log ID, and initial receipt
digest; it allocates no new coverage-level sequence and consumes no additional
`maximum_claims` slot. It increments both claim revision and revision-admission
sequence by exactly one. `CoverageClaimBodyV1.predecessor_claim_digest` is the
canonical predecessor claim **body** digest under
`tos.service.agent-guarantor-claim.v1`, never a complete envelope, manifest,
receipt, or signature digest. The new receipt's
`predecessor_revision_admission_receipt_digest` separately commits the complete
authorized predecessor-receipt envelope.

Every authorized admission receipt embeds the byte-identical ingress receipt
that its action consumed. That receipt carries the sole
`AuthorizedCoverageClaimV1`. The authority recomputes the
complete claim-envelope digest and requires equality with
`authorized_claim_envelope_digest`, then derives the claim ID, Agreement,
revision, predecessor, manifest, and authorization fields from that object.
The nested claim's revision equals `admitted_claim_revision`. The submission
action's effect and admission receipt contain the same ingress receipt bytes.
A direct second claim, digest-only claim or ingress receipt, alternate wrapper,
or claim that differs from the ingress action is invalid.

An initial admission advances the coverage-level claim-admission root and moves
its new per-claim revision root from the canonical empty root to revision 1. A
revision leaves the coverage-level high-water and root unchanged and advances
only that claim's revision root. Every prior/resulting root is committed by the
receipt and checked in the same CAS as the stated revisions.

The per-claim revision log is a cycle-free hash chain. Its canonical empty root
is `Digest("tos.service.agent-guarantor-claim-revision-log-root.v1", {
claim_id, sequence: 0})`. For sequence `n > 0`, the authority derives the exact
`ClaimRevisionAdmissionLeafV1` from the authorized claim resolved through the
embedded ingress receipt and already final predecessor receipt, computes its
leaf digest, and sets:

```text
revision_log_root_n = Digest(
  "tos.service.agent-guarantor-claim-revision-log-root.v1", {
    claim_id,
    sequence: n,
    prior_root: revision_log_root_(n-1),
    leaf_digest
  })
```

The current receipt digest is absent from its own leaf and root. Sequence 1
omits the predecessor receipt; every later leaf names the exact complete prior
receipt envelope, and its ingress-resolved claim names the prior canonical
claim-body digest. A gap, fork, reordered claim, changed manifest or authorization, or
body-only reconstruction produces another root and fails closed.

The initial-claim log is append-only. Each admitted claim has a separate append-
only revision log. A rejected submission consumes neither sequence; an exact
retry returns the byte-identical receipt; a committed sequence is never reused.
A supplemental revision may be admitted after filing close only during the
Agreement-authorized evidence or review window and only for an already admitted
claim ID. Every admitted revision is closure-visible and applies one CAS over
both the current claim revision and shared coverage revision; both advance in
the same transaction. No implementation may classify a revision as merely
local and leave the coverage revision unchanged.
Terminal claim-set evidence proves the frozen initial-claim high-water and root
plus every claim's final revision-log high-water and root.

### 17.3 Claim-filing close

Filing close is a distinct linearized mutation. It freezes which claim IDs may
exist while admitted claims may still be under evidence review, challenge, or
payment. It never creates terminal claim-set evidence.

```text
ClaimFilingCloseActionBodyV1 {
  schema_version
  coverage_agreement_body_digest
  coverage_obligation_id
  claim_admission_log_id
  claim_ingress_admission_cut_proof  # exact ClaimIngressAdmissionCutProofV1
  filing_close_reason                 # normal or never_activated
  filing_cutoff_unix
  expected_coverage_state
  expected_coverage_end_commitment_digest
  coverage_end_reason                 # normal_expiry, accepted_cancellation,
                                      # or never_activated
  activation_evidence_digest?
  coverage_cancellation_receipt_digest?
  non_activation_evidence_digest?
  expected_coverage_revision
  target_coverage_revision
  expected_claim_filing_state_revision
  target_claim_filing_state           # exactly frozen
  expected_claim_admission_high_water
  expected_claim_admission_log_root
  transition_evidence_projection
}

ClaimFilingCloseReceiptBodyV1 {
  schema_version
  authority_id
  coverage_agreement_body_digest
  coverage_obligation_id
  coverage_state_domain_digest
  coverage_end_commitment_digest
  claim_admission_log_id
  claim_ingress_admission_cut_proof_digest
  frozen_claim_ingress_high_water
  frozen_claim_ingress_log_root
  filing_close_reason
  filing_cutoff_unix
  prior_coverage_state
  coverage_end_reason
  incident_eligibility_ends_at_unix?
  coverage_end_evidence_digest?
  activation_evidence_digest?
  coverage_cancellation_receipt_digest?
  non_activation_evidence_digest?
  frozen_claim_admission_high_water
  frozen_claim_admission_log_root
  prior_coverage_revision
  closed_coverage_revision
  prior_claim_filing_state
  resulting_claim_filing_state        # exactly frozen
  prior_claim_filing_state_revision
  resulting_claim_filing_state_revision
  transition_evidence_projection_digest
  authorized_action_digest
  stable_action_id
  exact_request_digest
  writer_generation
  writer_fence_digest
  closed_at_unix
}

AuthorizedClaimFilingCloseReceiptV1 {
  body
  stage_action_admission_evidence     # exact PortableStageActionAdmissionEvidenceV1
  coverage_end_commitment            # exact current CoverageEndCommitmentV1
  claim_ingress_admission_cut_proof
  authorized_activation_evidence?
  authorized_coverage_cancellation_receipt?
  authorized_non_activation_evidence?
  transition_evidence_projection
  authorizations[]
}
```

Before either branch, the authority verifies the embedded
`ClaimIngressAdmissionCutProofV1`, its bounded bytes, exact Agreement/log/cutoff,
contiguous root, and zero pending-or-ambiguous count. For every successful
initial-ingress receipt through the cut, the proof carries exactly one terminal
claim-admission result; the admitted subset and their receipt digests reproduce
the claim-admission high-water and root that this action freezes. The filing-
close receipt copies the ingress high-water/root and commits the exact cut-proof
digest. A missing, later, forked, truncated, digest-only, or locally reconstructed
proof fails before the shared coverage CAS.

The action request commits predecessor envelopes by their exact complete-
envelope digests. The resulting receipt carries each selected complete
predecessor once. Re-embedding those already large envelopes in both the
canonical request and the enclosing portable stage receipt would recursively
duplicate the same bytes and can make a valid bounded lifecycle impossible to
encode. This digest-first request form preserves exact authorization while the
complete receipt remains self-contained and independently verifiable.

`normal` close uses the exact Agreement `claim_filing_ends_at_unix` as its
cutoff and cannot be admitted before that cutoff. If the current coverage state
is still `active`, the action derives `coverage_end_reason = normal_expiry`,
sets incident eligibility to the immutable scheduled end, binds the exact
authorized activation envelope digest, and forbids cancellation or end-
evidence digests. The receipt embeds that complete activation evidence. The
close authority's same-domain snapshot proves that no cancellation won before
the cut; the bound end commitment is exactly
`scheduled`, names the Agreement-bound `coverage_state_domain_digest`, and has
no end evidence. No separate scheduled-expiry action exists.
If state is `coverage_ended`, the branch is exactly `accepted_cancellation` and
the action binds both complete-envelope digests; the receipt embeds the exact
authorized activation evidence and authorized cancellation receipt whose
digests and cutoffs equal the durable coverage record. The end commitment is
reconstructed from that complete receipt and must
equal the current durable value byte-for-byte.

`never_activated` close uses the coverage-start activation cutoff, requires the
exact authorized non-activation evidence, sets the end reason to
`never_activated`, forbids activation evidence, and freezes the canonical empty
claim-admission log at high-water zero. Its ingress cut is likewise the
canonical coverage-bound empty initial-ingress log with zero pending actions;
an ingress receipt is invalid before activation. Its end commitment is the exact `never_activated` value
derived from that complete non-activation envelope. The receipt copies the
Agreement-bound state-domain digest and commits the exact end object in every
branch. The
projection purpose is `claim-filing-close`, its target is `frozen`, and it
requires role `activation`, kind `authorized_envelope`, under
`tos.service.agent-guarantor-activation-evidence-envelope.v1` exactly for both
normal branches; role `coverage_cancellation`, kind `authorized_envelope`, under
`tos.service.agent-guarantor-cancellation-receipt-envelope.v1` exactly for the
accepted-cancellation normal branch, or role `non_activation`, same kind, under
`tos.service.agent-guarantor-non-activation-evidence-envelope.v1` exactly for
the never-activated branch. Normal expiry has only `activation`. These three end
branches are mutually exclusive. In every branch, the claim-admission
authority atomically compares the coverage and filing revisions, high-water,
and log root; advances both revisions by one; changes `OPEN` or `NOT_OPEN` to
`frozen`; persists the action resolution; and authorizes the receipt. It
rejects a pending or ambiguous by-cutoff claim admission.

For `normal_expiry` and `accepted_cancellation`,
`incident_eligibility_ends_at_unix` is required and exactly equals the current
`CoverageEndCommitmentV1` cutoff (the scheduled coverage end or admitted
cancellation time respectively). For `never_activated` it is absent in the end
commitment, action-derived receipt, closure context, and terminal-set body. No
zero, coverage-start, or other sentinel value is valid. Every wrapper copies
the same presence bit and, when present, the same Unix second.

For `never_activated`, `prior_claim_filing_state` is exactly `NOT_OPEN` and its
revision is the value established at acceptance; the non-activation mutation
must not have advanced it. The close is the only operation that advances that
filing revision, commits the empty ingress/admission cuts, and produces the
portable filing-close receipt. Treating non-activation evidence itself as a
frozen filing state, or invoking `coverage_closure` before this distinct receipt
exists, fails closed.

`ResolveFilingCloseCoverageAgreementV1` follows exactly one branch. For either
normal branch it obtains the Agreement from the embedded activation evidence;
for `never_activated` it follows the non-activation evidence through its
acceptance receipt and acceptance request. The accepted-cancellation branch
also resolves the Agreement nested in the cancellation request and requires it
to be byte-identical to the activation path. The action and receipt carry no
additional Agreement copy. The resolved body's digest must equal every
Agreement commitment in the action, receipt, embedded lifecycle evidence, and
durable coverage record. The authority derives the scheduled incident cutoff,
filing cutoff, closure capacity, terminal deadline, and selected profiles from
these bytes. A filing close cannot rely on a locally cached Agreement or a bare
digest. Downstream terminal-set and coverage-resolution envelopes use this
resolver through the exact filing-close receipt and do not add another direct
copy.

Every receipt authorization names `claim-filing-close-receipt`, commits the
exact recomputed body digest, and satisfies the Agreement-selected claim-
admission authority profile/quorum at `closed_at_unix`.

After the receipt, a new claim ID is impossible. A predecessor-linked revision
of an already admitted claim remains possible only under the bounded evidence
or review window already authorized by the Agreement and does not change the
frozen initial-claim high-water or root. Terminal claim-set construction later
embeds this exact receipt and proves all permitted revision logs and claims have
resolved. For `independently-enforceable`, this mutation uses the immutable
`filing_close` stage Action Authority, Writer Fence, high-water, and direct
Adapter route; a Guarantor timer or private empty-list assertion is invalid.

### 17.4 Claim decision

```text
DeterministicFallbackAggregateProjectionV1 {
  schema_version
  fallback_profile_digest
  gross_fallback_amount
  cumulative_applied_approved_amount
  aggregate_pending_decision_reserve_before
  reclaimable_prior_amount
  remaining_aggregate_capacity
  projected_approved_amount
}

ClaimDecisionPolicyApplicationV1 {
  schema_version
  coverage_agreement_body_digest
  coverage_obligation_id
  authorized_claim_envelope_digest
  decision_path
  benefit_calculation_profile          # exact Agreement ProfileRefV1
  triggered_obligation_set_digest
  evidence_set_digest
  other_recovery_declaration_digest
  applicable_policy_clause_ids[]       # canonical sorted unique Agreement IDs
  policy_input_projection              # bounded canonical profile-defined bytes
  full_eligible_benefit_amount
  fallback_aggregate_projection?       # exact only for accepted-benefit fallback
}

ClaimDecisionReasonV1 {
  schema_version
  decision_profile                     # exact Agreement ProfileRefV1
  result
  reason_code                          # exact profile-registry token
  applicable_policy_clause_ids[]       # exact subset used by the reason
  evidence_predicate_ids[]             # exact canonical manifest references
}

ClaimDecisionBodyV1 {
  schema_version
  coverage_agreement_body_digest
  coverage_obligation_id
  claim_id
  authorized_claim_envelope_digest
  decision_sequence
  decision_revision                  # exactly 1 in V1
  predecessor_authorized_claim_decision_digest?
  decision_path                     # initial, successor,
                                    # initial_terminal_fallback,
                                    # terminal_fallback, or
                                    # late_recovery_terminal_fallback
  expected_claim_revision
  decision_profile
  decision_authority_subjects[]
  decision_quorum_rule
  result                             # approved, partially_approved, denied,
                                     # evidence_required, disputed
  approved_amount
  evidence_set_digest
  policy_application_digest
  reason_digest
  payout_lines[]
  challenge_window_seconds?
  resolution_window_seconds?
  decided_at_unix
  expires_at_unix
  required_extensions[]
  optional_extensions[]
}

AuthorizedClaimDecisionV1 {
  body
  policy_application                 # exact ClaimDecisionPolicyApplicationV1
  decision_reason                    # exact ClaimDecisionReasonV1
  decision_evidence_set              # exact CanonicalGuarantorEvidenceSetV1
  authorizations[]
}
```

The two mandatory digests have exactly one canonical source each:

```text
policy_application_digest = Digest(
  "tos.service.agent-guarantor-claim-decision-policy-application.v1",
  policy_application)

reason_digest = Digest(
  "tos.service.agent-guarantor-claim-decision-reason.v1",
  decision_reason)
```

The envelope embeds both byte-for-byte; a digest-only pointer is invalid. The
policy application repeats and must equal the body/Agreement/claim/evidence
inputs. `policy_input_projection` is canonical under the exact
`benefit_calculation_profile`, has that profile's released finite schema and
size bound, and contains every non-secret scalar/input needed to reproduce
`full_eligible_benefit_amount`; private evidence remains in the separately
bound evidence set. Clause IDs resolve uniquely in the accepted Agreement's
policy objects. The reason code resolves uniquely in the exact
`decision_profile` registry for the selected result, while its clause and
predicate arrays are sorted and duplicate-free. For an ordinary decision they
are authorized subsets of the policy application and admitted claim manifest;
for a fallback they obey the exact equality/complete-selection rules below.
Free-form prose, localized text, an unknown code,
or an unregistered parameter map is never canonical reason authority.
For every path, `decision_reason.decision_profile` and `result` equal the body
byte-for-byte. An ordinary Decision Authority may select only a reason row
registered for that exact profile/result and must bind its exact clause and
evidence subsets; a deterministic fallback has no such selection and uses only
the total mapping in the Agreement-fixed fallback object.

`fallback_aggregate_projection` is absent for ordinary decisions and
`deny_zero`; it is required for every `accepted_benefit_calculation` fallback.
Its fields exactly reproduce the section 10.1 checked aggregate computation, its
`projected_approved_amount = approved_amount`, and its fallback profile equals
the Agreement-fixed fallback. For an ordinary decision the policy application
commits the gross eligibility result but does not invent a portfolio snapshot;
the separate decision-admission CAS enforces current aggregate capacity. An
accepted-benefit fallback therefore commits both the deterministic policy rule
and the exact authority-generated aggregate operands, while `deny_zero` carries
the explicitly non-applicable representation above and an ordinary Decision
Authority cannot claim stale portfolio state.

The result matrix is normative. For every ordinary `approved`,
`partially_approved`, or `denied` decision and every accepted-benefit fallback,
the selected total
`benefit_calculation_profile` computes one canonical
`full_eligible_benefit_amount` from the exact admitted claim/revision and
portable evidence cut after exclusions, deductible, coinsurance, layer share,
and per-claim cap, but before the shared aggregate-cap projection. The decision
evidence and policy-application digests commit those inputs and output. A
`deny_zero` fallback instead uses the exact unevaluated zero/empty representation
above. `zero` means
canonical zero in the coverage asset and `empty` means a zero-length canonical
array.

| Result | Approved amount | Payout lines | Challenge duration | Resolution duration | Effect |
| --- | --- | --- | --- | --- | --- |
| `approved` | positive and exactly `full_eligible_benefit_amount` | nonempty; exact sum | required | forbidden | challengeable full approval |
| `partially_approved` | positive and strictly less than `full_eligible_benefit_amount` | nonempty; exact sum | required | forbidden | challengeable partial approval |
| `denied` | zero; for an ordinary decision `full_eligible_benefit_amount` is zero, while a deterministic fallback satisfies the exact zero-result rule below | empty | required | forbidden | challengeable denial |
| `evidence_required` | zero | empty | forbidden | required | nonterminal evidence request |
| `disputed` | zero; cumulative totals unchanged | empty | forbidden | required | nonterminal dispute |

The decision states merits and an exact proposed amount, not shared portfolio
state. Aggregate pending and applied amounts are checked only by the separately
linearized decision-admission/application authority. No result may carry an
amount, line, or deadline forbidden by its row.
For an ordinary pre-authorized decision, the three monetary categories are
disjoint and exhaustive: a positive amount equal to the full eligible benefit
is `approved`, a lower positive amount is `partially_approved`, and a zero full
eligible benefit is `denied`. Such a decision is never rewritten at admission;
if its exact amount no longer fits aggregate capacity it is rejected as
specified below.

For an Agreement-granted accepted-benefit fallback, the independently
recomputed `fallback_approved_amount` in section 10.1 is the category operand.
Equality to the positive gross eligible amount is `approved`; a lower positive
value is `partially_approved`; and zero is `denied` only when the exact
aggregate projection proves zero remaining capacity or gross eligibility is
zero. A `deny_zero` fallback is separately and always denied without evaluating
either operand. The reason and policy-application digests commit the exact
Agreement rule and, only for the accepted-benefit branch, aggregate state.
Decision path and fallback profile make these exceptions non-overlapping with
an ordinary denial. A result token cannot be selected independently of its
applicable total derivation.

For an approval, partial approval, or denial,
`challenge_window_seconds` is required and exactly equals the duration selected
by the accepted Agreement and decision profile. It is a duration, not an
absolute cutoff: decision authorization does not start or shorten the window.
For `evidence_required` or `disputed`, the challenge field is forbidden and
`resolution_window_seconds` is required. It exactly equals the duration frozen
in the accepted coverage terms, is positive, and does not exceed the selected
claim profile's `maximum_nonterminal_resolution_window_seconds` or the accepted
`review_deadline_seconds`. It is a duration, not a signer-selected absolute
deadline. A decision occurs after admission of the exact claim revision and by
the claim-relative `claim_review_cutoff` derived from the initial claim-
admission receipt. No revision, profile interpretation, or post-Agreement
extension can move that cutoff. Every payout line begins no earlier than the
linearized terminal challenge-close transition and fits the accepted payout
and Adapter recovery windows.

Passage of time alone is not terminal evidence. Challenge close is linearized
against typed challenge admission and records a new claim-state revision. An
admitted challenge is a state transition followed by a successor decision; it
is not a `challenged` decision result. Payout materialization uses only the
final authorized approving decision selected by that transition. A denial
becomes `final_denied` only after the same close rule. `evidence_required`,
`disputed`, timeout, and an unknown close action are never terminal.

Decision sequence starts at 1 per claim and advances only for a new admitted
merits, evidence-request, dispute, or post-challenge decision state.
`decision_revision` is exactly `1` in V1. A new state step increments the
sequence and predecessor-links the complete envelope digest of the last
actually admitted authorized decision through its admission receipt. The field
is absent for sequence 1 and is otherwise named
`predecessor_authorized_claim_decision_digest`; it always uses the
`tos.service.agent-guarantor-claim-decision-envelope.v1` domain. A failed or
unadmitted action is never a decision predecessor. Skipped sequences, another
revision value, two bodies at one sequence, or a body-only predecessor fail
closed. V1 has no `cas_rebase` path or failed-decision lineage.

`decision_path` is a closed V1 enum with the following exact admission rules:

| Path | Required predecessor evidence | Sequence/revision | Time and result rule |
| --- | --- | --- | --- |
| `initial` | no prior decision or claim-state transition | `1/1` | ordinary selected Decision Authority; any result row that passes the remaining-round rule |
| `initial_terminal_fallback` | exact current authorized claim-admission receipt; no prior decision or transition | `1/1` | admitted no earlier than `claim_review_cutoff`; exact deterministic fallback; challengeable candidate only |
| `successor` | exact prior decision-admission receipt and the current `challenge_admission` or `nonterminal_response_admission` receipt | next sequence, revision 1 | admitted no later than the transition receipt's `successor_decision_due_at_unix`; a challenge successor must be a challengeable candidate |
| `terminal_fallback` | exact current decision-admission receipt and, when state is `reviewing`, its exact current transition receipt | next sequence, revision 1 | admitted no earlier than the current resolution/successor cutoff; exact deterministic fallback object; result is only `approved`, `partially_approved`, or `denied` |
| `late_recovery_terminal_fallback` | exact late filing-close receipt plus the current admitted claim/decision/transition head | `1/1` when no decision exists, otherwise next sequence/revision 1 | only after a timely ingress ambiguity delayed filing close beyond the normal terminal target; exact deterministic fallback admitted no later than `late_ingress_recovery_deadline_unix`; challengeable candidate only |

For `successor`, the current claim-state revision and counters must equal the
embedded transition receipt. A challenge successor cannot produce another
nonterminal result. An `initial` or nonterminal successor may produce
`evidence_required` or `disputed` only while at least one nonterminal round
remains; otherwise admission rejects the decision without consuming a sequence
or slot. For `terminal_fallback` directly from
`evidence_required` or `disputed`, the admission atomically consumes one
nonterminal round; from `reviewing`, the preceding transition already consumed
the applicable challenge or nonterminal round, so the counters are unchanged.
`initial_terminal_fallback` changes neither counter. A
`late_recovery_terminal_fallback` deterministically consumes any current
nonterminal/reviewing head into one challengeable candidate without exceeding
the already reserved counters and forbids another nonterminal result. All three
fallback paths use
the exact `claim_closure_capacity.terminal_fallback.fallback_profile`, authority
set, quorum, and deterministic derivation instead of the ordinary
`decision_profile`; every other path forbids that profile. The admission
authority materializes a fallback exactly once from the immutable source head
and its current aggregate state as described below; no signed rebase object is
created. Missing, extraneous,
or wrong-kind predecessor evidence is invalid. The late path additionally
requires the exact authorized filing-close receipt, proves
`terminal_resolution_deadline_unix < closed_at_unix <=
late_ingress_recovery_deadline_unix`, and proves that the receipt's frozen
ingress cut contains the timely ingress whose ambiguity caused the late close.
That receipt is forbidden on the two normal fallback paths.
Unknown enum values require a new claim-profile and schema version.

`authorizations[]` contains
`ProfileQualifiedObjectAuthorizationV1`, is sorted by complete canonical
element bytes, and
rejects duplicate bytes, duplicate authority subjects, and two different
objects under one profile-defined evidence identity. The complete-envelope
digest is:

```text
authorized_claim_decision_digest
  = Digest(
      "tos.service.agent-guarantor-claim-decision-envelope.v1",
      AuthorizedClaimDecisionV1)
```

Every authorization element MUST name `claim-decision` and commit the exact
recomputed `claim_decision_body_digest` as its `authorized_body_digest`. For
ordinary paths it must match one Agreement-selected Decision Authority,
profile, role, and quorum slot. For `initial_terminal_fallback`,
`terminal_fallback`, or `late_recovery_terminal_fallback`, it instead must
match the Agreement-bound deterministic
fallback object exactly; mixing the two authority sets or supplying a
caller-selected fallback result is invalid. The fallback decision and its
authorization set are outputs of the same linearized admission transaction,
not caller inputs. Its profile-qualified evidence is the bound admission
authority's proof that it applied the Agreement grant and deterministic
fallback verifier to the exact current state; it is not a newly requested
discretionary Guarantor approval. The verifier resolves historical
authority as required by section 9.1, evaluates the complete quorum once, and
rejects missing, extraneous, duplicated, substituted, or expired evidence.
`CommerceProfileEventV1.object_digest`, terminal-decision references, claim-set
entries, and recovery journals commit `authorized_claim_decision_digest`.
Fields explicitly named `claim_decision_body_digest` continue to commit only
the body and never imply complete authorization.

The verifier recomputes `evidence_set_digest` from the embedded set. That set
uses purpose `claim-decision-evidence` and the exact authorized-claim envelope
digest as context; it carries each required evidence envelope or immutable
descriptor within the Agreement bounds. A Decision Authority's private
database, a bare evidence hash, or an unavailable mutable locator cannot make a
decision portable or terminal.

Authorization by a Decision Authority is not admission into the claim state.
Every decision first passes a separately fenced mutation:

```text
DecisionApplicationTokenV1 {
  schema_version
  token_id
  coverage_agreement_body_digest
  coverage_obligation_id
  claim_id
  authorized_claim_decision_digest
  decision_sequence
  decision_revision
  reserved_approved_amount
  token_revision                     # exactly 1 when created
  state                              # exactly pending
}

ClaimRevisionEpochExpectationV1 {
  schema_version
  coverage_agreement_body_digest
  coverage_obligation_id
  claim_id
  revision_epoch
  revision_ingress_log_id
  expected_epoch_state               # open, or frozen only for late recovery
  expected_epoch_state_revision
  expected_claim_revision
}

AuthorizedDecisionAdmissionVariantV1 {
  authorized_claim_decision_digest
  authorized_claim_admission_receipt_digest
  claim_revision_epoch_expectation   # exact epoch branch defined below
  predecessor_decision_admission_receipt_digest?
  predecessor_claim_state_transition_receipt_digest?
  expected_claim_state_revision
  expected_challenge_rounds_used
  expected_nonterminal_rounds_used
}

DeterministicFallbackAdmissionVariantV1 {
  coverage_agreement_body_digest
  coverage_obligation_id
  claim_id
  authorized_claim_admission_receipt
  claim_revision_epoch_expectation   # exact epoch branch defined below
  current_decision_admission_receipt?
  current_claim_state_transition_receipt?
  late_filing_close_receipt?         # required only for late recovery
  fallback_profile_digest
  source_claim_revision
  source_claim_state_revision
  source_claim_state
  expected_challenge_rounds_used
  expected_nonterminal_rounds_used
  trigger_cutoff_unix
  decision_sequence
}

ClaimDecisionSourceHeadV1 {
  schema_version                            # exactly 1
  authorized_claim_admission_receipt_digest
  current_decision_admission_receipt_digest?
  current_claim_state_transition_receipt_digest?
  late_filing_close_receipt_digest?
  claim_revision_epoch_expectation_digest
}

AuthorizedDecisionAdmissionIdentityV1 {
  schema_version                            # exactly 1
  claim_decision_body_digest
  decision_revision                         # exactly 1
  derived_target_state
}

DeterministicFallbackAdmissionIdentityV1 {
  schema_version                            # exactly 1
  fallback_profile_digest
  trigger_cutoff_unix
  claim_revision_epoch_expectation_digest
}

ClaimDecisionAdmissionActionBodyV1 {
  schema_version
  admission_mode                     # authorized_decision or
                                     # deterministic_fallback
  authorized_decision_variant?
  deterministic_fallback_variant?
}

ClaimDecisionAdmissionReceiptBodyV1 {
  schema_version
  authority_id
  coverage_agreement_body_digest
  coverage_obligation_id
  claim_id
  authorized_claim_decision_digest
  admission_mode
  fallback_trigger_cutoff_unix?
  authorized_claim_admission_receipt_digest
  claim_revision_ingress_cut_proof_digest
  late_filing_close_receipt_digest?
  frozen_revision_epoch
  prior_revision_epoch_state_revision
  frozen_revision_epoch_state_revision
  frozen_claim_revision_ingress_high_water
  frozen_claim_revision_ingress_log_root
  predecessor_decision_admission_receipt_digest?
  predecessor_claim_state_transition_receipt_digest?
  decision_sequence
  decision_revision
  decision_path
  prior_coverage_revision
  admitted_coverage_revision
  prior_coverage_end_commitment_digest
  resulting_coverage_end_commitment_digest
  prior_claim_state
  admitted_claim_state
  prior_claim_state_revision
  admitted_claim_state_revision
  challenge_rounds_used_before
  challenge_rounds_used_after
  nonterminal_rounds_used_before
  nonterminal_rounds_used_after
  challenge_starts_at_unix?
  challenge_ends_at_unix?
  resolution_starts_at_unix?
  resolution_due_at_unix?
  prior_application_token_digest?
  prior_application_token_terminal_state? # replaced or cancelled
  resulting_application_token?
  aggregate_pending_decision_reserve_before
  aggregate_pending_decision_reserve_after
  authorized_action_digest
  stable_action_id
  exact_request_digest
  writer_generation
  writer_fence_digest
  admitted_at_unix
  authority_admission_eligibility_proof_set_digest
}

AuthorizedClaimDecisionAdmissionReceiptV1 {
  body
  stage_action_admission_evidence     # exact PortableStageActionAdmissionEvidenceV1
  authorized_claim_decision
  authorized_claim_admission_receipt
  claim_revision_ingress_cut_proof
  late_filing_close_receipt?         # exact and only for late recovery
  coverage_end_commitment            # exact preserved CoverageEndCommitmentV1
  prior_pending_application_token?
  authority_admission_eligibility_proof_set
  authorizations[]
}
```

`claim_revision_epoch_expectation_digest` is exactly
`Digest("tos.service.agent-guarantor-claim-revision-epoch-expectation.v1",
claim_revision_epoch_expectation)`. The source head, identity preimage, and
selected tagged variant use that same exact embedded expectation. A digest
without those bytes, two expectations, or a mismatch in Agreement, obligation,
claim, epoch, log, state revision, or selected claim revision fails before
action admission. `late_filing_close_receipt_digest` and the embedded receipt
are both present exactly for `late_recovery_terminal_fallback`; they equal the
tagged variant and source-head digest and are absent otherwise. The released
maximum-size table budgets this additional complete envelope in every wrapper
that may carry the late path.

The receipt is also the immutable, portable proof of its stage-action
authorization. `authorized_action_digest` is recomputed from
`stage_action_admission_evidence.authorized_action`;
`writer_fence_digest`, `writer_generation`, stable action ID, exact request
digest, owner, Agent, action kind, expected prior state, and expiry must equal
both the body and the exact canonical request embedded by that stage evidence.
The verifier recomputes `writer_fence_digest` from
`stage_action_admission_evidence.writer_fence`, verifies its proof, scope,
owner, Agent, authority, key,
generation, and admission-time validity, and requires the action and fence to
satisfy the scalar binding in `GuarantorStageActionAuthorityV1` when that
assurance profile is selected. A digest-only reference, mutable Adapter lookup,
missing object, second conflicting copy, or action/fence combination that was
not valid at `admitted_at_unix` is invalid. The decision-admission business
evidence quorum in `authorizations[]` remains a distinct required layer; it
cannot substitute for the embedded Action Authority or Writer Fence.

The action is a closed tagged union. `authorized_decision` requires exactly one
`authorized_decision_variant` and forbids the fallback variant;
`deterministic_fallback` does the reverse. Mixed, empty, or unknown modes fail
canonical decoding. The ordinary variant carries a pre-authorized merits
decision. The fallback variant carries only immutable source-state objects and
the Agreement-bound fallback grant; it must not carry a proposed result,
amount, payout line, output authorization wrapper, application token, coverage
revision, aggregate operand, or target revision.

For an ordinary decision, the admission authority verifies the exact claim
revision and Decision Authority quorum both at signing time and in fresh
finalized authority state at `admitted_at_unix`. For a fallback, it verifies the
exact source head, cutoff, counters, profile, and Agreement grant, then constructs
and authorizes the deterministic `AuthorizedClaimDecisionV1` inside the same
transaction that admits it. The receipt's section 9.1 proof set covers every
newly admitted authorization and exactly matches that admission cut. The
authority atomically advances the coverage and claim-state revisions by one,
writes one decision-log entry, persists the action resolution, and authorizes
the receipt. Exact retry returns the same decision and receipt. Another body at
the same sequence, a skipped sequence, a forked predecessor, an unknown prior
action, or a stale claim head conflicts. An unrelated coverage-revision advance
is handled inside the same prepared action and is not a wire conflict.

The action embeds an exact `ClaimRevisionEpochExpectationV1`, never a
caller-created `decision_snapshot` cut. Revision ingress and decision admission
share the per-claim epoch-state CAS. On the ordinary path, the sink atomically
compares the expected open epoch, epoch-state revision, current admitted claim
revision, log ID, high-water, and root; advances the epoch state to `frozen`;
increments its state revision by one; and captures the then-current ingress
high-water and root.
`ingress_cutoff_unix` is the authority-generated freeze time written in the
resulting `ClaimIngressAdmissionCutProofV1`, not an input or a signer-selected
deadline. A revision ingress transaction either sequences before that CAS and
is included in the frozen high-water, or observes the frozen epoch and cannot
enter it. There is no time gap or implementation-selected cutoff.

Every revision ingress through the frozen high-water must then have a terminal
ingress result and, when received, a terminal admitted-or-rejected claim-
admission result before the decision action can become accepted. The admitted
high-water/root must end at the exact claim revision selected by the decision.
A pending entry keeps the same decision action prepared; it does not reopen the
epoch or permit a second action. A revision that wins the epoch CAS first
changes the expected revision and makes the decision request stale. A later
challenge or nonterminal-response transition may atomically open the next
bounded epoch with the next epoch number and state revision; its successor
decision must freeze that exact epoch. The late-recovery path forbids
nonterminal results and keeps revision ingress frozen. Its initial fallback
uses the ordinary open-to-frozen CAS; if that candidate is challenged, the
challenge transition does not reopen revision ingress and its one successor
uses `expected_epoch_state = frozen`, the exact unchanged epoch/state revision,
and the prior decision receipt's byte-identical cut proof. That exception may
neither create another proof nor change high-water, root, claim revision, or
epoch state. It exists only for a successor to a late-recovery candidate.
`challenge_close` accepts only the
current decision receipt and its authority-produced frozen cut. Timeout, local
queue absence, an unfrozen expectation, or a caller-supplied/digest-only cut is
insufficient.
The same transaction reads the exact current end commitment from the bound
coverage state, preserves it byte-for-byte, and writes equal prior/resulting
commitment digests in the receipt. The caller does not supply that volatile
value. Decision admission has no authority to reopen cancelled coverage,
lengthen its incident cutoff, or replace cancellation evidence.

The action carries the exact predecessor objects required by the
`decision_path` table; their complete-envelope digests equal the corresponding
result-body fields. The authorized receipt does not recursively embed them.
The authority verifies that the predecessor transition is the
current claim-state head, was admitted after the named predecessor decision,
and carries the same counters and unexpired successor cutoff. It copies all
four round counters into the receipt. Counts are monotonic, begin at zero,
never exceed the Agreement maxima, and may change only by the exact fallback
rule above or by a transition in the closed registry below. A caller-supplied
counter, local timer, omitted action input, or valid receipt from a different
state head conflicts in the same CAS. A standalone verifier receives the exact
predecessors as bounded context; the terminal bundle later supplies the
complete flat decision and transition logs in canonical order.

For `approved`, `partially_approved`, and `denied`, the receipt contains one
authority-derived `resulting_application_token`. Its ID is exactly:

```text
Digest("tos.service.agent-guarantor-decision-application-token-id.v1", {
  coverage_agreement_body_digest,
  coverage_obligation_id,
  claim_id,
  authorized_claim_decision_digest
})
```

Its reserved amount equals the admitted decision's `approved_amount`, including
canonical zero for denial. `evidence_required` and `disputed` omit the
resulting token. The authority reads any current pending token from the same
claim state and embeds it in the output envelope: admission of a successor
terminal candidate marks it `replaced`, while admission of a nonterminal
successor marks it `cancelled`. The old token and its reserved amount remain
live unless and until that same admission mutation commits. A foreign, already
consumed, or non-head token in authority state conflicts.

The admission transaction performs checked arithmetic:

```text
aggregate_pending_decision_reserve_after
  = aggregate_pending_decision_reserve_before
  - prior_pending_application_token.reserved_approved_amount_or_zero
  + resulting_application_token.reserved_approved_amount_or_zero

cumulative_applied_approved_amount
  + aggregate_pending_decision_reserve_after
  <= maximum_aggregate_payout
```

The authority reads the current aggregate value and persists the resulting
value, token disposition, decision-log entry, claim state, and coverage
revision atomically. Thus an approving decision reserves aggregate capacity at
admission rather than hoping it remains available after the challenge window.
An ordinary approving decision whose exact amount no longer fits is terminally
`rejected` as `ActionResolutionV1.state = rejected`, without a profile result,
decision-log entry, claim or coverage mutation, token, closure slot, or closure
byte consumption; its merits are never resized. `capacity_exhausted` is the
required local diagnostic classification, not a new canonical field in the
released generic `ActionResolutionV1`. Resolving the same stable action and
exact request returns that same terminal rejection. The unchanged claim remains
eligible for its mandatory deterministic fallback at the exact cutoff.
The mandatory fallback can later close the unchanged claim at its exact cutoff.
For either deterministic fallback path, the same transaction derives
`reclaimable_prior_amount`, `remaining_aggregate_capacity`, result, approved
amount, payout lines, authorization wrapper, and resulting token exactly by
section 10.1. Aggregate exhaustion therefore yields a zero-value denial, not a
failed fallback admission. If another claim changes an aggregate operand during
an optimistic datastore attempt, the prepared authority action rereads current
state and retries internally. It does not publish `conflict`, change its request
or stable ID, increment a decision revision, or emit a failed decision object.
No timeout, challenge message, worker crash, or later coverage mutation may
release or replace a pending token without the exact fenced successor
admission or successful application transaction.

For `approved`, `partially_approved`, and `denied`, the admission receipt
requires `challenge_starts_at_unix = admitted_at_unix` and
`challenge_ends_at_unix = checked_add(admitted_at_unix,
authorized_claim_decision.body.challenge_window_seconds)`. For
`evidence_required` and `disputed`, both challenge fields are absent,
`resolution_starts_at_unix = admitted_at_unix`, and
`resolution_due_at_unix = checked_add(admitted_at_unix,
authorized_claim_decision.body.resolution_window_seconds)`. Terminal candidates
omit both resolution fields. The admission time is the authority's canonical
linearization time. For `authorized_decision`, it must satisfy
`decided_at_unix <= admitted_at_unix <= expires_at_unix`. An ordinary `initial`
decision must be admitted no later than `claim_review_cutoff`; an
`initial_terminal_fallback` becomes eligible at that cutoff. Every path then
uses the exact target continuation entry. Every normal-case path must satisfy
`admitted_at_unix + maximum_remaining_closure_seconds <=
terminal_resolution_deadline_unix`. The derived challenge end or response due
is part of that target-state duration and is never compared to the obsolete
review cutoff or an implementation-local “latest effect” time. If delayed
delivery leaves insufficient room for the complete selected duration,
admission fails and only an already eligible exact fallback may race for the
same state; the authority never shortens a window. `expires_at_unix` limits
first admission only and does not truncate a window after admission.
The sole exception is `late_recovery_terminal_fallback` under the exact late-
close proof above. It retains the same continuation entry and durations,
records the ordinary deadline breach, and substitutes the Agreement-derived
late deadlines. Admission still fails unless the filing close and fallback are
no later than `late_ingress_recovery_deadline_unix` and the complete remaining
closure fits `late_recovery_terminal_deadline_unix`.
Consequently, delayed transport before admission consumes neither a challenge
nor a nonterminal response period. Passage of `resolution_due_at_unix` only
makes the profile's typed, fenced terminal-fallback decision eligible; it is
never terminal evidence by itself. A `successor` admission uses the exact
predecessor transition cutoff and must linearize no later than it. A
`terminal_fallback` linearizes no earlier than that cutoff and races a normal
successor on the same state revision. An `initial_terminal_fallback` instead
uses the exact claim-relative `claim_review_cutoff` derived from the initial
claim-admission receipt and current initial claim-state revision. At the exact
review cutoff an ordinary initial decision
and this fallback race on the same decision-log head and claim-state CAS; only
one can consume sequence 1. For a challenge transition the cutoff is
the checked sum of transition admission time and
`successor_decision_window_seconds`; for a nonterminal response it is the
inherited `resolution_due_at_unix`.

For an ordinary `initial_terminal_fallback` or `terminal_fallback`, timestamps
are outputs rather than caller bytes. The authority derives them exactly as
follows:

```text
trigger_at_unix =
  the exact deadline selected by the fallback source-state mapping

candidate_entry =
  continuation_budget[derived_challengeable_candidate,
                      challenge_rounds_remaining_after_admission,
                      0]

latest_fallback_admission_at_unix = checked_sub(
  terminal_resolution_deadline_unix,
  candidate_entry.maximum_remaining_closure_seconds)

trigger_at_unix <= admitted_at_unix <= latest_fallback_admission_at_unix
decided_at_unix = admitted_at_unix
expires_at_unix = latest_fallback_admission_at_unix
AuthorizedActionV1.expires_at = latest_fallback_admission_at_unix
```

For `late_recovery_terminal_fallback`, the authority instead derives
`trigger_at_unix` from the exact late filing-close receipt's `closed_at_unix`.
It requires
`trigger_at_unix <= admitted_at_unix <= late_ingress_recovery_deadline_unix`
and proves
`admitted_at_unix + candidate_entry.maximum_remaining_closure_seconds <=
late_recovery_terminal_deadline_unix`. The current Action Authority chooses a
bounded operational `AuthorizedActionV1.expires_at` no later than
`late_ingress_recovery_deadline_unix`; this envelope field is not part of the
semantic key or exact request. If the envelope expires before admission, the
current authority may reauthorize only the identical stable ID and request
bytes under a fresh Writer Fence, and never after that hard admission cutoff.
After admission, the stored action resolves normally even if that envelope time
passes.

The request freezes `trigger_at_unix` through `trigger_cutoff_unix`; the sink
recomputes it from the source head. `admitted_at_unix` is written once by the
linearizing authority. The fallback constructs only the same Agreement-fixed
relative payout offsets as an ordinary decision. Absolute payout times and
their dependent obligation digests remain absent until decision application,
when section 16.2 derives them from the later terminal challenge-close receipt.
Internal CAS retries cannot change the action identity, request bytes, trigger,
or latest-admission cutoff and add no portable decision, log, or closure-
capacity bytes.

The authority checks its trusted clock against `trigger_at_unix` before it
allocates, prepares, resolves, rejects, tombstones, or otherwise persists the
Semantic Action slot. A request observed before the trigger returns the
non-admitting precondition `not_yet_eligible`; it creates no
`ActionResolutionV1`, and `ResolveAction` for that stable action and request
remains `unknown`. It consumes no decision, claim, coverage, aggregate, token,
closure-slot, closure-byte, writer-high-water, or successor state. For the two
normal fallback paths, only a call whose authority time is within the closed interval
`[trigger_at_unix, latest_fallback_admission_at_unix]` may enter generic action
admission. Therefore an untrusted early caller cannot poison the sole fallback
identity, and the byte-identical request can enter admission at equality. This
validation order is mandatory even when a generic Action Authority would
normally persist terminal precondition failures. On those two paths,
`AuthorizedActionV1.expires_at` carries the same Unix-second value as
`latest_fallback_admission_at_unix`; there is no field named
`expires_at_unix` in that generic schema.

The admission transaction also applies the section 10.1 continuation table to
the proposed target state. An approval, partial approval, or denial retains the
required successor-decision and transition slots for every still-permitted
challenge. `evidence_required` and `disputed` retain either their response
transition plus successor decision or their direct terminal-fallback decision.
Checked backward time budgeting
must leave the target state's complete remaining closure duration before the
Agreement-bound terminal deadline. These cross-counter and time checks occur
with decision-log admission, token replacement, aggregate reserve, claim state,
and coverage revision in the same CAS.

Every receipt authorization names `claim-decision-admission-receipt`, commits
the exact recomputed body digest, and satisfies the Agreement-selected decision-
admission profile/quorum at `admitted_at_unix`.

The target state is derived only from the authorized result:

| Decision result | Decision-admission target state |
| --- | --- |
| `approved` | `approved` |
| `partially_approved` | `partially_approved` |
| `denied` | `denied` |
| `evidence_required` | `evidence_required` |
| `disputed` | `disputed` |

The body field, semantic action field, and receipt state must equal this table.
Approval, partial approval, and denial remain challengeable; this receipt is
not the terminal challenge-close receipt and cannot materialize a payout.
`evidence_required` and `disputed` are admitted nonterminal decisions whose
successors follow the selected profile.

For `independently-enforceable`, a final decision admission uses the immutable
`terminal_decision` stage Action Authority, Writer Fence, high-water, resolver,
and direct Adapter route. The same bound admission profile processes
nonterminal decision rows but they do not satisfy the terminal-decision stage.
The Guarantor may relay a decision but cannot admit, fork, or suppress it.

Applying the decision and allocating its payout sequences produces:

```text
ClaimDecisionApplicationReceiptBodyV1 {
  schema_version
  authority_id
  coverage_agreement_body_digest
  coverage_obligation_id
  claim_id
  authorized_claim_decision_digest
  claim_decision_admission_receipt_digest
  terminal_claim_state_transition_receipt_digest
  decision_application_token_id
  decision_application_token_digest
  prior_application_token_revision
  resulting_application_token_revision
  resulting_application_token_state  # exactly consumed
  materialized_payout_obligation_set_digest
  authorized_action_digest
  stable_action_id
  exact_request_digest
  writer_generation
  writer_fence_digest
  prior_coverage_revision
  applied_coverage_revision
  prior_coverage_end_commitment_digest
  resulting_coverage_end_commitment_digest
  prior_claim_state_revision
  applied_claim_state_revision
  prior_next_payout_sequence
  resulting_next_payout_sequence
  prior_materialized_payout_line_digest?
  resulting_materialized_payout_line_digest?
  cumulative_approved_before
  cumulative_approved_after
  aggregate_pending_decision_reserve_before
  aggregate_pending_decision_reserve_after
  applied_at_unix
}

AuthorizedClaimDecisionApplicationReceiptV1 {
  body
  stage_action_admission_evidence     # exact PortableStageActionAdmissionEvidenceV1
  coverage_end_commitment            # exact preserved CoverageEndCommitmentV1
  authorized_terminal_claim_state_transition_receipt
  decision_application_token
  materialized_payout_obligation_set
  authorizations[]
}
```

The terminal transition receipt is the single complete predecessor path: it
embeds the decision-admission receipt, which embeds the authorized decision and
claim-admission receipt. The application request commits their complete-envelope
digests. A verifier derives those objects only through that complete path and
rejects a missing or unequal digest. Repeating the same complete predecessors
directly in the request or application receipt is non-canonical because it
creates quadratic envelope growth without adding authority.

The rollback-resistant authority accepts this operation only for a final
`approved`, `partially_approved`, or `denied` decision. It verifies the exact
decision-admission receipt and requires its authorized decision and claim state
to match. The terminal close receipt must embed that byte-identical admission
receipt and select its decision-log head. It then verifies the exact
embedded terminal claim-state transition receipt, requires that receipt's
evidence projection to name the same authorized decision, and requires its
resulting state to prove that the challenge/appeal path is closed with no
pending or ambiguous transition. The application's prior claim-state revision
equals that terminal receipt's resulting revision. Elapsed time, a Decision
Authority signature, or a local `no challenge` observation cannot replace the
receipt. `evidence_required` and `disputed` use `TransitionClaim` and never
materialize a payout set.

The authority then validates the exact pending application token embedded in
the decision-admission receipt, applies a compare-and-swap against the current
coverage/exposure revision, consumes the token, moves its reserved amount from
the aggregate pending-decision bucket into cumulative applied approval, and
allocates payout sequences and extends the materialized-payout-line chain in
one transaction. The action's `expected_next_payout_sequence` and
`expected_materialized_payout_line_digest` are compared in that same CAS. The
receipt copies those prior values, assigns one contiguous global sequence to
each decision-local line, and commits the final line digest and next unused
sequence. For the first-ever line the prior digest is absent and the prior next
sequence is 1. For a denial, the resulting chain-head digest equals the prior
digest byte-for-byte (both are absent only when no payout was ever
materialized), the next sequence is unchanged, and the materialized set is
`not_applicable`. The current revision may be
newer than the decision-admission revision because unrelated admitted claims
or decisions may have advanced it; the pending token preserves both capacity
and identity across that concurrency. The action must name the current base
revision it observed, not copy the old admission revision. It recomputes every
embedded envelope/set digest and returns the permanent receipt. A deterministic
materialization without this admission receipt is a proposal, not evidence
that the portfolio or claim state accepted those payout instances.
That transaction also compares the exact current `CoverageEndCommitmentV1` and
copies its digest unchanged into both receipt fields. Materialization changes
aggregate exposure, never the scheduled/cancelled/non-activated end branch or
its incident cutoff and evidence.

`expected_application_token_revision` equals the embedded pending token's
revision. The receipt's prior token revision equals it, the resulting revision
is its checked successor, and the resulting state is exactly `consumed`.
Replacement or cancellation is evidenced only by a successor decision-
admission receipt; application cannot consume such a terminal token.

Decision application reads the terminal claim state under CAS but does not
create another claim-state transition: `prior_claim_state_revision` and
`applied_claim_state_revision` are equal to the embedded terminal-transition
receipt's resulting revision. The coverage revision advances by exactly one to
commit token consumption, pending-reserve and cumulative totals, and allocated
payout sequences. It also compares and advances the unique coverage-bound
materialized-line chain head atomically; allocating the same sequence range to
two concurrently admitted decisions is impossible. Checked arithmetic requires
the pending reserve to decrease
by the token amount and cumulative applied approval to increase by the same
amount. A denial consumes its zero-value token and creates the canonical
`not_applicable` payout set.

If the application loses the current-revision CAS because another valid
mutation advanced state, its action resolves durably as `rejected` with the
typed local reason `stale_expected_state`; it does not consume the token. The
same stable ID and different exact bytes remains `conflict` and is never this
contention outcome. After the stored rejection, a deterministic terminal
successor may bind the same token and newly observed current revision. Unknown
or ambiguous attempts are resolved, never rebased. The first
successful application permanently consumes the token, so every later attempt,
including a stale writer after takeover, conflicts even if it finds another
coverage revision.

The decision profile freezes signer or quorum identity, key resolution,
evidence predicates, timing, challenge and fallback rules, and verifier digest.
Duplicate quorum subjects and duplicate operator domains do not count twice.
Key rotation, revocation, and historical authorization follow the selected
profile rather than current-key guesswork.

Timeout by itself remains unresolved. It cannot silently become approval,
denial, release, or payment. Every valid V1 claim profile nevertheless binds the
mandatory deterministic terminal fallback from `ClaimClosureCapacityV1`. When
its exact cutoff is reached, any Agreement-authorized claimant or beneficiary
may invoke the deterministic admission route. Before any ordinary decision it
creates `decision_path = initial_terminal_fallback`; after an admitted
nonterminal or reviewing head it creates `decision_path = terminal_fallback`.
Both use the reserved decision, record, time, and payout capacity. The result is
a challengeable terminal candidate and can never request more evidence, open
another dispute, or reset a deadline.

The action identity is derived from the exact current authorized claim-
admission receipt; for a later fallback it additionally binds the exact current
decision-admission and transition heads when applicable, the fallback profile,
trigger, cut, state, counters, and decision sequence. It deliberately excludes
coverage revision, aggregate values, result, amount, payout lines, output
timestamps, and output authorization wrappers. The mutation verifier constructs
the evidence snapshot, result, amount, payout lines, timestamps, and authorized
decision from the fallback object, current linearized coverage state, and
accepted Agreement and rejects caller-supplied alternatives. The Agreement
grant, not a fresh discretionary Guarantor signature, authorizes this
materialization. For `independently-enforceable`, its authority cannot rely on
the absent Guarantor. If its action is prepared, pending, or ambiguous, the
claim remains open and the same action is resolved; no second fallback identity
is created.

An implementation using optimistic storage retries an unrelated coverage CAS
inside that one prepared action. Such attempts are not Action Resolutions,
decision revisions, or decision-log entries. To prevent starvation, the same
coverage authority services eligible prepared fallback slots in deterministic
`(trigger_cutoff_unix, claim_admission_sequence, claim_id canonical bytes)`
order. A later mutation cannot overtake an earlier slot if doing so would make
the earlier slot miss its continuation-table latest admission. A contract
Adapter obtains current state inside its transition and does not accept a
caller-supplied base coverage revision. A changed source claim head, invalid
cut, terminal coverage state, or already-admitted winner may terminate the
action; ordinary contention may not. A profile whose initial or later fallback
cannot be admitted and then challenge-closed within the reserved terminal
deadline is invalid before Agreement acceptance.

A denial is terminal only after every accepted challenge or appeal window and
profile transition completes. Forked decisions, skipped sequence, changed
authority, changed evidence profile, or changed payout destination fail closed.

Non-decision claim-state changes produce a portable receipt:

```text
ClaimStateTransitionReceiptBodyV1 {
  schema_version
  authority_id
  coverage_agreement_body_digest
  coverage_obligation_id
  claim_id
  transition_kind
  transition_evidence_projection_digest
  authorized_action_digest
  stable_action_id
  exact_request_digest
  writer_generation
  writer_fence_digest
  prior_claim_state
  resulting_claim_state
  prior_claim_state_revision
  resulting_claim_state_revision
  challenge_rounds_used_before
  challenge_rounds_used_after
  nonterminal_rounds_used_before
  nonterminal_rounds_used_after
  successor_decision_due_at_unix?
  transitioned_at_unix
  authority_admission_eligibility_proof_set_digest
}

AuthorizedClaimStateTransitionReceiptV1 {
  body
  stage_action_admission_evidence     # exact PortableStageActionAdmissionEvidenceV1
  authorized_claim_decision_admission_receipt
  transition_evidence_projection
  transition_evidence_set
  authority_admission_eligibility_proof_set
  authorizations[]
}
```

V1 has exactly three claim-state transition kinds. There is no “equivalent,”
implementation-defined, or timeout transition. Unknown kinds require a new
schema and claim-profile version and fail closed under V1:

| Transition kind | Permitted prior decision/state | Resulting state | Round-counter delta | Admission cutoff and successor field | Terminal? |
| --- | --- | --- | --- | --- | --- |
| `challenge_admission` | current admitted `approved`, `partially_approved`, or `denied` candidate | `reviewing` | challenge `+1`; nonterminal unchanged | linearize at or before the receipt's `challenge_ends_at_unix`; set `successor_decision_due_at_unix = transitioned_at_unix + successor_decision_window_seconds` | no |
| `nonterminal_response_admission` | current admitted `evidence_required` or `disputed` decision | `reviewing` | nonterminal `+1`; challenge unchanged | linearize strictly before the receipt's `resolution_due_at_unix`; inherit that exact value as `successor_decision_due_at_unix` | no |
| `challenge_close` | current admitted `approved`, `partially_approved`, or `denied` candidate | respectively `final_approved`, `final_partially_approved`, or `final_denied` | both unchanged | linearize at or after `challenge_ends_at_unix`; successor field absent | yes |

Every transition action and result embeds the exact current authorized
decision-admission receipt. Projection role `decision_admission` commits its
complete envelope, which in turn commits the exact authorized decision. The
authority requires that receipt to be the current decision-log and claim-state
head, derives the prior state, counter values, and deadline from it, and
atomically advances the claim-state revision by exactly one. The action's
expected/target counters and result receipt must equal the table; reaching a
configured maximum rejects another corresponding admission. The transition
evidence set uses a kind-specific purpose and the current decision-admission
receipt digest as context. A generic chat message, a decision signature alone,
elapsed time, or local claim status cannot replace it.
Every newly presented challenge or nonterminal-response authorization is
re-resolved against fresh finalized authority state at `transitioned_at_unix`;
the exact section 9.1 eligibility proof set is part of the authorized receipt.

`challenge_admission` and `challenge_close` race on the same expected claim-
state revision. Admission at the exact challenge cutoff is permitted; close at
that same authority time succeeds only if no challenge admission has already
won the CAS. A challenge that wins creates the only current `reviewing` head,
and its successor or fallback decision must be admitted by the bound successor
cutoff. `nonterminal_response_admission` must win strictly before its response
deadline so a response delivered exactly at the deadline cannot suppress the
deterministic fallback. It inherits, rather than extends, that deadline. A
successor decision and a fallback race on the same current state revision at
the cutoff; the winner advances the decision log and the loser conflicts.

For `challenge_close`, the resulting state is derived from the embedded final
decision and cannot be caller selected. The decision-application action later
requires this exact terminal receipt. For the other two kinds, the resulting
state is exactly `reviewing`; a successor or fallback decision is required and
no payout may be materialized. A delayed decision message starts its full
challenge or resolution window only at decision admission, while a delayed
transition request gains no power from its transport timestamp.

## 18. Collateral

```text
CollateralTermsV1 {
  position_id
  selected_collateral_profile_digest
  assurance_level
  asset
  amount
  collateral_principal_subject
  custody_adapter_profile
  collateral_control_disclosure      # exact authenticated profile value
  position_identity_profile
  transition_bindings[]               # exact CollateralTransitionBindingV1 set
  independent_execution_profile?
  independent_execution_authority_subjects[]
  independent_execution_quorum_rule?
  network_domain_digest?
  contract_or_account_digest
  adapter_code_digest?
  exclusive_allocation_required
  lock_by_unix
  lock_until_unix
  release_not_before_unix
  finality_profile
  maximum_evidence_age_seconds
  reorg_window_seconds
}

CollateralPositionStateV1 {
  schema_version
  coverage_agreement_body_digest
  collateral_obligation_id
  position_id
  position_digest
  coverage_binding_digest
  state_revision
  state
  asset
  allocated_amount
  cumulative_consumed
  cumulative_released
  cumulative_impaired
  remaining_amount
}

CollateralAdapterRequestV1 {
  schema_version
  adapter_profile
  adapter_request_profile
  coverage_agreement_body_digest
  collateral_obligation_id
  collateral_position_id
  transition_binding_digest
  transition_kind
  expected_position_state           # exact CollateralPositionStateV1
  expected_state_digest
  asset
  amount
  payout_destination_digest?
  agreement_payment_request_digest?
  obligation_instance_id?
  authorized_claim_decision_envelope_digest?
  prerequisite_evidence_set_digest
  adapter_operation_parameters      # bounded canonical bytes
}

CollateralEvidenceBodyV1 {
  schema_version
  coverage_agreement_body_digest
  collateral_obligation_id
  position_id
  position_digest
  transition_binding_digest
  collateral_transition_action_body_digest
  adapter_profile
  evidence_profile
  evidence_content_type
  transition_kind                    # released transition enum below
  amount
  cumulative_consumed
  prior_state_revision
  resulting_state_revision
  expected_state_digest
  resulting_state_digest
  coverage_binding_digest
  authorized_claim_decision_envelope_digest?
  agreement_payment_request_digest?
  obligation_instance_id?
  finality_reference
  finalized_at_unix
  adapter_request_digest
  adapter_evidence_digest
  authorized_action_digest
  stable_action_id
  exact_request_digest
  writer_generation
  writer_fence_digest
  authority_admission_eligibility_proof_set_digest
}

CollateralAdapterEvidenceV1 {
  content_type
  evidence_profile                   # exact ProfileRefV1
  transition_binding_digest
  adapter_profile_digest
  transition_kind
  adapter_request_digest
  prior_state_revision
  resulting_state_revision
  expected_state_digest
  resulting_state_digest
  representation                     # inline or content_addressed
  canonical_evidence_bytes?
  immutable_descriptor?
}

AuthorizedCollateralEvidenceV1 {
  body
  collateral_transition_action_body   # exact CollateralTransitionActionBodyV1
  adapter_evidence                    # exact CollateralAdapterEvidenceV1
  resulting_position_state            # exact sink-derived CollateralPositionStateV1
  authority_admission_eligibility_proof_set
  authorizations[]
}

CollateralPayoutPaymentEvidenceProjectionV1 {
  schema_version                       # exactly 1
  coverage_agreement_body_digest
  payout_template_obligation_id
  obligation_instance_id
  agreement_payment_request_digest
  collateral_obligation_id
  collateral_position_id
  collateral_transition_action_body_digest
  authorized_collateral_evidence_digest
  asset
  amount
  payout_destination_digest
  exact_transfer_reference
  finality_reference
  stable_action_id
  exact_request_digest
}
```

Exactly one Adapter-evidence representation is present. Its canonical digest
under `tos.service.agent-guarantor-collateral-adapter-evidence.v1` equals
`adapter_evidence_digest`; an inline value is bounded and byte-
canonical under the selected Adapter profile, while a descriptor uses the
same immutable retrieval rules as section 10. The envelope's authorization set
satisfies the custody or independent-execution subjects and quorum frozen by
the selected collateral profile. Its complete-envelope digest is
`tos.service.agent-guarantor-collateral-evidence-envelope.v1`; Messenger and every
evidence set use that digest, never the body digest or an unspecified Adapter
wrapper. An Adapter profile may define a stricter nested proof, but it cannot
change this outer envelope or digest domain.
Every outer authorization names `collateral-evidence`, commits the exact body
digest, and satisfies the selected collateral authority profile at
`finalized_at_unix`.
The Adapter also freezes the exact section 9.1 eligibility proof set for every
newly admitted custody, execution-quorum, and prerequisite authorization at
that finalized admission cut. A backdated custody signature cannot move the
position after its authority was revoked.

The profile-to-wire mapping is closed and deterministic. A published collateral
profile contains exactly one `CollateralTransitionProfileV1` for every kind it
supports, sorted by `transition_kind`; duplicates and fallback entries are
invalid. Both profile and binding arrays are bounded to the seven released V1
kinds. Agreement compilation resolves each selected entry into one
`CollateralTransitionBindingV1`, freezes the exact authorization binding,
sorts the bindings by kind, and forbids a kind not present in both the
signed service profile and accepted terms. `transition_profile_digest` is
`Digest("tos.service.agent-guarantor-collateral-transition-profile.v1",
transition_profile)` and `transition_binding_digest` is
`Digest("tos.service.agent-guarantor-collateral-transition-binding.v1",
transition_binding)`.

Authority derivation has exactly two branches. For
`authorization_subject_source = custodian`, the advertised transition profile
requires one `custodian_authorization_binding`; Agreement compilation copies it
byte-for-byte into `authorization_binding`, and the transition Adapter profile
equals the selected `GuarantorCollateralProfileV1.custody_adapter_profile`.
For `independent_execution_quorum`, the custodian binding is absent and
compilation constructs the binding from the selected collateral profile's
exact `independent_execution_profile`, subjects, and quorum. That branch is
permitted only for `independently-enforceable`. Subjects are sorted, unique,
and nonempty, and the quorum is satisfiable. A missing, mixed-source, caller-
selected, or alternative binding fails closed.

V1 releases this mapping; the corresponding profile fields freeze the Adapter,
request/evidence content types and profiles, maximum request size,
authorization binding, subject source, prerequisite roles, and binding rules:

| Transition kind | Permitted prior state | Permitted result | Required semantic binding |
| --- | --- | --- | --- |
| `lock` | `unproven` or `lock_pending` | `locked` | claim/decision forbidden; destination forbidden |
| `encumber` | `locked` | `encumbered` | claim/decision forbidden; destination forbidden |
| `payout` | `encumbered` or `partially_consumed` | `partially_consumed` or `depleted`, derived from checked remaining capacity | terminal decision required; Agreement payout destination required |
| `release` | `locked`, `encumbered`, or `partially_consumed` | `released` | authorized terminal claim set required as a prerequisite; claim/decision and destination forbidden |
| `reorg` | `locked`, `encumbered`, or `partially_consumed` | `reorged` | claim/decision forbidden; destination forbidden |
| `position_impairment` | `locked`, `encumbered`, `partially_consumed`, or `reorged` | `defaulted` | claim/decision forbidden; destination forbidden |
| `payout_default` | `encumbered` or `partially_consumed` | `defaulted` | terminal decision required; Agreement payout destination required |

For `payout` and `payout_default`,
`authorized_claim_decision_envelope_digest` is required in both
`CollateralAdapterRequestV1` and `CollateralEvidenceBodyV1` and is exactly:

```text
Digest(
  "tos.service.agent-guarantor-claim-decision-envelope.v1",
  exact AuthorizedClaimDecisionV1 selected by the terminal
  claim-state transition and materialized payout obligation set)
```

The complete authorized decision is carried once through the request's
`prerequisite_evidence_set`; the Adapter recomputes the digest, verifies its
decision-admission and terminal-transition lineage, and requires the same
decision, claim, obligation, amount, destination, and payout instance as the
materialized set and payment request. A body digest, decision-admission receipt
digest, terminal-transition digest, or another wrapper is invalid. The field is
forbidden for `lock`, `encumber`, `release`, `reorg`, and
`position_impairment`; `release` instead binds the complete authorized terminal
claim set through its distinct prerequisite role. Request and evidence presence
and bytes must match exactly.

Exhaustion is not another transition kind: it is a `payout` whose verified
resulting state is `depleted`. The action binding, body Adapter and evidence
profiles, content types, authorization profile and subjects, kind,
request digest, prerequisite roles, destination rule, and successor-derivation
profile must match one exact Agreement-bound transition binding. The Adapter
reads the authoritative expected position under CAS and alone derives the
resulting state and digest from the released table, transition inputs, checked
amounts, and bound successor profile. Neither the caller, Action Authority,
model, request, nor action body supplies a target state or resulting digest.
Missing, duplicate, substituted, mixed custody/
independent authority, or caller-selected mappings fail closed.

### 18.1 One atomic identity for collateral-backed payout

A successful collateral `payout` is not submitted as an independent
`collateral.transition` action followed by a second payment action. The
Agreement selects the composite operation profile
`tos.service.agent-guarantor.mutate.collateral-backed-payout.v1`, whose
canonical request is `CollateralBackedAgreementPaymentActionBodyV1` and whose
sole Semantic Action kind is the released `settlement.external`. Its stable ID
is derived from the exact materialized obligation, payer, beneficiary, asset,
amount, destination, external system, and selected Adapter exactly as required
by the released `settlement.external` registry entry. The nested
`AgreementPaymentRequestV2.stable_action_id`, the surrounding
`AuthorizedActionV1.stable_action_id`, and both result envelopes are equal.

The composite request embeds exactly one materialized obligation and its exact
containing `MaterializedPayoutObligationSetV1`. It also embeds exactly one
`CollateralTransitionActionBodyV1` with `transition_kind = payout`. The nested
collateral Adapter request requires
`agreement_payment_request_digest` and `obligation_instance_id`; both are
forbidden for `lock`, `encumber`, `release`, `reorg`, and
`position_impairment`, and are required for `payout` and `payout_default`.
For successful `payout`, the payment request, obligation, materialized line,
terminal decision, collateral binding, asset, amount, destination, and
beneficiary must agree byte-for-byte. The payout Adapter ProfileRef is the
Agreement-selected composite Adapter and is compatible with the selected
collateral transition binding. A URI-only match is invalid.

One linearizable Adapter transaction admits the single stable action and exact
composite request, executes at most one transfer, advances the collateral
position once, and produces both:

1. the exact `AuthorizedCollateralEvidenceV1` for that position transition;
2. the exact generic `AgreementPaymentEvidenceV1` for the materialized payment
   obligation.

Those two objects and the exact portable payout-stage Action/Fence evidence are
carried together as one
`AuthorizedGuarantorPayoutExecutionEvidenceV1` result component. The wrapper
does not merge their authority semantics; it makes their atomic association and
stage admission independently recoverable.

The collateral evidence body repeats the payment-request digest and obligation
instance ID and carries the same stable action ID and composite
`exact_request_digest`. The payment evidence's selected evidence profile
requires its `evidence` bytes to be the canonical
`CollateralPayoutPaymentEvidenceProjectionV1`. That projection commits the
complete collateral-evidence envelope digest, exact transfer and finality
references, economic fields, action ID, and request digest. The generic payment
evidence repeats the same payment-request digest, stable action ID, exact
transfer reference, finality reference, and terminal resolved state. The
terminal settlement evidence set carries both complete objects, so a verifier
can recompute the projection after every Adapter or Provider database is lost.

The single composite result component uses `accepted_effect_v1`: all three of
its nested evidences appear together in the same accepted mutation and remain
byte-identical through terminal recovery. Neither economic component may appear
alone or outside that wrapper. A timeout resolves the same composite
action; a caller cannot retry it as `payment.direct`, another
`settlement.external` request, or standalone `collateral.transition`. The
standalone collateral-transition operation rejects `transition_kind = payout`.
`payout_default` remains a no-transfer adverse collateral transition and cannot
produce `AgreementPaymentEvidenceV1`; the Agreement's selected default evidence
profile resolves the materialized obligation as defaulted instead. Thus one
vault debit is one payment identity, one collateral state transition, and one
obligation resolution rather than two independently retryable sends.

No subject can be counted through both authority-source branches. An identity
label, endpoint operator, `collateral_principal_subject`, or current Adapter
configuration is not an authorization subject unless the exact advertised
binding names it.

The canonical action body embeds that binding and one exact bounded
`CollateralAdapterRequestV1`. The request digest is exclusively:

```text
adapter_request_digest = Digest(
  "tos.service.agent-guarantor-collateral-adapter-request.v1",
  adapter_request)
```

The selected transition profile fixes its request profile and content type and
requires `len(canonical_cbor(adapter_request)) <=
maximum_adapter_request_bytes <= 256 KiB`. The sink bounded-decodes and re-
encodes the object, derives every Agreement, position, binding, kind,
prerequisite, asset, amount, and destination field from the action, and rejects
mutable locators, embedded credentials, alternate wrappers, or noncanonical
operation parameters. The Adapter request never contains the action-body
digest, stable action ID, authorization, Adapter evidence, or outer envelope.

The semantic action derives `transition_binding_digest` from the binding.
`CollateralAdapterEvidenceV1` commits the same binding digest, Adapter profile
digest, kind, Adapter request digest, revisions, and state digests, but never commits the later outer
body or envelope. `CollateralEvidenceBodyV1` then commits the action-body
digest, Adapter-evidence digest, Authorized Action, stable ID, exact request,
Writer Fence, and verified result. The complete envelope embeds the exact
action body and Adapter evidence. This one-way order is cycle-free and prevents
an Adapter proof for one request, profile, generation, or kind from being
rewrapped as another transition.
The position-state digest is
`Digest("tos.service.agent-guarantor-collateral-position-state.v1",
CollateralPositionStateV1)`. Checked same-asset arithmetic requires
`allocated_amount = cumulative_consumed + cumulative_released +
cumulative_impaired + remaining_amount`. The request's expected state has the
action's expected revision and digest. In the same linearizable mutation, the
sink compares that state, applies the exact `successor_derivation_profile`,
derives a complete successor, advances its revision by exactly one, persists
it, and only then constructs `CollateralAdapterEvidenceV1`. Expected digests
are recomputed from the request; resulting digests are recomputed from the
sink-derived successor and occur only in Adapter evidence, the authorized outer
body, and the durable position record. The complete envelope embeds the exact
sink-derived `resulting_position_state`; its recomputed digest must equal all
three outputs. A stale expected state or derivation failure rejects without a
successor; it never invites the caller to propose another state.
`CollateralEvidenceBodyV1.adapter_request_digest` equals the recomputed
embedded-request digest. No request field, semantic map, or authorization may
smuggle a resulting state or digest through operation parameters or an
extension.

Both collateralized assurance levels require
`exclusive_allocation_required = true` and prove a unique Adapter allocation
slot bound to the exact coverage Agreement, collateral obligation, and
position. The exact minimum atomic allocation is derived from the selected
authenticated collateral profile, never from an Adapter default:

```text
required_collateral_amount_atomic = checked_ceil_div(
  checked_mul(maximum_aggregate_payout.amount_atomic,
              selected_collateral_profile.minimum_collateralization_ppm),
  1_000_000)

collateral_terms.amount.amount_atomic >= required_collateral_amount_atomic
```

`checked_ceil_div(n, d)` is `checked_add(n, d - 1) / d` for positive `d` and
uses arbitrary-precision intermediate arithmetic before proving that the result
fits the canonical atomic-amount bound. The collateral and payout
`AssetIdentityV1` values must be byte-identical, so no price conversion or
rounding across assets is implicit. Overflow, zero ppm, a mismatched asset, or
an initial allocation one atomic unit below the rounded-up result fails
Agreement validation and activation.

After activation, both collateralized assurance levels enforce the dynamic
invariant in the same Adapter position-state CAS:

```text
beneficiary_secured_value_atomic =
  current_position.remaining_amount.amount_atomic
  + finalized_terminal_paid_from_this_position.amount_atomic

beneficiary_secured_value_atomic >= required_collateral_amount_atomic
current_position.cumulative_consumed.amount_atomic
  == finalized_terminal_paid_from_this_position.amount_atomic
```

`remaining_amount` counts only value still exclusively allocated to this exact
Agreement and executable for its beneficiary. The paid term counts only exact
finalized terminal payment evidence for this coverage and position. It is the
checked sum of unique payout-transition evidence in the current position's
unbroken predecessor chain; its equality to `cumulative_consumed` proves that
no fee, unrelated transfer, or unfinalized send is counted as paid collateral.
Released, impaired, reorged, merely submitted, ambiguous, cross-position, or
otherwise unavailable value does not count. Activation and every nonterminal
successor that claims the selected collateral assurance must satisfy the
invariant after the proposed transition. A `payout` may reduce remaining value
only by the same amount that its finalized terminal evidence adds to the paid
term.

An adverse `reorg`, `position_impairment`, or `payout_default` transition is
not rejected merely because it proves that the invariant has failed. The
Adapter must durably record that exact adverse successor, set the orthogonal
evidence status to `IMPAIRED` or `TERMINAL_DEFAULT`, stop claiming current
collateral assurance, and block ordinary release or new coverage admission.
Only the Agreement's bounded default and recovery path may continue. A final
`release` is likewise evaluated under the already authorized terminal claim set
rather than pretending that live-coverage collateral remains after liability
has ended.

`collateral-attested` may therefore allocate less than the full aggregate cap
only when its advertised ppm is below `1_000_000`, but no byte of its claimed
amount may be allocated concurrently to another coverage or obligation.
`independently-enforceable` additionally requires the control-deletion
properties below. Historical lock evidence,
a Provider-signed dashboard, a self-signed proof, a balance without a unique
slot, or overlapping allocation is insufficient. The verifier checks asset,
amount, network, custodian, code, position, unique slot, freshness, finality,
reorg window, and current state in the Adapter's allocation-state domain.

For `independently-enforceable`, the selected collateral-profile digest and
every execution field in `CollateralTermsV1` must exactly match the canonical
advertised entry. `minimum_collateralization_ppm` is at least `1_000_000`, the
position asset equals the payout asset, and `amount` is at least the rounded-up
`required_collateral_amount_atomic` above (which is therefore at least the
coverage terms' `maximum_aggregate_payout`). The independent execution subjects and
quorum can apply each Agreement-selected terminal decision against that
position without Guarantor participation. All execution and recovery costs are
funded outside `amount`. Activation and every live-assurance successor apply
the shared dynamic invariant above against the rounded-up advertised ratio,
not merely 100% of the cap. If any check fails, that Agreement version cannot
activate or continue claiming `independently-enforceable`; the exact adverse
transition remains recordable, but local labels or Provider assertions cannot
downgrade it in place or hide the failure.

Full capacity is necessary but not sufficient. The selected claim operation
Adapter must accept authorized claimant ingress, maintain the admission and
revision logs, apply evidence, dispute, and challenge transitions, close the
filing and challenge windows, verify the independent decision quorum, apply the
terminal decision, and drive payout using the Agreement's immutable
independence binding. After
removing the complete Guarantor technical-control closure, each stage remains
callable and its quorum remains satisfiable. If a Guarantor-controlled
lifecycle authority is the only party that can assign a claim sequence, freeze
the claim high-water, or present a decision, the tuple is not
`independently-enforceable` even when fully funded.

One position cannot support two coverage obligations unless the Adapter
natively provides atomic partitioned allocations and each allocation has a
different exact slot. Partial payout reduces the position monotonically. Full
or residual release is forbidden until:

- coverage and claim-filing windows have ended;
- all admitted claims, decisions, challenges, payouts, and disputes are
  terminal;
- no action remains unknown or ambiguous;
- applicable reorg and Adapter recovery windows have ended; and
- the release action wins the same position-state compare-and-swap domain as
  any competing payout.

Collateral withdrawal, stale evidence, or reorganization changes an orthogonal
Adapter-evidence status, not `CoverageStatus` or the coverage-end commitment.
It never becomes evidence that no claim is payable and cannot silently authorize
a return to usable collateral. Only exact selected-Adapter evidence may resolve
the status as current, impaired, or terminally defaulted.

## 19. Orthogonal state machines and race ordering

One monolithic engagement state cannot represent the independent uncertainty
of offer, coverage, collateral, claim, and payout. Implementations maintain
orthogonal, revisioned records.

### 19.1 Firm offer and exposure

```text
REQUESTED
  -> ALLOCATED
  -> RESERVED_UNSIGNED
      -> ABORT_RESOLVING -> ABORTED_RELEASED
  -> ISSUED
  -> ACCEPTANCE_RESOLVING
      -> ACCEPTED
      -> EXPIRY_RESOLVING -> EXPIRED -> RELEASE_RESOLVING -> RELEASED
      -> AMBIGUOUS
```

`RESERVED_UNSIGNED` is never deliverable. Crash recovery resumes the same
issuance action and offer allocation. A proven terminal-negative issuance
atomically records `ABORTED_RELEASED` and unwinds the private unsigned
reservation in that same authority transaction; it emits neither Guarantor
result component nor portable release receipt. Prepared, unknown, or ambiguous
issuance remains reserved. It cannot repurpose the reservation or create a
different offer. Only an issued offer can enter expiry, which requires the
exact non-acceptance evidence and pre-acceptance release receipt. V1 has no
issued-offer withdrawal transition. This branch uses no terminal claim set.

### 19.2 Coverage

```text
CoverageStatus:
  PENDING_AUTHORIZATION
  -> PENDING_PREREQUISITES
  -> ACTIVATION_RESOLVING
      -> ACTIVE
      -> NOT_ACTIVATED_CONFIRMED
      -> AMBIGUOUS
  ACTIVE -> CANCELLATION_RESOLVING -> COVERAGE_ENDED
  ACTIVE | COVERAGE_ENDED | NOT_ACTIVATED_CONFIRMED
      -> RELEASE_PENDING
      -> CLOSED | CANCELLED | EXHAUSTED | DEFAULTED |
         CLOSED_NOT_ACTIVATED | AMBIGUOUS

ClaimFilingStatus:
  UNINITIALIZED
  -> NOT_OPEN
  -> OPEN
  -> CLOSE_RESOLVING
  -> FROZEN(admission_high_water, admission_log_root)
  -> RESOLVED

  NOT_OPEN
  -> FILING_CLOSE_PENDING
  -> FROZEN(0, canonical_empty_log_root, never_activated)
  -> RESOLVED

AdapterEvidenceStatus:
  CURRENT
  -> EVIDENCE_UNKNOWN
  -> CURRENT | IMPAIRED | TERMINAL_DEFAULT
```

The three state projections are orthogonal. `CoverageStatus = ACTIVE` may coexist with
`ClaimFilingStatus = OPEN`, so an incident can be reported immediately during
coverage. `COVERAGE_ENDED` records an admitted early cancellation; scheduled
incident eligibility is always bounded directly by the Agreement and does not
need an expiry mutation. Filing remains open through
`claim_filing_ends_at_unix`. The linearized `FROZEN` transition stops new
admissions and fixes the exact high-water used by section 19.6. Passing the
scheduled cutoff never erases a valid filing, review, challenge, payout, or
reorg window.
Final `CLOSED`, `CANCELLED`, `EXHAUSTED`, or collateral release requires the
allowed terminal combination of both state machines and every dependent claim,
payout, and Adapter state.
`CLOSED_NOT_ACTIVATED` requires the second zero-claim filing path and exact
non-activation, fee, collateral, and exposure-release evidence.

`UNINITIALIZED` is permitted only as the acceptance action's expected absent
state at revision zero. Accepted coverage atomically creates `NOT_OPEN` at
revision one. Activation atomically advances it to `OPEN`; non-activation
preserves `NOT_OPEN`; neither a local projection nor an ordinary message may
create or skip either transition.

`AdapterEvidenceStatus` is a derived, revisioned projection of exact collateral,
settlement, finality, and action-resolution evidence. `EVIDENCE_UNKNOWN` is not
an authority action and does not change incident eligibility, reopen or cancel
coverage, advance the shared coverage revision, or select a closure reason. It
blocks new payout, collateral disposition, terminal-set construction when the
unknown evidence affects its prerequisites, exposure release, and final
resolution. It does not block the independent filing-close CAS: freezing the
claim high-water neither moves value nor asserts that Adapter evidence is
current. Fresh selected-profile evidence may return the projection to `CURRENT`;
exact impairment or terminal-default evidence selects the other terminal
branches. A timeout, missing endpoint, or local cache state cannot do so.

### 19.3 Claim and payout

```text
ClaimStatus:
  DRAFT
  -> SUBMITTING
  -> ADMITTED | AMBIGUOUS
  -> REVIEWING
  -> DECISION_ADMISSION_PENDING
  -> EVIDENCE_REQUIRED | APPROVED | PARTIALLY_APPROVED | DENIED |
     DISPUTED | AMBIGUOUS
  EVIDENCE_REQUIRED | DISPUTED
      -> REVIEWING -> DECISION_ADMISSION_PENDING
  APPROVED | PARTIALLY_APPROVED | DENIED
      -> REVIEWING -> DECISION_ADMISSION_PENDING
  APPROVED | PARTIALLY_APPROVED | DENIED
      -> FINAL_APPROVED | FINAL_PARTIALLY_APPROVED | FINAL_DENIED

PayoutStatus:
  NOT_MATERIALIZED
  -> NOT_APPLICABLE | PREPARED
  PREPARED -> SUBMITTED | AMBIGUOUS
  -> PARTIALLY_PAID
  -> PAID | DEFAULTED
```

The first `REVIEWING` edge is only
`nonterminal_response_admission`; the second is only
`challenge_admission`. If no first decision is admitted by `claim_review_cutoff`,
`initial_terminal_fallback` advances the initial reviewing head directly to a
challengeable candidate. A later `terminal_fallback` may do the same from an
eligible nonterminal or post-transition reviewing head.
Only `challenge_close` creates a `FINAL_*` state. Claim merits state and payout
state are orthogonal: an approving claim can be final while its materialized
payout remains prepared, partial, ambiguous, paid, or defaulted. Terminal
coverage evidence therefore proves both the exact `FINAL_*` claim state and
the separately terminal payout evidence set.

### 19.4 Collateral position

```text
UNPROVEN
  -> LOCK_PENDING
  -> LOCKED
  -> ENCUMBERED
  -> PAYOUT_PENDING -> PARTIALLY_CONSUMED | DEPLETED
  -> RELEASE_PENDING -> RELEASED
  -> AMBIGUOUS | REORGED | DEFAULTED
```

### 19.5 Shared ordering domains

The following races MUST be linearized by expected revision and durable CAS:

| Race | Shared authority domain |
| --- | --- |
| offer acceptance vs expiry | offer reservation and acceptance authority |
| activation/non-activation, claim or revision admission, filing close, decision admission/application, active cancellation, closure, or final resolution | Agreement-bound `coverage_state_domain_digest` and one coverage revision |
| competing claims vs aggregate cap | coverage exposure record |
| decision admission vs challenge or response transition | claim record |
| payout vs collateral release | collateral position and payout ledger |
| takeover vs stale writer action | owner/provider Writer Fence high-water |

An action admitted while its Writer Fence was current remains valid after a
takeover. The new writer inherits its reservations and unresolved actions. The
old writer cannot create a new action after its generation is superseded.

Scheduled coverage end is absent from this table because it is not an action or
state mutation. Claim eligibility uses the exact Agreement interval in either
arrival order. Final normal-expiry closure is a later one-shot transition that
requires the frozen filing cut and its bound authority time.
Every row that advances the shared coverage revision also compares the current
`CoverageEndCommitmentV1`. Only cancellation may shorten its scheduled branch;
all other rows preserve it exactly.

### 19.6 Terminal claim-set and coverage-resolution evidence

Collateral or exposure release cannot be authorized by asking one mutable
database whether it currently sees an open claim. The accepted claim-admission
authority first closes the filing window in the same linearizable domain that
admits claims. That close transition freezes an admission high-water; no later
claim can be inserted below or beyond it for that coverage version.

```text
ClaimTerminalResolutionRefV1 {
  claim_admission_sequence
  claim_id
  initial_claim_admission_receipt_digest
  final_claim_revision
  final_claim_revision_admission_receipt_digest
  claim_revision_admission_high_water
  claim_revision_admission_log_root
  claim_revision_ingress_high_water
  claim_revision_ingress_log_root
  terminal_authorized_claim_envelope_digest
  terminal_decision_digest           # complete AuthorizedClaimDecisionV1
  terminal_decision_admission_receipt_digest
  decision_application_receipt_digest
  terminal_claim_state
  claim_state_revision
  terminal_claim_state_transition_receipt_digest
  materialized_payout_obligation_set_digest
  terminal_payout_evidence_set_digest
}

ClaimTerminalResolutionRefSetV1 {
  schema_version
  coverage_agreement_body_digest
  coverage_obligation_id
  admission_high_water
  refs[]                            # exact refs in admission-sequence order
}

ClaimTerminalResolutionBundleV1 {
  resolution_ref                    # exact ClaimTerminalResolutionRefV1
  initial_claim_admission_receipt_proof
  revision_admission_receipt_proofs[]
  terminal_authorized_decision
  decision_admission_receipt_proofs[]
  decision_application_receipt_proof
  claim_state_transition_receipts[]
  materialized_payout_obligation_set
  terminal_payout_evidence_set
}

CoverageClosureEvidenceContextV1 {
  schema_version
  coverage_agreement_body_digest
  coverage_obligation_id
  claim_filing_close_receipt_digest
  coverage_cancellation_receipt_digest?
  coverage_end_commitment_digest
  filing_close_reason
  coverage_end_reason
  incident_eligibility_ends_at_unix?
  coverage_end_evidence_digest?
  activation_evidence_digest?
  coverage_closure_reason
  resolution_target_terminal_state
  admission_high_water
  claim_admission_log_root
  claim_resolution_set_digest
  cumulative_approved_amount
  cumulative_paid_amount
  cumulative_defaulted_amount
  outstanding_approved_amount         # exactly zero
  release_not_before_unix
}

TerminalClaimSetBodyV1 {
  schema_version
  coverage_agreement_body_digest
  coverage_obligation_id
  claim_admission_profile_digest
  claim_admission_authority_subjects[]
  claim_admission_log_id
  claim_filing_close_receipt_digest
  coverage_cancellation_receipt_digest?
  coverage_end_commitment_digest
  filing_close_reason                 # normal or never_activated
  coverage_end_reason                 # normal_expiry, accepted_cancellation,
                                      # or never_activated
  incident_eligibility_ends_at_unix?
  coverage_end_evidence_digest?
  activation_evidence_digest?
  coverage_closure_reason             # exact terminal-reason enum
  resolution_target_terminal_state    # final target; current state is release_pending
  coverage_closure_context_digest
  coverage_closure_evidence_set_digest
  transition_evidence_projection_digest
  non_activation_evidence_digest?
  filing_close_coverage_revision
  prior_coverage_revision
  release_pending_coverage_revision
  admission_high_water
  claim_admission_log_root
  claim_resolutions[]
  open_claim_count                    # exactly 0
  ambiguous_action_count             # exactly 0
  cumulative_approved_amount
  cumulative_paid_amount
  cumulative_defaulted_amount
  outstanding_approved_amount
  claim_set_revision                 # exactly 1 in V1
  filing_closed_at_unix
  all_claims_terminal_at_unix
  release_not_before_unix
  authorized_action_digest
  stable_action_id
  exact_request_digest
  writer_generation
  writer_fence_digest
  created_at_unix
  required_extensions[]
  optional_extensions[]
}

AuthorizedTerminalClaimSetEvidenceV1 {
  body
  stage_action_admission_evidence     # exact PortableStageActionAdmissionEvidenceV1
  authorized_claim_filing_close_receipt
  claim_resolution_bundles[]        # admission-sequence order
  claim_resolution_ref_set          # exact ClaimTerminalResolutionRefSetV1
  coverage_closure_evidence_context # exact CoverageClosureEvidenceContextV1
  coverage_closure_evidence_set     # exact CanonicalGuarantorEvidenceSetV1
  fee_resolution_evidence_set?
  collateral_release_eligibility_evidence_set?
  transition_evidence_projection
  authorizations[]
}
```

The closure mutation receives the complete filing-close receipt as a typed
Adapter input but commits it once by its complete-envelope digest in the
canonical Action request. The resulting terminal evidence carries that exact
complete receipt and the verifier recomputes the digest before verifying the
portable Action. Re-embedding the receipt in the Action request would duplicate
the activation and Agreement lineage inside the result's own stage evidence and
can make a valid one-claim closure unencodable; a mutable lookup or digest-only
terminal result remains forbidden.

`claim_resolution_set_digest` is exactly
`Digest("tos.service.agent-guarantor-claim-resolution-set.v1",
claim_resolution_ref_set)`. The set's Agreement, obligation, high-water, and
ordered `refs[]` exactly equal the closure context, filing-close receipt, and
`TerminalClaimSetBodyV1.claim_resolutions[]`. The sink derives every reference
from its corresponding `claim_resolution_bundles[]`; one bundle and one
reference are required for every sequence from 1 through the frozen high-water.
Admission and application proof objects are signed, bounded projections of
their exact complete receipts. Each proof carries the original receipt body,
original authorization quorum, the claim or application values needed for
lineage verification, an immutable descriptor for the complete receipt, and a
seal signed by the Agreement-bound stage Action Authority. The seal commits the
complete receipt envelope digest, body digest, Authorized Action digest,
Coverage Terms digest, and every projected predecessor or result digest. A bare
digest, unsigned projection, locally reconstructed summary, or mutable database
key is invalid. A verifier validates both the original receipt authorization
and the seal and MAY retrieve the descriptor to re-run full stage verification;
high-assurance profiles MUST do so. This compact proof rule prevents recursive
receipt embedding from making every non-empty claim history exceed the 1 MiB
complete-object ceiling without weakening content identity or authority.
Before admitting closure, the sink also recomputes the accepted
`ClaimClosureCapacityV1`, checks every per-claim count and encoded-size bound,
and measures the complete prospective authorized terminal envelope including
its authorization quorum. The measured bytes must not exceed the bound and the
section 10.1 worst-case proof must still verify. Since capacity was reserved at
Agreement and item admission time, a conforming terminal history cannot fail
closure for size. Truncation, digest-only replacement, pagination under the V1
identifier, or treating the 1 MiB ceiling separately for body and
authorizations is invalid.
The sole complete Agreement path in the terminal envelope is
`ResolveFilingCloseCoverageAgreementV1(
authorized_claim_filing_close_receipt)`. Its canonical body digest must equal
`body.coverage_agreement_body_digest`, the closure action commitment, and every
embedded receipt or bundle commitment. The accepted-cancellation branch also
derives its cancellation receipt only from that filing-close receipt; neither
the closure request nor terminal result carries a second copy. A normal-expiry
verifier derives the scheduled incident cutoff, filing cutoff, terminal
deadline, closure capacity, and selected authority profiles from these exact
bytes after every Carrier and Provider database has disappeared. A digest-only
Agreement, a reconstructed local projection, or an additional direct
Agreement or cancellation copy is invalid.
`coverage_closure_context_digest` is exactly
`Digest("tos.service.agent-guarantor-coverage-closure-context.v1",
coverage_closure_evidence_context)`. The context object is an input to the
closure action and does not contain the action, terminal claim-set body,
evidence-set digest, or transition-projection digest. Its Agreement, obligation,
filing receipt, reason, derived terminal state, frozen log, resolution-set
digest, coverage-end commitment, totals, and release cutoff must exactly equal the independently
recomputed values in the action and resulting terminal-set body.
`claim_filing_close_receipt_digest` is the complete authorized-envelope digest
under `tos.service.agent-guarantor-claim-filing-close-envelope.v1`. When present,
`coverage_cancellation_receipt_digest` is the complete envelope digest under
`tos.service.agent-guarantor-cancellation-receipt-envelope.v1`; it is required
exactly when `coverage_end_reason = accepted_cancellation`, including when a
later exhaustion or payout default selects the final closure outcome. It is
forbidden for `normal_expiry` and `never_activated`.
`coverage_end_commitment_digest` is recomputed from the exact commitment carried
by the filing-close receipt. The normal-expiry row requires its `scheduled`
branch; the cancellation row requires `accepted_cancellation` and the same
complete cancellation receipt; the non-activation row requires
`never_activated` and the same complete non-activation envelope. The context,
terminal-set body, action, and current coverage record must all agree. A later
default or exhaustion changes only the financial closure reason and cannot
rewrite this digest.
The closure context and terminal-set body's optional incident cutoff is present
exactly for the first two branches and equals the filing-close receipt and end
commitment. It is absent for `never_activated`; a decoder or materializer that
inserts a sentinel, inherits `coverage_starts_at_unix`, or omits a normal-branch
cutoff fails closed.
`activation_evidence_digest` is required for both normal branches and is the
complete envelope digest under
`tos.service.agent-guarantor-activation-evidence-envelope.v1` of the exact
activation evidence embedded by the filing-close receipt. It is forbidden for
`never_activated`. The context and terminal-set body copy that digest exactly;
they never use a local coverage-state flag as activation evidence.
The embedded receipt must name the same Agreement and obligation, prove the
earlier shared-revision CAS, and reproduce the filing receipt's incident cutoff,
end reason, and coverage-end evidence. A request, authorization alone, or body
digest cannot satisfy it. When present,
`non_activation_evidence_digest` is likewise the complete envelope digest under
`tos.service.agent-guarantor-non-activation-evidence-envelope.v1`, taken from the exact
embedded filing-close receipt. A body digest cannot satisfy either field.

For zero admitted claims, `ClaimTerminalResolutionRefSetV1` is still a canonical
coverage- and obligation-bound object with `admission_high_water = 0` and
`refs = []`; its digest is not a global empty-list digest. Every closure evidence
set member is carried inline or by an immutable descriptor in the exact closure
action. The output envelope may repeat those objects but cannot discover them
later from Provider-private state.

`coverage_closure_evidence_set` uses purpose `coverage-closure` and
`context_digest = coverage_closure_context_digest`. The verifier recomputes the
context first, then every bounded evidence object and the set digest, and
requires exact equality with `coverage_closure_evidence_set_digest`. No
placeholder, zeroed field, unsigned local projection, or body-under-construction
may enter either digest. The filing-close/terminal-claim-set authority is the V1
coverage-closure authority; a later resolution wrapper cannot choose another
reason or state.

The following matrix is exhaustive. Coverage end and final financial outcome
are orthogonal; default and exhaustion take precedence without erasing an
earlier cancellation cutoff:

| Filing close | Coverage end reason | Coverage closure reason | Required final-resolution target | Additional required proof |
| --- | --- | --- | --- | --- |
| `never_activated` | `never_activated` | `never_activated` | `closed_not_activated` | exact authorized non-activation, zero claim high-water and amounts, terminal fee disposition, and collateral release eligibility |
| `normal` | `normal_expiry` | `normal_expiry` | `closed` | exact Agreement/activation schedule, authorized filing close after the scheduled and filing cutoffs, every admitted claim and payment terminal, and no ambiguous action |
| `normal` | `accepted_cancellation` | `accepted_cancellation` | `cancelled` | exact activation evidence and authorized cancellation receipt that previously won the shared coverage CAS, plus every accrued claim and payment terminal |
| `normal` | `normal_expiry` or `accepted_cancellation` | `aggregate_exhaustion` | `exhausted` | cumulative paid amount equals the Agreement's maximum aggregate payout under checked same-asset arithmetic; preserve the selected end branch and receipt |
| `normal` | `normal_expiry` or `accepted_cancellation` | `terminal_default` | `defaulted` | exact selected-Adapter terminal payout-default evidence, or independently verifiable collateral impairment evidence that does not depend on this terminal set; preserve the selected end branch and receipt |

Every row establishes that all claim and payment liabilities are terminal and
that the release cutoffs have passed. For residual collateral it proves
release eligibility, but the collateral remains locked or encumbered until a
later `collateral.transition` consumes this signed terminal claim set. Actual
collateral release, consumption, or terminal default is required only by the
subsequent exposure-release and final coverage-resolution evidence. This
ordering prevents the terminal claim set from depending on the collateral-
release object that itself depends on that set. `terminal_default` cannot be
inferred from timeout, unavailability,
or an unpaid local invoice; `aggregate_exhaustion` cannot use approved-but-
unpaid value; cancellation cannot erase an accrued claim; and normal expiry
cannot precede any accepted review, challenge, payout, reorg, or recovery
window. Any other reason/state pair, mixed filing branch, missing proof,
multiple applicable state assertions, or caller-selected state fails closed.
The authority derives `resolution_target_terminal_state` from the verified row
before signing the terminal claim-set body. This field is a deterministic
future resolution target, not the current coverage state and not terminal
coverage evidence. Producing the terminal claim set atomically moves coverage
only to `release_pending`. The target becomes
`CoverageResolutionBodyV1.terminal_state` only after collateral disposition,
Provider portfolio disposition, and the final resolution CAS all succeed. A UI,
Indexer, Carrier, or verifier MUST NOT display the target as the current state.

For every row, checked same-asset arithmetic requires:

```text
cumulative_approved_amount
  = cumulative_paid_amount
  + cumulative_defaulted_amount
  + outstanding_approved_amount
```

At terminal-set admission, `outstanding_approved_amount` is exactly zero.
`closed`, `cancelled`, `exhausted`, and `closed_not_activated` require
`cumulative_defaulted_amount = 0`; `exhausted` additionally requires
`cumulative_paid_amount` to equal the maximum aggregate payout. The payout-
default branch of `defaulted` requires a positive
`cumulative_defaulted_amount`; the independent collateral-impairment branch may
have zero only when no approved payout default exists. In both branches the
amount equals the sum of the exact claim-bound
`TerminalPayoutEvidenceSetV1.defaulted_amount` values. Each payout-default
evidence object binds the payout obligation, asset,
beneficiary, amount, Adapter, attempted terminal action, and selected default
profile. The zero-amount impairment branch requires exact independently
verifiable position-impairment evidence. A Provider ledger entry, timeout,
write-off, or missing payment is not portable default evidence.

```text
ExposureReleaseReceiptBodyV1 {
  schema_version
  authority_id
  guarantor_agent_id
  coverage_agreement_body_digest
  coverage_obligation_id
  reservation_id
  exposure_admission_receipt_digest
  terminal_claim_set_evidence_digest
  terminal_payment_evidence_set_digest
  collateral_disposition_evidence_set_digest?
  release_evidence_projection_digest
  exposure_disposition_computation_digest
  release_sequence
  predecessor_exposure_release_receipt_digest?
  authorized_action_digest
  stable_action_id
  exact_request_digest
  writer_generation
  writer_fence_digest
  release_state_domain_digest
  base_release_state_revision
  released_release_state_revision
  released_exposure
  remaining_reserved_exposure
  portfolio_disposition              # residual_release, realized_loss,
                                     # retained_defaulted_liability, or mixed
  returned_to_available_exposure
  realized_loss
  retained_defaulted_liability
  state                              # released
  released_at_unix
}

ExposureDispositionComputationV1 {
  schema_version
  coverage_agreement_body_digest
  coverage_obligation_id
  reservation_id
  exposure_admission_receipt_digest
  reservation_scope_digest
  released_exposure
  cumulative_approved_amount
  cumulative_paid_amount
  cumulative_defaulted_amount
  outstanding_approved_amount         # exactly zero
  default_liability_disposition       # exact admission-scope value
  returned_to_available_exposure
  realized_loss
  retained_defaulted_liability
  portfolio_disposition
}

AuthorizedExposureReleaseReceiptV1 {
  body
  stage_action_admission_evidence     # exact PortableStageActionAdmissionEvidenceV1
  authorized_exposure_admission_receipt
  authorized_terminal_claim_set_evidence
  terminal_payment_evidence_set
  collateral_disposition_evidence_set?
  release_evidence_projection
  exposure_disposition_computation
  authorizations[]
}

CoverageResolutionBodyV1 {
  schema_version
  authority_id
  coverage_agreement_body_digest
  coverage_obligation_id
  coverage_end_commitment_digest
  activation_evidence_digest?
  non_activation_evidence_digest?
  terminal_claim_set_evidence_digest
  terminal_payment_evidence_set_digest
  coverage_closure_reason
  coverage_closure_evidence_set_digest
  cumulative_approved_amount
  cumulative_paid_amount
  cumulative_defaulted_amount
  outstanding_approved_amount         # exactly zero
  final_collateral_evidence_set_digest?
  exposure_release_receipt_digest
  transition_evidence_projection_digest
  prior_coverage_revision
  resolved_coverage_revision
  terminal_state
  authorized_action_digest
  stable_action_id
  exact_request_digest
  writer_generation
  writer_fence_digest
  resolved_at_unix
}

AuthorizedCoverageResolutionV1 {
  body
  stage_action_admission_evidence     # exact PortableStageActionAdmissionEvidenceV1
  authorized_exposure_release_receipt
  transition_evidence_projection
  authorizations[]
}
```

For `filing_close_reason = normal`, non-activation evidence is absent and the
coverage resolution requires the exact activation evidence nested in the
terminal set's filing-close receipt. For `never_activated`, that same nested
receipt requires non-activation evidence and forbids activation evidence; the
admission high-water and every amount/count are zero, and claim resolutions are
empty. `CoverageResolutionBodyV1.activation_evidence_digest` and
`non_activation_evidence_digest` copy the applicable nested complete-envelope
digest and cannot name a separately supplied wrapper. The never-activated
filing-close time is the later filing-close authority's `closed_at_unix`, is no
earlier than the admitted non-activation resolution time, and the zero-claim
`all_claims_terminal_at_unix` equals that close time. Its release-not-before
time still accounts for every fee, collateral, reorg, and Adapter recovery
disposition. The two branches are mutually exclusive and cannot be changed by
a later resolution wrapper.

`CoverageResolutionBodyV1.coverage_closure_reason`,
`coverage_closure_evidence_set_digest`, and `terminal_state` exactly equal the
closure reason, evidence-set digest, and `resolution_target_terminal_state`,
respectively, of the terminal claim-set body nested in the exposure-release
receipt. The four cumulative amount
fields also exactly equal that body. The action's expected end commitment is
resolved through that terminal set's exact filing-close receipt; its digest
equals both the terminal-set and resolution-body fields and the current durable
coverage record. Final resolution preserves it unchanged. The
resolution authority recomputes the matrix before signing; it cannot convert a
valid closure into a different terminal label. The direct body commitments are
redundant by design so a lightweight verifier can reject a mismatch before
walking the complete evidence bundle.

The resolution action and result carry the exact authorized exposure-release
receipt once. The verifier follows that receipt to its terminal claim set,
terminal payment aggregate, optional final collateral set, exposure
computation, and their portable members; it recomputes every body commitment
and projection and rejects a missing, extraneous, body-only, or unavailable
object. Neither wrapper may repeat those nested objects or accept caller-
supplied equal digests with different wrappers. A release-receipt digest or
lifecycle-authority signature alone is never a substitute for the complete
nested evidence graph.

`terminal_payment_evidence_set_digest` commits the exact
`CoverageTerminalPayoutEvidenceSetV1`. It contains exactly one verified entry
per admitted claim, contiguously ordered from admission sequence 1 through the
terminal high-water, including claim-bound `not_applicable` objects for terminal
denials by digest. The corresponding exact objects remain solely in the bound
terminal claim-set bundles. For a zero-claim coverage it binds that coverage and terminal claim-
set envelope with `entries = []`. The empty object is evidence of the terminal claim
cut only together with the authorized terminal claim-set object; it is never a
global proof that no payment exists.

This aggregate is constructed only after the terminal claim-set envelope is
final and binds its complete authorized-envelope digest under
`tos.service.agent-guarantor-terminal-claim-set-evidence.v1`. Closure verification uses
the per-claim `TerminalPayoutEvidenceSetV1` objects already embedded in
`claim_resolution_bundles[]`. Neither `CoverageClosureEvidenceContextV1`, a
closure input evidence set, `CoverageClosureActionBodyV1`, nor
`TerminalClaimSetBodyV1` may contain or commit the aggregate coverage payout
set, because doing so would create a digest cycle. Exposure release and final
coverage resolution consume the downstream aggregate and require its entries
to be derived exactly from those already-authorized per-claim objects.

Admission, filing-close, decision-admission, acceptance, activation,
cancellation, decision-application, non-activation, release, and resolution
receipts are permanent historical facts once durably
admitted. Their authorization is verified at the body-defined event time using
historical authority and revocation ordering. A later key, proof, service
profile, or offer expiry does not erase that fact. Expiry fields remain only on
requests, offers, reservations, provisional evidence, and other objects whose
initial admissibility genuinely ends.

For `unsecured-signed` and `collateral-attested`, the release receipt is
produced by the same rollback-resistant Provider exposure authority that
admitted the reservation. For `independently-enforceable`, it is instead
produced and authorized by the Agreement-bound independent exposure-operation
Adapter and exact `post_acceptance_exposure_release` stage Action Authority,
both outside the deleted Guarantor control closure. That Adapter initializes its
release record solely from the verified original admission receipt and
activation evidence and linearizes one release under its own bound state domain.
The first independent call expects absent revision zero and atomically creates
terminal released revision one; exact retry resolves that record. It neither
claims to mutate a deleted Provider's private ledger nor requires that ledger
to be online. In either mode, the `portfolio.release`
action embeds the original authorized exposure-admission receipt and binds the
exact terminal claim set, terminal payouts, any collateral release, expected
reservation and selected release-state revision, and released amount. The authority
recomputes the reservation-scope digest and rejects an admission receipt from
another offer, coverage, asset, policy bucket, or correlation bucket.
The selected authority atomically writes the permanent action resolution and
the final release record. The lower-assurance Provider authority also decrements
its asset and correlation buckets; the independent Adapter records the exact
released scope for portable resolution and later Provider reconciliation. It
then signs or otherwise authorizes the receipt under the Agreement-selected
profile. Guarantor V1 permits only a final exposure-release receipt:
`release_sequence` is exactly 1, the predecessor is absent,
`released_exposure` equals the still-reserved amount, and
`remaining_reserved_exposure` is zero. Implementations may track paid losses
and reduced remaining liability internally, but they retain the accepted
reservation until this terminal release rather than inventing an
interoperability-visible partial-release rule.

The receipt's `authority_id` is the Provider exposure authority only for the
two lower assurance levels. For `independently-enforceable`, it is the exact
non-Guarantor admission authority fixed by the exposure-operation Adapter
profile and stage binding. `release_state_domain_digest` always equals the
stage binding's resolved `portfolio_exposure_state_domain`; lower assurance may
map that domain to the Provider portfolio, while independent assurance must map
it to the Adapter's reservation-scoped one-shot record. The Action, Fence,
portable stage-admission evidence, receipt authorization, and resolution all
use the same selected authority and domain. Mixing the Provider authority into
the independent authorization quorum or requiring its signature after
activation invalidates the advertised assurance level.

The release request carries no disposition output. After the CAS succeeds, the
authority constructs the exact computation under
`tos.service.agent-guarantor-exposure-disposition.v1`, derives every receipt
bucket and enum from it, and embeds it with the original admission receipt in
the authorized result. The body digest, embedded computation digest, release
projection's admission-receipt digest, and complete embedded admission envelope
must all agree. This output-only construction prevents a caller from selecting
which loss bucket restores capacity.

Removing an amount from the reservation bucket does not necessarily return it
to underwriting capacity. The release authority derives, rather than accepts,
the exact `ExposureDispositionComputationV1` from the original embedded
exposure-admission receipt, its reservation scope, and the authorized terminal
claim set. V1 deliberately gives no capacity credit for later reimbursement,
subrogation, collateral recovery, or an accounting estimate; such value is a
separate fenced income/reconciliation action and never rewrites this receipt.
Checked same-asset arithmetic requires:

```text
released_exposure = original still-live reserved_exposure
cumulative_approved_amount
  = cumulative_paid_amount + cumulative_defaulted_amount
outstanding_approved_amount = 0

if default_liability_disposition = charge_off:
  realized_loss = cumulative_paid_amount + cumulative_defaulted_amount
  retained_defaulted_liability = 0

if default_liability_disposition = retain:
  realized_loss = cumulative_paid_amount
  retained_defaulted_liability = cumulative_defaulted_amount

returned_to_available_exposure
  = released_exposure - realized_loss - retained_defaulted_liability

released_exposure
  = returned_to_available_exposure
  + realized_loss
  + retained_defaulted_liability
```

All arithmetic is checked in the reservation asset; an underflow, asset
mismatch, or total exceeding the original reservation fails closed. The
`default_liability_disposition` is frozen in the reservation scope before the
firm offer and cannot be selected at release. `portfolio_disposition` is
`residual_release`, `realized_loss`, or `retained_defaulted_liability` when
exactly that one bucket is nonzero, and `mixed` when two or more are nonzero;
a zero reservation is forbidden. Paid value is always realized loss to this
underwriting reservation even when a selected collateral position supplied the
payment bytes. Collateral disposition is independently proved but cannot make
spent coverage capacity available again. A generic `state = released` receipt,
caller-supplied bucket split, or computation that omits the original admission
receipt cannot close coverage or support a new offer.

For a selected collateral profile,
`collateral_disposition_evidence_set` is required and proves the exact terminal
release, consumption, exhaustion, or default state permitted by the closure
matrix; unsecured coverage omits it. The exposure-release body, projection,
action, and later coverage resolution all commit the byte-identical set digest.
Calling every terminal disposition a release, substituting eligibility proof,
or omitting a consumed/defaulted position is invalid.

For a nonempty log, `claim_resolutions` contains exactly one entry for every
contiguous admission sequence from 1 through `admission_high_water`, in that
order. The envelope first verifies its exact authorized filing-close receipt;
the receipt's Agreement, obligation, reason branch, frozen high-water, root,
and coverage revision must equal the terminal-set body. Each entry then binds
the exact authorized admission receipt, final claim revision, terminal decision
and decision-admission receipt where required, every materialized payout
obligation, and its terminal settlement evidence. It also proves the initial
receipt at that coverage-level sequence and a contiguous per-claim revision log
from 1 through the stated revision high-water, ending in the named final body
and receipt. Revisions never create another coverage-level entry. For an empty
log, the high-
water is zero, the list is empty, and the accepted authority must still prove
the filing-close transition. A sparse list, duplicate or skipped sequence,
unknown action, nonterminal challenge, outstanding approved amount, changed
log root, or mismatch with the authority's frozen close revision is not
release eligible.

`claim_resolution_bundles[]` carries exactly the canonical objects named by
each body reference: one initial receipt and the complete contiguous revision-
receipt chain, each with its exact embedded ingress receipt and the sole claim
carried by that receipt, plus the terminal
authorized decision where required,
complete contiguous claim-state transition receipts through the named terminal
receipt, terminal authorized decision, the complete decision-admission receipt chain,
decision-application receipt,
materialized obligation set, and terminal payout evidence. Every admitted claim
must reach a final approved, partially approved, or denied decision after its
challenge rules; withdrawal or an invalid assertion is denied under the
selected profile rather than closed through an unaudited local shortcut. The verifier
recomputes every ingress, claim body and envelope digest, predecessor body and receipt
digest, revision-log leaf/root, and reference, and rejects a missing, extra,
reordered, or digest-only bundle. The last receipt's ingress-resolved authorized
claim is the terminal claim and its complete envelope digest equals
`terminal_authorized_claim_envelope_digest`; no separately retained final body
may substitute for it. Its length and order equal `claim_resolutions`; both are
empty for a zero-claim cut.

`decision_admission_receipts[]` is the complete bounded predecessor-linked
decision-log chain from sequence 1/revision 1 through the terminal decision's
admission receipt. The terminal element digest equals
`terminal_decision_admission_receipt_digest`; no receipt recursively embeds its
predecessor. A gap, fork, duplicate sequence/revision, missing nonterminal
decision, or terminal receipt found only in mutable storage fails verification.
Every receipt's embedded revision-ingress cut is verified; the final cut's
high-water and root equal the terminal resolution reference, and every revision
ingress through that cut is admitted or terminally rejected. A terminal bundle
cannot omit a revision that won the race before its decision snapshot.

The decision-application receipt's embedded terminal claim-state transition
receipt must equal the terminal receipt named by its resolution reference and
must select the same decision-admission receipt and authorized decision. The
decision-admission receipt digest must equal the resolution reference and its
per-claim decision-log predecessor must be complete. A verifier rejects a
bundle that splices an authorization, admission, close receipt, decision, or
materialized payout set from another claim state.

The evidence profile is selected inside the coverage Agreement. It defines how
the verifier proves the admission-log root, close transition, authority or
quorum, state revision, historical keys, and atomic snapshot. Under
`unsecured-signed`, this may be a signed assertion by the rollback-resistant
Provider lifecycle authority and carries only that assurance. Under
`collateral-attested` or `independently-enforceable`, the selected Collateral
Adapter MUST verify under its exact selected profile the same admission high-
water and prevent release while any admitted claim or payout remains open or
ambiguous. For `collateral-attested`, that statement does not imply Adapter,
custodian, or controller independence; only `independently-enforceable` must
also pass the control-deletion and direct-route rules. A
Provider-generated list, Merkle root, `open_claim_count = 0`, or clock reading
alone never upgrades assurance.

`AuthorizedTerminalClaimSetEvidenceV1` proves the claim cut selected by the
Agreement. Every authorization element names `terminal-claim-set`, commits the
exact recomputed body digest, and satisfies the Agreement-selected claim-
admission authority profile and quorum. It does not itself move collateral.
Release is a separate
`collateral.transition` whose canonical request binds this evidence digest,
the expected collateral state, and every applicable challenge, reorg, and
recovery cutoff. The release CAS and any competing claim admission or payout
share the Adapter's state domain. `AuthorizedCoverageResolutionV1` is a final
recoverable aggregation after all selected releases; its authorization remains an
authority assertion and never substitutes for the underlying terminal
evidence.

## 20. Semantic action identity

Guarantor V1 reuses the released registry wherever the semantic effect is
already generic:

- `publication.publish` and `publication.withdraw`;
- `messenger.contact` and `messenger.send`;
- `agreement.propose`, `agreement.authorize`, and `agreement.withdraw`;
- `portfolio.reserve` and `portfolio.release`;
- `billing.materialize` and `billing.resolve`;
- `payment.direct` and `settlement.external`;
- `reconcile.apply`; and
- a released Adapter-specific transition for a selected escrow or contract.

Paid Demand's `provider.offer` entry is not reusable because its semantic key
contains a Demand Mutation and Paid Demand offer identity. V1 proposes these
business-neutral additive entries at registry version 1, entry version 1:

| Action kind | Ordered semantic fields | Successor policy |
| --- | --- | --- |
| `commercial.quote.issue` | `owner_id:id`, `agent_id:id`, `agreement_body_digest:digest32`, `quote_request_digest:digest32`, `recipient_set_digest:digest32`, `authority_instance_id:digest32`, `offer_terms_digest:digest32` | none |
| `commercial.quote.close` | `owner_id:id`, `agent_id:id`, `agreement_body_digest:digest32`, `authority_instance_id:digest32`, `reservation_id:digest32`, `expected_offer_state_revision:u64`, `target_state:state` | none |
| `conditional.claim.ingress` | `owner_id:id`, `agent_id:id`, `agreement_body_digest:digest32`, `obligation_id:id`, `claim_id:id`, `claim_revision:u64` | none |
| `conditional.claim.submit` | `owner_id:id`, `agent_id:id`, `agreement_body_digest:digest32`, `obligation_id:id`, `authority_instance_id:digest32`, `claim_body_digest:digest32` | authority_instance |
| `conditional.claim-filing.close` | `owner_id:id`, `agent_id:id`, `agreement_body_digest:digest32`, `obligation_id:id`, `claim_admission_log_id:id`, `expected_coverage_revision:u64`, `expected_claim_filing_state_revision:u64`, `filing_cutoff_unix:u64`, `target_state:state` | terminal_successor |
| `conditional.claim-decision.admit` | `owner_id:id`, `agent_id:id`, `agreement_body_digest:digest32`, `obligation_id:id`, `claim_id:id`, `admission_mode:kind`, `source_claim_revision:u64`, `source_claim_state_revision:u64`, `source_head_digest:digest32`, `decision_sequence:u64`, `mode_specific_identity_digest:digest32` | none |
| `conditional.claim.decide` | `owner_id:id`, `agent_id:id`, `agreement_body_digest:digest32`, `obligation_id:id`, `authorized_claim_envelope_digest:digest32`, `decision_application_token_id:digest32`, `expected_coverage_revision:u64`, `expected_claim_revision:u64`, `expected_claim_state_revision:u64`, `decision_sequence:u64`, `decision_revision:u64`, `target_state:state` | terminal_successor |
| `conditional.claim.transition` | `owner_id:id`, `agent_id:id`, `agreement_body_digest:digest32`, `obligation_id:id`, `claim_id:id`, `expected_claim_state_revision:u64`, `transition_kind:kind`, `target_state:state`, `evidence_set_digest:digest32` | terminal_successor |
| `conditional.obligation.transition` | `owner_id:id`, `agent_id:id`, `agreement_body_digest:digest32`, `obligation_id:id`, `expected_state_revision:u64`, `target_state:state`, `evidence_set_digest:digest32` | terminal_successor |
| `collateral.transition` | `owner_id:id`, `agent_id:id`, `agreement_body_digest:digest32`, `obligation_id:id`, `collateral_position_id:id`, `transition_binding_digest:digest32`, `expected_state_revision:u64`, `transition_kind:kind` | terminal_successor |

Each domain tag is `tos.semantic-action.<action_kind>.v1`. The existing binary
framing and digest algorithm remain unchanged; adding entries does not change
any released stable ID.

For `commercial.quote.issue`, `authority_instance_id` is exactly `offer_id`.
`offer_terms_digest` is `Digest("tos.service.agent-guarantor-firm-offer-issuance-terms.v1",
unsigned_offer_template)` from section 14; the authority-generated exposure
receipt and authorization bytes cannot enter their own request digest or
semantic preimage. The sink recomputes both fields from the canonical issuance
body and rejects caller-supplied alternatives.

For `commercial.quote.close`, `target_state` is exactly `expired` and is derived
from `release_reason`. A terminal-negative issuance
never invokes this action. The sink derives the
Agreement, authority instance, reservation, revisions, and target from
`OfferNonAcceptanceResolutionActionBodyV1`; it does not accept an independent
semantic-field map. The action atomically produces
`AuthorizedOfferNonAcceptanceEvidenceV1` in the same offer/acceptance admission
domain. A losing or unknown close cannot release exposure, and no terminal
successor can reopen the offer.

For `conditional.claim.ingress`, the sink derives every semantic field from
`ClaimSubmissionIngressActionBodyV1.authorized_claim`. The body and complete
authorization-envelope bytes remain in the exact request digest but are not in
the stable key. Consequently one claim ID/revision has one durable ingress
identity: changing the claim, manifest, or authorization wrapper conflicts
rather than creating another inbox item. The operation creates exactly one
receipt slot and has no semantic successor.

For `conditional.claim-filing.close`, `target_state` is exactly `frozen` and
all fields are derived from `ClaimFilingCloseActionBodyV1`. A normal close uses
the Agreement filing cutoff; a never-activated close uses the activation cutoff
and exact non-activation evidence. A stale high-water or root conflicts before
state mutation, and a successor is admitted only after the prior action is
terminal.

For `conditional.claim-decision.admit`, the sink derives the common fields from
the closed action variant and its exact source objects. It constructs
`ClaimDecisionSourceHeadV1` in the field order shown in section 17.4 and
computes:

```text
source_head_digest = Digest(
  "tos.service.agent-guarantor-claim-decision-source-head.v1",
  ClaimDecisionSourceHeadV1)
```

The authorized claim-admission receipt and exact revision-epoch expectation are
always present and use their complete released digests. The authority-produced
decision-snapshot ingress-cut proof is a result and cannot enter this source
head or the request from which it is derived. Optional-field presence is closed
and path-dependent. `late_filing_close_receipt_digest` is present exactly for
`late_recovery_terminal_fallback`, is the complete authorized-envelope digest,
and equals the receipt embedded in the tagged variant; it is absent for every
other path:

| Admission path | Current decision receipt | Current state-transition receipt |
| --- | --- | --- |
| ordinary `initial` | absent | absent |
| ordinary `successor` | exact predecessor decision-admission receipt | exact current transition receipt |
| `initial_terminal_fallback` (`decision_sequence = 1`) | absent | absent |
| `terminal_fallback` from `evidence_required` or `disputed` | exact current decision-admission receipt | absent |
| `terminal_fallback` from `reviewing` after a transition | exact current decision-admission receipt | exact current transition receipt |
| `late_recovery_terminal_fallback` | current receipt when one exists; otherwise absent | current transition when one exists; otherwise absent; exact late filing-close receipt is separately mandatory |

Any other presence combination, a body-only digest, a digest that differs from
the embedded tagged variant, or a cut for another decision epoch fails before
stable-ID calculation. The two mode-specific values are canonical typed
preimages:

```text
mode_specific_identity_digest(authorized_decision) = Digest(
  "tos.service.agent-guarantor-authorized-decision-admission-identity.v1",
  AuthorizedDecisionAdmissionIdentityV1 {
    schema_version: 1,
    claim_decision_body_digest,
    decision_revision,                # exactly 1
    derived_target_state
  })

mode_specific_identity_digest(deterministic_fallback) = Digest(
  "tos.service.agent-guarantor-fallback-admission-identity.v1",
  DeterministicFallbackAdmissionIdentityV1 {
    schema_version: 1,
    fallback_profile_digest,
    trigger_cutoff_unix,
    claim_revision_epoch_expectation_digest
  })
```

The ordinary stable key commits the authorized decision body, not replaceable
signature/proof wrapper bytes; those bytes remain in the exact request digest
and conflict if changed after one variant is prepared. The fallback stable key
excludes the output decision, output authorization,
coverage revision, aggregate values, result, amount, lines, and timestamps.
Consequently every invoker, proof-wrapper choice, retry, crash recovery, and
writer takeover for one source head resolves one action slot and its one stored
output. The exact request digest covers the immutable tagged request. This
action is the sole mutation that admits a decision into the per-claim log;
authorization bytes alone cannot consume a sequence or start a challenge
window.

For this profile, `commercial.quote.issue` is the one composite Provider-
authority admission that creates the private portfolio reservation and the
authorized firm offer atomically. An implementation MUST NOT first admit an
independent `portfolio.reserve` and later let an ordinary Agent signer issue the
offer across a fencing gap. `portfolio.reserve` remains available for other
generic workflows. `portfolio.release` resolves an unaccepted Guarantor
reservation only through section 14.4, or an accepted coverage reservation only
after the terminal rules in section 19. The exact `release_variant`, request-
body schema, and profile-specific terminal-evidence projection distinguish the
two paths; neither can satisfy the other's verifier.

`conditional.claim.decide` deliberately leaves amount, evidence, and
destination out of the semantic key but includes them in the exact request
digest. The token ID binds those economic fields indirectly through the exact
authorized decision and decision-admission receipt. A second request against
the same token and base revision with different bytes is a conflict. A
current-revision CAS loser may use a terminal successor that binds the same
still-pending token, exact predecessor terminal resolution, and newly observed
base revision. It does not authorize different economics or a second payout.

For decision application, `expected_claim_state_revision` is the exact
resulting revision in the embedded terminal challenge-close receipt;
the application receipt's prior and applied claim-state revisions both equal
that value, because payout materialization consumes a terminal state but does
not invent a second claim-state transition. `target_coverage_revision` is the
checked current base coverage revision plus one. The registry's
`expected_coverage_revision` is derived from the request's
`expected_current_coverage_revision`; it is deliberately not required to equal
the embedded decision-admission receipt's older admitted revision. The
`decision_application_token_id` is derived from the exact pending token, whose
Agreement, obligation, claim, decision, reserved amount, revision, and state
must equal the decision-admission receipt. The sink
rejects a close receipt
that selects another decision, is nonterminal, has a pending/ambiguous
challenge, or was already consumed by a different application action.

`target_aggregate_pending_decision_reserve` is the checked subtraction of the
token's reserved amount from
`expected_aggregate_pending_decision_reserve`. The application authority CASes
both that aggregate value and the current coverage revision. A CAS loser may
create only a registry-authorized terminal successor against a newly observed
revision; the exact token remains pending. Unknown or ambiguous actions cannot
be rebased, and a successfully consumed token cannot be named by a successor.

The action body's `target_claim_state`, the semantic registry's `target_state`,
and the embedded terminal close receipt's `resulting_claim_state` are exact
equality. They are not independently supplied interpretations. V1 permits only
this mapping from the same embedded final decision:

| Final decision result | Required resulting and target claim state |
| --- | --- |
| `approved` | `final_approved` |
| `partially_approved` | `final_partially_approved` |
| `denied` | `final_denied` |

No other decision result or claim state is valid for
`conditional.claim.decide`. The sink derives the semantic field from the
receipt, checks the body field against it, and checks the table against the
authorized decision before calculating the stable ID. This is a read-and-
materialize target: decision application does not advance the claim-state
revision a second time.

If another claim legitimately advances the coverage revision before decision
admission, the admission authority rereads that revision and aggregate state in
its serializable transaction. An ordinary exact amount that no longer fits is
terminally `rejected` with the noncanonical local diagnostic
`capacity_exhausted`, without a profile result or decision entry. A
deterministic fallback
stays under the same prepared stable action and is recomputed from the newest
state until that action commits or a source-head conflict becomes terminal.
Neither path creates a V1 decision rebase or another decision revision.

For `collateral.transition`, the sink derives
`transition_binding_digest` from the exact binding embedded in
`CollateralTransitionActionBodyV1`; it does not accept a caller-supplied Adapter
or evidence-profile digest as the semantic field. The kind, Adapter request
content type, prerequisite roles, destination rule, and target state must match
that binding and section 18 before stable-ID calculation. The returned
`AuthorizedCollateralEvidenceV1` commits the same action body, action identity,
request digest, binding, and verified Adapter result.

The `collateral-backed-payout` operation is the sole exception to standalone
`collateral.transition` dispatch. Its semantic-field derivation profile reads
the released `settlement.external` fields exclusively from the embedded
`AgreementPaymentRequestV2` and exact materialized obligation, recomputes the
same stable ID, and forbids an independently supplied field map. Its generic
exact request digest covers the complete
`CollateralBackedAgreementPaymentActionBodyV1`, including the nested payment,
obligation set, and collateral transition. The nested payout transition does
not receive another stable action ID. Changing either half while retaining the
same payment identity is therefore `conflict`; allocating a second identity for
the same transfer is invalid.

Stable identity is not authorization. Every mutating request also carries an
`AuthorizedActionV1`, current `WriterFenceV1`, exact request digest, policy and
mandate references, expected prior state, expiry, and authority proof. For
lower assurance this may be the Agreement-selected owner/provider authority;
for an independent stage it is exactly the immutable independent authority and
fence binding above. Every sink validates the selected writer high-water and durably exposes
`ResolveAction(stable_action_id, exact_request_digest)`.

For `conditional.claim-decision.admit`, the Authorized Action's expected prior
state is the immutable `source_head_digest` and claim-state revision from the
tagged request. It must not include a shared coverage revision, aggregate
balance, output decision, or output token. The authority resolves and locks
those volatile coverage values internally; this stage-specific rule prevents
the generic expected-state field from reintroducing a caller-driven fallback
rebase.

### 20.1 Canonical mutation request bodies

Every Guarantor mutation consumes one registered canonical request body. The
sink receives its exact deterministic-CBOR bytes, bounded-decodes and
re-encodes them, derives the semantic-action fields itself, and checks both the
stable ID and generic exact-request digest. A caller cannot provide a decoded
object or semantic-field map that disagrees with those bytes.

`FirmOfferIssuanceActionBodyV1`,
`OfferNonAcceptanceResolutionActionBodyV1`,
`PreAcceptanceExposureReleaseActionBodyV1`,
`ClaimSubmissionIngressActionBodyV1`, `ClaimSubmissionActionBodyV1`,
`ClaimFilingCloseActionBodyV1`, and `ClaimDecisionAdmissionActionBodyV1` are
defined in sections 14 and 17. The remaining bodies are:

```text
TransitionEvidenceDigestRefV1 {
  evidence_role                    # released per-action role
  digest_kind                     # authorized_envelope, canonical_set,
                                  # or canonical_object
  object_digest
}

TransitionEvidenceProjectionV1 {
  schema_version
  purpose
  coverage_agreement_body_digest
  obligation_id
  claim_id?
  target_state
  evidence_digests[]                # canonical TransitionEvidenceDigestRefV1 set
}

ExposureReleaseEvidenceProjectionV1 {
  schema_version
  coverage_agreement_body_digest
  coverage_obligation_id
  reservation_id
  exposure_admission_receipt_digest
  terminal_claim_set_evidence_digest
  terminal_payment_evidence_set_digest
  collateral_disposition_evidence_set_digest?
}

CoverageAcceptanceAdmissionActionBodyV1 {
  schema_version
  authorized_acceptance_request
  transition_evidence_projection
  expected_reservation_revision
  expected_offer_state_revision
  target_offer_state_revision
  expected_coverage_revision
  target_coverage_revision
  expected_claim_filing_state           # exactly uninitialized
  target_claim_filing_state             # exactly not_open
  expected_claim_filing_state_revision  # exactly 0
  target_claim_filing_state_revision    # exactly 1
}

CoverageActivationActionBodyV1 {
  schema_version
  underlying_agreement_body
  underlying_authorization_evidence_set
  authorized_acceptance_receipt
  fee_prerequisite_evidence_set?
  collateral_evidence_set?
  collateral_control_evidence?
  operational_independence_evidence_set?
  target_coverage_end_commitment      # exact scheduled CoverageEndCommitmentV1
  transition_evidence_projection
  expected_coverage_revision
  target_coverage_revision
  expected_claim_filing_state           # exactly not_open
  target_claim_filing_state             # exactly open
  expected_claim_filing_state_revision
  target_claim_filing_state_revision
}

CoverageNonActivationActionBodyV1 {
  schema_version
  authorized_acceptance_receipt
  activation_admission_cut_proof
  non_activation_reason_evidence
  fee_resolution_evidence_set?
  collateral_non_activation_evidence_set?
  transition_evidence_projection
  expected_coverage_revision
  target_coverage_revision
  target_coverage_state               # exactly not_activated_confirmed
  expected_claim_filing_state         # exactly not_open
  target_claim_filing_state           # exactly not_open
  expected_claim_filing_state_revision
  target_claim_filing_state_revision  # exactly equals expected
}

CoverageCancellationActionBodyV1 {
  schema_version
  authorized_cancellation_request
  expected_coverage_end_commitment   # exact scheduled CoverageEndCommitmentV1
  transition_evidence_projection
  expected_coverage_revision
  target_coverage_revision
  target_coverage_state               # exactly coverage_ended
}

ClaimDecisionApplicationActionBodyV1 {
  schema_version
  authorized_claim_decision_digest
  authorized_claim_admission_receipt_digest
  authorized_claim_decision_admission_receipt_digest
  authorized_terminal_claim_state_transition_receipt_digest
  decision_application_token
  expected_coverage_end_commitment_digest
  payout_template_digest
  expected_current_coverage_revision
  target_coverage_revision
  expected_aggregate_pending_decision_reserve
  target_aggregate_pending_decision_reserve
  expected_application_token_revision
  expected_claim_state_revision
  target_claim_state
  expected_next_payout_sequence
  expected_materialized_payout_line_digest?
}

ClaimStateTransitionActionBodyV1 {
  schema_version
  coverage_agreement_body_digest
  coverage_obligation_id
  claim_id
  transition_kind
  expected_claim_state_revision
  target_state
  expected_challenge_rounds_used
  target_challenge_rounds_used
  expected_nonterminal_rounds_used
  target_nonterminal_rounds_used
  successor_decision_due_at_unix?
  authorized_claim_decision_admission_receipt_digest
  transition_evidence_projection
  transition_evidence_set
}

CollateralTransitionActionBodyV1 {
  schema_version
  coverage_agreement_body_digest
  obligation_id
  collateral_position_id
  transition_binding                 # exact CollateralTransitionBindingV1
  transition_kind
  expected_state_revision
  expected_state_digest
  asset
  amount
  payout_destination_digest?
  prerequisite_evidence_set
  adapter_request                     # exact CollateralAdapterRequestV1
}

CollateralBackedAgreementPaymentActionBodyV1 {
  schema_version
  agreement_payment_request           # exact AgreementPaymentRequestV2
  settlement_obligation               # exact materialized SettlementObligationV1
  materialized_payout_obligation_set  # exact containing set
  collateral_transition_action        # exact payout CollateralTransitionActionBodyV1
}

CoverageClosureActionBodyV1 {
  schema_version
  coverage_agreement_body_digest
  coverage_obligation_id
  claim_filing_close_receipt_digest
  expected_coverage_end_commitment_digest # derived from the filing-close receipt
  claim_resolution_bundles[]          # exact, admission-sequence order
  claim_resolution_ref_set            # exact derived ClaimTerminalResolutionRefSetV1
  closure_reason
  expected_coverage_revision
  target_coverage_revision
  target_coverage_state               # exactly release_pending
  expected_claim_set_revision
  target_claim_set_revision
  coverage_closure_evidence_context
  terminal_prerequisite_evidence_set
  fee_resolution_evidence_set?
  collateral_release_eligibility_evidence_set?
  transition_evidence_projection
}

CoverageResolutionActionBodyV1 {
  schema_version
  authorized_exposure_release_receipt_digest
  expected_coverage_revision
  target_coverage_revision
}

The resulting `AuthorizedCoverageResolutionV1` carries the complete exposure
release receipt exactly once. Its stage request binds that envelope by digest;
the verifier recomputes the digest from the carried predecessor before checking
the action. This is the only released V1 encoding and keeps the final portable
resolution within the global complete-object ceiling.

ExposureReleaseActionBodyV1 {
  schema_version
  release_variant                       # exactly post_acceptance
  coverage_agreement_body_digest
  coverage_obligation_id
  reservation_id
  authorized_exposure_admission_receipt
  authorized_terminal_claim_set_evidence
  terminal_payment_evidence_set
  collateral_disposition_evidence_set?
  release_evidence_projection
  release_state_domain_digest
  expected_release_state_revision
  expected_reserved_exposure
}
```

Every embedded object is the exact canonical object, not an unresolvable
digest. Large evidence uses the immutable descriptors inside the embedded
evidence set. The surrounding `AuthorizedActionV1`, Writer Fence, retry,
transport, and eventual receipt are excluded from request-body bytes. Same
stable ID with different bytes is `conflict`; same bytes after timeout are
resolved or retried exactly. Approval and payout-obligation materialization
occur in one authority transaction; each resulting payment later uses its
existing `billing.materialize` and payment/settlement action identities.

For any `conditional.obligation.transition`, the registry's
`evidence_set_digest` is the digest of the exact
`TransitionEvidenceProjectionV1`. The sink reconstructs its sorted member
references from the request's embedded offer, authorization, prerequisite,
terminal, fee, and collateral objects as applicable and requires exact
equality; the projection cannot omit an object or add an unverified digest.
`evidence_digests[]` is sorted by
`(evidence_role, digest_kind, object_digest)` and rejects duplicate roles.
`authorized_envelope` means the complete canonical envelope under its released
complete-envelope domain. `canonical_set` means the complete canonical set
object under its released set-object domain. `canonical_object` means the
complete released canonical object under the exact role-defined object domain.
A body digest, digest of encoded
digest text, wrapper digest, set-member digest, or caller-selected alternate
kind is invalid. Each action purpose releases its allowed roles, kind, source
field, and cardinality; unknown roles fail closed.

The `coverage-acceptance` projection contains exactly `acceptance_request` from
`authorized_acceptance_request` under
`tos.service.agent-guarantor-acceptance-request-envelope.v1` and `firm_offer` from
`ResolveAcceptanceFirmOfferV1(authorized_acceptance_request)` under
`tos.service.agent-guarantor-firm-offer-envelope.v1`, both with kind
`authorized_envelope`; its target is `pending_prerequisites`. The resolver
verifies the embedded Agreement and complete authorization-evidence set,
requires exactly one Guarantor firm-offer evidence group, verifies its complete
offer, and rejects zero, multiple, conflicting, body-only, or alternate-wrapper
offers. The action and receipt contain no second offer copy.
The sink also requires `target_coverage_revision =
expected_coverage_revision + 1`, expected filing state/revision exactly
`uninitialized/0`, and target exactly `not_open/1`, then stores all related
state and the accepted-effect result atomically.

The `coverage-activation` projection contains these required members:
`coverage_authorizations` from the acceptance request nested in the accepted
receipt and `underlying_authorizations` from the action, each kind
`canonical_set` under
`tos.service.agent-guarantor-agreement-authorization-evidence-set.v1`;
`firm_offer` from the same resolver path and `acceptance_receipt` from the
action, each kind `authorized_envelope` under their released envelope domains;
and the exact conditional members
`fee_prerequisites`, `collateral`, and `operational_independence`, each kind
`canonical_set` under `tos.service.agent-guarantor-evidence-set.v1` when and only when
its corresponding action-body field is required. It also contains
`collateral_control`, kind `authorized_envelope`, from
`collateral_control_evidence` under
`tos.service.agent-guarantor-collateral-control-evidence-envelope.v1` if and
only if the selected disclosure is `third_party_control_asserted`. Its target
is `active`.
The activation action requires target coverage and claim-filing revisions to be
their checked predecessors plus one and the filing transition exactly
`not_open -> open`; the evidence body copies those four state/revision values.
For `independently-enforceable`, the mutation uses the exact
`coverage_activation` stage entry and coverage-operation Adapter.

`CoverageNonActivationActionBodyV1` uses
`conditional.obligation.transition` with projection purpose
`coverage-non-activation` and target `not_activated_confirmed`. Its projection
contains exactly `firm_offer`, resolved through its embedded acceptance receipt,
and that `acceptance_receipt` as authorized-envelope digests; `activation_cut`
with kind `canonical_object` as the canonical
`ActivationAdmissionCutProofV1` digest under
`tos.service.agent-guarantor-activation-cut-proof.v1`;
`non_activation_reason` as the canonical
`CoverageNonActivationReasonEvidenceV1` digest under
`tos.service.agent-guarantor-non-activation-reason-evidence.v1`; and the
conditional canonical-set roles
`fee_resolution` and `collateral_non_activation` exactly when their action-body
fields are present. The sink validates the Agreement-bound reason rule,
complete zero-acceptance cut, current Writer Fence and revision, and every
embedded object in one admission. `target_coverage_revision` is the expected
revision plus one.
Its target claim-filing state and revision are byte-identical to the expected
`not_open` values; the result body proves that no filing revision advanced.
The produced non-activation envelope repeats those exact objects and cannot
substitute a Provider-local empty log.
For `independently-enforceable`, the mutation and activation-cut freeze use the
distinct `coverage_non_activation` stage entry and the same bound coverage-
operation Adapter/state domain as activation.

`CoverageCancellationActionBodyV1` also uses
`conditional.obligation.transition`. Its projection purpose is
`coverage-cancellation`, target is `coverage_ended`, and it contains
exactly one `cancellation_request` role of kind `authorized_envelope` from the
embedded `AuthorizedCoverageCancellationRequestV1` under
`tos.service.agent-guarantor-cancellation-request-envelope.v1`. The sink
derives the Agreement, obligation, policy branch, effective interval, expected
revision, and target from the exact embedded objects. It requires
`target_coverage_revision = expected_coverage_revision + 1`, atomically stores
the cutoff/end-reason fields from section 15.4, persists the action, and returns
the authorized cancellation receipt. For `independently-enforceable`, every
Action Authority, Writer Fence, resolver, and state-domain check comes from the
exact `coverage_cancellation` independent-stage entry. Reusing the filing-close
or Guarantor lifecycle entry without that explicit binding is invalid.

`CoverageClosureActionBodyV1` uses
`conditional.obligation.transition` with projection purpose
`coverage-closure`. Its `terminal_prerequisite_evidence_set` becomes the exact
`coverage_closure_evidence_set` in the authorized terminal claim-set envelope.
Its `coverage_closure_evidence_context` is the exact cycle-free context defined
in section 19.6. The authority resolves the exact canonical
`AgentAgreementBodyV1` only through
`ResolveFilingCloseCoverageAgreementV1` on the embedded authorized filing-close
receipt, recomputes `coverage_agreement_body_digest`, and derives the coverage
obligation and every closure deadline or profile from it. The action cannot
carry or select a second Agreement copy. Before admitting the action, the
authority reconstructs the
complete ordered `claim_resolutions[]` from the embedded portable bundles,
requires byte equality with `claim_resolution_ref_set.refs[]`,
computes `claim_resolution_set_digest`, verifies the amount invariant, derives
the reason/state pair, and requires every field of the supplied context to
match. It then recomputes `coverage_closure_context_digest`, requires that
digest as the terminal-prerequisite set's context, and derives the resulting
terminal-set body. Neither the request nor any context field may depend on the
resulting terminal-set body digest.
V1 has one terminal-claim-set slot per coverage obligation. The closure request
requires `expected_claim_set_revision = 0` and
`target_claim_set_revision = 1`; the resulting body has
`claim_set_revision = 1`. In the same serializable transaction, the authority
compares the coverage state/revision, both claim-set revisions, frozen filing
root/high-water, the exact receipt-derived coverage-end commitment digest, and every final
per-claim revision root, persists the action
resolution and terminal set, and moves coverage to `release_pending`. An exact
retry returns the same envelope. Any different action or successor after slot
revision 1 conflicts. V1 has no predecessor terminal set or amendment path; a
future mutable terminal-set protocol requires a new schema and profile version.
For `independently-enforceable`, admission of this same generic obligation
transition uses the exact `coverage_closure` independent-stage Action Authority,
Writer Fence, generation high-water, resolver, and admission-state domain. The
`filing_close` entry cannot be silently reused: it freezes the initial-claim
cut, while `coverage_closure` authorizes the terminal set and
`release_pending` CAS.
The request embeds the exact authorized filing-close receipt; its frozen high-
water, root, cutoff, reason branch, and filing revision are the only permitted
claim cut. The sink validates `closure_reason` against the exhaustive matrix in
section 19.6 and derives the matrix's final-resolution target, but this action's
registry `target_state`, request `target_coverage_state`, and resulting live
coverage state are exactly `release_pending`. `target_coverage_revision` is the
expected revision plus one, and the registry's `expected_state_revision` is
exactly `expected_coverage_revision`. The produced terminal claim-set body commits the
same closure reason, resolution target, evidence-set digest, filing-close
receipt, claim high-water, roots, totals, and release-pending revision. It proves
release eligibility; it does not claim that collateral or Provider exposure has
already been released.

The `coverage-closure` projection has these exact members and no others:

| Evidence role | Digest kind | Exact source and digest domain | Cardinality |
| --- | --- | --- | --- |
| `filing_close` | `authorized_envelope` | `authorized_claim_filing_close_receipt`, `tos.service.agent-guarantor-claim-filing-close-envelope.v1` | exactly one |
| `coverage_cancellation` | `authorized_envelope` | the cancellation receipt resolved from `authorized_claim_filing_close_receipt`, `tos.service.agent-guarantor-cancellation-receipt-envelope.v1` | one exactly when `coverage_end_reason = accepted_cancellation`; otherwise zero |
| `terminal_prerequisites` | `canonical_set` | `terminal_prerequisite_evidence_set`, `tos.service.agent-guarantor-evidence-set.v1` | exactly one |
| `fee_resolution` | `canonical_set` | `fee_resolution_evidence_set`, `tos.service.agent-guarantor-evidence-set.v1` | one exactly when a fee disposition remains relevant; otherwise zero |
| `collateral_release_eligibility` | `canonical_set` | `collateral_release_eligibility_evidence_set`, `tos.service.agent-guarantor-evidence-set.v1` | one for a selected collateral profile; otherwise zero |

The collateral eligibility set may prove only the accepted release conditions,
position state, cutoffs, and absence of a competing admitted payout at the
closure-action base revision. It MUST NOT contain a release, consumption,
default, exposure-release, or other disposition object whose request or
authorization commits the terminal claim-set body or its envelope. Such an
object is necessarily downstream and belongs only to the later collateral,
exposure-release, and coverage-resolution actions.

`CoverageResolutionActionBodyV1` is the only request that produces
`AuthorizedCoverageResolutionV1`. It uses
`conditional.obligation.transition` for the coverage obligation and requires
the projection purpose `coverage-resolution`. The projection contains the
following exact roles and no others:

| Evidence role | Digest kind | Exact source and digest domain | Cardinality |
| --- | --- | --- | --- |
| `activation` | `authorized_envelope` | activation evidence resolved through `authorized_exposure_release_receipt.authorized_terminal_claim_set_evidence.authorized_claim_filing_close_receipt`, `tos.service.agent-guarantor-activation-evidence-envelope.v1` | one for an activated coverage; otherwise zero |
| `non_activation` | `authorized_envelope` | non-activation evidence resolved through `authorized_exposure_release_receipt.authorized_terminal_claim_set_evidence.authorized_claim_filing_close_receipt`, `tos.service.agent-guarantor-non-activation-evidence-envelope.v1` | one for never-activated coverage; otherwise zero |
| `terminal_claim_set` | `authorized_envelope` | `authorized_exposure_release_receipt.authorized_terminal_claim_set_evidence`, `tos.service.agent-guarantor-terminal-claim-set-evidence.v1` | exactly one |
| `terminal_payment_set` | `canonical_set` | `authorized_exposure_release_receipt.terminal_payment_evidence_set`, `tos.service.agent-guarantor-coverage-terminal-payout-evidence-set.v1` | exactly one |
| `final_collateral_set` | `canonical_set` | `authorized_exposure_release_receipt.collateral_disposition_evidence_set`, `tos.service.agent-guarantor-evidence-set.v1` | one exactly when selected collateral requires it; otherwise zero |
| `exposure_release` | `authorized_envelope` | `authorized_exposure_release_receipt`, `tos.service.agent-guarantor-exposure-release-receipt-envelope.v1` | exactly one |

The activation roles follow the mutually exclusive normal versus never-
activated matrix in section 19.6. `target_coverage_revision` equals the expected
revision plus one, and the expected revision equals the embedded terminal claim
set's `release_pending_coverage_revision`. The authority admits this action only
from `release_pending`, after the exact exposure-release receipt and every
selected collateral disposition are terminal and mutually consistent. The
registry's `expected_state_revision` is the request's
`expected_coverage_revision`; its `target_state` and the resulting
`CoverageResolutionBodyV1.terminal_state` are both derived from
the nested terminal claim-set body's `resolution_target_terminal_state`; the
request has no caller-supplied terminal-state field. The result wrapper embeds
byte-identical evidence, and all action, request, revision, role, kind, domain,
and projection fields must match. A locally assembled resolution digest is not
admissible.

The resolution action and result obtain the exact coverage Agreement only
through the release receipt's terminal set and
`ResolveFilingCloseCoverageAgreementV1`; neither
carries another Agreement copy. The authority requires that body's digest to
equal every Agreement commitment in the terminal set, activation or non-
activation evidence, terminal payout set, collateral evidence, and exposure-
release receipt. A missing Agreement, a digest-only reconstruction, or two
non-byte-identical copies fails closed.

For `conditional.claim.transition`, the same projection requires `claim_id` and
the registry's `evidence_set_digest` is its digest; obligation transitions
forbid that optional field. `transition_kind` is exactly one of the three V1
rows in section 17.4 and is derived from the canonical request before the
stable ID is computed. Every such projection contains role
`transition_evidence`, kind
`canonical_set`, from `transition_evidence_set` under
`tos.service.agent-guarantor-evidence-set.v1`, and role `decision_admission`,
kind `authorized_envelope`, from the exact embedded
`AuthorizedClaimDecisionAdmissionReceiptV1` under
`tos.service.agent-guarantor-claim-decision-admission-envelope.v1`. No other
role or kind is accepted. The sink derives prior/result state, round counters,
and successor cutoff from these exact objects and the Agreement; a caller-
supplied transition label or deadline cannot alter the registry projection.

For a pre-acceptance `portfolio.release`, the registry's
`terminal_evidence_set_digest` is the digest of
`PreAcceptanceExposureReleaseEvidenceProjectionV1`. For a post-acceptance
release, it is the digest of `ExposureReleaseEvidenceProjectionV1`. The sink
selects the only projection permitted by the exact request's `release_variant`,
recomputes every member from the exact embedded release objects, requires
equality with `release_evidence_projection`, and rejects cross-path evidence.
For pre-acceptance release, `target_portfolio_revision` is exactly the base
revision plus one. For post-acceptance release, the request supplies only
`expected_release_state_revision`; the selected sink derives the registry's
`target_revision` as its checked successor inside admission. The receipt's
`base_release_state_revision` and `released_release_state_revision` must equal
those two values in the Agreement-bound `release_state_domain_digest`. A caller-
supplied post-acceptance target or Provider-private revision is invalid.

## 21. AI, autonomy, and economic evaluation

OpenFox AI may:

- classify Guarantor Intents;
- summarize policies and exclusions;
- estimate expected loss, completion and payment probability;
- recommend a fee, deductible, collateral ratio, cap, or decline;
- compare evidence and Decision Authority profiles;
- propose claim outcomes for an authorized human or Agent decision role; and
- learn bounded, de-identified risk features from terminal evidence.

AI may not:

- sign a firm offer or Agreement authorization;
- expand owner limits, capital, coverage, claim, or payout caps;
- create a role or evidence profile from conversation text;
- authorize collateral, credentials, private disclosure, claim decision,
  payout, or release;
- turn its own confidence into terminal evidence;
- select a weaker profile after Agreement authorization; or
- modify a destination, asset, amount, stable action, or exact request.

An AI-backed Agent MAY be a named Decision Authority only when the Agreement
binds its Agent identity, authority resolver, capability and verifier profile,
quorum or appeal rules, and exact decision target. Its typed authorization
proves that the selected authority made the decision; it does not make the
result objective truth.

### 21.1 Guarantor economics

The deterministic owner policy admits an offer only after calculating at least:

```text
expected premium revenue
- expected payout
- capital and collateral opportunity cost
- evidence, adjudication, settlement, and execution cost
- dispute and recovery reserve
- correlated portfolio loss reserve
- owner risk margin
= expected net value
```

Unknown asset, evidence, legal-policy, decision, correlation, collateral, or
settlement inputs fail closed or require explicit owner approval. A model score
never substitutes for the aggregate portfolio admission transaction.

The Provider-private exposure ledger separates:

- gross maximum liability;
- verified eligible collateral credit;
- net unsecured exposure;
- quote reservations;
- active coverage exposure;
- admitted and approved claim reserve;
- cumulative payout;
- premium receivable, collected, earned, and refunded;
- collateral locked, consumed, and released;
- disputed, ambiguous, defaulted, and written-off amounts; and
- risk and correlation bucket totals.

All amounts are keyed by exact asset identity and canonical atomic unit. An old
scalar `maximum_loss` counter is not sufficient for a multi-asset Guarantor.

## 22. Generic Messenger carriage

Carrier publication uses the existing generic Intent path. Negotiation may use
ordinary authenticated conversation, but every authority-changing object uses
a typed, non-model delivery path.

Current Messenger economic delivery is closed over known event kinds and a
one-shot Agreement delivery cannot represent repeated claims. V1 therefore
requires one generic, business-neutral envelope rather than a family of
Guarantor-specific Messenger opcodes:

```text
CommerceProfileEventV1 {
  schema_version
  profile_uri
  profile_version
  object_kind
  object_content_type
  object_digest
  object_size_bytes
  carriage_kind                    # inline or content_addressed
  related_intent_digest?
  agreement_body_digest?
  obligation_ids[]
  canonical_object_bytes?          # present exactly for inline
  object_descriptor?               # present exactly for content_addressed
  created_at_unix
  expires_at_unix
}

CommerceObjectDescriptorV1 {
  content_type
  content_digest
  content_size
  retrieval_hints[]                # untrusted candidate locators
}
```

For profile URI `tos.agent-service.guarantor.v1`, V1 freezes this dispatch
registry:

| Object kind | Canonical object type |
| --- | --- |
| `quote-request` | `AuthorizedCoverageQuoteRequestV1` |
| `firm-offer` | `AuthorizedFirmCoverageOfferV1` |
| `offer-non-acceptance-evidence` | `AuthorizedOfferNonAcceptanceEvidenceV1` |
| `pre-acceptance-exposure-release-receipt` | `AuthorizedPreAcceptanceExposureReleaseReceiptV1` |
| `acceptance-request` | `AuthorizedCoverageAcceptanceRequestV1` |
| `acceptance-receipt` | `AuthorizedCoverageAcceptanceReceiptV1` |
| `activation-evidence` | `AuthorizedCoverageActivationEvidenceV1` |
| `non-activation-evidence` | `AuthorizedCoverageNonActivationEvidenceV1` |
| `cancellation-request` | `AuthorizedCoverageCancellationRequestV1` |
| `cancellation-receipt` | `AuthorizedCoverageCancellationReceiptV1` |
| `collateral-control-evidence` | `AuthorizedCollateralControlEvidenceV1` |
| `collateral-evidence` | `AuthorizedCollateralEvidenceV1` |
| `claim` | `AuthorizedCoverageClaimV1` |
| `claim-ingress-receipt` | `AuthorizedClaimSubmissionIngressReceiptV1` |
| `claim-admission-receipt` | `AuthorizedClaimAdmissionReceiptV1` |
| `claim-filing-close-receipt` | `AuthorizedClaimFilingCloseReceiptV1` |
| `claim-decision` | `AuthorizedClaimDecisionV1` |
| `claim-decision-admission-receipt` | `AuthorizedClaimDecisionAdmissionReceiptV1` |
| `claim-decision-application-receipt` | `AuthorizedClaimDecisionApplicationReceiptV1` |
| `claim-state-transition-receipt` | `AuthorizedClaimStateTransitionReceiptV1` |
| `terminal-claim-set` | `AuthorizedTerminalClaimSetEvidenceV1` |
| `exposure-release-receipt` | `AuthorizedExposureReleaseReceiptV1` |
| `coverage-resolution` | `AuthorizedCoverageResolutionV1` |

The exact media type and complete-envelope domain are the entries in sections
1 and 9. `object_size_bytes` is the length of the complete canonical object and
must be no more than the profile's 1 MiB complete-object ceiling. Inline
carriage is valid only when `canonical_object_bytes` is a CBOR byte string,
`object_descriptor` is absent, the canonical object is no larger than 96 KiB,
the complete event content is no larger than Messenger's 128 KiB event-content
ceiling, and the complete encoded `CommerceProfileEventV1` including all
metadata and outer Agent Packet remains within the existing 1 MiB encrypted
packet ceiling. The 96 KiB rule reserves deterministic space for the event and
signed-envelope wrappers; it is a protocol limit, not an implementation hint.
There is no assumption that a 1 MiB object can fit inline: the encoder computes
the actual wrapper size before sending.

Content-addressed carriage is required when the object or either wrapper would
exceed an inline limit and may be selected for any object. In that mode `canonical_object_bytes`
is absent and `object_descriptor` is present; its content type, digest, and size
must equal the event fields exactly. The event and outer packet remain within
1 MiB. Retrieval hints are non-authoritative and the receiver obtains the exact
bytes only through an owner-approved `ContentResolver` under the complete
`ContentRetrievalPolicyV1` in the generic Intent profile. It applies origin,
SSRF, DNS, redirect, TLS, proxy, credential, fan-out, time, compressed-byte, and
expanded-byte limits before accepting bytes. Admission waits until the entire
object has been durably retrieved, bounded-decoded, canonically re-encoded,
rehash-verified, and retained for recovery; a descriptor, locator, partial byte
range, or successful fetch alone is never commercial authority.

For either carriage kind, Messenger checks `object_content_type`, recomputes
`object_digest` under the registered domain, and requires the measured length
to equal `object_size_bytes` before dispatch. Both or neither carriage fields,
an unknown carriage kind, unknown profile version or object kind, content-type
or domain substitution, noncanonical bytes, size mismatch, wrapper overflow,
or an oversized object is rejected before it reaches a profile verifier or
model.

Messenger verifies envelope bounds, canonical bytes, sender authentication,
recipient, object digest, replay identity, retention, and delivery resolution.
It does not interpret coverage or decide claims. OpenFox routes the event to a
dedicated `commerce-profile-events` inbox and invokes the installed profile
verifier. Unverified objects never enter ordinary chat, autonomous model
context, Agreement state, or an economic effect sink.

Firm offers, acceptance requests and receipts, claims, decisions, and coverage
transition notices use this same envelope. `messenger.send` remains the
transport side-effect identity; each embedded commercial action retains its
own profile identity and request digest.

## 23. Service and Adapter interfaces

The protocol package releases two static registries with different jobs. The
object registry dispatches pure, side-effect-free canonical verification. The
mutation registry dispatches a canonical action request to its state
transition and one or more result components. Combining these jobs under an
action-kind key is invalid: many portable objects are not mutations, while one
mutation may produce several independently verified results.

```text
GuarantorObjectVerifierRegistryV1 {
  schema_version                      # exactly 1
  registry_version                    # exactly 1
  entries[]                          # exact complete object-kind set
}

GuarantorObjectVerifierEntryV1 {
  object_kind
  object_content_type?
  schema_version
  canonical_type
  canonical_digest_binding           # direct domain or exact containing-object path
  complete_envelope_domain?
  verifier_profile_id
}

GuarantorMutationVerifierRegistryV1 {
  schema_version                      # exactly 1
  registry_version                    # exactly 1
  entries[]                          # exact complete mutation dispatch-key set
}

GuarantorMutationResultComponentV1 {
  role
  canonical_type
  digest_or_envelope_domain
  cardinality                       # exactly_one, optional_one, or profile_selected
  presence_rule                     # exactly accepted_effect_v1
}

GuarantorMutationVerifierEntryV1 {
  operation_id
  action_kind
  operation_purpose
  request_schema_version
  request_type
  request_body_profile_id
  result_components[]
  required_context_types[]
  semantic_field_derivation_profile_id
  transition_validator_profile_id
  materializer_profile_id
}
```

Object entries sort by `object_kind`. Mutation entries sort by
`(action_kind, operation_purpose, request_schema_version)`. Both registries
reject duplicate keys, duplicate operation IDs, unknown fields, and conflicting
metadata. Their digests are respectively
`Digest("tos.service.agent-guarantor-object-verifier-registry.v1", registry)`
and
`Digest("tos.service.agent-guarantor-mutation-verifier-registry.v1", registry)`.
The V1 schema release pins both exact digests and complete key sets.

Every `*_profile_id` is a released semantic verifier identifier whose behavior
is fixed by schemas and vectors. It is not executable code, a locator, or an
implementation binary hash. Implementations MAY attest their binaries in
deployment metadata, but those attestations are noncanonical and cannot change
an object digest, dispatch key, or verification result.

Every mutation uses the one generic exact-request formula from Semantic Action
Identity V1:

```text
exact_request_digest = "sha256:" || lower_hex(SHA-256(
  "tos.action-request.v1\0" ||
  uint32_big_endian(len(canonical_action_request_body)) ||
  canonical_action_request_body))
```

No Guarantor registry entry selects, prefixes, or replaces that digest domain.
The semantic stable-action identity and exact-request digest remain distinct:
the former identifies one semantic effect; the latter conflicts a retry that
changes any canonical request byte.

### 23.1 Exhaustive V1 object-verifier table

The following is the complete V1 pure-object set. “Embedded” means the type has
no independent object identity and is verified at the stated exact field path
inside its containing canonical object. The schema release expands every
abbreviated domain to the exact domain in sections 9, 10, 14--20, or the named
generic Agreement/Action specification. An unlisted object kind is not a
Guarantor V1 object.

| Object kind | Canonical type | Canonical digest or envelope binding | Verifier profile ID |
| --- | --- | --- | --- |
| `service-profile-revision-artifact` | `GuarantorServiceProfileRevisionArtifactV1` | embedded in `GuarantorServiceProfileArtifactV1.revisions[]` | `tos.service.agent-guarantor.verify.service-profile-revision.v1` |
| `service-profile-artifact` | `GuarantorServiceProfileArtifactV1` | `tos.service.agent-guarantor-service-profile-artifact.v1` | `tos.service.agent-guarantor.verify.service-profile-artifact.v1` |
| `service-profile` | `GuarantorServiceProfileV1` | `tos.service.agent-guarantor-service-profile.v1` | `tos.service.agent-guarantor.verify.service-profile.v1` |
| `collateral-profile` | `GuarantorCollateralProfileV1` | `tos.service.agent-guarantor-collateral-profile.v1` | `tos.service.agent-guarantor.verify.collateral-profile.v1` |
| `collateral-transition-profile` | `CollateralTransitionProfileV1` | `tos.service.agent-guarantor-collateral-transition-profile.v1` | `tos.service.agent-guarantor.verify.collateral-transition-profile.v1` |
| `claim-profile` | `GuarantorClaimProfileV1` | `tos.service.agent-guarantor-claim-profile.v1` | `tos.service.agent-guarantor.verify.claim-profile.v1` |
| `claim-closure-capacity` | `ClaimClosureCapacityV1` | embedded in requested and accepted coverage terms | `tos.service.agent-guarantor.verify.claim-closure-capacity.v1` |
| `stage-action-admission-body` | `PortableStageActionAdmissionBodyV1` | `tos.service.agent-guarantor-stage-action-admission.v1`; embedded in its evidence envelope | `tos.service.agent-guarantor.verify.stage-action-admission-body.v1` |
| `stage-action-admission-evidence` | `PortableStageActionAdmissionEvidenceV1` | `tos.service.agent-guarantor-stage-action-admission-evidence.v1`; embedded exactly once in each stage result at every assurance level | `tos.service.agent-guarantor.verify.stage-action-admission-evidence.v1` |
| `payout-execution-evidence` | `AuthorizedGuarantorPayoutExecutionEvidenceV1` | `tos.service.agent-guarantor-payout-execution-evidence.v1` | `tos.service.agent-guarantor.verify.payout-execution-evidence.v1` |
| `payout-destination` | `PayoutDestinationV1` | `tos.service.agent-guarantor-payout-destination.v1` | `tos.service.agent-guarantor.verify.payout-destination.v1` |
| `coverage-end-commitment` | `CoverageEndCommitmentV1` | `tos.service.agent-guarantor-coverage-end-commitment.v1` | `tos.service.agent-guarantor.verify.coverage-end-commitment.v1` |
| `stage-operation-binding` | `GuarantorStageOperationBindingV1` | `tos.service.agent-guarantor-stage-operation-binding.v1` | `tos.service.agent-guarantor.verify.stage-operation-binding.v1` |
| `collateral-control-disclosure` | `CollateralControlDisclosureV1` | `tos.service.agent-guarantor-collateral-control-disclosure.v1` | `tos.service.agent-guarantor.verify.collateral-control-disclosure.v1` |
| `collateral-control-evidence` | `AuthorizedCollateralControlEvidenceV1` | `tos.service.agent-guarantor-collateral-control-evidence-envelope.v1` | `tos.service.agent-guarantor.verify.collateral-control-evidence.v1` |
| `operational-independence-terms` | `GuarantorOperationalIndependenceTermsV1` | `tos.service.agent-guarantor-operational-independence-terms.v1` | `tos.service.agent-guarantor.verify.operational-independence-terms.v1` |
| `operational-independence-evidence` | `AuthorizedGuarantorOperationalIndependenceEvidenceV1` | `tos.service.agent-guarantor-operational-independence-evidence-envelope.v1` | `tos.service.agent-guarantor.verify.operational-independence-evidence.v1` |
| `requested-coverage-terms` | `RequestedCoverageTermsV1` | `tos.service.agent-guarantor-requested-coverage-terms.v1` | `tos.service.agent-guarantor.verify.requested-coverage-terms.v1` |
| `quote-request` | `AuthorizedCoverageQuoteRequestV1` | `tos.service.agent-guarantor-quote-request-envelope.v1` | `tos.service.agent-guarantor.verify.quote-request.v1` |
| `coverage-terms` | `GuarantorCoverageTermsV1` | `tos.service.agent-guarantor-coverage-terms.v1` | `tos.service.agent-guarantor.verify.coverage-terms.v1` |
| `cancellation-policy` | `CoverageCancellationPolicyV1` | `tos.service.agent-guarantor-cancellation-policy.v1` | `tos.service.agent-guarantor.verify.cancellation-policy.v1` |
| `coverage-agreement` | `AgentAgreementBodyV1` plus profile-qualified evidence | released generic Agreement domains | `tos.service.agent-guarantor.verify.coverage-agreement.v1` |
| `agreement-authorization-set` | `GuarantorAgreementAuthorizationEvidenceSetV1` | `tos.service.agent-guarantor-agreement-authorization-evidence-set.v1` | `tos.service.agent-guarantor.verify.agreement-authorization-set.v1` |
| `authority-admission-proof` | `AuthorityAdmissionEligibilityProofV1` | `tos.service.agent-guarantor-authority-admission-eligibility-proof.v1` | `tos.service.agent-guarantor.verify.authority-admission-proof.v1` |
| `authority-admission-proof-set` | `AuthorityAdmissionEligibilityProofSetV1` | `tos.service.agent-guarantor-authority-admission-eligibility-proof-set.v1` | `tos.service.agent-guarantor.verify.authority-admission-proof-set.v1` |
| `firm-offer-agreement-evidence` | `GuarantorFirmOfferAgreementEvidenceV1` | `tos.service.agent-guarantor-firm-offer-agreement-evidence.v1` | `tos.service.agent-guarantor.verify.firm-offer-agreement-evidence.v1` |
| `guarantor-evidence-set` | `CanonicalGuarantorEvidenceSetV1` | `tos.service.agent-guarantor-evidence-set.v1` | `tos.service.agent-guarantor.verify.evidence-set.v1` |
| `exposure-admission-descriptor` | `ProviderExposureAdmissionDescriptorV1` | `tos.service.agent-guarantor-exposure-admission.v1` | `tos.service.agent-guarantor.verify.exposure-admission-descriptor.v1` |
| `firm-offer-recipient-set` | `FirmOfferRecipientSetV1` | `tos.service.agent-guarantor-firm-offer-recipient-set.v1` | `tos.service.agent-guarantor.verify.firm-offer-recipient-set.v1` |
| `exposure-reservation-scope` | `ProviderExposureReservationScopeV1` | `tos.service.agent-guarantor-reservation-scope.v1` | `tos.service.agent-guarantor.verify.exposure-reservation-scope.v1` |
| `firm-offer-authority-instance-effect` | `FirmOfferAuthorityInstanceEffectV1` | embedded in `FirmOfferIssuanceActionBodyV1` | `tos.service.agent-guarantor.verify.firm-offer-authority-effect.v1` |
| `exposure-admission-receipt` | `AuthorizedProviderExposureAdmissionReceiptV1` | `tos.service.agent-guarantor-exposure-receipt-envelope.v1` | `tos.service.agent-guarantor.verify.exposure-admission-receipt.v1` |
| `firm-offer` | `AuthorizedFirmCoverageOfferV1` | `tos.service.agent-guarantor-firm-offer-envelope.v1` | `tos.service.agent-guarantor.verify.firm-offer.v1` |
| `offer-non-acceptance` | `AuthorizedOfferNonAcceptanceEvidenceV1` | `tos.service.agent-guarantor-offer-non-acceptance-envelope.v1` | `tos.service.agent-guarantor.verify.offer-non-acceptance.v1` |
| `pre-acceptance-exposure-release` | `AuthorizedPreAcceptanceExposureReleaseReceiptV1` | `tos.service.agent-guarantor-pre-acceptance-release-receipt-envelope.v1` | `tos.service.agent-guarantor.verify.pre-acceptance-release.v1` |
| `acceptance-request` | `AuthorizedCoverageAcceptanceRequestV1` | `tos.service.agent-guarantor-acceptance-request-envelope.v1` | `tos.service.agent-guarantor.verify.acceptance-request.v1` |
| `acceptance-receipt` | `AuthorizedCoverageAcceptanceReceiptV1` | `tos.service.agent-guarantor-acceptance-receipt-envelope.v1` | `tos.service.agent-guarantor.verify.acceptance-receipt.v1` |
| `activation-admission-cut` | `ActivationAdmissionCutProofV1` | `tos.service.agent-guarantor-activation-cut-proof.v1` | `tos.service.agent-guarantor.verify.activation-admission-cut.v1` |
| `activation-evidence` | `AuthorizedCoverageActivationEvidenceV1` | `tos.service.agent-guarantor-activation-evidence-envelope.v1` | `tos.service.agent-guarantor.verify.activation-evidence.v1` |
| `non-activation-evidence` | `AuthorizedCoverageNonActivationEvidenceV1` | `tos.service.agent-guarantor-non-activation-evidence-envelope.v1` | `tos.service.agent-guarantor.verify.non-activation-evidence.v1` |
| `non-activation-exposure-release` | `AuthorizedNonActivationExposureReleaseReceiptV1` | `tos.service.agent-guarantor-non-activation-exposure-release-envelope.v1` | `tos.service.agent-guarantor.verify.non-activation-exposure-release.v1` |
| `cancellation-request` | `AuthorizedCoverageCancellationRequestV1` | `tos.service.agent-guarantor-cancellation-request-envelope.v1` | `tos.service.agent-guarantor.verify.cancellation-request.v1` |
| `cancellation-receipt` | `AuthorizedCoverageCancellationReceiptV1` | `tos.service.agent-guarantor-cancellation-receipt-envelope.v1` | `tos.service.agent-guarantor.verify.cancellation-receipt.v1` |
| `collateral-terms` | `CollateralTermsV1` | embedded in the accepted coverage Agreement | `tos.service.agent-guarantor.verify.collateral-terms.v1` |
| `collateral-position-state` | `CollateralPositionStateV1` | `tos.service.agent-guarantor-collateral-position-state.v1` | `tos.service.agent-guarantor.verify.collateral-position-state.v1` |
| `collateral-adapter-request` | `CollateralAdapterRequestV1` | `tos.service.agent-guarantor-collateral-adapter-request.v1` | `tos.service.agent-guarantor.verify.collateral-adapter-request.v1` |
| `collateral-adapter-evidence` | `CollateralAdapterEvidenceV1` | `tos.service.agent-guarantor-collateral-adapter-evidence.v1` | `tos.service.agent-guarantor.verify.collateral-adapter-evidence.v1` |
| `collateral-evidence` | `AuthorizedCollateralEvidenceV1` | `tos.service.agent-guarantor-collateral-evidence-envelope.v1` | `tos.service.agent-guarantor.verify.collateral-evidence.v1` |
| `collateral-payout-payment-evidence-projection` | `CollateralPayoutPaymentEvidenceProjectionV1` | `tos.service.agent-guarantor-collateral-payout-payment-evidence.v1` | `tos.service.agent-guarantor.verify.collateral-payout-payment-evidence.v1` |
| `triggered-obligation-set` | `TriggeredObligationSetV1` | `tos.service.agent-guarantor-triggered-obligation-set.v1` | `tos.service.agent-guarantor.verify.triggered-obligation-set.v1` |
| `claim-evidence-manifest` | `ClaimEvidenceManifestV1` | `tos.service.agent-guarantor-claim-evidence-manifest.v1` | `tos.service.agent-guarantor.verify.claim-evidence-manifest.v1` |
| `other-recovery-declaration` | `OtherRecoveryDeclarationV1` | `tos.service.agent-guarantor-other-recovery-declaration.v1` | `tos.service.agent-guarantor.verify.other-recovery-declaration.v1` |
| `claim` | `AuthorizedCoverageClaimV1` | `tos.service.agent-guarantor-claim-envelope.v1` | `tos.service.agent-guarantor.verify.claim.v1` |
| `claim-ingress-receipt` | `AuthorizedClaimSubmissionIngressReceiptV1` | `tos.service.agent-guarantor-claim-ingress-receipt-envelope.v1` | `tos.service.agent-guarantor.verify.claim-ingress-receipt.v1` |
| `claim-ingress-cut` | `ClaimIngressAdmissionCutProofV1` | `tos.service.agent-guarantor-claim-ingress-cut-proof.v1` | `tos.service.agent-guarantor.verify.claim-ingress-cut.v1` |
| `claim-submission-authority-instance-effect` | `ClaimSubmissionAuthorityInstanceEffectV1` | `tos.service.agent-guarantor-claim-submission-authority-instance-effect.v1` | `tos.service.agent-guarantor.verify.claim-submission-authority-effect.v1` |
| `claim-admission-receipt` | `AuthorizedClaimAdmissionReceiptV1` | `tos.service.agent-guarantor-claim-admission-envelope.v1` | `tos.service.agent-guarantor.verify.claim-admission-receipt.v1` |
| `claim-admission-receipt-seal` | `ClaimAdmissionReceiptSealBodyV1` plus authorization | `tos.service.agent-guarantor-claim-admission-receipt-seal.v1` | `tos.service.agent-guarantor.verify.claim-admission-receipt-seal.v1` |
| `claim-admission-receipt-proof` | `ClaimAdmissionReceiptProofV1` | `tos.service.agent-guarantor-claim-admission-receipt-proof.v1` | `tos.service.agent-guarantor.verify.claim-admission-receipt-proof.v1` |
| `claim-filing-close-receipt` | `AuthorizedClaimFilingCloseReceiptV1` | `tos.service.agent-guarantor-claim-filing-close-envelope.v1` | `tos.service.agent-guarantor.verify.claim-filing-close-receipt.v1` |
| `claim-decision` | `AuthorizedClaimDecisionV1` | `tos.service.agent-guarantor-claim-decision-envelope.v1` | `tos.service.agent-guarantor.verify.claim-decision.v1` |
| `claim-revision-epoch-expectation` | `ClaimRevisionEpochExpectationV1` | `tos.service.agent-guarantor-claim-revision-epoch-expectation.v1` | `tos.service.agent-guarantor.verify.claim-revision-epoch-expectation.v1` |
| `claim-decision-admission-receipt` | `AuthorizedClaimDecisionAdmissionReceiptV1` | `tos.service.agent-guarantor-claim-decision-admission-envelope.v1` | `tos.service.agent-guarantor.verify.claim-decision-admission-receipt.v1` |
| `claim-decision-admission-receipt-seal` | `ClaimDecisionAdmissionReceiptSealBodyV1` plus authorization | `tos.service.agent-guarantor-claim-decision-admission-receipt-seal.v1` | `tos.service.agent-guarantor.verify.claim-decision-admission-receipt-seal.v1` |
| `claim-decision-admission-receipt-proof` | `ClaimDecisionAdmissionReceiptProofV1` | `tos.service.agent-guarantor-claim-decision-admission-receipt-proof.v1` | `tos.service.agent-guarantor.verify.claim-decision-admission-receipt-proof.v1` |
| `decision-application-token` | `DecisionApplicationTokenV1` | `tos.service.agent-guarantor-decision-application-token.v1` | `tos.service.agent-guarantor.verify.decision-application-token.v1` |
| `claim-decision-application-receipt` | `AuthorizedClaimDecisionApplicationReceiptV1` | `tos.service.agent-guarantor-decision-application-envelope.v1` | `tos.service.agent-guarantor.verify.claim-decision-application-receipt.v1` |
| `decision-application-receipt-seal` | `DecisionApplicationReceiptSealBodyV1` plus authorization | `tos.service.agent-guarantor-decision-application-receipt-seal.v1` | `tos.service.agent-guarantor.verify.decision-application-receipt-seal.v1` |
| `decision-application-receipt-proof` | `DecisionApplicationReceiptProofV1` | `tos.service.agent-guarantor-decision-application-receipt-proof.v1` | `tos.service.agent-guarantor.verify.decision-application-receipt-proof.v1` |
| `claim-state-transition-receipt` | `AuthorizedClaimStateTransitionReceiptV1` | `tos.service.agent-guarantor-claim-state-transition-envelope.v1` | `tos.service.agent-guarantor.verify.claim-state-transition-receipt.v1` |
| `conditional-settlement-template` | `ConditionalSettlementTemplateV1` | embedded in the accepted coverage Agreement | `tos.service.agent-guarantor.verify.conditional-settlement-template.v1` |
| `settlement-parameters` | `ProfileQualifiedSettlementParametersV1` | `tos.service.agent-guarantor-settlement-parameters.v1` | `tos.service.agent-guarantor.verify.settlement-parameters.v1` |
| `claim-payout-line` | `ClaimPayoutLineV1` | `tos.service.agent-guarantor-payout-line.v1` | `tos.service.agent-guarantor.verify.claim-payout-line.v1` |
| `materialized-payout-line` | `MaterializedPayoutLineV1` | `tos.service.agent-guarantor-materialized-payout-line.v1` | `tos.service.agent-guarantor.verify.materialized-payout-line.v1` |
| `materialized-payout-set` | `MaterializedPayoutObligationSetV1` | `tos.service.agent-guarantor-payout-obligation-set.v1` | `tos.service.agent-guarantor.verify.materialized-payout-set.v1` |
| `terminal-payout-set` | `TerminalPayoutEvidenceSetV1` | `tos.service.agent-guarantor-terminal-payout-evidence-set.v1` | `tos.service.agent-guarantor.verify.terminal-payout-set.v1` |
| `coverage-terminal-payout-set` | `CoverageTerminalPayoutEvidenceSetV1` | `tos.service.agent-guarantor-coverage-terminal-payout-evidence-set.v1` | `tos.service.agent-guarantor.verify.coverage-terminal-payout-set.v1` |
| `claim-terminal-resolution-ref-set` | `ClaimTerminalResolutionRefSetV1` | `tos.service.agent-guarantor-claim-resolution-set.v1` | `tos.service.agent-guarantor.verify.claim-resolution-ref-set.v1` |
| `coverage-closure-context` | `CoverageClosureEvidenceContextV1` | `tos.service.agent-guarantor-coverage-closure-context.v1` | `tos.service.agent-guarantor.verify.coverage-closure-context.v1` |
| `terminal-claim-set` | `AuthorizedTerminalClaimSetEvidenceV1` | `tos.service.agent-guarantor-terminal-claim-set-evidence.v1` | `tos.service.agent-guarantor.verify.terminal-claim-set.v1` |
| `exposure-disposition` | `ExposureDispositionComputationV1` | `tos.service.agent-guarantor-exposure-disposition.v1` | `tos.service.agent-guarantor.verify.exposure-disposition.v1` |
| `exposure-release-receipt` | `AuthorizedExposureReleaseReceiptV1` | `tos.service.agent-guarantor-exposure-release-receipt-envelope.v1` | `tos.service.agent-guarantor.verify.exposure-release-receipt.v1` |
| `coverage-resolution` | `AuthorizedCoverageResolutionV1` | `tos.service.agent-guarantor-resolution-envelope.v1` | `tos.service.agent-guarantor.verify.coverage-resolution.v1` |
| `transition-evidence-projection` | `TransitionEvidenceProjectionV1` | `tos.service.agent-guarantor-transition-evidence-projection.v1` | `tos.service.agent-guarantor.verify.transition-evidence-projection.v1` |
| `pre-acceptance-release-projection` | `PreAcceptanceExposureReleaseEvidenceProjectionV1` | `tos.service.agent-guarantor-pre-acceptance-release-evidence-projection.v1` | `tos.service.agent-guarantor.verify.pre-acceptance-release-projection.v1` |
| `exposure-release-projection` | `ExposureReleaseEvidenceProjectionV1` | `tos.service.agent-guarantor-exposure-release-evidence-projection.v1` | `tos.service.agent-guarantor.verify.exposure-release-projection.v1` |
| `commerce-profile-event` | `CommerceProfileEventV1` | released generic commerce-event domain | `tos.service.agent-guarantor.verify.commerce-profile-event.v1` |
| `object-verifier-registry` | `GuarantorObjectVerifierRegistryV1` | `tos.service.agent-guarantor-object-verifier-registry.v1` | `tos.service.agent-guarantor.verify.object-registry.v1` |
| `mutation-verifier-registry` | `GuarantorMutationVerifierRegistryV1` | `tos.service.agent-guarantor-mutation-verifier-registry.v1` | `tos.service.agent-guarantor.verify.mutation-registry.v1` |

The object registry is exhaustive at the public verifier boundary, but nested
supporting structs such as amount, destination, revision leaf, resolution ref,
and authority-proof entries retain their normative schemas and are recursively
verified through their listed containing object. They cannot be dispatched as
standalone authority objects unless a future profile assigns them an object
kind and direct digest binding.

### 23.2 Exhaustive V1 mutation-verifier table

Every mutation attempt resolves through exactly one generic
`ActionResolutionV1`; that universal resolution is omitted from the component
column. Every component entry sets `presence_rule = accepted_effect_v1`.
`unknown`, `prepared`, `submitted`, `rejected`, and `conflict` have zero
components. `accepted` has the listed cardinalities. A later `terminal` state
retains the exact accepted component vector. An atomic first terminal positive
state may carry that complete vector when `evidence_refs[]` commits every
verified digest in registry order; a terminal negative state has zero.
Components cannot disappear after acceptance, change across recovery, or
appear at terminal without complete positive evidence. A multi-component row
commits and persists its complete component vector in the same linearizable
accepted mutation. The table is the complete
Guarantor-specific V1
mutation set; generic publication, Messenger, Agreement, conditional-obligation,
billing, payment, and reconciliation identities remain governed by their
existing generic registries. The two `guarantor-payout` rows below are profile-
specific operation/result wrappers over the released generic payment semantic
keys; they do not add or reinterpret a payment action kind.
For every V1 row, let `P` be the immutable identifier in the final column. The
canonical registry entry encodes all five fields, all present, as:

```text
operation_id                         = P
request_body_profile_id              = P
semantic_field_derivation_profile_id = P
transition_validator_profile_id      = P
materializer_profile_id              = P
```

`request_schema_version` is exactly `1` and `required_context_types[]` is the
canonical empty array for every V1 row. All portable context is embedded in the
registered request; mutable CAS state is resolved by the sink and is not caller
context. This deliberate single composite operation profile prevents a stage
binding from naming one operation while dispatching another verifier or
materializer. A future separation or nonempty external context set requires a
new registry version and new exact vectors.

| Action kind / purpose | Canonical request type | Guarantor result components | Exact operation/profile ID (all five fields) |
| --- | --- | --- | --- |
| `commercial.quote.issue` / `firm-offer-issuance` | `FirmOfferIssuanceActionBodyV1` | `exposure_receipt: AuthorizedProviderExposureAdmissionReceiptV1 @ tos.service.agent-guarantor-exposure-receipt-envelope.v1` exactly one; `firm_offer: AuthorizedFirmCoverageOfferV1 @ tos.service.agent-guarantor-firm-offer-envelope.v1` exactly one | `tos.service.agent-guarantor.mutate.firm-offer-issuance.v1` |
| `commercial.quote.close` / `offer-non-acceptance` | `OfferNonAcceptanceResolutionActionBodyV1` | `non_acceptance: AuthorizedOfferNonAcceptanceEvidenceV1 @ tos.service.agent-guarantor-offer-non-acceptance-envelope.v1` exactly one | `tos.service.agent-guarantor.mutate.offer-non-acceptance.v1` |
| `portfolio.release` / `pre-acceptance` | `PreAcceptanceExposureReleaseActionBodyV1` | `release_receipt: AuthorizedPreAcceptanceExposureReleaseReceiptV1 @ tos.service.agent-guarantor-pre-acceptance-release-receipt-envelope.v1` exactly one | `tos.service.agent-guarantor.mutate.pre-acceptance-release.v1` |
| `conditional.obligation.transition` / `coverage-acceptance` | `CoverageAcceptanceAdmissionActionBodyV1` | `acceptance_receipt: AuthorizedCoverageAcceptanceReceiptV1 @ tos.service.agent-guarantor-acceptance-receipt-envelope.v1` exactly one | `tos.service.agent-guarantor.mutate.coverage-acceptance.v1` |
| `conditional.obligation.transition` / `coverage-activation` | `CoverageActivationActionBodyV1` | `activation_evidence: AuthorizedCoverageActivationEvidenceV1 @ tos.service.agent-guarantor-activation-evidence-envelope.v1` exactly one | `tos.service.agent-guarantor.mutate.coverage-activation.v1` |
| `conditional.obligation.transition` / `coverage-non-activation` | `CoverageNonActivationActionBodyV1` | `non_activation_evidence: AuthorizedCoverageNonActivationEvidenceV1 @ tos.service.agent-guarantor-non-activation-evidence-envelope.v1` exactly one | `tos.service.agent-guarantor.mutate.coverage-non-activation.v1` |
| `conditional.obligation.transition` / `coverage-cancellation` | `CoverageCancellationActionBodyV1` | `cancellation_receipt: AuthorizedCoverageCancellationReceiptV1 @ tos.service.agent-guarantor-cancellation-receipt-envelope.v1` exactly one | `tos.service.agent-guarantor.mutate.coverage-cancellation.v1` |
| `conditional.claim.ingress` / `claim-submission-ingress` | `ClaimSubmissionIngressActionBodyV1` | `claim_ingress_receipt: AuthorizedClaimSubmissionIngressReceiptV1 @ tos.service.agent-guarantor-claim-ingress-receipt-envelope.v1` exactly one | `tos.service.agent-guarantor.mutate.claim-submission-ingress.v1` |
| `conditional.claim.submit` / `claim-admission` | `ClaimSubmissionActionBodyV1` | `claim_admission_receipt: AuthorizedClaimAdmissionReceiptV1 @ tos.service.agent-guarantor-claim-admission-envelope.v1` exactly one | `tos.service.agent-guarantor.mutate.claim-admission.v1` |
| `conditional.claim-filing.close` / `claim-filing-close` | `ClaimFilingCloseActionBodyV1` | `filing_close_receipt: AuthorizedClaimFilingCloseReceiptV1 @ tos.service.agent-guarantor-claim-filing-close-envelope.v1` exactly one | `tos.service.agent-guarantor.mutate.claim-filing-close.v1` |
| `conditional.claim-decision.admit` / `claim-decision-admission` | `ClaimDecisionAdmissionActionBodyV1` | `decision_admission_receipt: AuthorizedClaimDecisionAdmissionReceiptV1 @ tos.service.agent-guarantor-claim-decision-admission-envelope.v1` exactly one | `tos.service.agent-guarantor.mutate.claim-decision-admission.v1` |
| `conditional.claim.decide` / `claim-decision-application` | `ClaimDecisionApplicationActionBodyV1` | `materialized_payout_set: MaterializedPayoutObligationSetV1 @ tos.service.agent-guarantor-payout-obligation-set.v1` exactly one; `application_receipt: AuthorizedClaimDecisionApplicationReceiptV1 @ tos.service.agent-guarantor-decision-application-envelope.v1` exactly one | `tos.service.agent-guarantor.mutate.claim-decision-application.v1` |
| `conditional.claim.transition` / `claim-state-transition` | `ClaimStateTransitionActionBodyV1` | `state_transition_receipt: AuthorizedClaimStateTransitionReceiptV1 @ tos.service.agent-guarantor-claim-state-transition-envelope.v1` exactly one | `tos.service.agent-guarantor.mutate.claim-state-transition.v1` |
| `collateral.transition` / `collateral-transition` | `CollateralTransitionActionBodyV1`; standalone form forbids `payout` | `collateral_evidence: AuthorizedCollateralEvidenceV1 @ tos.service.agent-guarantor-collateral-evidence-envelope.v1` exactly one | `tos.service.agent-guarantor.mutate.collateral-transition.v1` |
| `payment.direct` / `guarantor-payout` | `GuarantorAgreementPaymentActionBodyV1`; request variant is V1 | `payout_execution_evidence: AuthorizedGuarantorPayoutExecutionEvidenceV1 @ tos.service.agent-guarantor-payout-execution-evidence.v1` exactly one | `tos.service.agent-guarantor.mutate.direct-payout.v1` |
| `payment.domain-bound` / `guarantor-payout` | `GuarantorAgreementPaymentActionBodyV1`; request variant is V3 | `payout_execution_evidence: AuthorizedGuarantorPayoutExecutionEvidenceV1 @ tos.service.agent-guarantor-payout-execution-evidence.v1` exactly one | `tos.service.agent-guarantor.mutate.domain-bound-payout.v1` |
| `settlement.external` / `guarantor-payout` | `GuarantorAgreementPaymentActionBodyV1`; request variant is V2 | `payout_execution_evidence: AuthorizedGuarantorPayoutExecutionEvidenceV1 @ tos.service.agent-guarantor-payout-execution-evidence.v1` exactly one | `tos.service.agent-guarantor.mutate.external-payout.v1` |
| `settlement.external` / `collateral-backed-payout` | `CollateralBackedAgreementPaymentActionBodyV1`; nested transition is exactly `payout` | `payout_execution_evidence: AuthorizedGuarantorPayoutExecutionEvidenceV1 @ tos.service.agent-guarantor-payout-execution-evidence.v1` exactly one | `tos.service.agent-guarantor.mutate.collateral-backed-payout.v1` |
| `conditional.obligation.transition` / `coverage-closure` | `CoverageClosureActionBodyV1` | `terminal_claim_set: AuthorizedTerminalClaimSetEvidenceV1 @ tos.service.agent-guarantor-terminal-claim-set-evidence.v1` exactly one | `tos.service.agent-guarantor.mutate.coverage-closure.v1` |
| `portfolio.release` / `post-acceptance` | `ExposureReleaseActionBodyV1` | `release_receipt: AuthorizedExposureReleaseReceiptV1 @ tos.service.agent-guarantor-exposure-release-receipt-envelope.v1` exactly one | `tos.service.agent-guarantor.mutate.post-acceptance-release.v1` |
| `conditional.obligation.transition` / `coverage-resolution` | `CoverageResolutionActionBodyV1` | `coverage_resolution: AuthorizedCoverageResolutionV1 @ tos.service.agent-guarantor-resolution-envelope.v1` exactly one | `tos.service.agent-guarantor.mutate.coverage-resolution.v1` |

Within each component cell, `role: canonical_type @ digest_or_envelope_domain`
populates the three named registry fields, and the following phrase populates
`cardinality`; `presence_rule` is always the exact token
`accepted_effect_v1`. The one dynamic domain token
`agreement.selected-payout-adapter.terminal-evidence-profile` is encoded
literally in the registry and resolves to the full Agreement-selected
settlement-evidence `ProfileRefV1`, never a URI or caller value. Components are
encoded in their left-to-right table order; this is security-relevant for every
multi-component row. Each released mutation entry
also contains the mandatory composite materializer fixed above. A missing,
reordered, or additional component, different wrapper domain,
unknown purpose/version, or implementation-local dispatch fails closed. The
two registry digests therefore commit both the pure object surface and every
normative state-changing route.

The corresponding pure API surface includes at least:

```text
VerifyGuarantorObjectVerifierRegistry(...)
VerifyGuarantorMutationVerifierRegistry(...)
VerifyServiceProfileRevisionArtifact(...)
VerifyServiceProfileArtifact(...)
VerifyServiceProfile(...)
VerifyRequestedCoverageTerms(...)
VerifyQuoteRequest(...)
VerifyCoverageTerms(...)
VerifyCoverageEndCommitment(...)
ComputeClaimDecisionSourceHead(...)
VerifyClaimDecisionSourceHead(...)
VerifyGuarantorStageOperationBinding(...)
ComputeClaimClosureCapacity(...)
VerifyClaimClosureCapacity(...)
VerifyCoverageAgreement(...)
VerifyAgreementAuthorizationEvidenceSet(...)
VerifyAuthorityAdmissionEligibilityProofSet(...)
VerifyFirmCoverageOffer(...)
VerifyFirmOfferAgreementEvidence(...)
VerifyFirmOfferAuthorityInstanceEffect(...)
ResolveAcceptanceFirmOfferV1(...)
ResolveNonAcceptanceExposureSourceV1(...)
ResolveFilingCloseCoverageAgreementV1(...)
VerifyCanonicalGuarantorEvidenceSet(...)
VerifyExposureAdmissionDescriptor(...)
VerifyExposureAdmissionReceipt(...)
VerifyOfferNonAcceptanceEvidence(...)
VerifyPreAcceptanceExposureReleaseReceipt(...)
VerifyAcceptanceRequest(...)
VerifyAcceptanceReceipt(...)
VerifyActivationEvidence(...)
VerifyActivationAdmissionCutProof(...)
VerifyNonActivationEvidence(...)
VerifyCoverageCancellationPolicy(...)
VerifyCancellationRequest(...)
VerifyCancellationReceipt(...)
VerifyCollateralControlDisclosure(...)
VerifyCollateralControlEvidence(...)
VerifyCollateralTerms(...)
VerifyCollateralPositionState(...)
VerifyCollateralAdapterRequest(...)
VerifyCollateralAdapterEvidence(...)
VerifyCollateralEvidence(...)
VerifyCollateralPayoutPaymentEvidenceProjection(...)
ValidateCollateralBackedAgreementPayment(...)
VerifyOtherRecoveryDeclaration(...)
VerifyClaim(...)
VerifyClaimSubmissionIngressReceipt(...)
VerifyClaimIngressAdmissionCutProof(...)
VerifyClaimSubmissionAuthorityInstanceEffect(...)
VerifyClaimAdmissionReceipt(...)
VerifyClaimFilingCloseReceipt(...)
VerifyClaimDecision(...)
VerifyClaimRevisionEpochExpectation(...)
VerifyClaimDecisionAdmissionReceipt(...)
VerifyClaimDecisionApplicationReceipt(...)
VerifyClaimStateTransitionReceipt(...)
VerifyConditionalSettlementTemplate(...)
MaterializeClaimPayout(...)
VerifyMaterializedPayoutObligationSet(...)
VerifyTerminalPayoutEvidenceSet(...)
VerifyCoverageTerminalPayoutEvidenceSet(...)
VerifyCoverageClosureEvidenceContext(...)
VerifyClaimTerminalResolutionRefSet(...)
VerifyTerminalClaimSetEvidence(...)
VerifyExposureDispositionComputation(...)
VerifyExposureReleaseReceipt(...)
VerifyCoverageResolution(...)
ResolveCoverageAgreementFromTerminalSetV1(...)
VerifyTransitionEvidenceProjection(...)
VerifyExposureReleaseEvidenceProjection(...)
VerifyCommerceProfileEvent(...)
ValidateCoverageTransition(...)
ValidateClaimTransition(...)
ValidateCollateralTransition(...)
```

Every object and mutation entry has exact-byte request/result fixtures, per-
field mutation vectors, and an independent-verifier result. Resolver fixtures
exercise the single canonical paths and reject zero, multiple, duplicated, or
conflicting carriage; no resolver chooses the first of several candidates.

OpenFox's owner/provider authority exposes a durable boundary equivalent to:

```go
type GuarantorExposureLedger interface {
    IssueFirmOffer(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        FirmOfferIssuanceActionBody,
    ) (
        ExposureRecord,
        AuthorizedProviderExposureAdmissionReceipt,
        AuthorizedFirmCoverageOffer,
        agentcommerce.ActionResolution,
        error,
    )

    AdmitCoverageAcceptance(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        CoverageAcceptanceAdmissionActionBody,
    ) (
        CoverageRecord,
        AuthorizedCoverageAcceptanceReceipt,
        agentcommerce.ActionResolution,
        error,
    )

    ResolveOfferNonAcceptance(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        OfferNonAcceptanceResolutionActionBody,
    ) (
        AuthorizedOfferNonAcceptanceEvidence,
        agentcommerce.ActionResolution,
        error,
    )

    ReleaseUnacceptedExposure(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        PreAcceptanceExposureReleaseActionBody,
    ) (
        AuthorizedPreAcceptanceExposureReleaseReceipt,
        agentcommerce.ActionResolution,
        error,
    )

    ActivateCoverage(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        CoverageActivationActionBody,
    ) (
        CoverageRecord,
        AuthorizedCoverageActivationEvidence,
        agentcommerce.ActionResolution,
        error,
    )

    ResolveNonActivation(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        CoverageNonActivationActionBody,
    ) (
        CoverageRecord,
        AuthorizedCoverageNonActivationEvidence,
        agentcommerce.ActionResolution,
        error,
    )

    CancelCoverage(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        CoverageCancellationActionBody,
    ) (
        CoverageRecord,
        AuthorizedCoverageCancellationReceipt,
        agentcommerce.ActionResolution,
        error,
    )

    IngestClaim(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        ClaimSubmissionIngressActionBody,
    ) (
        AuthorizedClaimSubmissionIngressReceipt,
        agentcommerce.ActionResolution,
        error,
    )

    AdmitClaim(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        ClaimSubmissionActionBody,
    ) (
        ClaimRecord,
        AuthorizedClaimAdmissionReceipt,
        agentcommerce.ActionResolution,
        error,
    )

    CloseClaimFiling(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        ClaimFilingCloseActionBody,
    ) (
        CoverageRecord,
        AuthorizedClaimFilingCloseReceipt,
        agentcommerce.ActionResolution,
        error,
    )

    AdmitDecision(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        ClaimDecisionAdmissionActionBody,
    ) (
        ClaimRecord,
        AuthorizedClaimDecisionAdmissionReceipt,
        agentcommerce.ActionResolution,
        error,
    )

    ApplyDecision(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        ClaimDecisionApplicationActionBody,
    ) (
        ClaimRecord,
        MaterializedPayoutObligationSet,
        AuthorizedClaimDecisionApplicationReceipt,
        agentcommerce.ActionResolution,
        error,
    )

    TransitionClaim(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        ClaimStateTransitionActionBody,
    ) (
        ClaimRecord,
        AuthorizedClaimStateTransitionReceipt,
        agentcommerce.ActionResolution,
        error,
    )

    BeginClosure(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        CoverageClosureActionBody,
    ) (
        CoverageRecord,
        AuthorizedTerminalClaimSetEvidence,
        agentcommerce.ActionResolution,
        error,
    )

    ReleaseExposure(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        ExposureReleaseActionBody,
    ) (AuthorizedExposureReleaseReceipt, agentcommerce.ActionResolution, error)

    ResolveCoverage(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        CoverageResolutionActionBody,
    ) (
        AuthorizedCoverageResolution,
        agentcommerce.ActionResolution,
        error,
    )

    ResolveAction(
        context.Context,
        string,
        string,
    ) (
        agentcommerce.ActionResolution,
        error,
    )

    Snapshot() GuarantorPortfolioSnapshot
}

type IndependentCoverageOperationAdapter interface {
    ActivateCoverage(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        CoverageActivationActionBody,
    ) (
        CoverageRecord,
        AuthorizedCoverageActivationEvidence,
        agentcommerce.ActionResolution,
        error,
    )

    ResolveNonActivation(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        CoverageNonActivationActionBody,
    ) (
        CoverageRecord,
        AuthorizedCoverageNonActivationEvidence,
        agentcommerce.ActionResolution,
        error,
    )

    CancelCoverage(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        CoverageCancellationActionBody,
    ) (
        CoverageRecord,
        AuthorizedCoverageCancellationReceipt,
        agentcommerce.ActionResolution,
        error,
    )

    ResolveCoverage(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        CoverageResolutionActionBody,
    ) (
        AuthorizedCoverageResolution,
        agentcommerce.ActionResolution,
        error,
    )

    ResolveAction(
        context.Context,
        string,
        string,
    ) (agentcommerce.ActionResolution, error)
}

type IndependentClaimOperationAdapter interface {
    IngestClaim(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        ClaimSubmissionIngressActionBody,
    ) (AuthorizedClaimSubmissionIngressReceipt, agentcommerce.ActionResolution, error)

    AdmitClaim(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        ClaimSubmissionActionBody,
    ) (ClaimRecord, AuthorizedClaimAdmissionReceipt, agentcommerce.ActionResolution, error)

    CloseClaimFiling(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        ClaimFilingCloseActionBody,
    ) (CoverageRecord, AuthorizedClaimFilingCloseReceipt, agentcommerce.ActionResolution, error)

    AdmitDecision(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        ClaimDecisionAdmissionActionBody,
    ) (ClaimRecord, AuthorizedClaimDecisionAdmissionReceipt, agentcommerce.ActionResolution, error)

    ApplyDecision(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        ClaimDecisionApplicationActionBody,
    ) (ClaimRecord, MaterializedPayoutObligationSet,
        AuthorizedClaimDecisionApplicationReceipt, agentcommerce.ActionResolution, error)

    TransitionClaim(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        ClaimStateTransitionActionBody,
    ) (ClaimRecord, AuthorizedClaimStateTransitionReceipt,
        agentcommerce.ActionResolution, error)

    BeginClosure(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        CoverageClosureActionBody,
    ) (CoverageRecord, AuthorizedTerminalClaimSetEvidence,
        agentcommerce.ActionResolution, error)

    ResolveAction(context.Context, string, string) (agentcommerce.ActionResolution, error)
}

type IndependentExposureOperationAdapter interface {
    ReleaseExposure(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        ExposureReleaseActionBody,
    ) (AuthorizedExposureReleaseReceipt, agentcommerce.ActionResolution, error)

    ResolveAction(context.Context, string, string) (agentcommerce.ActionResolution, error)
}
```

This aggregate interface is an SDK convenience, not a hosting or authority
claim. For `independently-enforceable`, `ActivateCoverage`,
`ResolveNonActivation`, `CancelCoverage`, and `ResolveCoverage` are implemented
by the selected independent coverage-operation Adapter. `IngestClaim`,
`AdmitClaim`, `CloseClaimFiling`,
`AdmitDecision`, `TransitionClaim`, `BeginClosure`, and `ApplyDecision` are
implemented by the selected independent claim-operation Adapter.
`ReleaseExposure` is implemented by the selected independent exposure-
operation Adapter. Payout submission uses the Agreement-selected settlement
Adapter only after checking the exact `payout_execution` stage. A
collateral-backed payout uses that Adapter's composite method and never a
separate collateral call plus payment call. Their
`ResolveAction` paths are
directly reachable without the Guarantor runtime, session, credential, or
network endpoint. The Adapter uses the same canonical requests, stable IDs,
receipts, CAS domains, and control-deletion rules. For each call it derives
`owner_id` and `agent_id` from the immutable stage entry, validates an
authorization from that entry's independent Action Authority, and validates
the current fence against that entry's independent generation high-water in
the mutation's linearizable admission. The submitting Claimant or Decision
Authority is an authenticated request subject, not an implicit owner or Writer-
Fence issuer. A deployment that exposes
these methods only through OpenFox's Guarantor process cannot advertise that
assurance level.

Ordinary payout effects, collateral effects, and verification remain separate:

```go
type GuarantorPayoutEffectSink interface {
    SubmitPayment(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        GuarantorAgreementPaymentActionBody,
    ) (AuthorizedGuarantorPayoutExecutionEvidence,
        agentcommerce.ActionResolution,
        error)

    ResolveAction(
        context.Context,
        string,
        string,
    ) (agentcommerce.ActionResolution, error)
}

type CollateralEffectSink interface {
    SubmitTransition(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        CollateralTransitionActionBody,
    ) (AuthorizedCollateralEvidence, agentcommerce.ActionResolution, error)

    SubmitCollateralBackedPayment(
        context.Context,
        agentcommerce.AuthorizedAction,
        agentcommerce.WriterFence,
        CollateralBackedAgreementPaymentActionBody,
    ) (AuthorizedGuarantorPayoutExecutionEvidence,
        agentcommerce.ActionResolution,
        error)

    ResolveAction(
        context.Context,
        string,
        string,
    ) (agentcommerce.ActionResolution, error)
}

type CollateralEvidenceVerifier interface {
    VerifyCollateralEvidence(
        CollateralTerms,
        AuthorizedCollateralEvidence,
        time.Time,
    ) error


    VerifyCollateralBackedPayment(
        CollateralBackedAgreementPaymentActionBody,
        AuthorizedGuarantorPayoutExecutionEvidence,
    ) error
}
```

Every mutating sink follows durable prepare, submit, resolve, conflict, and
terminal semantics. A timeout after admission or broadcast triggers exact
resolution or byte-identical retry when the selected Adapter permits it. It
never authorizes a new semantic effect.

## 24. Optional TOS collateral Adapter

The unsecured and collateral-attested profiles require no change to TOS
consensus or contracts. If parties select independently enforceable TOS
collateral, the implementation requires an ordinary application contract such
as `ConditionalCollateralVaultV1`.

The existing task escrow and Paid Demand escrow MUST NOT be reinterpreted as a
Guarantor vault. Their roles, funding direction, claim meaning, single-release
lifecycle, and quote bindings do not support repeated claims, cumulative
partial payout, claim-versus-cancellation ordering, or residual collateral
release.

An optional vault StateInit binds at least:

- complete network domain;
- coverage Agreement digest and coverage obligation ID;
- underlying Agreement digest and covered-obligation-set digest;
- Guarantor, collateral principal, beneficiary, and accepted Decision Authority;
- asset, locked amount, per-claim cap, and aggregate cap;
- coverage, filing, review, challenge, payout, and release windows;
- activation-admission authority, cutoff, log ID, high-water, root, and
  activation status;
- claim-admission profile, authority or quorum, log ID, next admission sequence,
  admission-log root, filing status, frozen admission high-water, and each
  admitted claim's revision-log high-water and root;
- decision and evidence profile digests;
- next payout sequence, cumulative approved and paid amounts;
- Adapter code and configuration digest; and
- residual release and bounce-recovery rules.

Contract-local transitions are application messages, not new global TOS
opcodes. Collateral and claim-filing state are orthogonal:

```text
CoverageActivationStatus:
  PENDING -> ACTIVATION_PENDING -> ACTIVE | NEVER_ACTIVATED | AMBIGUOUS

CollateralStatus:
  LOCK -> LOCKED_PENDING_ACTIVATION
  LOCKED_PENDING_ACTIVATION -> ACTIVE
  LOCKED_PENDING_ACTIVATION -> RELEASE_PENDING -> RELEASED
  ACTIVE | CLAIMS_FROZEN -> PAYOUT_PENDING
    -> ACTIVE | CLAIMS_FROZEN | EXHAUSTED
  ACTIVE | CLAIMS_FROZEN -> DISPUTED
    -> ACTIVE | CLAIMS_FROZEN | PAYOUT_PENDING
  CLAIMS_FROZEN -> RELEASE_PENDING -> RELEASED

ClaimFilingStatus:
  UNINITIALIZED -> NOT_OPEN -> OPEN
  -> CLAIM_ADMISSION_PENDING -> OPEN
  -> FILING_CLOSE_PENDING
  -> FROZEN(admission_high_water, admission_log_root)

  NOT_OPEN -> FILING_CLOSE_PENDING
    -> FROZEN(0, empty_log_root, never_activated)
```

The contract mechanically verifies the accepted typed decision profile and
state order. It does not run AI or decide real-world facts. It supports replay-
safe partial payouts, monotonic sequence, cumulative caps, pending-before-send,
bounce rollback, challenge and grace windows, and residual release only after
all claim and reorg windows close.

For an `independently-enforceable` TOS tuple, finalized vault funding in the
coverage asset is at least the entire aggregate payout cap, excludes gas and
recovery reserves, and is exclusively bound to that coverage obligation. The
Agreement-selected Decision Authority can submit the exact terminal decision
and advance payout without a Guarantor signature or service. Any vault design
that instead requires the Guarantor to co-sign is only
`collateral-attested`, irrespective of its balance.

The same independence applies before payout: each permitted Claimant can submit
the canonical claim and predecessor-linked revisions directly; the accepted
non-Guarantor admission quorum can sequence them; and the bound close rule can
freeze the filing high-water after the deadline without a Guarantor message.
The same Adapter path admits the three closed V1 claim-state transitions and
the deterministic terminal-fallback decision path. A Decision Authority first
submits the authorized decision to
the separately fenced decision-admission transition, which advances the claim
and decision logs; challenge close selects that admitted receipt, and only then
may decision application materialize payout. Contract state
and getters expose the exact logs and pending actions needed by the Decision
Authority and beneficiary to recover through independent TOS nodes.

`CLAIM_ADMISSION_PENDING` verifies the Agreement-selected claimant and
claim-admission evidence, exact deterministic claim ID, and expected coverage/
vault revision. An initial claim consumes the next contiguous coverage-level
sequence and creates its revision log; a supplemental revision retains that
sequence and advances only the predecessor-bound per-claim revision root. It
then atomically commits the authorized claim digest, applicable sequence and
roots, and open-claim state. The filing-close
transition uses the same compare-and-swap domain, rejects before
`claim_filing_ends_at_unix`, and freezes the initial-claim high-water. It rejects
new claim IDs afterward, while an already admitted claim may receive the exact
bounded revisions authorized by its evidence/review window. A payout
references one admitted claim and terminal authorized decision. Release is
valid only from `ClaimFilingStatus = FROZEN`, after every sequence through the
frozen high-water has a proven final revision-log root, terminal decision and
payout state and no action is open or ambiguous. A Provider message cannot
advance the high-water, omit a claim or revision, or release against a stale
root.

`tosctl` and custody integration bind contract address, StateInit or deployed
code digest, full network domain, action and request IDs, body hash, amount,
destination, Writer Fence generation, and permanent replay tombstone. A new
strict deployment authorization is required before autonomous nonzero StateInit
is allowed; implementations must not bypass custody with an ordinary wallet.

## 25. Cross-repository implementation plan

| Repository | Required change | Explicit non-responsibility |
| --- | --- | --- |
| `tos-service-spec` | this profile and Guarantor JSON Schema; business-neutral `ConditionalSettlementTemplateV1`, dual-mode `CommerceProfileEventV1`, and `CommerceObjectDescriptorV1` additions to the generic Agent-commerce/Agreement specifications; canonical selectable-profile identities, Agreement evidence profile, fourteen-stage operation bindings, cancellation, durable claim ingress and portable claim revision, generated closure-size and continuation tables, the closed claim-transition registry, split object/mutation verifier registries with `accepted_effect_v1`, typed collateral and atomic collateral-backed-payment requests, deterministic exposure disposition, pre- and post-acceptance release schemas, semantic-action entries, exact-byte and attack/recovery vectors, independent verifier, Intent and Roadmap links | operating a Guarantor or market |
| `tos-service-protocol` | generic conditional-template, Agreement, inline/content-addressed commerce-event, payment-evidence, and Semantic Action changes in existing `pkg/agentcommerce`; Guarantor-only canonical codecs, signatures, all-level fourteen-stage operation-binding verification, profile selection and bounded lineage, generated closure-capacity/continuation arithmetic, static object/mutation verifier dispatch, ordinary direct/external payout wrappers, accepted-effect result retention, authority-control deletion tests, portable claim-admission Agreement context, claim-ingress/action/receipt verification, cancellation, portable revision receipts, collateral authority/request/state bindings, atomic collateral-payment projection, non-acceptance/release/decision verifiers, deterministic exposure disposition, closed state transitions, payout materializer, amount helpers, and fixtures in new `pkg/agentguarantor` | private risk policy, Messenger delivery ownership, or chain consensus |
| `openfox` | discovery and evaluation, Agreement compiler including the all-level stage binding, reserve-before-offer, linearized acceptance, typed cancellation, fenced unaccepted-reservation release, durable claim-ingress outbox/inbox, portable claim-admission context, multi-asset exposure ledger, coverage/claim/collateral journals, relative-to-absolute payout materializer, direct/external payout wrapping, one-action collateral-backed payment coordination, derived loss accounting, reconciliation, configuration, feature gates, and CLI | custody private keys or treating AI as authority |
| `tos-messenger` | generic `commerce.profile-event` transport with wrapper-aware inline and bounded content-addressed carriage, dedicated non-model inbox, claim-ingress request/receipt delivery and resolution, exact object resolution and autonomous economic-send mapping | coverage, claim, or payout truth |
| `tos-service-gateway` and other Carriers | no required Guarantor market API; existing signed Intent storage, search, cursor, admission, and provenance are reused | global latest, solvency, ranking authority, or claim database |
| `tos` and `tosctl` | optional application-level conditional collateral vault, atomic settlement-plus-position transition, dual payment/collateral evidence builders and getters, custody authorization, broadcast/resolve, and finalized evidence verifier | consensus change, global opcode, AI adjudication, or market discovery |
| optional Decision Authority Agents | publish ordinary service Intents and sign profile-qualified decisions | implicit court or network-wide truth |

Recommended protocol package layout:

```text
pkg/agentcommerce/
  conditional_settlement.go           # generic, not Guarantor-specific
  commerce_profile_event.go            # generic typed carriage object
  agreement_evidence.go                # generic profile-qualified integration
  semantic_action_registry.go          # additive released entries

pkg/agentguarantor/
  types.go
  canonical.go
  profile.go
  agreement.go
  quote.go
  collateral.go
  claim.go
  payout.go
  state.go
  interfaces.go
  *_test.go
  testdata/agent-guarantor-v1-vectors.json
```

OpenFox adds `EarningGuarantorSettings` and a default-off
`gates.guarantor` capability selector. Configuration binds provider/client
roles, assets, risk and correlation caps, outstanding offer and claim limits,
evidence and decision profiles, collateral and settlement Adapters, Decision
Authority allowlists, claim windows, and owner approvals.

Suggested operator commands are:

```text
openfox earning guarantor profile-check
openfox earning guarantor quote-check
openfox earning guarantor status
openfox earning guarantor claims
openfox earning guarantor reconcile --dry-run
openfox earning guarantor reconcile --apply
```

`--apply` requires local authorization, stable action identity, audit evidence,
and crash recovery. It is not a read-only synonym.

## 26. Implementation order and capability gates

### Phase 0: freeze specification

1. Release this document, the exact JSON Schema, and the generated maximum-
   canonical-size and complete continuation-state tables used by
   `ClaimClosureCapacityV1`.
2. Add the generic conditional-settlement rule and firm-offer evidence profile.
3. Release the closed claim-transition, fourteen-stage operation-binding, and
   split object/mutation verifier registries.
4. Release claim-ingress and all other semantic-action entries without changing
   existing IDs.
5. Publish positive, mutation, collision, race, and recovery vectors.
6. Require a separately implemented reference verifier.

No side-effecting Guarantor mode is enabled in Phase 0.

### Phase 1: protocol SDK

Implement `pkg/agentguarantor`, strict decode/verify functions, Agreement
binding, state transitions, conditional payout materialization, fixtures,
fuzzing, race tests, and compatibility behavior. Phase 1 exits only when the Go
implementation and independent verifier reproduce all exact bytes and failures.

### Phase 2: read-only OpenFox client

Implement multi-Carrier collection, safe detail retrieval, profile verification,
local AI analysis, deterministic economics, and operator display. Contact,
Agreement, collateral, claim, and payment remain disabled.

### Phase 3: signed unsecured coverage

Implement generic Messenger events, reserve-before-offer, firm-offer binding,
linearized acceptance, fenced pre-acceptance release, full Agreement
authorization, coverage journal, claims, decisions, direct or external payout,
and exact accounting for `unsecured-signed`.

### Phase 4: attested collateral

Add profile-qualified collateral Adapter verification, control disclosure,
exclusive allocation,
freshness and reorg handling, payout-versus-release ordering, and
`collateral-attested` readiness.

### Phase 5: optional independently enforceable TOS collateral

Implement and audit the application vault, deterministic build artifact,
custody, deployment authorization, three-node finality resolver, partial
payout, bounce recovery, residual release, and full-capacity offline execution
without a fresh Guarantor action. This phase does not change consensus and does
not block lower assurance modes.

### Phase 6: decentralized autonomous operation

Exercise independent Carriers, multiple Guarantors, an independent Decision
Authority, rollback-resistant multi-host authority stores, Provider loss,
source loss, claim and payout recovery, portfolio accounting, and bounded
learning. Readiness remains per exact tuple rather than one global production
boolean.

## 27. Authority and evidence matrix

| Fact or action | Required authority or evidence | Insufficient evidence |
| --- | --- | --- |
| service publication | signed Intent and exact profile detail | Carrier presence or rank |
| requested terms | authorized targeted quote request | ordinary chat |
| Provider commercial commitment | authorized firm offer bound to exact Agreement and valid exposure receipt | unauthorized quote or model text |
| private exposure admission | current Provider authority, Writer Fence, atomic portfolio receipt | public capacity hint |
| unaccepted exposure release | exact offer non-acceptance evidence plus fenced pre-acceptance release receipt | expiry timestamp, unsupported withdrawal message, empty inbox, or terminal claim-set placeholder |
| Agreement consent | complete body-bound profile-qualified predicates | transcript or local UI state |
| effective offer acceptance | linearized acceptance receipt or selected contract transition | signature timestamp or delayed message alone |
| active coverage | complete Agreement plus accepted fee, collateral, underlying-Agreement, and activation evidence | firm offer alone |
| current collateral | selected Adapter terminal evidence for exact position and allocation | historical balance or Provider signature |
| independently enforceable path | exclusive same-asset full-cap position plus Guarantor-control-deleted claim, close, decision, and payout quorums | partial collateral, revocable debit, shared Guarantor veto, or Guarantor-online path |
| claim submission | profile-authorized typed claim and admission receipt | email, chat, or model assertion |
| claim outcome | selected Decision Authority and evidence profile | Claimant or Carrier assertion |
| exact payout | selected settlement Adapter terminal evidence | decision, transaction hash, or acknowledgement alone |
| collateral release | terminal claim set, payout state, windows, and Adapter transition | Provider timeout or local expiry alone |
| revenue recognition | profile-qualified terminal fee or payout evidence | quote, Agreement value, or pending transfer |

## 28. Accounting, learning, and privacy

Accounting distinguishes:

- quoted fee and maximum exposure;
- reserved versus active contingent liability;
- collected, earned, refundable, and refunded premium;
- collateral claimed, verified, locked, consumed, and released;
- submitted, admitted, approved, denied, disputed, and ambiguous claims;
- approved, pending, partial, terminal, defaulted, and written-off payout;
- gross and net exposure by asset and correlation bucket; and
- internal campaign transfer from external customer revenue.

Revenue is recognized only under the exact selected Adapter evidence. A signed
offer or active coverage is not revenue. A claim decision is not a paid loss.
A Provider default is not a successful payout.

Learning consumes only de-identified, owner-approved, public-reusable facts
derived from terminal evidence. It cannot ingest private claims, customer
identities, raw Agreements, destinations, keys, credentials, or sealed policy
attachments without separate disclosure authority. Learned weights, skills,
and recommendations never expand authority, limits, profiles, or destinations.

Claim content uses authenticated bounded handoff, malware and archive checks,
no-follow immutable files, content digests, purpose limits, retention, deletion
evidence, and task-scoped model ingress. Logs contain typed error classes and
bounded digests, not raw claim evidence, complete canonical objects, private
addresses, amounts, or credentials.

## 29. Multi-Guarantor coverage and reinsurance

Several Guarantors may cover one underlying Agreement only through separate,
explicit coverage obligations or Agreements. Each binds:

- coverage layer or tranche ID;
- priority and share;
- maximum amount;
- other-coverage and coordination policy;
- independent fee, collateral, decision, payout, and release rules; and
- its own stable identities and authority evidence.

Within one Provider authority, an exact coverage-slot and layer policy prevents
accidental duplicate coverage. A decentralized network cannot prove that a
party has not obtained hidden coverage from another Provider. Indemnity terms
must therefore define disclosure, coordination, recovery, fraud, and maximum-
benefit consequences without claiming a global uniqueness oracle.

Reinsurance is a separate downstream Agreement between the primary Guarantor
and another Guarantor. The beneficiary need not depend on the downstream
Provider and retains its primary claim unless it explicitly authorizes a new
version. Circular guarantee or reinsurance dependencies fail the Portfolio DAG
admission check.

## 30. Error and recovery semantics

Implementations expose bounded typed outcomes at each side-effect sink. Only
`unknown`, `prepared`, `submitted`, `accepted`, `rejected`, `conflict`, and
`terminal` are canonical `ActionResolutionV1.state` values:

- `unknown`: no durable outcome can yet be proved;
- `prepared`: exact action durably admitted before the external effect;
- `submitted`: exact bytes may have reached the external system;
- `accepted`: the sink admitted the action but terminal evidence is pending;
- `rejected`: terminal evidence proves refusal under the selected profile;
- `conflict`: same semantic identity is presented with different exact bytes;
- `terminal`: exact positive or negative evidence satisfies the selected
  profile.

`invalid`, `not_ready`, `not_yet_eligible`, and the local projection label
`ambiguous` are API/pre-admission diagnostic classifications, not additional
`ActionResolutionV1` wire states. They are returned before action allocation or
mapped to the canonical in-progress state that the sink actually persists;
they cannot be encoded as Action Resolution states, advance a writer
high-water, create a replay tombstone, or satisfy evidence. In particular,
`not_yet_eligible` follows the non-admitting fallback rule in section 17.4, and
`ambiguous` means one of `unknown`, `prepared`, `submitted`, or `accepted` until
the same exact action is resolved.

The local diagnostics are bounded as follows: `invalid` means canonical,
signature, profile, scope, or policy validation failed before admission;
`not_ready` means a required current capability is unavailable; and
`not_yet_eligible` means the trusted time precondition has not yet been met.

Crash recovery follows:

```text
load durable action by stable ID and exact request digest
  -> if conflict, stop
  -> if rejected, return stored terminal refusal
  -> if terminal, return stored evidence
  -> if prepared/submitted/accepted/unknown, query selected sink
  -> retry only the exact original bytes when the Adapter permits
  -> never create a successor until profile-qualified terminal evidence and
     policy explicitly authorize a new semantic action
```

Provider 404, timeout, process loss, Carrier deletion, stale local cache, or a
missing dashboard record remains unknown. It cannot prove offer expiry,
claim denial, payout absence, coverage closure, or collateral release.

## 31. Conformance and adversarial tests

### 31.1 Canonical protocol vectors

The released vectors include exact canonical CBOR, digest preimages, object
digests, signature messages, signatures, semantic-action preimages, stable IDs,
and expected failure classes for:

1. signed service Intent, exact profile detail, canonical claim/collateral
   subprofile digests, and unambiguous selection;
2. embedded requested terms, their digest, the exact selected payout-Adapter
   profile, the authorized quote request, exact same-asset fee sum, and the V1
   rule that only the covered party pays premium directly to the Guarantor;
3. final Agreement body and authorization targets;
4. recoverable offer allocation, canonical recipient set and reservation scope,
   issuance request, exposure descriptor, Writer Fence, Authorized Action, and
   receipt;
5. atomic reserve-and-sign result, firm offer, and its exact generic Agreement
   evidence projection;
6. complete mixed-profile Agreement authorization and native plus non-Ed25519
   profile-qualified object authorization;
7. terminal-negative issuance with atomic private reservation unwind, plus
   expired non-acceptance evidence and its pre-acceptance
   exposure release actions and receipts;
8. acceptance request and receipt;
9. activation prerequisite carriage, self-contained activation cut and
   evidence, the accepted-but-never-activated terminal branch, and typed active-
   coverage cancellation request/action/receipt;
10. collateral authority and transition bindings, canonical Adapter request,
    position-state digests, lock, full independently executable capacity, operational-
    independence authority snapshot and deletion test, and current-state
    evidence;
11. claim manifest, canonical triggered-obligation set, embedded canonical
    other-recovery declaration, deterministic incident projection and claim
    ID, authorized claim, initial admission, and the portable per-claim
    revision envelope/root chain;
12. approving, partial, denying, evidence-required, and disputed decisions,
    admission-started challenge windows, pending application tokens, typed
    challenge and terminal-close transitions;
13. two equal-amount decision-local payout lines, their application-assigned
    materialized-line chain, and distinct obligation instances;
14. claim-bound not-applicable payout sets, payment, and external settlement
    resolution;
15. cancellation, frozen claim-admission high-water and log root, complete
    claim-resolution ref set, cycle-free closure context, terminal claim set,
    collateral disposition, sink-derived exposure disposition computation, and
    coverage resolution;
16. every new semantic-action entry and canonical mutation request body;
17. predecessor-linked coverage and claim revisions plus admitted decision
    sequences with `decision_revision = 1`;
18. native authorization-header rewrapping and quorum-identity attacks;
19. Messenger inline and content-addressed object carriage, exact wrapper-size
    accounting, and every valid and invalid kind/content-type/domain
    combination; and
20. satisfiable boundary time windows plus every impossible or overflowing
    ordering.

Mutation tests change every participant, Agreement, obligation, asset, amount,
cap, profile, predicate target, destination, time, sequence, predecessor,
network, position, action, and request field. Unknown required extensions,
duplicate keys, reordered sets, noncanonical integers, floats, overlong values,
alternate key/signature encodings, and non-shortest CBOR fail closed.

### 31.2 Authority, race, and recovery tests

Required tests include:

- reserve-before-sign and crash between reserve, signature, and send;
- crash at allocation, `RESERVED_UNSIGNED`, remote signing, signed persistence,
  and delivery, followed only by same-action recovery;
- terminal unsigned abort atomically releasing exactly one private reservation
  with zero profile components and no portable release receipt; reject an
  escaped preparatory receipt without the same action's accepted positive
  result; expiry releases exactly one issued-offer reservation; any attempted
  V1 withdrawal is rejected without state change;
  unknown-send, stale-log, pending-acceptance, and cross-path claim-evidence
  attempts retain the applicable reservation;
- issued-offer expiry requires the same complete firm-offer envelope digest in
  the non-acceptance body, release projection, and release receipt; reject an
  omitted, null, body-only, differently wrapped, or mismatched digest encoding;
- firm-offer version zero or two and any predecessor digest rejected; exact
  retry/takeover returns the same version-1 offer, while a separately authorized
  quote request produces a distinct version-1 offer and reservation;
- derive `coverage_id` only from the Guarantor and exact quote-request digest;
  reject a quote request carrying an authority-instance or coverage ID, a
  caller-selected coverage ID, or terms/Agreement bytes with a mismatched
  derived ID;
- two buyers concurrently accepting a one-use firm offer;
- acceptance and close racing on the same offer-state revision, including a
  stale expected revision, a skipped target revision, a receipt reporting a
  revision other than the admitted action, and an attempted non-acceptance
  proof after acceptance wins;
- acceptance `created_at`, receipt, acceptance, request-expiry, offer-cutoff plus
  grace, reservation-expiry, offer-expiry, and quote-request-expiry boundaries
  at equality and one second to either side; a request sequenced by `accept_by`
  but admitted after its own expiry is terminally rejected, including after
  writer takeover;
- acceptance atomically creates claim filing from `uninitialized/0` to
  `not_open/1`; activation advances that exact receipt-bound state to `open/2`,
  while non-activation preserves `not_open/1`; reject missing fields, skipped or
  replayed revisions, a pre-existing filing key, split coverage/filing commits,
  and any non-activation action that opens, freezes, or increments filing;
- late signed acceptance racing quote expiry and exposure release;
- non-activation leaves claim filing exactly `NOT_OPEN`; treating it as frozen
  or invoking closure without the distinct filing-close receipt fails, while
  the later empty-cut `NOT_OPEN -> FROZEN` action succeeds once and records its
  own close time;
- every non-activation reason against its exact Agreement rule: terminal
  prerequisite failure with correct and incorrect profile/member/subject/
  quorum/outcome combinations; expiry at one second before, exactly at, and
  after the cutoff with a complete zero-acceptance cut; and mutual cancellation
  with all role predicates, one missing role, a substituted request digest,
  expired evidence, unilateral assent, and ordinary-chat replay; reject mixed,
  empty, duplicate, extraneous, or reason-mismatched branch evidence;
- normal-expiry and accepted-cancellation closure carry the exact incident
  cutoff through end commitment, filing-close receipt, closure context, and
  terminal set; `never_activated` omits it at every path, and zero, start-time,
  maximum-u64, or another invented sentinel fails canonical verification;
- duplicate coverage and conflicting bytes for one coverage ID/version;
- replay across Agreement, underlying obligation, beneficiary, asset, profile,
  position, destination, or network;
- stale writer after takeover at quote, acceptance, decision, payout, and
  release;
- same Provider key used by two hosts against one authority high-water;
- aggregate, asset-bucket, counterparty, and correlation overexposure;
- premium obligations with an alternate payer or recipient, hidden fee,
  foreign asset, unbounded recurrence, duplicate ID, or checked-sum overflow;
- claim replay, incident replay, predecessor fork, skipped sequence, and
  evidence/profile substitution;
- evidence-manifest item count and checked content-size sum at zero, each exact
  profile boundary, and one unit over; reject duplicate or unsorted predicate
  IDs, a false `total_declared_bytes`, arithmetic overflow, compressed-size
  substitution, and any retry or transport wrapper treated as a fresh budget;
- missing, digest-only, mutable, foreign-claim, wrong-asset, duplicate-item,
  unsorted, status/amount-inconsistent, or over-limit other-recovery
  declarations; an exact empty declaration; and a predecessor-linked revision
  that changes a previously declared recovery without rewriting history;
- claim-ingress exact retry, changed-wrapper conflict, stale-fence takeover,
  absent/digest-only/duplicated ingress receipt, direct second claim carriage,
  admission without the matching receipt, receipt reuse across claim revisions,
  and fresh ingress-versus-admission authority revocation cuts;
- one initial claim with several revisions retaining one coverage-level
  sequence, plus an omitted/interchanged intermediate authorized claim,
  manifest or authorization mutation, body-only terminal claim, revision-log
  fork/gap/order failure, and post-close new-claim rejection;
- terminal-claim-set worst-case computation at exactly 1,048,576 bytes and one
  byte over; profile/request/Agreement capacity mismatch; oversized admitted
  claim; claim, decision, state-transition, and payout-line count exhaustion;
  independent recomputation of requested and final `computed_worst_case_*`
  fields, rejection of copied or stale computed values, non-identical requested
  and final fallbacks, and a final count, byte, slot, or duration bound above
  its corresponding request bound;
  refusal to consume any state-dependent continuation reserve with a
  nonterminal record; and
  proof that every maximum-size valid history still serializes and closes after
  Carrier, Provider database, process, and writer loss;
- each acceptance request/receipt, activation, non-activation, cancellation,
  filing-close, exposure-release request/receipt, and coverage-resolution
  request/envelope ceiling exactly at its accepted boundary and one byte over;
  a request or Agreement closure ceiling greater than any of the fourteen exact
  corresponding `GuarantorClaimProfileV1` closure-path ceilings; a large valid
  service-profile lineage or authorization set that fits acceptance or
  activation alone but makes filing close or a later wrapper overflow; a
  terminal-set size that fits its inner ceiling but exceeds any downstream
  residual capacity must be rejected before reservation, while the maximum
  admitted valid history must complete release and resolution;
- generated closure-size vectors at canonical-CBOR additional-information
  boundaries 23/24 and 255/256, including all three byte-identical copies of
  each `ClaimTerminalResolutionRefV1`, every nested receipt/envelope and the
  maximum authorization quorum; reject a calculator that omits or substitutes
  any one copy, counts an aggregate-array header per element, double-counts a
  header, or counts a body instead of its complete envelope;
- every reachable continuation-state/counter entry at its exact required
  decision, transition, byte, and duration reserve and one unit short; reject a
  caller-reduced entry, omitted cross-product state, challenge/nonterminal
  counter reset, last-slot nonterminal admission, and an ambiguous action that
  attempts to reclaim its reserved capacity;
- zero permitted nonterminal rounds with an attempted initial or successor
  `evidence_required`/`disputed` result; initial reviewing with no ordinary
  decision through `claim_review_cutoff` followed by exactly one recoverable
  `initial_terminal_fallback`; and a stale ordinary initial decision racing
  that fallback on the same claim-state revision;
- early and latest-possible initial claim admissions derive different
  claim-relative review cutoffs from their own admission receipts; a revision,
  retry, or takeover cannot reset the cutoff; and the initial-reviewing duration
  includes `I` exactly once in both forward and backward schedule checks; an
  ingress sequenced exactly at filing cutoff and admitted after the full ingress
  grace still receives the complete review window and fits the terminal bound;
- distinct `nonterminal_resolution_window_seconds` and
  `successor_decision_window_seconds` in both relative orders, proving that the
  generated table uses `N` and `S` independently rather than one substituted
  duration;
- latest-admission and successor cutoffs one second before, exactly at, and one
  second after each boundary, plus checked subtraction/addition underflow and
  overflow; a nonterminal response at its deadline, an early fallback, a late
  ordinary successor, or a challenge successor that returns another
  nonterminal result must fail;
- terminal fallback with missing/wrong profile, subject, quorum, predecessor,
  current transition, round counter, evidence projection, deterministic
  outcome rule, amount, payout-line projection, payout destination,
  Agreement-granted authorization mode, or action identity; missing/duplicate
  source-state or deadline mapping; normal successor versus fallback at one
  revision, ambiguous fallback retry/takeover, fresh discretionary-signature
  dependency, recursive nonterminal fallback, rejection before Agreement of
  every non-total benefit/aggregate/line function or reachable overflow,
  worker-crash recovery that derives the same output without inventing
  `deny_zero`, and a fallback whose final challenge close cannot fit the
  terminal deadline;
- every decision embeds byte-exact policy-application and typed-reason objects;
  mutate the benefit profile, projected input bytes, clause or predicate order,
  full eligible amount, reason registry token, result, or either digest; require
  accepted-benefit fallbacks to carry exact aggregate operands; require
  `deny_zero` to carry canonical zero/empty policy outputs with no aggregate
  projection and forbid that projection on ordinary decisions; exercise all
  five Agreement-fixed reason cases and reject any alternate valid reason code
  or subset for the same fallback state;
- two hosts and two valid Agreement-granted proof wrappers invoking the same
  fallback source head produce one stable ID, one exact request, and one stored
  output; crash before state read, after output construction, and after commit-
  before-response resolves that same action; changing the source head or cut
  creates the only permitted distinct slot;
- exact-byte, mutation, collision, retry, and takeover vectors for
  `ClaimDecisionSourceHeadV1` and both mode-specific identity preimages;
  reconstruct the source head from every terminal-bundle path and reject every
  forbidden optional-field combination, body-only digest, reordered field, or
  substituted decision-epoch cut;
- an ordinary approving decision that loses the last aggregate-capacity race
  resolves to generic `rejected` with zero Guarantor result components and zero
  claim, coverage, token, log, closure-slot, and closure-byte consumption;
  `ResolveAction` returns the same rejection, while the later exact fallback
  remains independently admissible and closes the claim;
- fallback `trigger_at`, `decided_at = admitted_at`, and derived expiry/latest-
  admission boundaries at equality and one second to either side, including
  checked underflow/overflow; reject caller-supplied coverage revision,
  aggregate snapshot, result, token, timestamp, output authorization, every
  `cas_rebase` enum/body, and every decision revision other than 1;
- a hostile caller invoking the byte-identical fallback one second before its
  trigger receives only non-admitting `not_yet_eligible`, leaves
  `ResolveAction = unknown`, consumes no action slot or state, and can admit the
  same request at trigger equality; races between early callers and the
  equality-time caller cannot create a tombstone or terminal rejection;
- two or more valid claims racing against the last aggregate capacity: prove
  exact zero, partial, and full remaining-cap projections; after one admission
  wins, require the other prepared fallback action to reread and recompute
  inside the same stable action/request; when the cap is exhausted, the later
  claim must admit a challengeable zero denial and reach terminal close rather
  than remain permanently open;
- requested maximum versus backward-derived final terminal deadline, including
  equality, an earlier valid final deadline, a later invalid final deadline,
  and collateral lock/reorg arithmetic unavailable at request time;
- filing close racing initial admission at the cutoff, including stale root,
  pending/ambiguous by-cutoff admission, normal/non-activation branch mixing,
  post-close new claim, permitted existing-claim revision, and exact recovery
  of the same close action and receipt;
- initial ingress one second before, at, and after filing cutoff; admission at
  the filing cutoff, at grace-end equality, and one second after grace; full
  ingress resolution grace; rejection of an ingress first sequenced during the
  grace; a prepared/ambiguous timely ingress blocking close at grace end, then
  late close after recovery to either a pre-endpoint stored admission or a
  terminal rejection; reject backdated admission and prove that late close does
  not change incident, review, or normal-case terminal deadlines; exercise
  `late_ingress_recovery_deadline_unix` one second before, exactly at, and after
  it, force every still-ambiguous ingress to its deterministic rejection at the
  hard cutoff, and prove no later admission; for a stored timely admission
  recovered only after the normal terminal target, admit exactly one
  late-recovery deterministic candidate, preserve its complete challenge,
  payout, Adapter-recovery, release, and resolution path at or before
  `late_recovery_terminal_deadline_unix`, and reject a payout one second after
  that deadline or use after an on-time close; a cut omitting,
  reordering, or substituting an ingress/admission resolution; and a cut or
  receipt at each size ceiling and one byte over;
- predecessor-linked revision ingress racing decision admission and challenge
  close in both orders, including an exact open-epoch expectation, an atomic
  authority-generated freeze time/high-water/root, stale/forked epoch
  revision, a revision that wins before the freeze CAS, a post-freeze revision
  without a reopened next epoch, a caller-supplied cutoff/proof, and terminal-
  bundle ingress high-water/root substitution; a challenged late-recovery
  candidate must reuse the same frozen epoch/cut for its sole successor, while
  any attempted reopen, new proof, or changed root fails;
- concurrent claims exceeding per-claim, claim-count, or aggregate caps;
- Agreement payout-template `first_sequence`, per-instance, aggregate, and
  checked instance-count values at their exact required equalities and one unit
  lower or higher; mismatches and multiplication overflow fail before
  authorization or reservation, while every maximum valid admitted claim still
  materializes;
- zero, one, and multiple fixed premium obligations; same-asset checked sums at
  `maximum_fee` equality and one atomic unit over; reject duplicate or omitted
  premium IDs, foreign assets, overflow, variable/recurring amounts, wrong fee
  payer or recipient, and a hidden Guarantor-controlled fee dependency under a
  different obligation kind;
- for ordinary decisions, full eligible benefit, one atomic unit below it, and
  zero derive respectively `approved`, `partially_approved`, and `denied`;
  deterministic fallback with positive gross benefit and zero remaining
  aggregate capacity derives a challengeable zero denial, as does the exact
  `deny_zero` rule; reject overlapping result tokens, a positive denial, a zero
  partial approval, an ordinary positive-benefit denial, and an ordinary
  approved decision rewritten after aggregate-cap contention;
- relative payout offsets at equality and one second outside every Agreement
  bound; delayed decision admission and delayed challenge close derive one
  absolute schedule only from the exact terminal-close receipt, and mutation of
  that receipt, close time, offset, materialized time, obligation ID, or payment
  request fails; ordinary and late-recovery decision lineages select only their
  respective hard deadline; cross-branch substitution, overflow, and a schedule
  beyond the applicable deadline fail at admission rather than strand an
  already terminal claim;
- collateral-backed payout crashes before transfer, after vault debit, after
  position update, after both result components, and before response; every
  retry resolves one `settlement.external` stable ID, one transfer, one
  position revision, and byte-identical payment plus collateral evidence;
  reject either component alone, a mismatched obligation/amount/destination,
  standalone `collateral.transition` payout, retry through `payment.direct`,
  terminal component disappearance/change, and first terminal appearance
  without the complete registry-ordered positive evidence references;
- payout and payout-default collateral requests/evidence bind the same complete
  authorized Decision envelope selected by the materialized set; reject body,
  admission-receipt, terminal-transition, foreign-wrapper, omitted, or
  mismatched digests, and reject the field on every non-payout transition;
- direct, external, and collateral-backed payout results each carry one
  sequence-matched `AuthorizedGuarantorPayoutExecutionEvidenceV1`; reject a
  generic payment proof without portable stage-action evidence, a wrapper reused
  for another obligation instance, and collateral evidence omitted from or
  added to the wrong payout form;
- checked overflow and exact partial-payment arithmetic;
- typed cancellation versus claim admission at one base revision in both
  orders, including cancellation one second before, exactly at, and one second
  after scheduled coverage end; wrong branch/profile/quorum/evidence,
  request creation before activation or after admission, checked timing
  overflow, activation-relative earliest admission and creation-relative latest
  admission at equality and one second to either side, retroactive or late
  effective interval, unknown/query/retry/takeover, an
  accrued pre-cutoff incident admitted after cancellation, a post-cutoff
  incident rejected, an initial claim whose occurrence is one second after its
  creation or admission rejected, exact equality at creation/admission accepted,
  and a pre-cancellation future-dated claim unable to survive as accrued; a
  revision that changes occurrence time or incident identity must fail; a
  fabricated scheduled-expiry action or receipt rejected,
  normal expiry derived only from the exact Agreement plus filing-close cut,
  and a closure missing or substituting the exact cancellation receipt;
- split state-domain bindings in cancellation, claim admission, filing close,
  decision admission/application, closure, or resolution rejected before
  Agreement acceptance; cancellation followed by an accrued claim, revision,
  decision, application, and filing close must preserve one byte-identical
  `CoverageEndCommitmentV1`, while clearing its evidence, lengthening its cutoff,
  restoring `active`, or changing the branch at any step fails;
- decision versus challenge and payout versus collateral release;
- authorized decision without admission, decision-admission fork/gap,
  same-sequence conflicting body, stale Writer Fence, takeover, and a challenge
  close or payout that cites a non-admitted or different decision;
- every one of the fourteen independent-stage result envelopes, including each
  payout-execution wrapper, remains verifiable after deleting the Action
  Authority, resolver, Adapter, Provider, and Guarantor stores through its exact
  embedded request, `AuthorizedActionV1`, and `WriterFenceV1`; reject a missing,
  digest-only, duplicated, mutated,
  wrong-scope, expired-at-admission, stale-generation, wrong-authority, or
  request/body-mismatched action or fence even when the business decision quorum
  is otherwise valid;
- decision application racing challenge admission or close, including missing,
  stale, nonterminal, already consumed, or cross-claim terminal-transition
  receipts and zero materialization before terminal close;
- decision authorization delivered near expiry still receiving the full
  admission-started challenge window, plus close at one second before and at
  the exact admitted cutoff;
- delayed `evidence_required` and `disputed` decisions receiving the full
  admission-started response duration, including insufficient remaining
  Agreement time, overflow, cross-result field presence, and typed timeout one
  second before and at the admitted due time;
- two claims whose decision admissions advance the shared coverage revision
  while the first waits for challenge close; each pending application token
  retains its aggregate reserve; a stale application CAS produces a durable
  `rejected` result with zero components, while changed bytes under the same ID
  produce `conflict`; the token is consumed exactly once by a terminal
  successor;
- repeated unrelated coverage-revision advances while one fallback stays
  `prepared`, then succeeds with the same stable ID/request, one decision at
  revision 1, and zero extra portable log or closure-capacity bytes;
- every decision result/amount/line/deadline matrix violation;
- accepted coverage whose activation succeeds, fails terminally, or remains
  ambiguous at the cutoff, including fee and collateral disposition;
- activation/non-activation verification after deleting the Provider database,
  including omitted/forked cut entries, wrong log root, hidden accepted action,
  and a digest-only Agreement, offer, receipt, or prerequisite object;
- single-carriage acceptance, non-acceptance release, cancellation, filing
  close, terminal closure, exposure release, and final resolution at their
  maximum valid lineage sizes, including an extra duplicate receipt, firm
  offer, cancellation receipt, terminal set, payout set, collateral set, or
  Agreement copy; a different Agreement hidden inside one nested receipt; and
  normal-expiry verification solely through the filing-close resolver;
- two concurrently authorized approving decisions with decision-local line
  indexes, applied in both possible orders: the losing CAS retries as the
  deterministic terminal successor against the new chain head, retains the
  byte-identical authorized decision, receives the next disjoint global payout
  range, and cannot strand closure or reuse a prior sequence; reject a signed
  decision that supplies a global payout sequence or predecessor;
- equal-amount payout lines retaining distinct stable identities;
- ambiguous payment followed by query-before-retry of the same action;
- collateral withdrawal, partial consumption, and reorg; plus concurrent
  allocation of one Adapter slot under two `collateral-attested` Agreements and
  two `independently-enforceable` Agreements, both of which must reject the
  second allocation even when the shared account balance covers both claims;
- collateralization at 50%, 100%, and 150%, including non-divisible atomic
  amounts that round upward, one atomic unit below the required allocation,
  zero ppm, overflow, and a profile whose advertised ratio differs from the
  Adapter default; repeat the invariant after partial finalized payout and
  after attempted release, impairment, and reorg, proving that only exact
  remaining beneficiary capacity plus finalized position-bound payment counts,
  and that adverse evidence is durably recorded while the assurance claim is
  blocked;
- Adapter evidence becoming unknown before scheduled expiry or filing close:
  claim-filing close must still freeze the exact claim cut, while payout,
  terminal-set construction where affected, collateral/exposure release, and
  final resolution remain blocked until exact current, impaired, or terminal-
  default evidence resolves the orthogonal status; it must never mutate the
  coverage-end commitment;
- terminal claim-set construction while collateral is still encumbered,
  collateral release consuming that exact set, exposure release consuming the
  resulting collateral evidence, and final resolution only afterward; reverse
  dependencies and early terminal coverage status must fail;
- terminal claim-set slot CAS from exact revision 0 to 1, closure racing a
  claim revision/decision/payout disposition, stale or skipped target revision,
  different second terminal set, an unknown caller-supplied collateral-state
  digest field, and any successor after `release_pending`;
- rejection of `independently-enforceable` for partial capacity, cost-depleted
  capacity, a Guarantor-controlled execution key, stale evidence, revocable
  debit authority, or any path requiring the Guarantor to return online;
- delete the Guarantor Agent, lifecycle/exposure authorities, and their
  transitive controller closure from every claim-ingress, admission, revision,
  evidence, dispute, challenge, close, decision, decision-application, and
  payout quorum; each required independent stage must still complete through a
  direct Adapter route, while a hidden shared controller or Guarantor-only
  claim ingress must fail;
- delete every Guarantor-controlled Action Authority, Writer-Fence issuer or
  validator, generation high-water, action resolver, and admission-state
  controller; each stage must retain its exact owner/Agent action identity,
  advance a fresh fence, reject a stale generation, and resolve an ambiguous
  action through the bound independent domain;
- after deleting the Provider exposure authority and private portfolio, invoke
  post-acceptance release through the independently bound exposure Adapter from
  absent revision zero to released revision one, resolve exact retry, and finish
  coverage resolution; reject a receipt co-signed by, routed through, or
  otherwise dependent on the deleted Provider authority, while lower-assurance
  release still requires its disclosed Provider authority;
- reject a stage binding with multiple action subjects, an action quorum,
  different action and fence subjects or keys, a contract/non-Ed25519 action
  proof, or any projection that cannot be represented byte-for-byte by the
  released scalar `AuthorizedActionV1` and `WriterFenceV1` envelopes;
- at `unsecured-signed` and `collateral-attested`, execute and recover every
  enabled stage from the Agreement-embedded binding after deleting the local
  route cache; reject an absent binding, a runtime-selected Adapter/fence/CAS
  domain, lifecycle authority substituted for exposure authority, and any
  lower-assurance result whose portable stage evidence does not match the exact
  sibling operation binding;
- delete Provider and claim-admission sink storage, then verify and admit a
  claim using only `ClaimSubmissionActionBodyV1` plus the current CAS head;
  reject a missing/substituted activation envelope, coverage Agreement,
  Agreement authorization set, cancellation receipt, end commitment, service-
  profile lineage, cap, window, covered obligation, or payout destination;
- reject any legacy eight- through thirteen-entry independent-stage set,
  missing,
  duplicate, substituted, or Guarantor-controlled `coverage_cancellation` or
  `coverage_closure` entry, or missing/substituted
  `coverage_activation`/`coverage_non_activation`,
  `post_acceptance_exposure_release`, or `coverage_resolution`; reject implicit
  reuse of another stage and any deletion test in which activation, non-
  activation, cancellation, `BeginClosure`, exposure release, or final
  resolution cannot finish directly;
- exercise the actual canonical request and Adapter call mapped to every one of
  the fourteen stage entries after Guarantor-control deletion, including separate
  claim-ingress and initial/revision admission calls, generic payout submission,
  post-acceptance exposure release and final coverage resolution; reject an
  enum-only unused entry,
  caller-selected stage, one action standing in for two required stages without
  the released composite, and a Guarantor-only exposure release or finalizer
  after independent `BeginClosure`;
- execute one `payment.direct` V1, one `payment.domain-bound` V3, one ordinary
  `settlement.external` V2, and one collateral-backed payout; each registry row
  must emit exactly one sequence-bound portable payout wrapper, while a bare
  generic payment result, wrong request variant, wrong purpose, collateral
  field on an ordinary result, or changed materialized containing set fails;
- mutate every independent operation binding's registry ProfileRef URI/version/
  digest, operation ID, each of the four handler-profile IDs, Semantic Action
  entry version, stage-derivation profile, request type/version, result role/
  domain/cardinality, maximum request bytes, required-context set, Adapter route/method, and CAS-domain
  source; test all underscore/kebab aliases, ordinal reordering, a same-URI
  different-digest registry, and omission of the payout registry ProfileRef;
  unknown or caller-selected wire tokens and a binding that disagrees with
  either verifier registry must fail before action admission;
- substitute the firm-offer envelope verifier for the distinct firm-offer
  Agreement-evidence verifier, or omit either registry entry; both fail closed;
- duplicate, missing, position-selected, unversioned, or substituted claim and
  collateral subprofile identities;
- payout-Adapter profile URI, version, descriptor digest, destination binding,
  or settlement-template substitution after quote request, including two
  profiles that share a URI but differ in version or digest;
- firm-offer allocation with a reordered, duplicated, omitted, cross-request,
  or caller-selected recipient set or reservation scope, including a scope
  whose digest is correct for its bytes but whose fields are not derivable from
  the exact request, Agreement, terms, owner policy, and portfolio buckets;
- claim identity with a permuted, duplicated, empty, out-of-coverage,
  cross-Agreement, digest-only, or alternate-wrapper triggered-obligation set,
  including two claims that retain every other field but change one triggered
  obligation;
- collateral-evidence body/envelope substitution, wrong Adapter-evidence
  domain, incomplete authorization quorum, unknown wrapper, and Messenger
  dispatch using a body or nested-proof digest instead of the complete envelope;
- Messenger inline carriage whose complete event or outer Agent Packet is at
  the 1 MiB limit and one byte over; automatic content-addressed carriage of a
  valid near-1-MiB terminal claim set; both/neither carriage fields, descriptor
  type/digest/size substitution, locator-only admission, partial retrieval,
  digest mismatch, unsafe redirect/DNS/proxy/credential origin, and recovery
  after descriptor delivery but before durable verified-object retention;
- collateral control-disclosure omission, stale evidence, relationship-token,
  Adapter/operator/controller-root, resolver, evidence-profile, authority,
  quorum, Agreement, collateral-obligation, and freshness mutation; require
  authority continuously from observation through signed validation time and
  again at admission, including revocation-at-signature followed by
  reauthorization; require
  exact `AuthorizedCollateralControlEvidenceV1` at activation if and only if
  the token is `third_party_control_asserted`, and prove that this valid
  `collateral-attested` evidence still does not satisfy the independently-
  enforceable Guarantor-control-deletion test;
- every collateral transition kind with its exact Agreement binding, plus
  Adapter, request/evidence content type, evidence profile, authorization
  source/quorum, prerequisite role, destination, result-state, and action-
  identity substitution;
- noncanonical, oversized, cross-profile, or digest-substituted collateral
  Adapter request; missing, duplicate, mixed, or substituted custodian authority
  binding; stale expected-state digest; any caller-supplied target or resulting
  state/digest in the request, action, operation parameters, or extension; and
  mismatched sink-derived successor bytes/digest across Adapter evidence,
  receipt, and durable position;
- subprofile version zero, missing or skipped predecessor, cross-provider or
  cross-authority predecessor, lineage fork, and predecessor found only in a
  Carrier copy;
- service-profile artifact at exactly 512 KiB and one byte over, 64 small
  revisions under the byte cap, earlier byte-cap rollover, and truncated,
  compressed, or locator-only lineage;
- Guarantor object- and mutation-verifier registry dispatch with a missing
  pure-object or mutation entry, unknown object/action kind, wrong operation
  purpose, wrong request schema version, duplicate key, conflicting semantic
  verifier ID, altered generic exact-request formula, body/envelope confusion,
  missing or extra multi-result component, and an implementation whose exact-
  byte result differs from the independent verifier;
- Provider failure remaining unknown or defaulted rather than falsely denied,
  paid, or released;
- key rotation, revocation, historical authority, quorum duplication, and
  operator-domain, authorization-header, validation-time, and wrapper
  substitution;
- decision-admission evidence that satisfies its profile/quorum while the
  stage action uses its distinct scalar authority, plus rejection when either
  layer is missing, substituted, Guarantor-controlled, or incorrectly compared
  byte-for-byte with the other;
- fixed-benefit versus indemnity, deductible, coinsurance, other-coverage,
  layer, and recovery substitution;
- coverage-resolution requests with normal/non-activation evidence mixed,
  omitted terminal objects, stale revision, wrong target state, wrong digest
  kind or role, set digest substituted by a wrapper or member digest, or a
  projection assembled from another coverage;
- deletion of every Carrier and Provider detail endpoint followed by recovery
  from the retained signed Intent operation, exact Intent payload, exact service
  profile, Firm Offer Agreement evidence, and lifecycle/Adapter envelopes;
- all five coverage-closure matrix branches, every invalid reason/state pair,
  timeout-as-default, approved-but-unpaid exhaustion, cancellation with an open
  accrued claim, and resolution state differing from the terminal claim set;
- closure context/action/output construction with no zero placeholder or hash
  cycle, missing claim-resolution bundle, global empty-set substitution,
  aggregate payout set supplied before terminal-set authorization, and release
  or final-state assertion before `release_pending` dependencies resolve;
- paid, partially paid then defaulted, zero-claim position-impairment, and
  ordinary close accounting, including every violation of approved = paid +
  defaulted + outstanding and every attempt to return defaulted liability to
  available underwriting capacity;
- exposure release with original reservation 100 and paid loss 60 returning
  exactly 40, paid/defaulted mixtures under each pre-bound default disposition,
  overflow/underflow, collateral-funded payment, cross-admission receipt, and
  every caller attempt to inject a disposition bucket or reclaim spent value;
- every final claim-decision result mapped to its one permitted target state,
  plus caller-selected, cross-receipt, and takeover-time target-state mismatch;
- private-evidence SSRF, DNS rebinding, redirect, proxy, credential capture,
  decompression bomb, oversized content, malware, and log/model leakage; and
- circular reinsurance and self-guarantee misrepresentation.

Every crash point is tested before and after durable admission, external send,
response persistence, terminal evidence, accounting handoff, and compaction.
Restoring an old local file must not permit a high-assurance writer, portfolio,
claim, payout, or collateral high-water rollback.

### 31.3 Decentralized source-loss campaign

A resilient public-discovery claim requires:

1. two independent Carrier implementations with independent operators, stores,
   credentials, upstreams, and failure domains;
2. publication of one exact signed Guarantor Intent through both;
3. complete deletion and shutdown of one Carrier database;
4. rediscovery and independent verification through the other;
5. reconstruction of existing coverage without either Carrier, using the
   retained signed Intent revision lineage, exact Intent payloads and service-
   profile bytes, Firm Offer Agreement evidence, and later lifecycle/Adapter
   evidence;
6. Covered Party, counterparty, Guarantor, beneficiary, and independent
   Decision Authority roles;
7. activation, at least one admitted partial claim, multiple exact payout
   lines, and residual release; and
8. complete exposure, collateral, claim, payout, accounting, and profitability
   reports with exact evidence boundaries.

When the TOS collateral Adapter is selected, the campaign repeats against at
least three independently queried TOS nodes and verifies exact vault StateInit,
funding, decision, partial payout, beneficiary credit, bounce behavior, final
state, and residual release. A local three-node run is local conformance, not
public-network decentralization.

## 32. Release and acceptance gates

The profile remains blocked for side effects until:

1. `AGENT_GUARANTOR_SERVICE_V1.md`, JSON Schema, media types, digest and
   signature domains, authorization statements, canonical mutation requests,
   generated closure-size/continuation tables, fourteen-stage operation
   bindings, claim-ingress cut rules, object/mutation verifier registries,
   bounds, and state machines are frozen;
2. the generic conditional-settlement rule and Guarantor firm-offer Agreement
   evidence profile are released;
3. the semantic-action registry and exact vectors are released without
   changing old IDs;
4. `tos-service-protocol` and a code-independent verifier agree on every
   positive and negative vector;
5. generic Messenger profile-event delivery and resolution are implemented;
6. OpenFox atomic reserve-and-sign, linearized acceptance, activation, non-
   activation and cancellation, multi-asset exposure, portable claim/revision,
   payout, deterministic loss disposition, release, and accounting journals
   pass crash and race tests;
7. every enabled assurance tuple has current concrete Adapter and authority
   dependencies; and
8. the acceptance report pins repository commits, schemas, verifier versions,
   configurations, operator and failure domains, run window, artifacts, and
   explicit exclusions.

While the Roadmap expansion gate is locked, a runtime may observe the same
ordinary signed Intents through the generic Intent profile, but it MUST NOT
advertise Guarantor V1 conformance or enable Guarantor-specific side effects.
After that gate opens and the applicable specification/codec prerequisites
above are released, read-only Guarantor discovery may enable before
side-effecting tuples. `unsecured-signed`, `collateral-attested`, and
`independently-enforceable` then enable independently; a missing higher-
assurance Adapter does not disable a valid lower tuple. Production deployment,
campaign count, or calendar age is not an enablement predicate, but none can
replace the exact current tuple's released schema, verifier, authority, and
Adapter capabilities.

## 33. Final boundary

This profile gives Agents a common language and verifier for discovering,
authorizing, operating, and resolving bounded third-party contingent payment
obligations. It lets Guarantor Agents earn fees for managed risk and lets other
Agents transact under explicitly chosen assurance.

It does not make a Carrier a market authority, make TOS Network the Guarantor,
make AI a claims judge, make a self-issued receipt proof of solvency, or make a
technical profile a legal promise beyond its selected parties and Adapters.
The authoritative path remains:

```text
exact authenticated and authorized objects
  + body-bound Agreement authorization
  + linearized owner/provider admission
  + selected claim-decision evidence
  + selected collateral and settlement terminal evidence
= the precise coverage state a verifier may claim
```
