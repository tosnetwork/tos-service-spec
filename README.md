# ATOS Native Protocol Specification

ATOS is an open gateway protocol for discovering and using agents whose
identity, capabilities, commercial commitments, and execution authority are
verifiable from finalized TOS state.

The protocol identifier is exactly `atos_native_v1`.

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

The Registry objects and relay/resolve service are implemented. Accepted Quote
commitment construction exists, while its TOS transaction, escrow, execution
Receipt, and settlement remain the next commercial delivery gate. See
`docs/ROADMAP.md` for evidence-backed status, implementation order, and
acceptance gates.

## System boundaries

- TOS contracts validate registry transitions and store canonical state.
- `tos-protocol` builds canonical cells, verifies signatures, relays messages,
  and resolves finalized state through independent endpoints.
- `atos` authenticates transport clients and exposes the Native service.
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

- [Decentralized Agent-to-Agent Use Cases](docs/A2A_USE_CASES.md) explains the
  interaction lifecycle, suitable paid-agent applications, the roles of TOS
  and TOS-network stablecoins, and when to batch many off-chain messages into one
  settlement.
- [Product and Commercial Strategy](docs/PRODUCT_STRATEGY.md) defines market
  positioning, the initial software-work wedge, revenue paths, development
  priorities, risks, and evidence required to establish a viable business.

## Normative contract

- Protobuf: [`proto/atos/native/v1/native.proto`](proto/atos/native/v1/native.proto)
- Identifiers: [`docs/NATIVE_IDENTIFIERS_V1.md`](docs/NATIVE_IDENTIFIERS_V1.md)
- Identity policy: [`docs/NATIVE_IDENTITY_V1.md`](docs/NATIVE_IDENTITY_V1.md)
- TVM representation: [`docs/NATIVE_REGISTRY_TVM_V1.md`](docs/NATIVE_REGISTRY_TVM_V1.md)
- Submission and resolution: [`docs/NATIVE_REGISTRY_RPC_V1.md`](docs/NATIVE_REGISTRY_RPC_V1.md)
- Security review: [`docs/NATIVE_REGISTRY_SECURITY_REVIEW.md`](docs/NATIVE_REGISTRY_SECURITY_REVIEW.md)
- Public testnet gate: [`docs/NATIVE_REGISTRY_PUBLIC_TESTNET_GATE.md`](docs/NATIVE_REGISTRY_PUBLIC_TESTNET_GATE.md)
- Quotes and settlement: [`docs/SETTLEMENT.md`](docs/SETTLEMENT.md)
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
| `atos-spec` | Normative schema, rules, and frozen vectors |
| `tos` | TVM contract and consensus execution |
| `tos-protocol` | Canonical encoding, relaying, resolution, and verification |
| `atos` | Reference Native gateway and transport authentication |
| `tos-ai` | Execution workers and result production |

## Repository layout

```text
docs/                                      Native architecture and protocol rules
deployments/                               public-network deployment evidence
proto/atos/native/v1/native.proto          sole normative wire schema
test-vectors/atos-native-v1-registry.json   frozen Agent and Capability vectors,
                                           addresses, and negative mutations
```

Do not add a second object schema beside the Native protobuf contract. New
canonical encodings belong in the Native schema and must include reproducible
vectors. Product-specific discovery views remain derived interfaces.

This repository describes a greenfield protocol. There is no deployed earlier
ATOS protocol whose behavior must be preserved.
