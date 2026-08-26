# Semantic Action Identity V1

**Status:** normative release candidate; production codec, standalone reference
verifier, exact vectors, and local cross-platform conformance are available;
external production acceptance remains pending

**Used by:**
[`AGENT_INTENT_EXCHANGE_V1.md`](AGENT_INTENT_EXCHANGE_V1.md),
[`OPENFOX_AUTONOMOUS_EARNING_IMPLEMENTATION_PLAN.md`](OPENFOX_AUTONOMOUS_EARNING_IMPLEMENTATION_PLAN.md),
and every side-effect sink

## 1. Purpose

`SemanticActionIdentityV1` gives one economic or externally visible side effect
the same identity across implementations, retries, crashes, transport sessions,
and writer takeover. It prevents a caller from escaping an ambiguous action by
choosing a new idempotency key, while still allowing an owner to authorize two
genuinely distinct but otherwise identical actions.

This registry is business-neutral. It identifies operations such as contact,
publication, execution, disclosure, and payment; it does not add a workflow for
each profession or trade category.

## 2. Normative encoding and digest

V1 uses SHA-256 and the following independent binary framing. It does not depend
on protobuf field order, JSON spelling, a transport wrapper, or a sink request
identifier.

```text
SemanticActionIdentityPreimageV1 {
  magic                  # exact 8 bytes: 54 4f 53 2d 53 41 49 00 ("TOS-SAI\0")
  registry_version       # uint16 big-endian; V1 = 1
  entry_version          # uint16 big-endian
  domain_tag             # lp16 bytes
  action_kind            # lp16 canonical lower-case ASCII
  field_count            # uint16 big-endian
  fields[] {             # exact registry order, never caller order
    field_name           # lp16 canonical lower-case ASCII
    field_value          # lp32 exact canonical bytes
  }
}

lp16(x) = uint16_big_endian(len(x)) || x
lp32(x) = uint32_big_endian(len(x)) || x

stable_action_id
  = "sha256:" || lower_hex(SHA-256(SemanticActionIdentityPreimageV1))
```

An `id` field is the exact canonical UTF-8 identifier defined by its owning
profile, without Unicode normalization by this registry. A `digest32` field is
the raw 32 bytes decoded from a canonical `sha256:` digest. A `u64` field is
eight-byte unsigned big-endian. A `kind` or `state` is the exact lower-case
ASCII registry token. A set is sorted and encoded by its owning canonical
schema, then represented here by its `digest32`. Empty, non-canonical, unknown,
duplicate, overlong, or type-invalid values fail closed.

The exact request is separately bound:

```text
exact_request_digest
  = "sha256:" || lower_hex(SHA-256(
      "tos.action-request.v1\0" ||
      uint32_big_endian(len(canonical_action_request_body)) ||
      canonical_action_request_body))
```

The canonical action request body is the exact side-effect payload and safety
parameters, not the enclosing `AuthorizedActionV1`. It excludes retry counters,
RPC ids, sessions, routes, connection metadata, queue offsets, writer
generation/fence/lease, wall time, and equivalent transport or admission
ephemera. A takeover may therefore present a new valid fence while binding the
same action ID and request digest. The sink recomputes the semantic key from the
request body and requires the supplied `stable_action_id` to match. The same
action id with a different exact request digest is `conflict`; a request whose
semantic fields do not match the registry entry is `invalid`.

## 3. Registry entry schema

```text
SemanticActionIdentityEntryV1 {
  registry_version
  action_kind
  entry_version
  domain_tag
  ordered_semantic_fields[] {
    field_name
    field_type
    presence              # required or condition(expression)
  }
  forbidden_input_classes[]
  successor_policy        # none, terminal_successor, authority_instance
}
```

Changing a field, order, type, condition, domain tag, or successor rule requires
a new entry version. An unknown kind/version fails closed. Implementations may
support several released versions concurrently but cannot silently reinterpret
an existing version.

