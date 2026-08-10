# ATOS Implementation Roadmap v0.2

**Revision:** 2026-08-10  
**Role:** canonical implementation-order and acceptance-gate document for ATOS v0.2.

> ✅ marks below indicate deliverables independently re-verified against the
> implementation repositories by direct code review and, where noted, by
> running live tests against PostgreSQL 16, real `tos-protocol` RPC services,
> and/or a real TOS localnet. Unmarked items remain open.
>
> This roadmap is intentionally implementation-oriented. It is not permission
> to invent missing public semantics. If a required public contract, scope,
> state transition, commitment field, or cross-repository RPC is still
> undefined in the normative specs, freeze that contract in `atos-spec` first,
> then implement it. Code MUST NOT silently become the specification.

Canonical companion documents:

- `docs/ARCHITECTURE_V0.2.md` — responsibility boundaries and legal call paths;
- `docs/MCP.md` — MCP transport, tool, visibility and scope semantics;
- `docs/PROOF_PROFILES.md` — normative trust/proof guarantees;
- `IMPLEMENTATION_STATUS.md` — current cross-repository implementation status.

---

## 1. Goal

ATOS v0.2 must ship a centralized product quickly without hard-coding
centralization into the protocol.

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

The public contracts MUST model the final semantics early enough that stronger
trust guarantees can activate without forking the client protocol.

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

The same Capability identity and the same REST/MCP/A2A commercial model must
survive the path from Managed to Verified to Native.

---

## 2. Repository Responsibilities and Legal Call Paths

ATOS v0.2 spans several repositories. Work must preserve these boundaries even
when one roadmap phase requires coordinated PRs in more than one repository.

```text
atos
= public REST/MCP/A2A gateway, auth, discovery, commercial Quote policy,
  Job orchestration, provider control plane, Managed accounting/disputes,
  adapter binding metadata and readiness projections

tos-protocol
= typed execution gateway plus identity, ownership, trust, proof,
  signer authorization, escrow and settlement integration

tos-ai
= execution/data plane: bounded workers and execution adapters
  (model/local/HTTP/MCP/A2A/human where applicable)

tos
= finalized TOS identity/commitment/economic/proof state and contracts

atos-spec
= normative public semantics, schemas, proof profiles, RPC contracts
  and this implementation roadmap
```

Legal dependency rules:

- ordinary `atos` business packages MUST NOT import TOS consensus/node clients directly;
- execution integration from the ATOS business layer goes through the existing execution boundary (`adapters/tos-ai` / `tos-protocol` ExecutionGateway), not a second direct provider execution engine;
- trust/economy/proof integration goes through `adapters/tos-core` / `tos-protocol`;
- provider endpoint health/certification orchestration MAY live in the ATOS control plane, but actual protocol probes/execution MUST use the same bounded adapter/execution boundary rather than ad-hoc ungoverned network calls from settlement or Job business logic;
- `trustmode` owns mode-selection/resolution rules across REST/MCP/A2A;
- `proof` owns proof-profile validation, signer-authorization verification and normalized proof status;
- `resolver` owns federation-safe Agent/Capability resolution;
- `indexer` owns off-chain search/index projections of TOS registry/proof events;
- semantic ranking remains outside consensus.

The architectural shorthand is:

```text
tos-ai executes;
tos-core trusts, proves, and settles.
```

Provider adapters MUST NOT become identity, trust-mode activation, escrow,
settlement, proof or reputation authorities.

---

## 3. Universal Implementation Rules

These rules apply to every unfinished phase and are specifically intended to
prevent implementation agents from filling specification gaps with plausible
but incompatible behavior.

### 3.1 Spec-first gate

Before implementing a new public operation or state transition, identify the
normative contract that defines:

- request and response shape;
- authorization scope and role/resource checks;
- idempotency identity;
- ownership/binding rules;
- state-machine transition;
- commitment/domain-separation rules where applicable;
- error semantics.

If one of those is materially undefined, update `atos-spec` first. Do not
invent a public API in implementation code and document it afterward.

### 3.2 Immutable committed history

A committed Quote is authoritative for:

- provider;
- Capability ID/version;
- selected execution binding or an immutable commitment that resolves it;
- concrete trust mode;
- proof profile;
- price/maximum/currency;
- settlement policy;
- dispute policy;
- expiry/deadline.

