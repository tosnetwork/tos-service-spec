# Decentralized Agent-to-Agent Use Cases

## 1. Purpose

ATOS adds decentralized identity, authorization, commerce, and settlement to
agent-to-agent interaction. It does not require every message or computation to
run on-chain.

A conventional A2A transport answers questions such as:

- how one Agent discovers another endpoint;
- how it sends a task;
- how progress and results are returned; and
- how errors and cancellation are represented.

ATOS additionally lets an Agent determine, without trusting one platform:

- who controls the provider Agent;
- which Capability and immutable version are being offered;
- whether the Agent, Capability, or version has been revoked;
- which endpoint and execution signer are authorized;
- which price, asset, escrow, expiry, and dispute terms were accepted;
- whether a receipt was signed by the selected execution authority; and
- whether funds were released, refunded, or placed in dispute.

The resulting model is decentralized A2A commerce rather than an on-chain
messaging system.

The scenarios below describe a long-term application portfolio, not parallel
initial-release commitments. Development starts with machine-checkable software
work and expands only after independent buyers and providers demonstrate
recurring paid use.

## 2. Interaction pattern

The target commercial interaction follows this sequence. The Registry and
resolution portion is implemented; Quote acceptance through settlement remains
the next roadmap gate.

```text
Agent A                         Agent B
   |                              |
   |-- resolve identity/state ----|
   |-- request Quote Proposal --->|
   |<------- proposal ------------|
   |                              |
   |-- commit Accepted Quote on TOS
   |-- fund required escrow on TOS
   |                              |
   |-- send off-chain task ------>|
   |<-- result + signed Receipt --|
   |                              |
   |-- settle/refund/dispute on TOS
```

Identity, Capability state, Accepted Quote terms, and economic outcomes are
canonical on TOS. Requests, intermediate messages, outputs, and large artifacts
normally remain off-chain and are bound by immutable digests.

## 3. Initial market: machine-checkable software work

An Agent can purchase objectively bounded software work from another Agent,
including:

- isolated compilation;
- deterministic test execution;
- static analysis;
- dependency and vulnerability scanning;
- reproducible builds; and
- bounded code transformation followed by tests.

The Accepted Quote identifies the exact Capability version, maximum price,
execution signer, deadline, toolchain commitment, and acceptance rule. A signed
Receipt binds repository commit, input digest, toolchain image, exit status,
test report, artifacts, usage, and charged amount to the selected provider.

This is useful when buyer and provider do not share an operator, account
database, or billing system. It is the initial market because results admit
objective checks and narrow release or refund rules.

## 4. Compute and infrastructure markets

Agents can autonomously buy resources such as:

- GPU or CPU execution;
- model inference and fine-tuning;
- zero-knowledge proof generation;
- compilation and isolated test execution;
- rendering and media encoding;
- storage, retrieval, or bandwidth; and
- confidential or hardware-attested computation.

The Capability manifest describes resource and evidence constraints. The Quote
binds selected capacity, endpoint, price ceiling, and signer. Usage included in
the Receipt drives settlement within the accepted bound.

## 5. Data markets

Agents can purchase access to:

- financial or market data;
- commercial and scientific databases;
- mapping, satellite, weather, or sensor data;
- blockchain analytics;
- licensed reports and archives; and
- real-time event feeds.

Raw data remains off-chain. On-chain commitments bind dataset version, license
or access policy digest, price, delivery digest, and Receipt. This supports
auditable delivery without publishing confidential or copyrighted content.

## 6. Multi-Agent supply chains

A coordinator Agent can decompose work across independent providers:

```text
coordinator
  |-- buys search from Agent B
  |-- buys data cleaning from Agent C
  |-- buys analysis from Agent D
  |-- buys chart generation from Agent E
  `-- returns the composed result
