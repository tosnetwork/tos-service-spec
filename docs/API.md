# ATOS REST API v1 — Protocol Semantics v0.2

Base URL:

`https://api.atos.im/v1`

## 1. Conventions

- JSON request/response.
- Bearer authentication except public discovery/card endpoints.
- RFC-style HTTP status codes.
- Financial mutations require `Idempotency-Key` or an equivalent body field.
- Cursor pagination for lists.
- Errors use stable machine codes.
- `requested_trust_mode = managed | verified | native | auto` is client pre-Quote policy.
- `trust_mode = managed | verified | native` is resolved transaction state.
- `auto` MUST resolve at Quote time and MUST NOT appear as a final Invocation/Job/Receipt mode.
- Invocation/Job creation inherits trust mode from the Quote; callers cannot override it.
- Verified uses `tos_verified_v1`; Native uses `tos_native_v1` or stronger compatible profiles.
- Verified/Native operations MUST NOT silently downgrade to Managed.

For boolean `proof_requirements`, `true` means required; `false`/omitted means not required, not forbidden.

## 2. Capability Endpoints

- `GET /capabilities?q=...`
- `GET /capabilities/{capability_id}`
- `GET /capabilities/mine` — capabilities owned by the authenticated provider (`capabilities:write`, matching MCP's `atos_list_my_capabilities`'s scope choice -- listing what you can manage is a provider-management operation, not a generic read). Response: `{"capabilities":[...]}`, mirroring `GET /open-tasks`'s `{"open_tasks":[...]}` wrapper convention (§5A).
- `POST /capabilities` — provider create/request mode support
- `PATCH /capabilities/{capability_id}` — provider metadata/request update
- `POST /capabilities/{capability_id}/pause`
- `POST /capabilities/{capability_id}/resume`

Discovery filters MAY include:

```text
requested_trust_mode=managed|verified|native|auto
network_verifiable_receipt=true|false
tos_settlement=true|false
```

Capability responses include public active:

```text
supported_trust_modes
```

containing only concrete `active` modes.

Provider create/update requests instead use:

```text
requested_trust_modes
```

because provider intent is not certification.

Example create request:

```json
{
  "name":"Document Translation",
  "description":"...",
  "delivery_mode":"async",
  "input_schema":{"type":"object"},
  "output_schema":{"type":"object"},
  "pricing":{"model":"per_unit"},
  "requested_trust_modes":["managed","verified","native"],
  "bindings":[
    {
      "transport":"http",
      "endpoint_ref":"ep_...",
      "eligible_trust_modes":["managed","verified"]
    }
  ]
}
```

Example response:

```json
{
  "capability_id":"cap_...",
  "requested_trust_modes":["managed","verified","native"],
  "supported_trust_modes":["managed"],
  "mode_support":{
    "managed":{"status":"active"},
    "verified":{"status":"requested","proof_profile":"tos_verified_v1"},
    "native":{"status":"requested","proof_profile":"tos_native_v1"}
  },
  "readiness":{
    "verified":{
      "requested":true,
      "status":"requested",
      "transport_healthy":false,
      "health_fresh":false,
      "certification_current":false,
      "signer_authorized":false,
      "activation_authority_satisfied":false,
      "reason_code":"NO_READINESS_EVIDENCE_YET"
    },
    "native":{
      "requested":true,
      "status":"requested",
      "transport_healthy":false,
      "health_fresh":false,
      "certification_current":false,
      "signer_authorized":false,
      "activation_authority_satisfied":false,
      "reason_code":"NO_READINESS_EVIDENCE_YET"
    }
  }
}
```

`mode_support[mode].status` is one of `requested|pending|active|suspended|unsupported`
per `docs/IMPLEMENTATION_ROADMAP.md` §7.2.0's frozen transition matrix. A
generic provider PATCH MUST NOT directly force `supported_trust_modes` or
`mode_support[mode].status` to `active` -- only the activation authority can,
and never as a side effect of a metadata PATCH.

