# TOS Service Protocol Implementation Roadmap

This roadmap defines implementation order and acceptance gates. Product
priority is defined by `PRODUCT_STRATEGY.md`. Authority boundaries are defined
by `ARCHITECTURE.md`; Agent and Capability transitions are defined by
`NATIVE_REGISTRY_STATE_MACHINES.md`.

No later gate may weaken an earlier authority or security invariant.

## Status convention

- ✅ Complete: implemented and supported by repository evidence.
- 🟡 Partial: implementation or design exists, but the task or its acceptance
  evidence is incomplete.
- ⬜ Pending: not implemented, or no qualifying evidence was found.

### 2026-08-15 protocol-domain migration

The repository and wire domain were renamed before production launch from the
pre-release names to TOS Service Protocol. The current identifier is
`tos_service_v1`, the protobuf package is `tos.service.v1`, and all current
media types and signature domains use `tos.service.*`.

This is intentionally a breaking reset. Protocol strings participate in
identifiers, signatures, manifest digests, Quote commitments, and execution
claims. Consequently, every deployment record created before this migration is
archived under `deployments/archive/pre-tos-service-v1/` and is historical
evidence only. It cannot satisfy a current Gate C, D, E, or F acceptance item.
No transaction hash, object ID, or settlement record may be relabeled as if it
were produced under `tos_service_v1`.

A gate is complete only when every delivery item and its acceptance condition
are complete. The final 2026-08-14 independent Gate B review evaluated
`tos-service-spec` commit `e72bab245a47b0f87a82977629cc03b1dfc64995`, `tos` commit
`a787cb02dd6bc386be053ab233d0581cc1a14ef3`, and `tos-service-protocol` commit
`7a21c070c1160fc0a4278e1a086c0682eb2d3d31`. It found no P0, P1, or P2,
confirmed the chain-time recovery remediation and crash-safe relay journal, and
independently reproduced the complete Native Registry TVM lifecycle matrix.
Gate C deployment evidence must continue to bind exact reviewed commits and
release hashes.

The initial Gate C deployment record is published by `tos-service-spec` commit
`7a6cc02360e4cc8c2d95f80d433704cd72b0dc32`. Persistent validator JSON-RPC
configuration is in `tos` commit
`145bf7de195ac6105c630510ab51912f4b9e92ca`; the production quorum checker,
live-node transaction response compatibility, and diagnostic-only quorum error
detail are in `tos-service-protocol` commit
`6bb42b8968d4bbc374a89b7b61ea2c0e958d91ca`. These operational additions do
not change the frozen Registry BOC, action encoding, authorization, state
machine, or quorum decision rule reviewed at Gate B.

The pre-escrow Gate D design and test-evidence baseline is `tos-service-spec` commit
`11464a84d0dec985f22636a8a94b3770c0cc2418`, `tos` commit
`dc71dc8712f58e3d11ed973f4980ff6ae71de845`, and `tos-service-protocol` commit
`6bb42b8968d4bbc374a89b7b61ea2c0e958d91ca`. It freezes the first
software-work manifest and Accepted Quote encodings, records the finalized
Capability binding and test-only stablecoin deployment, and provides
`tosctl`-generated Ed25519 test identities. It intentionally makes no escrow,
Quote-acceptance, execution, Receipt, or settlement claim; the implementation
status below supersedes that historical baseline and must be bound to new exact
commit hashes before public deployment.

The shared Gate E execution-admission implementation is `tos-service-protocol` commit
`92d8d1f114f984c5a1348318f7859b564428a3b4` and `tos-ai` commit
`7456cc22c22cc5105c9fe5beac48a3513a91fb4c`. It adds canonical Accepted Quote
decode, finalized escrow/Agent/Capability verification, one atomic durable
purchase-intent record shared by transports, monotonic three-object finality
evidence, and official A2A JSON-RPC and MCP streamable-HTTP bindings. This is
implementation evidence, not the fresh external interoperability evidence
required to accept Gate E.

The production buyer funding boundary is `tos` commit
`d9d725534cb1a9120b1e49854b360c01f043c22a` and `tos-service-protocol` commit
`d1a845eb7808365a413106d075c7c6316be67e27`. The SDK validates one exact
`tosctl`-signed stablecoin funding message before acquiring its one-way
broadcast lease, then submits those same bytes without rebuilding or
re-signing. This closes the implementation item; fresh-buyer acceptance
evidence remains outstanding. The same-host three-validator rehearsal in
`deployments/archive/pre-tos-service-v1/local-gate-e-tosctl-buyer-funding-2026-08-15.json` additionally
proves that a `tosctl`-native V1R3 wc=0 buyer can fund the exact new escrow and
reach three-vote finalized funded state; it is not the complete public buyer
session and does not establish external independence.

