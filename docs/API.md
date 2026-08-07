# ATOS REST API v1

Base URL:

`https://api.atos.im/v1`

## Conventions

- JSON request/response.
- Bearer authentication except public discovery/card endpoints.
- RFC-style HTTP status codes.
- Financial mutations require `Idempotency-Key` header or equivalent body field.
- Cursor pagination for lists.
- Errors use stable machine codes.

## Capability Endpoints

- `GET /capabilities?q=...`
- `GET /capabilities/{capability_id}`
- `POST /capabilities` — provider create
- `PATCH /capabilities/{capability_id}` — provider update
- `POST /capabilities/{capability_id}/pause`
- `POST /capabilities/{capability_id}/resume`

## Quote Endpoints

- `POST /quotes`
- `GET /quotes/{quote_id}`

## Invocation Endpoints

- `POST /invocations`
- `GET /invocations/{invocation_id}`

## Job Endpoints

- `POST /jobs`
- `GET /jobs/{job_id}`
- `POST /jobs/{job_id}/cancel`
- `POST /jobs/{job_id}/messages`
- `GET /jobs/{job_id}/artifacts`

## Artifact Endpoints

Optional — see `docs/ARTIFACTS.md`. Every upload/download exchanges
bytes over a signed URL directly with storage; these endpoints only
issue/verify those URLs.

- `POST /uploads` — request a signed upload target
- `POST /uploads/{upload_id}/complete` — finalize, returns `artifact_id`
- `GET /artifacts/{artifact_id}` — metadata
- `GET /artifacts/{artifact_id}/download-url` — signed download URL

## Account Endpoints

- `GET /account`
- `GET /account/usage`
- `GET /account/receipts`
- `GET /receipts/{receipt_id}`
- `GET /receipts/{receipt_id}/settlement-proof` — optional advanced proof

## Authentication Endpoints

- `POST /auth/device`
- `POST /auth/device/token`
- `POST /auth/token/refresh`
- `POST /auth/revoke`

## Provider Endpoints

- `GET /provider/jobs`
- `POST /provider/jobs/{job_id}/accept`
- `POST /provider/jobs/{job_id}/deliver`
- `POST /provider/jobs/{job_id}/reject`
- `GET /provider/earnings`

## Public/Metadata Endpoints

- `GET /taxonomy`
- `GET /network/status`
- `GET /providers/{provider_id}/agent-card`

## Error Envelope

```json
{
  "error": {
    "code": "quote_expired",
    "message": "The selected quote has expired.",
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
- `quote_expired`
- `quote_mismatch`
- `spend_limit_exceeded`
- `insufficient_balance`
- `idempotency_conflict`
- `job_not_cancelable`
- `provider_failed`
- `settlement_failed`
