# ATOS A2A Profile v0.2

## Purpose

Use A2A for stateful agent-to-agent collaboration. MCP remains the preferred client/tool surface for Codex-like hosts; A2A is the provider/inter-agent interoperability surface.

Reference gateway endpoint:

`https://a2a.atos.im`

Discovery:

`https://atos.im/.well-known/agent-card.json`

Native ATOS does not require all A2A traffic to pass through this reference endpoint; independently operated gateways/providers may expose compatible A2A endpoints.

## Mapping

ATOS maps A2A Tasks to ATOS Jobs.

| A2A concept | ATOS business object |
|---|---|
| Agent Card | Provider/ATOS discovery card |
| Task | Job |
| Message | Job interaction message |
| Artifact | Artifact |
| Task state | Job state |

## State Mapping

- `submitted` -> `submitted`
- `working` -> `working`
- `input-required` -> `input_required`
- `completed` -> `completed`
- `failed` -> `failed`
- `canceled` -> `canceled`
- provider refusal -> `rejected`

The A2A Task/ATOS Job inherits the concrete trust mode and proof profile from its Quote.

## Trust-Mode Semantics

Pre-Quote client policy may use:

```text
requested_trust_mode = managed | verified | native | auto
```

Once a Quote is selected, Task/Job commerce metadata uses:

```text
trust_mode = managed | verified | native
```

`auto` MUST NOT appear as the final Task/Job mode.

Standard profiles:

```text
verified -> tos_verified_v1
native   -> tos_native_v1
```

A remote agent MUST NOT reinterpret a quoted `verified` or `native` Task as Managed. If it cannot satisfy the Quote's proof profile, it must reject/fail the work so the caller can re-quote.

## ATOS Commerce Extension

ATOS-specific commercial/trust fields SHOULD be carried through an A2A extension instead of changing core A2A objects.

Proposed v0.2 extension URI:

`https://atos.im/extensions/commerce/v2`

### Pre-Quote request policy

```json
{
  "requested_trust_mode":"auto",
  "proof_requirements":{
    "network_verifiable_receipt":true,
    "tos_settlement":false
  },
  "max_total":{"amount":"10.00","currency":"USD"}
}
```

Boolean proof requirements follow the common v0.2 rule: `true` means required; `false`/omitted means not required, not forbidden.

### Quote-bound Verified Task/Job fields

```json
{
  "quote_id":"q_...",
  "trust_mode":"verified",
  "proof_profile":"tos_verified_v1",
  "price":{"total_max":"5.25","currency":"USD"},
  "settlement":{"backend":"tos","escrow":true},
  "proof_status":{
    "quote":"committed",
    "escrow":"reserved",
    "receipt":"pending",
    "settlement":"pending"
  },
  "idempotency_key":"..."
}
```

### Quote-bound Native Task/Job fields

```json
{
  "quote_id":"q_...",
  "trust_mode":"native",
  "proof_profile":"tos_native_v1",
  "price":{"total_max":"5.25","currency":"USD"},
  "settlement":{"backend":"tos","escrow":true},
  "idempotency_key":"..."
}
```

Do not put wallet private keys, chain RPC credentials, payment credentials, provider secrets, prompts, or private artifacts into extension fields.

## Open Task Marketplace Extension

