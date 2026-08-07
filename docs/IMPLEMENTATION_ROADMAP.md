# ATOS Implementation Roadmap

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
- provider delivery flow
- provider earnings
- disputes

## Phase 3 — Provider Self-Service

Add:

- `atos_register_capability`
- endpoint adapters for HTTP/MCP/A2A
- health checks
- schemas validator
- provider Agent Cards
- sandbox certification

## Phase 4 — TOS Network Integration

Replace internal centralized functions progressively:

- Agent identity -> TOS identity
- capability attestations -> TOS
- discovery anchoring -> TOS
- reputation attestations -> TOS
- settlement proofs -> TOS
- machine payment -> TOS

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
