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

Mode certification/activation use the dedicated provider/admin execution-signer endpoints defined in §2.1 (Phase 3B); ordinary Capability metadata PATCH cannot bypass ownership, manifest, signer-authorization, proof/settlement, or Native-resolution checks.

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
