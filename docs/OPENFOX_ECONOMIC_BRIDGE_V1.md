# OpenFox Economic Bridge V1

The cross-repository implementation sequence for autonomous discovery,
first-contact Messenger initiation and policy-gated execution is defined in
[`OPENFOX_AUTONOMOUS_MESSENGER_ECONOMY_PLAN.md`](OPENFOX_AUTONOMOUS_MESSENGER_ECONOMY_PLAN.md).
This document remains the authority boundary for the commercial lifecycle.

General economic discovery, AI-local interpretation, authenticated
conversation, Agreement, and settlement-mode selection are defined in
[`AGENT_INTENT_EXCHANGE_V1.md`](AGENT_INTENT_EXCHANGE_V1.md). This bridge is
invoked only when a negotiated Agreement selects a supported Native commercial
profile; it is not the required path for every Intent.

The optional fixed-price escrowed-work profile is split deliberately: signed
publication, permissionless propagation, discovery, and Provider Offers are
defined in
[`AGENT_PAID_DEMAND_DISCOVERY_V1.md`](AGENT_PAID_DEMAND_DISCOVERY_V1.md), while
[`PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md`](PAID_DEMAND_ACCEPTED_QUOTE_BINDING_V1.md)
defines the minimal versioned adapter from one exact Offer into this existing
Quote, escrow, execution, Receipt, and settlement rail. Neither document creates
a second commercial lifecycle.

Trusted person-to-person Agent Gifts are a separate non-purchase settlement
choice under the general Intent architecture and are defined in
[`OPENFOX_AGENT_GIFTS_V1.md`](OPENFOX_AGENT_GIFTS_V1.md). A Gift MUST NOT reuse
this bridge's Quote, Capability, software-work Receipt, or provider-settlement
semantics merely because both profiles move value.

The Direct Signed Gift profile creates no Receiver Profile, Gift delegation,
receive ticket, per-Gift Vault, or escrow. V1 supports native TOS only. Inside
an existing authenticated direct E2EE conversation, the sender asks the
recipient for one TOS address. Sender custody then constructs and signs one
exact time-limited standard-wallet BOC transferring native TOS to that returned
address. The recipient may submit those unchanged bytes but cannot redirect the
signed transfer.

Funds remain spendable by the sender until the BOC executes, so the UI must not
call an unbroadcast Gift funded, locked, or guaranteed. If it expires, no refund
is needed because no transfer occurred. If it succeeds, payment is recognized
only from finalized exact destination credit. Before broadcast, the address
exchange, BOC, and Agent relationship remain inside E2EE; after execution,
transparent TOS state still exposes wallet, amount, and timing information.

Native TOS support in the Gift profile is strictly non-purchase semantics. It
does not make native TOS a provider-service price or settlement asset under the
software-work commercial profile, where the controlling Quote and settlement
documents continue to apply.

None of the Gift privacy, relay, or asset mechanics creates another payment
authority or permits a model to handle custody secrets.

OpenFox is the autonomous application runtime for a TOS Agent. This bridge
connects its agent loop to the existing Native commercial lifecycle; it does
not create a second marketplace, ledger, trust mode, or settlement protocol.

## Responsibilities

OpenFox owns local intent, task scheduling, execution, artifacts, and owner
policy. `tos-service-protocol`/`tos-service-gateway` owns finalized-state
resolution, Quote preimage validation, relay, and escrow construction. TOS
contracts own canonical Agent, Capability, Accepted Quote, escrow, Receipt, and
settlement state.

OpenFox must never infer ownership or payment from a Gateway response. Every
candidate is re-resolved from finalized TOS state before spending.

## Buyer flow

1. Resolve a Capability through Gateway search or a signed Contact Card.
2. Verify Agent, Capability version, manifest digest, network tuple, and code
   hash from finalized state.
3. Request and validate a complete-preimage Quote Proposal.
4. Apply the owner-signed spending policy: asset, maximum amount, expiry,
   Capability allow-list, daily budget, and confirmation mode.
5. Build the Accepted Quote and deterministic escrow StateInit.
6. Authorize and submit the exact acceptance action through the `tosctl` custody
   boundary, then wait for finalized Quote acceptance. For schema-1 Capability-
   first escrow this is finalized deployment; a paid-demand schema successor
   uses its bound-buyer-wallet `pending_acceptance -> awaiting_funding`
   transition.
7. Send the exact stablecoin funding through the bound buyer wallet, enter
   funding resolution, and wait for the finalized exact transfer notification.
8. Submit the task over A2A, MCP, or Agent Packet only after finalized funding.
9. Verify the Receipt and settlement from finalized escrow and wallet state.

The OpenFox loop may sleep and resume. Journal phases are intent, prepared,
acceptance resolving, accepted-awaiting-funding, funding resolving, funded,
execution, Receipt, release, and resolved. Ambiguous acceptance, funding, or
release always resolves finalized state before retry. Every task transport
passes the shared Native execution Gate, so one funded purchase admits at most
one runner execution across A2A, MCP, and Agent Packet.

## Provider flow

1. Publish the Capability manifest and owner-controlled Quote policy.
2. Advertise a signed Contact Card or expose a Gateway-derived listing.
3. Accept only tasks bound to a finalized Accepted Quote and funded escrow.
4. Execute inside the bounded provider executor and content-addressed store.
5. Build the canonical Receipt, sign with the execution signer, and submit the
   release bytes.
6. Reconcile provider stablecoin credit from finalized wallet state.

OpenFox provider code cannot change the manifest, price, signer, or Receipt
after acceptance. A failed execution produces no successful Receipt; timeout
refund follows the escrow state machine.

## Required components

- `NativeResolver`: finalized Agent/Capability/escrow/wallet reads;
- `QuoteClient`: complete-preimage Quote exchange and Accepted Quote builder;
- `PurchaseJournal`: owner-private atomic journal with slot and budget claims;
- `CustodySigner`: `tosctl` or hardware-backed signing boundary;
- `TaskTransport`: A2A, MCP, or Agent Packet client;
- `ExecutionAdapter`: manifest-bound local executor;
- `ReceiptVerifier`: canonical Receipt and settlement-intent verifier; and
- `PolicyEngine`: explicit allow-list, amount, expiry, and operator approval.

The bridge is not complete merely because these interfaces compile. Acceptance
requires one OpenFox buyer and one OpenFox provider to complete a fresh funded
session and an independent resolver to reconstruct it.
