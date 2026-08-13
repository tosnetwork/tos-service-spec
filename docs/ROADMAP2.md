# ATOS Native-Only Implementation Roadmap 2

**Revision:** 2026-08-13
**Status:** Target replacement roadmap
**Target protocol:** `atos_native_v1`

## 0. Scope of On-Chain Authority

Finalized TOS state is authoritative for:

- Agent identity and controller policy;
- Capability identity, ownership, version commitments, and revocation;
- Accepted Quote terms, price, asset, escrow, and dispute policy;
- execution-signer authority;
- receipt/result commitments; and
- settlement, refund, and terminal economic state.

Gateways are authoritative only for their own local service facts, such as
ranking, moderation, cache freshness, transport availability, encrypted
artifact retention, and account preferences. Raw prompts, outputs, artifacts,
and search indexes stay off-chain. No gateway-local record can override a TOS
fact.

## 1. Goal

Build an open Agent Internet in which TOS is the canonical identity, trust,
economic, and proof plane, while independently operated gateways compete on
access, discovery, routing, policy, and user experience.

The target sequence is:

```text
simplify the Native Registry
            |
            v
complete independent Native Resolution
            |
            v
integrate proof and economic guarantees
            |
            v
prove two-gateway interoperability
            |
            v
retire protocol-level Managed/Verified modes
```

These milestones are delivery gates for one protocol, not additional runtime
modes or independently authoritative subsystems.

This roadmap defines the Native-only target and replaces the three-mode
implementation direction for new work. It does not reinterpret historical
v0.2 Quotes, Jobs, or settlements; those remain in an isolated legacy domain.

Normative target documents:

- `docs/NATIVE_ONLY_ARCHITECTURE_SLIMMING.md`;
- `docs/PHASE5_NATIVE_REGISTRY_SIMPLIFICATION.md`; and
- this `docs/ROADMAP2.md`.

The existing `NATIVE_IDENTITY_V1.md`, `NATIVE_CAPABILITY_REGISTRY_V1.md`, and
`PROOF_PROFILES.md`, together with the in-progress Phase 5B RPC and TVM drafts,
are migration inputs, not target authority, until rewritten and re-reviewed
against these three documents. In particular, caller-supplied portable
next-state, per-action Anchor, and selectable-profile semantics must not be
carried into the simplified implementation.

The three simplification documents have non-overlapping roles:

| Document | Normative responsibility |
|---|---|
| `NATIVE_ONLY_ARCHITECTURE_SLIMMING.md` | Product and system authority model |
| `PHASE5_NATIVE_REGISTRY_SIMPLIFICATION.md` | Agent/Capability contract state machines |
| `ROADMAP2.md` | Implementation order and acceptance gates |

If wording conflicts, the authority rule in
`NATIVE_ONLY_ARCHITECTURE_SLIMMING.md` controls architecture, the explicit
contract invariants in `PHASE5_NATIVE_REGISTRY_SIMPLIFICATION.md` control the
Registry, and this roadmap controls only sequencing.

## 2. Target Invariants

Every stage must preserve these invariants:

1. TOS state is the canonical source for Agent identity, Capability ownership,
   immutable versions, signer authority, and economic commitments.
2. No gateway owns the Native namespace.
3. A client can replace its gateway without changing canonical Agent or
   Capability identity.
4. Gateways may rank and filter, but cannot rewrite canonical facts.
5. Private inputs, outputs, and bulk artifacts remain off-chain unless an
   explicit protocol requires otherwise.
6. Relayers and gateways cannot alter signed actions or derive unauthorized
   state transitions.
7. Every ownership transfer is atomic.
8. Every policy installation uses complete on-chain validation.
9. A gateway Quote Proposal is not canonical. A finalized Accepted Quote
   immutably binds the purchased version, price, signer authority, escrow
   terms, and proof obligations.
10. Failure of Native infrastructure fails closed; it never creates an
    unlabelled hosted transaction.

## 3. Repository Responsibilities

```text
atos-spec
= normative Native protocol, schemas, vectors, and conformance requirements

tos
= authoritative contracts and finalized chain state

tos-protocol
= Native action construction, chain publication, resolution, indexing,
  proof verification, escrow, and settlement integration

atos
= reference gateway, public APIs, discovery, Quote policy, orchestration,
  hosted UX, sponsorship, and compatibility boundary

tos-ai
= bounded provider/worker execution and artifact data plane
```

Business packages in `atos` must not become direct consensus clients. Native
chain access and proof logic remain behind reviewed `tos-protocol` interfaces.

### 3.1 Clean schema cutover

Do not turn the legacy `atos.tos.v1` messages into another matrix of optional
fields. Freeze their wire semantics for historical compatibility and define a
small Native-only schema namespace, for example:

```text
protobuf: atos.native.v1
protocol: atos_native_v1
```

The Native schema contains no `TrustMode`, `RequestedTrustMode`,
`requested_trust_modes`, `supported_trust_modes`, `mode_support`, or selectable
`ProofProfile`. It models only:

