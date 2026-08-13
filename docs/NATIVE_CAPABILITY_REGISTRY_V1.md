# Native Capability Registry V1

This document defines Capability-specific registry constraints. The complete
transition rules are normative in
`PHASE5_NATIVE_REGISTRY_SIMPLIFICATION.md`.

## Registration tuple

Capability registration binds:

```text
network domain
object nonce
owner Agent ID
initial version string
initial manifest SHA-256 digest
registry contract code hash
```

The deterministic Capability ID and account are reconstructed from this tuple.
Registration is routed through the owner Agent, which must exist, be live, and
authorize the action using current finalized policy.

## Canonical state

The Capability account stores:

```text
object kind and ID
network configuration
generation and sequence
last action hash
owner Agent ID
bounded immutable version dictionary
tombstone flag
```

Each version dictionary value stores the original bounded version name,
manifest digest, and revocation bit. Storing the name permits complete typed
resolution without consulting an off-chain dictionary.

## Authorization routing

Capability operations are submitted to the current owner Agent account. The
Agent validates live authorization before forwarding identical action and
signature cells to the Capability. The Capability authenticates the forwarding
Agent using its deterministic address.

Transfer additionally passes through the new owner Agent for acceptance. Only
the Capability account mutates.

## Indexing

An indexer publishes only finalized Capability states. Records are keyed by
network domain and Capability ID and include the exact finalized checkpoint and
chain reference. Reorg handling removes or replaces all records above the new
common finalized checkpoint as one atomic index generation.

An indexer must not synthesize ownership from events when direct typed state is
available. Events may accelerate ingestion but state is the verification
target.

## Stable failures

Implementations distinguish malformed action, invalid signature, threshold
failure, wrong network, wrong contract, wrong sender, stale predecessor,
invalid sequence, immutable version conflict, revoked version, tombstoned
object, missing owner, and insufficient finality.

## Bounds

Controller counts, signatures, delegation counts, version counts, text lengths,
cell depth, references, response bytes, endpoint counts, and relay funding are
bounded before expensive work. Bounds must agree across schema validation, Go
construction, TVM execution, indexer decoding, and conformance tests.
