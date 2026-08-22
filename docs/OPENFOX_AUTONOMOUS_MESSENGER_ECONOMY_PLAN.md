# OpenFox Autonomous Messenger and Economy Implementation Plan

**Status (2026-08-22):** the scoped Phase A--E repository implementation and
local test work is complete. Phase B includes a deployable Descriptor-bound
HTTPS fallback and local TLS acceptance; Phase E includes the production
runner, verifier, two-host runbook and blank evidence record. This is **100%
implementation completion, not 100% production acceptance**. The M0-R route
decision and genuinely independent public-network/operator execution remain
external evidence gates, not unfinished local code and not Gate D--G
acceptance evidence.

**Related specifications:**

- [`AGENT_NATIVE_MESSENGER_V1.md`](AGENT_NATIVE_MESSENGER_V1.md)
- [`OPENFOX_ECONOMIC_BRIDGE_V1.md`](OPENFOX_ECONOMIC_BRIDGE_V1.md)
- [`ARCHITECTURE.md`](ARCHITECTURE.md)
- [`ROADMAP.md`](ROADMAP.md)

## 1. Product outcome

This plan closes two connected product gaps without moving protocol authority
into OpenFox:

1. one OpenFox instance can address another by canonical AgentID or `.tos`
   alias, establish a first direct conversation without a preconfigured peer
   route, and exchange messages over the production Messenger transport; and
2. an OpenFox instance can periodically discover software-work opportunities,
   evaluate them locally, and execute a policy-authorized purchase or provider
   workflow through the existing TOS commercial lifecycle.

The target operator experiences are:

```text
"Send a message to alice.tos"
  -> canonical AgentID
  -> daemon-owned first-contact/session bootstrap
  -> Messenger delivery
```

and:

```text
owner objective + policy
  -> bounded Capability discovery
  -> finalized verification
  -> local opportunity assessment
  -> Quote and policy gate
  -> custody-gated funding
  -> execution
  -> Receipt and finalized settlement
```

The two flows share Agent identity and authenticated Messenger context, but
neither is allowed to create new identity, commerce, or settlement authority.

## 2. Non-negotiable authority boundaries

### 2.1 Identity and messaging

- AgentID is the durable contact and conversation identity.
- `.tos` is accepted only at a recipient-canonicalization boundary and may be
  retained only as display metadata.
- A name transfer affects only a later lookup. It cannot retarget an existing
  contact, conversation, session, approval, mandate, Quote, escrow, payment or
  Receipt.
- OpenFox and model output cannot select EndpointID, DeviceID, SessionID,
  conversation ID, ADNL address, Relay, prekey, or delegation.
- `tos-messengerd` owns verified Contact Descriptor refresh, device selection,
  session bootstrap, conversation binding, replay protection and transport.
- Endpoint or device rotation updates the delivery set for the same AgentID; it
  does not change the conversation's counterparty identity.

### 2.2 Discovery and commerce

- Gateway search is a bounded discovery hint, never proof of ownership,
  availability, price, quality or payment.
- Every candidate used for a decision is re-resolved from finalized Agent and
  Capability state and is pinned by CapabilityID, version, manifest digest and
  network tuple.
- Model output may propose an objective, query, candidate preference or
  negotiation text. It cannot supply finalized-state evidence, Accepted Quote
  bytes, escrow identity, custody signatures, settlement facts or policy
  approval.
- No funding occurs without an exact owner policy or owner-signed mandate. The
  default opportunity mode is observe-only.
- `tosctl` or an equivalent custody boundary owns signing. OpenFox never stores
  or reconstructs chain signing keys.
- Successful execution and earnings are recognized only from canonical Receipt
  and finalized settlement/wallet state.

### 2.3 Gate ordering

- This plan does not open the Expansion Gate or make Messenger Gate evidence.
- Route-independent first-contact state and observe-only opportunity discovery
  may be implemented and locally tested now.