`readiness` is the public per-mode availability/evidence projection (§7.2.0/
§10 of the roadmap), present for every mode in `requested_trust_modes` other
than `managed` (Managed has no readiness concept -- it is unconditionally
`active`). It answers, without exposing secrets: was this mode requested; its
lifecycle status; is an eligible transport healthy and is that health
evidence fresh; has this exact Capability version/binding passed sandbox
certification; is a required execution-signer authorization current; is the
activation-authority condition satisfied; and a `reason_code` explaining
whichever of these is the blocking one when the mode is not `active` (e.g.
`NO_READINESS_EVIDENCE_YET`, `TRANSPORT_UNHEALTHY`, `HEALTH_STALE`,
`CERTIFICATION_NOT_CURRENT`, `SIGNER_NOT_AUTHORIZED`,
`ACTIVATION_AUTHORITY_UNAVAILABLE`). `readiness[mode].status` MUST always
equal `mode_support[mode].status` -- it is a detail projection of the same
authoritative state, never a second source of truth.

### 2.1 Execution-signer endpoints

Provider/admin only (`execution_signers:write` for mutations,
`execution_signers:read` for status), authorization identical to every other
provider mutation in this document: provider identity comes only from the
authenticated principal, never from a `provider_id` in the request body, and
the authenticated provider MUST own `capability_id`.

- `POST /capabilities/{capability_id}/execution-signer/authorize`
- `POST /capabilities/{capability_id}/execution-signer/rotate`
- `POST /capabilities/{capability_id}/execution-signer/revoke`
- `GET /capabilities/{capability_id}/execution-signer`

All three mutation endpoints require `Idempotency-Key` (same convention as
every other financial/trust mutation in this document, §1) and accept only a
signer public key and signer ID -- never a private key. Per
`docs/IMPLEMENTATION_ROADMAP.md` §7.2.2, `rotate` is durable `atos`-side
orchestration of authorize-then-revoke, never the reverse order, and the
response/status projection exposes the current durable checkpoint
(`intent_persisted|new_authorization_pending|new_authorized|cutover_pending|
old_revocation_pending|old_revoked|completed|reconciling`) rather than a
boolean success flag, so a caller can distinguish "still in progress" from
"failed" from "done."

Example authorize request:

```json
{
  "capability_version":"1.2.0",
  "execution_signer_id":"sig_...",
  "signer_public_key":"base64:...",
  "signature_algorithm":"ed25519"
}
```

Example status response (mid-rotation):

```json
{
  "capability_id":"cap_...",
  "capability_version":"1.2.0",
  "operation_id":"sigop_...",
  "operation_type":"rotate",
  "checkpoint":"new_authorization_pending",
  "old_execution_signer_id":"sig_old",
  "new_execution_signer_id":"sig_new",
  "current_execution_signer_id":"sig_old"
}
```

`current_execution_signer_id` MUST remain the old signer until `checkpoint`
reaches `new_authorized`, per the rotation ordering frozen in the roadmap --
a caller must never observe the new signer advertised as current before its
authorization is confirmed durable.

### 2.2 Activation-evaluation endpoint

Admin only (`activation:evaluate`), explicit-grant-only like
`execution_signers:write`/`disputes:review` -- never a default consumer
scope. Unlike every other Capability mutation in this document, this
endpoint is deliberately **not** owner-scoped: the authenticated principal
does not need to own `capability_id`. This is the entry point for
`docs/IMPLEMENTATION_ROADMAP.md` §7.2.1's `ActivationAuthority.Evaluate`,
which is by design an activation-authority-side operation, never a provider
one -- provider self-assertion (however the request is authenticated) is
explicitly insufficient authority to activate Verified/Native.

- `POST /capabilities/{capability_id}/activation/evaluate`

Requires `Idempotency-Key` (same convention as every other financial/trust
mutation in this document, §1), scoped by the calling admin's own identity
-- not `capability_id`, since this endpoint is not owner-scoped and two
different admins independently using the identical key string must not
collide. A retry with the same `Idempotency-Key` and identical
`capability_id`/`mode` replays the ORIGINAL decision this endpoint made
(the exact `granted`/`reason_code`/`mode_support` values from the first
call), even if live state has since changed for unrelated reasons -- it
never re-evaluates the authority a second time, and never fails with "mode
is already active" merely because the first attempt's response was lost.
Reusing the key against a different `capability_id` or `mode` is an
`idempotency_conflict`, not a replay.

Request:

```json
{"mode":"verified"}
```

`mode` MUST be `verified` or `native` (Managed has no `ActivationAuthority`
concept and is rejected). The referenced `mode_support[mode].status` MUST
currently be `pending` or `suspended` -- any other status (e.g. `requested`,
with no readiness evidence recorded yet, or already `active`) is rejected as
a validation error, not evaluated.

