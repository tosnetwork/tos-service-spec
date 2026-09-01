# OpenFox Agent Commerce Trust and Market Infrastructure — Codex Review Report

**Reviewed document:** [Post-Experiment Delta
Design](OPENFOX_AGENT_COMMERCE_TRUST_AND_MARKET_INFRASTRUCTURE_DESIGN.md)

**Review status:** PASS as a reconciled, non-normative application-delta draft;
repository validation passed

**Review class:** internal AI-assisted architecture and documentation review

**Claim limit:** this report is not an independent implementation review,
security audit, contract review, schema freeze, conformance result, deployment
record, external acceptance result, or roadmap-gate decision.

## 1. Why the earlier review was reopened

The initial OpenFox-local draft and its review concentrated on internal
milestone-state consistency, recovery, conservation, dispute fallback, and
exposure. That work found and corrected useful internal defects, but it did not
perform a complete comparison with the current `tos-service-spec` authority
documents and implementations.

Its final “no actionable findings” statement is therefore superseded. It must
not be interpreted as evidence that a generalized staged escrow, portable
reputation object, cost schema, or negotiation object is compatible with or
released by the existing specifications.

The document was moved conceptually from an OpenFox implementation design to a
non-normative post-experiment delta in `tos-service-spec`, then rewritten around
reuse and exact gaps. The experiment report remains in OpenFox at a pinned
commit.

## 2. Review scope and authority baseline

The review compared the delta with:

- `PRODUCT_STRATEGY.md`, `ARCHITECTURE.md`, and `ROADMAP.md`;
- `AGENT_INTENT_EXCHANGE_V1.md` and `schemas/agent-commerce-v1.json`;
- `AGENT_NATIVE_MESSENGER_CONVERSATION_AND_COMMERCE_V1.md`;
- `SETTLEMENT.md`, `ACCEPTED_QUOTE_TVM_V1.md`,
  `STABLECOIN_ESCROW_TVM_V1.md`,
  `PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md`, and the Native Execution Gate;
- `SEMANTIC_ACTION_IDENTITY_V1.md`;
- `AGENT_OPERATION_OUTCOME_EVENT_V1.md` and its implementation/review records;
- `AGENT_ECONOMY_METRICS_V1.md`;
- `AGENT_TRUSTED_CAPABILITY_AND_OWNER_CONTROL_V1.md` and its implementation
  report; and
- the OpenFox autonomous earning design, implementation plan, roadmap, and
  pinned eight-Agent experiment report.

Maturity was reviewed separately from object existence. Intent and Semantic
Action are release candidates with external acceptance pending. Outcome Event
is an implementation candidate with default-off public publication and no
independent-operator availability claim. Economy Metrics is not implemented.
Trusted Capability remains a design candidate with coordinated implementation
surfaces but without formal Phase 0, Gate S, Gate M, or campaign acceptance.
Paid Demand escrow remains the current fixed-price objective stablecoin rail.

## 3. Cross-specification findings and dispositions

| ID | Severity | Finding | Disposition in the rewritten delta |
|---|---:|---|---|
| R-01 | blocking | Generic demand, supply, and heterogeneous business discovery were described as missing even though Intent V1 already covers them | Classified `REUSE`; no new per-business API or schema |
| R-02 | blocking | A second Agreement/milestone model duplicated the existing obligation DAG, billing terms, per-obligation adapters, and settlement obligations | Reused the existing Agreement graph; milestone grouping is a composition/local projection |
| R-03 | blocking | A new generic `CounterOffer` overlapped Application V2, full Agreement proposals/versions, and older Messenger `negotiation.*` events | Agreement proposals are the primary path; legacy labels are non-authorizing rendering/compatibility events; a new profile needs a demonstrated ambiguity |
| R-04 | high | “Stale/superseded” implied a globally authoritative proposal head that V1 does not define | Rejected known expired/withdrawn/conflicting lineage, forbade arrival-order inference, and isolated a future proposal-head profile as conditional |
| R-05 | blocking | One milestone state graph combined chain escrow, Agreement/obligation, semantic-action, execution, and Outcome observation states | Removed the global graph and documented four separate namespaces and authorities |
| R-06 | blocking | Partial funding, buyer acceptance, revision re-execution, `disputed`, split settlement, fee split, adjudication, and cancellation remedies were attributed to current escrow behavior | Preserved escrow V1; moved every unsupported behavior to deferred or separately versioned candidate work |
| R-07 | blocking | The staged fixture used native TOS although the current Paid Demand service asset is one exact stablecoin issued on TOS Network | Replaced it with 4.0 display units of one exact supported stablecoin split 1.2/1.4/1.4; native TOS Gas is separate |
| R-08 | high | Exposure reservation and side-effect identity were presented as new concepts, and bounce/replay guarantees were stronger than escrow V1 | Reused Portfolio and Semantic Action; retained ambiguous reservations; documented that a bounced request may be accepted again while a second terminal payout remains forbidden |
| R-09 | blocking | A new portable outcome dossier duplicated Outcome Event sets, evidence manifests, disclosure projections, cohort checkpoints, corrections, conflicts, and perimeters | Reduced “dossier” to a bounded application view over existing objects; any exact missing portable field requires its own reuse-failure record |
| R-10 | high | Duplicate evidence, completeness, and expiry rules were overgeneralized | Exact Carrier copies deduplicate; distinct issuer assertions remain; checkpoints prove only their scope/cut; expiry does not invalidate historical signatures |
| R-11 | blocking | Cost classes, refund transfers, unknown projection state, Owner P&L, and narrow Agent Economy Metrics were at risk of being conflated | Reused Outcome cost classes; kept refunds as transfers, `unknown` as projection state, Owner reports separate, and Economy Metrics narrow/not implemented |
| R-12 | high | “Trust” could be confused with executable-artifact Admission, Promotion, and Use Binding | Renamed the computation `counterparty outcome-risk` and explicitly prohibited it from granting executable or economic authority |
| R-13 | blocking | New Slice 0--6 exit criteria created a weaker parallel gate/campaign system | Converted them to non-gating work packages; formal claims defer to ROADMAP and the controlling Campaigns 1--6 |
| R-14 | high | ROADMAP still said Trusted Capability schemas, vectors, verifier, codec, and runtime did not exist | Reconciled ROADMAP and the normative document with the implementation report while retaining design-candidate and unpassed-gate status |
| R-15 | high | The autonomous earning implementation plan's “Development gaps” table read as a current missing-capability list | Relabeled it as the historical baseline and pointed current status to authority documents and this reconciliation |
| R-16 | high | Messenger's older typed proposal labels could be mistaken for a second generic commerce authority | Added a precedence/reconciliation section and redefined MSG-034 as projection/rendering and compatibility work |
| R-17 | high | Keeping the full design in OpenFox would create two canonical sources and broken relative evidence links | Canonical delta and review moved to `tos-service-spec`; source report remains pinned in OpenFox; duplicate OpenFox drafts are removed |

