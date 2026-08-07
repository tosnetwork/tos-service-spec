# ATOS Capability Model v0.2

## 1. Canonical Capability

A **Capability** is the smallest unit of supply that can be discovered, quoted and invoked.

A Capability is independent of trust mode. The same capability may be available through `managed`, `verified`, and/or `native` execution without becoming three different Agent-facing products.

```json
{
  "id": "cap_01...",
  "provider_id": "agt_01...",
  "name": "Document Translation",
  "description": "Translate PDF/DOCX documents while preserving structure.",
  "version": "1.2.0",
  "manifest_commitment": "sha256:...",
  "tags": ["translation", "pdf", "document"],
  "modalities": ["text", "file"],
  "delivery_mode": "async",
  "input_schema": {"type":"object"},
  "output_schema": {"type":"object"},
  "supported_trust_modes": ["managed", "verified", "native"],
  "transports": ["mcp", "a2a", "http"],
  "pricing": {
    "model":"per_unit",
    "unit":"page",
    "price_hint":{"amount":"0.10","currency":"USD"}
  },
  "sla": {
    "target_latency_ms": 120000,
    "timeout_ms": 900000
  },
  "trust_summary": {
    "score":0.96,
    "identity_assurance":"tos_attested",
    "proof_of_service_count":12831
  },
  "ownership": {
    "status":"anchored",
    "network":"tos",
    "commitment":"tos:..."
  },
  "status":"active",
  "updated_at":"2026-08-07T00:00:00Z"
}
```

## 2. Trust Modes on Capabilities

`supported_trust_modes` contains only concrete modes:

```text
managed
verified
native
```

`auto` MUST NOT appear in `supported_trust_modes`. `auto` is a caller-side selection policy used before a Quote resolves to one concrete mode.

A provider MAY support different endpoint bindings, availability, pricing overhead, or proof requirements by trust mode, but the Agent-facing Capability identity remains the same.

Example mode support:

```json
{
  "supported_trust_modes":["managed","verified"],
  "mode_support": {
    "managed": {
      "status":"active"
    },
    "verified": {
      "status":"active",
      "proof_profile":"tos_verified_v1"
    },
    "native": {
      "status":"unsupported"
    }
  }
}
```

A capability MUST NOT advertise `verified` or `native` until the gateway can satisfy the minimum guarantees defined in `docs/ARCHITECTURE_V0.2.md`.

## 3. Trust Summary Is Not Trust Mode

A capability's reputation/identity quality and a transaction's trust mode are different dimensions.

Do not use ambiguous fields such as:

```json
{"trust":{"level":"verified"}}
```

because `verified` is also a transaction trust mode.

Use an explicit summary instead:

```json
{
  "trust_summary": {
    "score": 0.96,
    "identity_assurance": "tos_attested",
    "proof_of_service_count": 12831,
    "last_updated_at": "2026-08-07T00:00:00Z"
  }
}
```

A gateway-computed `score` is a convenience ranking signal. It MUST NOT be presented as a globally canonical TOS value. Verifiable evidence is represented separately through identity attestations, ownership commitments, Execution Receipts, and Proof-of-Service references.

## 4. Delivery Modes

Delivery mode describes execution interaction, not trust.

- `instant` — usually suitable for `atos_invoke`.
- `async` — use a Job.
- `interactive` — may enter `input_required` and continue.

Any delivery mode MAY be combined with any supported trust mode.

## 5. Pricing Models

Supported pricing models:

- `free`
- `fixed`
- `per_use`
- `per_unit`
- `metered`
- `negotiated`

The catalog may provide only a hint. The **Quote** is authoritative.

A capability MAY expose mode-specific pricing hints because TOS-backed proof/escrow may have different costs, but the client MUST rely on `atos_quote` for the final price.

Example:

```json
{
  "pricing": {
    "model":"fixed",
    "price_hint":{"amount":"5.00","currency":"USD"},
    "mode_hints": {
      "managed":{"amount":"5.00","currency":"USD"},
      "verified":{"amount":"5.05","currency":"USD"},
      "native":{"amount":"5.02","currency":"USD"}
    }
  }
}
```

Mode hints are non-binding.

## 6. Search Contract

Search accepts natural-language intent plus hard constraints. The client must not need to know category codes or blockchain internals.

Search MAY accept:

- `requested_trust_mode: managed | verified | native | auto`;
- required proof properties;
- maximum price;
- latency/SLA constraints;
- modality;
- geography/jurisdiction;
- minimum reputation/identity requirements.

Ranking should combine:

```text
semantic fit
+ provider reputation/evidence
+ historical completion quality
+ availability/freshness
+ latency fit
+ price fit
+ requested trust/proof fit
- policy risk
```

Do not expose exact anti-gaming weights.

Search results SHOULD return `supported_trust_modes` and mode availability so the client knows whether a later Quote can satisfy its policy.

## 7. Capability Registration

Provider registration requires:

- public metadata;
- input/output schemas;
- pricing policy;
- delivery mode;
- endpoint binding(s) (`http`, `mcp`, `a2a`, `human`, `tos-native`, or future adapters);
- health check policy;
- requested concrete trust-mode support;
- settlement destination/configuration as private provider data.

