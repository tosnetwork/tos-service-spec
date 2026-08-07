# ATOS Architecture v0.2

**Status:** Draft  
**Date:** 2026-08-07  
**Product:** ATOS (`atos.im`)  
**Network:** TOS Network  

> **ATOS is an open protocol for discovering, invoking, coordinating, verifying, and settling capabilities across the Agent Internet.**
>
> **atos.im is the canonical reference gateway and managed service.**
>
> **TOS Network is the decentralized trust, execution, proof, and settlement substrate underneath ATOS.**

---

## 1. Architectural Thesis

ATOS must not force users to choose between Web2 usability and Web3 verifiability.

The same Capability, the same MCP/A2A/REST contracts, and the same agent-facing workflow MUST support multiple trust and settlement modes. A user may consume a capability entirely inside `atos.im`, request cryptographic verification through TOS Network, or use TOS-native decentralized infrastructure without depending on `atos.im` as a mandatory intermediary.

The core rule is:

> **Decentralization is a selectable trust level, not a usability requirement.**

ATOS therefore separates four concepts that MUST NOT be conflated:

1. **ATOS Protocol** — the open agent-commerce protocol.
2. **atos.im** — the canonical managed implementation and reference gateway.
3. **ATOS-compatible gateways/indexers** — independently operated discovery and access points.
4. **TOS Network** — decentralized identity, registry anchoring, reputation evidence, proof, escrow, settlement, and native execution infrastructure.

This allows ATOS to compete directly with centralized agent marketplaces while simultaneously providing a migration path to an open Agent Internet.

---

## 2. Three Execution and Trust Modes

ATOS v0.2 defines three modes:

- `managed`
- `verified`
- `native`

These modes are execution/trust policies, not separate products or separate capability types.

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
                 atos.im           atos.im          ATOS Gateway
                    |                 + TOS             + TOS
                    |                 |                 |
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
Client Agent
    |
    v
atos.im
    |
    +-- centralized identity/session
    +-- capability index and ranking
    +-- quote engine
    +-- ATOS Credits / fiat accounting
    +-- job orchestration
    +-- managed reputation
    +-- managed receipts
    |
    v
Provider
```

Properties:

- no wallet required;
- no blockchain knowledge required;
- lowest latency and operational complexity;
- ATOS may use centralized databases and ledgers;
- receipts are platform-verifiable rather than necessarily network-verifiable;
- suitable for ordinary consumers and high-volume low-value calls.

Managed Mode MUST remain a first-class production mode even after decentralized infrastructure matures.

### 2.2 Verified Mode

Verified Mode preserves the `atos.im` UX while moving economically or cryptographically important state to TOS Network.

```text
Client Agent
    |
    v
atos.im
    |
    +-- discovery / ranking / UX
    +-- quote presentation
    +-- provider routing
    |
    +------> tos-core / TOS Network
    |           identity / ownership
    |           escrow commitment
    |           receipt verification
    |           reputation evidence
    |           settlement / proof
    |
    v
Provider / tos-ai
```

The provider executes the workload off-chain unless the capability explicitly requires TOS-native execution. The resulting execution receipt and relevant commitments are verified and/or anchored through TOS Network.

Verified Mode SHOULD become the preferred mode for enterprise, high-value, cross-organization, auditable, or trust-sensitive jobs.

### 2.3 Native Mode

Native Mode removes `atos.im` as a mandatory trust or transaction intermediary.

```text
Client Agent
    |
    +---- atos.im gateway
    +---- third-party gateway
    +---- enterprise gateway
    +---- local/open-source gateway
              |
              v
          TOS Network
       /      |       \
 identity  registry  reputation
 escrow     proof    settlement
              |
              v
        Provider / Worker
