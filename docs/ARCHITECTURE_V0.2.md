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

The same Capability and the same MCP/A2A/REST contracts support three concrete trust modes:

```text
managed
verified
native
```

A caller may also request:

```text
auto
```

but `auto` is only a pre-Quote selection policy, never a committed transaction mode.

**Core principle: decentralization is a selectable trust level, not a usability requirement.**

ATOS separates four concepts:

1. **ATOS Protocol** — open Agent Internet commerce/interoperability contracts.
2. **atos.im** — canonical managed implementation and reference gateway.
3. **ATOS-compatible gateways/indexers** — independently operated access/discovery implementations.
4. **TOS Network** — decentralized identity, registry commitments, reputation evidence, escrow, proof, and settlement.

Execution itself remains outside consensus. Providers and/or `tos-ai` perform work off-chain; `tos-core` verifies/commits the trust and economic facts when the selected mode requires it.

## 2. Trust-Mode Type System

ATOS v0.2 distinguishes request policy from committed state.

Client request-time type:

```text
requested_trust_mode = managed | verified | native | auto
```

Committed transaction type:

```text
trust_mode = managed | verified | native
```

Provider configuration additionally distinguishes:

```text
requested_trust_modes = provider intent
supported_trust_modes = derived active/quotable concrete modes
```

### Normative rules

1. `auto` MUST NOT appear as the final mode of a Quote, Invocation, Job, Escrow, Receipt, or settlement record.
2. A Capability MUST NOT list `auto` in provider/client concrete-mode sets.
3. `supported_trust_modes` contains only modes whose `mode_support.status` is `active`.
4. A provider cannot self-certify Verified/Native by writing public metadata.
5. `atos_quote` resolves `requested_trust_mode` to one concrete `trust_mode`.
6. The Quote's concrete mode is immutable.
7. A weaker mode requires a new Quote; there is no silent downgrade.

## 3. Three Modes, One Protocol

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
                         Provider / tos-ai
                                  |
                               tos-core
                                  |
                             TOS Network
```

The modes are trust/economic policies, not separate products and not separate Capability types.

## 4. Normative Proof Profiles

A trust-mode name must have a portable meaning across implementations.

ATOS v0.2 defines initial standard proof profiles:

```text
verified -> tos_verified_v1
native   -> tos_native_v1
```

Managed Mode does not require a standard network proof profile.

`tos_native_v1` extends all `tos_verified_v1` transaction guarantees with gateway/namespace independence.

See `docs/PROOF_PROFILES.md` for the normative guarantee sets.

A gateway MAY provide stronger guarantees than the selected standard profile, but MUST NOT use a standard profile name for weaker guarantees.

## 5. Guarantee Matrix

| Guarantee | managed | verified (`tos_verified_v1`) | native (`tos_native_v1`) |
|---|---:|---:|---:|
| Gateway may own local account/search/job state | yes | yes | yes, but not canonical Native trust facts |
| TOS-verifiable provider identity / capability ownership | optional | required | required |
| Immutable quoted capability manifest/version commitment | optional | required | required |
| TOS-verifiable Quote/terms commitment | optional | required | required |
| Enforceable TOS-backed escrow for paid committed work | optional | required | required |
| Authorized-signer Execution Receipt | required | required | required |
| TOS-verifiable signer authorization | optional | required | required |
| TOS-verifiable Receipt commitment | optional | required | required |
| TOS-backed settlement proof | optional | required | required |
| Portable Proof-of-Service evidence | optional | required | required |
| Canonical capability resolution independent of `atos.im` | no | not required | required |
| `atos.im` required in transaction path | allowed | allowed | no |
| Raw prompts/files/results stored on-chain | no | no | no |
| Model execution inside TOS consensus | no | no | no |

## 6. Managed Mode

Managed Mode is the default mainstream product experience and may complete entirely inside `atos.im`.

```text
Client
  |
atos.im
  +-- identity/session
  +-- capability index/ranking
  +-- quote engine
  +-- ATOS Credits / fiat accounting
  +-- job orchestration
  +-- managed reputation
  +-- managed reservation/settlement
  |
Provider / tos-ai
```

Properties:

- no wallet required;
- no blockchain knowledge required;
- centralized databases and ledgers are allowed;
- optimized for latency, cost, and operational simplicity;
- receipts are signed but need not be TOS-verifiable;
- suitable for ordinary consumers and high-volume low-value calls.

Managed Mode remains permanent even after TOS-backed infrastructure matures.

## 7. Verified Mode

Verified Mode preserves the managed `atos.im` UX while making the economically and cryptographically important checkpoints independently verifiable through TOS.

```text
Client
  |