A later Capability/provider configuration update MUST NOT silently reroute,
reprice, weaken or otherwise reinterpret an already committed Job.

When execution semantics depend on a provider binding, one of the following
must be true before Phase 3A is considered complete:

1. the immutable Capability version referenced by the Quote remains
   retrievable with that exact binding; or
2. the selected binding/snapshot (or its canonical commitment plus a durable
   resolver key) is frozen into committed Job/Quote state.

Reading the provider's current live endpoint at execution time for an old
Quote is forbidden.

### 3.3 Idempotency and external side effects

Every externally side-effecting operation follows:

```text
durable stable intent / identity
        |
        v
external operation using that same identity
        |
        v
durable completion / observed outcome
```

A lost response is not failure. A timeout is not proof the provider did
nothing. A retry must reuse the same semantic identity. Reusing the same
idempotency identity with changed semantics is an `idempotency_conflict`, not
a new operation.

If an external protocol cannot determine whether a side effect happened, the
local state must remain explicitly uncertain/recoverable; it must not guess a
terminal success or failure.

### 3.4 Economic mutations

Any principal balance, escrow, settlement, earning, refund, reversal or payout
transition must use the existing atomic economic/store boundaries or a new
purpose-built transactional primitive of equivalent strength.

Never implement an economic transition as an unsafe `Get + modify + Put` pair.

### 3.5 Multi-replica correctness

Correctness must not depend on process-local mutexes. Where a state is durable,
critical concurrency tests must use real PostgreSQL 16 and, when relevant, two
independent Store/service instances against the same database.

### 3.6 Real-protocol tests

A transport/adaptor deliverable is not complete with only Go-interface mocks.
Use real in-process protocol servers/clients for HTTP, MCP, A2A or ConnectRPC
where applicable, plus mocks only for deterministic fault injection.

### 3.7 Security by default

Provider-controlled network configuration is hostile input until validated.
Production defaults must bound:

- request and response sizes;
- deadlines and cancellation;
- redirects;
- private/link-local/loopback destinations unless explicitly operator-approved;
- DNS rebinding / resolved-address policy where relevant;
- credential/header forwarding;
- error/log redaction;
- concurrency and goroutine growth.

An invocation must never be allowed to choose an arbitrary outbound URL or
credential.

### 3.8 Completion claims

Before a phase/work package is reported complete:

```bash
git diff --stat origin/main...HEAD
git diff --name-only origin/main...HEAD
git diff --check origin/main...HEAD
gofmt -l .
go vet ./...
go build ./...
go test ./... -race -count=1
```

For PostgreSQL-backed behavior, also run migrations from a fresh PostgreSQL 16
database and execute the relevant suite against it.

A completion report must distinguish:

- tests actually executed on the exact current HEAD;
- tests skipped because an environment variable/service was absent;
- known pre-existing failures reproduced on `main`;
- CI jobs that failed to start versus tests that actually ran and failed.

### 3.9 PR reality gate

A roadmap work package is not reviewable unless the diff contains the real
implementation, real tests, and every required migration/schema change.

Do not substitute acceptance Markdown, TODO files, generated delivery notes,
placeholder adapters, or PR prose for implementation.

A cross-repository phase may require coordinated PRs. Keep them independently
reviewable and explicitly pinned to compatible commits. No single repository
PR may claim the whole phase complete until every required cross-repository
piece and the end-to-end acceptance test exist.

---

## 4. Phase 0 — Contract First (v0.2)

**Goal:** freeze public semantics before deep TOS integration.

✅ **Status: complete**, independently re-verified.

Delivered:

- ✅ Capability/Quote/Invocation/Job/Receipt models;
- ✅ REST/OpenAPI, MCP and A2A mappings;
- ✅ `requested_trust_mode` and concrete `trust_mode` types;
- ✅ provider `requested_trust_modes` vs derived `supported_trust_modes`;
- ✅ standard trust/proof error codes and proof-profile abstraction;
- ✅ `tos_verified_v1` and `tos_native_v1` contract definitions;
- ✅ execution-signer/delegation abstraction;
- ✅ federation-safe ID abstraction;
- ✅ mock provider and conformance tests.

Permanent invariants:

