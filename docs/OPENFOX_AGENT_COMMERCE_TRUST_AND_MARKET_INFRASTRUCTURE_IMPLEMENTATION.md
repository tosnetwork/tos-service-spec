# OpenFox Agent Commerce Trust and Market Infrastructure — Local Implementation Checkpoint

**Status:** local implementation checkpoint; non-gating

**Recorded:** 2026-09-01

**Normative effect:** none. This implementation reuses the existing Intent,
Agreement, Outcome Event, Semantic Action, Portfolio, Paid Demand Quote, and
escrow V1 boundaries. It does not release a CounterOffer object, reputation
record, multi-slot escrow, new chain state, wire profile, or ROADMAP gate.

**Controlling design:** [Post-Experiment Delta
Design](OPENFOX_AGENT_COMMERCE_TRUST_AND_MARKET_INFRASTRUCTURE_DESIGN.md)

**Design review:** [Codex Review
Report](OPENFOX_AGENT_COMMERCE_TRUST_AND_MARKET_INFRASTRUCTURE_DESIGN_REVIEW_REPORT.md)

## 1. Claim boundary

The reusable application code and deterministic local tests described below
are implemented. This record does not claim completion of the operational
parts that require independently operated hosts, real Carrier failure domains,
a released buyer-side chain-finality resolver, real model or invoice source
adapters, or actual escrow transactions.

In particular, a local Provider settlement record, a message from a
counterparty, a matching digest, or a Carrier receipt is not promoted into
stablecoin finality, delivery truth, cost truth, or economic authority. Where
the required qualified source is not installed, the implementation returns
`unknown` or defers the next funding action.

## 2. Implemented repository surfaces

| Repository | Implemented delta | Authority limit |
|---|---|---|
| `tos-service-spec` | Corrected the existing Cost Observation V1 lineage condition: a non-`contra` genesis has an empty original reference, while `contra` requires one exact canonical original reference. Expanded deterministic positive and negative vectors and the independent JSON Schema reference verifier. | No new profile or business-specific schema. |
| `tos-service-protocol` | Added a public exact-successor validator for Agreement revisions; enforced Agreement-body, predicate, and signed-acceptance validity windows during authorization; implemented the corrected Cost Observation lineage validation and fixtures. | A successor validator proves lineage only. It does not establish a global latest proposal head. |
| `openfox` | Added predecessor-bound Agreement revision construction, durable negotiation conflict handling, qualified Outcome import and local risk/economic projections, and local sequential composition admission for independent Paid Demand child escrows. | Every projection and composition object is Owner-local and non-authoritative. Existing profile verifiers remain the authority boundary. |
| `tos`, `tosctl`, `tos-messenger` | No implementation change was required for this checkpoint. | Escrow V1 and Messenger transport meanings remain unchanged. |

## 3. Work-package status

| Package | Implemented evidence | Status and remaining evidence |
|---|---|---|
| A — reconciliation and fixtures | The design/review inventory remains canonical in this repository. Cost genesis/contra schema, protocol fixtures, and executable negative mutations now agree. No duplicate Intent, Agreement, milestone, reputation, cost, or escrow object was added. | Local implementation complete for the changed surfaces; no protocol-acceptance claim. |
| B — negotiation and cost shadow mode | OpenFox builds complete consecutive Agreement bodies, recomputes authorization targets, preflights time and lineage, persists a proposal before Messenger submission, requires exact replay identity, and durably stops on a same-ID/version fork. Qualified cost import/reporting keeps cost class, subject, accounting policy, evidence source, asset, category, and direction separate; unresolved values remain unknown. A pure Owner-local, same-asset closed-economy projection reproduces the source experiment's 9.2 TOS internal seller gross receipts, 9.2 buyer spend, zero intra-perimeter transfer net, 1.4 conservative reserve, and -1.4 projected net. | Negotiation code and the local accounting regression helper are implemented. The accounting helper consumes caller-selected internal entries and does not verify transfer finality. Real model, tool, API, invoice, storage, network, and chain-fee producer adapters still require installation and source-specific acceptance evidence; therefore package diagnostic completion is not claimed. |
| C — Outcome evidence and counterparty outcome-risk | Carrier receipt, operation authority, artifact closure, evidence authority, and exact payload-to-source binding are separate checks. Buyer-payment, provider-delivery, and service-capability views are distinct, deduplicate exact assertions, retain conflicts, and never grant execution or economic authority. | Local import/projection tests pass. Two independently operated hosts and Carriers have not yet verified the same retained evidence, so package diagnostic completion is not claimed. |
| D — current escrow composition | OpenFox validates a non-authoritative parent projection over three independent current-profile child Agreements; pins exact stablecoin, settlement parameters, participants, work inputs, source digests, Quote predicates, and a 1.5-unit current-exposure cap; routes unrelated and deferred jobs without starvation; and requires unique qualified predecessor finality before funding a successor. | The 1.2/1.4/1.4 local fixture and negative admission tests are implemented. A released buyer-side finalized Paid Demand evidence resolver and real release/refund/bounce/partition runs are still absent; successors deliberately remain deferred without that resolver. No generalized escrow was implemented. |
| E — independent multi-host diagnostic | No result is recorded by this checkpoint. | Not run. It requires independent Owners, hosts, Agents, Carriers, failure domains, hostile inputs, partitions, clock skew, endpoint loss, nondelivery, refusal, and validator disagreement. Same-process tests cannot satisfy it. |