Finalized buyer asset resolution is implemented in `tos-service-protocol` commit
`57f6429f2a0dc21b3292de8a27fa5d3a26255dd4`. It derives the exact buyer wallet
from the authenticated stablecoin master's wallet-code preimage and verifies
both accounts, balance, ownership, network genesis, strict-majority finality,
and a durable monotonic checkpoint. The live three-node result is attached to
the local Gate E buyer-funding record.

Direct buyer-side Native resolution and the full live Buyer SDK revalidation
are implemented in `tos-service-protocol` commit
`a18162af3df971af265bf101ae9d40396e3c1370`. The SDK reproduced the finalized
Capability/manifest binding, Quote commitment, deterministic escrow, buyer
stablecoin wallet, and funded amount from the three-node chain at checkpoint
`143512` without a gateway or another broadcast. This is integration and
idempotency evidence; the documented fresh-buyer acceptance session remains
outstanding.

Gateway-local Capability search is defined in `tos-service-spec` commit
`c3ed72086798275021e1a45964f3b7d6d9d3eb5c`, implemented in `tos-service-protocol`
commit `f3223ed7f9ceca54fd03298ce60aabd666b1e76c`, and exposed by `tos-service-gateway` commit
`2981f6484e5310d2176717649cf41c50828c99ab`. Every result freshly resolves finalized Registry state and keeps its
chain-selected version and manifest digest separate from explicitly local
manifest metadata and match score. Pagination is Capability-ID ordered, so no
gateway ranking becomes a cursor or protocol fact.

The public-interface discovery example is implemented by
`tos-service-protocol/cmd/tos-service-discovery` at commit
`96bb82a3670270169650324a1c54397110b17e72`. It publishes, lists, searches,
and retrieves manifests only through authenticated Connect methods, reads its
credential from the environment, has no catalog-directory option, and is
covered by the full race/vet/build suite. No operator database edit or hidden
control service is part of the example.

The shared A2A/MCP public listener boundary is implemented in `tos-ai` commit
`97ef0cb31f598c298923f73b5959016603c54287`. The supported public constructors
require TLS 1.3, a strong constant-time-checked bearer credential, protected
certificate files, bounded request bodies/headers/concurrency/read time, and
default rejection of browser-origin requests. Optional client-CA configuration
enforces mTLS. This closes listener hardening; it is not fresh interoperability
or external operator evidence.

Local cross-transport acceptance is implemented in `tos-ai` commit
`2dcb7d9210f8163224459ee21644a7acc75e6636`. Official A2A JSON-RPC and MCP
streamable-HTTP clients connect to separate TLS 1.3 servers through the
hardened boundary. A2A claims and executes one purchase; the same Quote/escrow
submitted through MCP reaches the shared Gate but not the runner, yielding
exact counters `gate=2` and `runner=1`. This closes the local protocol-switch
replay test, not the fresh external interoperability requirement.

## 1. Gate A — Registry protocol freeze

Deliver:

- ✅ clean `tos.service.v1` schema;
- ✅ network domain, identifiers, action cells, policies, and state cells;
- ✅ deterministic Agent and Capability registration vectors, including
  independently reproduced identifiers, addresses, action hashes, and BOCs;
- ✅ stable typed errors and a frozen cross-implementation negative mutation
  corpus; and
- ✅ explicit repository ownership.

Accept when two independent implementations reproduce every frozen registry
digest and reject all negative mutations.

**Gate status: ✅ Complete.** `nativecore` and the independent
`internal/referencecodec` implementation reproduce the frozen Agent and
Capability vector and reject every frozen negative mutation without sharing
protocol encoding code.

## 2. Gate B — Registry implementation assurance

Deliver:

- ✅ deterministic Agent and Capability accounts;
- ✅ complete state machines;
- ✅ live policy authorization;
- ✅ atomic Capability transfer;
- ✅ direct typed-state resolution;
- ✅ internal contract and `nativecore` review and remediation;
- 🟡 independent contract and `nativecore` security review, including the
  chain-time recovery preflight and crash-safe relay journal remediations;
