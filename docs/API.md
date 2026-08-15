# TOS Native Service Public API

## Protocol surface

The public Native API is the Connect service generated from
`proto/tos/service/v1/native.proto`:

```text
tos.service.v1.NativeService/SubmitNativeAction
tos.service.v1.NativeService/ResolveNativeState
tos.service.v1.CapabilityDiscoveryService/ListCapabilities
tos.service.v1.CapabilityDiscoveryService/SearchCapabilities
tos.service.v1.CapabilityDiscoveryService/PublishSoftwareWorkManifest
tos.service.v1.CapabilityDiscoveryService/GetSoftwareWorkManifest
tos.service.v1.CapabilityDiscoveryService/RequestQuoteProposal
```

The canonical Connect path is generated from this fully qualified service name.
Gateways also expose:

```text
GET /livez
GET /readyz
```

Authentication bootstrap endpoints may be gateway-local. They do not define
protocol objects.

The Discovery service is a derived convenience boundary, separate from the
canonical Native service. `ListCapabilities`, `SearchCapabilities`, and
`GetSoftwareWorkManifest` require `native:read`;
`PublishSoftwareWorkManifest` requires `native:relay`.
`RequestQuoteProposal` requires `native:read`; it returns provider-supplied
non-canonical terms and never accepts them for the buyer.
These permissions control transport and storage use only.

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

## Capability discovery and manifest semantics

The discovered ID set is explicitly incomplete and gateway-local. A listing
must freshly resolve every returned Capability from finalized TOS state and
must exclude a freshly tombstoned Capability. Its continuation token means
only “after this locally discovered ID”; it is not a chain cursor or a proof of
completeness. Page size is at most 100 IDs.

Manifest publication accepts only the canonical CBOR defined in
`SOFTWARE_WORK_MANIFEST_V1.md`. Before storage, the gateway freshly resolves
the supplied Capability and proves that an active version with the same
version string commits to the exact SHA-256 digest. Storage is immutable and
content-addressed. Retrieval returns those exact canonical bytes by digest.

`SearchCapabilities` is deliberately gateway-local and incomplete. Every
result contains a freshly resolved finalized Capability plus the exact active
version and manifest digest selected from that chain state. Human-readable
manifest fields and the match score are nested under `gateway_local`; they are
digest-authenticated discovery projections, not chain state, ranking consensus,
or an availability guarantee. Pagination remains ordered by Capability ID so
the token does not silently encode a mutable ranking.

Consumers must hash the returned bytes and compare the digest with a fresh
Capability resolution or the Accepted Quote. Index inclusion, ordering,
availability, names, descriptions, and manifest storage are not protocol
facts. Resolver failure, rollback behind a persistent checkpoint fence,
same-checkpoint conflict, malformed bytes, or corrupted storage fails closed.

Clients may compose multiple independent discovery services according to
`GATEWAY_FEDERATION_V1.md`. Federation preserves source identity, rejects a
malformed Gateway page as a unit, isolates unavailable peers, and verifies
manifest bytes by the exact chain-committed digest. The union and its ordering
remain non-canonical discovery hints.

## Error mapping

Every error carries the single canonical `NativeErrorV1` detail defined by
`PUBLIC_ERRORS_V1.md`. The Connect code alone never authorizes an automatic
retry.

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

Unknown mutation outcomes use `aborted` plus `RESOLVE_BEFORE_RETRY`, not
`unavailable`. Read-only dependency failures may permit the identical request
after bounded backoff. Missing or inconsistent error details fail closed.

Error messages are diagnostic, not stable machine identifiers. Conformance
tests should assert code and structured detail where defined.

## Health

`/livez` confirms the process can serve. `/readyz` confirms authentication,
Native backend, relayer, resolver, network configuration, and required chain
connectivity are ready. A gateway must leave readiness when it cannot safely
establish canonical semantics.

## Quote Proposal exchange

`RequestQuoteProposal` names an exact Capability version and canonical raw
buyer address. A successful response carries `QuoteProposalV1` plus the exact
canonical manifest CBOR and canonical single-root BOCs for escrow terms,
transport binding, and objective dispute policy. Clients reject the package if
any preimage digest, requested identity, buyer address, bound, or expiry
conflicts. They still resolve Capability and asset state directly and select
their own execution-signer authorization.

The response remains discardable and non-canonical. Only the deterministic
Accepted Quote escrow commitment finalized on TOS records accepted terms.

## Next commercial surface

Minimal Capability discovery, manifest retrieval, and complete-preimage Quote
Proposal exchange are now frozen. Further API additions remain limited to
Accepted Quote and escrow submission, one bound job, artifact retrieval,
Receipt resolution, and release or refund. Exact methods must be frozen in
this Native protobuf before implementation.

General marketplace, reputation, consumer checkout, and generalized arbitration
APIs are not part of this release.

The provider-local execution and artifact boundary is frozen in
[`SOFTWARE_WORK_EXECUTION_V1.md`](SOFTWARE_WORK_EXECUTION_V1.md). It is not a
public RPC and cannot be exposed as one until the chain-verification inputs and
exact methods are added to this protobuf contract.

## Adapter boundary

A2A may carry task, progress, and result messages. MCP may expose the same
Capability as a tool. An optional x402 adapter may carry payment negotiation.
Adapters translate transport objects into the one Native lifecycle; they do not
create alternate identities, Quotes, Receipts, balances, or settlement state.

Every future gateway API must reuse the same Agent, Capability, Accepted Quote,
Receipt, and chain-reference types rather than invent parallel gateway-owned
objects.
