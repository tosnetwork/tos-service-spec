# Agent Operation and Outcome Event V1

**Status:** V1 implementation candidate. The schema, registries, canonical
fixtures, independent verifier, protocol implementation, local journal,
private transport, and bounded Carrier interfaces described by this document
exist on the coordinated implementation branches. Public publication remains
default-off, and no two-independent-operator availability claim is made.

**Scope:** generic, immutable, append-only evidence for Agent operations and
Agreement attempts across runtimes, Carriers, execution systems, custody, and
settlement Adapters

**Depends on:**

- [TOS Agentic Internet Operation Architecture V1](TOS_AGENTIC_INTERNET_OPERATION_ARCHITECTURE_V1.md)
- [Agent Intent Exchange V1](AGENT_INTENT_EXCHANGE_V1.md)
- [Semantic Action Identity V1](SEMANTIC_ACTION_IDENTITY_V1.md)
- [Native Execution Gate V1](NATIVE_EXECUTION_GATE_V1.md)

Names ending in `V1` that are introduced by this document are candidate wire
contracts until the coordinated branches are released. Their implemented
schema, registry, canonical encoding, authority/cardinality rules, stable
errors, vectors, and independent verification are listed in
[the V1 implementation report](AGENT_OPERATION_OUTCOME_EVENT_V1_IMPLEMENTATION.md).
An implementation may advertise only the separately enabled capability it has
passed: read, verify, local append, private send, or bounded publish. It may not
advertise resilient decentralized availability until the independent-operator
gate in Section 20.5 passes. Objects already released by a dependency retain
the status of that dependency.

The fourteen-round independent review and disposition record is
[Agent Operation and Outcome Event V1 Review Report](AGENT_OPERATION_OUTCOME_EVENT_V1_REVIEW_REPORT.md).

## 1. Purpose

TOS needs a business-neutral way to retain what happened after an Agent saw an
opportunity or began an Agreement attempt. A successful payment receipt is not
enough. An Agent must also be able to retain and, when policy permits, exchange
evidence of refusal, withdrawal, Gate rejection, ambiguous start, execution
failure, rework, dispute, refund, timeout, write-off, and actual resource cost.

This specification defines an immutable event layer over existing TOS objects.
It does not replace `AgentOperationEnvelopeV1`, `SemanticActionIdentityV1`,
`AuthorizedActionV1`, `ActionResolutionV1`, Agreement authorization evidence,
`SettlementObligationV1`, execution Receipts, or finalized chain state. It
binds those objects into a causally ordered evidence stream from which each
observer can build a local projection.

The architectural objective is:

> Every attempted Agreement and every authority-changing or externally visible
> operation can leave a bounded, signed, privacy-scoped, replay-safe evidence
> trail, including negative and ambiguous outcomes, without creating a central
> market database or a new business-category workflow.

## 2. Origin in the eight-Agent rehearsal

On 2026-08-27, eight logical OpenFox participants exercised six bounded earning
campaigns over two same-host Carrier processes and three same-host TOS validator
views. The participants offered secure code review, bounded software work,
release-evidence verification, content retention, data normalization, technical
localization, transaction reliability, and Agreement-risk analysis.

The local rehearsal recorded:

- twenty planned cross-Agent trades and twenty distinct local-chain payments;
- forty Carrier observations, one from each Carrier for every planned trade;
- sixty signed, structured discussion contributions;
- a complete Intent-to-finality digest chain for every successful trade; and
- zero errors in the final successful cohort.

Those are useful implementation facts, but they are not evidence of production
reliability or external profit. The Agents and Carriers shared one host and
operator, all value remained inside the campaign-controlled economy, actual
compute and subscription cost was not metered in nanotos, and the successful
cohort contained no rejected, timed-out, failed, disputed, refunded, retried,
or partially accepted Agreement attempts.

The final campaign evidence is recorded by
`tosnetwork/openfox@ad39cbf365d1468189bb78bd15ddc2390ab700ed` in
`docs/operations/bounded-adaptive-earning-campaign-report.md`. Its checkpoint
digest is
`sha256:333eb66b8c0ddd9c3fb2ad7ad15fcd10d8cbdc8e75185a5dbdd2e44dbc766b05`.
The report labels Campaigns 1--4 `INCONCLUSIVE` and Campaigns 5--6 `BLOCKED`.
This specification preserves those evidence limits.

This is an immutable cross-repository reference, not evidence vendored into
`tos-service-spec`; the facts above are externally asserted by that OpenFox
artifact and are not independently proven by this repository. Reviewers resolve
the exact source at
`https://github.com/tosnetwork/openfox/blob/ad39cbf365d1468189bb78bd15ddc2390ab700ed/docs/operations/bounded-adaptive-earning-campaign-report.md`.
Phase 0 must add a signed evidence-manifest digest for the retained external
artifact or vendor a signed snapshot before relying on it as conformance input.

### 2.1 How the roles converged

Each role approached the same missing evidence from a different business
boundary:

| Participant role | Observed gap | Bounded proposal |
|---|---|---|
| Security auditor | A deliverable digest did not prove coverage, and successful rows revealed no maximum-loss path | Bind a coverage manifest and retain failed, disputed, and reworked outcomes with stage and sunk cost |
| Software builder | Repository scope, acceptance tests, rollback, rework, and actual cost were absent | Freeze an implementation envelope and retain every terminal attempt, not only settlement |
| Evidence verifier | Digests were joinable but their verification method, preimages, and independent attestations were not | Use a transport-neutral evidence manifest with explicit pass, fail, or indeterminate result |
| Storage provider | A point-in-time delivery could not prove a continuing retention obligation | Append periodic, Agreement-linked re-attestation and end-of-term events |
| Data curator | Input schema, canonicalization, rejected rows, reversibility, and Gate result were opaque | Bind provenance, normalization, Gate, exception, and outcome evidence |
| Localization writer | Terminology constraints, acceptance outcome, and rework were not represented | Bind content-addressed constraints and retain acceptance/rework transitions |
| Transaction operator | Retry, idempotency, ambiguous send, duplicate-payment, writer takeover, and Gift separation were not observable | Bind stable operation identity, attempt lineage, writer evidence, Carrier acknowledgements, transfer class, and resolution |
| Guarantor analyst | Completion probability had no denominator; expected net was not probability-weighted; repeated scenario values looked like independent samples | Retain every outcome, disclose cohort provenance, and derive risk only from complete, authority-qualified evidence |

Across six rounds the roles stopped proposing profession-specific records and
converged on one generic structure: an append-only operation and outcome event
stream. That convergence is a design input, not protocol authority. The
campaign discussion cannot authorize this specification or any implementation.

### 2.2 Requirements derived from the rehearsal

The shared evidence must:

1. retain negative, ambiguous, partial, and successful outcomes;
2. preserve the existing stable semantic action identity across retry and
   writer takeover;
3. distinguish an Agreement attempt, an authorized action, an execution slot,
   a delivery, a payment obligation, and an entire engagement;
4. bind exact Gate, execution, acceptance, Carrier, settlement, and finality
   evidence without treating all issuers as equally authoritative;
5. distinguish declared ceilings, estimates, allocated cost, metered cost,
   invoiced cost, finalized value, and realized loss;
6. distinguish Agreement-bound value, Gift gratuity, refund, fee, collateral,
   and unrelated transfer;
7. remain useful after a Carrier, runtime, or optional market index disappears;
8. support private evidence and selective disclosure without putting secrets,
   private inputs, prompts, or credentials into a public event;
9. be bounded before signature verification, evidence retrieval, or model use;
10. make exact replay idempotent and conflicting bytes visible;
11. preserve forks and concurrent observations rather than invent a globally
    latest outcome; and
12. never turn a report, model statement, Carrier acknowledgement, or local
    projection into side-effect authority.

## 3. Non-goals

V1 does not define:

- a central job history, market head, reputation database, or global event log;
- a total order across Agents, Carriers, operations, or Agreement participants;
- a new Action ID or a caller-selected idempotency token;
- authority to contact, execute, disclose, sign, settle, refund, or retry;
- a universal reputation score, completion probability, or profitability
  formula;
- raw model transcripts, chain secrets, credentials, private task inputs, or
  unrestricted evidence locators;
- a profession-specific workflow for storage, audit, localization, software,
  OTC exchange, or any other business category;
- proof that an asserted result is true merely because its event is signed; or
- a requirement to put ordinary outcome events on TOS consensus.

## 4. First-principles invariants

### 4.1 An event is an assertion, not automatic truth

A valid signature proves that the resolved issuer made the exact bounded
assertion. Truth depends on the selected evidence profile and authority. A
Carrier may authoritatively attest that it accepted bytes, but not that work
was correct. A runner may attest that a process exited, but not that a payment
finalized. A model may propose a label but cannot produce a terminal economic
fact.

### 4.2 Append-only means new events, not mutable envelopes

There is no mutable `OperationOutcomeEnvelope` row. Each transition is a new
canonical event payload in its own signed `AgentOperationEnvelopeV1`. A
correction, compensation, evidence-availability change, redaction notice, or
reconciliation result appends another event. It never rewrites prior bytes.

### 4.3 Identity, authorization, observation, and projection stay separate

