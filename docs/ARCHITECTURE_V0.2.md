# ATOS Architecture v0.2

**Status:** Draft  
**Date:** 2026-08-07  
**Product:** ATOS (`atos.im`)  
**Network:** TOS Network

> **ATOS is an open protocol for discovering, invoking, coordinating, verifying, and settling capabilities across the Agent Internet.**
>
> **atos.im is the canonical reference gateway and managed service.**
>
> **TOS Network is the decentralized identity, registry, trust, proof, and economic substrate underneath ATOS.**
>
> **tos-ai is the execution fabric; tos-core is the trust/economy/proof boundary into TOS Network.**

## 1. Architectural Thesis

ATOS must provide the usability of a centralized agent marketplace without making centralization a protocol requirement.

The same Capability and the same MCP/A2A/REST contracts MUST support multiple trust and settlement modes. A user may complete a transaction entirely inside `atos.im`, request TOS-backed verification while retaining the managed UX, or use TOS-native decentralized infrastructure without depending on `atos.im` as a mandatory intermediary.

**Core principle: decentralization is a selectable trust level, not a usability requirement.**

ATOS separates four concepts:

1. **ATOS Protocol** — the open agent-commerce protocol.
2. **atos.im** — the canonical managed implementation and reference gateway.
3. **ATOS-compatible gateways/indexers** — independently operated discovery and access points.
4. **TOS Network** — decentralized identity, registry anchoring, reputation evidence, escrow, proof, and settlement.

Execution itself remains outside consensus. It is performed by providers and/or `tos-ai` workers, with commitments and receipts verified through `tos-core` when required.

## 2. Trust-Mode Semantics

ATOS v0.2 defines three concrete trust modes:

- `managed`
- `verified`
- `native`

It also defines one request policy value:

- `auto`

**`auto` is not a concrete trust mode.** It is valid only before quote resolution. A Capability MUST NOT list `auto` in `supported_trust_modes`, and a Quote, Invocation, Job, Escrow, or Receipt MUST NOT persist `auto` as its final mode.

Terminology:

- `requested_trust_mode`: `managed | verified | native | auto`
- `trust_mode`: resolved concrete value `managed | verified | native`

Once a Quote is issued, its resolved `trust_mode` is immutable. Execution MUST NOT silently downgrade from `verified` or `native` to `managed`; a different mode requires a new Quote.

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

A Capability MAY support one, two, or all three concrete modes.

## 3. Guarantee Profiles

Trust modes are protocol guarantees, not marketing labels. A gateway MUST satisfy the minimum guarantee profile for the resolved mode.

| Guarantee | managed | verified | native |
|---|---:|---:|---:|
| Gateway may be authoritative for account/search/job state | yes | yes | no for canonical trust facts |
| TOS-backed provider identity / capability ownership | optional | required | required |
| Quote/terms commitment verifiable through TOS | optional | required | required |
| TOS-backed escrow for paid committed work | optional | required | required |
| Signed Execution Receipt | required | required | required |
| Receipt commitment/verifiability through TOS | optional | required | required |
| TOS-backed settlement proof | optional | required | required |
| Proof-of-Service evidence portability | optional | required | required |
| Canonical capability resolution independent of `atos.im` | no | optional | required |
| `atos.im` required in transaction path | allowed | allowed | no |

A protocol version MAY define named proof profiles such as `tos_verified_v1`. A Quote MUST identify the proof profile when the resolved mode is `verified` or `native`.

### 3.1 Managed Mode

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

### 3.2 Verified Mode

Verified Mode preserves the `atos.im` experience while making the economically and cryptographically important checkpoints independently verifiable through TOS Network.

```text
Client
  |
atos.im ----------------------+
  |                            |
  | discovery/ranking/routing | identity/ownership
  |                            | quote commitment
  |                            | escrow
  |                            | receipt verification
  |                            | reputation evidence
  |                            | settlement/proof
  v                            v
Provider / tos-ai          tos-core -> TOS Network
```

The workload normally executes off-chain. TOS carries commitments, verification, trust evidence and settlement rather than bulk application data.

Verified Mode MUST satisfy the minimum guarantees in the table above. It is not sufficient to anchor only a final settlement transaction and call the execution "verified".

### 3.3 Native Mode

Native Mode removes `atos.im` as a mandatory transaction, namespace, or trust intermediary.

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

In Native Mode:

- gateways are replaceable;
- Agent and Capability identities are globally resolvable without relying on an `atos.im` database as the canonical source;
- capability ownership and manifest/version commitments are TOS-backed;
- paid committed work uses TOS-backed escrow/settlement;
- Execution Receipts and Proof-of-Service evidence are network-verifiable;
- provider execution can still occur off-chain through MCP, A2A, HTTP, `tos-ai`, or another compatible runtime;
- failure or censorship of `atos.im` MUST NOT make the underlying native capability economy unavailable.

