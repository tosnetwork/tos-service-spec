# Agent Economy Metrics V1

## Status

**Implementation status: ⬜ Not implemented.**

This document defines a derived economic-observability profile. It does not
add consensus state, a metrics contract, a token, or a new authority mode.
No repository currently implements the complete index, export API, or
conformance suite defined here.

## Purpose and authority

Agent Economy Metrics measure paid Agent activity without turning a Gateway or
analytics database into protocol authority. Every economic value included in a
finalized-derived metric must be reconstructible from finalized TOS state, the
authenticated TOS-network stablecoin transaction chain, and exact
content-addressed preimages whose digests are committed by that state. Manifest
bytes are verification inputs, never independent authority; missing bytes fail
closed.

The metrics service is a replaceable projection. Its output must carry its
network domain, finalized checkpoint range, exact asset identity, calculation
version, discovery mode, and coverage. Two indexers observing the same complete
finalized transaction interval must produce the same derived values. A partial
index is permitted, but it must label every result as observed rather than a
network total. Its counts and amounts are lower bounds; its rates and
distribution statistics describe only the observed sample.

Quote Proposals, search impressions, endpoint claims, token prices, unfinalized
transactions, self-reported revenue, and Gateway-local balances never count as
economic output.

The generic Intent, conversation, and Agreement architecture is defined in
[`AGENT_INTENT_EXCHANGE_V1.md`](AGENT_INTENT_EXCHANGE_V1.md). Intents,
negotiations, expected Gifts, unsecured receivables, direct payments, and
external settlement evidence may be useful participant-local business metrics,
but they do not enter the finalized TOS-derived Agent GDP in this document.
This document therefore remains a narrow on-chain measurement profile, not a
requirement that every Agent transaction use Quote, escrow, or Receipt.

## Canonical job identity and terminal facts

One commercial job is identified by the following byte preimage:

```text
job_id = "sha256:" || lowercase_hex(SHA-256(
  "tos.service.economic-job.v1\0" ||
  network_domain_cell_hash:bytes32 ||
  quote_commitment_hash:bytes32 ||
  escrow_workchain:int32_be ||
  escrow_account_id:bytes32
))
```

The network-domain hash is `cell_hash(network_domain)` from
`ACCEPTED_QUOTE_TVM_V1.md`. The digest and address are decoded to fixed-width
binary values before hashing; their display strings are never concatenated. V1
requires the escrow workchain to be zero. The pair remains explicit even though
the deterministic escrow StateInit also binds the Quote, because it is the
shared execution-Gate slot and makes a wrong network or Quote-to-account
association fail visibly.

Transport retries, Agent Packets, A2A messages, MCP calls, internal tool calls,
artifacts, and settlement retries do not create additional jobs.

A settled job may contribute economic value only after an indexer independently
verifies the complete terminal chain:

```text
finalized escrow deployment whose authenticated StateInit embeds the Accepted Quote
→ authenticated finalized escrow funding
→ canonical Receipt commitment
→ authenticated stablecoin-wallet transfer
→ finalized release outcome
```

A verified refund contributes job activity and refund statistics, but
contributes zero provider receipts and zero settled service value.
`release_pending` is exported separately and never counted as settled merely
because the escrow requested a transfer. `refund_pending` is likewise
nonterminal until the exact refund transfer is verified. Ambiguous or divergent
chain observations fail closed.

Each job has at most one derived terminal outcome: `released` or `refunded`.
The indexer must reject duplicate or conflicting terminal evidence rather than
choosing one by arrival order.

## Provider attribution and anti-spoofing

An Accepted Quote is created by the buyer and names a provider Agent and
Capability. Those names alone do not prove provider participation: an arbitrary
buyer can reference a public Agent ID or Capability ID. Network escrow activity
and provider-attributed economic output are therefore separate domains.

A released payment is eligible for Agent GDP, provider receipts, Capability
metrics, or an Agent ranking only when the indexer additionally proves:

1. at Quote acceptance, the exact Registry code identity shows a live provider
   Agent and a live Capability owned by that Agent, with the quoted version
   present, unrevoked, and bound to the quoted manifest digest;
2. the canonical manifest bytes match that digest and bind the same asset,
   endpoint commitment, and execution-signer authorization as the Accepted
   Quote;
3. the Receipt and settlement intent are valid, and the committed execution
   signer authorized the exact terminal release; and
