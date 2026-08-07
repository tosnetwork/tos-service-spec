# ATOS Implementation Roadmap v0.2

## 1. Goal

ATOS v0.2 must ship a centralized product quickly without hard-coding centralization into the protocol.

Implementation sequence:

```text
Managed first
   |
   v
Verified next
   |
   v
Native / federation last
```

The public contracts, however, MUST model the final semantics from Phase 0 so decentralization does not require a breaking API rewrite.

Core type rule:

```text
requested_trust_mode = managed | verified | native | auto
trust_mode           = managed | verified | native
```

Provider-mode rule:

```text
requested_trust_modes = provider intent
supported_trust_modes = derived active/quotable modes
```

`auto` is client request-only and resolves at Quote time.

Normative proof profiles:

```text
verified -> tos_verified_v1
native   -> tos_native_v1
```

See `docs/PROOF_PROFILES.md`.

## 2. Repository Layout

Recommended implementation layout:

```text
atos/
├── cmd/
├── gateway/
├── mcp/
├── a2a/
├── api/
├── auth/
├── discovery/
├── search/
├── matching/
├── quote/
├── invoke/
├── jobs/
├── marketplace/
├── billing/
├── spending/
├── trustmode/
├── proof/
├── resolver/
├── federation/
├── indexer/
├── agent-card/
├── events/
├── adapters/
│   ├── tos-ai/
│   ├── tos-core/
│   ├── http-provider/
│   ├── mcp-provider/
│   ├── a2a-provider/
│   └── human-provider/
├── sdk/
├── skills/
└── web/
```

Rules:

- ordinary gateway packages MUST NOT import TOS consensus/node clients directly;
- execution integration goes through `adapters/tos-ai`;
- trust/economy/proof integration goes through `adapters/tos-core`;
- `trustmode` owns mode-selection/resolution rules across MCP/REST/A2A;
- `proof` owns proof-profile validation, signer-authorization verification, and normalized proof status;
- `resolver` owns federation-safe Agent/Capability resolution;
- `indexer` owns off-chain search/index projections of TOS registry/proof events;
- semantic ranking remains outside consensus.

## 3. Phase 0 — Contract First (v0.2)

**Goal:** freeze public semantics before deep TOS integration.

Deliverables:

- Capability/Quote/Invocation/Job/Receipt models;
- MCP input/output definitions;
- REST/OpenAPI models;
- A2A commerce extension mapping;
- Agent Card extension fields;
- `requested_trust_mode` and concrete `trust_mode` types;
- provider `requested_trust_modes` vs derived `supported_trust_modes`;
- standard trust/proof error codes;
- proof-profile abstraction;
- `tos_verified_v1` and `tos_native_v1` contract definitions;
- execution-signer/delegation abstraction;
- federation-safe ID abstraction, even if final encoding remains provisional;
- mock provider;
- schema/conformance tests.

Mandatory invariants from day one:

1. Capability `supported_trust_modes` contains only active concrete modes.
2. Providers request modes through `requested_trust_modes`; they cannot self-certify active support.
3. `auto` is accepted only on client pre-Quote policy.
4. Quote always contains concrete `trust_mode`.
5. Invocation/Job/Receipt inherit mode from Quote.
6. No execution API allows Quote mode override.
7. No silent downgrade path exists.
8. Trust/reputation score is separate from transaction trust mode.
9. Receipt signer may be delegated, but signer authorization is explicit.
10. Bulk/private payloads remain off-chain by default.

Success criterion:

A contract test can run one mock Capability through simulated Managed, Verified, and Native resolved modes without changing the client API shape, and rejects `auto` as a final Job/Receipt mode.

## 4. Phase 1 — Codex-First Managed MVP

**Goal:** match or exceed the usability of centralized agent marketplaces.

Build:

1. `https://atos.im/skills/atos/SKILL.md`;
2. Device Authorization;
3. MCP Streamable HTTP server;
4. `atos_search`;
5. `atos_get_capability`;
6. `atos_quote`;
7. `atos_invoke`;
8. `atos_account`;
9. centralized Postgres capability/search registry;
10. Stripe/credit-style accounting or internal test credits;
11. Managed reservation/settlement ledger;
12. signed Managed Execution Receipts;
13. centralized mode activation/certification state;
14. `trustmode` resolver with only `managed` active in production while v0.2 semantics are already enforced.

During this phase:

```text
requested_trust_mode=auto -> managed
```

because no stronger production mode is active.

Explicit `verified` or `native` requests MUST return `trust_mode_unavailable`; they MUST NOT be silently treated as Managed.