- ✅ adversarial encoder, resolver, relay, mutation-corpus, release-hash,
  source-cleanliness, and recovery-policy-binding lifecycle checks; and
- ✅ independent full-lifecycle TVM emulator evidence covering every Agent and
  Capability transition, including negative and atomic-transfer cases.

Accept when the full lifecycle passes on a local chain, the exported code hash
matches frozen vectors, and independent review finds no unauthorized or partial
transition.

**Gate status: 🟡 Migration delta review pending.** Implementation, frozen
conformance, reproducible contract release, and full lifecycle tests pass under
the new domain. The prior independent review remains relevant to the unchanged
contract state machines, but Gate B requires a focused independent review of
the renamed domains, generated protobuf, vectors, and cross-repository imports
before it can be accepted for `tos_service_v1`.

## 3. Gate C — Public testnet authority

Deliver:

- ✅ reproducible contract build, frozen release BOC, code hash, release
  manifest, and two-build comparison;
- ✅ build/source separation that leaves generated `.fif` and embedded `.cpp`
  intermediates outside the source tree and verifies this invariant in CI;
- ✅ C++ consensus VM and Rust emulator `SHA256C` differential coverage using
  the same version-14 canonical snake vector;
- ✅ designated initial public-testnet ConfigParam 8 at global version 14;
- ⬜ current-domain public-testnet deployment record binding network domain, contract
  address, deployed code BOC, code hash, transaction, and exact source commit;
- ⬜ current-domain three-validator strict-majority finalized
  resolution through the production typed-state resolver;
- ✅ wallet action signing and semantic confirmation, including exact action-hash
  confirmation and fee-payer destination, amount, body, and StateInit binding;
- ✅ registry typed-state checker with machine-readable three-endpoint quorum
  evidence; and
- ⬜ recovery, transfer, former-owner rejection, and revocation drills on the
  designated initial public test network.

Accept the initial profile when distinct controller keys register, update,
transfer, revoke, and resolve objects through validator-backed quorum without
trusting the reference gateway. Independent operators and public HTTPS are
required by Gates F and G.

**Gate status: ⬜ Current-domain deployment pending.** The reproducible contract,
wallet, resolver, and lifecycle tooling pass locally. The 2026-08-14 deployment
is archived pre-migration evidence and cannot establish authority for
`tos_service_v1`. Gate C must deploy fresh objects and repeat the complete
quorum lifecycle under the current protocol domain.

## 4. Gate D — First commercial lifecycle

This gate is the highest product priority after Registry assurance. It covers
one machine-checkable software-work profile only.

Deliver:

- ✅ immutable software-work Capability manifest profile — canonical CBOR,
  bounds, positive vector, eight-case negative corpus, production Go encoder,
  and independent stdlib-only Python reproducer are frozen;
- ✅ deterministic Accepted Quote commitment, vector, and TOS transaction — the
  TVM cell, exact tUSDT identity, typed transport, execution authorization,
  escrow and dispute preimages, production encoder, independent vector, and
  finalized public escrow StateInit are recorded;
- ✅ exact endpoint and execution-signer binding — Capability version `1.1.0`
  and the finalized Accepted Quote bind the typed transport and execution
  authorization commitments;
- ✅ test-only TOS-network stablecoin deployment with exact master-contract
  identity, six-decimal metadata, controlled wc=0 buyer wallet, reproducible
  code hashes, and three-endpoint state evidence;
- ✅ TOS-network stablecoin escrow with bounded native TOS network fees — the
  fixed-price contract and frozen `0.1 TOS` wallet-call budget are implemented,
  emulator-tested, and deployed as the finalized Accepted Quote StateInit;
- ✅ isolated compilation, deterministic emulator tests, and reproducible-build
  execution for the frozen escrow BOC;
- ✅ canonical Receipt binding input, toolchain, result, artifacts, evidence,
  provider, and charged amount;
- ✅ objective fixed-price release and timeout-refund transfer initiation,
  including replay-blocking pending states and initial-wallet bounce recovery;
- ✅ narrowly defined dispute evidence where an automatic outcome is
  impossible — V1 freezes an objective no-arbiter policy and exact evidence
  preimage rather than introducing a gateway-controlled decision maker;
- ✅ content-addressed artifact delivery — bounded immutable storage,
  deterministic report/artifact construction, tamper detection, exact
  manifest-to-executor mapping, and crash-safe at-most-once execution are
  implemented; the reproducible Go 1.26.5 OCI toolchain is frozen at index
  digest `sha256:9624bca74096f810c5b24e489521dde124fadcfa1808581648b38bdc1ba1b105`,
  two builds were byte-identical, and its live containerd workspace
  conformance passed; and
