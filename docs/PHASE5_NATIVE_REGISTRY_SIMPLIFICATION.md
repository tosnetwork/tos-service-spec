# Phase 5 Native Registry Simplification

**Date:** 2026-08-13
**Status:** Target contract architecture
**Scope:** Phase 5 Native Agent and Capability Registry

## Executive Summary

Phase 5 is difficult to implement and audit because it has evolved from a portable protocol into a distributed on-chain state machine without redefining a single source of authority. The current design combines two state representations, multiple contracts, asynchronous approval flows, purpose-scoped weighted authorization, recovery, immutable revocation, and independent off-chain reconstruction.

Each requirement is understandable in isolation. Their composition, however, creates unnecessary consensus and liveness risks. The present implementation must continuously prove that several independently implemented views of the same transition agree:

```text
portable CBOR action
= typed TVM action
= portable next state
= typed TVM next state
= Go resolver reconstruction
= FunC contract execution
```

The simplified design establishes one authoritative on-chain state representation, executes each logical operation atomically in the object contract, and derives portable representations off-chain. In particular:

1. Make typed TVM state the sole on-chain authority.
2. Treat portable CBOR as a deterministic derived representation, not a second consensus state.
3. Remove the per-action Action Anchor from normal state transitions.
4. Submit both owner approvals in one atomic Capability transfer.
5. Let the contract derive the next state from the signed action and current state.
6. Keep relayers as untrusted transport and fee-payer components only.
7. Centralize and reuse complete policy validation for every policy installation path.

This changes Phase 5 from a cross-contract distributed transaction protocol into a multi-key on-chain registry with deterministic off-chain projection.

## Why the Current Design Became Complex

The complexity is primarily the result of incremental compatibility decisions:

```text
Phase 5A defines a portable CBOR protocol
                    |
Phase 5B adds native TVM execution
                    |
Portable state is retained for compatibility
                    |
Typed Cell state is added for contract execution
                    |
Signature commitments are added for untrusted relayers
                    |
Action Anchors are added for deterministic location and idempotency
                    |
Agents and Capabilities are split into independent contracts
                    |
Capability transfer becomes an asynchronous multi-contract approval flow
                    |
Recovery, timelocks, and irreversible tombstones add more intermediate states
```

The resulting system is not equivalent to a conventional DeFi contract. It combines identity management, weighted and purpose-scoped authorization, recovery, object ownership, asynchronous messaging, history verification, and two representations of consensus state.

## Necessary Versus Accidental Complexity

Some complexity follows directly from the product requirements and should remain:

- multiple controller keys with weights and thresholds;
- purpose separation such as control, delegation, and recovery;
- replay protection and ordered state transitions;
- approval by both parties for ownership transfer;
- delayed recovery for lost or compromised keys;
- irreversible revocation where explicitly required;
- untrusted relayers; and
- independently verifiable historical transitions.

Other complexity is architectural rather than necessary:

- treating typed Cell state and portable CBOR state as co-authoritative;
- deploying one persistent Action Anchor contract per action;
- persisting an unverified signature envelope before authorization succeeds;
- implementing ownership transfer as an abortless two-phase commit;
- signing both an action and several results that the contract could derive;
- duplicating the same transition rules across FunC, builders, decoders, resolvers, and publishers; and
- relying on SDK validation while also permitting unrestricted raw message submission.

The simplification should preserve the first group while eliminating as much of the second group as possible.

## Authority Model

### One Consensus State

Typed TVM Cell state should be the only authoritative state stored and validated by the contract.

Portable CBOR is a deterministic projection produced by indexers, resolvers, or clients:

```text
authoritative typed state
          |
          +-- deterministic portable CBOR projection
          +-- API representation
          +-- historical proof representation
```

The portable representation may retain a digest for caching, interchange, and historical evidence, but that digest is computed after resolution and is not stored as a second state commitment in the simplified Native Registry. A mismatch in an off-chain projection is an indexer or codec error and cannot corrupt or invalidate the canonical on-chain object.