- canonical Agent and Capability references;
- a gateway Quote Proposal;
- an Accepted Quote commitment/reference;
- invocation and Job transport state;
- Escrow and Receipt references; and
- proof retrieval for the one required Native proof schema.

Legacy protobuf field numbers remain reserved in their existing package. Do
not reuse them and do not copy their mode fields into the Native namespace.
REST, MCP, and A2A expose the same Native semantics; transport adapters must
not recreate mode selection under different field names.

### 3.2 Current contract-removal inventory

The legacy schema currently carries mode selection through:

- `proto/atos/tos/v1/common.proto` (`TrustMode` and `ProofProfile`);
- `capability.proto` (`active_trust_modes` and `requested_trust_modes`);
- `execution.proto` (available/intended/concrete mode and profile fields);
- `trust.proto`, `proof.proto`, and `settlement.proto`;
- `schemas/protocol-types.json`; and
- `schemas/mcp-tools.json`.

These fields stay readable in the legacy package but have no equivalent in
`atos.native.v1`. Migration is complete only when new Native handlers do not
branch on any of them.

## 4. Milestone 0 — Freeze the Native-Only Contracts

### Deliverables

- Record `NATIVE_ONLY_ARCHITECTURE_SLIMMING.md` as the normative target
  architecture decision.
- Define `atos_native_v1` as the only target public protocol. Its version
  fixes the required internal proof schema; clients do not select a profile.
- Mark `managed`, `verified`, and their selection fields as legacy rather than
  extending them with new behavior.
- Define the hosted compatibility label and its non-Native guarantees.
- Inventory every API, database column, protobuf field, test, and package that
  branches on trust mode.
- Freeze terminology: Native Resolution is the canonical-fact layer; Open
  Gateway Federation is the access layer.

### Acceptance gate

- One normative document identifies the authority for every public fact.
- No target-state field has both a gateway database and TOS as co-authority.
- Deprecation does not silently reinterpret existing committed Quotes or Jobs.

## 5. Milestone 1 — Simplify the Phase 5 Native Registry

### Deliverables

- Make typed TVM Cell state the sole authoritative contract state.
- Define portable CBOR as a deterministic projection.
- Remove caller-supplied portable next state from consensus authority.
- Remove the normal-operation Action Anchor. Use the target transaction and
  transition record as the receipt.
- Move sequence, generation, predecessor, and replay checks into the target
  Agent or Capability contract.
- Implement atomic Capability transfer with both authorization sets in one
  operation.
- Apply one complete policy validator to registration, update, recovery
  initiation, recovery completion, and migration.
- Define bounded state and gas limits for every collection and message.

### Required security tests

- invalid-envelope front-running cannot censor a valid action;
- a one-sided transfer approval cannot persist;
- mismatched typed/portable input cannot corrupt canonical state;
- malformed policy installation fails on every path;
- duplicate, reordered, and trailing signature data is rejected;
- stale sequence, generation, and predecessor values fail;
- raw TVM messages are as safe as official-SDK messages; and
- recovery and tombstone invariants survive replay and reordering.

### Acceptance gate

- No unresolved Critical or High findings in an independent contract review.
- One localnet test covers the complete Agent and Capability lifecycle.
- Contract, Go implementation, and frozen vectors agree on every canonical
  action and state hash.

## 6. Milestone 2 — Independent Native Resolution

### Deliverables

- Freeze collision-resistant Agent and Capability identifiers.
- Implement a reference indexer that rebuilds exclusively from finalized TOS
  history.
- Implement a Native resolver library independent of the mutable `atos.im`
  database.
- Resolve current and historical owner policy, Capability versions, revocation,
  and execution-signer authority.
- Support deterministic rebuild from genesis/checkpoint with reorg handling.
- Define canonical versus gateway-local fields.
- Publish conformance vectors for addresses, transitions, manifests, and
  resolver results.

### Acceptance gate

- Two fresh databases independently rebuild identical canonical state.
- Resolution succeeds while `atos.im` and its database are unavailable.
- Invalid code hashes, non-finalized history, reader disagreement, and malformed
  state fail closed.
- A third-party implementation can resolve the frozen public vectors.

## 7. Milestone 3 — Native Discovery and Endpoint Resolution

### Deliverables

- Define how immutable Capability manifests bind execution endpoints or
  endpoint commitments.
- Implement independent discovery indexes over Native Registry state.
- Separate canonical facts from gateway ranking, reputation, moderation, and
  availability observations.
- Define endpoint rotation without rewriting immutable purchased versions.
- Define spam resistance, indexing costs, and abuse policy boundaries.
- Finalize `atos://agent/...` and `atos://capability/...` semantics.

### Acceptance gate

- Two indexers expose the same canonical supply but may rank it differently.
- Suppression by one gateway does not remove the Capability from another.
- An Accepted Quote cannot be rerouted through a newly edited endpoint.
- Endpoint resolution is authenticated and version-bound.

## 8. Milestone 4 — Complete Native Trade and Proof

### Deliverables

- Reuse the existing chain-backed Authority, TaskEscrow, publisher sidecar,
  finality checks, and settlement verification as internal Native components;
  do not expose Verified as a mode.
