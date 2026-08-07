# ATOS Agent Gateway Specification v0.1

**Status:** Draft  
**Date:** 2026-08-07  
**Product:** ATOS (`atos.im`)  
**Network:** TOS Network  

> **ATOS is the gateway to the Agent Internet. TOS Network is the decentralized network underneath it.**

ATOS gives Codex, Claude Code, Cursor, OpenClaw, Hermes and other agents one simple interface for discovering, invoking, publishing and paying for capabilities. Client agents do not need to understand blockchains, wallets, validators, routing, settlement assets, or TOS internals.

## Design Goals

1. **One-sentence onboarding** — an agent can install/read an ATOS Skill and complete Device Authorization.
2. **Protocol-native** — MCP for tool use; A2A for stateful agent-to-agent work; REST for ordinary developers.
3. **Centralized UX, decentralized infrastructure** — `atos.im` is a stable gateway while identity, discovery, reputation, settlement and execution may progressively move to TOS Network.
4. **No wallet requirement for clients** — Codex users can operate with ATOS Credits or other supported payment methods; TOS settlement is an implementation detail.
5. **Machine-safe spending** — discovery is free; financially committing calls carry quote IDs, max-price constraints, idempotency keys and explicit policy/confirmation.
6. **Small MCP surface** — keep the default tool set compact enough for reliable model routing.
7. **Opaque providers** — external agents expose capabilities and contracts, not internal prompts, memory or chain topology.

## Public Entry Points

| Purpose | Production endpoint |
|---|---|
| Website | `https://atos.im` |
| API | `https://api.atos.im/v1` |
| MCP (2026 Streamable HTTP) | `https://mcp.atos.im/mcp` |
| MCP legacy SSE compatibility | `https://mcp.atos.im/sse` |
| A2A | `https://a2a.atos.im` |
| Agent Card | `https://atos.im/.well-known/agent-card.json` |
| Agent Card compatibility alias | `https://atos.im/.well-known/agent.json` |
| Skill | `https://atos.im/skills/atos/SKILL.md` |
| Skill package | `https://atos.im/skills/atos/atos-skill.zip` |

## Client Architecture

```text
Codex / Claude Code / Cursor / OpenClaw / Hermes
                      |
                 ATOS Skill
            onboarding + policy
                      |
              Device Authorization
                      |
          +-----------+-----------+
          |                       |
         MCP                     A2A
  tool discovery/calls    stateful collaboration
          |                       |
          +-----------+-----------+
                      |
               ATOS Gateway
                      |
       +--------------+--------------+
       |              |              |
  Discovery/Rank   Execution       Billing
       |              |              |
       +--------------+--------------+
                      |
              +-------+-------+
              |               |
            tos-ai         tos-core
   provider/worker runtime   identity / registry / reputation
   model, MCP, HTTP, GPU,    escrow / receipt verification /
   local, human adapters     settlement / proof
              |               |
              +-------+-------+
                      |
                 TOS Network
        consensus / P2P / ledger / settlement commitments
                      |
     Agents / APIs / humans / edge compute / services
```

## Core Business Objects

ATOS intentionally avoids splitting the Agent-facing protocol into separate Human Skill and Agent Capability models, as some prior art in this space does. The canonical unit is always a **Capability**.

- **Capability** — discoverable unit of supply.
- **Quote** — time-limited executable commercial offer for a capability.
- **Invocation** — immediate/synchronous execution attempt.
- **Job** — stateful asynchronous unit of work.
- **Artifact** — structured or file deliverable produced by an invocation/job.
- **Provider** — agent, API, human-operated service, or execution node supplying a capability.
- **Account** — client/provider identity and spending/earning policy at the ATOS gateway.
- **Settlement** — accounting and provider payout; may be backed by TOS Network without exposing chain details to clients.

## Default MCP Tool Set

The default MCP server exposes **11 tools**, not dozens:

1. `atos_search`
2. `atos_get_capability`
3. `atos_quote`
4. `atos_invoke`
5. `atos_create_job`
6. `atos_get_job`
7. `atos_cancel_job`
8. `atos_register_capability`
9. `atos_update_capability`
10. `atos_account`
11. `atos_artifact` (`operation`: create_upload/complete_upload/get_download_url — see `docs/ARTIFACTS.md`)

File transfer (11) is always visible: any caller might need it for any
capability with a file-typed field, so there's no reliable per-caller
signal to gate it on — its three steps are one tool with an `operation`
argument, not three separate tools, to keep the always-visible count
from growing every time this surface needs another verb. Provider/admin
tools are the one category actually gated — `tools/list` is computed per
request and includes them only for a principal that owns at least one
capability (see `docs/MCP.md`'s "Per-Caller Tool Visibility"). An earlier
draft kept file transfer out of the default list entirely, then a later
one exposed it as three separate always-visible tools (13 total);
testing against a real MCP client showed the first was simply
unreachable, and an independent review of the second flagged the
unnecessary tool-count growth.

## Recommended Client Flow

```text
User intent
   -> atos_search
   -> atos_get_capability (optional)
   -> atos_quote
   -> policy check
       -> under autonomous spend limit: atos_invoke / atos_create_job
       -> over limit: MCP input_required -> user confirmation
   -> result/artifacts
   -> transparent receipt
```

## Repository Map

- [`SKILL.md`](./SKILL.md) — install/onboarding/runtime instructions for Codex and other agents.
- [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md) — gateway/network separation.
- [`docs/MCP.md`](./docs/MCP.md) — MCP tools, resources and spend-safety contract.
- [`docs/A2A.md`](./docs/A2A.md) — stateful A2A profile.
- [`docs/AGENT_CARD.md`](./docs/AGENT_CARD.md) — discovery metadata.
- [`docs/AUTH.md`](./docs/AUTH.md) — Device Auth, tokens and scopes.
- [`docs/CAPABILITIES.md`](./docs/CAPABILITIES.md) — capability schema and matching.
- [`docs/SETTLEMENT.md`](./docs/SETTLEMENT.md) — ATOS Credits and hidden TOS settlement.
- [`docs/ARTIFACTS.md`](./docs/ARTIFACTS.md) — signed-URL file upload/download model.
- [`docs/API.md`](./docs/API.md) — REST API surface.
- [`docs/IMPLEMENTATION_ROADMAP.md`](./docs/IMPLEMENTATION_ROADMAP.md) — MVP phases.
- [`schemas/mcp-tools.json`](./schemas/mcp-tools.json) — compact machine-readable tool schemas.

## Compatibility Principles

- Prefer current MCP **Streamable HTTP**. Keep SSE only as a compatibility adapter.
- Publish the current A2A standard Agent Card at `/.well-known/agent-card.json`.
- Use semantic versioning in public contracts.
- Every financially committing operation requires an `idempotency_key`.
- Every quote contains `expires_at`, currency, total maximum and settlement model.
- Never require a client agent to own TOS merely to consume a capability.
