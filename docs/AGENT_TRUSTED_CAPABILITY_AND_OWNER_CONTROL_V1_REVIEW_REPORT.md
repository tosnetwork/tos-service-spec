# Agent Trusted Capability and Owner Control V1 Review Report

**Review date:** 2026-08-28

**Reviewed profile:**
[Agent Trusted Capability and Owner Control V1](AGENT_TRUSTED_CAPABILITY_AND_OWNER_CONTROL_V1.md)

**Source route:**
[OpenFox PR #16](https://github.com/tosnetwork/openfox/pull/16), merged as
`a2ee8bb89ce41aed7cd8835755ca1388d30e796f`

**Method:** eleven sequential, read-only Codex CLI reviews. Each of rounds
1--10 used a different threat-model focus. The specification was edited after
each review to resolve its findings. Round 11 reviewed the resulting complete
diff and served as a regression confirmation. Codex did not edit the files.

**Tool:** Codex CLI `0.150.1`, default configured Codex model. The review was
performed against the local repository and its referenced specifications.

## 1. Final disposition

`PASS` for design review: after the tenth remediation, the eleventh review
reported no actionable P0 or P1 design flaw.

This is not a release or implementation acceptance. The profile remains a
design candidate, Phase 0 is not started, Gates S/M have not passed, and every
new consequential path remains disabled until the required schemas, registries,
vectors, independent verifier, production implementation, and gate evidence
exist.

## 2. Review and remediation ledger

| Round | Review focus | Principal findings | Applied remediation |
|---:|---|---|---|
| 1 | Architecture, authority and scope | Initial authority objects lacked authenticated roots; global revocation claim was unimplementable; remote MCP identity overstated; installation had no transaction; application profiles blurred portable scope | Added detached authority evidence and bootstrap, bounded cross-host leases, observed-remote-service semantics, transactional installation, and explicit portable/application boundaries |
| 2 | Canonical bytes, digests and identity | Permission/artifact digest cycle; incomplete authorization preimage and predecessor chain; implicit common fields; mutable evidence references; unregistered IDs/actions | Added the canonical CBOR wrapper and digest formula, immutable references, ID registry, exact authorization envelope/signature preimage, linear CAS chains, and mandatory vectors |
| 3 | Skill/MCP supply chain | Publisher identity was unauthenticated; dependencies and quarantine were underspecified; environment denylist leaked authority; remote drift and network permissions were weak | Added publisher envelopes, complete dependency closure, non-executing safe unpack, empty-by-default environment, authenticated remote generations, and typed network/credential capabilities |
| 4 | Admission, promotion and revocation | Promotion was absent from leases; policy identity and takeover fencing were incomplete; drain semantics were broad; evaluation evidence could be fabricated; time rollback and fork denial were possible | Added dual authority heads in leases, digest-bound owner policy, authority epochs, bounded drain leases, verifier-authorized evaluation results, trusted-time high-waters, and deterministic recovery |
| 5 | Owner commands and mobile control | Bootstrap/enrollment lacked PoP state machines; session and sink takeover were not fenced; ambiguous cross-device retry could duplicate effects; confirmation, pause, notifications, and exit were incomplete | Added bootstrap/recovery and enrollment/session objects, command leases and sink deduplication, semantic confirmation, scope generations, untrusted notification rules, and staged owner exit |
| 6 | Reports, projection and privacy | Accounting cutoff and source completeness were ambiguous; report corrections and projection chains could fork; cache/deletion, multi-tenant isolation, hidden-test secrecy, and rendered disclaimers were weak | Added deterministic accounting and coverage manifests, report-series CAS, contiguous projection snapshots, AEAD cache/privacy policy, tenant isolation, hidden-evaluation secrecy, and mandatory non-authoritative rendering |
| 7 | Migration and compatibility | Legacy processes could survive cutover; old binaries could bypass new state; migration was non-atomic; mixed endpoints, optional profiles, and artifact deletion allowed downgrade/resurrection | Added global legacy fencing, resumable Inventory migration, deployment-format and feature epochs, authenticated negotiation, permanent old-path shutdown, registry-fixed criticality, and durable deletion tombstones |
| 8 | Cross-repository ownership and status | PR evidence was not immutable; independent verifier ownership contradicted the roadmap; mobile/API owners were unnamed; controlling roadmap omitted the candidate | Pinned PR/commit evidence, separated reference and production verifiers, named server/Web/future mobile ownership and APIs, moved the index category, and added the blocked incubation status to `docs/ROADMAP.md` |
| 9 | Gates and campaign evidence | Campaigns 1--5 lacked complete executable thresholds; independence and pre-registration were undefined; Gate S/M samples were weak; external revenue and claims could be self-certified | Added gate-wide pre-registration, two-of-two organizational independence, clean-room reproduction, claim registry, stronger Gate S/M matrices, Campaign 1--6 thresholds, and arm's-length profitability rules |
| 10 | Holistic adversarial trace | Dependency introduced a second digest cycle; promotion lacked signed-result binding/mutation; command retry still mixed effect and session; use binding omitted authority fields; migration lacked distributed completion | Introduced a pre-manifest digest, promotion result references and mutation, effect/authorization-attempt split, exhaustive use binding, and sink-membership/expiry cutover predicate |
| 11 | Final regression confirmation | No actionable P0/P1 remained | No further design change required; final result `PASS` |

## 3. Review-output integrity

The raw final responses were retained during the work session. Their byte sizes
and SHA-256 digests were:

| Round | Bytes | SHA-256 |
|---:|---:|---|
| 1 | 6,139 | `1e335ec3774f34f9152f5d90062a2197c7e98631b9f09d7c62a94a8cceb9a83b` |
| 2 | 11,500 | `055b35c0f90f0223bc95708d05279776fafa73ef95521094b23b66a110049de2` |
| 3 | 7,346 | `222cc9484fc49fa9184d3158a8e09f92134fda8335a66fc73db40227944de694` |
| 4 | 6,865 | `f6e9ebfc93105b7761ac3e21b8e553bb1b218dfc842819434623db306c529269` |
| 5 | 9,598 | `32bd80dca154a28ce3e37d1568d155026c844dd5db5ae26d2e76676d081ba9d7` |
| 6 | 6,590 | `42de2d13ef29685c61405553bcde047da75a3d9d1625407c99d1208aac326a77` |
| 7 | 7,338 | `58d9f70728fc7582e12fd79cd25bd8206b8d63228e76a5f16d6bbf749fc07714` |
| 8 | 4,613 | `dcf6d5dd1eb15428f54612b22ed8554049a6cc235117b847cfb5bb1b96ab05d1` |
| 9 | 9,065 | `7a1471852b6aa18980f035ce4b640b87944935adb9bc9ec2c49a6e5176612014` |
| 10 | 5,703 | `413109bfa5a3a0a45681fa1e4a840ea8be0571a4099a032bcc32c662a93270cc` |
| 11 | 1,056 | `e286f8a2df22aef82eea1341df20991f1f3d5ebb4920dbda54993c8763d7b5e9` |

These hashes document the review session; the normative deliverable is the
remediated specification and its repository diff.

## 4. Closed design invariants

The final review specifically confirmed:

- authenticated, predecessor-bound authority chains with CAS and epoch fencing;
- cycle-free, deterministic artifact, permission, and dependency identities;
- stable command-effect identity with replaceable authorization evidence;
- exact execution binding across admission, promotion, lease, environment,
  remote session, loaded handles, and pause/revocation generations;
- distributed migration fencing and fail-closed mixed-version behavior;
- explicit design-candidate status and no accidental production claim; and
- pre-registered, independently reproduced, bounded acceptance evidence.

## 5. Remaining implementation gates

No design-review PASS can substitute for implementation. Release remains
blocked until every artifact in Section 24 of the profile exists and two
independent implementations reproduce the canonical corpus. Gate S, Gate M,
formal Campaigns 1--5, and arm's-length Campaign 6 remain future evidence.
