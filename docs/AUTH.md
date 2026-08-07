# ATOS Authentication and Authorization

## Goals

- one-sentence onboarding for Codex/Claude/OpenClaw;
- no copying long-lived API keys into chat;
- scoped credentials;
- revocation and device visibility;
- no blockchain key requirement for consumers.

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

Advanced:

- `settlement:read`
- `network:read`

## MCP Authentication

Preferred: OAuth-compatible Bearer access token negotiated by the client/Skill.

Legacy compatibility may permit:

- `Authorization: Bearer <token>`
- or temporary `X-ATOS-API-Key` for service accounts.

Do not require a separate user-ID header if the authenticated token already identifies the principal. A combined API-key-plus-user-ID pair is redundant and error-prone by comparison.

## Service Accounts

For headless agents/servers, support service accounts with:

- scoped secret;
- optional IP restrictions;
- rotation;
- per-service spending limits;
- no interactive user impersonation.