## 4. Settlement-specific review result

The current rail can be evaluated as this composition:

```text
one generic parent Agreement
  -> several objective milestone obligations
  -> one current fixed-price Quote + escrow + Gate slot + Receipt per milestone
  -> sequential funding after exact predecessor evidence
  -> Owner-wide atomic Portfolio reservation before each funding action
```

This is a validation hypothesis, not a released cross-escrow profile. The
review does not claim that current Quote binding already proves the complete
parent-to-child mapping or cross-escrow dependency. Those are the first facts
the reuse trial must establish.

The following remain incompatible with escrow V1 and are not approved by the
delta: partial funding of one escrow, partial or split payout, post-delivery
buyer acceptance, same-Quote revision re-execution, a chain `disputed` state,
an adjudicator callback, subjective quality enforcement, or generalized
arbitration. If the multi-escrow composition fails, a successor requires a new
Quote binding, contract, Gate/Receipt lineage, resolver, canonical schema,
amount and deadline rules, Semantic Action mapping, security review, and
conformance vectors.

## 5. Remaining conditional gaps

These are questions to prove, not approved new objects:

1. Can existing Agreement references and Paid Demand Quote binding
   deterministically bind each child escrow to one parent milestone and exact
   predecessor terminal evidence?
2. Can independent implementations reconstruct multi-round proposal lineage
   safely without a global proposal-head/supersession profile?
3. Do current Outcome event sets, manifests, bundles, and disclosure
   projections carry every bounded commerce-history view required by the
   product without another wire object?
4. Which real meter and invoice sources can produce profile-qualified cost
   evidence while respecting Owner privacy?
5. Does sequential current-escrow composition satisfy the product's exposure,
   fee, recovery, and usability target, or does it produce a reproducible need
   for a versioned successor?

General subjective arbitration, a global reputation score, and expansion ahead
of recurring paid demand remain out of scope rather than unresolved blockers
for the current product wedge.

## 6. Review outcome and claim boundary

The cross-specification conflicts listed above are resolved at the design-text
level. A fresh read-only Codex review compared the rewritten delta and affected
documents with the controlling strategy, roadmap, Intent, schema, settlement,
Semantic Action, Outcome, metrics, Trusted Capability, Messenger, and OpenFox
earning documents. It returned `No actionable findings`.

The conclusion is:

> PASS as a reconciled, non-normative application-delta draft.

That conclusion means only that the document now distinguishes existing
capabilities, operational validation gaps, local policy, conditional portable
gaps, and deferred expansion. It does not approve a new schema or contract and
does not establish implementation, security, conformance, independent
operation, market demand, production readiness, or any ROADMAP gate.

## 7. Validation record

Validation completed on 2026-09-01:

- Codex CLI `0.152.0`, model `gpt-5.6-terra`, two read-only passes (full
  cross-specification review followed by a targeted final-diff/status review):
  both returned `No actionable findings`;
- `scripts/verify-trusted-capability-v1.sh`: 63 vectors, 255 executable negative
  mutations, independent Agent Commerce action/CBOR/digest/Ed25519 vectors, and
  trusted-capability specification artifacts passed;
- repository-local Markdown targets in every changed `tos-service-spec`
  document resolved;
- all `schemas/*.json` parsed with `jq`;
- the pinned OpenFox experiment commit and path resolved with `git cat-file`;
- `git diff --check` passed in `tos-service-spec` and OpenFox; and
- `make lint-docs` passed in OpenFox after the duplicate design drafts were
  removed and the canonical links were updated.

The Codex pass retained these non-blocking validation risks:

- prove parent-milestone, child-Quote, and predecessor-terminal binding for the
  multi-escrow composition;
- exercise permitted old-request replay after an authenticated escrow bounce;
- preserve Outcome Event's default-off public and unpassed
  independent-operator status;
- connect real cost/invoice sources and keep missing external-profit evidence
  explicit; and
- prevent multi-host diagnostic results from being promoted into production,
  recurring-demand, or ROADMAP-gate claims.
