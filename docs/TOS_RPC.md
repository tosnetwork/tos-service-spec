# ATOS ↔ TOS RPC / Protobuf Interface v0.2

> Phase 4C verification is strictly read-only. Its observer resolves finalized
> identity, ownership, Quote, TaskEscrow, Receipt, outcome and Proof-of-Service
> tuples; it exposes no mutation or publisher method. Cache miss, generic 404,
> malformed response, unsupported route, journal loss and transport failure
> are unavailable/error, not authoritative absence. See
> `VERIFIED_PROOF_PACKAGE_V1.md`.
> For Verified reads, principal binding, Capability ownership and execution
> signer records are tuple projections only; the server re-resolves their
> exact authority digest/reference and requires a nonzero live checkpoint
> before returning evidence to the independent verifier.

`ProofService.ResolveExecutionReceipt` is the Phase 4C read-only receipt
resolver. It recomputes the field-level CBOR Receipt digest, resolves the exact
`(verified-receipt, receipt_id, digest, expected_reference)` tuple against the
live authority, and returns only a nonzero finalized checkpoint. It never
calls `Commit` or a publisher; typed not-found remains distinct from authority
unavailability.

`ProofService.ResolveProofOfServiceEvidence` provides the same live, read-only
tuple resolution for Proof-of-Service evidence. Local cache absence is not
canonical absence and the method never commits or publishes evidence.

**Status:** Draft implementation contract  
**Branch:** `architecture-v0.2`  
**Related:** `ARCHITECTURE_V0.2.md`, `PROOF_PROFILES.md`, `SETTLEMENT.md`

## 1. Repository Mapping

The Architecture name `tos-core` maps to the implementation repository:

```text
tos-core          = tosnetwork/tos-protocol
tos-ai            = tosnetwork/tos-ai
ATOS specification= tosnetwork/atos-spec
TOS Network / L1  = tosnetwork/tos
```

`tos-protocol` already owns protocol envelopes, Edge Core, chain integration, quote/payment/receipt binding, discovery primitives, SDKs, and the private vertical Worker RPC. `tos-ai` is a vertical AI Worker implementation behind that private RPC boundary.

Therefore this specification makes one important deployment distinction:

> **ATOS does not directly expose or call the private tos-ai Worker RPC over the network. ATOS calls a tos-protocol Edge/Core execution boundary; Edge Core drives tos-ai through the existing private `tos.edge.v1.WorkerService` / `WorkerStreamService`.**

This preserves the current fail-closed security boundary while keeping architectural ownership clear: `tos-ai` executes; `tos-protocol` binds execution to identity, quote, payment/escrow, proof and receipt state.

## 2. High-Level Call Graph

```text
Codex / Claude / OpenClaw
          |
          v
     ATOS Gateway
          |
          | ATOS/TOS v1 RPC
          v
+----------------------------------+
| tos-protocol / Edge Core         |
|                                  |
| IdentityService                  |
| CapabilityService                |
| TrustService                     |
| SettlementService                |
| ProofService                     |
| ExecutionGatewayService          |
+----------------+-----------------+
                 |
                 | private local RPC
                 v
       tos.edge.v1.WorkerService
                 |
                 v
              tos-ai
                 |
                 | model / MCP / HTTP / GPU / local runtime
                 v
             execution

      tos-protocol / tos-core
                 |
                 v
            TOS Network
     identity / registry / escrow
     proof / settlement / evidence
```

A third-party ATOS-compatible gateway may implement the same client-facing ATOS protocol while using the same TOS RPC contracts or equivalent verifiable TOS interfaces.

## 3. Protobuf Files

Canonical v0.2 design files:

```text
proto/atos/tos/v1/common.proto
proto/atos/tos/v1/identity.proto
proto/atos/tos/v1/capability.proto
proto/atos/tos/v1/trust.proto
proto/atos/tos/v1/settlement.proto
proto/atos/tos/v1/proof.proto
proto/atos/tos/v1/execution.proto
```

All use package:

```proto
package atos.tos.v1;
```

The files in `atos-spec` are the cross-repository contract source during v0.2 design. Before production code generation, the team SHOULD decide whether the canonical generated Go package remains in `atos-spec` or is promoted into `tos-protocol/api/tos/...` with explicit versioned import mapping. Do not maintain two independently edited proto copies.

