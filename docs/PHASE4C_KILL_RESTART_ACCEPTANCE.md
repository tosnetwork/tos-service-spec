# Phase 4C proof checkpoint kill/restart acceptance

Status: passed locally on 2026-08-12.

This acceptance exercises the production HTTP/RPC/store boundaries. It is not
a mock-only service test and it does not treat a local projection as canonical
TOS state.

## Topology

- one real three-validator TOS localnet, observed through the configured quorum;
- one persistent TaskEscrow publisher process and enrolled bbolt journal;
- two independently constructed `tos-protocol` processes, with separate bbolt
  files and process-local caches, sharing only canonical TOS state;
- two independently constructed ATOS API processes, with separate auth state
  and protocol clients, sharing a fresh PostgreSQL 16 database;
- the production REST authentication/middleware path;
- the standalone `tos-verified-proof` verifier using read-only protocol RPC.

The transaction under fault injection was a real Verified dispute-resolution
outcome. Provider-settlement and requester-release terminal packages were also
present in the same fresh database and had previously returned `VALID` through
the same independent verifier.

## Matrix and assertions

| Boundary or failure | Durable state at interruption | Recovery assertion |
|---|---|---|
| after `intent_persisted`, before canonical observation | `intent_persisted`, no package bytes | restart re-observed every authority and completed without mutation |
| after canonical observation, before projection | `canonical_observed` with frozen bytes/digest | `SIGKILL` rollback preserved that row; a different ATOS replica completed with the identical digest |
| after projection, before terminal checkpoint | `projection_persisted` with frozen bytes/digest | restart completed with identical bytes/digest |
| after `completed`, before response delivery | `completed` | deliberately dropped client response; exact retry returned the durable digest |
| completed cache while protocol is down | `completed` | REST returned retryable `network_unavailable`; it did not return cached proof as valid |
| protocol restart after the preceding failure | `completed` | live re-observation succeeded and returned the original digest |
| PostgreSQL process outage | `completed` | request failed retryably; database restart returned the original digest |
| two ATOS and two protocol replicas racing | one shared operation | both HTTP responses were 200 and byte-identical; PostgreSQL contained exactly one completed row |
| proof replay versus publisher journal | unchanged journal | publisher bbolt SHA-256 and mtime were unchanged; verification performed no economic mutation |

The kill boundaries used a PostgreSQL `BEFORE UPDATE` fault trigger that paused
the target transition. The API process was then terminated with `SIGKILL`.
Because each prior checkpoint is committed separately, inspection from an
independent PostgreSQL connection proved which boundary survived. The trigger
was removed before takeover.

During the matrix, advancing live finality initially caused replay to derive a
new package digest. That was a real defect: a completed proof must be immutable
even though later observations have higher checkpoints. ATOS now freezes the
first canonical bytes, revalidates their full tuple against live references at
equal-or-higher checkpoints, and resumes only the remaining local checkpoints.
A second race exposed a stale-worker `store: conflict` after another worker had
already completed the operation. Checkpoint writers now converge on an equal or
newer durable state instead of reporting the successful operation as failed.

The final independent verifier result was:

```text
VALID
version: tos_verified_v1
network: tos-localnet
outcome: dispute_resolution
package digest: sha256:af3eac17c5e89468181b5a685c33d402fb19f959f72079031271bff582a1dd44
```

Finality checkpoints in that package were nonzero and independently observed.
The exact numeric checkpoints are not normative because the localnet continued
to finalize blocks during the matrix.

## Genuinely empty protocol-replica acceptance

The final remaining local gate was rerun after upgrading identity and
principal-binding anchors to the deterministic v2 tuples documented in
`TOS_RPC.md`. A third production `tos-atos-rpc` process was started with a new
bbolt file and **without** `-identity-seed-file`. It shared no process cache or
local protocol projection with the producer. The standalone verifier resolved
every identity, binding, ownership, Quote, escrow and release reference through
the three-validator canonical authority and returned:

```text
VALID
package_id: proof_a9f21f0f999adfa85a6a39064ba919f5
package_digest: sha256:a9f21f0f999adfa85a6a39064ba919f5fbd940ea0cfa3fab7ad9dd19266e3818
quote_id: q_c8d484fc-a025-4f97-94dc-f33d9aefa6d0
job_id: job_f8d6ebd5-d0b6-49d6-b1ce-e775bb0d6a19
escrow_id: esc_f1de0cd4a8705256096f8669bc7a9930
outcome: requester_release
```

The empty replica was stopped and reconstructed against the same still-empty
local projection, then returned `VALID` again with the identical package
digest. No identity seed, database copy, publisher mutation or cached finality
result was used. This closes the genuine empty-replica recovery item; loss of
the live authority still remains a fail-closed `AUTHORITY_UNAVAILABLE` result.

The renewed current-state matrix then committed and revoked isolated signer
authorization and principal-binding tuples on the same real three-validator
chain. A newly constructed empty-bbolt replica independently derived the exact
revocation transaction `utime`. It rejected signer use at and after that time,
accepted execution strictly before it, and reported the historical principal
binding as revoked rather than synthesizing `ACTIVE`. This proves that an old
anchor's existence is not confused with current authorization.

After the permanent-tombstone rule was added, a newly built protocol process
with another fresh bbolt file was connected to the same three-validator chain.
It attempted to recreate the already revoked real tuple
`(phase4c-revoked-principal-20260813, requester-localnet)`. The production
ConnectRPC path returned HTTP 409 with `BINDING_TUPLE_REVOKED` before Commit;
the in-process lifecycle matrix additionally proves both direct A→revoke→A
and A→revoke→B→revoke→A reuse are rejected.

Finally, two separately configured ATOS OS processes used the shared fresh
PostgreSQL database, separate authentication state, and independent protocol
connections; one protocol connection used the empty-bbolt replica. Real REST
GET and POST proof-package calls returned HTTP 200 from both processes with the
same package ID, digest and 9,028-byte canonical CBOR. Both ATOS processes and
the empty protocol process were terminated and reconstructed before replay.
PostgreSQL retained exactly one `completed` proof operation, and the standalone
CLI returned `VALID` after protocol restart. No proof-generation path invoked a
publisher or economic mutation.

## Scope boundary

This closes the Phase 4C local real-process checkpoint gate. It does not claim
production validator diversity, production quorum operations, or HSM/Vault
deployment. Those remain Phase 4D gates.
