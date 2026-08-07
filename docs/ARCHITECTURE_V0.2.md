# ATOS Architecture v0.2

**Status:** Draft  
**Date:** 2026-08-07  
**Product:** ATOS (`atos.im`)  
**Network:** TOS Network

> **ATOS is an open protocol for discovering, invoking, coordinating, verifying, and settling capabilities across the Agent Internet.**
>
> **atos.im is the canonical reference gateway and managed service.**
>
> **TOS Network is the decentralized trust, proof, execution, and settlement substrate underneath ATOS.**

## 1. Architectural Thesis

ATOS must provide the usability of a centralized agent marketplace without making centralization a protocol requirement.

The same Capability and the same MCP/A2A/REST contracts MUST support multiple trust and settlement modes. A user may complete a transaction entirely inside `atos.im`, request TOS-backed verification while retaining the managed UX, or use TOS-native decentralized infrastructure without depending on `atos.im` as a mandatory intermediary.

**Core principle: decentralization is a selectable trust level, not a usability requirement.**

ATOS therefore separates four concepts:

1. **ATOS Protocol** — the open agent-commerce protocol.
2. **atos.im** — the canonical managed implementation and reference gateway.
3. **ATOS-compatible gateways/indexers** — independently operated discovery and access points.
4. **TOS Network** — decentralized identity, registry anchoring, reputation evidence, proof, escrow, settlement, and native execution infrastructure.

## 2. Three Trust Modes

ATOS v0.2 defines `managed`, `verified`, and `native`. These are policies, not separate products.

```text
                   Codex / Claude / Cursor / OpenClaw
                                  |
                             ATOS Protocol
                      search / quote / invoke / jobs
                                  |
                +-----------------+-----------------+
                |                 |                 |
             MANAGED           VERIFIED           NATIVE
                |                 |                 |
             atos.im           atos.im          any gateway
                |                 + TOS             + TOS
                +-----------------+-----------------+
                                  |
                              Capability
                                  |
                               Provider
```

A Capability MAY support one, two, or all three modes.

### 2.1 Managed Mode

Managed Mode is the default mainstream experience and may complete entirely inside `atos.im`.

```text
Client -> atos.im -> search/quote/account/job/billing -> Provider
```

Properties:

- no wallet or blockchain knowledge required;
- centralized identity/session, registry index, accounting, orchestration, reputation and receipts are allowed;
- optimized for latency, cost and operational simplicity;
- suitable for ordinary users and high-volume low-value calls.

Managed Mode MUST remain first-class even after TOS-backed infrastructure matures.

### 2.2 Verified Mode

Verified Mode preserves the `atos.im` experience while moving economically or cryptographically important state to TOS Network.

```text
Client
  |
atos.im ----------------------+
  |                            |
  | discovery/ranking/routing | identity/ownership
  |                            | escrow
  |                            | receipt verification
  |                            | reputation evidence
  |                            | settlement/proof
  v                            v
Provider / tos-ai          tos-core -> TOS Network
```

The workload normally executes off-chain. TOS carries commitments, verification, trust evidence and settlement rather than bulk application data.

Verified Mode SHOULD be preferred for enterprise, high-value, cross-organization, auditable or trust-sensitive jobs.

### 2.3 Native Mode

Native Mode removes `atos.im` as a mandatory transaction or trust intermediary.

```text
Client Agent
    |
    +-- atos.im gateway
    +-- third-party gateway
    +-- enterprise gateway
    +-- local/open-source gateway
              |
          TOS Network
       /      |       \
 identity  registry  reputation
 escrow     proof    settlement
              |
        Provider / Worker
```

In Native Mode, gateways are replaceable, identities and capabilities are globally resolvable, settlement is TOS-backed, and network-verifiable receipts are available. Failure or censorship of `atos.im` MUST NOT make the underlying native capability economy unavailable.

## 3. One Public Protocol

The three modes MUST NOT create three client APIs. Clients continue to use the compact ATOS surface:

```text
atos_search
atos_get_capability
atos_quote
atos_invoke
atos_create_job
atos_get_job
atos_cancel_job
atos_register_capability
atos_update_capability
atos_account
```

Mode selection is expressed as policy:

```json
{
  "capability_id":"cap_...",
  "trust_mode":"verified",
  "max_price":{"amount":"10.00","currency":"USD"}
}
```

Allowed values are `managed`, `verified`, `native`, and `auto`. `auto` selects the cheapest mode satisfying trust, spending, jurisdiction, latency and provider constraints.

The authoritative Quote MUST state the selected mode before financial commitment.

## 4. TOS Is Not the Bulk Data Plane

"TOS-backed" MUST NOT mean storing all application payloads on-chain.

TOS Network is primarily the **Trust + Economic + Proof Plane**.

Normally off-chain:

- prompts and private inputs;
- credentials, context and memory;
- source documents and large artifacts;
- images, audio and video;
- private provider implementation details;
- intermediate execution state.

Depending on trust mode, TOS MAY anchor or commit:

- Agent identity and attestations;
- Capability ownership and manifest/version commitments;
- Quote/terms commitments;
- escrow state;
- optional input commitment;
- output/artifact commitment;
- signed Execution Receipt;
- settlement state;
- dispute outcome commitment;
- reputation evidence and audit proofs.

Use commitments/hashes rather than plaintext whenever the underlying data is private, large or commercially sensitive.

## 5. Capability Model

A Capability remains the canonical unit of supply and is independent of trust mode.

```json
{
  "id":"cap_...",
  "provider_id":"agt_...",
  "name":"Document Translation",
  "supported_trust_modes":["managed","verified","native"],
  "transports":["mcp","a2a","http"],
  "ownership":{"status":"anchored","network":"tos"}
}
```

The public Capability ID MUST be federation-safe and MUST NOT depend solely on an `atos.im` database primary key.

## 6. Global Addressability

ATOS v0.2 requires globally resolvable Agent and Capability identifiers.

Conceptually:

```text
atos://agent/<agent-id>
atos://capability/<capability-id>
```

The URI syntax is provisional; global resolvability is the requirement.

```text
ATOS ID
   |
Gateway Resolver
   +-- local/hot index
   +-- federated index
   +-- tos-core resolution
   |
Agent / Capability Manifest
   |
MCP / A2A / HTTP / TOS-native endpoint
```

The design MUST distinguish gateway-local IDs, globally resolvable IDs, immutable manifest commitments, and TOS-anchored ownership records before federation ships.

## 7. Decentralized Discovery

Search itself does not belong on-chain. Semantic retrieval, embeddings, personalization, ranking, latency estimation and anti-spam are indexing functions performed by gateways/indexers.

TOS provides shared verifiable registry events and commitments.

```text
Provider
   |
Capability Manifest
   +---- managed registration ----> atos.im registry
   +---- TOS anchor/event --------> TOS Network
                                      |
                         +------------+------------+
                         |            |            |
                      Indexer A    Indexer B    Indexer C
                         |            |            |
                      Gateway A    Gateway B    Search App
```

No search engine is canonical. Anyone may build a specialized index or ranking system. `atos.im` may remain the best default discovery experience without owning the Agent Internet.

## 8. Gateway Federation

Federation is an architectural assumption in v0.2 even if implementation remains a later roadmap phase.

```text
                         ATOS Protocol
                              |
          +-------------------+-------------------+
          |                   |                   |
      atos.im             Gateway B          Enterprise Gateway
          |                   |                   |
          +-------------------+-------------------+
                              |
                         TOS Network
                              |
                Providers / Agents / Workers
```

A compliant gateway MAY provide authentication, local accounts, fiat/credit billing, indexing, ranking, policy, caching, provider routing, managed execution, and TOS-backed verification/settlement.

No gateway owns the protocol namespace. A gateway MUST NOT be required for another gateway to verify a TOS-backed identity, ownership record, receipt or settlement proof.

## 9. Execution Receipts and Proof-of-Service

Execution Receipts are a core ATOS trust primitive, not merely billing records.

A signed receipt SHOULD establish or commit to:

```text
WHO performed the work
WHAT capability/version was used
FOR WHOM
WHEN
UNDER WHICH quote/terms
WHAT input was committed
WHAT output/artifact was committed
WHAT usage/resources were charged
WHETHER result/SLA conditions were satisfied
HOW settlement resolved
WHO signed the receipt
```

Example:

```json
{
  "receipt_id":"rcpt_...",
  "job_id":"job_...",
  "provider_id":"agt_...",
  "capability_id":"cap_...",
  "capability_version":"1.2.0",
  "quote_id":"q_...",
  "input_commitment":"sha256:...",
  "output_commitment":"sha256:...",
  "usage_commitment":"sha256:...",
  "result":"success",
  "provider_signature":"...",
  "network_proof":"tos:..."
}
```

### Proof-of-Service

**Proof-of-Service** is the verifiable evidence graph produced by completed capability executions.

```text
Execution Receipts
        |
Proof-of-Service Evidence
        +-- successful executions
        +-- completion rate
        +-- latency distributions
        +-- settlement volume
        +-- dispute rate/outcomes
        +-- capability reliability
        +-- counterparty diversity
        |
Reputation Graph
```

A gateway may expose a normalized score for usability, but TOS-backed evidence SHOULD be independently verifiable. Reputation MUST NOT be reducible to one mutable platform star rating.

## 10. Three Architectural Planes

### Gateway / Control Plane

Onboarding, auth/session UX, discovery/ranking, quote presentation, policy/spending controls, routing, risk, observability, managed billing and managed disputes.

### Execution / Data Plane (`tos-ai` + providers)

