# Phase 5B Local Acceptance Record

Status: **implementation-complete and locally accepted on 2026-08-13**

This record identifies the reproducible local acceptance evidence for Phase
5B. It is not a production-network, HSM or operator certification.

## Frozen deployment identity

- network: `tos-phase5b-localnet`
- genesis root: `sha256:c75774012b55e1d1dbe8efbef47d0e58c77475e6327163124b8ae80fe7b71ad8`
- genesis file: `sha256:8f2f88bd2bcc406181e82224b82e946f875d7eaf356fddf8c3f4e17da63a6b12`
- validator RPC endpoints: `127.0.0.1:29545`, `127.0.0.1:29546`,
  `127.0.0.1:29547`; strict majority `2/3`
- Native Registry code hash:
  `tvm-cell-sha256:efb7b9260383ff66e9f0ca6a9bc2e30979186bd48416d3d61b116ccb65098ba7`
- compiled code BOC SHA-256:
  `6aecd66d56b456b45360dc2f325ae8206b12ec151a51ef162c87b44bd80ddcec`
- acceptance run ID: `20260813-v6-latest-binaries`

The committed FunC/Fift source was compiled twice and produced byte-identical
Fift and BOC outputs. Fift independently reported the code representation hash
above.

## Canonical lifecycle result

The production ConnectRPC server, production Unix-socket publisher, persistent
bbolt journal, hardened `tosctl`, wallet signing and three real validators
completed this lifecycle:

```text
register Agent 1 -> delegate Quote authority
 -> register Capability version 1 -> append immutable version 2
 -> rotate Agent 1 controller policy -> reject old controller
 -> register Agent 2
 -> dual-authorized Capability transfer -> reject former owner
 -> initiate recovery -> reject early execution
 -> execute timelocked recovery -> reject old controller
 -> revoke Capability version 1 -> tombstone Capability lineage
 -> tombstone Agent 2 -> resolve every final state read-only
```

Canonical objects:

- Agent 1:
  `agent_d834e16236399c66df6286d6574293b1f10b9b4511a173e6e31a5486b2f6fad9`
- Agent 2:
  `agent_f31d3c2443634c7966d5f7bdb4e04b3e3af503df006ac7bcff09a2aa1c171a5f`
- Capability:
  `cap_ce1fcd86f2f58602774491c3e59ee743e6d64b89c396fef21c9be8aa1bf19135`
- terminal finalized checkpoint: `22029`
- terminal transaction:
  `sha256:fb4a10717ebaf983ea94ffae7512fd69c058fe07676dc833f636731ba4af3064`

A separately constructed protocol process with a new empty bbolt database and
no copied seed/cache reconstructed both Agents, both immutable Capability
versions, transfer, revocations and tombstones at checkpoint `22083`. After a
cold restart of both publisher and resolver, it reproduced the same state at
checkpoint `22198`. The publisher journal SHA-256 remained byte-identical across
that read-only restart (`dd49819b382697833194e442ec3049269e60f796ffe5dfd6c61acdb778e327e9`).

## Fault and adversarial evidence

- stopping two validators made the live resolver return authority unavailable;
  restarting them restored the same canonical state;
- two honest endpoints outvoted one conflicting/stale endpoint;
- two identical stale endpoints after a recorded high-water mark were rejected
  as checkpoint regression;
- wrong genesis, network, code hash, contract address and Action Anchor tuples
  failed closed;
- canonical pending state, incomplete transaction pagination and reorganization
  ambiguity never became authoritative absence;
- a generic/proxy 404, malformed schema, wrong Action ID, wrong journal identity
  or binding, and unbound HTTP 200 never authorized mutation;
- concurrent independent publishers converged on one broadcast/action;
- real subprocess termination at prepared, attempted and completed journal
  boundaries recovered byte-identical prepared wallet messages and never
  regressed a completed record;
- purpose substitution, duplicate physical keys/weight, one-sided transfer,
  stale owner policy, forged next state, skipped predecessor, premature or
  superseded recovery, immutable-version overwrite and tombstone resurrection
  were rejected.

Negative controls used deliberately broken inputs and test implementations for
policy currentness, deterministic next-state derivation, transfer dual
authorization, recovery immediate-predecessor binding, journal-before-broadcast,
generic-404 handling, strict-majority finality and the code-hash allowlist. Each
control failed at its intended invariant before the protected implementation
was accepted.

## Validation commands

The coordinated implementation passed:

- Go formatting, `go vet ./...`, `go build ./...` and
  `go test ./... -race -count=1`;
- Native protocol/execution/registry/publisher/localrpc/toschain/atosrpc tests
  with `-race -count=10`;
- the independent Python deterministic-CBOR verifier over 12 complete state
  transitions and 16 executable negative mutations;
- protobuf byte parity and descriptor generation;
- Rust `commands` tests (32 tests) and targeted formatting;
- VM SHA256C activation and canonical-snake rejection tests;
- deterministic FunC/Fift/BOC compilation and real three-validator lifecycle,
  cold-restart, empty-replica and quorum-loss tests.

Production deployment with real operator custody/HSM, production validators,
monitoring and disaster recovery remains an external operational gate. Phase
5C discovery, 5D wallet sessions, 5E Native economics/proofs and 5F federation
failover remain out of scope and incomplete.
