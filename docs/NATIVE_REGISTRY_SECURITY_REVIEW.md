# Native Registry Internal Security Review

**Review date:** 2026-08-14
**Protocol:** `atos_native_v1`
**Reviewed code hash:**
`tvm-cell-sha256:943c6cb3ddfeb470cfb76a343a29471ffbced9af25a467fde834926c1a8d525d`

The previous reviewed artifact had code hash
`tvm-cell-sha256:c4af55e476c296c8a1dc7985e82db42218475b9e3864b7c733351bab526ab23d`.
It is superseded and must not be deployed.

## Scope and conclusion

This review covered the canonical action and identity encoder in
`tos-protocol/pkg/nativecore`, the independent conformance encoder, finalized
state resolution, the wallet sender boundary, and the Native Registry FunC
contract in `tos/crypto/smartcont/native-registry-code.fc`.

Six implementation findings were corrected. The corrected source builds
reproducibly to the frozen code hash and both registry encoders reproduce the
Agent and Capability identifiers, contract addresses, action hashes, action
BOCs, and frozen negative results.

This is an internal engineering security review. It does not satisfy the
ROADMAP requirement for an independent auditor with no implementation role.
No public deployment should be described as audited until that separate review
is complete.

## Findings closed

### NR-01 — Capability text was not bounded by the contract

**Severity:** High
**Status:** Closed

The Go encoder limited a Capability version to 128 printable ASCII bytes, but
the contract previously accepted any snake-cell tree whose SHA-256 matched the
declared version hash. A manually constructed signed action could therefore
consume unbounded traversal gas or store a representation that a conforming
client would never create.

The contract now enforces non-empty printable ASCII, a maximum of 128 bytes,
byte alignment, at most one continuation reference, and a full 127-byte chunk
for every non-final snake cell. Registration, version addition, and version
revocation all apply the same check.

### NR-02 — Client ordering and zero-identifier checks lagged the contract

**Severity:** Medium
**Status:** Closed

`nativecore` previously allowed zero generation or sequence in some action
shapes and did not reject a syntactically valid all-zero object ID at the
generic identifier boundary. The contract rejected those actions, so this did
not permit an unauthorized transition, but it could cause avoidable fee loss
and inconsistent preflight results.

The encoder now rejects zero identifiers, zero ordering values, non-`1/1`
registration ordering, and zero registration object nonces before signing or
relay.

### NR-03 — Prepared wallet BOC lacked semantic confirmation

**Severity:** Medium
**Status:** Closed

The sender pinned the `tosctl` binary and verified the returned wallet-message
BOC digest, but the build response did not bind the operator-visible
destination, amount, body, and StateInit semantics. A signing boundary must
confirm those values, not only opaque bytes.

The prepared-send response now includes destination, exact nanoTOS amount,
body cell hash, and optional StateInit cell hash. `tos-protocol` recomputes and
matches every field before broadcast. The Native wallet tool also displays the
complete semantic review and requires the exact action hash to be typed unless
an explicit non-interactive flag is supplied.

### NR-04 — Contract export could consume stale generated Fift

**Severity:** Medium
**Status:** Closed

The old export helper loaded an ignored `auto/` file, so a source change did not
guarantee that the exported BOC came from that source. The release build now
compiles the canonical FunC source directly, checks the code hash, container
digest, and size, and compares two independent builds with the frozen Base64
artifact.

The obsolete complex contract and the temporary `native-registry-v2` naming
were removed. There is one canonical ATOS Native Registry source.

### NR-05 — The protocol encoder rejected canonical generation resets

**Severity:** High
**Status:** Closed

The protocol encoder previously treated `sequence == 1` as equivalent to a
zero predecessor. That is valid only for registration. Recovery completion and
Capability transfer reset sequence because they start a new generation, but
they must still commit to the immediately preceding live state. As a result,
the SDK could not construct a transition that the contract required.

Registration now uniquely requires generation `1`, sequence `1`, and a zero
predecessor. Every mutation requires a nonzero predecessor. Recovery completion
and Capability transfer require a reset sequence of `1`; the contract remains
responsible for proving the exact generation increment and predecessor match
against live state. Go regression tests and an offline TVM recovery lifecycle
exercise this boundary.

### NR-06 — Pending recovery lacked an explicit initiating-policy binding

**Severity:** High
**Status:** Closed

Recovery is authority delegation across time. Its validity must therefore be a
function of the authority state that created it, rather than merely the passage
of time. Pending recovery now stores the initiating live-policy cell hash.
Completion fails closed unless that hash equals the current policy hash, and a
policy replacement clears the pending proposal. Non-policy mutations preserve
it but remain covered by the ordinary predecessor chain.

The typed-state decoder independently validates the same binding. Offline TVM
tests prove both required paths: initiation followed by delegation and
generation-reset completion succeeds, while initiation followed by policy
replacement makes completion fail without changing state.

## Verified invariants

- Agent and Capability registration identities are derived, not selected by a
  caller.
- All actions bind network genesis, network ID hash, target code hash, target
  object, ordering, predecessor, nonce, and typed payload.
- Controller and signature sets are bounded and strictly ordered.
- New controller policies require proof of possession.
- Registration alone uses a zero predecessor; generation resets retain the
  immediate nonzero state predecessor.
- Pending recovery is bound to its initiating policy, is invalidated by policy
  replacement, and cannot bypass intervening state transitions.
- Capability authorization traverses the live owner Agent policy.
- Capability transfer commits only once in the Capability account after both
  owner policies authorize the unchanged action.
- Failed or stale forwarded messages cannot create a pending, dual-owner, or
  ownerless state.
- Typed TVM state is decoded only after endpoint quorum, finality, network,
  account code, transaction tuple, and state checks.
- Portable CBOR is produced only after typed-state decoding.
- Relayer acknowledgement is not treated as transition finality.

## Frozen evidence

- Normative vector:
  `test-vectors/atos-native-v1-registry.json`
- Primary implementation: `tos-protocol/pkg/nativecore`
- Independent implementation: `tos-protocol/internal/referencecodec`
- Stable error range: `2200` through `2213`, shared with TVM exit codes
- Contract release manifest:
  `tos/crypto/smartcont/atos-native-registry-v1.release.json`
- Reproducible build test: `tos/scripts/test-atos-native-registry-v1.sh`
- Executable recovery lifecycle:
  `tos/tosctl/src/node-control/contracts/tests/native_registry_sandbox.rs`

StateInit and action identities are frozen by TVM cell hash. A BOC container
may legally use a different topological cell ordering while representing the
same cell DAG, so a container byte digest is frozen only for the published code
artifact, not used as a consensus identity.

## Independent review requirements

The independent reviewer must, at minimum:

1. reproduce the code BOC and code hash from a clean toolchain;
2. reproduce every positive and negative frozen vector without importing
   `nativecore`;
3. execute the complete Agent and Capability lifecycle in a TVM emulator;
4. attempt sender, network, code-hash, address, predecessor, ordering,
   signature, policy, replay, recovery, immutable-version, and transfer races;
5. confirm every failure leaves canonical state unchanged; and
6. publish findings, tool versions, test corpus, and the exact reviewed commit.
