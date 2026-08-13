# ATOS Native Architecture

**Normative authority:** product and system architecture

**Protocol:** `atos_native_v1`

## 1. Product definition

ATOS is an open protocol for locating and transacting with agents over TOS.
Users may choose any conforming gateway or interact with TOS directly. The
protocol has one authority model and one canonical state path.

The product consists of:

- deterministic on-chain Agent and Capability identities;
- immutable Capability version commitments;
- independently reproducible discovery projections;
- gateway-generated Quote Proposals;
- finalized Accepted Quote commitments;
- provider execution bound to an authorized signer and endpoint;
- escrow, receipt, dispute, and settlement commitments; and
- open gateway interoperability.

This list describes the target architecture, not the scope of the first
release. Initial delivery is limited to the Native Registry plus one
machine-checkable software-work lifecycle: resolve, Quote, escrow, execute,
Receipt, release or refund, and independent history resolution. Other markets,
generalized arbitration, and broader federation follow only after recurring
paid use.

## 2. Canonical authority

Finalized TOS state is the sole canonical authority for:

- Agent controller policy, delegations, recovery, and revocation;
- Capability ownership, immutable versions, and revocation;
- Accepted Quote terms and selected execution authority;
- escrow and settlement state;
- receipt and dispute commitments; and
- protocol version and network domain.

No service database, search index, cache, proposal, log, or portable encoding
can create a protocol fact. Such data is useful only when it can be checked
against finalized TOS state.

## 3. Architectural planes

### TOS authority plane

TOS contracts validate signatures and state transitions. Each Native Registry
object has a deterministic account containing typed TVM state. Commerce
contracts hold Accepted Quote, escrow, receipt, dispute, and settlement facts.

### Protocol plane

`tos-protocol` implements canonical cell construction, identifier derivation,
signature verification, transaction relaying, quorum reads, finalized-state
resolution, and deterministic projections. It does not replace contract
validation.

### Gateway plane

A gateway provides authentication, rate limiting, discovery, proposal
construction, routing, transaction transport, and user experience. Multiple
gateways may independently serve the same canonical state.

### Execution plane

Providers and workers execute the version and input bound by an Accepted Quote.
They return content-addressed artifacts and signed receipt commitments. Bulk
bytes remain outside consensus.

## 4. Legal information flow

```text
TOS finalized state
  -> independent resolver/indexer
  -> gateway discovery and derived views
  -> client-side verification

client canonical action + signatures
  -> arbitrary relayer
  -> TOS contract validation
  -> finalized typed state

gateway Quote Proposal
  -> client validation and acceptance
  -> TOS commitment transaction
  -> finalized Accepted Quote
  -> bound execution and settlement
```

The arrows never reverse authority. A cache cannot update TOS, a proposal
cannot authorize execution, and a relay response cannot prove finality.

## 5. Registry representation

Typed TVM state is the sole Native Registry representation used by consensus.
The off-chain protocol may derive deterministic CBOR or JSON for interchange,
but derivation always starts from authenticated typed TVM state. A projection is
never supplied to the contract as an intended next state and is never hashed
into transition authorization as an alternate state representation.

The registry deploys one deterministic account per Agent or Capability. It
does not deploy an auxiliary contract for each action.

## 6. Gateway neutrality

A conforming gateway must be replaceable without changing identity or
commercial semantics. Therefore:

- controller keys are not held by gateways;
- object IDs do not include a gateway identity;
- Capability versions do not depend on a gateway database;
- proposal IDs are local convenience identifiers;
- Accepted Quote commitments exclude proposal-local identity;
- signed actions are valid through any conforming relayer;
- resolution is reproducible without the submitting gateway; and
- gateway policy cannot weaken contract authorization.

Gateway authentication protects transport resources. It does not authorize an
on-chain state transition; contract signatures do that.

## 7. Interoperability boundary

ATOS does not define a new general Agent messaging protocol. A2A or MCP may
carry task, progress, tool, and result messages. x402 or AP2 adapters may bridge
payment negotiation or delegated purchase intent. These adapters map into ATOS
objects and never become an alternate authority path.

The Accepted Quote remains the canonical ATOS commercial boundary regardless
of transport. An adapter cannot replace its Capability version, endpoint,
signer, asset, amount, escrow, expiry, or dispute commitment.

## 8. Discovery

Discovery indexes finalized Agent and Capability state plus manifest
content addressed by immutable digest. Indexes may add ranking, availability,
latency, price estimates, and local policy annotations. Those additions are
non-canonical and must be distinguishable from chain-derived fields.

Clients must be able to verify:

- the network and finalized checkpoint;
- the deterministic object ID and account address;
- the contract code and state hashes;
- Capability ownership and version commitment; and
- the manifest bytes matching the selected digest.

Initial discovery needs only enough search and manifest retrieval to complete
the software-work commercial lifecycle. General ranking, reputation, and broad
marketplace features are deferred until real provider and buyer activity exists.

## 9. Commerce

A Quote Proposal is discovery output. It may describe a Capability version,
provider, manifest, endpoint binding, maximum price, expiry, escrow terms,
dispute policy, and execution signer. It has no authority before acceptance.

Acceptance creates a deterministic commitment and submits it to TOS. Only the
finalized TOS commitment is an Accepted Quote. Execution, escrow, receipt, and
settlement must reference that commitment and may not substitute its bound
version, endpoint, signer, price, asset, or policy.

The initial commerce profile covers machine-checkable software work and narrow
objective release or refund rules. Native TOS pays network execution and
protocol security costs. A supported stablecoin issued on TOS Network may
denominate and settle the provider service through TOS contracts. The Accepted
Quote fixes both economic roles explicitly.

## 10. Data placement

Place only stable commitments and transition state on-chain. Keep prompts,
inputs, outputs, logs, model traces, and large evidence off-chain. Bind off-chain
content using immutable digests and disclose it only to authorized parties.

Evidence bundles may aggregate finalized chain references, manifests,
artifacts, and receipts. They are derived containers, not an additional
authority layer.

## 11. Failure model

Clients and gateways fail closed when:

- the TOS network domain differs;
- endpoints disagree below quorum;
- finality cannot be established;
- the registry code hash is unknown;
- deterministic address reconstruction fails;
- typed state is malformed;
- an action predecessor or sequence is stale;
- signatures or thresholds fail;
- an object or selected version is revoked; or
- Quote-bound execution terms cannot be reproduced.

Availability failure never permits semantic fallback.

## 12. Completion criterion

The architecture is complete when two independently operated gateways can
discover the same finalized Capability, produce interoperable proposals, relay
the same client-signed action, verify the same Accepted Quote, route execution,
verify its receipt, and complete settlement without sharing a private database
or trusted control service. The first product gate applies this criterion to a
software-work Capability with a real TOS-network stablecoin payment and providers
and buyers outside the core development team.
