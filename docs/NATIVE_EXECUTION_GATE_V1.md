# Native Execution Gate V1

## Purpose

The Native Execution Gate is the provider-side boundary between transport and
paid work. It does not authorize payment. It reconstructs authority from
finalized TOS state and durably admits at most one exact execution intent for
one funded purchase.

A2A, MCP, HTTP credentials, gateways, and provider databases are inputs or
transport. None is canonical authority.

## Boundary

```text
   A2A adapter ──┐
   MCP adapter ──┤   any task-admitting transport
Agent Packet  ──┤   (+ every future adapter)
   receiver      │
                 ▼
 ┌────────────────────────────────────────────────────────┐
 │             Shared Native Execution Gate                │
 │  slot key: (quote_commitment, escrow_address)           │
 │  reconstruct authority from finalized TOS state:        │
 │    - Accepted Quote commitment matches the claim        │
 │    - escrow funded == exact quoted amount               │
 │    - Capability owner / version / manifest, not revoked │
 │    - Registry, escrow, and stablecoin identities        │
 │    - checkpoints monotonic; regression fails closed     │
 │  => admit AT MOST ONE exact execution intent            │
 └────────────────────────────────────────────────────────┘
                 │  admit once
                 ▼
        provider runner ──▶ runner execution journal
        (one admitted execution_id starts exactly once,
         even across retry or crash)
                 │
                 ▼
   artifact + report + canonical Receipt ──▶ settlement
```

Authority is finalized TOS state only. TLS, bearer tokens, rate limits, gateway
routing, and provider databases are transport, never authority. No transport
can reach the runner except through this Gate, so one funded purchase admits at
most one runner execution across A2A, MCP, Agent Packet, and any future adapter.

## Claim

Every transport maps its request to the same claim:

```text
escrow_address
quote_commitment
execution_id
input_digest
source_digest
```

Those five fields are the frozen schema-1 core. Quote-version dispatch requires
a paid-demand successor transport to add:

```text
input_acceptance_record_digest
```

The shared purchase-slot key remains `(quote_commitment, escrow_address)`, but
the first valid claimant binds this extension as part of the entire claim. An
exact digest retry is idempotent; a different, omitted, or unresolved record
digest conflicts. Every paid-demand A2A, MCP, Agent Packet, or future adapter
must carry that same field rather than relying on an ingress-local lookup.

The escrow address is mandatory because a Quote commitment alone is not a
canonical account locator. It is included in each transport's input digest.
Omitting it would force the provider to trust an off-chain index to locate the
purchase.

The durable purchase slot is keyed by the exact pair:

```text
(quote_commitment, escrow_address)
```

The first valid claimant atomically binds that slot to the entire claim. An
identical retry is idempotent. Any different execution ID, input digest, source
digest, paid-demand input-acceptance-record digest, Quote, or escrow conflicts
before provider work begins. This rule is
shared across A2A, MCP, and every future adapter; transport-specific journals
cannot safely enforce it.

## Finalized verification

Before decoding commercial state, the Gate uses a frozen immutable version-
dispatch table. A bounded discriminator maps the authenticated network and
Quote schema/profile to exactly one tuple:

```text
(network_domain, quote_schema, binding_profile)
  -> (Quote parser,
      escrow StateInit/state parser,
      exact escrow code hash,
      Gate claim-extension parser and predicate set)
```

Schema 1 maps to its released five-field claim and frozen escrow semantics; the
paid-demand successor maps to its own exact parser/code/predicates and mandatory
`input_acceptance_record_digest`. Unknown, ambiguous, trailing-data, wrong-code,
or cross-version parser/profile combinations fail closed. The selected dispatch-
entry digest is bound into the first durable claim and cannot change on retry or
preflight to reinterpret the purchase more permissively.

Every admission and start preflight first quorum-resolves a sufficiently fresh
finalized TOS network anchor under a released resolver profile. That profile
freezes positive `max_finalized_anchor_age_seconds` and
`max_finalized_anchor_lag_blocks`, the strict-majority endpoint and finality
rule, chain-time comparison, and cross-shard inclusion/order proof. Escrow,
Quote, Registry, Agent, and Capability observations must be authenticated at or
through that anchor. Reusing a monotonic but old checkpoint is not freshness;
endpoint disagreement, an unavailable current quorum, excess age/head lag, or
an unresolved cross-shard order fails closed. The Gate binds the exact anchor,
chain time, checkpoint sequence, and quorum/proof digest to its durable record.