```text
SemanticActionIdentityV1       identifies one semantic side effect
AuthorizedActionV1             authorizes one exact request
ActionResolutionV1             records the responsible sink's resolution
OperationOutcomeEventV1        carries a bounded signed assertion and evidence
LocalOutcomeProjectionV1       derives one observer's current view
```

An outcome event references the first three where applicable. It does not
replace or weaken them. A local projection is rebuildable and never signed as
if it were an issuer fact.

### 4.4 No global head

Each issuer maintains an ordered stream only within a defined issuer/subject
scope. Different participants and services may emit concurrent or conflicting
events. Causal links and qualified authority let an observer derive a view;
they do not create one protocol-global latest event.

### 4.5 Negative evidence is first-class

Refusal, policy rejection, Gate failure, timeout, conflict, indeterminate
resolution, nonpayment, dispute, refund, and write-off are valid results. A
system that exports successful receipts but silently drops negative rows is not
conformant for risk or profitability analysis.

### 4.6 Privacy is enforced before propagation

Hashing a low-entropy secret does not make it public. Event producers minimize
metadata, select an audience before signing and sending, and use encrypted,
content-addressed evidence objects when details are required. Carriers enforce
the declared audience and resource policy but are not evidence authorities.

### 4.7 Verified learning has no authority

An Agent may learn only from authority-qualified terminal evidence and must
retain adverse outcomes. Learning output remains a proposal. It cannot change
budgets, policy, Skills, credentials, settlement Adapters, networking, or
signing authority without the separate controls that already govern those
changes.

`LearningDatasetManifestV1` commits included and excluded assertion roots,
cohort checkpoints, cluster and sampling policy, weights, conflicts, censored
rows, producer concentration, code/build digest, and an evaluation holdout.
`SkillPromotionDecisionV1` binds old/new Skill digests, dataset manifest,
evaluation report, regression and safety thresholds, approver authority,
rollback target, and exact `AuthorizedActionV1`. Learning produces proposal
bytes only. Installation, activation, scope expansion, or rollback requires a
separately registered stable Action, current Writer Fence, owner authorization,
and Gate evaluation. Self-produced evidence is capped or independently
evaluated; disputed, quarantined, incomplete, and out-of-distribution cohorts
cannot promote Skills.

### 4.8 An event stream does not prove its own completeness

An issuer can omit an attempt, delay an adverse event, or stop publishing. A
valid chain proves the integrity and order of included events; it does not prove
that every relevant event was included. Completion-rate, loss, reliability, or
profitability claims therefore require an independently defined denominator:
an authority-qualified admission log or checkpoint, a pre-registered cohort,
and explicit inclusion/exclusion rules. There is no network-wide completeness
claim and no global event checkpoint.

## 5. Relationship to existing objects

### 5.1 `AgentOperationEnvelopeV1`

The root Agent Operation envelope is the only propagation and issuer-signature
wrapper. An outcome event is carried as canonical payload bytes under the
reserved profile URI `tos.operation-outcome.event.v1`. The outer envelope
supplies network, actor, authorization, audience, ordering, lifetime, payload
commitment, and admission metadata. The payload supplies only the
outcome-specific subject, causality, assertion, and evidence commitments.

There is no inner event signature, issuer field, audience, clock, expiry,
sequence, or authorization envelope. The exact outer envelope is the signed
issuer assertion. A verifier rejects an operation whose opcode, payload
profile, `object_id`, payload digest, or ordering profile does not satisfy this
specification.

The outer `operation_id` identifies the signed assertion carrying this event.
It is not the same as the Carrier-specific publication Action, a referenced
economic `stable_action_id`, or the event content ID. Re-publication of the same
exact operation preserves its operation ID and bytes. Before release, the root
Agent Operation specification must freeze a verifier-derived operation-ID
projection; caller-selected operation IDs are forbidden for this profile.

### 5.2 `SemanticActionIdentityV1`

`stable_action_id` and `execution_id` may be copied from the normative registry,
but they are `unverified_reference` values until the exact canonical request,
registry version, and required predecessor/reservation inputs are available and
recomputation succeeds. No retry, successor, terminal Action state,
reconciliation, accounting join, or cross-event grouping may rely on an
unverified reference. Retry, transport, event time, event sequence, issuer
generation, Carrier path, and event digest never enter the semantic Action ID.

Publishing any Agent Operation to a Carrier is externally visible. Phase 0
must release a new, versioned generic `operation.publish` Semantic Action entry
whose semantic key binds owner, publishing Agent, Carrier, exact operation ID,
exact operation-envelope digest, and disclosure/audience profile. It coexists
with the released Intent-specific `publication.publish`; its preimage and IDs
are different and existing IDs never migrate or change. Until that entry and
vectors are released, public outcome-event publication is disabled. Outcome
events do not introduce a special publication authority or reuse the identity
of the Action being described.

Private transport similarly uses a new versioned `operation.private-send`
entry binding owner, sending Agent, exactly one recipient, the recipient's
audience or membership epoch, operation ID, operation-envelope digest,
conversation-scope digest, and transport profile digest. V1 deliberately
forbids a multi-recipient request: one semantic Action and one sink resolution
must never conceal partial fan-out. Sending the same event to a group therefore
creates one independently authorized, fenced, recoverable Action per recipient.
It coexists with generic `messenger.send`; no caller-selected
`authority_instance_id` may hide multiple event sends. A recipient or
membership-epoch change creates a different semantic Action. Timeout,
cross-device retry, and writer takeover query the same Action before any retry.

### 5.3 `AuthorizedActionV1` and `WriterFenceV1`

When an owner-controlled runtime publishes or privately sends an outcome event,
that send uses its own `AuthorizedActionV1`, current Writer Fence, exact event
request digest, policy, mandate, approval when required, and expiry. Retaining a
local-private event in an owner journal does not require network publication
authority, but it still cannot trigger a side effect.

An event may reference the authorization and fence that governed an earlier
action. A stale fence can remain valid historical evidence that an action was
admitted at that time. It cannot authorize a new publication or retry after a
takeover.

### 5.4 Non-circular construction and submission

The immutable assertion and its transport authorization are different objects:

```text
canonical event payload
  -> event_content_id
  -> outer AgentOperationBodyV1
     authorization_ref = issuer/delegation authority only
  -> issuer signs AgentOperationEnvelopeV1
  -> operation_envelope_digest

operation_envelope_digest + carrier/audience request
  -> publication exact_request_digest
  -> operation.publish stable Action + AuthorizedActionV1 + WriterFenceV1
  -> OperationCarrierSubmissionV1
  -> Carrier receipt digest

operation_envelope_digest + conversation/recipient-epoch request
  -> private-send exact_request_digest
  -> operation.private-send stable Action + AuthorizedActionV1 + WriterFenceV1
  -> OperationPrivateSubmissionV1
  -> Messenger ActionResolutionV1
```

The assertion envelope never contains or references its publication/private-send
Action, authorization, submission wrapper, or receipt. The outer
`authorization_ref` resolves only issuer/delegation authority for the signed
Agent Operation. Submission wrappers bind exact envelope bytes by digest and
remain outside those bytes. `operation_id` is the verifier-derived outer-body
projection ID defined in Section 6.2; `operation_envelope_digest` is the common
codec digest of the complete outer body, signature, and historical proof;
publication/private-send `exact_request_digest` covers the destination,
audience/epoch, transport profile, and envelope digest; the receipt digest
covers that request digest, stable Action ID, sink result, sink authority time,
and sink proof. Cycle detection and mutation vectors are mandatory.

### 5.5 `ActionResolutionV1`

The responsible sink remains authoritative for its action admission and
resolution. An outcome event referencing `ActionResolutionV1` must bind its
exact canonical digest and issuer profile. An observer cannot replace an
`unknown` or ambiguous sink result with a model-generated `terminal` event.

### 5.6 Agreement and settlement objects

Agreement authorization evidence determines whether and when an Agreement was
formed. `SettlementObligationV1` and its state determine payment obligations.
Finalized chain state or a selected Adapter's exact evidence determines payment
or refund. The outcome layer links those facts; it does not reinterpret them.

Agent Gift remains gratuity. A Gift event cannot satisfy, offset, or prove
discharge of an Agreement obligation.

## 6. Canonical event payload

### 6.1 Core body

```text
OperationOutcomeEventBodyV1 {
  schema_version: u16
  event_kind: token
  primary_subject_ref {
    subject_profile_uri: profile-uri
    subject_id: id
  }
  causal_predecessor_assertion_refs[]
  assertion_profile_uri: profile-uri
  assertion_payload_digest: digest32
  assertion_payload_size: u64
  evidence_manifest_digest: digest32
  extension_set_digest: digest32
}
```

The body never embeds an unrestricted map. `primary_subject_ref` is the only
core subject identity. Its owning specification defines that identity. An
assertion profile may carry mechanically derived Agreement, obligation,
Action, execution, delivery, transfer, cost, or other references, but it must
define their equality checks and reject inconsistent combinations. The core
never requires sentinel commerce fields from non-commerce operations.

The event-kind and assertion profiles freeze required and forbidden references,
payload schema, qualified assertion authority, and evidence rules. Unknown
required profiles and extensions fail closed. Unknown optional extensions may
be retained but cannot change validity, authority, state, cost, transfer class,
or terminal disposition.

