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
    "verified":{"status":"pending","proof_profile":"tos_verified_v1"},
    "native":{"status":"pending","proof_profile":"tos_native_v1"}
  }
}
```

A generic provider PATCH MUST NOT directly force `supported_trust_modes` or certification state to `active`.

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

Mode certification/activation MAY use dedicated provider/admin endpoints later, but ordinary Capability metadata PATCH cannot bypass ownership, manifest, signer-authorization, proof/settlement, or Native-resolution checks.

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
