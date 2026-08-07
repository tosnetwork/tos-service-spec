# ATOS Agent Internet Specification v0.2

**Status:** Draft  
**Date:** 2026-08-07  
**Product:** ATOS (`atos.im`)  
**Network:** TOS Network

> **ATOS is an open protocol for discovering, invoking, coordinating, verifying, and settling capabilities across the Agent Internet.**
>
> **atos.im is the canonical reference gateway and managed service.**
>
> **TOS Network is the decentralized identity, registry, trust, proof, and economic substrate underneath ATOS.**

ATOS gives Codex, Claude Code, Cursor, OpenClaw, Hermes and other agents one compact interface for discovering, invoking, publishing and paying for capabilities without requiring ordinary clients to understand wallets, validators, gas, node topology, or settlement internals.

## Core Product Model

ATOS provides one protocol with three concrete trust modes:

```text
managed   = atos.im may complete the transaction as a centralized managed service
verified  = atos.im UX may remain centralized, but critical trust/economic checkpoints are TOS-verifiable
native    = TOS-backed trust/settlement plus gateway-independent canonical resolution
```

Clients may request:

```text
requested_trust_mode = managed | verified | native | auto
```

`auto` is a pre-Quote policy only. `atos_quote` always resolves it to:

```text
trust_mode = managed | verified | native
```

The resolved mode is immutable for that Quote. Verified/Native work MUST NOT silently downgrade to Managed.

Providers separately request desired concrete modes through `requested_trust_modes`; public `supported_trust_modes` contains only modes that ATOS has actually activated/certified for the Capability.

Initial standard proof profiles:

```text
verified -> tos_verified_v1
native   -> tos_native_v1
```

**Decentralization is a selectable trust level, not a usability requirement.**

## Architecture

```text
Codex / Claude Code / Cursor / OpenClaw / Hermes
                      |
                 ATOS Skill
                      |
                  MCP / A2A
                      |
                 ATOS Protocol
                      |
         +------------+------------+
         |            |            |
      Managed      Verified       Native
         |            |            |
      atos.im       atos.im      any gateway
         |            + TOS         + TOS
         +------------+------------+
                      |
                  Capability
                      |
              Provider / tos-ai
                      |
                   tos-core
                      |
                 TOS Network
```

Plane boundary:

```text
atos.im / gateways = UX, discovery, ranking, policy, routing, managed billing
tos-ai             = execution fabric/provider-worker runtime
tos-core           = trust/economy/proof adapter boundary
TOS Network         = identity, registry commitments, reputation evidence, enforceable escrow, proof, settlement
```

The blockchain is not the bulk execution data plane. Prompts, private files and large artifacts remain off-chain by default; Verified/Native modes commit the trust/economic facts and content hashes required for independent verification.

## Design Goals

1. **One-sentence onboarding** — an agent can install/read an ATOS Skill and complete Device Authorization.
2. **One client protocol** — Managed, Verified and Native do not fork MCP/A2A/REST APIs.
3. **Centralized product quality** — `atos.im` can compete directly with centralized agent marketplaces.
4. **Selectable verifiability** — users can require TOS-backed proof without becoming blockchain operators.
5. **Open Native network** — Native capabilities survive without `atos.im` as the canonical gateway/namespace authority.
6. **No wallet requirement for mainstream clients** — fiat/credits/sponsored settlement may abstract the provider settlement asset.
7. **Machine-safe spending** — Quotes, max-price constraints, idempotency and explicit approval bind financial commitment.
8. **Small MCP surface** — an ordinary consumer sees 9 stable tools; provider/administrative tools appear only when the request authorization and role/resource preconditions permit them.
9. **Portable Proof-of-Service** — authorized-signer execution receipts become verifiable reputation evidence.
10. **Opaque providers** — capabilities expose public contracts, not private prompts, memory, secrets or topology.

## Public Entry Points

| Purpose | Production endpoint |
|---|---|
| Website | `https://atos.im` |
| API | `https://api.atos.im/v1` |
| MCP (Streamable HTTP) | `https://mcp.atos.im/mcp` |
| MCP legacy SSE compatibility | `https://mcp.atos.im/sse` |
| A2A reference gateway | `https://a2a.atos.im` |
| Agent Card | `https://atos.im/.well-known/agent-card.json` |
| Agent Card compatibility alias | `https://atos.im/.well-known/agent.json` |
| Skill | `https://atos.im/skills/atos/SKILL.md` |
| Skill package | `https://atos.im/skills/atos/atos-skill.zip` |

## Core Business Objects

The canonical discoverable supply unit is always a **Capability**.

- **Capability** — discoverable unit of supply, with derived active concrete trust modes.
- **Quote** — immutable time-limited commercial/trust contract that resolves the concrete trust mode.
- **Invocation** — bounded/synchronous execution attempt inheriting Quote mode.
- **Job** — stateful asynchronous unit of work inheriting Quote mode.
- **Artifact** — structured/file deliverable; bytes normally remain off-chain.
- **Provider** — agent, API, human-operated service, execution node, or other supplier.
- **Execution Signer** — provider or authorized delegated runtime that signs execution evidence.
- **Execution Receipt** — signed evidence of what was executed and settled.
- **Proof-of-Service** — portable evidence graph derived from receipts/outcomes.
- **Account** — gateway-local identity, spend and earning policy where applicable.
- **Settlement** — Managed or TOS-backed accounting/payout according to the Quote.

