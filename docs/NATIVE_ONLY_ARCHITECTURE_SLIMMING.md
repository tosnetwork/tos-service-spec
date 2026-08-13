# ATOS Native-Only Architecture Slimming Proposal

**Revision:** 2026-08-13
**Status:** Target architecture
**Scope:** ATOS protocol, Native Resolution, and Open Gateway Federation

## 0. Normative Design Rule

The simplified architecture follows one rule:

> If a fact determines identity, authority, ownership, purchased terms,
> payment, settlement, or proof validity, its canonical value is finalized TOS
> state. A gateway may cache or present that fact but cannot create it.

"On-chain is authoritative" does not mean storing private prompts, model
outputs, bulk artifacts, search indexes, rankings, or transient transport state
on-chain. Those remain off-chain and are bound to canonical transactions only
by the minimum hashes, signatures, and references required for verification.

## 1. Decision Summary

ATOS should converge its protocol on one decentralized operating model:

```text
atos_native_v1
```

Phase 5 Native Resolution and Phase 6 Open Gateway Federation are not two
competing modes. They are two layers of the same system:

- Phase 5 defines canonical facts: identity, ownership, Capability versions,
  authorization, and deterministic resolution from TOS.
- Phase 6 defines open access: independent gateways, discovery, routing,
  invocation, verification, and gateway failover.

`atos.im` remains a reference gateway and may provide hosted convenience, but
it is not the canonical namespace, registry, ownership, or settlement
authority.

The long-term protocol should therefore remove `managed` and `verified` as
parallel transaction modes. The cryptographic and economic work built for
Verified remains necessary, but becomes mandatory infrastructure inside the
Native protocol rather than a separate product choice.

## 2. Problem with the Current Model

The current architecture exposes three concrete transaction modes:

```text
managed | verified | native
```

This creates three partially overlapping authority models:

| Mode | Namespace/identity authority | Economic/proof authority | Gateway authority |
|---|---|---|---|
| Managed | `atos.im` database | `atos.im` | `atos.im` |
| Verified | primarily `atos.im` | TOS-backed checkpoints | `atos.im` |
| Native | TOS Native Registry | TOS | any compatible gateway |

The implementation must consequently maintain mode selection, activation,
pricing, downgrade prevention, proof profiles, per-mode readiness, settlement
branches, and different interpretations of the same Capability identity.

This complexity is not only cosmetic. It makes it difficult to answer the
most important protocol question: which system is authoritative?

## 3. Native-Only Model

```text
                         TOS Network
        Agent identity / Capability ownership / versions
        signer authority / escrow / settlement / commitments
                              |
          +-------------------+-------------------+
          |                   |                   |
       atos.im             Gateway B        Local Gateway
          |                   |                   |
          +-------------------+-------------------+
                              |
                       Provider / Worker
```

The responsibilities are:

### TOS trust and economic plane

- canonical Agent and Capability identity;
- ownership and controller-policy state;
- immutable Capability-version commitments;
- execution-signer authorization;
- escrow and settlement state;
- receipt and proof commitments; and
- finalized history needed for independent resolution.

### Gateways

- indexing and caching canonical facts;
- search, ranking, personalization, and anti-spam;
- Quote construction and policy checks;
- transport routing and invocation orchestration;
- wallet abstraction and optional fee sponsorship;
- artifact transport and temporary private storage;
- proof presentation; and
- user-facing dispute workflows.

Gateways may differ in quality, policy, availability, and pricing, but cannot
create or overwrite canonical Native facts.

### Providers and workers

- execute the purchased Capability;
- protect private inputs and bulk artifacts;
- produce signed execution receipts; and
- interact through one or more compatible gateways or direct bindings.

## 4. Remove Trust Mode as a Product Axis

The following protocol fields should be deprecated and ultimately removed:

```text
requested_trust_mode
trust_mode
requested_trust_modes
supported_trust_modes
mode_support[managed|verified|native]
```

The protocol instead has one invariant version:

```text
protocol = atos_native_v1
```

The verifier may use `tos_native_v1` as an internal proof-schema identifier,
but clients do not negotiate or select it and it is not repeated in every
Accepted Quote. The `atos_native_v1` protocol version determines the required
proof schema. A future incompatible profile requires a protocol version change.

Callers may still express policies, but these should describe concrete
requirements rather than select a weaker authority model. Examples include:

- maximum price;
- maximum finality delay;
- required proof type;
- gateway diversity;
- artifact-retention policy;
- accepted settlement asset;
- required dispute policy; and
- privacy or locality constraints.

There is no silent downgrade rule because there is no weaker protocol mode to
downgrade into. If Native prerequisites are unavailable, the operation fails
closed or the client obtains a new Quote with different non-trust terms.

## 5. Preserve Verified Infrastructure

Removing `trust_mode=verified` does not mean deleting the Phase 4 security and
economic components. Native depends on them.

The following remain and become part of the Native baseline:

- TOS TaskEscrow contracts and economic driver;
- accepted on-chain Quote commitments;
- execution-signer authorization;
- signed execution receipts;
- settlement and refund proofs;
- independent proof verification;
- finality and multi-reader checks;
- publisher/key-custody isolation;
- reconciliation and disaster recovery; and
- dispute and resolution transitions.

The architectural change is:

```text
Before: Verified is an optional mode below Native.
After:  Verified guarantees are mandatory internal layers of Native.
```

## 6. atos.im After the Change

`atos.im` remains valuable as the default reference implementation. It may
provide:

- account login, API tokens, and passkeys;
- hosted or delegated wallet custody;
- gas sponsorship;
- high-quality search and ranking;
- provider onboarding and endpoint certification;
- moderation and abuse controls;
- MCP, REST, A2A, and streaming interfaces;
- artifact relay and encrypted temporary storage;
- fiat payment adapters;
- notifications, support, and dispute UI; and
- performance caches and operational monitoring.

These are convenience and product services. They must not become canonical
protocol facts.

For example, `atos.im` may refuse to index a Capability, but another gateway
must still be able to resolve it from TOS. A hosted account may sponsor gas,
but the resulting Native action must remain independently verifiable. Internal
credits may fund a gateway-sponsored transaction, but those credits must not
be represented as finalized Native settlement until the required TOS state
exists.

## 7. Simplified Public Objects

A Capability no longer advertises three modes. A representative public shape
is:

```json
{
  "capability_id": "cap_...",
  "owner_agent_id": "agent_...",
  "version": "1.0.0",
  "manifest_commitment": "sha256:...",
  "bindings": [],
  "price": {
    "asset": "TOS",
    "atomic": "5000000000"
  }
}
```

A gateway may prepare a Quote Proposal, but it is not a canonical purchase
until the buyer accepts it as a TOS-backed Quote Commitment. The Accepted Quote
binds the Native transaction contract directly:

```json
{
  "protocol": "atos_native_v1",
  "capability_id": "cap_...",
  "provider_agent_id": "agent_...",
  "transport_binding": "sha256:...",
  "manifest_digest": "sha256:...",
  "escrow_terms": {},
  "execution_signer": {},
  "expires_at": "..."
}
```

The transport binding identifies the selected route without making the
gateway authoritative. Price, version, signer authority, escrow, expiry, and
dispute terms become canonical only in the Accepted Quote. An
unsigned gateway-database Quote is discovery output, not a protocol fact.

## 8. Relationship to Phase 5 Registry Simplification

Native-only operation is practical only if the Phase 5 Registry itself is
made smaller and safer. The companion proposal requires:

- typed TVM state as the sole authoritative on-chain state;
- portable CBOR as a deterministic off-chain projection;
- removal of the per-action Anchor from ordinary transitions;
- atomic dual-authorization Capability transfer;
- contract-derived next state; and
- one complete policy validator used by every installation path.

Without this simplification, removing Managed and Verified product modes would
still leave an unnecessarily complex Native core.

## 9. Minimal Native v1 Product Surface

The first Native-only release should implement only five canonical objects or
records:

1. **Agent** — identity and validated controller policy.
2. **Capability** — owner, immutable versions, and revocation.
3. **Accepted Quote** — on-chain purchase terms and selected immutable version.
4. **Escrow** — reserved funds and deterministic terminal economic state.
5. **Receipt** — result/evidence commitment signed by authorized execution
   authority.

The first release must not place the following in consensus:

- search ranking or recommendations;
- gateway reputation scores;
- raw prompts, outputs, or artifacts;
- provider availability and latency;
- fiat balances or gateway credits;
- mutable marketing metadata;
- generalized on-chain messaging; or
- multiple selectable trust/proof modes.

Those remain gateway or later-version concerns. Dispute logic should initially
use the already reviewed bounded TaskEscrow state machine rather than adding a
new general arbitration protocol.

## 10. Costs and Tradeoffs

The Native-only direction is strategically cleaner but has real costs:

- Managed is currently the most complete path, while Native Resolution and
  federation are still incomplete.
- Product availability may temporarily regress if the hosted compatibility
  path is removed before Native is operational.
- Every canonical mutation must handle chain fees, finality, replay, and
  failure recovery.
- Walletless UX requires custody, delegation, account abstraction, or gas
  sponsorship without weakening protocol guarantees.
- Search remains vulnerable to spam and quality manipulation even when
  identity is decentralized.
- Fiat and internal-credit entry points remain centralized adapters.
- Independent gateways require a conformance suite and operational guidance,
  not merely an open API description.

These tradeoffs should be addressed explicitly rather than hidden behind
multiple trust-mode labels.

## 11. Compatibility Policy

Existing Managed and Verified implementations must not define the new
protocol. During migration they may remain available only behind a separate
hosted compatibility API and explicit label, for example:

```text
atos.im hosted beta
```

Such operations must not claim `atos_native_v1` guarantees. New protocol work
should not add more mode-dependent branches to preserve the compatibility
path.

Legacy and Native records must use distinct version domains, storage paths,
and public status. Legacy APIs may prepare Native operations only when every
Native precondition is satisfied and the result is committed on-chain.
Otherwise they must return a clear compatibility or availability error. A
hosted database mutation can never be promoted into canonical Native state by
labelling it differently.

## 12. Completion Criterion

The Native-only architecture is proven when the following scenario succeeds:

1. A provider registers an Agent and Capability through Gateway A.
2. An independent indexer reconstructs them from finalized TOS state.
3. Gateway B resolves the same canonical identities and manifest version.
4. A client obtains a Quote Proposal through Gateway B and commits a canonical
   Accepted Quote on-chain.
5. Escrow, signer authorization, receipt, and settlement are independently
   verified.
6. Gateway A and `atos.im` are unavailable throughout resolution and
   verification.
7. A third implementation reaches the same canonical result from chain data.

If the system cannot complete this flow, it is not yet an open Native Agent
Internet regardless of how many fields are named `native`.

## 13. Recommendation

Adopt Native-only as the target protocol architecture:

- one canonical TOS-backed identity and economic model;
- one Native proof profile;
- many replaceable gateways;
- `atos.im` as a reference and convenience service, not an authority; and
- temporary hosted compatibility isolated from the protocol core.

This decision removes an entire product dimension while preserving the work
that provides real cryptographic, economic, and federation guarantees.