- A concrete production Messenger carrier may be selected only from the M0-R
  reachability result. Existing ADNL/RLDP/Overlay/Sites components are
  candidates, not a pre-decided answer.
- Automatic paid execution does not become enabled by default before the
  documented external buyer/provider acceptance prerequisites are satisfied.

## 3. Repository ownership

| Repository | Owns | Must not own |
|---|---|---|
| `tos-messenger` | recipient canonicalization; finalized contact discovery; AgentID-keyed direct-conversation record; device/prekey selection; pair-session bootstrap; encryption; replay; transport; offline delivery | marketplace ranking; spending policy; custody; chain settlement |
| `OpenFox` | human/model intent; local opportunity scheduler; non-authoritative scoring; owner policy orchestration; calls into Messenger and buyer/provider SDKs; user-visible progress | DNS/finality proof validation; Endpoint/Device/Session selection; chain keys; Gateway facts as authority |
| `tos-service-protocol` | typed finalized-state, Gateway discovery, Quote, buyer, Receipt and settlement clients | AgentLoop scheduling; model policy; private custody |
| `tos-service-gateway` | bounded derived Capability search and Quote Proposal exchange | canonical ownership, ranking authority, escrow or settlement truth |
| `tos-ai` | provider execution adapter and shared execution Gate | buyer policy; Messenger identity; settlement authority |
| `tos` / `tosctl` | chain state, contracts, transaction signing and broadcast | OpenFox objectives or opportunity ranking |
| `tos-service-spec` | normative boundaries, milestone status and independently reproducible acceptance evidence | runtime authority or private operator state |

## 4. First-contact Messenger design

### 4.1 OpenFox boundary

OpenFox submits only:

```text
SendRecipientIntent {
  recipient_input
  plaintext/message semantics
  runtime_delivery_intent_id
  optional_runtime_owned_admission_invite
}
```

The runtime delivery-intent ID is generated outside the model. It is not the
durable Messenger replay key by itself. After canonicalization the durable
idempotency key commits the canonical AgentID **and** delivery-intent ID; the
composition record separately commits the canonical message semantics so that
an exact retry is idempotent while changed content under the same intent fails
closed. Omitting the delivery-intent ID would incorrectly collapse two
intentional identical messages to the same Agent.

OpenFox must not cache a resolved alias as a renewable name-to-route mapping.
It may retain the alias in presentation history, alongside the immutable
AgentID actually contacted.

### 4.2 Daemon-owned ensure operation

The intended typed daemon operation is conceptually:

```text
EnsureDirectConversation(ctx, recipient_input)
  -> DirectConversationHandle {
       recipient_agent_id
       conversation_id
       readiness: session-ready | admission-pending | transport-pending
     }
```

`conversation_id` is returned for observability, not selected by OpenFox. The
handle never exposes SessionID, EndpointID, DeviceID, prekey bytes or transport
addresses.

The daemon performs a fail-closed, durable and resumable state machine. Network
reads and device cryptography are not one filesystem transaction. Each
transition is persisted atomically, and readiness is returned only after the
committed state supports it:

1. canonicalize explicit AgentID or finalized `.tos` to AgentID;
2. load or create the durable direct-conversation record keyed by local AgentID
   and remote AgentID;
3. run the existing finalized delegation, DHT locator, Contact Descriptor,
   device succession and prekey chain;
4. deterministically plan all currently authorized recipient devices and local
   sibling-device copies;
5. apply the existing first-contact admission policy: a known-contact allow
   rule or daemon-validated one-time invite may continue; otherwise the contact
   remains owner-held or is denied without creating send authority;
6. reuse a valid pair session or ask the device-owned cryptographic boundary to
   create the approved suite's first-message state from verified prekeys;
7. atomically persist the conversation/session bindings before returning
   session readiness; and
8. enqueue through the configured daemon-owned transport.

Partial bootstrap is never reported ready. An exact retry either returns the
same durable record or resumes its pending state. Conflicting AgentID,
conversation, endpoint, device, prekey generation or network input fails
closed. The optional invite is runtime/owner-supplied authorization material,
not model-visible text or a model-selected route.