atos.im ---------------------------+
  |                                 |
  | discovery / ranking / routing  | identity / ownership
  |                                 | manifest commitment
  |                                 | quote commitment
  |                                 | enforceable escrow
  |                                 | signer authorization
  |                                 | receipt verification
  |                                 | settlement / evidence
  v                                 v
Provider / tos-ai               tos-core -> TOS Network
```

The workload normally executes off-chain.

Verified Mode MUST satisfy `tos_verified_v1` or a stronger compatible profile. Anchoring only a final payment transaction is not enough to call an execution Verified.

## 8. Native Mode

Native Mode removes `atos.im` as a mandatory namespace, trust, or transaction authority.

```text
Client Agent
    |
    +-- atos.im gateway
    +-- partner gateway
    +-- enterprise gateway
    +-- local/open-source gateway
              |
          TOS Network
       /      |       \
 identity  registry  reputation/proof
 escrow              settlement
              |
        Provider / tos-ai / endpoint
```

Native Mode MUST satisfy `tos_native_v1` or stronger.

In Native Mode:

- Agent/provider identity is globally resolvable;
- Capability ID is federation-safe;
- ownership and manifest/version are resolvable without an `atos.im` canonical database;
- paid committed work uses enforceable TOS-backed escrow/settlement;
- Receipt signer authority is independently verifiable;
- Proof-of-Service evidence is portable;
- another compatible gateway/resolver can verify canonical trust/economic/proof state;
- failure or censorship of `atos.im` does not destroy the Native capability economy.

Native does **not** mean running LLM inference or bulk workload data inside consensus.

## 9. One Public Client Protocol

The three concrete modes MUST NOT create three MCP/A2A/REST APIs.

The compact Agent-facing surface remains:

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

Example policy request:

```json
{
  "capability_id":"cap_...",
  "requested_trust_mode":"auto",
  "proof_requirements":{
    "network_verifiable_receipt":true
  },
  "max_price":{"amount":"10.00","currency":"USD"}
}
```

For boolean proof requirements in v0.2:

- `true` means required;
- `false`/omitted means not required;
- `false` does not mean forbidden.

The authoritative Quote states the resolved concrete mode before commitment.

## 10. Capability Model

A Capability is the canonical discoverable supply object.

It may represent an agent, API, human service, GPU/worker-backed operation, local service, or other executable supply through adapters.

```json
{
  "id":"cap_...",
  "provider_id":"agt_...",
  "version":"1.2.0",
  "manifest_commitment":"sha256:...",
  "supported_trust_modes":["managed","verified"],
  "mode_support":{
    "managed":{"status":"active"},
    "verified":{"status":"active","proof_profile":"tos_verified_v1"},
    "native":{"status":"pending","proof_profile":"tos_native_v1"}
  },
  "transports":["mcp","a2a","http"]
}
```

Provider registration may request stronger modes through `requested_trust_modes`; activation is derived from certification/proof readiness.

Transport, delivery mode, reputation, and trust mode are orthogonal dimensions.

## 11. Global Addressability

ATOS v0.2 requires federation-safe Agent and Capability identifiers before federation ships.

Conceptually:

```text
atos://agent/<global-agent-id>
atos://capability/<global-capability-id>
```

The URI syntax is provisional; global resolvability is the architectural requirement.

Global IDs MUST be collision-resistant across gateways and MUST NOT simply be an `atos.im` auto-increment database key.

The system distinguishes:

- gateway-local account/database IDs;
- globally resolvable Agent/Capability IDs;
- immutable manifest/version commitments;
- TOS-anchored ownership/registry facts.

## 12. Decentralized Discovery

Semantic search does not belong in consensus.

Embeddings, ranking, personalization, anti-spam, latency prediction, price fit, and policy filtering are gateway/indexer functions.

TOS provides verifiable registry/trust events and commitments from which independent indexers can build projections.

```text
Provider
   |
Capability Manifest
   +---- Managed registration ----> atos.im registry/index
   +---- TOS registry event ------> TOS Network
                                      |
                         +------------+------------+
                         |            |            |
                      Indexer A    Indexer B    Indexer C
                         |            |            |
                      Gateway A    Gateway B    Search App
