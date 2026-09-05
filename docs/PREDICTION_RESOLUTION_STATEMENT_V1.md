# Prediction Resolution Statement V1

Status: release candidate. This document freezes the hashes that independent
normal and appellate reporter Agent Accounts submit to PredictionMarket V1.

## 1. Outcomes and rounds

```text
round: NORMAL=0, APPEAL=1
outcome: YES=0, NO=1, INVALID=2
review_reason: NORMAL_TIMEOUT=0, CHALLENGE=1
```

`INVALID` is a final 50/50 economic outcome. “Too early” is not an outcome: a
vote round cannot open before its frozen observation boundary. Protocol timeout
and factual invalidity retain different finalization provenance even when both
pay 50/50.

## 2. Normal context

```text
normal_binding$_
  market_id:uint256 rules_hash:uint256 normal_round_nonce:uint256
  = PredictionNormalBindingV1;

prediction_normal_context#504e4331
  schema_version:uint16
  domain_hash:uint256
  normal_round_opened_at:uint64
  resolve_not_before:uint64
  oracle_vote_deadline:uint64
  binding:^PredictionNormalBindingV1
  = PredictionNormalContextV1;
```

`domain_hash = SHA256("TOS_PREDICTION_NORMAL_CONTEXT_V1")`. All hashes and
timestamps are nonzero. Opening and observation times cannot exceed the vote
deadline. The market creates and stores the nonce; reporters never propose it.

## 3. Review base and vote context

```text
review_identity$_ market_id:uint256 rules_hash:uint256
  = PredictionReviewIdentityV1;

review_proposal$_ proposed_statement_hash:uint256 proposed_outcome:uint8
  proposed_evidence_root:uint256 = PredictionReviewProposalV1;

review_counter$_ challenger_address:MsgAddressInt counter_outcome:uint8
  counter_evidence_root:uint256 = PredictionReviewCounterV1;

prediction_review_base#50524231
  schema_version:uint16
  domain_hash:uint256
  review_reason:uint8
  review_started_at:uint64
  review_vote_not_before:uint64
  appeal_deadline:uint64
  identity:^PredictionReviewIdentityV1
  proposal:(review_reason == CHALLENGE ? ^PredictionReviewProposalV1 : ())
  counter:(review_reason == CHALLENGE ? ^PredictionReviewCounterV1 : ())
  = PredictionReviewBaseContextV1;
```

The base domain is
`SHA256("TOS_PREDICTION_REVIEW_BASE_CONTEXT_V1")`. A `NORMAL_TIMEOUT` base has
exactly one reference and no proposal/challenger. A `CHALLENGE` base has exactly
three references and complete nonzero provenance; its counter outcome differs
from the proposal. Tagged structure, not zero hashes, represents absence.

```text
prediction_review_vote#50525631
  schema_version:uint16
  domain_hash:uint256
  review_base_context_hash:uint256
  review_round_nonce:uint256
  review_round_opened_at:uint64
  = PredictionReviewVoteContextV1;
```

The vote domain is
`SHA256("TOS_PREDICTION_REVIEW_VOTE_CONTEXT_V1")`. Review entry freezes the
base but does not open voting. A later, separate `advance_phase` creates the
nonce and vote context only during the half-open appellate vote window. Thus a
report authorization cannot exist before the exact dispute is known.

The reporter obtains these exact cells through the contract's bounded
`get_resolution_contexts` getter. It MUST NOT attempt to derive a cell from the
published hash: the contract-generated nonce and opening timestamp are not
otherwise recoverable. The client recomputes the returned cell hashes, matches
them against `get_market_phase` at the same checkpoint, and requires an
independently pinned RPC strict majority to reproduce the identical BOCs and
phase metadata. NORMAL requires no review base; APPEAL requires the exact base
whose hash appears inside `PredictionReviewVoteContextV1`.

## 4. Resolution statement

```text
resolution_identity$_ market_address:MsgAddressInt market_id:uint256
  = PredictionResolutionIdentityV1;

resolution_policy$_ rules_hash:uint256 round_policy_hash:uint256
  = PredictionResolutionPolicyV1;

prediction_resolution#50525331
  schema_version:uint16
  domain_hash:uint256
  global_id:int32
  round:uint8
  outcome:uint8
  statement_created_at:uint64
  statement_expiry:uint64
  round_context_hash:uint256
  evidence_root:uint256
  identity:^PredictionResolutionIdentityV1
  policy:^PredictionResolutionPolicyV1
  = PredictionResolutionStatementV1;
```

`domain_hash = SHA256("TOS_PREDICTION_RESULT_V1")`. Every referenced hash is
nonzero and `statement_created_at < statement_expiry`. The market reconstructs
the applicable network, market ID, rules hash, policy hash and current context;
message fields are equality guards, not authority.

For NORMAL:

```text
max(resolve_not_before, normal_round_opened_at)
  <= statement_created_at <= now < statement_expiry <= oracle_vote_deadline
```

For APPEAL:

```text
max(review_vote_not_before, review_round_opened_at)
  <= statement_created_at <= now < statement_expiry <= appeal_deadline
```

Only exact `cell_hash(PredictionResolutionStatementV1)` equality aggregates
toward quorum. Votes for the same outcome but different evidence, context,
policy or timestamps do not combine.

## 5. State-machine safety

Normal reporters and appellate reporters are frozen, sorted, disjoint address
sets. Only a successful internal message from a member address counts; an
off-chain signature is not a vote. Each address gets one vote per exact round
context and equivocation does not create two weights.

The first normal quorum freezes proposal time and challenge deadline. One valid
challenge freezes the review base. An appellate quorum is final. If appellate
reporters time out after a challenge, the normal proposal remains final and the
bond becomes refundable; if both independent layers time out without a normal
proposal, the market finalizes `INVALID` with timeout provenance.

Finalization is one-way. It atomically changes the liability representation
from locked backing to an equal remaining payout liability and emits no payout
message. Claims later reduce that liability in any account order.

## 6. Conformance

Canonical context and statement BOCs and hashes appear in
`test-vectors/prediction-market-v1.json`. Implementations reject unexpected
references, trailing bits, noncanonical addresses, zero hashes, wrong domains,
unknown enums, and mixed normal/review provenance.