The implementation now wires the finalized discovery chain, retained verified
prekeys, pair-session initiation/acceptance, per-device fan-out and admission
into daemon-owned `messages.send-direct` and `messages.reply-direct`
operations. The dispatcher supports strict Descriptor-bound HTTPS transport as
a deployable fallback in addition to queue-only/test behavior. OpenFox's normal
`message` tool can submit a `.tos` or AgentID recipient intent, and the Phase E
runner exercises the same production channel boundary. None of those callers
can represent Endpoint, Device, Session or route authority. The M0-R study must
still select the final production carrier; the HTTPS fallback and local TLS
tests do not manufacture that external decision.

### 4.3 Durable identity continuity

The direct-conversation index is keyed by canonical remote AgentID, not alias,
EndpointID or DeviceID. Its record commits at least:

- local and remote AgentID;
- daemon-generated conversation ID;
- creation time and current lifecycle state;
- the last verified directory checkpoint used for bootstrap; and
- references to daemon-owned per-device sessions, without copying session
  secrets into the contact record.

Endpoint and device changes append verified session/delivery transitions. A
`.tos` reassignment creates or selects the record for the newly resolved
AgentID only; it cannot rewrite the former record.

### 4.4 Transport selection

The bootstrap state machine targets the existing Messenger transport
interface. The production implementation selected after M0-R must provide:

- authenticated peer transport independent of message semantic authority;
- bounded discovery, connect, frame, retry and concurrency budgets;
- exact recipient Endpoint binding supplied by the daemon, not OpenFox;
- offline behavior compatible with the existing Mailbox profile;
- restart-safe ambiguous-send resolution and delivery acknowledgement; and
- independently operated two-peer delivery/recovery evidence.

Any new loopback harness, the existing lab Relay and `transport:none` are
test/queue behavior and cannot be labelled production delivery. There is no
daemon loopback transport profile today.

## 5. Autonomous opportunity design

### 5.1 Runtime modes

The OpenFox opportunity scheduler has three explicit modes:

1. `off` — no polling or discovery;
2. `observe` — search, verify and report candidates, but never request a custody
   action; and
3. `policy-gated` — continue only when an exact owner policy/mandate authorizes
   the candidate and every existing buyer/provider security gate succeeds.

There is no unrestricted autonomous-spend mode.

### 5.2 Opportunity state machine

Before purchase preparation, each durable opportunity is a non-authoritative
orchestration projection keyed by an OpenFox-generated intent ID and the
canonical tuple:

```text
network
CapabilityID
Capability version
manifest digest
provider AgentID
```

Its pre-purchase phases are:

```text
discovered
  -> finalized-verified
  -> locally-assessed
  -> quote-requested
  -> quote-verified
  -> policy-authorized
  -> purchase-referenced | terminal-failed
```

From purchase preparation onward, payment identity is the existing OpenFox
`PurchaseKey{QuoteCommitment, EscrowAddress}`. Request keys, opportunity intent
IDs and Capability tuples never define payment identity. The opportunity
record stores only an immutable reference to that PurchaseKey and mirrors the
authoritative purchase journal phases:

```text
intent -> prepared -> funding_lease -> funded -> execution
       -> receipt -> release -> resolved
```

The opportunity projection never advances the purchase journal. On any
disagreement, the purchase journal plus finalized chain state win and the
projection is rebuilt or marked inconsistent. The `tos-service-protocol`
funding budget journal covers only its bounded funding responsibility; it is
not confused with OpenFox's multi-phase purchase journal.

Search score, model commentary, display names and `.tos` aliases are evidence
for none of these transitions. Crash recovery resumes from the durable phase
through the existing buyer journal and finalized-state resolution; it never
repeats an ambiguous funding, dispatch, release or refund action blindly.
Any pre-funding phase may terminate directly. A post-funding failure cannot
simply become failed: it must resolve finalized state to release, refund or a
terminal state that retains the exact unresolved chain evidence.