All structure names above encode as CBOR maps with the exact lower-case field
names shown, all strings are valid NFC UTF-8, `u16`/`u64` are unsigned minimal
CBOR integers, and arrays are definite length. The common protocol data model
represents digests as lower-case `sha256:` plus exactly 64 hexadecimal digits.
There are no omitted, null, magic-zero, raw-zero, or empty-string optional
fields in the core. An absent evidence or extension set is represented by the
domain-separated digest of its canonical typed empty structure.

### 6.2 Identity and outer-envelope binding

```text
event_body_bytes = CoreDeterministicCBOR(OperationOutcomeEventBodyV1)

event_content_id = AgentOperationPayloadDigest(
  profile = tos.operation-outcome.event.v1,
  payload = event_body_bytes)
```

V1 public JSON maps to RFC 8949 Core Deterministic CBOR using the common
`tos-service-protocol` JSON data model: no floats, duplicate keys, indefinite
lengths, invalid UTF-8, unknown fields, or non-canonical integers.

`AgentOperationBodyV1.payload_digest` equals `event_content_id`, `payload_size` equals
the exact byte length, `payload_profile` equals the released profile reference,
and `object_id` equals `event_content_id`. The outer Agent Operation signature and its
historical authority proof establish who issued the assertion. The selected
assertion profile determines whether that actor is qualified to make it and
which additional source evidence is required. Adding, removing, or substituting
assertion evidence changes `evidence_manifest_digest` and therefore the event
content ID. The outer signature never turns an unqualified assertion into truth.

The three identities are distinct:

```text
event_content_id       = exact profile-qualified payload content
operation_id           = verifier-derived signed assertion identity
operation_envelope_digest = exact outer body, signature, and historical-proof bytes
```

For this profile, Phase 0 freezes `operation_id` as a domain-separated digest of
the complete canonical `AgentOperationBodyV1` projection with
`operation_id` absent. A verifier recomputes and rejects a mismatch. The exact
projection, outer signature preimage, historical-proof encoding, and envelope
digest are root Agent Operation rules, not locally redefined here. Public
propagation remains disabled until those root rules and cross-language vectors
are released.

### 6.3 Ordering and causality

Issuer-local ordering uses the outer Agent Operation `ordering_domain`,
`epoch`, `sequence`, and `predecessor_digests`; this payload does not allocate a
second sequence. The selected ordering profile defines whether gaps, forks, or
epochs are invalid, retained conflicts, or merely incomplete evidence. A
profile claiming a contiguous admitted-attempt denominator requires a
single-writer lease plus rollback-resistant generation/high-water admission, or
equivalent linearizable semantics. Independently signed observations may use a
non-contiguous ordering profile and remain valid without a coordinator, but
they cannot prove stream completeness.

Each causal reference is:

```text
OutcomeAssertionRefV1 {
  network_id: id
  actor_agent_id: id
  operation_id: id
  operation_envelope_digest: digest32
}
```

`causal_predecessor_assertion_refs` contains at most eight entries, sorted by
their canonical encoding and unique. A bare event content ID is never a causal
reference because different actors and networks can assert the same content.
Causal edges do not create a total order and never substitute for the source
object's own identity or revision rules.

`actor_agent_id` in an assertion reference equals the actor in the referenced
outer Agent Operation. V1 does not hide that routing/verification identity from
authorized recipients or the transporting Carrier. A future audience-scoped
Agent-alias profile may replace it only when the alias has independent identity,
delegation, equality, and historical-resolution rules; an evidence-descriptor
pseudonym cannot substitute for it.

### 6.4 Denominator-capable ordering profile

The reserved profile `tos.operation-ordering.admitted-journal.v1` is required
for any stream used as a complete denominator. Its Phase-0 schema derives
`ordering_domain` from the owner ID, issuer Agent ID, authority ID, journal
purpose, and cohort scope digest. The outer `epoch` equals the
authority-issued Writer Fence generation. Sequence allocation and durable
record append commit at one linearization point under that generation.

A takeover begins a new epoch and commits the prior epoch's last durable
checkpoint and head. The new writer never fills or reuses an old epoch's
reserved sequence. Reserved-but-uncommitted numbers become explicit gaps in
the next checkpoint. Stale-writer records remain quarantined fork evidence and
carry a machine-readable exclusion reason; they are never silently truncated
or included in a complete denominator. A gap, conflicting sequence, rollback,
unproven prior-epoch head, or checkpoint discontinuity makes the affected cut
incomplete. Non-contiguous observational ordering profiles are explicitly
ineligible as completeness sources.

The minimum durable append state machine is `IDLE -> RESERVED -> BYTES_DURABLE
-> HEAD_COMMITTED -> CHECKPOINT_ELIGIBLE`. Under one current Writer Fence
generation, the journal reserves the next sequence, writes a length-delimited
record and checksum, flushes record bytes, atomically replaces the head record
containing sequence/digest/fence high-water, and flushes the containing
directory. A checkpoint may advance only after all covered bytes, head state,
gap inventory, exclusions, and prior checkpoint are durable. Crash in
`RESERVED` publishes a gap; crash after bytes but before head quarantines an
uncommitted record; crash after head replays idempotently. It never reuses a
reserved number.

Takeover first verifies an authority-issued higher-generation proof, seals the
last recoverable old-epoch head/checkpoint and gaps, then opens the new epoch.
A stale writer cannot advance the shared head or checkpoint. Two-process and
two-host matrices crash at every reserve/write/flush/head/checkpoint boundary,
including partition, rollback backup, stale journal replay, and simultaneous
takeover.

## 7. Core event kinds and assertion profiles

The core event kind is deliberately small:

| Core event kind | Meaning |
|---|---|
| `observation` | Reports a source fact without asserting a transition |
| `transition_observation` | Reports a transition defined by the subject's owning profile |
| `terminal_observation` | Reports a scoped terminal disposition defined by an assertion profile |
| `availability_observation` | Reports retention, redaction, or key-destruction state of evidence |
| `cohort_checkpoint` | Commits an authority-scoped denominator or evidence cut |

Commerce assertion profiles then define Agreement-attempt admission and
authorization observations, exact `ActionResolutionV1` observations, Gate and
execution observations, delivery and acceptance observations, obligation and
transfer observations, cost observations, reconciliation observations, and
engagement summaries. Each profile references exact source-object digests and
names the authority already selected by the source specification. It does not
create a generic “coordinator,” “verifier,” or replacement authority.

No kind or assertion profile is a profession. New professions normally add
evidence or deliverable profiles. A new core kind requires shared assertion,
causality, privacy, or admission semantics that a released kind cannot express.

## 8. State and terminal disposition

### 8.1 No single global lifecycle state

An Agreement may contain concurrent obligations and executions. One delivery
can be accepted while another is disputed. V1 therefore has no scalar global
market or engagement state that silently overwrites child state.

```text
StateTransitionPayloadV1 {
  subject_kind
  subject_id
  prior_state
  target_state
  prior_state_revision
  target_state_revision
  transition_reason_code
}
```

The subject's owning specification freezes its graph and authority; the event
profile only records the observed edge and exact source evidence. Concurrent transitions
from one prior revision remain a visible fork until profile-qualified
resolution. Last-write-wins is forbidden.

### 8.2 Terminal disposition

```text
TerminalDispositionV1 {
  terminal_scope
  terminal_subject_id
  owning_state_profile_uri
  authoritative_resolution_digest
  terminal_state_revision
  successor_policy_digest
  disposition
  failure_stage
  failure_code
  retry_disposition
  resolved_at_unix
}
```

The event body's single `evidence_manifest_digest` is the only evidence-set
commitment. Assertion profiles specify required, optional, and forbidden roles,
exact cardinality, and direct-versus-causal evidence rules. Nested payloads
never commit a competing evidence manifest.

Terminal scopes are `agreement_attempt`, `authorized_action`, `execution`,
`delivery`, `obligation`, `transfer_attempt`, and `engagement`. Dispositions are
`succeeded`, `refused`, `withdrawn`, `expired`, `superseded`, `cancelled`,
`failed`, `timed_out`, `conflict`, `disputed`, `refunded`, `written_off`, and
`indeterminate`. Retry dispositions are `forbidden`, `exact_retry`,
`successor_after_terminal`, `owner_review`, `counterparty_action`, and `none`.

Success is scoped. Successful execution does not imply accepted delivery,
payment, profit, or successful engagement. `indeterminate` permits a successor
only where the subject profile explicitly makes it terminal.

`retry_disposition` is descriptive and authorizes nothing. An executor or
coordinator allocates a successor only from the owning state machine's durable,
authority-qualified terminal resolution and performs the atomic successor
transaction required by `SemanticActionIdentityV1`. An Outcome Event, summary,
Carrier acknowledgement, or local projection is never sufficient. In
particular, `AMBIGUOUS_START` remains nonterminal until the owning runner
resolves it under the Native Gate profile.

An engagement summary assertion is qualified only when a released profile derives the
complete required child set from the Agreement and verifies every required
terminal fact. It remains a derived attestation, not a new Agreement or
settlement authority. A self-selected subset is invalid.

## 9. Failure stages

V1 stages are `discovery`, `retrieval`, `policy`, `contact`, `agreement`,
`reservation`, `funding`, `input`, `gate`, `execution`, `delivery`,
`acceptance`, `billing`, `settlement`, `finality`, `reconciliation`,
`not_applicable`, and `unknown`.

