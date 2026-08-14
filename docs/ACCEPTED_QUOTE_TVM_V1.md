# Accepted Quote TVM Cell V1

## Canonical boundary

A Quote Proposal is gateway-local and non-canonical. The client converts one
proposal into the cell below. Its TVM cell hash is the Accepted Quote
commitment. `proposal_id` is deliberately excluded, so gateways cannot become
part of canonical commercial identity.

The first finalized transaction carrying this exact cell makes the terms an
Accepted Quote. For the first commercial lifecycle, the transaction is the
deployment of the stablecoin escrow whose StateInit embeds this cell. The
escrow is a real custody and settlement state machine, not an Action Anchor.
Its exact StateInit linkage and asynchronous settlement requirements are
defined in [`STABLECOIN_ESCROW_TVM_V1.md`](STABLECOIN_ESCROW_TVM_V1.md).

## Cell layout

```text
accepted_quote$_ magic:uint32=0x4e415131 schema:uint16=1
  ^network_domain ^identity ^economic ^authority = AcceptedQuoteV1;

network_domain$_ genesis_root:uint256 genesis_file:uint256
  network_id_sha256:uint256 = NetworkDomainV1;

identity$_ capability_id:uint256 provider_agent_id:uint256
  ^version = QuoteIdentityV1;

version$_ capability_version_sha256:uint256 manifest_digest:uint256
  transport_binding_digest:uint256 expires_at:uint64
  ^capability_version_snake = QuoteVersionV1;

economic$_ escrow_terms_digest:uint256 dispute_policy_digest:uint256
  ^asset ^maximum_atomic_amount_snake = QuoteEconomicV1;

asset$_ workchain:int32 master_account_id:uint256
  master_code_hash:uint256 wallet_code_hash:uint256 decimals:uint8
  = TOSAssetIdentityV1;

authority$_ execution_signer_authorization:uint256 = QuoteAuthorityV1;
```

Strings are printable ASCII, minimally encoded as byte-aligned TVM snakes.
Atomic amounts use `0 | [1-9][0-9]*`, with no sign, fraction, exponent,
whitespace, or leading zero. V1 accepts only wc=0 stablecoins, 1–18 decimals,
and non-zero account and code hashes on the surrounding TOS network domain.
A ticker such as `USDT` is never an asset identity.

The manifest digest is the digest of the canonical software-work manifest.
The exact Capability version in finalized Registry state must bind the same
digest and must be non-revoked. The provider must be the finalized Capability
owner when the Quote is accepted.

## Vector and transaction rule

[`accepted-quote-v1.json`](../test-vectors/accepted-quote-v1.json) freezes the
cell and commitment using the test-only tUSDT contract identity, the finalized
software-work Capability ID, concrete escrow terms, and the test execution
signer's Ed25519 public key. Production and independent Go encoders reproduce
it without sharing Quote encoding code and verify the typed preimage hashes.

The vector proves encoding only. Before escrow deployment, a resolver must also
verify the network genesis, Capability version and owner, stablecoin master and
wallet code, decimals, expiry, and exact escrow code identity from finalized
TOS state. Deployment fails closed if any authoritative value is absent or
ambiguous.
