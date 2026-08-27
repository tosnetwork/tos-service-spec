<!-- markdownlint-disable MD013 -->

# Agent Guarantor Service V1 Implementation Report

## 1. Status and evidence boundary

This report records the implementation candidate produced on 2026-08-27 for
the pre-freeze [Decentralized Agent Guarantor Service V1](AGENT_GUARANTOR_SERVICE_V1.md).
It is reproducibility evidence, not a declaration that the profile is frozen,
legally enforceable, deployed on a public network, or accepted for every
assurance tuple.

The implemented production boundary is the Go protocol SDK, generic Messenger
carriage, and an owner-assembled OpenFox Provider runtime for
`unsecured-signed`. The runtime defaults off and refuses incomplete authority,
signing, underwriting, journal, transport, or payment dependencies. OpenFox's
general CLI does not synthesize these dependencies from AI output or inbound
Intent data and rejects an enabled but unassembled Guarantor runtime.

## 2. Pinned revisions

| Repository | Branch | Revision | Role |
| --- | --- | --- | --- |
| `tos-service-spec` | `docs/agent-guarantor-service-v1` | `5ea416d4c97446ee2083a7a021fa4d0e3f76ce15` plus this report | design and generated JSON Schema |
| `tos-service-protocol` | `feat/agent-guarantor-service-v1` | `d87b62b98e1f18a7811a1c3a005b1e74d671f22d` | canonical objects, registries, verification, state machines, fixtures |
| `tos-messenger` | `feat/agent-guarantor-service-v1` | `53ddf27a47d62056391050f924e0f58c8e18e1c9` | generic profile-event carriage and isolated inbox |
| `openfox` | `feat/agent-guarantor-service-v1` | `82d3f98081aae3e3273e05cf7ac9e5960c2edb45` | durable Provider lifecycle and runtime assembly boundary |
| `tos` | unchanged | `337417210411e9cd46bb0c765409a9c1e116fca4` | no consensus or contract change for the enabled tuple |

The Messenger module pins protocol revision `d87b62b`; the OpenFox module pins
both `d87b62b` and `53ddf27`. The verification below used those remote module
versions with `GOWORK=off`, so a local workspace replacement was not required
for success.

## 3. Implemented capability matrix

| Capability | Result |
| --- | --- |
| canonical Guarantor objects and strict CBOR | implemented in `pkg/agentguarantor` |
| generated JSON Schema | generated and byte-compared with `schemas/agent-guarantor-service-v1.json` |
| object and mutation verifier registries | closed registries, generated fixture, static dispatch, unknown-kind rejection |
| Semantic Action identities | Guarantor action entries, canonical semantic fields, collision and mutation checks |
| service profile and signed Intent artifact | strict profile validation, bounded lineage, publication authorization resolution |
| quote request and firm offer | exact request/profile/Agreement/terms binding and reserve-before-sign |
| acceptance | single-winner admission, writer fencing, accepted-effect evidence, recovery |
| activation, non-activation, and cancellation | portable evidence and durable state transitions |
| claim ingress and revision | isolated carriage, durable ingress/admission logs, bounded revision lineage |
| decision and deterministic fallback | profile-qualified decisions, admission/application receipts, bounded fallback |
| payout | conditional materialization, direct/external Adapter boundary, ambiguity-safe resolution |
| closure and exposure release | filing cut, terminal set, payout evidence, deterministic disposition, durable release |
| generic Messenger transport | inline and content-addressed `commerce.profile-event`, exact digest/size checks, lease completion/rejection |
| OpenFox Provider runtime | explicit dependency injection, private journal, single-writer lock, fenced actions, recovery |
| configuration and operator status | owner-authored limits, default-off gates, profile/journal inspection |

## 4. Security properties exercised

The test corpus covers malformed and non-canonical encodings, unknown object
and mutation kinds, digest and signature substitution, wrong profile and
authority domains, stale writer generations, split writers, stale portfolio
revisions, duplicate acceptance, claim-revision conflicts, admission-root
tampering, deadline and arithmetic overflow, Unix timestamp wraparound,
ambiguous sends, crash recovery, and payout recovery after an external
transfer but before local result persistence.

