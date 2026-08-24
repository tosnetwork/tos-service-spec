# HTTP Payment Adapter Decision

## Decision

TOS Service Protocol does not implement an x402 settlement scheme in Gate E. The optional
adapter is deferred until Gate F demonstrates recurring demand from buyers
that already use x402.

This is a scope decision, not a rejection of x402. The x402 version 2
specification deliberately separates common types, scheme-specific payment
logic, and transport representation. Its documented `exact` EVM scheme uses
EIP-3009 authorization. TOS-network stablecoin escrow has a different
authorization, finality, Receipt, refund, and settlement state machine.

Implementing an x402 facilitator or an `exact`-like TOS settlement path now
would create a second payment authority beside the canonical TOS Service Protocol escrow. It
would violate the Native-only architecture and make success depend on a
facilitator response rather than finalized TOS state.

Primary reference: the
[x402 protocol version 2 specification](https://github.com/coinbase/x402/blob/main/specs/x402-specification-v2.md).

## Permitted future adapter

A future adapter may use x402 only as a negotiation and representation layer:

- `PaymentRequired` may project a non-canonical TOS Service Protocol Quote Proposal;
- the resource must identify the exact Capability and version;
- the payment requirements must identify the exact TOS network, stablecoin,
  amount, provider, and deterministic escrow terms;
- the client must independently resolve the Capability, manifest, Agent,
  asset, Quote commitment, and escrow;
- a submitted payload may carry an already-created escrow commitment or
  finalized chain reference, but cannot authorize a parallel transfer;
- a facilitator response is transport evidence only; and
- success requires the exact escrow and amount in finalized TOS state, followed
  by the canonical Receipt and settlement transition.

The adapter must reuse the existing Buyer SDK, budget journal, escrow resolver,
execution Gate, and Receipt verifier. It must not introduce another wallet
journal, replay identity, Quote acceptance rule, or settlement database.

## Conditions for implementation

Implementation becomes eligible only when all of the following are true:

1. Gate F has evidence of recurring paid use.
2. At least one real buyer requires x402 interoperability.
3. A reviewed TOS network identifier and scheme representation exist.
4. Conformance tests prove that x402 cannot bypass escrow deployment, buyer
   budget enforcement, finalized funding, single execution, Receipt checking,
   or settlement finality.
5. Gateway or facilitator failure cannot change or erase any canonical fact.

Until then, A2A and MCP cover task transport, while the Native Buyer SDK and
TOS escrow remain the single payment path.
