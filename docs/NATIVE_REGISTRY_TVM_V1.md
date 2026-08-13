# Native Registry TVM Execution V1

Status: **normative Phase 5B consensus contract**

## 1. Two representations, one signed meaning

Phase 5A canonical CBOR remains the portable protocol value. A TVM contract
cannot safely authorize a caller-supplied interpretation of those bytes. Phase
5B therefore defines a typed TVM action cell. Controllers sign both values in
one execution commitment, the contract validates the typed cell, and every
resolver compares the typed fields to decoded canonical CBOR field-for-field.
Neither representation is authoritative alone.

The execution version is `tos_native_registry_tvm_v1`. Each signature covers
the 32-byte TVM representation hash of this canonical commitment cell:

```text
native_registry_signature$_ magic:uint32 = 0x4e534731 schema:uint16 = 1
  key_id_hash:uint256 contract_workchain:int32 contract_account:uint256
  ^[contract_code_hash:uint256 portable_action_digest:uint256]
  ^[action_cell_hash:uint256 previous_tvm_state_hash:uint256
    expected_tvm_state_hash:uint256]
  ^[expected_portable_state_digest:uint256
    action_anchor_workchain:int32 action_anchor_account:uint256]
```

`key_id_hash` is SHA-256 over the exact printable-ASCII key ID. The key ID is
also present in the sorted signature envelope and canonical policy; resolvers
require both to match. Hash strings use their raw 32-byte value.
The contract address is canonical `workchain:64-lowercase-hex`; aliases,
leading-zero workchains and `-0` are invalid. Signatures are Ed25519 and sorted
by `key_id`. Current-owner and transfer-acceptance sets are disjoint.

## 2. Typed action cell

`action_cell_boc_base64url` is a canonical single-root BOC. The root begins
with `0x4e525631` (`NRV1`), a 16-bit schema version `1`, an 8-bit action kind,
generation and sequence as uint64, the raw 32-byte Agent ID, optional
Capability ID, previous TVM state hash, portable action digest and payload
tag. References contain the canonical network tuple, typed payload, authority
policy, optional new-owner policy, the complete expected typed next-state cell,
and immutable portable action bytes as a
canonical snake cell. Every non-bootstrap action also carries the complete
typed predecessor state cell; its representation hash must equal both the
signed predecessor hash and current on-chain object state. Empty values have
one representation only. Bootstrap
uses an all-zero previous TVM state hash; all later actions require a nonzero
exact predecessor. Expected TVM and portable next-state commitments are
derived before signing and checked against the contract's deterministic result.

Controller policy cells contain threshold, recovery threshold, timelock and a
dictionary keyed by `SHA-256(key_id)` whose values contain the exact key ID,
Ed25519 public key, weight and a fixed purpose bitmask. The cell also commits
the portable controller-policy digest. Duplicate key IDs, duplicate public
keys, unknown purpose bits and weight overflow are invalid.

Typed payload cells contain every field of the corresponding Phase 5A payload,
including exact printable-ASCII strings, arrays and referenced policy cells.
Array order and limits are those frozen in
`NATIVE_CAPABILITY_REGISTRY_V1.md`. A resolver rejects any typed/CBOR mismatch
as `NATIVE_EXECUTION_SEMANTICS_MISMATCH`.

The action cell hash is the ordinary TVM representation hash and the BOC MUST
decode to exactly one non-exotic root whose hash matches `action_cell_hash`.
The embedded portable bytes are hashed by consensus opcode `SHA256C`; they MUST
equal `portable_action_digest` after the frozen Phase 5A domain framing.

The reviewed V1 FunC source compiles to contract code representation hash
`tvm-cell-sha256:efb7b9260383ff66e9f0ca6a9bc2e30979186bd48416d3d61b116ccb65098ba7`.
Deployments MUST pin this value and reproduce it from the committed source,
stdlib, compiler and generated Fift artifact. Any source or VM opcode change
creates a new allowlisted code hash; a runtime-learned hash is invalid.

## 3. Contract state and transition

The registry is a deterministic family of per-object contracts, not one
ever-growing account. An Agent contract stores its complete typed identity
state. A Capability contract stores its immutable lineage, current owner,
versions and tombstone. Addresses are derived from the pinned code hash,
network/genesis, object kind and raw object ID; a resolver recomputes the
StateInit address and rejects any caller-selected alternative.

