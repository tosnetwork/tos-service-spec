# ATOS MCP Specification v0.2

## 1. Transport

Preferred production endpoint:

`POST https://mcp.atos.im/mcp`

Use current MCP Streamable HTTP semantics. The server should be horizontally scalable and avoid hidden transport session state. Keep an SSE compatibility endpoint at `https://mcp.atos.im/sse` for older clients during migration.

## 2. Trust-Mode Contract

ATOS v0.2 exposes one MCP surface across all trust modes.

Request-time values:

```text
requested_trust_mode = managed | verified | native | auto
```

Resolved transaction value:

```text
trust_mode = managed | verified | native
```

**`auto` is request-only.** It MUST NOT appear as the resolved trust mode on a Quote, Invocation, Job, Escrow, or Receipt.

The mode becomes immutable at `atos_quote`.

Therefore:

- `atos_search` MAY filter by requested mode/proof requirements;
- `atos_quote` accepts `requested_trust_mode` and resolves it;
- `atos_invoke` and `atos_create_job` MUST NOT accept a replacement `trust_mode` field that could override the Quote;
- results MUST echo the concrete `trust_mode` from the Quote;
- a weaker fallback requires a new Quote.

## 3. Tool Design Principles

- Keep the default tool list small.
- Separate discovery from financially committing operations.
- Use a **Quote** as the immutable commercial/trust contract between search and invocation.
- Every committing call requires `idempotency_key`.
- Return machine-readable structured content, with concise text summaries only as secondary output.
- Use `input_required` when user approval or missing sensitive parameters are needed.
- Do not expose blockchain implementation details in ordinary responses.
- Never silently downgrade `verified`/`native` to a weaker mode.
- Distinguish gateway-computed reputation summaries from network-verifiable proof facts.

## 4. Common Trust/Proof Fields

### Request policy

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

### Resolved quote fields

```json
{
  "requested_trust_mode":"auto",
  "trust_mode":"verified",
  "proof_profile":"tos_verified_v1",
  "proof": {
    "quote_commitment":true,
    "execution_receipt":true,
    "settlement_proof":true,
    "proof_of_service":true
  }
}
```

`proof_profile` MAY be null for `managed`. It is required for standard `verified`/`native` guarantees.

## 5. Default Tools

### 5.1 `atos_search`

Search and rank capabilities.

Input:

```json
{
  "query": "audit a Solidity smart contract",
  "filters": {
    "max_price": {"amount": "10.00", "currency": "USD"},
    "delivery_modes": ["instant", "async"],
    "requested_trust_mode": "auto",
    "proof_requirements": {
      "network_verifiable_receipt": true
    },
    "min_trust_score": 0.8,
    "max_latency_ms": 60000
  },
  "limit": 5
}
```

Output candidate fields:

```json
{
  "matches": [
    {
      "capability_id": "cap_...",
      "name": "Solidity Security Audit",
      "summary": "...",
      "provider": {"id": "agt_...", "name": "AuditAgent"},
      "delivery_mode": "async",
      "supported_trust_modes": ["managed", "verified"],
      "mode_availability": {
        "managed":"online",
        "verified":"online",
        "native":"unsupported"
      },
      "pricing_hint": {"from": "3.00", "currency": "USD"},
      "trust_summary": {
        "score": 0.97,
        "identity_assurance":"tos_attested",
        "proof_of_service_count": 1204
      },
      "latency_hint_ms": 120000,
      "match_score": 0.94
    }
  ],
  "next_cursor": null
}
```

Search does not create an economic commitment and does not resolve `auto` permanently.

### 5.2 `atos_get_capability`

Retrieve full metadata and schemas for one capability.

Input:

```json
{"capability_id":"cap_..."}
```

Returns:

- input/output schemas;
- delivery mode;
- pricing model/hints;
- provider/trust summary;
- `supported_trust_modes` containing only `managed | verified | native`;
- mode availability;
- proof profiles supported by concrete mode;
- transport bindings;
- ownership/manifest commitment metadata where public.

### 5.3 `atos_quote`

Create a short-lived executable Quote and resolve trust mode.

Input:

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

Output:

```json
{
  "quote_id": "q_...",
  "capability_id": "cap_...",
  "capability_version":"1.2.0",
  "provider_id":"agt_...",
  "requested_trust_mode":"auto",
  "trust_mode":"verified",
  "proof_profile":"tos_verified_v1",
  "price": {
    "subtotal": "5.00",
    "fees": "0.25",
    "total_max": "5.25",
    "currency": "USD"
  },
  "settlement": {
    "backend":"tos",
    "escrow":true
  },
  "proof": {
    "quote_commitment":true,
    "execution_receipt":true,
    "settlement_proof":true,
    "proof_of_service":true
  },
  "expires_at": "2026-08-07T05:10:00Z",
  "requires_confirmation": false,
  "terms_hash": "sha256:...",
  "dispute_policy_hash":"sha256:..."
}
```

