# Agent Packet V1

Agent Packet V1 is the minimal decentralized Agent-to-Agent message envelope.
It supplements A2A/MCP transport without creating a second consensus protocol.

It is an existing messaging-profile component under
[`TOS_AGENTIC_INTERNET_OPERATION_ARCHITECTURE_V1.md`](TOS_AGENTIC_INTERNET_OPERATION_ARCHITECTURE_V1.md),
not the still-unfrozen common Agent Operation Envelope for every opcode family.

## Authority and transport

Packet payloads are off-chain bytes. TOS finalized Agent state authorizes the
sender controller key and proves that the sender and recipient Agents exist and
are live. A Gateway, relay, or transport connection cannot create identity or
authorization. The packet may travel over any authenticated channel, including
direct provider endpoints, A2A, MCP, or a Gateway used only as a router.

## Signed discovery

`ContactCard` is a signed, non-canonical locator that carries the Agent ID,
network tuple, HTTPS endpoint, bounded expiry, and optional Capability IDs. It
can be exchanged through DNS, a file, QR code, or another rendezvous channel;
the verifier resolves the Agent from finalized TOS state and checks that a live
controller signed the card. Expired cards, public plaintext endpoints, and
duplicate Capabilities are rejected; callers must additionally compare the
 card's network tuple with their local network policy. Production callers use
 `VerifyContactForNetwork` to enforce this comparison before dialing.

`EncodeContactJSON` and `DecodeContactJSON` provide the strict
`tos.service.agent-contact.v1` exchange format; unknown fields and trailing
JSON are rejected before the card is used.

## Envelope

The signed preimage includes protocol domain `tos.service.agent.packet.v1`, sender and
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

`tos-service-protocol/pkg/agentpacket` implements signing, finalized-state verification,
replay protection, and strict JSON wire encoding/decoding for transport
interoperability. It deliberately has no Gateway database, no arbitrary
on-chain message storage, and no Managed/Verified trust mode.

Its standard-library HTTP adapter accepts only bounded JSON `POST` requests,
verifies before delivery, claims the replay guard before invoking the receiver,
and rejects redirects. `Post` permits HTTPS endpoints and loopback HTTP for
development; production discovery and endpoint authentication remain the
operator's responsibility.
