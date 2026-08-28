# Agent Operation and Outcome Event V1 Implementation Report

**Status:** coordinated implementation candidate

**Normative design:**
[Agent Operation and Outcome Event V1](AGENT_OPERATION_OUTCOME_EVENT_V1.md)

This report records what is implemented, which repository owns each boundary,
how an operator enables it, and which claims remain gated by deployment
evidence. It does not turn a local test into evidence of independent operation,
market completeness, economic profit, or chain consensus.

## 1. Delivered capability

The implementation records positive, negative, partial, ambiguous, and failed
operations as immutable signed Agent Operations. It preserves the Action that
caused the observation, the exact sink resolution, qualified evidence, privacy
policy, causal predecessor set, and append authority. OpenFox can rebuild local
projections and learning cuts from the retained stream without treating a
Carrier, model, report, or local database as global truth.

The implemented path is:

```text
side-effect sink resolution
-> OutcomeRecordingAuthority
-> profile-qualified assertion
-> signed AgentOperationEnvelopeV1
-> authority-fenced append admission
-> durable OpenFox journal and checkpoint
-> local projection / bounded learning cut
-> optional one-recipient private send
-> optional explicitly declassified Carrier publication
```

Recording an outcome grants no permission to repeat the underlying side
effect. Append, private send, and public publish each use their own stable
`SemanticActionIdentityV1`, exact request digest, current Writer Fence, and
query-before-retry resolution.

## 2. Repository implementation matrix

| Repository | Implemented responsibility | Important boundary |
|---|---|---|
| `tos-service-spec` | Complete JSON Schema, profile registry, stable-error registry, Semantic Action entries, canonical fixture corpus, and an independent Python verifier | Specification artifacts contain no operational history and define no global head |
| `tos-service-protocol` | Bounded event, evidence, authority, transport, privacy, economics, reporting, learning, Merkle/cohort, codec, digest, signature, and verifier APIs | Structural verification performs no network retrieval; issuer qualification is explicit |
| `openfox` | Authority-side append high-water, durable journal, recovery, archive, signed checkpoint, local projection, learning cut, automatic Action-resolution capture, private send, directory Carrier, and HTTP Carrier client | Local projection is derived; public publication is a separate default-off declassification capability |
| `tos-messenger` | Typed `operation.outcome` payload and local transport admission isolated from ordinary chat/model delivery | Exactly one recipient per Action; a chat message cannot become outcome authority |
| `tos-service-gateway` | Authenticated bounded HTTP admission, retrieval, search, subscription, action resolution, signed Carrier receipts, quotas, and database-loss rebuild path | Carrier fields are recomputed from exact retained bytes; Carrier acknowledgement is not business truth |
| `tos-ai` | Exact execution-Gate evidence and physical resource-meter evidence | Execution success does not imply acceptance, payment, profit, or monetary cost |
| `tos` | No change | V1 needs no new opcode, contract, or consensus state; existing finalized evidence remains authoritative |

The Gateway HTTP Carrier and OpenFox directory Carrier are separate code
implementations. They are not evidence of separate operators until deployed
with independent storage, identities, administration, and upstream failure
domains.

## 3. Frozen protocol surface

### 3.1 Core and evidence

The protocol implementation includes:

- bounded `OperationOutcomeEventBodyV1`, artifact bundle, evidence manifest,
  audience policy, predecessor and extension sets;
- canonical operation, content, scope, envelope, request, receipt, checkpoint,
  cohort and projection digests;
- Agent-operation signature verification against an explicit historical
  authority resolver;
- pinned authority-time and issuer-qualification profiles for authenticated
  deployments;
- profile validators for action resolution, execution/Gate, Carrier,
  settlement, obligation, state, availability, economics, report, and learning
  assertions;
- exact Merkle set and membership proofs for complete cohort cuts;
- AES-256-GCM evidence envelopes using a fresh random 96-bit nonce and an
  authenticated context that binds the schema, cipher suite, key-reference
  digest, object digest, audience, retention policy, evidence role, and
  canonical plaintext size;
- hiding commitments and purpose/audience-bound disclosure projections; and
- bounded report, learning dataset, and Skill-promotion objects that cannot
  enlarge authority.

Unknown required profiles, duplicate or unsorted set members, non-canonical
digests, wrong authority, invalid time, cardinality violations, oversized
objects, signature mutations, and incomplete evidence fail closed.

