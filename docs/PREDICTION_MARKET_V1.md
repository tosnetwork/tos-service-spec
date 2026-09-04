# TOS PredictionMarket V1

Status: release candidate / incubation profile. Activation on a public network
requires the repository's normal compatibility, reproducibility, audit,
economics and operations gates. This additive profile does not alter existing
Agent Commerce, escrow, Registry, wallet, or Intent wire formats.

## 1. Scope and trust model

One market is one immutable binary proposition backed by native TOS. The
contract owns custody, conditional-position accounting, exact order execution,
resolution quorum, challenge state and payouts. OpenFox supplies discovery,
Intent routing, an off-chain order book, solvers, durable transaction relay,
evidence collection and independent Agent Account reporters.

OpenFox is not trusted for balances, prices, fills, outcomes, time, sender
identity or signatures. A Carrier can hide or reorder orders but cannot modify
or execute them. A reporter quorum is explicitly trusted for external facts;
the chain cannot derive political results from consensus alone.

V1 has no upgrade path, admin settlement override, pause-and-seize key,
arbitrary payout vector, hidden percentage fee, transferable position token,
AMM, scalar market, or multilateral basket. A new code/config version is needed
to change those facts.

## 2. Immutable identity and admission

The canonical StateInit freezes network `global_id`, workchain, deployment
salt, lot payout `L`, price scale `S=10000`, close/observation/vote/challenge/
appeal/claim deadlines, capacity and liability caps, storage contributions,
reserve floors, rules hash, normal/appellate policies, stable reserve recipient,
and code version.

```text
market_config_hash = cell_hash(canonical config without derived identifiers)
market_id = SHA256("TOS_PREDICTION_MARKET_V1" || global_id || workchain_id ||
                   deployment_salt || market_config_hash)
market_address = workchain_id:cell_hash(StateInit)
```

Derived identifiers never participate in their own preimage. The two reporter
address sets are sorted, unique, disjoint and immutable. Thresholds are between
one and set size. `L % S == 0`, `L` is even, and every configured deadline and
capacity is checked against hard code bounds before activation.

Risk-increasing operations accept only audited TOS global versions 14 and 15.
Version below 14 fails; an unknown higher version fails closed for activation,
registration, deposit, split and match but retains cancellation, rotation,
merge, resolution, challenge, claim and withdrawal exits. The contract parses
ConfigParam 8 itself for every classified entry.

## 3. Ledgers and solvency

For account `a`, `F[a]` is free collateral and `Y[a]`/`N[a]` are whole lots.
Before finalization:

```text
sum(Y) = sum(N) = Q
K = Q * L
position_liability = K
```

After finalization, `K` atomically becomes the equal
`remaining_payout_liability`; the two representations are never counted
together. Across claims:

```text
remaining_payout_liability + cumulative_claimed_payout = final_backing
```

The total liability is free balances plus the phase-selected position
liability, refundable challenge bonds and account/order cleanup credits.
Operating reserve, entry fees and nonrefundable challenge processing fees are
unencumbered reserve. Every transition uses checked intermediate arithmetic and
proves both:

```text
total_liability_after <= max_total_liability
physical_balance_after >= total_liability_after + required_reserve(status_after)
```

The fixed `challenge_bond` headroom remains unavailable to other liability
classes until the challenge window closes. Cleanup rewards pay directly to the
actual caller or are waived into reserve; they never create a caller account
balance.

## 4. Trading and exact prices

Canonical orders and their signatures follow
`PREDICTION_ORDER_AUTHORIZATION_V1.md`. Each match has exactly one maker and one
taker. The maker fixes a YES price:

```text
maker YES quote: pY = maker.limit_price_tick
maker NO quote:  pY = S - maker.limit_price_tick
pN = S - pY
unit_value = L / S
notional = quantity_lots * L
yes_value = quantity_lots * unit_value * pY
no_value = notional - yes_value
```

Prices 0 and S are forbidden. The taker limit is checked against `pY` or `pN`.
Only these pairs execute:

| Pair | Atomic transition |
|---|---|
| BUY YES + BUY NO | debit `yes_value/no_value`, mint one complete set, increase `Q/K` |
| BUY X + SELL X | transfer X lots and its exact price; `Q/K` unchanged |
| SELL YES + SELL NO | burn one complete set, credit `yes_value/no_value`, decrease `Q/K` |

Every other combination fails. Self-trade fails unconditionally. `split(q)`
debits `qL` and creates `q` YES plus `q` NO; `merge(q)` is its exact inverse.
Match and split stop at the effective trade-close phase. Merge remains available
in every pre-final phase.

Order records are created only on first fill or exact cancellation. Per-account
and market record caps, paid entry contribution and cleanup credit bound state.
An order record can be pruned only after trade close, older key epoch, or nonce
below the stored floor—not merely because one observed payload expired.

## 5. Resolution state machine

```text
TRADING -> REPORTING -> PROPOSED -> FINALIZED
                    \-> REVIEWING -> FINALIZED
```

All windows are half-open and use contract `now()`. `advance_phase` is
permissionless and follows one pure effective-phase function. A transition that
creates a round nonce must be a separate transaction; a report cannot both open
and vote in a round.

Normal quorum freezes a proposal and challenge deadline. One valid challenge
must bind the exact proposal, a different counter outcome, canonical challenge
evidence, the authenticated challenger, fixed refundable bond and nonrefundable
processing fee. No second challenge exists.

Appellate quorum is final. Challenge-review timeout preserves the normal
proposal and refunds the bond as an internal credit; normal-timeout appellate
failure finalizes protocol-timeout INVALID. Factual INVALID and timeout INVALID
have the same payout but different audit provenance. Resolution cells,
contexts and evidence follow `PREDICTION_RESOLUTION_STATEMENT_V1.md` and
`PREDICTION_CHALLENGE_EVIDENCE_V1.md`.

## 6. Payouts

The enum fixes payouts; reporters cannot submit arbitrary fractions:

```text
YES:     YES lot = L,   NO lot = 0
NO:      YES lot = 0,   NO lot = L
INVALID: YES lot = L/2, NO lot = L/2
```

Any keeper may call `claim(owner)`, but credit always enters that authenticated
owner's free balance. Only the owner withdraws before claim deadline. After the
deadline anyone may force-close, yet principal still goes to the owner and any
cleanup bounty separately goes to the actual caller (or is waived).

Native payout messages are exact-value, non-bounceable internal messages using
strict send mode 17 after reserving every other liability. They never use mode
2 or mode 128. A failed action rolls back state; recipient compute failure does
not create a late bounce that would contradict the market ledger.

## 7. Internal message surface

All state changes are internal messages. Business calls that carry value are
bounceable and the contract checks inbound flags before creating any record or
liability. An explicitly empty body remains the only non-bounce reserve-
donation form and accepts any positive value. Agent Account V2 cannot authorize
an empty checked-call body, so automated reserve donation uses the distinct,
bounceable typed body:

```text
pm_top_up_reserve#504d0019 query_id:uint64 = InternalMsgBody;
```

The typed form requires the ordinary operation budget, has exactly 96 bits and
no references, and returns before reading or writing market state. Thus it is
valid before activation and after terminal compaction without creating any
liability; all value left after execution fees becomes reserve. Trailing bits
or references, a non-bounce typed message, or insufficient operation budget
fail closed. Bounced inbound messages are consumed before opcode parsing and
never credited to a user ledger.

The V1 surface comprises `activate`, `register_and_deposit`, `deposit`,
`set_trading_key`, `raise_nonce_floor`, `cancel_exact`, `split`, `merge`,
`match_pair`, `report_result`, `challenge_result`, `advance_phase`,
`finalize_uncontested`, `finalize_review_timeout`, `claim`, `withdraw`,
`withdraw_challenge_bond`, `force_refund_challenge_bond`, bounded order/account
pruning, `force_close_account`, `compact_terminal`,
`withdraw_terminal_surplus`, and `top_up_reserve`.

