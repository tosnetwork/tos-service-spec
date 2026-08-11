# Verified Quote Commitment V1

## Contract

`atos_verified_quote_commitment_v1` is the immutable authority value required
before an ATOS Quote with `trust_mode=verified` is usable. It contains only
public commercial/trust facts; task input, proposal content, credentials and
bulk artifacts are forbidden.

Required fields are the fields of `QuoteCommitmentInput` in
`proto/atos/tos/v1/trust.proto`: version, network/domain, Quote and requester
identities, provider, exact Capability/version, manifest digest and ownership
reference, concrete mode/profile, subtotal/fees/maximum and asset decimals,
settlement and dispute terms, acceptance/expiry/execution deadlines, the
deterministic ATOS terms digest, underlying service quote reference, and the
current execution-signer authorization identity/reference.

`version` is `atos_verified_quote_commitment_v1`. `domain` is the configured
gateway trust domain, not request input. `network_id` equals the Authority's
configured network. `trust_mode` is `TRUST_MODE_VERIFIED` and `proof_profile`
is `PROOF_PROFILE_TOS_VERIFIED_V1`. All timestamps are UTC Unix milliseconds.
Amounts are canonical non-negative base-10 decimal strings at exactly
`asset_decimals` fractional digits; subtotal and fees use the same asset as
`total_max`, and `subtotal + fees = total_max`.

## Canonical encoding and digest

The canonical bytes are protobuf deterministic serialization of the complete
`QuoteCommitmentInput`, using the field numbers frozen in `trust.proto`.
Unknown fields are rejected before canonicalization. The semantic commitment
digest is:

```text
SHA-256("ATOS-TOS-VERIFIED-QUOTE-COMMITMENT-V1" || 0x00 || canonical_bytes)
```

and is rendered as lowercase `sha256:<64 hex>`. Transport `RequestContext`,
commit time, authority reference and finality metadata are excluded. Schema
changes require a new `version`, domain separator and test vectors.

### Test vector 1

The complete literal fixture is `verifiedQuoteFixture` in
`tos-protocol/pkg/atosrpc/verified_quote_test.go`. Its deterministic protobuf
bytes, in lowercase hex, are:

```text
0a0771756f74652d3112137072696e636970616c2d7265717565737465721a0a70726f76696465722d3122056361702d312a05312e302e3030023802420b0a04312e303512035553444a2a0a06736861323536122051d2361f4faea3bc8f9facdbc7d99abb555596a2e51f7b25fd3b41c93587e61658c08beb85ff336203746f736a03544f537a2161746f735f76657269666965645f71756f74655f636f6d6d69746d656e745f7631820108746f732d746573748a010761746f732e696d92010f6167656e742d7265717565737465729a012a0a06736861323536122005b3abf2579a5eb66403cd78be557fd860633a1fe2103c7642030defe32c657fa20181010a08746f732d746573741271746f733a746573743a6361706162696c6974792d6f776e6572736869703a6361702d3140312e302e303a7368613235363a353037373836303163306634646232663734393839623764336337633435306366613131396635373537303739366263363164613064366465663765373737301801202aaa010b0a04312e30301203555344b2010b0a04302e30351203555344b80102c001c08beb85ff33c80180db8f86ff33d20106617574682d31da01780a08746f732d746573741268746f733a746573743a657865637574696f6e2d7369676e65723a617574682d313a7368613235363a383133383336373264646138653635633663643232663865366663336263383564353130343632376333323637366438303466646461323065396434333735361801202a
```

The semantic digest is
`sha256:fe88505b6e6404e97b02973e189ae008e896a46449806706ec2259f621998043`;
the protocol test recomputes and asserts it.

## Authority validation

The server derives or freshly verifies every authority-controlled fact. It
rejects unbound/revoked requester or provider identity; non-current or
mismatched ownership/manifest/version; missing, expired, revoked or mismatched
signer authorization; cross-network/domain input; non-Verified mode/profile;
expired acceptance/expiry/execution windows; invalid money; and unavailable,
non-final, reorganized or inconsistent authority results. Supplied ownership
and signer references are equality assertions and cannot select identities.

## Idempotency and recovery

`context.idempotency_key` equals `quote_id`. Exact replay returns the original
value, digest, reference, commit time and finality. The same Quote/key with
different canonical bytes is `IDEMPOTENCY_CONFLICT`/`QUOTE_MISMATCH`.

ATOS durably records intent before the call. After every ambiguous outcome it
calls `GetQuoteCommitment` first. A found exact finalized value completes the
local projection; a found mismatch is terminal conflict; only a not-found
result permits replaying the same mutation. Concurrent replicas therefore
converge on one canonical Quote commitment.

No failed or uncertain Verified operation may create or expose a Managed
Quote under the same identity. Acceptance, escrow and execution re-check the
stored projection against the immutable Quote and refuse absent/mismatched
commitments.
