# ATOS MCP Specification v0.2

## 1. Transport

Preferred production endpoint:

`POST https://mcp.atos.im/mcp`

Use current MCP Streamable HTTP semantics. The server should be horizontally scalable and avoid hidden transport session state. Keep `https://mcp.atos.im/sse` only as a legacy compatibility adapter during migration.

## 2. Trust-Mode Contract

ATOS v0.2 exposes one MCP surface across all trust modes.

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

## 4. Tool Design Principles

- Keep the default tool list small.
- Separate discovery from financially committing operations.
- Use a **Quote** as the immutable commercial/trust contract between search and execution.
- Every committing call requires `idempotency_key`.
- Return machine-readable structured content; concise text summaries are secondary.
- Use MCP `input_required`/elicitation when user approval or missing sensitive parameters are needed.
- Do not expose blockchain implementation details in ordinary responses.
- Never silently downgrade `verified`/`native` to a weaker mode.
- Distinguish gateway-computed reputation summaries from TOS-verifiable proof facts.
- Keep bulk/private payloads off-chain; Verified/Native receipts carry commitments when required.
- **Never hide a tool nobody can then discover.** `tools/list` is what a real client uses to decide what it may call; a tool absent from every possible `tools/list` response is not "optional," it is unreachable. This spec distinguishes two different reasons a tool might not belong in the always-visible default set, and handles them differently:
  - *Cost/routing concern* (§ 6.11 `atos_artifact`): any caller might legitimately need it for any Capability with a file-typed schema field. There is no reliable per-caller signal to gate it on, so it is simply part of the always-visible default surface.
  - *Authorization concern* (§ 8 provider/admin tools): only a caller that actually owns a Capability has any use for these. These ARE conditionally included, computed per request from the caller's real ownership state.

## 5. Common Resolved Quote Fields

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

## 6. Default Tools

### 6.1 `atos_search`

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

`atos_search` does not create an economic commitment and does not permanently resolve `auto`.

`supported_trust_modes` contains only modes that are currently active and quotable for the capability.

### 6.2 `atos_get_capability`

Input:

```json
{"capability_id":"cap_..."}
```

Returns:

- input/output schemas;
- delivery mode;
- pricing model/hints;
- provider and `trust_summary`;
- active `supported_trust_modes` containing only `managed | verified | native`;
- `mode_support` state;
- proof profiles supported by active concrete modes;
- transport bindings;
- ownership/manifest commitment metadata where public.

### 6.3 `atos_quote`

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

Verified example output:

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
    "escrow":true,
    "funding_model":"gateway_sponsored"
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
2. If it is `auto`, the gateway chooses a concrete mode satisfying all request constraints.
3. The returned `trust_mode` is immutable for the Quote.
4. A Verified Quote uses `tos_verified_v1` or stronger.
5. A Native Quote uses `tos_native_v1` or stronger.
6. A Verified/Native Quote MUST NOT be returned unless the required proof/settlement path is currently satisfiable.
7. Network/proof unavailability is an error, not permission to weaken requirements.

### 6.4 `atos_invoke`

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
- `accepted` — converted to async Job
- `input_required`
- `failed`