Failure codes are bounded, versioned, lower-case ASCII names such as
`gate.network_destination_denied`. Free-text exceptions, stack traces, URLs,
filesystem paths, prompts, and private content are forbidden in public or
participant-visible canonical payloads. A private detail object may be
referenced by digest under a separate audience and retention policy.

## 10. Evidence and authority

### 10.1 Evidence manifest

```text
OutcomeEvidenceManifestV1 {
  schema_version
  manifest_purpose
  authority_proof_refs[]
  evidence_items[] {
    evidence_role
    evidence_profile_uri
    source_object_profile_uri
    source_object_digest
    object_digest
    canonical_size
    media_type
    issuer_descriptor
    subject_descriptor
    claimed_observation_time_unix
    authority_time_proof_digest
    issuer_qualification_proof_digest
    visibility
    audience_digest
    retention_policy_digest
    retrieval_policy_digest
  }
}
```

The manifest is constructed independently and its digest is then committed by
the event body; it never contains the event ID, event-body digest, or another
field that depends on its own digest. Evidence objects may bind the subject,
Action, Agreement, execution, or obligation directly. This one-way construction
prevents circular hashes.

```text
evidence_manifest_digest = CodecDigest(
  "tos.operation-outcome.evidence-manifest.v1",
  OutcomeEvidenceManifestV1)

OutcomeExtensionSetV1 {
  schema_version: u16
  extensions[] {
    profile_uri: profile-uri
    canonical_value: bytes
  }
}

extension_set_digest = CodecDigest(
  "tos.operation-outcome.extension-set.v1",
  OutcomeExtensionSetV1)
```

Items and extensions are sorted by their complete canonical encoded bytes,
strictly increasing and unique. V1 always commits the digest of the typed
structure, including the canonical empty structure; a zero sentinel or omitted
digest is invalid. Unknown extension bytes remain inside the committed set and
cannot be interpreted as authority.

`authority_proof_refs` is a sorted unique array of at most 16 canonical proof
object descriptors. Every authority-qualified item references exactly one
member whose issuer, key, scope, subject, and authority-time proof equal the
item fields. Assertion profiles enumerate required roles, eligible principals,
time rule, direct-versus-causal rule, and cardinality. Unreferenced proofs,
partial proof unions, unexpected duplicate roles, and field mismatch are
invalid.

Before cryptographic verification, authority material is limited to 64 KiB
aggregate and 8 KiB per referenced proof, 16 delegation links, 64
revocation/checkpoint proof nodes, 32 Ed25519 signature checks, and 1,024 hash
operations per event. V1 permits no pairing operation. A future proof profile
using other cryptography must publish a stricter operation-cost schedule and
admission charge. Exceeding any bound returns `resource_exhausted` before
persistence or retrieval.

`claimed_observation_time_unix` is descriptive and never selects historical
authority. Every authority-qualified item commits an authenticated authority
time proof:

```text
AuthorityTimeProofV1 {
  profile_uri: profile-uri
  authority_or_checkpoint_id: id
  interval_start_unix: u64
  interval_end_unix: u64
  finalized_high_water: u64
  finalized_root_digest: digest32
  proof_digest: digest32
}
```

The assertion profile selects the applicable time: authenticated sink admission
time for Action admission/resolution, finalized checkpoint or chain time for
Gate/finality facts, and the Agreement evidence profile's authorization time
for Agreement formation. Current validity is checked at the actual evaluation
or admission time while historical issuer/delegation state is resolved at the
authenticated authority time. Missing, future, issuer-chosen, rolled-back,
forked, or ambiguous time evidence fails closed.

Every qualified assertion also references:

```text
IssuerQualificationProofV1 {
  root_authority_id: id
  issuer_agent_id: id
  issuer_key_digest: digest32
  ordered_delegation_chain_digest: digest32
  scope_profile_uri: profile-uri
  subject_scope_digest: digest32
  valid_from_unix: u64
  valid_until_unix: u64
  revocation_handle_set_digest: digest32
  authority_time_proof_digest: digest32
  revocation_high_water: u64
  revocation_root_digest: digest32
}
```

Assertion profiles enumerate the exact eligible principal, sink, custody role,
Agreement-selected role, scope equality rules, and authority-time profile.
Verification fails on a missing delegation link, subject/profile mismatch,
expiry, revocation effective at or before authority time, unavailable history,
fork, or rollback. Role labels in prose never suffice.

For public evidence, issuer and subject descriptors may be released stable
identifiers only when their source disclosure policies permit it. For every
non-public audience they are audience-scoped pairwise pseudonyms; encrypted
qualification evidence binds each pseudonym to the actual principal. A
descriptor is never itself identity authority.

An assertion that an Action was admitted, an execution started, or a writer was
current additionally requires the exact `AuthorizedActionV1` digest, complete
`WriterFenceV1`, authenticated sink admission receipt, admission authority-time
proof, and generation/lease/instance/high-water proof. Owner, Agent, authority,
key, generation, lease, action kind, stable Action ID, and exact-request digest
must all match. A bare fence, signature, or event timestamp is invalid.

Evidence items are sorted by their complete canonical encoded bytes, strictly
increasing and unique; role, profile, and digest are not a separate ordering
key. A locator is not authority and is not embedded. Retrieval uses owner-configured origins and
SSRF, DNS, redirect, TLS, proxy, credential-origin, compressed/expanded-size,
fan-out, and timeout controls. Digest and size are checked before parsing.

### 10.2 Authority matrix

| Assertion | Required authority | Insufficient evidence |
|---|---|---|
| Agreement proposal admitted | proposal sink and exact signed proposal | transcript, UI state, or model text |
| Agreement formed | complete profile-qualified authorization for one body | one party's summary or partial predicate union |
| Action admitted or resolved | responsible sink's exact resolution and action binding | caller journal alone |
| Writer was current | resolved fence and authority high-water at admission | bare generation integer |
| Gate result | selected Gate over exact policy, plan, inputs, resources, credentials, and effects | runner or model assertion |
| Execution transition | task-scoped runner/broker plus one-shot slot evidence | model completion text |
| Delivery released | delivery broker and exact manifest | payment or chat acknowledgement |
| Delivery accepted | Agreement-selected acceptance authority | provider self-assertion unless selected |
| Transfer finalized | finalized TOS state or selected Adapter finality evidence | Carrier receipt, HTTP success, or wallet intent |
| Gift occurred | exact finalized Gift evidence | conversation association |
| Obligation satisfied | exact obligation plus qualifying evidence | unrelated Gift or same-amount transfer |
| Cost incurred | selected meter, invoice, or finalized fee evidence | declared ceiling or estimate |
| Carrier accepted bytes | that Carrier's receipt | payload truth or global availability |
| Engagement terminal | verifier over complete Agreement-derived children | selected successes or missing adverse rows |

Conflicting authority-qualified events are retained. A verifier applies only
released precedence and otherwise remains indeterminate. Signature count,
Carrier count, arrival time, and model confidence are not implicit truth rules.

## 11. Cost and economic evidence

```text
CostObservationPayloadV1 {
  subject_kind
  subject_id
  cost_item_id
  cost_class
  category
  asset_identity_digest
  amount_atomic: u128
  economic_direction
  quantity_digest
  meter_interval_digest
  meter_unit
  invoice_identity_digest
  payment_request_digest
  meter_or_invoice_evidence_digest
  accounting_policy_digest
  incurred_at_unix
  original_cost_assertion_ref
}
```

Cost classes are `declared_ceiling`, `estimate`, `usage_measured`,
`payable_invoiced`, `cash_finalized`, `allocated`, `contra`, `penalty`, and
`write_off`. `economic_direction` is `debit` or `credit`; amounts remain
unsigned atomic quantities. Categories
are `compute`, `model`, `api`, `tool`, `storage`, `network`, `labor`, `capital`,
`chain_fee`, `collateral`, `dispute`, and `other`.

Ceilings and estimates are not realized cost. Usage proves measured
consumption, while an invoice proves a payable claim; neither proves cash
payment. Allocated values remain labeled and bind their accounting policy.
Evidence is mandatory for usage, invoice, cash, contra, penalty, and write-off
claims. Corrections and reversals append a contra event naming the original
assertion; both remain visible. Profit reports expose unpaid invoices and
contra entries separately and count only policy-selected classes.

Different assets are never summed without separate conversion evidence binding
source, time, rate, fee, and rounding. Expected profit and probability are
local projections, not cost events.

### 11.1 Reproducible ledger and economic perimeter

```text
EconomicLedgerEntryV1 {
  entry_id: digest32
  book_id: id
  accounting_entity_id: id
  accounting_policy_digest: digest32
  recognition_basis: token
  effective_at_unix: u64
  posting_at_unix: u64
  source_assertion_ref: OutcomeAssertionRefV1
  transaction_group_id: digest32
  lines[] {
    account_code: token
    debit_or_credit: token
    asset_profile_uri: profile-uri
    asset_instance_id: id
    amount_atomic: u128
  }
  reverses_entry_id: digest32
}
```