### 5.3 Bounded discovery and assessment

An operator configures:

- explicit Gateway origins and credentials;
- query/objective templates;
- polling interval with jitter;
- maximum pages, candidates and bytes per cycle;
- Capability classes and exact asset allow-list;
- price, daily budget and concurrent-work ceilings;
- minimum expiry/finality margin;
- provider allow/deny policy; and
- `observe` or `policy-gated` mode.

Before polling is enabled beyond a single bounded operator instance, Gateway
deployment must enforce per-credential request/concurrency quotas and rate
limits, or serve a checkpoint-bound cache whose staleness is explicit. Current
catalog search performs serial fresh finalized reads per scanned entry, so an
unbounded scheduler would amplify chain and Gateway load.

OpenFox aggregates Gateway hints, deduplicates by canonical Capability tuple,
and re-resolves each retained candidate. Local scoring may use manifest facts,
price, historical finalized outcomes and owner preferences. Missing metrics are
unknown, never zero or success. A score can order review but cannot authorize a
purchase.

### 5.4 Negotiation and execution

Messenger may carry human-readable negotiation, but the Quote Proposal's
complete preimage remains the only commercial input to Accepted Quote
construction. A chat statement such as “I will do it for 10” is not a Quote.

The buyer path composes existing discovery/federation, Quote validation,
funding budget, safe-handoff verification and execution-Gate primitives. It
does not assume one existing end-to-end Buyer SDK: dispatch, Receipt checking
and settlement execution still require explicit integration deliverables.

The provider path reuses the `tos-ai` bounded executor and shared execution
Gate, including the existing Messenger event bridge, but automated canonical
Receipt production, execution-signer custody, a production `Settler`, and
provider publication wiring are new deliverables. The current manual Receipt
release command and nil-Settler execution-only adapter are not an automated
provider flow.

OpenFox adds orchestration and durable presentation state only. Its AgentLoop
module must not import the nested custody-bearing `servicebridge/nativeimpl`
module directly. A private bounded coordinator boundary, following the existing
heartbeat-to-Gateway-handler pattern, owns the native bridge and returns typed
progress without keys, chain evidence authority or low-level transaction
inputs.

## 6. Typed integration surfaces

The preferred OpenFox interfaces are narrow adapters over existing SDKs:

```text
OpportunityDiscovery.Search(ctx, boundedQuery) -> []CandidateHint
FinalizedVerifier.VerifyCandidate(ctx, hint) -> VerifiedCandidate
QuoteRequester.Request(ctx, verifiedCandidate) -> VerifiedQuote
PolicyEvaluator.Evaluate(ctx, verifiedQuote) -> Decision
PurchaseRunner.Run(ctx, authorizedQuote) -> PurchaseProgress
ProviderRunner.OfferAndExecute(ctx, policy) -> ProviderProgress
```

Production constructors require real finalized verifiers, journals, custody
and execution gates. Test doubles are injectable only through explicitly named
test constructors or tests; production cannot silently fall back to them.

## 7. Implementation sequence

### Phase A — route-independent first contact

Primary repository: `tos-messenger`; thin caller change: `OpenFox`.

- freeze the AgentID-keyed direct-conversation record and atomic lifecycle;
- expose daemon-owned ensure/send semantics without low-level route fields;
- reuse verified directory and prekey state;
- wire the currently library-only pair-session initiate/accept and fan-out
  operations through the device-owned cryptographic boundary;
- enforce known-contact, one-time-invite and owner-hold admission parity before
  session/send readiness;
- cover alias transfer, endpoint/device rotation, stale prekey, restart,
  conflict and model-route-substitution cases; and
- prove loopback/queue behavior without claiming production delivery.

