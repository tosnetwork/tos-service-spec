# Native Capability Registry V1

Status: **normative Phase 5A contract**

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

Kinds and required authorization are:

| Kind | Required purpose and threshold | Typed payload |
|---|---|---|
| `register_agent` | new policy `agent_control`, normal threshold | object nonce, initial policy digest |
| `update_agent_policy` | current `agent_control`, normal threshold | new policy digest |
| `delegate_agent` | current `delegation`, normal threshold | delegate key, purposes/resources, checkpoint validity/staleness |
| `initiate_recovery` | current recovery keys, recovery threshold | new policy digest, execute-after TOS time |
| `recover_agent` | same recovery set and finalized initiation | new policy, initiation action/reference, execute-after |
| `revoke_agent` | current `agent_control`, normal threshold | scope and reason |
| `register_capability` | current owner `capability_control`, normal threshold | CapabilityVersionPayload |
| `update_capability` | current owner `capability_control`, normal threshold | new immutable version payload |
| `transfer_capability` | current owner and new owner each `capability_control` | both Agent IDs and new-owner policy digest |
| `revoke_capability` | current owner `capability_control`, normal threshold | lineage/version scope and reason |

Signature arrays are strict key-ID order with no duplicates. Every signature
binds its version, algorithm, key ID and complete action. Weight is counted once
per unique key ID and unique public key. Unknown keys/purposes fail closed. A
transfer is valid only when independently verified signature sets from the
current-owner policy and the committed new-owner policy both satisfy threshold.

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

Delegation validity is evaluated against finalized TOS checkpoints. It is valid
only within `[valid_from_checkpoint, valid_until_checkpoint)` and only while the
resolver observation lag does not exceed `max_staleness_checkpoints`.

Recovery uses finalized TOS block Unix seconds. Initiation records a pending
recovery. Execution must reference that exact finalized initiation transaction,
use its exact proposal and execute-after value, satisfy the old policy recovery
threshold, and occur no earlier than execute-after. Recovery increments
generation and starts sequence 1; ordinary actions retain generation and use
previous sequence plus one. Permanent Agent tombstones cannot recover.

## 4. Chain event versus network observation

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

## 5. Index/reorg rules

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

## 6. Stable errors and vectors

Stable codes include `NATIVE_SEQUENCE_CONFLICT`,
`NATIVE_PREDECESSOR_MISMATCH`, `NATIVE_POLICY_UNAUTHORIZED`,
`NATIVE_PURPOSE_UNAUTHORIZED`, `NATIVE_RECOVERY_TIMELOCK_PENDING`,
`NATIVE_PERMANENTLY_REVOKED`, `NATIVE_STALE_AUTHORITY`,
`NATIVE_FINALITY_UNAVAILABLE` and the identifier/canonicalization errors.

`test-vectors/native_registry_v1.json` contains executable positive and
field-level negative operations with exact expected code/field. Both the Go
implementation and independent verifier execute them.
