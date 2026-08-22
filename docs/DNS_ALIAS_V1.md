# TOS DNS Alias Boundary V1

**Status:** normative `tos_service_v1` read interface

**Authority:** [TIP-1](https://github.com/tosnetwork/TIP/blob/main/TIPS/tip-1.md)
defines `.tos` DNS bytes, contracts, auctions, lifecycle, categories, and
deployment governance. This document only defines how TOS Service Protocol
consumes three of those categories.

## Purpose

TOS DNS lets a person enter a readable name where an Agent or Capability ID is
otherwise required. It does not add a second identity registry. Finalized typed
Native state remains the sole authority for controllers, ownership, versions,
revocation, Quotes, payment, execution, and Messaging delegation.

The V1 API supports only:

| Alias kind | TIP-1 category | Required DNS record | Verified Native target |
|---|---|---|---|
| `AGENT` | `agent` | `dns_smc_address` | Agent |
| `CAPABILITY` | `capability` | `dns_smc_address` | Capability |
| `MESSENGER` | `messenger` | `dns_smc_address` | Agent |

Wallet, Site, storage, and text resolution belongs to their owning clients and
is not widened into the Native service API.

## Resolution algorithm

A conforming implementation MUST:

1. reject an unspecified or unsupported kind and reject a non-canonical name;
2. read ConfigParam 4 and all resolver states from one quorum-finalized
   checkpoint;
3. use the exact TIP-1 encoding and frozen category hash;
4. contact at most eight resolvers, rejecting a repeated address before contact;
5. require the category's exact record constructor and reject trailing data;
6. retain the Root, Collection, Domain Item, and delegated resolver path;
7. prove that the third path element is the deterministic Domain Item for the
   second-level label and belongs to the `.tos` Collection;
8. reject any nonzero auction end, missing renewal clock, or time later than the
   366-day renewal deadline;
9. load the resolved account at the same checkpoint, check the accepted Registry
   code hash and typed object kind, recover its object ID, and re-derive its
   deterministic address from the network and object ID;
10. reject tombstoned Agents and Capabilities, and for a Capability reject a
    tombstoned owner Agent when the caller intends to use it; and
11. return `QUORUM_AGREED`, never `proof`, with the complete checkpoint,
    lifecycle, resolver path, raw account, object ID, and typed Native state.

For `MESSENGER`, success yields an Agent. The caller must then perform the
separate finalized delegation, DHT locator, Contact Descriptor, endpoint-key,
expiry, and replay checks defined by the Messenger protocol. DNS MUST NOT carry
or authorize a private endpoint, prekey set, bearer capability, or transport
session.

## Atomicity and finality

One logical result MUST come from one immutable checkpoint snapshot. An
implementation MUST NOT combine a DNS record read at one checkpoint with
lifecycle or Native state from another. Endpoint agreement below the configured
strict majority, rollback behind the durable checkpoint fence, a same-height
hash conflict, or a changed checkpoint during composition fails closed.

A cache key includes network, canonical name, alias kind, and full checkpoint
identity. Positive cache lifetime is bounded by the lesser of local TTL and
renewal deadline. Record, delegation, lifecycle, auction, or reorg changes
invalidate the affected entry or subtree. Until an implementation retains
authenticated subtree provenance, any checkpoint change MUST clear its DNS
alias cache. An older in-flight result MUST NOT repopulate it.

## Bounds

- `name` and `canonical_name`: 1..126 ASCII bytes;
- `category_hash`: exactly 64 lowercase hexadecimal characters;
- account IDs and checkpoint hashes: exactly 32 bytes;
- `native_object_id`: one canonical `agent_` or `cap_` identifier;
- resolver path: 3..8 entries, with no duplicate address;
- one request resolves exactly one name and one alias kind; and
- implementations apply their existing request deadline and public capacity
  bounds, without an availability fallback.

Unknown protobuf enum values, missing required semantic fields, arithmetic
overflow in the renewal deadline, and malformed endpoint output are errors.

## Use and persistence

Applications MAY display a verified alias beside its raw object ID. Before an
irreversible action they MUST show and bind the raw Agent or Capability ID and
the exact Native state required by that action. They persist the object ID, not
the name, as the session, purchase, contact, authorization, Receipt, or audit
key.

Name transfer, release, re-auction, record mutation, Registry code migration,
object transfer, or revocation never retargets an existing authorization. A
future interaction performs a fresh resolution and is treated as a newly
selected identity.

## API

`tos.service.v1.DNSAliasService/ResolveDNSAlias` is a read-only convenience
method and requires `native:read`. A Gateway cannot use it to create or mutate
DNS or Native authority. `NativeErrorV1` and the retry rules in
`PUBLIC_ERRORS_V1.md` apply. Lifecycle rejection and malformed names are
non-retryable; quorum/finality unavailability permits bounded identical-read
retry; a conflicting checkpoint requires a fresh resolution.

## Conformance

Implementations MUST consume the versioned TIP-1 corpus without altering its
JSON bytes and add adversarial tests for:

- wrong category/record type and plain-SHA256 item index substitution;
- ninth hop, a cycle, partial answer without `dns_next_resolver`, and mixed
  checkpoints;
- active and ended-but-unfinalized auctions, deadline plus one second, and a
  missing renewal clock;
- same-height reorganization and stale in-flight cache insertion;
- wrong workchain, Registry code, object kind, object ID/address derivation,
  owner, version, or tombstone state; and
- name transfer/re-auction proving that stored authority stays bound to the old
  object ID while a fresh lookup may select a different one.

The corpus digest, TIP commit, resolver implementation commit, accepted
Registry release hashes, and test result MUST be recorded for release. Local
tests do not establish public-network or independent-operator acceptance.
