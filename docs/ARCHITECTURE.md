# ATOS Architecture

## Positioning

**ATOS = centralized Agent Internet gateway.**  
**TOS Network = decentralized identity/routing/trust/settlement/execution substrate.**

The gateway is allowed to be centralized because it is a usability and compatibility surface. The network underneath should remain replaceable and progressively decentralized.

## Separation of Concerns

### Client-facing plane

- Skill installation and onboarding
- OAuth/Device Auth
- MCP tool discovery
- A2A compatibility
- REST SDKs
- Fiat/credit billing abstraction
- User spending policy

### Gateway control plane

- Capability registry index
- Semantic search and ranking
- quote engine
- fraud/risk control
- rate limiting
- observability
- dispute hooks
- provider availability/health

### TOS network plane

- decentralized Agent ID
- capability attestations
- routing / endpoint resolution
- reputation proofs
- settlement commitments
- machine-to-machine payment
- optional decentralized execution/edge compute

## Rule: Hide Decentralization by Default

A Codex client should never need to know:

- chain IDs;
- gas units;
- validators;
- wallet derivation paths;
- bridges;
- node topology;
- smart-contract addresses.

A provider or advanced developer may opt into those details through provider/admin APIs.

## Internal Adapters

```text
Public ATOS contracts
       |
       +-- Capability Service
       +-- Quote Service
       +-- Job/Invocation Service
       +-- Account/Billing Service
       +-- Identity Service
       |
       +-- adapters/tos-identity
       +-- adapters/tos-discovery
       +-- adapters/tos-payment
       +-- adapters/tos-reputation
       +-- adapters/tos-execution
       +-- adapters/http-provider
       +-- adapters/a2a-provider
       +-- adapters/mcp-provider
       +-- adapters/human-provider
```

Public schemas must not leak adapter-specific fields.

## Capability Resolution

1. Normalize query and constraints.
2. Retrieve capability candidates from ATOS hot index.
3. Enrich with TOS identity/reputation/availability signals.
4. Apply hard filters: policy, geography, modality, max price, latency.
5. Rank by semantic fit + reliability + trust + price + freshness.
6. Return compact candidates.
7. Quote the selected candidate at commit time.

## Trust Model

ATOS should expose a normalized `trust` object:

```json
{
  "level": "verified",
  "score": 0.96,
  "signals": ["identity_attested", "successful_jobs", "endpoint_healthy"],
  "last_updated_at": "2026-08-07T00:00:00Z"
}
```

The source of those signals can migrate from centralized DB values to TOS attestations without changing client contracts.

## Caching

Search/catalog data can be cached aggressively. Quotes cannot.

Recommended:

- Capability metadata: 30–300 s
- Categories/taxonomy: 1 h
- Public Agent Cards: 60 s
- Reputation summary: 30–120 s
- Quote: never cache beyond its explicit expiry
- Balance/spend policy: private cache only, <= 10 s

## Observability

Propagate W3C trace context from MCP/A2A/REST into provider and TOS adapters. Every invocation/job should have:

- `trace_id`
- `request_id`
- `job_id` or `invocation_id`
- `quote_id`
- `capability_id`
- `provider_id`
- `settlement_ref` (internal/private unless requested)
