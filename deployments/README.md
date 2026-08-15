# Native Registry Deployment Records

This directory is reserved for immutable public-network deployment evidence.
Copy `public-testnet.template.json`, replace every `REQUIRED` value with
verified chain data, and rename it to the network and deployment date. An
initial profile may use same-host endpoints only when the record declares that
operator independence and public Internet reachability are false. A mature
profile requires independently operated HTTPS endpoints. A template is never
evidence and must not be marked accepted.

Before publication:

1. reproduce the release BOC and verify every frozen vector;
2. obtain the exact network genesis hashes from endpoint quorum;
3. deploy with a funded testnet wallet using semantic confirmation;
4. resolve the first Agent account from quorum after finality; and
5. attach transaction, state, lifecycle, independent resolver, and audit
   evidence required by `docs/NATIVE_REGISTRY_PUBLIC_TESTNET_GATE.md`.

Test-only asset and lifecycle records may also live here when they bind the
exact network, contracts, code hashes, supply, holder state, transactions,
endpoint quorum, manifests, artifacts, and receipts. They must state explicitly
that they are test infrastructure and make no production reserve, issuer, or
operator-independence claim.

The directory currently contains no accepted `tos_service_v1` deployment.
Evidence produced under the pre-release protocol domain is preserved unchanged
under `archive/pre-tos-service-v1/` for audit history. Because protocol-domain
strings participate in cryptographic commitments, those files cannot satisfy a
current acceptance gate and must never be relabeled as current evidence.

For a post-acceptance Gateway handoff, retain the complete Quote package and
the output of `native-receipt-release`, then assemble the portable bundle with
`tos-service-protocol/cmd/native-safe-handoff-pack`. Use
`safe-handoff.template.json` only as a field guide: it is not evidence. Verify
the resulting bundle with `native-safe-handoff-check` against at least three
validator endpoints and an absolute durable checkpoint path. The checker must
be run while the original Gateway is unavailable; its JSON output is the
machine-readable handoff evidence attached to the independent operator record.

Gate G evidence must use `production-readiness-evidence.template.json` as its
starting shape. A template is never an acceptance record; it must bind exact
release commits, contract hashes, endpoint diversity, drills, reconciliation,
and operator signatures.
