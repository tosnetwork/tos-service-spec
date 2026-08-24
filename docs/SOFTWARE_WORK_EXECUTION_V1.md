# Software-Work Execution and Artifact Delivery V1

## Scope and authority

This document freezes the provider-local execution boundary used by the first
software-work profile. It does not create a second protocol authority. Before
this boundary is exposed publicly, the caller must prove from finalized TOS
state that the Capability version, Accepted Quote, funded escrow, manifest,
endpoint, and execution signer are the committed objects. A gateway assertion
alone is insufficient.

This boundary consumes one already-verified manifest and one bound job. The
initial public transport mapping is frozen in
`EXTERNAL_AGENT_TASK_TRANSPORT_ADAPTER_V1.md`; it carries
these same commitments and cannot weaken this execution boundary.

## Bound job

A V1 job contains only:

- the non-zero Accepted Quote commitment in exact
  `tvm-cell-sha256:<64 lowercase hex>` form;
- a non-zero 256-bit execution ID;
- the non-zero canonical input digest;
- a non-zero SHA-256 source-archive digest; and
- the exact source archive bytes.

Before a job enters this boundary, `NATIVE_EXECUTION_GATE_V1.md` also requires
the transport to supply the exact escrow address and atomically binds the paid
purchase to this job. The escrow address is chain-location input to the Gate,
not a runner-selected execution parameter.

The provider configuration, not the request, supplies the manifest digest,
toolchain image digest, sandbox-policy digest, executable, arguments, working
directory, Unix identity, and resource ceilings. The source digest is checked
before an execution lease is acquired. Remote callers cannot supply an image,
command, environment, host mount, network exception, user ID, or limit.

V1 defines `sandbox_digest` as exactly the canonical manifest digest. The
manifest already commits the invocation, network policy, resource ceilings,
artifact types, success rule, endpoint, signer authorization, and asset route;
allowing a separate provider-chosen sandbox identifier would create an
uncommitted settlement input. A runner must reject any configuration where
these two digests differ.

The initial source media type is uncompressed POSIX tar. Entries are limited to
regular files and directories. Absolute paths, `..`, non-canonical names,
duplicate paths, symlinks, hard links, devices, FIFOs, sparse expansion, too
many entries, and total extracted bytes above the committed scratch limit are
rejected. The runtime selects a private host directory, extracts there, removes
write permission while retaining container readability, and mounts it read-only and `noexec` at
`/workspace/source`. The request never names a host path.

## Isolation mapping

The frozen manifest maps exactly to the existing `tos-ai` policy executor:

- the toolchain digest is a SHA-256-pinned, operator-allowlisted OCI image;
- the invocation is executed directly, without a shell;
- the working directory is `/workspace/source` or a canonical descendant;
- the root filesystem and source mount are read-only;
- the process is non-root, has no capabilities, cannot gain privileges, and
  cannot access the container-runtime socket;
- a private network namespace with no allowed hosts implements `network=none`;
- cgroup and runtime limits bound CPU, memory, PIDs, wall time, writable
  scratch, and combined stdout/stderr; and
- cancellation synchronously stops and removes the task, container, snapshot,
  workspace, and FIFOs before returning.

The writable `/workspace` tmpfs is owned by the fixed non-root execution user.
The source is mounted over `/workspace/source`; compiler cache uses
`/workspace/go-cache`, while temporary compiler files and executables use the
existing `/workspace` root. The fixed `GOMAXPROCS=2` setting prevents the host
CPU count from exhausting the committed PID ceiling. There is no unsafe host-process fallback:
if the configured containerd isolation boundary is unavailable, execution
fails closed.

## At-most-once execution

Immediately before any first transition that can start the container, the
runner verifies a fresh start-preflight receipt from the shared Native Execution
Gate over the same `(quote_commitment, escrow_address)` claim and execution
fingerprint. For a paid-demand successor, that receipt binds the exact effective
duration, preflight-to-start bound, execution/refund deadlines, release-pipeline
margin, complete fresh escrow/Quote/Registry/Agent/Capability authority
snapshot, coherent fresh monotonic checkpoints, exact code identities,
current-quorum finalized anchor identity/time/sequence and proof digest,
max-age/head-lag results, and conservative time upper bound. The Gate must have
repeated the complete authority check through that anchor, not only funding
resolution or a monotonic old checkpoint. This final fresh preflight is the linearization point
for one bounded start-authority ticket. A change finalized at or before its
checkpoint rejects; one finalized only afterward is non-retroactive until the
checked `start_not_after`. Original Gate admission freezes no authority. The
runner rejects an expired ticket; the caller must refresh the same claim and
repeat all checks, never create a second admission. A durable Gate claim without
a fresh first-start receipt is insufficient.

