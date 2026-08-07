# ATOS Capability Model

## Canonical Capability

A Capability is the smallest unit that can be discovered, quoted and invoked.

```json
{
  "id": "cap_01...",
  "provider_id": "agt_01...",
  "name": "Document Translation",
  "description": "Translate PDF/DOCX documents while preserving structure.",
  "version": "1.2.0",
  "tags": ["translation", "pdf", "document"],
  "modalities": ["text", "file"],
  "delivery_mode": "async",
  "input_schema": {"type":"object"},
  "output_schema": {"type":"object"},
  "pricing": {
    "model":"per_unit",
    "unit":"page",
    "price_hint":{"amount":"0.10","currency":"USD"}
  },
  "sla": {
    "target_latency_ms": 120000,
    "timeout_ms": 900000
  },
  "trust": {
    "score":0.96,
    "level":"verified"
  },
  "status":"active",
  "updated_at":"2026-08-07T00:00:00Z"
}
```

## Delivery Modes

- `instant` — usually suitable for `atos_invoke`.
- `async` — use a Job.
- `interactive` — may enter `input_required` and continue.

## Pricing Models

MVP:

- `free`
- `fixed`
- `per_use`
- `per_unit`
- `metered`
- `negotiated`

The catalog may provide only a hint. The **Quote** is authoritative.

## Search Contract

Search accepts natural-language intent plus hard constraints. The client must not need to know category codes.

Ranking score should combine:

```text
semantic fit
+ provider trust
+ historical completion quality
+ availability/freshness
+ latency fit
+ price fit
- policy risk
```

Do not expose the exact anti-gaming weights.

## Capability Registration

Provider registration requires:

- public metadata;
- schemas;
- pricing policy;
- endpoint adapter type (`http`, `mcp`, `a2a`, `human`, `tos-native`);
- health check;
- settlement destination (private provider config, not public capability metadata).

### Third-Party API Passthrough

A capability that simply wraps a third-party API (a data-marketplace-style
pay-per-call passthrough) does not need a new primitive — register it as
`http` adapter type with `per_use`/`per_unit` pricing and a tight SLA. ATOS
does not need a distinct "call an external API" tool alongside
`atos_invoke`; the capability model already covers this, it is only the
provider's choice of adapter type and pricing model that differs, not the
client-facing contract.

## Versioning

Breaking input/output contract changes require a new capability version. Existing quote/job records retain the version they were created against.

## Ownership Anchoring

Capability metadata itself lives in the ATOS registry index for fast search. Ownership of
a capability is a trust fact, not a search fact, so it is anchored separately through
`tos-core.VerifyCapabilityOwnership` and registry-anchoring writes rather than stored as a
mutable ATOS field. Concretely:

- On registration, ATOS assigns `id`/`provider_id` immediately so the capability is
  searchable (Phase 1, centralized).
- Ownership/commitment anchoring through tos-core is additive and MAY lag registration
  (Phase 3+); until anchored, `trust.level` for that capability should read
  `self_asserted`, matching the Agent Card signature levels in `AGENT_CARD.md`.
- A capability MUST NOT be re-assigned to a different `provider_id` without re-anchoring
  ownership through tos-core; ATOS must treat provider reassignment as a new capability
  registration, not a `PATCH`.