1. ✅ `supported_trust_modes` contains only active concrete modes.
2. ✅ Provider intent cannot self-certify active support.
3. ✅ `auto` is request-only.
4. ✅ Quote contains one concrete immutable trust mode.
5. ✅ Invocation/Job/Receipt inherit the Quote mode.
6. ✅ Execution cannot override the Quote mode.
7. ✅ No silent downgrade path exists.
8. ✅ Reputation score is separate from transaction trust mode.
9. ✅ Delegated execution signers are explicit.
10. ✅ Bulk/private payloads remain off-chain by default.

---

## 5. Phase 1 — Codex-First Managed MVP

**Goal:** match or exceed centralized agent-marketplace usability.

✅ **Status: complete**, independently re-verified live against PostgreSQL 16.

Delivered foundations include Device Authorization, compact MCP, capability
search/quote/invoke/account, PostgreSQL registry, Managed reservation and
settlement, signed Managed Execution Receipts, centralized mode activation
state, fail-closed stronger-mode behavior, crash-safe economic recovery, and a
real `atos -> tos-protocol -> tos-ai` execution path.

Managed Mode remains a permanent product mode; later decentralization does
not remove it.

---

## 6. Phase 2 — Async Managed Agent Economy + `tos-ai`

**Goal:** make execution real and long-running while preserving the control /
execution / trust-plane split.

### 6.1 Phase 2A — StreamJob and resumable streaming

✅ **Status: complete**, merged through `tosnetwork/atos` PR #5.

Delivered:

- ✅ durable per-Job stream-event journal and cursor;
- ✅ sequence/offset/digest substitution protection;
- ✅ REST SSE with MCP/A2A equivalent stream mapping;
- ✅ real `tos-protocol.StreamJob` integration;
- ✅ bounded delivery;
- ✅ restart, duplicate, disconnect and genuine working-to-completed tests on PostgreSQL 16.

### 6.2 Phase 2B — Metered billing and provider earnings

✅ **Status: complete**, merged through `tosnetwork/atos` PR #6.

Delivered:

- ✅ deterministic billing from frozen Quote terms + verified usage;
- ✅ final charge bounded by `total_max`;
- ✅ immutable BillingSnapshot / semantic idempotency checks;
- ✅ one earning per settlement;
- ✅ maturation and idempotent payout state machine;
- ✅ crash-safe and multi-replica payout recovery;
- ✅ fail-fast pricing validation and sub-cent metered rates;
- ✅ production default payout disabled unless a real backend is explicitly configured.

### 6.3 Phase 2C — Managed disputes

✅ **Status: complete**, merged through `tosnetwork/atos` PR #7.

Delivered:

- ✅ open/review/resolve lifecycle;
- ✅ dispute hold/freeze preventing new payouts while disputed;
- ✅ honest `clawback_required` for already-paid earnings;
- ✅ maturity-aware provider release;
- ✅ principal-win reversal + refund + terminal dispute checkpoint in one atomic transaction;
- ✅ full Job/Quote/Receipt/Billing/Earning binding checks;
- ✅ exclusive reviewer claim;
- ✅ real payout-vs-dispute and conflicting two-replica resolution tests;
- ✅ held earnings excluded from payout candidate batches.

Open follow-up, not a Phase 2C completion blocker: dispute-bound Artifact
access for reviewers must eventually allow an authorized reviewer to retrieve
only evidence actually bound to the dispute, without turning
`disputes:review` into global Artifact access.

---

## 7. Phase 3 — Provider Self-Service and Mode Readiness

**Goal:** open supply while preparing providers for stronger trust modes.

### 7.0 Already delivered

- ✅ `atos_register_capability` and `atos_update_capability`;
- ✅ provider Agent Card foundations;
- ✅ `requested_trust_modes` vs derived `supported_trust_modes`;
- ✅ `requested | pending | active | suspended | unsupported` mode-support data model;
- ✅ immutable Capability manifest/version commitment generation;
- ✅ federation-safe public IDs;
- ✅ execution-signer authorization abstraction.

Permanent Phase 3 rule:

```text
provider requested Verified support
!=
Verified is active and quotable
```

Health, transport reachability, sandbox success, provider self-assertion and
signer presence are readiness evidence only. They are not sufficient authority
to activate Verified or Native.

### 7.1 Phase 3A — Provider Adapters, Readiness Probes and Provider/Admin Surface

