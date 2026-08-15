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

The metrics service is an incomplete, replaceable projection. Its output must
carry its network domain, finalized checkpoint range, exact asset identity,
calculation version, and coverage. Two indexers observing the same complete
finalized inputs must produce the same result.

Quote Proposals, search impressions, endpoint claims, token prices, unfinalized
transactions, self-reported revenue, and Gateway-local balances never count as
economic output.

## Canonical job identity and terminal facts

One commercial job is identified by:

```text
job_id = SHA-256("atos.native.economic-job.v1\0" ||
                quote_commitment || escrow_address)
```

Transport retries, Agent Packets, A2A messages, MCP calls, internal tool calls,
artifacts, and settlement retries do not create additional jobs.

A settled job may contribute economic value only after an indexer independently
verifies the complete terminal chain:

```text
finalized Accepted Quote
→ authenticated finalized escrow funding
→ canonical Receipt commitment
→ authenticated stablecoin-wallet transfer
→ finalized release outcome
```

A refund contributes job activity and refund statistics, but contributes zero
provider revenue and zero settled service value. `release_pending` is exported
separately and never counted as settled merely because the escrow requested a
transfer. Ambiguous or divergent chain observations fail closed.

## Amount and asset rules

All amounts are unsigned base-10 atomic-unit strings. Aggregation is performed
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

## Network metrics

For each time window and exact asset bucket, export:

| Field | Definition |
|---|---|
| `gross_agent_value_atomic` | Sum of verified settled service payments. |
| `settled_provider_revenue_atomic` | Amount actually transferred to providers. |
| `funded_job_count` | Unique jobs whose exact escrow funding finalized. |
| `settled_job_count` | Unique jobs with verified terminal provider payment. |
| `refunded_job_count` | Unique jobs with verified terminal buyer refund. |
| `release_pending_job_count` | Nonterminal release attempts awaiting authoritative resolution. |
| `unique_buyer_wallet_count` | Distinct canonical buyer wallet addresses among included jobs. |
| `unique_provider_agent_count` | Distinct provider Agent IDs among included jobs. |
| `active_capability_count` | Distinct non-tombstoned Capabilities observed at the report end checkpoint. |
| `active_capability_version_count` | Distinct unrevoked versions at that checkpoint. |
| `settlement_success_rate_ppm` | `settled / (settled + refunded)` in integer parts per million. |
| `refund_rate_ppm` | `refunded / (settled + refunded)` in integer parts per million. |
| `median_settlement_seconds` | Median finalized funding-to-terminal duration. |
| `p95_settlement_seconds` | Nearest-rank P95 finalized funding-to-terminal duration. |

Zero-denominator rates are `null`, not zero. Durations use finalized block time,
not Gateway receipt time or local wall-clock time.

The standard windows are `1h`, `24h`, `7d`, `30d`, and `all`. Window membership
is based on the terminal finalized time for terminal metrics and the funding
finalized time for funded-job metrics.

## Per-Agent metrics

For a provider Agent, export:

- `gross_agent_value_atomic`;
- `settled_revenue_atomic`;
- `paid_to_other_agents_atomic` when the same controlled wallet is provably the
  buyer in another verified job;
- `net_agent_revenue_atomic = settled_revenue - paid_to_other_agents`;
- funded, settled, refunded, and release-pending job counts;
- unique buyer-wallet count;
- unique counterparty-Agent count where both identities are provably bound;
- settlement success and refund rates;
- median and P95 settlement duration;
- active Capability and active Capability-version counts;
- Capability utilization, defined as Capabilities with at least one settled job
  divided by active Capabilities, in integer parts per million; and
- last settled job finalized time.

Wallet-to-Agent control must be established by an explicit finalized protocol
binding before Agent spend or net revenue is exported. Address similarity,
Gateway configuration, or an operator assertion is insufficient. Until such a
binding exists, the affected fields are `null` and coverage explains why.

## Per-Capability metrics

For each exact Capability and version, export:

- settled value and provider revenue;
- funded, settled, refunded, and pending job counts;
- unique buyer-wallet count;
- settlement success and refund rates;
- median settled price;
- median and P95 settlement duration;
- current finalized owner Agent ID;
- current tombstone/revocation status; and
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
wallet, not an economic provenance graph, so this field is initially `null`.
It must include `classified_job_count` and `classification_coverage_ppm` when
implemented. A Gateway must never infer end-buyer status from traffic or labels.

## Availability and operational metrics

The following useful discovery signals are non-authoritative and must be
exported under a separate `operational` object:

- `online`;
- `last_seen_at`;
- `minutes_since_last_seen`;
- `endpoint_latency_ms`; and
- `recent_transport_success_rate_ppm`.

They may be derived from A2A, MCP, Agent Packet, or HTTPS probes. Every value
must identify the observing operator and observation time. These signals cannot
authorize execution, payment, ranking as a protocol fact, or Capability use.

## Export envelope

Every network, Agent, or Capability report uses the following conceptual JSON
envelope:

```json
{
  "schema": "atos.native.agent-economy-metrics.v1",
  "scope": { "kind": "network|agent|capability", "id": "" },
  "network": {},
  "asset": {},
  "window": "24h",
  "from_unix_seconds": 0,
  "to_unix_seconds": 0,
  "first_finalized_checkpoint": 0,
  "last_finalized_checkpoint": 0,
  "metrics": {},
  "coverage": {
    "indexed_escrow_count": 0,
    "unresolved_escrow_count": 0,
    "classified_job_count": 0,
    "classification_coverage_ppm": 0
  },
  "operational": {},
  "generated_at_unix_seconds": 0
}
```

The concrete protobuf/Connect API remains unimplemented. The implementation
must use integer counters and atomic-unit strings; floating-point monetary
values are forbidden. Pagination and ranking are derived presentation features,
not protocol authority.

## Ranking

Clients may rank Agents by settled revenue, gross value, settled jobs, unique
buyers, success rate, or recency. Every ranked row must expose the underlying
metric, asset identity, window, finality checkpoint, and coverage. Rankings
must not combine different stablecoin identities or treat online status as
economic authority.

## Required implementation and acceptance

Implementation requires:

1. a rollback-protected finalized escrow and stablecoin transaction index;
2. deterministic terminal-job classification and exact-asset aggregation;
3. network, Agent, and Capability export APIs;
4. optional operational probes kept in a separate authority domain;
5. restart, reorg, duplicate-event, partial-coverage, asset-confusion,
   overflow, time-window, percentile, refund, and pending-state tests;
6. an independent implementation reproducing frozen metric vectors; and
7. comparison of two independent indexers over the same finalized checkpoint
   interval.

Until all seven items exist, the feature remains **⬜ Not implemented** and no
Gateway may advertise its output as canonical ATOS GDP.