Capability contracts never trust a cached copy of an Agent policy. For every
Capability mutation they send the unchanged signed execution action to the
canonical current-owner Agent contract. That Agent contract validates its live
policy and replies with an action-bound internal approval. Transfer sends the
same action to both canonical Agent contracts and finalizes only after current
owner authorization and new-owner acceptance are present. Pending approvals
are keyed by action hash and predecessor, cannot change semantics, and a late
approval cannot cross a newer Capability transition. Policy rotation therefore
takes effect immediately without enumerating owned capabilities.

Each portable Action ID also deterministically derives a one-action Anchor
account using the same pinned code and StateInit grammar. The relayer deploys
the Anchor with the complete TVM-signed execution envelope before it can emit any
Agent/Capability mutation. The Anchor forwards the unchanged action to the
canonical Agent contract and records the completed state commitments returned
by the canonical object contract. For Capability actions the completion also
stores the exact finalized current-owner Agent state used by the approval; a
transfer stores both current- and new-owner Agent states. A resolver hashes
those snapshots, resolves the identical historical Agent states through their
own predecessor chains, verifies their policy digests, and independently
rechecks every stored Ed25519 execution signature, key ID, purpose and weighted
threshold. Historical commitment existence without this authority proof is
invalid. A duplicate envelope may re-drive only that
same action: an already-mutated object re-sends its durably stored completion
tuple and performs no second state transition. Consequently a crash after the
object mutation but before Anchor completion is recoverable, and an empty
resolver performs no unbounded history search: it derives the Anchor address
from the Action ID and obtains the complete envelope there. Historical state
resolution follows the signed predecessor state cell and its last Action ID
to the preceding deterministic Anchor. A missing local cache, gateway database
or publisher journal is irrelevant.

For every mutation the contract:

1. verifies network, deterministic object-contract identity, BOC and execution commitment;
2. loads the exact predecessor and rejects stale digest/sequence/generation;
3. validates Agent actions against the Agent's stored or bootstrap policy;
4. validates Capability actions through action-bound Agent-contract approvals,
   with independent current/new-owner approvals for transfer;
5. derives the only legal next typed state and uses TOS `now()` only to prove a
   signer-selected recovery not-before time is no earlier than the old-policy
   timelock after actual inclusion;
6. checks that the supplied portable next-state digest is signed;
7. stores typed state and emits action/state hashes and portable digests.

An Agent or Capability tombstone is permanent. Capability versions cannot be
overwritten. Policy rotation and recovery clear delegations. Recovery execution
requires the immediate pending initiation and chain time at or after its
execute-after value.

The enrolled relayer funds each Action Anchor with at least `200000000` nanoTOS.
The contract forwards `100000000` nanoTOS to the Agent execution hop; the
remaining margin pays Anchor compute and action fees. Funding policy is part of
the publisher enrollment binding and cannot change without a new journal.

## 4. Resolver and failure behavior

A resolver obtains the complete action BOC, signatures, completion tuple and
object state from deterministic accounts at one strict-majority finalized TOS
checkpoint. The `ChainReference` identifies the exact account-state observation
anchor; a transaction's own success flag is never accepted as a substitute for
the included account data. It replays both
the typed transition and Phase 5A transition, then compares all fields and both
state commitments. Local caches, publisher journals and ordinary HTTP 404s are
never canonical authority or absence.

The portable semantic signatures carried by the submission RPC are validated
before relay but are not redundantly stored in consensus. Canonical chain
evidence is the TVM execution signature set: its commitment binds the exact
portable Action digest and CBOR-containing action cell as well as the object,
Action Anchor, code hash and both next-state commitments. An independent
resolver MUST decode and verify that set; trusting the contract code hash or a
publisher receipt without rechecking the stored signatures is insufficient.

An Action Anchor completion permanently stores the consensus `now()` and
`cur_lt()` of its successful `complete` transaction alongside the immutable
submission and completion tuple. A resolver MUST completely paginate the
Anchor account history to that logical-time boundary and verify the exact
successful inbound completion transaction, its Action ID, BOC hash and chain
timestamp. It MUST NOT substitute the account's mutable latest transaction or
treat a bounded-history miss as absence. History pruning, incomplete pagination
or timeout is `NATIVE_ACTION_UNAVAILABLE` and cannot authorize mutation.

Stable additions are `NATIVE_EXECUTION_SEMANTICS_MISMATCH`,
`NATIVE_CONTRACT_CODE_HASH_MISMATCH`, `NATIVE_CONTRACT_STATE_MISMATCH` and
`NATIVE_ACTION_UNAVAILABLE`.
