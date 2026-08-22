# OpenFox Phase E independent acceptance record

**Status:** blank external evidence template. A repository maintainer, local
process, CI job or AI coding session MUST NOT fill operator attestations on
behalf of the independent parties.

## 1. Scope

This record binds one two-operator OpenFox Messenger round trip and, when Gate
D/E credit is claimed, one independently resolved commercial lifecycle. The
Messenger portion follows
`OpenFox/docs/guides/tos-messenger-independent-network.md`.

## 2. Independent parties

| Role | Legal/operator identity | Site/ASN/network | Attestation key | Signature |
|---|---|---|---|---|
| Alice OpenFox | TODO | TODO | TODO | TODO |
| Bob OpenFox/provider | TODO | TODO | TODO | TODO |
| Gateway/resolver | TODO | TODO | TODO | TODO |
| Independent reviewer | TODO | TODO | TODO | TODO |

No two required roles may be controlled by the same operator. Separate
processes, hosts, cloud instances, keys, repositories or AI agents under one
operator do not establish independence.

## 3. Immutable build and configuration binding

Record exact commit IDs and reproducible binary SHA-256 digests:

| Artifact | Commit | Binary/config digest | Operator |
|---|---|---|---|
| OpenFox Alice | TODO | TODO | TODO |
| OpenFox Bob/provider | TODO | TODO | TODO |
| `tos-messenger` Alice | TODO | TODO | TODO |
| `tos-messenger` Bob | TODO | TODO | TODO |
| `tos-service-protocol` | TODO | TODO | TODO |
| Gateway/resolver | TODO | TODO | TODO |

Attach redacted strict configuration documents or their canonical digests.
Redaction must not remove network identity, public endpoint, route mode,
quorum, policy ceilings or artifact identity. Never publish bearer tokens,
private keys, prekey private material or wallet secrets.

## 4. Network and finalized-state checkpoint

- Network ID: TODO
- Genesis root/file hashes: TODO
- Alice/Bob public TLS origins and certificate fingerprints: TODO
- Resolver/Gateway origins: TODO
- Finalized checkpoint before first contact: TODO
- Finalized checkpoint after completion/refund: TODO
- Capability ID/version/manifest digest/provider AgentID: TODO

## 5. Messenger evidence

- Alice transcript SHA-256: TODO
- Bob transcript SHA-256: TODO
- Initial recipient input (`.tos` or AgentID): TODO
- Canonical recipient AgentID: TODO
- Initial Event ID: TODO
- Reply Event ID and `reply_to_event_id`: TODO
- Bob OpenFox restart run IDs: TODO
- Bob daemon restart observation: TODO
- OpenFox verifier output: TODO
- Proof OpenFox had no peer-specific Endpoint/Device/Session/route input: TODO

Required command:

```text
openfox-messenger-evidence -left alice.json -right bob.json \
  -require-restart-agent agent_<bob>
```

The transcript verifier proves consistency, not operator independence. Each
operator signs its own transcript digest, public endpoint and run interval.

## 6. Commercial lifecycle evidence (when claimed)

- Opportunity intent and finalized candidate tuple: TODO
- Gateway hints and independent finalized re-resolution: TODO
- Quote Proposal and commitment: TODO
- Exact owner policy/mandate digest and authorization: TODO
- Escrow address and deterministic StateInit digest: TODO
- Funding transaction/finalized checkpoint: TODO
- Transport profile and execution ID: TODO
- Shared Execution Gate claim-store identity: TODO
- Receipt digest and provider signature: TODO
- Final provider credit or objective refund and checkpoint: TODO
- Original-Gateway loss/recovery observation: TODO
- Buyer/provider/reviewer transcript and artifact digests: TODO

Ambiguous funding, dispatch, release or refund is not a pass until canonical
finalized state resolves it. Gateway responses and chat text are never payment
or completion authority.

## 7. Fault and restart matrix

| Fault | Injection time | Expected invariant | Observation | Pass |
|---|---|---|---|---|
| Bob OpenFox restart | after first reply | no duplicate model turn/reply | TODO | TODO |
| Bob daemon restart | between messages | same AgentID conversation recovers | TODO | TODO |
| Original Gateway loss | after Quote/funding | finalized resolver/journal wins | TODO | TODO |
| Exact request replay | after ambiguous response | at-most-once mutation | TODO | TODO |
| Provider interruption | during execution | shared Gate prevents duplicate | TODO | TODO |

## 8. Verdict

- Messenger independent acceptance: TODO (`PASS` or `FAIL`)
- Commercial independent acceptance: TODO (`PASS`, `FAIL`, or `NOT CLAIMED`)
- Gate D/E credit claimed: TODO
- Remaining exceptions: TODO

All required operators and the independent reviewer sign the canonical digest
of the completed record and its attachments. A partial, unsigned or
self-operated record remains implementation/smoke evidence only.
