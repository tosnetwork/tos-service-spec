# ATOS Artifacts

## Purpose

A capability that accepts or produces binary content (documents, images,
audio, datasets) needs a way to move that content that isn't "base64 it
into a JSON-RPC tool call." This document defines the Artifact object and
the signed-URL transfer flow referenced by `docs/MCP.md`'s optional file
transfer tools and `docs/API.md`'s upload/artifact endpoints.

## Principle

**MCP/A2A/REST tool calls carry references, never bytes.** Every upload
and download happens over a direct signed HTTP URL between the client and
object storage; ATOS mediates by issuing and verifying those URLs, not by
proxying the payload through its own request handlers. This keeps large
files off the same request path that quote/invoke/job latency budgets are
built around, and keeps ATOS itself stateless with respect to file
content.

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

### Status

```text
uploading -> available
uploading -> expired   (client never called complete-upload before upload_url expired)
available -> expired   (retention window elapsed)
```

`expired` artifacts return `410 Gone` / `not_found`-equivalent on
download — ATOS does not guarantee indefinite retention. Capabilities
that need an artifact past its retention window must copy it into their
own storage during execution, not treat ATOS as permanent storage.

## Upload Flow

```text
atos_create_upload (or POST /v1/uploads)
      |
      v
client PUTs bytes directly to upload_url
      |
      v
atos_complete_upload (or POST /v1/uploads/{id}/complete)
      |
      v
artifact_id usable in a job's `input`
```

`atos_create_upload` MUST bound `size_bytes` against a maximum (a
gateway-wide limit; per-capability limits are a `docs/CAPABILITIES.md`
concern, not this document's). Rejecting an oversized request before
issuing a signed URL is cheaper than discovering the limit after the
client has already uploaded the bytes.

## Download Flow

Any artifact referenced by a job's `output`/`artifacts` — or one the
caller uploaded — can be exchanged for a short-lived signed download URL:

```text
atos_get_download_url (or GET /v1/artifacts/{id}/download-url)
      |
      v
client GETs the file directly from download_url
```

## Ownership and Access

- An artifact is visible only to `owner_principal_id` and, for
  job-output artifacts, the job's `principal_id` — a provider does not
  get standing access to a client's uploaded input beyond the single job
  execution it was attached to.
- `atos_get_download_url` for a job's output artifact requires the
  caller to be that job's owning principal, mirroring `atos_get_job`'s
  ownership check.
- Providers receive artifact content only through the execution pipeline
  (tos-ai resolves `input.<field>.artifact_id` into actual bytes before
  invoking the provider), never through a general artifact-read API.

## What This Document Does Not Define

- The storage backend (S3-compatible bucket, GCS, etc.) — an
  implementation detail behind `atos_create_upload`/`atos_get_download_url`,
  not a public contract.
- Virus/content scanning, size limits per content type, or retention
  policy specifics — operational policy, not protocol.
- Streaming/chunked upload for very large files — Phase 1 assumes a
  single PUT is sufficient; multipart upload is a straightforward
  extension of `atos_create_upload` (return multiple part URLs) if a
  real use case needs it later, not a redesign.