The following input classes are forbidden for every V1 entry: retry or attempt
counter except the released execution lineage below; source cursor; model turn;
wall-clock observation; transport, RPC, session, device, route, wrapper, or
queue id; writer generation, lease, fence, process, host, or deployment id; and
sink-local database primary key.

## 4. V1 registry

All entries have `registry_version = 1`, `entry_version = 1`, and a domain tag
equal to `tos.semantic-action.<action_kind>.v1` unless the table states
otherwise. Fields appear in the exact order shown.

| `action_kind` | Ordered semantic fields | Successor policy |
|---|---|---|
| `publication.publish` | `owner_id:id`, `agent_id:id`, `carrier_id:id`, `intent_object_id:id`, `revision:u64`, `operation_digest:digest32` | none |
| `authority.instance` | `owner_id:id`, `agent_id:id`, `purpose_kind:kind`, `mandate_digest:digest32`, `allocation_request_digest:digest32`, `authority_allocation_sequence:u64` | none |
| `publication.reply` | `owner_id:id`, `agent_id:id`, `carrier_id:id`, `parent_operation_digest:digest32`, `authority_instance_id:digest32` | authority_instance |
| `publication.withdraw` | `owner_id:id`, `agent_id:id`, `carrier_id:id`, `intent_object_id:id`, `withdrawn_revision:u64`, `withdrawal_operation_digest:digest32` | none |
| `messenger.contact` | `owner_id:id`, `agent_id:id`, `recipient_agent_id:id`, `intent_reference_digest:digest32`, `authority_instance_id:digest32` | authority_instance |
| `messenger.send` | `owner_id:id`, `agent_id:id`, `recipient_set_digest:digest32`, `conversation_scope_digest:digest32`, `authority_instance_id:digest32` | authority_instance |
| `agreement.propose` | `owner_id:id`, `agent_id:id`, `agreement_body_digest:digest32`, `recipient_set_digest:digest32` | none |
| `agreement.authorize` | `owner_id:id`, `agent_id:id`, `agreement_body_digest:digest32`, `authority_subject_digest:digest32`, `predicate_set_digest:digest32`, `evidence_profile_digest:digest32` | none |
| `agreement.withdraw` | `owner_id:id`, `agent_id:id`, `agreement_body_digest:digest32`, `proposal_action_id:digest32` | none |
| `provider.offer` | `owner_id:id`, `agent_id:id`, `agreement_body_digest:digest32`, `demand_mutation_digest:digest32`, `buyer_agent_id:id`, `provider_offer_id:id`, `binding_digest:digest32` | none |
| `portfolio.reserve` | `owner_id:id`, `agent_id:id`, `agreement_body_digest:digest32`, `reservation_scope_digest:digest32`, `target_revision:u64` | terminal_successor |
| `portfolio.release` | `owner_id:id`, `agent_id:id`, `reservation_id:digest32`, `target_revision:u64`, `terminal_evidence_set_digest:digest32` | terminal_successor |
| `schedule.entry.transition` | `owner_id:id`, `agent_id:id`, `schedule_entry_id:id`, `agreement_body_digest:digest32`, `execution_id:digest32`, `expected_state_revision:u64`, `target_state:state`, `target_dispatch_generation:u64` | terminal_successor |
| `schedule.dependency.transition` | `owner_id:id`, `agent_id:id`, `upstream_agreement_digest:digest32`, `upstream_obligation_id:id`, `downstream_agreement_digest:digest32`, `downstream_obligation_id:id`, `dependency_type:kind`, `dependency_class:kind`, `transition_kind:kind`, `graph_base_revision:u64` | terminal_successor |
| `execution.slot` | `owner_id:id`, `agent_id:id`, `agreement_body_digest:digest32`, `execution_obligation_id:id`, `canonical_plan_digest:digest32`, `accepted_input_manifest_digest:digest32`, `attempt_index:u64`, `predecessor_terminal_resolution_digest:digest32` | terminal_successor |
| `execution.prepare` | `owner_id:id`, `agent_id:id`, `execution_id:digest32` | none |
| `execution.start` | `owner_id:id`, `agent_id:id`, `execution_id:digest32` | none |
| `executor.effect` | `owner_id:id`, `agent_id:id`, `agreement_body_digest:digest32`, `obligation_id:id`, `execution_id:digest32`, `plan_effect_id:id`, `effect_profile_digest:digest32`, `target_digest:digest32`, `operation_kind:kind`, `effect_semantic_key_digest:digest32` | none |
| `credential.issue` | `owner_id:id`, `agent_id:id`, `agreement_body_digest:digest32`, `obligation_id:id`, `execution_id:digest32`, `recipient_id:id`, `capability_descriptor_digest:digest32` | none |
| `disclosure.release` | `owner_id:id`, `agent_id:id`, `agreement_body_digest:digest32`, `obligation_id:id`, `recipient_id:id`, `content_digest:digest32`, `purpose_digest:digest32` | none |
| `content.upload` | `owner_id:id`, `agent_id:id`, `agreement_body_digest:digest32`, `obligation_id:id`, `handoff_id:id`, `sender_id:id`, `receiver_id:id`, `content_manifest_digest:digest32` | none |
| `content.delete` | `owner_id:id`, `agent_id:id`, `agreement_body_digest:digest32`, `obligation_id:id`, `handoff_id:id`, `content_manifest_digest:digest32`, `retention_policy_digest:digest32` | none |
| `delivery.release` | `owner_id:id`, `agent_id:id`, `agreement_body_digest:digest32`, `obligation_id:id`, `recipient_id:id`, `deliverable_manifest_digest:digest32` | none |
| `gift.send` | `owner_id:id`, `agent_id:id`, `authority_instance_id:digest32`, `recipient_id:id`, `network_id:id`, `asset_digest:digest32`, `amount_atomic:id`, `destination_digest:digest32` | authority_instance |
| `payment.direct` | `owner_id:id`, `agent_id:id`, `agreement_body_digest:digest32`, `obligation_instance_id:digest32`, `payer_id:id`, `payee_id:id`, `network_id:id`, `asset_digest:digest32`, `amount_atomic:id`, `destination_digest:digest32` | none |
| `settlement.external` | `owner_id:id`, `agent_id:id`, `agreement_body_digest:digest32`, `obligation_instance_id:digest32`, `adapter_profile_digest:digest32`, `payer_id:id`, `payee_id:id`, `system_id:id`, `asset_digest:digest32`, `amount_digest:digest32`, `destination_digest:digest32` | none |
| `escrow.transition` | `owner_id:id`, `agent_id:id`, `quote_commitment:digest32`, `escrow_account_id:id`, `transition_kind:kind`, `expected_state_digest:digest32` | terminal_successor |
| `billing.materialize` | `owner_id:id`, `agent_id:id`, `agreement_body_digest:digest32`, `agreement_obligation_id:id`, `sequence:u64` | none |
| `billing.resolve` | `owner_id:id`, `agent_id:id`, `obligation_instance_id:digest32`, `target_state:state`, `evidence_set_digest:digest32` | terminal_successor |
| `reconcile.apply` | `owner_id:id`, `agent_id:id`, `scope_digest:digest32`, `base_revision:u64`, `evidence_cut_digest:digest32` | terminal_successor |

