# ATOS Native Implementation Roadmap

This roadmap defines implementation order and acceptance gates. Product
priority is defined by `PRODUCT_STRATEGY.md`. Authority boundaries are defined
by `ARCHITECTURE.md`; Agent and Capability transitions are defined by
`NATIVE_REGISTRY_STATE_MACHINES.md`.

No later gate may weaken an earlier authority or security invariant.

## 1. Gate A — Registry protocol freeze

Deliver:

- clean `atos.native.v1` schema;
- network domain, identifiers, action cells, policies, and state cells;
- deterministic Agent and Capability registration vectors;
- stable errors and negative mutations; and
- explicit repository ownership.

Accept when two independent implementations reproduce every frozen registry
digest and reject all negative mutations.

**Current status:** schema and initial Agent registration vector implemented; a
Capability vector and second independent implementation remain.

## 2. Gate B — Registry implementation assurance

Deliver:

- deterministic Agent and Capability accounts;
- complete state machines;
- live policy authorization;
- atomic Capability transfer;
- direct typed-state resolution;
- contract and `nativecore` audit; and
- adversarial coverage aligned across TVM and protocol code.

Accept when the full lifecycle passes on a local chain, the exported code hash
matches frozen vectors, and independent review finds no unauthorized or partial
transition.

**Current status:** implementation and local testing complete; independent
security review remains.

## 3. Gate C — Public testnet authority

Deliver:

- reproducible contract build and deployment manifest;
- public code BOC, code hash, and network domain;
- multi-endpoint quorum and finality configuration;
- wallet action signing and semantic confirmation;
- registry explorer and typed-state checker; and
- recovery, transfer, and revocation drills.

Accept when an independently operated wallet registers, updates, transfers,
revokes, and resolves objects without trusting the reference gateway.

## 4. Gate D — First commercial lifecycle

This gate is the highest product priority after Registry assurance. It covers
one machine-checkable software-work profile only.

Deliver:

- immutable software-work Capability manifest profile;
- deterministic Accepted Quote commitment, vector, and TOS transaction;
- exact endpoint and execution-signer binding;
- stable-value-asset escrow with bounded TOS network fees;
- isolated compilation, deterministic test, static-analysis, dependency-scan,
  or reproducible-build execution;
- canonical Receipt binding input, toolchain, result, artifacts, usage, and
  charged amount;
- objective release and refund transitions;
- narrowly defined dispute evidence where an automatic outcome is impossible;
- content-addressed artifact delivery; and
- independent Quote, escrow, Receipt, and settlement resolution.

Accept when a buyer outside the core development team pays an independent
provider on a public TOS network and another resolver reconstructs the complete
history without a private gateway database.

Do not block this gate on general marketplace ranking, generalized arbitration,
multiple verticals, cross-chain support, or per-message settlement.

## 5. Gate E — Developer usability and protocol adapters

Deliver:

- provider SDK and deployment template;
- buyer SDK and wallet budget flow;
- minimal finalized-state Capability index and manifest retrieval;
- A2A task and result adapter;
- MCP tool adapter;
- optional x402 payment-negotiation adapter;
- gateway-local search with chain-derived fields kept separate; and
- examples that require no operator database edits or hidden control service.

Accept when a new provider publishes and sells the software-work Capability and
a new buyer purchases it using public documentation in one working session.

Adapters must map into the same Agent, Capability, Accepted Quote, Receipt, and
chain-reference objects. They cannot create parallel protocol facts.

## 6. Gate F — Open gateway and market evidence

Deliver:

- gateway discovery document;
- interoperable search and Quote Proposal exchange;
- canonical error and retry semantics;
- pre-acceptance routing and post-acceptance failover rules;
- public relay, resolver, Quote, and Receipt conformance tests;
- at least two independently operated gateways;
- at least three independently operated providers; and
- at least ten useful, purchasable Capabilities in the proven profile.

Accept when either gateway can disappear at every safe handoff point without
loss of identity, ownership, accepted terms, artifacts, Receipt, or settlement,
and buyers outside the core team demonstrate recurring paid use.

## 7. Gate G — Production readiness

Deliver:

- independent contract and protocol audits;
- production key custody, wallet recovery, and bounded spending policy;
- endpoint diversity and finality incident procedures;
- load, storage, denial-of-service, and fee-budget evidence;
- stable-value-asset accounting and operator compliance controls;
- monitoring for code, state, quorum, finality, and economic divergence;
- reproducible releases and signed deployment artifacts; and
- operator runbooks for degraded and emergency states.

Accept only after a multi-operator exercise completes discovery, Quote
acceptance, paid software execution, Receipt checking, settlement, gateway
failure, provider failure, endpoint disagreement, refund, and client recovery.

## 8. Expansion gate

Data APIs, model inference, GPU markets, provider composition, payment channels,
additional assets, and additional networks are eligible only after Gate F shows
recurring paid demand. Each expansion needs a measurable customer outcome and
must reuse the existing authority objects.

## 9. Work ordering rules

- Registry mutations require finalized typed-state authority first.
- The first commercial lifecycle precedes broad marketplace features.
- Execution follows Accepted Quote and required escrow finality.
- Settlement follows Receipt checking.
- Convenience projections follow typed-state decoding.
- Adapters follow one working direct protocol path.
- Open federation follows one conforming gateway and one real transaction path.
- Expansion follows recurring paid use.

## 10. Immediate work

1. Obtain an independent audit of the Registry contract and `nativecore`.
2. Add a Capability registration vector and second vector implementation.
3. Deploy the frozen Registry code to a public TOS testnet.
4. Implement wallet-native action signing and finalized lifecycle tests.
5. Freeze the software-work manifest and Accepted Quote commitment.
6. Implement stable-value-asset escrow, Receipt, release, and refund.
7. Complete one independently resolvable paid software-work transaction.
