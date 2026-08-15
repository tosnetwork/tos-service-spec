# Native Registry Internal Security Review

**Review date:** 2026-08-14
**Protocol:** `tos_service_v1`
**Reviewed code hash:**
`tvm-cell-sha256:600f2fda83462bc86a1c32af930c35a4fc8f80f1d2966f5593ceba217a91ffa0`

The incremental independent review evaluated the previous artifact with code
hash
`tvm-cell-sha256:189c292404fe59293001c70ec568d8d38cd938d8bef92c7867e3268000808d1f`.
It and the still earlier
`tvm-cell-sha256:c4af55e476c296c8a1dc7985e82db42218475b9e3864b7c733351bab526ab23d`
artifact are superseded and must not be deployed.

## Scope and conclusion

This review covered the canonical action and identity encoder in
`tos-service-protocol/pkg/nativecore`, the independent conformance encoder, finalized
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
body cell hash, and optional StateInit cell hash. `tos-service-protocol` recomputes and
matches every field before broadcast. The Native wallet tool embeds the entire
validated `NativeActionV1` in its review and always requires the exact action
hash to be typed. There is no generic confirmation bypass.

### NR-04 — Contract export could consume stale generated Fift

**Severity:** Medium
**Status:** Closed

The old export helper loaded an ignored `auto/` file, so a source change did not
guarantee that the exported BOC came from that source. The release build now
compiles the canonical FunC source directly, checks the code hash, container
digest, and size, and compares two independent builds with the frozen Base64
artifact.

The obsolete complex contract and the temporary `native-registry-v2` naming
were removed. There is one canonical TOS Native Service Registry source.

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

## Independent audit remediation

The independent audit in
`memo/native-registry-security-audit-2026-08-14` reviewed superseded commits and
reported nine findings. Its portable eight-assertion adversarial harness now
has seven assertions passing unchanged against the remediated source. The
eighth, legacy duplicate-relay assertion constructs a relayer without the now
mandatory durable journal and finalized resolver, so it fails closed before
broadcast rather than exercising its old in-memory setup. The equivalent
durable duplicate, restart, conflict, and two-process race cases pass in the
remediated test suite. In addition to generation reset, this remediation
provides:

- a durable, process-independent idempotency journal written before broadcast,
  conflict rejection, terminal replay, read-only ambiguous-result recovery,
  and no blind rebroadcast;
- fail-closed code binding, registration proof, signature, and finalized live
  policy preflight before relay funds are spent;
- purpose-isolated controllers with independently reachable Agent-control,
  delegation, Capability-control, and recovery thresholds in Go and FunC;
- a durable monotonic finalized-checkpoint fence committed only after the
  complete observation validates;
- strict zero-hash, zero-owner, printable minimal-snake, and single-root BOC
  decoding;
- complete signed-action wallet review with no generic `--yes`; and
- one canonical frozen BOC consumed by release and CMake embedding paths.

The remediation also found a compiler-level enforcement hazard while adding
the TVM regression tests: FunC validation helpers whose result was discarded
could be optimized away unless declared `impure`. Every throwing validation
and signature helper is now explicitly `impure`, and the negative TVM tests
are executed against the newly frozen BOC. Source-only inspection is not
accepted as evidence for these guards.

These are internal remediation results, not an independent audit pass. Gate B
still requires the independent reviewer to retest the new commits and frozen
code hash, as well as execute the complete TVM lifecycle matrix.

## Incremental independent review remediation

The incremental review evaluated `tos` commit
`53a3a796161bdb4e21714c1aa497a01ec5de666c`, `tos-service-protocol` commit
`fd165aeabbf128b4c3ae887008fb3b8e75bde44b`, and `tos-service-spec` commit
`7b9ebca793a85211d804f0cfad35281e40d69901`. It found one P1, two P2, and two
P3 issues. The internal remediation closes them as follows:

- request idempotency keys are aliases to a separate process-independent
  canonical action claim, preventing the same signed action from buying a
  second broadcast under a fresh key;
- query IDs derive from canonical action identity, and every exact outbound
  field remains bound by the action record;
- forbidden counterparty signature sets fail before journaling or payment;
- purpose-specific least privilege is restored while each purpose threshold
  remains independently reachable;
- frozen-BOC decoding uses Python's cross-platform strict Base64 decoder; and
- Roadmap evidence names the exact commits reviewed.

The fresh-key replay and forbidden-counterparty adversarial cases now pass
internally. This section does not close the independent review: the reviewer
must retest the remediation commits and the new frozen artifact, and Gate B
still requires the complete Agent and Capability TVM lifecycle matrix.

## State-slot fee-spend remediation

