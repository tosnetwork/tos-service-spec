# ATOS MCP Specification v0.2

## 1. Transport

Preferred production endpoint:

`POST https://mcp.atos.im/mcp`

Use MCP 2026 Streamable HTTP semantics. The server should be horizontally scalable and avoid hidden transport/session state. Keep `https://mcp.atos.im/sse` only as a legacy compatibility adapter during migration.

ATOS v0.2 does not require a persistent MCP session to determine tool visibility. Authorization is carried on each request.

## 2. Trust-Mode Contract

ATOS exposes one MCP business surface across all trust modes.

Request-time value:

```text
requested_trust_mode = managed | verified | native | auto
```

Resolved transaction value:

```text
trust_mode = managed | verified | native
```

**`auto` is request-only.** It MUST NOT appear as the resolved mode on a Quote, Invocation, Job, Escrow, Receipt, or settlement record.

The concrete mode becomes immutable at `atos_quote`.

Therefore:

- `atos_search` MAY filter by requested mode and proof requirements;
- `atos_quote` accepts `requested_trust_mode` and resolves it;
- `atos_invoke` and `atos_create_job` MUST NOT accept a replacement `trust_mode` field;
- Invocation/Job/Receipt results MUST inherit the Quote's concrete `trust_mode`;
- a weaker fallback requires a new Quote;
- `verified` uses `tos_verified_v1` or a stronger compatible proof profile;
- `native` uses `tos_native_v1` or a stronger compatible proof profile.

Normative profile guarantees are defined in `docs/PROOF_PROFILES.md`.

## 3. Proof Requirement Semantics

Example request policy:

```json
{
  "requested_trust_mode":"auto",
  "proof_requirements": {
    "network_verifiable_receipt": true,
    "tos_settlement": false,
    "portable_proof_of_service": true
  }
}
```

For v0.2 boolean proof requirements:

- `true` means the property is required;
- `false` or omission means the property is not required;
- `false` does **not** mean the property is forbidden.

This lets `auto` choose a stronger mode when it is cheaper or otherwise preferable without violating the request.

## 4. Tool Visibility Model

### 4.1 Fundamental rule

`tools/list` is the model's reachable action vocabulary. A tool that can be dispatched by the server but can never appear in a valid `tools/list` result is unreachable to ordinary MCP clients and MUST NOT be described as merely "optional."

ATOS distinguishes:

1. **ordinary consumer tools** — useful for normal capability consumption;
2. **capability-management tools** — visible only when request authorization includes provider management scope;
3. **provider/admin tools** — visible only when authorization plus provider/role/resource conditions make them relevant.

Tool visibility is an optimization and UX boundary. It is **not** an authorization grant. Every `tools/call` re-validates authorization.

### 4.2 Authorization-derived, never history-derived

The available set MAY vary from the authorization presented on the current request.

It MUST NOT vary because of:

- connection identity;
- a hidden session object;
- an earlier `atos_search` result;
- an earlier `atos_get_capability` result;
- which Capability the model most recently viewed;
- any other side effect of earlier requests.

### 4.3 Visibility formula

Where relevant:

```text
tool_visible
  = required_scope_present
    AND optional_role/resource_visibility_precondition
```

The required scope is always a hard floor. Ownership or provider role can only further hide a tool; it can never reveal a tool when its required scope is absent.

Examples:

| Tool | Visibility minimum |
|---|---|
| `atos_search`, `atos_get_capability` | `capabilities:read` |
| `atos_quote` | `quotes:read` |
| `atos_invoke` | `invocations:create` |
| `atos_create_job` | `jobs:create` |
| `atos_get_job` | `jobs:read` |
| `atos_cancel_job` | `jobs:cancel` |
| `atos_account` | `account:read` |
| `atos_artifact` | visible to normal consumers; operation-level scopes checked at call time |
| `atos_register_capability` | `capabilities:write` |
| `atos_update_capability` | `capabilities:write` |
| `atos_list_my_capabilities` | `capabilities:write`; provider role may be used as an additional visibility filter |
| `atos_pause_capability` | `capabilities:write`; owning at least one Capability may be used as an additional visibility filter |
| `atos_provider_jobs` | `provider_jobs:read` + provider role |
| `atos_deliver_job` | `provider_jobs:deliver` + provider role |
| `atos_request_settlement` | `settlement:write` + provider role |
| `atos_dispute_job` | `disputes:review` |
| `atos_authorize_execution_signer`, `atos_rotate_execution_signer`, `atos_revoke_execution_signer` | `execution_signers:write` + provider role |
| `atos_get_execution_signer_status` | `execution_signers:read` + provider role |
| `atos_evaluate_activation` | `activation:evaluate` -- deliberately no ownership/provider-role visibility precondition; this is an activation-authority-side tool, not a provider one |
| `atos_open_certification` | `certifications:write` + provider role |
| `atos_get_certification_status` | `certifications:read` + provider role |
| `atos_publish_open_task`, `atos_cancel_open_task`, `atos_accept_open_task_proposal` | `open_tasks:write` -- default consumer scope, the task-owner side |
| `atos_search_open_tasks`, `atos_get_open_task`, `atos_list_open_task_proposals` | `open_tasks:read` -- default consumer scope |
| `atos_apply_to_open_task`, `atos_withdraw_open_task_proposal` | `open_task_proposals:write` + provider role -- deliberately NOT implied by `open_tasks:write`, mirroring `provider_jobs:deliver`'s pattern: applying to fulfill someone else's task is a distinct trust-side-effect class from managing one's own tasks |

Target-object ownership is always checked on `tools/call`, even if a coarse ownership condition was already used to hide/show the tool.

### 4.4 `tools/list` caching

MCP 2026 list results are cacheable. Because ATOS tool visibility can vary by authorization context, every authorization-sensitive `tools/list` page MUST return private cache semantics.

Recommended v0.2 result fields:

```json
{
  "ttlMs": 30000,
  "cacheScope": "private"
}
```

A 30-second TTL is intentionally short enough for permission/provider-role changes during early deployment while avoiding a list fetch before every model turn.

ATOS MAY later tune the TTL operationally without changing the tool contract.

ATOS v0.2 MAY rely entirely on TTL freshness and does not need to advertise `listChanged: true`. If ATOS later implements MCP's subscription/listen stream and advertises list changes, notifications complement rather than replace TTL.

### 4.5 Deterministic ordering

For the same underlying visible set, return tools in deterministic order. Never emit tools by iterating an unordered Go map.

Canonical grouping/order:

```text
consumer core
artifact
capability management
provider jobs/admin
```

Within each group, preserve the order defined by this specification.

## 5. Tool Design Principles

- Keep the model-visible tool list small.
- Separate discovery from financially committing operations.
- Use a **Quote** as the immutable commercial/trust contract between search and execution.
- Every committing call requires `idempotency_key`.
- Return machine-readable structured content; concise text summaries are secondary.
- Use MCP elicitation/input-required semantics when user approval or missing sensitive parameters are needed.
- Do not expose blockchain implementation details in ordinary responses.
- Never silently downgrade `verified`/`native` to a weaker mode.
- Distinguish gateway-computed reputation summaries from TOS-verifiable proof facts.
- Keep bulk/private payloads off-chain; Verified/Native receipts carry commitments when required.

## 6. Ordinary Consumer Tools

A token carrying the full recommended consumer scopes sees **9 tools** in this order:

1. `atos_search`
2. `atos_get_capability`
3. `atos_quote`
4. `atos_invoke`
5. `atos_create_job`
6. `atos_get_job`
7. `atos_cancel_job`
8. `atos_account`
9. `atos_artifact`

A narrower token MAY see fewer than 9 if its granted scopes omit a corresponding operation.

### 6.1 `atos_search`

Search and rank capabilities.

```json
{
  "query": "audit a Solidity smart contract",
  "filters": {
    "max_price": {"amount": "10.00", "currency": "USD"},
    "delivery_modes": ["instant", "async"],
    "requested_trust_mode": "auto",
    "proof_requirements": {"network_verifiable_receipt": true},
    "min_trust_score": 0.8,
    "max_latency_ms": 60000
  },
  "limit": 5
}
```

Search does not create an economic commitment and does not permanently resolve `auto`.

Search results SHOULD expose whether a Capability requires Artifact transport, for example:

```json
{
  "capability_id":"cap_...",
  "requires_artifact_transfer":true,
  "artifact_input_fields":["document"]
}
```

This helps the model know when to use `atos_artifact` without changing `tools/list`.

### 6.2 `atos_get_capability`

```json
{"capability_id":"cap_..."}
```

