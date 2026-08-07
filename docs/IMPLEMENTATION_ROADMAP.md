# ATOS Implementation Roadmap

## Repository Layout

The `~/atos` implementation repo should follow this top-level layout so module
boundaries match `docs/ARCHITECTURE.md`'s planes from day one:

```text
atos/
├── cmd/
├── gateway/
├── mcp/
├── a2a/
├── api/
├── auth/
├── discovery/
├── search/
├── matching/
├── quote/
├── invoke/
├── jobs/
├── marketplace/
├── billing/
├── spending/
├── indexer/
├── agent-card/
├── events/
├── sdk/
├── skills/
└── web/
```

None of these packages should import a TOS Network client directly — only
`adapters/tos-ai` and `adapters/tos-core` packages (added in Phase 2 and Phase 4
respectively) may do so, per the Cross-Service Interface Contracts in
`docs/ARCHITECTURE.md`.

## Phase 0 — Contract First

Implement and freeze public v0.1 schemas before integrating deep TOS internals.

Deliverables:

- Agent Card
- Device Auth
- Capability/Quote/Invocation/Job models
- MCP tool definitions
- REST OpenAPI
- mock provider

## Phase 1 — Codex-First MVP

Goal: one Codex user can install ATOS, authorize, search, quote and invoke a capability.

Build:

1. `https://atos.im/skills/atos/SKILL.md`
2. Device Auth web flow
3. MCP Streamable HTTP server
4. `atos_search`
5. `atos_get_capability`
6. `atos_quote`
7. `atos_invoke`
8. `atos_account`
9. centralized Postgres registry
10. Stripe/credit-style accounting or internal test credits

Success criterion: from a clean Codex environment, one prompt installs/authorizes ATOS and a second prompt successfully buys a sandbox capability.

## Phase 2 — Async Agent Economy

Add:

- `atos_create_job`
- `atos_get_job`
- `atos_cancel_job`
- A2A gateway
- artifacts/files
- a real **tos-ai** provider/worker runtime behind the job model — `SubmitJob`,
  `GetJob`, `StreamJob`, `FetchResult`, `FetchReceipt` (Phase 1's mock provider is
  retired here, not before)
- provider earnings
- disputes

This is the phase where the `ATOS → tos-ai` interface in `docs/ARCHITECTURE.md`
becomes real rather than mocked. Trust/settlement still stay centralized in ATOS's own
ledger — do not pull `tos-core` forward into this phase.

## Phase 3 — Provider Self-Service

Add:

- `atos_register_capability`
- endpoint adapters for HTTP/MCP/A2A
- health checks
- schemas validator
- provider Agent Cards
- sandbox certification
- open task marketplace: publish/apply/accept flow (`atos_publish_task`,
  `atos_list_open_tasks`, `atos_apply_task`, `atos_accept_task_application`,
  and related query/cancel/withdraw tools) for work a client wants bid on
  rather than fulfilled by a single pre-selected capability. Deliberately
  not part of Phase 0/1/2: it needs a real queued/matched-provider model
  (multiple providers competing for one task) that synchronous
  capability invocation doesn't have a reason to build until providers
  other than tos-ai exist to compete.

## Phase 4 — tos-core Trust Integration

Replace internal centralized functions progressively, all routed through **tos-core**
(not tos-ai, which is already live since Phase 2):

- Agent identity -> `tos-core.ResolveAgentIdentity` (see `docs/AUTH.md` Agent Identity
  Migration)
- capability ownership/attestations -> `tos-core.VerifyCapabilityOwnership` (see
  `docs/CAPABILITIES.md` Ownership Anchoring)
- reputation attestations -> `tos-core.ReadReputation` / `UpdateReputationEvidence`
- escrow -> `tos-core.CreateEscrow`
- receipt verification -> `tos-core.VerifyExecutionReceipt`
- settlement -> `tos-core.SettleJob`
- settlement proofs -> `tos-core.ReadProof`, exposed via the optional
  `settlement-proof` endpoint

Keep all ATOS public client contracts unchanged.

## Phase 5 — Open Gateway/Federation

Allow third parties to run compatible ATOS gateways while sharing TOS discovery/settlement.

```text
Codex
  |-- atos.im gateway
  |-- partner gateway
  |-- enterprise private gateway
          \
           -> TOS Network
```

This is the step where ATOS becomes a reference gateway rather than a mandatory centralized choke point.
