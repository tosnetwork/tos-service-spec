# TOS Service Documentation Map

This directory is organized logically around
[The Open System for the Agentic Internet](TOS_AGENTIC_INTERNET_OPERATION_ARCHITECTURE_V1.md).
Files remain in one directory for link stability; this map defines their
dependency and reading order.

## 1. Root architecture and delivery control

1. [Agentic Internet Operation Architecture V1](TOS_AGENTIC_INTERNET_OPERATION_ARCHITECTURE_V1.md)
2. [System Architecture](ARCHITECTURE.md)
3. [Product Strategy](PRODUCT_STRATEGY.md)
4. [Implementation Roadmap](ROADMAP.md)

The root architecture controls layer boundaries. Strategy selects priorities
but cannot narrow the protocol mission or weaken safety. The roadmap records
implementation evidence and must not present an application profile as the
whole network.

## 2. Finalized authority

- [Native Identity V1](NATIVE_IDENTITY_V1.md)
- [Native Identifiers V1](NATIVE_IDENTIFIERS_V1.md)
- [Registry State Machines](NATIVE_REGISTRY_STATE_MACHINES.md)
- [Registry TVM V1](NATIVE_REGISTRY_TVM_V1.md)
- [Registry RPC V1](NATIVE_REGISTRY_RPC_V1.md)
- [Registry Security Review](NATIVE_REGISTRY_SECURITY_REVIEW.md)
- [Capabilities](CAPABILITIES.md)

These documents define currently implemented Agent and Capability authority.

## 3. Operation transport and propagation

- [Agent Packet V1](AGENT_PACKET_V1.md)
- [Agent-Native Messenger V1](AGENT_NATIVE_MESSENGER_V1.md)
- [Messenger Conversation and Commerce V1](AGENT_NATIVE_MESSENGER_CONVERSATION_AND_COMMERCE_V1.md)
- [Gateway Discovery V1](GATEWAY_DISCOVERY_V1.md)
- [Gateway Federation V1](GATEWAY_FEDERATION_V1.md)
- [DNS Alias Boundary V1](DNS_ALIAS_V1.md)
- [Edge CDN Architecture V1](EDGE_CDN_ARCHITECTURE_V1.md)

These are Carrier, routing, addressing, storage, or delivery profiles. A
Carrier may admit and rank operations but is not protocol authority.

## 4. Publication and discovery profiles

- [Agent Intent Exchange V1](AGENT_INTENT_EXCHANGE_V1.md)
- [Paid Demand Discovery V1](AGENT_PAID_DEMAND_DISCOVERY_V1.md)
- [Society of Agents Gap Analysis](SOCIETY_OF_AGENTS_GAP_ANALYSIS.md)
- [FreeCity Application Profile V1](FREECITY_APPLICATION_V1.md)

Intent is a generic publication profile. Paid Demand and FreeCity are narrower
application profiles above it.

## 5. Value, agreement, and settlement profiles

- [OpenFox Agent Gifts V1](OPENFOX_AGENT_GIFTS_V1.md)
- [Settlement](SETTLEMENT.md)
- [Accepted Quote TVM V1](ACCEPTED_QUOTE_TVM_V1.md)
- [Stablecoin Escrow TVM V1](STABLECOIN_ESCROW_TVM_V1.md)
- [Software Work Receipt TVM V1](SOFTWARE_WORK_RECEIPT_TVM_V1.md)
- [Paid-Demand Accepted-Quote Binding V1](PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md)
- [Agent Gas Sponsorship and Transaction Relay V1](AGENT_GAS_SPONSORSHIP_AND_TRANSACTION_RELAY_V1.md)
- [Decentralized Agent Guarantor Service V1](AGENT_GUARANTOR_SERVICE_V1.md)
- [Native Execution Gate V1](NATIVE_EXECUTION_GATE_V1.md)
- [Semantic Action Identity V1](SEMANTIC_ACTION_IDENTITY_V1.md)

The on-chain path is optional for discovery and conversation. It becomes
authoritative only after parties explicitly select that profile.

## 6. OpenFox application compositions

- [OpenFox Economic Bridge V1](OPENFOX_ECONOMIC_BRIDGE_V1.md)
- [OpenFox Autonomous Messenger Economy Plan](OPENFOX_AUTONOMOUS_MESSENGER_ECONOMY_PLAN.md)
- [OpenFox Autonomous Earning — Operation-Composed Cross-Repository Design](OPENFOX_AUTONOMOUS_EARNING_CROSS_REPOSITORY_DESIGN.md)
- [OpenFox Autonomous Earning — Operation-Composed Implementation Plan](OPENFOX_AUTONOMOUS_EARNING_IMPLEMENTATION_PLAN.md)
- [OpenFox Autonomous Earning Roadmap](OPENFOX_AUTONOMOUS_EARNING_ROADMAP.md)

These documents explain how OpenFox composes generic operations, AI reasoning,
skills, runtime policy, and optional settlement. They do not define new
business-category opcodes.

## 7. Software-work application profile

- [Software Work Manifest V1](SOFTWARE_WORK_MANIFEST_V1.md)
- [Software Work Execution V1](SOFTWARE_WORK_EXECUTION_V1.md)
- [A2A Adapter V1](A2A_ADAPTER_V1.md)
- [MCP Adapter V1](MCP_ADAPTER_V1.md)
- [A2A Use Cases](A2A_USE_CASES.md)

Software work is the first deeply specified commerce profile, not the root
definition of TOS.

## 8. Operations and acceptance evidence

- [Production Readiness Runbook V1](PRODUCTION_READINESS_RUNBOOK_V1.md)
- [Safe Handoff V1](SAFE_HANDOFF_V1.md)
- [Public Errors V1](PUBLIC_ERRORS_V1.md)
- [Gate D External Pilot](GATE_D_EXTERNAL_PILOT.md)
- [Gate D Pilot Readiness](GATE_D_PILOT_READINESS.md)
- [Gate E Buyer Onboarding](GATE_E_BUYER_ONBOARDING.md)
- [Gate E Provider Onboarding](GATE_E_PROVIDER_ONBOARDING.md)

Implementation evidence for one profile must be labeled as such and cannot be
used to claim completion of the root Agentic Internet architecture.
