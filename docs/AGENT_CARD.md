# ATOS Agent Card v0.2

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
  "description": "Reference gateway for the ATOS Agent Internet protocol. Discover, invoke, verify and settle capabilities through Managed, Verified or Native trust modes.",
  "url": "https://a2a.atos.im",
  "version": "0.2.0",
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
      "description": "Quote and invoke capabilities with selectable trust and settlement guarantees.",
      "tags": ["invoke", "commerce", "agents", "verification"]
    },
    {
      "id": "open-task-marketplace",
      "name": "Open Task Marketplace",
      "description": "Publish demand-side tasks without a known capability_id, discover open tasks, submit or accept proposals. See docs/A2A.md's Open Task Marketplace Extension for the openTasks/* method namespace.",
      "tags": ["marketplace", "open-task", "discovery", "commerce", "agents"]
    }
  ],
  "extensions": {
    "atos": {
      "protocolVersion": "0.2.0",
      "mcp": {
        "url": "https://mcp.atos.im/mcp",
        "legacySseUrl": "https://mcp.atos.im/sse"
      },
      "api": "https://api.atos.im/v1",
      "deviceAuth": "https://api.atos.im/v1/auth/device",
      "network": "TOS",
      "clientWalletRequired": false,
      "supportedTrustModes": ["managed", "verified", "native"],
      "autoTrustModeSelection": true,
      "proofProfiles": ["tos_verified_v1", "tos_native_v1"],
      "nativeResolution": true
    }
  }
}
```

`auto` is not included in `supportedTrustModes` because it is a pre-Quote selection policy, not a concrete transaction mode.

The platform card advertises what the gateway implementation is capable of serving. A specific Capability's public `supported_trust_modes` still contains only modes that are currently active for that Capability.

## Individual Provider Cards

Reference gateway URL:

`GET https://api.atos.im/v1/providers/{provider_id}/agent-card`

The gateway may also expose provider-owned signed Agent Cards.

Individual cards SHOULD include only public Capability metadata and protocol endpoints. The ATOS extension SHOULD advertise:

- active concrete trust modes;
- applicable proof profiles;
- global Agent/provider identifier where available;
- Native resolver/address information where applicable;
- Capability IDs/links;
- public signing/attestation references.

Provider-requested but not yet activated modes SHOULD NOT be presented as supported transaction modes. If useful for provider/admin tooling, they may be represented separately as pending/requested state.

Do not put private keys, internal prompts, private settlement destinations, or non-public network topology in Agent Cards.

## Trust/Identity Assurance vs Transaction Trust Mode

Agent Card identity assurance is distinct from a transaction's `trust_mode`.

Identity/card assurance may use labels such as:

- `self_asserted`
- `atos_verified`
- `tos_attested`

Transaction trust mode is separately:

- `managed`
- `verified`
- `native`

Do not use a single ambiguous `verified` label to represent both concepts.

## Signed Cards

Support Agent Card signatures when providers can supply them.

A signed card alone is not sufficient for Verified or Native activation.

Verified additionally requires the `tos_verified_v1` trust/economic/proof guarantees.

Native additionally requires `tos_native_v1`, including gateway-independent canonical provider/Capability resolution.

See `docs/PROOF_PROFILES.md`, `docs/ARCHITECTURE_V0.2.md`, and `docs/CAPABILITIES.md`.