**Goal:** allow third-party provider endpoints to serve Managed traffic through
bounded execution adapters, validate their contracts before persistence, and
add the provider/admin control surface needed to operate them — without
creating a second execution path or prematurely activating stronger modes.

Phase 3A is broad enough that it MUST be delivered in the ordered work packages
below. They may be separate coordinated PRs, especially when `atos`,
`tos-protocol` and `tos-ai` all change. A PR may claim only the package it
actually implements. Phase 3A is complete only after all packages and the
cross-repository acceptance criteria are met.

#### 7.1.0 3A-S — Specification and binding freeze

Before adapter implementation, freeze the following semantics:

- exact CapabilityBinding / provider-endpoint contract and validation rules;
- how a committed Job resolves the exact binding frozen by its quoted Capability version;
- adapter request identity and response binding fields;
- health/readiness freshness semantics;
- sandbox certification identity/state semantics;
- exact MCP schemas and authorization scopes for the four Phase 3A provider/admin tools.

`docs/MCP.md` currently labels some of those tools/scopes as later/undefined.
Implementation MUST NOT invent the missing contract. Update the normative MCP
spec first if it is still undefined when coding starts.

Binding rules:

- `endpoint_ref` is an identifier/configuration reference, never a bearer credential;
- invocation data cannot replace or override the frozen endpoint/tool/agent binding;
- secrets remain private operator/provider configuration and are not exposed in public Capability JSON, Agent Cards, logs or commitments;
- a semantically meaningful binding change MUST create a new Capability version/manifest commitment;
- an already-issued Quote/Job MUST continue to use its frozen version/binding semantics after a Capability update;
- `eligible_trust_modes` is eligibility metadata, not activation authority.

**Acceptance:** a test changes only the provider binding on a Capability and
proves a new version/manifest is produced while an older Quote/Job continues to
resolve the old binding.

#### 7.1.1 3A-A — Adapter execution plane: HTTP, MCP and A2A

Deliver:

- HTTP provider adapter;
- MCP provider adapter;
- A2A provider adapter;
- common normalized adapter request/result/error contract;
- binding resolver from immutable Capability-version state;
- bounded timeout/cancellation, response size and concurrency behavior;
- stable request identity / duplicate/lost-response handling;
- input/output validation against the frozen Capability schema;
- production-safe outbound network policy.

**Placement rule:** the ATOS Job/economic service MUST NOT directly perform
arbitrary provider HTTP/MCP/A2A calls. ATOS owns orchestration and binding
selection; actual provider execution/probing belongs behind the existing
execution/data-plane boundary (`tos-protocol` ExecutionGateway / `tos-ai` or an
explicitly specified equivalent execution-side component). If existing code
cannot support this without a new RPC, define that RPC in `atos-spec` first.

Adapter request/result binding must include enough immutable identity to reject
substitution, at least conceptually:

```text
job/request identity
provider_id
capability_id
capability_version
binding identity/commitment
quote/trust-mode context where required
deadline
```

A response for Capability version N MUST NOT mutate or satisfy version N+1.
A provider-returned trust flag MUST NOT mutate `supported_trust_modes`.

HTTP requirements include:

- no unrestricted SSRF;
- no unsafe redirect credential forwarding;
- bounded body and headers;
- cancellation/deadline propagation;
- malformed/non-2xx handling;
- explicit remote HTTPS policy, with any private/local exceptions operator-controlled rather than invocation-controlled.

MCP tests MUST use a real in-process MCP server. A2A tests MUST use a real
in-process A2A server. HTTP tests MUST use real in-process HTTP servers plus
fault injection.

**Acceptance:** for each adapter, prove success plus malformed response,
timeout, delayed response, duplicate/replay, wrong binding, cancellation and
lost-response behavior. No lost/duplicate/delayed response may corrupt
Capability state, produce duplicate economic effects, or activate a trust
mode.

#### 7.1.2 3A-V — Capability schema validation

Deliver registration/update validation of the schema documents themselves and
runtime validation of adapter I/O against the immutable schemas used by the
Job.

Rules:

```text
Register candidate
    -> validate input_schema/output_schema
    -> validate binding
    -> persist only if all pass

Update current Capability
    -> construct complete candidate
    -> validate candidate schemas/bindings
    -> persist + version/manifest bump atomically
```

An invalid update must leave the stored Capability unchanged: version,
manifest, schemas, bindings, requested modes and supported modes.

