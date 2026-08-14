# Native Agent Identity V1

## Controller policy

An Agent is controlled by a bounded weighted Ed25519 policy. Each controller
declares key ID, public key, positive weight, allowed purposes, and whether it
may participate in recovery. The policy declares ordinary and recovery
thresholds plus a recovery timelock.

Policies are encoded in canonical key order. Every threshold must be reachable
using distinct eligible controllers. Unknown purposes and duplicate keys are
invalid.

## Signature semantics

Controllers sign the canonical TVM action-cell hash. Signatures are sorted by
key identity. Each key contributes weight at most once. Verification binds the
signature to protocol, network, target object, registry code, ordering,
predecessor, nonce, and payload.

Policy changes and recovery proposals require proof of possession from every
key being installed. This prevents unusable or attacker-selected public keys
from silently contributing to future thresholds.

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

Private controller keys remain in the client wallet or dedicated signer.
Gateways, relayers, indexers, providers, and workers receive only public policy,
canonical action details, and required signatures.
