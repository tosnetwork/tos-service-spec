# ATOS Native Implementation Status

**Protocol:** `atos_native_v1`

**Status basis:** repository evidence, not deployment claims

## Implemented

### Normative schema

- Clean Native protobuf namespace at `proto/atos/native/v1/native.proto`.
- Typed Agent, Capability, action, signature, network, chain-reference, Quote
  Proposal, and Accepted Quote messages.
- Frozen deterministic Agent-registration vector.

### TOS contract

- Deterministic Agent and Capability accounts.
- Typed `NVD1`, `NVS1`, `NVA1`, `NVP1`, and `NVI1` cells.
- Agent registration, policy update, delegation, recovery, and revocation.
- Capability registration, immutable version addition, version revocation,
  complete revocation, and atomic ownership transfer.
- Live policy validation and Ed25519 threshold authorization.
- Policy proof-of-possession checks when installing new controller keys.

The reviewed contract code hash is:

```text
tvm-cell-sha256:c4af55e476c296c8a1dc7985e82db42218475b9e3864b7c733351bab526ab23d
```

### Protocol implementation

- Canonical TVM action and policy construction.
- Deterministic Agent and Capability ID derivation.
- Action signing and signature verification.
- Direct relay routing through the authoritative Agent where required.
- Quorum and finalized direct account resolution.
- Strict typed TVM state decoding.
- Deterministic off-chain CBOR projection derived from decoded state.
- Accepted Quote commitment construction.

### Reference gateway

- Native Connect service at the canonical generated path.
- `native:read` and `native:relay` transport scopes.
- Direct proxying to the protocol relayer and resolver.
- Native service is the default runtime surface.

## Local validation

- `atos-spec` JSON vectors and adversarial registry vectors.
- `tos-protocol` complete Go test suite.
- `atos` complete Go test suite using the local protocol workspace.
- FunC compilation and Fift export.
- Exported contract code hash equals the frozen registration vector.

## Not yet production-complete

- Public testnet deployment and reproducible deployment record.
- Independent contract audit and adversarial test corpus review.
- Multi-endpoint finality evidence under forks and endpoint disagreement.
- End-to-end wallet signing and recovery UX.
- Native discovery index and cross-gateway interoperability protocol.
- Finalized Accepted Quote transaction flow.
- Escrow, execution receipt, dispute, and settlement contracts for the Native
  commerce path.
- Multi-operator conformance and failover exercise.
- Production key custody, monitoring, incident response, and capacity evidence.

## Completion rule

A feature is complete only when its normative schema, implementation,
adversarial tests, cross-repository vector, and operational evidence all agree.
Local compilation alone is not a production claim.
