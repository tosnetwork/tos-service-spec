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
- `docs/FINANCIAL_INTEGRITY.md` — cross-cutting Managed financial integrity, reconciliation, immutable ledger and TOS anchor hardening;
- `docs/THIRD_PARTY_EXECUTION_PLANE.md` — the RPC contract and endpoint-allowlist trust model for routing third-party HTTP/MCP/A2A execution/probing behind the execution/data plane instead of the ATOS Gateway;
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

**Resolved:** an earlier revision of this document tracked a "known gap" here
(`atos`'s `internal/service/job.go` allegedly hard-failing a Job whose
Capability moved to a new version since its Quote, rather than continuing to
resolve the Quote's frozen binding). That gap no longer exists in the code —
commits `f3e6b30` ("fix(phase3a): freeze Quote binding/schema so Job creation
survives a later Capability update") and `b3a6dca` ("fix(phase3a): keep
Quote's frozen execution snapshot out of public API responses") closed it,
and both are ancestors of `origin/main` (part of the Phase 3B PR #12 history).
`internal/service/job.go`'s `submit()` no longer compares `capability.Version`
against `quote.CapabilityVersion` at all, and builds the Job's
`CapabilityVersion`/`Binding`/`InputSchema`/`OutputSchema` fields entirely
from the Quote's own frozen snapshot (job.go:156-211, with an explicit code
comment citing this section by name). `internal/service/economic_recovery.go`'s
dispatch/recovery path (`SubmitJobRequest{...}`, economic_recovery.go:565-580)
sources the same fields from the Job's own already-frozen state, never
re-fetching or re-resolving the live Capability's current bindings. This
closes the contradiction with §7.1.5's "immutable binding/version semantics"
line, which already marked this ✅.

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

The required RPC is now defined: see
[`docs/THIRD_PARTY_EXECUTION_PLANE.md`](THIRD_PARTY_EXECUTION_PLANE.md) and
`proto/atos/tos/v1/execution.proto`'s `ThirdPartyBinding` message
(`GetProviderStatusRequest`/`QuoteExecutionRequest`/`SubmitJobRequest`, added
as purely additive optional fields). That document also resolves a real
trust-model tension this spec work surfaced: `tos-ai`'s existing adapter
plugin surface (`pkg/runtime.Adapter`) is deliberately built so an invocation
payload can never select its own outbound endpoint -- the endpoint is
operator-fixed. A third-party ATOS Capability's `endpoint_ref` is
provider-chosen, effectively business data. Naively threading it into
`tos-ai`'s existing worker process would invert that invariant. The
resolution is a worker-operator-curated endpoint allowlist: an invocation may
only *reference* a `(transport, endpoint_ref, capability_id)` the operator
already approved, never introduce a new one. This is normative for whatever
implements the private `tos-protocol` ↔ `tos-ai` extension, even though that
wire format itself remains `tos-protocol`'s own implementation concern (same
status as the existing `WorkerService` message shapes).

This closes both the **specification** and **implementation** halves of the
placement rule. `tos-protocol` routes `ThirdPartyBinding` requests to the
execution/data plane (`ThirdPartyExecutionService`) instead of failing them;
`tos-ai` performs the allowlisted dial (`internal/thirdparty`, operator
endpoint allowlist enforced fail-closed before any outbound call); `atos`
consumes this instead of dialing locally (`dispatch.WithRemoteThirdPartyExecution`,
required — not merely available — in production via
`ATOS_REMOTE_THIRD_PARTY_EXECUTION=true`, enforced by `internal/config.Validate()`).
Landed end-to-end across `tos-protocol#14`, `tos-ai#3` and `atos#8`/`#9`
(merged `tos-protocol@cf64ae9`, `tos-ai@50fd5d7`, `atos@7196b60`), including two
independent post-merge review rounds that fixed: unbounded MCP/A2A response
reads, a wildcard-`capability_version` allowlist lookup bug, quoted
`max_output_bytes` not being enforced on the third-party output path, and a
`capability_version` field missing from `GetProviderStatusRequest` that
silently under-specified every remote health/certification probe.

**Resolved:** `HealthService`/`CertificationService` in `atos` gained an
optional remote-probing path (`WithRemoteProber`, consuming the same
`ThirdPartyExecutionService` boundary as Job execution — see §7.1.3 below) as
part of this work. At the time this note was first written, neither service
had a real production call site. That gap has since been closed on both
sides: `HealthService.CheckCapability` runs via `GET /capabilities/{id}`'s
readiness projection (`GetCapabilityWithReadiness`) and via
`health.RunReconciler`'s periodic sweep, both wired in `cmd/api/main.go`;
`CertificationService.Open` gained its own entry point in `atos@ad2dbf4`
(`POST /v1/capabilities/{id}/certification` and the matching MCP tools,
gated by new `certifications:read`/`write` scopes) — see §7.1.3's "Known
gap" note below for the detail on why that one lagged behind.

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

**Resolved:** `atos`'s `HealthService`/`CertificationService` (including the
optional remote-probing path added alongside §7.1.1's execution-plane
placement work) had zero production call sites for a period spanning Phase
3A/3B. `HealthService` was closed out first, reachable via `GET
/capabilities/{id}`'s readiness projection and `health.RunReconciler`'s
periodic sweep. `CertificationService.Open` — the sandbox certification
workflow itself — was the last piece still unreachable: fully implemented
with full test coverage since Phase 3A, but no REST route, no MCP tool, and
no reconciler ever called it, discovered as a genuine gap during a Phase
3B/3C completeness audit rather than by any review of new work. Closed in
`atos-spec@54a406f` (spec: `docs/API.md` §2.3, `docs/MCP.md`) and
`atos@ad2dbf4` (implementation: `POST`/`GET
/v1/capabilities/{id}/certification`, `atos_open_certification`/
`atos_get_certification_status` MCP tools, new `certifications:read`/`write`
scopes mirroring `execution_signers:read`/`write`'s provider-role,
ownership-checked pattern). See §7.1.1's "Resolved" note above for
`HealthService`'s side of this.

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
sandbox certification workflow                ✅ [1]
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

[1] This checkmark reflects `CertificationService.Open`'s logic and test
coverage, which were genuinely complete since Phase 3A. It was only later,
during a Phase 3B/3C completeness audit, that the entry point itself was
found unreachable in any real deployment (no REST route, no MCP tool, no
reconciler) — closed in `atos-spec@54a406f`/`atos@ad2dbf4`; see §7.1.3's
"Resolved" note above.

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

#### 7.2.0 Mode-support transition matrix (normative)