Success criterion:

From a clean Codex environment, one prompt installs/authorizes ATOS and a second prompt searches, quotes, pays for, and executes a sandbox Capability entirely through Managed Mode.

## 5. Phase 2 — Async Managed Agent Economy + tos-ai

**Goal:** make execution real and support long-running work without coupling execution to chain logic.

Add:

- `atos_create_job`;
- `atos_get_job`;
- `atos_cancel_job`;
- A2A gateway;
- artifacts/files;
- real `tos-ai` provider/worker runtime;
- `SubmitJob`, `GetJob`, `StreamJob`, `FetchResult`, `FetchReceipt`;
- provider earnings;
- Managed disputes;
- usage/metered billing;
- receipt signing and artifact/output commitments where practical;
- execution-signer identity on receipts.

Trust/settlement remains centrally managed in this phase.

Important boundary:

```text
atos gateway -> tos-ai = execution
```

Do not move identity, ownership, escrow, settlement, or reputation authority into `tos-ai`.

Success criterion:

A long-running Capability can execute through `tos-ai`, generate artifacts, produce an authorized-signer Execution Receipt, settle through the Managed ledger, and preserve Quote mode end-to-end.

## 6. Phase 3 — Provider Self-Service and Mode Readiness

**Goal:** open supply while preparing providers for stronger trust modes.

Add:

- `atos_register_capability`;
- `atos_update_capability`;
- HTTP/MCP/A2A provider adapters;
- health checks;
- schema validator;
- provider Agent Cards;
- sandbox certification;
- provider `requested_trust_modes`;
- derived public `supported_trust_modes`;
- mode-support state machine: `requested | pending | active | suspended | unsupported`;
- per-mode availability;
- immutable Capability manifest/version commitment generation;
- federation-safe public IDs even while canonical resolution still uses `atos.im`;
- authorized execution-signer lifecycle;
- delegated signer authorization scope and rotation/revocation;
- open task marketplace publish/apply/accept flow.

Providers may request `verified`/`native`, but production activation remains gated on later TOS integration.

The public API MUST distinguish:

```text
provider requested Verified support
```

from:

```text
Verified is active and quotable
```

Success criterion:

A third-party provider can self-register once, serve Managed traffic, request stronger modes, and already possess the manifest/signer material needed for later certification without changing its Capability identity.

## 7. Phase 4 — Verified Mode (`atos.im` UX + TOS Guarantees)

**Goal:** ship `trust_mode=verified` as a real protocol guarantee.

Integrate `tos-core`:

- Agent/provider identity resolution;
- Capability ownership anchoring;
- manifest/version commitment anchoring;
- Quote/terms commitments;
- enforceable escrow creation/release;
- execution-signer authorization registration/resolution;
- Execution Receipt verification;
- settlement;
- proof retrieval;
- reputation evidence / Proof-of-Service updates;
- dispute outcome commitments.

Required interface families include:

```text
tos-core.ResolveAgentIdentity
tos-core.ResolveCapability
tos-core.VerifyCapabilityOwnership
tos-core.ResolveExecutionSignerAuthorization
tos-core.CreateEscrow
tos-core.ReleaseEscrow
tos-core.VerifyExecutionReceipt
tos-core.SettleJob
tos-core.ReadReputation
tos-core.UpdateReputationEvidence
tos-core.ReadProof
```

Implement the normative profile:

```text
tos_verified_v1
```

It must guarantee at least:

- TOS-backed provider identity/capability ownership;
- immutable Capability version/manifest commitment;
- Quote/terms commitment;
- economically enforceable TOS-backed escrow for paid committed work;
- authorized execution signer and verifiable signer authorization;
- signed Receipt and TOS-verifiable receipt commitment;
- TOS-backed settlement proof;
- portable Proof-of-Service evidence.

The implementation MAY aggregate/batch registry, receipt, and evidence commitments for performance as long as independent verification remains possible. Economic escrow/settlement MUST remain enforceable; a hash of a private ledger is not enough.

Failure rule:

If any required Verified checkpoint is unavailable, return an explicit proof/network error or require re-quote. Never finish the call as Managed under the original Quote.

Success criterion:

An independent verifier can take a completed Verified proof package and verify provider/capability ownership, manifest version, Quote commitment, signer authorization, Receipt commitment, and settlement outcome without trusting the mutable `atos.im` database.

## 8. Phase 5 — Native Resolution and Decentralized Discovery

**Goal:** activate `trust_mode=native` and remove `atos.im` as canonical namespace/trust authority for Native supply.

