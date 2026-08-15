# ATOS Native Implementation Roadmap

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

A gate is complete only when every delivery item and its acceptance condition
are complete. The final 2026-08-14 independent Gate B review evaluated
`atos-spec` commit `e72bab245a47b0f87a82977629cc03b1dfc64995`, `tos` commit
`a787cb02dd6bc386be053ab233d0581cc1a14ef3`, and `tos-protocol` commit
`7a21c070c1160fc0a4278e1a086c0682eb2d3d31`. It found no P0, P1, or P2,
confirmed the chain-time recovery remediation and crash-safe relay journal, and
independently reproduced the complete Native Registry TVM lifecycle matrix.
Gate C deployment evidence must continue to bind exact reviewed commits and
release hashes.

The initial Gate C deployment record is published by `atos-spec` commit
`7a6cc02360e4cc8c2d95f80d433704cd72b0dc32`. Persistent validator JSON-RPC
configuration is in `tos` commit
`145bf7de195ac6105c630510ab51912f4b9e92ca`; the production quorum checker,
live-node transaction response compatibility, and diagnostic-only quorum error
detail are in `tos-protocol` commit
`6bb42b8968d4bbc374a89b7b61ea2c0e958d91ca`. These operational additions do
not change the frozen Registry BOC, action encoding, authorization, state
machine, or quorum decision rule reviewed at Gate B.

The pre-escrow Gate D design and test-evidence baseline is `atos-spec` commit
`11464a84d0dec985f22636a8a94b3770c0cc2418`, `tos` commit
`dc71dc8712f58e3d11ed973f4980ff6ae71de845`, and `tos-protocol` commit
`6bb42b8968d4bbc374a89b7b61ea2c0e958d91ca`. It freezes the first
software-work manifest and Accepted Quote encodings, records the finalized
Capability binding and test-only stablecoin deployment, and provides
`tosctl`-generated Ed25519 test identities. It intentionally makes no escrow,
Quote-acceptance, execution, Receipt, or settlement claim; the implementation
status below supersedes that historical baseline and must be bound to new exact
commit hashes before public deployment.

## 1. Gate A — Registry protocol freeze

Deliver:

- ✅ clean `atos.native.v1` schema;
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
- ✅ independent contract and `nativecore` security review, including the
  chain-time recovery preflight and crash-safe relay journal remediations;
- ✅ adversarial encoder, resolver, relay, mutation-corpus, release-hash,
  source-cleanliness, and recovery-policy-binding lifecycle checks; and
- ✅ independent full-lifecycle TVM emulator evidence covering every Agent and
  Capability transition, including negative and atomic-transfer cases.

Accept when the full lifecycle passes on a local chain, the exported code hash
matches frozen vectors, and independent review finds no unauthorized or partial
transition.

**Gate status: ✅ Complete.** Implementation, frozen conformance, reproducible
contract release, full lifecycle testing, and independent security review are
complete for the reviewed commits above. The independent review found no
unauthorized or partial transition.

## 3. Gate C — Public testnet authority

Deliver:

- ✅ reproducible contract build, frozen release BOC, code hash, release
  manifest, and two-build comparison;
- ✅ build/source separation that leaves generated `.fif` and embedded `.cpp`
  intermediates outside the source tree and verifies this invariant in CI;
- ✅ C++ consensus VM and Rust emulator `SHA256C` differential coverage using
  the same version-14 canonical snake vector;
- ✅ designated initial public-testnet ConfigParam 8 at global version 14;
- ✅ initial public-testnet deployment record binding network domain, contract
  address, deployed code BOC, code hash, transaction, and exact source commit;
- ✅ three validator-backed JSON-RPC endpoints and strict-majority finalized
  resolution through the production typed-state resolver;
- ✅ wallet action signing and semantic confirmation, including exact action-hash
  confirmation and fee-payer destination, amount, body, and StateInit binding;
- ✅ registry typed-state checker with machine-readable three-endpoint quorum
  evidence; and
- ✅ recovery, transfer, former-owner rejection, and revocation drills on the
  designated initial public test network.

Accept the initial profile when distinct controller keys register, update,
transfer, revoke, and resolve objects through validator-backed quorum without
trusting the reference gateway. Independent operators and public HTTPS are
required by Gates F and G.

**Gate status: ✅ Complete under the initial public-testnet profile.** The
2026-08-14 deployment and lifecycle are recorded in
`deployments/initial-public-testnet-2026-08-14.json`, and production quorum
typed-state outputs are recorded in
`deployments/initial-public-testnet-quorum-2026-08-14.json`. The record openly
states that the three endpoints share one host and use loopback HTTP; this does
not satisfy Gate F/G diversity or production-readiness requirements.

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
  `deployments/initial-public-testnet-paid-software-work-2026-08-14.json`.

Accept when a buyer outside the core development team pays an independent
provider on a public TOS network and another resolver reconstructs the complete
history without a private gateway database.

Do not block this gate on general marketplace ranking, generalized arbitration,
multiple verticals, cross-chain support, or per-message settlement.

**Gate status: 🟡 Core escrow and provider execution implementation complete;
Gate not accepted.**
Accepted Quote primitives, the test-only `tUSDT` asset recorded in
`deployments/initial-public-testnet-tusdt-2026-08-14.json`, the fixed-price
escrow, canonical Receipt, objective transfer transitions, reproducible BOC,
and finalized typed escrow-state resolver now exist. Typed endpoint and dispute
commitments and the public escrow deployment are finalized. The same-host
public-testnet rehearsal now includes a complete independently reproducible
paid transaction, but it does not satisfy the acceptance requirement for a
buyer outside the core team, an independent provider, and an independently
operated resolver. Local operator diversity is not external independence.