`domain.ModeSupportStatus` already defines exactly these five states
(`requested`, `pending`, `active`, `suspended`, `unsupported`); Phase 3A only
ever produced `active`/`pending`/`unsupported` (Managed goes straight to
`active`, a requested Verified/Native goes straight to `pending`, `requested`
itself was defined but never assigned). Phase 3B gives `requested` a real,
distinct meaning and freezes the complete legal transition graph:

```text
requested  = provider has asked for this mode; no readiness evidence
             (health/certification) has been recorded yet for the
             Capability's CURRENT version.
pending    = at least one readiness evidence cycle has run for the current
             version, but the activation authority has not granted active.
active     = the activation authority has granted this mode active.
suspended  = was active; readiness evidence that active depended on
             (health, certification, or signer authorization) is no longer
             valid for the current version. Underlying historical trust
             evidence (e.g. a still-recorded past certification) is not
             destroyed, only no longer treated as current.
unsupported = not requested, or the provider stopped requesting it.
```

Legal transitions and their sole authority:

| From | To | Trigger | Authority |
|---|---|---|---|
| `unsupported` | `requested` | provider adds the mode to `requested_trust_modes` (existing `PATCH /capabilities/{id}` contract, unchanged) | **Provider** |
| `requested` | `pending` | first readiness evidence (health check or certification attempt) recorded for the Capability's current version | **Readiness pipeline** (system) |
| `requested` | `unsupported` | provider removes the mode from `requested_trust_modes` | **Provider** |
| `pending` | `unsupported` | provider removes the mode from `requested_trust_modes` | **Provider** |
| `pending` | `active` | activation authority evaluates and grants | **Activation authority** |
| `active` | `suspended` | readiness evidence this activation depended on becomes invalid for the current version | **Readiness pipeline** (system) |
| `active` | `unsupported` | provider removes the mode from `requested_trust_modes` | **Provider** |
| `suspended` | `active` | activation authority re-evaluates and grants (readiness restored) | **Activation authority** |
| `suspended` | `unsupported` | provider removes the mode from `requested_trust_modes` | **Provider** |

Any other transition (in particular anything driven directly by a
provider-supplied `{"status":"active"}` or equivalent) MUST be rejected, not
silently normalized. Managed is a permanent exception to this whole table:
it has exactly two states (`unsupported`/`active`, no `pending`/`suspended`),
requires no signer/certification evidence, and Phase 3B MUST NOT change its
existing unconditional-`active`-on-request behavior.

A Capability version bump resets per-version readiness evidence (health,
certification, and -- since it is itself version-scoped, see
`ExecutionSignerAuthorizationInput.capability_version` below -- signer
authorization currency) for that mode, per the existing binding-freeze
precedent (§7.1.0). It does NOT automatically demote `active`/`suspended`
back to `requested` purely because the version changed; readiness re-checks
against the new version drive any resulting `suspended` transition through
the normal rule above, the same way health/certification staleness already
does. Historical evidence tied to the old version remains auditable and is
never mutated.

#### 7.2.1 ActivationAuthority (normative interface, not just an internal detail)

Stronger-mode activation MUST be delegated to a single, explicit interface
-- never inlined boolean logic like `if healthy && certified && signerExists`.
Conceptually:

```text
ActivationAuthority.Evaluate(provider_id, capability_id, capability_version, mode)
    -> (granted: bool, reason_code: string)
```

Two implementations are in scope for Phase 3B:

- **Production** (`atos_env=production` or any deployment without a
  configured Phase 4 authority): fail-closed for `verified`/`native` --
  always returns `granted=false` with a stable reason code (e.g.
  `ACTIVATION_AUTHORITY_UNAVAILABLE`). Managed never goes through this
  interface at all.
- **Test-only**: proves the positive path (§7.2's own success criterion
  requires demonstrating `pending` + readiness + signer authorization +
  authoritative grant `= active`, and that `supported_trust_modes` is
  correctly derived from it). MUST NOT be reachable from production
  configuration.

Phase 4 later supplies the real TOS-backed authority behind the same
interface; Phase 3B does not implement fake on-chain activation to make this
interface non-trivial.