- ✅ independently resolvable Quote, escrow, Receipt, and settlement — one
  finalized 25,000,000 atomic `tUSDT` software-work transaction, its immutable
  artifact and report, the provider-wallet credit, and matching escrow state
  from three validator-backed endpoints are recorded in
  `deployments/archive/pre-tos-service-v1/initial-public-testnet-paid-software-work-2026-08-14.json`.

Accept when a buyer outside the core development team pays an independent
provider on a public TOS network and another resolver reconstructs the complete
history without a private gateway database.

Do not block this gate on general marketplace ranking, generalized arbitration,
multiple verticals, cross-chain support, or per-message settlement.

**Gate status: 🟡 Core escrow and provider execution implementation migrated;
current-domain chain evidence and external acceptance pending.**
Accepted Quote primitives, the test-only `tUSDT` asset recorded in
`deployments/archive/pre-tos-service-v1/initial-public-testnet-tusdt-2026-08-14.json`, the fixed-price
escrow, canonical Receipt, objective transfer transitions, reproducible BOC,
and finalized typed escrow-state resolver now exist. The archived same-host
transaction proves the pre-migration implementation only. A fresh
`tos_service_v1` Capability, Quote, escrow, Receipt, and settlement must be
recorded before the external buyer/provider/resolver acceptance session.

## 5. Gate E — Developer usability and protocol adapters

Deliver:

- ✅ provider SDK and deployment template — the first Go publication SDK and
  dedicated private-containerd template are implemented; a fresh same-host
  provider identity and Capability were published with newly generated
  controller custody and real signed Native actions, recorded in
  `deployments/archive/pre-tos-service-v1/local-gate-e-fresh-native-publication-2026-08-15.json`; an
  externally operated provider onboarding session is still required;
- ✅ buyer SDK and wallet budget flow — canonical purchase preflight and the
  crash-safe bounded funding journal and production `tosctl` stablecoin sender
  are implemented and have been revalidated end to end against live finalized
  state; a fresh same-host buyer used new custody to purchase the newly
  published software-work Capability for 25,000,000 atomic `tUSDT`, recorded
  in `deployments/archive/pre-tos-service-v1/local-gate-e-fresh-buyer-purchase-2026-08-15.json`; its
  canonical Receipt subsequently authorized the exact 25,000,000-atomic
  settlement at a later finalized checkpoint; an externally operated buyer
  working session remains;
- ✅ minimal finalized-state Capability index and manifest retrieval — the
  bounded derived catalog, fresh-finality listing, canonical content store,
  protobuf service, and gateway handlers are implemented; a clean public
  same-host deployment published, searched, and retrieved the fresh
  Capability exclusively through the public Connect API without catalog file
  edits, recorded in
  `deployments/archive/pre-tos-service-v1/local-gate-e-fresh-buyer-purchase-2026-08-15.json`; a second
  same-host Gateway with separate storage and credentials correctly returned
  no result before provider publication and independently retrieved the exact
  manifest afterward, recorded in
  `deployments/archive/pre-tos-service-v1/local-gate-e-role-isolated-simulation-2026-08-15.json`; an
  independently operated cross-gateway retrieval test remains;
- ✅ A2A task and result adapter — the official A2A 1.0 Go types, exact
  request/result mapping, shared production finalized-chain execution Gate,
  synchronous JSON-RPC server binding, and negative tests are implemented;
  the public listener and local cross-transport single-execution test are
  complete; a fresh funded purchase was admitted from a strict-majority
  finalized chain view and executed through the public TLS transport in
  `deployments/archive/pre-tos-service-v1/local-gate-e-live-chain-adapter-acceptance-2026-08-15.json`;
  external interoperability remains an acceptance activity, not engineering;
- ✅ MCP tool adapter — official MCP 2026-07-28 typed tool registration,
  committed input/result mapping, shared production finalized-chain execution
  Gate, stateless streamable-HTTP binding, and negative tests are implemented;
  the public listener and local cross-transport single-execution test are
  complete; replaying the same live funded purchase after its A2A execution
  reached the shared chain Gate but never the runner, as recorded in
  `deployments/archive/pre-tos-service-v1/local-gate-e-live-chain-adapter-acceptance-2026-08-15.json`;
  external interoperability remains an acceptance activity, not engineering;