Before writing the claim, the Gate independently resolves and verifies:

1. the exact escrow account has authenticated contract code and a nonzero
   finalized checkpoint;
2. its typed state is `funded`, commits the supplied Accepted Quote, names the
   configured provider wallet, has not reached its refund time, and leaves the
   worst-case execution plus release-pipeline slack required below;
3. the Accepted Quote decodes canonically and binds the configured network,
   provider Agent, Capability/version, manifest, transport commitment,
   execution-signer authorization, stablecoin identity, and funded amount;
4. the provider Agent is finalized under the configured Native Registry code
   identity and is not tombstoned; and
5. the Capability is finalized under that same Registry identity, remains
   owned by the provider Agent, is not tombstoned, and contains the exact
   unrevoked version and manifest digest.

Missing, malformed, divergent, stale, or unavailable resolution fails closed.
An Agent revocation, Capability transfer/revocation, escrow settlement, or
refund-window transition prevents a new claim.

For a paid-demand successor, the Gate also verifies the exact signed
`InputAcceptanceRecordV1` from the Quote-bound ingress. Its Quote, escrow,
execution/upload action, challenge, input/source digests, accepted byte bounds,
ingress-attestation key/profile, conservative clock-profile digest and
evidence/checkpoint, and monotonic ingress journal sequence/head must match the
binding and available immutable bytes. Checked comparison must prove:

```text
input_accept_time_upper_bound <= input_delivery_deadline
```

The acceptance record is created atomically with challenge consumption and
immutable-byte binding. A local wall-clock timestamp, request-arrival time,
backdated receipt, checkpoint/journal regression, or missing bytes cannot prove
delivery. A valid record remains usable when Gate admission happens after
`input_delivery_deadline`; admission has its own later cutoff below.

### Deadline admission

Merely observing `now < refund_available_at` is insufficient: a task admitted
near that boundary can consume its full allowed runtime and become impossible
to release. Deadline inputs are dispatched by Quote version rather than
invented by the adapter.

For a paid-demand Quote successor, the Gate resolves and verifies the exact
committed `effective_max_completion_duration_seconds`,
`max_preflight_to_start_delay_seconds`, and
`release_pipeline_margin_seconds`, plus
`acceptance_to_funding_margin_seconds`, `funding_to_input_margin_seconds`, and
`input_to_admission_margin_seconds`. It recomputes the effective duration from
the exact signed Demand Mutation digest transitively committed by the accepted
paid-demand binding—historically active when the Offer/acceptance was valid—and
`ceil(manifest.limits.wall_clock_millis / 1000)`,
verifies every margin's complete step composition and exact value inside the
released profile's range, and never substitutes a profile minimum. Checked
arithmetic first verifies:

```text
acceptance_to_funding_margin_seconds > 0
funding_to_input_margin_seconds > 0
input_to_admission_margin_seconds > 0
max_preflight_to_start_delay_seconds > 0
effective_max_completion_duration_seconds > 0
release_pipeline_margin_seconds > 0
accept_by + acceptance_to_funding_margin_seconds
  <= funding_deadline
funding_deadline + funding_to_input_margin_seconds
  <= input_delivery_deadline
input_delivery_deadline + input_to_admission_margin_seconds
  <= execution_admission_deadline
execution_admission_deadline + max_preflight_to_start_delay_seconds
  + effective_max_completion_duration_seconds
  <= execution_deadline
execution_deadline + release_pipeline_margin_seconds
  < refund_available_at
```

With that profile's conservative network-time upper-bound rule it then
requires:

```text
admission_time_upper_bound
  + max_preflight_to_start_delay_seconds
  + effective_max_completion_duration_seconds
  + release_pipeline_margin_seconds
  < refund_available_at
```

The same conservative time value used in the slack calculation must satisfy
`admission_time_upper_bound <= execution_admission_deadline`; local request
arrival or claim-write time cannot substitute for that comparison. The Gate
MUST NOT require this later admission time to be at or before
`input_delivery_deadline`; only the separately verified input-acceptance record
proves that boundary. The
release-pipeline margin covers bounded objective validation; evidence/report and
Receipt construction; query-specific signing; initial release inclusion;
and definitive downstream acceptance of the initial escrow-wallet request
without bounce. It is not task-runner time. Frozen escrow V1 clears pending
query history on bounce, so a public old attempt may be permissionlessly
replayed from `funded`; no finite nonzero-bounce retry bound is enforced.
Automatic paid-demand admission therefore requires a proven zero-bounce initial
release path under the exact wallet state/code/value/fee assumptions. Any
unexpected bounce enters resolver/operator recovery and never authorizes blind
automatic retry. A future settlement-critical successor may preserve valid
release priority or a consumed-query generation across bounces, but that is not
this profile.