4. archived finalized Registry history shows that the Agent remained live and
   the Capability remained owned by it, with the version unrevoked, from Quote
   acceptance through the Receipt's signed `completed_at` time.

The signed completion time must satisfy the Receipt and escrow rules and map to
the finalized Registry history without ambiguity. Attribution additionally
requires `acceptance_time <= funding_time <= completed_at <=
release_request_time`; a Receipt timestamp outside that order is conclusively
unattributable even if the escrow transfer itself finalized. A later Capability
transfer or revocation does not rewrite work completed before that transition.

A conclusive attribution mismatch is an `unattributed_release`, not Agent GDP.
Unavailable manifest or historical Registry evidence is
`attribution_unresolved`; it fails closed and prevents total Agent-GDP status.
Funding, refund, or timeout without a provider-authorized Receipt may be counted
as network escrow activity, but cannot lower the named Agent's performance or
appear as that Agent's accepted work. This prevents third-party spam from
poisoning provider statistics.

## Discovery completeness

An indexer may advertise network totals only when it scans the complete
finalized TOS history needed to discover every escrow deployment by the frozen
escrow code identity and authenticated StateInit. A Gateway catalog,
known-address list, provider feed, or API traffic log is necessarily partial
because it cannot prove that no other escrow exists.

Every report declares one discovery mode:

- `complete_chain_scan`: uninterrupted finalized transaction coverage from
  genesis through the report end checkpoint; totals for the explicitly bound
  escrow-code profile are permitted;
- `bounded_address_set`: an explicit committed set of escrow addresses; only
  observed aggregates are permitted; or
- `gateway_observed`: traffic- or catalog-derived discovery; only observed
  aggregates are permitted.

For `bounded_address_set`, the export binds a digest of the sorted canonical
address set. For `complete_chain_scan`, it binds the scanner's origin and
high-water master checkpoints. A shorter report window does not shorten this
history requirement: an escrow may deploy before the window and settle inside
it. Unknown or unresolved escrows cannot be represented as a percentage of an
unknown universe; a partial report therefore never uses the word `total`. Even
with `complete_chain_scan`, network totals require
`unresolved_escrow_count == 0`; otherwise the values remain observed lower
bounds for counts and amounts and observed-sample statistics for rates and
distributions.

Every economic report binds one exact escrow code hash. Different escrow code
identities are reported separately unless a later specification freezes an
explicit cross-version semantic aggregation rule. Registry snapshots likewise
bind one exact Registry code hash.

A same-code deployment is only a candidate. It becomes a discovered TOS Service Protocol
escrow after strict typed decoding, root-to-reference validation, canonical
StateInit reconstruction, and address equality succeed. A conclusively invalid
candidate is excluded and counted in `rejected_candidate_count`; it cannot
destroy completeness. A candidate whose authentication cannot be completed is
counted in `unresolved_candidate_count`, causes fail-closed loss of total
status, and cannot contribute any metric. The same rule applies to Registry
account candidates.

## Amount and asset rules

Monetary inputs and gross aggregates are unsigned base-10 atomic-unit strings.
The one net-flow field may be a signed canonical decimal string
`0 | -?[1-9][0-9]*`. Aggregation is performed
separately for each exact `TOSAssetIdentityV1`, including network domain,
stablecoin master contract identity, wallet-code hash, and decimals. A ticker
symbol is display metadata and cannot join asset buckets.

Aggregate amounts use unsigned 256-bit arithmetic and must remain below
`2^256`. `net_agent_flow_atomic` uses the signed range
`[-(2^256 - 1), 2^256 - 1]`. Counts and Unix-second durations are unsigned
64-bit integers; PPM rates are nullable unsigned 32-bit integers in
`[0, 1_000_000]`. Any overflow invalidates the report rather than saturating,
wrapping, or switching representation.

The metrics protocol does not publish a fiat conversion as canonical-derived
value. A UI may show an explicitly labelled, timestamped, non-authoritative
conversion beside the atomic-unit result.

TOS Service Protocol V1 supports service-only jobs. Consequently:

- `settled_cash_flow_atomic` is the sum of every authenticated terminal release
  transfer, whether or not Agent attribution succeeds;
- `gross_agent_value_atomic` is the attributable subset that passes every
  provider-attribution rule above;
- `settled_provider_receipts_atomic` is that same attributable amount actually
  transferred to providers;