Before outbound dispatch, request data must satisfy the frozen input schema.
Before accepting provider output into a successful Job/Receipt/settlement,
output must satisfy the frozen output schema. Schema failure is a provider or
validation failure, never a successful settlement.

Use a real, standards-compliant JSON Schema implementation consistent with the
contract. If the exact supported JSON Schema draft/feature subset is not yet
normatively specified, specify it before relying on implementation-specific
behavior.

**Acceptance:** invalid registration/update is rejected before persistence on
memory and PostgreSQL stores, and invalid provider output cannot produce a
successful settled Job.

#### 7.1.3 3A-H — Health, per-mode availability and sandbox certification

Health and certification are operational/readiness evidence, not trust-mode
activation.

Keep four questions separate:

```text
Did the provider request the mode?
Is the mode cryptographically/economically active and quotable?
Is the selected transport/binding currently available?
Has this exact Capability version/binding passed sandbox certification?
```

Health observations MUST be bound to a Capability version + binding identity
and carry freshness (`observed_at` plus a bounded validity/staleness rule).
A stale success is `unknown/stale`, not indefinitely healthy.

Health checks must be bounded in timeout and concurrency and must not modify
Capability manifest/version merely because the endpoint temporarily changed
health.

Sandbox certification MUST be durable and version/binding-bound. Minimum
state semantics must distinguish at least:

```text
pending/running
passed
failed
inconclusive or retryable uncertainty
```

A crash or lost response cannot be recorded as `passed`. Repeating the same
semantic certification identity is idempotent; changed semantics under the
same identity conflict. Updating the Capability version/binding makes older
certification evidence non-current for the new version.

Certification should exercise the actual adapter path and validate protocol
handshake, bounded execution, response shape and schema compatibility.

Critical fail-closed rule:

```text
provider requested verified/native
+ endpoint healthy
+ sandbox passed
+ signer exists

DOES NOT imply

mode_support[verified/native] = active
supported_trust_modes += verified/native
```

**Acceptance:** real PostgreSQL tests with two service/store instances prove
concurrent/restarted certification converges, stale results do not certify a
new Capability version, and health/certification alone never activate
Verified or Native.

#### 7.1.4 3A-M — Provider/Admin MCP tools

Phase 3A includes these four tools only after their exact schemas/scopes are
frozen in `docs/MCP.md`:

```text
atos_provider_jobs
atos_deliver_job
atos_request_settlement
atos_dispute_job
```

They are not ordinary consumer tools. `tools/list` visibility is derived from
current authorization plus role/resource preconditions and remains separate
from `tools/call` authorization.

Minimum security semantics:

**`atos_provider_jobs`**

- requires `provider_jobs:read` plus provider role;
- reads only Jobs belonging to the authenticated provider;
- provider identity comes from auth, never request JSON.

**`atos_deliver_job`**

- requires `provider_jobs:deliver` plus target Job/provider ownership;
- cannot override Quote trust mode, proof profile, provider, price or settlement amount;
- wrong Job/provider/capability-version delivery is rejected;
- duplicate delivery is idempotent or deterministically rejected according to the frozen Job contract;
- successful output must pass the frozen output schema before settlement.

**`atos_request_settlement`**

- requires an explicit mutation scope; a read-only settlement scope is insufficient;
- is a facade over the existing settlement/reconciliation state machine, never a second settlement engine;
- cannot choose an amount, trust mode or proof result supplied by the provider;
- may only request/retry/reconcile settlement for a Job already eligible under its immutable Quote/verified receipt/billing state;
- requires stable idempotency and produces at most one economic outcome.

**`atos_dispute_job`**

- MUST delegate to the Phase 2C dispute state machine; it must not create parallel dispute records or weaker transitions;
- exact allowed operations and scopes must be frozen in `docs/MCP.md` before implementation;
- party restrictions, exclusive reviewer claim, payout hold, maturity-aware release, atomic refund and `clawback_required` semantics remain identical to REST/Phase 2C.

Provider role must be derived from the existing provider identity/ownership
model, not a request boolean. Scope alone does not imply ownership; ownership
alone does not grant scope.

**Acceptance:** `tools/list` and `tools/call` matrices cover scope-only,
role-only, correct provider, wrong provider and revoked/changed authorization
for every tool. Settlement/dispute tools reuse the existing durable state
machines and preserve all Phase 2B/2C economic invariants.