✅ **Status: the full §7.2 slice below (§7.2.0 through §7.2.4) is implemented
and merged.** `atos` PR [#12](https://github.com/tosnetwork/atos/pull/12)
(branch `agent/phase3b-mode-activation`, 11 commits, merged as `b7d2be2`)
went through three independent post-hoc review rounds before merge, each
finding real, previously-unnoticed correctness gaps that were fixed and
re-verified rather than deferred -- see below for what each round found.
Per this document's own verification standard (see the top of this file),
this mark reflects that history, not a single clean pass.

What the PR contains: `domain.ModeSupport.AdvanceToPending`/`.Suspend`/
`.Activate` implement the full transition graph above; `domain.ActivationAuthority`
+ `service.FailClosedActivationAuthority` (the only production-wired
implementation, always denies verified/native with
`ACTIVATION_AUTHORITY_UNAVAILABLE`); `HealthService.CheckCapability` and
`CertificationService.Open` drive `requested -> pending` and `active ->
suspended` automatically, and are now constructed and periodically swept in
`cmd/api/main.go` (closing the §7.1.1/§7.1.3 "known gap" this document
previously recorded). §7.2.2's durable execution-signer journal
(`domain.ExecutionSignerOperation`, migration `011_phase3b_execution_signer.sql`,
`service.ExecutionSignerService`) implements the full checkpoint sequence for
authorize/rotate/revoke with a startup+periodic reconciler, reusing the
existing `OpenCertification`-style idempotent-create pattern rather than a
new digest model. §7.2.3's public surface exists on both REST
(`POST /v1/capabilities/{id}/execution-signer/{authorize,rotate,revoke}`,
`GET .../execution-signer`) and MCP (`atos_authorize_execution_signer` /
`atos_rotate_execution_signer` / `atos_revoke_execution_signer` /
`atos_get_execution_signer_status`), plus the `readiness` projection
extension on the existing Capability read response, with `signer_authorized`
reflecting real signer state (not a placeholder). §7.2.4's success criterion
has direct test coverage: an 18-step end-to-end acceptance test against real
Postgres (rotation crashing mid-flight, two simulated restarts, reconciler
convergence, a lost revoke response, and a final assertion that verified/
native never entered `supported_trust_modes`), a two-independent-Postgres-
replicas-race test for the reconciler (5x with `-race`, clean), and a
positive activation-authority test proving the granted-path derives
`supported_trust_modes` correctly. A genuine version-scoping bug was found
and fixed during this work: execution-signer currency was originally
capability-scoped only, not capability-*version*-scoped, so a signer
authorized for version N incorrectly stayed "current" after a version bump
to N+1; `CurrentSigner` now checks both.

`tos-protocol`'s own signer RPCs were audited separately on `tos-protocol` PR
[#15](https://github.com/tosnetwork/tos-protocol/pull/15) (merged, HEAD
`fd446c1`). **That audit's initial conclusion -- "already idempotent and
version-bound, no RPC/proto changes needed" -- was wrong**, caught by an
independent second review before merge: 5 of the 12 `Authority.Commit` call
sites in `tos-protocol` (`RevokeExecutionSigner`, `CreateEscrow`,
`ReleaseEscrow`, `SettleJob`, `CommitCapabilityManifest`) hashed the entire
request message -- including `RequestContext.request_id`/`trace_id`, which a
well-behaved caller legitimately regenerates on every retry of the same
logical operation -- into the commitment digest that `Authority.Commit`'s
`(kind, id, digest)` idempotency is keyed on. A retry after the caller never
received the first attempt's response therefore minted a second, divergent
commitment instead of converging on the original one, exactly the failure
mode a retry is supposed to recover through. Fixed by excluding
transport-scoped `RequestContext` fields from the digest before it reaches
`Authority.Commit` (`withoutTransportContext`, `pkg/atosrpc/mutation.go`);
`Authority.Commit`'s idempotency contract (same `(kind, id, digest)` must
always return the same `NetworkReference`) is now stated explicitly on the
interface and backed by a conformance test run against every `Authority`
implementation, plus retry-convergence tests for all five previously-broken
call sites and a true lost-response test (the underlying `Commit` actually
succeeds and produces a real reference; the caller never sees it; a retry
must land on that exact reference). Confirmed against what is actually live
today: `atos_env=production`'s bundled `LocalAuthority` is a pure, stateless
function of `(kind, id, digest)`, so this bug had zero real-world blast
radius yet -- it becomes load-bearing the moment a real `ActionPublisher` /
`chainAuthority` goes live for Verified mode, which is why it was fixed now
rather than deferred. The same PR also fixed two narrower gaps in
`AuthorizeExecutionSigner`/`RevokeExecutionSigner`: the business-level dedup
check only compared `authorization_id` + `signer_public_key` (silently
accepting a changed validity window or algorithm as "the same request"; now
a full content-digest comparison, mirroring `CommitQuote`'s existing
pattern), and `authorization_id` was never enforced unique across different
`signer_id`s, so `RevokeExecutionSigner`'s full-bucket scan for the first
cursor match could revoke the wrong one of two signers sharing an ID (new
secondary index makes `Authorize` reject the reuse and `Revoke` an O(1)
lookup).

That same second review then re-examined `atos` PR #12 itself (round 1 of
three on this PR) and found five more gaps in the `atos`-side journal design
this section describes, all confirmed with tests that fail without the fix
and fixed in commit `7328dd6`:

- **P0**: two concurrent `Rotate` calls on different idempotency keys for
  the same capability both read the same old signer as current before
  either persists an operation that would change it, and could both
  independently authorize a new signer and complete -- two
  valid-at-`tos-protocol` signers, only one ever visible through
  `CurrentSigner`, the other permanently orphaned. Locking only the
  read-then-open sequence per `(capability_id, capability_version)` is NOT
  sufficient on its own -- verified empirically: a deterministic
  concurrency test (forcing genuine overlap via a blocking fake `Core`
  rather than relying on goroutine-scheduling luck) still reproduced the
  bug with that lock alone, since it only prevents two callers reading at
  the exact same instant, not in quick succession before the first reaches
  `completed`. The actual fix adds a second invariant inside the same
  lock: reject opening a new operation while ANY non-terminal operation
  already exists for that capability version
  (`domain.ErrSignerOperationInProgress`, retryable). New store method
  `OpenSignerOperationForCapability` (postgres + memory) replaces the
  separate `CurrentSigner`-then-`OpenSignerOperation` call pair in
  `Revoke`/`Rotate` (`Authorize` was unaffected -- it never reads
  `CurrentSigner`).
- `Revoke`/`Rotate` read `CurrentSigner` before checking for an existing
  operation, so a retry after the original call already **completed** saw
  whatever is current *now* (nothing, for `Revoke`; the new signer, for
  `Rotate`) instead of the value the original call actually opened the
  operation with -- `Revoke` returned `NotFound`, `Rotate`'s own
  content-hash conflict-detection fired on `Old*` fields the caller never
  supplied. Fixed by checking `SignerOperationByIdempotencyKey` first and
  resuming the existing operation when the caller-controlled stable
  fields match -- which also fixes REST/MCP's omitted-validity-window
  default (`time.Now()` recomputed on every delivery when `valid_from`/
  `valid_until` are omitted) spuriously conflicting on a plain retry.
- `LatestCompletedSignerOperationByCapability` now filters
  `capability_version` inside the query itself, not after the fact in Go:
  a stuck v1 operation that a reconciler only finishes recovering AFTER a
  v2 signer already completed can have a later `updated_at` than v2's own
  completed operation, masking the real current signer behind the wrong
  version's row and reporting no current signer at all.
- `advance()` now takes an `expectedFrom` checkpoint and no-ops on
  mismatch instead of unconditionally overwriting -- `UpdateSignerOperation`'s
  per-row lock already made each individual `advance` call atomic, but
  nothing stopped a stale-snapshot caller from dragging an operation
  another driver had already legitimately advanced further back down.
- `signerOperationContentHash` (postgres + memory) now includes
  `RevocationReasonCode`, which is forwarded verbatim into
  `tos-protocol`'s own commitment digest and must be identity content like
  every other caller-supplied field.

**Round 2** re-pulled and re-reviewed `7328dd6` specifically and found the
round-1 fix had itself left one more P0 and two P1s, fixed in `ab34483`:

- **P0**: `Authorize` was not routed through `OpenSignerOperationForCapability`
  at all -- it still called the plain `OpenSignerOperation`, and never
  checked whether a current signer already existed despite its own doc
  comment describing it as authorizing only the "first" signer. Two
  concurrent `Authorize` calls on different idempotency keys for the same
  capability could each open and complete independently -- the identical
  orphaned-signer shape round 1 fixed for `Rotate`, just missed for
  `Authorize`. Fixed by routing `Authorize` through
  `OpenSignerOperationForCapability` too, rejecting when a signer is
  already current (directs the caller to `Rotate` instead); verified with
  the same deterministic blocking-core concurrency test technique used for
  `Rotate`.