- Let a gateway prepare a Quote Proposal, then bind the Accepted Quote on-chain
  to the canonical Agent, Capability version, manifest, execution
  signer, price, escrow, dispute terms, and transport commitment.
- Complete the portable proof package and independent verifier.
- Resolve signer authorization against historical Native Registry state.
- Complete dispute, refund, reconciliation, and crash-recovery paths.
- Define walletless sponsorship without transferring canonical authority to the
  sponsoring gateway.

### Acceptance gate

- A client-to-worker-to-chain-to-independent-verifier test succeeds on a real
  localnet.
- Exact payout, refund, terminal escrow state, receipt authority, and finality
  are independently verified.
- Loss of a gateway response is recoverable without duplicate economic effect.
- No proof verifier trusts mutable gateway database fields as canonical input.

## 9. Milestone 5 — Open Gateway Protocol

### Deliverables

- Freeze gateway identity and signed feature advertisement.
- Specify cross-gateway search, Quote Proposal, Quote acceptance, invocation,
  Job status, artifact, proof, and error semantics.
- Bind replay domains to the protocol and intended target without making one
  gateway the namespace owner.
- Define gateway-local authentication separately from Native Agent identity.
- Define failover before a proposal and after on-chain Quote commitment.
- Define portable idempotency and stable transaction references.
- Publish a gateway conformance suite and reference implementation components.

### Acceptance gate

- Gateway A registers/indexes a provider and Gateway B resolves and invokes it.
- Quote Proposals interoperate, and Accepted Quotes and receipts verify across both
  implementations.
- Cross-gateway retries cannot duplicate execution or settlement.
- Gateway shutdown does not prevent canonical state reconstruction or proof
  verification.

## 10. Milestone 6 — Reference atos.im Native Product

### Deliverables

- Make `atos.im` consume the same public Native resolver and gateway contracts
  required of third parties.
- Add hosted wallet, delegated key, and gas-sponsorship UX.
- Retain search, moderation, provider onboarding, streaming, artifacts,
  notifications, and dispute UI as gateway services.
- Clearly label internal credits, fiat adapters, and hosted custody boundaries.
- Remove new protocol dependencies on the legacy Managed database authority.
- Operate at least one independent reference gateway in addition to atos.im.

### Acceptance gate

- The ordinary walletless user flow produces fully Native-verifiable state.
- atos.im can be removed from a completed transaction's verification path.
- Hosted features fail without falsely claiming Native completion.
- Operational monitoring, backups, key rotation, and incident response pass
  production review.

## 11. Milestone 7 — Isolate and Retire Legacy Trust Modes

### Deliverables

- Stop accepting new Quote commitments using `managed` or `verified` modes.
- Preserve read-only interpretation of historical committed records.
- Remove mode activation and `auto` resolution from new Native APIs.
- Isolate any remaining hosted beta flow behind separate non-Native endpoints,
  schemas, storage, and labels.
- Publish client and provider migration guides.
- Remove dead mode branches after the compatibility window.

### Acceptance gate

- No new Native object, Accepted Quote, or proof depends on legacy mode fields.
- Historical records remain auditable with their original semantics.
- Conformance tests contain one Native protocol path rather than a mode matrix.
- Operators can disable hosted compatibility without affecting Native service.

## 12. Milestone 8 — Production Decentralization Gate

### Deliverables

- Run multiple independently operated gateways, indexers, and TOS readers.
- Complete external contract, protocol, and economic audits.
- Exercise chain reorg, reader partition, gateway censorship, key compromise,
  publisher loss, and disaster-recovery drills.
- Establish version negotiation and upgrade governance.
- Publish service health without creating a central activation authority.

### Final acceptance scenario

The release is complete only when:

1. Gateway A is used to publish an Agent and Capability.
2. Gateway B independently resolves them from TOS.
3. A client purchases and invokes the immutable version through Gateway B.
4. A provider signs the result with historically authorized authority.
5. TOS escrow settles the exact committed terms.
6. An independent verifier reconstructs and verifies the entire proof.
7. atos.im is unavailable for steps 2 through 6.
8. Gateway C reaches the same canonical conclusion.

## 13. Work Excluded from the Target

For all new work under this roadmap, do not add features that increase the
legacy mode matrix, including:

- new Managed-versus-Verified-versus-Native business branches;
- new mode-specific Capability identities;
- additional activation-authority states for legacy modes;
- gateway database fields that duplicate canonical Native ownership;
- new fallback behavior from Native to hosted execution; or
- new portable next-state authority alongside typed TVM state.

Security fixes, historical compatibility, and migration instrumentation remain
allowed and required.

## 14. Immediate Next Sprint

The first implementation sprint should be intentionally narrow:

1. Approve the authority and compatibility decisions.
2. Freeze the simplified Agent and Capability state machines.
3. Produce the minimal signed-action schema and vectors.
4. Fix or redesign the three High-severity Native Registry findings.
5. Implement atomic Capability transfer.
6. Build one independent resolver from finalized localnet history.
7. Demonstrate identical resolution from two clean databases.

Do not begin general gateway federation until the authoritative Registry and
resolver are stable. Federation multiplies ambiguity; it does not repair it.
