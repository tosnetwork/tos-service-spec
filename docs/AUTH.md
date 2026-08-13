# ATOS Authentication and Authorization v0.2

> **Legacy v0.2 account contract:** Trust-mode preferences below apply only to
> the current compatibility API. In the Native-only target, gateway
> authentication remains local while canonical Agent authority is finalized
> TOS state. See `NATIVE_ONLY_ARCHITECTURE_SLIMMING.md`.

## Goals

- one-sentence onboarding for Codex/Claude/OpenClaw;
- no copying long-lived API keys into chat;
- scoped credentials;
- revocation and device visibility;
- no blockchain key requirement for ordinary consumers;
- authentication remains separate from transaction trust mode;
- MCP tool visibility reflects request authorization without replacing call-time authorization.

## Authentication Is Not Trust Mode

Authentication answers **who is calling this gateway**.

Trust mode answers **which guarantees apply to a quoted transaction**.

A Bearer token, Device Authorization session, service account, or `principal_id` MUST NOT implicitly change a Quote from `managed` to `verified`/`native` or vice versa.

Pre-Quote policy may be stored on the account as:

```text
default_requested_trust_mode = managed | verified | native | auto
```

but every financially committing Quote still resolves and records its own concrete:

```text
trust_mode = managed | verified | native
```

## Device Authorization

### Start

`POST /v1/auth/device`

```json
{
  "client_type": "codex",
  "client_name": "Codex on MacBook",
  "requested_scopes": [
    "capabilities:read",
    "quotes:read",
    "invocations:create",
    "jobs:create",
    "jobs:read",
    "jobs:cancel",
    "account:read"
  ]
}
```

Response:

```json
{
  "device_code": "dc_...",
  "user_code": "ABCD-EFGH",
  "verification_uri": "https://atos.im/activate",
  "verification_uri_complete": "https://atos.im/activate?code=ABCD-EFGH",
  "expires_in": 900,
  "interval": 5
}
```

### Poll/Token

`POST /v1/auth/device/token`

```json
{"device_code":"dc_..."}
```

Pending:

```json
{"error":"authorization_pending"}
```

Success:

```json
{
  "access_token":"...",
  "token_type":"Bearer",
  "expires_in":3600,
  "refresh_token":"...",
  "principal_id":"prn_...",
  "scopes":[
    "capabilities:read",
    "quotes:read",
    "invocations:create",
    "jobs:create",
    "jobs:read",
    "jobs:cancel",
    "account:read"
  ]
}
```

## Human Account Authentication (Passkey/WebAuthn)

Device Authorization (above) answers "how does a third-party app/agent get
scoped, delegated access from an already-identified human" -- it assumes
that identification already happened somewhere else (see `/activate`'s
"trusted login/reverse-proxy boundary" requirement). Until now, ATOS never
actually built that boundary: nothing anywhere establishes who a human
actually is. This section is that missing first-party primitive --
`atos.im`'s own account system, modeled directly on `tosnetwork/atos-aidrop`'s
proven `tos-wallet-web` passkey implementation (same library --
`github.com/go-webauthn/webauthn` -- same usernameless/discoverable-credential
design, same ceremony-begin/ceremony-finish shape), not a new design from
scratch.

No passwords, no email, no username. A passkey (platform authenticator or
security key, resident/discoverable credential) is both how an account is
created and how it signs back in -- the browser's own passkey picker
resolves which account is authenticating; the client submits no identifier
at all at login time.

### Registration

```text
POST /auth/passkey/register/begin
  -> {} (no body required)
  <- {"ceremony_id":"...", "options": <PublicKeyCredentialCreationOptions>}

POST /auth/passkey/register/finish/{ceremony_id}
  -> <PublicKeyCredentialAttestation response, from navigator.credentials.create()>
  <- same token response shape as POST /auth/device/token's success case:
     {"access_token":"...","token_type":"Bearer","expires_in":3600,
      "refresh_token":"...","principal_id":"prn_...","scopes":[...]}
```

A successful `finish` call both creates the account (a fresh `prn_...`
principal ID, minted once and stable for that account from then on) and
attests the first passkey in one atomic ceremony -- there is no separate
"create account" step that could exist without a working credential
attached to it.

