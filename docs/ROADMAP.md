# ATOS Native Implementation Roadmap

This roadmap defines implementation order and acceptance gates. Product
priority is defined by `PRODUCT_STRATEGY.md`. Authority boundaries are defined
by `ARCHITECTURE.md`; Agent and Capability transitions are defined by
`NATIVE_REGISTRY_STATE_MACHINES.md`.

No later gate may weaken an earlier authority or security invariant.

## Status convention

- ✅ Complete: implemented and supported by repository evidence.
- 🟡 Partial: implementation or design exists, but the task or its acceptance
  evidence is incomplete.
- ⬜ Pending: not implemented, or no qualifying evidence was found.

A gate is complete only when every delivery item and its acceptance condition
are complete. Status was last reviewed on 2026-08-14 against `tos` commit
`d2ae6d92d`, `tos-protocol` commit `cfe6c4e`, `atos` commit `b6fad23`, and
`tos-ai` commit `003633c`, plus the uncommitted remediation described in the
Native Registry internal security review. Before Gate B or Gate C is accepted,
published evidence must bind the reviewed sources and deployment to exact
commit IDs and release hashes.

## 1. Gate A — Registry protocol freeze

Deliver:

- ✅ clean `atos.native.v1` schema;
- ✅ network domain, identifiers, action cells, policies, and state cells;
- ✅ deterministic Agent and Capability registration vectors, including
  independently reproduced identifiers, addresses, action hashes, and BOCs;
- ✅ stable typed errors and a frozen cross-implementation negative mutation
  corpus; and
- ✅ explicit repository ownership.

Accept when two independent implementations reproduce every frozen registry
digest and reject all negative mutations.

**Gate status: ✅ Complete.** `nativecore` and the independent
`internal/referencecodec` implementation reproduce the frozen Agent and
Capability vector and reject every frozen negative mutation without sharing
protocol encoding code.

## 2. Gate B — Registry implementation assurance

Deliver:

- ✅ deterministic Agent and Capability accounts;
- ✅ complete state machines;
- ✅ live policy authorization;
- ✅ atomic Capability transfer;
- ✅ direct typed-state resolution;
- ✅ internal contract and `nativecore` review and remediation;
- 🟡 independent contract and `nativecore` security review — the first review
  delivered nine findings; remediation is implemented and awaits independent
  retest against the new frozen artifact;
- ✅ adversarial encoder, resolver, relay, mutation-corpus, release-hash,
  source-cleanliness, and recovery-policy-binding lifecycle checks; and
- ⬜ independent full-lifecycle TVM emulator evidence covering every Agent and
  Capability transition.

Accept when the full lifecycle passes on a local chain, the exported code hash
matches frozen vectors, and independent review finds no unauthorized or partial
transition.

**Gate status: 🟡 In progress.** Implementation, frozen conformance, internal
review remediation, and reproducible contract release are complete. The gate
is not accepted until independent TVM lifecycle testing and security review
close without an unauthorized or partial transition finding.

## 3. Gate C — Public testnet authority

Deliver:

- ✅ reproducible contract build, frozen release BOC, code hash, release
  manifest, and two-build comparison;
- ✅ build/source separation that leaves generated `.fif` and embedded `.cpp`
  intermediates outside the source tree and verifies this invariant in CI;
- ⬜ public-testnet deployment record binding network domain, contract address,
  deployed code BOC, code hash, transaction, and exact source commit;
- 🟡 multi-endpoint quorum and finality configuration — client support exists,
  but no public testnet configuration has been accepted;
- ✅ wallet action signing and semantic confirmation, including exact action-hash
  confirmation and fee-payer destination, amount, body, and StateInit binding;
- 🟡 registry explorer and typed-state checker — direct typed-state RPC checking
  exists; a public explorer does not; and
- ⬜ recovery, transfer, and revocation drills on a public testnet.

Accept when an independently operated wallet registers, updates, transfers,
revokes, and resolves objects without trusting the reference gateway.

**Gate status: ⬜ Not accepted.** No qualifying public-testnet lifecycle has been
recorded.

## 4. Gate D — First commercial lifecycle

This gate is the highest product priority after Registry assurance. It covers
one machine-checkable software-work profile only.

Deliver:

- ⬜ immutable software-work Capability manifest profile;
- 🟡 deterministic Accepted Quote commitment, vector, and TOS transaction — the
  commitment implementation and local vector exist; the canonical transaction
  path does not;
- 🟡 exact endpoint and execution-signer binding — commitment fields exist, but
  the end-to-end commercial lifecycle is incomplete;
- ⬜ TOS-network stablecoin escrow with bounded native TOS network fees;
- 🟡 isolated compilation, deterministic test, static-analysis, dependency-scan,
  or reproducible-build execution;
- ⬜ canonical Receipt binding input, toolchain, result, artifacts, usage, and
  charged amount;
