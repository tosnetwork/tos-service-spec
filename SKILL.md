---
name: atos-native
description: Build clients and gateways for the atos_native_v1 protocol using finalized TOS state as the canonical authority.
---

# ATOS Native Protocol

Use this skill when implementing an ATOS client, wallet, gateway, registry
indexer, relayer, resolver, or conformance test.

## Core rule

Treat finalized TOS state as the only source of protocol truth. Never infer a
successful registry mutation from an HTTP response, relay acknowledgement,
gateway database row, mempool observation, or unfinalized transaction.

## Required reading

Read, in order:

1. `docs/PRODUCT_STRATEGY.md`
2. `docs/ARCHITECTURE.md`
3. `docs/NATIVE_REGISTRY_STATE_MACHINES.md`
4. `docs/ROADMAP.md`

Then read the focused document for the feature being changed and the complete
`proto/atos/native/v1/native.proto` schema.

For product work, complete the machine-checkable software-work lifecycle before
adding another market, transport, asset, or generalized policy system.

## Client flow

1. Pin a `NetworkDomain` containing network ID and both genesis digests.
2. Resolve Agent and Capability state from finalized TOS through a quorum of
   independently operated endpoints.
3. Verify the deterministic address, contract code hash, typed state, state
   hash, and chain reference.
4. Build the canonical action locally.
5. Show the exact action semantics to the signer.
6. Collect the required weighted Ed25519 signatures.
7. Submit through any relayer.
8. Treat `relay_accepted` only as transport acknowledgement.
9. Resolve again until finalized state contains the expected action hash or a
   terminal conflicting state is observed.

## Quote flow

This flow becomes canonical only after the Gate D TOS contracts and conformance
tests in `docs/ROADMAP.md` are complete. Until then, implementations may build
and compare commitments but must not claim a finalized purchase lifecycle.

1. Resolve the Capability and immutable version.
2. Obtain one or more gateway Quote Proposals.
3. Validate provider, manifest, endpoint, price, expiry, escrow, dispute, and
   execution-signer terms locally.
4. Build the Accepted Quote commitment locally.
5. Sign and submit the TOS transaction.
6. Consider the Quote canonical only after finalized chain verification.

## Safety rules

- Never accept a caller-selected object ID that disagrees with deterministic
  derivation.
- Never sign for a different network or registry code hash.
- Never sign an action whose predecessor does not equal the resolved state.
- Never reuse a sequence number for different action content.
- Never use portable CBOR to calculate or authorize a state transition.
- Never let a gateway substitute a Capability version or endpoint after Quote
  acceptance.
- Never expose private controller or wallet keys to a gateway or worker.
- Never retry a paid execution unless idempotency and chain state prove it safe.

## Gateway behavior

A gateway may authenticate clients, enforce rate limits, index state, search,
prepare proposals, route execution, relay signed transactions, and cache
derived views. These functions improve availability and usability but do not
grant protocol authority.

## Error behavior

Fail closed on malformed cells, unknown code, invalid signatures, threshold
failure, stale predecessor, sequence conflict, tombstoned objects, immutable
version conflicts, network mismatch, endpoint disagreement, or insufficient
finality. Preserve stable typed error categories at API boundaries.
