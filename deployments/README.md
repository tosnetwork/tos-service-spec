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

Test-only asset deployment records may also live here when they bind the exact
network, master contract, code hashes, supply, holder state, transactions, and
endpoint quorum. They must state explicitly that they are test infrastructure
and make no claim on production reserves or issuer independence. The initial
`tUSDT` record is `initial-public-testnet-tusdt-2026-08-14.json`.

The executable software-work manifest and its non-revoked Native Capability
`1.2.0` binding are recorded in
`initial-public-testnet-software-work-capability-v1-2-2026-08-14.json`. The
earlier `initial-public-testnet-software-work-capability-2026-08-14.json`
record is retained as historical `1.1.0` evidence; its placeholder schema and
toolchain digests are not valid execution inputs.
The canonical Accepted Quote event and exact typed Escrow StateInit deployment
are recorded in `initial-public-testnet-escrow-2026-08-14.json`.
