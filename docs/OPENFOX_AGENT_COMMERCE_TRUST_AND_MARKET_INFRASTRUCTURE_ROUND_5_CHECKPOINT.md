# OpenFox Agent Commerce Trust and Market Infrastructure — Round 5 Design and Acceptance Checkpoint

**Status:** local implementation and bounded Round 5 run complete; local
acceptance gates passed, with production, external-demand, escrow, cost, and
independent-host claims explicitly remaining open

**Recorded:** 2026-09-02

**Normative effect:** none. This document does not define a new Intent,
counteroffer, Agreement, acceptance, cost, reputation, escrow, staking,
Validator, or Outcome protocol. Round 5 JSON files are local test artifacts,
not portable TOS Service Protocol objects or ROADMAP release evidence.

**Controlling design:** [Post-Experiment Delta
Design](OPENFOX_AGENT_COMMERCE_TRUST_AND_MARKET_INFRASTRUCTURE_DESIGN.md)

**Prior checkpoint:** [Round 4 Reconciliation and Run
Checkpoint](OPENFOX_AGENT_COMMERCE_TRUST_AND_MARKET_INFRASTRUCTURE_ROUND_4_CHECKPOINT.md)

**Controlling references:**

- [Product Strategy](PRODUCT_STRATEGY.md)
- [System Architecture](ARCHITECTURE.md)
- [Agent Intent Exchange V1](AGENT_INTENT_EXCHANGE_V1.md)
- [Agent Operation and Outcome Event V1](AGENT_OPERATION_OUTCOME_EVENT_V1.md)
- [Native Quote, Execution, and Settlement Model](SETTLEMENT.md)
- [Agent Economy Metrics V1](AGENT_ECONOMY_METRICS_V1.md)

## 1. Decision rule: reconcile before building

Round 4 produced repeated requests for safer negotiation, measured cost,
acceptance evidence, deployed escrow, independent operators and demand, and
machine-checkable generic terms. A repeated request is not evidence that the
protocol primitive is absent. Round 5 applies this order:

1. identify the existing authority and wire object;
2. identify whether the gap is protocol, deployment, instrumentation, or
   independent evidence;
3. add only the missing local infrastructure;
4. preserve the existing authority boundary; and
5. keep every unresolved quantity and claim explicitly unknown or not run.

| Concentrated Round 4 observation | Existing protocol or authority | Actual gap | Round 5 delta | Deliberately not built |
|---|---|---|---|---|
| Schema-safe negotiation and exact price precedence | Generic signed Intent, authenticated dialogue, Agreement V1, predecessor-linked revisions, PersonalAuthority, Portfolio, and final atomic reservation | Some otherwise usable model decisions supplied an amount inconsistent with the frozen Owner range | An explicit Round 5-only deterministic compiler canonicalizes offer fields from frozen bounds, records signed repair evidence, and converts an incompatible known choice to a fail-closed decline | No business API, `CounterOffer`, order book, AI spending authority, or second Agreement lineage |
| Measured cost evidence | Cost Observation V1 meanings and the existing owner-private Provider-usage journal | Most Provider calls omit usage and no authenticated price schedule, invoice, allocation, tax, or currency conversion exists | Reuse the durable call journal, retain reported usage and missingness, and keep monetary amount unknown | No token estimate presented as measurement and no invented monetary cost |
| Acceptance and service correctness | Agreement obligations, acceptance requirements, Outcome Event V1, and existing settlement adapters | Payload delivery does not establish buyer acceptance, correctness, usefulness, or complete service execution | Continue retaining source-bound delivery evidence and explicit unknown execution state | No second acceptance object, subjective oracle, or synthetic success assertion |
| Current-genesis escrow and refund | Existing Paid Demand and escrow lifecycle, including release, refund, and recovery paths | A fresh deployment, active service accounts, funding, and current-genesis evidence were not supplied | No escrow mutation is attempted without those preconditions | No duplicate escrow state machine or simulated on-chain success |
| Independent hosts, operators, and external demand | Carrier and RPC domain pinning already distinguish endpoints and network domains | This local environment has one host, one operator, and operator-funded participants | Record each process view and preserve the single-host boundary | No claim of Byzantine independence, external demand, product-market fit, or public-network finality |
| Typed generic commercial terms | Intent V1 ranges and Agreement V1 typed parties, amounts, obligations, evidence, billing, dispute, adapter, validity, and revision lineage | Deployment maturity and interoperability evidence remain incomplete | Continue compiling the accepted generic dialogue into the existing Agreement | No security-review, localization, data-sale, or staking-specific commerce schema |
| Validator reward attribution | Existing TOS multi-nominator pool and Elector | Round 4 used identity-bound proxy wallets on another genesis rather than the actual campaign Agent Accounts | Deploy the exact campaign Agent Account StateInit identities on one isolated accelerated genesis, nominate part of each test balance, and then run the market on that same genesis | No governance vote, `DelegateAgentV1` reuse, new pool, new Elector, new reward rule, or production capital authority |