- Round 1's validity-explicitness fix (comparing `valid_from`/`valid_until`
  only when the CURRENT request explicitly supplies them) overcorrected: an
  explicit, deliberate validity change under a reused idempotency key was
  also silently ignored instead of conflicting, since the caller had no way
  to signal "I changed this on purpose" versus "the server defaulted it
  again." Partially fixed here by comparing whenever the CURRENT request is
  explicit (closed in round 3 below, which found this was still
  asymmetric).
- A genuine, `go test -race`-confirmed data race through PRODUCTION code
  (not a test fixture): `RecordReadinessEvidence`'s `AdvanceToPending` call
  mutated a `Capability`'s `ModeSupport` map in place while
  `CapabilityService.Get` (via `ActiveModes`) concurrently read the same
  map -- the memory store's `Get` returns a `Capability` by value, but Go
  copies map fields by reference, so the returned copy's `ModeSupport` was
  still the store's own live map. Fixed at the root: `AdvanceToPending`/
  `Suspend`/`Activate` are now copy-on-write, never mutating the receiver.
  This exposed a test (`TestHealthService_CheckCapability_NeverMutatesModeSupport`)
  that had been vacuously passing for the identical reason -- a `before`
  snapshot secretly aliasing `after` -- renamed and fixed to assert the
  real invariant (never directly activates Verified/Native) instead of a
  stricter one the design was never meant to satisfy. A second, non-production
  test-only race noted in passing (`fakeThirdPartyHealthProber`'s call
  counter) was fixed too, so the full suite runs `-race` clean with zero
  exclusions.

**Round 3** re-pulled `ab34483` and found round 2's validity-explicitness
fix was still asymmetric -- fixed in `bc03561`, the PR's final commit:

- **P2**: the comparison only checked "if the CURRENT request is explicit,
  values must match," so a field explicitly supplied on the FIRST call and
  then omitted on a same-idempotency-key retry had its comparison skipped
  entirely and silently resumed the original operation -- the one
  remaining case where "different content under a reused key" didn't
  conflict. Fixed by persisting `NewValidFromExplicit`/`NewValidUntilExplicit`
  on `domain.ExecutionSignerOperation` itself (new columns on migration
  `011`, which only existed within this unmerged PR so amended in place
  rather than adding `012`) and comparing symmetrically:
  `existing.NewValidFromExplicit == in.ValidFromExplicit && (!explicit ||
  values match)`. All four explicit/omitted combinations now behave
  correctly; new tests for both `Authorize` and `Rotate` cover the closed
  gap directly.

All three rounds of verification on `atos` (and the `tos-protocol` review
above) used a fresh local Postgres (`gofmt`, `go vet`, full test suite with
`-race`, including the deterministic concurrency and lost-response tests)
rather than a shared long-lived dev database, to avoid the
historical-dirty-data false failures that database is known to produce for
unrelated tests. The final `-race` run before merge covered every package
with zero skips or exclusions.

Both remaining gaps this section used to track here have since been closed:

- **Admin-triggered `EvaluateActivation`**: `CapabilityService.EvaluateActivation`
  had full service-layer test coverage since this section's original work but
  zero production callers -- no REST route, no MCP tool, and
  `cmd/api/main.go` never even constructed a `domain.ActivationAuthority`.
  Contract frozen in `docs/API.md` §2.2 / `docs/MCP.md` §4.3/§8
  (`tosnetwork/atos-spec#3`) and implemented in `tosnetwork/atos#14`: new
  admin-only, explicit-grant-only scope `activation:evaluate` (deliberately
  no ownership precondition -- this is an activation-authority-side
  operation, not a provider one), `POST
  /v1/capabilities/{id}/activation/evaluate`, MCP tool
  `atos_evaluate_activation`, and `cmd/api/main.go` now wires
  `service.FailClosedActivationAuthority` into both servers. `granted:false`
  is a normal `200`/`isError:false` outcome, matching
  `EvaluateActivation`'s own doc comment.
- **"Real ConnectRPC tos-protocol, not only a Go-interface mock"**: rebuilding
  the full §29 scenario against a live server was the wrong scope -- it would
  have duplicated coverage `tos-protocol#15` already independently provides
  for the mock-based scenario's business logic (see
  `phase3b_e2e_acceptance_test.go`'s own doc comment for that reasoning,
  still valid). The actually-untested slice was narrower:
  `tosprotocol.Client`'s `AuthorizeExecutionSigner`/`RevokeExecutionSigner`/
  `ResolveExecutionSignerAuthorization` had never been exercised against a
  real server, even though `integration_test.go`'s existing harness already
  stands up a real `TrustService` (just never calls it). Closed in
  `tosnetwork/atos#15`: real-in-process-server coverage for all three signer
  RPCs (`internal/adapters/tosprotocol/signer_integration_test.go`), plus one
  authorize -> rotate -> revoke pass through `ExecutionSignerService`'s real
  durable checkpoint journal against a real `tosprotocol.Client` and real
  Postgres instead of `toscoremock`
  (`internal/service/execution_signer_real_rpc_postgres_test.go`). Writing
  real assertions caught a stale `toscore.Core` doc comment in the same PR
  (claimed `created`/`revoked` are `false` on an idempotent replay;
  verified `RevokeExecutionSigner` has no `revoked=false` path once a signer
  has ever been revoked, and a literal retry replays the original
  `created=true` response verbatim) -- fixed to match verified behavior.

Independent review of `atos#14` before merge found two further real P1s,
both fixed in the same PR: the new `activation:evaluate` scope could be
requested and approved through the same self-service Device Authorization
flow as any ordinary scope (no code-level distinction between "admin" and
"ordinary" scopes existed anywhere) -- closed with a second operator
secret (`ATOS_ADMIN_APPROVAL_TOKEN`) additionally required to approve a
grant carrying an admin scope; and `EvaluateActivation`'s
`Get`-then-`Put` was a systemic pattern shared by every `CapabilityService`
mutation (not just this one), already racing against the production
health/certification reconciler today -- closed by adding a real CAS
primitive (`store.Capabilities.UpdateCapability`, mirroring the
pre-existing `UpdateJob` pattern) and migrating all four affected
mutations to it, which also surfaced and fixed a live-map-mutation bug
(`EvaluateActivation`'s denial branch bypassed `ModeSupport`'s
copy-on-write helper) of the exact class Phase 3B's own round-2 review had
already fixed elsewhere. A separate review of `docs/API.md` §2.2 also
found the endpoint lacked idempotency protection (a lost response
followed by a retry would either re-consult the authority or fail as an
illegal source state); closed by adding the same `Reserve`/`Finish`
pattern `Register`/`Update` already use, scoped by the calling admin's own
identity rather than the target capability.

