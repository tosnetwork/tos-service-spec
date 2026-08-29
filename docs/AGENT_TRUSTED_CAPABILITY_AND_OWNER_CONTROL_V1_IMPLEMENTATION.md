# Trusted Capability and Owner Control V1 Implementation Status

This document records implementation evidence without upgrading diagnostic
results into production, independent-operation, physical-device, or external
commerce claims. The normative design remains
[`AGENT_TRUSTED_CAPABILITY_AND_OWNER_CONTROL_V1.md`](AGENT_TRUSTED_CAPABILITY_AND_OWNER_CONTROL_V1.md).

## Implemented surfaces

| Repository | Implemented surface |
|---|---|
| `tos-service-spec` | A 38-kind machine registry, a generated recursive body-shape registry, exact full-field wrapper coverage for every kind, a versioned exact-target/repeat-ID profile for all 25 Owner Command kinds, executable semantic mutations for every released kind and command fixture, expanded Semantic Action registry/vectors, and a dependency-free Python verifier that reconstructs and compares the Go registry bytes and independently validates all 38 body semantics |
| `tos-service-protocol` | Integer-key deterministic CBOR, profile/object and body-schema registry binding, domain-separated identifiers, artifact pre-manifest identity, permission checks, detached Ed25519 authorization, predecessor/epoch checks, Admission, Promotion, invocation-bound Lease, Inventory, Use Binding, canonical acquisition CAS closure, signed ambiguous-action outcome evidence, per-command Owner Command profiles and projection/report types |
| `openfox` | Durable owner-local Inventory, fail-closed `UNVERIFIED_LEGACY` migration, quarantine/verification/admission/promotion/install/remove projections, externally assigned stable installation identity, policy-committed publisher-revocation source coverage, signed generator participation and controller-separated promotion, monotonic pause and revocation fencing, one-shot use admission, read API, strict request-file CLI coverage for signed bootstrap/session/policy and non-authority preparation steps, common-ledger adaptive drafting, exact local MCP entrypoint selection, compute-only hermetic local MCP execution, immutable MCP pipe arguments, sealed admitted-Skill execution for the bounded LLM runner, durable per-call MCP Action fencing, sink-bound signed ambiguous-outcome recovery, and a staged cryptographically authorized Owner Exit state machine with a common new-work fence |
| `tos-ai` | Sink-side capability-use Gate with fresh authority-head resolution, sink/lease/use-binding checks, epoch high-water and one-shot execution identity |
| `tos-messenger` | Typed Owner Command submission/resolution service and HTTP binding with exact parameter, lease and command-class binding, authorization-before-existence, stable Action deduplication, rollback-resistant journaling and a valid `prepared -> admitted -> applied/ambiguous` lifecycle |
| `tos-service-gateway` | Bounded, non-authoritative exact-object Carrier with source-local ordering, advisory search, explicit unverified provenance, and a mandatory external HTTPS generation/sequence/state-commitment authority whose pinned-key acknowledgement binds a fresh client challenge, exact request, signed generation lease, sequence, and commitment and rejects same-generation database restoration |
| `tos` | No change: this owner-local profile introduces no opcode or consensus state |

## Safety status

The implementation keeps consequential activation fail-closed unless exact
Admission, Promotion where required, installation identity, current policy,
revocation generations, control generation, Use Lease and execution binding all
match. Existing Skills are imported only as `UNVERIFIED_LEGACY`. Production
adaptive learning writes to quarantine and cannot directly replace a loaded
Skill.

