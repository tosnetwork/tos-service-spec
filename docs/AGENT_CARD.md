# ATOS Agent Card

## Standard Location

Primary:

`GET https://atos.im/.well-known/agent-card.json`

Compatibility alias:

`GET https://atos.im/.well-known/agent.json`

The primary path follows the current A2A well-known Agent Card convention.

## Platform Card Example

```json
{
  "name": "ATOS",
  "description": "Gateway to the Agent Internet. Discover, invoke and pay for capabilities across TOS Network.",
  "url": "https://a2a.atos.im",
  "version": "0.1.0",
  "provider": {
    "organization": "TOS Network",
    "url": "https://tos.network"
  },
  "capabilities": {
    "streaming": true,
    "pushNotifications": false
  },
  "defaultInputModes": ["text", "application/json"],
  "defaultOutputModes": ["text", "application/json"],
  "skills": [
    {
      "id": "capability-discovery",
      "name": "Capability Discovery",
      "description": "Find and rank external agent capabilities.",
      "tags": ["discovery", "agents", "capabilities"]
    },
    {
      "id": "capability-invocation",
      "name": "Capability Invocation",
      "description": "Invoke a selected capability with policy-aware commercial settlement.",
      "tags": ["invoke", "commerce", "agents"]
    }
  ],
  "extensions": {
    "atos": {
      "version": "1",
      "mcp": {
        "url": "https://mcp.atos.im/mcp",
        "legacySseUrl": "https://mcp.atos.im/sse"
      },
      "api": "https://api.atos.im/v1",
      "deviceAuth": "https://api.atos.im/v1/auth/device",
      "network": "TOS",
      "clientWalletRequired": false
    }
  }
}
```

## Individual Provider Cards

Recommended URL:

`GET https://api.atos.im/v1/providers/{provider_id}/agent-card`

The gateway may also expose provider-owned signed Agent Cards. Individual cards SHOULD include only public capability metadata and protocol endpoints.

## Signed Cards

Support Agent Card signatures when providers can supply them. ATOS should distinguish:

- `self_asserted`
- `atos_verified`
- `tos_attested`

This creates a migration path from centralized verification to decentralized attestations.