Immediately before first process start, the runner obtains a fresh preflight on
the same Gate claim. The Gate repeats every finalized verification item above,
not merely the escrow funding check. Under the same configured code identities
and finality/freshness policy, it obtains a coherent fresh monotonic checkpoint
set at or through a newly quorum-resolved anchor and
revalidates the exact escrow code/state and Quote, provider Agent identity and
non-tombstone state, and Capability ownership, exact unrevoked version, and
manifest digest. Any checkpoint regression, fork conflict, code substitution,
escrow transition, Agent tombstone, Capability transfer/revocation, or Quote
divergence already finalized in that fresh checkpoint set fails closed. The
Gate then verifies:

```text
start_preflight_time_upper_bound
  + max_preflight_to_start_delay_seconds
  + effective_max_completion_duration_seconds
  <= execution_deadline

start_preflight_time_upper_bound
  + max_preflight_to_start_delay_seconds
  + effective_max_completion_duration_seconds
  + release_pipeline_margin_seconds
  < refund_available_at
```

The fresh receipt is the linearization point for a bounded start-authority
ticket. It binds the exact verified authority snapshot/checkpoints and a checked
`start_not_after` derived from the conservative preflight time upper bound plus
`max_preflight_to_start_delay_seconds`. Authority changes finalized after that
checkpoint do not retroactively invalidate this ticket; requiring otherwise
would leave an unavoidable distributed check-to-start race. The runner must
atomically bind the receipt on `prepared -> starting` and make the first runtime
call only while its conservative process-start time upper bound is no later than
`start_not_after`.

Queue or restart while durably `prepared` beyond that bound requires another
fresh preflight over the same claim, and every refresh repeats the complete
authority check at checkpoints no older than the durable high-water marks. A
revocation or other adverse transition finalized before that new checkpoint
then blocks start. The original admission freezes nothing; only the final fresh
preflight creates this short, non-renewing authority snapshot, and it grants no
new claim or second execution. A crash at or after `prepared -> starting` is
execution ambiguity, not permission to refresh or readmit. The runner journal
records each preflight attempt and independently enforces the effective
duration.
Because a safe refresh resets only this receipt-validity interval, the field is
not a promise about total time from the original Gate claim to process start;
the fresh execution and refund deadline comparisons bound that total delay.

Schema-1 Quotes retain their frozen protocol validity and contain no committed
paid-demand margin or admission deadline. A production Provider must apply a
nonzero local late-start refusal policy before enabling schema-1 execution. That
policy conservatively reserves the manifest wall-clock maximum plus local
preflight/start delay and the same complete validation, Receipt, signing,
and proven zero-bounce initial-wallet-request pipeline described above. It
remains an operator safety policy, not a buyer term, Quote field, or new schema-1
validity rule. If the operator has not configured and tested those bounds,
schema-1 production admission remains disabled rather than being presented as a
protocol commitment.

The paid-demand profile must freeze allowed duration/delay/margin ranges, each
pre-input pipeline's complete step bound, `InputAcceptanceRecordV1` and ingress-
attestation/clock/journal rules, clock-skew/finality assumptions, upper-bound
algorithm, finalized-anchor age/head-lag bounds and cross-shard proof rule,
integer-rounding rule, exact wallet/attached-value/fee assumptions, zero-bounce
initial-request proof, permissionless old-query replay/resolver rule, execution-
signer custody bound to the Gate/runner completion record and conservative clock
interval, and boundary vectors. An absent or zero required value, unresolved
profile, stale/unavailable finality anchor, clock outside its admitted skew,
overflow, or insufficient remaining time rejects the claim. Until those values
are frozen, paid-demand execution remains blocked.

## Durable record

The claim and its complete outbound intent are written as one owner-private,
atomically published record under an exclusive directory lock. There is no
separate slot record and intent record, so a crash cannot leave a slot-only
state. The record contains the chain code identities, transaction hashes, and
finalized checkpoints for escrow, Agent, and Capability. It also records the
schema-dispatched runtime bound, preflight-to-start delay, release-pipeline
margin, time upper bound, refund boundary, and checked slack result used for
admission and each start preflight. For a paid-demand successor it additionally
stores the exact three pre-input margins and their checked pipeline results,
the verified `InputAcceptanceRecordV1` digest, immutable-byte lookup and digest
result, clock evidence/checkpoint, ingress journal high-water marks, and each
fresh finality anchor's identity, chain time, sequence, quorum/proof digest, and
age/head-lag checks.