Status on 2026-08-22: **implementation complete; local acceptance complete**.
`tos-messenger` commits `af8ef48`, `242097d`, `1649e68`, `542f283`, and
`ce552e8` retain exact verified prekeys, persist daemon-owned asynchronous
sessions, create one independently sealed/retried copy per verified device,
apply ordinary admission through an atomic Event+ratchet commit, and derive
replies from authenticated inbound Events. Local API v10 exposes
`messages.send-direct` and `messages.reply-direct`; neither operation can
represent an OpenFox-selected Endpoint, Device, Session or route. The full
`make verify` gate passed, including race, ADNL/RLDP, Rust/OpenMLS and build.

OpenFox commit `9e241774` sends high-level recipient intent directly to that
boundary and replies from authenticated Event origin without a preconfigured
direct route. The normal AgentLoop `message` tool accepts only `channel`,
`recipient` and content at this proactive boundary. The complete tagged local
gate (`go test -tags goolm ./cmd/... ./pkg/...`, vet and command builds) passes;
the native Messenger and evidence packages also pass focused race tests.

`TestTwoIndependentDaemonsExchangeEncryptedDirectMessages` uses separate
AgentIDs, Endpoint keys, DeviceIDs and durable journals with the real candidate
X25519/AES-256-GCM double-ratchet suite. It proves first message, ordinary
admission, reply and retry idempotency five consecutive times. This is same-host
loopback evidence only. It does not satisfy M0-R, production-carrier or
independent-operator acceptance.

### Phase B — M0-R and production transport

Primary repository: `tos-messenger`; modify `tos` only for a proven missing
native primitive.

- complete representative multi-operator reachability measurements;
- record the selected route and rejected alternatives;
- bind the existing transport interface to the selected native carrier;
- prove two independently operated OpenFox instances can discover, bootstrap,
  exchange messages, restart and recover.

Status on 2026-08-22: **deployable fallback implementation and local TLS
acceptance complete; final M0-R selection and independent evidence open**.
`tos-messenger` commit `13b5ccc` binds the daemon transport interface to a
strict Descriptor-selected HTTPS fallback. The carrier accepts only public
port-443 exact-path URLs from verified Contact Descriptors, disables proxies
and redirects, pins checked public DNS answers, requires TLS, and accepts only
an exact Endpoint-signed durable acknowledgement bound to Event, session,
Endpoint, Device and ciphertext digest. Two independent daemon identities,
state owners and ratchets exchange over real local TLS in tests, and full
`make verify` passes. This does not pre-select the final native route or replace
the required multi-operator reachability study.

### Phase C — observe-only opportunity loop

Primary repository: `OpenFox`.

- add bounded scheduler/configuration and a durable candidate journal;
- connect existing Gateway search and finalized verification clients;
- keep the AgentLoop separated from `servicebridge/nativeimpl` through a
  bounded local coordinator interface;
- require Gateway credential quotas/rate limits or checkpoint-bound caching
  before recurring multi-instance polling;
- expose verified opportunities to the AgentLoop and operator UI;
- prohibit Quote acceptance, custody or execution in this phase; and
- test malicious Gateway ranking, rollback, cross-network and manifest
  substitution.

Status on 2026-08-22: **implementation and local tests complete**. OpenFox
`8d52b817` adds the bounded scheduler, strict durable candidate journal,
multi-Gateway hint aggregation and independent finalized Capability/manifest
verification behind a private Unix coordinator. The AgentLoop surface is
read-only and cannot request a Quote, custody action or execution. Protocol
`5248a15` exposes the finalized Capability verifier used by the coordinator.

### Phase D — policy-gated commercial loop

Primary repository: `OpenFox`; reuse `tos-service-protocol`, `tos-ai` and
`tosctl` boundaries.

- connect verified Quote, exact owner policy/mandate and buyer journal;
- resume crash-safely through funding, dispatch, Receipt and settlement;
- add typed buyer dispatch, Receipt verification and settlement integration;
- add automated provider publication, canonical Receipt construction,
  execution-signer custody and a production `Settler` implementation in their
  owning protocol/provider repositories;
- harden autonomous buyer `tosctl` execution to the existing publisher
  standard: pinned binary digest, descriptor-based execution, scrubbed
  environment and descriptor-passed configuration;