Native Mode means decentralized trust and commerce, not "put the model execution on consensus."

## 4. One Public Protocol

The three concrete modes MUST NOT create three client APIs. Clients continue to use the compact ATOS surface:

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
  "requested_trust_mode":"auto",
  "proof_requirements": {
    "network_verifiable_receipt": true
  },
  "max_price":{"amount":"10.00","currency":"USD"}
}
```

`auto` selects a concrete mode satisfying caller trust, proof, spending, jurisdiction, latency, provider, and network-availability constraints.

The authoritative Quote MUST state the resolved concrete `trust_mode` before financial commitment.

## 5. TOS Is Not the Bulk Data Plane

"TOS-backed" MUST NOT mean storing all application payloads on-chain.

TOS Network is primarily the **Trust + Economic + Proof Plane**.

Normally off-chain:

- prompts and private inputs;
- credentials, context and memory;
- source documents and large artifacts;
- images, audio and video;
- private provider implementation details;
- intermediate execution state.

Depending on resolved trust mode, TOS MAY or MUST anchor/commit:

- Agent identity and attestations;
- Capability ownership and manifest/version commitments;
- Quote/terms commitments;
- escrow state;
- optional input commitment;
- output/artifact commitment;
- signed Execution Receipt commitment;
- settlement state;
- dispute outcome commitment;
- reputation evidence and audit proofs.

Use commitments/hashes rather than plaintext whenever the underlying data is private, large or commercially sensitive.

"On-chain" in the ATOS protocol means that a state transition or commitment is verifiable against TOS Network. Implementations MAY batch, aggregate, or commit multiple events efficiently as long as an independent verifier can prove the relevant event and the required ordering/finality guarantees are preserved.

## 6. Capability Model

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

`auto` MUST NOT appear in `supported_trust_modes`.

The public Capability ID MUST be federation-safe and MUST NOT depend solely on an `atos.im` database primary key.

A capability's mutable search metadata and its immutable/versioned trust commitments are separate concepts. Search metadata may be cached and re-indexed; a quoted capability version MUST resolve to an immutable manifest/version commitment for `verified` and `native` execution.

## 7. Global Addressability

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

Globally minted identifiers MUST be collision-resistant across gateways. The final encoding MAY be self-certifying, provider-key-derived, or issuer-namespaced; the encoding decision is deferred, but a plain gateway-local auto-increment database key is not acceptable as a global identifier.

The design MUST distinguish:

- gateway-local IDs;
- globally resolvable IDs;
- immutable manifest/version commitments;
- TOS-anchored ownership records.

## 8. Decentralized Discovery

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

A search result MUST distinguish gateway-computed ranking/reputation summaries from independently verifiable TOS-backed facts.

## 9. Gateway Federation

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

Gateway-specific ranking scores, account IDs, billing records and local job metadata MAY remain gateway-local. They MUST NOT be presented as globally canonical protocol state.

## 10. Execution Receipts and Proof-of-Service

Execution Receipts are a core ATOS trust primitive, not merely billing records.

A signed receipt SHOULD establish or commit to:

```text
WHO performed the work
WHAT capability/version was used
FOR WHOM
WHEN
UNDER WHICH quote/terms
WHICH concrete trust mode applied
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
  "trust_mode":"verified",
  "proof_profile":"tos_verified_v1",
  "input_commitment":"sha256:...",
  "output_commitment":"sha256:...",
  "usage_commitment":"sha256:...",
  "result":"success",
  "provider_signature":"...",
  "network_proof_ref":"tos:..."
}
```

### Proof-of-Service

**Proof-of-Service** is the portable evidence graph produced by completed capability executions.

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

Raw private job contents are not reputation evidence; cryptographic commitments and outcome attestations are.

## 11. Three Architectural Planes

### Gateway / Control Plane

Onboarding, auth/session UX, discovery/ranking, quote presentation, policy/spending controls, routing, risk, observability, managed billing and managed disputes.

### Execution / Data Plane (`tos-ai` + providers)

Provider/worker runtime, jobs, streaming, model/MCP/HTTP/GPU/local/human adapters, sandboxing, artifacts, resource accounting and receipt signing.

### Trust / Economic / Proof Plane (`tos-core` + TOS Network)

Global identity, capability ownership, registry commitments/events, reputation evidence, escrow, receipt verification, settlement, dispute commitments and audit/proof.

**The blockchain is not the bulk execution data plane.**

## 12. Legal Call Paths

The modularity rule remains:

> **tos-ai is execution, not marketplace. tos-core is trust/economy/proof, not AI orchestration.**

```text
ATOS Gateway -> tos-ai       execution
ATOS Gateway -> tos-core     trust/economy/proof
tos-ai       -> tos-core     receipt/identity/settlement lifecycle
tos-core     -> TOS Network  consensus/ledger/P2P commitments
```

Ordinary ATOS schemas MUST NOT leak consensus internals, validators, gas units, contract addresses or node topology.

Managed implementations MAY bypass `tos-core` for managed-only trust/economic state. Verified and Native guarantees MUST route through the defined `tos-core` trust/economy/proof boundary or an equivalent protocol-compatible verifier.

## 13. Quote and Settlement Semantics

Every financially committing Quote MUST state:

- `requested_trust_mode`;
- resolved concrete `trust_mode`;
- capability/version and immutable manifest commitment where required;
- provider;
- currency and maximum price;
- expiry;
- terms commitment;
- settlement model;
- dispute policy reference/hash;
- proof profile and proof availability.

```json
{
  "quote_id":"q_...",
  "capability_id":"cap_...",
  "requested_trust_mode":"auto",
  "trust_mode":"verified",
  "proof_profile":"tos_verified_v1",
  "price":{"total_max":"5.25","currency":"USD"},
  "settlement":{"backend":"tos","escrow":true},
  "proof":{"execution_receipt":true,"settlement_proof":true},
  "expires_at":"...",
  "terms_hash":"sha256:...",
  "dispute_policy_hash":"sha256:..."
}
```

Managed Mode may use ATOS's internal ledger. Verified and Native modes use the TOS-backed settlement guarantees defined by their proof profile.

Client-facing currency does not have to equal provider settlement asset. Fiat/credits may be presented to the client while a gateway, payment processor, or sponsor funds the corresponding TOS-backed settlement position.

## 14. Mode Selection Policy

Users and agents express outcomes, not blockchain mechanics:

```text
Use the cheapest provider.
Require a network-verifiable receipt.
Require TOS-backed settlement.
Do not use centralized settlement.
Maximum $10 autonomous spend.
```

Example:

```json
{
  "requested_trust_mode":"auto",
  "proof_requirements":{
    "network_verifiable_receipt":true,
    "tos_settlement":false
  }
}
```

The ATOS Skill/gateway translates policy into routing constraints. Agents should not reason about gas, validators, chain IDs or wallet derivation paths.

If no concrete mode satisfies the policy, the gateway MUST return a mode/proof availability error rather than silently weakening the requirement.

## 15. Failure, Downgrade and Censorship Model

### Managed

`atos.im` is in the critical path. Its availability and policies define service availability.

### Verified

`atos.im` may remain in the routing/execution path, but TOS-backed ownership, quote, receipt and settlement evidence can be independently verified. Gateway failure must not erase already committed proofs.

### Native

No single gateway is authoritative. A client can resolve the same globally addressable supply through another compatible gateway/indexer. TOS-backed trust and settlement survive loss of `atos.im`.

### No silent downgrade

After Quote issuance:

```text
verified -> managed   forbidden without re-quote
native   -> managed   forbidden without re-quote
native   -> verified  forbidden without re-quote
```

A network outage, proof failure, expired commitment, or unavailable escrow path causes the committed call to fail/requote; it does not weaken the user's trust contract.

This is the architectural boundary between **a marketplace using a blockchain** and **an open Agent Internet**.

## 16. Migration Strategy

ATOS can ship progressively without changing its public mental model.

```text
Phase A: Managed
atos.im DB + credits + managed providers

