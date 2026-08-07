# ATOS REST API v1 — Protocol Semantics v0.2

Base URL:

`https://api.atos.im/v1`

## Conventions

- JSON request/response.
- Bearer authentication except public discovery/card endpoints.
- RFC-style HTTP status codes.
- Financial mutations require `Idempotency-Key` header or equivalent body field.
- Cursor pagination for lists.
- Errors use stable machine codes.
- `requested_trust_mode` is a pre-Quote policy value: `managed | verified | native | auto`.
- `trust_mode` is a resolved transaction value: `managed | verified | native`.
- `auto` MUST resolve at Quote time and MUST NOT appear as a final Invocation/Job/Receipt mode.
- Invocation/Job creation inherits trust mode from the Quote; callers cannot override it.
- Verified/Native operations MUST NOT silently downgrade to Managed.

## Capability Endpoints

- `GET /capabilities?q=...`
- `GET /capabilities/{capability_id}`
- `POST /capabilities` — provider create
- `PATCH /capabilities/{capability_id}` — provider update
- `POST /capabilities/{capability_id}/pause`
- `POST /capabilities/{capability_id}/resume`

Discovery filters MAY include:

```text
requested_trust_mode=managed|verified|native|auto
network_verifiable_receipt=true|false
tos_settlement=true|false
```

Capability responses include `supported_trust_modes` containing only concrete values and SHOULD expose per-mode availability/proof-profile information.

## Quote Endpoints

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

Example response:

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
  "settlement":{"backend":"tos","escrow":true},
  "proof":{"execution_receipt":true,"settlement_proof":true},
  "expires_at":"...",
  "terms_hash":"sha256:...",
  "dispute_policy_hash":"sha256:..."
}
```

The returned concrete `trust_mode` is immutable for that Quote.

## Invocation Endpoints

- `POST /invocations`
- `GET /invocations/{invocation_id}`

Creation request includes `quote_id`, `capability_id`, input and idempotency key/header. It MUST NOT accept a caller-provided trust-mode override.

Invocation responses include the concrete `trust_mode` inherited from the Quote.

## Job Endpoints

- `POST /jobs`
- `GET /jobs/{job_id}`
- `POST /jobs/{job_id}/cancel`
- `POST /jobs/{job_id}/messages`
- `GET /jobs/{job_id}/artifacts`

Every Job stores and returns the concrete Quote `trust_mode` and MAY expose compact `proof_status`.

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

Cancellation/refund follows the existing Job mode. A Verified/Native Job cannot be canceled by silently moving its economic state to a Managed ledger.

## Artifact Endpoints

Optional — see `docs/ARTIFACTS.md`. Upload/download transfers bytes over signed URLs; API endpoints issue/verify references.

- `POST /uploads`
- `POST /uploads/{upload_id}/complete`
- `GET /artifacts/{artifact_id}`
- `GET /artifacts/{artifact_id}/download-url`

Artifact bytes remain off-chain by default. Verified/Native receipts may contain content commitments/hashes.

## Account Endpoints

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

## Authentication Endpoints

- `POST /auth/device`
- `POST /auth/device/token`
- `POST /auth/token/refresh`
- `POST /auth/revoke`

Authentication identifies the principal and policy context. It does not by itself determine a transaction trust mode.

## Provider Endpoints

- `GET /provider/jobs`
- `POST /provider/jobs/{job_id}/accept`
- `POST /provider/jobs/{job_id}/deliver`
- `POST /provider/jobs/{job_id}/reject`
- `GET /provider/earnings`

Provider operations MUST preserve the Job's Quote-bound trust mode and proof profile.

Mode activation/certification MAY use provider/admin endpoints added later, but generic metadata PATCH MUST NOT bypass Verified/Native eligibility checks.

## Public/Metadata Endpoints

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

## Error Envelope

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

## REST Invariants

1. `auto` is accepted only before Quote resolution.
2. Quote returns one concrete mode.
3. Invocation/Job cannot override Quote mode.
4. Receipt returns the concrete mode actually contracted.
5. Verified/Native failure returns an error or requires re-quote; it never silently falls back to Managed.