```

Consequences:

- no search engine is globally canonical;
- different gateways may rank the same supply differently;
- gateway scores remain convenience signals, not canonical TOS facts;
- `atos.im` can be the best default search experience without owning the Agent Internet.

## 13. TOS Is the Trust / Economic / Proof Plane

"TOS-backed" does not mean storing application payloads on-chain.

Normally off-chain:

- prompts and private inputs;
- API credentials;
- context/memory;
- source documents;
- images/audio/video;
- large artifacts;
- private provider implementation details;
- intermediate execution state.

Depending on mode/profile, TOS carries or proves:

- Agent/provider identity;
- Capability ownership;
- manifest/version commitment;
- Quote/terms commitment;
- enforceable escrow state;
- execution-signer authorization;
- input/output/artifact commitments where required;
- signed Receipt commitment;
- settlement/release/refund state;
- dispute outcome commitment;
- Proof-of-Service evidence.

### Batching rule

Registry, Receipt, and evidence commitments MAY be batched/aggregated if an independent verifier can prove inclusion, relevant ordering, and finality.

### Economic-state rule

A Merkle root/hash of a private centralized balance database is **not** sufficient to claim TOS-backed escrow or settlement.

When a proof profile promises TOS-backed economic state, reservation/release/settlement must be economically enforceable through the TOS-backed mechanism.

## 14. Execution Signer Model

The Provider identity and the key/runtime that attests a particular execution may differ.

Possible authorized execution signers include:

- provider agent key;
- `tos-ai` worker/runtime key;
- HTTP/MCP adapter key;
- enterprise delegated key;
- gateway execution adapter for a human-backed capability.

Conceptually:

```text
Provider / Capability ownership
          |
          v
Execution-signer authorization
          |
          v
Signed Execution Receipt
```

Example Receipt fields:

```json
{
  "provider_id":"agt_...",
  "execution_signer_id":"sig_...",
  "signer_authorization_ref":"tos:...",
  "signature":"..."
}
```

Verified/Native verification MUST establish that the signer was authorized for the quoted provider/capability/version at the relevant time.

This avoids requiring every worker to hold a provider root key while preserving service attribution.

## 15. Execution Receipts and Proof-of-Service

Execution Receipts are core ATOS trust primitives, not merely billing records.

A Receipt SHOULD establish or commit to:

```text
WHO provided the service
WHICH authorized signer attested execution
WHAT capability/version was used
FOR WHOM
WHEN
UNDER WHICH Quote/terms/proof profile
WHAT input/output/artifact commitments applied
WHAT usage/resources were charged
WHETHER result/SLA conditions were satisfied
HOW settlement resolved
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
  "execution_signer_id":"sig_...",
  "signer_authorization_ref":"tos:...",
  "signature":"...",
  "network_proof_ref":"tos:..."
}
```

### Proof-of-Service

**Proof-of-Service** is the portable evidence graph derived from completed executions and outcomes.

```text
Execution Receipts
        |
        v
Proof-of-Service Evidence
        +-- successful executions
        +-- completion rate
        +-- latency distributions
        +-- settlement volume
        +-- dispute outcomes
        +-- capability reliability
        +-- counterparty diversity
        |
        v