Simplified Native Registry actions must not contain a caller-supplied portable next state. If an external system needs a portable action, it is generated from the canonical signed action schema; portable state is generated only from finalized typed state. Cross-chain adapters may verify these projections but cannot submit them as consensus inputs.

### One Atomic Transition Boundary

Each logical operation should either complete entirely in the authoritative object contract or leave no persistent partial state.

The normal transition should be:

```text
canonical signed action
        |
        v
Agent or Capability contract
  1. authenticates the message
  2. validates signatures and purposes
  3. checks sequence and predecessor
  4. derives the next state
  5. commits the transition atomically
        |
        v
event/history observed by resolver
```

No other contract should permanently reserve the Action ID before authorization succeeds.

## Remove the Action Anchor from Normal Operations

The current Action Anchor combines too many responsibilities:

- deterministic action location;
- idempotency and replay protection;
- submission journaling;
- signature-envelope storage;
- message routing;
- completion receipts; and
- funding.

These responsibilities conflict. In particular, journal-before-validation allows an invalid envelope to reserve an otherwise valid Action ID.

For normal operations, replay protection can live directly in the target object through:

- sequence number;
- generation number;
- predecessor state hash; and
- an optional bounded record of completed Action IDs where required.

The transaction and emitted event already provide a durable historical reference. A separate persistent contract is not required solely to prove that an action occurred.

The simplified Native Registry does not deploy a per-action Anchor. The target object's finalized transaction and emitted transition record are the action receipt. Legacy Anchor contracts may remain readable under their original version, but no new Native operation depends on or creates one.

## Make Capability Transfer Atomic

Capability transfer should carry both authorization sets in one message:

```text
TransferCapability {
    capability_id
    current_owner_agent_id
    new_owner_agent_id
    expected_current_owner_policy
    expected_new_owner_policy
    sequence
    predecessor_state_hash
    current_owner_signatures
    new_owner_signatures
}
```

The Capability contract should validate both policies and both signature sets before changing any state. The operation then has only two outcomes:

- both approvals are valid and ownership changes; or
- any check fails and the Capability remains unchanged.

There should be no persistent half-transfer state and therefore no requirement for timeout, cancellation, or recovery from a missing second approval.

If reading both Agent policies synchronously is impossible in TVM, the signed transfer should contain policy proofs or snapshots bound to the action, and the Capability should validate the required authenticated evidence before committing. The protocol must still avoid committing the first half of the transfer while waiting for the second.

## Simplify the Signature Commitment

An untrusted relayer does not need authority to derive or alter state. Its role should be limited to transporting an already signed action and paying fees.

Controllers should sign a canonical action containing the complete intended mutation and its replay domain:

- network and genesis domain;
- target object identity;
- target contract/code domain where upgrade rules require it;
- action kind and payload;
- generation and sequence;
- predecessor state hash;
- nonce or expiry where appropriate; and
- policy version or digest used for authorization.

The contract should derive the next typed state from the signed action and its current state. Controllers should not need to sign multiple independently supplied next-state representations or values that are deterministic consequences of the action.

Every retained commitment field should have a documented threat that cannot already be addressed by another signed field.

## Consolidate Policy Validation

Every policy installation path must execute the same complete validation routine:

- initial Agent registration;
- normal policy update;
- recovery initiation;
- recovery completion; and
- any future migration or upgrade path.

The validation routine should enforce:

- canonical key ordering;
- unique key IDs and public keys;
- valid Ed25519 key encoding;
- nonzero, bounded weights;
- attainable normal and recovery thresholds;
- allowed purpose masks;
- bounded controller count;
- canonical Cell shape with no trailing data; and
- required recovery properties where recovery is enabled.

SDK validation remains useful for user feedback, but the contract must be safe when a caller submits a raw TVM message without using the official SDK.

