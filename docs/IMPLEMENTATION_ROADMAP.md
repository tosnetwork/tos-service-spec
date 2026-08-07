# ATOS Implementation Roadmap v0.2

## 1. Goal

ATOS v0.2 must ship a centralized product quickly without hard-coding centralization into the protocol.

The implementation sequence is therefore:

```text
Managed first
   |
   v
Verified next
   |
   v
Native/federated last
```

But the public schemas MUST support the final model from Phase 0 so later decentralization does not require a breaking API redesign.

Core mode rule:

```text
requested_trust_mode = managed | verified | native | auto
trust_mode           = managed | verified | native
```

`auto` is request-only and MUST resolve at Quote time.

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
- `trustmode` owns mode-selection/resolution rules and must not be duplicated ad hoc across MCP/API/A2A handlers;
- `proof` owns proof-profile validation and proof-status normalization;
- `resolver` owns federation-safe Agent/Capability resolution;
- `indexer` owns off-chain search/index projections of TOS registry/proof events.

## 3. Phase 0 — Contract First (v0.2)

**Goal:** freeze the public semantics before deep TOS integration.

Deliverables:

- Capability/Quote/Invocation/Job/Receipt models;
- MCP tool definitions;
- REST/OpenAPI models;
- A2A mapping;
- Agent Card fields;
- `requested_trust_mode` and concrete `trust_mode` types;
- standard error codes for mode/proof failures;
- proof-profile abstraction;
- federation-safe ID abstraction (encoding may remain provisional);
- mock provider;
- schema validation tests.

Mandatory invariants from day one:

1. Capability `supported_trust_modes` contains only concrete modes.
2. `auto` is accepted only on pre-Quote requests/policy.
3. Quote always contains concrete `trust_mode`.
4. Invocation/Job/Receipt inherit mode from Quote.
5. No API allows execution to override Quote mode.
6. No silent downgrade path exists.
7. Trust/reputation score is modeled separately from transaction trust mode.

Success criterion:

A contract test can run the same mock Capability through three simulated resolved modes without changing the client API shape.

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
13. `trustmode` resolver with only `managed` active in production but v0.2 semantics already enforced.

`requested_trust_mode=auto` resolves to `managed` during this phase because no stronger production mode is active.

Requests explicitly requiring `verified` or `native` MUST return `trust_mode_unavailable`; they MUST NOT be silently treated as Managed.

Success criterion:

From a clean Codex environment, one prompt installs/authorizes ATOS and a second prompt searches, quotes, pays for, and executes a sandbox Capability entirely through Managed Mode.

## 5. Phase 2 — Async Managed Agent Economy + tos-ai

**Goal:** make execution real and support long-running work without prematurely coupling execution to chain logic.

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
- receipt signing and artifact/output commitments even in Managed Mode where practical.

Trust/settlement remains centrally managed in this phase.

Important boundary:

```text
atos gateway -> tos-ai = execution
```

Do not move identity, escrow, settlement, or reputation authority into `tos-ai`.

Success criterion:

A long-running Capability can execute through `tos-ai`, generate artifacts, produce a signed Execution Receipt, settle through the Managed ledger, and preserve the Quote's concrete mode end-to-end.

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
- per-mode availability;
- mode-support state machine: `requested | pending | active | suspended | unsupported`;
- immutable Capability manifest/version commitment generation;
- federation-safe public IDs even though canonical resolution is still via `atos.im`;
- provider signing-key lifecycle for Execution Receipts;
- open task marketplace publish/apply/accept flow.

Providers may request `verified`/`native`, but production activation remains gated on later TOS integration.

The public API MUST distinguish "provider requested Verified support" from "Verified guarantee is active."

Success criterion:

A third-party provider can self-register once, serve Managed traffic, and already possess the identity/manifest/receipt material needed for later Verified certification without changing its Capability identity.

## 7. Phase 4 — Verified Mode (`atos.im` UX + TOS Guarantees)

**Goal:** ship `trust_mode=verified` as a real protocol guarantee, not a marketing flag.

Integrate `tos-core`:

- Agent/provider identity resolution;
- Capability ownership anchoring;
- manifest/version commitment anchoring;
- Quote/terms commitments;
- escrow creation/release;
- Execution Receipt verification;
- settlement;
- proof retrieval;
- reputation evidence / Proof-of-Service updates;
- dispute outcome commitments.

Required interface families:

```text
tos-core.ResolveAgentIdentity
tos-core.ResolveCapability
tos-core.VerifyCapabilityOwnership
tos-core.CreateEscrow
tos-core.ReleaseEscrow
tos-core.VerifyExecutionReceipt
tos-core.SettleJob
tos-core.ReadReputation
tos-core.UpdateReputationEvidence
tos-core.ReadProof
```

Define and implement the first normative proof profile:

```text
tos_verified_v1
```

It must guarantee at least:

- TOS-backed provider identity/capability ownership;
- immutable Capability version/manifest commitment;
- Quote/terms commitment;
- TOS-backed escrow for paid committed work;
- signed receipt and TOS-verifiable receipt commitment;
- TOS-backed settlement proof;
- portable Proof-of-Service evidence.

The implementation MAY aggregate/batch TOS commitments for cost/performance as long as independent verification remains possible.

Failure rule:

If any required Verified checkpoint is unavailable, return an explicit proof/network error or require re-quote. Never finish the call as Managed under the original Quote.

Success criterion:

An independent verifier can take a completed Verified Receipt and prove the provider/capability identity, Quote commitment, receipt commitment, and settlement outcome without trusting the mutable `atos.im` database.

## 8. Phase 5 — Native Resolution and Decentralized Discovery

**Goal:** remove `atos.im` as the canonical namespace authority for Native supply.

Add:

- finalized global Agent/Capability ID scheme;
- TOS-backed capability registry/ownership events;
- globally resolvable Capability manifests;
- open registry event format;
- indexer ingestion protocol;
- reference TOS indexer;
- native resolver library;
- Native-mode provider endpoint resolution;
- cross-gateway receipt/proof verification;
- index rebuild from TOS-verifiable registry/proof events;
- `atos://agent/...` and `atos://capability/...` resolution semantics (or final equivalent URI scheme).

Search ranking remains off-chain and competitive.

`atos.im` continues to run its own fast semantic index, but another operator can reconstruct the Native supply/trust facts needed to build a competing index.

Success criterion:

A Native Capability registered/anchored through one compatible path can be independently discovered/resolved by another indexer/gateway without querying the `atos.im` canonical database.

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
           -> TOS Network / shared proof and registry state
```

Ship:

- gateway conformance test suite;
- open reference gateway components;
- gateway capability/feature advertisement;
- cross-gateway Native resolution tests;
- proof-profile interoperability tests;
- standardized error semantics;
- federation-safe caching rules;
- anti-replay/domain separation for cross-gateway signatures;
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
- stronger sybil-resistance for Proof-of-Service;
- counterparty-diversity weighting;
- proof aggregation/rollups;
- privacy-preserving reputation proofs;
- provider collateral/stake policy where justified;
- enterprise attestations;
- sponsored/meta-transaction flows;
- multi-asset settlement;
- cross-region compliance controls;
- fraud/risk signal portability without exposing private payloads.

These are later optimizations. They MUST NOT be prerequisites for the Managed MVP.

## 11. Cross-Phase Compatibility Rules

The following rules apply to every phase:

1. **One Capability identity.** Adding Verified/Native support does not create a new Agent-facing capability solely because trust mode changed.
2. **One client API.** MCP/A2A/REST do not fork into Managed vs Web3 APIs.
3. **Quote resolves mode.** `auto` never survives into committed transaction state.
4. **No silent downgrade.** Stronger trust contracts fail/requote rather than weaken.
5. **Execution remains off-chain by default.** `tos-ai`/providers execute; TOS anchors trust/economic/proof facts.
6. **Global IDs are planned early.** Local database keys never become accidental protocol IDs.
7. **Search remains an indexer function.** Consensus does not perform semantic ranking.
8. **Proof-of-Service grows from receipts.** Do not build a separate unrelated reputation silo.
9. **Managed Mode remains permanent.** Decentralization is an additional guarantee, not a forced migration.
10. **Public schemas remain stable.** Later phases activate fields/guarantees already modeled in v0.2 instead of inventing a second protocol.

## 12. Recommended Build Order Inside Each Mode

For each newly activated concrete trust mode, implement in this order:

```text
Capability eligibility
    -> Quote resolution
    -> reservation/escrow
    -> execution inheritance
    -> receipt generation
    -> receipt verification
    -> settlement
    -> proof retrieval
    -> Proof-of-Service evidence
    -> failure/retry/dispute paths
```

Do not declare a mode production-ready after implementing only the happy-path settlement call.
