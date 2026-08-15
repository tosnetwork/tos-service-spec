# Native Registry Public Testnet Gate

This document defines the evidence required to complete ROADMAP Gate C. The
project owner may designate a versioned TOS network as the initial TOS Service Protocol public
test network. Gate C bootstraps protocol authority; operator and Internet
diversity remain separate Gate F and Gate G requirements. A mocked RPC
response, relay acknowledgement, or single endpoint is never acceptance
evidence.

## Initial public-testnet profile

The initial profile permits three validator-backed endpoints operated on one
host when all limitations are published in the deployment record. It requires:

- at least three live TOS validator-backed JSON-RPC endpoints and quorum two;
- ConfigParam 8 at version 14 or later;
- one immutable network/genesis identity and frozen Registry release;
- distinct Agent controller keys for the transfer lifecycle;
- the production quorum resolver and typed-state decoder, not direct database
  inspection; and
- a complete finalized lifecycle with transaction and checkpoint evidence.

Loopback HTTP endpoints may satisfy this bootstrap profile only when the record
states that they are not publicly reachable or independently operated. They do
not satisfy gateway federation, production endpoint diversity, or production
readiness. Publishing an endpoint later requires authenticated HTTPS.

## Deployment identity

A deployment record must publish:

- protocol `tos_service_v1`;
- exact TOS network ID and genesis root/file hashes;
- Registry workchain;
- frozen code BOC, TVM code hash, BOC container SHA-256, byte size, source
  commit, and reproducible build command;
- at least three validator-backed JSON-RPC endpoints and a strict majority
  quorum, with operator and transport limitations stated explicitly;
- deployment time and finality policy; and
- an explorer URL when one exists, plus the exact typed-state checker command
  and machine-readable output.

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

Two distinct Agent controller keys must complete and publish:

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

## Initial public-testnet deployment — 2026-08-14

The complete required lifecycle passed against a version-14 TOS network
with a four-validator genesis, three validators online, and three same-host
liteservers. The project owner subsequently designated this network as the
initial TOS Service Protocol public test network. The run deployed the frozen Registry code,
exercised two Agent controllers, recovery, Capability version management,
atomic transfer, former-owner rejection, and terminal revocations, then
reproduced the final typed state through all three liteservers.

The machine-readable deployment record is
`deployments/archive/pre-tos-service-v1/initial-public-testnet-2026-08-14.json`. Three embedded JSON-RPC
servers on ports 8011 through 8013 were then checked by the production quorum
resolver. Its typed outputs are recorded in
`deployments/archive/pre-tos-service-v1/initial-public-testnet-quorum-2026-08-14.json`.

**Gate C verdict: accepted under the initial public-testnet profile.** The
record explicitly discloses that all nodes and endpoints share one host and
that the endpoints are loopback HTTP. Independent operators, public HTTPS,
gateway failover, and Internet reachability remain mandatory Gate F/G work and
must not be inferred from this acceptance.
