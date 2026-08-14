# Native Registry State Machines

**Normative authority:** Agent and Capability contract transitions

**Protocol:** `atos_native_v1`

## 1. Common transition envelope

Every action commits to:

- exact protocol identifier;
- complete TOS network domain;
- target object ID;
- target contract code hash;
- generation and sequence;
- predecessor typed-state hash;
- nonce; and
- exactly one typed payload.

The TVM action cell is canonical. Its cell hash is the action hash signed by
controllers. Callers do not provide an action hash or intended result state.

For a new object, generation and sequence are both `1` and the predecessor is
zero. Every existing-object mutation, including a generation-reset mutation,
commits to the nonzero hash of the immediately preceding typed state. For an
ordinary mutation, generation is unchanged and sequence increases by one.
Recovery completion and Capability ownership transfer advance generation and
reset sequence to `1`; sequence reset never resets or omits the predecessor.

Exact replay of the last finalized action is idempotent. Reuse of the same
ordering position for different content is rejected.

## 2. Agent state

Canonical Agent state contains only:

- Agent ID;
- generation and sequence;
- last action hash;
- current controller policy;
- delegation digests;
- optional pending recovery time, initiating action hash, initiating policy
  hash, and new policy; and
- tombstone flag.

### Register Agent

The Agent ID is derived from network domain, object nonce, and canonical
initial policy. The caller-supplied target must equal the derived ID. Every key
in the initial policy proves possession by signing the registration action.

### Update policy

The current policy authorizes the action using the Agent-control purpose.
Every key in the new policy proves possession. Installation replaces the policy
atomically and clears pending recovery state.

### Add delegation

The current policy authorizes a nonzero delegation digest. Delegation digests
are immutable and unique within the bounded Agent state.

### Initiate recovery

Recovery-designated controllers satisfy the recovery threshold. The execution
time must respect the current recovery timelock. Every key in the proposed
policy proves possession. The contract stores the initiating action hash,
execution time, and proposed policy.

### Complete recovery

The action references the pending initiation, is submitted after the timelock,
and satisfies the recovery authorization rule. The stored initiating-policy
hash must still equal the live policy hash. Completion installs the stored
policy, clears recovery state, advances generation, and resets sequence while
retaining the immediately preceding typed-state hash as its predecessor.

Any policy replacement clears pending recovery. Mutations that do not replace
policy, such as adding a delegation, do not invalidate it: they are committed
by the completion action's immediate predecessor and cannot be skipped or
reordered. A later recovery initiation replaces the earlier pending proposal.

### Revoke Agent

The current policy authorizes a terminal tombstone. A tombstoned Agent cannot
authorize Capability operations or later Agent mutations.

## 3. Controller policy

A policy is a bounded, canonically ordered set of Ed25519 controllers. Each
controller contains:

- key ID exactly `ed25519:<lowercase-public-key-hex>`;
- the matching 32-byte public key;
- positive weight;
- purpose bitmask; and
- recovery designation.

The policy contains action and recovery thresholds plus recovery timelock.
Duplicate keys, inconsistent key IDs, unsupported purposes, zero weights,
unreachable thresholds, excessive counts, and trailing cell data are rejected.

Authorization sums each distinct valid signer once. The contract validates the
purpose and current live policy; gateways do not calculate authoritative
permission.

## 4. Capability state

Canonical Capability state contains only:

- Capability ID;
- generation and sequence;
- last action hash;
- current owner Agent ID;
- immutable bounded version map containing version string, manifest digest,
  and revocation bit; and
- tombstone flag.

It does not copy the owner's controller policy. Capability authorization always
passes through the current owner Agent account and therefore uses live policy.

### Register Capability

The Capability ID is derived from network domain, object nonce, owner Agent ID,
initial version string, and manifest digest. The target must equal the derived
ID. The owner Agent validates its current policy before forwarding the action
to the deterministic Capability account.

### Add version

The current owner Agent authorizes the action. The version string and manifest
digest are nonempty and canonical. A version key is immutable and cannot be
overwritten, including after revocation.

### Revoke version

The current owner Agent authorizes setting one existing version's revocation
bit. Revocation is irreversible.

### Revoke Capability

An empty version selector requests a terminal Capability tombstone. The current
owner Agent authorizes it. No later mutation is accepted.

### Transfer Capability

Transfer must be atomic and uses a no-state authorization path:

1. The relayer sends the signed action to the current owner Agent.
2. The current owner Agent validates its live policy and forwards unchanged
   action bytes and signatures to the new owner Agent.
3. The new owner Agent validates that the sender is the deterministic current
   owner Agent, validates its own live acceptance signatures, and forwards the
   unchanged action to the Capability account.
4. The Capability verifies the sender is the deterministic new owner Agent and
   changes `owner_agent_id` in its single committed transition.

The intermediate Agent calls do not alter Agent state. Failure at either Agent
leaves Capability ownership unchanged. There is no pending-transfer state and
no interval with two owners or no owner.

## 5. Contract authentication

Each account verifies:

- its own code hash and deterministic address;
- network ID and genesis hashes;
- target object ID and object kind;
- expected sender contract for forwarded operations;
- action code hash, generation, sequence, and predecessor;
- canonical payload bounds;
- current tombstone and immutable-version rules; and
- required authority and counterparty signatures.

## 6. State projection

Resolvers decode the complete typed TVM state. JSON or CBOR views are derived
after code-hash, address, network, state-hash, quorum, and finality checks. A
projection must round-trip semantically to the decoded state but cannot be used
to request a transition.

## 7. Required adversarial tests

- wrong network, code hash, object ID, address, sender, or state hash;
- malformed or over-bound cell trees and trailing data;
- duplicate, unknown, unsorted, wrong-purpose, or invalid signatures;
- unreachable thresholds and controller key mismatch;
- caller-selected registration identity;
- stale predecessor, skipped sequence, conflicting replay, or wrong generation;
- policy installation without proof of possession;
- stale recovery after policy rotation;
- generation reset with a zero or stale predecessor;
- recovery completion after an intervening delegation, proving the delegation
  transition is included in the predecessor chain;
- superseded recovery initiation; and
- duplicate or overwritten Capability version;
- mutation by a former owner after transfer;
- transfer rejected by either current or new owner policy; and
- any failure producing a partial ownership transfer.
