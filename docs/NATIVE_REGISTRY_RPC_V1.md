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

`request_id` and `trace_id` are observability values. `idempotency_key` is a
mandatory request-retry alias, but it is not the fee-spend identity. The
canonical state-slot identity is derived from protocol, network domain,
Registry code hash, target object, generation, sequence, and predecessor TVM
state hash. It deliberately excludes nonce, payload, signatures, and action
hash because different signed intents for one ordering position are mutually
exclusive on-chain. Before paying any fee, the relayer atomically claims that
state slot. Exactly one canonical action identity, derived from network domain,
Registry code hash, and action hash, may occupy it. A fresh request key or a
fresh nonce therefore cannot buy another broadcast for the same transition.

The canonical action identity deterministically supplies the query ID, so a
caller cannot alter the outbound body by changing its request key. One
atomically created slot record binds the ordering position, action identity,
action hash, destination, query ID, body hash, StateInit hash, funded nanoTOS,
claim time, and durable phase. A separate request record binds each
`idempotency_key` to the action; it is not a fee-spend boundary. Reusing a
request key, state slot, or action with different semantics is a conflict.

The slot phases are `prepared`, `broadcasting`, and `complete`. `prepared`
proves the sender has not been entered and may be recovered after process
restart. Immediately before calling the sender, a process must atomically
acquire the sole broadcast lease by changing `prepared` to `broadcasting`
under the journal's exclusive lock. Concurrent recovery attempts cannot both
acquire it. `broadcasting` means the outcome may be ambiguous and permits only
read-only finalized-state resolution, never rebroadcast. `complete` records
sender acceptance and returns the recorded action hash on retry. A crash after
the durable `broadcasting` transition but before the sender call is treated
conservatively as ambiguous because the sender boundary is not transactional.

`caller_id` describes the authenticated transport principal. It does not
participate in contract authorization. Deadlines bound server work but do not
alter on-chain semantics.

The relayer must locally reject wrong network/code binding and every signature
or proof-of-possession failure decidable from the registration policy or a
finalized live policy. Failure to resolve required authority is an unavailable
decision, never permission to spend relay funds.

The relayer must also resolve the finalized target object before claiming a
new state slot. Registration requires authoritative absence. Every mutation
requires an exact predecessor hash, the immediately next generation/sequence,
the correct object kind, and a non-terminal target. Capability preflight also
requires the finalized current owner, immutable-version conditions, and the
requested revocation state. Transfer additionally requires a live new-owner
Agent. Resolver failure, non-finalized evidence, and ambiguous absence fail
closed before journaling or payment.

That target-state result also carries the chain-authored unix time from the
same quorum-finalized masterchain observation. Gateway wall-clock time is not
contract time and MUST NOT authorize a recovery transition. Recovery
initiation requires:

```text
execute_after >= finalized_chain_time
               + live_policy.recovery_timelock
               + recovery_relay_safety_seconds
```

`recovery_relay_safety_seconds` is mandatory deployment policy in the inclusive
range 300 through 86400 seconds. It covers finalized-observation age, relay
latency, and inclusion delay; a missing or out-of-range value makes the relayer
unready. Recovery completion requires the same finalized chain time to be at or
after the stored `execute_after`. The resolver must return time, state, and
checkpoint from one observation; it may not combine a fresh timestamp with an
older account read. It rechecks observation freshness inside every resolution;
a readiness probe performed earlier cannot authorize a later paid request.
Zero, stale, future, unavailable, or inconsistent chain time fails closed before
a journal claim or paid broadcast.

Before creating a journal claim, the relayer also mirrors the contract's
signature-set shape: counterparty signatures are forbidden for registration,
delegation, recovery completion, revocation, and Capability register/add/revoke;
they are required and fully verified for policy update, recovery initiation,
and Capability transfer.

The durable journal and finalized resolver are mandatory dependencies of the
submission operation itself, not merely startup recommendations. A caller that
bypasses server readiness checks still fails closed; there is no in-memory
idempotency or authorization fallback.

## Security

- Bound message size before protobuf decoding and cell construction.
- Authenticate and rate-limit public submission.
- Enforce persistent sliding-window action and nanoTOS ceilings per target and
  per relay wallet in the same exclusive journal transaction that claims a new
  state slot. Count prepared and ambiguous claims conservatively as spent.
- Keep fee-payer keys outside the gateway process where practical.
- Never rewrite signed action fields.
- Never accept caller-supplied action-result or next-state cells.
- Avoid automatic paid resubmission after ambiguous errors; resolve first.
- Never use process wall-clock time to satisfy a contract timelock. Bind
  recovery preflight to quorum-finalized chain time and the configured relay
  safety margin.
- All processes or hosts spending from one relay wallet must share the same
  durable state-slot/action journal; otherwise each wallet boundary must be
  treated as an independent fee budget.
- Persist finalized checkpoint high-water state per network and genesis; commit
  it only after the complete account observation and typed state validate.
- Make the durable checkpoint a mandatory resolver dependency and fsync both
  its owner-private file and containing directory before serving advanced
  state; no process-local-only fallback is permitted.
- Return stable typed errors without leaking private configuration.

## Stable errors

Validation errors use `NativeErrorV1` Connect error details. Numeric values
`2200` through `2213` exactly match the Native Registry TVM exit-code family.
Clients branch on the enum value or stable identifier and must not parse the
human diagnostic. The frozen negative corpus in
`test-vectors/atos-native-v1-registry.json` pins representative preflight
results across two implementations.
