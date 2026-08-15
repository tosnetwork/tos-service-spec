# MCP Software-Work Tool Adapter V1

The MCP tool `atos_native_software_work` maps the official MCP Go SDK's typed
`tools/call` boundary into the same Native software-work runner. MCP is
model-controlled transport; tool discovery, arguments, client identity, and
tool results have no Agent, payment, Receipt, or settlement authority.

The input contains the exact funded escrow address, Accepted Quote commitment,
execution ID, input digest, source digest, and canonical standard-Base64 source
archive. The input digest uses domain `atos.mcp.software-work-input.v1`, a zero byte, and canonical
JSON of protocol, escrow address, Quote, execution ID, and source digest. Unknown or changed
bytes fail before authoritative reads.

Before execution, a production gate must both verify finalized Capability,
manifest, Accepted Quote, funded escrow, endpoint, and signer, and atomically
claim one `(Quote commitment, escrow, execution ID, input digest, source
digest)` intent under the shared `(Quote commitment, escrow)` purchase slot.
The same slot is used by A2A and every future adapter. Merely
observing a funded escrow is insufficient: accepting another execution ID for
the same purchase would allow repeated unpaid computation.

Success returns structured content containing finalized evidence and exact
result, artifact, report, source, toolchain, and sandbox commitments. Artifact
locations require HTTPS and remain unauthenticated transport hints; their
SHA-256 digests authenticate bytes. Tool success is neither a signed Receipt
nor permission to release funds.

V1 uses official Go SDK `github.com/modelcontextprotocol/go-sdk` v1.7.0 and its
MCP 2026-07-28 tool model. Experimental MCP task augmentation, sampling,
prompts, resources, arbitrary commands, remote policy selection, and automatic
payment are outside this adapter.

The production finalized execution-claim Gate and official stateless
streamable-HTTP binding are implemented. The shared public boundary requires
TLS 1.3, bearer authentication, bounded bodies/headers/concurrency, and rejects
browser origins by default. Gate E completion still requires a fresh
interoperability session.