Reputation projections
```

Gateway-normalized scores may exist for UX, but Verified/Native evidence should be independently verifiable.

Raw private job payloads are not reputation evidence; commitments and outcome attestations are.

## 16. Quote Is the Trust/Economic Contract

A financially committing Quote MUST bind:

- Quote ID;
- provider;
- Capability/version and manifest commitment where required;
- `requested_trust_mode`;
- resolved concrete `trust_mode`;
- proof profile;
- price/currency/maximum;
- expiry;
- settlement backend/funding model;
- terms commitment;
- dispute-policy commitment;
- proof availability/requirements.

Example:

```json
{
  "quote_id":"q_...",
  "capability_id":"cap_...",
  "capability_version":"1.2.0",
  "requested_trust_mode":"auto",
  "trust_mode":"verified",
  "proof_profile":"tos_verified_v1",
  "price":{"total_max":"5.25","currency":"USD"},
  "settlement":{
    "backend":"tos",
    "escrow":true,
    "funding_model":"gateway_sponsored"
  },
  "terms_hash":"sha256:...",
  "dispute_policy_hash":"sha256:..."
}
```

Client-facing asset and provider settlement asset may differ.

A gateway may sponsor the TOS-side escrow for a fiat/credit-paying Verified user, preserving walletless UX while maintaining the promised TOS-backed trade state.

## 17. No Silent Downgrade

After Quote issuance:

```text
verified -> managed   forbidden without new Quote
native   -> verified  forbidden without new Quote
native   -> managed   forbidden without new Quote
```

If required proof, signer authorization, escrow, settlement, or network infrastructure becomes unavailable, the operation must fail, wait within contract/SLA rules, or require re-quote.

A gateway cannot "helpfully" weaken the user's trust contract.

## 18. Three Architectural Planes

### Gateway / Control Plane

- onboarding/auth/session UX;
- discovery/ranking;
- Quote presentation;
- trust/spend policy;
- provider routing;
- rate/risk controls;
- managed billing/disputes;
- observability/caching.

### Execution / Data Plane (`tos-ai` + providers)

- provider/worker runtime;
- jobs/streaming/cancellation;
- model/MCP/HTTP/GPU/local/human adapters;
- sandboxing;
- artifact production;
- resource accounting;
- Receipt signing.

### Trust / Economic / Proof Plane (`tos-core` + TOS Network)

- global identity;
- Capability ownership/registry commitments;
- signer authorization;
- reputation evidence;
- escrow;
- Receipt verification;
- settlement;
- dispute commitments;
- proof/audit.

**The blockchain is not the bulk execution data plane.**

## 19. Legal Call Paths

The modularity rule is:

> **tos-ai executes; tos-core trusts, proves, and settles.**

```text
ATOS Gateway -> tos-ai       execution
ATOS Gateway -> tos-core     trust/economy/proof
tos-ai       -> tos-core     identity/signer/receipt/settlement lifecycle
tos-core     -> TOS Network  consensus/ledger/P2P commitments and value state
```

Ordinary ATOS schemas MUST NOT leak validator topology, gas units, raw contract addresses, wallet derivation, or consensus internals.

Managed implementations MAY keep Managed-only trust/economic state outside `tos-core`.

Verified/Native guarantees must use the protocol-compatible TOS trust/economic/proof boundary.

## 20. Gateway Federation

Federation is an architectural assumption from v0.2 even if implementation ships later.

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

A gateway may provide proprietary:

- authentication/accounts;
- fiat/credit billing;
- semantic search/ranking;
- policy/risk controls;
- caches;
- enterprise workflows;
- Managed execution.

But no gateway owns the Native protocol namespace.

Gateway-local account IDs, rankings, billing records, and caches MUST NOT be presented as globally canonical Native state.

## 21. Failure and Censorship Model

### Managed

`atos.im` may be fully in the critical path. Its availability and policies define the Managed service.

### Verified

`atos.im` may remain in routing/UX, but committed identity/Quote/Receipt/settlement evidence can be independently checked. Gateway failure must not erase already committed proofs.

### Native

No single gateway is authoritative for canonical trust/namespace/economic facts. A client can resolve and verify through another compatible implementation.

This is the boundary between **a marketplace that uses blockchain** and **an open Agent Internet**.

## 22. Migration Strategy

```text
Phase A: Managed
atos.im DB + credits + managed providers

Phase B: Verified
atos.im UX + tos-ai execution + tos-core/TOS proof and settlement

Phase C: Native
federated gateways + TOS registry/resolution + decentralized trust economy
```

Migration rule:

> **Add verifiability without breaking usability.**

Existing Managed Capabilities can gain Verified/Native support without becoming new Agent-facing Capability types.

Public v0.2 schemas already distinguish request mode, resolved mode, provider requested modes, and active supported modes so later phases do not require a breaking redesign.

## 23. Architecture Invariants

1. **One Capability Model.** Human, agent, API, GPU, and other supply are adapters behind Capabilities.
2. **One Client Protocol.** Managed/Verified/Native do not fork MCP/A2A/REST contracts.
3. **`auto` is request-only.** It never appears as a resolved transaction mode.
4. **Provider intent is not certification.** `requested_trust_modes` does not equal active `supported_trust_modes`.
5. **Quote freezes trust.** Concrete mode, proof profile, price, terms, and dispute policy are immutable for the Quote.
6. **No silent downgrade.** A weaker mode requires re-quote.
7. **No mandatory wallet for ordinary consumers.** Fiat/credits/sponsorship can abstract chain mechanics.
8. **No mandatory chain payloads.** Private/bulk data stays off-chain.
9. **Economic proof is enforceable.** A private-ledger hash is not TOS-backed escrow/settlement.
10. **No gateway owns the Native namespace.** Global IDs are federation-safe.
11. **Search is competitive.** TOS anchors facts; gateways/indexers rank them.
12. **Receipts are portable evidence.** Verified/Native executions create independently checkable proof.
13. **Authorized execution signers are first-class.** Provider root keys need not sign every execution.
14. **tos-ai executes; tos-core trusts/proves/settles.** Plane boundaries remain strict.
15. **atos.im is important but replaceable for Native.** Native ATOS survives without it.
16. **Managed remains first-class.** Decentralization is an additional guarantee, not a forced migration.

## 24. Strategic Positioning

ATOS should not be described merely as a decentralized marketplace.

A centralized marketplace owns supply, discovery, reputation, and transactions inside one platform boundary.

ATOS aims to define a common commerce/trust layer through which autonomous agents can discover capabilities, agree on terms, execute work, produce portable evidence, establish reputation, and settle value across independently operated infrastructure.

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

TOS Network supplies the decentralized identity, registry, proof, and economic guarantees that make Native ATOS open and independently verifiable.