## 4. Service Ownership Matrix

| Service | Primary implementation | Primary callers | State authority |
|---|---|---|---|
| `IdentityService` | `tos-protocol` | ATOS, Edge Core | TOS identity/binding state |
| `CapabilityService` | `tos-protocol` | ATOS/indexers | TOS capability ownership/manifest commitments |
| `TrustService` | `tos-protocol` | ATOS, Edge Core | quote commitments + signer authorization |
| `SettlementService` | `tos-protocol` | ATOS, Edge Core | TOS escrow/settlement state |
| `ProofService` | `tos-protocol` | ATOS, Edge Core, indexers | receipt/proof/PoS evidence |
| `ExecutionGatewayService` | `tos-protocol` Edge Core | ATOS | durable execution/job projection |
| `tos.edge.v1.WorkerService` | existing `tos-protocol` contract; implemented by `tos-ai` | local Edge Core only | private Worker task state |

`tos-ai` MUST NOT gain wallet ownership, client account authority, semantic marketplace ranking, escrow control, or public Internet authentication merely to satisfy this interface.

## 5. Trust-Mode Rules

The protobuf layer uses a concrete `TrustMode`:

```text
MANAGED
VERIFIED
NATIVE
```

`AUTO` exists only as an ATOS request policy (`RequestedTrustMode`) before Quote resolution.

Once ATOS issues a Quote, the RPC path receives one concrete `TrustMode` and, where applicable, one concrete `ProofProfile`:

```text
verified -> TOS_VERIFIED_V1
native   -> TOS_NATIVE_V1
```

The following objects MUST NOT contain unresolved `AUTO`:

```text
QuoteCommitment
Escrow
JobRecord
ExecutionReceipt
Settlement
ProofOfServiceEvidence
```

A failure to satisfy the committed mode/profile requires failure or a new Quote. It MUST NOT silently downgrade the same transaction.

## 6. Two Quote Layers

ATOS and `tos-protocol` have different commercial responsibilities and therefore two related Quote objects.

### 6.1 Service Execution Quote

Produced by `ExecutionGatewayService.QuoteExecution`.

This is the provider/Edge execution offer and binds execution-relevant facts such as:

- provider/capability/version;
- provider-side price / network amount;
- capacity revision;
- model/runtime revision where relevant;
- execution deadline;
- expiry;
- signed service quote digest/reference.

For a `tos-ai` backed Edge, Edge Core derives this from its existing execution/Worker quote pipeline; ATOS never calls the private Worker `Quote` method directly.

### 6.2 ATOS Commercial Quote

Produced by `atos_quote` for the client.

ATOS may add:

- gateway fees;
- fiat/credit pricing;
- exchange-rate handling;
- user spend policy;
- selected trust mode;
- proof profile;
- dispute policy;
- client-facing `total_max`.

For Verified/Native execution, `TrustService.CommitQuote` binds the ATOS Quote to the underlying service quote through `underlying_service_quote_ref`.

```text
ServiceExecutionQuote
        |
        v
ATOS pricing/policy
        |
        v
ATOS Commercial Quote
        |
        v
CommitQuote
        |
        v
TOS-verifiable QuoteCommitment
```

Changing provider, capability version, mode, proof profile, maximum price, settlement backend, dispute policy, deadline or underlying service quote requires a new ATOS Quote.

## 7. Verified Execution Flow

A recommended Verified flow:

```text
1. ATOS search/index chooses capability
2. ResolveCapability / VerifyCapabilityOwnership
3. ExecutionGateway.QuoteExecution
4. ATOS constructs client-facing Quote
5. TrustService.CommitQuote
6. SettlementService.CreateEscrow
7. ExecutionGateway.SubmitJob
8. Edge Core maps exact intent -> private Worker invocation
9. tos-ai executes through existing WorkerService
10. Edge Core obtains/replays terminal Worker result
11. authorized execution signer signs receipt
12. ProofService.CommitExecutionReceipt
13. ProofService.VerifyExecutionReceipt
14. SettlementService.SettleJob
15. ProofService.CommitProofOfServiceEvidence
16. ATOS returns result + receipt/proof references
```

The current `tos-protocol` exact-once semantics remain authoritative inside Edge Core: an already-running durable Worker task is recovered with read-only task lookup rather than re-invocation.

