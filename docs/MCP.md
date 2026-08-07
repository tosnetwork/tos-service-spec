# ATOS MCP Specification

## Transport

Preferred production endpoint:

`POST https://mcp.atos.im/mcp`

Use current MCP Streamable HTTP semantics. The server should be horizontally scalable and avoid hidden transport session state. Keep an SSE compatibility endpoint at `https://mcp.atos.im/sse` for older clients during migration.

## Tool Design Principles

- Keep the always-visible tool list small — but never hide a tool nobody
  can then discover. `tools/list` is what a real client uses to decide
  what it may call; a tool absent from every possible `tools/list`
  response is not "optional," it is unreachable dead code (confirmed
  against a real MCP client — see "Per-Caller Tool Visibility" below).
- Separate discovery from financially committing operations.
- Use a **Quote** as the commercial contract between search and invocation.
- Every committing call requires `idempotency_key`.
- Return machine-readable structured content, with concise text summaries only as secondary output.
- Use `input_required` when user approval or missing sensitive parameters are needed.
- Do not return blockchain implementation details in normal responses.

## Per-Caller Tool Visibility

`tools/list` is a session-scoped response, not a fixed constant — a
server is expected to tailor it to the authenticated caller. This spec
distinguishes two different reasons a tool might not belong in every
response, and handles them differently:

- **Cost/routing concern** (file transfer tools): any caller might
  legitimately need these for any capability with a file-typed schema
  field. There is no reliable per-caller signal to gate them on, so they
  are simply part of the always-visible surface — see "Default Tools"
  below, which now includes them.
- **Authorization concern** (provider/admin tools): only a caller that
  actually owns at least one capability has any use for
  `atos_pause_capability` etc. These ARE conditionally included, computed
  per request from the caller's real ownership state — not by a static
  "optional" list that never actually appears in `tools/list`. See
  "Provider/Admin Tools" below.

An earlier draft of this spec kept both categories out of the default
`tools/list` unconditionally, intending "discoverable when relevant."
Testing against a real MCP client showed that produces tools no client
can ever call, since none of them re-request an unlisted tool by guessing
its name. Always-visible-but-honest beats hidden-but-dead.

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

`callback` is **reserved and unimplemented in Phase 1/2**; the only supported way to learn
a job's state is polling `atos_get_job`. Clients MUST omit it or pass `null` — servers
MUST reject any non-null value with `validation_failed` until webhook delivery ships.
When implemented (Phase 3+, alongside `docs/IMPLEMENTATION_ROADMAP.md`'s provider
self-service phase), the shape will be:

```json
{
  "callback": {
    "url": "https://client.example/webhooks/atos",
    "events": ["job.completed", "job.failed", "job.input_required"],
    "secret_ref": "whsec_..."
  }
}
```

`secret_ref` identifies a client-registered signing secret used to sign the webhook body
(never the secret value itself, which is never round-tripped through job records).

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

### 11. `atos_artifact`

One tool for `docs/ARTIFACTS.md`'s three-step signed-URL flow, not three.
From a model's perspective, requesting an upload target, finalizing it,
and fetching a download link are one intent — "work with an ATOS
artifact" — not three separate ones. An earlier draft exposed these as
three always-visible tools (13 total); collapsing them to one
`operation`-dispatched tool keeps the default surface at 11 while still
being always-visible for the reason given in "Per-Caller Tool
Visibility" above (file I/O isn't an authorization concern, so there's
no reliable per-caller signal to gate it on instead).

Binary bytes never travel through this call itself; every operation
returns or consumes a signed HTTP URL the client uses directly, the same
reason the other default tools never accept inline file content either.

Input carries `operation` plus only the fields that operation needs; a
server validates the operation-specific required fields itself rather
than leaning on an ever-looser top-level JSON Schema to catch it.

**`operation: "create_upload"`** — requests a short-lived signed upload target.

```json
{"operation": "create_upload", "content_type": "application/pdf", "size_bytes": 2140233, "purpose": "job_input"}
```

```json
{"upload_id": "up_...", "upload_url": "https://...", "upload_method": "PUT", "expires_at": "2026-08-07T05:10:00Z"}
```

**`operation: "complete_upload"`** — finalizes an upload after the client
has PUT the bytes to `upload_url`, returning a stable reference usable in
a capability's `input`.

```json
{"operation": "complete_upload", "upload_id": "up_..."}
```

```json
{"artifact_id": "art_...", "content_type": "application/pdf", "size_bytes": 2140233, "sha256": "..."}
```

An `atos_invoke`/`atos_create_job` call then references the upload as
part of `input`, e.g. `{"document": {"artifact_id": "art_..."}}` — the
capability's `input_schema` declares which fields are artifact
references.

**`operation: "get_download_url"`** — returns a short-lived signed
download URL for an artifact the caller owns — either something it
uploaded, or an artifact produced in a job's `artifacts` output.

```json
{"operation": "get_download_url", "artifact_id": "art_..."}
```

```json
{"download_url": "https://...", "expires_at": "2026-08-07T05:10:00Z", "content_type": "application/pdf", "size_bytes": 891004}
```

## Provider/Admin Tools

Unlike the 13 tools above, these are genuinely conditional — computed
into `tools/list` per request rather than statically returned, per
"Per-Caller Tool Visibility." A server determines eligibility from the
same fact that governs whether the tool would succeed if called: does
this authenticated principal actually own at least one capability. That
check is cheap (an existing lookup, not new state) and cannot be spoofed
into granting access it wouldn't otherwise enforce, since
`atos_pause_capability` itself re-checks ownership before acting.

Implemented (Phase 3, gated as above):

- `atos_list_my_capabilities`
- `atos_pause_capability`

Specified but not yet implemented — depend on a real queued/matched
provider model that doesn't exist before Phase 3's task marketplace (see
`docs/IMPLEMENTATION_ROADMAP.md`); the same per-principal-ownership
gating applies once they exist:

- `atos_provider_jobs`
- `atos_deliver_job`
- `atos_request_settlement`
- `atos_dispute_job`

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