Response -- HTTP 200 only once the activation authority has returned a
completed decision (granted or denied); a fail-closed denial is a normal,
expected 200 outcome here, not an error (see
`docs/IMPLEMENTATION_ROADMAP.md` §7.2.1: production has no implementation
that ever returns `granted=true` until Phase 4 supplies a real authority).
If the authority itself errors (timeout, transport failure, or the
resulting activation cannot be durably persisted), that is a genuine error
response, not a 200 denial -- an unavailable/failed authority call MUST
remain distinguishable from an authoritative rejection so callers can apply
ordinary error/retry handling instead of treating "the authority said no"
and "we couldn't reach the authority" as the same outcome:

```json
{
  "granted":false,
  "reason_code":"ACTIVATION_AUTHORITY_UNAVAILABLE",
  "mode_support":{"status":"pending","reason":"ACTIVATION_AUTHORITY_UNAVAILABLE"}
}
```

On `granted:true`, `mode_support[mode].status` becomes `active` and
`supported_trust_modes` is re-derived to include `mode`, exactly as if
readiness evidence plus authority approval had converged automatically --
this endpoint does not bypass any state-machine invariant, it only supplies
the explicit trigger for evaluating the transition that already existed.

### 2.3 Sandbox certification endpoints

Provider only (`certifications:write` for the mutation, `certifications:read`
for status), ownership enforced identically to every other provider
mutation in this document: provider identity comes only from the
authenticated principal, never from a `provider_id` in the request body,
and the authenticated provider MUST own `capability_id`. Unlike §2.2, this
*is* a provider-role operation -- a provider proving their own capability's
binding actually works, not an authority-side decision.

- `POST /capabilities/{capability_id}/certification`
- `GET /capabilities/{capability_id}/certification`

`POST` requires `Idempotency-Key` (same convention as every other
trust/financial mutation in this document, §1) and opens (or, on a replay
of the same key, recovers) one sandbox certification attempt against the
Capability's binding for the given `transport`, at the Capability's
*current* version. The probe itself runs synchronously: health
(bounded reachability) first, then -- where the resolved adapter supports
it -- a deeper transport-specific check (protocol handshake, bounded
execution, response shape and schema compatibility per
`docs/IMPLEMENTATION_ROADMAP.md` §7.1.3). A newly opened attempt is
itself the §7.2.0 `requested -> pending` readiness-evidence trigger for
every mode eligible on that binding, independent of whether the probe
ultimately passes or fails.

Example request:

```json
{"transport":"http"}
```

Example response:

```json
{
  "id":"cert_...",
  "provider_id":"agt_...",
  "capability_id":"cap_...",
  "capability_version":"1.2.0",
  "transport":"http",
  "endpoint_ref":"ep_...",
  "status":"passed",
  "created_at":"...",
  "completed_at":"..."
}
```

`status` is one of `pending|passed|failed`. A `failed` result is a normal
response (200), not an error -- `failure_reason` and `evidence` explain
why, mirroring the execution-signer status projection's convention of
distinguishing "the operation ran and told you no" from "the operation
could not run at all." Sandbox certification alone -- like health alone,
like signer authorization alone -- never activates Verified or Native; it
is one of the readiness dimensions `ActivationAuthority.Evaluate` (§2.2)
may consider, never a substitute for it.

`GET` returns the certification history for `capability_id` (newest
first), scoped to the requesting provider's own capability -- there is no
cross-provider certification visibility.

## 3. Quote Endpoints

- `POST /quotes`
- `GET /quotes/{quote_id}`

Example request:

```json
{
  "capability_id":"cap_...",
  "requested_trust_mode":"auto",
  "proof_requirements":{
    "network_verifiable_receipt":true,
    "tos_settlement":false
  },
  "constraints":{
    "max_total":{"amount":"10.00","currency":"USD"}
  }
}
```

Example Verified response:

```json
{
  "quote_id":"q_...",
  "capability_id":"cap_...",
  "capability_version":"1.2.0",
  "provider_id":"agt_...",
  "requested_trust_mode":"auto",
  "trust_mode":"verified",
  "proof_profile":"tos_verified_v1",
  "price":{"total_max":"5.25","currency":"USD"},
  "settlement":{
    "backend":"tos",
    "escrow":true,
    "funding_model":"gateway_sponsored"
  },
  "proof":{"execution_receipt":true,"settlement_proof":true},
  "expires_at":"...",
  "terms_hash":"sha256:...",
  "dispute_policy_hash":"sha256:..."
}
```

The returned concrete `trust_mode` and proof profile are immutable for that Quote.

## 4. Invocation Endpoints