```

In Native Mode:

- globally resolvable identities and capabilities are anchored/resolved through TOS infrastructure;
- gateways are replaceable;
- escrow and settlement are TOS-backed;
- execution receipts are network-verifiable;
- providers can be reached through compatible MCP, A2A, HTTP, or TOS-native transports;
- failure or censorship of `atos.im` MUST NOT make the underlying capability economy unavailable.

Native Mode is the long-term Agent Internet mode.

---

## 3. One Public Protocol

The three modes MUST NOT create three client APIs.

Clients continue to use the same compact surface:

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

Mode selection is expressed as policy/constraints.

Example:

```json
{
  "capability_id": "cap_01...",
  "trust_mode": "verified",
  "max_price": {"amount":"10.00","currency":"USD"}
}
```

A client MAY specify:

```text
managed
verified
native
```

or:

```text
auto
```

`auto` allows the gateway to choose the cheapest mode satisfying the caller's trust, spending, jurisdiction, latency, and provider constraints.

The authoritative Quote MUST state the selected mode before financial commitment.

---

## 4. What Goes On-Chain

"TOS-backed" MUST NOT mean storing application payloads on-chain.

TOS Network is primarily the **Trust + Economic + Proof Plane**, not the bulk data plane.

### 4.1 Data that SHOULD remain off-chain

- prompts;
- private user inputs;
- API credentials;
- model context and memory;
- large artifacts;
- source documents;
- images, audio, video;
- private provider implementation details;
- intermediate reasoning or execution state.

These may live in provider storage, ATOS-managed object storage, customer storage, or decentralized content storage according to capability policy.

### 4.2 State that MAY be anchored or committed to TOS

Depending on mode and policy:

- Agent identity / identity attestations;
- Capability ownership;
- Capability manifest/version commitment;
- Quote/terms commitment;
- Escrow state;
- input commitment/hash where appropriate;
- output/artifact commitment/hash;
- signed Execution Receipt;
- settlement state;
- dispute outcome commitment;
- reputation evidence;
- audit/proof references.

A commitment SHOULD be used instead of plaintext whenever the underlying data is private, large, mutable, or commercially sensitive.

---

## 5. Capability Model

A Capability remains the canonical unit of supply.

A capability is independent of execution mode.

```text
Capability
   |
   +-- metadata
   +-- input/output schemas
   +-- pricing policy
   +-- SLA
   +-- provider
   +-- supported trust modes
   +-- supported transports
   +-- ownership commitment
```

Example extension:

```json
{
  "id":"cap_01...",
  "provider_id":"agt_01...",
  "name":"Document Translation",
  "supported_trust_modes":["managed","verified","native"],
  "transports":["mcp","a2a","http"],
  "ownership": {
    "status":"anchored",
    "network":"tos"
  }
}
```

The public capability ID MUST be designed for future federation and MUST NOT depend solely on an `atos.im` database primary key.

---

## 6. Global Addressability

ATOS v0.2 introduces the requirement for globally resolvable Agent and Capability identifiers.

Conceptually:

```text
atos://agent/<agent-id>
atos://capability/<capability-id>
```

The URI syntax is provisional; the architectural requirement is not.

A globally addressable object MUST be resolvable without assuming that `atos.im` owns the canonical database record.

Resolution may use:

```text
ATOS URI / ID
      |
      v
Gateway Resolver
      |
      +--> local/hot index
      +--> federated index
      +--> tos-core resolution
      |
      v
Agent / Capability Manifest
      |
      v
MCP / A2A / HTTP / TOS-native endpoint
```

Identifiers SHOULD distinguish:

- gateway-local IDs;
- globally resolvable IDs;
- immutable content/manifest commitments;
- TOS-anchored ownership records.

This distinction MUST exist before federation is implemented so Phase 5 does not require rewriting every public object identifier.

---

## 7. Decentralized Capability Discovery

Search itself does not belong on-chain.

Semantic search, embeddings, personalization, ranking, latency estimation, policy filtering, and anti-spam systems are computational indexing functions. They SHOULD be performed by gateways/indexers.

The decentralized layer provides a common source of verifiable registry events and commitments.

```text
Provider
   |
   v
Capability Manifest
   |
   +---- managed registration ----> atos.im registry
   |
   +---- TOS anchor/event --------> TOS Network
                                      |
                         +------------+------------+
                         |            |            |
                      Indexer A    Indexer B    Indexer C
                         |            |            |
                      Gateway A    Gateway B    Search App
