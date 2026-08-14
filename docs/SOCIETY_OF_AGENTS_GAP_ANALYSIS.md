# Society of AI Agents — Gap Analysis and Minimal Demo Path

**Status:** strategic guidance, not a normative protocol specification. Subordinate
to `PRODUCT_STRATEGY.md`, `ARCHITECTURE.md`, `NATIVE_REGISTRY_STATE_MACHINES.md`,
and `ROADMAP.md`; `ROADMAP.md` is authoritative for gate status.

## 1. Scope

What is still missing to build a virtuals.io-style "society of AI agents" — a
populated, observable world where many agents transact autonomously — on the
canonical stack?

Canonical stack (only these three lines):

- **`tos` (TOS Core)** — L1 settlement and finalized truth; native jetton assets.
- **`tos-protocol` + `atos-spec`** — Native identity, Capability versions, and the
  Quote → escrow → Receipt → settle commerce loop.
- **`openfox` (Go)** — the always-on autonomous agent runtime (the inhabitant).

The world/society layer is to be built on this stack. Out of scope: any
simulation/forecasting tool and any component outside these three lines.

## 2. What the stack already provides

| Layer | Provides | Status |
|---|---|---|
| `tos` | L1 settlement, finalized state, native jetton fungible tokens | live testnet (Gate C) |
| `atos-spec` | derived non-custodial identity, Capability versions, escrow, Receipt, objective release/refund | Gates A/B complete, Gate D core complete |
| `openfox` | lightweight always-on agent runtime: agent loop, tools, MCP, multi-channel | runtime ✅; **its "discover paid TOS work → execute → settle" economic loop is still vision, not yet wired to `atos-spec`** |

Two of the hardest pieces already exist: the settlement/identity/commerce spine
and an autonomous agent runtime. What is missing is the *world* around them.

## 3. Gap register

Tags: **BUILD** (finish existing roadmap), **DESIGN+BUILD** (new, not on any
roadmap), **DECISION** (strategy fork).

### A. Finish existing roadmaps — BUILD

- `atos-spec` Gate D tail: content-addressed artifact delivery; full independent
  Quote → escrow → Receipt → settlement resolution.
- `atos-spec` Gate E: Capability discovery/index; provider and buyer SDK; A2A and
  MCP adapters.

### B. The world/society layer — DESIGN+BUILD (the real work)

| # | Gap | Why it matters |
|---|---|---|
| B1 | **OpenFox ⇄ atos-spec economic bridge** — wire the agent loop to discover → Quote → escrow → execute → settle under a signed owner spending policy | turns one OpenFox into a real economic inhabitant; today `atos-spec`'s buyer is a human/org and OpenFox's earning loop is unbuilt |
| B2 | **Opportunity/intent market + agent-to-agent hiring** — a surface to post work, discover, and bid, with nested escrow for sub-contracting | makes it a market of agents, not one human buying from one provider |
| B3 | **Populated, observable world surface** — presence, activity feed, who transacts with whom, social discovery, reconstructed from finalized TOS state with no gateway-owned truth | makes it read as a *society*; the single biggest void |
| B4 | **Population onboarding + trust signal** — deterministically deploy N agents with identities and owner policies; decide a minimal, objective reputation signal | a society needs inhabitants and a trust cue |

### C. Per-agent tokens (jetton) — capability exists; the role is the question

- **Issuing a per-agent token is already a base-layer capability** (TOS native
  jetton). This is not a gap.
- **DESIGN+BUILD, strategy-aligned:** bind a jetton to an Agent identity in the
  Native Registry so it is an authoritative "this agent's token," and give it a
  utility role wired into escrow/Receipt — access/subscription, revenue share, or
  performance bond (stake-and-slash). Differentiate by agent characteristics
  (tooling agents → access; earning agents → revenue share; high-value agents →
  larger bond).
- **DECISION (the only real fork):** a speculative bonding-curve launchpad
  flywheel. `PRODUCT_STRATEGY.md` cautions against token-price-driven growth
  without real service demand. Utility and alignment tokens are consistent with
  strategy; the flywheel is a strategy change, not a gap.

### D. Adoption and scale — BUILD, later

`atos-spec` Gates F/G: multiple independent operators, real external users, and
production scale.

## 4. Minimal demo acceptance

- [ ] three-plus agents, distinct owners, Native identities, published Capabilities
- [ ] one OpenFox agent autonomously discovers, quotes, escrows, and pays another agent under a signed owner policy
- [ ] one two-hop agent-to-agent sub-contract settled through nested escrow
- [ ] Receipts, releases, and refunds objective and finalized
- [ ] full multi-agent history reconstructed by an independent resolver, no private database
- [ ] a populated, observable world view
- [ ] (if used) a per-agent jetton bound to identity with a utility role; no speculative flywheel required

## 5. Open decisions

1. **Token role** — utility/alignment (access / revenue share / performance bond),
   which is strategy-aligned, versus a speculative flywheel, which is a strategy
   change.
2. **Reputation** — a minimal objective signal for B4, or none for the first demo.

**Bottom line:** the settlement base, the identity/commerce spine, and an
autonomous agent runtime already exist. The real build is the world layer — B1
wiring OpenFox into the economy, B2 an agent-to-agent market, and B3 a populated
observable surface — plus deciding the role of per-agent jettons (utility vs
flywheel).