Lines balance exactly per asset. Meter, invoice, payment, and allocation events
are source facts, not postings until the selected accounting policy maps them.
One fact is recognized at most once per book and basis. Corrections reverse the
exact prior entry and post a replacement. Collateral principal is a restricted
asset, not expense; only fees, impairment, or slashing may become cost. Capital
and labor require explicit capitalization/expense and allocation policies.

`EconomicPerimeterV1` commits controller, beneficial-owner, related-party and
funding-origin sets plus a validity interval. `RevenueRecognitionV1` binds the
obligation, payment assertion, seller and buyer perimeters, relationship,
consideration asset, gross/recognized amounts, and policy. External revenue
requires authority-qualified evidence that payer funding and beneficial control
are outside the seller perimeter. Related-party, intra-perimeter, unknown,
circular, and campaign-funded value is reported separately and excluded from
external revenue and profit.

### 11.2 Asset conversion, forecasts, and reports

`AssetConversionEvidenceV1` binds source/target assets and versions, source
atomic amount, rational numerator/denominator, spot/executed/period-average
type, price-source profile and evidence, quote/validity times, fee, rounding,
and target atomic amount. Checked integer/rational arithmetic, stale-rate
rejection, source precedence, triangulation policy, and realized-versus-market
gain separation are mandatory; floats are forbidden.

An `OutcomeForecastV1` binds issuance authority time, model artifact, feature
cut, cohort policy, target profile, horizon, and integer probability in ppm.
Issuance precedes outcome evidence. `CalibrationReportV1` binds forecast/outcome
sets, censoring and cluster policies, scoring rule, exact rational Brier/log
scores, and bin specification. Cluster dimensions include controller,
counterparty, fund source, host, runtime, Carrier, model/Skill version,
campaign, and shared template. Reports publish unique-cluster counts and a
frozen variance method; without correlation identifiers, confidence or
significance claims are forbidden.

`FinancialReportV1` binds report ID, event/cohort roots, authority/finality
cuts, accounting book/policy, economic perimeter, reporting asset, conversion
evidence root, timezone/window, software build and registry digests, arithmetic
profile, ledger root, unknown/conflict/exclusion sets, prior report, restatement
reason, and output digest. Cross-language golden vectors reproduce ledger,
cohort, conversion, calibration, and report bytes.

A profitability or completion report declares the exact cohort manifest,
inclusion and exclusion predicates, window, every terminal and unknown count,
duplicate/supersession rules, evidence threshold, missing-evidence count, and
the independence of counterparties, hosts, Carriers, and funds. A success-only
stream cannot support completion probability or maximum-loss claims.

For a claim of complete admitted attempts, the cohort manifest also binds an
authority-qualified, append-only admission checkpoint containing the admission
scope, authority epoch, contiguous sequence interval, predecessor/head event
IDs, admitted-attempt count, event-set commitment, policy revision, and cutoff
time. The checkpoint proves completeness only for that named authority and
scope through that cutoff. It cannot prove unsubmitted attempts, events hidden
before admission, another authority's history, or network-wide completeness.

```text
CohortCheckpointPayloadV1 {
  schema_version: u16
  admission_authority_id: id
  ordering_domain: id
  authority_epoch: u64
  previous_checkpoint_digest: digest32
  first_sequence: u64
  last_sequence: u64
  admitted_attempt_set_root: digest32
  admitted_attempt_count: u64
  eligible_attempt_set_root: digest32
  eligible_count: u64
  excluded_attempt_set_root: digest32
  excluded_count: u64
  exclusion_reason_histogram_digest: digest32
  included_attempt_set_root: digest32
  outcome_cutoff_unix: u64
  followup_policy_digest: digest32
  censoring_set_root: digest32
  censored_count: u64
  explicit_gap_set_digest: digest32
  fork_inventory_digest: digest32
  inclusion_policy_digest: digest32
  admission_closure_state: token
  outcome_closure_state: token
  cutoff_unix: u64
}
```

The admitted-attempt set is a canonical sorted Merkle set of exact admission
operation references, not publisher-selected outcome events. Checkpoints are
monotonic and predecessor-linked. Overlap with different membership,
replacement without exact predecessor, count/root mismatch, hidden gaps,
conflicting closure, or late admission before a closed cutoff is equivocation
and makes the cut incomplete. A `closed` cohort is complete only if every
committed admission resolves to an authority-qualified terminal fact or an
explicit `unknown`; `unknown` remains in all rates and loss bounds.

`admitted_attempt_count = eligible_count + excluded_count`; exclusions never
disappear and their predicates are frozen before outcomes are inspected.
`OutcomeCensoringV1` binds attempt reference, admission time, observation end,
censor kind/reason, and last authoritative state. Right-censored attempts stay
in the admitted denominator and are not silently relabeled failed or unknown.
Reports give success bounds: lower is successes/admitted; upper is
`(successes + censored + unresolved) / admitted`. Admission closure and outcome
completion are independent.

Right-censored and `unknown` are distinct: censored means the observation window
ended under a declared follow-up policy before a terminal fact; `unknown` means
the required fact or evidence cannot currently be resolved. A row may not be
counted in both sets at one cut. Every typed empty cohort set uses the released
domain-separated empty-set root. The only empty interval encoding is
`first_sequence = 0`, `last_sequence = 0`, count zero, and the typed empty root;
range fields are ignored only in this exact case. For a non-empty interval both
sequences are nonzero and `first_sequence <= last_sequence`.

Merkle leaves are
`SHA-256("tos.outcome.cohort.leaf.v1\0" || canonical_assertion_ref)` and nodes
are `SHA-256("tos.outcome.cohort.node.v1\0" || left || right)`. Leaves sort by
canonical reference bytes and duplicates are invalid. An odd node is promoted
unchanged to the next level; it is never duplicated. The unsigned leaf count is
committed beside the root. V1 permits at most `2^32 - 1` leaves, proof depth 32,
256 proof nodes, 16 KiB proof bytes, and 512 hash operations per admission.
Count, range, epoch, and checkpoint predecessor are checked before membership
proofs.

## 12. Transfer classification

Every value event selects exactly one class:

| Class | Meaning |
|---|---|
| `agreement_bound` | Bound to one exact Agreement obligation instance |
| `gift` | Gratuity with no consideration or counter-obligation |
| `refund` | Return bound to an exact prior payment or obligation |
| `fee` | Network, Carrier, Adapter, or service fee |
| `collateral` | Locked value with exact release, slash, and expiry terms |
| `unrelated` | No asserted relation to this Agreement |
| `unknown` | Relationship cannot be proven |

Coincidental payer, recipient, amount, asset, or time establishes no class. A
Gift cannot satisfy or offset an Agreement obligation.

The released Gift observation profile requires the exact Gift BOC, network
domain, destination-credit/finality chain, and Gift profile identity, and
forbids Agreement, obligation, and payment-request references. The separate
Agreement-payment observation profile requires the exact Agreement body,
obligation instance, payment request, payer, payee, asset, amount, destination,
stable Action/request identity, and Adapter evidence. Profile substitution is
invalid even if transaction, parties, asset, and amount happen to match.

### 12.1 Obligation state and evidence consumption

```text
AgreementObligationStateObservationV1 {
  agreement_body_digest: digest32
  agreement_obligation_id: id
  obligation_instance_id: digest32
  obligation_digest: digest32
  payment_request_digest: digest32
  prior_revision: u64
  target_revision: u64
  prior_paid_amount_atomic: u128
  applied_amount_atomic: u128
  target_paid_amount_atomic: u128
  target_outstanding_amount_atomic: u128
  applied_payment_evidence_set_digest: digest32
  owning_billing_profile_uri: profile-uri
}
```

Every transfer evidence identity is consumable by exactly one payment request
and obligation instance unless the Agreement itself freezes a canonical
multi-obligation allocation. The transition checks exact atomic arithmetic and
rejects cross-Agreement, cross-obligation, duplicate, overpayment, asset,
party, destination, or Adapter replay. A partial payment remains nonterminal;
an ambiguous, disputed, or reversed amount retains exposure.

The billing registry freezes distinct assertion profiles and owning state
edges for obligation materialization, partial payment, full satisfaction,
overdue, dispute opened/resolved, write-off, refund, and reversal. Each profile
defines source authority, prior/target revision, amount arithmetic, evidence
roles, terminality, reservation effect, and whether a later transition is
permitted. Implementations cannot infer these edges from a generic disposition.

Transfer resolution states are `observed_unproven`, `corroborated_terminal`,
`validator_finalized`, `reversed`, and `finality_indeterminate`. The selected
Adapter/finality profile freezes precedence and maturity. Reversal is not a
refund: it binds the original transfer assertion and authoritative reversal
proof, appends a new obligation revision, restores or adjusts outstanding
value, and appends a revenue contra entry. A refund is a new intentional
transfer bound to its prior payment or obligation. No engagement can be
`succeeded` while any required obligation is partial, ambiguous, disputed,
reversed, overdue, or missing authority-qualified evidence.

### 12.2 TOS escrow observation profile

`tos.outcome.transfer.tos-escrow.v1` uses the escrow contract's owning state
machine and records distinct `funding_observed`, `principal_locked`,
`release_submitted`, `release_finalized`, `refund_submitted`,
`refund_finalized`, `bounce_recovery`, `fee_finalized`, and
`finality_indeterminate` assertions. Each binds the exact Accepted Quote,
Agreement/obligation instance, escrow account, contract code/config, stable
Action and request, transaction bytes/hash, finalized checkpoint, amount/asset,
and authority/finality proof.