### Mode activation

Registration and trust-mode activation are separate concerns.

#### Managed

A capability may become searchable in Managed Mode after ordinary gateway validation.

#### Verified

Before `verified` becomes active, the implementation MUST be able to provide the applicable proof profile, including at minimum:

- TOS-backed provider identity/capability ownership;
- immutable capability version/manifest commitment;
- quote/terms commitment;
- TOS-backed escrow for paid committed work;
- signed Execution Receipt and TOS-verifiable receipt commitment;
- TOS-backed settlement proof;
- portable Proof-of-Service evidence.

#### Native

Before `native` becomes active, all Verified guarantees apply and the capability MUST additionally be globally resolvable without relying on `atos.im` as the canonical registry.

A provider MAY request a new mode before it is active. Public capability metadata MUST distinguish `requested`, `pending`, `active`, `suspended`, and `unsupported` mode states rather than falsely advertising a guarantee that has not been provisioned.

## 8. Endpoint Bindings

Transport is separate from trust mode.

A capability may expose one or more bindings:

```json
{
  "bindings": [
    {
      "transport":"mcp",
      "endpoint_ref":"ep_...",
      "trust_modes":["managed","verified"]
    },
    {
      "transport":"a2a",
      "endpoint_ref":"ep_...",
      "trust_modes":["native"]
    }
  ]
}
```

Public metadata SHOULD expose transport type and availability but MUST NOT expose provider secrets, private network topology, internal prompts, wallet keys, or sensitive settlement configuration.

## 9. Third-Party API Passthrough

A capability that wraps a third-party API does not need a separate primitive.

Register it as an `http` binding with suitable pricing and SLA. The client still uses `atos_invoke` or `atos_create_job`.

If the wrapper advertises `verified`, the ATOS/TOS guarantees apply to the wrapper's delivered service and receipt. They do not magically make the upstream third-party API itself decentralized or independently trustworthy beyond the evidence actually committed.

## 10. Versioning and Manifest Commitments

Breaking input/output contract changes require a new capability version. Existing Quotes, Jobs, and Receipts retain the version they were created against.

For `verified` and `native`, the quoted version MUST resolve to an immutable `manifest_commitment` covering at least the fields necessary to prove what was bought, including:

- capability ID;
- provider ID;
- semantic version;
- input/output schema commitments;
- relevant delivery/SLA terms;
- mode/proof compatibility;
- immutable provider execution identity/binding references where required by the proof profile.

Mutable discovery metadata such as descriptions, tags, popularity, health snapshots, and gateway ranking features do not need to be inside the immutable manifest unless a proof profile explicitly requires them.

## 11. Global IDs and Federation

Public Capability IDs MUST be designed for multi-gateway federation from v0.2 onward.

A global ID MUST be collision-resistant across independent gateways. The exact encoding is deferred, but it MAY be:

- provider-key-derived;
- self-certifying;
- issuer-namespaced;
- another protocol-defined globally unique scheme.

It MUST NOT be merely an auto-increment primary key from the `atos.im` database.

Gateways MAY maintain local aliases and database keys, but those are implementation details.

Conceptual addressing:

```text
atos://capability/<global-capability-id>
```

## 12. Ownership Anchoring

Capability metadata is indexed off-chain for fast search. Ownership is a trust fact and is anchored separately through `tos-core`/TOS.

Concretely:

- Managed registration MAY create a capability before any TOS anchor exists.
- Until ownership is anchored, the capability may operate in `managed` but MUST NOT advertise `verified` or `native` merely because the provider self-asserted ownership.
- Verified/Native activation requires the ownership state required by the selected proof profile.
- A capability MUST NOT be reassigned to another `provider_id` through a normal metadata patch.
- Provider reassignment requires a protocol-defined ownership transfer/re-anchoring operation or a new capability identity.

## 13. Availability and Health by Mode

Availability MAY differ by trust mode.

Example:

```json
{
  "availability": {
    "managed":{"status":"online"},
    "verified":{"status":"degraded","reason":"tos_settlement_delayed"},
    "native":{"status":"offline","reason":"resolver_unavailable"}
  }
}
```

A gateway MUST NOT silently route a request quoted for `verified` or `native` through a weaker mode because the stronger path becomes unavailable. It must fail, wait according to the quoted SLA, or require a new Quote.

## 14. Capability Invariants

1. One capability identity may support multiple concrete trust modes.
2. `auto` is request-only and never a supported concrete mode.
3. Delivery mode and trust mode are orthogonal.
4. Trust/reputation score is not the same thing as transaction trust mode.
5. A Quote, not catalog pricing, determines the final commercial terms and concrete mode.
6. Verified/Native capability versions have immutable verifiable manifest commitments.
7. Native capabilities are globally resolvable without `atos.im` as canonical registry.
8. Search metadata remains off-chain and indexable; ownership/proof facts may be TOS-backed.
9. Mode unavailability never permits a silent downgrade after Quote issuance.