The remaining cost, acceptance, escrow, external-host, and external-demand
items stay visible because evidence is missing. Suppressing the gap or adding a
duplicate object would be less correct than reporting it.

## 2. Deterministic negotiation repair

Round 5 keeps AI responsible for the commercial choice and explanation while
making the Owner-bound amount a compiled field rather than free model text.
The compiler receives only an already validated Round 5 runtime profile and
the frozen seller minimum, seller ask, buyer budget, and buyer maximum loss.
The campaign nonce is identity only and cannot enable behavior.

For a strictly decoded buyer decision:

- `accept` can compile only to the ask and only when budget equals ask;
- `counter` can compile only to the budget and only when it is inside the
  non-degenerate signed seller range;
- `decline` always compiles with no amount; and
- an impossible but known choice becomes a signed, explicitly marked decline.

A seller accepting a counteroffer can compile only the exact counter amount;
a seller decline carries no amount. The Round 5 parser requires exactly the
three non-null string fields `decision`, `amount_nanotos`, and `message`.
Duplicate keys, aliases or case changes, unknown fields, wrong types, invalid
enums, non-canonical strings, trailing values, and reserved audit-marker text
remain typed model-output failures. They are not guessed or repaired and they
cannot create a negotiation checkpoint.

The existing signed negotiation checkpoint retains the original bounded model
decision and amount, a digest of the canonical original model object, the local
repair profile, ordered repair dispositions, and matching markers inside the
signed messages. Validation reconstructs the original object and proves the
compiled result from the frozen bounds; a disposition is not trusted merely
because it is present. Resume requires canonical bytes, valid participant
signatures, the exact campaign run and sequence, exact frozen bounds, exact
message lineage, and agreement with those markers.

Round 5 also keeps an owner-private, run-and-sequence-scoped attempt journal.
The appropriate buyer or seller counter-decision attempt is incremented and
durably written before the Provider call. A crash therefore conservatively
consumes an attempt, and restart cannot reset the three-attempt ceiling. A
fourth attempt is rejected before either Provider is invoked. The repair
profile, exact dispositions, and source digest are carried through result
recovery, the campaign aggregate, financial summary, and closing-assessment
input. PersonalAuthority and the final atomic Portfolio reservation remain the
only spending and execution authorities.

Round 4 behavior and checkpoint bytes remain unchanged when the Round 5
profile is absent.

## 3. Same-genesis campaign Account nomination

The requested “vote some TOS to a Validator” is interpreted as **nominator
stake delegation through the existing multi-nominator pool**. It is not a
configuration vote, governance vote, Agent-controller delegation, service
payment, Gift, or Agreement settlement.

The local harness creates a fresh accelerated genesis and redeploys the exact
eight campaign Agent Account StateInit identities. Address equality alone is
not sufficient. Before use, the harness must preserve and verify:

- workchain 0;
- the owner wallet identity and controller public key;
- the fixed deployment ID;
- initial per-transaction, daily-limit, and timeout policy;
- metadata and service-endpoint hashes;
- the supported Agent Account code hash; and
- `build-state.address == manifest.target`.

Only the copied config's deployed-address cache is cleared before rebuilding.
No key material is exported from the existing vault. Three JSON-RPC processes
must expose the same actual zero-state, ConfigParam 19, and Agent Account
getters before the lifecycle can pass.

This is a same-address, same-StateInit identity on a **new genesis**. It does
not migrate Round 4 balances, history, task sequence numbers, or assets.

### 3.1 Cross-genesis replay isolation

Agent Account and wallet task signatures bind the chain `global_id`, but the
zero-state is not itself a signed task field. Reusing the legacy local
`global_id=3` with the same keys, address, epoch, and sequence could allow a
captured message to cross replay between local genesis domains.

Round 5 therefore deterministically derives a fresh positive int32 global ID
from both the exact campaign run ID and the owner-private durable genesis
attempt ID. A failed attempt and a fresh genesis for the same campaign run
cannot reuse the same signing domain. Evidence exposes only a domain-separated
SHA-256 commitment to that pair, never the private attempt ID. The harness
writes the derived value into genesis and reads it back from ConfigParam 19 on
every selected RPC process. The Round 5 consumer rejects zero, the legacy
value 3, or any mismatch with its exact environment and zero-state hashes.
Global ID is not part of Agent Account StateInit, so this isolation does not
change the campaign account addresses.

### 3.2 Fixed low-level harness boundary

The current production Economic Action Authority supports Agreement-bound
commerce custody effects. It does not define autonomous capital allocation to
a pool. Manufacturing a fake Agreement or broadening escrow authority would
conflict with the existing protocol.

For this one integration test, existing low-level Agent Account `task-send` is
used under these constraints:

- the pool address, deposit/withdraw body, amount, and time are fixed by the
  operator test code, never by model output;
- only the primary config may mutate accounts; secondary RPC configs are
  owner-read-only views;
- action identity binds the run, full network domain, deployment, Agent,
  pool, operation, amount, and body;
- an ambiguous broadcast is resolved only by matching the journal's original
  signed BOC, controller state, exact destination, value, and body against a
  strict majority of three distinct RPC process views;
- resolution never signs or broadcasts, conservatively leaves a non-majority
  result unresolved, and remains idempotent for an already proved winner;
- pool ledger acceptance, not Agent Account sequence advancement, establishes
  a deposit;
- deposit, reward, and at least one withdrawal finish before market readiness
  is published; and
- no low-level staking task runs after readiness or concurrently with market
  payment custody.

The ordering is material because low-level task-send and market payment have
different local journals. This experiment does not prove safe concurrent
staking and commerce writes. A future autonomous capital action requires a
separate reviewed design with a pool/code allowlist, maximum locked capital,
minimum liquid reserve, exact network and message binding, Writer Fence,
Portfolio reservation, and recovery rules.

## 4. Exact capital and accounting boundary

Each Agent Account receives a bounded 30 TOS operator capital contribution on
the new genesis. It sends exactly 5 TOS to the pool; the existing pool charges
1 TOS processing fee and records exactly 4 TOS principal. Approximately 25 TOS
plus later chain effects remains available before the market, so only part of
the test holding is nominated and two bounded campaign rounds are not starved
of liquidity.

| Observation | Accounting class |
|---|---|
| 30 TOS fresh-genesis funding | Operator capital contribution; not revenue |
| 4 TOS recorded pool principal | Locked asset; not expense |
| 1 TOS pool processing fee | Capital-operation cost; not service cost |
| Deposit, withdrawal, or market Gas | Separate chain cost; unknown unless exact current-run evidence exists |
| Positive pool-ledger delta | Accrued capital return |
| Election-derived reward floor | Attributable Validator reward lower bound |
| Withdrawal wallet credit | Locked-to-liquid asset movement; not a second reward |
| Direct campaign payment | Internal service revenue/spend inside the operator-funded ring |
| Provider usage | Operational observation; monetary cost unknown without qualified pricing and invoice evidence |