Completed Verified output:

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
    "proof_profile":"tos_verified_v1",
    "charged": {"amount":"5.25","currency":"USD"},
    "execution_signer_id":"sig_...",
    "signer_authorization_ref":"tos:...",
    "proof_status":"verified",
    "network_proof_ref":"tos:..."
  }
}
```

The execution signer may be the provider or an authorized delegated runtime/adapter. Verified/Native proof must establish signer authority for the quoted provider/capability/version.

For Managed Mode, TOS proof references may be absent.

### 6.5 `atos_create_job`

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

Mode is inherited from the Quote and cannot be overridden.

Native example output:

```json
{
  "job_id": "job_...",
  "quote_id":"q_...",
  "trust_mode":"native",
  "proof_profile":"tos_native_v1",
  "state": "submitted",
  "created_at": "...",
  "estimated_completion_at": "..."
}
```

`callback` is reserved and unimplemented in the initial phases. Clients MUST omit it or pass `null`; servers MUST reject a non-null value with `validation_failed` until webhook delivery ships.

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

`secret_ref` identifies a registered webhook-signing secret; the secret value itself is never returned in Job records.

### 6.6 `atos_get_job`

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

Response MUST include the concrete `trust_mode` inherited from the Quote. For `verified`/`native`, response SHOULD expose compact proof progress/status.

```json
{
  "job_id":"job_...",
  "trust_mode":"verified",
  "proof_profile":"tos_verified_v1",
  "state":"working",
  "proof_status": {
    "quote":"committed",
    "escrow":"reserved",
    "receipt":"pending",
    "settlement":"pending"
  }
}
```

### 6.7 `atos_cancel_job`

Input:

```json
{
  "job_id":"job_...",
  "reason":"no longer needed",
  "idempotency_key":"0198..."
}
```

Cancellation uses the Job's existing concrete mode. Verified/Native release/refund MUST follow that mode's settlement guarantees. Cancellation MUST NOT downgrade the transaction to Managed accounting.

### 6.8 `atos_register_capability`

Provider-side registration requests desired concrete trust modes; it does not self-certify active modes.

Input includes:

- name/description/tags;
- input/output schemas;
- pricing;
- delivery mode;
- endpoint bindings;
- visibility;
- `requested_trust_modes`, containing only `managed | verified | native`.

Example:

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

Rules:

- `requested_trust_modes` is provider intent.
- `supported_trust_modes` is the derived set of `active` modes.
- `eligible_trust_modes` on a transport binding means technical eligibility, not certification.
- `auto` is invalid in provider concrete-mode sets.
- Verified/Native activation requires the guarantees in `docs/CAPABILITIES.md`, `docs/ARCHITECTURE_V0.2.md`, and `docs/PROOF_PROFILES.md`.

### 6.9 `atos_update_capability`

Partial provider-side update.

Immutable identity/ownership fields cannot be changed through an ordinary patch.

Providers may update `requested_trust_modes`. They MUST NOT directly force `supported_trust_modes` or `mode_support.status=active` through a generic metadata patch.

Verified/Native activation must pass ownership, manifest, proof-profile, signer-authorization, settlement, and Native-resolution checks as applicable.

### 6.10 `atos_account`

Read-only account summary:

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

### 6.11 `atos_artifact`

One tool for `docs/ARTIFACTS.md`'s three-step signed-URL flow, not three. From a model's perspective, requesting an upload target, finalizing it, and fetching a download link are one intent — "work with an ATOS artifact" — not three separate ones. Collapsing them to one `operation`-dispatched tool keeps the default surface at 11 while staying always-visible per § 4's "Per-Caller Tool Visibility" principle (file I/O isn't an authorization concern, so there's no reliable per-caller signal to gate it on instead).

Binary bytes never travel through this call itself; every operation returns or consumes a signed HTTP URL the client uses directly. Artifacts remain off-chain by default; Verified/Native receipts may commit content hashes according to the selected proof profile. Input carries `operation` plus only the fields that operation needs; a server validates the operation-specific required fields itself rather than leaning on an ever-looser top-level JSON Schema to catch it.

**`operation: "create_upload"`** — requests a short-lived signed upload target. `size_bytes` MUST be bounded before a signed URL is issued.

```json
{"operation": "create_upload", "content_type": "application/pdf", "size_bytes": 2140233, "purpose": "job_input"}
```

```json
{"upload_id": "up_...", "upload_url": "https://...", "upload_method": "PUT", "expires_at": "2026-08-07T05:10:00Z"}
```

**`operation: "complete_upload"`** — finalizes an upload after the client has PUT the bytes to `upload_url`, returning a stable `artifact_id` and content commitment usable in a Capability's `input`.

```json
{"operation": "complete_upload", "upload_id": "up_..."}
```

```json
{"artifact_id": "art_...", "content_type": "application/pdf", "size_bytes": 2140233, "sha256": "..."}
```

**`operation: "get_download_url"`** — returns a short-lived authorized download URL and artifact metadata for an artifact the caller is authorized to access — either something it uploaded, or an artifact produced in a Job's output.

```json
{"operation": "get_download_url", "artifact_id": "art_..."}
```

```json
{"download_url": "https://...", "expires_at": "2026-08-07T05:10:00Z", "content_type": "application/pdf", "size_bytes": 891004}
```

## 7. Required Error Semantics

Recommended machine codes:

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

A server MUST NOT turn a trust/proof failure into a weaker successful execution without a new Quote.

## 8. Provider/Admin Tools (Dynamically Gated)

Unlike § 6's default tools, these are genuinely conditional: `tools/list`
is computed per request from the authenticated principal, and includes
them only when that principal actually owns at least one Capability —
the same fact that governs whether the tool would succeed if called
(`atos_pause_capability` re-checks ownership before acting regardless).
This is the real MCP mechanism for per-caller tool visibility: the
`tools/list` response is a function of who is asking, not a static
constant. See § 4's "Per-Caller Tool Visibility" principle for why this
differs from how § 6.11 (`atos_artifact`) is handled.

Implemented, gated as above:

- `atos_list_my_capabilities`
- `atos_pause_capability`

Specified but not yet implemented — depend on a real queued/matched
provider model that doesn't exist yet; the same ownership gating applies
once they do:

- `atos_provider_jobs`
- `atos_deliver_job`
- `atos_request_settlement`
- `atos_dispute_job`

Provider/admin settlement operations MUST preserve the Quote/Job concrete trust mode and proof profile.

## 9. MCP Resources

Recommended resources:

- `atos://taxonomy`
- `atos://capabilities/trending`
- `atos://account/policy`
- `atos://network/status`
- `atos://docs/protocol-version`

