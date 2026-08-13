# Native Capability Registry V1

Status: **normative Phase 5A contract**

Pre-deployment erratum (Phase 5B): V1 domains, identifiers, field meanings and
digest algorithms are unchanged, but the executable size/count limits in
§2.1 and §4 are normative. The original unbounded repeated fields admitted
canonical actions larger than a TOS external message and append-only states
that could eventually exceed account-state limits. No Native V1 registry was
deployed before this correction.

## 1. Scope

This freezes every Phase 5B authorization input: typed payloads, action-purpose
mapping, multisignature rules, state transitions, chain events and independently
verified TOS observations. Phase 5B implements these semantics but MUST NOT
invent or weaken them.

## 2. Registry action

Domain: `tos.native.registry-action.v1`. Every field is present:

```text
version = "tos_native_registry_v1"; kind; NetworkDomain
agent_id; capability_id; capability_version
generation; sequence; previous_state_digest
policy_digest; payload_digest; payload_cbor_base64url
nonce_base64url
```

Payload bytes are canonical CBOR, encoded as canonical raw base64url. Their
digest uses `tos.native.registry-payload.<hyphenated-kind>.v1`. Both bytes and
digest are in the signed action; a digest without the typed bytes is invalid.
The 32-byte nonce is stable across exact retries. Changed semantics under the
same action identity are an idempotency conflict.

### 2.1 Consensus execution limits

These are semantic V1 limits and MUST be enforced before signing, publishing,
contract execution and independent replay:

```text
canonical RegistryAction CBOR             <= 24576 bytes
canonical typed payload CBOR               <= 16384 bytes
canonical ControllerPolicy CBOR             <= 12288 bytes
purposes per controller                     <= 16
delegation purposes                         <= 16
delegation resources                        <= 32
manifest retrieval locations                <= 16
Capability endpoint references              <= 32
Quote signer key IDs                        <= 32
Receipt signer key IDs                      <= 32
active delegation action digests/generation <= 128
immutable Capability versions/lineage       <= 256
```

The complete Phase 5B execution envelope, including action, authorization sets
and framing, MUST be at most 49152 bytes before BOC encoding. Implementations
MUST additionally prove that the resulting external message is within the
active TOS `max_ext_msg_size`, `max_msg_bits`, `max_msg_cells` and depth limits;
a configuration increase never relaxes these semantic limits. Oversize input
is `NATIVE_CANONICAL_ENCODING_INVALID`, never a transport retry.

The consensus-safe dual representation and signature binding are frozen in
`NATIVE_REGISTRY_TVM_V1.md`. A relayer MUST NOT synthesize the typed TVM action
from an already signed CBOR action: controllers sign the joint execution
commitment before the relayer receives it.

Kinds and required authorization are:

| Kind | Required purpose and threshold | Typed payload |
|---|---|---|
| `register_agent` | new policy `agent_control`, normal threshold | object nonce, initial policy digest and canonical policy bytes |
| `update_agent_policy` | current `agent_control`, normal threshold | new policy digest and canonical policy bytes |
| `delegate_agent` | current `delegation`, normal threshold | delegate key, purposes/resources, checkpoint validity/staleness |
| `initiate_recovery` | current recovery keys, recovery threshold | new policy digest/bytes, execute-after TOS time |
| `recover_agent` | same recovery set and finalized initiation | new policy, initiation action/reference, execute-after |
| `revoke_agent` | current `agent_control`, normal threshold | scope and reason |
| `register_capability` | current owner `capability_control`, normal threshold | bootstrap nonce and CapabilityVersionPayload |
| `update_capability` | current owner `capability_control`, normal threshold | new immutable version payload |
| `transfer_capability` | current owner and new owner each `capability_control` | both Agent IDs and new-owner policy digest/bytes |
| `revoke_capability` | current owner `capability_control`, normal threshold | lineage/version scope and reason |