## 4. Fail-closed properties implemented

### 4.1 Negotiation

- A revision must be exactly version `N+1`, bind the predecessor body digest,
  preserve the Agreement identity, and recompute every authorization target.
- A same Agreement ID and version with different bodies is a durable ambiguous
  fork. Neither body can be authorized, and a concurrent fork is rejected
  before a second Messenger side effect.
- The fork marker is also enforced by reservation, Provider Offer, buyer
  candidate, wallet-evidence, custody-payment, and escrow `accept`/`fund`
  paths. The final custody signature check runs under the Authority mutex;
  Paid Demand reservation admission and new `accept`/`fund` signatures both
  reconstruct the exact buyer asset, spend, locked-capital, and maximum-loss
  exposure from the retained Agreement. The custody effect must also name an
  actual Paid Demand buyer payment obligation. The matching Portfolio
  reservation must exist, remain unreleased, and match every field.
  Already-incurred `release`/`refund` recovery is not disabled by a later
  observation.
- An exact proposal replay is idempotent only for the same proposer and stable
  action identity. A withdrawal cannot cancel an already accepted Agreement.
- Agreement-body, predicate, and signed-acceptance expiry boundaries are
  checked before authorization.

### 4.2 Outcome evidence and economics

- Carrier retention is transport evidence only. The selected finality, meter,
  invoice, Gate, delivery, or equivalent adapter must parse the exact retained
  evidence and bind all authority-relevant payload fields.
- Payment observations are grouped only by exact network and transaction
  digest and must retain exact stable-action and request bindings.
- Cost aggregation never crosses subject, accounting policy, qualified source,
  asset, category, class, or economic direction. `contra` is reported only
  after exact original-assertion lineage is present and compatible; unresolved
  lineage is quarantined without an amount.
- Missing closed denominators never become a probability, and missing cost
  evidence never becomes numeric zero.
- Closed-economy accounting binds one Owner policy, perimeter, participant set,
  and exact asset. Each exact internal transfer appears once as seller gross
  receipts and once as buyer spend; conflicting replay, cross-perimeter, and
  cross-asset inputs fail closed. The conservative reserve remains a planning
  bound, not realized cost, and internal gross receipts are not external
  revenue. Transfer finality qualification remains an upstream input duty.
- A learning cut requires both an authority-qualified, source-bound cohort
  checkpoint and authority-qualified, source-bound members. Generic issuer
  qualification alone cannot populate the cut.
- Provider-delivery and service-capability projections remain explainable
  Owner-local observations. A favorable result cannot admit executable bytes,
  authorize an Agreement, raise a budget, select an adapter, or release funds.

### 4.3 Sequential escrow composition

- The parent object is named and treated as a local projection. It is not an
  accepted Agreement and cannot authorize a child.
- Each child remains one ordinary fixed-price Paid Demand Agreement, Quote,
  escrow, Gate slot, and Receipt. Partial funding, partial release, subjective
  buyer acceptance, revision re-execution, chain `disputed`, fee splitting,
  and adjudicator callbacks remain unavailable.
- `NotApplicable`, `Deferred`, and `Admitted` are distinct local routing
  results, so an unrelated or not-yet-final child does not starve other work.
- A later child requires both exact local Settlement-obligation closure and a
  source-qualified finalized Provider credit for every predecessor. Evidence
  identities cannot be reused across milestones.
- Exact-asset live reservations, released predecessor reservations, ordering,
  and the Owner's current exposure bound are checked before ordinary Paid
  Demand reservation. Native TOS Gas is not counted as stablecoin principal.

## 5. Local validation record