#### 7.1.5 Phase 3A overall success criterion

Phase 3A is complete only when all of the following are true:

```text
HTTP provider adapter                         ✅
MCP provider adapter                          ✅
A2A provider adapter                          ✅
immutable binding/version semantics           ✅
input/output schema validation                ✅
provider health checks                        ✅
per-mode availability projection              ✅
sandbox certification workflow                ✅
atos_provider_jobs                            ✅
atos_deliver_job                              ✅
atos_request_settlement                       ✅
atos_dispute_job                              ✅
lost/duplicate/delayed response safety        ✅
schema-invalid-before-persistence             ✅
health/certification cannot activate modes    ✅
real PostgreSQL multi-replica tests            ✅
real-protocol HTTP/MCP/A2A tests              ✅
```

The cross-repository acceptance test must demonstrate a third-party Managed
Capability using a real provider adapter path from ATOS orchestration through
the execution boundary and back into the existing Receipt/settlement pipeline,
without bypassing Quote, receipt verification, billing or dispute semantics.

### 7.2 Phase 3B — Provider Trust Readiness

**Goal:** make readiness and signer operations production-operable without
allowing readiness signals to self-activate stronger trust modes.

Deliver:

- complete provider-facing mode-support lifecycle UX for
  `requested -> pending -> active -> suspended -> unsupported`;
- public per-mode availability alongside active `supported_trust_modes`;
- execution-signer authorize / rotate / revoke workflows;
- durable pending/reconciliation checkpoints for signer mutations;
- explicit activation authority boundaries.

Transition authority rule:

- providers may request modes;
- health/certification may create readiness evidence and pending/suspended operational states;
- providers may not set `active` directly;
- Verified/Native `active` requires the stronger trust activation authority defined by the TOS-backed path; before Phase 4 production activation exists, stronger modes remain fail-closed even if every readiness check is green.

Signer mutations are external trust-side effects and require stable action
identity, durable intent, replay-safe `tos-protocol` calls and restart
reconciliation. Rotation/revocation must never briefly advertise both an
unauthorized new signer and an unrecoverably removed old signer without a
well-defined transition.

**Success criterion:** signer rotation/revocation survives a crash at every
external-call boundary; two replicas converge on one signer state; and no
combination of provider self-assertion, health, sandbox certification or signer
registration alone can add Verified/Native to `supported_trust_modes` without
the activation authority.

### 7.3 Phase 3C — Open Task Marketplace

**Goal:** add demand-side open tasks without creating a weaker parallel
commercial contract.

An OpenTask is a marketplace demand object, not a replacement for Capability,
Quote or Job.

Required lifecycle:

```text
publish
  -> open
  -> applications/proposals
  -> exactly one accepted proposal
  -> immutable Quote/Job binding
  -> normal Job/Receipt/settlement/dispute lifecycle
```

Rules:

- task publication, application and acceptance are durable and idempotent;
- accept binds the winning provider/capability/version and creates or binds the same Quote/Job contract normal invocation uses;
- the accepted Job cannot use a provider-supplied price/trust mode that bypasses Quote policy;
- concurrent accept attempts use database uniqueness/locking to produce one winner;
- crash after winner selection but before Quote/Job binding is recoverable from durable intent;
- expiry/cancel rules are explicit and cannot strand an accepted Job;
- a losing proposal can never later create a second Job for the same accepted task.

**Success criterion:** N concurrent accept attempts from at least two
independent PostgreSQL-backed service instances yield exactly one accepted
proposal and one bound Job; restart at every accept/bind checkpoint converges
without double-binding or permanent limbo.

### 7.4 Phase 3 overall success criterion

A third-party provider can self-register once, configure an immutable execution
binding, pass schema/sandbox readiness checks, serve Managed traffic, operate
provider jobs/settlement/disputes through correctly scoped surfaces, request
stronger modes and possess the material needed for later activation — all
without changing Capability identity or self-certifying a stronger trust mode.

---

## 8. Phase 4 — Verified Mode (`atos.im` UX + TOS Guarantees)

**Goal:** ship `trust_mode=verified` as an independently verifiable production
guarantee, not merely a locally functional chain path.

