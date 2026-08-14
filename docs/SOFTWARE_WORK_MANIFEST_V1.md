# Software-Work Manifest V1

## Status and authority

This document freezes the first ATOS commercial Capability profile. The
manifest is immutable, content-addressed off-chain data. Finalized typed TOS
state remains the authority for the Capability version and its manifest
digest; a gateway copy has no authority.

The media type is
`application/vnd.atos.software-work-manifest.v1+cbor`. Canonical bytes use RFC
8949 Core Deterministic Encoding, definite lengths, no floats, and the integer
field keys below. The digest is `sha256:<lowercase hex>` over those exact bytes.

The manifest MUST NOT contain `capability_id`. A Capability ID commits to the
manifest digest, so placing the resulting ID back inside the hashed manifest
would create a circular definition. The finalized Capability state supplies
that association.

## Canonical root map

| Key | JSON projection | Type and bound |
|---:|---|---|
| 1 | `protocol` | exact `atos.software-work-manifest.v1` |
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
| 18 | `execution_signer_authorization` | non-zero SHA-256 digest |
| 19 | `retention_seconds` | 3600 through 2592000 |
| 20 | `supported_assets` | sorted unique TOS asset identities, 1–8 |

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
`not-started-before-deadline`. Infrastructure, resource-limit, or digest
failures simply cannot produce a releasable Receipt; if no valid Receipt is
settled, the committed timeout returns the complete price. Normal tool failure
is a valid charged result only when the selected profile explicitly treats it
as success; this first profile requires exit code zero.

## Asset identity

Each asset map contains workchain (1), 32-byte lowercase hexadecimal master
account ID (2), master TVM code hash (3), wallet TVM code hash (4), and decimals
(5). V1 accepts only wc=0 stablecoins issued on the same TOS network. A ticker
is display metadata and cannot replace this identity. The Accepted Quote must
select one exact advertised identity and atomic amount.

## Frozen conformance evidence

[`software-work-manifest-v1.json`](../test-vectors/software-work-manifest-v1.json)
contains the positive vector and negative mutation corpus. Reproduce it without
the production Go implementation:

```bash
python3 scripts/reproduce-software-work-manifest-v1.py
```

Implementations must reproduce the exact CBOR and digest and reject every
negative mutation before a manifest can be bound to a Capability version.