Before the container can start, the provider atomically creates and durably
syncs a journal record keyed by execution ID. Its stable execution fingerprint
binds the manifest, Quote, execution, input, source, Gate claim, and committed
timing policy, but not the timestamp-specific start-preflight receipt. The
journal separately retains every preflight attempt and its resolution.

The local start states are `prepared`, `starting`, `running`, and `completed`.
Only `prepared`, which is durably proven to have caused no runtime side effect,
may replace an expired preflight with a fresh receipt for the same Gate claim
and stable execution fingerprint. Immediately before calling any runtime API
that could start work, one atomic durable transition binds the current
preflight and changes `prepared -> starting`. The actual process start must
remain inside that preflight's bound.

- A different stable execution fingerprint under the same execution ID is a
  conflict.
- A completed matching record returns the immutable prior outcome without
  executing again.
- A matching `starting` or `running` record after a crash is ambiguous and is
  never retried automatically.
- Refresh never changes the execution ID, Gate claim, stable fingerprint, or
  prior append-only preflight history.

This intentionally chooses safety over automatic availability. The runtime
interface cannot prove that a connection failure happened before execution, so
replaying an ambiguous job could perform paid or externally visible work twice.
Any future recovery protocol must add independently verifiable execution
attestation; it must not infer safety from a process restart.

## Reports and artifacts

Successful V1 execution requires exit code zero. The result digest is SHA-256
over the exact bounded combined output. The canonical report media type is:

```text
application/vnd.tos.service.test-report.v1+json
```

The report contains schema identifier, execution ID, result digest, exit code,
bounded resource usage, and completion time. The artifact media type is:

```text
application/vnd.tos.service.software-artifact.v1+tar
```

It is a deterministic USTAR archive, in this exact order:

1. `output.log`, mode `0444`, timestamp zero;
2. `report.json`, mode `0444`, timestamp zero.

UID, GID, owner names, extended attributes, and host paths are absent. The
artifact and report digests are SHA-256 over their exact delivered bytes.

## Content-addressed storage

Objects are written to an owner-private store through a bounded temporary file,
synced, changed to mode `0400`, and atomically linked under the lowercase
SHA-256 digest. A duplicate digest is accepted only after the existing bytes
are reverified. Retrieval accepts only the exact digest grammar, rejects links
and non-regular or over-bound files, detects replacement between metadata and
open, rereads the bounded object, and recomputes its digest before delivery.

Media type and size are returned as immutable outcome descriptors. Bulk bytes
remain off-chain. A Receipt commits to the result, artifact, report, source,
toolchain, and sandbox digests; the artifact store is never a settlement or
consensus authority.

## Acceptance evidence

Unit and race tests must cover exact manifest-to-runtime mapping, traversal and
link rejection, read-only source mounting, network isolation configuration,
output and storage bounds, tamper detection, idempotent object insertion,
completed replay, conflicting execution identity, and crash/restart ambiguity.
A deadline matrix must additionally cover a stale/mismatched start-preflight,
queue delay within and beyond the committed bound, crash before first process
start while still `prepared`, atomic `prepared -> starting` binding, same-claim
preflight refresh, escrow/Agent/Capability/code-identity change and checkpoint
regression/fork between admission and each preflight, an adverse change
finalized at/before versus only after the final checkpoint, start inside versus
after `start_not_after`, stale/excess-age/head-lag anchor, endpoint disagreement,
missing cross-shard proof, crash in `starting`, and refusal to turn refresh into
a second execution identity or to replace a preflight after a possible runtime
side effect.
A production provider additionally requires the existing live containerd
conformance suite against the exact pinned toolchain image. Unit tests alone do
not attest host or runtime isolation.