## 8. Native Execution Flow

Native uses the same transaction pipeline as Verified plus `tos_native_v1` guarantees:

- globally resolvable provider identity;
- federation-safe capability ID;
- manifest/ownership resolution without an `atos.im` canonical database;
- independent gateway/indexer reconstruction of registry facts;
- gateway-independent proof verification;
- domain separation sufficient to prevent cross-gateway/network replay.

The execution workload still remains off-chain. Native does not mean model inference inside consensus.

## 9. Managed Mode

Managed Mode may bypass the TOS trust/economic services entirely:

```text
ATOS -> managed provider adapter -> result
```

or it may execute against a TOS Edge/provider while retaining managed ATOS accounting.

A Managed call MUST NOT be presented as `tos_verified_v1` merely because its provider happens to run `tos-ai` or `tos-protocol`.

### 9.1 Managed Financial Ledger Anchor V1

Phase 7A adds one purpose-specific service. It is an integrity boundary, not a
Managed escrow or settlement backend:

```protobuf
service FinancialIntegrityService {
  rpc PublishManagedFinancialAnchor(PublishManagedFinancialAnchorRequest)
      returns (PublishManagedFinancialAnchorResponse);
  rpc ResolveManagedFinancialAnchor(ResolveManagedFinancialAnchorRequest)
      returns (ResolveManagedFinancialAnchorResponse);
}

message ManagedFinancialAnchorInput {
  string version = 1;                 // atos_managed_financial_anchor_v1
  string anchor_id = 2;
  string batch_id = 3;
  uint64 batch_sequence = 4;
  uint64 first_sequence = 5;
  uint64 last_sequence = 6;
  uint32 commitment_count = 7;
  string previous_anchor_id = 8;
  Digest previous_merkle_root = 9;
  Digest merkle_root = 10;
  Digest manifest_digest = 11;
  Digest signature_digest = 12;
  string signing_key_id = 13;
  string canonicalization = 14;
  string gateway_id = 15;
  string network_id = 16;
}

message PublishManagedFinancialAnchorRequest {
  RequestContext context = 1;
  ManagedFinancialAnchorInput anchor = 2;
}

message PublishManagedFinancialAnchorResponse {
  ManagedFinancialAnchorInput anchor = 1;
  Digest payload_digest = 2;
  NetworkReference anchor_ref = 3;
  bool finalized = 4;
  uint64 finalized_checkpoint = 5;
}

message ResolveManagedFinancialAnchorRequest {
  RequestContext context = 1;
  string anchor_id = 2;
  string network_id = 3;
}

message ResolveManagedFinancialAnchorResponse {
  ManagedFinancialAnchorInput anchor = 1;
  Digest payload_digest = 2;
  NetworkReference anchor_ref = 3;
  bool finalized = 4;
  uint64 finalized_checkpoint = 5;
}
```

The canonical payload and stable `anchor_id` are defined by
`MANAGED_FINANCIAL_INTEGRITY_V1.md`. `RequestContext.request_id` and
`trace_id` are transport fields and MUST NOT enter semantic identity.
`context.idempotency_key` MUST equal `anchor.anchor_id` on publish.

`tos-protocol` durably records the exact anchor and payload digest before
calling its existing chain `Authority`. It commits with kind
`managed-financial-ledger-root`, object ID `anchor_id`, and the canonical
payload digest. An exact retry returns the original reference. Reuse of
`anchor_id` with changed payload is `ALREADY_EXISTS` /
`IDEMPOTENCY_CONFLICT`. Resolve is read-only and never republishes.

The chain-backed Authority's existing ActionPublisher and independent quorum
observation are reused. A successful response requires the configured network,
an exact action receipt, `confirmed && finalized && !reorganized`, and a
current finalized checkpoint. The local development Authority may exercise
contract serialization but MUST report a non-finalized/local reference and
cannot satisfy the Phase 7A anchor acceptance test.

No field from this service may populate Verified Quote, escrow, Receipt, or
settlement proof state. Public UI/API descriptions call it a Managed financial
history integrity anchor, never a Verified Job.

## 10. Identity Service

### `ResolveAgentIdentity`

Read-only resolution of a globally meaningful Agent/provider identity.

### `ResolvePrincipalBinding`