Signature arrays are strict key-ID order with no duplicates. Every signature
binds its version, algorithm, key ID and complete action. Weight is counted once
per unique key ID and unique public key. Unknown keys/purposes fail closed. A
transfer is valid only when independently verified signature sets from the
current-owner policy and the committed new-owner policy both satisfy threshold.
For every non-bootstrap action, the caller also supplies the independently
resolved policy digest that was canonical at the action predecessor. The
action's `policy_digest`, the supplied policy bytes and that resolved digest
MUST all be equal before any signature weight is counted. Registration binds
the new policy in the Agent ID and action payload. A payload-provided policy is
never sufficient evidence that it was the canonical current policy.

## 3. Typed payloads

The protobuf messages in `native_registry.proto` and their same-named JSON/CBOR
fields are normative. Unknown fields are rejected recursively.

`CapabilityVersionPayload` binds owner Agent, manifest reference, endpoint
commitments, recipient-key IDs, disjoint Quote/Receipt signer IDs, and nonzero
finalized-checkpoint validity interval. The manifest reference contains:

```text
digest; media_type = application/vnd.atos.native-capability+json
size_bytes = 1..1048576; sorted unique retrieval locations
```

Locations are availability hints, never authority. Phase 5C applies URL/SSRF
policy and accepts bytes only when size and digest match. Endpoint references
are sorted by `(transport, endpoint_digest, recipient_key_id)` and bind endpoint
semantics without placing credentials or private workload data on-chain.
Every Quote/Receipt signer ID MUST name a key in the canonical owner policy and
that key MUST carry the corresponding `quote` or `receipt` purpose. The two
sets are individually sorted and mutually disjoint. Locations, resources and
other protocol strings described as ASCII contain printable bytes `0x21..0x7e`
only; Unicode, whitespace and control-character aliases are invalid.

`register_capability` repeats the 32-byte Capability bootstrap nonce alongside
the first version payload. A verifier recomputes `capability_id` from the
network, bootstrap owner and nonce. Later transfer changes current ownership,
not that bootstrap tuple or the Capability ID. A transfer increments the
Capability ownership generation and starts sequence 1; the next action is
authorized by the new owner's independently resolved current policy.

Delegation validity is evaluated against finalized TOS checkpoints. It is valid
only within `[valid_from_checkpoint, valid_until_checkpoint)` and only while the
resolver observation lag does not exceed `max_staleness_checkpoints`.

Recovery uses finalized TOS block Unix seconds. Initiation records a pending
recovery. Execution must reference that exact finalized initiation transaction,
use its exact proposal and execute-after value, satisfy the old policy recovery
threshold, and occur no earlier than execute-after. The Registry contract MUST
reject an execute-after earlier than the initiation's canonical TOS block time
plus the old policy's recovery timelock. A later signer-selected not-before time
is valid and remains part of the deterministic signed state. The finalized initiation
MUST be the recovery action's immediate predecessor state; an older, parallel
or superseded initiation cannot be used. Recovery increments
generation and starts sequence 1; ordinary actions retain generation and use
previous sequence plus one. Permanent Agent tombstones cannot recover.

## 4. Canonical registry state

Domain: `tos.native.registry-state.v1`.

`NativeRegistryStateV1` is the complete logical state committed by every
event. It binds the network/object identity, generation/sequence, predecessor
state digest, last action digest and tombstone. Agent state additionally binds
the immutable bootstrap nonce/policy digest, the exact current controller-policy
digest/bytes, ordered delegation action digests and exact pending-recovery
tuple. Capability state additionally binds
the immutable bootstrap owner/nonce, current owner and the sorted immutable
version entries with version revocation state. Repeated state fields are
always encoded as canonical CBOR arrays; a zero-entry collection is `[]`,
never CBOR `null`. Decoders MUST normalize language-specific nil collections
to empty arrays before validation, hashing, TVM-state construction or public
transport. Other inapplicable fields MUST have their protobuf/JSON zero value.