Implement:

```text
tos_native_v1
```

which extends all `tos_verified_v1` guarantees with gateway/namespace independence.

Add:

- finalized global Agent/Capability ID scheme;
- TOS-backed capability registry/ownership events;
- globally resolvable Capability manifests;
- open registry event format;
- independent indexer ingestion protocol;
- reference TOS indexer;
- Native resolver library;
- Native provider endpoint resolution;
- cross-gateway receipt/proof verification;
- signer-authorization verification independent of `atos.im`;
- index rebuild from TOS-verifiable registry/proof events;
- replay/domain separation for Native commitments/signatures;
- `atos://agent/...` and `atos://capability/...` semantics, or final equivalent URI scheme.

Search ranking remains off-chain and competitive.

`atos.im` continues to run a fast semantic index, but another operator can reconstruct the Native supply/trust projection needed to build a competing index.

Success criterion:

A Native Capability anchored through one compatible path can be independently resolved, quoted, invoked, verified, and settled through another compatible gateway/resolver without querying the `atos.im` canonical database.

## 9. Phase 6 — Open Gateway Federation

**Goal:** make `atos.im` a reference gateway rather than a mandatory choke point.

Allow:

```text
Codex
  |-- atos.im gateway
  |-- partner gateway
  |-- enterprise private gateway
  |-- local/open-source gateway
          \
           -> TOS Network / shared registry, proof, and economic state
```

Ship:

- gateway conformance test suite;
- open reference gateway components;
- gateway feature/mode advertisement;
- cross-gateway Native resolution tests;
- `tos_native_v1` interoperability tests;
- standardized trust/proof error semantics;
- federation-safe caching rules;
- anti-replay/domain separation tests;
- gateway-local vs globally canonical field rules;
- failover guidance.

A gateway may still provide proprietary ranking, UX, risk controls, billing, enterprise policy, and Managed execution.

Success criterion:

Loss of `atos.im` prevents access to its Managed service but does not prevent a compatible client/gateway from resolving, invoking, verifying, and settling Native ATOS capabilities.

## 10. Phase 7 — Economy and Proof Hardening

**Goal:** harden the network once real multi-provider/multi-gateway volume exists.

Potential work:

- dispute resolver profiles;
- multi-resolver/federated arbitration;
- stronger sybil resistance for Proof-of-Service;
- counterparty-diversity weighting;
- proof aggregation/rollups;
- privacy-preserving reputation proofs;
- provider collateral/stake policy where justified;
- enterprise attestations;
- sponsored/meta-transaction flows;
- multi-asset settlement;
- cross-region compliance controls;
- fraud/risk signal portability without exposing private payloads;
- signer-delegation policy hardening and hardware/TEE attestations where useful.

These are later optimizations and MUST NOT block the Managed MVP.

## 11. Cross-Phase Compatibility Rules

1. **One Capability identity.** Adding Verified/Native support does not create a new Agent-facing Capability solely because trust mode changed.
2. **One client API.** MCP/A2A/REST do not fork into Managed vs Web3 APIs.
3. **Quote resolves mode.** `auto` never survives into committed transaction state.
4. **Provider intent is not certification.** `requested_trust_modes` does not equal active `supported_trust_modes`.
5. **No silent downgrade.** Stronger trust contracts fail/requote rather than weaken.
6. **Execution remains off-chain by default.** `tos-ai`/providers execute; TOS anchors trust/economic/proof facts.
7. **Economic proofs are enforceable.** A private-ledger hash is not TOS-backed escrow/settlement.
8. **Global IDs are planned early.** Local database keys never become accidental protocol IDs.
9. **Search remains an indexer function.** Consensus does not perform semantic ranking.
10. **Proof-of-Service grows from Receipts.** Do not build a separate unrelated reputation silo.
11. **Authorized signers are first-class.** Provider root keys do not need to sign every execution.
12. **Managed Mode remains permanent.** Decentralization is an additional guarantee, not a forced migration.
13. **Public schemas remain stable.** Later phases activate guarantees already modeled in v0.2.

## 12. Recommended Build Order Inside Each Mode

For each newly activated concrete trust mode, implement in this order:

```text
Capability eligibility
    -> mode activation/certification
    -> Quote resolution
    -> reservation/escrow
    -> execution inheritance
    -> signer authorization
    -> Receipt generation
    -> Receipt verification
    -> settlement
    -> proof retrieval
    -> Proof-of-Service evidence
    -> cancellation/expiry/dispute paths
```

Do not declare a mode production-ready after implementing only the happy-path settlement call.
