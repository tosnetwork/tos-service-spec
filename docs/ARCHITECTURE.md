# ATOS Architecture

## Positioning

**ATOS = centralized Agent Internet gateway.**  
**TOS Network = decentralized identity/routing/trust/settlement/execution substrate.**

The gateway is allowed to be centralized because it is a usability and compatibility surface. The network underneath should remain replaceable and progressively decentralized.

## Separation of Concerns

ATOS sits above two distinct TOS Network layers, not one undifferentiated "network plane."
Conflating them breaks the architecture's core modularity rule: **tos-ai is execution, not
marketplace; tos-core is trust, not AI.** ATOS must route every downstream call to exactly
one of them.

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

### tos-ai plane — execution

Everything about *running* a capability. No identity, ownership, escrow or settlement
logic lives here.

- provider/worker runtime registration and health
- job submission, streaming and cancellation
- model / MCP tool / HTTP / GPU / local-process / human-backed execution adapters
- sandboxing and resource accounting
- signed execution receipt generation

### tos-core plane — trust & economy

Everything about *whether a party can be trusted and how value moves*. No prompt
engineering, model orchestration or marketplace UX lives here.

- agent identity resolution
- capability ownership / registry anchoring
- reputation state
- escrow creation and release
- execution receipt verification
- settlement and payout
- proof / audit

### TOS Network plane

Consensus, P2P and ledger. ATOS and tos-ai never talk to TOS Network nodes directly —
only tos-core does. This keeps chain topology, block height and validator details fully
invisible to the gateway and to execution.

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
       +-- Capability Service ----------- adapters/tos-ai      (execution)
       +-- Quote Service   ----+
       +-- Job/Invocation Service --------- adapters/tos-ai      (execution)
       +-- Account/Billing Service --------- adapters/tos-core    (trust/economy)
       +-- Identity Service ---------------- adapters/tos-core    (trust/economy)
       |
       +-- adapters/tos-ai
       |     provider/worker execution, model/mcp/http/gpu/local adapters
       +-- adapters/tos-core
       |     identity, registry, reputation, escrow, receipt verification, settlement, proof
       +-- adapters/http-provider   (behind tos-ai)
       +-- adapters/a2a-provider    (behind tos-ai)
       +-- adapters/mcp-provider    (behind tos-ai)
       +-- adapters/human-provider  (behind tos-ai)
```

Public schemas must not leak adapter-specific fields.

## Cross-Service Interface Contracts

These three call directions are the only legal paths from ATOS/tos-ai into TOS Network.
No service should call directly into TOS Network nodes, consensus or ledger state.

### ATOS → tos-ai (execution)

```text
RegisterProvider
GetProviderStatus
SubmitJob
CancelJob
GetJob
StreamJob
FetchResult
FetchReceipt
```

### tos-ai → tos-core (trust/economy, receipt lifecycle)

```text
ResolveAgentIdentity
VerifyCapabilityOwnership
CreateEscrow
CommitExecutionReceipt
VerifyExecutionReceipt
SettleJob
ReadReputation
UpdateReputationEvidence
```

### ATOS → tos-core (direct trust reads/writes, no execution involved)

```text
ResolveAgent
ResolveCapability
ReadReputation
CreateEscrow
ReadSettlementStatus
ReadProof
```

High-frequency reads (reputation, capability resolution) should go through the ATOS
indexer/cache rather than hitting tos-core synchronously on every request. Quote,
escrow creation and settlement status are never cached beyond their explicit expiry.

## Capability Resolution

1. Normalize query and constraints.
2. Retrieve capability candidates from ATOS hot index.
3. Enrich with identity/reputation/availability signals via cached `tos-core.ReadReputation` /
   `tos-core.ResolveCapability` reads (not a live tos-ai execution call).
4. Apply hard filters: policy, geography, modality, max price, latency.
5. Rank by semantic fit + reliability + trust + price + freshness.
6. Return compact candidates.
7. Quote the selected candidate at commit time. Only once the client commits to
   `atos_invoke`/`atos_create_job` does the request cross into `tos-ai.SubmitJob`.

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
