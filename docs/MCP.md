# ATOS MCP Specification

## Transport

Preferred production endpoint:

`POST https://mcp.atos.im/mcp`

Use current MCP Streamable HTTP semantics. The server should be horizontally scalable and avoid hidden transport session state. Keep an SSE compatibility endpoint at `https://mcp.atos.im/sse` for older clients during migration.

## Tool Design Principles

- Keep the default tool list small.
- Separate discovery from financially committing operations.
- Use a **Quote** as the commercial contract between search and invocation.
- Every committing call requires `idempotency_key`.
- Return machine-readable structured content, with concise text summaries only as secondary output.
- Use `input_required` when user approval or missing sensitive parameters are needed.
- Do not return blockchain implementation details in normal responses.

## Default Tools

### 1. `atos_search`

Search and rank capabilities.

Input:

```json
{
  "query": "audit a Solidity smart contract",
  "filters": {
    "max_price": {"amount": "10.00", "currency": "USD"},
    "delivery_modes": ["instant", "async"],
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
      "pricing_hint": {"from": "3.00", "currency": "USD"},
      "trust": {"score": 0.97, "level": "verified"},
      "latency_hint_ms": 120000,
      "match_score": 0.94
    }
  ],
  "next_cursor": null
}
```

### 2. `atos_get_capability`

Retrieve full metadata and schemas for one capability.

Input:

```json
{"capability_id":"cap_..."}
```

Returns `input_schema`, `output_schema`, policies, supported modalities, provider trust, SLA and pricing model.

### 3. `atos_quote`

Create a short-lived executable quote.

Input:

```json
{
  "capability_id": "cap_...",
  "input_summary": {"bytes": 140233, "pages": 38},
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
  "price": {
    "subtotal": "5.00",
    "fees": "0.25",
    "total_max": "5.25",
    "currency": "USD"
  },
  "expires_at": "2026-08-07T05:10:00Z",
  "requires_confirmation": false,
  "terms_hash": "sha256:..."
}
```

### 4. `atos_invoke`

Execute a bounded, normally synchronous capability.

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

Possible result types:

- `completed`
- `accepted` (converted to async job)
- `input_required`
- `failed`

Completed output:

```json
{
  "result_type": "completed",
  "invocation_id": "inv_...",
  "output": {},
  "artifacts": [],
  "receipt": {
    "quote_id": "q_...",
    "charged": "5.25",
    "currency": "USD"
  }
}
```

### 5. `atos_create_job`

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

Output:

```json
{
  "job_id": "job_...",
  "state": "submitted",
  "created_at": "...",
  "estimated_completion_at": "..."
}
```

### 6. `atos_get_job`

```json
{"job_id":"job_..."}
```

Canonical states:

`submitted -> working -> input_required -> working -> completed`

Terminal alternatives: `failed`, `canceled`, `rejected`.

### 7. `atos_cancel_job`

```json
{
  "job_id":"job_...",
  "reason":"no longer needed",
  "idempotency_key":"0198..."
}
```

### 8. `atos_register_capability`

Provider-side registration.

Input contains name, description, tags, schemas, pricing, delivery mode, endpoint binding and visibility.

### 9. `atos_update_capability`

Partial provider-side update; immutable identity and ownership fields cannot be changed via this tool.

### 10. `atos_account`

Read-only account summary:

```json
{
  "balance": {"available":"25.00","currency":"USD"},
  "spend_policy": {
    "per_call_autonomous_limit":"2.00",
    "daily_limit":"20.00",
    "remaining_today":"17.50"
  },
  "provider_earnings": null
}
```

## Optional Provider/Admin Tools

Expose only to principals with matching scopes:

- `atos_list_my_capabilities`
- `atos_pause_capability`
- `atos_provider_jobs`
- `atos_deliver_job`
- `atos_request_settlement`
- `atos_dispute_job`

Do not burden ordinary Codex clients with these tools.

## MCP Resources

Recommended resources:

- `atos://taxonomy`
- `atos://capabilities/trending`
- `atos://account/policy`
- `atos://network/status`
- `atos://docs/protocol-version`

Resources should be read-only and cacheable where possible.

## MCP Prompts

Optional prompts:

- `atos-find-specialist`
- `atos-publish-capability`
- `atos-compare-quotes`

Prompts are convenience templates, not business APIs.

## Spend Confirmation via MRTR

When the requested amount exceeds autonomous policy, return an MCP multi-round-trip response conceptually equivalent to:

```json
{
  "resultType": "input_required",
  "inputRequests": {
    "confirm_purchase": {
      "type": "elicitation",
      "message": "This capability costs up to USD 8.25. Approve?",
      "schema": {"type":"boolean"}
    }
  },
  "requestState": "opaque-signed-state"
}
```

The client reissues the original call with the response. The server validates the signed `requestState` and quote expiry.

## Idempotency

`atos_invoke`, `atos_create_job`, `atos_cancel_job`, registration mutations and settlement mutations MUST require `idempotency_key`.

Server behavior:

- Same principal + same key + same request hash => return original result.
- Same principal + same key + different request hash => `409 idempotency_conflict`.
- Store keys for at least the maximum financial dispute/retry window.
