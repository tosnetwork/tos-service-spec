# Gateway Discovery V1

## Purpose

Gateway discovery lets a client locate compatible TOS Service Protocol transport endpoints
without granting the publisher semantic authority. The document is an
availability hint. Every Agent, Capability, asset, escrow, Receipt, and
settlement claim remains subject to direct finalized TOS verification.

Gateways publish the document at:

```text
GET /.well-known/tos-service.json
```

The response media type is `application/json`. V1 is strict JSON: duplicate
keys, unknown fields, invalid UTF-8, non-integer numbers, and trailing data are
rejected.

## Document

```json
{
  "schema": "tos.service.gateway-discovery.v1",
  "protocol": "tos_service_v1",
  "network": {
    "network_id": "tos-mainnet",
    "genesis_root_hash": "sha256:<64 lowercase hex>",
    "genesis_file_hash": "sha256:<64 lowercase hex>"
  },
  "registry_code_hash": "tvm-cell-sha256:<64 lowercase hex>",
  "services": {
    "native_connect": "https://gateway.example/",
    "a2a_jsonrpc": "https://gateway.example/a2a",
    "mcp_streamable_http": "https://gateway.example/mcp"
  },
  "limits": {
    "max_request_bytes": 1048576,
    "max_response_bytes": 16777216
  },
  "expires_at_unix_seconds": 1786800000
}
```

Required fields are `schema`, `protocol`, `network`, `registry_code_hash`,
`services.native_connect`, `limits`, and `expires_at_unix_seconds`. A2A and MCP
service URLs are optional. V1 defines no wildcard service names or extension
map.

All service URLs must be absolute HTTPS URLs without user information or URL
fragments. Loopback development MAY use HTTP when the client explicitly opts
into insecure local operation. Redirects are not part of discovery and clients
must not follow them automatically.

The expiry must be in the future and no more than 24 hours after retrieval.
Clients may cache the exact document only until that time. An expired,
unavailable, malformed, or conflicting document yields no discovered Gateway;
it never permits fallback to a Managed mode or stale semantic state.

## Authority boundary

The discovery origin and TLS connection authenticate only the transport
operator. The document does not prove that:

- an Agent or Capability exists;
- a listed provider owns a Capability;
- a Quote Proposal is fair or accepted;
- an asset ticker identifies the intended stablecoin;
- an escrow is funded;
- execution or settlement succeeded; or
- the Gateway has a complete market view.

Clients must match the entire network tuple and Registry code hash to their
local policy before using any service. They then perform normal finalized
Native, stablecoin, escrow, and Receipt verification. Gateway responses cannot
override those checks.

V1 deliberately has no Gateway-controlled signing key or on-chain Gateway
registry. TLS and deployment policy are sufficient for locating transport;
adding a second identity hierarchy would not strengthen TOS-authoritative
commercial facts.

## Failover

A buyer may discover multiple Gateways and use any compatible one before Quote
acceptance. Local search results and Quote Proposals may differ.

After Quote acceptance, failover is allowed only from portable inputs:

- exact canonical manifest bytes and digest;
- finalized Capability and Agent references;
- Accepted Quote and escrow preimages;
- finalized escrow address and state;
- content-addressed input, artifact, report, and Receipt objects; and
- durable buyer/provider journals retained by their owners.

A replacement Gateway must reconstruct from those inputs and finalized TOS
state. It must not import another Gateway's hidden database or treat the old
Gateway's acknowledgement as authority.

## Security requirements

Clients must bound the document size, connection time, redirects, DNS results,
and response time. They must reject private, loopback, link-local, multicast,
or otherwise disallowed destinations when discovering remote Gateways, to
prevent SSRF. Credentials are selected only after the final origin has passed
policy checks and must never be forwarded across origins.

Conformance requires negative tests for wrong genesis, wrong Registry code
hash, expiry, HTTP downgrade, redirect, unknown field, duplicate key, oversized
body, and disallowed destination classes.
