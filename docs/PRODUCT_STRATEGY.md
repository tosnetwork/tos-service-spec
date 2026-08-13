# ATOS Product and Commercial Strategy

**Status:** strategic guidance, not a normative protocol specification

**Planning horizon:** 2026–2027

## 1. Executive conclusion

ATOS is pursuing a credible and timely market: autonomous software will need to
discover, authorize, purchase, execute, and settle services across organizational
boundaries. The Native architecture is technically strong because it separates
public authority from gateway convenience and binds commercial execution to
finalized TOS commitments.

The opportunity is real, but protocol quality alone does not create a business.
ATOS succeeds only if independent buyers and providers complete recurring paid
transactions. Development must therefore move from broad protocol construction
to one narrow, production-quality commercial loop.

The strategic objective is:

> Make ATOS the open authority and settlement layer for high-value Agent work,
> while interoperating with established communication and payment protocols.

## 2. Market signal

The surrounding market validates the category:

- Google contributed A2A to the Linux Foundation, establishing open Agent
  communication as an industry concern. See the
  [Linux Foundation A2A announcement](https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents).
- Google's Agent Payments Protocol addresses delegated purchase intent,
  authorization, and accountability with participation from more than 60
  payment and technology organizations. See the
  [AP2 announcement](https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol).
