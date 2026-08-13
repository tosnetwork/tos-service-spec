# ATOS Component Architecture

This document maps the Native protocol to software components. The normative
authority model is defined in `NATIVE_ONLY_ARCHITECTURE_SLIMMING.md`.

## Components

### TOS Network

TOS validators execute registry and commerce contracts, order transactions,
and finalize typed state. Contract code and state hashes are externally
verifiable.

### `tos-protocol`

The protocol service contains no independent business authority. It:

- constructs canonical TVM cells;
- derives object IDs, addresses, and commitments;
- validates client-side signatures and bounds;
- pays transport fees and relays signed cells;
- queries multiple chain endpoints;
- verifies quorum and finality; and
- decodes typed state and produces derived projections.

Transaction keys used only to pay relay fees must remain in a restricted
publisher or wallet process. They do not authorize object semantics.

### `atos`

The reference gateway authenticates transport clients, applies rate limits,
and proxies Native submission and resolution. Future gateway components add
discovery, proposal construction, and orchestration over the same authority
boundary.

### `tos-ai` and providers

Workers execute Quote-bound jobs. A worker receives the minimum necessary
input, selected Capability version, endpoint binding, deadline, and receipt
context. It does not receive controller or buyer wallet keys.

## Deployment topology

```text
wallet/client
  | authenticated Connect request
  v
ATOS gateway
  | Native RPC
  v
tos-protocol relayer/resolver
  | signed TVM message / quorum reads
  v
TOS Network

Accepted Quote -> provider router -> worker -> signed receipt -> TOS settlement
```

The gateway, relayer, provider router, and worker may be operated by different
parties. No pair is required to share a database.

## Availability and caching

Resolvers may cache only data labeled with network, finalized checkpoint,
account, logical time, transaction hash, code hash, and state hash. A cache hit
must satisfy the caller's finality and expected-state requirements. Negative
results are checkpoint-scoped and short-lived.

Discovery indexes consume finalized state and handle reorgs before publication.
They expose chain-derived fields separately from local health or ranking data.

## Observability

Logs and traces may contain request IDs, action hashes, object IDs, chain
references, state hashes, latency, and typed errors. They must not contain
private keys, signatures before submission, raw confidential inputs, bearer
tokens, or unredacted output artifacts.

Readiness requires every dependency needed for safe semantics: authentication,
relayer, quorum resolver, network match, known code hash, and finality source.
Liveness alone never implies readiness.

## Scaling

Gateway replicas are stateless with respect to canonical protocol facts.
Relayers may scale independently and submit the same idempotent action.
Resolvers and indexers scale through checkpointed caches. Workers scale by
Capability and resource class after Accepted Quote binding.