Local MCP executable bytes are copied into a sealed Linux memory file after
installed-file identity verification and launched through the inherited sealed
descriptor, so a pathname replacement cannot change the admitted executable.
The currently released local profile is static-ELF-only and compute-only: it
rejects scripts, `PT_INTERP`, shared-library imports, and every executable that
would select a host interpreter, loader, library, module, or certificate store.
It also rejects ambient
environment, process, filesystem, network, credential, disclosure, upload,
destructive, data-class and extension authority; bubblewrap unshares every
supported namespace including network, mounts no OpenFox instance/workspace or
host `/usr`, `/bin`, loader, library, certificate, timezone, or language-runtime
tree, and exposes only private ephemeral home/tmp.
The Linux sandbox launcher is selected by the fixed administrator-owned
`/usr/bin/bwrap` path, opened without following links, required to be a
root-owned, single-link, non-group/world-writable regular file, and hashed from
the opened descriptor. Ambient `PATH` cannot select it. The measured launcher
and released namespace/mount profile are part of the runtime-and-sandbox
digest. The sealed admitted entrypoint is mounted with `--ro-bind-fd`; no
caller-writable pathname is reopened after verification. A future dynamic or
interpreted profile must use a separately admitted content-addressed immutable
rootfs and bind its complete closure digest.
The fixed runtime/environment/empty-broker digests are rechecked against the
Use Binding immediately before exec. MCP arguments are converted once into a
detached closed plain-JSON object; those same immutable bytes are authorized,
journaled and written to the pipe, so caller mutation and stateful marshalers
cannot substitute the request.
The signed Use Lease itself commits the admission, promotion, installation,
Inventory, and control-scope revisions consumed by the binding. Pause/resume
therefore invalidates every unused pre-transition lease; a caller cannot refresh
only the unsigned binding and replay the old authorization.
Non-Linux local MCP execution fails closed until an equivalent immutable
execution-handle backend is implemented. Consequential remote MCP is deliberately disabled until a released
authenticated, nonce- and generation-bound session profile exists. A lost
local MCP tool response is retained as an ambiguous outcome and is never
automatically replayed. Ambiguous MCP calls and capability executions can be
closed only by current-policy signed `ActionOutcomeEvidenceV1` from the one
exact sink authority and authority epoch frozen at action admission; the
evidence binds the original Action/request/execution and
survives restart, while forged, expired and cross-action evidence is rejected.
The OpenFox web backend mounts the typed Owner Command
service at `/api/owner-control/`; command parameters, the command-class set and
the signed command lease are digest-bound before admission. Every external
owner-control request also requires a channel binding derived by the server
only after dashboard-session authentication. The binding, audience and
evidence-read scope are never accepted from request headers; they are compared
with the enrolled device session and retained through ambiguous-action
recovery and final sink revalidation. Every external
control-authority request carries a fresh 256-bit challenge, and the signed
response must echo the challenge, exact request digest, and operation-specific
state acknowledgement. Installation writer-fence admission is also performed
by that pinned external authority over the exact canonical installation
transaction; a locally writable receipt directory is not installation
authority. The installation identity is resolved from that external authority
before a projection is created or reopened, so deleting local state cannot
select a fresh rollback namespace. Publisher status is accepted only from the
complete source/key set committed by the active capability policy; unknown,
missing, duplicate, rolled-back, or equivocating sources fail closed.
Every model tool, Web upload/download, CLI retrieval, adaptive model draft, and direct
quarantine-ledger reserve/commit phase now shares one exclusively locked,
crash-recoverable ledger and requires a challenge-bound acknowledgement from
the pinned external control authority. Reserve and commit intent are durable
before the authority acknowledgement, and the acknowledgement precedes
publication. The authority performs an idempotent Owner/Agent and
ledger-bound CAS over acquisition ID, provenance, source generation, quota,
expiry, exact content digest/size/file count and predecessor ledger revision.
The caller-controlled retrieval tree is copied through no-follow handles into
one bounded detached snapshot. Only those snapshot bytes are hashed, admitted,
and published at the content-addressed path. Commit returns a
`QuarantineCommitReceiptV1`; Inventory registration has no raw-path entry point
and reopens the receipt-bound ledger, replays its exact CAS, derives the path,
and rehashes the full closure. Reconciliation also rehashes every retained
object, rather than trusting stored byte/file counts. The ledger holds one root
directory descriptor for its lifetime and performs every operational pathname
through `/proc/self/fd`; its device/inode identity is persisted and included in
the receipt, preventing a same-UID rename-and-replace from separating the lock,
state, staged bytes, and published namespace.
Recovery replays only the same transition. Restored state cannot substitute
content or open a second ledger, and unknown acknowledged-looking objects are
never deleted without authoritative retention evidence. Owner
pause/exit advances the control high-water and external acquisition state in
one authority transaction; an available but disconnected authority cannot
continue admitting new IDs. Consequently, owner exit fences network acquisition
and durable quarantine retention even when a caller bypasses the main Store.
The common Store new-work fence also rejects verification, admission,
promotion, installation, registration, and adaptive materialization while the
Owner scope is paused or exiting; only exact action resolution and explicitly
authorized bounded drain behavior remain possible.
High-risk commands require both the authenticated
device role and an independent-owner-authority role whose policy-bound
controlling principal differs from the device controller; two keys owned by
one controller do not form quorum. The concrete local
sink currently implements owner pause/resume and predecessor-bound Owner Exit
stages for fencing, authority revocation, ambiguous-action retention, custody
disposition, evidence export, and irreversible tombstoning; it also implements capability activation,
suspend/resume/revocation/removal, promotion revocation, and device-session revocation. Other
released command kinds reject rather than falling through to an untyped path.
The `openfox capability` command exposes signed bootstrap, policy rotation,
device-session issuance, quarantine, verification, signed admission,
independently evidenced promotion, signed fenced installation, and
deterministic confirmation rendering. Activation, suspension, resumption,
revocation, removal, session revocation, pause/resume, and owner exit exist
only behind `/api/owner-control/` as profile-qualified Owner Commands; there is
no unsigned scalar CLI or exported raw Store mutator for those transitions.
Portfolio revision starts at genesis and has no unsigned public increment
method; subsequent portfolio authority must arrive through its signed,
predecessor-bound economic authority journal.
Neither interface reinterprets chat or model prose as lifecycle authority.
Messenger replacement-device recovery accepts a fresh authenticated attempt
for an already-existing exact ambiguous Action even after the immutable effect
window expires; it never re-admits an expired effect as a new Action.
The same stable sink identity may reconcile that retained Action after a
monotonic cluster-epoch failover through the shared journal fence; new commands
still require the exact current epoch.
The released local FileJournal is explicitly single-host: its exclusive writer
lock prevents replacement startup until the predecessor closes, and closing
irreversibly invalidates every method on the superseded journal object. A
future multi-host journal must prove current epoch-lease possession and rotate
its recovery fence; the local journal cannot be used as such an implementation.
Consequential local MCP is one-shot at the effect layer: the signed Use Lease
closure commits the exact tool, canonical request digest, and independently
derived `executor.effect` Action ID. The manager no longer allocates random
effect identities, and any argument or Action substitution fails before the
pipe write. The execution sink derives the exact canonical use-binding request
digest before its slot compare-and-swap. A pre-existing execution ID is
idempotent only if its Action ID, exact request digest, and started state all
match; a different request is a terminal conflict.

