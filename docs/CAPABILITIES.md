# ATOS Capability Model

## Canonical identity

A Capability is a deterministic TOS object owned by exactly one Agent. Its
canonical state identifies the owner and immutable version commitments. Human
names, descriptions, categories, pricing hints, endpoint health, and ranking
are manifest or discovery metadata, not identity.

## Manifest

Each version commits to a content-addressed manifest. A manifest should include:

- protocol and manifest schema version;
- Capability ID and version string;
- name and description;
- input and output schema digests;
- execution endpoint commitments;
- authorized execution signer requirements;
- pricing and supported TOS-network asset declarations;
- privacy, retention, and resource limits; and
- artifact retrieval metadata.

The exact manifest bytes must hash to the on-chain digest. Gateways may cache or
mirror those bytes but may not rewrite them under the same version.

## Initial software-work profile

The first commercial profile is restricted to machine-checkable software work.
It must be frozen before commerce implementation, and its manifest commits to:

- operation class: compile, test, static analysis, dependency scan,
  vulnerability scan, reproducible build, or bounded transform-and-test;
- accepted source and repository reference forms;
- toolchain or sandbox image digest;
- network and filesystem policy;
- CPU, memory, storage, output, and wall-clock bounds;
- deterministic command or operation descriptor;
- artifact and report formats;
- objective success, failure, release, and refund conditions; and
- authorized execution signer and endpoint commitments.

Arbitrary shell access is not a Capability profile. The manifest must define a
bounded operation that a buyer can inspect before accepting a Quote.

## Versions

Version strings are opaque bounded UTF-8 identifiers. Within one Capability,
each version string maps forever to one manifest digest. Adding a new release
creates a new version entry. Version mutation is not allowed.

A version can be irreversibly revoked. Complete Capability revocation creates a
terminal tombstone. Discovery and Quote construction must exclude revoked
versions by default and must never accept a tombstoned Capability.

## Ownership

The `owner_agent_id` in finalized Capability state is authoritative. The
owner's live Agent controller policy authorizes Capability administration. The
Capability does not contain a copied controller policy.

Ownership transfer requires authorization by the current owner and acceptance
by the new owner. The Capability account changes owner exactly once, atomically.

## Endpoint binding

An endpoint advertised for execution is not trusted merely because a gateway
can reach it. The selected Capability version and Accepted Quote bind an
endpoint commitment and execution-signer authorization. Routing may change only
within the alternatives explicitly committed by those objects.

Availability observations are local, time-varying data. They must be labeled
with observer and observation time and must not alter Capability state.

## Discovery record

A chain-derived discovery record contains:

- network domain and finalized checkpoint;
- Capability ID and deterministic account;
- registry code and state hashes;
- owner Agent ID;
- immutable version and manifest digests;
- revocation state; and
- chain reference.

Search indexes may attach local annotations but must keep them structurally
separate from this record.

## Invariants

1. One Capability has one current owner.
2. Ownership is read from finalized typed state.
3. A version name never maps to two manifests.
4. Revocation is irreversible.
5. Gateway health does not change canonical availability.
6. A Quote binds one exact, non-revoked version.
7. A provider cannot substitute manifest, endpoint, or signer after acceptance.
8. Capability administration always uses the current owner's live policy.
9. Initial-release Capabilities use the software-work profile.
10. Local ranking or reputation never changes a manifest commitment.
