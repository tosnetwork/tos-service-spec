# Native Registry Public Testnet Gate

This document defines the evidence required to complete ROADMAP Gate C. A
local chain, mocked RPC response, relay acknowledgement, or single endpoint is
not public-testnet acceptance evidence.

## Deployment identity

A deployment record must publish:

- protocol `atos_native_v1`;
- exact TOS network ID and genesis root/file hashes;
- Registry workchain;
- frozen code BOC, TVM code hash, BOC container SHA-256, byte size, source
  commit, and reproducible build command;
- at least three independently operated HTTPS JSON-RPC endpoints and a strict
  majority quorum;
- deployment time and finality policy; and
- explorer and typed-state-checker URLs.

There is no global mutable Registry database contract. Agent and Capability
accounts are deterministic instances of the published code. The first accepted
Agent registration therefore publishes the code on-chain; later registrations
must resolve to the same pinned code hash.

## Wallet requirements

The signing wallet must:

- load controller seeds only from owner-private local or hardware-backed
  storage;
- display network, target object, contract code hash, generation, sequence,
  predecessor, action type, and action hash;
- require explicit semantic confirmation before signing;
- preserve the exact action bytes through relay;
- confirm destination, exact nanoTOS relay amount, body hash, and StateInit hash
  before the fee-payer wallet broadcasts; and
- treat broadcast acceptance as pending until finalized typed state contains
  the action hash.

## Required lifecycle evidence

Two independently controlled wallets must complete and publish:

1. Agent registration;
2. Agent policy update with new-key proof of possession;
3. recovery initiation and completion after the timelock;
4. Capability registration through the live owner Agent;
5. Capability version addition and version revocation;
6. atomic Capability transfer accepted by the new owner;
7. rejection of a post-transfer mutation signed only by the former owner;
8. terminal Capability and Agent revocation drills on disposable objects; and
9. resolution of every result from endpoint quorum without the reference
   gateway.

Each record includes object ID, deterministic address, action hash, state hash,
transaction hash, logical time, finalized checkpoint, code hash, and the
independent resolver outputs. Secrets, private wallet configuration, gateway
tokens, and private RPC credentials are never part of the record.

## Current external blocker — 2026-08-13

The implementation and release artifact are ready for deployment preparation,
but this gate is not accepted:

- the machine has no configured funded public-testnet wallet or deployment
  authority;
- no set of three independently operated public TVM JSON-RPC endpoints and
  exact genesis hashes is configured;
- the advertised public testnet endpoint was not reachable from the deployment
  host during this review; and
- no independently operated wallet or resolver has produced lifecycle
  evidence.

Supplying one funded testnet wallet is not sufficient by itself. Endpoint
diversity, a second independent wallet/resolver, and the independent security
review remain mandatory acceptance inputs.