- ⬜ objective release and refund transitions;
- ⬜ narrowly defined dispute evidence where an automatic outcome is impossible;
- ⬜ content-addressed artifact delivery; and
- ⬜ independent Quote, escrow, Receipt, and settlement resolution.

Accept when a buyer outside the core development team pays an independent
provider on a public TOS network and another resolver reconstructs the complete
history without a private gateway database.

Do not block this gate on general marketplace ranking, generalized arbitration,
multiple verticals, cross-chain support, or per-message settlement.

**Gate status: ⬜ Not accepted.** Accepted Quote primitives and an isolated
executor foundation exist, but there is no stablecoin escrow, canonical Receipt,
settlement path, or independently resolvable paid transaction.

## 5. Gate E — Developer usability and protocol adapters

Deliver:

- ⬜ provider SDK and deployment template;
- ⬜ buyer SDK and wallet budget flow;
- ⬜ minimal finalized-state Capability index and manifest retrieval;
- ⬜ A2A task and result adapter;
- ⬜ MCP tool adapter;
- ⬜ optional x402 payment-negotiation adapter;
- ⬜ gateway-local search with chain-derived fields kept separate; and
- ⬜ examples that require no operator database edits or hidden control service.

Accept when a new provider publishes and sells the software-work Capability and
a new buyer purchases it using public documentation in one working session.

Adapters must map into the same Agent, Capability, Accepted Quote, Receipt, and
chain-reference objects. They cannot create parallel protocol facts.

**Gate status: ⬜ Not started.** The direct Native protocol path must be completed
before adapters and SDK acceptance work begins.

## 6. Gate F — Open gateway and market evidence

Deliver:

- ⬜ gateway discovery document;
- 🟡 interoperable search and Quote Proposal exchange — non-canonical Quote
  objects are defined, but federation is not implemented;
- 🟡 canonical error and retry semantics — protocol errors exist, but public
  conformance is incomplete;
- 🟡 pre-acceptance routing and post-acceptance failover rules — architecture
  rules exist without multi-gateway acceptance evidence;
- 🟡 public relay, resolver, Quote, and Receipt conformance tests — local relay
  and resolver tests exist; public Quote and Receipt conformance does not;
- ⬜ at least two independently operated gateways;
- ⬜ at least three independently operated providers; and
- ⬜ at least ten useful, purchasable Capabilities in the proven profile.

Accept when either gateway can disappear at every safe handoff point without
loss of identity, ownership, accepted terms, artifacts, Receipt, or settlement,
and buyers outside the core team demonstrate recurring paid use.

**Gate status: ⬜ Not accepted.** Multi-operator deployment and recurring paid-use
evidence do not exist.

## 7. Gate G — Production readiness

Deliver:

- ⬜ independent contract and protocol audits;
- ⬜ production key custody, wallet recovery, and bounded spending policy;
- ⬜ endpoint diversity and finality incident procedures;
- ⬜ load, storage, denial-of-service, and fee-budget evidence;
- ⬜ TOS-network stablecoin accounting and operator compliance controls;
- ⬜ monitoring for code, state, quorum, finality, and economic divergence;
- ⬜ reproducible releases and signed deployment artifacts; and
- ⬜ operator runbooks for degraded and emergency states.

Accept only after a multi-operator exercise completes discovery, Quote
acceptance, paid software execution, Receipt checking, settlement, gateway
failure, provider failure, endpoint disagreement, refund, and client recovery.

**Gate status: ⬜ Not started.** Production acceptance depends on Gates C through
F.

## 8. Expansion gate

Data APIs, model inference, GPU markets, provider composition, payment channels,
additional assets, and additional networks are eligible only after Gate F shows
recurring paid demand. Each expansion needs a measurable customer outcome and
must reuse the existing authority objects.

**Status: ⬜ Locked.** Gate F has not demonstrated recurring paid demand.

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

1. ⬜ Obtain an independent audit of the Registry contract and `nativecore`.
2. ✅ Add a Capability registration vector and second vector implementation.
3. ✅ Freeze and continuously reproduce the Registry BOC, code hash, release
   manifest, negative corpus, and clean source/build boundary.
4. ⬜ Deploy the frozen Registry code to a public TOS testnet and publish the
   complete deployment record.
5. ✅ Implement wallet-native action signing and exact semantic confirmation.
6. ⬜ Record the complete finalized Agent and Capability lifecycle on the public
   testnet using an independently operated wallet and resolver.
7. 🟡 Freeze the software-work manifest and Accepted Quote commitment — the
   deterministic commitment implementation and local test exist; the immutable
   software-work profile, frozen vector, and canonical TOS transaction do not.
8. ⬜ Implement TOS-network stablecoin escrow, Receipt, release, and refund.
9. ⬜ Complete one independently resolvable paid software-work transaction.