`amount_atomic` is a canonical unsigned base-10 integer and therefore uses the
`id` byte rule; leading zeroes are invalid except for the exact value `0` where
the selected operation permits zero. Every destination- or asset-bearing
Adapter must project its complete canonical destination and asset identity into
the listed digest. Omitting a chain, token contract, workchain, memo/tag that
changes the recipient, wrapper code identity, or equivalent routing authority
is invalid.

An implementation that needs an unlisted side-effect kind must first add and
release a registry entry and vectors. It cannot fall back to a caller-provided
UUID. A read-only calculation, cache update, model turn, or Carrier-derived rank
does not receive an economic action identity because it has no external or
authority-changing side effect.

`schedule.entry.transition` covers entry admission, dispatch, cancellation,
preemption, ambiguous-state resolution, and terminal transition. The canonical
request carries the complete entry mutation; changing priority, deadline,
reservation, dependency set, cancellation/preemption class, irreversible
boundary, or evidence while reusing the same semantic transition therefore
conflicts through `exact_request_digest`. `schedule.dependency.transition`
covers both insertion and removal. `transition_kind` is `add` or `remove`, and
the Action Authority performs the graph-revision check, cycle check, edge
mutation, reservation/exposure update, and action admission in one transaction.

`executor.effect` is the business-neutral identity for a Skill's post-start
external or destructive effect when no more specific released action kind
applies. `plan_effect_id` is a nonzero unique identifier frozen in the exact
Gate-approved canonical plan, never allocated by the runner or model after
start. The selected effect profile deterministically projects the complete
destination, principal, resource, operation, and semantic replay key into
`target_digest` and `effect_semantic_key_digest`; its immutable descriptor is
bound by `effect_profile_digest`. A credentialed API write, repository mutation,
cloud-resource change, email send, or other visible tool effect cannot be
treated as an unregistered local detail. `content.delete` separately identifies
the destructive retention transition for accepted private content.