- for the current exact-payment profile,
  `gross_agent_value_atomic == settled_provider_receipts_atomic`;
- `settled_cash_flow_atomic == gross_agent_value_atomic +
  unattributed_released_value_atomic +
  attribution_unresolved_released_value_atomic`; and
- arbitrary trading notional, assets under management, or provider-reported
  "handled value" is not counted.

If later profiles authorize fund-managed work, their principal/notional value
must be exported as a separate field and must never be silently added to
service revenue.

Product interfaces may label `gross_agent_value_atomic` as "Agent GDP" or
"aGDP" only when they display the exact definition, asset, window, discovery
mode, and coverage. The protocol field name remains explicit because gross
multi-stage transaction value is not conventional value-added GDP.

Likewise, a product may label `settled_provider_receipts_atomic` as "Total
Revenue" only when it states that this is gross protocol-settled receipt value,
not generally accepted accounting revenue, profit, taxable income, or value
after costs and off-protocol adjustments.

## Economic metrics

For each time window and exact asset bucket, export the following. A
`complete_chain_scan` may use the names as written; a partial index must present
them as observed values in the UI and expose its discovery mode beside them. A
complete scan with any unresolved escrow is treated as partial for this rule.

Accepted, funded, refunded, request, and open-state counts describe authenticated
escrow activity. They are permissionless and can be increased by one actor
using many wallets, so they are not proof of independent demand, customers, or
provider performance. Only attributed releases contribute Agent GDP and
provider rankings.

| Field | Definition |
|---|---|
| `settled_cash_flow_atomic` | Sum of all authenticated terminal provider-wallet releases. |
| `gross_agent_value_atomic` | Attributable released value that passes the provider anti-spoofing rules. |
| `settled_provider_receipts_atomic` | Same attributable amount, presented as provider receipts. |
| `unattributed_released_value_atomic` | Conclusively non-attributable released value; never Agent GDP. |
| `attribution_unresolved_released_value_atomic` | Released value whose provider attribution cannot be resolved; excluded from Agent GDP. |
| `accepted_job_count` | Unique jobs whose schema-dispatched Quote acceptance event finalized in the window: authenticated escrow deployment for frozen schema 1, or the bound-wallet-authenticated `pending_acceptance -> awaiting_funding` transition for the paid-demand successor. |
| `funded_job_count` | Unique jobs whose exact escrow funding finalized. |
| `released_escrow_count` | Unique jobs with an authenticated terminal provider-wallet payment. |
| `attributed_settled_job_count` | Released jobs that pass every provider-attribution rule. |
| `refunded_job_count` | Unique jobs with verified terminal buyer refund. |
| `release_pending_entered_job_count` | Unique jobs whose release request finalized in the window, whether later released, bounced, or still pending. |
| `refund_pending_entered_job_count` | Unique jobs whose refund request finalized in the window, whether later refunded, bounced, or still pending. |
| `release_request_count` | Finalized transitions into `release_pending`, including a later retry after an authenticated bounce restored `funded`. |
| `refund_request_count` | Finalized transitions into `refund_pending`, including a later retry after an authenticated bounce restored `funded`. |
| `unique_buyer_wallet_count` | Distinct canonical buyer wallets in jobs with acceptance, funding, or a terminal outcome finalized in the window. |
| `unique_quote_named_provider_agent_count` | Distinct provider Agent IDs named by those jobs; not proof of participation. |
| `unique_attributed_provider_agent_count` | Distinct provider Agent IDs among attributed settled jobs. |
| `terminal_release_rate_ppm` | `released / (released + refunded)` in integer parts per million; this is a network escrow outcome, not provider quality. |
| `refund_rate_ppm` | `refunded / (released + refunded)` in integer parts per million. |
| `median_settlement_seconds` | Median finalized funding-to-terminal duration. |
| `p95_settlement_seconds` | Nearest-rank P95 finalized funding-to-terminal duration. |

Zero-denominator rates are `null`, not zero. Durations use finalized block time,
not Gateway receipt time or local wall-clock time. For an even sample count,
the median is the integer floor of the mean of the two central values. P95 uses
the sorted value at one-based rank `ceil(0.95 * n)`. Checked arithmetic must
reject overflow.

Event times are unambiguous:

- acceptance time is schema-dispatched: the authenticated containing-block Unix
  time of canonical escrow deployment for schema 1, or of the bound-wallet-
  authenticated `pending_acceptance -> awaiting_funding` transition for the
  paid-demand successor;
- funding time is the authenticated containing-block Unix time of the escrow
  transaction that accepts the stablecoin `transfer_notification`;
- pending-entry time is the authenticated containing-block Unix time of the
  escrow transaction that records the release or refund request; and
- terminal time is the authenticated containing-block Unix time of the
  recipient-wallet credit transaction that completes the derived release or
  refund chain.

An unknown Quote/escrow schema or unresolved acceptance transition makes the
metric bucket partial. Deployment alone must never be used as a fallback
acceptance event for a paid-demand successor.

All transactions in one terminal proof must be finalized no later than the
report end checkpoint. A containing block is usable only through the exact
quorum-finalized masterchain checkpoint that authenticates it. Resolver
observation time, Gateway receipt time, and local wall-clock time cannot
substitute for any event time.

The standard windows are `1h`, `24h`, `7d`, `30d`, and `all`, where the bounded
durations are exactly 3,600, 86,400, 604,800, and 2,592,000 seconds. Every time
window is the half-open interval `[from_unix_seconds, to_unix_seconds)`, with
`to - from` equal to the selected duration. Membership is
based on the terminal finalized time for terminal value, terminal count, rate,
and duration metrics; on acceptance finalized time for `accepted_job_count`; on
funding finalized time for `funded_job_count`; and on pending-request finalized
time for pending-entry counts. An `all` report starts at genesis. A bounded
report may start later but cannot call itself all-time.
For `all`, `from_unix_seconds` is the authenticated genesis block time.
`to_unix_seconds` must not exceed the authenticated finalized chain time at the
report's as-of checkpoint.

Current economic state is exported separately from window events, but remains
inside the same exact asset and escrow-code profile:

- `open_awaiting_funding_job_count` is the number still derived as
  `awaiting_funding`;
- `open_funded_job_count` is the number of jobs still derived as `funded`;
- `open_release_pending_job_count` is the number still derived as
  `release_pending`; and
- `open_refund_pending_job_count` is the number still derived as
  `refund_pending`.

These are snapshots at the report as-of checkpoint and do not change when only
the selected time window changes.

State derivation is deterministic. A verified terminal wallet-transfer chain
takes precedence over the escrow's persistent pending state. Otherwise an
authenticated bounce that restores `funded` takes precedence over the earlier
pending request. Without either, the latest authenticated typed escrow state at
the as-of checkpoint determines `awaiting_funding`, `funded`,
`release_pending`, or `refund_pending`. Conflicting evidence is unresolved,
never selected by transaction arrival or index order.

## Registry snapshot metrics

Active Registry supply is not a stablecoin-specific economic value. It is
exported once per network at the report end checkpoint, outside every asset
bucket:

- `active_agent_count`;
- `active_capability_count`; and
- `active_capability_version_count`.

These counts do not claim that a provider is online, willing to quote, or able
to execute, so they must not be labelled "purchasable offerings". Network-wide
names require a complete finalized Registry-account scan. A Gateway-local
Capability catalog may export only observed snapshot counts.

An active Agent is present and not tombstoned. An active Capability is present,
not tombstoned, and owned by an active Agent. An active Capability version
belongs to an active Capability and is not revoked. This mirrors the Native
rule that an owner Agent tombstone makes its Capability unusable even when the
Capability account itself is not tombstoned.

## Per-Agent metrics

For a provider Agent, export:

- `contributed_gross_agent_value_atomic`, the settled value of jobs whose
  Accepted Quote names this provider Agent;
- `settled_receipts_atomic`;
- `paid_to_other_agents_atomic` when the same controlled wallet is provably the
  buyer in another verified job;
- `net_agent_flow_atomic = settled_receipts - paid_to_other_agents`, encoded as
  the signed canonical decimal form defined above;
- attributed settled-job count and provider-authorized release-pending count;
- unique buyer-wallet count among attributed settled jobs;
- unique counterparty-Agent count where both identities are provably bound;
- median and P95 settlement duration among attributed settled jobs;
- active Capability and active Capability-version snapshot counts at the report
  end checkpoint;
- Capability utilization, defined as Capabilities with at least one attributed
  settled job in the selected window among the Agent's active Capabilities at
  the report end checkpoint, divided by that same active set, in integer parts
  per million; and