Payout recovery durably records `submitted` before calling an external sink.
After any ambiguous result, automatic recovery resolves the same stable action
and request digest; it does not issue a semantically new payment or resubmit
the transfer. The OpenFox Provider runtime validates that its inbox, verifier,
engine, sink, economic authority, coordinator identity, mandate, policy
revision, writer source, and bounded event lifetime are mutually consistent
before it claims an event.

## 5. Reproducible verification

The following commands passed on the pinned revisions:

The host was Linux amd64 with Go 1.26.6 and Python 3.14.4. Windows amd64 and
macOS arm64 results below are compile-only cross-platform checks; they are not
claims of runtime testing on those operating systems.

```text
# tos-service-protocol
GOWORK=off go test ./...
GOWORK=off go vet ./...
GOWORK=off go test -race ./pkg/agentguarantor ./pkg/agentcommerce
GOOS=windows GOARCH=amd64 CGO_ENABLED=0 GOWORK=off go test -exec=/bin/true ./...
GOOS=darwin GOARCH=arm64 CGO_ENABLED=0 GOWORK=off go test -exec=/bin/true ./...
python3 tests/conformance/agent_guarantor_registry_verify.py \
  < tests/conformance/agent-guarantor-v1.json

# tos-messenger
GOWORK=off go test ./...
GOWORK=off go vet ./...
GOWORK=off go test -race ./pkg/daemon ./pkg/envelope ./pkg/payload ./pkg/localapi
GOOS=windows GOARCH=amd64 CGO_ENABLED=0 GOWORK=off go test -exec=/bin/true ./...
GOOS=darwin GOARCH=arm64 CGO_ENABLED=0 GOWORK=off go test -exec=/bin/true ./...

# openfox
GOWORK=off go test -tags 'goolm stdjson' ./...
GOWORK=off go vet -tags 'goolm stdjson' ./...
GOWORK=off go test -race -count=1 -timeout=30m \
  -tags 'goolm stdjson' ./pkg/earning
GOOS=windows GOARCH=amd64 CGO_ENABLED=0 GOWORK=off \
  go test -exec=/bin/true -tags 'goolm stdjson' ./...
GOOS=darwin GOARCH=arm64 CGO_ENABLED=0 GOWORK=off \
  go test -exec=/bin/true -tags 'goolm stdjson' ./...
```

The schema generator produced SHA-256
`5c7780a6084c5a630122541128001097a97ae42a3086a4f0085fc4b2bc9d12eb`.
The fixture generator produced SHA-256
`d6012dc69d8e99a2e313b889baafde2b8903e183a9d26a3ea46cdf3de0d49459`.
Both generated files were byte-identical to their committed artifacts. The
Python verifier independently reproduced the released registry, deterministic
CBOR digest, state, and Semantic Action fixture checks.

## 6. Deliberate exclusions and remaining gates

This implementation does not claim the following:

- specification freeze or final profile-wide conformance;
- public-network deployment, independent Carrier failure domains, or legal
  guarantee enforceability;
- a concrete `collateral-attested` custody Adapter with current finality and
  reorganization evidence;
- an `independently-enforceable` operation Adapter or TOS application vault;
- automatic CLI construction of a Provider's signer, underwriting policy,
  historical authority proofs, Decision Authority, or payment Adapter;
- a public-network multi-party campaign covering Provider loss, Carrier loss,
  partial claims, multiple payouts, and residual collateral release; or
- exhaustive code-independent verification of every positive and negative
  object vector required by the final profile-wide release gate.

The protocol types and verification boundaries for collateral are present,
but an assurance tuple remains disabled until its exact owner-approved Adapter
and authority dependencies are installed and independently tested. The
`independently-enforceable` tuple is explicitly rejected by the local Provider
coordinator because its defining property requires an external operation
authority that remains usable after the Provider is unavailable.

## 7. Deployment decision

The code is suitable for integration and further audit as a fail-closed
`unsecured-signed` Provider SDK/runtime candidate. It must not advertise full
Agent Guarantor V1 conformance while the profile remains pre-freeze. Operators
must keep all Guarantor side effects disabled unless they explicitly assemble
the runtime with current owner authority, bounded underwriting, durable
journals, authenticated Messenger transport, and a verified payment Adapter.