`atos://network/status` SHOULD expose high-level mode availability without chain plumbing:

```json
{
  "managed":"available",
  "verified":"available",
  "native":"degraded"
}
```

## 10. MCP Prompts

Optional convenience prompts:

- `atos-find-specialist`
- `atos-publish-capability`
- `atos-compare-quotes`

Prompts are not business APIs.

## 11. Spend Confirmation via MCP Elicitation

When a Quote exceeds autonomous policy, return an MCP multi-round-trip response conceptually equivalent to:

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

The confirmation state MUST bind to Quote ID, concrete trust mode, proof profile, maximum amount, and Quote expiry so approval for one contract cannot be replayed for another.

## 12. Idempotency

`atos_invoke`, `atos_create_job`, `atos_cancel_job`, registration mutations, and settlement mutations MUST require `idempotency_key`.

Server behavior:

- same principal + same key + same request hash => return original result;
- same principal + same key + different request hash => `409 idempotency_conflict`;
- retain keys for at least the maximum financial dispute/retry window.

For committing operations, the idempotency record MUST bind the Quote and therefore the resolved trust mode/proof profile.

## 13. MCP Invariants

1. The default surface remains 11 tools; `tools/list` is computed per authenticated principal, never per connection/session history (see "Per-Caller Tool Visibility" in § 4).
2. `auto` is only a client pre-Quote policy value.
3. `atos_quote` resolves and freezes a concrete mode.
4. Invoke/Job creation inherit mode from Quote and cannot override it.
5. Verified uses `tos_verified_v1`; Native uses `tos_native_v1` or stronger compatible profiles.
6. Verified/Native proof failure is a failure/requote, never a silent Managed fallback.
7. Provider `requested_trust_modes` is not public active `supported_trust_modes`.
8. Execution Receipts may use an authorized delegated signer; signer authority is proved for Verified/Native.
9. Bulk payloads remain off-chain; receipts may commit their hashes.
10. Normal MCP clients see proof status/references, not blockchain plumbing.
11. Trust/reputation summaries are distinct from transaction trust mode.
