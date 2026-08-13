# ATOS Native Public API

## Protocol surface

The public Native API is the Connect service generated from
`proto/atos/native/v1/native.proto`:

```text
atos.native.v1.NativeService/SubmitNativeAction
atos.native.v1.NativeService/ResolveNativeState
```

The canonical Connect path is generated from this fully qualified service name.
Gateways also expose:

```text
GET /livez
GET /readyz
```

Authentication bootstrap endpoints may be gateway-local. They do not define
protocol objects.

## Submit semantics

`SubmitNativeAction` requires `native:relay`. The caller supplies canonical
action fields and semantic signatures. The gateway may reject malformed,
over-bound, unauthenticated, or rate-limited requests before relaying. It may
not change the action to make it acceptable.

Success at this API boundary means relay acceptance only. Clients must resolve
finalized state to determine canonical outcome.

## Resolve semantics

`ResolveNativeState` requires `native:read`. It returns typed Agent or
Capability state plus network, TVM state hash, and chain reference. The gateway
must fail closed if quorum, finality, deterministic address, code identity, or
typed decoding cannot be established.

## Error mapping

| Connect code | Meaning |
|---|---|
| `invalid_argument` | malformed or non-canonical request |
| `unauthenticated` | missing or invalid transport credential |
| `permission_denied` | credential lacks required transport scope |
| `not_found` | authoritative finalized absence when represented as an error |
| `already_exists` | immutable registration or version conflict |
| `failed_precondition` | stale predecessor, sequence, revocation, or policy state |
| `aborted` | finalized conflicting transition |
| `resource_exhausted` | size, rate, fee, or capacity bound reached |
| `unavailable` | quorum, finality, relayer, or required dependency unavailable |
| `internal` | bounded unexpected implementation failure |

Error messages are diagnostic, not stable machine identifiers. Conformance
tests should assert code and structured detail where defined.

## Health

`/livez` confirms the process can serve. `/readyz` confirms authentication,
Native backend, relayer, resolver, network configuration, and required chain
connectivity are ready. A gateway must leave readiness when it cannot safely
establish canonical semantics.

## Future gateway protocol

Discovery, proposal, invocation, artifact, receipt, and settlement APIs are
added only after their chain commitments and conformance rules pass the roadmap
gate. They must reuse the same Agent, Capability, Accepted Quote, and chain
reference types rather than invent parallel gateway-owned objects.
