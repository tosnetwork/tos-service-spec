# Agent Packet V1

Agent Packet V1 is the minimal decentralized Agent-to-Agent message envelope.
It supplements A2A/MCP transport without creating a second consensus protocol.

## Authority and transport

Packet payloads are off-chain bytes. TOS finalized Agent state authorizes the
sender controller key and proves that the sender and recipient Agents exist and
are live. A Gateway, relay, or transport connection cannot create identity or
authorization. The packet may travel over any authenticated channel, including
direct provider endpoints, A2A, MCP, or a Gateway used only as a router.

## Envelope

The signed preimage includes protocol domain `atos.agent.packet.v1`, sender and
recipient Agent IDs, Capability ID, optional finalized Accepted Quote
commitment, strictly positive sender sequence, 32-byte nonce, creation time,
sender Ed25519 public key, and SHA-256 of the payload. Payloads are bounded to
1 MiB. The signature is Ed25519 and is checked against a controller in the
finalized sender Agent policy.

The recipient must resolve the sender and recipient from finalized Native state
before accepting the packet. A local durable replay guard must atomically claim
`sender_agent_id + nonce`; retries of the same packet are rejected after the
first acceptance. The packet sequence is an application ordering signal, not a
replacement for on-chain Agent sequence.

## Commercial binding

An optional Quote commitment binds the packet to an Accepted Quote. It does not
authorize payment by itself: escrow funding, execution admission, Receipt, and
settlement still require their existing finalized-chain checks.

`tos-protocol/pkg/agentpacket` implements signing, finalized-state verification,
replay protection, and strict JSON wire encoding/decoding for transport
interoperability. It deliberately has no Gateway database, no arbitrary
on-chain message storage, and no Managed/Verified trust mode.