```

Consequences:

- no single search engine is canonical;
- anyone may build a specialized capability index;
- different gateways may rank the same supply differently;
- TOS provides shared trust facts, not a mandatory ranking algorithm;
- `atos.im` can remain the best default discovery experience without becoming the owner of the Agent Internet.

The exact anti-gaming ranking weights remain gateway-private.

---

## 8. Gateway Federation

Federation is a protocol assumption from v0.2 even if implementation remains a later roadmap phase.

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

A compliant gateway MAY provide:

- authentication;
- local accounts;
- fiat/credit billing;
- capability indexing;
- semantic ranking;
- policy enforcement;
- caching;
- provider routing;
- managed execution;
- TOS-backed verification/settlement.

But no gateway owns the protocol namespace.

A gateway MUST NOT be required for another gateway to verify a TOS-backed identity, ownership record, receipt, or settlement proof.

---

## 9. Execution Receipts and Proof-of-Service

Execution Receipts are promoted from a billing implementation detail to a core ATOS trust primitive.

A signed Execution Receipt SHOULD commit to enough information to establish:

```text
WHO performed the work
WHAT capability/version was used
FOR WHOM it was performed
WHEN it was performed
UNDER WHICH quote/terms
WHAT was committed as input
WHAT result/artifact was committed as output
WHAT usage/resources were charged
WHETHER SLA/result conditions were satisfied
HOW settlement was resolved
WHO signed the receipt
```

Sensitive input/output data MUST NOT be embedded directly when commitments are sufficient.

Conceptual receipt:

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

ATOS defines **Proof-of-Service** as the verifiable evidence graph produced by completed capability executions.

Execution Receipts can feed reputation without exposing private workloads.

```text
Execution Receipts
        |
        v
Proof-of-Service Evidence
        |
        +-- successful executions
        +-- completion rate
        +-- latency distributions
        +-- settlement volume
        +-- dispute rate/outcomes
        +-- capability-specific reliability
        +-- counterparty diversity
        |
        v
Reputation Graph
```

Reputation MUST NOT be reducible to a single mutable platform star rating.

A normalized gateway score may still be exposed for usability, but the underlying TOS-backed evidence SHOULD be independently verifiable.

---

## 10. Control Plane vs Data Plane vs Trust Plane

ATOS v0.2 uses three conceptual planes.

### Gateway / Control Plane

- onboarding;
- authentication/session UX;
- discovery and ranking;
- quote presentation;
- policy and spending controls;
- routing;
- rate limiting;
- fraud/risk controls;
- observability;
- managed billing;
- managed dispute workflow.

### Execution / Data Plane (`tos-ai` + providers)

- provider/worker runtime;
- job execution;
- streaming;
- model/MCP/HTTP/GPU/local/human adapters;
- sandboxing;
- artifact production;
- resource accounting;
- receipt signing.

### Trust / Economic / Proof Plane (`tos-core` + TOS Network)

- globally resolvable identity;
- capability ownership anchoring;
- registry commitments/events;
- reputation evidence;
- escrow;
- receipt verification;
- settlement;
- dispute commitments;
- audit/proof.

The chain is not the bulk execution data plane.

---

## 11. Legal Call Paths

The existing modularity rule remains:

> **tos-ai is execution, not marketplace. tos-core is trust/economy/proof, not AI orchestration.**

Legal high-level paths:

```text
ATOS Gateway -> tos-ai      execution
ATOS Gateway -> tos-core    trust/economy/proof

tos-ai -> tos-core          receipt/identity/settlement lifecycle

tos-core -> TOS Network     consensus/ledger/P2P commitments
```

ATOS gateways and `tos-ai` SHOULD NOT directly depend on consensus internals.

Native clients may eventually use standardized TOS resolution/settlement libraries, but this MUST NOT leak chain-specific fields into ordinary ATOS capability schemas.

---

## 12. Quote and Settlement Semantics

Every financially committing Quote MUST state:

- `quote_id`;
- capability/version;
- provider;
- selected `trust_mode`;
- currency;
- maximum price;
- expiry;
- terms hash/commitment;
- settlement model;
- proof availability.

Example:

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

Managed Mode may use ATOS's internal ledger.

Verified and Native modes SHOULD use TOS-backed escrow/settlement where supported.

The client-facing currency does not have to equal the provider settlement asset.

---

## 13. Mode Selection Policy

Users and agents SHOULD be able to express policy instead of reasoning about blockchain mechanics.

Examples:

```text
"Use the cheapest provider."
"Require cryptographic receipt."
"Require TOS-backed settlement."
"Do not use centralized settlement."
"Maximum $10 autonomous spend."
"Enterprise providers only."
```

The ATOS Skill/gateway translates these into constraints.

Example policy:

```json
{
  "trust_mode":"auto",
  "requirements": {
    "network_verifiable_receipt": true,
    "tos_settlement": false
  }
}
```

The agent should reason about outcomes and trust requirements, not gas, validators, chain IDs, contract addresses, or wallet derivation paths.

---

## 14. Failure and Censorship Model

### Managed Mode