## 5. Authority-issued repeatable instances

Some actions are intentionally repeatable: an owner may send the same text
twice or send two Gifts of the same amount. Their distinction cannot be inferred
from content and cannot be left to a worker-selected nonce.

Allocation itself must be recoverable before the sequence or resulting
`authority_instance_id` is known to the caller. The request is therefore:

```text
AuthorityInstanceAllocationRequestV1 {
  owner_id
  agent_id
  purpose_kind
  mandate_digest
  approval_digest_or_zero           # raw 32 zero bytes when absent
  downstream_effect_descriptor_digest
  predecessor_authority_instance_id # raw 32 zero bytes for the first instance
}

downstream_effect_descriptor_digest
  = SHA-256("tos.authority-instance-effect.v1\0" ||
            uint32_big_endian(len(canonical_effect_body)) ||
            canonical_effect_body)

allocation_request_digest
  = SHA-256("tos.authority-instance-allocation.v1\0" ||
            uint32_big_endian(len(canonical_allocation_request_body)) ||
            canonical_allocation_request_body)

canonical_allocation_request_body
  = uint16_big_endian(1) ||       # request version
    uint16_big_endian(7) ||       # field count
    allocation_field("owner_id", owner_id) ||
    allocation_field("agent_id", agent_id) ||
    allocation_field("purpose_kind", purpose_kind) ||
    allocation_field("mandate_digest", raw32(mandate_digest)) ||
    allocation_field("approval_digest_or_zero", approval_digest_or_zero) ||
    allocation_field("downstream_effect_descriptor_digest",
                     raw32(downstream_effect_descriptor_digest)) ||
    allocation_field("predecessor_authority_instance_id",
                     predecessor_authority_instance_id)

allocation_field(name, value) = lp16(lower_ascii_name) || lp32(value)
```

`canonical_effect_body` is the exact intended downstream side-effect payload
with `authority_instance_id`, `AuthorizedActionV1`, retry, transport, writer,
and admission fields absent. Its released action profile defines exact canonical
bytes and a finite size bound; an unknown or non-canonical profile fails closed.
The `id`, `kind`, `lp16`, and `lp32` rules are those in §2; `raw32(x)` decodes a
canonical `sha256:` digest to its raw 32 bytes. Digest fields and zero sentinels
are exact 32-byte values, including `predecessor_authority_instance_id` despite
its ID name. The caller knows every allocation-request field before allocation
and can therefore query or retry the same digest after a lost response. The
Action Authority keeps one durable record for
`(owner_id, agent_id, allocation_request_digest)`. It allocates the sequence,
instance ID, policy result, and exposure change in one serializable transaction
before returning. Exact retry returns that record and never increments the
sequence.

The normative authority interface is:

```text
AllocateAuthorityInstance(request, writer_fence) -> authority_instance_record
ResolveAuthorityInstance(owner_id, agent_id, allocation_request_digest)
  -> authority_instance_record | unknown
```

