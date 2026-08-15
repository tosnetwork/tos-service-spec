# Native Execution Gate V1

## Purpose

The Native Execution Gate is the provider-side boundary between transport and
paid work. It does not authorize payment. It reconstructs authority from
finalized TOS state and durably admits at most one exact execution intent for
one funded purchase.

A2A, MCP, HTTP credentials, gateways, and provider databases are inputs or
transport. None is canonical authority.

## Boundary

```text
   A2A adapter ──┐
   MCP adapter ──┤   any task-admitting transport
Agent Packet  ──┤   (+ every future adapter)
   receiver      │
                 ▼
 ┌────────────────────────────────────────────────────────┐
 │             Shared Native Execution Gate                │
 │  slot key: (quote_commitment, escrow_address)           │
 │  reconstruct authority from finalized TOS state:        │
 │    - Accepted Quote commitment matches the claim        │
 │    - escrow funded == exact quoted amount               │
 │    - Capability owner / version / manifest, not revoked │
 │    - Registry, escrow, and stablecoin identities        │
 │    - checkpoints monotonic; regression fails closed     │
 │  => admit AT MOST ONE exact execution intent            │
 └────────────────────────────────────────────────────────┘
                 │  admit once
                 ▼
        provider runner ──▶ runner execution journal
        (one admitted execution_id starts exactly once,
         even across retry or crash)
                 │
                 ▼
   artifact + report + canonical Receipt ──▶ settlement
```

Authority is finalized TOS state only. TLS, bearer tokens, rate limits, gateway
routing, and provider databases are transport, never authority. No transport
can reach the runner except through this Gate, so one funded purchase admits at
most one runner execution across A2A, MCP, Agent Packet, and any future adapter.

## Claim

Every transport maps its request to the same claim:

```text
escrow_address
quote_commitment
execution_id
input_digest
source_digest
```

The escrow address is mandatory because a Quote commitment alone is not a
canonical account locator. It is included in each transport's input digest.
Omitting it would force the provider to trust an off-chain index to locate the
purchase.

The durable purchase slot is keyed by the exact pair:

```text
(quote_commitment, escrow_address)
```

The first valid claimant atomically binds that slot to the entire claim. An
identical retry is idempotent. Any different execution ID, input digest, source
digest, Quote, or escrow conflicts before provider work begins. This rule is
shared across A2A, MCP, and every future adapter; transport-specific journals
cannot safely enforce it.

## Finalized verification

Before writing the claim, the Gate independently resolves and verifies:

1. the exact escrow account has authenticated contract code and a nonzero
   finalized checkpoint;
2. its typed state is `funded`, commits the supplied Accepted Quote, names the
   configured provider wallet, and has not reached its refund time;
3. the Accepted Quote decodes canonically and binds the configured network,
   provider Agent, Capability/version, manifest, transport commitment,
   execution-signer authorization, stablecoin identity, and funded amount;
4. the provider Agent is finalized under the configured Native Registry code
   identity and is not tombstoned; and
5. the Capability is finalized under that same Registry identity, remains
   owned by the provider Agent, is not tombstoned, and contains the exact
   unrevoked version and manifest digest.

Missing, malformed, divergent, stale, or unavailable resolution fails closed.
An Agent revocation, Capability transfer/revocation, escrow settlement, or
refund-window transition prevents a new claim.

## Durable record

The claim and its complete outbound intent are written as one owner-private,
atomically published record under an exclusive directory lock. There is no
separate slot record and intent record, so a crash cannot leave a slot-only
state. The record contains the chain code identities, transaction hashes, and
finalized checkpoints for escrow, Agent, and Capability.

On an identical retry, all three checkpoints must be monotonic. Higher
finalized observations atomically replace the record and advance its durable
high-water marks. A regression or change in commercial authority fails closed.
The directory and files must remain owner-private; malformed, linked,
wrong-owner, oversized, or trailing-data records are rejected.

This Gate is separate from the runner's execution journal. The Gate prevents
one purchase from authorizing multiple intents or transports. The runner
prevents one admitted execution ID from starting twice after retry or crash.
Both boundaries are required.

## Adapter and server boundary

Every transport that can admit a purchase-bound task to the runner — the A2A
adapter, the MCP adapter, and the Agent Packet receiver — must use this shared
Gate before invoking the runner. The A2A and MCP official SDK server bindings
expose only the frozen synchronous A2A operation and the single purchase-bound
MCP tool; the Agent Packet receiver admits a task only when the packet carries
the matching finalized Accepted Quote commitment and passes the same Gate. No
transport may reach the runner on any other path. TLS, authentication,
rate-limits, listener policy, and public deployment remain operator concerns;
they cannot weaken or replace finalized-state verification.

The production composition constructs both typed resolvers directly from the
same configured strict-majority TOS JSON-RPC endpoint set, frozen Registry BOC
and code hash, escrow code hash, and separate durable checkpoint paths. It does
not route Native authority through an A2A/MCP gateway or require a private RPC
translation layer.

## Acceptance

Unit and race tests must cover canonical Accepted Quote decode, exact escrow
and Registry identities, Agent tombstone, Capability ownership/version/revoke,
expired escrow, identical retry, concurrent conflicting claims across every
admitting transport (A2A, MCP, and Agent Packet),
checkpoint advancement, checkpoint regression, malformed durable records, and
restart recovery. A public interoperability session must additionally use
fresh buyer/provider identities and independently operated finalized
endpoints.
