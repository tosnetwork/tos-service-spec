# Native Registry Submission and Resolution V1

## Service

`atos.native.v1.NativeService` exposes two operations:

```text
SubmitNativeAction
ResolveNativeState
```

Connect and Protobuf are the canonical wire contract. JSON transcoding, if
offered, must preserve exact field semantics and byte encodings.

## SubmitNativeAction

The request contains context and a `SignedNativeActionV1`. The service performs
bounded syntax checks, constructs the canonical action cell, derives the
destination, constructs the message body, and asks a fee-paying sender to relay
it.

Routing rules:

- Agent registration targets the deterministic new Agent account and includes
  StateInit.
- Agent mutations target the Agent account directly.
- Capability registration and administration target the current owner Agent.
- Capability transfer first targets the current owner Agent.

The response returns the canonical action hash and `relay_accepted`. The flag
means only that the transport backend accepted submission. It does not prove
inclusion, successful execution, or finality. A response may omit state.

Clients confirm success through `ResolveNativeState` and compare
`last_action_hash`, generation, sequence, state hash, and chain reference.

## ResolveNativeState

The request contains object ID and an optional expected TVM state hash. The
resolver:

1. reconstructs the deterministic account;
2. queries configured independent TOS endpoints;
3. establishes endpoint quorum and finality;
4. verifies account, code hash, and state hash;
5. decodes typed TVM state without an auxiliary database; and
6. returns the typed state and exact chain reference.

`found=false` is valid only for authoritative absence at the reported finalized
checkpoint. Endpoint failure or disagreement is an error, not absence.

When `expected_tvm_state_hash` is supplied, a different finalized hash is a
conflict. It must not be silently returned as success.

## Request context

`request_id` and `trace_id` are observability values. `idempotency_key` helps
transport deduplication. `caller_id` describes the authenticated transport
principal. None participates in contract authorization. Deadlines bound server
work but do not alter on-chain semantics.

## Security

- Bound message size before protobuf decoding and cell construction.
- Authenticate and rate-limit public submission.
- Keep fee-payer keys outside the gateway process where practical.
- Never rewrite signed action fields.
- Never accept caller-supplied action-result or next-state cells.
- Avoid automatic paid resubmission after ambiguous errors; resolve first.
- Return stable typed errors without leaking private configuration.