Both Agent and Capability IDs are recomputed from the immutable bootstrap
fields whenever state is validated. The next state is deterministically derived from the predecessor state and the
complete finalized action bytes. Its digest is recomputed independently and
must equal the event's `state_digest`; an event may not supply an arbitrary
nonzero state digest. Bootstrap IDs are recomputed, an existing version cannot
be overwritten, transfer increments ownership generation, and a lineage or
Agent tombstone makes every later transition fail with
`NATIVE_PERMANENTLY_REVOKED`. Recovery clears old delegations and pending
recovery state. Controller-policy rotation also clears every delegation action
digest authorized by the previous policy. A generation cannot contain more
than 128 active delegation digests. A Capability lineage cannot contain more
than 256 immutable versions; the limit is checked before mutation. Reaching a
frozen limit is an explicit protocol error and MUST NOT yield a partially
updated state.

Controller policies needed to replay authority are canonical CBOR embedded in
registration, rotation, recovery-initiation and transfer-acceptance payloads.
Their committed digest must match those bytes. A fresh resolver reads the
complete action from the finalized transaction, validates its event and
inclusion proof, derives the next state, and compares the emitted state digest;
the compact event alone is not treated as the action payload.

## 5. Chain event versus network observation

The chain-stored event domain is `tos.native.registry-event.v1`:

```text
version, kind, network, action_digest
agent_id, capability_id, capability_version
generation, sequence, previous_state_digest, state_digest
```

It contains only values the registry contract can compute/store. An action
predecessor is the prior contract `state_digest`, never a digest containing
future transaction coordinates.

The separate observation domain is `tos.native.event-observation.v1` and binds:

```text
event_digest; network/genesis
workchain; account; logical_time; transaction_hash; event_index
contract_code_hash
finalized_checkpoint; finalized root/file hashes
finalized block Unix seconds; inclusion_proof_digest
```

All hashes are nonzero canonical digests and checkpoint/logical time are
nonzero. This tuple—not a shard-local transaction index, gateway row or RPC
URL—identifies and proves inclusion of the real TOS transaction. Contract code
hash is checked against the version allowlist. A quorum/finality adapter derives
the observation; callers cannot assert it.

The decimal workchain prefix inside `account` MUST be the shortest canonical
base-10 rendering of the separate signed `workchain` field. Leading zeroes,
`-0` and a prefix/field mismatch are rejected.

The enrolled publisher persists the exact signed external wallet-message BOC
and its SHA-256 digest before broadcast. Recovery resubmits only those
byte-identical bytes; it never requests a second signature or constructs a
second wallet transaction semantic.

## 6. Index/reorg rules

- order observations by canonical TOS inclusion order, never arrival time;
- reject gaps, state predecessor mismatch, cross-network objects and conflicting
  events at one logical state transition;
- exact replay is harmless;
- retain historical state and observations needed to verify authority at an
  execution/Receipt boundary;
- roll back observations/state above a reorg boundary and replay finalized
  canonical history;
- a checkpoint regression or unavailable quorum fails closed;
- search, ranking, manifest availability and gateway caches are projections,
  never ownership authority.

## 7. Stable errors and vectors

Stable codes include `NATIVE_SEQUENCE_CONFLICT`,
`NATIVE_PREDECESSOR_MISMATCH`, `NATIVE_POLICY_UNAUTHORIZED`,
`NATIVE_PURPOSE_UNAUTHORIZED`, `NATIVE_RECOVERY_TIMELOCK_PENDING`,
`NATIVE_PERMANENTLY_REVOKED`, `NATIVE_STALE_AUTHORITY`,
`NATIVE_FINALITY_UNAVAILABLE` and the identifier/canonicalization errors.

`test-vectors/native_registry_v1.json` contains executable positive and
field-level negative operations with exact expected code/field. It also freezes
canonical payload, Action and complete next-state bytes/digests for every
Action kind, including both Capability revocation scopes. Both the Go
implementation and the independent Python deterministic-CBOR implementation
execute all mutations and all transition vectors; neither generates expected
values at test runtime.