Maps an ATOS `principal_id` to a TOS identity when such a server-side binding exists. This enables ordinary ATOS users to receive TOS-backed guarantees without owning or exposing wallet keys.

### `CreatePrincipalBinding` / `RevokePrincipalBinding` (Phase 4A)

Durable, idempotent binding mutations, added for `docs/IMPLEMENTATION_ROADMAP.md`
§8.1's production identity binding. `CreatePrincipalBinding` never creates an
`AgentIdentity` from nothing -- `agent_id` must already independently resolve
through `ResolveAgentIdentity` before the binding is anchored, so a caller can
never conjure ownership of an identity merely by naming it. Creating a new
`AgentIdentity` itself remains an out-of-band operator/bootstrap action in
Phase 4A; full self-service, wallet-signature-proved identity creation and
rotation is Phase 5 Wallet-Native's deliverable, not this phase's.

These are gateway-operator actions, authorized one layer above this RPC (at
ATOS's own REST/MCP boundary, through an explicit-grant-only scope never in
the passkey/Device-Authorization self-service default bundle -- the same
admin-scope discipline already applied to `activation:evaluate`), not
ordinary end-user self-service. `context.caller_id` identifies the operating
ATOS backend, not the human/agent the binding is being created for.

A revoked binding does not retroactively invalidate facts anchored while it
was active; it only stops future resolution from treating the principal as
currently bound. Every dependent Phase 4A decision (ownership resolution,
`ActivationAuthority.Evaluate`) MUST re-resolve the binding fresh rather than
caching "was bound," and MUST fail closed / suspend, never silently
downgrade, when a previously-bound identity is no longer active.

No method returns wallet seed phrases, private keys or key-derivation data.

## 11. Capability Service

### `ResolveCapability`

Returns canonical provider/version/manifest/ownership facts and public endpoint hints.

### `VerifyCapabilityOwnership`

Verifies that the quoted provider owns the quoted capability/version and expected manifest digest.

### `CommitCapabilityManifest`

Anchors immutable manifest/version/ownership facts. This is not a search API. Embeddings, semantic ranking, health scoring and personalized ordering remain gateway/indexer functions.

## 12. Trust Service

### `CommitQuote`

Creates or exact-replays a Quote commitment for Verified/Native mode.

For Phase 4B-1 Verified Quotes the normative value is
`atos_verified_quote_commitment_v1`, encoded and hashed as specified by
`VERIFIED_QUOTE_COMMITMENT_V1.md`. `context.idempotency_key` MUST equal
`quote_id`. The configured authority network MUST equal `network_id`, and
`domain` MUST identify the committing gateway deployment. `trust_mode` is
exactly `VERIFIED` and `proof_profile` is exactly `TOS_VERIFIED_V1`; `AUTO`
is not representable here. `canonicalization` MUST equal
`rfc8949_core_deterministic_cbor`. Implementations MUST reject protobuf
unknown fields recursively before conversion to the normative field model.

Before mutation, the service MUST freshly resolve and validate the provider
identity, exact Capability ownership/version/manifest, and the exact live
execution-signer authorization. Caller-supplied references are assertions to
compare with authoritative state, never selectors. An exact replay returns
the original commitment. Reuse of `quote_id` or the same idempotency identity
with different canonical semantics returns `IDEMPOTENCY_CONFLICT` /
`QUOTE_MISMATCH`.

### `GetQuoteCommitment`

Read-only resolution for recovery/audit.

