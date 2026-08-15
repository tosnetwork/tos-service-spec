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
- **`tos-service-protocol` + `tos-service-spec`** — Native identity, Capability versions, and the
  Quote → escrow → Receipt → settle commerce loop.
- **`openfox` (Go)** — the always-on autonomous agent runtime (the inhabitant).

The world/society layer is to be built on this stack. FreeCity is the selected
first application profile for that layer; see
[`FREECITY_APPLICATION_V1.md`](FREECITY_APPLICATION_V1.md). It is an
application of the canonical stack, not a fourth authority layer.

## 2. What the stack already provides

| Layer | Provides | Status |
|---|---|---|
| `tos` | L1 settlement, finalized state, native jetton fungible tokens | contracts and earlier-domain evidence exist; fresh current-domain Gate C evidence remains pending |
| `tos-service-spec` | derived non-custodial identity, Capability versions, escrow, Receipt, objective release/refund | Gate A complete; migration-delta review and current-domain Gate C/D/E acceptance remain incomplete as recorded by `ROADMAP.md` |
| `openfox` | lightweight always-on agent runtime: agent loop, tools, MCP, multi-channel | runtime ✅; **its "discover paid TOS work → execute → settle" economic loop is still vision, not yet wired to `tos-service-spec`** |

Two of the hardest pieces already exist: the settlement/identity/commerce spine
and an autonomous agent runtime. What is missing is the *world* around them.

## 3. Gap register

Tags: **BUILD** (finish existing roadmap), **DESIGN+BUILD** (new, not on any
roadmap), **DECISION** (strategy fork).

### A. Finish existing roadmaps — BUILD

- complete the migration-delta review and fresh current-domain Gate C evidence;
- complete the Gate D external buyer/provider/resolver pilot on the current
  domain; and
- complete Gate E independent provider/buyer adoption and current-domain
  acceptance using the implemented discovery, SDK, A2A, and MCP paths.

Local implementation and pre-migration evidence do not satisfy those items.

### B. The world/society layer — DESIGN+BUILD

| # | Gap | Why it matters |
|---|---|---|
| B1 | **OpenFox ⇄ tos-service-spec economic bridge** — wire the agent loop to discover → Quote → escrow → execute → settle under a signed owner spending policy | design is frozen in [`OPENFOX_ECONOMIC_BRIDGE_V1.md`](OPENFOX_ECONOMIC_BRIDGE_V1.md); runtime integration and fresh paid session remain |
| B2 | **Opportunity and Agent hiring experience** — FreeCity supplies listings, social context, discovery, and human/Agent workflows over the existing Capability and Quote lifecycle | makes useful Agent work discoverable without creating a second marketplace authority; nested escrow remains a later expansion |
| B3 | **Populated, observable world surface** — FreeCity supplies residents, places, presence, activity, social discovery, and a projection of finalized TOS history | makes the economy read as a society while keeping FreeCity-local and observed facts distinct from TOS authority |
| B4 | **Population onboarding and minimal trust cues** — FreeCity links profiles to deterministic Agent identities and owner policies, then presents objective protocol history and clearly labelled operational signals | a society needs inhabitants and legible trust without a gateway-owned universal reputation score |

The [FreeCity Application Profile](FREECITY_APPLICATION_V1.md) defines the
authority boundary for B2 through B4. B1 remains an OpenFox integration
responsibility. FreeCity may operate supporting infrastructure, but finalized
TOS state remains the only authority for protocol facts.

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

`tos-service-spec` Gates F/G: multiple independent operators, real external users, and
production scale.

## 4. Minimal demo acceptance

- [ ] three-plus Agents with distinct accountable owners, current-domain
      identities, and published Capabilities
- [ ] one human-to-Agent machine-checkable software-work purchase through
      Accepted Quote, escrow, Receipt, and finalized terminal settlement
- [ ] one OpenFox buyer Agent autonomously discovers and purchases work under a
      signed bounded owner policy
- [ ] Receipts, releases, and refunds are objective and finalized
- [ ] a second Gateway or validator-backed resolver reconstructs the complete
      multi-Agent history without the FreeCity private database
- [ ] a populated FreeCity view distinguishes finalized TOS facts,
      FreeCity-local civic facts, and operational observations
- [ ] the current-domain evidence satisfies the applicable Roadmap gates; mocks
      and pre-migration evidence are visibly excluded

Two-hop subcontracting and nested escrow are not V1 acceptance requirements.
They remain provider-composition expansion work after recurring demand is
established.

## 5. Open decisions

1. **Token role** — utility/alignment (access / revenue share / performance bond),
   which is strategy-aligned, versus a speculative flywheel, which is a strategy
   change.
2. **Reputation** — a minimal objective signal for B4, or none for the first demo.

**Bottom line:** the settlement base, identity/commerce spine, and autonomous
runtime foundations exist, but current-domain and external acceptance remain
unfinished. FreeCity is the selected first society application for B2 through
B4; OpenFox integration supplies B1. The next proof is a populated, observable
FreeCity experience around one independently resolvable software-work lifecycle,
not a speculative token economy or a parallel source of protocol truth.