- ⏸ optional x402 payment-negotiation adapter — deliberately deferred until
  Gate F demonstrates recurring buyer demand. `docs/X402_ADAPTER_DECISION.md`
  forbids a parallel facilitator-owned settlement path and limits any future
  adapter to representation over the existing finalized TOS escrow lifecycle;
- ✅ gateway-local search with chain-derived fields kept separate; and
- ✅ examples that require no operator database edits or hidden control service.

Accept when a new provider publishes and sells the software-work Capability and
a new buyer purchases it using public documentation in one working session.

Adapters must map into the same Agent, Capability, Accepted Quote, Receipt, and
chain-reference objects. They cannot create parallel protocol facts.

**Gate status: 🟡 Engineering migration complete; current-domain live and
external acceptance pending.** Unit, race, adapter, and cross-transport code
passes under the new imports and domains. The archived same-host role-isolated
run is pre-migration evidence. A fresh current-domain live session must precede
the independently operated provider and buyer acceptance sessions.

## 6. Gate F — Open gateway and market evidence

Deliver:

- ✅ gateway discovery document — `docs/GATEWAY_DISCOVERY_V1.md` freezes the
  bounded `/.well-known/tos-service.json` locator and its non-authority,
  expiry, failover, downgrade, credential, and SSRF rules; `tos-service-gateway` commit
  `657bd4a` implements the explicit-origin well-known response without trusting
  request forwarding headers, and `tos-service-protocol` commit `4e7b45c` adds strict
  client validation with bounded reads, authority-domain matching, redirect
  rejection, HTTPS enforcement, address filtering, and DNS-pinned dialing;
- ✅ interoperable search and Quote Proposal exchange —
  `docs/GATEWAY_FEDERATION_V1.md` freezes authority-neutral client-side search
  composition and content-addressed manifest failover; `tos-service-protocol` commit
  `ec145a9` implements bounded multi-Gateway aggregation, source preservation,
  malformed peer isolation, and exact-digest retrieval. `tos-service-protocol` commit
  `aedc832` adds the `RequestQuoteProposal` wire method and strict complete-
  preimage validator; `tos-service-gateway` commit `1e2a812` adds the authenticated provider
  source boundary and rejects conflicting packages. `tos-service-protocol` commit
  `6a9582d` constructs packages only from freshly finalized provider-owned
  Capability state, and `tos-service-gateway` commit `7f88298` loads bounded commercial policy
  from owner-private files. Two isolated local Gateways returned independently
  validated packages and Gateway B continued after Gateway A stopped, recorded
  in `deployments/archive/pre-tos-service-v1/local-gate-f-federated-quote-conformance-2026-08-15.json`;
- ✅ canonical error and retry semantics — `docs/PUBLIC_ERRORS_V1.md` freezes
  codes `2300..2308`, Connect mappings, bounded backoff, fail-closed parsing,
  and mandatory resolution after ambiguous mutations. `tos-service-protocol` commit
  `5c091f9` implements creation/parsing and private Native classification;
  `tos-service-gateway` commit `7a0b58f` applies it to every public Gateway boundary and
  verifies detail survival across the Connect wire;
- ✅ pre-acceptance routing and post-acceptance failover rules —
  `docs/SAFE_HANDOFF_V1.md` freezes the portable boundary; the production
  verifier reconstructs Quote, Accepted Quote, Receipt, and settlement intent
  solely from owner-held inputs and finalized escrow, covers funded and
  release-pending recovery, and fails closed on every authority boundary; the
  `native-safe-handoff-check` CLI emits quorum-bound external evidence with
  zero Gateway inputs;
- 🟡 public relay, resolver, Quote, and Receipt conformance tests — local relay
  and resolver tests exist; public Quote conformance and portable Receipt
  conformance now exist locally. `tos-service-protocol` commits `f000e6d` and `b83515b`
  add the strict bundle packer, quorum checker, and parser negative tests;
  `tos-service-spec` commits `92129a5` and `e0ea5c6` publish the template and operator
  runbook. The live two-process failover rehearsal is recorded in
  `deployments/archive/pre-tos-service-v1/local-gate-f-safe-handoff-conformance-2026-08-15.json`.
  An independently operated public Receipt session still does not exist;
- ⬜ at least two independently operated gateways;
- ⬜ at least three independently operated providers; and
- ⬜ at least ten useful, purchasable Capabilities in the proven profile.