Eight deposits therefore attach 40 TOS, create 32 TOS locked principal, and
incur 8 TOS of pool processing fees. A positive gross ledger reward does not
by itself establish net staking profit. Only an Agent with a completed payout
can claim liquid wallet credit; the other Agents can claim only positive pool
ledger credit. The exact ledger delta can include residual keeper value, so
the Elector-derived part remains a lower bound.

Validator capital return is excluded from market service revenue, buyer spend,
closed-economy service net, and Agent Economy Metrics V1.

## 5. Runtime phases and release gates

```text
source profiles + owner-private vault
                |
                v
fresh unique-global-ID genesis and five local Validators
                |
                v
redeploy and verify exact eight Agent Account StateInit identities
                |
                v
fund 30 TOS each -> send 5 TOS each -> pool records 4 TOS each
                |
                v
Elector selection observed in ConfigParam 34 -> recovery -> 8 positive ledger deltas
                |
                v
at least one payout -> seal delegation evidence -> publish ready
                |
                v
same accounts and genesis run the uninterrupted two-hour market
                |
                v
seal market, financial, Provider-usage, and closing-assessment evidence
```

The delegation lane must pass before the market starts. The network remains
available during the market so direct TOS payments use the exact same domain
and Agent Accounts. The local runner may stop only after the market evidence
has been sealed or the attempt has been explicitly aborted.

A qualifying delegation artifact must establish at least:

1. the exact campaign run ID and raw manifest digest;
2. a non-legacy global ID and exact zero-state root/file hashes read from the
   live chain;
3. all eight manifest targets as deployed, funded nomination accounts;
4. exact 5 TOS message, 1 TOS processing fee, and 4 TOS principal per Agent;
5. the pool's actual ledger key equal to each manifest target;
6. Elector selection of the pool Validator, observed in ConfigParam 34;
7. positive exact ledger delta and a positive election-derived floor for all
   eight active Agent accounts;
8. zero reward for a control deposited only after the stake became active;
9. at least one bounded positive withdrawal credit to the same Agent Account;
10. liquid and locked positions at market readiness; and
11. explicit accelerated-timing, operator-scripted, and single-host claim
    limits.

A qualifying market artifact must establish an uninterrupted process window
of exactly 7,200 requested seconds, the same campaign run ID, manifest,
network domain, and Agent Accounts, sixteen bounded decisions over two rounds,
eight closing assessments, and separately sealed Provider-usage evidence.

If no direct TOS payment finalizes, the result may say only that the market was
configured for the same genesis. It may call the genesis actually used for
market payment only when at least one current-run payment finalized there.

## 6. Evidence and operator limits

The local network exposes several node processes and three JSON-RPC process
views. They all run on one host under one operator. Process-specific hashes are
endpoint provenance labels, not organizational attestations. They do not
prove independent custody, Byzantine-independent quorum, independent
Validator finality, cross-host behavior, or external demand.

The delegation and withdrawal actions are operator-scripted low-level custody
harness actions. They are not autonomous OpenFox AI choices or
PersonalAuthority-approved capital decisions. Buyer AI remains autonomous only
within the bounded market-planning and negotiation role described by the
campaign profile.

The accelerated election timing proves real local contract and block
transitions. It does not establish production-duration liveness, storage-rent
economics, slashing safety, mainnet APR, annual issuance, or expected public
Validator selection.

## 7. No-duplicate-build record

Round 5 intentionally adds none of the following:

- a business-specific Intent endpoint or payload;
- another counteroffer, Agreement, acceptance, Outcome, reputation, cost, or
  billing object;