Provider/worker runtime, jobs, streaming, model/MCP/HTTP/GPU/local/human adapters, sandboxing, artifacts, resource accounting and receipt signing.

### Trust / Economic / Proof Plane (`tos-core` + TOS Network)

Global identity, capability ownership, registry commitments/events, reputation evidence, escrow, receipt verification, settlement, dispute commitments and audit/proof.

**The blockchain is not the bulk execution data plane.**

## 11. Legal Call Paths

The modularity rule remains:

> **tos-ai is execution, not marketplace. tos-core is trust/economy/proof, not AI orchestration.**

```text
ATOS Gateway -> tos-ai      execution
ATOS Gateway -> tos-core    trust/economy/proof
tos-ai       -> tos-core    receipt/identity/settlement lifecycle
tos-core     -> TOS Network consensus/ledger/P2P commitments
```

Ordinary ATOS schemas MUST NOT leak consensus internals, validators, gas units, contract addresses or node topology.

## 12. Quote and Settlement Semantics

Every financially committing Quote MUST state capability/version, provider, selected trust mode, currency, maximum price, expiry, terms commitment, settlement model and proof availability.

```json
{
  "quote_id":"q_...",
  "capability_id":"cap_...",
  "trust_mode":"verified",
  "price":{"total_max":"5.25","currency":"USD"},
  "settlement":{"network":"tos","escrow":true},
  "proof":{"execution_receipt":true,"settlement_proof":true},
  "expires_at":"...",
  "terms_hash":"sha256:..."
}
```

Managed Mode may use ATOS's internal ledger. Verified and Native modes SHOULD use TOS-backed escrow/settlement where supported. Client-facing currency does not have to equal provider settlement asset.

## 13. Mode Selection Policy

Users and agents express outcomes, not blockchain mechanics:

```text
Use the cheapest provider.
Require a cryptographic receipt.
Require TOS-backed settlement.
Do not use centralized settlement.
Maximum $10 autonomous spend.
```

Example:

```json
{
  "trust_mode":"auto",
  "requirements":{
    "network_verifiable_receipt":true,
    "tos_settlement":false
  }
}
```

The ATOS Skill/gateway translates policy into routing constraints. Agents should not reason about gas, validators, chain IDs or wallet derivation paths.

## 14. Failure and Censorship Model

### Managed

`atos.im` is in the critical path. Its availability and policies define service availability.

### Verified

`atos.im` may remain in the execution path, but TOS-backed ownership, receipt and settlement evidence can be independently verified. Gateway failure must not erase already committed proofs.

### Native

No single gateway is authoritative. A client can resolve the same globally addressable supply through another compatible gateway/indexer. TOS-backed trust and settlement survive loss of `atos.im`.

This is the architectural boundary between **a marketplace using a blockchain** and **an open Agent Internet**.

## 15. Migration Strategy

ATOS can ship progressively without changing its public mental model.

```text
Phase A: Managed
atos.im DB + credits + managed providers

Phase B: Verified
atos.im UX + tos-ai execution + tos-core/TOS proofs and settlement

Phase C: Native
federated gateways + decentralized registry/indexers + TOS-native trust economy
```

The migration rule is **add verifiability without breaking usability**.

Existing managed capabilities can progressively gain `verified` and `native` support without receiving a new Agent-facing capability type.

## 16. Architecture Invariants

1. **One Capability Model.** Human, agent, API, GPU and other supply are adapters behind Capabilities.
2. **One Client Protocol.** Managed, Verified and Native do not fork MCP/A2A/REST contracts.
3. **Mode is explicit at commitment.** A Quote states the final trust/settlement mode.
4. **No mandatory wallet for consumers.** Mainstream clients can use fiat/credits.
5. **No mandatory chain payloads.** Private and bulk data stay off-chain by default.
6. **No gateway owns the namespace.** Global IDs are federation-safe.
7. **Search is competitive.** TOS anchors facts; gateways/indexers rank them.
8. **Receipts are portable evidence.** Verified/native execution creates independently checkable proof.
9. **tos-ai executes; tos-core trusts and settles.** Plane boundaries remain strict.
10. **atos.im is important but replaceable.** Native ATOS survives without it.

## 17. Strategic Positioning

ATOS should not be described merely as a decentralized marketplace.

A centralized marketplace owns supply, discovery, reputation and transactions inside one platform boundary.

ATOS instead aims to define the common commerce layer through which autonomous agents can discover capabilities, agree on terms, execute work, produce portable evidence, establish reputation and settle value across independently operated infrastructure.

The intended progression is:

```text
Managed Agent Marketplace
          |
          v
Verifiable Agent Commerce Network
          |
          v
Open Agent Internet
```

`atos.im` competes on product experience.

ATOS Protocol competes on interoperability.

TOS Network provides the decentralized trust and economic substrate that makes the protocol open, portable and independently verifiable.