`unknown` permits only an exact retry of the same allocation request. It never
authorizes a caller to vary a request field or choose a new sequence.

A second intentionally identical effect either references the prior terminal
authority instance as its predecessor or binds a distinct owner approval whose
policy explicitly permits an independent series. The authority validates the
predecessor, terminal resolution, mandate, approval, repeat limit, and aggregate
exposure. Reused, skipped, nonterminal, fabricated, or caller-selected
predecessors fail closed. A worker UUID, RPC ID, session ID, timestamp, or fresh
allocation request over the same effect cannot turn an ambiguous allocation
into a second admitted instance.

For an `authority_instance` entry, the Owner Economic Action Authority allocates
the instance in the same serializable transaction that validates policy,
mandate, approval, aggregate exposure, and writer fence:

```text
authority_instance_id = SemanticActionIdentityV1(
  action_kind = "authority.instance",
  fields = [
    owner_id,
    agent_id,
    purpose_kind,
    mandate_digest,
    allocation_request_digest,
    authority_allocation_sequence
  ])
```

`authority.instance` uses domain
`tos.semantic-action.authority.instance.v1`; the allocation sequence is a
rollback-resistant owner/Agent `u64`. The worker cannot supply or increment it.
The authority durably returns the allocated id before its exclusive broker can
perform the external action. Lost responses are resolved by the exact
`allocation_request_digest`; they do not allocate again. A second identical
action requires the predecessor- or approval-bound policy-admitted allocation
defined above and is not a retry.

## 6. Terminal successors

`none` forbids another action with the same semantic identity. Exact retry uses
the existing id and request digest.

`terminal_successor` permits a new semantic action only when the prior action
has a durable terminal resolution and the governing Agreement and policy permit
the transition. Its registry fields must already distinguish the new target
revision, target state, sequence, or transition. `unknown`, `prepared`,
`submitted`, `accepted`, `STARTING`, and any other ambiguous or nonterminal state
cannot allocate a successor. Cycle check, predecessor validation, successor
allocation, Portfolio change, and new action admission occur in one linearized
transaction.

A terminal successor never means “try the same effect under a new id.” If its
semantic projection is unchanged, it is the old action and resolves or retries
under the old identity.

## 7. Execution identity and attempt lineage

Execution uses a separately named slot identity encoded by the same V1 framing:

```text
action_kind = "execution.slot"
domain_tag  = "tos.semantic-action.execution.slot.v1"
fields = [
  owner_id:id,
  agent_id:id,
  agreement_body_digest:digest32,
  execution_obligation_id:id,
  canonical_plan_digest:digest32,
  accepted_input_manifest_digest:digest32,
  attempt_index:u64,
  predecessor_terminal_resolution_digest:digest32
]
```

Attempt zero uses `attempt_index = 0` and 32 zero bytes for the predecessor. A
timeout, process crash, partition, lease loss, or `AMBIGUOUS_START` is not
terminal and recomputes the same `execution_id`. A replacement attempt exists
only when the prior slot has a durable `FAILED`, `CANCELLED`, or `KILLED`
resolution, the Agreement and owner policy allow replacement, and no recorded
irreversible effect forbids it. The Action Authority atomically allocates
`attempt_index = prior + 1`, binds the exact predecessor terminal-resolution
digest, reserves the replacement exposure, and admits its `execution.prepare`
action. `SUCCEEDED` has no replacement. Skipped, reused, caller-selected, or
concurrently allocated attempt indexes fail closed.

`execution.prepare` and `execution.start` then derive distinct action IDs from
the same `execution_id`. This separates preparation from the one-shot start
linearization without allowing a takeover writer to invent another slot.

## 8. Exact-byte vectors

The following positive vector uses `agreement.propose` with:

```text
registry_version       = 1
entry_version          = 1
domain_tag             = "tos.semantic-action.agreement.propose.v1"
action_kind            = "agreement.propose"
owner_id               = UTF-8 "owner:test"
agent_id               = UTF-8 "agent:test"
agreement_body_digest  = 32 bytes of 0x11
recipient_set_digest   = 32 bytes of 0x22
```