- prove cross-transport replay reaches one shared execution Gate/claim store;
  separately operated provider instances require a shared authoritative claim
  boundary or must be treated as distinct execution domains; and
- keep automatic paid mode disabled until operator configuration explicitly
  enables an accepted policy.

Status on 2026-08-22: **implementation and local tests complete; external paid
acceptance open**. OpenFox `42268bd3` and `ab356fc1` implement the immutable
opportunity-to-`PurchaseKey` projection and policy-gated coordinator over the
existing authoritative buyer journal. It validates multi-Gateway Quotes,
owner-signed spending policy and Messenger mandate, deploys/funds at most once,
dispatches A2A/MCP/Agent Packet through one shared execution Gate, verifies the
canonical Receipt and resolves finalized release/refund state. OpenFox
`129ec08d` and protocol `284fc3a` pin the enrolled `tosctl` inode/size/SHA-256,
recheck it at every call, execute the opened descriptor, pass pinned config by
anonymous file descriptor and inherit no ambient process environment. OpenFox
`d3a64104` requires `tosctl` execution-signer custody in the production
provider. Protocol `3809bb7` adds restartable reviewed Capability publication:
deterministic prepare, external controller signature, exact finalized publish,
then immutable manifest admission; `22eed2a` additionally requires the Gateway
credential file to be owned by the running operator identity. Automatic spend
remains opt-in only.

### Phase E — independent acceptance

Evidence repository: `tos-service-spec`.

- fresh OpenFox buyer and provider under separate operators;
- independently operated Gateway/resolver and Messenger endpoints;
- first-contact conversation followed by Quote negotiation;
- exact funded execution, Receipt, provider credit or objective refund;
- full restart and original-Gateway loss recovery; and
- a published record binding configs, artifacts, network checkpoints and exact
  repository commits.

Status on 2026-08-22: **runnable Messenger and commerce acceptance surfaces and
strict evidence tooling complete; independent execution not yet performed**.
OpenFox `3a82ae94` runs a real production `tos_messenger` channel and AgentLoop
as one independently restartable process with an owner-private control socket
and transcript. It accepts only recipient intent and message content; direct
replies derive exclusively from authenticated daemon Events. OpenFox
`2bbb9434` adds process-run identities, restart-safe applied-reply deduplication,
a two-transcript verifier and the public-TLS two-host runbook. The verifier
requires exact cross-host Event/content equality, canonical authenticated peer
AgentIDs, reply causality and two durable run epochs, but deliberately cannot
infer operator independence. OpenFox `13eb5ba8` further requires the initiating
transcript to carry a proactive recipient intent, preventing an unrelated
reply chain from being presented as discovery/bootstrap evidence. OpenFox
`95a25e70` adds race-covered proof that a fresh authenticated inbound Event is
published to AgentLoop while its daemon application lease remains retained
until the reply path completes. OpenFox `5eab6cf8` closes the machine-evidence
binding gap with canonical externally signed Ed25519 operator attestations over
the exact transcripts, AgentIDs, public endpoints, network/genesis tuple,
commits, binary/configuration digests and run intervals. It verifies distinct
asserted operators/sites/endpoints/keys while explicitly leaving real-world
independence to the external reviewer. Use
[`OPENFOX_PHASE_E_EVIDENCE_TEMPLATE.md`](OPENFOX_PHASE_E_EVIDENCE_TEMPLATE.md)
for the external record. No repository process may mark Phase E externally
accepted until unrelated operators actually publish that evidence.

The commerce half may count toward roadmap item 17 and Gate D/E external
acceptance only when it independently satisfies those gates' operator,
transport and resolver requirements. Messenger is not a prerequisite for
commerce acceptance: A2A, MCP or Agent Packet remains an allowed task transport
so an unfrozen Messenger carrier cannot block or weaken Gate D/E evidence.

## 8. Acceptance gates

### Messaging acceptance