Rules:

1. If `requested_trust_mode` is concrete, the Quote MUST use that mode or fail.
2. If it is `auto`, the gateway chooses the cheapest/most suitable concrete mode satisfying all constraints.
3. The returned `trust_mode` is immutable for the Quote.
4. For `verified`/`native`, the Quote MUST NOT be returned unless the selected proof profile is currently satisfiable.
5. Network/proof unavailability is an error, not permission to weaken the caller's requirements.

### 5.4 `atos_invoke`

Execute a bounded, normally synchronous capability using a Quote.

Input:

```json
{
  "capability_id": "cap_...",
  "quote_id": "q_...",
  "input": {"text": "..."},
  "idempotency_key": "0198...",
  "max_wait_ms": 45000
}
```

`trust_mode` is intentionally absent from the input. The Quote is authoritative.

Possible result types:

- `completed`
- `accepted` (converted to async Job)
- `input_required`
- `failed`

Completed output:

```json
{
  "result_type": "completed",
  "invocation_id": "inv_...",
  "quote_id":"q_...",
  "trust_mode":"verified",
  "output": {},
  "artifacts": [],
  "receipt": {
    "receipt_id":"rcpt_...",
    "quote_id": "q_...",
    "trust_mode":"verified",
    "charged": {"amount":"5.25","currency":"USD"},
    "proof_status":"verified",
    "network_proof_ref":"tos:..."
  }
}
```

For Managed Mode, `network_proof_ref` MAY be absent/null.

### 5.5 `atos_create_job`

Create long-running or interactive work.

Input:

```json
{
  "capability_id": "cap_...",
  "quote_id": "q_...",
  "input": {},
  "idempotency_key": "0198...",
  "callback": null
}
```

Again, mode is inherited from the Quote and cannot be overridden.

Output:

```json
{
  "job_id": "job_...",
  "quote_id":"q_...",
  "trust_mode":"native",
  "proof_profile":"tos_verified_v1",
  "state": "submitted",
  "created_at": "...",
  "estimated_completion_at": "..."
}
```

`callback` is reserved and unimplemented in Phase 1/2. Clients MUST omit it or pass `null`; servers MUST reject a non-null value with `validation_failed` until webhook delivery ships.

When implemented, the shape is:

```json
{
  "callback": {
    "url": "https://client.example/webhooks/atos",
    "events": ["job.completed", "job.failed", "job.input_required"],
    "secret_ref": "whsec_..."
  }
}
```

`secret_ref` identifies a client-registered signing secret; the secret value itself is never returned in Job records.

### 5.6 `atos_get_job`

Input:

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

Response MUST include the concrete `trust_mode` inherited from the Quote. For `verified`/`native`, the response SHOULD also expose compact proof progress/status without requiring chain-specific reasoning.

Example:

```json
{
  "job_id":"job_...",
  "trust_mode":"verified",
  "state":"working",
  "proof_status": {
    "quote":"committed",
    "escrow":"reserved",
    "receipt":"pending",
    "settlement":"pending"
  }
}
```

### 5.7 `atos_cancel_job`

Input:

```json
{
  "job_id":"job_...",
  "reason":"no longer needed",
  "idempotency_key":"0198..."
}
```

Cancellation uses the Job's existing concrete mode. A Verified/Native refund/release MUST follow that mode's settlement guarantees. Cancellation MUST NOT downgrade the transaction to Managed accounting.

### 5.8 `atos_register_capability`

Provider-side registration.

Input includes:

- name/description/tags;
- input/output schemas;
- pricing;
- delivery mode;
- endpoint bindings;
- visibility;
- requested `supported_trust_modes` containing only concrete values.

Example:

```json
{
  "name":"Document Translation",
  "description":"...",
  "delivery_mode":"async",
  "input_schema":{"type":"object"},
  "output_schema":{"type":"object"},
  "pricing":{"model":"per_unit"},
  "supported_trust_modes":["managed","verified"],
  "bindings":[
    {"transport":"http","endpoint_ref":"ep_...","trust_modes":["managed","verified"]}
  ]
}
```

Requesting a trust mode does not mean it is immediately active. Verified/Native activation requires the guarantees defined in `docs/CAPABILITIES.md` and `docs/ARCHITECTURE_V0.2.md`.

### 5.9 `atos_update_capability`

Partial provider-side update.

Immutable identity/ownership fields cannot be changed through an ordinary patch.

Adding or activating `verified`/`native` MUST pass the corresponding ownership/proof/resolution validation; a generic metadata PATCH cannot bypass certification.