Accept when either gateway can disappear at every safe handoff point without
loss of identity, ownership, accepted terms, artifacts, Receipt, or settlement,
and buyers outside the core team demonstrate recurring paid use.

**Gate status: ⬜ Not accepted.** Multi-operator deployment and recurring paid-use
evidence do not exist. All remaining Gate F work is external acceptance, not
unimplemented protocol engineering.

## 7. Gate G — Production readiness

Deliver:

- ⬜ independent contract and protocol audits;
- 🟡 production key custody, wallet recovery, and bounded spending policy —
  operational baseline is defined in `docs/PRODUCTION_READINESS_RUNBOOK_V1.md`;
- 🟡 endpoint diversity and finality incident procedures — runbook baseline
  exists; multi-operator exercise remains;
- ⬜ load, storage, denial-of-service, and fee-budget evidence;
- ⬜ TOS-network stablecoin accounting and operator compliance controls;
- 🟡 monitoring for code, state, quorum, finality, and economic divergence —
  required signals and stop-the-line rules are defined in the runbook;
- 🟡 reproducible releases and signed deployment artifacts — repository-level
  reproducibility exists; production signing and release ceremony remain; and
- 🟡 operator runbooks for degraded and emergency states — baseline published
  in `docs/PRODUCTION_READINESS_RUNBOOK_V1.md`.

Accept only after a multi-operator exercise completes discovery, Quote
acceptance, paid software execution, Receipt checking, settlement, gateway
failure, provider failure, endpoint disagreement, refund, and client recovery.

**Gate status: 🟡 Operational baseline drafted; production acceptance pending.**
The runbook closes the documentation/design gap, but independent audits,
production custody, endpoint diversity, load/DoS evidence, accounting evidence,
signed release ceremony, and the multi-operator exercise remain.

## 8. Expansion gate

Data APIs, model inference, GPU markets, provider composition, payment channels,
additional assets, and additional networks are eligible only after Gate F shows
recurring paid demand. Each expansion needs a measurable customer outcome and
must reuse the existing authority objects.

**Status: ⬜ Locked.** Gate F has not demonstrated recurring paid demand.

## 9. Work ordering rules

- Registry mutations require finalized typed-state authority first.
- The first commercial lifecycle precedes broad marketplace features.
- Execution follows Accepted Quote and required escrow finality.
- Settlement follows Receipt checking.
- Convenience projections follow typed-state decoding.
- Adapters follow one working direct protocol path.
- Open federation follows one conforming gateway and one real transaction path.
- Off-chain Agent packets require finalized sender/recipient identity and
  replay protection; transport discovery never becomes semantic authority.
- Expansion follows recurring paid use.

## 10. Immediate work

1. ✅ Close the independent Registry contract and `nativecore` audit — the
   final 2026-08-14 review found no P0, P1, or P2 and accepted the chain-time,
   atomic slot-intent, and broadcast-lease remediations.
2. ✅ Produce independent full-lifecycle TVM emulator evidence for every Agent
   and Capability transition — the final review independently reproduced the
   ten-test Agent/Capability matrix with no unauthorized or partial transition.
3. ✅ Add a Capability registration vector and second vector implementation.
4. ✅ Freeze and continuously reproduce the Registry BOC, code hash, release
   manifest, negative corpus, and clean source/build boundary.
5. ✅ Deploy the frozen Registry code to the operator-designated initial public
   TOS testnet and publish the complete deployment record.
6. ✅ Implement wallet-native action signing and exact semantic confirmation.
7. ✅ Record the complete finalized Agent and Capability lifecycle and resolve
   it through three validator-backed JSON-RPC endpoints with quorum two.
