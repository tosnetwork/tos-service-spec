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

The breaking reset is enforced cryptographically by the **network domain** and
**contract code identity**, not by the protocol identifier string. Identifiers,
signatures, Agent/Capability IDs, Accepted Quote commitments, manifests, and
execution claims each bind the complete network domain (genesis root hash,
genesis file hash, network ID) and, where applicable, the contract code hash and
the immutable manifest digest. The wire protocol identifier (`tos_service_v1`)
and schema strings are transport and build-time validation fields; they are
validated before bytes are built and are deliberately **not** part of any signed
cell or on-chain commitment (see `NATIVE_REGISTRY_STATE_MACHINES.md` §1.1). This
is consistent with the contributor rule *"keep transport context outside signed
action semantics"* and matches the frozen implementation and vectors.

A pre-migration object cannot be renamed in place; it must be created again from
current bytes and signed again. Because that recreation happens on a **fresh,
unique genesis**, its network-domain commitment differs from every archived
network, so no pre-migration signature, identifier, or commitment is valid on the
current network — this, not the identifier rename, is what makes the reset
binding. Consequently every current deployment MUST use a network domain whose
genesis root/file hashes differ from all prior and archived networks;
`ROADMAP.md` Gate C records that distinctness as acceptance evidence. Historical
deployment evidence remains byte-for-byte unchanged under
`deployments/archive/pre-tos-service-v1/` and is not current acceptance
evidence.

Adding the protocol identifier to a signed cell is intentionally **not** done: it
would place transport context inside signed action semantics, would duplicate the
separation the network domain already provides more strongly, and would require
retiring the independently reviewed frozen Registry code hash
`600f2fda83462bc86a1c32af930c35a4fc8f80f1d2966f5593ceba217a91ffa0` and
regenerating every frozen identifier, address, action, signature, and Quote
vector for no additional cross-chain guarantee.

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