Important: substantial Phase 4 foundations already exist (typed `tos-core`
interfaces, chain Authority, TaskEscrow Economic Driver, publisher sidecar,
receipt verification and real-localnet settlement), but production activation
is incomplete.

### 8.1 Phase 4A — Production identity and Capability ownership activation

Complete:

- production Agent/principal identity binding;
- production provider identity and Capability ownership resolution;
- manifest/version anchoring on the same configured TOS network;
- network/domain binding that prevents mixing references from different TOS networks;
- activation policy that only marks a Capability Verified when every required ownership/manifest checkpoint is current.

### 8.2 Phase 4B — Live signer authorization and Verified transaction path

Complete:

- live execution-signer authorization resolution/rotation/revocation;
- Quote commitment;
- enforceable TaskEscrow create/release/settle on production-shaped infrastructure;
- signed Execution Receipt verification;
- receipt/settlement proof references;
- reconciliation after lost responses/restarts;
- no fallback to Managed under the original Quote.

All components for one Verified transaction must agree on the same network,
provider, Capability version, Quote and signer authorization.

### 8.3 Phase 4C — Portable proof package and independent verifier

Define one canonical `tos_verified_v1` proof package sufficient for an
independent verifier to establish at least:

```text
provider identity / Capability ownership
manifest/version commitment
Quote/terms commitment
signer authorization at execution time
Receipt commitment and signature
settlement/refund outcome
required Proof-of-Service evidence references
network/finality/domain identity
```

Expose proof retrieval through the public ATOS surface and ship an independent
verifier library/CLI that does not trust mutable `atos.im` database state.

Proof package encoding, domain separation and test vectors must be normative in
`atos-spec` before multiple implementations depend on them.

### 8.4 Phase 4D — Full-stack and production gate

Required acceptance path:

```text
external client
 -> ATOS quote(trust_mode=verified)
 -> TOS-backed escrow
 -> tos-protocol / tos-ai execution
 -> authorized-signer Receipt
 -> TOS-backed verification + settlement
 -> public proof retrieval
 -> independent verifier
 -> VALID
```

Also prove fail-closed behavior for identity, ownership, signer, escrow,
network, receipt, proof and settlement failures.

Production readiness additionally requires multi-endpoint quorum deployment,
reviewed code-hash allowlists, production key custody/HSM/Vault policy,
monitoring, reconciliation, backup/disaster recovery and incident procedures.

**Phase 4 success criterion:** an independent verifier can validate a completed
Verified transaction end to end without trusting mutable `atos.im` state, and
failure of any required Verified checkpoint never completes the original Quote
as Managed.

---

## 9. Phase 5 — Native Resolution and Decentralized Discovery

**Goal:** activate `trust_mode=native` and remove `atos.im` as canonical
namespace/trust authority for Native supply.

Before implementation, freeze these normative primitives in `atos-spec`:

- final global Agent and Capability identifier scheme;
- registry/ownership event format and domain separation;
- globally resolvable manifest format;
- indexer ingestion/rebuild protocol;
- final `atos://agent/...` / `atos://capability/...` (or replacement) semantics;
- cross-gateway replay and signature domains.

Do not let the existing provisional URI or local database key accidentally
become the permanent federation identifier merely because code already uses it.

Implement:

- TOS-backed Capability registry/ownership events;
- independent reference indexer;
- deterministic index rebuild from canonical events;
- Native resolver library;
- Native provider endpoint resolution;
- signer authorization independent of `atos.im`;
- cross-gateway receipt/proof verification;
- complete portable `tos_native_v1` proofs.

Search ranking remains off-chain and competitive.

**Success criterion:** a Capability anchored through one compatible path can be
resolved, quoted, invoked, verified and settled through another compatible
gateway/resolver without querying the `atos.im` canonical database.

---

## 10. Phase 6 — Open Gateway Federation

**Goal:** make `atos.im` a reference gateway rather than a mandatory choke
point.

Ship:

- normative gateway feature/mode advertisement;
- gateway conformance suite;
- open reference gateway components;
- cross-gateway Native resolution and `tos_native_v1` interoperability tests;
- standardized trust/proof error semantics;
- federation-safe caching/freshness rules;
- anti-replay/domain-separation tests;
- explicit gateway-local vs globally canonical field rules;
- failover and recovery guidance.

A gateway may keep proprietary ranking, UX, risk controls, Managed billing and
enterprise policy, but may not redefine the guarantees behind standard trust
mode/profile names.