The subset reproducible in this managed runner was checked with the following
commands. They assume the three repositories are adjacent checkouts:

```text
cd tos-service-spec
python3 scripts/operation-outcome-reference.py

cd ../tos-service-protocol
go test ./...

cd ../openfox
GOWORK=off go test ./pkg/earning -run '^$' -count=1
GOWORK=off go test ./pkg/earning -run 'Test(BuildAgreementRevision|UniqueUnforkedAgreementLeafTopology|ForkedAgreementCannotEnterPaidDemandEconomicPaths|AgreementProposalPreflightChecksTimeAndParticipants|LiveReservationForNewEscrowExposure|OutcomeLearningCutRequiresPayloadSourceBinding|OwnerLocalClosedEconomyProjection|ImportOutcomeCarrierPage|CounterpartyAgreementPaymentSummary|QualifiedCostEvidence|CostEvidenceCompatibility|ProviderDeliveryOutcomeRisk|ServiceCapabilityOutcomeRisk|OutcomeRiskViews|ObjectiveMilestone|PaidDemandBuyerReservation|PaidDemandFunding)' -count=1
GOWORK=off go test -race ./pkg/earning -run 'Test(BuildAgreementRevision|UniqueUnforkedAgreementLeafTopology|ForkedAgreementCannotEnterPaidDemandEconomicPaths|AgreementProposalPreflightChecksTimeAndParticipants|LiveReservationForNewEscrowExposure|OutcomeLearningCutRequiresPayloadSourceBinding|OwnerLocalClosedEconomyProjection|ImportOutcomeCarrierPage|CounterpartyAgreementPaymentSummary|QualifiedCostEvidence|CostEvidenceCompatibility|ProviderDeliveryOutcomeRisk|ServiceCapabilityOutcomeRisk|OutcomeRiskViews|ObjectiveMilestone|PaidDemandBuyerReservation|PaidDemandFunding)' -count=1
GOWORK=off go vet ./pkg/earning
```

The specification verifier checks 34 objects, three Actions, and ten named
negative mutations. The OpenFox tests executed in this runner cover Agreement
revision construction and preflight, payload-unbound evidence, network and
assertion conflicts, cost lineage/perimeter isolation, the source experiment's
9.2/9.2/0/1.4/-1.4 native-TOS accounting fixture, the 4.0/1.5 stablecoin
fixture, route starvation, missing finality, evidence reuse, mixed assets, and
unsafe milestone sequence states.

The managed runner used for this checkpoint denies socket creation. The
production `PersonalAuthority` intentionally acquires a deterministic loopback
UDP lock to prevent two local writers from opening one economic authority
domain. Consequently, tests that open a real `PersonalAuthority`, including
the durable fork, replay, negotiation race, and crash-window cases, compiled
here but were blocked at lock acquisition with the generic fail-closed
`economic authority domain is already active on this host` error. Other
socket-backed `httptest` cases are restricted for the same reason. The runner
independently confirmed that even an unrelated Python UDP socket fails with
`EPERM`. The production lock was not weakened or bypassed to make those tests
pass.

The opt-in direct three-node accept fixture is only a low-level Authority to
wallet to escrow to quorum plumbing check. Its generated deployment fixture
does not carry a canonical Agreement or negotiation package, so it is not
Quote-to-Agreement binding evidence. That stronger binding remains the duty of
the full `buyersdk.PreparePurchase` lifecycle path and is not claimed from the
direct fixture.

On a Linux verification host that permits loopback sockets, the remaining
required local command is:

```text
GOWORK=off go test ./pkg/earning -count=1
```

These commands are local verification. They are not independent-operation,
public-network, external-profit, recurring-demand, escrow-security, or
ROADMAP-gate evidence.

## 6. Required next operational evidence

1. Implement and review concrete evidence binders for each admitted real cost
   source; capture actual model/tool/API/storage/network/Gas invoices or meters
   without exposing private content.
2. Implement a buyer-side Paid Demand resolver that reconstructs the exact
   Quote, escrow, Receipt, transfer, and configured finality from authenticated
   chain endpoints. Run release, timeout refund, bounce, replay, crash,
   takeover, and endpoint-disagreement cases.
3. Export one bounded Outcome corpus through independently operated Carriers
   and prove identical verification on at least two independently operated
   hosts while allowing explainable Owner-policy recommendations to differ.
4. Execute Work package E under the design's independence and adverse-path
   requirements. Record unauthorized payments, duplicate effects, maximum
   exposure, recovery, conflicts, unknowns, and rational declines without
   promoting the run into a formal gate claim.