- `POST /invocations`
- `GET /invocations/{invocation_id}`

Creation includes `quote_id`, `capability_id`, input and idempotency protection. It MUST NOT accept a caller-provided trust-mode override.

Invocation responses include the concrete `trust_mode` inherited from the Quote.

Verified/Native completed responses SHOULD expose compact Receipt/proof status, including authorized execution signer references where useful.

## 5. Job Endpoints

- `POST /jobs`
- `GET /jobs/{job_id}`
- `POST /jobs/{job_id}/cancel`
- `POST /jobs/{job_id}/messages`
- `GET /jobs/{job_id}/artifacts`

Every Job stores and returns the concrete Quote `trust_mode` and proof profile.

Example:

```json
{
  "job_id":"job_...",
  "quote_id":"q_...",
  "trust_mode":"verified",
  "proof_profile":"tos_verified_v1",
  "state":"working",
  "proof_status":{
    "quote":"committed",
    "escrow":"reserved",
    "receipt":"pending",
    "settlement":"pending"
  }
}
```

Cancellation/refund follows the existing Job mode. A Verified/Native Job cannot move its economic state to a Managed ledger merely because cancellation occurs.

## 5A. Open Task (Marketplace) Endpoints

Phase 3C's demand-side marketplace (`docs/IMPLEMENTATION_ROADMAP.md` §7.3): a
requester publishes an OpenTask describing the outcome/work it wants, without
needing to know a `capability_id` in advance; Providers discover it and
submit proposals; the requester accepts exactly one proposal, which durably
drives the existing Quote/Job pipeline forward using the requester as
principal and the winning proposal's Capability/version. An OpenTask is never
a parallel commercial contract -- pricing, trust mode and proof requirements
are always resolved by the same `QuoteService.Create` path an ordinary direct
Quote request uses; a proposal's own `proposed_price` is a non-authoritative
hint only.

- `POST /open-tasks` — publish (`open_tasks:write`)
- `GET /open-tasks` — browse public open tasks, or `?mine=true` for the
  caller's own tasks in any status (`open_tasks:read`)
- `GET /open-tasks/{task_id}` (`open_tasks:read`)
- `POST /open-tasks/{task_id}/cancel` — owner only (`open_tasks:write`)
- `POST /open-tasks/{task_id}/proposals` — submit a proposal, provider side
  (`open_task_proposals:write`)
- `GET /open-tasks/{task_id}/proposals` (`open_tasks:read`)
- `POST /open-tasks/{task_id}/proposals/{proposal_id}/withdraw` — provider
  withdraws their own proposal (`open_task_proposals:write`)
- `POST /open-tasks/{task_id}/proposals/{proposal_id}/accept` — owner accepts
  a winner (`open_tasks:write`)