- a second Portfolio, speculative reservation, or AI-owned spending authority;
- another Paid Demand or escrow state machine;
- a governance-vote or Agent-delegation interpretation of nomination;
- a new staking pool, Elector, reward split, or issuance rule;
- a portable staking-evidence profile; or
- Validator reward fields in Agent Economy Metrics V1.

The new report, ready descriptor, negotiation repair fields, and same-genesis
delegation evidence are local harness artifacts. They document composition of
existing authorities rather than changing wire protocol.

## 8. Claims that remain open after a local PASS

Even a complete Round 5 local PASS does not establish:

- authenticated Provider pricing, invoices, total model/API monetary cost, or
  complete realized profit;
- buyer acceptance, usefulness, or service correctness beyond exact retained
  Outcome evidence;
- current-genesis Paid Demand escrow release, refund, dispute, or recovery;
- independently operated Owners, Carriers, RPCs, Validators, custody, or
  failure domains;
- malicious-counterparty, partition, clock-skew, refusal, disagreement, or
  cross-host resilience;
- customers, capital, or demand outside the operator-funded ring;
- autonomous staking selection or production capital management; or
- public-network readiness, product-market fit, mainnet yield, or ROADMAP gate
  completion.

The final operational report must preserve these open items rather than infer
them from negotiation repair, same-account nomination, or a two-hour local
process window.

## 9. Observed local acceptance result

The bounded run completed on 2026-09-02 under campaign run ID
`round5:df038cbfe136902e65f81cfe81067d9e48cb82a6562cc4756a36a04fcb1a0779`.
The immutable Agent manifest has the same raw SHA-256 suffix. The exact
qualifying process window was:

`2026-09-02T10:13:08.913386374Z` through
`2026-09-02T12:13:09.012666623Z`

The artifact records 7,200 observed seconds; the independent timestamp
difference is 7,200.099 seconds. Two earlier starts remain as incomplete
windows and are not combined with it.

| Acceptance item | Observed result | Classification |
|---|---|---|
| Two-hour process evidence | one completed uninterrupted 7,200-second window | `PASS_LOCAL` |
| Decisions and closing assessments | 16 decisions over two rounds; 8 of 8 non-empty assessments, no error | `PASS_LOCAL` |
| Direct TOS settlement | 6 unique transactions and 6 unique finality references; 7.8 TOS internal service volume | `PASS_LOCAL` |
| Negotiation compiler | 8 profiled results, zero invalid model objects, 2 V2 settlements, 2 incompatible choices compiled to decline | `PASS_LOCAL` |
| Outcome-informed history | local source-bound evidence changed later scope and willingness without a global score | `PASS_LOCAL` |
| Service correctness | 6 bound deliveries; all retain `service_execution=unknown` | `NOT_ESTABLISHED` |
| Provider usage | 97 calls; 15 with usage, 82 missing, 18 failed; monetary amount unknown | `PARTIAL` |
| Realized service profit | Provider price/invoice and chain-fee evidence absent | `NOT_ESTABLISHED` |
| Paid Demand escrow | no fresh deployment or funded service-account preconditions; no mutation | `NOT_RUN` |
| Cross-host malicious behavior and external demand | one host and operator; no external buyer | `NOT_RUN` |
| Exact campaign-Account nomination | 8 of 8 exact Accounts with positive reward on the payment genesis | `PASS_LOCAL` |
| Liquid nomination payout | one Account received a bounded wallet credit | `PASS_LOCAL_ONE_ACCOUNT` |

The service-payment result consists of four delivery-evidence-verification
sales and two TOS cost-and-settlement-audit sales. No domain-output capability
sold. Gross seller receipts and buyer spend are both 7.8 TOS, so internal
transfer net is zero. The 1.2 TOS maximum internal cost aggregate is a declared
ceiling; subtracting it produces a closed-economy projection of -1.2 TOS, not
realized profit.

