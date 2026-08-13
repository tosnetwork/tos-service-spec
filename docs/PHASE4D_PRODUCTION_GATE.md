# Phase 4D Production Gate

Status: normative contract frozen; implementation and local acceptance are
complete. A production deployment is admitted only when its own current,
signed evidence passes the gate.

## 1. Scope

Phase 4D does not add another economic state machine. It admits or rejects one
deployment of the Phase 4A–4C Verified path. The gate is read-only and MUST
have no publisher, escrow mutation, settlement mutation or Managed-ledger
fallback dependency.

The acceptance transaction is:

```text
external client -> Verified Quote -> finalized TaskEscrow reservation
 -> execution -> authorized Receipt -> finalized settlement/release/dispute
 -> portable proof -> independent live verifier -> VALID
```

## 2. Machine gate

`tos-phase4d-gate` consumes a strict JSON manifest with version
`tos_phase4d_production_gate_v1`. Unknown fields, trailing values, symlinks,
relative paths and group/world-writable manifests are rejected.

The manifest binds:

- at least two independently addressable ATOS replicas;
- at least two independently addressable `tos-protocol` replicas;
- at least three TOS observation endpoints, a strict-majority quorum, and a
  distinct operator identity for every endpoint;
- the TOS network and gateway trust domain;
- reviewed Agent/service and TaskEscrow TVM cell SHA-256 allowlists;
- purpose-separated Quote, Receipt, TaskEscrow and chain-action keys;
- monitoring signals;
- reconciliation, backup, restore and incident-drill evidence;
- one completed canonical `tos_verified_v1` proof package.

Remote health and monitoring URLs MUST use HTTPS. Plain HTTP is accepted only
for an explicit loopback local-acceptance run. Redirects are rejected.

## 3. Readiness

ATOS exposes:

- `GET /livez`: process liveness only;
- `GET /readyz`: live PostgreSQL and `tos-protocol` dependency readiness.

`tos-protocol` exposes:

- `GET /livez`: process liveness only;
- `GET /readyz` and backwards-compatible `GET /healthz`: live authority,
  economic-driver and configured Worker readiness.

A load balancer MUST send new work only to `/readyz`-healthy replicas. A
dependency outage MUST NOT be hidden by liveness.

## 4. Production key custody

Each required purpose declares `backend` as exactly `hsm`, `kms` or `vault`, a
non-empty key identity and an HTTPS health URL. The URL MUST return exactly one
bounded JSON value:

```json
{
  "version": "tos_phase4d_custody_health_v1",
  "purpose": "receipt",
  "backend": "hsm",
  "key_id": "production-receipt-key-2026-01",
  "healthy": true
}
```

The response must match the manifest tuple exactly. File/software custody
cannot pass the production gate.

## 5. Signed operator evidence

Every custody ceremony, reconciliation report, backup, restore drill and
incident drill is a non-empty, read-only regular file with a pinned SHA-256,
completion time and bounded maximum age. It also carries an Ed25519 signer
identity, a context-specific subject (for example
`custody:receipt:hsm:production-receipt-key-2026-01`), public key and signature
over:

```text
"TOS-PHASE4D-EVIDENCE-V1" || NUL
|| subject || NUL
|| sha256 || NUL
|| completed_unix_decimal || NUL
|| maximum_age_seconds_decimal || NUL
|| signer_id
```

The production trust process controls which evidence signer public key is
placed in the root-owned manifest. A stale, future-dated, writable, replaced,
unsigned or incorrectly signed artifact fails closed.

## 6. Monitoring and proof verification

The monitoring endpoint uses Prometheus text format. Every required signal has
an explicit minimum and/or maximum. Signals are matched as exact unlabelled
metric names, not comments, substrings or ambiguous multi-series label sets;
duplicate samples, NaN and infinity fail closed. Operators MUST include
readiness, reconciliation error/lag, proof reconciliation lag,
publisher/journal failure, quorum/finality lag and settlement failure signals
appropriate to the deployment.

The gate pins the proof file digest, requires its TaskEscrow code hash to occur
in the reviewed deployment allowlist, then runs the normal independent
verifier with explicit network/domain pins and live read-only protocol
observation. Only `VALID` passes.

## 7. Failure rule

Any missing dependency, non-majority observation, identity/ownership/signer
failure, code-hash mismatch, escrow/Receipt/settlement mismatch, unavailable
monitoring signal, stale evidence, backup/restore failure or invalid proof
causes a non-zero gate result. The gate never retries an economic mutation and
never converts a Verified Quote to Managed.

## 8. Completion boundary

Repository implementation is complete when the gate, readiness behavior,
strict parsing and all adversarial tests pass. A specific production rollout
is certified only by running the gate against that rollout's real HTTPS
replicas, independent validator endpoints, real HSM/KMS/Vault identities and
current signed operational evidence. Local test fixtures cannot be relabeled
as production evidence.