Locked principal is collateral, not revenue or expense. Obligation payment
evidence is consumed only at the profile's finalized destination-credit point,
never at funding, submission, Carrier/RPC acknowledgement, or pending contract
state. Release and refund are mutually exclusive terminal economic resolutions
for the same locked principal except for explicitly separated fee lines. A
bounce, reorg, or authoritative reversal appends its own assertion, restores
the exact outstanding obligation/reserve required by the owning state machine,
and is resolved before retrying the same Action. Old-query replay, duplicate
release/refund, zero-bounce failure, fee substitution, and cross-escrow evidence
reuse fail closed.

## 13. Privacy and selective disclosure

Visibility is one of `local_private`, `named_participants`,
`named_recipients`, or `public`. The body and evidence descriptors use an
audience no broader than every referenced object.

```text
AudiencePolicyV1 {
  schema_version: u16
  network_id: id
  audience_kind: token
  recipient_principal_key_set_digest: digest32
  group_id: id
  membership_epoch: u64
  membership_root_digest: digest32
  permitted_purpose_set_digest: digest32
  onward_disclosure_rule: token
  expires_at_unix: u64
  policy_revision: u64
}
```

Every non-public outer operation and evidence item commits an
`audience_policy_digest`. Named-recipient membership binds sorted principal and
encryption-key IDs. Group membership binds an immutable epoch and membership
root. Evidence audience must be a verifier-provable subset of the outer event
audience. Retrieval requires authenticated requester membership at that epoch,
permitted purpose, and an unexpired capability bound to object digest, audience
policy, resolver profile, and maximum bytes. Failure or indeterminate subset,
membership, purpose, or expiry evaluation denies access.

Public bodies and manifests never contain credentials, bearer tokens, private
inputs, deliverables, prompts, transcripts, stack traces, filesystem paths,
internal hosts, unrestricted URLs, unauthorized personal data, undisclosed
Agreement terms, low-entropy secret hashes, or exact private economics when a
coarser profile was selected.

No externally disclosed commitment is an unsalted digest of
attacker-enumerable content. Such content uses a context-separated hiding
commitment with at least 128 bits of fresh randomness stored only inside
authorized encrypted evidence. Public and participant-visible descriptors use
policy-approved pairwise pseudonyms and bucketed size, time, and media classes.
Commitment randomness and correlation scope are never reused across audiences,
Agreements, projections, or retention epochs.

These descriptor protections do not hide the outer Agent Operation actor,
audience routing metadata, or causal-reference actor from the Carrier and
authorized recipients. Implementations and reports disclose that residual
linkability rather than describing the envelope as anonymous.

A public summary is a new signed `OutcomeDisclosureProjectionV1` binding every
transitive source assertion, source disclosure-policy digest, source audience
epoch, projection profile, field-granular disclosed/omitted/bucketed labels,
derivation profile, composition-budget ID, audience, purpose, expiry, retention,
and projection issuer. It is not the source event and cannot satisfy a
full-evidence requirement. A verifier computes the union of disclosed and
inferable fields across all inputs and previously issued projections in that
budget. Composition succeeds only when every source policy permits that exact
audience, purpose, derivation, and union. Unknown policy, omitted provenance,
audience widening, or budget exhaustion fails closed.

Non-public evidence uses a released authenticated-encryption envelope binding
the schema version, cipher suite, key-reference digest, object digest,
audience-policy digest, retention-policy digest, evidence role, and canonical
size as associated data. Keys are per object or retention epoch and wrapped
only to authorized recipient keys; nonce reuse is forbidden.
Retention policy fixes expiry, deletion deadline, cache and backup treatment,
legal-hold behavior, and required custodian acknowledgements.

Propagation expiry stops compliant future forwarding; it does not erase copies
or invalidate historical signatures. Destruction states are `requested`,
`partially_attested`, `custodian_attested`, and `unverifiable`. A destruction or
redaction event names each controlled replica/custodian and never claims
deletion from other systems or recipients. Post-expiry retrieval and key unwrap
fail unless a disclosed legal-hold rule applies.

Evidence locators come only from authenticated resolver records keyed by object
digest; they never appear in events, manifests, projections, errors, or logs.
The resolver applies `ContentRetrievalPolicyV1` before every DNS lookup,
connection, redirect, proxy choice, and retry. Credentials are purpose-limited
handles bound to exact origin, resolver profile, object, audience, requester,
and expiry. Ambient credentials and credentials derived from content, locator,
Carrier, redirect, proxy, or model output are rejected.

## 14. Carrier and spam rules

Carriers transport exact envelopes or content-addressed references, may index
disclosed metadata, and may issue Carrier observation events. They cannot alter
bytes, choose a global head, infer missing events do not exist, or promote their
acknowledgement to Agreement, Gate, execution, or settlement truth.

V1 bounds before profile-specific tightening are:

| Resource | Maximum |
|---|---:|
| Canonical event body | 64 KiB |
| Canonical event payload | 64 KiB |
| Outer Agent Operation envelope for this profile | 128 KiB |
| Causal predecessors | 8 |
| Evidence items | 64 |
| Authority evidence references | 16 |
| Typed extensions | 16 |
| Extension bytes | 16 KiB total |
| Identifier or profile URI | 256 UTF-8 bytes |
| Failure code | 128 lower-case ASCII bytes |
| Public propagation lifetime ceiling | 30 days |

Receivers use this fixed admission pipeline:

```text
bounded framing
-> raw origin/connection token bucket
-> declared-length checks
-> streaming bounded structural CBOR scan
-> scarce admission capability check
-> content hash and untrusted negative/duplicate cache
-> signature verification
-> authenticated actor quotas
-> bounded authority-proof verification
-> persistence
-> optional separately-budgeted evidence retrieval
```

Default pre-authentication limits per Carrier are 10 events/second and 1
MiB/second burst per network origin, two concurrent validations per origin, and
a global signature queue no larger than twice the available CPU cores. Queue
overflow rejects without persistence. Actor quotas apply only after signature
and identity authentication. A cache hit never establishes validity.

The streaming CBOR scanner has depth at most 16, at most 2,048 total items, at
most 128 entries per map, at most 16 KiB per individual text/byte string, at
most 64 KiB aggregate decoded payload bytes, and no tags, shared references,
indefinite lengths, duplicate/non-NFC keys, or trailing bytes. It checks
declared collection sizes before allocation and map-key order incrementally;
it never materializes an unrestricted generic value tree.

Every untrusted submitter presents an expiry-bound scarce admission capability
before signature work: authenticated customer quota, prepaid byte-and-CPU
ticket, or adaptive proof of work. Accounting charges separately for ingress
bytes, signature and authority-proof work, retained byte-days, retrieval bytes,
and fan-out. Malformed, duplicate-conflicting, or unavailable-evidence
submissions receive no refund. Admission economics affect only this Carrier,
never event validity or reputation.

One projection processes at most 10,000 unique assertions, causal depth 64,
40,000 edges, 1,024 unresolved references, 64 MiB working memory, and two
seconds CPU/wall budget. Exceeding any limit returns
`resource_exhausted/incomplete`, never a partial `complete` result. Evidence
retrieval is opt-in and limited per operation to 32 objects, 64 MiB expanded
bytes total, four origins, four concurrent requests, two redirects, five
seconds per request, and twenty seconds total. Negative results cache by
object, retrieval policy, and authority cut.

Carriers retain at most two full conflicting envelopes per ordering-domain,
epoch, and sequence, plus a domain-separated accumulator/root and counters for
further conflicts. Quarantine obeys tenant disk quota; excess conflicts retain
audit commitments only. Default TTL is 24 hours unless storage is explicitly
purchased; 30 days is a protocol ceiling, not an entitlement. Availability
transitions are capped at 16 per object and retention epoch and repeated states
are coalesced.

Rebuild begins from an operator-configured signed checkpoint/head allowlist,
exchanges manifests and set differences before bytes, verifies chunk hashes,
limits a request to 64 MiB and two peers concurrently, and caps daily ingress at
the smaller of ten percent of free disk and the tenant quota. Received content
never supplies recursive source discovery. Expired payload bytes may be
garbage-collected while bounded tombstone and checkpoint commitments remain.

## 15. Projection and reconciliation

```text
verified bounded events
  -> group by exact subject and issuer scope
  -> verify sequence and causal links
  -> resolve authority for each assertion
  -> retain conflicts and missing evidence
  -> apply the selected state graph and authority precedence
  -> derive local state, accounting, risk, and learning views
```

A conforming projector is a pure function of the canonical assertion set,
projection profile, authority-resolution cut, chain/finality cut, policy
revision, and explicit evaluation time:

1. validate bounds and canonical bytes, then sort by complete assertion
   reference encoding;
2. reject duplicate references with different bytes and retain them as input
   conflicts;
3. build the transitive causal closure; retain unresolved references as
   `missing`, never silently prune or fetch during projection;
4. resolve issuer and assertion authority at the frozen authority cut;
5. group by exact owning subject and state-machine profile;
6. apply owning revision/predecessor rules, retaining sibling transitions as a
   conflict set;
7. apply only explicitly released authority precedence; count or arrival time
   never breaks a tie;