The next incremental independent review evaluated `tos-service-spec` commit
`fd92cb921b1be1bef0db718908d3744b13694448`, `tos` commit
`37a27f8fb09e577412b922d5b0138c4b7fc91e58`, and `tos-service-protocol` commit
`6dff78ce53347e92565769ad32947fa8b9eef55b`. It confirmed all five preceding
findings closed but found one new P1: exact-action deduplication allowed an
authorized caller to vary the nonce and make a relayer pay for multiple
mutually exclusive actions occupying one on-chain ordering position.

The internal remediation replaces action identity as the fee-spend boundary
with a durable state-slot claim over network, code, target object, generation,
sequence, and predecessor. The action identity remains the exact signed intent
inside that slot. Before claiming it, the relayer now proves authoritative
finalized absence for registration or exact live target continuity for a
mutation, including Capability owner, terminal, and immutable-version state.
The claim transaction also enforces persistent time-window action and nanoTOS
ceilings per target and relay wallet. Concurrent nonce variants, stale or
already-existing targets, and restart-surviving budget exhaustion are covered
by adversarial tests and fail before paid broadcast.

This is internal remediation, not audit closure. Gate B remains blocked until
the independent reviewer reruns the nonce-variant exploit, concurrent slot and
budget cases, full Agent/Capability target-state preflight, and the complete
TVM lifecycle matrix against the remediation commit.

## Atomic slot-intent crash recovery

The following incremental independent review evaluated `tos-service-spec` commit
`61ad4851e7c5fd398f6064fd8e13c860921e6d49`, `tos` commit
`c4814f3edb539888c5b333ab9a10c1164259964a`, and `tos-service-protocol` commit
`b649927a3ceb3178bd95a611185c5bf1b1d3e782`. It confirmed the state-slot P1
closed and found one P2 recovery failure: a crash after the slot file was
created but before the separate action-intent file was created permanently
classified a transition that had never entered the sender as ambiguous.

The internal remediation removes the separate action record. One atomically
created slot record now contains the state-slot identity, action identity,
complete outbound intent, claim time, and a durable `prepared` phase. A second
atomic operation under the cross-process journal lock grants exactly one
broadcast lease by changing `prepared` to `broadcasting`; sender acceptance
changes it to `complete`. A restarted `prepared` record can obtain a new lease,
whereas `broadcasting` remains read-only and cannot buy another send. Budget
accounting reads the same unified record.

Fault-injection tests cover restart after prepare, restart while broadcasting,
completion recovery, and concurrent lease acquisition. This remains internal
remediation. Gate B stays blocked until independent retest and the complete
Agent/Capability TVM lifecycle matrix both pass.

## Finalized chain-time recovery preflight

The next incremental independent review evaluated `tos-service-spec` commit
`6bcc655cee1784491d6b4cbd5a36019f0f1768e1`, `tos` commit
`65ac8f9f0e1b910916b27ec3890b5611d80579e6`, and `tos-service-protocol` commit
`5e0841b9db4a496af5c292032899fa52631437a5`. It confirmed atomic slot-intent
recovery closed the preceding P2 and found one new P2: recovery initiation and
completion preflight used gateway wall-clock time while the contract evaluates
the same conditions with chain `now()`. A boundary action could therefore buy
a broadcast, fail after ordinary inclusion delay, and leave its sole state slot
ambiguous.

The internal remediation makes the relayer require a chain-authored unix time
from the same quorum-finalized observation as the target-state read. Recovery
completion cannot enter the journal until that time reaches the stored
execution time. Initiation additionally requires a mandatory deployment safety
margin of 300 through 86400 seconds on top of the live policy timelock. Missing,
zero, stale, future, inconsistent, or unavailable finalized time fails before
the slot claim and fee spend. Observation freshness is checked inside each
state resolution rather than delegated to an earlier readiness probe. Gateway
time remains usable only for freshness rejection and the conservative relay
budget window; it cannot authorize a contract timelock.

Regression tests put gateway time both ahead of and behind chain time and cover
the exact initiation and completion boundaries. This remains internal
remediation. Gate B stays blocked until independent retest and the complete
Agent/Capability TVM lifecycle matrix both pass.

## Internal full-lifecycle emulator matrix

The internal Gate B matrix now executes the frozen Registry BOC in the Rust
TVM sandbox at global version 14. It covers:

- Agent registration, exact replay, policy replacement with proof of
  possession, delegation, recovery initiation, recovery after an intervening
  delegation, generation-reset completion, superseded and invalidated
  recovery, terminal revocation, and post-tombstone rejection;
