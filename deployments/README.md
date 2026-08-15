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

A second fresh same-host rehearsal using the custody-safe two-stage Receipt
signing flow is recorded in
`initial-public-testnet-gate-d-local-preflight-2026-08-14.json`, with its exact
Quote and escrow deployment in the adjacent `-quote-` and `-escrow-` records.
It proves the provider-wallet balance delta from a finalized funded checkpoint
rather than assuming an initially empty provider wallet. The new immutable
artifact and report are stored in `artifacts/` under their SHA-256 names. This
record is explicitly a local preflight and does not satisfy external operator
independence.

The completed local Gate E engineering acceptance is recorded in
`local-gate-e-live-chain-adapter-acceptance-2026-08-15.json`. It binds a fresh
Provider SDK Capability and Buyer SDK funded purchase to a live 2-of-3 chain
execution Gate, successful A2A/TLS execution, rejected cross-transport MCP
replay, exactly one runner invocation, and settlement of the exact execution
outcome by canonical Receipt. It proves the integrated implementation, not the
independent provider/buyer operator session required to accept Gate E.

The local Gate F search/Quote engineering record is
`local-gate-f-federated-quote-conformance-2026-08-15.json`. Two processes with
separate catalogs and credentials constructed complete-preimage proposals from
the same finalized provider Capability; the buyer continued through Gateway B
after Gateway A stopped. This is failover implementation evidence only and
does not claim independent Gateway operators or recurring market demand.

The 2026-08-15 safe-handoff rehearsal is recorded in
`local-gate-f-safe-handoff-conformance-2026-08-15.json`. It ran two isolated
Gateway processes against the three-node validator quorum, stopped Gateway A,
and verified that Gateway B continued with a rebuilt Quote commitment. It is
explicitly local technical evidence and does not satisfy the independent
operator, three-provider, ten-Capability, or recurring-buyer requirements.

For a post-acceptance Gateway handoff, retain the complete Quote package and
the output of `native-receipt-release`, then assemble the portable bundle with
`tos-protocol/cmd/native-safe-handoff-pack`. Use
`safe-handoff.template.json` only as a field guide: it is not evidence. Verify
the resulting bundle with `native-safe-handoff-check` against at least three
validator endpoints and an absolute durable checkpoint path. The checker must
be run while the original Gateway is unavailable; its JSON output is the
machine-readable handoff evidence attached to the independent operator record.

Gate G evidence must use `production-readiness-evidence.template.json` as its
starting shape. A template is never an acceptance record; it must bind exact
release commits, contract hashes, endpoint diversity, drills, reconciliation,
and operator signatures.
