# ATOS Implementation Roadmap v0.2

> ✅ marks below indicate deliverables independently re-verified against the
> `tosnetwork/atos` (and, for Phase 4, `tos-protocol`/`tos`) implementation —
> by direct code review and, where noted, by running tests live against
> PostgreSQL 16 and a live `tos-protocol` RPC server — not merely asserted.
> Unmarked items remain open per `IMPLEMENTATION_STATUS.md`.

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

✅ **Status: complete**, independently re-verified.

Deliverables:

- ✅ Capability/Quote/Invocation/Job/Receipt models;
- ✅ MCP input/output definitions;
- ✅ REST/OpenAPI models;
- ✅ A2A commerce extension mapping;
- ✅ Agent Card extension fields;
- ✅ `requested_trust_mode` and concrete `trust_mode` types;
- ✅ provider `requested_trust_modes` vs derived `supported_trust_modes`;
- ✅ standard trust/proof error codes;
- ✅ proof-profile abstraction;
- ✅ `tos_verified_v1` and `tos_native_v1` contract definitions;
- ✅ execution-signer/delegation abstraction;
- ✅ federation-safe ID abstraction, even if final encoding remains provisional;
- ✅ mock provider;
- ✅ schema/conformance tests.

Mandatory invariants from day one:

1. ✅ Capability `supported_trust_modes` contains only active concrete modes.
2. ✅ Providers request modes through `requested_trust_modes`; they cannot self-certify active support.
3. ✅ `auto` is accepted only on client pre-Quote policy.
4. ✅ Quote always contains concrete `trust_mode`.
5. ✅ Invocation/Job/Receipt inherit mode from Quote.
6. ✅ No execution API allows Quote mode override.
7. ✅ No silent downgrade path exists.
8. ✅ Trust/reputation score is separate from transaction trust mode.
9. ✅ Receipt signer may be delegated, but signer authorization is explicit.
10. ✅ Bulk/private payloads remain off-chain by default.

Success criterion:

✅ A contract test can run one mock Capability through simulated Managed, Verified, and Native resolved modes without changing the client API shape, and rejects `auto` as a final Job/Receipt mode. (`internal/service/v02_contract_test.go`, `internal/service/phase0_lifecycle_conformance_test.go`.)

## 4. Phase 1 — Codex-First Managed MVP

**Goal:** match or exceed the usability of centralized agent marketplaces.

✅ **Status: complete**, independently re-verified live against PostgreSQL 16.

Build:

1. ✅ `https://atos.im/skills/atos/SKILL.md`;
2. ✅ Device Authorization;
3. ✅ MCP Streamable HTTP server;
4. ✅ `atos_search`;
5. ✅ `atos_get_capability`;
6. ✅ `atos_quote`;
7. ✅ `atos_invoke`;
8. ✅ `atos_account`;
9. ✅ centralized Postgres capability/search registry;
10. ✅ Stripe/credit-style accounting or internal test credits;
11. ✅ Managed reservation/settlement ledger;
12. ✅ signed Managed Execution Receipts;
13. ✅ centralized mode activation/certification state;
14. ✅ `trustmode` resolver with only `managed` active in production while v0.2 semantics are already enforced.

During this phase:

```text
requested_trust_mode=auto -> managed
```

✅ because no stronger production mode is active — verified live.

✅ Explicit `verified` or `native` requests MUST return `trust_mode_unavailable`; they MUST NOT be silently treated as Managed. Verified live: explicit `verified`/`native` Quote requests against a Managed-only capability return `trust_mode_unavailable`, not a silently downgraded Managed Quote.

Success criterion:

✅ From a clean Codex environment, one prompt installs/authorizes ATOS and a second prompt searches, quotes, pays for, and executes a sandbox Capability entirely through Managed Mode. The underlying API sequence — device authorization, `atos_search`, `atos_quote`, `atos_invoke` with idempotent replay, and exact account balance settlement — is verified end to end against a live PostgreSQL-backed server (`TestPhase1PublicHTTPFlowAgainstPostgres`).

Also independently verified beyond the original roadmap text: a ✅ crash-safe Managed economic checkpoint state machine (debit, escrow, settlement and release all durable and atomic with Job state, with a startup + periodic reconciler), and a ✅ real `atos -> tos-protocol -> tos-ai Worker` RPC path proven by a passing live integration test, not only the deterministic mock backend.

## 5. Phase 2 — Async Managed Agent Economy + tos-ai

**Goal:** make execution real and support long-running work without coupling execution to chain logic.

### 5.0 Already delivered

