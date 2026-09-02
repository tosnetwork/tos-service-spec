# OpenFox Agent Commerce Trust and Market Infrastructure — Round 4 Reconciliation and Run Checkpoint

**Status:** local implementation and evidence checkpoint; source validation and
the bounded Round 4 runtime passed

**Recorded:** 2026-09-02

**Normative effect:** none. This checkpoint does not release a new Intent,
CounterOffer, Agreement, reputation, cost, escrow, Validator-voting, staking,
or Outcome profile. The Round 4 report formats described here are local test
artifacts, not TOS Service Protocol wire objects or ROADMAP gates.

**Controlling design:** [Post-Experiment Delta
Design](OPENFOX_AGENT_COMMERCE_TRUST_AND_MARKET_INFRASTRUCTURE_DESIGN.md)

**Prior implementation record:** [Local Implementation
Checkpoint](OPENFOX_AGENT_COMMERCE_TRUST_AND_MARKET_INFRASTRUCTURE_IMPLEMENTATION.md)

**Source evidence:** [OpenFox Round 3 operational
report](https://github.com/tosnetwork/openfox/blob/7744ddaa407dde9a4a685130ca272ed3649fb07b/docs/operations/eight-agent-capability-market-round-3-report.md)

**Controlling references:**

- [Product Strategy](PRODUCT_STRATEGY.md)
- [System Architecture](ARCHITECTURE.md)
- [Implementation Roadmap](ROADMAP.md)
- [Agent Intent Exchange V1](AGENT_INTENT_EXCHANGE_V1.md)
- [Agent Operation and Outcome Event V1](AGENT_OPERATION_OUTCOME_EVENT_V1.md)
- [Native Quote, Execution, and Settlement Model](SETTLEMENT.md)
- [Agent Economy Metrics V1](AGENT_ECONOMY_METRICS_V1.md)

## 1. Why another checkpoint is necessary

The Round 3 recommendations do not mean that their underlying protocol
objects were absent. Most recommendations asked for stronger operational
evidence over capabilities already implemented after the earlier design and
review. Source presence, local tests, and one same-host campaign answer
different questions:

- a released or candidate object answers whether the requirement can be
  represented without another protocol;
- local implementation answers whether OpenFox can enforce or project it;
- a campaign answers whether the selected path actually ran under its stated
  conditions; and
- independent-host, current-genesis escrow, external-demand, invoice, and
  public-network evidence answer stronger acceptance questions.

Round 4 therefore reuses the existing commerce and chain mechanisms, adds
missing campaign instrumentation and an explicitly limited Validator
nominator test, and leaves the stronger unexercised claims open. It does not
reinterpret repeated Agent requests as permission to build parallel protocol
authority.

The source reviewed for this checkpoint is an uncommitted working tree. The
runtime result is therefore bound to the immutable campaign binary and final
artifact hashes, not to a falsely claimed source commit. Source conclusions
are limited to the separately tested final worktree at the base commits
recorded below.

## 2. Prior recommendation reconciliation

| Concentrated recommendation and Round 3 background | Capability that already exists | Actual remaining gap before Round 4 | Round 4 reuse or source delta | Duplicate authority deliberately not added |
|---|---|---|---|---|
| **Acceptance, escrow, and dispute handling; acceptance-quality separation (8/8).** Earlier Agents repeatedly wanted custody protection. Round 3 proved `provider_delivery=succeeded` while `service_execution` remained `unknown`, and its current-genesis Paid Demand preflight stopped before mutation. | Generic Agreement obligations already bind acceptance-evidence requirements, cancellation, dispute policy, dependencies, billing, and settlement adapters. Outcome Event V1 keeps delivery, acceptance, execution, dispute, refund, and finality assertions separate. Current escrow V1 supplies one fixed-price objective release/refund rail with exact chain authority. | A current-domain deployment, active buyer/provider service accounts, exact Quote-to-Agreement binding, and current-genesis release/refund evidence are still absent from this campaign environment. Delivery evidence still does not prove buyer acceptance or business quality. | Retain the existing Agreement, local Outcome views, direct-TOS path, and fail-closed Paid Demand availability checks. Round 4 does not weaken an unavailable escrow Adapter into a simulated success. Runtime evidence is pending. | No new escrow state, subjective quality oracle, adjudicator callback, global commerce state, or second dispute contract. |
| **Outcome-based reputation or trustworthy history (8/8 in the earlier recommendation set).** Earlier Agents wanted results, rather than names or claims, to inform later choices. Round 3 used qualified local delivery evidence but lacked a complete denominator. | Outcome Event V1 already carries positive, negative, ambiguous, corrected, and conflicting observations, event sets, cohort checkpoints, disclosure projections, and economic perimeters. OpenFox already computes separate Owner-local buyer-payment, provider-delivery, and service-capability outcome-risk views. | Independent retention and verification on two hosts have not run. Missing denominators remain unknown, and current observations do not prove correctness, usefulness, independence, or global reliability. | Continue importing only source-bound evidence and feed it into advisory local policy. Later Round 4 decisions may refer to retained evidence, but the runtime result is pending. | No portable reputation record, `.tos` trust flag, global score, or path by which history admits executable bytes, raises a budget, signs an Agreement, or releases funds. |
| **Cross-host malicious scenarios and broader untrusted settlement trials (at least 6/8 earlier; 8/8 in some form in Round 3).** Earlier rounds requested hostile publishers, refusal, nondelivery, partitions, replay, and independent operators. Round 3 still used eight logical Agents, two Carriers, and one operator on one host. | The existing ROADMAP, Work package E, semantic action recovery, Carrier neutrality, Writer Fence, Portfolio, and profile-specific adversarial matrices already define the required boundaries. | Independent Owners, hosts, Carrier failure domains, external counterparties, prompt-injection campaigns, partitions, clock skew, nondelivery, payment refusal, and endpoint disagreement have not been exercised together. | The two-hour campaign remains a same-host diagnostic. Its exact duration and same-host failure domain must be recorded; it receives no cross-host or Gate F/G credit. | No relaxed definition of “independent,” no synthetic host label, and no campaign-only consensus or recovery rule. |
| **Measured cost and Gas transparency (4/8 plus one explicit Gas request earlier; 8/8 measured-cost requests in Round 3).** Round 3's declared maximum cost was an admission reserve, not model/API cash cost. A later chain audit measured its five direct-payment fees, but model, API, tool, human-review, and opportunity cost remained unknown. | Cost Observation V1 already separates `declared_ceiling`, `estimate`, `usage_measured`, `payable_invoiced`, `cash_finalized`, `allocated`, `contra`, `penalty`, and `write_off`, with exact asset, category, direction, subject, policy, and evidence bindings. | The campaign had no provider-usage journal and no accepted model price, authenticated invoice, API/tool meter, or conversion evidence. Current-run chain fees also require their own finalized transaction binder. | Wrap every configured Round 4 `LLMProvider.Chat` call and retain owner-private per-Agent call counts, failed calls, missing-usage calls, and prompt/completion/total token counts when the Provider returns them. The aggregate report references the private summary by digest. Prompt, response, tool content, options, and provider error text are not retained. | No campaign Cost Observation wire schema and no conversion of tokens into money without exact price or invoice evidence. Measured tokens remain `amount_status=unknown`; unknown is not zero. |
| **Structured generic economic terms (at least 6/8).** Round 3 showed that price ranges, loss caps, acceptance criteria, and precedence should be machine-checkable while business meaning stays generic. | Intent V1 already carries bounded value ranges and settlement preferences. Application V2 can carry a complete proposed Agreement. Generic Agreement V1 already carries typed parties, obligations, amounts, dependencies, evidence, dispute, billing, adapter, validity, and predecessor-bound revisions. | Deployment maturity and independent interoperability remain incomplete. Some free-form business facts still need explicit promotion into the exact Agreement before authority. | Continue using one generic signed Intent, authenticated dialogue, and the existing Agreement compiler/verifier. No category-specific change is needed for security review, localization, data, API access, or other advertised work. | No per-business endpoint, trade schema, or parallel milestone object. |
| **Earlier Portfolio and capacity gating (at least 6/8).** Round 3 proved that aggregate maximum-loss policy can reject an Agreement, but some rejections occurred only after discovery and dialogue. | Owner Economic Action Authority, atomic Portfolio reservation, Writer Fence, stable action identity, and exact Agreement admission already protect signatures, execution, and payment. | An advisory observation can become stale immediately and therefore cannot authorize dialogue, signatures, execution, or payment by itself. The final atomic Agreement reservation remains necessary under concurrency. | Reuse the same aggregate `admitReservation` calculation through `CheckReservationCapacity`: filter infeasible sellers before the planner prompt, recheck the chosen seller before contact, and recheck immediately before demand/negotiation. Scheduled custody-expiry housekeeping matches Snapshot/Admit. The existing final `ReserveAgreement` remains the sole authoritative linearization point. | No second Portfolio, per-process budget, candidate reservation, or AI-owned capacity authority. |
| **Real price negotiation (3/8 in the earlier set) and exogenous demand.** Round 3 produced one actual V1-to-V2 counteroffer but price discovery remained shallow, and every buyer was also inside the same funded ring. | Natural-language negotiation, typed `AGREEMENT/PROPOSE`, exact predecessor-bound Agreement versions, accept, withdraw, and deterministic owner bounds already cover price and scope changes. | External buyers, committed downstream demand, deeper bid/ask discovery, and independently funded revenue remain absent. | Keep signed bounded dialogue and compile an accepted changed amount into an exact Agreement successor. The two-hour run can measure whether this repeats, but cannot make internal transfers external revenue. | No standalone `CounterOffer` wire object or global order book. |

## 3. New Validator delegation scenario is existing chain composition

The requested “vote some held TOS to a Validator” is interpreted as
**nominator stake delegation through the existing multi-nominator pool**. It
is not:

- `DelegateAgentV1`, which commits Agent controller/delegation authority;
- a governance or configuration-proposal yes/no vote; or
- a commerce payment, service purchase, Gift, or Agreement settlement.

The existing pool contract already accepts several nominators, combines their
principal with the Validator's principal, stakes through the Elector, assigns
a configured Validator reward share, credits remaining reward to active
nominators, queues withdrawals while staked, and pays withdrawals after
recovery. The missing infrastructure was safe multi-wallet operation,
machine-readable inspection, and one evidence-complete lifecycle tied to the
eight campaign identities.

The reviewed `tos` delta therefore reuses the pool and Elector unchanged:

1. `tosctl pool nominator deposit` and `withdraw` accept an explicit
   configured `--wallet`; omitting it preserves the existing owner-then-binding
   fallback.
2. `tosctl pool get --format json` reads the existing on-chain pool getters
   and emits exact pool data and nominator positions, with nanotos amounts as
   decimal strings.
3. The lifecycle runner requires the exact public eight-Agent campaign
   manifest, rejects missing or duplicate identity bindings, and commits its
   raw SHA-256 digest in the sidecar evidence.
4. Eight fresh basechain wallets each delegate only part of their funded
   balance. A ninth control deposits only after the pool is already staked and
   must receive zero reward for that round.
5. The runner requires the pool Validator to appear in elected ConfigParam 34,
   records every Agent proxy's before/after pool-ledger delta and an
   election-derived reward floor, and requires at least one exact positive
   withdrawal credit to a proxy wallet.
6. Queue blocking, permissionless recovery, payout, solvency, and return to a
   later election remain part of the same full lifecycle rather than being
   inferred from one balance snapshot.

These changes add no TOS Service Protocol object. The sidecar JSON schema name
is a test-harness artifact only. Nominator principal remains an asset placement,
not an expense; a Validator/nominator reward is capital income, not service
revenue; and processing or chain fees must remain separate costs.

## 4. Two independent evidence lanes

| Property | Two-hour OpenFox market lane | Validator nominator sidecar lane |
|---|---|---|
| Purpose | Observe eight AI-led buyers and sellers discovering generic Intents, screening, negotiating, declining or entering Agreements, executing bounded work, and using the enabled settlement path | Verify that eight identity-bound nominator proxies can contribute partial stake to one existing pool and receive a positive reward lower bound, with one wallet payout |
| Network | Current local three-node Agent-payment chain | Fresh, different-genesis local network with four initial Validators and a fifth spare identity |
| Runtime | Real minimum two-hour OpenFox process window for the explicit Round 4 profile | Accelerated complete election, selection, recovery, reward, and withdrawal lifecycle that should finish independently of the market window |
| Identities and funds | The eight campaign runtimes and their current campaign payment accounts | Fresh Wallet V1 accounts bound by manifest digest to the same logical Agent IDs, names, campaign wallet labels, and campaign account addresses |
| Timing | Ordinary campaign pacing; planned two rounds | Test-only ConfigParam 15 election timing. The production candidate's `stake_held_for=32768` seconds exceeds the experiment window; ConfigParam 16 also requires at least four Validators |
| Required evidence | Independent Round 4 report schema, uninterrupted process window, per-decision artifacts, final financial summary, closing assessments, provider-usage digest, and exact campaign-run nonce | Passing complete sidecar report with the same campaign-run nonce, ConfigParam 34 selection, eight positive ledger deltas no smaller than their election floors, zero-reward post-stake control, and at least one positive withdrawal credit |
| Economic treatment | Direct internal service transfers and exact current-run fees are reported only when finalized evidence exists; the same funded ring is not external revenue | Delegated principal, reward, and withdrawal are excluded from market service revenue, buyer spend, and closed-economy service net |
| What it cannot prove | External demand, independent operators, current-genesis escrow, public-network acceptance, or product-market fit | Actual same-genesis campaign-wallet delegation, an autonomous AI choice to stake, production liveness, storage-rent economics, slashing safety, mainnet APR, or annual issuance |
| Evidence status at this checkpoint | **PASS** for the exact same-host two-hour profile; 16 decisions, 3 direct-TOS settlements, and 8 closing assessments | **PASS** for the identity-bound, accelerated, different-genesis lifecycle; 8/8 proxy nominators received a positive ledger reward |

The two evidence lanes are linked by both the exact raw campaign-manifest
digest and the exact campaign-run nonce. The digest proves identity mapping,
and the nonce rejects artifacts from a different campaign run. A persistent
generation lock and durable sidecar-attempt marker separately protect a retry
that deliberately reuses the same nonce. The runner holds the lock exclusively
for the whole attempt; the campaign holds it shared from preflight through
final sealing. The marker is created before network setup, remains after a
hard failure, and makes OpenFox reject the older stable evidence until a new
result has been fsynced, atomically published, and the marker durably cleared.
Neither binding makes the fresh sidecar wallet the live campaign account,
merges the two genesis domains, nor turns a separate capital action into
market revenue.

## 5. Sidecar reward attribution boundary

The pool ledger's before/after change is exact for each nominator position.
The Elector-only part is deliberately reported as a lower bound because the
pool's recovery reply can combine returned Elector credit with residual keeper
message value. A passing artifact therefore requires:

- positive Elector returned credit above the exact staked principal;
- a positive election-derived floor for every active Agent proxy;
- an actual ledger increase at least as large as that floor;
- no reward for the control whose deposit was pending during that election;
- one exact positive wallet credit after withdrawal; and
- explicit claim limits preserving the accelerated, different-genesis proxy
  boundary.

It must not publish the complete ledger delta as an exact network-reward
attribution. It must not extrapolate the accelerated reward into APR, mainnet
yield, total issuance, or a guarantee that any production Validator will be
selected.

## 6. Round 4 campaign instrumentation boundary

The reviewed `openfox` delta adds an explicit Round 4 campaign profile rather
than weakening the legacy minimum-duration profiles:

- the selected profile requires capability-market mode and a minimum
  two-hour requested duration and uninterrupted process window;
- before reading or recovering campaign artifacts, it requires one validated
  `campaign_run_id` and an exact mode-`0600`, owner-private root marker. The
  report, every result source, every per-Agent provider-usage record and
  summary, the provider-usage aggregate/reference, and the delegation artifact
  must carry that same nonce; missing, duplicated, unknown, trailing, or
  mismatched identity data fails closed;
- it uses independent report, financial-summary, and closing-assessment names
  and schema identifiers, while legacy three-hour behavior remains unchanged;
- it requires a supplied passing nominator sidecar artifact and validates its
  schema, evidence class, network, campaign-run nonce, campaign-manifest
  digest, exact ConfigParam 34 selection, eight unique Agent bindings, pool
  identity, independently recomputed reward arithmetic, zero-reward control,
  and bounded positive withdrawal evidence before attaching a reference;
- it acquires the sidecar's persistent generation lock shared before
  preflight and holds it through final report sealing. Before each read it
  rejects the paired in-progress marker and repeats that check after reading
  the evidence and manifest. The runner holds the same lock exclusively,
  creates the marker exclusively and durably before a same-nonce attempt,
  fsyncs the final evidence before atomic replacement, fsyncs the directory,
  and only then removes and durably clears the marker;
- it records all configured LLM provider calls through the private usage
  recorder, including calls whose Provider omits or returns invalid token
  data. Before invoking the real Provider, the recorder durably creates an
  owner-private in-flight marker under a parent-and-child-directory-synced
  hierarchy. Recovery syncs the exact validated journal inode before removing
  a matched marker; an unmatched marker, poisoned recorder, or unresolved call
  cannot be finalized;
- it seals every per-Agent recorder under the same lock used to begin calls,
  then writes a content-addressed immutable aggregate; and
- it adds only that aggregate's digest and usage-count reference to campaign
  reports.

Provider usage is a measured quantity only when the configured Provider
returns a nonnegative usage object. Missing or invalid usage stays visible.
Even a complete token count does not establish a payable or finalized amount:
there is no accepted price schedule, invoice, discount, subscription
allocation, tax, currency conversion, or payment evidence in this delta.
Consequently model cost in money and complete campaign profit remain
`unknown`, not zero.

The usage journal is owner-private and metadata-only. It must not retain
prompts, responses, tool definitions, tool calls, model options, or Provider
error text merely to improve accounting.

## 7. No-duplicate-build record

Round 4 intentionally adds none of the following:

- business-specific Intent or commerce APIs;
- a `CounterOffer` message or another proposal lineage;
- another Agreement, obligation, milestone, acceptance, or billing object;
- a portable reputation dossier or global score;
- another Cost Observation class or Agent Economy Metrics meaning;
- partial release, subjective acceptance, chain `disputed`, fee splitting, or
  an adjudicator callback in escrow V1;
- another Agent delegation state machine; or
- a new staking, Elector, reward-split, or governance contract.

`Agent Economy Metrics V1` remains the narrow finalized stablecoin-escrow
aggregate described by its controlling document. It must not absorb direct
native-TOS market transfers, Provider token usage, Owner P&L, or Validator
rewards merely because all four appear in one operational report.

## 8. Required evidence before a post-run claim

The final operational record must separately attach or identify:

1. the OpenFox base commit, an explicit dirty-worktree disclosure, and the
   immutable campaign binary digest; an exact source commit may be claimed
   only after these changes are committed;
2. a qualifying uninterrupted process window of at least 7,200 seconds;
3. the eight-Agent manifest and its raw digest;
4. every decision disposition, negotiation lineage, Agreement version,
   execution result, payment identity, recovery result, and explicit unknown;
5. the owner-private provider-usage summary digest, observed/missing token
   counts, and `amount_status=unknown` unless separately qualified price and
   invoice evidence exists;
6. exact chain-fee evidence for current-run transactions before any Gas-cost
   claim;
7. the separate passing sidecar artifact, its pool code hash and address,
   ConfigParam 34 selection, eight reward proofs, control, withdrawal, and
   claim limits; and
8. the final source unit/integration checks in both changed repositories.

A campaign may pass its exact local profile while the following remain
uncompleted:

- live same-genesis campaign-payment-wallet nomination using the Agents'
  actual held campaign TOS;
- autonomous AI selection of staking as an earning action;
- a current-genesis Paid Demand deployment and complete funded
  release/refund/recovery session;
- portable buyer-acceptance and service-execution evidence beyond delivery;
- independently operated hosts, Owners, Carriers, Validators, and endpoint
  failure domains;
- malicious-content, partition, clock-skew, nondelivery, refusal, and
  disagreement campaigns;
- authenticated model/API/tool invoices and cash-finalized costs;
- buyers and funds outside the operator-funded campaign perimeter; and
- public-network, production-liveness, storage-rent, slashing, APR, recurring
  demand, or ROADMAP-gate acceptance.

## 9. Completed Round 4 evidence

The qualifying market process ran without restart from
`2026-09-02T02:49:41.830739700Z` through
`2026-09-02T04:49:41.857675863Z`. The process-window record reports exactly
7,200 observed seconds and `outcome=completed`; the enclosing Go test passed
after 7,609.34 seconds including closing assessments and evidence sealing.

| Evidence item | Completed observation |
|---|---|
| Campaign run scope | `round4:596f06f8f0b8fc2e24eac103098b83cf8bd990b52fd24e84afcbdb8b0f81d33e` |
| OpenFox base commit | `7744ddaa407dde9a4a685130ca272ed3649fb07b` plus the tested uncommitted Round 4 worktree |
| TOS base commit | `e68ce75ef5c0c0f74561585b6a6a04ca29800b57` plus the tested uncommitted nominator tooling worktree |
| Campaign binary SHA-256 | `825d361e1c815edd57ad353d26486cd7fed9e8a7e3ba3167a4fe9df4e911997f` |
| Manifest SHA-256 | `4d197150fa4e0471090b81420049db2a0848a66c617d39e37e57e9a7b40062a2` |
| Market decisions | 16: 3 settled, 4 invalid-model negotiation declines, 3 seller-strategy declines, 3 buyer-strategy skips, and 3 early Portfolio-capacity skips |
| Internal service volume | 4.1 TOS received and 4.1 TOS spent inside the same funded ring; transfer net exactly zero |
| Provider observations | 141 calls; 24 with usage, 117 with missing usage, 0 invalid usage, 8 failed; 190,901 reported-token subtotal for covered calls; total usage and monetary amount unknown |
| Closing assessments | 8 of 8 non-empty responses |
| Sidecar SHA-256 | `0fdbb8cb53d42411e013f7096b412d6f1262b43a82b30dd6c6383652f15a0bfb` |
| Delegated principal | 8 x 999 TOS = 7,992 TOS recorded principal, from eight fresh partially funded proxy wallets |
| Nominator reward | 102.029875672 TOS exact aggregate ledger delta; 101.729951768 TOS aggregate election-derived lower bound |
| Control and payout | post-stake control reward exactly zero; one proxy received 1,011.753733336 TOS including returned principal |

All three settled service records remain
`provider_delivery=succeeded;service_execution=unknown`. Their chain fee,
model cost, and API cost remain unknown. The 4.1 TOS is internal service
volume, not external revenue, and the 0.6 TOS declared maximum-cost aggregate
is an admission reserve, not realized expense. Nominator principal and reward
are capital activity and are excluded from both service revenue and spend.

Final validation passed for the OpenFox earning package, focused OpenFox race
tests, 33 TOS Python encoding tests, 18 Rust pool-command tests, Ruff, Rust
formatting, and repository whitespace checks. One unrelated existing Rust
unused-import warning was emitted.

A post-run independent review found that the runtime runner's atomic final
replacement did not itself invalidate an older PASS while a retry with the
same campaign nonce was still in progress. The final source now has the
generation-lock and durable attempt-marker handshake described above. This
correction is covered by focused Python and Go tests, but it was made after the immutable campaign
binary and sidecar completed; the report does not claim that the two-hour run
exercised that crash seam.

The completed evidence does not close the uncompleted list above. In
particular, it does not prove external demand or profit, buyer acceptance,
current-genesis escrow, independent-host or malicious-counterparty behavior,
portable reputation, live campaign-wallet nomination, autonomous staking
choice, production Validator liveness, slashing or storage-rent safety,
mainnet APR or issuance, or any ROADMAP gate.