### 3.2 Stable side-effect identity

The versioned Semantic Action registry contains:

- `operation.journal.append`;
- `operation.publish`; and
- `operation.private-send`.

Every entry defines required and forbidden semantic fields, a domain-separated
preimage, stable Action ID, exact request digest, retry behavior, and mutation
vectors. Private send contains exactly one recipient. Group delivery is a set
of separately authorized and recoverable Actions so partial fan-out cannot be
hidden behind one terminal result.

### 3.3 Stable errors

The generated error registry distinguishes malformed input, unsupported
profiles, unauthorized issuers, stale writers, exact replay, semantic conflict,
resource exhaustion, evidence unavailability, and indeterminate authority.
HTTP failures expose a stable `X-TOS-Error-Code` while logs and responses omit
private evidence.

## 4. OpenFox durability and recovery

Each journal record retains:

- the exact source `AuthorizedActionV1` and `ActionResolutionV1` for automatic
  side-effect capture, bound to the digests and revision in the signed
  assertion;
- the exact signed Agent Operation and artifact bytes;
- event, content, envelope, predecessor and evidence digests;
- the exact append admission request;
- the exact `AuthorizedActionV1` and Writer Fence used for append; and
- a checksum chain over the immutable record.

The economic authority linearizes `(ordering domain, epoch, sequence)` before
the local append and stores a rollback-resistant high-water within its selected
authority store. A stale writer cannot reserve a later sequence. Commit,
replay, archive import, checkpoint generation and startup scan reverify the
operation signature, artifact bindings, append Action, fence, request, head,
gap set and checksum chain. A crash after append but before terminal Action
resolution recovers only the exact previously admitted Action.

Signed checkpoints and bounded archive export/import permit independent
retention. Import writes the complete archive as a durable recovery intent
before materializing records; startup completes the same validated archive
after a crash before head promotion and rejects conflicting retained bytes.
Journal validation streams the complete chain while retaining only the
requested bounded tail; exact Action/revision idempotency lookup scans the
whole validated history rather than a recent-window cache. A single V1 archive
is capped at 10,000 records and 64 MiB. Detecting rollback of an entire journal
directory still requires the operator to pin the
latest signed checkpoint outside that directory or use a separately protected
authority/storage service. The implementation never claims that a checksum
whose bytes and key are rolled back together detects that attack.

Negative terminal resolutions are captured even when the sink also returns an
error. This prevents a success-only dataset caused by dropping error paths.
Projection ingestion and reads deep-copy retained structures so caller-owned
buffers cannot rewrite local history.

## 5. Transport and Carrier operation

### 5.1 Private Messenger transport

`operation.outcome` is a typed payload. The Messenger validates the exact
private-send request and Action identity, applies its writer and recipient
boundary, persists resolution, and does not place the payload in ordinary chat
or model-input queues. The existing signed Messenger Event envelope supplies
the endpoint acceptance/delivery observation; it does not assert Agreement,
execution, payment, or global outcome truth. Timeout recovery queries the same
Action; a recipient or membership-epoch change creates a new semantic Action.

### 5.2 Public Carrier transport

OpenFox public Outcome publication requires all of the following:

1. the general publication Gate;
2. `earning.outcome.public_publication_enabled = true`;
3. a sorted owner-authored audience-policy digest allowlist;
4. a sorted owner-authored assertion-profile allowlist;
5. extension permission when extensions are present;
6. the current Writer Fence and exact `operation.publish` Action; and
7. for each HTTP Carrier, a pinned Ed25519 receipt public key in
   `outcome_receipt_public_key`.

The Gateway daemon prints its Outcome receipt public key during `--check` and
readiness startup so it can be transferred through an authenticated
configuration channel. OpenFox never trusts a key supplied by a publish
response. It verifies challenge and submission receipts, recomputes the event
body and all derived fields from exact retained request bytes, and checks
source-local sequence, timestamp and provenance.

The Gateway exposes bounded authenticated endpoints under:

```text
POST /v1/operations/admission-challenge
POST /v1/operations
GET  /v1/operations/{digest}
GET  /v1/operation-actions/{action}
GET  /v1/operations
GET  /v1/operations/subscribe
```

