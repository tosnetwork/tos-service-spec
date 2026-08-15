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
canonical-derived metric must be reconstructible from finalized TOS state and
the authenticated TOS-network stablecoin transaction chain.

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

## Canonical job identity and terminal facts

One commercial job is identified by the following byte preimage:

```text
job_id = "sha256:" || lowercase_hex(SHA-256(
  "atos.native.economic-job.v1\0" ||
  quote_commitment_hash:bytes32 ||
  escrow_workchain:int32_be ||
  escrow_account_id:bytes32
))
```

The digest and address are decoded to fixed-width binary values before hashing;
their display strings are never concatenated. V1 requires the escrow workchain
to be zero. The pair remains explicit even though the deterministic escrow
StateInit also binds the Quote, because it is the shared execution-Gate slot
and makes a wrong Quote-to-account association fail visibly.

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

A verified refund contributes job activity and refund statistics, but contributes zero
provider revenue and zero settled service value. `release_pending` is exported
separately and never counted as settled merely because the escrow requested a
transfer. `refund_pending` is likewise nonterminal until the exact refund
transfer is verified. Ambiguous or divergent chain observations fail closed.

Each job has at most one derived terminal outcome: `released` or `refunded`.
The indexer must reject duplicate or conflicting terminal evidence rather than
choosing one by arrival order.

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

## Amount and asset rules

Monetary inputs and gross aggregates are unsigned base-10 atomic-unit strings.
The one net-flow field may be a signed canonical decimal string
`0 | -?[1-9][0-9]*`. Aggregation is performed
separately for each exact `TOSAssetIdentityV1`, including network domain,
stablecoin master contract identity, wallet-code hash, and decimals. A ticker
symbol is display metadata and cannot join asset buckets.

The metrics protocol does not publish a fiat conversion as canonical-derived
value. A UI may show an explicitly labelled, timestamped, non-authoritative
conversion beside the atomic-unit result.

ATOS V1 supports service-only jobs. Consequently:

- `gross_agent_value` is the sum of verified settled service payments;
- `settled_provider_revenue` is the sum actually transferred to providers;
- for the current exact-payment profile, the two totals are equal at network
  level; and
- arbitrary trading notional, assets under management, or provider-reported
  "handled value" is not counted.

If later profiles authorize fund-managed work, their principal/notional value
must be exported as a separate field and must never be silently added to
service revenue.

Product interfaces may label `gross_agent_value_atomic` as "Agent GDP" or
"aGDP" only when they display the exact definition, asset, window, discovery
mode, and coverage. The protocol field name remains explicit because gross
multi-stage transaction value is not conventional value-added GDP.

## Economic metrics

For each time window and exact asset bucket, export the following. A
`complete_chain_scan` may use the names as written; a partial index must present
them as observed values in the UI and expose its discovery mode beside them. A
complete scan with any unresolved escrow is treated as partial for this rule.

| Field | Definition |
|---|---|
| `gross_agent_value_atomic` | Sum of verified settled service payments. |
| `settled_provider_revenue_atomic` | Amount actually transferred to providers. |
| `funded_job_count` | Unique jobs whose exact escrow funding finalized. |
| `settled_job_count` | Unique jobs with verified terminal provider payment. |
| `refunded_job_count` | Unique jobs with verified terminal buyer refund. |
| `release_pending_entered_job_count` | Unique jobs whose release request finalized in the window, whether later released, bounced, or still pending. |
| `refund_pending_entered_job_count` | Unique jobs whose refund request finalized in the window, whether later refunded, bounced, or still pending. |
| `unique_buyer_wallet_count` | Distinct canonical buyer wallets in jobs with funding or a terminal outcome finalized in the window. |
| `unique_provider_agent_count` | Distinct provider Agent IDs in those same jobs. |
| `settlement_success_rate_ppm` | `settled / (settled + refunded)` in integer parts per million; this is an economic release rate, not proof of subjective job quality. |
| `refund_rate_ppm` | `refunded / (settled + refunded)` in integer parts per million. |
| `median_settlement_seconds` | Median finalized funding-to-terminal duration. |
| `p95_settlement_seconds` | Nearest-rank P95 finalized funding-to-terminal duration. |

Zero-denominator rates are `null`, not zero. Durations use finalized block time,
not Gateway receipt time or local wall-clock time. For an even sample count,
the median is the integer floor of the mean of the two central values. P95 uses
the sorted value at one-based rank `ceil(0.95 * n)`. Checked arithmetic must
reject overflow.