### Login

```text
POST /auth/passkey/login/begin
  -> {} (no body required)
  <- {"ceremony_id":"...", "options": <PublicKeyCredentialRequestOptions>}

POST /auth/passkey/login/finish/{ceremony_id}
  -> <PublicKeyCredentialAssertion response, from navigator.credentials.get()>
  <- same token response shape as registration's finish call
```

### Relationship to Device Authorization

A passkey-authenticated session is issued through the *same* underlying
token/scope/revocation machinery Device Authorization already uses (same
access/refresh token format, same `principal_id` namespace, same per-device
revocation record) -- it is a second front door onto the identical
mechanism, not a parallel identity system. Concretely: successful passkey
registration/login mints a token pair directly, skipping the
grant/user-code/poll ceremony entirely, since the passkey ceremony itself
*is* the identification step Device Authorization otherwise assumes already
happened.

Passkey-issued tokens carry a fixed scope bundle for v1 -- the full
self-service bundle a first-party `atos.im` account needs today (ordinary
consumer scopes plus `capabilities:write` and `open_task_proposals:write`,
so a signed-up user can immediately publish tasks, register/manage
capabilities, and bid as a provider without a second consent step).
Explicit-grant-only scopes (`execution_signers:write`, `settlement:write`,
`disputes:review`, `activation:evaluate`, admin scopes generally) are never
included -- exactly the same restriction Device Authorization's own
self-service path already enforces. A future version MAY narrow this to a
smaller default plus an explicit "become a provider" upgrade step; v1
deliberately keeps one bundle to avoid re-introducing a second
grant/consent flow for the common case.

Device Authorization itself is untouched and remains the correct mechanism
for third-party apps/agents/MCP clients requesting *delegated*, narrower
access from an already-authenticated human (e.g. a Codex/Claude integration
asking a human to approve read-only access) -- passkey login is specifically
for a human authenticating as themselves on a first-party ATOS surface, not
a replacement for delegated authorization.

### Storage and credential data

Mirrors `atos-aidrop`'s schema (encrypted public key at rest, credential
ID/AAGUID/transports/sign-count/backup-state tracked per credential,
short-lived ceremony records keyed by `ceremony_id` holding the WebAuthn
challenge state until `finish` consumes them or they expire). No wallet
keys, balances, or ledger provisioning are part of this -- that is
`atos-aidrop`'s domain, not `atos.im`'s; only the passkey/account
primitive is shared in spirit.

## Recommended Scopes

Consumer:

- `capabilities:read`
- `quotes:read`
- `invocations:create`
- `jobs:create`
- `jobs:read`
- `jobs:cancel`
- `account:read`

Provider:

- `capabilities:write`
- `provider_jobs:read`
- `provider_jobs:deliver`
- `earnings:read`
- `execution_signers:read` (Phase 3B; execution-signer status)
- `execution_signers:write` (Phase 3B; execution-signer authorize/rotate/revoke -- deliberately separate from `capabilities:write`, since signer mutation is a distinct trust-side effect, not ordinary Capability metadata)

Advanced/proof:

- `settlement:read`
- `proofs:read`
- `network:read`

`proofs:read` permits retrieval of advanced proof material when available; compact proof status/references may still appear on a Receipt/Job visible to its owner.

## MCP Authentication

Preferred: OAuth-compatible Bearer access token negotiated by the client/Skill.

Compatibility may permit:

- `Authorization: Bearer <token>`;
- temporary `X-ATOS-API-Key` for service accounts where policy allows it.

Do not require a separate user-ID header if the authenticated token already identifies the principal.

## MCP Tool Visibility

MCP `tools/list` is a **projection of the authorization carried on that request**. It is not a session-scoped capability cache and it is not an authorization decision that can be trusted later without re-checking.

For a tool to be returned, both of these conditions apply where relevant:

```text
request scope permits the operation
AND
role/resource precondition permits the operation
```

Examples:

| Tool | Required visibility condition |
|---|---|
| `atos_search` / `atos_get_capability` | `capabilities:read` |
| `atos_quote` | `quotes:read` |
| `atos_invoke` | `invocations:create` |
| `atos_create_job` | `jobs:create` |
| `atos_get_job` | `jobs:read` |
| `atos_cancel_job` | `jobs:cancel` |
| `atos_account` | `account:read` |
| `atos_register_capability` | `capabilities:write` |
| `atos_update_capability` | `capabilities:write` |
| `atos_list_my_capabilities` | `capabilities:write` and provider role |
| `atos_pause_capability` | `capabilities:write` and ownership of the target capability at call time |
| `atos_provider_jobs` | `provider_jobs:read` and provider role |
| `atos_deliver_job` | `provider_jobs:deliver` and authorization for the target provider/job |

The ordinary consumer token therefore sees the 9-tool consumer surface described in `docs/MCP.md`. A provider token may see additional tools.

### Visibility is not authorization

Every `tools/call` MUST independently validate:

1. token validity;
2. required scope;
3. current role/resource ownership or job access;
4. operation-specific policy.

A cached tool list MUST NOT confer authority after a scope is revoked or ownership changes.

### Caching and ordering

Because the tool list can vary by authorization context, ATOS SHOULD return:

```json
{
  "ttlMs": 30000,
  "cacheScope": "private"
}
```

The server SHOULD return the same underlying tool set in deterministic order:

```text
consumer core
-> artifact
-> capability-management
-> provider-job/admin
```

ATOS does not vary `tools/list` because of earlier tool calls, connection history, selected capabilities, or other hidden session state.

## Artifact Operation Authorization

`atos_artifact` remains model-visible to ordinary consumers because file needs are capability-dependent, but each operation has its own authorization rule.

### `create_upload`

For:

```text
purpose = job_input
```

require at least one execution-creation scope appropriate to the intended use:

```text
invocations:create OR jobs:create
```

For:

```text
purpose = capability_asset
```

require:

```text
capabilities:write
```

### `complete_upload`

The caller MUST be the same principal/security context that created the upload, or hold an explicitly delegated administrative permission. Knowing an `upload_id` is never sufficient authorization.

### `get_download_url`

The caller MUST be authorized for the Artifact itself or for the owning Job/output. For Job outputs, authorization SHOULD be equivalent to the corresponding `atos_get_job` access check.

Signed URLs are short-lived transport credentials and MUST NOT grant broader standing Artifact access.

## Agent Identity Migration

`principal_id` is an **ATOS gateway account identifier**. It is not itself a wallet, private key, or globally canonical TOS Agent Identity.

### Managed phases

Managed Mode can operate with gateway-local `principal_id` identities.

### Verified integration

When Verified Mode is activated, a gateway account/provider MAY be bound to a `tos-core` Agent Identity through `ResolveAgentIdentity` so ownership, receipt verification, reputation evidence, escrow and settlement can be TOS-backed without requiring the user to manually manage TOS keys.

This binding:

- is server-side by default;
- does not change the public Device Authorization flow;
- does not require a consumer to import an external wallet as a precondition for ordinary use;
- can be surfaced through normalized identity/proof references when a Verified/Native transaction requires it.

### Native identity

Native Mode cannot treat a gateway-local `principal_id` as the globally canonical identity by itself.

Native Agent/provider identity and Capability ownership must be resolvable/verifiable through the TOS-backed identity/registry model defined by the v0.2 architecture.

A gateway MAY maintain a local alias from `principal_id` to that global identity for UX.

## Walletless Verified/Native UX

A client does not necessarily need to sign raw TOS transactions itself.

Where operationally and legally supported, a gateway/sponsor may abstract transaction submission, fees, or settlement funding while the resulting required state remains verifiable through TOS according to the Quote's proof profile.

This is different from weakening the trust mode: abstraction of chain mechanics is allowed; loss of the required TOS-backed proof/settlement guarantees is not.

## Service Accounts

For headless agents/servers, support service accounts with:

- scoped secret;
- optional IP restrictions;
- rotation;
- per-service spending limits;
- default requested trust policy;
- no interactive user impersonation.

Service-account credentials MUST NOT be embedded in Capability metadata, Agent Cards, Execution Receipts, or A2A extensions.
