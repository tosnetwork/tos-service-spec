# ATOS Native Implementation Roadmap

This roadmap defines implementation order and acceptance gates. Architecture is
defined by `ARCHITECTURE.md`; contract transitions are defined by
`NATIVE_REGISTRY_STATE_MACHINES.md`.

## 1. Gate A — Protocol freeze

Deliver:

- clean `atos.native.v1` schema;
- network domain, identifiers, action cells, policies, state cells, errors;
- deterministic registration and Accepted Quote vectors; and
- explicit repository ownership.

Accept when two independent implementations reproduce every frozen digest and
reject all negative mutations.

**Current status:** schema and initial registration vector implemented; a
second independent implementation is still required.

## 2. Gate B — Native Registry contract

Deliver:

- deterministic Agent and Capability accounts;
- complete state machines;
- live policy authorization;
- atomic Capability transfer;
- direct typed-state resolution; and
- contract security review.

Accept when the full lifecycle passes on a local chain, the exported code hash
matches the frozen vector, and adversarial tests show no unauthorized or
partial transition.

**Current status:** implementation and local verification complete;
independent security review remains.

## 3. Gate C — Public testnet registry

Deliver:

- reproducible contract build and deployment manifest;
- public code BOC and code hash;
- multi-endpoint finality configuration;
- wallet action signing;
- registry explorer and typed-state verifier; and
- recovery and revocation drill.

Accept when an independently operated client registers, updates, transfers,
revokes, and resolves objects without trusting the reference gateway.

## 4. Gate D — Decentralized discovery

Deliver:

- finalized-state indexer with reorg handling;
- content-addressed manifest retrieval;
- deterministic chain-derived records;
- clearly labeled local ranking and health metadata;
- checkpointed pagination; and
- independent index reconstruction.

Accept when two indexers built from the same finalized checkpoint agree on all
canonical fields and a client verifies every result without indexer trust.

## 5. Gate E — Native commerce

Deliver:

- interoperable Quote Proposal format;
- deterministic Accepted Quote commitment and TOS transaction;
- endpoint and execution-signer binding;
- escrow lifecycle;
- signed execution receipts;
- dispute and settlement transitions; and
- content-addressed artifact delivery.

Accept when a client accepts a proposal through one gateway, executes through
another, and independently verifies the finalized Quote, escrow, receipt, and
settlement facts.

## 6. Gate F — Open gateway interoperability

Deliver:

- gateway discovery document;
- search and proposal protocol;
- canonical error and retry semantics;
- capability and version negotiation;
- relay and resolver conformance tests;
- pre-acceptance routing and post-acceptance failover rules; and
- at least two independent gateway implementations.

Accept when either gateway can disappear at every safe handoff point without
loss of identity, ownership, accepted terms, or settlement correctness.

## 7. Gate G — Production readiness

Deliver:

- independent contract and protocol audits;
- production key custody and wallet recovery;
- endpoint diversity and finality incident procedures;
- load, storage, denial-of-service, and fee-budget evidence;
- monitoring for code, state, quorum, and finality divergence;
- reproducible releases and signed deployment artifacts; and
- operator runbooks for degraded and emergency states.

Accept only after a multi-operator exercise completes discovery, Quote
acceptance, paid execution, receipt verification, settlement, gateway failure,
provider failure, endpoint disagreement, and client recovery.

## 8. Work ordering rule

Do not build product surfaces on facts that have not passed the preceding
authority gate. In particular:

- discovery follows registry finality;
- execution follows Accepted Quote finality;
- settlement follows receipt verification;
- convenience projections follow typed-state decoding; and
- federation follows single-gateway conformance.

## 9. Immediate work

1. Obtain an independent audit of the registry contract and `nativecore`.
2. Add a second vector implementation outside the Go/TVM codebase.
3. Deploy the frozen registry code to a public TOS testnet.
4. Implement wallet-native action signing and finalized lifecycle tests.
5. Specify the discovery record and checkpoint pagination contract.
6. Implement the Accepted Quote transaction and escrow state machine.
