# Society of AI Agents — Gap Analysis and Minimal Demo Path

**Status:** strategic guidance, not a normative protocol specification.

This document is subordinate to `PRODUCT_STRATEGY.md`, `ARCHITECTURE.md`,
`NATIVE_REGISTRY_STATE_MACHINES.md`, and `ROADMAP.md`. Where it and any of those
disagree, they win. `ROADMAP.md` remains the authoritative source for gate status;
this document does not restate gate percentages, it maps the **delta** from the
implemented single-buyer commercial loop to a minimal multi-agent society demo.

## 1. Purpose and scope

A common question is whether the Native design can support a "society of AI
agents" application in the style of tokenized-agent marketplaces. This document
answers it concretely by separating three things:

1. what the current design already supplies as a substrate;
2. what is genuinely missing to run a minimal society-of-agents demo; and
3. what is deliberately out of scope by product strategy and therefore is not a
   gap to close.

"Society of AI agents" here means: many agents, each with an independent
non-custodial identity and one or more Capabilities, that **discover one
another, transact autonomously under owner policy, sub-contract work to each
other, and settle on finalized TOS state**, with the entire multi-agent history
independently resolvable and the population observable as a running world.

The current implemented lifecycle targets **one human or organizational buyer
purchasing from one provider**. A society is the same trust spine with
autonomous agent buyers, agent-to-agent composition, discovery, and a runtime
that gives the population behavior and observability.

## 2. What the current design already supplies (the substrate)

These exist today and are reused unchanged; see `ROADMAP.md` for exact status.

- **Agent and Capability identity** — derived, non-custodial, typed on-chain
  state machines with live policy authorization, delegation, recovery, atomic
  transfer, and revocation (Gates A and B).
- **Public-testnet authority** — reproducible Registry code, finalized
  multi-endpoint quorum resolution, wallet-native signing (Gate C, initial
  profile).
- **Commercial lifecycle core** — Accepted Quote, TOS-network stablecoin escrow
  with bounded fees, canonical Receipt, objective fixed-price release and
  timeout refund, provider execution, and a narrow objective dispute path
  (Gate D core, implemented).
- **Autonomous-spend primitives** — non-custodial agent wallets, per-target and
  per-wallet relay spend budgets, and delegation. These are the building blocks
  for an agent that pays without a human in the loop, but the autonomous buyer
  flow that drives them is not yet specified (see Gap II.1).
- **Trust modes** — managed / verified / native execution assurance, frozen at
  Quote time.
- **Articulated multi-agent markets** — `A2A_USE_CASES.md` already describes
  multi-agent supply chains, composable agent businesses, and open task markets;
  those sections are intent, not yet an implemented settlement mechanism.

Assessment: the substrate carries a society's economy and governance
(identity, ownership, authorization, escrow, Receipt, settlement, bounded
autonomous spend) and is more rigorous on the trust layer than SDK-only,
closed-contract peers. It does not by itself make a society *live*.

## 3. Definition of the minimal society demo

Accept the minimal demo when all of the following hold on a public TOS network,
within the machine-checkable software-work profile (no subjective evaluation, no
per-agent tokenization):

1. at least three agents exist, each with a distinct owner, a Native identity,
   and at least one published Capability;
2. at least one agent, acting autonomously under a bounded owner policy,
   discovers a Capability it does not own, obtains a Quote, funds escrow, and
   pays another agent for completed, objectively checked work;
3. at least one two-hop supply chain occurs: an agent hired for a task
   sub-contracts part of it to a second provider agent and settles both legs;
4. the complete multi-agent history — identities, ownership, accepted terms,
   Receipts, releases, refunds — is reconstructed by an independent resolver
   from finalized TOS state, with no private gateway database; and
5. the running population is observable as a world (who is transacting with
   whom, for what, and with what outcome).

## 4. Gap register

Each gap is tagged **BUILD** (implement work already on the roadmap),
**DESIGN** (new specification needed), **REUSE** (application/runtime layer,
above the protocol), or **OUT-OF-SCOPE** (deliberate non-goal, not a gap).

### Category I — Finish in-flight implementation (BUILD; already on the roadmap)

| # | Gap | State | Needed for demo criterion |
|---|---|---|---|
| I.1 | Content-addressed artifact delivery (bounded immutable storage) | roadmap in progress | 2, 4 |
| I.2 | Full independent Quote → escrow → Receipt → settlement resolution in production | roadmap in progress | 4 |
| I.3 | Minimal Capability discovery / index for finalized-state resolution | Gate E, not started | 2 |

Category I closes the single-lifecycle loop end to end and gives agents a way to
find each other. No new protocol facts are introduced.

