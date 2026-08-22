# OpenFox Economic Bridge V1

The cross-repository implementation sequence for autonomous discovery,
first-contact Messenger initiation and policy-gated execution is defined in
[`OPENFOX_AUTONOMOUS_MESSENGER_ECONOMY_PLAN.md`](OPENFOX_AUTONOMOUS_MESSENGER_ECONOMY_PLAN.md).
This document remains the authority boundary for the commercial lifecycle.

OpenFox is the autonomous application runtime for a TOS Agent. This bridge
connects its agent loop to the existing Native commercial lifecycle; it does
not create a second marketplace, ledger, trust mode, or settlement protocol.

## Responsibilities

OpenFox owns local intent, task scheduling, execution, artifacts, and owner
policy. `tos-service-protocol`/`tos-service-gateway` owns finalized-state resolution, Quote preimage
validation, relay and escrow construction. TOS contracts own canonical Agent,
Capability, Accepted Quote, escrow, Receipt, and settlement state.

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
6. Sign and fund through the `tosctl` custody boundary; persist the crash-safe
   purchase journal.
7. Submit the task over A2A, MCP, or Agent Packet only after finalized funding.
8. Verify the Receipt and settlement from finalized escrow and wallet state.

The OpenFox loop may sleep and resume. Journal phases are intent, prepared,
funding lease, funded, execution, Receipt, release, and resolved. Ambiguous
funding or release always resolves finalized state before retry. Every task
transport passes the shared Native execution Gate, so one funded purchase
admits at most one runner execution across A2A, MCP, and Agent Packet.

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
