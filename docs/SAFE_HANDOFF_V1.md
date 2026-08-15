# Safe Handoff V1

## Purpose

This profile defines when a buyer may change Gateways without transferring
semantic authority or depending on private Gateway state. Finalized TOS state
remains the sole canonical authority.

## Boundary

Before Quote acceptance, a buyer may abandon any Gateway response and obtain a
new Quote Proposal elsewhere. Every proposal is independently validated with
its complete manifest, escrow-terms, transport, and dispute-policy preimages.
No Gateway acknowledgement survives this boundary.

After acceptance, the buyer must retain a portable purchase bundle containing:

- the complete Quote Proposal package and request identity;
- the execution-signer public key selected by the buyer;
- the deterministic escrow address;
- the locally approved escrow contract code hash;
- the canonical Receipt BOC;
- the settlement query ID and signature; and
- owner-held request, artifact, report, and broadcast journals where relevant.

Proposal expiry controls pre-acceptance selection. It does not make an already
finalized Accepted Quote unverifiable. Post-acceptance recovery validates the
immutable proposal preimages without applying the current Gateway clock, then
requires their reconstructed Accepted Quote to match finalized escrow state.

## Required verification

A post-acceptance handoff implementation must fail closed unless it proves all
of the following without querying the original Gateway:

1. every Quote digest has the exact portable preimage;
2. the execution-signer authorization reconstructs the Accepted Quote;
3. the Accepted Quote cell and commitment match finalized escrow state;
4. the Receipt is canonical and binds the same Quote and provider;
5. the funded stablecoin amount covers the Receipt charge;
6. the settlement intent signature verifies under the signer fixed by escrow;
7. the chain reference names the escrow and a non-zero finalized checkpoint;
8. a funded escrow has no settlement residue; or
9. a release-pending escrow contains the same Receipt, query ID, and amount.

A funded result permits the same signed release body to be submitted through
any compatible relay. A matching release-pending result is idempotent evidence
that rebroadcast is unnecessary. Missing or ambiguous finalized state never
permits a broadcast.

## Non-authority of replacement Gateways

The verification interface has no Gateway identity, session, order record, or
acknowledgement input. A replacement Gateway may transport already signed
bytes, but cannot replace a preimage, modify a Receipt, select another signer,
declare finality, or authorize settlement.

## Conformance

Conformance includes:

- pre-acceptance Quote retrieval from two isolated Gateways and continued use
  after either one stops;
- post-acceptance reconstruction with the original Gateway unavailable;
- both funded and release-pending recovery states;
- rejection of corrupted Quote preimages, Receipt BOCs, signatures, finalized
  Quote commitments, and unavailable finality; and
- verification of an expired but previously accepted proposal against its
  finalized escrow.

`tos-protocol/pkg/safehandoff` is the production verifier for this profile.
Its resolver interface exposes only finalized typed escrow state.

The operator-facing checker is `tos-protocol/cmd/native-safe-handoff-check`.
It accepts one strict `atos.native.safe-handoff.v1` JSON bundle, at least three
validator JSON-RPC endpoints, and a durable checkpoint path. Its evidence
output records zero Gateway inputs, the endpoint quorum, finalized checkpoint,
commitments, and whether the release is ready to broadcast or already pending.
The bundle uses protobuf JSON for `network`, `quote_request`, and
`quote_package`; canonical Receipt bytes are Base64, while the Ed25519 public
key and signature are lowercase hexadecimal.
`deployments/safe-handoff.template.json` is a strict input template. Operators
must replace every `REQUIRED` or placeholder value with bytes retained by the
buyer/provider owner; placeholders are not valid evidence.
