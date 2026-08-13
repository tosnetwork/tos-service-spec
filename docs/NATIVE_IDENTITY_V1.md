# Native Identity V1

Status: **normative Phase 5A contract**

## 1. Authority model

A Native Agent is a stable global identifier governed by a versioned controller
policy. It is not a wallet address and does not change when keys rotate. A
gateway may relay an unchanged signed action but has no implicit controller,
recovery, ownership or spending authority.

The initial policy digest participates in Agent-ID derivation. Registration and
every policy-changing action carry both the digest and exact canonical policy
bytes so a fresh verifier does not need an `atos.im` policy table. Every later
policy is linked by a finalized registry event. Current authority is the latest
valid finalized state after deterministic reorg handling, not a gateway cache.

## 2. Controller policy

Domain: `tos.native.controller-policy.v1`.

The canonical policy fields are:

```text
threshold                   uint32, nonzero
recovery_threshold          uint32, nonzero
controllers[]               1..64, sorted strictly by key_id
  key_id                    ASCII stable key identifier
  algorithm                 "ed25519" in V1
  public_key_base64url      canonical raw base64url, exactly 32 nonzero bytes
  weight                    uint32, nonzero
  purposes[]                sorted unique ASCII purpose labels
recovery_key_ids[]          sorted unique subset of controller key IDs
recovery_timelock_seconds   uint64
```

Canonical ControllerPolicy CBOR is limited to 12288 bytes and each controller
has at most 16 purposes. Delegations contain at most 16 purposes and 32
resources. The complete action/payload and accumulated-state limits are frozen
in `NATIVE_CAPABILITY_REGISTRY_V1.md` §2.1.

The normal threshold cannot exceed total controller weight. The recovery
threshold cannot exceed the total weight of `recovery_key_ids`; every recovery
key carries the `recovery` purpose. The same public-key bytes MUST NOT occur
under two key IDs, so one physical key can never contribute weight twice.
V1 semantic action
signatures use Ed25519. TOS transaction authorization may use the TOS-native
Schnorr transaction scheme; that outer transaction signature is not a
substitute for this purpose-bounded semantic signature.

Standard V1 purpose labels include `agent_control`, `delegation`, `recovery`,
`capability_control`, `quote`, `receipt`, `invocation`, `funding`, `release`,
`dispute` and `settlement`. A key is authoritative only for its explicit
purpose. Quote and Receipt authority are disjoint unless both are granted.

## 3. Ordered identity actions

Identity actions use the registry action format in
`NATIVE_CAPABILITY_REGISTRY_V1.md` with exactly one of:

```text
register_agent
update_agent_policy
delegate_agent
initiate_recovery
recover_agent
revoke_agent
```

Recovery is two-step. `initiate_recovery` records the proposed policy digest
and `execute_after_unix_seconds`; it is authorized using `recovery_threshold`.
`recover_agent` names the exact finalized initiation action and canonical TOS
transaction reference, and that initiation state must be the recovery's direct
predecessor. The initiation time is the finalized TOS block time. The offline
signer chooses the exact `execute_after_unix_seconds` committed by both actions
and states; the Registry contract requires it to be greater than or equal to
the actual initiation block time plus the old policy's timelock. Gateway clocks
and transaction submission time are not authority.

`generation` changes only when recovery executes. Ordinary actions keep the
generation and increment sequence. Recovery increments generation exactly once
and starts sequence 1. Every non-bootstrap action binds the immediately prior
on-chain `state_digest`, not a later finality wrapper.
Skipped, duplicate, forked or stale predecessors fail closed.

Delegation payloads bind delegate key, purposes, resources, validity interval,
maximum chain checkpoint staleness and canonical action identity. They cannot
broaden the delegator's authority, and are valid only while the referenced key
and purposes remain in the current policy. Recovery, controller-policy rotation
and permanent revocation invalidate prior-policy or prior-generation
delegations. Recovery binds the old generation, new policy,
recovery authorization and timelock. Permanent revocation produces a tombstone;
no later action can revive that Agent ID.

Every authorization call binds three equal values before signatures are
evaluated: the policy digest in the signed action, the digest recomputed from
the supplied canonical policy bytes, and the current policy digest independently
resolved from the predecessor state. Supplying a self-consistent attacker
policy is not authorization. Recovery uses the old policy embedded in the
canonical predecessor state; callers cannot substitute a different timelock or
recovery set.

## 4. Finalized ordering

Canonical observation order is the tuple:

```text
(finalized_checkpoint, workchain, account, logical_time,
 transaction_hash, event_index)
```

The account, logical time and transaction hash are the canonical TOS
transaction identity. The observation additionally binds contract code hash,
masterchain root/file hashes and inclusion-proof digest. A later
rotation/revocation affects authority only at its canonical event position.
Earlier legitimate history remains verifiable. Two conflicting events at the
same logical sequence are an integrity conflict until canonical finality
selects one; a resolver MUST NOT choose by arrival time or local write order.

Reorganization removes events above the new common finalized boundary and
deterministically reapplies the canonical sequence. A checkpoint regression or
unavailable quorum is an error, not permission to use stale authority.

## 5. Semantic signatures

Registry action canonical bytes are hashed with SHA-256 and signed over:

```text
"TOS-NATIVE-SEMANTIC-SIGNATURE" || 0x00 ||
uint16_be(len("tos.native.semantic-signature.v1")) ||
"tos.native.semantic-signature.v1" ||
uint16_be(len("tos_native_registry_v1")) ||
"tos_native_registry_v1" ||
uint16_be(len("ed25519")) || "ed25519" ||
uint16_be(len(key_id)) || key_id ||
uint16_be(len("tos.native.registry-action.v1")) ||
"tos.native.registry-action.v1" ||
SHA-256(canonical_registry_action_cbor)
```

Version, algorithm and key ID are therefore signed fields. Signature threshold and
purpose are evaluated against the policy valid at the action's predecessor.
Signatures cannot be replayed as wallet sessions, transfers, Quotes,
invocations, Receipts, disputes or settlements because those later contracts
use distinct domains.

## 6. Privacy and recovery

Registry state contains public keys, policy commitments and public bounded
delegation facts only. It MUST NOT contain wallet seeds, private task data,
credentials, proposals or bulk artifacts. Offline, HSM and TEE signing are
supported because canonical action bytes do not require gateway secrets.

Fresh replicas rebuild authority solely from finalized canonical events.
Historical existence does not imply current authority; revocation, recovery,
generation and tombstone state must also be resolved.