### 5.10 `atos_account`

Read-only account summary.

```json
{
  "balance": {"available":"25.00","currency":"USD"},
  "spend_policy": {
    "per_call_autonomous_limit":"2.00",
    "daily_limit":"20.00",
    "remaining_today":"17.50"
  },
  "trust_policy": {
    "default_requested_trust_mode":"auto",
    "minimum_for_high_value":"verified"
  },
  "provider_earnings": null
}
```

Normal account output should not expose wallet derivation, gas, validators, or internal settlement keys.

## 6. Required Error Semantics

ATOS v0.2 adds explicit trust/proof failures.

Recommended machine codes:

- `trust_mode_unavailable` — capability does not currently support the requested concrete mode.
- `proof_requirements_unsatisfied` — no mode/provider can satisfy requested proof properties.
- `proof_profile_unavailable` — required proof backend/profile is temporarily unavailable.
- `network_unavailable` — TOS-backed operation cannot currently meet the Quote contract.
- `quote_mode_mismatch` — caller attempts execution inconsistent with Quote mode.
- `requote_required` — a different trust mode/price/terms would be needed.

A server MUST NOT convert these failures into a weaker successful execution without a new Quote.

## 7. Optional Provider/Admin Tools

Expose only to principals with matching scopes:

- `atos_list_my_capabilities`
- `atos_pause_capability`
- `atos_provider_jobs`
- `atos_deliver_job`
- `atos_request_settlement`
- `atos_dispute_job`

Provider/admin settlement tools MUST preserve the Quote/Job concrete trust mode and proof profile.

## 8. Optional File Transfer Tools

See `docs/ARTIFACTS.md` for the object model.

Binary bytes never travel through an MCP tool call. Signed URLs are used for upload/download.

Artifacts remain off-chain by default. Verified/Native flows MAY commit artifact hashes/commitments to the Execution Receipt according to the selected proof profile.

### `atos_create_upload`

```json
{
  "content_type": "application/pdf",
  "size_bytes": 2140233,
  "purpose": "job_input"
}
```

### `atos_complete_upload`

```json
{"upload_id": "up_..."}
```

Returns:

```json
{
  "artifact_id": "art_...",
  "content_type": "application/pdf",
  "size_bytes": 2140233,
  "sha256": "..."
}
```

### `atos_get_download_url`

```json
{"artifact_id":"art_..."}
```

Returns a short-lived signed URL and artifact metadata.

## 9. MCP Resources

Recommended resources:

- `atos://taxonomy`
- `atos://capabilities/trending`
- `atos://account/policy`
- `atos://network/status`
- `atos://docs/protocol-version`

`atos://network/status` SHOULD report whether `managed`, `verified`, and `native` infrastructure is currently available without exposing unnecessary chain internals.

Example:

```json
{
  "managed":"available",
  "verified":"available",
  "native":"degraded"
}
```

## 10. MCP Prompts

Optional prompts:

- `atos-find-specialist`
- `atos-publish-capability`
- `atos-compare-quotes`

Prompts are convenience templates, not business APIs.

## 11. Spend Confirmation via MCP Elicitation

When the requested amount exceeds autonomous policy, return an MCP multi-round-trip response conceptually equivalent to:

```json
{
  "resultType": "input_required",
  "inputRequests": {
    "confirm_purchase": {
      "type": "elicitation",
      "message": "This verified capability costs up to USD 8.25. Approve?",
      "schema": {"type":"boolean"}
    }
  },
  "requestState": "opaque-signed-state"
}
```

The confirmation MUST bind to the Quote ID, concrete trust mode, maximum amount, and Quote expiry so an approval for one mode cannot be replayed for another.

## 12. Idempotency

`atos_invoke`, `atos_create_job`, `atos_cancel_job`, registration mutations and settlement mutations MUST require `idempotency_key`.

Server behavior:

- same principal + same key + same request hash => return original result;
- same principal + same key + different request hash => `409 idempotency_conflict`;
- store keys for at least the maximum financial dispute/retry window.

For committing operations, the request hash or idempotency record MUST indirectly bind the Quote and therefore the resolved concrete trust mode.

## 13. MCP Invariants

1. The default surface remains 10 tools.
2. `auto` is only a request policy value.
3. `atos_quote` resolves and freezes a concrete mode.
4. Invoke/Job creation inherit mode from Quote and cannot override it.
5. Verified/Native proof failure is a failure/requote, never a silent Managed fallback.
6. Bulk payloads remain off-chain; receipts may commit their hashes.
7. Normal MCP clients see proof status/references, not blockchain plumbing.
8. Trust/reputation summaries are distinct from transaction trust mode.
