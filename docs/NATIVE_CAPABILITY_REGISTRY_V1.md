# Native Capability Registry V1

Status: **normative Phase 5A contract**

## 1. Scope

This document freezes the common action/event envelope and Capability lineage
semantics consumed by Phase 5B. It does not implement registry mutation,
indexing, wallet sessions or Native economics.

## 2. Registry action

Domain: `tos.native.registry-action.v1`.

The canonical V1 value contains every field, including empty inapplicable
fields:

```text
version                    "tos_native_registry_v1"
kind                       frozen action enum
network                    NetworkDomain
agent_id                   canonical controlling Agent
capability_id              canonical Capability ID or empty for Agent action
capability_version         exact SemVer when the action targets a version
generation                 uint64, nonzero
sequence                   uint64, nonzero within generation
previous_event_digest      empty for sequence 1, required otherwise
policy_digest              controller/ownership policy digest
payload_digest             digest of the kind-specific canonical payload
nonce_base64url            canonical 32-byte raw base64url
```

Kinds are `register_agent`, `update_agent_policy`, `delegate_agent`,
`recover_agent`, `revoke_agent`, `register_capability`, `update_capability`,
`transfer_capability` and `revoke_capability`. Unknown kinds fail closed.

The nonce is stable across exact retries. Reusing the same semantic operation
identity with changed fields is an idempotency conflict. Sequence and previous
event establish an append-only chain; local insertion order is irrelevant.

## 3. Capability payload semantics

The kind-specific payload schemas frozen before Phase 5B implementation bind:

- immutable Capability ID and exact version;
- current owner Agent and ownership generation;
- immutable manifest digest and content-addressed retrieval reference;
- bounded endpoint references and provider-authorized recipient/encryption key;
- purpose-separated Quote and Receipt signer references;
- validity interval and predecessor;
- transfer target/acceptance for ownership transfer;
- revocation or version-supersession reason.

Private inputs, outputs, proposals and bulk manifest bytes remain off-chain.
Retrieval references are locations, never authority; fetched bytes must match
the committed content digest.

Transfer changes the owner, not the Capability ID or immutable historical
versions. An update cannot mutate an old version. Revocation is permanent for
the targeted lineage/version according to its payload and event order.

## 4. Registry event

Domain: `tos.native.registry-event.v1`.

```text
version, kind, network
action_digest
agent_id, capability_id, capability_version
generation, sequence, previous_event_digest
finalized_checkpoint, transaction_index, event_index
```

The event repeats the action identity and ordering tuple so an indexer can
validate rather than trust transport metadata. `finalized_checkpoint` is
nonzero. The event digest is recomputed from canonical CBOR. Block timestamp,
RPC URL, gateway ID and local database cursor are not semantic event fields.

## 5. Indexer contract boundary

Phase 5C will freeze ingestion, cursor and rebuild APIs. Phase 5A freezes these
minimum invariants now:

- order by canonical finalized position, never arrival time;
- reject gaps, predecessor mismatch, cross-network objects and duplicate
  logical positions with different digests;
- exact replay is harmless;
- retain enough finalized history to evaluate authority at a historical
  transaction/Receipt boundary;
- rollback above a reorg boundary and deterministically replay;
- never present search ranking or manifest availability as ownership authority.

## 6. Stable errors and vectors

Implementations expose stable classifications including
`NATIVE_SEQUENCE_CONFLICT`, `NATIVE_PREDECESSOR_MISMATCH`,
`NATIVE_POLICY_UNAUTHORIZED`, `NATIVE_PURPOSE_UNAUTHORIZED`,
`NATIVE_PERMANENTLY_REVOKED`, `NATIVE_STALE_AUTHORITY`,
`NATIVE_FINALITY_UNAVAILABLE` and the identifier/canonicalization errors from
`NATIVE_IDENTIFIERS_V1.md`.

The shared normative vectors are `test-vectors/native_registry_v1.json`.
