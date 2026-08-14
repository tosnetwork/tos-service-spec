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
The payable Capability `1.2.0` Quote and exact typed Escrow StateInit are
recorded in `initial-public-testnet-paid-escrow-v1-2-2026-08-14.json`. Earlier
escrow records are immutable historical rehearsals: the original used the
placeholder manifest, while `initial-public-testnet-escrow-v1-2-2026-08-14.json`
bound a buyer address that did not own the deployed tUSDT balance and was
therefore superseded before funding.

The completed same-host paid software-work rehearsal is recorded in
`initial-public-testnet-paid-software-work-2026-08-14.json`. It binds the
funding, pinned execution, canonical Receipt, release transaction, provider
wallet credit, immutable artifact and report, and three-endpoint finalized
state reconstruction. The referenced files in `artifacts/` are named by their
SHA-256 digests and must be rehashed before use. This is complete local Gate D
evidence, but it is not the external commercial acceptance required by the
Roadmap.