### Category II — New design needed for a multi-agent society (DESIGN)

| # | Gap | What exists | What is missing |
|---|---|---|---|
| II.1 | **Autonomous agent-buyer flow and spend-policy object** | non-custodial agent wallet, relay per-target/per-wallet budgets, delegation | a specified decision-to-purchase flow where an agent selects a Capability, accepts a Quote, and funds escrow **under a signed owner spending policy**, with the policy as a first-class, resolvable object rather than relayer configuration |
| II.2 | **Agent-to-agent sub-contracting / nested escrow** | single Accepted Quote → escrow → Receipt; `A2A_USE_CASES.md` §6, §10 describe the intent | a composition rule for chaining Accepted Quotes so a provider agent can escrow and settle a downstream leg bound to its upstream obligation, without a gateway holding funds |
| II.3 | **Agent-facing discovery contract** | resolver over finalized typed state | a minimal, abuse-bounded query surface agents use to find Capabilities by kind and terms, kept separate from canonical state per `ARCHITECTURE.md` |
| II.4 | **Reproducible society population fixture** | deterministic registration vectors for one agent/Capability | a manifest that deterministically registers N agents, Capabilities, and owner policies, so the demo population is reproducible and independently verifiable |

Category II is the true protocol-level delta between "one buyer, one provider"
and "a society." It reuses the existing authority objects and must not create
parallel protocol facts or gateway-owned canonical state.

### Category III — Society runtime and observability (REUSE; application layer, above the protocol)

| # | Gap | Reuse source |
|---|---|---|
| III.1 | Agent personas and autonomous behavior loop (what an agent wants, decides, and does) | Mira persona generation and simulation engine |
| III.2 | Inter-agent messaging and task transport | A2A and MCP adapters (Gate E), mapping into the same Native objects |
| III.3 | Observable world: who transacts with whom, live population and outcome view | Mira world/reporting layer over finalized-state resolution |

The protocol anchors only trust-bearing facts. Personas, autonomy, messaging,
and the observable world are runtime concerns that live above `atos-spec` and are
supplied by a Mira-style application, not by the Native protocol.

### Category IV — Deliberately out of scope by strategy (NOT gaps)

Per `PRODUCT_STRATEGY.md` these are intentional non-goals and must not be treated
as missing capabilities:

- per-agent tokenization, bonding curves, and token-price growth flywheels;
- subjective creative-work evaluation and an open evaluator/reputation market;
- a universal marketplace for every agent type; and
- complex on-chain reputation scoring and generalized arbitration.

Reconsideration condition: revisit only after Gate F demonstrates recurring paid
demand and a specific, measurable customer outcome justifies the added scope, and
only in a way that reuses the existing authority objects.

## 5. Dependency ordering (path to the minimal demo)

1. **Phase 0 — close the loop.** Finish I.1 and I.2 so one autonomous-free
   lifecycle is fully independently resolvable end to end.
2. **Phase 1 — autonomous buyer.** Specify and implement II.1 and I.3 so an agent
   can discover, decide, and pay under a signed owner policy.
3. **Phase 2 — agent-to-agent composition.** Specify and implement II.2 and the
   II.4 population fixture so a two-hop supply chain settles.
4. **Phase 3 — society overlay.** Add III.1–III.3 (Mira runtime and
   observability) over the finalized-state resolver.

Each phase must preserve every earlier authority and security invariant, and
each phase's evidence must bind exact reviewed commits and release hashes, as
required by the roadmap.

## 6. Minimal demo acceptance checklist

- [ ] three-plus agents, distinct owners, Native identities, published Capabilities
- [ ] one autonomous agent purchase under a signed, resolvable owner spending policy
- [ ] one two-hop agent-to-agent sub-contract settled through nested escrow
- [ ] Receipts, releases, and refunds objective and finalized
- [ ] full multi-agent history reconstructed by an independent resolver, no private database
- [ ] observable running population
- [ ] no per-agent token, no subjective evaluation used to gate settlement

## 7. Open decision

The scope of Category II and IV depends on one product decision:

- **Objective-work agent society** — autonomous agents transacting for
  machine-checkable work with independent settlement. This is the direct
  extension of the current design; the gaps above are sufficient.
- **Tokenized-agent flywheel society** — per-agent tokens, speculative markets,
  and subjective reputation. This requires the Category IV scope that
  `PRODUCT_STRATEGY.md` currently defers, and is a strategy change, not a gap.

Resolve this before starting Category II design, because it determines whether
II.1 and II.2 are the full picture or only the settlement substrate beneath an
additional economic layer.