8. 🟡 **Active Gate D workstream:**
   1. ✅ freeze the bounded software-work manifest schema, canonical byte
      encoding, media type, digest rule, positive vector, and negative corpus;
   2. ✅ implement the manifest in `tos-service-spec`, `tos-service-protocol`, and one
      independent vector implementation, then bind its digest to a Capability
      version on the initial public test network — the non-revoked Capability
      and three-endpoint evidence are recorded in
      `deployments/archive/pre-tos-service-v1/initial-public-testnet-software-work-capability-2026-08-14.json`;
   3. ✅ freeze the Accepted Quote TVM cell and vector using an exact
      TOS-network stablecoin contract identity, endpoint commitment, typed
      execution signer authorization, typed escrow terms, dispute terms, price,
      and expiry; the cell encoding, actual Capability ID, asset identity,
      signer key preimage, and escrow terms preimage. The manifest now binds
      typed transport digest `dca9babc…6c44c` and the objective no-arbiter
      dispute-policy digest `1b42dbb0…d76345`; Capability version `1.1.0` is
      finalized at generation 1, sequence 2, and the regenerated Quote
      commitment is `3143417c…23ce57`;
   4. ✅ deploy the escrow StateInit containing the complete Accepted Quote,
      finalize that TOS transaction, and resolve both the transaction and typed
      escrow state without gateway-private data; this transaction is the
      canonical Quote acceptance event — escrow `0:ee6918da…a4241f7a`,
      transaction `2e02dd6c…1f19db`, and identical typed data hash
      `c7cbb362…cda4eb` are recorded from all three endpoints in
      `deployments/archive/pre-tos-service-v1/initial-public-testnet-escrow-2026-08-14.json`.
9. ✅ Deploy a test-only TOS-network stablecoin and controlled wc=0 buyer
   wallet. The exact `tUSDT` master identity is
   `0:ca11200a7d4a3c6822af077f035131868584f40f48fb1b7b7b1889ae51f9926a`;
   this is test infrastructure, not a claim on real USDT reserves.
10. ✅ Implement the TOS-network stablecoin escrow contract, reproducible
    release artifact, exact StateInit builder, and finalized typed resolver.
11. ✅ Freeze the canonical software-work Receipt and implement objective
    release and refund transitions. Five TVM emulator groups cover full release,
    timeout refund, source/amount/signature rejection, buyer/deadline/replay
    rejection, malformed Receipt rejection, and wallet-bounce recovery through
    the actual frozen test stablecoin wallet code. Standard-wallet `excesses`
    is explicitly non-authoritative; terminal settlement resolution remains in
    item 13's multi-account transaction proof.
12. ✅ Integrate the bounded executor and content-addressed artifact delivery —
    `tos-ai` now maps the provider-fixed image, invocation, workspace, and
    limits into containerd; safely extracts source archives; produces
    deterministic reports and USTAR artifacts; stores and reverifies immutable
    SHA-256 objects; and journals at-most-once execution across crashes. The
    reproducible Go 1.26.5 OCI image is frozen at index digest
    `sha256:9624bca74096f810c5b24e489521dde124fadcfa1808581648b38bdc1ba1b105`;
    two build archives were byte-identical and the pinned image passed the live
    containerd workspace test under the production isolation policy. The
    provider-local executor also rejects non-canonical, symlinked, non-private,
    foreign-owned, or oversized privileged input paths; raw containerd access
    remains isolated from gateways and signing custody.
13. ✅ Complete one independently resolvable paid software-work transaction —
    Capability `cap_c1745824…e657` version `1.2.0` was sold for 25,000,000
    atomic `tUSDT`; the pinned OCI job completed successfully; the canonical
    Receipt committed the result, artifact, report, source, toolchain, and
    sandbox; and the release credited the provider wallet. Three endpoints
    independently report the same finalized escrow and wallet state in
    `deployments/archive/pre-tos-service-v1/initial-public-testnet-paid-software-work-2026-08-14.json`.

All local Gate D implementation items are complete. The next Gate D acceptance
task is an external pilot with a buyer outside the core team, an independent
provider, and an independently operated resolver or endpoint set. The
same-host transaction is reproducible deployment evidence, not grounds to mark
Gate D accepted. The role separation, execution sequence, strict verification
command, custody-safe two-stage Receipt signing flow, and acceptance record are
frozen in `docs/GATE_D_EXTERNAL_PILOT.md`. A fresh local preflight exercised
that flow through a second 25,000,000 atomic `tUSDT` settlement and proved the
provider balance increase between finalized checkpoints; its evidence is
`deployments/archive/pre-tos-service-v1/initial-public-testnet-gate-d-local-preflight-2026-08-14.json`.
Multi-operator HTTPS endpoint diversity remains required in Gates F and G and
is not implied by Gate C's initial profile.

