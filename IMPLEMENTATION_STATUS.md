# ATOS v0.2 Implementation Status

**Status date:** August 8, 2026  
**Canonical roadmap:** [`docs/IMPLEMENTATION_ROADMAP.md`](docs/IMPLEMENTATION_ROADMAP.md)  
**Canonical architecture:** [`docs/ARCHITECTURE_V0.2.md`](docs/ARCHITECTURE_V0.2.md)

> **Legacy implementation baseline:** Status below measures the existing v0.2
> three-mode implementation. For new work, the target architecture and roadmap
> are `docs/NATIVE_ONLY_ARCHITECTURE_SLIMMING.md` and `docs/ROADMAP2.md`.
> Existing completion percentages do not set Native-only implementation order.

## 1. Purpose

This document records the current cross-repository implementation status of
ATOS v0.2 against the canonical roadmap in this repository.

The implementation spans these repositories:

- [`tosnetwork/atos`](https://github.com/tosnetwork/atos) — REST, MCP and A2A gateway, marketplace, commercial Quote and job orchestration;
- [`tosnetwork/tos-protocol`](https://github.com/tosnetwork/tos-protocol) — ATOS/TOS RPC services, trust, proof, chain integration and economic control;
- [`tosnetwork/tos-ai`](https://github.com/tosnetwork/tos-ai) — private Worker execution runtime;
- [`tosnetwork/tos`](https://github.com/tosnetwork/tos) — TOS chain, TaskEscrow contract, `tosctl` and real-localnet validation;
- this repository — canonical public semantics, schemas, proof profiles, RPC contracts and roadmap.

The percentages below are **engineering planning estimates**, not code-coverage
numbers, SLA claims or formal completion certificates. They are based on the
roadmap deliverables and success criteria, with explicit distinction among:

1. protocol semantics specified;
2. code implemented;
3. behavior validated in tests or a real local chain;
4. production infrastructure deployed and activated.

A component may be implemented and locally validated without yet being safe to
advertise as a production trust mode.

✅ marks below indicate items independently re-verified (code read, and/or
tests run against a live PostgreSQL 16 / `tos-protocol` RPC instance) rather
than only asserted by this document.

## 2. Executive Summary

ATOS has moved beyond an architecture-only project. The Managed product path is
substantially implemented, the real cross-repository execution path exists, and
the Verified stack now includes real TOS contract-backed escrow and settlement
components.

Current high-level estimates:

```text
ATOS Managed Product                 85-90%
ATOS Verified Protocol               60-70%
Whole v0.2-to-Federation Roadmap      50-55%
```

The practical interpretation is:

- ✅ **Managed Mode** is close to a deployable product beta.
- ✅ **Verified Mode** has passed the most important architectural threshold: it
  now has chain-backed commitments, a contract-backed Economic Driver, a
  private key-custody publisher and real-localnet TaskEscrow validation.
- **Native Mode** and open gateway federation remain later-stage work (not yet complete).

The current implementation order remains consistent with the roadmap:

```text
Managed first
    |
    v
Verified next
    |
    v
Native / federation last
```

## 3. Current Realized Architecture

The implemented cross-repository boundary is now approximately:

```text
Codex / Claude Code / Agent Client
                 |
                 v
               ATOS
         REST / MCP / A2A
                 |
                 | typed ConnectRPC
                 v
           tos-protocol
      +----------+-----------+
      |          |           |
  Identity   Capability    Trust
      |          |           |
 Settlement   Proof    ExecutionGateway
      |                      |
      |                      | private Unix-socket RPC
      |                      v
      |                    tos-ai
      |                      |
      |                      v
      |                AI / Agent Execution
      |
      | chain Authority + Economic Driver
      v
        TOS Network / TaskEscrow
```

The responsibility split is preserved:

```text
ATOS
= marketplace, gateway, commercial policy, REST, MCP, A2A,
  client authorization, discovery UX and orchestration

tos-protocol
= identity, ownership, trust, execution admission, signer authorization,
  receipt verification, escrow, settlement and proof integration

tos-ai
= bounded execution only

TOS
= finalized identity/commitment/economic/proof state
```

`tos-ai` does not own provider trust, Capability ownership, trust-mode
activation, escrow validity, settlement authority or TOS finality.

## 4. Trust-Mode Status

| Mode | Current status | Meaning |
|---|---|---|
| `managed` | ✅ **Operational in code** | Centralized ATOS account, execution and settlement path; available through explicit mock or real RPC deployments. |
| `verified` | **Implemented as a composable protocol path; locally validated; not yet a general production claim** | Supported by `tos-protocol` when a chain-backed Authority and TaskEscrow Economic Driver are configured on the same TOS network. Production deployment, identity/ownership activation and portable proof verification still require completion. |
| `native` | **Fail closed** | Global canonical resolution, independent index reconstruction, cross-gateway verification and federation are not complete. |
| `auto` | ✅ **Request-time policy only** | Resolves to a concrete mode at Quote time and never survives into Job, Escrow, Receipt or Settlement state. |

The no-downgrade invariant remains mandatory:

```text
verified requested + verified unavailable
    -> explicit error or re-Quote
    -> never Managed under the original Quote

native requested + native unavailable
    -> explicit error or re-Quote
    -> never Managed under the original Quote
```

## 5. Phase Progress Summary

| Roadmap phase | Goal | Estimated completion |
|---|---|---:|
| Phase 0 | Contract First | ✅ **95-100%** |
| Phase 1 | Codex-First Managed MVP | ✅ **85-90%** |
| Phase 2 | Async Managed Agent Economy + `tos-ai` | ✅ **85-90%** |
| Phase 3 | Provider Self-Service and Mode Readiness | **55-65%** |
| Phase 4 | Verified Mode | **60-70%** |
| Phase 5 | Native Resolution and Decentralized Discovery | **15-20%** |
| Phase 6 | Open Gateway Federation | **10-15%** |
| Phase 7 | Economy and Proof Hardening | **5-10%** |

## 6. Phase 0 — Contract First

### Implemented

The public v0.2 semantics are substantially frozen and implemented across the
schemas and gateway domain model:

- ✅ Capability, Quote, Invocation, Job, Escrow, Execution Receipt and Settlement models;
- ✅ REST/OpenAPI, MCP and A2A mappings;
- ✅ `requested_trust_mode = managed | verified | native | auto`;
- ✅ concrete `trust_mode = managed | verified | native`;
- ✅ provider `requested_trust_modes` separated from active
  `supported_trust_modes`;
- ✅ normative `tos_verified_v1` and `tos_native_v1` proof-profile types;
- ✅ immutable Quote-mode propagation through execution and settlement;
- ✅ explicit execution-signer authorization and receipt fields;
- ✅ federation-safe identifiers and commitment fields modeled early;
- ✅ mock implementations and conformance-oriented tests;
- ✅ fail-closed stronger-mode behavior.

The core invariants are present in real code rather than only in documents:

1. ✅ providers cannot self-certify active trust modes;
2. ✅ `auto` is not a committed mode;
3. ✅ Quote freezes one concrete mode;
4. ✅ Job, Escrow, Receipt and Settlement inherit the Quote mode;
5. ✅ execution cannot override the Quote mode;
6. ✅ stronger modes never silently downgrade;
7. ✅ trust/reputation is distinct from transaction trust mode;
8. ✅ delegated execution signers are explicit;
9. ✅ bulk and private payloads stay off-chain by default.

### Remaining work

Phase 0 is effectively complete, but long-term contract maintenance still
requires:

- a single authoritative protobuf/schema source-of-truth workflow;
- automated drift detection between `atos-spec`, generated code and
  implementation repositories;
- preservation of deterministic commitment and compatibility vectors as later
  phases add fields.

## 7. Phase 1 — Codex-First Managed MVP

### Implemented

The Managed gateway currently includes:

- ✅ one REST + MCP + A2A business model;
- ✅ scoped Device Authorization, access-token refresh and revocation;
- ✅ Capability search and retrieval;
- ✅ commercial Quote creation;
- ✅ synchronous invocation;
- ✅ asynchronous jobs;
- ✅ account and spending-policy handling;
- ✅ PostgreSQL relational projections plus complete v0.2 JSON payload persistence;
- ✅ Managed reservation, receipt verification and settlement;
- ✅ signed Managed Execution Receipts;
- ✅ stable Agent Cards and A2A commerce metadata;
- ✅ no stronger-mode downgrade when only Managed is available.

The ordinary MCP consumer surface is intentionally limited to nine tools:

```text
atos_search
atos_get_capability
atos_quote
atos_invoke
atos_create_job
atos_get_job
atos_cancel_job
atos_account
atos_artifact
```

Capability-management and provider tools appear only when the current
Authorization scopes allow them. Tool visibility is not treated as
Authorization; every call revalidates scopes and object ownership.

Also independently verified as part of a crash-safety re-review: ✅ an
explicit crash-safe Managed economic checkpoint state machine (debit/escrow/
settlement/release all atomic with Job state), ✅ a startup + periodic
reconciler that resumes stale jobs, and ✅ a real end-to-end `atos ->
tos-protocol -> tos-ai Worker` RPC path proven by a passing live integration
test — see `tosnetwork/atos`'s own `IMPLEMENTATION_STATUS.md` for the
per-repository detail.

### Remaining work

The main gaps are productization and deployment rather than core protocol
semantics:

- production user-consent and Device Authorization UI;
- final public `atos.im` installation and authorization flow;
- production billing/credit integration and financial operations;
- operational dashboards, alerting, support and incident procedures;
- complete public Codex/Claude installation experience and hosted
  `SKILL.md` distribution;
- production secrets, TLS, database backup and recovery configuration.

The Managed code path is therefore close to beta readiness, but the hosted
product should not be called complete until the public authorization, billing
and operations layers are deployed.

## 8. Phase 2 — Async Managed Agent Economy and `tos-ai`

### Implemented

The real execution boundary now exists:

```text
ATOS
  -> ConnectRPC
  -> tos-protocol ExecutionGatewayService
  -> private Unix-socket tos-ai Worker RPC
  -> execution
  -> signed Execution Receipt
  -> verification
  -> settlement
```

Implemented capabilities include:

- ✅ `atos_create_job`, `atos_get_job` and `atos_cancel_job`;
- ✅ shared A2A Task lifecycle;
- ✅ signed-URL Artifact upload/download, with binary bytes outside MCP/A2A calls;
- ✅ real `tos-ai` Worker execution behind `tos-protocol`;
- ✅ private ConnectRPC over owner-controlled Unix sockets;
- ✅ durable Worker task identity and idempotent replay;
- ✅ resource admission, concurrency, RAM/VRAM/output/deadline bounds;
- ✅ runtime and model preflight;
- ✅ signed model artifacts and activation controls;
- ✅ Ollama, OpenAI-compatible and controlled isolated-executor paths;
- ✅ execution signer identity and content commitments on receipts;
- ✅ cross-service Quote -> Escrow -> Worker -> Receipt -> Verify -> Settle tests;
- ✅ explicit `ATOS_TOS_BACKEND=mock|rpc` selection with no failure fallback.

The `tos-ai` implementation is already deeper than the minimum Phase 2
roadmap in resource safety, model supply-chain controls and container execution
boundaries.

### Remaining work

- complete user-facing Managed dispute workflows;
- broader metered-billing and provider-earnings product flows;
- more production workload, restart, load and long-duration evidence;
- production runtime/model certification for deployed providers;
- complete streaming behavior and large-scale Artifact lifecycle operations;
- reconciliation and operations across many independent Worker deployments.

## 9. Phase 3 — Provider Self-Service and Mode Readiness

### Implemented or substantially present

- ✅ Capability registration, update and pause controls;
- ✅ scoped provider MCP visibility;
- ✅ provider-requested modes separated from active/quotable modes;
- ✅ mode support and proof-profile fields;
- ✅ immutable Capability manifest/version commitments;
- ✅ provider Agent Card foundations;
- ✅ execution-signer authorization abstractions;
- ✅ signed receipt and commitment material required by later certification;
- ✅ real provider execution through `tos-protocol` and `tos-ai`.

### Partial or missing

- complete HTTP-provider adapter;
- complete MCP-provider adapter;
- complete A2A-provider adapter;
- provider health, certification and sandbox product workflows;
- full mode-support lifecycle UX for
  `requested | pending | active | suspended | unsupported`;
- complete provider signer rotation, revocation and operational recovery UI;
- open task marketplace publish/apply/accept lifecycle;
- provider earnings, reporting and support surfaces;
- scalable provider onboarding and policy review operations.

Phase 3 is therefore more than half implemented at the protocol/domain level,
but still requires substantial marketplace product work.

## 10. Phase 4 — Verified Mode

Phase 4 has made the largest recent advance.

### 10.1 ✅ Implemented: typed ATOS/TOS RPC services

`tos-protocol` implements the v0.2 service families used by ATOS:

```text
IdentityService
CapabilityService
TrustService
SettlementService
ProofService
ExecutionGatewayService
```

ATOS has a real typed client for these services and does not silently fall back
to mock behavior when the RPC backend is selected.

✅ Also independently confirmed: the RPC transport's mutation idempotency now
correctly excludes transport metadata (`request_id`/`trace_id`/deadline) from
the replay digest (`tos-protocol` PR #12), and ATOS's `CommitQuote` call binds
`underlying_service_quote_ref` to the same `service_quote_id` `SubmitJob`
presents later — both fixed, merged, and proven by a passing live
`TestATOSConnectRPCManagedLifecycle` end-to-end RPC test.

### 10.2 ✅ Implemented: chain-backed Authority

`tos-protocol` supports explicit Authority selection:

```text
local  -> Managed-only synthetic references
chain  -> finalized TOS references verified by strict-majority readers
```

The chain Authority:

- ✅ has no automatic fallback to `local`;
- ✅ uses deterministic, domain-separated Action identities;
- ✅ delegates transaction publication to a narrow private sidecar;
- ✅ independently verifies the exact TOS transaction;
- ✅ checks payer, payee, amount, commitment purpose, code commitment and finality;
- ✅ does not load wallet or treasury private keys into the ATOS RPC process.

A chain commitment anchor alone is not represented as economic escrow.

### 10.3 ✅ Implemented: contract-backed Economic Driver

The TaskEscrow Economic Driver maps the ATOS lifecycle onto the reviewed TOS
TaskEscrow contract:

```text
CreateEscrow  -> deploy and fund TaskEscrow
SubmitJob     -> accept before Worker dispatch
SettleJob     -> commit result/evidence and settle exact provider payout
ReleaseEscrow -> cancel, timeout or preserve disputed funds as appropriate
```

The driver verifies:

- ✅ allowlisted TaskEscrow code hash;
- ✅ contract identity and immutable fields;
- ✅ exact sender, opcode, query ID and message-body hash;
- ✅ successful VM/action execution;
- ✅ exact provider payout;
- ✅ minimum principal refund;
- ✅ finalized contract post-state;
- ✅ strict-majority agreement and masterchain finality.

### 10.4 ✅ Implemented: key-custody publisher sidecar

The merged TaskEscrow publisher provides a production-shaped private signing
boundary:

```text
GET  /healthz
POST /v1/economic/task-escrow/action
```

It supports:

```text
deploy
accept
result
settle
cancel
timeout
reject
dispute
resolve
```

Its security properties include:

- ✅ wallet/vault material remains outside `tos-protocol`;
- ✅ owner-private Unix socket and state database;
- ✅ exact nanoTOS amounts rather than floating-point conversion;
- ✅ deterministic action identities;
- ✅ durable idempotency before broadcast;
- ✅ lost-response recovery using the original transaction;
- ✅ rejection of reused Action IDs with changed semantics;
- ✅ strict wallet-role mapping for creator, provider, verifier and executor.

The implementation was merged through
[`tos-protocol` PR #4](https://github.com/tosnetwork/tos-protocol/pull/4).

### 10.5 ✅ Implemented: real-localnet TaskEscrow validation

The TOS repository contains a merged real-localnet acceptance test that:

1. ✅ builds TOS and `tosctl`;
2. ✅ boots a real local validator and JSON-RPC endpoint;
3. ✅ creates and funds creator, provider and verifier wallets;
4. ✅ starts the key-custody publisher on a private Unix socket;
5. ✅ deploys the real TaskEscrow contract;
6. ✅ executes reserve/deploy, accept, result and settle;
7. ✅ checks replay recovery and cancellation/refund behavior;
8. ✅ verifies exact payout, refund, terminal state and transaction references.

This was merged through
[`tos` PR #19](https://github.com/tosnetwork/tos/pull/19).

This is a real-chain economic validation, not an in-memory contract mock.
However, it should not be overstated: the merged test primarily validates the
Economic Driver, publisher, `tosctl`, validator and TaskEscrow contract. A
single permanent test that begins with an external ATOS client and includes the
complete ATOS gateway, `tos-protocol`, `tos-ai`, TOS contract settlement and an
independent proof verifier is still a separate completion gate.

### 10.6 What remains before Verified Mode is production-ready

The roadmap success criterion is not yet fully met. The following work remains:

- production TOS-backed Agent/principal identity binding;
- production Capability ownership and manifest-version activation;
- execution-signer authorization registration, rotation, revocation and
  resolution against live TOS state;
- a complete portable `tos_verified_v1` proof package;
- an independent verifier library/CLI that does not trust the mutable ATOS
  database;
- proof retrieval through the public ATOS product surface;
- production Proof-of-Service/reputation evidence updates;
- a public dispute API and operator/user dispute workflow;
- real multi-endpoint quorum deployment and reviewed code-hash allowlists;
- production wallet/HSM/Vault integration;
- reconciliation, monitoring, alerting and disaster recovery;
- one true client-to-worker-to-chain-to-independent-verifier end-to-end test.

Accordingly, Verified should be described as:

> a substantially implemented and locally validated protocol path, not yet a
> general production availability claim.

## 11. Phase 5 — Native Resolution and Decentralized Discovery

### Existing foundations

- ✅ federation-safe IDs and URI fields modeled in v0.2;
- ✅ ARD-compatible discovery and registry components in `tos-protocol`;
- ✅ signed manifests and commitment infrastructure;
- ✅ chain Authority and proof/economic references;
- ✅ resolver and index concepts present in the architecture.

### Major missing work

- finalized global Agent and Capability identifier scheme;
- TOS-backed registry/ownership event format;
- globally resolvable Capability manifests;
- independent reference indexer and complete rebuild process;
- Native resolver library;
- provider endpoint resolution independent of `atos.im`;
- cross-gateway Quote, invocation and proof verification;
- `atos://agent/...` and `atos://capability/...` final semantics;
- Native replay and domain separation across gateways;
- complete `tos_native_v1` proof portability.

Native remains correctly fail closed.

## 12. Phase 6 — Open Gateway Federation

There are useful federation primitives in `tos-protocol`, especially around
ARD registries, bounded federation input and safe discovery. The ATOS gateway
federation product is nevertheless at an early stage.

Still required:

- gateway conformance suite;
- reference compatible gateway components;
- cross-gateway Native resolution tests;
- `tos_native_v1` interoperability tests;
- gateway feature/mode advertisement;
- standardized cross-gateway error semantics;
- canonical-versus-gateway-local field rules;
- anti-replay and domain-separation tests;
- failover and independent operations guidance.

## 13. Phase 7 — Economy and Proof Hardening

Some foundations already exist:

- ✅ TaskEscrow dispute and resolution transitions;
- ✅ durable idempotency and crash-recovery mechanisms;
- ✅ signed receipts and proof commitments;
- ✅ bounded chain observation and finality checks.

Later network-hardening work remains largely open:

- public dispute resolver profiles;
- federated arbitration;
- stronger Sybil resistance;
- counterparty-diversity weighting;
- proof aggregation or rollups;
- privacy-preserving reputation proofs;
- provider collateral/stake policy;
- enterprise attestations;
- sponsored/meta-transactions;
- multi-asset settlement;
- portable fraud/risk signals.

These are intentionally not blockers for the Managed MVP.

## 14. Cross-Repository Feature Matrix

| Capability | Status |
|---|---|
| Canonical v0.2 schemas and trust-mode semantics | ✅ **Implemented** |
| REST gateway | ✅ **Implemented** |
| MCP gateway with compact scoped tool surface | ✅ **Implemented** |
| A2A task/message mapping | ✅ **Implemented** |
| Managed Quote -> reserve -> execute -> receipt -> settle | ✅ **Implemented** |
| PostgreSQL persistence | ✅ **Implemented** |
| Artifact signed-URL transfer | ✅ **Implemented** |
| Real ATOS -> `tos-protocol` RPC | ✅ **Implemented** |
| Private `tos-protocol` -> `tos-ai` Worker RPC | ✅ **Implemented** |
| Long-running jobs and durable Worker tasks | ✅ **Implemented** |
| Crash-safe Managed economic checkpoint state machine | ✅ **Implemented** |
| Provider self-service | **Partial** |
| Chain-backed commitment Authority | ✅ **Implemented** |
| Contract-backed TaskEscrow Economic Driver | ✅ **Implemented** |
| Key-custody publisher sidecar | ✅ **Implemented** |
| Real-localnet TaskEscrow economic E2E | ✅ **Implemented** |
| Production Verified identity/ownership activation | **Not complete** |
| Portable Verified proof package | **Partial / not product-complete** |
| Independent Verified verifier | **Not complete** |
| Public production dispute workflow | **Partial** |
| Native global resolution | **Early foundation** |
| Open gateway federation | **Early foundation** |

## 15. Recommended Next Milestone: Verified Mode Completion Sprint

The highest-value next milestone is to turn the existing Verified components
into one independently verifiable product path.

Recommended order:

1. finalize production TOS Authority and principal identity binding;
2. activate Capability ownership and manifest-version anchoring;
3. complete live execution-signer authorization and revocation;
4. assemble one canonical `tos_verified_v1` proof package;
5. expose proof retrieval from ATOS;
6. ship an independent verifier library/CLI;
7. build one true full-stack end-to-end test;
8. add production reconciliation, monitoring and operational controls.

The target acceptance path is:

```text
Codex / Agent
    -> atos_search
    -> atos_quote (trust_mode = verified)
    -> TOS TaskEscrow reserve
    -> tos-ai execution
    -> authorized-signer Execution Receipt
    -> TOS receipt/settlement commitments
    -> atos_get_proof or equivalent proof retrieval
    -> independent verifier
    -> VALID
```

The same test suite must also prove that:

- unavailable Verified checkpoints fail closed;
- no request silently becomes Managed;
- a wrong principal, provider, Capability version, signer, Receipt, escrow or
  settlement is rejected;
- duplicate requests do not duplicate execution or payment;
- lost responses recover the original chain action;
- expired Quotes and execution deadlines cannot settle;
- raw private payloads are not required for independent verification.

When this milestone is complete, the project can reasonably describe the
result as **ATOS Verified Mode Alpha**.

## 16. Readiness Summary

```text
Managed Product
█████████░  approximately 85-90%

Verified Protocol
███████░░░  approximately 60-70%

Native / Federation
██░░░░░░░░  early foundation

Whole Roadmap Through Federation
█████░░░░░  approximately 50-55%
```

The most important conclusion is that the project no longer needs another
large architectural rewrite. The central abstractions are holding:

- ✅ one Capability identity;
- ✅ one client API;
- ✅ Quote-time mode resolution;
- ✅ off-chain execution by providers/`tos-ai`;
- ✅ TOS-backed trust, economics and proof;
- ✅ Managed Mode as a permanent product option;
- Native Mode as an additional gateway-independent guarantee (not yet complete).

The next work should concentrate on closing the Verified proof chain and
production activation gates rather than expanding the default MCP vocabulary
or introducing a second Web3-specific client API.

## 17. Maintenance Rule

Update this file whenever one of the following changes:

- a roadmap phase reaches a new success criterion;
- a trust mode becomes production-active or is suspended;
- a major cross-repository RPC or proof contract changes;
- a real-chain or cross-gateway acceptance gate is added;
- the recommended next milestone changes.

Per-repository status documents may describe narrower or earlier snapshots.
This file is intended to remain the cross-repository status summary aligned
with the canonical ATOS v0.2 roadmap.
