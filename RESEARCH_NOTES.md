# ATOS Design Decisions

## Prior Art Considered

Several existing agent-commerce and agent-marketplace platforms were reviewed while
shaping ATOS. Common surfaces observed across this class of platform include:

- Getting Started / Quick Start guides
- Agent Card discovery documents
- A2A JSON-RPC endpoints
- MCP protocol servers
- Integrations with coding/agent clients (e.g. IDE agents, autonomous coding agents)
- Authentication flows
- Capabilities/Skills registries
- Transaction and task lifecycle APIs
- Wallet/settlement APIs
- Guides covering skill registration, earning platform credits, agent deployment,
  and best practices

A typical Agent-facing architecture in this space uses:

- a Skill document for onboarding/initialization;
- MCP for long-running client tool access;
- A2A for agent-to-agent transaction/task lifecycle;
- an Agent Card for discovery;
- Device Authorization to issue credentials;
- a capability registry and matching layer;
- a platform-native settlement unit.

## Ideas Retained for ATOS

1. Skill-first onboarding.
2. Device Authorization.
3. MCP + A2A dual-protocol approach.
4. Machine-readable Agent Card.
5. Capability as the Agent-side supply object.
6. Synchronous direct invoke plus asynchronous transaction/job model.
7. Idempotency for financially meaningful writes.
8. Artifacts as first-class deliverables.

## Design Choices ATOS Makes Differently

### 1. Reduce MCP tool count

Some comparable platforms document upwards of two dozen MCP tools. ATOS's default
surface is 10 tools to improve model selection reliability and lower context/tool-routing
cost.

### 2. Use current MCP transport

Rather than relying primarily on SSE, ATOS uses 2026 Streamable HTTP as the primary
transport and keeps SSE only for compatibility.

### 3. Quote is first-class

ATOS inserts `atos_quote` between discovery and financial commitment. This gives the
agent a stable price ceiling, expiry and terms hash before spending.

### 4. Use MCP `input_required` for approval

If a quote exceeds autonomous spending policy, ATOS returns MCP `input_required`
instead of inventing a bespoke confirmation tool.

### 5. Standard Agent Card path

ATOS uses `/.well-known/agent-card.json` as primary; `/.well-known/agent.json` is
only an alias.

### 6. Remove user-ID header duplication

Rather than pairing an API key with a separate platform user ID, ATOS prefers a
scoped Bearer token that already identifies the principal.

### 7. Do not expose blockchain to consumers

ATOS clients see balance, quote, receipt and spend policy. TOS settlement is hidden
unless an advanced user requests a settlement proof.

### 8. Unify Agent-facing terminology

ATOS does not expose separate Human Skill and Agent Capability models to Codex.
Everything discoverable by an Agent is a Capability. Human providers can exist behind
a Capability adapter.

## External Standards Considered

- OpenAI/Codex Skills: `SKILL.md` as reusable, installable workflow guidance.
- MCP 2026-07-28: Streamable HTTP, reduced reliance on long-lived SSE, multi-round-trip
  input requirements, routable headers and trace propagation.
- A2A current specification: Agent Card at `/.well-known/agent-card.json`, opaque
  remote agents, tasks/messages/artifacts and extension mechanism.
