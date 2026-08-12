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
`total_max`. TaskEscrow V1 requires `fees = 0` and
`subtotal = total_max`; a later non-zero fee requires a separately frozen
contract version with an independently observed gateway payout.

## Canonical encoding and digest

The canonical value is an explicit field-by-field data model owned by
`tos-protocol/pkg/quotecommitment`, encoded as RFC 8949 Core Deterministic
CBOR by `tos-protocol/pkg/codec`. It is independent of protobuf field numbers
and serialization. `canonicalization` is
`rfc8949_core_deterministic_cbor`; protobuf unknown fields are rejected
recursively before conversion. The semantic digest is:

```text
SHA-256("TOS-PROTOCOL-CBOR" || 0x00 || uint16_be(len(domain)) || domain || canonical_bytes)
domain = "tos.atos.verified-quote-commitment.v1"
```

and is rendered as lowercase `sha256:<64 hex>`. Transport `RequestContext`,
commit time, authority reference and finality metadata are excluded. Schema
changes require a new `version`, domain separator and test vectors.

### Test vector 1

The complete literal fixture is `verifiedQuoteFixture` in
`tos-protocol/pkg/atosrpc/verified_quote_test.go`. Its asserted semantic
digest is:

`sha256:a726197baa2d392aa4dfaf67a81ce89c6617177d607a14104f6d5bdb1a1ae159`;
the protocol test recomputes and asserts it.

## Authority validation

The server derives or freshly verifies every authority-controlled fact. It
rejects unbound/revoked requester or provider identity; non-current or
mismatched ownership/manifest/version; missing, expired, revoked or mismatched
signer authorization; cross-network/domain input; non-Verified mode/profile;
expired acceptance/expiry/execution windows; invalid money; and unavailable,
non-final, reorganized or inconsistent authority results. Supplied ownership
and signer references are equality assertions and cannot select identities.
For Verified, `settlement_backend=tos`, `settlement_asset=TOS`, a valid
`dispute_policy_digest`, and a non-empty `underlying_service_quote_ref` are
mandatory commercial terms, not optional transport defaults.

## Idempotency and recovery

`context.idempotency_key` equals `quote_id`. Exact replay returns the original
value, digest, reference, commit time and finality. The same Quote/key with
different canonical bytes is `IDEMPOTENCY_CONFLICT`/`QUOTE_MISMATCH`.

Before the authority call, ATOS durably binds the authenticated
`(principal_id, caller_idempotency_key)` to one generated Quote ID, complete
immutable snapshot and request hash. Ambiguous reservations are retained.
The operation advances through `intent_persisted`/`reconciling`, then
`authority_committed`, and becomes `completed` only after both the public
Quote projection and caller idempotency result are durable. Terminal state is
monotonic; a stale replica cannot regress `completed` to `reconciling`.
Retries and a stale-operation reconciler load that snapshot (including on a
different ATOS replica), call `GetQuoteCommitment` first, and resume the exact
Quote ID. A found exact finalized value completes the local projection; a
found mismatch is terminal conflict; only authoritative not-found permits
replaying the same mutation. Concurrent replicas therefore converge on one
canonical Quote commitment.

For Verified lookup, `expected_quote` and, when known,
`expected_commitment_ref` are sent so any `tos-protocol` replica can recompute
the digest and freshly resolve the exact value against the live authority by
`(kind, quote_id, digest)`. A missing reference is the normal lost-response
case and MUST trigger tuple lookup, not a local-cache not-found result.
Local bbolt state is never sufficient evidence of existence or finality.

No failed or uncertain Verified operation may create or expose a Managed
Quote under the same identity. Acceptance, escrow and execution re-check the
stored projection against the immutable Quote and refuse absent/mismatched
commitments.
