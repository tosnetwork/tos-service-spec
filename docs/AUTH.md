# ATOS Authentication and Authorization v0.2

## Goals

- one-sentence onboarding for Codex/Claude/OpenClaw;
- no copying long-lived API keys into chat;
- scoped credentials;
- revocation and device visibility;
- no blockchain key requirement for ordinary consumers;
- authentication remains separate from transaction trust mode.

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
    "jobs:read",
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
  "scopes":["capabilities:read","quotes:read","invocations:create","jobs:read","account:read"]
}
```

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

## Agent Identity Migration

`principal_id` is an **ATOS gateway account identifier**. It is not itself a wallet, private key, or globally canonical TOS Agent Identity.

### Managed phases

Managed Mode can operate with gateway-local `principal_id` identities.

### Verified integration

When Verified Mode is activated (Roadmap Phase 4), a gateway account/provider MAY be bound to a `tos-core` Agent Identity through `ResolveAgentIdentity` so ownership, receipt verification, reputation evidence, escrow and settlement can be TOS-backed without requiring the user to manually manage TOS keys.

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