This is the mandatory recovery operation after a timeout or lost response.
For Verified Quotes the caller supplies `expected_quote` and, when known,
`expected_commitment_ref`. The server independently recomputes the semantic
digest and freshly resolves that exact `(kind, quote_id, digest)` tuple using
the live canonical authority. When the reference is unknown after a lost
response, the resolver MUST perform tuple discovery and return either the
finalized canonical reference or explicit authoritative not-found.
For the chain-backed Authority, tuple discovery resolves the deterministic
Action ID through the publisher's durable read-only receipt journal and then
independently re-observes the returned exact transaction through the quorum
chain adapter. Receipt-journal unavailability is not not-found and fails
closed; discovery never calls the mutation/publish endpoint.
The publisher MUST persist an intent before broadcasting. A pending or
uncertain intent MUST NOT be reported as absent. Authoritative absence is a
versioned `action_not_found` response bound to the requested Action ID from the
durable journal; a generic HTTP 404, unsupported route, proxy fallback or
malformed/mismatched response is resolver unavailability. Publisher readiness
MUST advertise the resolve endpoint, journal version, typed-not-found and
intent-before-publish capabilities; clients MUST reject legacy health
responses that do not negotiate this contract.
The durable journal MUST be explicitly enrolled once with a pinned identity;
normal service startup MUST NOT create missing state and MUST reject a missing
or identity-mismatched journal. The publisher MUST independently recompute the
Action ID from the configured network, service address/ID, commitment kind,
object ID/digest and operator-fixed payer/payee/amount policy before invoking
key custody. The production backend MUST negotiate recover-by-Action-ID and
search-before-broadcast behavior and prove the exact payer wallet/RPC binding
at readiness.
The client MUST also pin the versioned journal enrollment digest. Health and
typed not-found responses MUST echo the exact expected journal identity and
binding; network equality alone is insufficient.
The send and recovery clients MUST use the same pinned endpoint set and verify
the configured network's genesis identity. A bounded history lookup is not
authoritative absence: once an intent may have been broadcast, failure to find
it within the available window MUST fail closed and MUST NOT trigger another
send. Safe automatic recovery requires complete pagination to a pre-broadcast
cursor or an authoritative Action-ID index.
Compatibility fields MUST be interpreted identically on both sides. In
particular, a legacy single `url` and modern `urls` list are merged, trimmed
and deduplicated before comparison; an implementation MUST NOT ignore either
field when both are present.
The validated sender configuration MUST remain immutable for the publisher
lifetime. Merely comparing a pathname at startup or immediately before spawn
is insufficient because the child may reopen changed contents. A sender MAY
use an unlinked, inherited file-descriptor snapshot with an explicit format
(not a synthetic `/proc` pathname whose extension or availability varies by
platform); otherwise it MUST provide
an equivalent mechanism that removes the check/use race.
The production tosctl TaskEscrow publisher selects the inherited-descriptor
mechanism and is explicitly Linux-only. It MUST run as an unprivileged account
and accept only an executable and parent path owned by root and not writable by
group or world. Unsupported platforms and service-owned executables fail
startup.
Process-local persistence is only a cache: it MUST NOT
make a Quote found or finalized by itself. This lookup must therefore work on
a different stateless `tos-protocol` replica and MUST fail closed when live
resolution is unavailable, changes network/reference, is non-final, reports
a zero or regressed finalized checkpoint, or returns inconsistent facts.

The caller compares the returned canonical value, digest, network and
finality before retrying `CommitQuote`; authoritative absence is the only
outcome that permits another mutation attempt.

### Execution signer authorization

`AuthorizeExecutionSigner`, `RevokeExecutionSigner`, and `ResolveExecutionSignerAuthorization` implement:

```text
Provider / Capability owner
          |
          v
Execution signer authorization
          |
          v
Signed Execution Receipt
```

The signer may be a provider key, Edge runtime, `tos-ai` worker/runtime identity, enterprise delegate or audited adapter. The signer authorization MUST be scoped to provider/capability and SHOULD bind version and validity interval.

## 13. Settlement Service

Verified result review and dispute RPCs are governed by
`VERIFIED_DISPUTE_V1.md`. They extend the existing SettlementService and
TaskEscrow driver; they are not a parallel settlement authority.

### `CreateEscrow`

Creates an economically enforceable reservation for the Quote. A Merkle root of a private ATOS ledger is not equivalent to TOS-backed escrow.

For Verified, `verified_terms` is mandatory and is validated against a live
finalized Phase 4B-1 commitment. The response is usable only after independent
canonical TaskEscrow observation with a non-zero checkpoint. The deterministic
schema and recovery rules are defined by `VERIFIED_TASK_ESCROW_V1.md`.

### `ReleaseEscrow`

Releases unused or canceled reservations under the original Quote semantics.

Verified release requires the original terms, reservation digest/reference and
a frozen reason. It is idempotent but never treats local state or an untyped
404 as proof that a mutation may be replayed.

### `SettleJob`

The server MUST re-verify the referenced receipt and proof profile. A caller cannot force settlement by supplying `verified=true`.