- caller-selected identity, stale and zero predecessor, skipped sequence,
  wrong target, wrong network, forbidden signature shape, invalid signer,
  unreachable purpose threshold, and early timelock rejection, with unchanged
  state on every failure;
- Capability registration, version addition, irreversible version revocation,
  duplicate-version rejection, two-policy ownership transfer, former-owner
  rejection, direct forged forwarding rejection, rejection by either transfer
  policy, terminal revocation, and unchanged ownership after every failed
  transfer; and
- relayer journal restart from `prepared`, non-rebroadcast from
  `broadcasting`, durable completion, conflicting-intent fencing, concurrent
  broadcast-lease exclusion, and restart-surviving spend budgets.

The matrix exposed that the Rust emulator lacked the TOS v14 `SHA256C` opcode
used by the frozen contract even though the C++ TVM already implemented it.
The Rust VM and assembler now implement opcode `0xf903` with the same version
gate, canonical snake bounds, chunk-independent SHA-256 result, and malformed
cell rejection. The sandbox uses an explicit pre-activation global-version
configuration; ordinary defaults remain at the Rust implementation's declared
supported version. Consequently, public deployment is invalid on any network
whose finalized ConfigParam 8 remains below version 14.

Run the TVM evidence with:

```text
tos/scripts/test-tos-service-registry-tvm-lifecycle.sh
```

Run the crash-boundary evidence from `tos-service-protocol` with:

```text
go test ./pkg/nativecore -race -count=20 \
  -run 'TestFileRelayJournal|TestRelayerResolvesAmbiguousIntentWithoutRebroadcast'
```

These results are internal evidence only. The independent reviewer must run
the same matrix from clean checkouts and publish exact commits, tool versions,
and results before the independent Gate B item becomes complete.

## Verified invariants

- Agent and Capability registration identities are derived, not selected by a
  caller.
- All actions bind network genesis, network ID hash, target code hash, target
  object, ordering, predecessor, nonce, and typed payload.
- Controller and signature sets are bounded and strictly ordered.
- Purpose-specific controllers preserve least privilege; each normal purpose
  independently reaches the ordinary threshold and cross-purpose weights are
  never pooled.
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
- Relay intent and finalized high-water state survive process restart.

## Frozen evidence

- Normative vector:
  `test-vectors/tos-service-v1-registry.json`
- Primary implementation: `tos-service-protocol/pkg/nativecore`
- Independent implementation: `tos-service-protocol/internal/referencecodec`
- Stable error range: `2200` through `2213`, shared with TVM exit codes
- Contract release manifest:
  `tos/crypto/smartcont/tos-service-registry-v1.release.json`
- Reproducible build test: `tos/scripts/test-tos-service-registry-v1.sh`
- Executable recovery lifecycle:
  `tos/tosctl/src/node-control/contracts/tests/native_registry_sandbox.rs`
- TVM lifecycle entry point:
  `tos/scripts/test-tos-service-registry-tvm-lifecycle.sh`
- Version-gated `SHA256C` conformance:
  `tos/tosctl/src/vm/tests/test_sha256c.rs`

StateInit and action identities are frozen by TVM cell hash. A BOC container
may legally use a different topological cell ordering while representing the
same cell DAG, so a container byte digest is frozen only for the published code
artifact, not used as a consensus identity.

## Final independent review — 2026-08-14

The independent reviewer evaluated `tos-service-spec` commit
`e72bab245a47b0f87a82977629cc03b1dfc64995`, `tos` commit
`a787cb02dd6bc386be053ab233d0581cc1a14ef3`, and `tos-service-protocol` commit
`7a21c070c1160fc0a4278e1a086c0682eb2d3d31`. The review reproduced the
ten-test Agent and Capability TVM lifecycle matrix and retested the chain-time
recovery preflight, atomic slot-intent record, and broadcast lease. It reported
no P0, P1, or P2 finding and accepted the Gate B remediation baseline.

This closes Gate B for the exact frozen release and commits above. It does not
pre-authorize later consensus, contract, action-encoding, authorization,
relayer-journal, or resolver changes.

## Independent review requirements for a new release

A new release that changes any security-sensitive behavior must again have an
independent reviewer, who must at minimum:

1. reproduce the code BOC and code hash from a clean toolchain;
2. reproduce every positive and negative frozen vector without importing
   `nativecore`;
3. execute the complete Agent and Capability lifecycle in a TVM emulator;
4. attempt sender, network, code-hash, address, predecessor, ordering,
   signature, policy, replay, recovery, immutable-version, and transfer races;
5. confirm every failure leaves canonical state unchanged; and
6. publish findings, tool versions, test corpus, and the exact reviewed commit.