14. 🟡 **Gate E external acceptance:** the public Native client, provider SDK and
    deployment template, plus the buyer's canonical purchase preflight and
    crash-safe bounded funding journal, plus the minimal authority-neutral
    Capability catalog/manifest API, and the authority-gated A2A task/result
    mapping, MCP tool adapter, shared production chain execution-claim Gate,
    official server bindings, hardened public listener, local search, and
    public-interface discovery CLI are implemented. A fresh funded purchase
    has now passed the live 2-of-3 chain execution Gate over A2A/TLS, its MCP
    replay was rejected with one runner call, and its exact Receipt settled on
    chain; see
    `deployments/archive/pre-tos-service-v1/local-gate-e-live-chain-adapter-acceptance-2026-08-15.json`.
    Engineering is complete. The remaining Gate E task is one independently
    operated provider/buyer working session using the public onboarding docs.
    The optional x402 adapter has been evaluated and
    deferred under `docs/X402_ADAPTER_DECISION.md` until Gate F supplies real
    demand. In parallel, deploy and cross-check discovery
    and run the fresh provider/buyer sessions from
    `docs/GATE_E_PROVIDER_ONBOARDING.md` and
    `docs/GATE_E_BUYER_ONBOARDING.md`. Gate D external acceptance continues
    independently and is not being claimed by this work.
15. 🟡 **Active Gate F external acceptance only:** client-side federated Capability search,
    exact-digest manifest failover, complete-preimage Quote Proposal exchange,
    finalized provider-state construction, and local two-Gateway failover are
    complete. Canonical public error/retry details, portable safe-handoff
    verification, the bundle packer, and the quorum checker are also complete.
    No additional local protocol implementation is required for this item. The
    next executable task is an independent buyer/provider/resolver session:
    create a complete bundle with `native-safe-handoff-pack`, stop the original
    Gateway, and verify it with `native-safe-handoff-check` against three
    validator endpoints. Then recruit two independently operated Gateways,
    three providers, ten useful Capabilities, and recurring buyers. Until that
    evidence exists, Gate F must remain not accepted.
16. ✅ **Chain-authenticated off-chain Agent messaging:** `tos-service-protocol` commits
    `7aa6f86`, `9603c9d`, `ee25dea`, `e689536`, `79ab13d`, and `2537154`
    implement the signed Agent Packet, strict JSON wire format, replay guard,
    direct HTTPS/loopback HTTP transport, signed Contact Card discovery,
    network-tuple binding, and bounded Contact Card issuance lifetime.
    `tos-service-spec` commits `41e01a9`, `4306efe`, `54e2b4d`, `df9194c`, and
    `804ba08` define the envelope, locator, wire exchange, and security
    boundary. Payloads remain off-chain; finalized Agent policy authorizes
    keys; no Gateway, Managed mode, or arbitrary on-chain message store is
    introduced. Follow-up is integration into a production Agent runtime after
    Gate D/E/F external sessions, not a new consensus feature.
17. 🟡 **Application-layer product bridge:** the OpenFox buyer/provider
    integration contract and shared iOS/Android client design are now frozen in
    `docs/OPENFOX_ECONOMIC_BRIDGE_V1.md` and
    `docs/MOBILE_TOS_SERVICE_CLIENT_V1.md`. Runtime integration, mobile UX, and a fresh
    paid application session remain after the protocol/SDK work; these apps
    must reuse the finalized Native lifecycle and cannot create parallel facts.
18. ⬜ **Agent economy metrics:** `docs/AGENT_ECONOMY_METRICS_V1.md` defines
    exact-asset network, Agent, and Capability statistics derived only from
    finalized escrow, Receipt, and stablecoin settlement evidence. It includes
    gross Agent value, provider receipts, job counts, unique buyer wallets,
    terminal release and refund rates, settlement latency, active Registry
    supply, rankings,
    coverage, and
    separately labelled operational availability. The finalized transaction
    and historical Registry indexes, provider anti-spoofing attribution,
    deterministic aggregator, protobuf/Connect export, frozen vectors, and
    independent-indexer comparison are not implemented.
19. 🟡 **FreeCity first society application:**
    `docs/FREECITY_APPLICATION_V1.md` now defines the non-normative application
    profile and authority mapping for FreeCity as the first human-and-Agent city
    built on TOS Network. The profile adds no protocol surface and preserves the
    machine-checkable software-work wedge. Implementation and acceptance remain
    pending. The next application tasks are a read-only finalized Agent and
    Capability projection, provenance-labelled city events, and one
    current-domain testnet collaboration from Quote Proposal through Accepted
    Quote, escrow, OpenFox or `tos-ai` execution, canonical Receipt, settlement,
    and independent resolution. This item cannot claim completion before the
    relevant Gate C, D, and E current-domain evidence exists, and it cannot
    claim an open recurring economy before Gate F.