For Verified settlement, the server MUST independently observe the canonical
TaskEscrow settled state and return a `settlement_ref` with the configured
network, `finalized=true` and a non-zero finalized checkpoint. The response
MUST reproduce the exact escrow/Quote/Job/Receipt tuple and preserve atomic
money conservation: requested charge equals `charged`, all amounts use TOS,
and `charged + refunded == reserved`. A transition string or publisher
receipt without this observation is not settlement proof.

Verified `SettleJobRequest` additionally carries `expected_terms`,
`expected_escrow_ref`, and `expected_reservation_digest`. All three are
mandatory together. Before any settlement mutation, the server performs the
same live tuple recovery as `GetEscrow`, requires the canonical escrow to be
reserved, and verifies that its local projection matches the canonical Quote
commitment, reservation digest, contract reference and code hash. Local
bbolt/cache state never selects the payout contract by itself.

TaskEscrow V1 cannot pay a separate gateway recipient. Consequently Verified
Quote `fees` MUST be exactly zero and `total_max == subtotal`; non-zero fees
are rejected at both Quote commitment and escrow-term validation.

`requested_charge.atomic_amount` MAY be zero. A zero charge is a successful
settlement, not a release failure: the canonical settle transition pays zero
to the provider and refunds the full reserve to the requester. Implementations
MUST NOT strand such a Job in settlement-pending or replace it with a Managed
refund.

The ATOS gateway MUST compare every returned tuple and monetary field before
writing its projection. A Verified response MUST never invoke the Managed
ledger adapter or credit a Managed balance/policy; TOS TaskEscrow is the sole
financial authority for that Job.

### `GetEscrow` / `GetSettlement`

Read-only recovery and audit calls.

`GetEscrow` accepts the full expected tuple and optional known reference. A
missing reference invokes deterministic tuple/action discovery; it never
weakens live finality validation.

For a released escrow, portable-proof observation additionally supplies
`expected_terminal_ref`, `expected_release_digest`, and
`expected_release_reason_code`. The service reconstructs the exact cancel,
timeout, or reject ActionID, resolves it read-only from the enrolled publisher
journal, and independently observes that chain transition. Generic absence,
typed journal absence, pending state, or transport failure is unavailable and
MUST NOT call `Publish`. The returned immutable contract reference remains
separate from the terminal release transaction reference.

State-changing settlement methods require idempotency.

## 14. Proof Service

### Execution receipts

`CommitExecutionReceipt` persists/anchors the signed receipt or receipt commitment.

`VerifyExecutionReceipt` verifies at least:

- Quote/job binding;
- capability/version/provider binding;
- signer authorization;
- result/usage/output commitments;
- maximum-charge rules;
- required proof profile;
- network inclusion/finality rules where applicable.

A signed receipt is evidence of execution outcome and signer statement; it is not automatically proof of semantic correctness of the provider's answer.

### Proof-of-Service

`CommitProofOfServiceEvidence` converts terminal verified outcomes into portable evidence.

`ReadProofOfService` and `ReadReputation` provide the data needed for independent indexers/gateways to compute reputation projections.

The normalized `score` is a derived convenience value, not a financial or consensus-critical field.

## 15. Execution Gateway Service

`ExecutionGatewayService` is intentionally placed in this specification even though actual AI execution belongs to `tos-ai`.

It is implemented at the Edge/Core boundary because existing `tos-ai` correctly exposes only a private Unix-socket Worker service.

### `GetProviderStatus`

Returns short-lived execution readiness/capacity projection. It is not long-term reputation.

### `QuoteExecution`

Obtains a provider/Edge service execution quote.

### `SubmitJob`

Creates or exact-replays the durable Edge execution claim bound to:

- ATOS Job ID;
- ATOS Quote ID;
- service quote ID;
- escrow ID where required;
- principal/provider/capability/version;
- concrete trust mode/proof profile;
- exact input commitment;
- execution deadline and retention bound.

### `GetJob`

Read-only durable recovery path.

### `CancelJob`

Claim-bound cancellation request. An ambiguous cancellation does not create a terminal success/failure by itself.

### `StreamJob`

Server streaming of bounded output/state events. Resume uses sequence/offset/digest fields consistent with the existing Worker streaming model.

