# Software-Work Manifest V1

## Status and authority

This document freezes the first TOS Service Protocol commercial Capability profile. The
manifest is immutable, content-addressed off-chain data. Finalized typed TOS
state remains the authority for the Capability version and its manifest
digest; a gateway copy has no authority.

The media type is
`application/vnd.tos.service.software-work-manifest.v1+cbor`. Canonical bytes use RFC
8949 Core Deterministic Encoding, definite lengths, no floats, and the integer
field keys below. The digest is `sha256:<lowercase hex>` over those exact bytes.

The manifest MUST NOT contain `capability_id`. A Capability ID commits to the
manifest digest, so placing the resulting ID back inside the hashed manifest
would create a circular definition. The finalized Capability state supplies
that association.

## Canonical root map

| Key | JSON projection | Type and bound |
|---:|---|---|
| 1 | `protocol` | exact `tos.service.software-work-manifest.v1` |
| 2 | `version` | 1–64 printable ASCII identifier |
| 3 | `name` | 1–128 printable UTF-8 bytes |
| 4 | `description` | 1–2048 printable UTF-8 bytes |
| 5 | `operation` | frozen operation enum |
| 6 | `accepted_source_kinds` | sorted unique array, 1–8 |
| 7 | `input_schema_digest` | non-zero SHA-256 digest |
| 8 | `output_schema_digest` | non-zero SHA-256 digest |
| 9 | `toolchain_digest` | non-zero SHA-256 digest |
| 10 | `invocation` | invocation map |
| 11 | `network_policy` | exact `none` in v1 |
| 12 | `limits` | resource-limit map |
| 13 | `artifact_media_types` | sorted unique array, 1–16 |
| 14 | `report_media_types` | sorted unique array, 1–16 |
| 15 | `success_condition` | exact objective condition |
| 16 | `refund_conditions` | sorted unique frozen enum |
| 17 | `endpoint_commitment` | non-zero SHA-256 digest |
| 18 | `execution_signer_authorization` | non-zero SHA-256 digest of the attestor key text form |
| 19 | `retention_seconds` | 3600 through 2592000 |
| 20 | `supported_assets` | exactly one asset entry: native TOS |
| 21 | `settlement` | settlement map |

Schema digests are SHA-256 over the exact UTF-8 bytes, including the final
newline, of the corresponding files in [`schemas/`](../schemas/). V1 freezes
`software-work-job-v1.schema.json` as the input schema and
`software-work-outcome-v1.schema.json` as the output schema.

Operation values are `compile`, `test`, `static-analysis`,
`dependency-scan`, `vulnerability-scan`, `reproducible-build`, and
`bounded-transform-and-test`. Accepted source kinds are
`content-addressed-archive` and `immutable-repository-commit`.

The invocation map keys are executable (1), argument array (2), and working
directory (3). Paths are absolute sandbox paths; the working directory is
under `/workspace`. General-purpose shell interpreters are forbidden. The
argument array has at most 64 printable entries of at most 512 bytes.

The limit map keys are CPU milliseconds (1), memory bytes (2), scratch bytes
(3), output bytes (4), and wall-clock milliseconds (5). Zero and values above
the implementation bounds are invalid. These values are execution-contract
bounds, not post-hoc gateway observations.

The v1 success condition is `exit-code-zero-and-valid-reports`. The first
fixed-price profile permits exactly one refund value:
`no-attested-response-before-deadline`. The Service Actor returns the price
whenever no attested `respond` lands before the request's
`response_deadline`, whether or not work started: through `claim_refund` by
the caller before `refund_claim_deadline`, or through a sweep at or after it,
which pays the price to the caller. The storage fee is not refunded in either
case. Infrastructure, resource-limit, or digest failures cannot produce a
releasable Receipt, because the attestor custody refuses to sign one (see the
Receipt document). Normal tool failure is a valid charged result only when the
selected profile explicitly treats it as success; this first profile requires
exit code zero.

## Asset

Key 20 is an array of exactly one element, the native TOS entry: the map
`{0: "native-tos"}` (key 0, the exact text). Amounts are nanoTOS. The Service
Actor rail settles nothing else, so stablecoin identities are not admitted in
this profile; a ticker is display metadata and never an asset identity.

## Settlement map

Key 21 names the Service Actor that settles this Capability version. It is the
owner Agent's statement, published under its Capability-control policy, that
this actor settles this version
([`SERVICE_ACTOR_SETTLEMENT_DESIGN.md`](SERVICE_ACTOR_SETTLEMENT_DESIGN.md)
section 2.3):

| Key | Field | Type and bound |
|---:|---|---|
| 1 | rail | exact `tos.service.service-actor.v1` |
| 2 | actor workchain | exactly `0` |
| 3 | actor account ID | 32-byte byte string |
| 4 | actor code hash | 32-byte byte string; equals a published Service Actor release |
| 5 | attestor key | text form `mldsa44:<64 lowercase hex key id>` |

Key 18 equals SHA-256 over the exact ASCII bytes of field 5. The attestor key is
pinned by the manifest (D5): rotating it requires a new Capability version
whose manifest names the new key, under the owner Agent's policy. A buyer or
resolver refuses an actor whose code hash, account, or snapshotted attestor key
differs from this map (design section 2.4).

## Frozen conformance evidence

Pending for the current root map. The frozen
[`software-work-manifest-v1.json`](../test-vectors/software-work-manifest-v1.json)
and its reproducer predate keys 20 (native TOS) and 21 and the refund value
above; they are not conformance evidence for this profile until regenerated
from the implementation with negative mutations for the new keys. The existing
vector is reproduced with:

```bash
python3 scripts/reproduce-software-work-manifest-v1.py
```

Implementations must reproduce the exact CBOR and digest and reject every
negative mutation before a manifest can be bound to a Capability version.
