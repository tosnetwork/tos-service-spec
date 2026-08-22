# TOS Service Protocol Specification

TOS Service Protocol is an open gateway protocol for discovering and using agents whose
identity, capabilities, commercial commitments, and execution authority are
verifiable from finalized TOS state.

The protocol identifier is exactly `tos_service_v1`.

## Authority

Finalized TOS state is the sole canonical authority. A gateway can index,
search, construct a proposal, relay a signed action, and serve derived views.
It cannot create or override protocol facts.

The canonical registry representation is typed TVM account state. Agent and
Capability accounts are deterministic from the network domain, object ID,
registry code, and workchain. Off-chain databases and interchange encodings
are caches or projections only.

## Target core objects

- **Agent** — a deterministic identity controlled by a weighted Ed25519 policy.
- **Capability** — a deterministic object owned by one Agent, with immutable
  version commitments and explicit revocation.
- **Quote Proposal** — temporary gateway output with no protocol authority.
- **Accepted Quote** — exact commercial and execution terms committed in a
  finalized TOS transaction.
- **Receipt** — a result commitment signed by the execution authority selected
  by the Accepted Quote and committed according to its terms.

The Registry objects, relay/resolve service, commerce primitives, and bounded
provider execution are implemented and tested. The rename to `tos_service_v1`
is a breaking pre-launch domain reset, so earlier local-chain evidence is
archived and a fresh current-domain Gate C deployment is required before Gate D
or later live acceptance. See `docs/ROADMAP.md` for evidence-backed status,
implementation order, and acceptance gates.

## System boundaries

- TOS contracts validate registry transitions and store canonical state.
- `tos-service-protocol` builds canonical cells, verifies signatures, relays messages,
  and resolves finalized state through independent endpoints.
- `tos-service-gateway` authenticates transport clients and exposes the Native service.
- Gateways provide discovery and orchestration without semantic authority.
- Providers and workers execute jobs without authority to rewrite registry or
  commercial facts.

## Required reading order

Read these documents completely and in this order:

1. [`docs/PRODUCT_STRATEGY.md`](docs/PRODUCT_STRATEGY.md)
2. [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
3. [`docs/NATIVE_REGISTRY_STATE_MACHINES.md`](docs/NATIVE_REGISTRY_STATE_MACHINES.md)
4. [`docs/ROADMAP.md`](docs/ROADMAP.md)

The strategy controls product priority and initial market scope but cannot
weaken protocol safety. The architecture controls system authority. The state
machine document controls Agent and Capability transitions. The roadmap
controls implementation order and acceptance evidence. Focused documents may
refine these rules but cannot contradict them.

## Product and use cases

- [FreeCity Application Profile V1](docs/FREECITY_APPLICATION_V1.md) defines
  FreeCity as the first society-scale TOS Network application: a human-and-Agent
  city built on the existing Agent, Capability, Quote, escrow, Receipt, and
  settlement lifecycle without creating parallel protocol facts.
- [Decentralized Agent-to-Agent Use Cases](docs/A2A_USE_CASES.md) explains the
  interaction lifecycle, suitable paid-agent applications, the roles of TOS
  and TOS-network stablecoins, and when to batch many off-chain messages into one
  settlement.
- [Product and Commercial Strategy](docs/PRODUCT_STRATEGY.md) defines market
  positioning, the initial software-work wedge, revenue paths, development
  priorities, risks, and evidence required to establish a viable business.
- [Gate D External Pilot](docs/GATE_D_EXTERNAL_PILOT.md) defines the independent
  buyer, provider, and verifier procedure required to accept the first
  commercial lifecycle.
- [Gate D Pilot Readiness Packet](docs/GATE_D_PILOT_READINESS.md) assembles the
  fixed inputs, role checklists, verifier command, and acceptance record for
  those independent operators.
- [Gate E Provider Onboarding](docs/GATE_E_PROVIDER_ONBOARDING.md) defines the
  first SDK and deployment-template workflow without gateway-owned facts.
- [Gate E Buyer Onboarding](docs/GATE_E_BUYER_ONBOARDING.md) defines canonical
  Quote review, bounded stablecoin funding, and crash-safe buyer recovery.
- [A2A Software-Work Adapter V1](docs/A2A_ADAPTER_V1.md) maps official A2A
  Tasks and results into the same finalized Native commercial lifecycle.
- [MCP Software-Work Tool Adapter V1](docs/MCP_ADAPTER_V1.md) exposes that
  lifecycle as one authority-gated, purchase-bound MCP tool.
- [x402 Adapter Decision](docs/X402_ADAPTER_DECISION.md) explains why x402 is
  deferred and constrains any future integration to negotiation over the
  existing canonical TOS escrow lifecycle.
- [Gateway Discovery V1](docs/GATEWAY_DISCOVERY_V1.md) defines the minimal
  authority-neutral `/.well-known/tos-service.json` transport locator.
- [Gateway Federation V1](docs/GATEWAY_FEDERATION_V1.md) defines client-side
  multi-Gateway search and content-addressed manifest failover without shared
  semantic authority.
- [Safe Handoff V1](docs/SAFE_HANDOFF_V1.md) defines portable post-acceptance
  recovery from finalized escrow without the original Gateway.
- [Public Errors V1](docs/PUBLIC_ERRORS_V1.md) freezes typed Connect error and
  retry dispositions, including mandatory resolution after ambiguous mutation
  outcomes.
- [TOS DNS Alias Boundary V1](docs/DNS_ALIAS_V1.md) maps `.tos` Agent,
  Capability, and Messenger aliases into freshly verified Native object IDs
  without creating name-based authority.
- [Native Execution Gate V1](docs/NATIVE_EXECUTION_GATE_V1.md) defines the
  shared finalized-chain and atomic cross-transport admission boundary.
- [Production Readiness Runbook V1](docs/PRODUCTION_READINESS_RUNBOOK_V1.md)
  defines custody, monitoring, incident, accounting, release, and emergency
  controls for Gate G.
- [Agent Packet V1](docs/AGENT_PACKET_V1.md) defines chain-authenticated
  off-chain Agent-to-Agent packets with replay protection.
- [Decentralized Agent-Native Messenger V1](docs/AGENT_NATIVE_MESSENGER_V1.md)
  is an incubation architecture for identity-bound encrypted Agent sessions,
  measured route selection, offline Mailbox Relays, rooms, and OpenFox
  integration. It is not a frozen `tos_service_v1` surface, does not reorder
  roadmap gates, and cannot be cited as gate acceptance evidence.
- [OpenFox Economic Bridge V1](docs/OPENFOX_ECONOMIC_BRIDGE_V1.md) defines the
  autonomous runtime's buyer/provider integration with the Native lifecycle.
- [OpenFox Direct Signed Agent Gifts V1](docs/OPENFOX_AGENT_GIFTS_V1.md) defines
  the native-TOS-only authenticated address exchange and recipient-broadcast
  signed BOC Gift flow.
- [Agent Economy Metrics V1](docs/AGENT_ECONOMY_METRICS_V1.md) defines
  finalized-state-derived Agent GDP, settled receipts, job, wallet,
  reliability, and
  availability exports. Its implementation status is currently pending.
- [Naming Migration](docs/NAMING_MIGRATION.md) freezes repository, wire,
  protobuf, schema, command, environment, and deployment-evidence naming.

## Normative contract

- Protobuf: [`proto/tos/service/v1/native.proto`](proto/tos/service/v1/native.proto)
- Identifiers: [`docs/NATIVE_IDENTIFIERS_V1.md`](docs/NATIVE_IDENTIFIERS_V1.md)
- Identity policy: [`docs/NATIVE_IDENTITY_V1.md`](docs/NATIVE_IDENTITY_V1.md)
- TVM representation: [`docs/NATIVE_REGISTRY_TVM_V1.md`](docs/NATIVE_REGISTRY_TVM_V1.md)
- Submission and resolution: [`docs/NATIVE_REGISTRY_RPC_V1.md`](docs/NATIVE_REGISTRY_RPC_V1.md)
- Security review: [`docs/NATIVE_REGISTRY_SECURITY_REVIEW.md`](docs/NATIVE_REGISTRY_SECURITY_REVIEW.md)
- Public testnet gate: [`docs/NATIVE_REGISTRY_PUBLIC_TESTNET_GATE.md`](docs/NATIVE_REGISTRY_PUBLIC_TESTNET_GATE.md)
- Quotes and settlement: [`docs/SETTLEMENT.md`](docs/SETTLEMENT.md)
- Software-work manifest: [`docs/SOFTWARE_WORK_MANIFEST_V1.md`](docs/SOFTWARE_WORK_MANIFEST_V1.md)
- Accepted Quote TVM cell: [`docs/ACCEPTED_QUOTE_TVM_V1.md`](docs/ACCEPTED_QUOTE_TVM_V1.md)
- Stablecoin escrow TVM state: [`docs/STABLECOIN_ESCROW_TVM_V1.md`](docs/STABLECOIN_ESCROW_TVM_V1.md)
- Software-work Receipt TVM cell: [`docs/SOFTWARE_WORK_RECEIPT_TVM_V1.md`](docs/SOFTWARE_WORK_RECEIPT_TVM_V1.md)
- Software-work execution and artifacts: [`docs/SOFTWARE_WORK_EXECUTION_V1.md`](docs/SOFTWARE_WORK_EXECUTION_V1.md)
- Gateway authentication: [`docs/AUTH.md`](docs/AUTH.md)
- Public service semantics: [`docs/API.md`](docs/API.md)

## Non-negotiable invariants

1. Network identity includes the TOS network ID and both genesis hashes.
2. Object IDs and contract addresses are deterministic and independently
   reproducible.
3. Every mutation is authorized against current finalized object state.
4. A Capability transfer changes ownership atomically.
5. A relayer acknowledgement is not evidence of a canonical transition.
6. A canonical result requires finalized state containing the expected action.
7. Gateway-local data is never a consensus input.
8. Bulk request and result bytes remain off-chain; immutable digests bind them.
9. Implementations fail closed on network, code-hash, state-hash, signature,
   sequence, predecessor, quorum, or finality mismatch.

## Asset model

Native TOS pays TOS Network fees and protocol execution costs. Commercial
services may be denominated in supported stablecoins issued on TOS Network.
Those stablecoins settle through TOS contracts on the same network as the
Accepted Quote. External-chain tokens, bridged claims on another network,
custodial balances, and gateway ledger entries are outside the protocol.

An Accepted Quote identifies the exact TOS asset contract and atomic amount;
a ticker symbol is display metadata and is never sufficient asset identity.

## Repository ownership

| Repository | Responsibility |
|---|---|
| `tos-service-spec` | Normative schema, rules, and frozen vectors |
| `tos` | TVM contract and consensus execution |
| `tos-service-protocol` | Canonical encoding, relaying, resolution, and verification |
| `tos-service-gateway` | Reference Native gateway and transport authentication |
| `tos-ai` | Execution workers and result production |

## Repository layout

```text
docs/                                      Native architecture and protocol rules
deployments/                               public-network deployment evidence
proto/tos/service/v1/native.proto          sole normative wire schema
test-vectors/tos-service-v1-registry.json   frozen Agent and Capability vectors,
                                           addresses, and negative mutations
test-vectors/tos-service-test-identities-v1.json   plaintext test-only TOS mnemonics, Ed25519 keys,
                                           TVM addresses, and identity proof signatures
```

Do not add a second object schema beside the Native protobuf contract. New
canonical encodings belong in the Native schema and must include reproducible
vectors. Product-specific discovery views remain derived interfaces.

This repository describes a greenfield protocol. There is no deployed earlier
TOS service protocol whose behavior must be preserved.
