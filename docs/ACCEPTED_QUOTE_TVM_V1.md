# Accepted Quote TVM Cell V1

## Canonical boundary

A Quote Proposal is gateway-local and non-canonical. The client converts one
proposal into the cell below. Its TVM cell hash is the Accepted Quote
commitment. `proposal_id` is deliberately excluded, so gateways cannot become
part of canonical commercial identity.

The cell settles on the Service Actor rail
([`SERVICE_ACTOR_TVM_V1.md`](SERVICE_ACTOR_TVM_V1.md); binding rules in
[`SERVICE_ACTOR_SETTLEMENT_DESIGN.md`](SERVICE_ACTOR_SETTLEMENT_DESIGN.md)
sections 2-3). It is not itself stored on chain. The buyer commits to it through
the `request_hash` of a `call` (section "Request commitment"), and the
finalized successful `call` transaction is the acceptance event. Schema 1 is
this layout; the earlier stablecoin-escrow layout of schema 1 and the Paid
Demand schema 2 are retired and not accepted by any conforming tool.

## Cell layout

```text
accepted_quote$_ magic:uint32=0x4e415131 schema:uint16=1
  ^network_domain ^identity ^rail ^authority = AcceptedQuoteV1;

network_domain$_ genesis_root:uint256 genesis_file:uint256
  network_id_sha256:uint256 = NetworkDomainV1;

identity$_ capability_id:uint256 provider_agent_id:uint256
  ^version = QuoteIdentityV1;

version$_ capability_version_sha256:uint256 manifest_digest:uint256
  transport_binding_digest:uint256 expires_at:uint64
  ^capability_version_snake = QuoteVersionV1;

rail$_ actor:MsgAddressInt actor_code_hash:uint256 policy_version:uint32
  ^rail_terms = QuoteRailV1;                                -- 555 bits

rail_terms$_ terms_hash:uint256 price:Coins storage_fee:Coins
  = QuoteRailTermsV1;                                       -- <= 504 bits

authority$_ attestor_key_id:uint256 = QuoteAuthorityV1;

transport_binding$_ magic:uint32=0x4e544231 schema:uint16=1
  security_mode:uint8 max_request_bytes:uint32
  ^base_url_snake = NativeTransportBindingV1;
```

The rail is split across two cells because one cell would need 1,059 bits; the
Quote keeps the contract's full Coins bound instead of a narrower one
(design section 3.1).

- `actor` is a canonical `addr_std` on workchain 0 with no anycast. It equals
  manifest key 21 and the destination of the `call`.
- `actor_code_hash` equals manifest key 21, the account's code hash and a
  published Service Actor release (pending: no release is published yet, so no
  Quote can currently be verified).
- `policy_version`, `terms_hash`, `price` and `storage_fee` equal the decoded
  current actor policy at quote time; `terms_hash` is computed as
  `SERVICE_ACTOR_TVM_V1.md` section 5 defines it. `price` is the exact
  `price_per_call` in nanoTOS, below `2^120` and non-zero; `storage_fee` is
  non-refundable and the Quote must disclose it as such (D4).
- `attestor_key_id` is the ML-DSA-44 key id that manifest key 21 names and that
  `terms_hash` covers; its text form is `mldsa44:<64 lowercase hex>`.
- `expires_at` is a buyer-side acceptance deadline only: a buyer refuses to
  `call` at or after it. The contract does not see it; a stale quote fails
  closed through `terms_hash` (D7).
- The asset is native TOS and has no field: this rail settles nothing else (D8).
- The dispute policy is fixed by contract code: an attested response pays,
  otherwise the price returns to the caller (design section 3.3). There is no
  dispute-policy digest.

Strings are printable ASCII, minimally encoded as byte-aligned TVM snakes.

The transport digest is `cell_hash(transport_binding)`. Security mode `0` is
Connect RPC over plaintext HTTP and is permitted only for an explicit loopback
bootstrap endpoint; mode `1` is Connect RPC over HTTPS. The base URL is a
canonical absolute ASCII URL with no credentials, query, fragment, or trailing
slash. It is at most 120 bytes and occupies one canonical cell without
continuation references. `max_request_bytes` is non-zero and at most 16 MiB. The service is fixed
by this schema to `tos.service.v1.NativeService`; it is not supplied by a
gateway. A production Quote must use mode `1`.

The manifest digest is the digest of the canonical software-work manifest.
The exact Capability version in finalized Registry state must bind the same
digest and must be non-revoked when the buyer calls. The provider must be the
finalized Capability owner.

## Request commitment

```text
quote_commitment = cell_hash(accepted_quote)
request_hash     = cell_hash(service_request)
service_request$_ magic:uint32=0x4e535231 schema:uint16=1
  quote_commitment:uint256 execution_id:uint256 input_digest:uint256
  = ServiceRequestV1;
```

`magic` is ASCII `NSR1`. Every field is non-zero. The `call` carries
`request_hash` and `expected_terms_hash = rail_terms.terms_hash`; buyer tooling
always passes the quoted value, never the actor's live terms. A buyer never
reuses a `request_hash`.

## Verification rule

Before building a `call`, the buyer runs admission-time verification, and a
resolver attributes an existing request only after existing-request
verification, both as `SERVICE_ACTOR_SETTLEMENT_DESIGN.md` section 2.4
specifies, from one quorum-finalized checkpoint. Any absent, ambiguous or
mismatched authoritative value is a verification error.

## Vectors

Pending. The frozen [`accepted-quote-v1.json`](../test-vectors/accepted-quote-v1.json)
and `accepted-quote-v1-2.json` encode the retired stablecoin-escrow layout and
are not conformance vectors for this cell. Vectors for this layout,
`ServiceRequestV1` and `terms_hash` must be generated from the changed contract
and reproduced by the production and an independent encoder before this cell
is frozen.