Event times are unambiguous:

- funding time is the authenticated containing-block Unix time of the escrow
  transaction that accepts the stablecoin `transfer_notification`;
- pending-entry time is the authenticated containing-block Unix time of the
  escrow transaction that records the release or refund request; and
- terminal time is the authenticated containing-block Unix time of the
  recipient-wallet credit transaction that completes the derived release or
  refund chain.

All transactions in one terminal proof must be finalized no later than the
report end checkpoint. A containing block is usable only through the exact
quorum-finalized masterchain checkpoint that authenticates it. Resolver
observation time, Gateway receipt time, and local wall-clock time cannot
substitute for any event time.

The standard windows are `1h`, `24h`, `7d`, `30d`, and `all`. Every time window
is the half-open interval `[from_unix_seconds, to_unix_seconds)`. Membership is
based on the terminal finalized time for terminal value, terminal count, rate,
and duration metrics; on funding finalized time for `funded_job_count`; and on
pending-request finalized time for pending-entry counts. An `all` report starts
at genesis. A bounded report may start later but cannot call itself all-time.
`to_unix_seconds` must not exceed the authenticated finalized chain time at the
report's as-of checkpoint.

Current economic state is exported separately from window events, but remains
inside the same exact asset and escrow-code profile:

- `open_funded_job_count` is the number of jobs still derived as `funded`;
- `open_release_pending_job_count` is the number still derived as
  `release_pending`; and
- `open_refund_pending_job_count` is the number still derived as
  `refund_pending`.

These are snapshots at the report as-of checkpoint and do not change when only
the selected time window changes.

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
- `settled_revenue_atomic`;
- `paid_to_other_agents_atomic` when the same controlled wallet is provably the
  buyer in another verified job;
- `net_agent_flow_atomic = settled_revenue - paid_to_other_agents`, encoded as
  the signed canonical decimal form defined above;
- funded, settled, refunded, pending-entry, and open-pending job counts;
- unique buyer-wallet count;
- unique counterparty-Agent count where both identities are provably bound;
- settlement success and refund rates;
- median and P95 settlement duration;
- active Capability and active Capability-version snapshot counts at the report
  end checkpoint;
- Capability utilization, defined as Capabilities with at least one settled job
  in the selected window among the Agent's active Capabilities at the report
  end checkpoint, divided by that same active set, in integer parts per
  million; and
- last settled job finalized time.

Wallet-to-Agent control must be established by an explicit finalized protocol
binding before Agent spend or net revenue is exported. Address similarity,
Gateway configuration, or an operator assertion is insufficient. Until such a
binding exists, `paid_to_other_agents_atomic`, `net_agent_flow_atomic`, and
unique counterparty-Agent count are `null`, not zero, and coverage explains
why. ATOS Native V1 currently defines no such general wallet-control binding.

For the fixed-price V1 profile,
`contributed_gross_agent_value_atomic == settled_revenue_atomic`. Summing the
contributed value over all provider Agents equals network
`gross_agent_value_atomic`; buyer-side subcontract spend is not attributed a
second time to the hiring Agent. This preserves one network contribution per
settled job while still exposing provable outbound spend separately.

## Per-Capability metrics

For each exact Capability and version, export:

- settled value and provider revenue, attributed to the provider Agent committed
  by each job's Accepted Quote;
- funded, settled, refunded, pending-entry, and open-pending job counts;
- unique buyer-wallet count;
- settlement success and refund rates;
- median settled price;
- median and P95 settlement duration;
- current finalized owner Agent ID;
- current Capability tombstone, version revocation, and effective owner-Agent
  tombstone status at the report end checkpoint; and
- last settled job finalized time.

Historical jobs remain attributed to the owner and version committed by their
Accepted Quote. A later Capability transfer or revocation changes the current
status but cannot rewrite historical attribution.

## Gross value and supply-chain duplication

Agent-to-Agent subcontracting creates a new paid job and therefore contributes
to gross Agent value. Summing all settlements intentionally measures gross
network activity and may count multiple stages of one supply chain.

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
  "schema": "atos.native.agent-economy-metrics.v1",
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
    "discovered_escrow_count": 0,
    "indexed_escrow_count": 0,
    "unresolved_escrow_count": 0,
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

