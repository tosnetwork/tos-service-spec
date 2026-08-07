# ATOS Artifacts v0.2

## Purpose

A capability that accepts or produces binary content (documents, images, audio, datasets) needs a way to move that content without embedding bytes in MCP/A2A/REST calls.

This document defines the Artifact object and signed-URL transfer flow referenced by `docs/MCP.md` and `docs/API.md`.

## Principle

**MCP/A2A/REST calls carry references, never bulk bytes.**

Uploads/downloads use direct signed HTTP URLs between the client and the configured storage backend. ATOS mediates authorization and references, not the bulk payload path.

This rule applies to all trust modes:

```text
managed
verified
native
```

Selecting Verified/Native does **not** mean uploading the raw artifact to TOS Network.

For stronger modes, the Execution Receipt may commit the artifact's content hash/commitment so the delivered bytes can be independently checked against the receipt/proof.

## Artifact Object

```json
{
  "artifact_id": "art_...",
  "owner_principal_id": "prn_...",
  "content_type": "application/pdf",
  "size_bytes": 2140233,
  "sha256": "sha256:...",
  "status": "available",
  "created_at": "2026-08-07T05:00:00Z",
  "expires_at": "2026-08-14T05:00:00Z"
}
```

The `sha256` field is a content commitment candidate, not proof that it was actually included in a TOS-backed receipt. Proof inclusion is represented by the Job/Receipt proof fields.

## Artifact IDs and Federation

`artifact_id` may remain gateway-local for Managed/Verified storage delivery unless a protocol flow explicitly requires global portability.

Native Capability identity MUST be globally resolvable, but this does not imply every temporary artifact ID must be a global protocol identifier.

Portable artifacts SHOULD be addressable by stable content commitment and an authorized retrieval mechanism rather than assuming an `atos.im` signed URL is permanently valid.

## Status

```text
uploading -> available
uploading -> expired
available -> expired
```

`expired` artifacts return `410 Gone` / equivalent not-found/expired semantics on download.

ATOS does not guarantee indefinite retention. Capabilities that need an artifact past its retention window must copy it into permitted provider/customer storage during execution.

## Upload Flow

`atos_create_upload`/`atos_complete_upload` below are MCP shorthand for
`atos_artifact` called with `operation: "create_upload"` /
`operation: "complete_upload"` — see `docs/MCP.md` § 6.11 for why the
three-step flow is one tool, not three. The REST paths are the
equivalent, unconsolidated surface for non-MCP clients.

```text
atos_artifact(operation: create_upload) (or POST /v1/uploads)
      |
      v
client PUTs bytes directly to upload_url
      |
      v
atos_artifact(operation: complete_upload) (or POST /v1/uploads/{id}/complete)
      |
      v
artifact_id + sha256 usable in capability input
```

`create_upload` MUST bound `size_bytes` before issuing a signed URL.

`complete_upload` SHOULD verify or calculate the final content commitment and return it with the stable Artifact reference.

## Download Flow

```text
atos_artifact(operation: get_download_url) (or GET /v1/artifacts/{id}/download-url)
      |
      v
client GETs bytes directly from download_url
```

A signed URL is an ephemeral transport credential. It MUST NOT be embedded into an on-chain commitment or long-lived Execution Receipt.

Use `artifact_id` and/or content commitment in durable records instead.

## Ownership and Access

- An uploaded Artifact is visible only to authorized principals and the execution pipeline for Jobs that legitimately reference it.
- A provider does not receive standing access to all client artifacts.
- Providers receive permitted input content through the execution pipeline, not a general artifact-read API.
- Job-output downloads require authorization equivalent to `atos_get_job` ownership/access policy.
- Signed URL expiry does not change the cryptographic content commitment already recorded in a receipt.

## Trust-Mode Behavior

### Managed

The gateway may store Artifact metadata and bytes through its managed storage service. Receipt inclusion of artifact commitments is optional but recommended.

### Verified

Bytes remain off-chain. When an Artifact materially represents the input/output being paid for, the selected proof profile SHOULD require the relevant content commitment in the signed Execution Receipt.

Conceptually:

```text
artifact bytes -> object storage
       |
       +-> sha256/content commitment -> Execution Receipt -> tos-core/TOS proof
```

### Native

The same commitment rule applies, but retrieval MUST NOT assume `atos.im` is the only possible long-term transport/storage authority when portability is required.

Native implementations may use provider/customer storage, content-addressed storage, decentralized storage, or another authorized mechanism. The storage backend itself is outside the ATOS core protocol.

## Receipt Commitment Example

```json
{
  "receipt_id":"rcpt_...",
  "trust_mode":"verified",
  "output_commitment":"sha256:...",
  "artifacts":[
    {
      "artifact_id":"art_...",
      "content_commitment":"sha256:..."
    }
  ],
  "network_proof_ref":"tos:..."
}
```

A verifier can hash the downloaded bytes and compare them with the committed value without placing the bytes themselves on-chain.

## What This Document Does Not Define

- the storage backend (S3-compatible, GCS, decentralized storage, customer storage, etc.);
- virus/content scanning;
- content moderation policy;
- retention policy specifics;
- multipart/chunked upload details;
- encryption/key-management policy;
- whether a particular Artifact commitment is mandatory for a Capability — that is determined by the Quote/proof profile and capability contract.

## Artifact Invariants

1. Bulk bytes do not travel through MCP/A2A business calls.
2. Bulk bytes are not placed on TOS merely because trust mode is Verified/Native.
3. Durable proofs use content commitments, not signed URLs.
4. A signed URL is temporary transport authorization, not a protocol identity.
5. Quote/proof profile determines whether an Artifact commitment is required in the Receipt.