On an identical retry, the legacy escrow, Agent, and Capability checkpoints and
every persisted chain anchor/object checkpoint and ingress journal head obey
their respective monotonicity rules. Monotonicity does not waive the fresh-
anchor age/head-lag/current-quorum requirement. Higher valid observations
atomically replace the record and advance its durable high-water marks. A
regression or change in commercial authority fails closed. The directory and
files must remain owner-private; malformed, linked, wrong-owner, oversized, or
trailing-data records are rejected.

This Gate is separate from the runner's execution journal. The Gate prevents
one purchase from authorizing multiple intents or transports. The runner
prevents one admitted execution ID from starting twice after retry or crash.
Both boundaries are required. A prior Gate claim alone never authorizes an
arbitrarily delayed first process start.

## Adapter and server boundary

Every transport that can admit a purchase-bound task to the runner — the A2A
adapter, the MCP adapter, and the Agent Packet receiver — must use this shared
Gate before invoking the runner. The A2A and MCP official SDK server bindings
expose only the frozen synchronous A2A operation and the single purchase-bound
MCP tool; the Agent Packet receiver admits a task only when the packet carries
the matching finalized Accepted Quote commitment and passes the same Gate. No
transport may reach the runner on any other path. TLS, authentication,
rate-limits, listener policy, and public deployment remain operator concerns;
they cannot weaken or replace finalized-state verification.

The production composition constructs both typed resolvers directly from the
same configured strict-majority TOS JSON-RPC endpoint set, frozen Registry BOC
and code hash, immutable released Quote/escrow/Gate version-dispatch table, and
separate durable checkpoint paths. It does not route Native authority through
an A2A/MCP gateway or require a private RPC translation layer.

## Acceptance

Unit and race tests must cover canonical Accepted Quote decode, exact escrow
and Registry identities, Agent tombstone, Capability ownership/version/revoke,
expired escrow, identical retry, concurrent conflicting claims across every
admitting transport (A2A, MCP, and Agent Packet),
schema-1 core versus paid-demand claim dispatch, omitted/substituted/different
`input_acceptance_record_digest`,
unknown/mismatched Quote/parser/escrow-code/Gate-predicate dispatch, cross-
version substitution, and retry/preflight attempts to redispatch a bound claim,
later Demand successor/withdrawal with a lower or higher duration attempting to
deny or relax an already accepted binding,
checkpoint advancement, checkpoint regression, malformed durable records, and
restart recovery. Deadline tests must reject exact-boundary admission and cover
one second too little, `wall_clock_millis` round-up, duration/margin/profile
substitution, input acceptance exactly at its deadline, input acceptance one
second late, on-time input admitted after its delivery deadline but within its
admission deadline, exact/zero/substituted pre-input margins and pipeline
overflow, delayed acceptance/funding finality, backdated/rolled-back input time
evidence, wrong ingress attestation, missing accepted bytes, use of admission
time as delivery time, preflight-to-start queue delay, crash before first start,
fresh start preflight while durably `prepared`,
escrow settlement, Agent tombstone, Capability transfer/revocation/version
change, code substitution, checkpoint regression, or fork conflict between
admission and every refreshed preflight, atomic `prepared -> starting`, crash
ambiguity after that transition, overflow, clock-skew rejection, and schema-1
versus successor version dispatch without recomputing a more permissive prior
decision. It must also cover the profile's exact wallet/attached-value/fee
assumptions, zero-bounce proof, old-query permissionless release/refund replay,
concurrent old/new attempts, repeated replay/fee consumption, semantic-action
grouping, and fail-closed behavior when zero-bounce cannot be proven. Start-
ticket vectors must distinguish an adverse transition
finalized at or before the preflight checkpoint (reject), finalized only after
that checkpoint with start inside `start_not_after` (non-retroactive ticket),
and any attempted start after ticket expiry (refresh and recheck required).
Freshness vectors must reject a monotonic old anchor after a newer finalized
revocation, excessive anchor age/head lag, endpoint disagreement, missing cross-
shard inclusion/order proof, and unavailable current quorum.
A public interoperability session must additionally use
fresh buyer/provider identities and independently operated finalized
endpoints.