`asset`, `authority.registry_code_hash`, and
`authority.escrow_code_hash` are mandatory. `scope.id` is empty only for
network reports; an Agent ID or Capability ID is mandatory otherwise, and
`scope.capability_version` is mandatory only for `capability_version`.

Both authority fields use exact TVM cell identities. The Registry identity is
required because every current economic report attributes jobs to a provider
Agent and Capability. The asset object supplies the exact stablecoin master
contract and wallet code identities. The discovery high-water checkpoint must
equal `as_of_finalized_checkpoint`.

For nonempty discovered sets,
`indexed_escrow_count + unresolved_escrow_count == discovered_escrow_count`.
These counts cover every escrow of the bound code identity discovered through
the report as-of checkpoint, not only escrows with an event in the selected
window. `indexed` means that the deployment, typed state, Quote linkage, and
relevant stablecoin transaction history resolve without ambiguity through that
checkpoint. Metrics exclude unresolved escrows and therefore lose total status
when the unresolved count is nonzero.

For `complete_chain_scan`, `index_origin_checkpoint` is the network genesis
checkpoint and `address_set_digest` is null. For `bounded_address_set`, the
address-set digest is mandatory. For `gateway_observed`, the response must name
the observing Gateway in discovery metadata; an address-set digest is optional
and cannot upgrade completeness.

Set commitments use fixed deterministic preimages:

```text
address_set_digest = "sha256:" || lowercase_hex(SHA-256(
  "atos.native.metrics-address-set.v1\0" ||
  count:uint32_be ||
  each sorted (workchain:int32_be || account_id:bytes32)
))

object_set_digest = "sha256:" || lowercase_hex(SHA-256(
  "atos.native.metrics-object-set.v1\0" ||
  count:uint32_be ||
  each sorted (utf8_length:uint16_be || canonical_object_id:utf8)
))
```

Sorting is lexicographic over each encoded binary entry. Sets reject duplicate
entries, zero account IDs, unsupported workchains, malformed object IDs, and
counts that exceed their encoded bounds.

`classification_coverage_ppm` is the integer floor of
`classified_job_count * 1,000,000 / provenance_eligible_job_count`; it is
`null` when the denominator is zero. Eligible jobs are settled jobs in the
selected economic window for which end-buyer classification would affect the
requested metric. The classified count must not exceed the eligible count.
This classification coverage concerns optional end-buyer provenance, not
chain-scan completeness.

Registry supply uses a separate conceptual envelope so it cannot inherit a
meaningless asset bucket, economic window, or escrow coverage:

```json
{
  "schema": "atos.native.agent-economy-registry-snapshot.v1",
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
    "discovered_object_count": 0,
    "indexed_object_count": 0,
    "unresolved_object_count": 0
  },
  "generated_at_unix_seconds": 0
}
```

The same completeness rule applies: only a genesis-to-checkpoint scan with zero
unresolved objects may use network-total labels. Snapshot generation time is
excluded from deterministic value comparison.

## Ranking

Clients may rank Agents by settled revenue, contributed gross value, settled
jobs, unique buyers, success rate, or recency. Every ranked row must expose the
underlying metric, its numerator and denominator where applicable, asset
identity, window, finality checkpoint, and coverage. Rankings must not combine
different stablecoin identities or treat online status as economic authority.
Ties are resolved by ascending canonical Agent ID so every implementation
produces the same order.

## Required implementation and acceptance

Implementation requires:

1. a rollback-protected genesis-to-high-water finalized transaction scanner,
   plus escrow, Registry, and stablecoin transaction indexes;
2. deterministic terminal-job classification and exact-asset aggregation;
3. network, Agent, and Capability export APIs;
4. if operational probes are exposed, a separate response and authority domain;
5. restart, reorg, pre-window-deployment, duplicate-event,
   conflicting-terminal, incomplete-discovery, partial-coverage,
   code-identity, owner-tombstone, asset-confusion, signed-net-flow, overflow,
   authenticated-block-time, time-window, percentile, refund, and
   pending-entry/open-pending tests;
6. an independent implementation reproducing frozen metric vectors; and
7. comparison of two independent indexers over the same network, code
   identities, asset, time window, and as-of finalized checkpoint.

Until all seven items exist, the feature remains **⬜ Not implemented** and no
Gateway may advertise its output as canonical ATOS GDP.
