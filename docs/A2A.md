# ATOS A2A Profile v0.2

## Purpose

Use A2A for stateful agent-to-agent collaboration. MCP remains the preferred client/tool surface for Codex-like hosts; A2A is the provider/inter-agent interoperability surface.

Reference gateway endpoint:

`https://a2a.atos.im`

Discovery:

`https://atos.im/.well-known/agent-card.json`

Native ATOS does not require all A2A traffic to pass through this reference endpoint; independently operated gateways/providers may expose compatible A2A endpoints.

## Mapping

ATOS maps A2A Tasks to ATOS Jobs.

| A2A concept | ATOS business object |
|---|---|
| Agent Card | Provider/ATOS discovery card |
| Task | Job |
| Message | Job interaction message |
| Artifact | Artifact |
| Task state | Job state |

## State Mapping

- `submitted` -> `submitted`
- `working` -> `working`
- `input-required` -> `input_required`
- `completed` -> `completed`
- `failed` -> `failed`
- `canceled` -> `canceled`
- provider refusal -> `rejected`

The A2A Task/ATOS Job inherits the concrete trust mode from its Quote.

## Trust-Mode Semantics

Pre-Quote policy may use:

```text
requested_trust_mode = managed | verified | native | auto
```

Once a Quote is selected, Task/Job commerce metadata uses:

```text
trust_mode = managed | verified | native
```

`auto` MUST NOT appear as the final Task/Job mode.

A remote agent MUST NOT reinterpret a quoted `verified` or `native` Task as Managed. If it cannot satisfy the Quote's proof profile, it must reject/fail the work so the caller can re-quote.

## ATOS Commerce Extension

ATOS-specific commercial/trust fields SHOULD be carried through an A2A extension instead of changing core A2A objects.

Proposed v0.2 extension URI:

`https://atos.im/extensions/commerce/v2`

### Pre-Quote request policy

```json
{
  "requested_trust_mode":"auto",
  "proof_requirements":{
    "network_verifiable_receipt":true,
    "tos_settlement":false
  },
  "max_total":{"amount":"10.00","currency":"USD"}
}
```

### Quote-bound Task/Job fields

```json
{
  "quote_id":"q_...",
  "trust_mode":"verified",
  "proof_profile":"tos_verified_v1",
  "price":{"total_max":"5.25","currency":"USD"},
  "settlement":{"backend":"tos","escrow":true},
  "proof_status":{
    "quote":"committed",
    "escrow":"reserved",
    "receipt":"pending",
    "settlement":"pending"
  },
  "idempotency_key":"..."
}
```

Do not put wallet private keys, chain RPC credentials, payment credentials, provider secrets, prompts, or private artifacts into extension fields.

## Quote Authority

The ATOS Quote is the commercial/trust contract.

After a Task is associated with `quote_id`:

- capability/provider/version must match the Quote;
- concrete `trust_mode` must match the Quote;
- proof profile must match the Quote;
- maximum price/terms must match the Quote;
- a change to any of these requires a new Quote.

A2A messages may continue an interactive Task but MUST NOT mutate the Quote's trust contract.

## Artifacts and Receipts

A2A Artifacts remain off-chain by default.

For Verified/Native work, the final Execution Receipt may commit:

- artifact hashes;
- output commitment;
- usage commitment;
- provider signature;
- TOS proof reference.

Conceptual final commerce extension:

```json
{
  "quote_id":"q_...",
  "trust_mode":"native",
  "receipt":{
    "receipt_id":"rcpt_...",
    "output_commitment":"sha256:...",
    "proof_status":"verified",
    "network_proof_ref":"tos:..."
  }
}
```

## Provider Federation

Managed/Verified proxy path:

```text
Client Agent -> atos.im A2A Gateway -> remote Agent Card -> remote A2A Agent
```

Native/federated path:

```text
Client Agent -> any ATOS resolver/gateway -> TOS capability resolution -> provider A2A endpoint
```

The caller receives the same ATOS Job/Receipt semantics in either case.

## A2A Invariants

1. A2A Task maps to one ATOS Job.
2. `auto` is allowed only before Quote resolution.
3. Quote-bound Task/Job uses one concrete trust mode.
4. A2A extension carries ATOS commerce/proof state without modifying core A2A semantics.
5. Artifact bytes remain off-chain; commitments may be included in Verified/Native receipts.
6. Native routing does not require `a2a.atos.im` as the canonical intermediary.
7. No remote agent or gateway may silently downgrade a quoted trust mode.