Exact preimage hex:

```text
544f532d53414900000100010028746f732e73656d616e7469632d616374696f6e2e61677265656d656e742e70726f706f73652e7631001161677265656d656e742e70726f706f7365000400086f776e65725f69640000000a6f776e65723a7465737400086167656e745f69640000000a6167656e743a74657374001561677265656d656e745f626f64795f6469676573740000002011111111111111111111111111111111111111111111111111111111111111110014726563697069656e745f7365745f646967657374000000202222222222222222222222222222222222222222222222222222222222222222
```

Expected identity:

```text
sha256:4e98f9968e35e2493b666370342471a3e80336a23d61f57b6f5b15d93d230b3c
```

Changing only `recipient_set_digest` to 32 bytes of `0x33` produces this exact
preimage and identity:

```text
544f532d53414900000100010028746f732e73656d616e7469632d616374696f6e2e61677265656d656e742e70726f706f73652e7631001161677265656d656e742e70726f706f7365000400086f776e65725f69640000000a6f776e65723a7465737400086167656e745f69640000000a6167656e743a74657374001561677265656d656e745f626f64795f6469676573740000002011111111111111111111111111111111111111111111111111111111111111110014726563697069656e745f7365745f646967657374000000203333333333333333333333333333333333333333333333333333333333333333

sha256:c7dac213b5297bf30b08422b3c59887c953a54c06c71919813e76fdfb0444c98
```

Every implementation must also pass generated entry-specific vectors covering:

- mutation of each semantic field changes the identity;
- mutation of retry, route, session, wall time, writer generation, or fence does
  not enter the preimage and cannot change the identity;
- field omission, addition, reordering, wrong type, duplicate field, unknown
  version, overlong value, or non-canonical amount fails;
- changing recipient, destination, asset, network, obligation instance, content,
  Agreement, or expected transition never preserves an id;
- same id plus different exact request bytes is `conflict`;
- ambiguous execution, payment, publication, upload, or settlement cannot gain
  a successor id;
- takeover recomputes the same id for the same side effect;
- a lost authority-instance allocation response resolves by the same allocation
  request digest without incrementing the sequence, while a second intentional
  repeat requires a valid terminal predecessor or distinct owner approval;
- schedule entry and dependency transitions reproduce their state/graph
  revisions and reject concurrent cycle-forming or conflicting mutations;
- every post-start external/destructive effect uses `executor.effect` or a more
  specific released kind, and a runner-chosen effect ID, target, operation, or
  semantic-key substitution fails; and
- accepted private-content deletion uses `content.delete`, and conflicting
  manifest or retention-policy bytes cannot reuse the action identity.

Phase 0 cannot exit until `tos-service-protocol` and a code-independent
reference verifier consume the same registry data and reproduce every exact
preimage, identity, mutation result, failure class, and execution-lineage
decision.

## 9. Security boundary

Semantic identity provides deduplication and conflict detection. It does not
authorize an action. Every side effect still requires `AuthorizedActionV1`, its
authority signature, a valid `WriterFenceV1`, resolved policy/mandate/approval content, expected prior
state, Portfolio admission where relevant, and sink-side durable resolution.

The V1 action authorization signature is Ed25519 over:

```text
SHA-256("tos.authorized-action-proof.v1\0" ||
        uint32_big_endian(len(canonical_authorized_action_without_proof)) ||
        canonical_authorized_action_without_proof)
```

The canonical object includes `authority_id` and `authority_public_key` and has
an empty `authorization_proof`. The public key must equal the key in the
referenced Writer Fence and must independently resolve as authorized for the
named authority. This proof is deliberately separate from semantic identity:
identity deduplicates an intended effect, while the proof grants permission for
the exact request and policy context.

The registry is not a global transaction database. Each owner and participating
sink retains only the actions it must authorize or resolve. No Carrier, market,
or chain-wide canonical action head is introduced.