- Visa's Trusted Agent Protocol addresses merchant recognition and safe Agent
  commerce. See the
  [Visa announcement](https://corporate.visa.com/en/sites/visa-perspectives/newsroom/visa-unveils-trusted-agent-protocol-for-ai-commerce.html).
- x402 demonstrates demand for programmatic stable-value-asset payments and has
  developed a substantial payment, cloud, and developer ecosystem. Its public
  site reports live transaction, volume, buyer, and seller metrics. See
  [x402](https://x402.org/) and its
  [ecosystem directory](https://www.x402.org/ecosystem).
- Ethereum proposals now cover on-chain Agent identity and Agent commerce. See
  [ERC-8004](https://eips.ethereum.org/EIPS/eip-8004) and
  [ERC-8183](https://eips.ethereum.org/EIPS/eip-8183).

These signals validate Agent commerce, but they also mean ATOS enters an active
standards market rather than an empty category.

## 3. Strategic position

ATOS should not replace every layer of the Agent stack.

```text
A2A and MCP
  communication, tasks, tools, progress, and result transport

x402 and AP2 adapters
  simple payment negotiation and delegated purchase interoperability

ATOS Native
  Agent authority, Capability ownership and versions, Accepted Quotes,
  execution binding, escrow, Receipts, disputes, and settlement

TOS
  final state, contract execution, fees, and economic security
```

ATOS differentiates itself by connecting identity, immutable Capability
versions, commercial terms, execution authority, result commitments, and
settlement in one independently resolvable lifecycle.

The product promise is not that every message is on-chain. The promise is that
every fact requiring shared trust is independently checkable after a gateway
fails or is replaced.

## 4. Target customer

The initial customer should be a developer or organization buying digital work
from a provider it does not operate. The customer values:

- exact service-version selection;
- budget and asset controls;
- escrow instead of unsecured prepayment;
- an execution identity fixed before sensitive input is disclosed;
- content-addressed outputs and signed Receipts;
- refund or dispute rules fixed before work begins; and
- accounting reconstructed from finalized transactions.

Internal, free, low-risk calls within one security domain do not need ATOS.

## 5. Initial market wedge

The first production market should be machine-checkable software work:

- isolated compilation;
- deterministic test execution;
- static analysis;
- dependency and vulnerability scanning;
- reproducible build artifacts; and
- bounded code transformation followed by tests.

This wedge fits the existing `tos-ai` execution foundation and produces outputs
that can be bound by repository commit, input digest, toolchain image, exit
status, test report, artifact digest, and execution Receipt.

It is preferable to an unconstrained general marketplace because acceptance and
failure are easier to specify, providers can automate delivery, and disputes
can refer to objective evidence.

After this loop works with independent operators, expand to paid data APIs,
batch inference, GPU jobs, and multi-Agent work supply chains.

## 6. Commercial lifecycle to finish first

Development should complete exactly one end-to-end path:

```text
resolve Agent and Capability
  -> obtain Quote Proposal
  -> accept Quote on TOS
  -> fund escrow
  -> dispatch one bound job
  -> receive artifact and signed Receipt
  -> release or refund escrow
  -> resolve the complete history through another gateway
```

Every step must work through documented public interfaces. A demonstration that
uses private database edits, operator shortcuts, or a shared hidden service does
not satisfy the product gate.

## 7. Business model

The protocol should remain open. Revenue comes from services that improve
availability, usability, risk management, and operations.

### Reference gateway services

- high-quality Capability search and ranking;
- reliable routing and low-latency relaying;
- hosted resolver and indexer APIs;
- wallet, budget, approval, and organizational policy tools;
- stable-value-asset checkout and accounting exports;
- risk, abuse, and compliance controls; and
- operational support and service-level commitments.

### Provider infrastructure

- hosted Agent and Capability publishing;
- worker deployment and autoscaling;
- signer and key-custody integration;
- metering, Receipt, and artifact services;
- provider analytics; and
- test and conformance certification.

### Enterprise products

- private or hybrid gateways;
- organizational wallets and spending policy;
- audit and reconciliation systems;
- approved-provider catalogs; and
- support, deployment, and integration contracts.

The reference gateway must earn revenue by delivering a better service, not by
making identity or transaction history portable only through itself.

## 8. Asset strategy

Use TOS and stable-value assets for different jobs.

### TOS

- contract execution and deployment fees;
- Agent and Capability registry operations;
- relayer costs and spam resistance;
- protocol staking, penalties, and incentives where required; and
- services voluntarily priced in the TOS economy.

### Stable-value assets

- software work;
- data and API access;
- compute, storage, and inference;
- enterprise procurement; and
- longer-running commercial agreements.

A practical transaction may use TOS for network costs while denominating the
provider service in a stable-value asset. The Accepted Quote fixes the exact
asset and amount bounds. Asset substitution after acceptance is forbidden.

The business must not depend on token price appreciation as its primary revenue
model.

## 9. Settlement efficiency

Do not put every message, output token, progress event, or metering increment in
a separate TOS transaction. Use:

- one Accepted Quote for a bounded session;
- prepaid escrow with a spending ceiling;
- cumulative usage Receipts;
- batch settlement; or
- payment channels for high-frequency flows.

On-chain operations should secure identity, authorization, commercial terms,
and terminal economic outcomes. Ordinary data transfer and computation remain
off-chain.

## 10. Durable competitive advantage

Contract source code is reproducible and therefore not a sufficient moat. ATOS
should build compounding advantages in:

1. useful Capability supply;
2. recurring buyer demand;
3. independently checkable execution and settlement history;
4. wallet, budget, and approval experience;
5. cross-gateway conformance;
6. reliable TOS finality and low transaction cost;
7. provider deployment and Receipt tooling;
8. enterprise stable-value-asset and accounting integration; and
9. developer onboarding measured in minutes, not weeks.

The strongest network effect is a market where providers earn recurring revenue
and buyers can compare and purchase services without bilateral integration.

## 11. Major risks

### No market liquidity

A technically complete registry with no useful services has little product
value. Provider and buyer onboarding must be developed alongside protocol work.

### Excess protocol scope

Building reputation, governance, generalized arbitration, every transport, and
every payment asset before the first commercial loop delays evidence of demand.

### Standards isolation

Requiring developers to abandon A2A, MCP, x402, or established wallets raises
adoption cost. ATOS should provide adapters and reuse stable conventions where
they do not weaken its authority model.

### Chain cost and latency

If Quote acceptance or settlement is slow or expensive relative to service
value, buyers will bypass the protocol. Sessions, batching, and channels must be
part of the product design.

### Weak outcome assurance

A valid signature proves who signed, not whether work is useful. The first
market must use objective output checks, reproducible artifacts, and narrow
dispute conditions.

### Key and budget compromise

Autonomous spending increases loss potential. Wallet policies, limited
allowances, recovery, anomaly controls, and human escalation are product
requirements, not optional polish.

### Regulatory and accounting burden

Stable-value-asset custody, conversion, sanctions controls, taxation, and
enterprise accounting vary by operator and jurisdiction. Protocol neutrality
does not remove operator obligations.

## 12. Explicit non-goals for the initial release

Do not prioritize:

- a universal marketplace for every kind of Agent;
- consumer retail checkout;
- subjective creative-work arbitration;
- a new general messaging protocol;
- per-token on-chain settlement;
- a proprietary provider transport;
- complex on-chain reputation scoring;
- cross-chain expansion before one TOS market works; or
- token-price-driven growth incentives without real service demand.

## 13. Development priorities

### Priority 0 — Complete authority foundations

- independent audit of the Registry contract and `nativecore`;
- public TOS testnet deployment;
- wallet-native registration, update, transfer, recovery, and revocation;
- multi-endpoint finalized resolution; and
- a second independent vector implementation.

### Priority 1 — Complete Native commerce

- Accepted Quote contract and transaction;
- stable-value-asset escrow;
- one bound software-work execution flow;
- canonical execution Receipt;
- release and refund;
- narrow objective dispute handling; and
- independent history resolution.

### Priority 2 — Make it usable

- provider SDK and deployment template;
- buyer SDK and wallet approval flow;
- A2A and MCP execution adapters;
- optional x402 payment adapter;
- searchable Capability index; and
- end-to-end examples that require no private operator action.

### Priority 3 — Prove openness

- two independently operated gateways;
- three independent providers;
- cross-gateway purchase and failover;
- public conformance suite; and
- reproducible operational evidence.

### Priority 4 — Expand only after recurring use

- data APIs and model inference;
- batch and channel settlement;
- provider composition;
- enterprise controls; and
- additional assets or networks justified by customer demand.

## 14. Twelve-month evidence targets

The following are product evidence targets, not protocol constants:

- at least 10 useful, purchasable Capabilities;
- at least 3 independently operated providers;
- at least 2 independently operated gateways;
- recurring transactions from buyers outside the core development team;
- real stable-value-asset settlement on a public TOS network;
- successful Quote-to-settlement completion through different gateways;
- documented provider earnings and buyer repeat usage;
- measured completion, refund, dispute, latency, and fee rates; and
- no canonical state that depends on a private gateway database.

Raw registration count, token price, social followers, and test transactions
are not substitutes for recurring paid usage.

## 15. Decision filter

Before starting a major feature, answer:

1. Does it help a real buyer purchase or check a real service?
2. Is shared authority required, or can it remain gateway-local?
3. Does it complete the first commercial lifecycle?
4. Can it interoperate with existing Agent and payment tooling?
5. Can two operators reproduce the result independently?
6. What measurable adoption or reliability outcome will improve?
7. What simpler implementation would test the same market assumption?

If a feature does not improve authority safety, commercial completion,
interoperability, or real market usage, defer it.

## 16. Strategic completion criterion

ATOS has crossed from protocol project to viable business infrastructure when
independent providers repeatedly earn revenue from independent buyers, either
gateway can fail without losing canonical state or accepted terms, and the
reference operator earns service revenue without controlling protocol truth.