Search and subscription use source-local cursors and explicit limits. Corrupt
retained records, receipts, derived metadata or action references fail the
whole operation rather than disappearing from results. Rebuild after database
loss requires the exact authorized corpus and the same explicitly restored
Carrier identity key; deleting both cannot preserve identity continuity.

## 6. Execution evidence and monetary interpretation

The execution producer emits a manifest over the exact Agreement, plan,
inputs, Skill/model, sandbox, credentials, network policy, start ticket,
execution slot, runner and result. The resource meter records physical CPU
milliseconds, peak memory bytes, disk bytes and elapsed duration plus the meter
build digest.

Physical resource evidence is only a `cost_source`. OpenFox applies an
owner-authorized rate card, accounting policy and economic perimeter before it
can derive monetary cost. A declared ceiling is not realized cost, and
execution success is not customer acceptance or settlement.

## 7. Conformance corpus and verification

The generated corpus contains canonical objects, three Semantic Action
identities and negative mutations. The independent
`scripts/operation-outcome-reference.py` implementation contains its own
canonical CBOR encoder, digest construction and RFC 8032 Ed25519 verifier; it
does not call the Go protocol implementation. It verifies both the Agent
Operation and Carrier receipt signatures and rejects signature mutation.

The implementation was exercised with:

```text
python3 scripts/operation-outcome-reference.py
go test ./...
go vet ./...
go test -race <security-relevant packages>
GOOS=windows GOARCH=amd64 CGO_ENABLED=0 go test -exec=true ./...
GOOS=windows GOARCH=amd64 CGO_ENABLED=0 \
  go test -tags goolm,stdjson -exec=true ./...     # OpenFox
GOOS=darwin GOARCH=arm64 CGO_ENABLED=0 \
  go test -exec=true <changed packages>
GOOS=linux GOARCH=mipsle GOMIPS=softfloat CGO_ENABLED=0 \
  go test -exec=true <changed packages>
```

The reference verifier reports 32 canonical objects, three Actions and seven
negative mutations. Repository-specific test coverage includes signature and
authority mutation, exact replay versus conflict, stale writer and takeover,
crash recovery, fork/gap/checkpoint handling, archive round trip, tamper and
rollback boundaries, AEAD tamper/AAD mutation, projection immutability,
negative-outcome capture, private-recipient cardinality, Carrier omission and
corruption, HTTP authentication and bounds, full Carrier database deletion and
explicit rebuild, resource metering, stable-error ordering, and Windows
cross-compilation. The changed security-boundary packages also cross-compile
for macOS arm64 and Linux MIPS little-endian/soft-float; this is compile
evidence, not runtime evidence on those targets.

## 8. Claim matrix

| Claim | Candidate result |
|---|---|
| Decode and structurally verify V1 corpus | Implemented and independently reproduced |
| Verify pinned historical Agent/evidence authority | Implemented; deployments retain all selected historical pins |
| Durable local append and recovery | Implemented; external checkpoint pin required for whole-directory rollback detection |
| Rebuild local projection and bounded learning cut | Implemented; incomplete/conflicted evidence remains unknown |
| Private one-recipient transport | Implemented and default-deny through existing side-effect Gates |
| Bounded allowlisted public publication | Implemented and default-off |
| One Carrier database-loss rebuild | Implemented and tested with explicitly retained corpus and identity key |
| Two independently operated Carrier availability | Not claimed; requires deployment evidence |
| Global latest event or complete market history | Forbidden and not implemented |
| New chain consensus behavior | Not required and not implemented |

## 9. Release checklist

Before enabling a selected production capability, an operator must:

1. pin the coordinated repository commits and schema/registry digests;
2. retain the independent conformance corpus and verifier result;
3. choose and retain historical authority/delegation proofs;
4. place the economic authority and external checkpoint pin in the intended
   rollback-protection domain;
5. configure evidence-key creation, rotation, maximum per-key encryption
   volume, retention and deletion attestation;
6. keep public publication disabled unless the exact audience and assertion
   allowlists are approved;
7. provision HTTP Carrier receipt keys over an authenticated channel;
8. enable bounded quotas, metrics and alerts without logging private evidence;
9. rehearse crash, ambiguous send, stale writer, restore and key-loss behavior;
   and
10. make only the capability and failure-domain claims supported by that
    deployment's evidence.
