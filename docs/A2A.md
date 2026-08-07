# ATOS A2A Profile

## Purpose

Use A2A for stateful agent-to-agent collaboration. MCP is the preferred client/tool surface for Codex-like hosts; A2A is the provider/inter-agent interoperability surface.

Endpoint:

`https://a2a.atos.im`

Discovery:

`https://atos.im/.well-known/agent-card.json`

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

## Extensions

ATOS-specific commercial fields SHOULD be carried in an A2A extension rather than modifying core A2A objects.

Proposed extension URI:

`https://atos.im/extensions/commerce/v1`

Extension fields:

```json
{
  "quote_id": "q_...",
  "price": {"total_max":"5.25","currency":"USD"},
  "settlement_mode": "atos",
  "trust": {"score":0.96},
  "idempotency_key": "..."
}
```

Do not put wallet private keys, chain RPC credentials or provider secrets into extension fields.

## Provider Federation

ATOS may proxy a remote A2A Agent:

```text
Client Agent -> ATOS A2A Gateway -> remote Agent Card -> remote A2A Agent
```

or resolve through TOS Network:

```text
Client Agent -> ATOS -> TOS provider resolution -> provider endpoint -> A2A
```

The caller receives the same public ATOS job contract in either case.