Every request carries `query_id`; stable errors distinguish malformed object,
wrong network/config/code, incompatible global version, non-bounce input,
wrong phase/window/context, authorization/signature/replay failure, price/pair/
fill failure, capacity/contribution failure, arithmetic/liability/reserve
failure, quorum/challenge conflict and action-budget failure.

## 8. Agent Account V2 requirement

Value-bearing market calls require the V2 checked-bounceable transport. It
commits the complete canonical body reference DAG, builds internal header
`0x18`, and fixes `extra_flags=3`: require bounceable target, require nonempty
body, forbid StateInit. The controller signature remains bound to Agent Account
address/workchain, network, opcode, controller epoch, seqno and expiry through
the existing signed-body hash. V1 transport remains byte-for-byte unchanged.

Automated calls use the closed, independently signed
`PREDICTION_CUSTODY_EFFECT_AUTHORIZATION_V1.md` profile. It binds the exact
semantic action and TVM effect to the finalized Agent Account V2 and market
code identities. Escrow custody fields must not be fabricated for Prediction,
and off-chain order authorization/publication never enters this effect union.

## 9. Durable two-hop resolution

An automated call is not successful merely because the Agent Account consumed
its controller sequence. Implementations persist the exact external BOC, the
source account cursor and an exact masterchain checkpoint before broadcast,
then advance only through the following evidence states:

`Broadcasting -> SourceFinalized -> DestinationCommitted`, or
`SourceActionSkipped`, or
`DestinationFailedBounceCreated -> BounceCreditedAtAgent`, or the bounded
terminal state `DestinationFailedNoBounce`.

Source finality walks the authenticated account transaction chain back to the
persisted cursor and uniquely locates the submitted external message. It then
extracts the chain-created outbound and verifies exact target, value, complete
body/StateInit, bounce bit and `extra_flags=3`. Once this source evidence is
durable, the submitted BOC MUST NOT be broadcast again.

Destination recovery scans forward from the pre-broadcast masterchain
checkpoint through the shard blocks referenced by each masterchain state. It
does not use a post-broadcast target cursor as a lower bound and does not apply
a fixed latest-10,000 transaction window. A strict majority of independently
pinned RPC operators must agree on the exact inbound transaction BOC, block
identity and conservative finality head. The verifier independently parses the
BOC and requires the fixed market code/config plus ordinary, non-aborted,
compute-success and action-success execution. Exact inbound bytes together
with immutable market code make the opcode transition deterministic; no latest
getter is used as transaction-local state evidence.

For failure, a rich bounce must be the unique output of that exact destination
transaction and must commit the complete original message/body and failure
phase. Source liquidity remains reserved until a later exact Agent Account
transaction proves that same bounce in its inbound slot and its full value in
the credit phase. If the destination transaction created no output, a bounded
multi-operator observation window of at least the configured masterchain depth
is required; this terminalizes the loss but does not claim a refund.

All masterchain, shard-block, transaction, response-BOC, observer and
outstanding-action collections have explicit admission bounds. Exhausting any
bound leaves the action ambiguous and reserved rather than truncating the scan
or guessing success.

## 10. Capacity and retention

Participants, live order records, reporter votes, distinct statements,
evidence entries, input cells/depth, liabilities and all economic counters have
hard code maxima. Telemetry fill count alone saturates rather than blocking
valid trading. Getters never scan an unbounded dictionary.

Evidence and source snapshots remain independently reconstructible from two
replicas through `claim_deadline + AUDIT_RETENTION`. Terminal compaction is
allowed only after all account, order, bond and cleanup liabilities reach zero;
it retains a minimum audit tombstone and immutable final provenance.

## 11. Required conformance

Implementations consume `test-vectors/prediction-market-v1.json` and the
semantic registry. Tests cover canonical/malformed cells, all eight Ed25519
torsion keys, order field tampering, nonce/epoch replay, exact price arithmetic,
the closed three-pair matrix, every time boundary, both timeout classes,
challenge bond accounting, arbitrary claim order, storage/cap exhaustion,
bounce/action rollback, global-version gates and restart-safe exact-BOC relay.

The independent verifier is `scripts/prediction-market-reference.py`. Passing
fixtures is necessary but not sufficient for public-network admission.
