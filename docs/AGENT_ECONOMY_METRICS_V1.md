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
finalized TOS transaction interval and discovers every escrow deployment by the
frozen escrow code identity and authenticated StateInit. A Gateway catalog,
known-address list, provider feed, or API traffic log is necessarily partial
because it cannot prove that no other escrow exists.

Every report declares one discovery mode:

- `complete_chain_scan`: complete finalized transaction coverage for the
  stated checkpoint interval; network totals are permitted;
- `bounded_address_set`: an explicit committed set of escrow addresses; only
  observed aggregates are permitted; or
- `gateway_observed`: traffic- or catalog-derived discovery; only observed
  aggregates are permitted.

For `bounded_address_set`, the export binds a digest of the sorted canonical
address set. For `complete_chain_scan`, it binds the scanner's inclusive master
checkpoint interval. Unknown or unresolved escrows cannot be represented as a
percentage of an unknown universe; a partial report therefore never uses the
word `total`. Even with `complete_chain_scan`, network totals require
`unresolved_escrow_count == 0`; otherwise the values remain observed lower
bounds for counts and amounts and observed-sample statistics for rates and
distributions.

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
| `release_pending_job_count` | Nonterminal release attempts whose request finalized in the window and still lack a derived terminal outcome at the report end checkpoint. |
| `refund_pending_job_count` | Nonterminal refund attempts whose request finalized in the window and still lack a derived terminal outcome at the report end checkpoint. |
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

The standard windows are `1h`, `24h`, `7d`, `30d`, and `all`. Every time window
is the half-open interval `[from_unix_seconds, to_unix_seconds)`. Membership is
based on the terminal finalized time for terminal value, terminal count, rate,
and duration metrics; on funding finalized time for `funded_job_count`; and on
pending-request finalized time for pending counts. An `all` report starts at
genesis. A bounded report may start later but cannot call itself all-time. The
checkpoint range is inclusive and must contain every finalized transaction
used by the time interval.

## Registry snapshot metrics

Active Registry supply is not a stablecoin-specific economic value. It is exported
once per network at the report end checkpoint, outside every asset bucket:

- `active_agent_count`;
- `active_capability_count`; and
- `active_capability_version_count`.

These counts do not claim that a provider is online, willing to quote, or able
to execute, so they must not be labelled "purchasable offerings". Network-wide
names require a complete finalized Registry-account scan. A Gateway-local
Capability catalog may export only observed snapshot counts.

## Per-Agent metrics

For a provider Agent, export:

- `gross_agent_value_atomic`;
- `settled_revenue_atomic`;
- `paid_to_other_agents_atomic` when the same controlled wallet is provably the
  buyer in another verified job;
- `net_agent_flow_atomic = settled_revenue - paid_to_other_agents`, encoded as
  the signed canonical decimal form defined above;
- funded, settled, refunded, release-pending, and refund-pending job counts;
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

## Per-Capability metrics

For each exact Capability and version, export:

- settled value and provider revenue, attributed to the provider Agent committed
  by each job's Accepted Quote;
- funded, settled, refunded, release-pending, and refund-pending job counts;
- unique buyer-wallet count;
- settlement success and refund rates;
- median settled price;
- median and P95 settlement duration;
- current finalized owner Agent ID;
- current tombstone/revocation status at the report end checkpoint; and
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

Every network, Agent, or Capability report uses the following conceptual JSON
envelope:

```json
{
  "schema": "atos.native.agent-economy-metrics.v1",
  "scope": {
    "kind": "network|agent|capability_version|registry_snapshot",
    "id": "",
    "capability_version": null
  },
  "network": {},
  "asset": {},
  "window": "24h",
  "from_unix_seconds": 0,
  "to_unix_seconds": 0,
  "first_finalized_checkpoint": 0,
  "last_finalized_checkpoint": 0,
  "discovery": {
    "mode": "complete_chain_scan|bounded_address_set|gateway_observed",
    "address_set_digest": null
  },
  "metrics": {},
  "coverage": {
    "discovered_escrow_count": 0,
    "indexed_escrow_count": 0,
    "unresolved_escrow_count": 0,
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

`asset` is mandatory for economic network, Agent, and Capability-version
reports. It is `null` only for `registry_snapshot`, whose metrics contain no
monetary values. `scope.id` is empty only for network and Registry-snapshot
reports; an Agent ID or Capability ID is mandatory otherwise, and
`scope.capability_version` is mandatory only for `capability_version`.

For nonempty discovered sets,
`indexed_escrow_count + unresolved_escrow_count == discovered_escrow_count`.
`classification_coverage_ppm` is the integer floor of
`classified_job_count * 1,000,000 / indexed_escrow_count`; it is `null` when
the denominator is zero. This classification coverage concerns optional
end-buyer provenance, not chain-scan completeness.

## Ranking

Clients may rank Agents by settled revenue, gross value, settled jobs, unique
buyers, success rate, or recency. Every ranked row must expose the underlying
metric, asset identity, window, finality checkpoint, and coverage. Rankings
must not combine different stablecoin identities or treat online status as
economic authority. Ties are resolved by ascending canonical Agent ID so every
implementation produces the same order.

## Required implementation and acceptance

Implementation requires:

1. a rollback-protected complete finalized transaction scanner, plus escrow,
   Registry, and stablecoin transaction indexes;
2. deterministic terminal-job classification and exact-asset aggregation;
3. network, Agent, and Capability export APIs;
4. if operational probes are exposed, a separate response and authority domain;
5. restart, reorg, duplicate-event, conflicting-terminal, incomplete-discovery,
   partial-coverage, asset-confusion, signed-net-flow, overflow, time-window,
   percentile, refund, and both pending-state tests;
6. an independent implementation reproducing frozen metric vectors; and
7. comparison of two independent indexers over the same finalized checkpoint
   interval.

Until all seven items exist, the feature remains **⬜ Not implemented** and no
Gateway may advertise its output as canonical ATOS GDP.
