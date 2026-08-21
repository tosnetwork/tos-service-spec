# Mobile TOS Service Client V1 (iOS and Android)

> **Archived reference; outside the active product roadmap.** Desktop/Web,
> Android, and iOS clients are not deliverables or acceptance dependencies of
> the OpenFox-only Agent-native Messenger. Nothing in this document contributes
> to that roadmap or its completion percentage.

The iOS and Android applications are owner-controlled Native clients. They
provide discovery, approval, custody, task status, and settlement receipts;
they are not Gateway authorities and do not maintain a parallel balance ledger.

## Shared lifecycle

The mobile app displays a finalized Agent/Capability result, the complete Quote
terms, the exact Accepted Quote commitment, escrow address, asset identity,
amount, expiry, and fee payer before requesting approval. The app then signs
through the platform custody boundary, submits the exact bytes, and tracks only
finalized checkpoints and typed state.

After funding, the app may launch A2A, MCP, or Agent Packet transport. Every
transport passes the shared Native execution Gate, so a funded purchase executes
at most once regardless of transport. Payloads and artifacts remain off-chain.
The app verifies the Receipt commitment and settlement before showing “paid”; a
Gateway response or HTTP success is never payment evidence.

## iOS design

- Swift Native client module owns network tuple, finalized resolver, Quote and
  escrow models, and strict JSON/protobuf decoding.
- Secure Enclave/Keychain or the reviewed `tosctl` handoff owns private keys;
  application views never receive raw seeds.
- A background task resumes the purchase journal and resolves ambiguous funding
  or release after process death.
- Universal links or QR codes may carry signed Contact Cards; network tuple and
  expiry are checked before any endpoint connection.
- The confirmation screen shows Capability version, manifest digest, stablecoin
  master/wallet code hashes, amount, escrow address, and exact transaction body.

## Android design

- Kotlin Native client module mirrors the same typed lifecycle and JSON/protobuf
  strictness; it must not fork commercial semantics.
- Android Keystore/StrongBox or the reviewed `tosctl` handoff owns private keys.
- WorkManager persists bounded journal recovery and finality polling with an
  explicit network/fee budget.
- App links or QR codes carry the same signed Contact Card wire format as iOS.
- Approval UI displays the same canonical fields and rejects asset ticker-only
  or Gateway-only payment claims.

## Security and acceptance

Both platforms must enforce TLS outside loopback, bounded responses, endpoint
origin policy, redirect rejection, strict-majority finality, and secure local
journal storage. They must support refund and recovery views without inventing
new contract transitions.

The first mobile milestone is read-only discovery plus Quote review. The paid
milestone is a fresh buyer session that funds escrow, receives a Receipt, and
reconstructs settlement from an independent resolver. iOS and Android share
vectors and evidence; platform UI differences cannot alter protocol facts.
