# Gateway Federation V1

## Scope

V1 federation is client-side composition of independently operated Gateway
discovery APIs. It is not a Gateway registry, shared market database, consensus
system, or new source of protocol authority. Finalized TOS state remains the
sole authority for Agent ownership, Capability versions, Accepted Quotes,
escrow, Receipts, and settlement.

## Federated Capability search

A buyer may issue the same bounded `SearchCapabilities` request to two or more
Gateway origins that passed `GATEWAY_DISCOVERY_V1.md`. Each response retains
its source Gateway identity. The client must not average match scores, treat
the union as complete, or infer consensus because several Gateways return the
same candidate.

Before exposing a candidate, the federation client checks that:

- the Native network tuple and Registry code hash match local policy;
- the response contains a non-tombstoned finalized Capability;
- its chain reference, state hash, and transaction hash have valid shapes;
- the selected version exists, is active, and commits to the returned manifest
  digest; and
- per-Gateway and aggregate result bounds are respected.

A malformed response invalidates that Gateway's entire page. An unavailable
Gateway is isolated when another Gateway returns a valid page. If every
Gateway fails, search fails closed. Results are sorted deterministically only
for client presentation; the order has no protocol meaning.

Before purchase, the buyer independently resolves the selected Capability
from finalized TOS state. Search responses never satisfy that check.

## Manifest failover

Manifest retrieval may try compatible Gateways in local policy order. A byte
sequence is usable only when it is canonical manifest CBOR and its SHA-256
digest equals the requested digest committed by the finalized Capability or
Accepted Quote. A missing or corrupted response is isolated to its source.

Clients retain exact canonical manifest bytes after Quote acceptance. A
Gateway outage must not force the buyer to accept replacement content.

## Quote Proposal boundary

Quote Proposals remain non-canonical transport objects. Federation may compare
proposals obtained from different providers or Gateways, but no proposal count,
ranking, signature, or Gateway acknowledgement makes terms canonical. The
buyer validates every preimage and creates the deterministic Accepted Quote;
only its finalized TOS escrow commitment establishes accepted terms.

`RequestQuoteProposal` carries the complete preimages needed to reproduce every
proposal digest. `tos-protocol` validates those preimages and `atos` exposes a
provider-source boundary that fails closed when no source is configured. The
RPC does not introduce a Gateway order book, Gateway-controlled acceptance
record, or server-side buyer wallet. A production provider quote source and
multi-Gateway conformance deployment remain Gate F work.

## Safe handoffs

Before acceptance, a buyer may switch Gateways and request a different Quote.
After acceptance, failover uses only the exact manifest, Accepted Quote and
escrow preimages, finalized chain references, owner-held journals, and
content-addressed artifacts. A replacement Gateway acknowledgement is never a
prerequisite for execution, Receipt checking, refund, or settlement.

`SAFE_HANDOFF_V1.md` defines the exact portable bundle, finalized-state checks,
funded/release-pending decisions, and negative conformance matrix. Proposal
expiry is enforced while selecting a Quote; after acceptance, the finalized
escrow anchors immutable reconstruction and no current Gateway clock or
acknowledgement participates.