Registry retrieval uses dial-time post-resolution address checks, exact-origin
redirect policy and HTTPS outside an explicitly configured loopback development
endpoint. The development exception accepts literal loopback IP addresses only,
not hostnames such as `localhost`; registry retrieval rejects proxy use until an
authenticated proxy profile is released. Credentialed registry requests never
redirect. Control and Carrier
epoch authority clients reject every redirect. Direct workspace copy/install,
uninstall and adaptive-draft materialization paths are disabled or routed
through trusted quarantine; they cannot bypass Admission/Promotion.

The Carrier HTTP listener defaults to a literal loopback address and rejects a
non-loopback bind. Public exposure therefore requires an explicitly configured
TLS terminator or authenticated service mesh in front of the loopback listener;
the implementation does not advertise plaintext multi-host deployment.

Source presence and local tests do not pass Gate S or Gate M. In particular,
the mobile repositories and physical-device evidence required by Gate M are not
present in this workspace. Public-network, independent-operator and external
profit claims remain forbidden until their normative evidence gates pass.

## Reproduction

Run `scripts/verify-trusted-capability-v1.sh` from any directory. The script
checks schema/registry equality, independently reconstructed registry bytes,
63 exact-byte vectors and 255 executable negative mutations. Repository test
suites separately check the Go implementation; a script result alone is not a
production or independent-implementation claim.