## MCP Tool Visibility

The ordinary consumer surface is intentionally **9 tools**:

1. `atos_search`
2. `atos_get_capability`
3. `atos_quote`
4. `atos_invoke`
5. `atos_create_job`
6. `atos_get_job`
7. `atos_cancel_job`
8. `atos_account`
9. `atos_artifact` (`operation`: `create_upload` / `complete_upload` / `get_download_url`)

`atos_artifact` is always present because any consumer may select a Capability whose schema requires file input/output. The three signed-URL operations remain one model-visible intent rather than three tools.

Provider tools are **not** part of the ordinary consumer vocabulary. `tools/list` is computed from the authorization carried on that request and then from relevant role/resource preconditions. Examples:

```text
capabilities:write
  -> atos_register_capability
  -> atos_update_capability

capabilities:write + provider role/ownership
  -> atos_list_my_capabilities
  -> atos_pause_capability

provider_jobs:read
  -> atos_provider_jobs        (when implemented)

provider_jobs:deliver
  -> atos_deliver_job          (when implemented)
```

Visibility is an optimization and usability boundary, not an authorization substitute: every `tools/call` MUST re-check the required scope and object-level authorization.

Because `tools/list` varies by authorization, ATOS returns it with private caching semantics and deterministic ordering. The v0.2 recommendation is:

```json
{
  "ttlMs": 30000,
  "cacheScope": "private"
}
```

ATOS does not vary the list from connection/session history or from earlier tool calls.

## Recommended Client Flow

```text
User intent / trust policy
   -> atos_search
   -> atos_get_capability (optional)
   -> atos_quote(requested_trust_mode, proof requirements)
   -> Quote resolves concrete trust_mode + proof_profile
   -> policy + spend check
       -> within autonomous policy: invoke/create job
       -> otherwise: MCP input_required / user approval
   -> result/artifacts
   -> authorized-signer receipt
   -> optional/required TOS proof + Proof-of-Service evidence
```

## Repository Map

- [`SKILL.md`](./SKILL.md) — Codex/agent onboarding and runtime policy.
- [`docs/ARCHITECTURE_V0.2.md`](./docs/ARCHITECTURE_V0.2.md) — normative v0.2 architecture and trust-mode guarantees.
- [`docs/PROOF_PROFILES.md`](./docs/PROOF_PROFILES.md) — normative `tos_verified_v1` and `tos_native_v1` guarantees.
- [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md) — historical v0.1 architecture retained for comparison during review.
- [`docs/MCP.md`](./docs/MCP.md) — MCP v0.2 tool, visibility and trust-mode contract.
- [`docs/A2A.md`](./docs/A2A.md) — A2A v0.2 profile.
- [`docs/AGENT_CARD.md`](./docs/AGENT_CARD.md) — Agent Card / mode advertisement.
- [`docs/AUTH.md`](./docs/AUTH.md) — Device Auth, tokens, scopes, tool visibility and identity binding.
- [`docs/CAPABILITIES.md`](./docs/CAPABILITIES.md) — Capability, global ID, mode activation, ownership and signer rules.
- [`docs/SETTLEMENT.md`](./docs/SETTLEMENT.md) — Managed/Verified/Native settlement and proof model.
- [`docs/ARTIFACTS.md`](./docs/ARTIFACTS.md) — signed-URL artifact transfer / content commitments.
- [`docs/API.md`](./docs/API.md) — REST API v0.2 semantics.
- [`docs/IMPLEMENTATION_ROADMAP.md`](./docs/IMPLEMENTATION_ROADMAP.md) — staged Managed -> Verified -> Native implementation plan.
- [`docs/TOS_RPC.md`](./docs/TOS_RPC.md) — ATOS ↔ tos-protocol RPC/protobuf implementation contract.
- [`schemas/mcp-tools.json`](./schemas/mcp-tools.json) — v0.2 MCP input/output schemas and visibility policy.
- [`schemas/protocol-types.json`](./schemas/protocol-types.json) — reusable trust-mode/proof/signer JSON Schema definitions.

## Compatibility Principles

- Prefer current MCP Streamable HTTP; keep legacy SSE only as a compatibility adapter.
- `tools/list` MAY vary by per-request authorization, MUST NOT vary from connection/session history, and SHOULD use deterministic ordering.
- Authorization-specific `tools/list` results use `cacheScope: private`; v0.2 recommends `ttlMs: 30000`.
- Publish the A2A Agent Card at `/.well-known/agent-card.json`, with compatibility aliases where useful.
- Use semantic versioning in public contracts and proof-profile names.
- Every financially committing operation requires idempotency protection.
- Every Quote contains concrete trust mode, proof profile when required, expiry, maximum price, settlement/proof contract, terms commitment and dispute-policy commitment.
- Never require an ordinary client agent to own TOS merely to consume a Capability.
- Never treat `auto` as a committed execution mode.
- Never treat provider-requested trust modes as already certified/active.
- Never silently downgrade a Verified/Native Quote.