### 9.1 Negotiation observation

All eight sequences that reached negotiation persisted one seller quote and
one buyer decision on the first strict attempt. The two accepted counters also
persisted one first-attempt seller counter decision. No attempt journal records
an invalid model output.

Four settlements used Agreement V1. Two used Agreement V2 with exact
predecessor digests, at 1.1 and 1.2 TOS. In the two remaining negotiation
conflicts, the model returned `counter` with the exact seller ask. The compiler
did not reinterpret that choice as acceptance; it produced signed
`buyer_incompatible_choice_declined` evidence. This closes the prior malformed
amount retry gap for the tested ask/budget profile. It does not establish
general bargaining, scope exchange, auctions, or order-book price discovery.

### 9.2 Same-genesis nomination observation

The fresh network used global ID `1417268827` and the following domain:

- zero-state root:
  `sha256:835634b48209288c21e872d89b6c55cd0783a1f5397da978168a83ef0ee19772`;
- zero-state file:
  `sha256:b83b85151e0026f0382cc66b2aea1136a0cb17fe0f7ee7bab60f75e47e6b8e43`.

For each of the eight exact campaign Agent Accounts:

- configured deployment contribution was 30 TOS;
- observed pre-deposit wallet balance was 29.999992150 TOS;
- the pool message was 5 TOS;
- the existing pool retained a 1 TOS processing fee;
- recorded principal was 4 TOS;
- exact ledger reward was 12.758141727 TOS; and
- election-derived attributable reward floor was 12.720651240 TOS.

The aggregate principal is 32 TOS. Aggregate exact ledger reward is
102.065133816 TOS, while the strictly attributable election floor is
101.765209920 TOS. A post-stake control received zero. One exact Agent Account
received a 16.758133553 TOS withdrawal credit including returned principal.
The withdrawal is not a second reward.

At least one current-run direct-TOS payment also finalized through the exact
same genesis and campaign Accounts, so the result may state that the domain was
actually used for campaign payment rather than merely configured.

These figures remain test-only accelerated-election observations. The
delegation and withdrawal were operator-scripted low-level harness actions,
not AI investment decisions or PersonalAuthority capital actions.

### 9.3 Startup incidents and resolved implementation defects

The first incomplete market start failed after service delivery and before
payment because the executable path had writable ancestors. The trust gate
correctly rejected it. Round 5 startup now pins an Owner-only executable before
any payer bind or Provider construction, revalidates the pathname for each
launch, executes one sealed snapshot, and requires all eight bindings before
Provider construction. Stable action recovery completed the retained delivery
and paid once.

The second incomplete start failed release-profile network preflight because
the generated RPC locator used a non-canonical origin form. The TOS lifecycle
generator and all three generated configs now use exact `/jsonRPC` locators.
Readiness evidence exposes the same locators, and regression tests reject the
origin and trailing-slash aliases.

These are runtime trust and deployment-generator fixes. Neither changes an
Intent, Agreement, payment, pool, Elector, or consensus protocol.

### 9.4 Validation performed

- The full OpenFox earning package passed after final source hardening.
- Focused negotiation, startup-order, sealed-executable, payment-preflight,
  race, and vet checks passed.
- TOS nominator-pool encoding and generator checks passed 51 of 51 tests;
  Ruff, format, and Python compilation checks passed.
- Final artifact review recomputed the exact process duration, all result and
  financial totals, transaction uniqueness, Provider summary digest,
  Validator evidence digest, exact Agent Account identities, reward totals,
  payout, control result, and 8 closing assessments.
- Independent protocol review found no duplicate-protocol blocker and required
  the `NOT_RUN`, `PARTIAL`, and `NOT_ESTABLISHED` claims above to remain.

The immutable campaign binary predates small post-run regression-test seams and
the generator source fix. The run proves the frozen binary behavior. The final
worktrees prove the subsequently hardened source tests; this checkpoint does
not conflate the two.