`atos-spec#3`/`#4` merged as `d98c40f`/`d681769`; `atos#14`/`#15` merged
as `62a5fea`/`25bb98f`. Merging `#14` after `#13` (Phase 3C, §7.3) had
already landed produced a real conflict -- both PRs added fields to the
same shared structs (`auth.go`'s scope block, `httpapi.Server`/`mcp.Server`,
`cmd/api/main.go`'s wiring) -- resolved by keeping both sides' additions
and re-running the full suite before completing the merge. That same
full-suite run against a fresh Postgres instance then caught one more real
bug: `TestPhase3B_EndToEndProviderTrustReadinessAcceptance` used a
hardcoded idempotency key for its (newly idempotency-protected)
`EvaluateActivation` call while the target capability ID is randomized
per run, so a second run against the same persistent database collided
with the first run's durable idempotency record; fixed by suffixing the
key with the same per-run identifier every other idempotency key in that
test already uses (`dd1d7cb`, pushed directly to `main` after `#14`
merged).

§32's
Receipt-verification requirement ("use signer-authorization semantics
applicable to the relevant execution time/version, not simply whatever
signer is current now") was checked, not found to be a gap:
`toscore.Core.VerifyExecutionReceipt` already resolves authorization via
`ResolveExecutionSignerAuthorization(..., receipt.CapabilityVersion,
receipt.ExecutionSignerID, receipt.CompletedAt)` -- the receipt's own frozen
execution-time identity and timestamp, never "whatever is current now". This
predates Phase 3B and needed no change.

#### 7.2.2 Execution-signer operations (normative)

`tos-protocol`'s `TrustService.AuthorizeExecutionSigner` /
`RevokeExecutionSigner` / `ResolveExecutionSignerAuthorization` (this
repository's `proto/atos/tos/v1/trust.proto`, already implemented) are
reused unchanged -- they are already idempotent (shared `atomicMutation`
canonicalized-digest machinery, same as `CommitQuote`) and already
version-bound (`ExecutionSignerAuthorizationInput.capability_version`). Phase
3B does not add a `RotateExecutionSigner` RPC: rotation is durable `atos`-side
orchestration of `Authorize` + `Revoke`, because the existing two RPCs are
already sufficient and atomic individually -- only the multi-step sequencing
between them needs a new durable checkpoint model, entirely on the `atos`
side.

Rotation is NEVER `revoke old` -> `authorize new`. The frozen sequence and
its durable checkpoints:

```text
intent_persisted
    -> new_authorization_pending
    -> new_authorized
    -> cutover_pending
    -> old_revocation_pending
    -> old_revoked
    -> completed
```

plus a `reconciling` checkpoint for any step whose remote outcome is
uncertain (RPC response lost, process crashed mid-step). The old signer
remains authoritative and ATOS MUST NOT advertise the new signer as current
until `new_authorized` is durably reached; ATOS MUST NOT irrecoverably
discard the old signer's local record before `new_authorized`. A crash at
any checkpoint boundary must converge to the correct next step on restart,
never silently skip a step.

Plain `authorize` and plain `revoke` (not part of a rotation) use the
relevant subset of the same checkpoint model (`intent_persisted` ->
`new_authorization_pending`/`old_revocation_pending` -> `new_authorized`/
`old_revoked` -> `completed`).

An RPC timeout or lost response is never treated as a definitive outcome --
the operation stays `reconciling` until a subsequent attempt (retry or
reconciler) observes a deterministic result. `tos-protocol` itself has no
async/pending concept for these RPCs (confirmed: every signer RPC there is
synchronous, atomic-or-nothing); all crash recovery is `atos`'s
responsibility, exactly like the existing Managed economic reconciler.

#### 7.2.3 Public surface (normative)

New REST/MCP surface, following this repository's existing conventions
(`docs/API.md` / `docs/MCP.md` own the exact schemas; this section freezes
only the shape and authorization rule):

- Per-mode availability/readiness projection is exposed as an extension of
  the existing `mode_support` object on the Capability read response
  (`GET /capabilities/{id}`, `atos_get_capability`) -- not a new endpoint --
  reusing `domain.ModeAvailability` per §7.1.3, extended with the signer/
  activation-authority dimensions §7.2.1/§7.2.2 add. Public: no
  authentication-scoped secrets, callable by any authenticated consumer
  (existing `capabilities:read` scope), never exposes endpoint credentials
  or signer key material.
- Execution-signer authorize/rotate/revoke/status are new provider/admin-only
  operations (new scopes `execution_signers:read` / `execution_signers:write`,
  following the existing `provider_jobs:read`/`provider_jobs:deliver` naming
  convention), REST under `/v1/capabilities/{id}/execution-signer` and MCP
  tools `atos_authorize_execution_signer` / `atos_rotate_execution_signer` /
  `atos_revoke_execution_signer` / `atos_get_execution_signer_status`.
  Ownership is enforced identically to every existing provider mutation
  (`internal/service/capability.go`'s `ProviderID != requestingProviderID`
  pattern): provider identity comes only from the authenticated principal,
  never from request JSON. Idempotency reuses the existing
  `Reserve`/`Finish`/`Release` + canonical-request-digest primitive
  (`internal/store`), the same one every other provider mutation already
  uses -- not a new digest model.
- Per §7.1.4's rule (and the ordinary-tool-list-compactness rule below),
  these four tools are visible only to a caller holding the relevant scope
  and are never added to the ordinary nine-tool consumer surface;
  `tools/call` re-authorizes independently of `tools/list` visibility,
  exactly like the existing four Phase 3A provider/admin tools already do.

Signer public/private key handling: the public API accepts only a signer
public key and signer ID on authorize; there is no operation that accepts or
returns a private key; no response, log, or observability field may contain
raw key material.

#### 7.2.4 Success criterion

signer rotation/revocation survives a crash at every external-call boundary;
two replicas converge on one signer state; and no combination of provider
self-assertion, health, sandbox certification or signer registration alone
can add Verified/Native to `supported_trust_modes` without the activation
authority.

### 7.3 Phase 3C — Open Task Marketplace

**Goal:** add demand-side open tasks without creating a weaker parallel
commercial contract.

✅ **Status: complete and merged.** `atos` PR [#13](https://github.com/tosnetwork/atos/pull/13)
(branch `agent/phase3c-open-task-marketplace`, merged `1a98aeb`) went
through five independent post-hoc review rounds before merge, each finding
real, verified issues that were fixed and re-verified rather than
deferred -- per this document's own verification standard, this mark
reflects that full history, not a single clean pass.

**Round 1** (manual review): 3 P0 + 3 P1 + 1 P2 found and fixed --
`OpenAcceptanceOperation` and Cancel locked different advisory-lock keys
(zero mutual exclusion); operation-Completed/Failed and the OpenTask
projection were two separate commits (a crash between them could strand a
task permanently, since Completed/Failed are excluded from the stale-sweep
query) -- closed with atomic `CompleteAcceptance`/`FailAcceptance` store
methods; a resumed/reconciler-driven Quote-creation call never checked
whether the Capability version had drifted since the operation froze it --
closed with `CreateQuoteInput.ExpectedCapabilityVersion`; `Withdraw`'s
pre-check raced `Accept` with no shared lock; `Publish`/`Propose` validated
live state *before* the idempotency-replay check, so a legitimate retry
could fail on business state instead of replaying its original result;
MCP's `atos_search_open_tasks` forwarded an omitted `limit` as literal `0`,
which the in-memory store treats as unlimited and Postgres treats as zero
rows; `OpenTaskProposal.Public()` leaked `ProposedPrice`. A self-dealing
gap (neither `Propose` nor `Accept` checked the acting identity differed
from the task owner) was also found and closed in the same round.

**Round 2** (independent review of the round-1 fix): the round-1 fix
itself introduced a genuine, reproducible deadlock -- `OpenAcceptanceOperation`
locked task-then-proposal while the new `WithdrawOpenTaskProposal` locked
proposal-then-task, confirmed via 30x concurrent runs against real
Postgres with `deadlock_timeout`/`log_lock_waits` tuned and the server log
grepped directly rather than trusting Go-level pass/fail -- closed by
giving `WithdrawOpenTaskProposal` a lock-free preview read (safe, since
`TaskID` is immutable) purely to learn which task lock to acquire first,
enforcing task-before-proposal ordering everywhere. Also found: the
idempotency `Reserve`/`Release` pattern's hard-delete-on-abandoned-reservation
behavior meant a later, genuinely different request under a reused key
could silently receive an earlier abandoned attempt's committed result --
closed with content-hash re-validation on the crash-recovery replay path
for `Publish`/`Propose`/`Quote.Create`.

**Round 3**: re-verified round 2's fixes using the same server-log-grepping
methodology (still clean); found the self-dealing regression test never
actually exercised the self-dealing guard (it used an identity that only
ever hit the pre-existing ownership check) -- fixed the test to bypass
`Propose`'s own self-dealing guard directly via `PutOpenTaskProposal` so
`Accept`'s guard is what's actually under test; found
`UpdateAcceptanceOperation`'s documented "MUST NOT set a terminal
checkpoint" contract had no runtime enforcement in either store --
added it.

**Round 4**: the round-3 enforcement was itself a real P1 regression --
it rejected *any* attempt to write a terminal checkpoint without checking
whether the *current* checkpoint was already terminal, which broke
`advanceAcceptance`'s legitimate CAS no-op branch (a stale worker
converging after a different worker already completed/failed the same
operation) and was simultaneously too permissive (never checked whether
an already-terminal operation was being revived). Fixed by checking
`current.Checkpoint.Terminal()` first and, if true, returning the stored
value unconditionally without ever inspecting `next`.

**Round 5**: found two more real, previously unaddressed issues from an
automated review that predated all four rounds above --
`ListPublicOpenTasks` applied `LIMIT` before filtering lazily-expired
rows, so a run of newest-but-expired tasks could consume the entire limit
window and hide older tasks that are still genuinely open (fixed by
pushing the expiry filter into the store query itself); and
`PutOpenTaskProposal` was a plain unconditional insert with no lock and no
task-state check, so a concurrent `Accept`/`Cancel` could commit between
`Propose`'s live-state check and the insert, landing a proposal against a
task that was already closed (fixed with a new `CreateOpenTaskProposal`
store method sharing `OpenAcceptanceOperation`'s lock discipline). A third
finding (accept/withdraw lock order) was already fixed in round 2 and
needed no change.

All five rounds used a freshly created Postgres 16 instance for final
verification (not a shared long-lived database) after this session
independently diagnosed and confirmed two apparent test failures during
the process were pure container-reuse artifacts (accumulated rows from
many manual runs exceeding a test's own `LIMIT`/count assumptions), not
product bugs -- confirmed via `git stash` bisection and fresh-container
reruns.

An OpenTask is a marketplace demand object, not a replacement for Capability,
Quote or Job.

#### 7.3.1 Product publishing surface and marketplace entry points

Phase 3C has two first-class demand-entry surfaces and they MUST remain one
marketplace, not separate human and agent products:

```text
Human user
    -> atos.im/tasks/new
    -> OpenTask

AI Agent
    -> ATOS REST / MCP / A2A
    -> OpenTask
```

The public web product owns the human-facing task marketplace:

```text
atos.im/tasks
= browse/search open demand

atos.im/tasks/new
= publish a task through a human-facing form

atos.im/tasks/{task_id}
= task detail, proposals and winner-selection UX
```

The human publishing form should express the same canonical OpenTask semantics
as the programmatic interfaces. At minimum the product should be able to
capture a task goal/description, input or artifact references, budget/price
constraints, deadline/expiry, requested trust requirements and winner-selection
preference where supported by the frozen OpenTask contract. The web layer MUST
NOT invent a second task model or bypass the same authorization, idempotency,
Quote and Job rules used by agents.

Agents publish programmatically through the canonical ATOS protocol surface.
The intended product-level operations are conceptually:

```text
REST   -> publish/search/read/propose/accept OpenTask operations
MCP    -> atos_publish_task / atos_search_tasks / atos_submit_proposal
A2A    -> equivalent OpenTask publication/discovery/proposal mapping
```

Exact route/tool names remain owned by `docs/API.md`, `docs/MCP.md` and the A2A
contract; the Roadmap defines the product responsibility rather than silently
renaming an already-frozen public operation. An Agent MUST NOT need to know a
Capability ID before publishing demand. It may publish the goal, budget,
deadline, inputs and trust requirements first; ATOS discovery/matching and
Provider proposals resolve suitable Capability/provider candidates afterward.

This creates an intentional two-sided product model:

```text
atos.im/capabilities
= supply-driven discovery
= requester/Agent already knows what service capability it wants
= requester finds a Provider

atos.im/tasks
= demand-driven marketplace
= requester knows the outcome/work it wants, not necessarily the Capability
= Providers find the requester and compete/propose
```

Both paths MUST converge on the same commercial contract after selection:

```text
Human / Agent publishes OpenTask
        -> Providers discover demand
        -> proposals/applications
        -> requester selects exactly one winner
        -> normal immutable Quote
        -> normal Job
        -> Execution Receipt
        -> settlement / dispute lifecycle
```

Phase 3C therefore establishes ATOS as an **AI Work Marketplace**, combining
Capability discovery (supply-driven) with OpenTask publication (demand-driven),
without creating a weaker parallel transaction path.

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

✅ **Status: complete.** §7.1 (3A), §7.2 (3B) and §7.3 (3C) are all merged.

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

## 11. Phase 7 — Economy, Financial Integrity and Proof Hardening

**Goal:** harden the network and the `atos.im` Managed financial control plane
after real multi-provider/multi-gateway volume exists.

A major cross-cutting workstream in this phase is **Financial Integrity
Hardening**, defined normatively in [`docs/FINANCIAL_INTEGRITY.md`](FINANCIAL_INTEGRITY.md).
It protects Managed balances, escrow, provider earnings, refunds, disputes and
payout state against silent historical rewriting even if an application host
or privileged database path is compromised.

### 11.1 Reuse-first implementation rule

Phase 7 MUST NOT start by building a new ledger, reconciliation engine, generic
hold/refund engine, or financial journal from scratch. Two existing TOS Network
repositories are the required starting point and implementation reference:

```text
tosnetwork/blnk
= preferred Managed financial-ledger foundation

tosnetwork/atos-aidrop
= proven ATOS/Wallet -> Blnk integration and immutable-audit reference
```

Coding agents MUST inspect both repositories before proposing new Phase 7
financial primitives. If a required capability already exists there, reuse,
adapt or harden it unless a documented correctness/security gap makes reuse
unsafe.

#### `tosnetwork/blnk` — preferred financial core

The current fork already provides substantial Phase 7 foundations that should
be treated as existing implementation, not greenfield requirements:

- double-entry ledger and authoritative balances;
- historical balance queries and multi-currency transaction support;
- inflight/hold flows suitable as the financial primitive beneath Managed escrow;
- refund/reversal transaction flows that create compensating transactions instead of rewriting history;
- external reconciliation engine, matching rules and reconciliation persistence;
- PostgreSQL-backed transaction storage and concurrency controls;
- transactional/outbox patterns used by lineage processing;
- metrics, tracing, worker/queue infrastructure and load tests;
- basic PostgreSQL backup support to disk/S3;
- transaction immutability enforcement for core financial fields;
- a background SHA-256 transaction hash chain with serialized `chain_state` advancement;
- crash-safe hash-chain batching using one PostgreSQL transaction and `FOR UPDATE` on chain state;
- a local `verify-chain` path that replays the chain and detects discontinuity or changed sealed fields.

Do not duplicate these mechanisms inside `atos`. The intended production
shape is an explicit financial-service boundary:

```text
ATOS business state
       |
       v
ATOSFinancialAdapter
       |
       v
tosnetwork/blnk
       |
       v
Blnk PostgreSQL financial journal / balances
```

ATOS remains responsible for commercial/business identities and workflow;
Blnk remains responsible for financial accounting primitives.

#### `tosnetwork/atos-aidrop` — proven integration/reference implementation

`atos-aidrop` already demonstrates the architectural pattern Phase 7 should
follow rather than rediscover:

- the application database does not store a mutable financial balance;
- Blnk is the authoritative source of truth for balances and journal entries;
- application/business workflow state is kept separate from financial truth;
- treasury/user debit-credit flows are expressed through Blnk operations;
- held/cancelable transfers provide an existing example of business workflow over Blnk inflight transactions;
- reversal is implemented as a new opposite-direction Blnk transaction;
- stable idempotency and PostgreSQL advisory-lock patterns protect business workflows from concurrency races;
- operator financial actions use distinct roles/credentials and audited identities;
- external immutable audit export uses ordered durable batches, stable batch identity, chained hashes and replay-safe delivery;
- the archive side is required to be append-only and suitable for object-lock/WORM retention;
- backup, recovery, database-security, secrets, audit-export and incident-response operational patterns already exist as implementation references.

Phase 7 may extract/refactor reusable patterns from `atos-aidrop`, but MUST NOT
couple the production ATOS gateway to the airdrop application's product model.
It is a reference implementation for integration, security and durability
semantics, not the canonical ATOS financial API.

### 11.2 Existing foundations are not the final integrity format

The existing Blnk transaction hash chain is a useful local tamper-evidence
foundation, but it is not yet the normative ATOS Financial Commitment format.
In particular, its current canonicalization is implementation-local and based
on delimiter-joined transaction fields. Phase 7 MUST define a versioned,
domain-separated, deterministic canonical encoding before independently
signed or TOS-anchored commitments depend on it.

Conceptually:

```text
ATOS_FINANCIAL_COMMITMENT_V1
    + canonical immutable economic identity
    + ordered ledger facts
    + previous commitment / sequence
        -> deterministic digest
```

The final encoding MUST have unambiguous field boundaries and normative test
vectors. Reuse an already-standardized deterministic encoding from the TOS
stack where appropriate rather than inventing ad-hoc string concatenation.

The existing Blnk `meta_data` field MUST NOT be the sole carrier of immutable
ATOS economic identity. Current Blnk transaction immutability intentionally
allows metadata updates, and the existing transaction hash chain does not make
arbitrary mutable metadata part of its sealed canonical row. Therefore any
ATOS-specific commitment identity that must survive independent verification
(Job/Quote/Billing/earning/dispute/payout binding) must be stored in immutable,
versioned fields or in an immutable external commitment sealed by the financial
integrity chain.

### 11.3 ATOSFinancialAdapter — remaining business/financial boundary

The primary ATOS-side Phase 7 implementation is an explicit adapter that maps
existing ATOS economic state into Blnk without making Blnk aware of ATOS
business policy.

At minimum, immutable financial operations/commitments must bind the relevant
subset of:

```text
principal_id
provider_id
job_id
quote_id
capability_id
capability_version
billing_snapshot_id
execution_receipt_id
settlement_id
provider_earning_id
dispute_id
payout_id
asset/currency
exact amount
economic event type
stable idempotency identity
```

The adapter owns the chart-of-accounts mapping for ATOS concepts such as:

```text
principal_available
principal_reserved
managed_escrow
provider_payable
provider_disputed
gateway_fee_revenue
gateway_refund_liability
payout_clearing
```

The adapter MUST preserve the existing ATOS Job/Quote/Billing/Receipt/Dispute
state machines; it is not permission to create a parallel settlement engine.
Blnk transactions are the financial expression of an already-authorized ATOS
economic transition.

### 11.4 Reconciliation and projection strategy

Reuse Blnk's generic reconciliation engine rather than building another
matching engine. Add ATOS-specific connectors/projections for the independent
representations Phase 7 must compare:

```text
Blnk ledger / balances
    <-> ATOS account/escrow projections

Blnk settlement entries
    <-> BillingSnapshot / Receipt / ProviderEarning

payout clearing entries
    <-> external payout backend results

refund/reversal entries
    <-> ATOS dispute state

finalized integrity batches
    <-> external signatures
    <-> TOS anchors
```

Projection rebuild and comparison must be deterministic. A mismatch is an
integrity incident and may trigger financial safe mode; it must not silently
choose whichever mutable database value is newest.

### 11.5 Financial Commitment, Merkle batches, KMS/HSM and TOS anchor

The main cryptographic work still missing from the reusable foundations is the
externalized integrity layer:

1. freeze `ATOS Financial Commitment V1` canonical encoding and domain separation in `atos-spec`;
2. group finalized financial commitments into deterministic Merkle batches;
3. bind each batch to sequence range/count, previous batch/root, canonicalization version and gateway/network identity;
4. sign finalized roots through external KMS/HSM/Vault-backed signing authority whose private key is outside the normal ATOS/Blnk application host;
5. retain signed roots/manifests independently from the operational database;
6. periodically publish the signed Managed-ledger root commitment to TOS Network through the normal `atos -> tos-protocol -> TOS` trust/economic integration boundary;
7. ship an independent verifier that can rebuild the commitment/Merkle root from retained ledger evidence and compare it with the external signature and finalized TOS anchor.

The `atos-aidrop` immutable audit exporter is the preferred reference for
ordered durable batches, stable batch IDs, lost-response-safe delivery and an
append-only receiver. Phase 7 upgrades that pattern from application audit
events to normative financial commitments and from HMAC-only transport
authentication to independently verifiable KMS/HSM signatures plus TOS
anchoring.

The TOS root anchor is an **integrity commitment for Managed financial
history**. It does not turn the underlying Managed Jobs into Verified Jobs and
must never be represented as satisfying `tos_verified_v1` escrow/settlement
requirements. Verified and Native transactions retain their own stronger
per-transaction proof/economic guarantees.

### 11.6 Infrastructure hardening still required

Blnk's existing `pg_dump` disk/S3 backup support is a useful baseline but does
not by itself satisfy the Phase 7 recovery threat model. Production hardening
still requires:

- PITR with WAL archiving and tested arbitrary-point restore;
- independently retained base backups/WAL outside the ordinary application trust domain;
- immutable/WORM/Object-Lock retention where supported;
- periodic restore drills;
- independent retention of signed integrity manifests/roots;
- separate runtime/migration/audit database roles and break-glass procedures;
- no superuser/owner credential in normal ATOS or Blnk runtime configuration;
- external SQL/DDL/security audit evidence;
- monitoring/alerting for reconciliation divergence, hash-chain lag, missing batches, failed signatures/anchors and backup/restore health;
- tested financial safe mode for detected integrity incidents.

Reuse the operational/security patterns and documents already present in
`atos-aidrop` where applicable instead of drafting equivalent controls from
scratch.

### 11.7 Phase 7 implementation order for coding agents

Unless a discovered correctness dependency requires otherwise, implement the
financial-integrity work in this order:

```text
1. Audit current tosnetwork/blnk and tosnetwork/atos-aidrop exact HEADs
2. Freeze ATOS chart of accounts + ATOSFinancialAdapter contract
3. Integrate ATOS economic transitions with Blnk source-of-truth accounting
4. Add deterministic ledger/projection reconciliation and rebuild checks
5. Freeze ATOS Financial Commitment V1 canonicalization + test vectors
6. Harden/upgrade local hash-chain commitment semantics without duplicating Blnk's engine
7. Add deterministic Merkle batch builder
8. Add external KMS/HSM signer abstraction + durable signing checkpoints
9. Add independent immutable signed-root retention
10. Add tos-protocol/TOS Managed Financial Ledger Anchor publication/resolution
11. Extend verifier to validate ledger -> batch -> signature -> finalized TOS anchor
12. Complete PITR/WAL/WORM/privilege-separation/failure drills
```

A coding agent MUST NOT claim Phase 7 completion after merely connecting ATOS
to Blnk or after merely anchoring a local database hash. The acceptance target
is independent reconstruction and verification across the entire chain of
evidence.

### 11.8 Financial-integrity acceptance gate

At minimum prove all of the following against real infrastructure where
applicable:

- ATOS can execute reserve/settle/refund/reversal/payout-related financial transitions through Blnk without maintaining a second mutable source-of-truth balance;
- the same semantic economic action is idempotent, while changed semantics under the same identity conflict;
- concurrent replicas cannot double-reserve, double-settle, double-refund or double-pay;
- historical economic transactions are corrected by compensating entries, not in-place mutation;
- ATOS projections can be rebuilt or reconciled deterministically from the financial ledger;
- deliberate mutation/deletion/reordering of sealed financial history is detected by local verification;
- deterministic Merkle batches reproduce the same root from independently retained evidence;
- KMS/HSM signature verification fails on a substituted root/key/domain;
- a lost response after TOS anchor publication is reconciled without publishing a different semantic anchor;
- the independent verifier detects disagreement between reconstructed history and the finalized TOS anchor;
- restore from independently retained backup/WAL evidence is tested;
- compromising the normal ATOS application/database host is insufficient to silently rewrite previously externally finalized Managed financial history.

**Financial-integrity completion gate:** the normal ATOS application/database
host can no longer silently rewrite previously externally finalized Managed
financial history; ledger-derived projections are rebuildable, divergence is
detected by reconciliation/signature/TOS-anchor verification, and recovery from
independently retained evidence is tested. The detailed acceptance matrix is in
[`docs/FINANCIAL_INTEGRITY.md`](FINANCIAL_INTEGRITY.md).

Other Phase 7 hardening work includes:

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
forward into Phase 3 merely because adjacent domain fields already exist.
However, deployments that hold material real customer/provider value SHOULD
prioritize the Financial Integrity controls proportionally to financial risk
rather than waiting for every federation feature to be complete.

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
15. **Managed financial integrity is distinct from Verified transaction proof.** Periodically anchoring a Managed ledger root makes historical Managed accounting tamper-evident; it does not upgrade those Jobs to `trust_mode=verified`.
16. **Public schemas remain stable.** Later phases activate guarantees already modeled or version them explicitly rather than silently changing meaning.

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