8. derive scoped terminals only after causal/source-evidence closure; and
9. emit canonical state, missing, conflict, exclusion, and unknown sets.

`OutcomeEventSetV1` is the sorted unique assertion-reference list plus each
exact envelope digest. `event_set_digest` and the final projection digest use
separate released `CodecDigest` domains. The projection binds that event-set
digest, all input cuts and revisions, explicit evaluation time, and projection
profile. Reordered delivery of identical inputs must produce identical bytes.
It is derived data and authorizes nothing.

Reconciliation dry-run is read-only. Apply uses `reconcile.apply`, current
Writer Fence, owner authorization, stable Action ID, exact evidence cut,
crash recovery, and an audit event. Late evidence produces a new projection;
it does not edit an old report. Unknown or conflict reserves risk and fails
closed under owner policy.

## 16. Security and failure analysis

| Threat or failure | Required behavior |
|---|---|
| Retry to the same Carrier | Same `operation.publish` stable Action and exact request; query before idempotent retry |
| Publish through another Carrier | Preserve assertion operation ID/envelope digest; create a separate authorized Carrier-bound publication Action |
| Same scope/sequence with different bytes | Retain equivocation; never choose by arrival time |
| Stale writer publishes after takeover | Sink rejects against current fence/high-water |
| Action result lost | Query same stable Action ID/request; append when resolved |
| Caller chooses fresh ID after timeout | Registry recomputes original identity |
| Carrier invents success | Receipt proves only Carrier observation |
| Provider self-accepts work | Invalid unless Agreement selected that authority |
| Same-amount Gift closes invoice | Invalid class and obligation binding |
| Public low-entropy input hash | Disclosure violation |
| Locator targets local metadata | Retrieval denied before request |
| Estimate is reported as realized | Invalid cost promotion |
| Success-only export feeds learning | Incomplete cohort; reject learning input |
| Event disappears from one index | Rebuild from retained bytes/other sources |
| Qualified authorities disagree | Apply released precedence or remain indeterminate |
| Wall clock rolls backward | Compare expiry against `max(authenticated_time_high_water, current_authenticated_time)`; persist the high-water before admission and never decrease it |
| Evidence is redacted | Append availability event; preserve historical limit |

## 17. Repository change plan

### 17.1 `tos-service-spec`

- Freeze the core schema, registries, failure stages, dispositions, evidence,
  cost, transfer, disclosure, privacy, spam, and retention rules.
- Add deterministic CBOR, signing, sequence, fork, disclosure, size, and error
  vectors plus a code-independent verifier.
- Add generic `operation.publish` to `SemanticActionIdentityV1` with exact
  Carrier, operation-envelope, audience/disclosure, retry, and conflict rules;
  retain the Intent-specific `publication.publish` entry unchanged, with no ID
  rewrite or aliasing.
- Add `operation.private-send` with exactly one recipient per Action, the
  recipient's audience/membership epoch,
  conversation/transport profile, envelope identity, query-before-retry,
  ambiguous delivery, device-takeover, and membership-change vectors.
- Bind carriage through `AgentOperationEnvelopeV1` and distinguish event
  content ID, outer assertion operation ID/envelope digest, and referenced
  Action ID.
- Update Intent, earning, Gate, Messenger, settlement, Gift, relay, and
  guarantor documents to reference this layer rather than redefine it.

This repository defines interoperability but stores no operational history.

### 17.2 `tos-service-protocol`

- Implement typed core/payload structures, deterministic codec,
  digest/signature helpers, strict bounds, registries, and stable errors.
- Implement scope derivation, sequence/predecessor checks, equivocation,
  causal-DAG verification, disclosure validation, and deterministic projection.
- Reuse existing Agreement, Action, fence, resolution, billing, Gift, payment,
  relay, guarantor, and Gate validators.
- Expose event, event-set, authority, and projection APIs with streaming
  verification that fetches no evidence by default.
- Consume the independent positive, mutation, replay, fork, takeover, privacy,
  size, and mixed-version corpus.

Package naming must not narrow the core to paid work.

### 17.3 `openfox`

- Append local-private events for decisions and every Agreement attempt,
  including refusal, expiry, withdrawal, Gate failure, execution failure,
  rework, nonpayment, dispute, refund, and write-off.
- Publish only through policy, current Writer Fence, `AuthorizedActionV1`,
  stable publication identity, bounded audience, and disclosure projection.
- Add a crash-safe append-only journal with sequence high-water, equivocation
  quarantine, authority-scoped admission checkpoints, import/export, query, and
  source-loss rebuild.
- Use checksummed length-delimited records, an atomically replaced head record,
  an explicit data-and-directory durability boundary, torn-tail quarantine,
  rollback-detecting checkpoint/head linkage, and deterministic recovery of
  reserved-but-uncommitted sequences. Never repair by silently truncating a
  signed or checkpoint-committed branch.
- Make Engagement, Portfolio, scheduler, billing, accounting, reconciliation,
  reports, and learning consume complete authority-qualified evidence.
- Separate ceilings/estimates from actual costs, Gifts from obligations, and
  controlled internal transfers from external revenue.
- Migrate existing journals without fabricating absent historical evidence.

### 17.4 `tos-messenger`

- Transport exact encrypted events/evidence with audience membership, bounds,
  stable send identity, Writer Fence, and query-before-retry. Dedupe exact
  assertions only by network, actor, operation ID, and envelope digest;
  `event_content_id` is payload caching only and never merges issuers.
- Issue signed Carrier observations limited to acceptance/delivery facts.
- Preserve issuer bytes across retry, device sync, membership epochs, and
  retention changes.
- Test duplicates, withheld/reordered events, stale epoch, ambiguous send, and
  cross-device takeover.

Messenger derives no Agreement, acceptance, payment, or global outcome truth.

### 17.5 `tos-service-gateway` and other Carriers

- Publish, resolve, and subscribe to exact events or safe projections using
  source-local cursors and provenance.
- Index disclosed metadata only; preserve forks and avoid a canonical head.
- Enforce admission, TTL, audience, quota, fan-out, retrieval, and spam budgets.
- Rebuild after complete database loss only from named, authorized retention
  custodians/sources in the release manifest, with checkpoint roots, minimum
  retention through the tested cut, and required decryption-key availability.
- Prove two independent implementations/operators before decentralized
  availability claims.

### 17.6 `tos-ai` and execution systems

- Emit Gate results over exact Agreement, plan, input, Skill/model, sandbox,
  resources, network, credentials, disclosure, and planned effects.
- Bind one-shot start ticket, slot, start linearization, runner, attempt lineage,
  terminal state, and output manifest.
- Meter resource use honestly and mediate post-start effects through released
  Action identities.
- Never infer payment, acceptance, or profit from execution success.

### 17.7 `tos`, custody, and `tosctl`

- Expose prepared, submitted, rejected, ambiguous, and finalized transfer
  evidence bound to Action ID, request, network domain, asset, amount,
  destination, validity, and signed transaction bytes.
- Preserve query-before-retry and resolution across restart.
- Produce qualified direct-payment, refund, fee, collateral, sponsorship,
  relay, and guarantor-payout evidence.
- Distinguish local RPC observation from finalized network evidence.
- Reject event publication as a bypass around custody or contract policy.

V1 requires no new chain opcode or consensus state. Optional future anchoring
needs separate justification and cannot make the off-chain stream complete.

### 17.8 External settlement, storage, and service Adapters

- Freeze request, resolution, finality, reversal, privacy, retention, and
  failure profiles.
- Bind the same stable Action and request across response, timeout, webhook,
  polling, and reconciliation.
- Distinguish Adapter acceptance from final settlement.
- Reject bearer-only evidence, unrelated transfer, substitution, replay, and
  partial evidence union.

### 17.9 Optional market applications and analytics

Applications may rank, summarize, moderate, price, or visualize disclosed
events. They label derived fields, publish cohort rules, retain source
commitments, honor visibility, and never claim complete market coverage or
Agent, Agreement, execution, settlement, or outcome authority.

### 17.10 Accountable ownership and API contracts

| Responsibility | Accountable repository/component | Required boundary |
|---|---|---|
| schemas, profile registry, vectors, release manifest | `tos-service-spec` | signed versioned corpus and commit manifest |
| production codec/verifier and independent verifier fixtures | `tos-service-protocol` plus separately implemented verifier | language-neutral conformance API |
| journal, checkpoints, projections, reports | `openfox` | append/checkpoint/project API |
| delegation and historical authority resolution | `tos-service-protocol` API backed by selected identity/custody authority | no network fetch inside structural verification |
| encrypted evidence store and key lifecycle | selected OpenFox storage provider; profile named in deployment manifest | capability-scoped resolve/fetch/delete-attest API |
| Gate/execution evidence | `tos-ai` or selected executor repository | exact Gate/slot/runner evidence API |
| custody/finality evidence | `tos`, `tosctl`, or selected Adapter named in manifest | prepared/submitted/resolved/finality API |
| private transport | `tos-messenger` | send/resolve/subscribe with Action identity |
| first public Carrier | `tos-service-gateway` deployment named in manifest | publish/resolve/subscribe/checkpoint API |
| second independent Carrier | separate implementation/operator named before resilience gate | same wire contract, independent failure domain |