```

Each purchase has its own Accepted Quote, budget, execution identity, and
Receipt. The coordinator may include the subordinate receipt commitments in
its final evidence. This creates a traceable supply chain while keeping private
inputs and outputs off-chain.

## 7. Open task and bounty markets

An Agent can publish or solicit work such as:

- finding and fixing a software defect;
- identifying a security vulnerability;
- labeling or validating a dataset;
- producing a proof or optimization result;
- monitoring an external condition; or
- completing a research or content task.

Providers respond with Quote Proposals. The buyer selects one proposal, commits
an Accepted Quote, and funds escrow. The result is settled using the selected
policy rather than a gateway's private adjudication state.

## 8. Cross-organization automation

Organizations can expose Agents through independently operated gateways and
wallets. A buyer organization can resolve a provider's identity and Capability
directly from TOS, accept terms under its own policy, and reconcile settlement
from finalized transactions.

Examples include automated procurement, logistics coordination, compliance
checks, supply-chain data exchange, customer-support escalation, and business
process outsourcing. Neither organization must delegate canonical identity or
accounting to the other's gateway.

## 9. Machine and device commerce

Devices can transact under bounded controller and spending policies. Examples
include:

- vehicles buying charging, parking, maps, or connectivity;
- robots buying perception, planning, or remote-control assistance;
- drones buying weather, routing, compute, or data relay;
- edge devices selling sensor observations; and
- autonomous infrastructure buying maintenance diagnostics.

The wallet policy must bound assets, amounts, counterparties, Capability
classes, and frequency. High-value or unusual actions should require additional
controller approval.

## 10. Composable Agent businesses

A provider Agent may purchase lower-level services while fulfilling a
higher-level Accepted Quote:

```text
buyer -> report Agent
             |-> data Agent
             |-> analysis Agent
             `-> visualization Agent
```

Each relationship is a separate commercial contract. The top-level provider
remains responsible for its own Accepted Quote unless its terms explicitly bind
and disclose subordinate providers.

This model supports autonomous service businesses, resellers, brokers, and
specialized Agent networks without requiring one marketplace operator.

## 11. Asset roles

### TOS

TOS is well suited to protocol-native costs and incentives:

- transaction fees and contract deployment;
- registry mutations;
- spam resistance;
- relayer fees;
- protocol staking or penalties; and
- services priced directly in the TOS economy.

### TOS-network stablecoins

Supported stablecoins issued on TOS Network are well suited to commercial
services whose providers need predictable accounting:

- AI inference and professional work;
- compute time and storage;
- data licenses;
- enterprise procurement; and
- longer-running service agreements.

A common arrangement is to pay native TOS for network execution while
denominating the Agent service in a stablecoin issued on TOS Network. The
Accepted Quote names the exact TOS asset and issuing contract; neither gateway
nor provider may substitute another asset after acceptance.

## 12. Interactions that should not settle per message

It is inefficient to create an on-chain transaction for every token, progress
event, control signal, or low-value request. Suitable examples include:

- streaming model output;
- high-frequency device control;
- repeated calls within one workflow;
- internal calls among Agents under one operator;
- free discovery and health checks; and
- very small metered usage increments.

Use one of these patterns instead:

- one Accepted Quote for a bounded session;
- prepaid escrow with a strict spending ceiling;
- cumulative usage followed by one Receipt;
- periodic batch settlement;
- a payment channel; or
- free proposals followed by paid execution.

The preferred shape is:

```text
one finalized Quote and budget
        -> many off-chain A2A messages
        -> one or a few signed Receipts
        -> one final settlement
```

## 13. Selection criteria

ATOS is most valuable when at least one of the following is true:

- buyer and provider are operated by different parties;
- payment or escrow is required;
- Capability ownership or version must be independently checked;
- execution authority must be bound before disclosure of work;
- a signed result and auditable settlement are valuable;
- gateways must be replaceable; or
- multiple autonomous services are composed into one supply chain.

For a private, free, low-risk interaction inside one security domain, direct
A2A transport may be sufficient. ATOS should secure the trust and commercial
boundaries that require shared public facts, not add consensus overhead to
every message.

## 14. Implementation boundary

The Native Registry and direct resolution establish the identity and Capability
foundation. The first subsequent delivery is the software-work Quote, escrow,
execution, Receipt, release, or refund lifecycle. Broader scenarios in this
document advance only through the acceptance gates in `ROADMAP.md`. Product code
must not present a future commerce flow as canonical before its TOS contracts,
adapters, and conformance tests are complete.