Returns input/output schemas, pricing, provider/trust summary, delivery mode, active concrete trust modes, proof profiles, transport bindings, and explicit Artifact-transfer metadata derived from the schemas.

### 6.3 `atos_quote`

Create a short-lived executable Quote and resolve trust mode.

```json
{
  "capability_id": "cap_...",
  "input_summary": {"bytes": 140233, "pages": 38},
  "requested_trust_mode": "auto",
  "proof_requirements": {
    "network_verifiable_receipt": true,
    "tos_settlement": false
  },
  "constraints": {
    "deadline": "2026-08-07T06:00:00Z",
    "max_total": {"amount": "8.00", "currency": "USD"}
  }
}
```

Representative Verified response:

```json
{
  "quote_id":"q_...",
  "capability_id":"cap_...",
  "capability_version":"1.2.0",
  "provider_id":"agt_...",
  "requested_trust_mode":"auto",
  "trust_mode":"verified",
  "proof_profile":"tos_verified_v1",
  "price":{"subtotal":"5.00","fees":"0.25","total_max":"5.25","currency":"USD"},
  "settlement":{"backend":"tos","escrow":true,"funding_model":"gateway_sponsored"},
  "proof":{"quote_commitment":true,"execution_receipt":true,"settlement_proof":true,"proof_of_service":true},
  "expires_at":"2026-08-07T05:10:00Z",
  "requires_confirmation":false,
  "terms_hash":"sha256:...",
  "dispute_policy_hash":"sha256:..."
}
```

Rules:

1. concrete requested mode -> use it or fail;
2. `auto` -> choose a concrete mode satisfying all requirements;
3. returned mode is immutable for the Quote;
4. Verified uses `tos_verified_v1` or stronger;
5. Native uses `tos_native_v1` or stronger;
6. Verified/Native is not quotable unless its proof/settlement path is currently satisfiable;
7. proof/network failure does not permit silent downgrade.

### 6.4 `atos_invoke`

```json
{
  "capability_id":"cap_...",
  "quote_id":"q_...",
  "input":{"text":"..."},
  "idempotency_key":"0198...",
  "max_wait_ms":45000
}
```

`trust_mode` is intentionally absent. The Quote is authoritative.

Possible result types:

```text
completed | accepted | input_required | failed
```

### 6.5 `atos_create_job`

```json
{
  "capability_id":"cap_...",
  "quote_id":"q_...",
  "input":{},
  "idempotency_key":"0198...",
  "callback":null
}
```

Mode and proof profile are inherited from the Quote and cannot be overridden.

### 6.6 `atos_get_job`

```json
{"job_id":"job_..."}
```

Canonical states:

```text
submitted -> working -> input_required -> working -> completed
```

Terminal alternatives:

```text
failed | canceled | rejected
```

Response MUST include the concrete Quote-inherited mode and SHOULD expose compact proof progress for Verified/Native work.

### 6.7 `atos_cancel_job`

```json
{
  "job_id":"job_...",
  "reason":"no longer needed",
  "idempotency_key":"0198..."
}
```

Cancellation cannot downgrade the transaction's trust/settlement guarantees.

### 6.8 `atos_account`

Read-only account summary:

```json
{
  "balance":{"available":"25.00","currency":"USD"},
  "spend_policy":{"per_call_autonomous_limit":"2.00","daily_limit":"20.00","remaining_today":"17.50"},
  "trust_policy":{"default_requested_trust_mode":"auto","minimum_for_high_value":"verified"},
  "provider_earnings":null
}
```

### 6.9 `atos_artifact`

One tool implements three signed-URL transport operations:

```text
create_upload
complete_upload
get_download_url
```

Binary bytes never travel through the MCP call itself.

#### Strict input schema semantics

The machine schema MUST use operation-discriminated alternatives rather than accepting `operation` alone and deferring all missing-field validation to runtime.

Valid shapes:

```json
{
  "operation":"create_upload",
  "content_type":"application/pdf",
  "size_bytes":2140233,
  "purpose":"job_input"
}
```

```json
{"operation":"complete_upload","upload_id":"up_..."}
```

```json
{"operation":"get_download_url","artifact_id":"art_..."}
```

The output MUST echo `operation` so `outputSchema` can be equally discriminated.

Create-upload response:

