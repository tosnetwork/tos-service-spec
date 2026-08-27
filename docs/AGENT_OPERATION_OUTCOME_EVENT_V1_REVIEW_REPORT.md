# Agent Operation and Outcome Event V1 Review Report

**Review date:** 2026-08-27

**Reviewed document:**
[Agent Operation and Outcome Event V1](AGENT_OPERATION_OUTCOME_EVENT_V1.md)

**Review boundary:** design coherence only. This report is not implementation,
deployment, interoperability, security-certification, or production evidence.

## 1. Method

Fourteen independent, ephemeral, read-only Codex CLI reviews were run against
the evolving design. Each review used a fresh session and a distinct threat or
implementation focus. Findings were evaluated against first-principles TOS
authority boundaries and incorporated only when the proposed correction did
not create a central market, a second economic authority, or a
profession-specific core workflow.

The final closure review returned `PASS AS DESIGN DRAFT`. Public propagation,
cross-host learning, authoritative financial reporting, and production claims
remain blocked by the Phase-0 decisions, schemas, vectors, implementations, and
evidence listed in the design.

## 2. Review rounds and dispositions

| Round | Independent focus | Verdict at that round | Material disposition |
|---:|---|---|---|
| 1 | First-principles layering and duplication | Changes required | Removed the inner signature/authority/order layer; reduced the event to an `AgentOperationEnvelopeV1` payload; moved commerce identifiers and state authority into assertion profiles |
| 2 | Canonical encoding, digests, signatures, and replay | Changes required | Separated event content ID, signed assertion operation ID, and envelope digest; added non-circular construction, canonical empty sets, typed assertion references, and root-envelope freeze gates |
| 3 | Ordering, forks, checkpoints, crash, and takeover | Changes required | Added denominator-capable ordering, epoch takeover, durable append states, cohort checkpoints, terminal-source binding, and a deterministic projection algorithm |
| 4 | Delegation, revocation, Writer Fence, and Action identity | Changes required | Added authenticated authority time, issuer qualification, historical admission proof, fence/high-water equality, and verified-versus-unverified Action references |
| 5 | Agreement, billing, Gift, payment, escrow, and finality evidence | Changes required | Bound proof sets in the manifest; removed competing evidence commitments; added obligation consumption, Gift/payment separation, reversal, partial-state, and TOS escrow rules |
| 6 | Privacy, retrieval, selective disclosure, and retention | Changes required | Added audience epochs, requester capabilities, hiding commitments, disclosure composition budgets, authenticated encryption, bounded destruction claims, and resolver/credential-origin rules |
| 7 | Spam and resource exhaustion | Changes required | Froze admission ordering, parser/queue/proof/DAG/retrieval limits, scarce admission capability, equivocation retention caps, TTL rules, and bounded rebuild |
| 8 | Cross-repository implementation, compatibility, and rollout | Changes required | Corrected dependency order; added ownership and API boundaries, version matrix, migration, feature gates, rollback, and observability |
| 9 | Accounting, cohorts, probability, and verified learning | Design accepted with blocked claims | Added double-entry ledger, economic perimeter, external-revenue rules, censoring, conversion, forecasts/calibration, financial report, dataset, and Skill-promotion controls |
| 10 | End-to-end adversarial lifecycle | Changes required | Separated assertion signing from Carrier/private-send authorization; added `operation.private-send`; tightened escrow, crash, retained-source, external-evidence, billing, and clock rules |
| 11 | Integrated remediation | Changes required | Disclosed residual outer-actor linkability, bounded authority-proof work, corrected private/public canary dependencies, and froze the empty checkpoint range |
| 12 | Closure after remediation | Changes required | Distinguished same-Carrier retry from a new Carrier-bound publication Action; forbade content-ID dedupe across issuers |
| 13 | Canonical manifest closure | Changes required | Removed the conflicting secondary evidence-item sort order |
| 14 | Final internal P0/P1 consistency check | **Pass as design draft** | No remaining internal P0/P1 contradiction found under the explicitly blocked design-draft status |

## 3. Final architecture reached through review

The reviewed design now has one non-circular construction:

```text
canonical outcome payload
  -> signed Agent Operation assertion
  -> separately authorized Carrier publication or private send
  -> authority-qualified evidence observations
  -> deterministic local projection
```

The event never authorizes contact, execution, payment, retry, Skill promotion,
or settlement. It records an assertion and evidence. Agreement predicates,
side-effect sinks, the Native Gate, custody, settlement Adapters, and finalized
TOS state retain their existing authority.

The common event core has no profession-specific state. Agreement, execution,
delivery, billing, transfer, cost, storage, audit, and other semantics live in
versioned assertion/evidence profiles. Carriers remain replaceable and cannot
establish a global head, a complete market history, or economic truth.

## 4. Repository conclusion

The implementation scope remains the seven repository/component families
identified by the design:

| Repository/component | Required responsibility |
|---|---|
| `tos-service-spec` | Freeze schemas, profiles, registries, stable errors, bounds, vectors, release manifest, and cross-repository acceptance gates |
| `tos-service-protocol` | Implement canonical codecs, identity helpers, structural/authority/evidence verification, projections, APIs, and the shared corpus |
| `openfox` | Implement the crash-safe journal, checkpoints, outcome capture, projections, accounting, reports, bounded learning, and operator controls |
| `tos-messenger` | Implement exact private event transport, audience-epoch enforcement, `operation.private-send`, resolution, and retry/takeover recovery |
| `tos-service-gateway` and a second independent Carrier | Implement bounded publish/resolve/subscribe, Carrier observations, source-local provenance, retention, and database-loss recovery |
| `tos-ai` and selected executors | Produce exact Gate, slot, runner, delivery, resource-metering, and terminal execution evidence |
| `tos`, custody, `tosctl`, and selected settlement Adapters | Produce prepared/submitted/finalized/reversed value evidence and query-before-retry recovery without changing consensus |

No new TOS consensus opcode or chain state is required by V1. Optional market
applications and analytics are consumers, never mandatory authorities.

## 5. Remaining gates

The final pass means the document is internally coherent as a design draft. It
does not waive the design's explicit Phase-0 blockers. At minimum, the project
must still release complete schemas and profiles, exact-byte vectors, a second
independent verifier, protocol implementations, named independent Carrier and
retention failure domains, crash/takeover/adversarial corpora, and a pinned
cross-repository acceptance manifest before enabling public or autonomous use.