`JobEvent.stream_digest` (and the `expected_stream_digest` a resumed
`StreamJobRequest` echoes back) is the digest of the **complete output
currently retained for the Job** (`digestMessage(stored.Output)`), not a
progressive digest accumulated chunk by chunk. Every event in one
`StreamJob` response — the `STATE` event, every `OUTPUT_CHUNK`, and the
final `TERMINAL` event alike — carries this same value.

Two consequences a caller MUST account for:

- It is an execution-identity check ("am I resuming the same retained
  output"), not a per-chunk integrity checksum. A consumer that wants a
  progressive cumulative digest over the bytes it has received must compute
  that itself from the chunk contents; it cannot derive it from
  `stream_digest`.
- Before a Job produces any output (a non-terminal `Job`, where
  `stored.Output` is still empty), this digest is `digestMessage(nil)` — the
  digest of zero bytes, identical across every such Job in the system. It is
  **not yet Job-specific**. A caller must not persist or replay this
  pre-output value as if it identified a particular Job's execution; only
  once real output exists (i.e. once at least one `OUTPUT_CHUNK` has
  actually been observed) does `stream_digest` become a meaningful,
  Job-specific value safe to echo back as `expected_stream_digest` on a
  later resumed pull.

### `FetchResult`

Returns terminal output/artifact commitments and bounded usage.

### `FetchExecutionReceipt`

Returns canonical signed receipt bytes/reference. The typed receipt contract lives in `proof.proto`.

## 16. Mapping to Existing `tos.edge.v1.WorkerService`

The new ATOS-facing execution contract does not replace the existing Worker contract.

Conceptual mapping:

| ATOS/TOS execution RPC | Edge Core internal action | existing private Worker RPC |
|---|---|---|
| `GetProviderStatus` | inspect deployment plan/readiness | `Health`, `GetCapabilities` |
| `QuoteExecution` | bind provider policy + capacity | `Quote` |
| `SubmitJob` | commit durable execution claim | `Invoke` exactly once |
| `GetJob` | recover durable claim | `GetTask` only after dispatch |
| `CancelJob` | validate claim ownership | `Cancel` |
| `StreamJob` | bounded stream/recovery | `InvokeStream` / `ResumeStream` |
| `FetchResult` | return validated terminal projection | retained `GetTask` result |
| `FetchExecutionReceipt` | Edge receipt journal/signer | Worker never signs economic receipt |

Important invariant:

> A failed or uncertain Edge-to-Worker RPC MUST NOT cause ATOS to resubmit the same work with a new Worker task identity. Edge Core's durable claim and read-only recovery semantics remain authoritative.

## 17. Idempotency

`RequestContext.idempotency_key` is REQUIRED for state-changing calls:

```text
CommitCapabilityManifest
CommitQuote
AuthorizeExecutionSigner
RevokeExecutionSigner
CreateEscrow
ReleaseEscrow
SettleJob
CommitExecutionReceipt
CommitProofOfServiceEvidence
SubmitJob
CancelJob
CreatePrincipalBinding
RevokePrincipalBinding
```

Rules:

```text
same caller + same key + same canonical request -> original semantic result
same caller + same key + different canonical request -> idempotency conflict
```

Read-only methods MAY omit the key.

Implementations must retain replay records for at least the longest applicable execution, settlement and dispute window.

## 18. Canonicalization and Signatures

Protobuf transport bytes themselves MUST NOT be assumed to be the canonical signed representation.

When an object is cryptographically committed/signed, the implementation should reuse the deterministic canonical-value rules already established by `tos-protocol` (including its bounded deterministic CBOR model) or an explicitly versioned successor.

RPC messages carry structured values plus digests/references; signing code receives purpose-specific canonical bytes.

## 19. Money and Amount Rules

Never use IEEE floating point for prices or settlement amounts.

- `Money.amount` is a decimal string for client-facing/accounting values.
- `NetworkAmount.atomic_amount` is an integer base-unit decimal string.
- conversions/exchange rates belong to the ATOS commercial layer and must be bound into Quote terms when they affect the maximum client charge.

`ReputationSummary.score` is allowed to be a `double` because it is a derived non-consensus display/ranking signal, not money or signed settlement state.

## 20. Transport

Recommended implementation transports:

### ATOS ↔ tos-protocol

- ConnectRPC or gRPC over HTTP/2/HTTP/3-capable service infrastructure;
- TLS required outside loopback/private test environments;
- mTLS or equivalent workload identity for privileged internal gateway calls;
- explicit message/deadline/concurrency bounds;
- no transparent retry of state-changing execution calls unless idempotency semantics are preserved.

### tos-protocol ↔ tos-ai

Keep the existing private authenticated local transport model:

```text
mode-0600 Unix socket
bounded ConnectRPC
no public listener
no wallet/private owner key in Worker
```

## 21. Error Model

Transport status and stable application error codes are both required.

Recommended stable codes include:

```text
INVALID_ARGUMENT
NOT_FOUND
ALREADY_EXISTS
IDEMPOTENCY_CONFLICT
PERMISSION_DENIED
UNAVAILABLE
DEADLINE_EXCEEDED
RESOURCE_EXHAUSTED
TRUST_MODE_UNAVAILABLE
PROOF_PROFILE_UNAVAILABLE
QUOTE_EXPIRED
QUOTE_MISMATCH
SERVICE_QUOTE_EXPIRED
ESCROW_REQUIRED
ESCROW_UNAVAILABLE
RECEIPT_INVALID
SIGNER_UNAUTHORIZED
SETTLEMENT_FAILED
PAYMENT_REORGANIZED
EXECUTION_UNCERTAIN
REQUOTE_REQUIRED
```

`EXECUTION_UNCERTAIN` is especially important: it preserves exact-once recovery and MUST NOT be translated into an automatic new execution.

## 22. Security Invariants

1. No wallet seed/private key crosses ATOS RPC.
2. `tos-ai` receives no client wallet/payment authority.
3. ATOS cannot self-assert a Verified/Native receipt as valid.
4. Provider execution signer authority is independently verifiable for Verified/Native.
5. Quote, service quote, escrow, Job and receipt identities are cross-bound.
6. A different trust mode/proof profile requires a new Quote.
7. Bulk private payloads stay off-chain; commitments are used for proof.
8. Gateway ranking/search state is not consensus state.
9. Settlement cannot exceed the Quote maximum or proven reservation.
10. Ambiguous execution never authorizes blind resubmission.

## 23. Implementation Promotion Plan

### Step 1 — Spec freeze

Freeze these v0.2 messages/RPC names in `atos-spec` after review.

### Step 2 — Canonical proto ownership

Choose one canonical code-generation source. Recommended direction:

```text
generic TOS/Edge RPC contracts -> tos-protocol/api/tos/agent/v1
ATOS client/public contracts    -> atos-spec
```

If moved, preserve wire field numbers and service semantics.

### Step 3 — tos-protocol implementation

Implement adapters/services around existing Edge Core, chain adapters, journal, signer and proof boundaries rather than bypassing them.

### Step 4 — tos-ai integration

Do not add a public ATOS listener to `tos-ai`. Reuse the existing private Worker API and add only narrowly required fields/versioned extensions if the Edge mapping proves impossible without them.

### Step 5 — ATOS adapter

Add `adapters/tos-protocol` (or equivalent) to atos.im. Public MCP/A2A/REST schemas remain chain-abstracted.

### Step 6 — conformance

Add fixed vectors for:

- Quote/service-quote binding;
- idempotent CommitQuote/CreateEscrow/SubmitJob/SettleJob;
- signer authorization and revocation;
- receipt replay;
- execution-uncertain recovery;
- native cross-gateway resolution;
- no-silent-downgrade behavior.

## 24. Non-Goals

This interface does not:

- replace MCP or A2A;
- expose TOS consensus RPC directly to Codex;
- make `tos-ai` a marketplace;
- put model payloads on-chain;
- define semantic correctness of AI answers;
- define search ranking weights;
- require consumers to own TOS;
- require Managed Mode to use TOS.

## 25. Architectural Summary

```text
ATOS owns:
  UX / discovery / ranking / account policy / client commercial quote

Edge Core (tos-protocol) owns:
  execution admission / exact durable claim / service quote binding /
  identity-trust bridge / chain observation / receipt boundary /
  escrow-settlement-proof adapters

tos-ai owns:
  bounded vertical AI execution only

TOS Network owns:
  decentralized identity / registry commitments / escrow / settlement /
  portable proof and economic finality
```

This is the intended implementation interpretation of ATOS Architecture v0.2.