- ✅ `atos_create_job`;
- ✅ `atos_get_job`;
- ✅ `atos_cancel_job`;
- ✅ A2A gateway;
- ✅ artifacts/files;
- ✅ real `tos-ai` provider/worker runtime;
- ✅ `SubmitJob`, `GetJob`, `FetchResult`, `FetchReceipt` (`StreamJob` is the subject of Phase 2A below);
- ✅ receipt signing and artifact/output commitments where practical;
- ✅ execution-signer identity on receipts.

Trust/settlement remains centrally managed in this phase.

Important boundary:

```text
atos gateway -> tos-ai = execution
```

Do not move identity, ownership, escrow, settlement, or reputation authority into `tos-ai`.

### 5.1 Delivery discipline for Phase 2 / Phase 3

> **Incident record:** `tosnetwork/atos` PR #4 ("Complete ATOS v0.2 Phase 2 and
> Phase 3") was opened claiming all of the remaining Phase 2 and Phase 3 work
> below as delivered and validated. Independent review found its diff against
> `main` contained zero Go source files, zero tests, and zero migrations —
> only placeholder documents and two unrelated CI workflows. The PR was
> rejected. The remaining Phase 2/3 work is split into the independently
> shippable sub-phases below specifically so this cannot recur: each sub-phase
> is small enough to review completely, and each has its own success
> criterion that can be checked against a real diff.

**Mandatory PR reality gate — applies to every sub-phase from here forward.**
Before a Phase 2 or Phase 3 sub-phase PR is opened for review, `git diff
main...HEAD` MUST contain actual changes to:

- `*.go` implementation files for the claimed behavior;
- `*_test.go` files that exercise it, including the PostgreSQL-backed
  crash-recovery tests named in that sub-phase's success criterion;
- any PostgreSQL migration the behavior requires;
- any OpenAPI / MCP / A2A schema changes the behavior requires.

A PR whose diff does not contain these is not eligible for review, regardless
of what its description, delivery notes, or acceptance-gate documents claim.
One sub-phase per PR. Do not bundle 2A/2B/2C or 3A/3B/3C into a single PR.

### 5.2 Phase 2A — `StreamJob` and resumable streaming

Deliverables:

- durable stream-event journal per Job;
- resume cursor binding sequence, offset, and content digest, rejecting substitution;
- REST Server-Sent Events and MCP/A2A equivalent mappings;
- real `tos-protocol.StreamJob` RPC integration (not only the mock backend);
- bounded delivery (no unbounded buffering of a slow or absent consumer).

Success criterion: a client can disconnect mid-stream and resume from its last
acknowledged cursor without missing, duplicating, or misordering events, and
this is proven by tests against real PostgreSQL 16 covering process restart,
a duplicated upstream event, and a mid-stream disconnect — not only the
in-memory/mock path.

### 5.3 Phase 2B — Metered billing and provider earnings

✅ **Status: complete**, independently re-verified across three adversarial
review rounds and live against PostgreSQL 16 (`tosnetwork/atos` PR #6,
merged as `97441b3`).

Deliverables:

- ✅ Execution Receipt usage metering feeding the charged amount (`computeBillingSnapshot`, `internal/service/billing.go`), gated on the frozen Quote's `pricing_model` — a non-metered model carrying a stray metered rate (corrupted/legacy data) fails closed rather than silently billing by usage;
- ✅ charged amount bounded by the frozen Quote's `total_max` — metered usage only ever narrows the charge (`providerGross.Min(subtotal)`, `grossCharge.Min(totalMax)`), verified by adversarial usage-far-in-excess-of-quote tests;
- ✅ a provider earnings ledger derived only from verified settlement — `RecordSettlement` is only reachable after `VerifyExecutionReceipt` succeeds and `SettleJob` durably commits (`internal/service/economic_recovery.go`'s `settleProviderResultUnderLock`); a receipt that fails verification charges nothing and creates no earning;
- ✅ earnings maturation and payout states (`maturing -> available -> payout_pending -> paid`) with an idempotent external-payout state machine; `frozen`/`released`/`reversed` are modeled in the schema for Phase 2C but intentionally not driven by any Phase 2B code path;
- ✅ every amount-changing transition uses an atomic Job/Ledger boundary — `UpdateJobAndAccount` on the job/principal side, and `UpdateEarning`'s row-locked compare-and-swap (mirroring `UpdateJob`) on the provider-earning side, with both stores (Postgres and in-memory) enforcing that only lifecycle fields — never identity/economic fields or the earning's own ID — can change through it.

Success criterion: ✅ a lost settlement/payout response, a duplicated
settlement attempt, and concurrent payout requests for the same earnings
each leave exactly one economic effect, proven by tests against real
PostgreSQL 16 — verified by
`TestCreateEarningConcurrentCreationHasSingleWinner`,
`TestUpdateEarningCASConcurrentPayoutTransitionHasSingleWinner`
(`internal/store/postgres/billing_test.go`), and
`TestEarningsService_TwoRealPostgresInstancesConvergeToOnePayout`
(`internal/service/earnings_postgres_test.go`, two independent
`postgres.Store` connections simulating two ATOS replicas racing
`PayoutSweep` against a shared payout adapter).

Also independently verified beyond the original roadmap text: fail-fast
`pricing_model`/`metered_rates` contract validation at Capability
registration/update and at Quote-creation time (rejecting an incompatible
combination, e.g. a Fixed-priced capability with a stray metered rate,
before it can ever be frozen into a Quote); and a settlement-time failure
(invalid or incompatible frozen pricing on a legacy/corrupted Quote) now
releases escrow and fully refunds the principal instead of leaving the Job
stuck retrying reconciliation forever — proven by
`TestJobSettlement_LegacyBadFrozenPricingReleasesAndRefunds` and
`TestJobSettlement_CorruptFixedModelWithFrozenRatesReleasesAndRefunds`
(`internal/service/earnings_integration_test.go`), including a confirmed
reproduction of both failure modes against the pre-fix code.

### 5.4 Phase 2C — Managed disputes

Deliverables:

- dispute lifecycle: open, review, resolve;
- opening a dispute freezes the disputed earnings (they cannot mature/pay out while disputed);
- resolution results in exactly one of: principal refund, or provider release of the frozen earnings;
- the resolution transition is one atomic economic operation, not a sequence of independently-failable steps.

Success criterion: a crash between dispute resolution and the atomic
economic transition leaves the dispute (and the frozen earnings) recoverable
to a correct terminal state on restart, never silently resolved twice and
never left frozen forever; proven against real PostgreSQL 16.

## 6. Phase 3 — Provider Self-Service and Mode Readiness

**Goal:** open supply while preparing providers for stronger trust modes.

### 6.0 Already delivered

- ✅ `atos_register_capability`;
- ✅ `atos_update_capability`;
- ✅ provider Agent Card foundations;
- ✅ provider `requested_trust_modes`;
- ✅ derived public `supported_trust_modes`;
- ✅ mode-support data model: `requested | pending | active | suspended | unsupported` (full lifecycle UX is Phase 3B below);
- ✅ immutable Capability manifest/version commitment generation;
- ✅ federation-safe public IDs even while canonical resolution still uses `atos.im`;
- ✅ execution-signer authorization abstraction (rotation/revocation is Phase 3B below).

The public API MUST distinguish:

```text
provider requested Verified support
```

from:

```text
Verified is active and quotable
```

✅ This distinction is implemented (`requested_trust_modes` vs. `supported_trust_modes`, with `supported_trust_modes`/`mode_support` immutable through a generic provider PATCH) and MUST remain true through every sub-phase below.

The same **mandatory PR reality gate** from §5.1 applies to every Phase 3 sub-phase: one sub-phase per PR, and `git diff main...HEAD` must contain real `*.go`/`*_test.go`/migration/schema changes before the PR is opened.

### 6.1 Phase 3A — Provider adapters

Deliverables:

- HTTP, MCP, and A2A provider adapters (outbound calls to third-party/provider endpoints);
- provider health checks and per-mode availability projection;
- Capability input/output schema validation at registration and update time;
- sandbox certification workflow.

Success criterion: a provider adapter call whose outbound response is lost,
duplicated, or delayed past deadline does not corrupt Capability state or
silently mark a mode active; a schema-invalid Capability registration/update
is rejected before persistence.

### 6.2 Phase 3B — Provider trust readiness

Deliverables:

- full mode-support lifecycle UX: `requested -> pending -> active -> suspended -> unsupported`, driven by certification/adapter/health results rather than provider self-assertion;
- per-mode availability exposed alongside `supported_trust_modes`;
- execution-signer authorize / rotate / revoke, with durable pending checkpoints and replay-safe `tos-protocol` calls;
- `verified`/`native` remain fail-closed throughout — mode-support transitions, health, sandbox certification, and signer registration/rotation MUST NOT, by themselves, activate a stronger trust mode.

Success criterion: a signer rotation or revocation that crashes mid-flight is
safely resumable/idempotent on restart, and no combination of health status,
sandbox certification, or signer registration alone can move a capability's
`supported_trust_modes` to `verified`/`native` without the Phase 4 TOS-backed
activation path.

### 6.3 Phase 3C — Open task marketplace

Deliverables:

- publish, apply, and accept lifecycle for open tasks;
- an accepted task is bound to a Quote/Job the same way any other invocation is (no parallel, weaker commercial contract);
- concurrent accept attempts for the same open task resolve to exactly one winner;
- durable recovery after a crash mid-publish/apply/accept.

Success criterion: N concurrent accept attempts for one open task against
real PostgreSQL 16 yield exactly one accepted Job, and a crash between accept
and Quote/Job binding leaves the task recoverable rather than double-bound or
permanently stuck.

### 6.4 Phase 3 overall success criterion

A third-party provider can self-register once, serve Managed traffic, request stronger modes, and already possess the manifest/signer material needed for later certification without changing its Capability identity. (Self-registration, Managed traffic, and requested-mode/manifest material are ✅ implemented; 3A/3B/3C above are what remain before the full self-service onboarding product is complete.)

## 7. Phase 4 — Verified Mode (`atos.im` UX + TOS Guarantees)

**Goal:** ship `trust_mode=verified` as a real protocol guarantee.

Integrate `tos-core`:

- ✅ Agent/provider identity resolution;
- provider identity/ownership production activation — not yet complete;
- ✅ Capability ownership anchoring (interface/manifest-commitment layer implemented; production activation not yet complete);
- ✅ manifest/version commitment anchoring;
- ✅ Quote/terms commitments;
- ✅ enforceable escrow creation/release — contract-backed TaskEscrow Economic Driver implemented and validated on a real localnet (`tos-protocol` PR #4, `tos` PR #19); production multi-endpoint quorum deployment not yet complete;
- ✅ execution-signer authorization registration/resolution (abstraction implemented; live production rotation/revocation not yet complete);
- ✅ Execution Receipt verification;
- ✅ settlement (contract-backed settlement implemented and localnet-validated; production activation not yet complete);
- proof retrieval — not yet exposed through the public ATOS product surface;
- reputation evidence / Proof-of-Service updates — abstraction implemented; production evidence updates not yet complete;
- dispute outcome commitments — not yet implemented.

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

✅ This full interface family is implemented on the ATOS side (`internal/adapters/toscore.Core`), with both a deterministic mock and a real `tos-protocol` RPC-backed implementation; neither silently falls back to the other.

Implement the normative profile:

```text
tos_verified_v1
```

It must guarantee at least:

- TOS-backed provider identity/capability ownership — chain-backed Authority implemented; production identity/ownership activation not yet complete;
- immutable Capability version/manifest commitment — ✅ implemented;
- Quote/terms commitment — ✅ implemented;
- economically enforceable TOS-backed escrow for paid committed work — ✅ contract-backed and real-localnet validated; production deployment not yet complete;
- authorized execution signer and verifiable signer authorization — ✅ abstraction implemented; production rotation/revocation not yet complete;
- signed Receipt and TOS-verifiable receipt commitment — ✅ implemented;
- TOS-backed settlement proof — ✅ contract-backed and real-localnet validated; production deployment not yet complete;
- portable Proof-of-Service evidence — abstraction implemented; not yet a complete portable proof package.

The implementation MAY aggregate/batch registry, receipt, and evidence commitments for performance as long as independent verification remains possible. Economic escrow/settlement MUST remain enforceable; a hash of a private ledger is not enough.

Failure rule:

✅ If any required Verified checkpoint is unavailable, return an explicit proof/network error or require re-quote. Never finish the call as Managed under the original Quote. (Verified live for the Managed-only production configuration; no code path falls back from a failed RPC/Verified checkpoint to Managed.)

Success criterion:

An independent verifier can take a completed Verified proof package and verify provider/capability ownership, manifest version, Quote commitment, signer authorization, Receipt commitment, and settlement outcome without trusting the mutable `atos.im` database. **Not yet met** — no independent verifier library/CLI exists yet; this remains the primary Phase 4 completion gate (see `IMPLEMENTATION_STATUS.md` §10.6, §15).

## 8. Phase 5 — Native Resolution and Decentralized Discovery

**Goal:** activate `trust_mode=native` and remove `atos.im` as canonical namespace/trust authority for Native supply.

Implement:

```text
tos_native_v1
```

which extends all `tos_verified_v1` guarantees with gateway/namespace independence.

Add:

- finalized global Agent/Capability ID scheme — not yet implemented (✅ federation-safe ID fields already modeled from Phase 0, but the finalized global scheme is not yet complete);
- TOS-backed capability registry/ownership events — not yet implemented;
- globally resolvable Capability manifests — not yet implemented;
- open registry event format — not yet implemented;
- independent indexer ingestion protocol — not yet implemented;
- reference TOS indexer — not yet implemented;
- Native resolver library — not yet implemented;
- Native provider endpoint resolution — not yet implemented;
- cross-gateway receipt/proof verification — not yet implemented;
- signer-authorization verification independent of `atos.im` — not yet implemented;
- index rebuild from TOS-verifiable registry/proof events — not yet implemented;
- replay/domain separation for Native commitments/signatures — not yet implemented;
- `atos://agent/...` and `atos://capability/...` semantics, or final equivalent URI scheme — not yet finalized (a provisional `atos://capability/<id>` form already exists from Phase 0).

Search ranking remains off-chain and competitive.

`atos.im` continues to run a fast semantic index, but another operator can reconstruct the Native supply/trust projection needed to build a competing index.

Success criterion:

A Native Capability anchored through one compatible path can be independently resolved, quoted, invoked, verified, and settled through another compatible gateway/resolver without querying the `atos.im` canonical database. **Not yet met** — Native remains correctly fail-closed; this is later-stage work per `IMPLEMENTATION_STATUS.md`.

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

- gateway conformance test suite — not yet implemented;
- open reference gateway components — not yet implemented;
- gateway feature/mode advertisement — not yet implemented;
- cross-gateway Native resolution tests — not yet implemented;
- `tos_native_v1` interoperability tests — not yet implemented;
- standardized trust/proof error semantics — not yet implemented;
- federation-safe caching rules — not yet implemented;
- anti-replay/domain separation tests — not yet implemented;
- gateway-local vs globally canonical field rules — not yet implemented;
- failover guidance — not yet implemented.

A gateway may still provide proprietary ranking, UX, risk controls, billing, enterprise policy, and Managed execution.

Success criterion:

Loss of `atos.im` prevents access to its Managed service but does not prevent a compatible client/gateway from resolving, invoking, verifying, and settling Native ATOS capabilities. **Not yet met** — open gateway federation remains an early-stage foundation per `IMPLEMENTATION_STATUS.md`.

## 10. Phase 7 — Economy and Proof Hardening

**Goal:** harden the network once real multi-provider/multi-gateway volume exists.

Potential work:

- dispute resolver profiles — TaskEscrow contract-level dispute/resolution transitions ✅ implemented; public dispute resolver product profiles not yet implemented;
- multi-resolver/federated arbitration — not yet implemented;
- stronger sybil resistance for Proof-of-Service — not yet implemented;
- counterparty-diversity weighting — not yet implemented;
- proof aggregation/rollups — not yet implemented;
- privacy-preserving reputation proofs — not yet implemented;
- provider collateral/stake policy where justified — not yet implemented;
- enterprise attestations — not yet implemented;
- sponsored/meta-transaction flows — not yet implemented;
- multi-asset settlement — not yet implemented;
- cross-region compliance controls — not yet implemented;
- fraud/risk signal portability without exposing private payloads — not yet implemented;
- signer-delegation policy hardening and hardware/TEE attestations where useful — not yet implemented.

These are later optimizations and MUST NOT block the Managed MVP.

## 11. Cross-Phase Compatibility Rules

1. ✅ **One Capability identity.** Adding Verified/Native support does not create a new Agent-facing Capability solely because trust mode changed.
2. ✅ **One client API.** MCP/A2A/REST do not fork into Managed vs Web3 APIs.
3. ✅ **Quote resolves mode.** `auto` never survives into committed transaction state.
4. ✅ **Provider intent is not certification.** `requested_trust_modes` does not equal active `supported_trust_modes`.
5. ✅ **No silent downgrade.** Stronger trust contracts fail/requote rather than weaken.
6. ✅ **Execution remains off-chain by default.** `tos-ai`/providers execute; TOS anchors trust/economic/proof facts.
7. **Economic proofs are enforceable.** A private-ledger hash is not TOS-backed escrow/settlement. (Contract-backed and real-localnet validated per Phase 4; not yet a general production claim.)
8. ✅ **Global IDs are planned early.** Local database keys never become accidental protocol IDs.
9. ✅ **Search remains an indexer function.** Consensus does not perform semantic ranking.
10. ✅ **Proof-of-Service grows from Receipts.** Do not build a separate unrelated reputation silo.
11. ✅ **Authorized signers are first-class.** Provider root keys do not need to sign every execution.
12. ✅ **Managed Mode remains permanent.** Decentralization is an additional guarantee, not a forced migration.
13. **Public schemas remain stable.** Later phases activate guarantees already modeled in v0.2. (An ongoing process commitment rather than a single verifiable point-in-time deliverable.)

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
