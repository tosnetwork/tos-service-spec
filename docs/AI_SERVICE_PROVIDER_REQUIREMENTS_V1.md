# TOS AI Service Provider — Product Requirements & Architecture V1

**Status:** Proposed product requirements; not a frozen wire profile, implementation
completion report, or deployment approval. The general inference profile is an
incubation design subject to the existing expansion gate.

**Date:** 2026-11-14  
**Specification baseline reviewed:** `3d94e459d55c3d8f56c56c0c299df716f4378b14`  
**Implementation baseline reconciled (`main`):** `tos`
`5af405dcb1f523be0ff3b812e9f6945275c4945b`, `tos-service-protocol`
`62f5b740bc7778b809ad136fca7fc4f222a7be03`, `tos-service-gateway`
`7cefe92d0c9075a69d12eaa4964973e2e7ed0323`, `tos-ai`
`b41e7496d26e64db5cee114c6c5c320aa2030278`, OpenFox
`6eb93009d24e9e390f1659871ecac07541abea82`. Statements below about current
behavior refer to these commits; reconciliation is source reading, not
acceptance evidence.  
**Scope:** Provider onboarding, service publication, discovery, bounded execution,
and native-TOS payment through the existing TOS Service Protocol authority model.

## 1. Purpose and authority

Enable an independent operator to offer a useful AI-related service to humans and
Agents, accept an explicitly authorized purchase, perform the work on equipment
or infrastructure the operator controls, and receive native TOS with independently
checkable settlement evidence.

The intended experience is:

> Connect a service, establish an Agent identity, publish a Capability, accept a
> bounded order, deliver its result, and get paid without making one marketplace
> database the source of truth.

**TOS Provider** is the working name for this operator experience. It is not a new
protocol, token, registry, custody service, mandatory marketplace, or necessarily
a new repository. AI execution remains off-chain. TOS supplies shared identity,
authorization, immutable service commitments, and the selected economic rules.
Offering a service must not itself require becoming a validator, surrendering
hardware, or granting a Gateway access to private signing keys.

This document is subordinate to:

- [Root Agentic Internet architecture](TOS_AGENTIC_INTERNET_OPERATION_ARCHITECTURE_V1.md)
  and [system architecture](ARCHITECTURE.md) for layer and authority boundaries;
- [product strategy](PRODUCT_STRATEGY.md) and [roadmap](ROADMAP.md) for delivery
  priority, expansion eligibility, and acceptance evidence;
- [Native Registry state machines](NATIVE_REGISTRY_STATE_MACHINES.md) for identity
  and Capability transitions; and
- [settlement](SETTLEMENT.md), [Service Actor TVM](SERVICE_ACTOR_TVM_V1.md), and
  [Service Actor settlement binding](SERVICE_ACTOR_SETTLEMENT_DESIGN.md) for the
  current native-TOS commercial path.

MUST, MUST NOT, and SHOULD express requirements on the proposed product release,
not assertions that those requirements are implemented. This document assigns no
new opcodes, signing domains, schema fields, or contract semantics. Any required
normative extension must be specified, reviewed, encoded, and tested separately.
Committing this document does not change any roadmap gate or deployment status.

## 2. Product scope and delivery order

### 2.1 First delivery: one usable software-work service

Package and complete the existing machine-checkable software-work path first:
publication, discovery, exact Quote review, funded Service Actor request,
bounded execution, attested response or timeout refund, and independent
reconciliation. Examples are a pinned compilation or test service.

The first acceptance exercise must involve a new provider and a buyer outside the
core development team, with independent resolution of the result. A local demo,
a registered Agent, or a successful RPC submission is insufficient.

### 2.2 Expansion design: bounded model inference

After the roadmap expansion gate opens, add a separately versioned inference
Capability profile and reviewed adapters for operator-controlled model servers.
The reference use case is an operator offering a bounded text-generation or
summarization request from a local model server, such as an Ollama or vLLM
backend. These are target adapter integrations, not current compatibility claims.

A provider may eventually wrap an authorized remote API instead of owning a GPU.
The service must disclose that dependency and its data-handling implications.
An API wrapper must not be represented as independently proven local execution.
Model ownership, operating control, and authorization to resell access are distinct.

The first inference slice should be fixed-price, bounded, and non-streaming.
It must not masquerade as a software-work operation or silently add fields to the
frozen software-work manifest. Documentation and design can proceed now;
implementation and commercial activation follow the existing expansion rules.

### 2.3 Non-goals

This release does not introduce bare-metal rental, permissionless arbitrary
container execution, autonomous installation of buyer-selected models, model
training, a global reputation score, subjective arbitration, guaranteed AI-answer
correctness, cross-chain settlement, stablecoin settlement, per-token chain
transactions, or a new high-frequency payment channel. General messaging and free
services are not required to enter a paid Service Actor workflow.

## 3. Existing foundations and implementation honesty

Reuse these foundations rather than creating parallel authority:

| Foundation | Source or controlling document | Requirement for this product |
|---|---|---|
| Agent identity and immutable Capability versions | [Registry state machines](NATIVE_REGISTRY_STATE_MACHINES.md) | Preserve current ownership, policy, recovery, revocation, and network binding. |
| Provider publication SDK | [Provider SDK](https://github.com/tosnetwork/tos-service-protocol/blob/main/docs/provider-sdk.md) | Reuse prepare, external signing, exact submission, and finalized resolution. |
| Provider onboarding | [Gate E provider onboarding](GATE_E_PROVIDER_ONBOARDING.md) | Turn the public procedure into a repeatable operator workflow. |
| Native-TOS purchase and settlement | [Settlement](SETTLEMENT.md) | Use Service Actor `call`, `respond`, and refund paths, not the retired stablecoin escrow. |
| Local execution and provider deployment | [TOS AI foundation](https://github.com/tosnetwork/tos-ai/blob/main/README.md) and [deployment template](https://github.com/tosnetwork/tos-ai/blob/main/deploy/provider/README.md) | Reuse container isolation and bounded resources (`pkg/executor`), the single-owner at-most-once job journal (`pkg/softwarework`), content-addressed artifacts (`pkg/artifactstore`), and finalized pending-request admission (`pkg/railgate`). Custody separation is a documented deployment boundary; `tos-ai` itself holds no signer. |
| Provider runtime loop and buyer composition | OpenFox `pkg/servicebridge` | Reuse the existing admit/execute/respond/redeliver provider loop (which drives `tos-ai` and signs through pinned `tosctl`) and the policy-gated Service Actor buyer flow rather than building a parallel runtime. |
| Discovery and alternative delivery paths | [Gateway discovery](GATEWAY_DISCOVERY_V1.md) (`tos-service-gateway`, `tos-service-protocol/pkg/capabilitycatalog`) and [federation](GATEWAY_FEDERATION_V1.md) (`tos-service-protocol/pkg/gatewayfederation`; the Gateway currently serves only its well-known descriptor) | Keep catalogs and routing replaceable and non-authoritative. |

Source presence, historical tests, and current-domain product acceptance are
separate. The `tos-ai` documentation records removal of old inference and
stablecoin-escrow-bound transport surfaces. Neither their old documentation nor
an archived successful run proves a current inference, A2A, or MCP path works.
No model adapter, A2A binding, or MCP binding is currently wired to the Service
Actor rail. Conversely, current-rail pending-request admission does exist
(`tos-ai/pkg/railgate`, composed by OpenFox `pkg/servicebridge`), although the
`tos-ai` README still says such a gate "is not provided here" and its own
`cmd/software-work-execute` does not use it. The first implementation task must
reconcile current code, documentation, release hashes, and executable evidence
for the exact Service Actor path. A component's presence must not be used to
infer full cross-repository integration.

The following remain deliverables of this proposal unless independently accepted:
a cohesive provider installation/onboarding experience, the new inference
profile, each claimed model adapter, current-rail transport integration,
operator-facing accounting, and external end-to-end product acceptance.

## 4. Actors and architecture

| Actor | Responsibility | Authority it must not acquire implicitly |
|---|---|---|
| Provider owner | Select services, keys, resources, admission policy, and prices | Authority over the buyer's wallet or undisclosed upstream data use |
| Provider Agent | Publish authorized identity and Capability actions | Unlimited access to the owner's machine or recovery keys |
| Buyer Agent or human client | Select exact terms and authorize bounded spending | Control over the provider's host, models, or signer |
| Provider runtime | Admit and execute authorized jobs, retain outputs and local evidence | Registry control, unrestricted wallet signing, or chain settlement truth |
| Separate signer/custody boundary | Authorize allowed identity, wallet, and Receipt operations | A blind signing API reachable by untrusted job content |
| Gateway, Carrier, or index | Discover, relay, deliver, and expose derived views | Canonical identity, ownership, payment, or execution authority |
| Resolver/verifier | Reconstruct claims from exact objects and chain evidence | Authority to invent finality or decide subjective result quality |

```text
Buyer runtime / owner policy
        |
        | discovery and negotiation through replaceable paths
        v
Provider offer + finalized Agent / Capability / Service Actor terms
        |
        | reviewed wallet authorization -> finalized Service Actor call
        v
Provider admission gate -> durable execution claim -> approved local adapter
        |                                             |
        |                                      off-chain result
        v                                             v
Separate attestor custody <- validated Receipt and content commitments
        |
        | owner-authorized respond, or timeout/refund processing
        v
Finalized Service Actor outcome -> provider revenue -> separate withdrawal
```

The chain executes contracts, not every AI model call. Prompts, source inputs,
model weights, progress events, and bulk outputs stay off-chain. On-chain state
holds the authority and commitments required by the selected profile. A signed
operation establishes only the assertion its signer is authorized to make.

## 5. Provider onboarding and daily operation

### PRV-01 — Install and diagnose

Provide a documented Linux reference deployment with pinned releases and a
machine-readable preflight report. Check selected backend reachability, resource
limits, disk capacity, time synchronization, chain/network configuration,
resolver health, signer availability, and supported contract/profile versions.
Installation must not silently open a public inference port or import wallet
secrets into the executor. Unsupported configurations fail with actionable errors.

### PRV-02 — Establish identity and custody

Guide the owner through fresh controller creation, recovery preparation, Agent
registration, and exact finalized-state verification. Reuse `tosctl` custody and
the current Native Registry policy rather than accepting a private-key field in
the Provider SDK or Gateway. Distinguish the Registry Agent identity, its
controller keys, a funding wallet, the Service Actor owner, and its attestor.
Their relationship must be explicitly verified; a similar display name is not
an authorization binding.

### PRV-03 — Configure one approved service

The owner selects the exact backend, supported operation, allowed inputs, output
bounds, execution policy, evidence level, retention policy, price, and resource
budget. Only approved local adapters and operator-installed artifacts may run.
A buyer's request cannot become an arbitrary shell command, container image,
model download, tool installation, or network destination.

### PRV-04 — Preview, sign, publish, and resolve

Preview the Agent, Capability version, manifest digest, network/genesis, endpoint
binding, Service Actor address/code identity, attestor, commercial terms, and
estimated costs before any signing. Reuse the Provider SDK's prepare/sign/apply
workflow (`cmd/tos-service-provider-publish`). The SDK itself persists no
provider state; it is restartable only when the operator retains the prepared
action, nonces, and retry keys and re-runs `apply` with them, so the product
must persist those before signing. The current CLI does not yet preview the
Service Actor, attestor, terms, and costs. Publication succeeds only when exact finalized
Capability state matches the submitted action. Catalog admission and transport
acknowledgement must be displayed separately from chain publication.

A new provider must complete this workflow from public documentation without
editing a Gateway database, patching repository source, or using private developer
instructions. The acceptance target is one operator working session, measured
with prerequisites and interventions reported separately, not a promised number
of minutes.

### PRV-05 — Operate, pause, and recover

Provide CLI/API-visible readiness, admitted jobs, deadlines, resource use,
unknown outcomes, refunds, revenue, withdrawals, and actionable failure reasons.
Support stopping new admission, draining admitted jobs, pausing a backend,
rotating authorized keys through their proper lifecycle, and publishing a new
Capability version. A pause must not confiscate customer funds or erase already
accepted terms. Recovery must work without the original Gateway database.

### PRV-06 — Explain product state accurately

Use distinct states for configured, published, discoverable, quoteable, funded,
executing, result available, responded, refunded, swept, revenue credited,
withdrawal submitted, withdrawal finalized, and outcome unknown. These are local
UI projections of the relevant facts, not new contract states. Do not label
source code, a listing, an RPC acknowledgement, or credited contract revenue as
money already received in a provider wallet.

## 6. Capability publication and discovery

### CAP-01 — Bind the exact service

Use a finalized Capability version whose immutable manifest commits to the
selected service profile, input/output schemas, execution restrictions, endpoint
or transport binding, execution authority, and settlement binding. Verify the
owner Agent and applicable revocation state before new purchases. A changed
manifest requires a new version; existing version bytes cannot be overwritten.

Keep the manifest off-chain and content-addressed. Do not place the derived
Capability ID inside the manifest bytes from which that ID is derived. Every
accepted encoding must be bounded, canonical, and supported by positive and
negative conformance vectors.

### CAP-02 — Separate offers from authority

Discovery results may include categories, descriptions, indicative prices,
availability, and local ranking. Identify which fields are issuer assertions,
chain-derived facts, or index-local observations. A listing is not a live Quote,
capacity reservation, payment authorization, or guarantee of result quality.
Do not imply that one search result set is a globally complete directory.

### CAP-03 — Support replaceable discovery paths

Use current Native publication and derived discovery first. Make signed service
information and exact manifest bytes recoverable through alternative allowed
paths. ARD interoperability is an optional future mapping to a pinned external
specification, not a prerequisite for the first direct sale and not a claim that
a global ARD deployment already exists. External listings must resolve back to
TOS authority and may not replace it.

## 7. Quotation, authorization, and settlement

### PAY-01 — Verify and display complete terms

Before payment, the buyer independently verifies the exact network/genesis,
Provider Agent, Capability/version, manifest, transport binding, Service Actor
address and released code hash, attestor, current policy version, `terms_hash`,
service price, non-refundable storage fee, request limits, and deadlines.
Enforce per-purchase, aggregate outstanding, and daily spending budgets through
owner-controlled policy. Unresolved submissions continue consuming reservations.
Current code provides a per-call maximum and count/total caps over a rolling
window (`buyersdk`; OpenFox `servicebridge` adds an open-purchase cap and owner
confirmation above a threshold); a distinct calendar-day budget is not yet
implemented.

The buyer must refuse an actor that does not snapshot the manifest-bound
attestor for new requests, as [settlement design](SERVICE_ACTOR_SETTLEMENT_DESIGN.md)
steps 5 and 7 already require (`has_attestor = 1`). The contract itself accepts
an owner `respond` without any signature when no attestor is configured or after
`revoke_attestor`, so this refusal is a client obligation; the current Buyer SDK
enforces it in `serviceactor.VerifyAdmission` before funding and again on the
request snapshot.

For the current rail, amounts are canonical unsigned integer nanoTOS strings
with checked arithmetic within the contract's Coins bound. Do not use floating
point in signed economic terms. Display service price, storage fee, network
fees, and any separately authorized optional service charges distinctly. The
current actor also requires the `call` value to cover a fixed 0.2 TOS admission
gas allowance above price and storage fee; the unused part returns as change and
must not be shown as a charge. The contract does not itself require a non-zero
price, so the product must reject a zero-price paid offer explicitly.

### PAY-02 — Keep one canonical commercial path

A purchase is one Service Actor `call` carrying `request_hash`, the quoted
`expected_terms_hash`, and the required funds. In the current Buyer SDK,
`request_hash` is the hash of the NSR1 ServiceRequest cell, which binds the
Accepted Quote hash, the execution ID, and the input digest; it is not the
Accepted Quote commitment itself. The contract treats it as an opaque 256-bit
value. The buyer obtains the contract-assigned request ID and committed terms
from the finalized call and its `SAR1` request snapshot. The `get_request`
getter answers only while a request is pending: `expire` moves it to
`get_refund`, and `respond`, `claim_refund`, or `sweep_expired_request` delete
it, so recovery after resolution depends on the retained snapshot and
transaction history. A proposal, signed
Quote alone, HTTP response, or Gateway ledger entry does not create an accepted
on-chain purchase.

A `call` can also be refused for reasons such as an inactive actor, an
unauthorized caller, the daily rate limit, a live-request capacity cap (global
or per caller), an unfunded operating reserve, or a failed policy-bounds check. These refusals must surface as
pre-execution failures, with the buyer verifying where the attached value
actually went, and never as a started job.

A separate native-coin Task Escrow contract (`task-escrow-code.fc`, `tosctl
agent task`) still exists in `tos` but is not connected to the Service
Actor; it is not part of this product's commercial path.
The initial product does not add a second Task Escrow, facilitator balance,
stablecoin rail, or Gateway-managed balance around that call. Native TOS pays for
the service as well as the applicable network costs. Do not assume an Energy
credit, fee waiver, sponsorship service, or shielded commercial path exists unless
the exact selected implementation and profile independently support it.

### PAY-03 — Respect the actor's pricing model

Initially charge a fixed amount for one bounded request. A Quote must match the
actor's actual price and terms; a Gateway cannot invent a per-buyer price. Use
supported policy/version handling or separately configured actors for distinct
price tiers, preserving existing requests' snapshots.

Token usage may be reported for observability, but must not silently change the
settled price. Per-token charging, prepaid balances, partial billing, subscriptions,
streaming payments, batching, and channels need separate specifications and
review. Never send one chain transaction for each generated token.

### PAY-04 — Admit execution only after verified funding

Before running paid work, verify the finalized call, pending request, exact
Quote/input binding, authority, resource reservation, and remaining deadline.
Read each logical chain view at a coherent checkpoint and preserve the approved
resolver's rollback/finality protections. Multiple URLs owned by one operator do
not establish independent operators; RPC agreement is not automatically a portable
validator-finality proof. Expose the assurance actually available. The current
Native resolver (`toschain`) requires a strict majority of 3–8 endpoints with
distinct host:port authorities and keeps a persisted checkpoint high-water mark,
but it does not bind endpoints to operators. Operator independence is therefore
a configuration responsibility until the resolver enforces it.

A short-lived local capacity reservation may reduce stale quotations. It is not
a chain guarantee. Do not begin with insufficient time for execution, result
persistence, signer checks, transaction inclusion, and the actor's deadline. If
capacity is lost after funding, preserve the order and its refund rights instead
of changing its price, provider, model, or deadline.

### PAY-05 — Preserve exact resolution semantics

| Event | Current Service Actor consequence | Required product behavior |
|---|---|---|
| Valid `call` finalized | Funds and terms are bound to a request; attestor key (if any), price, fee, bounty, and deadlines are snapshotted | Record the exact actor/request identity before execution. |
| Owner `respond` before the response deadline | Price and storage fee become provider revenue. The snapshotted attestor's ML-DSA-44 signature (domain `SRP2`) is required only if the request snapshotted an attestor; otherwise the owner's message alone settles | Verify the Receipt and finalized response; report revenue credit, not wallet payout. Attestor-less settlement never arises for an admitted request; the product refuses such actors per PAY-01. |
| No valid response by the response deadline | Permissionless `expire` (between response deadline and refund-claim deadline) marks the request refundable | Trigger or explain `expire` and the caller's claim path. |
| Caller sends `claim_refund` before the refund-claim deadline | Price is paid to a caller-chosen destination; the storage fee is credited to provider revenue | Verify the actual terminal transaction and account for non-refundable fees. |
| Pending or refundable request reaches the refund-claim deadline | Permissionless `sweep_expired_request` (no prior `expire` needed) returns the price to the caller and pays the sweeper a 0.1–1 TOS cleanup bounty from the storage fee; the provider is credited `storage_fee − bounty` | Maintain a bounded keeper/watch process; time passing alone is not a transaction. |
| Owner sends `withdraw_revenue` | Separate payout of at most the smaller of accrued revenue and the balance left after pending, refundable, and locked liabilities and a 1 TOS operating reserve; the message must carry a 0.2 TOS payout gas allowance (as must `claim_refund` and `sweep_expired_request`), returned as change | Verify the withdrawal outcome and wallet credit before claiming received funds. Reject a zero-amount withdrawal in the product; the contract does not. |

The storage fee is not refunded; network fees already incurred are not undone.
An operator may offer a separate voluntary commercial refund, but it is not a
new contract remedy and requires a separately authorized transfer.

### PAY-06 — Do not promise nonexistent arbitration

The current actor verifies the sender, pending state, deadline, and, when the
request snapshotted an attestor, that attestor's SRP2 signature over the
response commitment. It does not decode the entire Receipt or judge whether an
answer is correct or useful. Without a snapshotted attestor no signature is
checked at all. A valid attested
response can settle without buyer approval. Evidence of a signed but
non-conforming Receipt is not an automatic on-chain refund or slashing remedy.
The UI and documentation must disclose this trust boundary before purchase.

## 8. Execution, retry, and failure requirements

### EXE-01 — Enforce local resource authority

Enforce finite CPU, RAM, GPU/VRAM, concurrency, queue, context/input, output,
wall-clock, disk, artifact, network, and retention limits appropriate to the
backend. GPU visibility must follow operator-approved device assignments; a
claim of isolation requires backend-specific evidence. Current `tos-ai` assigns
GPUs through operator-fixed CDI device mappings with exclusive leases and
enforces a device count only; it has no per-job VRAM limit (its resource guard
checks host-level VRAM capacity, not per-job use). Run no unbounded queue
while waiting for chain or model availability.

The provider remains responsible for its own infrastructure. Private container
runtime sockets must not be exposed to a Gateway, buyer, model process, or
untrusted job. Containers and approved model servers receive no controller,
wallet, recovery, or attestor private keys.

### EXE-02 — Claim once across processes and transports

One semantic purchase must map to one durable execution claim across direct
calls and all enabled adapters. Persist the canonical actor/request and Quote
identity, exact input binding, execution identity, and state transitions. Use a
process-independent atomic claim when several workers share the same service.
The current `tos-ai/pkg/softwarework` journal is durable and crash-safe but is
owned by one process per directory (an exclusive lock makes a second process
fail rather than share claims), and the reference deployment uses a per-job
state directory; a shared multi-worker claim store remains to be built.
Changing HTTP retry keys, transport, Gateway, or connection must not purchase a
second execution or charge.

An ambiguous submission or crash requires resolution, not blind re-signing,
rebroadcast under a new intent, or automatic rerunning. Persist exact authorized
transaction bytes and the submission lease before sending. Rebuild safe chain
observations after restart; do not infer that an off-chain execution never ran
merely because a local file or remote response is missing. Unknown execution
outcomes remain quarantined until safely resolved or timed out. This is
at-most-once admission, not a claim of guaranteed exactly-once completion.

### EXE-03 — Bind inputs and outputs

Verify input commitments and declared sizes before execution. Reject path
traversal, symlinks where forbidden, archive/decompression bombs, unsupported
encodings, and unauthorized fetch destinations before privileged processing.
Bind every result and artifact to the exact job and retain it under the agreed
policy. Nondeterministic model output must not be advertised as reproducible
simply because a seed was recorded.

### EXE-04 — Handle cancellation and degradation honestly

Cancellation may stop local work under owner policy, but is not an immediate
on-chain refund instruction unless the selected contract supports that effect.
Document the remaining timeout/refund path. If the resolver, signer, journal,
backend, storage, or required evidence becomes unavailable, stop new affected
admissions. Do not fall back to a different model, signer, endpoint, payment rail,
network, or weaker assurance without a new explicitly authorized purchase.

## 9. Proposed inference Capability profile

This section specifies requirements for a future profile, not wire field names
or an accepted manifest schema. The existing software-work enum and canonical
encoding remain unchanged.

| Subject | Required semantics before profile freeze |
|---|---|
| Operation and schemas | Precisely bounded text-generation or summarization input/output; unsupported operations rejected. |
| Model identity | Immutable model/version reference; weights or artifact digest when available; quantization, adapters, tokenizer, and chat-template identities where relevant. |
| Evidence of model use | Distinguish declared model identity from evidence that those weights actually ran; disclose unverifiable upstream aliases. |
| Runtime | Approved backend and version, execution environment identity, and allowed options; no caller-supplied arbitrary runtime. |
| Request bounds | Maximum encoded input bytes, context tokens, generated tokens, stop conditions, runtime, queue residence, and concurrent work. |
| Economics | Fixed native-TOS price, storage fee, actor binding, deadlines, and refusal/refund semantics. |
| Data handling | Retention/deletion policy, logging policy, processing location claims, and explicitly allowed upstream recipients. |
| Output acceptance | Objective delivery/schema/limit conditions, treatment of refusal and truncation, and separate disclosure of semantic-quality limitations. |
| Evidence and signing | Receipt schema, input/result commitments, exact attestor authorization, and assurance label. |
| Compatibility | Canonical encoding, strict bounds, extension/rejection rules, version migration, and independently reproduced vectors. |

Freeze the intended behavior for filtered requests, empty output, invalid output,
provider errors, truncated generation, and upstream outages before enabling paid
inference. Do not let the model decide which outcome is billable. The first
profile must state what its attestor checks and what the buyer still trusts.

For private low-entropy inputs, review randomized, domain-separated commitment
construction rather than assuming a plain public hash hides the prompt. Keep the
randomizer and preimage available to authorized verifiers. Any new commitment
rule belongs in the new profile and vectors, not an undocumented reinterpretation
of an existing input hash.

## 10. Receipt, delivery, and assurance

### RCP-01 — Make the Receipt independently checkable

Use the exact released Receipt schema for the selected profile. Bind the Quote,
actor/request identity through its specified signing domain, Capability version,
input, output/artifacts, provider/execution identity, charged price, and required
evidence. The separate signer validates releasability against committed terms
before signing the request-bound SRP2 statement. A caller-controlled result hash
alone must not be enough to obtain a signature. A provider offering this product
must configure an attestor on its Service Actor; the contract's attestor-less
mode cannot carry a Receipt signature on chain.

For a new inference profile, specify model/runtime/tokenizer claims and measured
usage without treating provider-supplied counters as independently verified
metering. Do not extend an old Receipt encoding implicitly.

### RCP-02 — Distinguish evidence levels

| Evidence | What it can establish | What it does not establish by itself |
|---|---|---|
| Signed Receipt | An authorized signer committed to exact statements/results | Correctness, fairness, actual model execution, or delivery to the buyer |
| Independent recomputation | Agreement with the specified reproducible execution and inputs | General factual truth or equivalence for nondeterministic generation |
| Hardware attestation | The claims supported by a reviewed device/runtime trust model | Automatic semantic correctness or universal confidentiality |
| Cryptographic computation proof | The exact formally encoded relation under its assumptions | That the relation captures usefulness, real-world truth, or end-to-end PQ security |

The initial product may honestly use an attested-receipt trust model. It must not
market that as trustless model inference or as completed TOS Verifiable Compute.
Stronger assurance adapters require their own specification, verification costs,
security assumptions, and acceptance evidence.

### RCP-03 — Address availability separately

Persist and verify deliverable objects before authorizing a successful response.
Give the buyer an authenticated retrieval path and a declared retention window.
A result hash proves neither availability nor receipt by the buyer. The current
actor is not an atomic fair exchange of plaintext and payment: a dishonest
attestor/provider may still withhold a committed result after settlement, and
this profile supplies no automatic on-chain delivery dispute. Disclose that
risk; test retrieval independently and record failures separately from settlement.

## 11. Security, privacy, and post-quantum boundaries

### SEC-01 — Owner policy is the authority boundary

Treat prompts, source files, tool output, discovery descriptions, and model
responses as untrusted data. They may propose actions but cannot enlarge key,
wallet, filesystem, network, tool, resource, or disclosure permissions. Keep
identity administration, recovery, receipt signing, fee payment, and execution
credentials separately scoped. Provider publication grants no wallet-spending
permission. Human approval or a preconfigured bounded owner policy is required
for consequential changes.

### SEC-02 — Protect ingress and secrets

Require authenticated protected transport for public services, strict body and
stream bounds, timeouts, rate limits, replay controls, and per-caller resource
budgets. Prevent SSRF, DNS rebinding, credential forwarding to discovered hosts,
and cross-job data leakage. Remote model/API secrets remain provider-local and
are released only to an approved egress adapter. Do not log raw prompts, private
sources, results, seed material, or bearer credentials by default.

### SEC-03 — Make privacy claims layer-specific

Private content stays off-chain, but this alone does not hide transaction timing,
amounts, counterparties, endpoint addresses, or network metadata. The chosen
provider normally sees inference inputs unless a separately reviewed confidential
execution scheme says otherwise. Gateways should see only necessary routing and
commercial metadata, but confidentiality depends on the actual transport and
termination points. A shielded transfer elsewhere in TOS does not automatically
make Service Actor settlement or model execution private.

### SEC-04 — Preserve PQ authorization without overstating coverage

Reuse current ML-DSA-44 Registry authorization and the Service Actor's specified
attestor profile. Verify signature contexts, network and request binding, key
identity, canonical encodings, and revocation/snapshot rules. Unknown suites or
profiles fail closed; no silent classical fallback is permitted. The current
Native Registry carries no suite selector: it hard-codes ML-DSA-44 key and
signature lengths, so any other suite is rejected structurally rather than by
an explicit suite check. Agent Account contracts still verify Ed25519, so a
Registry ML-DSA-44 controller does not make an Agent Account PQ-authorized.

For any end-to-end post-quantum claim, publish a security dependency inventory
covering consensus, Registry controllers, funding/owner wallets, all delegated
signers, Receipt authorization, transport authentication/key exchange, content
encryption, commitments, and any computation-proof backend. A PQ controller or
Receipt signature does not establish PQ security for a classical wallet, TLS
configuration, or proof system. The desired PQ architecture is a requirement to
verify, not a product claim created by this document. No proof backend may be
called PQ-secure merely because it is described as zero-knowledge.

## 12. Protocol and developer integration

### INT-01 — Direct path before adapters

Expose a documented provider/buyer flow using the existing Native SDKs and current
settlement rail first. An adapter maps transport operations onto the same
identities, authorization, admission journal, Receipt, and economic outcome. It
must never maintain a second payment balance or execution claim.

### INT-02 — A2A and MCP are integrations, not authority

Select and pin external protocol versions, supported methods, error semantics,
and interoperability fixtures before claiming compatibility. A2A task operations
and MCP tool invocation may transport a purchase-bound request, but neither an
Agent Card nor tool discovery authorizes payment or host execution. Revalidate
current-rail integration; do not restore removed escrow-bound code unreviewed.
Cross-transport replay must reach the same durable execution guard.

### INT-03 — Keep optional integrations optional

ARD mapping, model API compatibility, x402 negotiation, and future payment
mechanisms require explicit scope and demand. Follow the existing
[x402 decision](X402_ADAPTER_DECISION.md); do not add a facilitator-owned settlement
path. The product must not depend on a public marketplace launch or a particular
external Agent framework to complete its first direct paid transaction.

### INT-04 — Ship usable, non-secret developer surfaces

Provide validated configuration examples, exact release/build prerequisites,
prepare/preview/sign/submit/resolve examples, structured errors, dry-run modes,
health checks, machine-readable output, and recovery procedures. Examples must
use actual implemented commands from the pinned release. This PRD does not
introduce a fictitious one-command Provider CLI or promise that installation
alone completes publication and custody setup.

## 13. Observability and economic viability

Report publication success, independently resolved purchases, admission refusal,
execution completion, result retrieval, responded/refunded/swept outcomes,
unknown outcomes, credited revenue, withdrawals, and actual wallet receipts as
separate measurements. Record sample sizes, network/release identities, workload,
provider hardware/backend, and operator independence.

Measure discovery, Quote, funding finality, queueing, execution, response finality,
refund, and withdrawal latency separately, including median and p95. Do not infer
inference latency from block time or promise throughput from a chain benchmark.
Missing telemetry is unknown, not success or zero cost.

Before approving a fixed-price offer, estimate service revenue against execution,
upstream API, storage, bandwidth, network, and operational costs. Disclose price
volatility exposure without promising earnings. Repeated real purchases and
successful delivery matter more than Agent registrations or subsidized self-sales.
The product must expose whether its on-chain cost is appropriate for its bounded
request size; a batching redesign is later work, not an invisible fee assumption.

## 14. Cross-repository implementation plan

The specification stays in this repository. Open implementation tasks against
existing repositories; do not create a new repository merely to host this PRD.
The packaging location for the TOS Provider experience is an implementation
choice, not a new protocol authority.

"Exists" below records source present at the implementation baseline, not
reviewed acceptance; every item still needs the evidence that WP-07 requires.

| Work package | Primary repository | Exists at baseline | Remaining deliverable |
|---|---|---|---|
| WP-01: current-rail inventory | `tos-service-spec`, with all implementers | Source-level reconciliation recorded in this document. | Executable evidence matrix bound to exact commits and release hashes; fix stale component docs (for example the `tos-ai` README gate statement) without inflating gate status. |
| WP-02: onboarding and service publication | `tos-service-protocol` | External-signing prepare/apply CLI (`cmd/tos-service-provider-publish`), exact manifest publication (`PublishManifest`), finalized-state check, no private-key option. | Persisted publication state for restart (PRV-04), pre-signing preview of actor/attestor/terms/costs, and a clean-room operator guide. |
| WP-03: bounded provider execution | `tos-ai` (execution) and OpenFox `pkg/servicebridge` (provider loop) | Container executor with digest pinning and resource limits, single-owner job journal, artifact store, `pkg/railgate` admission, OpenFox admit/execute/respond/redeliver loop. | Shared multi-worker execution claim, artifact retention and deletion, `railgate` use in `tos-ai`'s own CLI, independent review, per-job VRAM limits where GPUs are offered; approved model adapters belong to WP-08. |
| WP-04: discovery and public interfaces | `tos-service-gateway`, `tos-service-protocol` | Derived catalog (`capabilitycatalog`), actor index and verified offers (`serviceactorindex`, `cmd/tos-service-discovery`), manifest retrieval and federation package. | Harden the public Gateway: its Connect handlers currently have no request-body cap or rate limit, only the server's 30 s read timeout, despite an advertised 1 MiB bound (the Capability Carrier has both a body cap and a rate limit; the Intent Carrier has body caps only). |
| WP-05: custody and contract gaps | `tos` / `tosctl` | Registry, wallet, and Service Actor `tosctl` commands. | Change contracts only for a demonstrated invariant gap with separate review and vectors. |
| WP-06: buyer/runtime composition | `tos-service-protocol` Buyer SDK and OpenFox | Single `call` with re-verified terms and attestor binding, crash-safe buyer journal that never re-sends an ambiguous call, rolling-window budgets, OpenFox owner confirmation and refund recovery. | One purchase identity across more than the Agent Packet transport, and a calendar-day budget if required. |
| WP-07: independent commercial acceptance | `tos-service-spec` evidence plus participating repositories | Current-domain paid execution, refund, withdrawal, and independent reconstruction under the existing roadmap. |
| WP-08: inference expansion | `tos-service-spec`, then `tos-ai` and protocol/adapters | New inference profile, canonical vectors, at least one reviewed backend, and fresh acceptance; locked until expansion eligibility. |

WP-01 through WP-07 complete and package the existing commercial direction.
WP-08 must not delay its acceptance. None of these work packages requires an
LLM-specific consensus opcode, a separate canonical service database, or a
mandatory protocol-wide provider bond. A reputation field is not slashable
collateral; collateral requirements need their own enforced contract semantics.

## 15. Acceptance and adversarial test matrix

Each claimed test result must identify exact repository commits, artifact/code
hashes, network/genesis, configuration, commands, and retained evidence. The
following are requirements, not recorded passing results.

| ID | Scenario | Required observable result |
|---|---|---|
| AT-01 | New independent provider follows public instructions | Publishes and sells one exact Capability without source/database edits or shared developer keys. |
| AT-02 | Wrong network, code, owner, version, manifest, or attestor, or an actor with no attestor | Refused before spending or execution; no substituted fallback. |
| AT-03 | Registration/relay acknowledgement without finality | Remains pending/unknown, never reported as published or funded. |
| AT-04 | Terms change between quotation and `call` | Old expected terms cannot silently buy the changed service; no job starts on a rejected call. |
| AT-05 | Paid happy path | One funded request, one execution, retrievable matching result, valid Receipt, finalized response, and independently verified revenue credit. |
| AT-06 | Revenue withdrawal | Exact finalized withdrawal and provider-wallet credit, with fees distinguished from service revenue. |
| AT-07 | No response; caller claims in time | Contract-defined price refund verified; non-refundable storage/network costs disclosed. |
| AT-08 | Caller misses claim window | Permissionless `sweep_expired_request` returns price to caller; the bounded cleanup bounty comes from the storage fee, not the price, and provider revenue is credited `storage_fee − bounty`. |
| AT-09 | Response/expiry boundary and duplicate terminal calls | Only contract-permitted transition succeeds; no double payout/refund or loss of another request's backing. |
| AT-10 | Retry through another Gateway, process, A2A, or MCP | Same semantic purchase; at most one execution claim and no second payment intent. |
| AT-11 | Crash before/after submission, execution, signing, or response | Durable recovery preserves budgets and exact identities; ambiguous effects are resolved or quarantined, not blindly repeated. |
| AT-12 | Gateway lost or replaced | A second resolver reconstructs authority and settlement; independent retained objects preserve promised retrieval. |
| AT-13 | Stale/revoked identity, changed controller, or rotated attestor | New admission follows live authorization; existing requests retain their contract-defined snapshots and refund rights. |
| AT-14 | Resolver disagreement or checkpoint rollback | Affected operations fail closed; assurance is not downgraded silently. |
| AT-15 | Oversized/malicious input, path escape, SSRF, or prompt injection | Rejected or contained within declared bounds; no key, wallet, host, or network authority escalation. |
| AT-16 | Resource exhaustion, full queue, signer outage, or short deadline | Bounded refusal/degradation; no unbounded work or false success; funded requests remain recoverable. |
| AT-17 | Tampered Receipt, wrong input, or cross-request signature | Rejected by custody/client verification and by the on-chain SRP2 signature binding of a request that snapshotted an attestor. |
| AT-18 | Result unavailable despite a valid response | Delivery failure is visible separately from settlement; no invented automatic buyer remedy. |
| AT-19 | Data retention and tenant isolation | No unauthorized cross-job reads; secrets excluded from logs/evidence; declared retention/deletion behavior exercised. |
| AT-20 | Inference model substitution, tokenizer drift, or upstream fallback | Rejected unless the selected future profile explicitly authorized it; claims match actual assurance. |
| AT-21 | Claimed interoperability/PQ protection | Exact versions, dependency inventories, negative cases, and independently reproducible evidence support only the stated claim. |

AT-20 applies to the gated inference expansion. Adapter-specific portions of
AT-10 and AT-21 apply only when that adapter is claimed. Passing a smaller direct
profile must be reported as such, not as full product or network completion.

## 16. Milestones and definition of done

**M0 — Requirements and inventory.** Publish this PRD and the current-rail gap
inventory. No new commercial or expansion gate is marked accepted.

**M1 — Reproducible direct software-work path.** A fresh local-network lifecycle
covers response, refund, sweep, recovery, and withdrawal using pinned releases.
This establishes local integration evidence only.

**M2 — Independent provider and buyer onboarding.** A clean provider and buyer
complete the public documented session, and an independent resolver reconstructs
current-domain transactions and verifies deliverables. Submit evidence to the
existing Gate D/E acceptance process; this milestone does not self-approve it.

**M3 — Open operation and recurring use.** Meet applicable Gate F requirements,
including independent operators, Gateway failure/reconstruction, and recurring
paid demand. Production activation also requires applicable Gate G controls.
No registration-count or same-owner transaction proxy substitutes for this.

**M4 — Inference profile and adapter.** Only after expansion eligibility, freeze
and implement the inference profile, independently reproduce vectors, integrate
one reviewed backend, and repeat relevant acceptance/security tests. Add further
backends or metered/streaming economics only with explicit evidence and review.

The product is done for a declared release scope only when an unrelated provider
can publish, execute, deliver, resolve failure, and receive funds through public
interfaces; an unrelated buyer can inspect exact terms and evidence; and an
independent verifier can reconstruct selected chain effects without either
party's private Gateway database. Each release must state its supported profiles,
remaining trust assumptions, operational limits, and unaccepted gates.

## 17. Decisions required before inference implementation

Record separate decisions for the initial model operation/backend, objective
output acceptance and refusal handling, model-identity/evidence commitments,
transport versions, data retention and upstream disclosure, acceptable assurance,
Provider packaging location, and measured economic viability. Freeze all numeric
resource bounds and compatibility rules in the appropriate released profile or
operator policy before enabling it.

A stronger computation-verification system, confidential inference, partial billing,
and high-frequency settlement are separate design projects. They may reuse this
provider experience, but are not prerequisites to honestly offering the initial
attested software-work service and are not delivered by this document.
