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

## Scope boundary

This closes the Phase 4C local real-process checkpoint gate. It does not claim
production validator diversity, production quorum operations, or HSM/Vault
deployment. Those remain Phase 4D gates.