```json
{
  "operation":"create_upload",
  "upload_id":"up_...",
  "upload_url":"https://...",
  "upload_method":"PUT",
  "expires_at":"2026-08-07T05:10:00Z"
}
```

Complete-upload response:

```json
{
  "operation":"complete_upload",
  "artifact_id":"art_...",
  "content_type":"application/pdf",
  "size_bytes":2140233,
  "sha256":"sha256:..."
}
```

Download response:

```json
{
  "operation":"get_download_url",
  "download_url":"https://...",
  "expires_at":"2026-08-07T05:10:00Z",
  "content_type":"application/pdf",
  "size_bytes":891004
}
```

#### Operation authorization

- `create_upload` + `purpose=job_input`: `invocations:create OR jobs:create`;
- `create_upload` + `purpose=capability_asset`: `capabilities:write`;
- `complete_upload`: caller/security context must own the upload record;
- `get_download_url`: caller must have Artifact or owning-Job access.

`upload_id` and `artifact_id` are identifiers, never bearer credentials.

## 6A. Open Task (Marketplace) Tools

Phase 3C's demand-side marketplace (`docs/IMPLEMENTATION_ROADMAP.md` §7.3,
`docs/API.md` §5A). These are the task-owner side, using the same
`open_tasks:read`/`write` default consumer scopes as `atos_create_job`/
`atos_cancel_job` -- publishing a task and accepting a proposal are ordinary
consumer actions, not a distinct role. The provider side
(`atos_apply_to_open_task`/`atos_withdraw_open_task_proposal`) is listed in
§8, since applying to fulfill someone else's task is a distinct
trust-side-effect class requiring `open_task_proposals:write` + provider
role.

- `atos_publish_open_task` — `open_tasks:write`. Publishes a new OpenTask.
  `expires_at` is required (an OpenTask MUST NOT be publishable with no
  expiry) and `idempotency_key` is required. An Agent MUST NOT need to know
  a `capability_id` before publishing demand -- it publishes goal, budget,
  deadline, inputs and trust requirements; discovery/matching and Provider
  proposals resolve suitable Capability/provider candidates afterward.
- `atos_search_open_tasks` — `open_tasks:read`. Browses currently open
  tasks. Only publicly safe fields are returned; task `input` and other
  owner-only detail are never included here.
- `atos_get_open_task` — `open_tasks:read`. Full `input` is only visible to
  the task's own owner or, once accepted, the winning provider; every other
  caller receives the redacted public view.
- `atos_cancel_open_task` — `open_tasks:write`; owner only. Refused once a
  proposal has already been accepted -- an accepted winner is never
  silently discarded by a cancel.
- `atos_list_open_task_proposals` — `open_tasks:read`. The task owner sees
  every proposal in full; a provider sees their own proposal in full and
  every other proposal redacted; anyone else sees only redacted proposals.
- `atos_accept_open_task_proposal` — `open_tasks:write`; owner only.
  Durably claims a winning proposal and drives the existing Quote/Job
  creation pipeline forward (`docs/API.md` §5A's `acceptance.checkpoint`
  sequence), using the task owner as principal and the winning proposal's
  Capability/version -- never a caller-supplied price, trust mode or
  Capability override. Idempotent: retrying with the same
  `idempotency_key` resumes the same acceptance rather than creating a
  second Quote/Job.

## 7. Capability-Management Tools

These are not ordinary consumer tools.

### 7.1 `atos_register_capability`

Visibility minimum:

```text
capabilities:write
```

Provider-side registration requests desired concrete trust modes; it does not self-certify active modes.

`requested_trust_modes` contains only:

```text
managed | verified | native
```

`auto` is invalid in provider concrete-mode sets.

### 7.2 `atos_update_capability`

Visibility minimum:

```text
capabilities:write
```

Providers may update mutable metadata and requested trust modes, but cannot force `supported_trust_modes` or `mode_support.status=active` through a generic patch.

Target capability ownership is checked at call time.

## 8. Provider/Admin Tools

These tools are conditionally visible only after required scopes pass. Role/ownership may further narrow visibility.

Implemented:

- `atos_list_my_capabilities` — `capabilities:write`; returns an empty list if the provider owns none.
- `atos_pause_capability` — `capabilities:write`; target ownership re-checked on call.
- `atos_provider_jobs` — `provider_jobs:read` + provider role; lists Jobs owned by the authenticated provider, or gets one by `job_id` (ownership re-checked on the single-job path).
- `atos_deliver_job` — `provider_jobs:deliver` + target-job/provider authorization; delivers a completed result for a Job owned by the authenticated provider. Provider identity always comes from the authenticated principal, never request JSON; the Job's Quote remains authoritative for trust_mode/pricing — only `output` is accepted. A duplicate delivery for an already-completed Job is a safe, idempotent no-op.
- `atos_request_settlement` — **`settlement:write`** (Phase 3A resolves this scope; deliberately separate from the pre-existing read-only `settlement:read`, never overloading a read scope to authorize a money-changing operation). A thin facade over the existing Job economic-reconciliation entry point — never a second settlement engine, never a caller-supplied settlement amount. Provider ownership of the target Job is required.
- `atos_dispute_job` — **`disputes:review`** (the same scope Phase 2C's REST dispute-review/-resolve operations already require — Phase 3A reuses it rather than inventing a broader provider/admin dispute scope). Strictly operation-discriminated (`operation: "review" | "resolve"`) thin facade over the existing Phase 2C `DisputeService`; no parallel dispute state machine. `reviewer_id` always comes from the authenticated principal.
- `atos_authorize_execution_signer` / `atos_rotate_execution_signer` / `atos_revoke_execution_signer` — **`execution_signers:write`** (Phase 3B; new scope, deliberately separate from every other provider/admin scope rather than overloading `capabilities:write`, since signer mutation is a distinct trust-side effect class from ordinary Capability metadata). Distinct tools rather than one operation-discriminated tool (unlike `atos_dispute_job`) because `authorize`/`rotate`/`revoke` take meaningfully different required parameters, not near-identical review/resolve shapes. `provider_id`/`execution_signer_id` ownership always resolves from the authenticated principal + `docs/IMPLEMENTATION_ROADMAP.md` §7.2.0's Capability-ownership rule, never from request JSON. `rotate` is durable orchestration of authorize-then-revoke (§7.2.2) — it is never implemented as two independent tool calls a client must sequence itself. Accepts only a signer public key and signer ID; no tool in this repository's contract ever accepts or returns a private key.
- `atos_get_execution_signer_status` — **`execution_signers:read`**; returns the current signer, and the in-progress operation's durable checkpoint if one is pending/reconciling, for the target Capability. Read-only, no mutation.
- `atos_evaluate_activation` — **`activation:evaluate`** (new scope; explicit-grant-only like `disputes:review`/`execution_signers:write`, never a default consumer scope). The entry point for `docs/IMPLEMENTATION_ROADMAP.md` §7.2.1's `ActivationAuthority.Evaluate` — deliberately **not** capability-owner-scoped, unlike every other tool in this section: it is an activation-authority-side operation, not a provider one, so a caller only needs `activation:evaluate`, never ownership of the target Capability. Takes `{capability_id, mode, idempotency_key}` (`mode` is `verified` or `native`; Managed has no `ActivationAuthority` concept). `idempotency_key`'s namespace is the calling admin's own identity (not `capability_id`) — a retry with the same key and identical `capability_id`/`mode` replays the original decision without re-consulting the authority; reused against a different `capability_id`/`mode` is `idempotency_conflict`. `mode_support[mode].status` must currently be `pending` or `suspended`, else the call is rejected as a validation error before the authority is ever consulted. A `granted:false` result is a normal (`isError:false`) outcome, not an error — see the endpoint's own doc comment in `docs/API.md` §2.2: production has no `ActivationAuthority` implementation that ever returns `granted:true` until Phase 4 supplies a real one, so this tool's production behavior today is a deterministic, informative no-op that exists to give Phase 4 an entry point without needing new API surface later. Merged in `tosnetwork/atos#14`.
- `atos_open_certification` — **`certifications:write`** (new scope pair, mirroring `execution_signers:read`/`write`'s naming convention rather than overloading `capabilities:write`, since certifying a binding is a distinct trust-side effect class from ordinary Capability metadata). Unlike `atos_evaluate_activation`, this **is** a provider-role tool: a provider proves their own capability's binding actually works, so ownership of `capability_id` is required. Takes `{capability_id, transport, idempotency_key}`. Opens (or, on a replay, recovers) one sandbox certification attempt at the Capability's current version, running the probe synchronously (health, then a deeper transport-specific check where the adapter supports it, per `docs/IMPLEMENTATION_ROADMAP.md` §7.1.3) and returning the completed result. A `failed` status is a normal outcome, not an error. This is the CertificationService.Open entry point §7.1.3's own success criterion always assumed existed; before this it had zero callers anywhere.
- `atos_get_certification_status` — **`certifications:read`**; returns the certification history for a Capability owned by the authenticated provider, newest first. Read-only, no mutation.
- `atos_apply_to_open_task` — **`open_task_proposals:write`** (deliberately separate from `open_tasks:write`, mirroring `provider_jobs:deliver`'s explicit-grant-only pattern -- see §6A). Submits a proposal to fulfill someone else's OpenTask, as the calling provider. `capability_version` is never caller-supplied; it is frozen from the Capability's current version at propose time. Any `proposed_price` is a non-authoritative hint only -- the real price is always computed by the existing Quote pricing rules at acceptance time, bounded by the task's own `constraints.max_total`.
- `atos_withdraw_open_task_proposal` — **`open_task_proposals:write`**. Withdraws the calling provider's own proposal. Refused once that proposal has already been accepted as the task's winner.

Provider/admin settlement operations MUST preserve Quote/Job concrete trust mode and proof profile.

## 9. Required Error Semantics

Recommended machine codes:

- `authentication_required`
- `permission_denied`
- `trust_mode_unavailable`
- `proof_requirements_unsatisfied`
- `proof_profile_unavailable`
- `network_unavailable`
- `quote_expired`
- `quote_mismatch`
- `quote_mode_mismatch`
- `requote_required`
- `spend_limit_exceeded`
- `insufficient_balance`
- `idempotency_conflict`
- `job_not_cancelable`
- `artifact_not_found`
- `artifact_access_denied`
- `upload_expired`
- `upload_mismatch`
- `provider_failed`
- `settlement_failed`

A server MUST NOT turn a trust/proof failure into a weaker successful execution without a new Quote.

## 10. MCP Resources

Recommended resources:

- `atos://taxonomy`
- `atos://capabilities/trending`
- `atos://account/policy`
- `atos://network/status`
- `atos://docs/protocol-version`

`atos://network/status` exposes high-level mode availability without chain plumbing.

## 11. MCP Prompts

Optional convenience prompts:

- `atos-find-specialist`
- `atos-publish-capability`
- `atos-compare-quotes`

Prompts are not business APIs.

## 12. Spend Confirmation via MCP Elicitation

When a Quote exceeds autonomous policy, request explicit approval and bind that approval to:

- Quote ID;
- concrete trust mode;
- proof profile;
- maximum amount;
- Quote expiry.

Approval for one Quote/mode cannot be replayed for another.

## 13. Idempotency

`atos_invoke`, `atos_create_job`, `atos_cancel_job`, registration mutations, and settlement mutations MUST require `idempotency_key`.

Server behavior:

- same principal + same key + same request hash => return original result;
- same principal + same key + different request hash => `409 idempotency_conflict`;
- retain keys for at least the maximum financial dispute/retry window.

For committing operations, the idempotency record binds the Quote and therefore its resolved trust mode/proof profile.

## 14. MCP Invariants

1. A fully scoped ordinary consumer sees 9 stable tools.
2. Provider/capability-management tools require provider scopes and are not injected into ordinary consumer context.
3. `tools/list` may vary from current-request authorization, never from connection/session history.
4. Authorization-sensitive `tools/list` results use `cacheScope=private`; v0.2 recommends `ttlMs=30000`.
5. The same visible tool set is returned in deterministic order.
6. Tool visibility never replaces call-time scope/ownership checks.
7. `atos_artifact` is one always-reachable routing intent with strict operation-discriminated schemas.
8. `auto` is only a client pre-Quote policy value.
9. `atos_quote` resolves and freezes a concrete mode.
10. Invoke/Job creation inherit mode from Quote and cannot override it.
11. Verified uses `tos_verified_v1`; Native uses `tos_native_v1` or stronger compatible profiles.
12. Verified/Native proof failure is a failure/requote, never a silent Managed fallback.
13. Provider `requested_trust_modes` is not public active `supported_trust_modes`.
14. Execution Receipts may use an authorized delegated signer; signer authority is proved for Verified/Native.
15. Bulk payloads remain off-chain; receipts may commit their hashes.
16. Normal MCP clients see proof status/references, not blockchain plumbing.