`open_task_proposals:write` (the provider side: submitting or withdrawing a
proposal against someone else's OpenTask) is deliberately a separate,
explicit-grant-only scope from `open_tasks:write` (the owner side: publish,
cancel, accept) -- mirroring `provider_jobs:deliver`'s pattern of never
letting an ordinary consumer scope imply the ability to act as a provider.
`open_tasks:read`/`write` ARE default consumer scopes (publishing a task and
accepting a proposal for one's own task are ordinary consumer actions, the
same as creating or cancelling a Job); `open_task_proposals:write` is not.

Publish, propose and accept require an idempotency key, but as a JSON body
field (`idempotency_key`) rather than the `Idempotency-Key` header used
elsewhere in this document (§1's "or an equivalent body field" convention;
see the request examples below). Withdraw and cancel act on an already
durable record and require no idempotency key of their own.

Example publish request:

```json
{
  "title": "Summarize Q3 filings",
  "description": "...",
  "input": {"document_url": "..."},
  "requested_trust_mode": "managed",
  "proof_requirements": {"network_verifiable_receipt": false},
  "constraints": {"max_total": {"amount": "5.00", "currency": "USD"}},
  "expires_at": "2026-09-01T00:00:00Z",
  "idempotency_key": "task-publish-..."
}
```

`expires_at` is required — an OpenTask MUST NOT be publishable with no
expiry. `input` is the durable payload the eventual Job will use verbatim
once a proposal is accepted; it is never re-derived from a proposal or from
the accept request.

Example public listing entry (`GET /open-tasks`, no `?mine=true`) — `input`
is the only field stripped for this view (never owner-only detail in
general: `title`/`description`/`requested_trust_mode`/`proof_requirements`/
`constraints.max_total` are all public), unlike the owner's own
`GET /open-tasks/{task_id}` view:

```json
{
  "id": "task_...",
  "principal_id": "agt_...",
  "title": "Summarize Q3 filings",
  "description": "...",
  "requested_trust_mode": "managed",
  "constraints": {"max_total": {"amount": "5.00", "currency": "USD"}},
  "status": "open",
  "expires_at": "2026-09-01T00:00:00Z",
  "created_at": "..."
}
```

`status` is one of `open|accepted|fulfilled|cancelled|expired`. `accepted` is
deliberately not terminal: it means a winning proposal has been durably
claimed and the Quote/Job binding sequence is in flight, or — if that
sequence hits a definitive (non-ambiguous) failure — the task reopens to
`open` rather than being stranded.

Example propose request:

```json
{
  "capability_id": "cap_...",
  "message": "...",
  "proposed_price": {"amount": "4.50", "currency": "USD"},
  "idempotency_key": "task-propose-..."
}
```

`capability_version` is never caller-supplied — the proposal freezes the
Capability's current version at propose time. `proposed_price` is a
non-authoritative hint only; `accept` always re-derives the real price
through `QuoteService.Create`'s own pricing rules, bounded by the task's own
`constraints.max_total`, exactly as an ordinary direct Quote request would
be.

Example accept response:

```json
{
  "open_task": {"id": "task_...", "status": "accepted", "accepted_proposal_id": "prop_..."},
  "acceptance": {
    "id": "acceptop_...",
    "task_id": "task_...",
    "proposal_id": "prop_...",
    "checkpoint": "completed",
    "quote_id": "q_...",
    "job_id": "job_..."
  }
}
```

`acceptance.checkpoint` is one of
`intent_persisted|winner_claimed|quote_binding_pending|quote_bound|
job_binding_pending|job_bound|completed|failed|reconciling` — the durable
winner-selection → Quote → Job binding sequence's own checkpoint, mirroring
the execution-signer rotation checkpoint's role in §2.1. Accept is
idempotent: retrying with the same `idempotency_key` resumes the same
`AcceptanceOperation` rather than creating a second Quote/Job.  `open_task`
reaches terminal `status:"fulfilled"` only once `checkpoint` reaches
`completed`; a `checkpoint:"failed"` outcome reopens `open_task` back to
`status:"open"` with `accepted_proposal_id` cleared, never leaving it
permanently `accepted` with no path forward.

## 6. Artifact Endpoints

Optional — see `docs/ARTIFACTS.md`.

- `POST /uploads`
- `POST /uploads/{upload_id}/complete`
- `GET /artifacts/{artifact_id}`
- `GET /artifacts/{artifact_id}/download-url`

Artifact bytes remain off-chain by default. Verified/Native Receipts may include content commitments/hashes.

Signed URLs are temporary transport credentials and MUST NOT be used as durable proof identifiers.

## 7. Account and Receipt Endpoints

- `GET /account`
- `GET /account/usage`
- `GET /account/receipts`
- `GET /receipts/{receipt_id}`
- `GET /receipts/{receipt_id}/execution-proof`
- `GET /receipts/{receipt_id}/settlement-proof`

Account policy MAY include:

```json
{
  "trust_policy":{
    "default_requested_trust_mode":"auto",
    "minimum_for_high_value":"verified"
  }
}
```

Normal account responses do not expose wallet derivation, validator topology, gas units, or private settlement credentials.

Advanced proof endpoints may return normalized proof packages containing provider/capability ownership proof, manifest/Quote commitments, escrow proof, authorized-signer proof, Receipt commitment, settlement proof, and Proof-of-Service references.

## 8. Authentication Endpoints

- `POST /auth/device`
- `POST /auth/device/token`
- `POST /auth/token/refresh`
- `POST /auth/revoke`

Authentication identifies the gateway principal and policy context. It does not determine transaction trust mode by itself.

## 9. Provider Endpoints

- `GET /provider/jobs`
- `POST /provider/jobs/{job_id}/accept`
- `POST /provider/jobs/{job_id}/deliver`
- `POST /provider/jobs/{job_id}/reject`
- `GET /provider/earnings`

Provider operations MUST preserve the Job's Quote-bound concrete trust mode and proof profile.

Mode certification/activation use the dedicated provider/admin execution-signer endpoints defined in §2.1 (Phase 3B); ordinary Capability metadata PATCH cannot bypass ownership, manifest, signer-authorization, proof/settlement, or Native-resolution checks.

## 9A. Identity Binding Endpoints (Phase 4A)

Admin only (`identity_bindings:write` for the mutations, `identity_bindings:read`
for status), explicit-grant-only like `activation:evaluate` -- never a
default consumer or provider scope, and never obtainable through the
passkey/Device Authorization self-service bundle (`docs/AUTH.md`'s "Human
Account Authentication" section explicitly excludes it). These are
gateway-operator actions establishing which TOS Agent Identity a
`principal_id` (gateway account or provider) is bound to
(`docs/IMPLEMENTATION_ROADMAP.md` §8.1, `docs/TOS_RPC.md` §10's
`CreatePrincipalBinding`/`RevokePrincipalBinding`) -- never self-service:
a principal cannot bind itself to an arbitrary claimed TOS identity merely
by being authenticated.

- `POST /v1/identity-bindings/{principal_id}/bind`
- `POST /v1/identity-bindings/{principal_id}/revoke`
- `GET /v1/identity-bindings/{principal_id}`

`POST .../bind` and `POST .../revoke` require `Idempotency-Key` (§1's
universal convention), scoped by the calling admin's own identity, exactly
like §2.2's activation-evaluation endpoint -- never by `principal_id`, since
two different admins independently reusing the identical key string must
not collide.

`POST .../bind` request:

```json
{"agent_id":"agt_..."}
```

`agent_id` MUST already independently resolve through
`IdentityService.ResolveAgentIdentity` -- this endpoint (and the
`CreatePrincipalBinding` RPC underneath it) never creates a new TOS Agent
Identity from nothing; creating one is a separate out-of-band
operator/bootstrap action in Phase 4A. Rebinding a principal that already
has a DIFFERENT current `agent_id` is rejected (`ALREADY_BOUND`) --
`POST .../revoke` must run first.

Response (200, both the newly-created and idempotent-replay case):

```json
{
  "principal_id":"prn_...",
  "agent_id":"agt_...",
  "network":"tos-devnet",
  "binding_ref":"tos:...",
  "created":true
}
```

`POST .../revoke` request:

```json
{"reason_code":"operator_requested"}
```

Response -- `revoked:false` is a normal outcome (nothing was bound), never
an error, mirroring the execution-signer revoke convention:

```json
{"revoked":true,"revocation_ref":"tos:..."}
```

`GET /v1/identity-bindings/{principal_id}` returns the current binding
status without mutating anything:

```json
{
  "principal_id":"prn_...",
  "bound":true,
  "agent_id":"agt_...",
  "network":"tos-devnet",
  "binding_ref":"tos:...",
  "status":"active"
}
```

or, for a never-bound or revoked principal:

```json
{"principal_id":"prn_...","bound":false,"status":"revoked","revocation_reason_code":"operator_requested"}
```

`status` is one of `unspecified|active|revoked`, mirroring
`PrincipalBindingStatus` (`docs/TOS_RPC.md` §10) exactly -- distinguishing
"never bound" (`unspecified`) from "was bound, now revoked" (`revoked`) for
operator audit/UX, even though both states deny Phase 4A activation
identically.

## 10. Public/Metadata Endpoints

- `GET /taxonomy`
- `GET /network/status`
- `GET /providers/{provider_id}/agent-card`

`GET /network/status` SHOULD expose high-level mode availability:

```json
{
  "managed":"available",
  "verified":"available",
  "native":"degraded"
}
```

without requiring ordinary clients to inspect chain internals.

## 11. Error Envelope

```json
{
  "error": {
    "code": "proof_profile_unavailable",
    "message": "The requested verified proof profile is temporarily unavailable.",
    "retryable": true,
    "request_id": "req_...",
    "details": {}
  }
}
```

Important error codes:

- `authentication_required`
- `permission_denied`
- `rate_limited`
- `validation_failed`
- `capability_unavailable`
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
- `provider_failed`
- `settlement_failed`

## 12. REST Invariants

1. `auto` is accepted only before Quote resolution.
2. Quote returns one concrete mode and proof profile when required.
3. Invocation/Job cannot override Quote mode.
4. Receipt returns the concrete mode actually contracted.
5. Provider `requested_trust_modes` does not equal public active `supported_trust_modes`.
6. Verified uses `tos_verified_v1`; Native uses `tos_native_v1` or stronger compatible profiles.
7. Verified/Native failure returns an error or requires re-quote; it never silently falls back to Managed.