Phase B: Verified
atos.im UX + tos-ai execution + tos-core/TOS proofs and settlement

Phase C: Native
federated gateways + decentralized registry/indexers + TOS-backed trust economy
```

The migration rule is **add verifiability without breaking usability**.

Existing managed capabilities can progressively gain `verified` and `native` support without receiving a new Agent-facing capability type.

From v0.2 onward, however, public schemas MUST already distinguish request-mode selection from resolved-mode execution so the later phases do not require a breaking API rewrite.

## 17. Architecture Invariants

1. **One Capability Model.** Human, agent, API, GPU and other supply are adapters behind Capabilities.
2. **One Client Protocol.** Managed, Verified and Native do not fork MCP/A2A/REST contracts.
3. **`auto` is request-only.** It never appears as a resolved Quote/Job/Receipt mode.
4. **Mode is immutable at commitment.** A Quote states the final trust mode and proof profile.
5. **No silent downgrade.** A weaker mode requires a new Quote and new approval when applicable.
6. **No mandatory wallet for consumers.** Mainstream clients can use fiat/credits.
7. **No mandatory chain payloads.** Private and bulk data stay off-chain by default.
8. **No gateway owns the namespace.** Global IDs are federation-safe.
9. **Search is competitive.** TOS anchors facts; gateways/indexers rank them.
10. **Receipts are portable evidence.** Verified/native execution creates independently checkable proof.
11. **tos-ai executes; tos-core trusts and settles.** Plane boundaries remain strict.
12. **atos.im is important but replaceable.** Native ATOS survives without it.

## 18. Strategic Positioning

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

TOS Network provides the decentralized trust, proof and economic substrate that makes the protocol open, portable and independently verifiable.