## 5. Gate E — Developer usability and protocol adapters

Deliver:

- 🟡 provider SDK and deployment template — the first Go publication SDK and
  dedicated private-containerd template are implemented; a fresh-provider
  onboarding session is still required;
- 🟡 buyer SDK and wallet budget flow — canonical purchase preflight and the
  crash-safe bounded funding journal are implemented; the production `tosctl`
  stablecoin sender and a fresh-buyer working session remain;
- ⬜ minimal finalized-state Capability index and manifest retrieval;
- ⬜ A2A task and result adapter;
- ⬜ MCP tool adapter;
- ⬜ optional x402 payment-negotiation adapter;
- ⬜ gateway-local search with chain-derived fields kept separate; and
- ⬜ examples that require no operator database edits or hidden control service.

Accept when a new provider publishes and sells the software-work Capability and
a new buyer purchases it using public documentation in one working session.

Adapters must map into the same Agent, Capability, Accepted Quote, Receipt, and
chain-reference objects. They cannot create parallel protocol facts.

**Gate status: 🟡 In progress.** The complete same-host Native transaction and
independent reconstruction are sufficient to continue SDK and adapter
engineering; Gate D's external commercial acceptance proceeds independently
and remains unaccepted. Provider publication/deployment and the buyer's
canonical preflight/bounded funding journal are implemented foundations. This
sequencing exception does not weaken either gate's acceptance criteria.

## 6. Gate F — Open gateway and market evidence

Deliver:

- ⬜ gateway discovery document;
- 🟡 interoperable search and Quote Proposal exchange — non-canonical Quote
  objects are defined, but federation is not implemented;
- 🟡 canonical error and retry semantics — protocol errors exist, but public
  conformance is incomplete;
- 🟡 pre-acceptance routing and post-acceptance failover rules — architecture
  rules exist without multi-gateway acceptance evidence;
- 🟡 public relay, resolver, Quote, and Receipt conformance tests — local relay
  and resolver tests exist; public Quote and Receipt conformance does not;
- ⬜ at least two independently operated gateways;
- ⬜ at least three independently operated providers; and
- ⬜ at least ten useful, purchasable Capabilities in the proven profile.

Accept when either gateway can disappear at every safe handoff point without
loss of identity, ownership, accepted terms, artifacts, Receipt, or settlement,
and buyers outside the core team demonstrate recurring paid use.

**Gate status: ⬜ Not accepted.** Multi-operator deployment and recurring paid-use
evidence do not exist.

## 7. Gate G — Production readiness

Deliver:

- ⬜ independent contract and protocol audits;
- ⬜ production key custody, wallet recovery, and bounded spending policy;
- ⬜ endpoint diversity and finality incident procedures;
- ⬜ load, storage, denial-of-service, and fee-budget evidence;
- ⬜ TOS-network stablecoin accounting and operator compliance controls;
- ⬜ monitoring for code, state, quorum, finality, and economic divergence;
- ⬜ reproducible releases and signed deployment artifacts; and
- ⬜ operator runbooks for degraded and emergency states.

Accept only after a multi-operator exercise completes discovery, Quote
acceptance, paid software execution, Receipt checking, settlement, gateway
failure, provider failure, endpoint disagreement, refund, and client recovery.

**Gate status: ⬜ Not started.** Production acceptance depends on Gates C through
F.

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
   2. ✅ implement the manifest in `atos-spec`, `tos-protocol`, and one
      independent vector implementation, then bind its digest to a Capability
      version on the initial public test network — the non-revoked Capability
      and three-endpoint evidence are recorded in
      `deployments/initial-public-testnet-software-work-capability-2026-08-14.json`;
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
      `deployments/initial-public-testnet-escrow-2026-08-14.json`.
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
    `deployments/initial-public-testnet-paid-software-work-2026-08-14.json`.

All local Gate D implementation items are complete. The next Gate D acceptance
task is an external pilot with a buyer outside the core team, an independent
provider, and an independently operated resolver or endpoint set. The
same-host transaction is reproducible deployment evidence, not grounds to mark
Gate D accepted. The role separation, execution sequence, strict verification
command, custody-safe two-stage Receipt signing flow, and acceptance record are
frozen in `docs/GATE_D_EXTERNAL_PILOT.md`. A fresh local preflight exercised
that flow through a second 25,000,000 atomic `tUSDT` settlement and proved the
provider balance increase between finalized checkpoints; its evidence is
`deployments/initial-public-testnet-gate-d-local-preflight-2026-08-14.json`.
Multi-operator HTTPS endpoint diversity remains required in Gates F and G and
is not implied by Gate C's initial profile.

14. 🟡 **Active Gate E workstream:** the public Native client, provider SDK and
    deployment template, plus the buyer's canonical purchase preflight and
    crash-safe bounded funding journal, are implemented. Next build the minimal
    finalized-state Capability index and digest-addressed manifest retrieval.
    In parallel, add the production `tosctl` stablecoin sender and run the fresh
    provider/buyer sessions from `docs/GATE_E_PROVIDER_ONBOARDING.md` and
    `docs/GATE_E_BUYER_ONBOARDING.md`. Gate D external acceptance continues
    independently and is not being claimed by this work.
