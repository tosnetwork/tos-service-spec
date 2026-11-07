# Native Agent Identity V1

## Controller policy

An Agent is controlled by a bounded weighted ML-DSA-44 policy of 1 to 8
controllers. Each controller declares its key ID (`NATIVE_IDENTIFIERS_V1.md`),
its 1,312-byte ML-DSA-44 public key, positive weight, allowed purposes, and
whether it may participate in recovery. The policy declares ordinary and
recovery thresholds plus a recovery timelock. ML-DSA-44 is the only admitted
controller suite; there are no mixed-suite policies.

Policies are encoded in strictly ascending key-ID order. Controllers may be isolated by
purpose so a delegation key need not control Agent policy or Capabilities. The
eligible weight for Agent control, delegation, and Capability control must each
independently reach the ordinary threshold. Recovery is an opt-in subset whose
purpose bit must exactly match its recovery designation, and its eligible
weight must reach the recovery threshold. Weights from different purposes are
never pooled. Unknown purposes and duplicate keys are invalid.

## Signature semantics

Controllers sign with Pure ML-DSA-44 (FIPS 204, no pre-hash) over the 32 raw
bytes of the canonical TVM action-cell hash, with the context string
`TOS-NATIVE-REGISTRY` (19 bytes). Signature sets hold at most 8 entries in
strictly ascending key-ID order. Each key contributes weight at most once.
Verification binds the signature to protocol, network, target object, registry
code, ordering, predecessor, nonce, and payload.

ML-DSA-44 signing may be hedged (randomized), so two valid signature sets for
one action can differ byte for byte. A registry operation is therefore
identified by its action hash, never by signature bytes: two valid signature
sets for one action produce exactly one state transition, and the contract
accepts a resubmission of the already-applied last action as a replay. Frozen
vectors use the FIPS 204 deterministic variant (all-zero randomness) and
record signatures as data.

A policy submitted for installation (registration, policy update, recovery
initiation) is admitted once: its shape is checked, every controller of the
installed policy must provide a possession signature over the action in
key-ID order, and each declared key ID must equal the ID derived from the key
that signature verified against. This prevents unusable or attacker-selected
public keys from silently contributing to future thresholds. A stored policy is
not re-validated; recovery completion promotes the pending policy exactly as it
was admitted at initiation.

## Purposes

The contract distinguishes exactly:

- Agent control, including registration, policy update, and revocation;
- delegation;
- Capability control, including transfer acceptance; and
- recovery.

An implementation must use the exact purpose constants frozen by the TVM and
canonical-cell specification. A signature valid for one purpose is not
implicitly valid for another.

## Recovery

Recovery is a two-step timelocked operation. Initiation stores the proposed
policy, execution time, initiating action hash, and initiating live-policy
hash. Completion must reference that exact initiation, occur after the
timelock, and prove that the live policy still has the initiating hash. Any
policy replacement clears pending recovery so an old proposal cannot overwrite
a newer policy. Non-policy mutations remain in the typed-state predecessor
chain and do not cancel recovery.

Recovery completion advances the Agent generation and resets sequence to `1`,
but its predecessor remains the nonzero hash of the immediately preceding
typed state. Clients must resolve the resulting state before building further
actions.

## Delegations

An Agent may commit bounded delegation digests. The registry stores only the
immutable digest; the delegation document remains off-chain. Consumers must
verify its bytes, scope, expiry, and intended use against the digest and current
Agent state.

## Revocation

Agent revocation is a terminal tombstone. A revoked Agent cannot authorize its
own updates or Capability operations. Capability discovery must report an
owner Agent tombstone as unusable even if the Capability account itself remains
unchanged.

## Key custody

Private controller keys remain in the client wallet or dedicated signer. In
the reference implementation, ML-DSA-44 controller keys stay in `tosctl`
custody (vault): `tos-service-protocol` calls `tosctl` for ML-DSA-44 signing
and verification rather than linking a Go ML-DSA library, and no private key
leaves custody.
Gateways, relayers, indexers, providers, and workers receive only public policy,
canonical action details, and required signatures.