**Success criterion:** loss of `atos.im` prevents access to its Managed service
but does not prevent a compatible client/gateway from resolving, invoking,
verifying and settling Native ATOS capabilities.

---

## 11. Phase 7 — Economy and Proof Hardening

**Goal:** harden the network after real multi-provider/multi-gateway volume
exists.

Potential work:

- dispute resolver profiles and public resolver policy;
- federated/multi-resolver arbitration;
- stronger Sybil resistance and counterparty-diversity weighting;
- proof aggregation/rollups;
- privacy-preserving reputation proofs;
- provider collateral/stake policy where justified;
- enterprise attestations;
- sponsored/meta-transaction flows;
- multi-asset settlement;
- cross-region compliance controls;
- portable fraud/risk signals without exposing private payloads;
- signer-delegation policy hardening and hardware/TEE attestations where useful.

These are later hardening steps and MUST NOT block the Managed MVP or be pulled
forward into Phase 3 simply because adjacent domain fields already exist.

---

## 12. Cross-Phase Compatibility Rules

1. ✅ **One Capability identity.** Trust-mode support does not create a new Capability solely because the mode changed.
2. ✅ **One client protocol.** REST/MCP/A2A do not fork into Managed vs Web3 products.
3. ✅ **Quote resolves mode.** `auto` never survives into committed transaction state.
4. ✅ **Provider intent is not certification.** `requested_trust_modes` does not equal active `supported_trust_modes`.
5. ✅ **No silent downgrade.** Stronger trust contracts fail/requote rather than weaken.
6. ✅ **Execution remains off-chain.** Providers/`tos-ai` execute; TOS anchors trust/economic/proof facts.
7. **Economic proofs are enforceable.** A hash of a private ledger is not TOS-backed escrow/settlement.
8. ✅ **Global IDs are planned early.** Local database keys never become accidental protocol IDs.
9. ✅ **Search remains an indexer function.** Consensus does not perform semantic ranking.
10. ✅ **Proof-of-Service grows from Receipts.** Do not build a separate unrelated reputation silo.
11. ✅ **Authorized signers are first-class.** Provider root keys do not need to sign every execution.
12. ✅ **Managed Mode remains permanent.** Decentralization adds guarantees rather than forcing migration.
13. **Committed execution binding is immutable.** A later endpoint/binding update cannot reroute an old Quote/Job.
14. **Operational readiness is not trust activation.** Health/certification cannot self-activate Verified/Native.
15. **Public schemas remain stable.** Later phases activate guarantees already modeled or version them explicitly rather than silently changing meaning.

---

## 13. Recommended Build Order Inside Each Newly Activated Trust Mode

For each newly activated concrete trust mode, implement in this order:

```text
Capability eligibility
    -> readiness evidence
    -> authoritative mode activation
    -> Quote resolution
    -> binding freeze / execution routing
    -> reservation/escrow
    -> execution inheritance
    -> signer authorization
    -> Receipt generation
    -> Receipt verification
    -> settlement
    -> proof retrieval
    -> Proof-of-Service evidence
    -> cancellation/expiry/dispute paths
    -> independent verification / recovery
```

Do not declare a mode production-ready after implementing only the happy-path
settlement call.

---

## 14. Instructions for Coding Agents

When Claude Code, Codex or another coding agent is asked to implement a roadmap
phase, it must:

1. read this file, `ARCHITECTURE_V0.2.md`, and every normative document named by the target phase from current `main` before coding;
2. inspect the current implementation before proposing new domain types or duplicate state machines;
3. list the target phase's MUST/MUST NOT invariants before changing code;
4. identify any underspecified public contract and stop that portion until the spec is frozen instead of guessing;
5. preserve existing Phase 0–N regression invariants;
6. use stable idempotency identities and purpose-built atomic store operations for monetary or externally side-effecting transitions;
7. add real-protocol and real-PostgreSQL tests where required by this roadmap;
8. run the exact-head validation commands and report skipped/unrun tests honestly;
9. show `git diff --stat` and changed implementation/test/migration/schema files before claiming completion;
10. stop at the requested roadmap work package and not opportunistically implement later phases.

A coding agent's completion report is evidence to review, not proof of
completion. The implementation diff and executable acceptance tests remain the
source of truth.