Phase 0 publishes language-neutral fixtures for `decode`,
`verify_structural`, `resolve_authority`, `verify_evidence`, `append`, `publish`,
`resolve`, `subscribe`, `checkpoint`, and `project`, including request/response
types and stable errors. Structural and streaming verification performs no
retrieval by default. Retrieval is an explicit caller-supplied capability with
budgets and provenance.

All production components export privacy-safe metrics for stable decode and
verification errors, unsupported profiles, gaps/forks, stale writers, journal
durability/checkpoint lag, projection unknown/conflict counts, ambiguous
publication, Carrier divergence, retrieval denial, evidence availability,
migration progress, and consumer version distribution. Logs bind operation and
envelope digests plus repository build IDs, never private payloads, evidence,
locators, credentials, or stable private-party identifiers.

## 18. Dependency and delivery order

```text
S0  tos-service-spec schemas/profiles/registries/vectors
R0  separately implemented verifier
P0  tos-service-protocol codec/verifier/API
S0 + R0 + P0 -> local conformance

P0 -> J1  OpenFox experimental local journal
P0 -> E1  selected Gate/executor evidence producer
P0 -> D1  selected custody/settlement evidence producer
P0 -> M1  Messenger transport
P0 -> C0  first named Carrier

J1 + E1 + D1 -> authority-qualified local projections
S0 + P0 + J1 + M1 + operation.private-send vectors
  -> cross-device private-transport canary
S0 + P0 + J1 + C0 + operation.publish vectors
  -> allowlisted Carrier-publication canary
C0 + C1 named independent Carrier -> resilient propagation
all selected producers + C0 + C1 -> accounting, learning, and campaigns
```

Local-private capture may ship before public propagation, but it cannot claim
interoperability until S0/R0/P0 vectors pass. Public propagation remains
default-off until privacy, spam, source-loss, and independent-Carrier gates
pass.

## 19. Compatibility and migration

V1 is additive. Existing Agreements, Actions, Receipts, Gifts, transfers, and
chain state remain valid. Implementations may emit events for new observations
only and never fabricate historical sequence, Gate, cost, failure, or
acceptance evidence.

Historical import retains exact original bytes and authority, uses a labeled
local import observation, marks missing data `unknown`, keeps success-only
cohorts incomplete, never changes existing Action resolution, and permits old
peers to ignore optional outcome payloads while ordinary Intent and Agreement
operation continues.

Peers advertise support separately for the outer opcode/payload profile, event
schema, assertion profiles, ordering profile, evidence profiles, extension
profiles, and registry revision. The compatibility matrix for each combination
states whether a peer may `read`, `store`, `relay`, `verify`, `project`, or
`emit`. Unknown required semantics fail closed. Unknown optional committed bytes
may round-trip but never affect authority or projection. An unsupported member
of a contiguous stream produces an explicit gap and makes that cut incomplete;
“ignore” never means silently skip. Downgrade is forbidden when authoritative
state cannot be represented.

Migration shadow-imports into a new versioned namespace, preserves original
bytes, deterministically maps each legacy record, records restartable migration
checkpoints, and compares source/destination counts and digests before cutover.
Duplicate mappings are idempotent; success-only sources stay labeled
incomplete. `operation.publish` is added alongside `publication.publish`; no
existing registry entry, preimage, or ID is rewritten or aliased.

Deployment gates are:

1. schema/registry freeze and signed corpus;
2. agreement by production and independent verifiers;
3. protocol library release;
4. consumer read-only ingestion;
5. OpenFox local shadow-write and projection comparison;
6. selected producer canaries;
7. one-Carrier private allowlisted canary;
8. two-Carrier database-loss recovery;
9. bounded public emission; and
10. reporting and learning enablement last.

Every repository gates `accept`, `emit`, `publish`, `project`, and `learn`
independently. Rollback disables new emission/publication, preserves and exports
accepted bytes and registry versions, reverts consumers to read-only, and never
destructively down-migrates a journal or Carrier database. Already published
immutable operations are not described as “rolled back.”

## 20. Conformance and acceptance gates

### 20.1 Schema and codec

- Two independent implementations reproduce canonical bytes, digests, event
  IDs, signatures, scope IDs, sequences, and failure classes.
- Mutation of authority, subject, audience, payload, evidence, state, cost,
  transfer, time, predecessor, and extension fields is detected.
- Duplicate keys, unknown required profiles, floats, overflow, invalid UTF-8,
  non-canonical CBOR, trailing bytes, oversize, and excessive nesting fail
  before expensive work.
- Replay is idempotent and conflicting same-scope/sequence bytes equivocate.

### 20.2 Authority and recovery

- Stale writer, forged fence, unauthorized key, partial Agreement evidence,
  wrong Gate, runner substitution, Carrier inflation, unrelated payment, Gift
  substitution, and finality substitution fail.
- Timeout recovery uses the same Action and event scope.
- Fork, two-process append, two-host takeover, stale journal, rollback, delayed
  evidence, and authority conflict remain deterministic.
- Publication and reconciliation cannot bypass Action Authority, Portfolio,
  custody, Gate, or Adapter policy.

### 20.3 Privacy and resource safety

- Private input, prompt, credential, path, host, counterparty, cost, and
  low-entropy-secret tests do not leak through public fields or indexes.
- Unauthorized projection composition fails.
- Retrieval rejects local/private addresses, DNS rebinding, redirects,
  untrusted proxy, credential forwarding, compression bombs, fan-out, and wrong
  digest/size.
- Replay/equivocation floods remain within CPU, memory, storage, network,
  signature, and inference budgets.

### 20.4 Economics and learning

- Reports include every terminal class, unknown count, cohort manifest,
  exclusion, evidence threshold, and independence boundary.
- Estimates never count as realized cost; controlled transfers never count as
  external revenue; missing negatives block probability/loss claims; Gifts
  never close obligations.
- Success-only, conflicted, unauthorized, or incomplete evidence cannot
  activate a Skill or enlarge authority.

### 20.5 Decentralized propagation

- Two independently implemented and operated Carriers preserve bytes and
  source-local provenance.
- Complete deletion of one Carrier database permits authorized rebuild only
  when the tested signed corpus, keys, manifests, and checkpoint roots still
  exist at the named independent retention sources. Without those sources the
  claim is limited to integrity verification of whatever bytes remain.
- No implementation asserts a global latest event or complete market history.
- Carrier or market loss cannot change Agreement, Action, settlement, or chain
  truth.

## 21. Release status and remaining operational gates

The implementation candidate closes the protocol decisions that previously
blocked Phase 0. This table is normative about claim scope; code existence does
not substitute for operational evidence.

| Decision or artifact | Candidate status | Remaining release or deployment gate |
|---|---|---|
| Core schemas, canonical encoding and structural bounds | Implemented in the V1 schema and protocol codec | Freeze coordinated repository commits and publish the release manifest |
| Profile and stable-error registries | Implemented as generated, sorted registries | Registry revisions must be immutable after release |
| Ordering domain, operation ID, construction DAG and append semantics | Implemented with append authority high-water and exact request binding | Externally pin signed checkpoints to detect whole-directory rollback |
| `operation.journal.append`, `operation.publish`, and `operation.private-send` identities | Implemented with exact-byte vectors; private send is exactly one recipient per Action | Every deployed sink must persist action resolution and fence high-water |
| Historical Agent-operation and evidence authority | Implemented through explicit resolver APIs and authenticated pinned profiles | A deployment must retain superseded pins or select and name a historical delegation provider |
| Observation time and authority-time qualification | Implemented with bounded intervals and pinned proofs | Deployment clock and proof-retention policy must be named in its manifest |
| Disclosure, audience, hiding commitment and anti-composition fields | Implemented; public release also passes an owner-authored declassification policy | Public profile/audience allowlists remain default-deny |
| Encrypted evidence | Implemented with AES-256-GCM, random 96-bit nonces and authenticated schema, suite, key reference, object, audience, retention, role and size context | The selected storage provider must define key rotation, nonce-volume limits, retention and deletion attestation |
| Agent Operation payload mapping and Messenger type | Implemented without a new consensus opcode | Peers advertise the exact payload/profile revisions they accept |
| Independent verification | Implemented by the Python reference verifier over the language-neutral corpus | CI ownership and immutable release artifact location must be recorded |
| Carrier propagation | Two separate implementations exist: the Gateway HTTP Carrier and OpenFox directory Carrier | Resilient-public claims require two independently operated failure domains and a witnessed database-loss recovery campaign |

Local-private capture, verification, projection, archive and private transport
may be deployed after their selected release artifacts are frozen. Bounded
public publication may be enabled only with explicit declassification policy,
pinned Carrier receipt keys, quotas and action fencing. Cross-host risk-learning
and resilient decentralized-publication claims remain disabled until their
corresponding Section 20 gates have operational evidence.

## 22. Final design test

The design succeeds when a failed storage renewal, rejected translation,
ambiguous relay, disputed audit, refunded software milestone, and successful
evidence-verification job use the same event core while retaining their exact
profile authority and evidence.

If a new profession requires a new core state machine, the design has failed.
If a signed event can authorize a side effect, turn a Carrier into truth, reveal
private work, erase a fork, relabel an estimate as realized cost, or manufacture
a missing denominator, the design has failed.