Phase 3C's demand-side marketplace (`docs/IMPLEMENTATION_ROADMAP.md` §7.3,
`docs/API.md` §5A, `docs/MCP.md` §6A/§8). An OpenTask is a marketplace
*demand* object — a requester publishes a goal/budget/deadline without
necessarily knowing a `capability_id` in advance, Providers discover it and
submit proposals, and the requester accepts exactly one proposal. This is
**not** the same relationship an ordinary A2A Task expresses (a client
already addressing one specific remote Agent) and is therefore never
represented as an A2A Task or wrapped in the `message/send` / Task/Message
model — see Invariant 9 below. It is carried as its own custom JSON-RPC
method namespace, `openTasks/*`, deliberately distinct from the reserved
`tasks/*` namespace (which MUST always mean "the A2A Task mapped 1:1 to an
ATOS Job," per Invariant 1) so a compliant A2A client can never confuse the
two.

Every `openTasks/*` method uses the same JSON-RPC 2.0 envelope, Bearer
authentication and error-code conventions already defined for
`message/send`/`tasks/get`/`tasks/cancel` above. `idempotency_key` is a
request-param field (never an HTTP header) for every method that requires
one — the same convention `message/send`'s commerce extension already uses,
and the same "JSON body field, not `Idempotency-Key` header" convention
`docs/API.md` §5A defines for the REST surface, since a JSON-RPC method's
own params are the natural place for it (a batched JSON-RPC request could
carry several calls under one shared set of HTTP headers, so a header
cannot scope a single call's idempotency the way a param can).

Object field names/shapes are identical to the already-frozen REST/MCP
contract (`docs/API.md` §5A: `OpenTask`, `OpenTaskProposal`/`ProposalView`,
`AcceptanceOperation`) — this section defines the RPC method surface over
that same contract, never a second naming or shape for the same objects.

### Methods

| Method | Scope | Params | Result |
|---|---|---|---|
| `openTasks/publish` | `open_tasks:write` | `title` (required), `description`, `input`, `requested_trust_mode`, `proof_requirements`, `constraints.max_total`, `expires_at` (required), `idempotency_key` (required) | `OpenTask` (owner view) |
| `openTasks/search` | `open_tasks:read` | `limit` (optional, 1-100, default 50) | `{"open_tasks": [OpenTask (public view), ...]}` |
| `openTasks/get` | `open_tasks:read` | `task_id` (required) | `OpenTask` (full for owner/winning provider, public view otherwise) |
| `openTasks/cancel` | `open_tasks:write` | `task_id` (required) | `OpenTask` (owner view) |
| `openTasks/proposals/submit` | `open_task_proposals:write` | `task_id` (required), `capability_id` (required), `message`, `proposed_price`, `idempotency_key` (required) | `OpenTaskProposal` (submitting provider's own view) |
| `openTasks/proposals/list` | `open_tasks:read` | `task_id` (required) | `{"proposals": [ProposalView, ...]}` |
| `openTasks/proposals/withdraw` | `open_task_proposals:write` | `proposal_id` (required) | `OpenTaskProposal` |
| `openTasks/proposals/accept` | `open_tasks:write` | `task_id` (required), `proposal_id` (required), `idempotency_key` (required) | `{"open_task": OpenTask, "acceptance": AcceptanceOperation}` |

`openTasks/proposals/submit`/`openTasks/proposals/withdraw` require
`open_task_proposals:write` — deliberately a separate, explicit-grant-only
scope from `open_tasks:write`, never implied by it, mirroring
`provider_jobs:deliver`'s pattern: applying to fulfill someone else's task
is a distinct trust-side-effect class from managing one's own task.
`open_tasks:read`/`write` are ordinary default consumer scopes (publishing a
task and accepting a proposal for one's own task are ordinary consumer
actions, the same as creating or cancelling a Job).

`openTasks/publish`/`proposals/submit`/`proposals/accept` requiring
`idempotency_key`, retried with the same key and an identical request,
return the original result rather than erroring or re-executing; a reused
key against a materially different request is `idempotency_conflict`
(`codeInvalidParams`, `data.code = "idempotency_conflict"`) — the same
convention every other idempotent mutation in this document family uses.

`capability_version` is never caller-supplied in `proposals/submit` — it is
frozen from the Capability's current version at submission time.
`proposed_price` is a non-authoritative hint only; `proposals/accept`
always re-derives the real price through the existing Quote pricing rules,
bounded by the task's own `constraints.max_total`.

`openTasks/get` and `openTasks/proposals/list` apply the same
viewer-dependent redaction the REST/MCP surface already defines: task
`input` and full proposal detail (`message`/`proposed_price`) are visible
only to the task's own owner or, for a proposal, its own submitting
provider or (once accepted) the winning provider — every other caller
receives the redacted public view. Redaction is enforced server-side; it is
never a client-side filtering convention.

### Example: publish

Request:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "openTasks/publish",
  "params": {
    "title": "Summarize Q3 filings",
    "input": {"document_url": "..."},
    "requested_trust_mode": "managed",
    "constraints": {"max_total": {"amount": "5.00", "currency": "USD"}},
    "expires_at": "2026-09-01T00:00:00Z",
    "idempotency_key": "task-publish-..."
  }
}
```

Result:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "id": "task_...",
    "principal_id": "agt_...",
    "title": "Summarize Q3 filings",
    "status": "open",
    "expires_at": "2026-09-01T00:00:00Z",
    "created_at": "..."
  }
}
```

### Example: accept

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "openTasks/proposals/accept",
  "params": {"task_id": "task_...", "proposal_id": "prop_...", "idempotency_key": "task-accept-..."}
}
```

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "open_task": {"id": "task_...", "status": "accepted", "accepted_proposal_id": "prop_..."},
    "acceptance": {
      "id": "acceptop_...",
      "checkpoint": "completed",
      "quote_id": "q_...",
      "job_id": "job_..."
    }
  }
}
```

Once `acceptance.checkpoint` reaches `completed`, `job_id` is a normal ATOS
Job — from that point on it is addressable through the ordinary `tasks/get`/
`tasks/cancel` Task/Job surface like any other Job, exactly as
`docs/IMPLEMENTATION_ROADMAP.md` §7.3 describes ("normal immutable Quote ->
normal Job -> Execution Receipt -> settlement/dispute lifecycle"). The
`openTasks/*` namespace's responsibility ends at that handoff.

## Quote Authority

The ATOS Quote is the commercial/trust contract.

After a Task is associated with `quote_id`:

- Capability/provider/version must match the Quote;
- concrete `trust_mode` must match the Quote;
- proof profile must match the Quote;
- maximum price/terms must match the Quote;
- dispute-policy commitment must match the Quote;
- a change to any of these requires a new Quote.

A2A messages may continue an interactive Task but MUST NOT mutate the Quote's trust contract.

## Artifacts and Receipts

A2A Artifacts remain off-chain by default.

For Verified/Native work, the final Execution Receipt may commit:

- artifact hashes;
- input/output commitments;
- usage commitment;
- execution signer identity;
- signer authorization reference;
- signature;
- TOS proof reference.

Conceptual Native final extension:

```json
{
  "quote_id":"q_...",
  "trust_mode":"native",
  "proof_profile":"tos_native_v1",
  "receipt":{
    "receipt_id":"rcpt_...",
    "output_commitment":"sha256:...",
    "execution_signer_id":"sig_...",
    "signer_authorization_ref":"tos:...",
    "proof_status":"verified",
    "network_proof_ref":"tos:..."
  }
}
```

## Provider Federation

Managed/Verified proxy path:

```text
Client Agent -> atos.im A2A Gateway -> remote Agent Card -> remote A2A Agent
```

Native/federated path:

```text
Client Agent -> any ATOS resolver/gateway -> TOS Capability resolution -> provider A2A endpoint
```

The caller receives the same ATOS Job/Receipt semantics in either case.

For Native, canonical trust/proof state must remain independently verifiable even if the routing gateway is replaced.

## A2A Invariants

1. A2A Task maps to one ATOS Job.
2. `auto` is allowed only before Quote resolution.
3. Quote-bound Task/Job uses one concrete trust mode and proof profile.
4. Verified uses `tos_verified_v1`; Native uses `tos_native_v1` or stronger compatible profiles.
5. A2A extension carries ATOS commerce/proof state without modifying core A2A semantics.
6. Artifact bytes remain off-chain; commitments may be included in Verified/Native Receipts.
7. Native routing does not require `a2a.atos.im` as the canonical intermediary.
8. No remote agent or gateway may silently downgrade a quoted trust mode.
9. An OpenTask is never represented as an A2A Task or wrapped in the `message/send`/Task/Message model -- it is carried only through the dedicated `openTasks/*` method namespace, kept disjoint from the `tasks/*` namespace reserved for Job-mapped Tasks (Invariant 1).
10. `openTasks/proposals/submit`/`openTasks/proposals/withdraw` require `open_task_proposals:write`; this scope is never implied by `open_tasks:write` or any other scope.
11. `openTasks/proposals/accept` never accepts a caller-supplied price, trust mode or Capability override -- the resulting Quote/Job always uses the task owner as principal and is priced through the existing Quote pricing rules.
12. Once an OpenTask's acceptance reaches `job_id`, that Job is addressable only through the ordinary `tasks/*` surface from then on -- `openTasks/*` never re-exposes a second view of an already-bound Job.
