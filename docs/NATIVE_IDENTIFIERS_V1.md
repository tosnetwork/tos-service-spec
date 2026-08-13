# Native Identifiers V1

## Network domain

Every identifier and signed action is bound to:

```text
network_id
genesis_root_hash = sha256:<64 lowercase hex>
genesis_file_hash = sha256:<64 lowercase hex>
```

All three values are mandatory. A human network name alone is insufficient.

## Text and digest rules

- Protocol text is UTF-8, bounded, and free of control characters.
- Protocol identifiers and hexadecimal digests are lowercase.
- SHA-256 digests use `sha256:<64 lowercase hex>`.
- TVM cell hashes use `tvm-cell-sha256:<64 lowercase hex>`.
- Object IDs are parsed strictly; alternate encodings are rejected.

## Agent ID

An Agent ID is:

```text
agent_<lowercase SHA-256 hex>
```

The digest is calculated from the canonical identity cell containing protocol
version, network domain, object nonce, and canonical initial controller policy.
Controller input order does not affect the result because policies are sorted
canonically before encoding.

## Capability ID

A Capability ID is:

```text
cap_<lowercase SHA-256 hex>
```

The digest is calculated from the canonical identity cell containing protocol
version, network domain, object nonce, owner Agent ID, initial version string,
and initial manifest digest.

The owner's controller policy is not part of Capability identity. Policy
rotation therefore never changes Capability ID.

## Deterministic account

The account address is derived from the StateInit containing the reviewed
registry code cell and the data cell for network, object kind, and object ID.
Resolution must reconstruct this address rather than accept an unverified
address from a gateway.

## Version identity

A Capability version is identified by the pair:

```text
(capability_id, version_string)
```

The version string maps immutably to one manifest digest. Reusing a version
string for different bytes is invalid. Revocation does not free the name.

## Controller key ID

Controller key IDs are exactly:

```text
ed25519:<64 lowercase hex public key>
```

This format makes the key identity reconstructible from canonical state without
an alias registry.

## Rejection rules

Reject wrong prefixes, uppercase or short hexadecimal forms, whitespace,
Unicode lookalikes, malformed digests, unknown object kinds, empty version
names, inconsistent key IDs, and identifiers that disagree with deterministic
registration derivation.