- no peer-specific route exists in OpenFox before the send;
- `.tos` and explicit AgentID converge on the same AgentID-keyed daemon path;
- name transfer does not mutate the first conversation;
- model-selected route/session/device fields are unrepresentable or rejected;
- an unknown first contact without a valid invite is held or denied, and a
  consumed invite cannot authorize a second event;
- two independently operated agents exchange and recover messages over the
  M0-R-selected production transport; and
- delivery evidence distinguishes queued, accepted and application-applied
  states.

### Opportunity acceptance

- observe mode finds and independently verifies bounded candidates without any
  custody call;
- malicious or stale Gateway data cannot reach policy authorization;
- policy-gated mode cannot exceed exact asset, amount, count, expiry,
  Capability, provider or concurrency limits;
- ambiguous mutations resolve finalized state before retry;
- one funded purchase executes at most once across transports sharing the same
  provider execution claim store; multi-instance deployments prove the claim
  boundary they rely on rather than assuming process-local state is global; and
- an independent resolver reconstructs Accepted Quote, escrow, execution
  evidence, Receipt and final provider credit/refund.

## 9. Explicit non-goals

- no OpenFox-owned DNS, directory, session, transport, wallet or chain index;
- no `.tos`-keyed conversation, replay, policy or commerce record;
- no model-selected route, finality proof, Quote, escrow or signature;
- no Gateway-controlled canonical ranking or payment fact;
- no parallel marketplace, payment rail, Receipt or settlement lifecycle;
- no production-transport claim from loopback, same-host or queue-only tests;
- no automatic spending merely because an LLM assigned a high score; and
- no Gate D--G completion claim from implementation or same-host evidence.

## 10. Completed first implementation slice

The first code slice after design review was Phase A's route-independent durable
direct-conversation boundary in `tos-messenger`, plus a local API operation and
tests. It must accept only recipient intent, resolve to AgentID, create or reuse
an AgentID-keyed conversation record atomically, return no low-level routing
authority, and leave delivery pending when no production transport exists.

This slice is intentionally smaller than session cryptography or transport
selection. It establishes the identity-continuity boundary that both later
bootstrap and OpenFox proactive send require, without pre-deciding M0-R.

Initial implementation evidence: `tos-messenger` commit `219ed91` added local API v9
`conversations.ensure-direct`, the AgentID-keyed durable record, monotonic
finalized-directory evidence, restart/idempotency/alias-transfer/rotation and
route-substitution tests. Its full `make verify` passed on 2026-08-22. That
initial operation reported only `transport-pending`. The Phase A status
record above supersedes its then-open pair-session and OpenFox integration
gaps. Phase B now provides the deployable strict HTTPS fallback, while final
carrier selection remains dependent on a qualifying M0-R route-decision
report.

## 11. Design review record

Claude Code performed a read-only review across the current
`tos-service-spec`, `tos-messenger`, `OpenFox`, `tos-service-protocol`,
`tos-service-gateway`, `tos-ai` and `tos` trees on 2026-08-22. The first pass
returned `REVISE`. The design was then corrected to:

- bind Messenger idempotency to canonical AgentID plus a runtime-owned delivery
  intent while committing content separately;
- make the opportunity journal a non-authoritative projection onto OpenFox's
  existing `PurchaseKey{QuoteCommitment, EscrowAddress}` and purchase journal;
- name Receipt production, settlement, provider publication and buyer dispatch
  as real missing deliverables;
- distinguish library-only pair-session/fan-out code and `transport:none` from
  a production-wired Messenger path;
- require first-contact admission parity, the OpenFox native-implementation
  module boundary, bounded Gateway polling, hardened `tosctl` custody, durable
  resumable transitions, pre/post-funding terminal rules and a correctly scoped
  execution claim store; and
- keep Gate D/E commerce acceptance independent of Messenger transport.

The second read-only pass returned `APPROVE` and found no remaining blocker,
high or medium design issue. This tool-assisted review is an implementation
design check only; it is not the independent cryptographic, multi-operator or
Gate acceptance evidence required elsewhere in this specification.
