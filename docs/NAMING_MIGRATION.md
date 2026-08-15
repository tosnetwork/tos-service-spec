# TOS Service Protocol Naming Migration

## Decision

The pre-launch protocol is named **TOS Service Protocol**. The rename is a
breaking domain reset, not a compatibility alias. Current implementations must
not accept old protocol identifiers, protobuf service names, schema domains,
environment variables, discovery paths, or module imports.

## Canonical names

| Surface | Current value |
|---|---|
| specification repository | `tosnetwork/tos-service-spec` |
| Go protocol repository/module | `tosnetwork/tos-service-protocol` |
| reference Gateway repository/module | `tosnetwork/tos-service-gateway` |
| wire protocol | `tos_service_v1` |
| protobuf package | `tos.service.v1` |
| protobuf Go package | `gen/tos/service/v1` |
| schema and signing domain prefix | `tos.service.*` |
| Gateway locator | `/.well-known/tos-service.json` |
| Gateway environment prefix | `TOS_SERVICE_*` |
| private RPC configuration | `TOS_SERVICE_V1_CONFIG` |
| wallet command | `tos-service-wallet` |
| discovery command | `tos-service-discovery` |
| private RPC command | `tos-service-rpc` |

`TOS Service Gateway` names a replaceable implementation. It is not the name
of the protocol and has no semantic authority.

## Cryptographic consequence

Protocol and schema domains participate in identifiers, signatures, manifests,
Quote commitments, and execution claims. A pre-migration object cannot be
renamed in place. It must be created again from current bytes and signed again.
Historical deployment evidence remains byte-for-byte unchanged under
`deployments/archive/pre-tos-service-v1/` and is not current acceptance
evidence.

## Release sequence

1. Publish `tos-service-spec` with the current schema and vectors.
2. Publish `tos-service-protocol` with its new Go module and generated protobuf.
3. Update dependent Go modules to the new protocol commit and regenerate their
   checksums.
4. Publish `tos-service-gateway`, `tos-ai`, OpenFox, and client updates.
5. Deploy fresh Registry and commerce objects and repeat Gates C–F as required
   by `ROADMAP.md`.

There is no production deployment requiring a dual-name transition. Adding an
old-name fallback would create a second authority domain and is prohibited.
