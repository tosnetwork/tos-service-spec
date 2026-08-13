# Native Identifiers V1

Status: **normative Phase 5A contract**

## 1. Scope

This document freezes gateway-independent Agent and Capability identifiers for
TOS Native mode. A local `principal_id`, database primary key, HTTP origin,
wallet address, controller key, mutable display name, ARD identifier or
`atos.im` namespace MUST NOT be used as a Native identifier.

All strings in this contract are exact ASCII. Implementations MUST reject
Unicode lookalikes, leading/trailing whitespace, case aliases, percent escapes,
path normalization, default-network inference and unknown critical versions.

## 2. Network domain

Every identifier bootstrap value includes this exact tuple:

```text
network_id        ASCII lower-case [a-z0-9.-], 1..63 bytes
genesis_root_hash "sha256:" + 64 lower-case hexadecimal digits, not all zero
genesis_file_hash "sha256:" + 64 lower-case hexadecimal digits, not all zero
```

The two genesis hashes are independent fields. Network display names alone are
not authority. A change to any field produces a different identifier.

## 3. Canonical encoding and digest

Values use RFC 8949 Core Deterministic CBOR over the explicitly tagged JSON
data model. Maps use the RFC 8949 deterministic ordering. Integers are encoded
in their shortest form. Floats, CBOR tags, indefinite lengths, duplicate map
keys, invalid UTF-8, unknown fields and non-canonical encodings are rejected.

The digest function is:

```text
SHA-256(
  "TOS-PROTOCOL-CBOR" || 0x00 ||
  uint16_be(byte_length(domain)) || UTF8(domain) ||
  canonical_cbor(value)
)
```

No delimiter-joined field hashing is permitted.

## 4. Agent ID

Domain: `tos.native.agent-id.v1`.

```text
version                           = "tos_native_registry_v1"
network                           = NetworkDomain
object_nonce_base64url            = exactly 32 bytes, RFC 4648 raw base64url
initial_controller_policy_digest  = lower-case sha256 digest
```

The text ID is `agent_` followed by the 64 lower-case hexadecimal digest
digits. The object nonce MUST come from a cryptographically secure random
source. Controller rotation, recovery, delegation and policy changes do not
change the Agent ID. Re-registering the same bootstrap value is exact replay,
not a second Agent.

Canonical URI: `atos://agent/<agent-id>`.

## 5. Capability ID and version URI

Domain: `tos.native.capability-id.v1`.

```text
version                 = "tos_native_registry_v1"
network                 = NetworkDomain
owner_agent_id          = canonical Agent ID
object_nonce_base64url  = exactly 32 bytes, RFC 4648 raw base64url
```

The text ID is `cap_` followed by the 64 lower-case hexadecimal digest digits.
Ownership transfer and owner-controller rotation do not change it.

The lineage URI is `atos://capability/<capability-id>`. An immutable version URI is:

```text
atos://capability/<capability-id>/versions/<semver>
```

`semver` is canonical SemVer without leading-zero numeric components or build
metadata (`+...`), because build metadata would create multiple textual aliases
with equal SemVer precedence. The bare
Capability ID names the stable lineage; commercial commitments MUST name an
exact immutable version.

## 6. Error taxonomy

| Code | Meaning |
|---|---|
| `NATIVE_UNSUPPORTED_VERSION` | version or critical extension is unknown |
| `NATIVE_INVALID_NETWORK` | network/genesis tuple is invalid or mismatched |
| `NATIVE_INVALID_IDENTIFIER` | ID bytes/text do not match this contract |
| `NATIVE_NONCANONICAL_URI` | URI has an alias, escape or invalid version |
| `NATIVE_CANONICAL_ENCODING` | deterministic CBOR validation failed |
| `NATIVE_CROSS_DOMAIN_REPLAY` | value was used under another purpose/domain |

Normative positive and adversarial values are in
`test-vectors/native_registry_v1.json`.