## Reduce Duplicate Implementations

The current business rules are distributed across FunC, the Go builder, Go decoder, resolver, publisher, portable protocol, and test-vector code. The redesign should assign a narrow responsibility to each component:

| Component | Responsibility |
|---|---|
| FunC contract | Authoritative authorization and state transition |
| Go action builder | Construct canonical action and signatures |
| Go resolver | Decode authoritative chain state and derive portable output |
| Publisher/relayer | Transport bytes and pay fees without semantic authority |
| Portable codec | Deterministic external representation only |
| Test vectors | Cross-language action and state projection conformance |

Where practical, schemas and constants should be generated from one frozen specification rather than independently copied.

## Suggested Minimal State Machines

### Agent

An Agent needs only:

- immutable Agent ID and network domain;
- generation and sequence;
- current validated controller policy;
- delegation records or their authenticated root;
- optional pending recovery with activation time;
- tombstone flag; and
- last transition reference/hash.

Policy update and delegation are atomic Agent operations. Recovery may retain one intentional pending state because the timelock is a product requirement, but that state must be replaceable or cancellable according to a clearly defined authorization rule.

### Capability

A Capability needs only:

- immutable Capability ID and network domain;
- generation and sequence;
- current owner Agent ID;
- immutable version records or their authenticated root;
- revocation/tombstone state; and
- last transition reference/hash.

Registration, version addition, ownership transfer, and revocation should each be atomic. Capability state should never contain one side of a transfer approval.

## Migration Plan

### Stage 1: Freeze the Authority Decision

Before further implementation, record a normative architecture decision:

> Typed TVM state is the sole authoritative on-chain Native Registry state. Portable CBOR is a deterministic projection and interchange format, not an independent consensus state.

Update the specification and test vocabulary to reflect that decision.

### Stage 2: Define the Minimal Canonical Action

Specify exactly which fields controllers sign and remove independently supplied results that the contract can derive. Produce cross-language vectors for:

- action encoding;
- action digest;
- signature commitment;
- typed next state; and
- portable projection from typed state.

### Stage 3: Implement Direct Atomic Object Operations

Add direct Agent and Capability handlers that perform validation and state updates in one transaction. Implement atomic dual-signature Capability transfer.

### Stage 4: Remove Anchor Dependency

Change the publisher and resolver to use the target object transaction and event as the action receipt. Legacy Anchors are handled only by an explicitly versioned read-only legacy resolver.

### Stage 5: Derive Portable State

Modify the resolver to derive portable CBOR exclusively from the accepted typed state. Compare the result against test vectors, not against a second caller-supplied state embedded in the action.

### Stage 6: Security and Migration Testing

Add regression tests covering:

- front-running with a modified signature envelope;
- duplicate and reordered signatures;
- replayed sequence and predecessor values;
- policy rotation between signing and submission;
- atomic transfer with either owner invalid;
- tombstoned proposed owner;
- malformed policy installation through every path;
- direct raw messages that bypass the SDK;
- relayer mutation of every signed field; and
- deterministic portable projection across independent implementations.

Existing objects should either remain under an explicitly versioned legacy resolver or migrate through a one-time, fully authorized transition. The new contract version and locator rules must prevent legacy and simplified state formats from being confused.

## Expected Benefits

The simplified architecture provides:

- one clearly defined consensus authority;
- fewer cross-contract failure modes;
- no persistent half-transfer state;
- no pre-validation Action ID reservation;
- fewer independently signed and compared hashes;
- smaller FunC and Go attack surfaces;
- simpler funding estimates;
- easier localnet and property testing;
- clearer upgrade and compatibility boundaries; and
- more reliable independent resolution of historical state.

## Architecture Decision

The architecture decision is final for the simplified design: typed TVM state is authoritative and portable CBOR is derived off-chain. Co-authoritative representations are outside the scope of this roadmap.