- last settled job finalized time.

Wallet-to-Agent control must be established by an explicit finalized protocol
binding before Agent spend or net flow is exported. Address similarity,
Gateway configuration, or an operator assertion is insufficient. Until such a
binding exists, `paid_to_other_agents_atomic`, `net_agent_flow_atomic`, and
unique counterparty-Agent count are `null`, not zero, and coverage explains
why. TOS Native Service V1 currently defines no such general wallet-control binding.

For the fixed-price V1 profile,
`contributed_gross_agent_value_atomic == settled_receipts_atomic`. Summing the
contributed value over all provider Agents equals network
`gross_agent_value_atomic`; buyer-side subcontract spend is not attributed a
second time to the hiring Agent. This preserves one network contribution per
settled job while still exposing provable outbound spend separately.

`unique_buyer_wallet_count` counts addresses, not humans, organizations, or
independent economic actors. Wallet rotation and Sybil wallets can increase it;
interfaces must label it "unique buyer wallets", never "unique users".
Likewise, an Agent ID is not proof of a unique legal entity.

Buyer-created, pre-Receipt fields may be shown separately as
`quote_referenced` exposure: accepted, funded, refunded, awaiting-funding, and
refund-pending counts that merely name the Agent. They are not provider-
authorized activity, are excluded from Agent GDP, success rates, and rankings,
and must carry that warning in every response. V1 defines no fair per-Agent
refund or success rate because a third party can create and fund a Quote that
the provider never accepts.

## Per-Capability metrics

For each exact Capability and version, export:

- settled value and provider receipts, attributed to the Agent named by each
  Accepted Quote only after the anti-spoofing proof succeeds;
- attributed settled-job count and provider-authorized release-pending count;
- unique buyer-wallet count among attributed settled jobs;
- median settled price among attributed settled jobs;
- median and P95 settlement duration among attributed settled jobs;
- current finalized owner Agent ID;
- current Capability tombstone, version revocation, and effective owner-Agent
  tombstone status at the report end checkpoint; and
- last settled job finalized time.

Historical jobs remain attributed to the provider Agent and version named by
their Accepted Quote only after the anti-spoofing proof establishes the owner
relationship through completion. A later Capability transfer or revocation
changes the current status but cannot rewrite that proven historical
attribution.

As with Agent reports, buyer-created pre-Receipt counts may appear only under a
separate `quote_referenced` exposure object. They cannot be used as Capability
quality, acceptance, failure, or refund metrics.

## Gross value and supply-chain duplication

An attributable Agent-to-Agent subcontract creates a new paid job and therefore
contributes to gross Agent value. Summing attributed settlements intentionally
measures gross network activity and may count multiple stages of one supply
chain.

To avoid presenting that number as unique final demand, an implementation may
also export `end_buyer_economic_value_atomic`, but only when it can prove that a
job is the root of a payment graph. The current V1 Accepted Quote binds a buyer
wallet but commits neither a parent job nor a general wallet-to-Agent binding,
so this field is `null` in V1. It must include `classified_job_count` and
`classification_coverage_ppm` if a later protocol profile supplies that
provenance. A Gateway must never infer end-buyer status from traffic or labels.

## Availability and operational metrics

The following useful discovery signals are non-authoritative and must be
exported in a separate operational response:

- `online`;
- `last_seen_at`;
- `minutes_since_last_seen`;
- `endpoint_latency_ms`; and
- `recent_transport_success_rate_ppm`.

They may be derived from A2A, MCP, Agent Packet, or HTTPS probes. Every value
must identify the observing operator and observation time. These signals cannot
authorize execution, payment, ranking as a protocol fact, or Capability use.
They are not part of the deterministic economic report and must not be included
in its content digest or cross-indexer equality comparison.

Availability is endpoint-specific. An Agent with multiple endpoints is online
for one observation only if the report states the exact endpoint-selection and
probe-success rule; there is no canonical network-wide online bit.

## Export envelope

Every economic network, Agent, or Capability-version report uses the following
conceptual JSON envelope:

```json
{
  "schema": "tos.service.agent-economy-metrics.v1",
  "scope": {
    "kind": "network|agent|capability_version",
    "id": "",
    "capability_version": null
  },
  "network": {},
  "asset": {},
  "window": "24h",
  "from_unix_seconds": 0,
  "to_unix_seconds": 0,
  "as_of_finalized_checkpoint": 0,
  "authority": {
    "registry_code_hash": "tvm-cell-sha256:...",
    "escrow_code_hash": "tvm-cell-sha256:..."
  },
  "discovery": {
    "mode": "complete_chain_scan|bounded_address_set|gateway_observed",
    "index_origin_checkpoint": 0,
    "index_high_water_checkpoint": 0,
    "address_set_digest": null,
    "observer_id": null
  },
  "metrics": {
    "window": {},
    "as_of": {}
  },
  "coverage": {
    "candidate_account_count": 0,
    "rejected_candidate_count": 0,
    "unresolved_candidate_count": 0,
    "discovered_escrow_count": 0,
    "indexed_escrow_count": 0,
    "unresolved_escrow_count": 0,
    "attribution_eligible_release_count": 0,
    "attributed_release_count": 0,
    "unattributed_release_count": 0,
    "attribution_unresolved_release_count": 0,
    "attribution_coverage_ppm": 0,
    "provenance_eligible_job_count": 0,
    "classified_job_count": 0,
    "classification_coverage_ppm": 0
  },
  "generated_at_unix_seconds": 0
}
```

The concrete protobuf/Connect API remains unimplemented. The implementation
must use integer counters and canonical decimal strings; floating-point
monetary values are forbidden. `generated_at_unix_seconds` describes the export
operation and is excluded from deterministic value comparison. Operational
metrics use a separate response envelope. Pagination and ranking are derived
presentation features, not protocol authority.

The exact `schema` string is the calculation-version identifier. Changing a
formula, field meaning, event-time rule, numeric width, set commitment, or Job
ID derivation requires a new schema version. Adding presentation metadata does
not reinterpret an existing version.

`asset`, `authority.registry_code_hash`, and
`authority.escrow_code_hash` are mandatory. `scope.id` is empty only for
network reports; an Agent ID or Capability ID is mandatory otherwise, and
`scope.capability_version` is mandatory only for `capability_version`.

Both authority fields use exact TVM cell identities. The Registry identity is
required because every current economic report attributes jobs to a provider
Agent and Capability. The asset object supplies the exact stablecoin master
contract and wallet code identities. The discovery high-water checkpoint must
equal `as_of_finalized_checkpoint`.

For every report,
`indexed_escrow_count + unresolved_escrow_count == discovered_escrow_count`.
These counts cover every escrow of the bound code identity discovered through
the report as-of checkpoint, not only escrows with an event in the selected
window. `indexed` means that the deployment, typed state, Quote linkage, and
relevant stablecoin transaction history resolve without ambiguity through that
checkpoint. Metrics exclude unresolved escrows and therefore lose total status
when the unresolved count is nonzero.

Candidate coverage counts distinct canonical account addresses, not transaction
attempts. `candidate_account_count` equals the sum of rejected candidates,
unresolved candidates, and authenticated discovered escrows. Rejected
candidates are deterministically proven non-protocol accounts. Any unresolved
candidate or unresolved authenticated escrow removes total status.

For releases whose terminal time is inside the selected window, every
authenticated release is attribution-eligible, so
`attribution_eligible_release_count == released_escrow_count`. That set is
partitioned exactly into attributed, conclusively unattributed, and
attribution-unresolved release counts. `attribution_coverage_ppm` is the integer floor of
`(attributed_release_count + unattributed_release_count) * 1,000,000 /
attribution_eligible_release_count`, or null for a zero denominator. An
attribution-unresolved release does not prevent a complete cash-flow total, but
it prevents a complete Agent-GDP total and all affected Agent, Capability, and
ranking claims.

The window metric `attributed_settled_job_count` equals coverage
`attributed_release_count`; the duplicate semantic name is retained only to
make the economic metric readable while the coverage object exposes the full
classification partition.

For `complete_chain_scan`, `index_origin_checkpoint` is the network genesis
checkpoint and `address_set_digest` is null. For `bounded_address_set`, the
address-set digest is mandatory. For `gateway_observed`, the response must name
the observing Gateway in discovery metadata; an address-set digest is optional
and cannot upgrade completeness.

Set commitments use fixed deterministic preimages:

```text
address_set_digest = "sha256:" || lowercase_hex(SHA-256(
  "tos.service.metrics-address-set.v1\0" ||
  network_domain_cell_hash:bytes32 ||
  count:uint32_be ||
  each sorted (workchain:int32_be || account_id:bytes32)
))

object_set_digest = "sha256:" || lowercase_hex(SHA-256(
  "tos.service.metrics-object-set.v1\0" ||
  network_domain_cell_hash:bytes32 ||
  count:uint32_be ||
  each sorted (utf8_length:uint16_be || canonical_object_id:utf8)
))
```

Sorting is lexicographic over each encoded binary entry. Sets reject duplicate
entries, zero account IDs, unsupported workchains, malformed object IDs, and
counts that exceed their encoded bounds.

`classification_coverage_ppm` is the integer floor of
`classified_job_count * 1,000,000 / provenance_eligible_job_count`; it is
`null` when the denominator is zero. Eligible jobs are attributed settled jobs
in the selected economic window for which end-buyer classification would
affect the requested metric. The classified count must not exceed the eligible
count.
This classification coverage concerns optional end-buyer provenance, not
chain-scan completeness.

Registry supply uses a separate conceptual envelope so it cannot inherit a
meaningless asset bucket, economic window, or escrow coverage:

```json
{
  "schema": "tos.service.agent-economy-registry-snapshot.v1",
  "network": {},
  "registry_code_hash": "tvm-cell-sha256:...",
  "finalized_checkpoint": 0,
  "discovery": {
    "mode": "complete_chain_scan|bounded_object_set|gateway_observed",
    "index_origin_checkpoint": 0,
    "index_high_water_checkpoint": 0,
    "object_set_digest": null,
    "observer_id": null
  },
  "metrics": {
    "active_agent_count": 0,
    "active_capability_count": 0,
    "active_capability_version_count": 0
  },
  "coverage": {
    "candidate_account_count": 0,
    "rejected_candidate_count": 0,
    "unresolved_candidate_count": 0,
    "discovered_object_count": 0,
    "indexed_object_count": 0,
    "unresolved_object_count": 0
  },
  "generated_at_unix_seconds": 0
}
```

For Registry snapshots, `candidate_account_count` equals rejected candidates
plus unresolved candidates plus authenticated discovered objects, and
`indexed_object_count + unresolved_object_count == discovered_object_count`.
Only a genesis-to-checkpoint scan with zero unresolved candidates and zero
unresolved objects may use network-total labels. Snapshot generation time is
excluded from deterministic value comparison.

## Ranking

Clients may rank Agents by settled receipts, contributed gross value, settled
jobs, unique buyer wallets, or recency. Every ranked row must
expose the underlying metric, its numerator and denominator where applicable, asset
identity, window, finality checkpoint, and coverage. Rankings must not combine
different stablecoin identities or treat online status as economic authority.
Ties are resolved by ascending canonical Agent ID so every implementation
produces the same order.

Settled receipts, contributed value, attributed settled jobs, unique buyer
wallets, and recency rank descending. Null values sort after non-null values. Rankings are
partitioned by network domain, Registry code, escrow code, asset identity,
window, as-of checkpoint, and discovery mode before sorting. V1 forbids a
per-Agent success-rate ranking because refunds and abandoned funding do not
carry provider authorization.

## Required implementation and acceptance

Implementation requires:

1. a rollback-protected genesis-to-high-water finalized transaction scanner,
   plus escrow, Registry, and stablecoin transaction indexes;
2. deterministic terminal-job classification and exact-asset aggregation;
3. historical Registry/manifest/signer attribution and network, Agent, and
   Capability export APIs;
4. if operational probes are exposed, a separate response and authority domain;
5. restart, reorg, pre-window-deployment, duplicate-event,
   conflicting-terminal, incomplete-discovery, partial-coverage,
   code-identity, owner-tombstone, asset-confusion, signed-net-flow, overflow,
   authenticated-block-time, exact-window, percentile, candidate-account,
   forged provider-name, missing manifest, wrong execution signer,
   mid-job transfer/revocation, attribution-unresolved, Sybil-label, refund,
   bounce-retry, and pending-entry/open-pending tests;
6. an independent implementation reproducing frozen metric vectors; and
7. comparison of two independent indexers over the same network, code
   identities, asset, time window, and as-of finalized checkpoint.

Until every applicable item exists, the feature remains **⬜ Not implemented**
and no Gateway may advertise its output as canonical Agent GDP.
