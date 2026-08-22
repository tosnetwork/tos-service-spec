# TOS Edge CDN Architecture V1

## Status

**Application status: 🟡 Incubation architecture defined; protocol profiles,
implementation, independent operators, and live customer evidence pending.**

This document defines the target architecture for TOS Edge CDN: an open edge
storage and content-delivery market built on the existing TOS Agent,
Capability, Accepted Quote, escrow, Receipt, and settlement lifecycle.

It is an application and integration architecture, not a new consensus
protocol. It adds no alternate Agent identity, Capability registry, canonical
balance, payment rail, Receipt authority, network domain, or protocol
identifier. The sole service-protocol identifier remains `tos_service_v1`.

This document is subordinate to:

- [`PRODUCT_STRATEGY.md`](PRODUCT_STRATEGY.md), which controls product priority;
- [`ARCHITECTURE.md`](ARCHITECTURE.md), which controls authority boundaries;
- [`NATIVE_REGISTRY_STATE_MACHINES.md`](NATIVE_REGISTRY_STATE_MACHINES.md),
  which controls Agent and Capability transitions;
- [`SETTLEMENT.md`](SETTLEMENT.md), which controls Quote, escrow, Receipt, and
  settlement semantics; and
- [`ROADMAP.md`](ROADMAP.md), which controls implementation order and acceptance
  evidence.

If this document conflicts with a controlling document, the controlling
document wins. TOS Edge CDN does not reorder the initial software-work market
wedge and cannot be cited as acceptance evidence for an earlier roadmap gate.

The profile names in this document are architectural names. They MUST NOT be
used as frozen signature domains, manifest identifiers, or wire identifiers
until a focused specification publishes canonical encodings, vectors, and a
negative corpus.

---

## 1. Executive decision

TOS Edge CDN is designed as a **standard CDN product backed by an open market of
verifiable edge workers**.

A customer such as a video platform, AI-model distributor, game publisher, or
software vendor should integrate with familiar CDN surfaces:

```text
CNAME / HTTPDNS / optional client SDK
  -> HTTPS GET / HEAD / Range
  -> cache, preload, purge, logs, and metrics APIs
```

The customer should not need to know which household box, NAS, enterprise
server, carrier edge, or data-center node served an object. Worker selection is
an internal scheduling decision.

Inside the network, TOS provides the authority and commercial spine:

```text
Customer Agent
  -> customer-facing CDN Capability
  -> finalized Accepted Quote and funded escrow
  -> provider-operated scheduling and delivery
  -> content-addressed evidence and signed Receipt
  -> finalized release or refund

CDN Provider Agent
  -> worker-supply Capability
  -> separate finalized Accepted Quote and funded escrow
  -> edge storage / delivery work
  -> worker evidence and signed Receipt
  -> finalized worker payment
```

The two commercial relationships are deliberately separate in V1. A
customer-facing purchase does not create an implicit multi-party escrow or an
unverifiable revenue split. The CDN Provider remains accountable to the
customer; each independently operated Worker remains accountable to the CDN
Provider under its own Quote.

The core product principle is:

> **Use standard CDN interfaces at the customer edge, TOS-native authority and
> settlement at the commercial edge, and content-addressed evidence at the
> worker edge.**

---

## 2. First-principles design decisions

### 2.1 A CDN, not a remote-shell marketplace

A TOS Edge CDN Worker stores and serves bounded content objects. It does not
expose SSH, arbitrary container execution, customer code execution, or
unrestricted filesystem and network access.

General compute belongs to a separate Capability and execution profile. The CDN
worker's narrow operation set is intentional:

```text
PLACE
FETCH
VERIFY
PIN
SERVE
EVICT
PURGE
REPORT
```

This narrow surface makes community hardware materially safer than a generic
compute rental product.

### 2.2 Standard customer compatibility, TOS-native internals

The public data plane should behave like an ordinary HTTP CDN. TOS-specific
identity, Quotes, worker selection, evidence, and settlement remain behind the
customer integration boundary.

The protocol should innovate in:

- worker discovery and verifiable authority;
- open capacity purchasing;
- content-addressed placement;
- usage evidence;
- replay-safe settlement; and
- independent reconstruction of commercial history.

It should not require a large customer to replace HTTP, HLS, DASH, browser, or
mobile playback semantics merely to use TOS.

### 2.3 Finalized TOS state remains the only shared authority

Finalized TOS state is authoritative for:

- the Customer, Provider, and Worker Agent identities;
- Capability ownership, version commitment, and revocation;
- Accepted Quote terms;
- escrow custody and state;
- Receipt commitments and execution authorization; and
- release, refund, and final settlement.

DNS answers, CNAMEs, scheduler decisions, cache indexes, placement databases,
worker dashboards, traffic measurements, and CDN logs are operational or
derived state. They cannot create or override a TOS protocol fact.

### 2.4 High-frequency delivery stays off-chain

No design may require one chain transaction per HTTP request, byte range,
segment, cache hit, or worker heartbeat.

Delivery requests, cache operations, signed tickets, telemetry, and evidence
remain off-chain. A bounded billing window produces an aggregate evidence root
and one Receipt or another explicitly bounded settlement object.

### 2.5 The Scheduler is replaceable and non-canonical

A Scheduler may rank nodes, place objects, issue bounded delivery tickets,
steer traffic, and aggregate evidence. It may not:

- invent a Worker or Capability identity;
- change Accepted Quote terms;
- declare a payment final;
- rewrite a Receipt signer;
- turn an unverified log row into canonical usage; or
- make its private database necessary to reconstruct the settlement history.

### 2.6 Standard HTTP cannot prove every human-viewed byte

The architecture does not claim a magical cryptographic proof that every byte
reported by a Worker reached a distinct human viewer. Standard browsers and
video players do not sign delivery acknowledgements for the CDN.

Instead, each Quote commits to an explicit evidence profile. Payments are based
on the evidence that profile can objectively establish, with conservative
metering, sampling, independent challenges, bounded dispute rules, and no
misrepresentation of weaker evidence as stronger proof.

---

## 3. V1 scope

### 3.1 Included

The first implementable TOS Edge CDN profile should support:

- immutable and versioned cacheable objects;
- video segments, model files, software releases, game patches, container
  layers, and other large static artifacts;
- HTTPS `GET` and `HEAD`;
- single and bounded byte-range requests with correct `206`, `Content-Range`,
  and `416` behavior;
- HTTP/2, with HTTP/3 as a separately tested capability;
- HLS, DASH, CMAF, and ordinary file delivery through their existing HTTP
  object semantics;
- pull-through caching from a bounded origin;
- explicit preload and purge;
- TTL, pin, retention, and storage-reservation policies;
- signed URL or signed-cookie access control;
- CNAME/GeoDNS steering, with HTTPDNS and a client SDK as optional adapters;
- professional data-center, carrier-edge, enterprise, and NAS Workers;
- community/home Workers only under the restricted trust tier defined below;
- integer storage and egress metering over bounded billing windows;
- off-chain evidence aggregation and one replay-safe Receipt per settlement
  window; and
- one independently resolvable customer payment and one independently
  resolvable worker payment.

### 3.2 Deferred

The following are not required for V1:

- arbitrary edge compute or customer-supplied code;
- live video ingest, transcoding, or real-time media production;
- client-to-client P2P swarming;
- browser-side TOS wallets;
- one on-chain transaction per request;
- generalized multi-party revenue-split contracts;
- subjective traffic arbitration;
- anonymous cash-like worker payouts;
- an unverifiable claim of exact proof-of-bandwidth for all traffic;
- unrestricted household-node termination of customer-domain TLS; and
- a global regulatory or content-liability policy encoded as protocol truth.

---

## 4. Actors and planes

### 4.1 Actors

| Actor | Responsibility | Authority boundary |
|---|---|---|
| **Customer Agent** | Purchases CDN service, owns or controls content/origin policy, reviews terms, funds escrow, verifies service Receipt | Controls only its own signed actions and customer-local configuration |
| **End Client** | Browser, app, player, package manager, model client, or other consumer of delivered bytes | Usually has no TOS identity and creates no canonical protocol fact |
| **CDN Provider Agent** | Commercial counterparty to the Customer; operates or selects control-plane services and fulfils the customer SLA | Bound by the customer-facing Accepted Quote |
| **Worker Operator Agent** | Independently operates one or more edge nodes and sells bounded storage/delivery service | Bound by a worker-supply Accepted Quote |
| **Worker Endpoint** | Runs the data-plane worker under a current Agent delegation and bounded local policy | Executes work; cannot rewrite Agent, Quote, escrow, or settlement state |
| **Scheduler / Control Plane** | Places objects, issues tickets, steers traffic, aggregates observations, initiates worker purchases | Operational only; no canonical semantic authority |
| **Origin** | Supplies authoritative customer bytes for an object generation | External data source; its responses are accepted only under the committed origin/object policy |
| **Verifier / Auditor** | Challenges storage and delivery claims, checks evidence bundles, reproduces billing calculations | Produces evidence or review; cannot unilaterally create settlement authority unless selected by the Quote's dispute policy |
| **Gateway / Resolver** | Discovers Capabilities, constructs proposals, relays actions, and resolves finalized state | Replaceable and non-canonical |

### 4.2 Architectural planes

```text
TOS authority plane
  Agent / Capability / Accepted Quote / escrow / Receipt / settlement

TOS Service Protocol plane
  canonical encodings, verification, resolution, replay protection, adapters

Edge CDN control plane
  customer configuration, domain onboarding, origin policy, placement,
  scheduling, traffic steering, purge/preload, metering, evidence aggregation

Edge CDN data plane
  origin fetch, content verification, cache storage, HTTPS object delivery,
  range service, health and bounded telemetry

Customer compatibility plane
  CNAME, HTTPDNS, CDN APIs, HTTPS, HLS, DASH, logs, metrics, SDK adapters
```

Authority flows downward from finalized TOS state and signed, bounded
operational delegations. Observations flow upward as evidence. An observation
never becomes canonical merely because it reached the control plane.

---

## 5. Canonicality matrix

### 5.1 Finalized TOS facts

Only finalized TOS state can establish:

- Agent identity and current controller policy;
- Endpoint and execution delegation committed by an Agent;
- Capability ownership, immutable version, and revocation status;
- exact Customer↔Provider and Provider↔Worker Accepted Quote commitments;
- asset identity and maximum funded amount;
- escrow state;
- selected execution/Receipt signer;
- Receipt commitment; and
- released or refunded outcome.

### 5.2 Signed off-chain facts

The following may be signed and content addressed but remain off-chain facts:

- Worker availability advertisements;
- Scheduler placement and delivery tickets;
- object manifests and origin-fetch grants;
- cache-presence proofs;
- Worker delivery logs and monotonic counters;
- client samples and independent challenge results;
- billing-window evidence bundles;
- purge and preload directives; and
- derived SLA reports.

Their authority is limited to the exact Quote, signer, expiry, and policy that
accepts them.

### 5.3 Provider-local application state

The following may be provider-local:

- distribution names and dashboard labels;
- CNAME onboarding state;
- customer support records;
- route ranking and load-balancing weights;
- cache index placement;
- origin health;
- threat intelligence;
- abuse decisions; and
- provisional billing views.

Provider-local state must never be displayed as finalized TOS settlement.

---

## 6. Commercial topology

### 6.1 Customer-facing purchase

The Customer purchases a CDN service from one Provider Agent:

```text
Customer Agent
  -> resolve Provider Agent and customer-facing CDN Capability
  -> obtain Quote Proposal
  -> accept exact service terms on TOS
  -> fund bounded escrow
  -> use the provider's standard CDN interfaces
  -> verify aggregate service Receipt
  -> release or refund according to committed terms
```

The customer-facing Quote should bind, directly or by immutable digest:

- network identity;
- Customer and Provider Agent IDs;
- exact Capability and version;
- service-profile digest;
- distribution-policy digest;
- supported protocol and security class;
- allowed regions and jurisdictions;
- maximum storage, egress, origin-fill, and request bounds;
- billing-window start, end, and maximum duration;
- exact asset and maximum funded amount;
- rate-card digest and integer rounding rules;
- evidence-profile digest;
- SLA and failure-policy digest;
- endpoint / signer authorization;
- escrow and dispute-policy digest; and
- expiry.

### 6.2 Worker-supply purchase

The Provider separately purchases capacity or delivery from each independent
Worker Operator:

```text
CDN Provider Agent
  -> resolve Worker Agent and worker-supply Capability
  -> accept storage / delivery terms
  -> fund bounded worker escrow
  -> issue placement and delivery tickets within those terms
  -> verify Worker evidence and Receipt
  -> release or refund worker payment
```

The worker Quote must bind a maximum economic exposure and must not permit the
Scheduler to create unlimited usage merely by issuing more tickets.

### 6.3 No hidden split settlement in V1

A Customer payment does not automatically split among Workers. A Worker has no
claim against the Customer's escrow unless the Customer explicitly accepted a
future multi-party profile.

This V1 separation has three advantages:

1. the Customer has one accountable CDN Provider;
2. each Worker has one accountable capacity buyer; and
3. existing single-provider Quote, escrow, Receipt, and settlement semantics
   remain reusable without a parallel CDN payment system.

---

## 7. Capability model

The architecture anticipates two focused Capability profiles. The exact strings
are provisional until focused canonical specifications and vectors exist.

### 7.1 Customer-facing CDN service Capability

Provisional profile name:

```text
tos.edge-cdn.service.v1
```

Its immutable version commitment should describe bounded service classes, not
live capacity. Candidate committed fields include:

- accepted object and media classes;
- protocol support and exact conformance profile;
- cache-key and object-generation rules;
- maximum object, range, header, and request sizes;
- origin-fetch policy classes;
- signed URL/cookie methods;
- region and jurisdiction policy classes;
- TLS trust tier;
- purge and preload semantics;
- evidence-profile identifiers;
- SLA calculation profile;
- Receipt profile;
- endpoint and signer commitments; and
- implementation/version digests where required.

### 7.2 Worker-supply Capability

Provisional profile name:

```text
tos.edge-cdn.worker.v1
```

Its immutable version commitment should describe what the Worker is permitted
and able to do under stable policy:

- Worker trust tier;
- supported object and protocol profiles;
- storage class and maximum committed capacity class;
- maximum object/range/request bounds;
- supported evidence modes;
- supported IP families;
- region, jurisdiction, and declared network class;
- origin-fetch restrictions;
- update and software-attestation policy;
- endpoint and evidence signer commitments; and
- operator custody and incident-contact commitments where applicable.

### 7.3 Dynamic availability advertisement

Live free storage, current egress capacity, queue depth, measured latency,
health, temporary price estimates, addresses, and routing observations are too
dynamic for immutable Capability state.

A Worker publishes a short-lived signed advertisement containing:

```text
worker_agent_id
capability_id + version
endpoint_id
timestamp + expiry
available_storage_bytes
available_ingress_bps
available_egress_bps
current_load_class
reachable_address / tunnel references
supported evidence mode for this window
software release digest
advertisement nonce
```

A Scheduler must resolve the referenced Agent and Capability before trusting the
advertisement. Expiry or failure to resolve makes it unusable, not stale truth.

---

## 8. Content and distribution model

### 8.1 Distribution

A Distribution is provider-local application state that groups:

- customer domain or provider-hosted delivery name;
- origin configuration;
- cache-key policy;
- access-control policy;
- geographic and Worker trust-tier policy;
- TTL, retention, purge, and preload policy; and
- logging and SLA policy.

A Distribution is not a new TOS Registry object. Its immutable policy digest may
be committed by an Accepted Quote.

### 8.2 Cache key

The cache key is derived from a canonical tuple such as:

```text
scheme class
canonical host / distribution ID
normalized path
selected query parameters
selected request headers
content-encoding variant
customer cache-policy revision
```

The exact normalization profile must be frozen before interoperability. Workers
must not invent local normalization that can cause cache poisoning or serve one
customer's object under another customer's key.

### 8.3 Object generation

A mutable URL is not a stable content identity. Each exact byte sequence is an
immutable object generation.

A future canonical profile should bind at least:

```text
customer_agent_id
distribution_id or distribution-policy digest
cache_key_digest
object_digest of the exact bytes served
object_size_bytes
canonical media type
content-encoding variant
origin validator / version evidence
policy digest
creation time and bounded expiry
```

The `object_digest` is over the exact delivered bytes. A customer may encrypt
content before CDN ingestion; in that case Workers store and serve opaque
ciphertext and the digest commits to that ciphertext.

A changed origin object creates a new generation. Purge revokes serving and
placement authorization for an old generation; it does not change the old
generation's digest.

### 8.4 Chunking

Large objects may be stored in fixed-size, content-addressed chunks. The object
manifest commits:

- ordered chunk digests;
- exact chunk lengths;
- total object length;
- object digest;
- media type and encoding; and
- manifest format version.

Range responses must reproduce the exact byte interval of the object generation
regardless of internal chunk boundaries.

---

## 9. Customer interface requirements

### 9.1 Data plane

A V1-compatible customer data plane should support:

- TLS with current secure versions and no obsolete protocol fallback;
- HTTP/2 as a baseline and HTTP/3 as a separately advertised capability;
- `GET` and `HEAD`;
- correct `Range`, `If-Range`, `ETag`, `If-None-Match`, `Last-Modified`, and
  `If-Modified-Since` behavior according to the selected profile;
- exact `Content-Length`, `Content-Range`, content type, encoding, and cache
  metadata;
- bounded headers and request rates;
- signed URL or signed-cookie authorization;
- origin and cache error semantics that distinguish miss, denied, unavailable,
  malformed, and integrity failure; and
- HLS, DASH, CMAF, model, package, and file delivery as ordinary immutable or
  versioned HTTP objects.

The data plane must not expose TOS private keys, escrow internals, Worker
settlement state, or Scheduler authority to the End Client.

### 9.2 Control plane

The customer-facing control plane should eventually expose provider-neutral
operations equivalent to:

```text
Create / update / disable Distribution
Verify customer domain
Configure origin and origin authentication
Configure cache key, TTL, stale, and retention policy
Configure signed URL/cookie policy
Preload object generation
Purge object generation or cache-key revision
Read traffic, bandwidth, cache-hit, error, and SLA metrics
Export bounded access and billing logs
Inspect finalized Quote, escrow, Receipt, and settlement references
```

The exact REST, Connect, or SDK surface is a separate adapter specification. Its
database is not canonical TOS state.

### 9.3 Traffic steering

V1 may use one or more of:

- CNAME plus GeoDNS;
- Anycast front doors;
- HTTPDNS for mobile applications;
- manifest or URL rewriting to a provider-owned hostname; and
- an optional client SDK for stronger delivery evidence and path control.

Routing decisions may use client region, ASN, carrier, object presence, Worker
health, trust tier, congestion, cost, and policy. These are operational choices,
not protocol authority.

---

## 10. Worker protocol

### 10.1 Worker onboarding

A Worker Operator should:

1. resolve or register its Agent identity;
2. publish a worker-supply Capability version;
3. delegate a bounded Worker Endpoint and evidence signer;
4. install a signed Worker release in a dedicated runtime boundary;
5. allocate an isolated cache directory and explicit bandwidth/storage limits;
6. pass protocol, integrity, Range, crash-recovery, and resource tests;
7. publish a short-lived availability advertisement; and
8. accept only work covered by a finalized worker Quote and funded escrow.

A dashboard registration or Scheduler row is not sufficient authority.

### 10.2 Placement ticket

The Scheduler issues a signed, bounded Placement Ticket. A future focused
specification should bind at least:

```text
network identity
ticket profile + version
ticket ID and nonce
provider Agent / delegated Scheduler identity
worker Agent / Endpoint identity
worker Accepted Quote commitment
object-generation digest
source/fetch-grant digest
maximum origin bytes
storage bytes and retention window
region / jurisdiction / trust-tier constraints
evidence-profile digest
not-before and expiry
```

The Worker verifies the ticket, Quote, delegation, expiry, bounds, and object
manifest before fetching. It stores the object only after all size and digest
checks pass.

### 10.3 Placement state machine

```text
proposed
  -> accepted
  -> fetching
  -> verified
  -> available
  -> expired | evicted | purged | quarantined
```

A crash must not turn partially fetched bytes into an available object. Restart
recovers or discards the partial state according to a journaled transaction.

### 10.4 Delivery authorization

A delivery request must be authorized by the customer/provider access policy.
Depending on the adapter, authorization may be represented by:

- a signed URL;
- a signed cookie;
- a provider-issued request ticket;
- an authenticated tunnel/front-door request; or
- an SDK-generated request carrying an optional client acknowledgement path.

The authorization binds a distribution, object/cache identity, expiry, and any
range or audience restriction. It must not grant general access to the Worker or
origin.

### 10.5 Delivery state

A Worker records a bounded delivery attempt as:

```text
authorized
  -> started
  -> complete | partial | failed
  -> included in evidence window
```

Retries and byte ranges require stable identities so the same authorized
transfer is not billed twice merely because a connection resumed. Exact rules
belong in the metering profile.

### 10.6 Purge and eviction

A purge directive is signed, monotonically revisioned, bounded to a
Distribution/cache key/object generation, and expires. Workers fail closed on a
revision gap until they refresh authoritative provider state.

Eviction caused by local capacity policy must be reported; it cannot be shown
as continued cache presence. A pinned or reserved object may be evicted only
under the failure and refund terms committed by the worker Quote.

---

## 11. Scheduler and routing

### 11.1 Scheduler responsibilities

The Scheduler may:

- discover and verify Worker Capabilities;
- consume short-lived availability advertisements;
- benchmark and classify Workers;
- purchase bounded worker capacity;
- assign object replicas;
- issue placement, preload, purge, and delivery tickets;
- select direct, tunneled, or front-door paths;
- steer clients;
- collect health and delivery observations;
- trigger independent challenges; and
- assemble billing-window evidence.

### 11.2 Scheduler non-authority

The Scheduler may not:

- pay an unregistered identity as if it were a TOS Agent;
- use a revoked Capability version;
- exceed the maximum worker Quote exposure;
- change the accepted asset or rate-card digest;
- substitute an evidence signer;
- claim that a private traffic counter is finalized settlement; or
- make a later database edit rewrite a previously signed evidence bundle.

### 11.3 Multi-scheduler operation

Multiple Schedulers may serve one Provider. Tickets carry the exact delegated
signer and monotonic or replay-safe identity. A Worker must not rely on a
Scheduler-local sequence that another authorized Scheduler cannot verify or
reconcile.

A future profile must define either:

- disjoint ticket namespaces per authorized Scheduler;
- a shared durable provider ticket journal; or
- a content-addressed idempotency rule that prevents conflicting allocation.

---

## 12. Worker trust tiers and TLS

### 12.1 Why trust tiers are necessary

Directly handing a customer-domain TLS private key or unrestricted origin
credential to an arbitrary household box is unacceptable. TOS identity and
payment do not make an untrusted device safe to hold another organization's
high-value credentials.

The architecture therefore distinguishes at least three deployment tiers.

### 12.2 Tier M — managed professional edge

Examples:

- provider-operated data center;
- audited independent IDC;
- carrier edge;
- managed enterprise appliance.

Tier M may terminate customer-domain TLS when the selected policy provides:

- protected key custody;
- short-lived or tightly scoped credentials where available;
- signed software and rollback protection;
- private management interfaces;
- incident response and revocation;
- independent conformance evidence; and
- explicit customer acceptance of the trust class.

### 12.3 Tier E — enterprise / NAS edge

Tier E may serve customer traffic through a provider-controlled authenticated
front door, tunnel, or provider-owned delivery hostname. Direct customer-domain
TLS termination requires the same credential and audit controls as Tier M.

### 12.4 Tier C — community / home box

Tier C must not receive:

- customer TLS master private keys;
- origin master credentials;
- unrestricted origin network access;
- customer code execution authority;
- access to the operator's unrelated files; or
- an unlimited bandwidth or storage mandate.

A Tier C Worker initially operates as an opaque cache behind a trusted
provider-controlled front door/tunnel or under a provider-owned hostname with
short-lived scoped authorization. It stores exact encrypted or public objects
and returns only bounded delivery data.

Direct customer-domain termination by Tier C is a later profile requiring an
independently reviewed credential design, revocation drill, and explicit
customer opt-in.

### 12.5 Local Worker safety

All tiers require:

- a dedicated OS identity and private state directory;
- no symlink-following or path traversal;
- exact cache and bandwidth quotas;
- bounded file descriptors, connections, headers, ranges, and request bodies;
- origin allowlists and SSRF prevention;
- immutable object verification before availability;
- signed update and rollback protection;
- crash-safe journals;
- secure deletion policy appropriate to the storage class;
- no access to unrelated host files; and
- an operator kill switch.

---

## 13. Metering, evidence, and anti-fraud

### 13.1 Metered units

The architecture supports integer units such as:

- reserved byte-seconds;
- verified available byte-seconds;
- origin-fill bytes;
- completed egress bytes;
- completed request count; and
- separately committed premium classes, such as independently attested
  delivery.

All arithmetic uses checked integers and canonical base-10 atomic amounts. No
floating-point value enters a Quote, Receipt, or settlement calculation.

### 13.2 Billing window

High-frequency events are aggregated into a bounded billing window with exact:

```text
window ID
start and end time
Customer / Provider / Worker identities as applicable
Accepted Quote commitment
rate-card digest
object/distribution scope
usage counters
evidence-profile digest
evidence Merkle root
charged atomic amount
```

The Quote fixes the maximum window duration and maximum charge. A Receipt may
charge no more than the funded maximum.

### 13.3 Evidence profiles

A focused specification should define at least these evidence classes:

#### Operator-metered

Evidence may include:

- provider-issued request/placement tickets;
- Worker-signed monotonic counters;
- exact object/range identities;
- Scheduler observations;
- cache-presence challenges; and
- bounded logs committed in a Merkle tree.

This class can support known commercial counterparties but must not be marketed
as proof that every byte reached an independent human.

#### Sampled-client

In addition to operator-metered evidence, a statistically selected subset of
clients or SDK instances returns nonce-bound delivery acknowledgements. The
sampling method, privacy treatment, minimum sample size, and confidence rule
are committed by the evidence profile.

#### Independent-attested

An independent verifier, approved appliance, trusted execution environment, or
other reviewed measurement system attests to selected storage and delivery
facts. The Quote fixes the attestor set and threshold.

### 13.4 Evidence bundle

Bulk evidence remains off-chain. A bundle should contain or reference:

- exact signed tickets;
- Worker delivery records;
- object and byte-range digests;
- cache-presence challenges;
- client samples where applicable;
- independent probe or attestation results;
- duplicate/retry reconciliation;
- usage calculation inputs;
- evidence tree construction; and
- a deterministic calculation report.

The Receipt commits the evidence root and calculation profile. An independent
verifier must be able to reproduce the charged usage from disclosed evidence
without trusting a mutable dashboard.

### 13.5 Fraud and abuse threats

The security model must explicitly test:

- self-generated or circular traffic;
- repeated use of one request ticket;
- duplicate billing of resumed ranges;
- inflated bytes or request counts;
- cache-presence claims without the object;
- substituted object bytes;
- forged geographic or ASN claims;
- Worker/Scheduler collusion;
- Customer/Provider collusion against a Worker;
- Sybil Workers pretending to be independent supply;
- replayed evidence windows;
- selective omission of failures;
- token sharing and hotlink traffic;
- purge suppression; and
- evidence-root substitution.

### 13.6 Anti-fraud controls

Candidate controls include:

- content-addressed objects and exact Range verification;
- nonce-bound, expiring, usage-bounded tickets;
- one execution/evidence identity per Quote window;
- replay-blocking journals;
- deterministic retry reconciliation;
- independent cache challenges;
- sampled client acknowledgements;
- route and traffic diversity checks;
- operator and control-domain correlation analysis;
- payout delay/challenge windows;
- conservative exclusion of unverifiable traffic; and
- slashing or bond rules only if a later profile defines objective evidence and
  due process.

A weak evidence class may earn less or be ineligible for some customers. The
classification must be explicit; it cannot be silently upgraded by a Scheduler.

---

## 14. Receipt and settlement profile

### 14.1 Customer service Receipt

A customer-facing CDN Receipt should bind:

- customer-facing Accepted Quote commitment;
- Provider Agent and authorized signer;
- service Capability and version;
- Distribution/service-policy digest;
- billing-window identity and times;
- storage, egress, origin-fill, and request usage as selected by the Quote;
- SLA calculation inputs and outcome;
- evidence-profile digest and evidence root;
- charged amount and exact asset;
- completion time; and
- failure/refund evidence where applicable.

### 14.2 Worker supply Receipt

A worker Receipt should bind:

- worker Accepted Quote commitment;
- Worker Agent, Endpoint, and authorized signer;
- worker Capability and version;
- placement/delivery ticket-set commitment;
- exact object-generation scope;
- measured storage and delivery usage;
- cache-presence and delivery evidence root;
- charged amount and asset;
- software release/evidence-agent digest where committed; and
- completion time.

### 14.3 Settlement model

The intended metered model is:

```text
fund maximum amount for a bounded billing window
  -> execute many off-chain cache and delivery operations
  -> produce one deterministic aggregate usage calculation
  -> sign one Receipt committing evidence and charged amount
  -> release charged amount and refund unused maximum
```

This requires a focused metered-settlement profile and must not be presented as
implemented by the current fixed-price first-release escrow merely because the
architecture is documented here.

### 14.4 No per-request chain settlement

One million HTTP requests do not create one million escrows or Receipts. The
billing window is the economic unit. Any future payment-channel or streaming
settlement adapter remains subordinate to the same Quote, evidence, replay, and
finality rules.

### 14.5 AIPoW relationship

A finalized, independently verifiable CDN work Receipt may later be eligible as
useful-work input to AIPoW. AIPoW scoring is additional protocol distribution,
not customer payment authority. It cannot turn an unpaid, self-declared, or
unverified traffic log into a settled CDN Receipt.

---

## 15. End-to-end lifecycle

### 15.1 Customer onboarding

1. Customer resolves a Provider Agent and exact CDN Capability version.
2. Customer verifies domain/origin control through the Provider's application
   interface.
3. Provider supplies a Quote Proposal binding the immutable service-policy and
   rate/evidence digests.
4. Customer accepts the Quote on TOS and funds bounded escrow.
5. Independent resolution confirms the exact Quote and funding.
6. Provider activates the Distribution and returns standard CDN integration
   data such as CNAME, HTTPDNS, or SDK configuration.

### 15.2 Worker onboarding and purchase

1. Provider discovers a Worker Capability and verifies the Worker Agent.
2. Provider checks live signed availability and independent benchmarks.
3. Provider accepts a bounded worker Quote and funds worker escrow.
4. Scheduler admits the Worker only after finalized verification.
5. Worker receives placement tickets inside the accepted limits.

### 15.3 Content placement

1. Customer publishes or updates an object generation at the origin.
2. Provider constructs and verifies the object manifest.
3. Scheduler selects Workers satisfying region, trust, capacity, and policy.
4. Workers verify placement tickets and fetch using a scoped grant.
5. Workers verify every chunk and the final object digest.
6. Workers atomically mark the generation available.
7. Scheduler confirms sufficient replica diversity before steering traffic.

### 15.4 Delivery

1. End Client resolves a route through CNAME, HTTPDNS, front door, or SDK.
2. Request carries the selected signed access authorization.
3. Worker/front door validates host, token, expiry, cache key, object generation,
   and Range.
4. Worker serves exact bytes or returns a typed failure.
5. Worker records bounded evidence without persisting unnecessary personal data.
6. Retry/resume logic prevents duplicate economic accounting.

### 15.5 Evidence and settlement

1. Billing window closes.
2. Scheduler and Worker seal their evidence logs.
3. Independent samples/challenges run as required by the evidence profile.
4. Deterministic usage calculation excludes duplicates and unverifiable claims.
5. Authorized signer creates the exact Receipt.
6. Counterparty verifies Receipt, evidence root, amount, and Quote bounds.
7. Settlement releases the charged amount or follows the committed refund or
   narrow dispute rule.
8. Another resolver reconstructs Quote, escrow, Receipt, and terminal outcome
   without access to the Scheduler's private database.

---

## 16. Failure and recovery model

### 16.1 Worker failure

A Worker may disappear, lose an object, run out of disk, suffer address change,
or return incorrect bytes. The control plane responds by:

- removing it from routing;
- invalidating outstanding tickets as permitted;
- creating replacement replicas;
- retaining objective failure evidence;
- applying Quote-bound SLA/refund rules; and
- never treating availability failure as permission to weaken integrity checks.

### 16.2 Scheduler failure

Workers retain enough signed ticket and Quote state to explain accepted work.
A replacement Scheduler can reconstruct active authority from finalized state
and durable Provider records. It must not reuse ticket IDs or create overlapping
payment claims.

### 16.3 Origin failure

A cache hit may continue only under the exact stale-serving policy committed by
the Distribution/service digest. A miss or expired generation fails according
to policy. An origin error cannot authorize substituted bytes.

### 16.4 Chain or resolver failure

If finality, quorum, network identity, code hash, Quote, Capability, escrow, or
signer authorization cannot be verified, new paid work fails closed. Already
cached public content may be served only if the current Quote and local
authorization remain valid under a predeclared offline window; the exact rule
must be committed and bounded.

### 16.5 Crash recovery

Worker state must durably distinguish:

```text
partial fetch
verified object
active placement
purged object
in-progress delivery accounting
sealed evidence window
submitted Receipt
settled window
```

Restart must not expose partial bytes, resurrect purged content, reuse a
one-time ticket, or submit a second Receipt for the same economic window.

---

## 17. Security requirements

A conforming implementation must address at least:

- cache poisoning and cache-key ambiguity;
- origin SSRF and DNS rebinding;
- request smuggling and header confusion;
- path traversal, symlink, special-file, and sparse-file abuse;
- decompression bombs and content-encoding confusion;
- Range amplification and overlapping-range abuse;
- token theft, replay, and clock skew;
- cross-customer object substitution;
- stale purge and revision rollback;
- customer TLS credential theft;
- origin credential leakage;
- malicious update and rollback;
- DDoS and resource exhaustion;
- log injection and evidence substitution;
- privacy leakage through raw client identifiers;
- unauthorized content retention after expiry or purge;
- malicious Worker, Scheduler, Customer, Provider, and colluding combinations;
  and
- supply-chain compromise of Worker software.

Customer payload bytes, client addresses, signed URLs, and access tokens remain
off-chain. Evidence should minimize personal data and use bounded retention.

---

## 18. Compliance and abuse boundary

TOS Edge CDN is an infrastructure protocol, not a mechanism for bypassing
telecommunications, CDN, copyright, privacy, sanctions, consumer-protection, or
ISP-contract obligations.

The protocol does not encode one jurisdiction's legal conclusion as global
truth. Each Provider and Worker Operator is responsible for operating within
its jurisdiction, licensing, network contract, and accepted content policy.

The product architecture must support:

- jurisdiction and trust-tier exclusions;
- customer and origin verification;
- abuse reporting;
- emergency disable and purge;
- transparent policy identifiers;
- retained objective audit evidence;
- no silent serving after a valid purge; and
- separation between an application abuse decision and finalized TOS payment
  facts.

Community/home Workers should be introduced only where the Provider has a
lawful operating and network-access model. The existence of a TOS Agent or
payment does not itself grant permission to resell residential bandwidth.

---

## 19. Observability and SLA

A Provider should expose, with exact source and freshness:

- request and byte counts;
- cache hit, miss, fill, and error rates;
- P50/P95/P99 time to first byte;
- delivery completion and partial-transfer rates;
- Range correctness;
- origin error and shield rate;
- purge propagation time;
- preload completion time;
- Worker availability and replica diversity;
- regional/ASN coverage;
- evidence coverage and excluded traffic;
- customer service charges; and
- Worker payout calculations.

Operational metrics are not canonical merely because they are signed. A
settlement-facing metric becomes authoritative only through the exact evidence
and Receipt profile committed by the Quote.

---

## 20. Implementation ownership

A likely repository split is:

| Repository | Responsibility |
|---|---|
| **`tos-service-spec`** | Architecture, canonical manifest/Quote/Receipt/evidence profiles, vectors, negative corpus, acceptance gates |
| **`tos-service-protocol`** | Canonical codecs, identifier/digest derivation, finalized-state verification, client/provider SDKs |
| **future `tos-edge-cdn`** | Worker daemon, cache engine, scheduler/control plane reference implementation, evidence collector, customer adapters |
| **`tos-service-gateway`** | Optional hosted discovery, proposal construction, customer API, routing and operations without semantic authority |
| **`tos-ai`** | Reusable bounded journals, artifact, update, metrics, and isolation primitives where appropriate; not the CDN execution authority by default |
| **`tosnetwork/doc`** | Worker installation, IDC/NAS/home-box deployment, customer CNAME/API integration, operations and troubleshooting guides |

The CDN Worker should remain a narrow service. It must not expose `tos-ai`'s
privileged container runtime or resurrect a retired general Edge gateway.

---

## 21. Rollout plan

### Phase 0 — specification and lab

- freeze object-generation and cache-key semantics;
- freeze customer-facing and worker Capability manifest profiles;
- freeze Placement Ticket, purge, evidence, and Receipt encodings;
- publish positive vectors and an adversarial corpus;
- implement one local Scheduler and multiple isolated Worker processes;
- prove byte, Range, purge, restart, and duplicate-accounting correctness.

### Phase 1 — professional static-content pilot

- managed IDC/NAS Workers only;
- immutable model, software, game-patch, and video-segment objects;
- HTTP/2 `GET`/`HEAD`/Range;
- provider-managed TLS and origin credentials;
- bounded prepaid worker windows;
- independent customer, Provider, Worker, and resolver;
- one finalized customer payment and one finalized Worker payment.

### Phase 2 — multi-operator and multi-region

- at least three independent Worker Operators;
- at least three regions and multiple ASNs;
- independent evidence verifier;
- multi-Scheduler recovery;
- purge and replacement under live failure;
- HTTP/3 acceptance where advertised;
- live customer traffic with published evidence coverage.

### Phase 3 — restricted community edge

- Tier C opaque caching behind provider-controlled front doors/tunnels;
- operator bandwidth/storage schedule and kill switch;
- no customer TLS or origin master keys on community hardware;
- anti-Sybil and correlated-traffic controls;
- jurisdiction and ISP-contract operating review;
- bounded payout and challenge window.

### Phase 4 — advanced community delivery

- only after independent review of direct credential and routing design;
- customer opt-in by trust tier;
- broad hardware/OS conformance;
- production incident and credential-revocation drills;
- stronger client-sampled or independently attested evidence.

---

## 22. Acceptance criteria

TOS Edge CDN is not production-accepted until all of the following are true.

### 22.1 Protocol correctness

- two independent implementations reproduce every frozen digest and encoding;
- adversarial decoders reject ambiguous cache keys, malformed manifests,
  oversized objects/ranges, replayed tickets, and substituted evidence;
- object bytes and byte ranges are identical across implementations;
- purge and version transitions are monotonic and crash safe.

### 22.2 Authority correctness

- every paid Worker and Provider is resolved from finalized Agent/Capability
  state;
- no Scheduler database can create a canonical purchase or payment;
- Quote bounds are enforced across all tickets and usage windows;
- the selected signer and endpoint are reproduced from finalized state;
- replay or protocol switching cannot execute or pay twice.

### 22.3 Data-plane correctness

- `GET`, `HEAD`, conditional, and Range conformance passes against an independent
  client suite;
- object corruption, partial fetch, origin substitution, cache poisoning, and
  purge rollback fail closed;
- restart and failover do not serve partial or withdrawn bytes;
- advertised HTTP/2/HTTP/3 and IP-family support is demonstrated, not declared.

### 22.4 Evidence and billing correctness

- deterministic calculation from disclosed evidence reproduces every charged
  unit and atomic amount;
- duplicate, resumed, failed, and unverifiable traffic is handled exactly as the
  committed profile specifies;
- evidence sampling cannot be selected after observing a favorable result;
- one billing window produces at most one economic transfer intent;
- another resolver reconstructs the terminal outcome without private Scheduler
  state.

### 22.5 Operational evidence

- a Customer outside the core team purchases service from an independent CDN
  Provider;
- the Provider purchases work from at least one independent Worker Operator;
- live traffic traverses independently operated infrastructure;
- a Worker failure, Scheduler restart, object purge, and origin failure are
  drilled;
- customer and Worker settlements finalize in the exact accepted assets; and
- evidence, source commits, binary hashes, configuration digests, and finality
  references are published in an acceptance record.

---

## 23. Open decisions requiring focused specifications

This architecture deliberately does not freeze the following without vectors,
security review, and implementation evidence:

1. exact canonical cache-key encoding;
2. exact object/chunk manifest encoding and size limits;
3. customer-facing service and worker Capability manifest schemas;
4. Placement Ticket, purge, preload, and delivery authorization encodings;
5. TLS credential model for each Worker trust tier;
6. signed URL/cookie profiles and key rotation;
7. exact metered units, rounding, and billing-window bounds;
8. evidence modes, sampling method, confidence calculation, and privacy rules;
9. aggregate CDN Receipt encoding;
10. metered escrow/release/refund state machine;
11. independent verifier and challenge rules;
12. Scheduler delegation and multi-Scheduler ticket namespace;
13. anti-Sybil/operator-independence evidence;
14. customer API and compatibility profile;
15. direct community-worker routing and credential policy; and
16. whether any future AIPoW profile accepts finalized CDN Receipts and at what
    evidence weight.

Each decision must preserve this document's authority separation and may not
create a parallel identity, payment, or settlement system.

---

## 24. Non-negotiable invariants

1. **The Worker is a TOS Agent/Endpoint acting under a verified Capability and
   delegation, not a Scheduler-created account row.**
2. **The Customer-facing Provider and each independent Worker are paid through
   explicit, separate Accepted Quotes in V1.**
3. **No high-frequency request, byte range, heartbeat, or log row becomes an
   on-chain transaction.**
4. **Finalized TOS state is the sole authority for identity, Capability, Quote,
   escrow, Receipt commitment, and settlement.**
5. **Schedulers, gateways, DNS, logs, and dashboards remain replaceable and
   non-canonical.**
6. **Every served object generation is content addressed; mutable URLs do not
   replace byte identity.**
7. **A Worker never gains unrestricted customer code, filesystem, origin, TLS,
   or network authority merely because it can earn payment.**
8. **Tier C community Workers do not directly hold customer-domain master TLS
   keys or origin master credentials.**
9. **Evidence strength is explicit and Quote-bound; weak evidence is never
   presented as cryptographic proof of all delivered bytes.**
10. **Usage arithmetic is integer, bounded, deterministic, and reproducible.**
11. **A billing window can create at most one terminal economic transfer under
    one escrow.**
12. **Availability failure never permits content-integrity, identity, Quote, or
    settlement verification to fall back to a weaker authority path.**
13. **Bulk content, raw client data, logs, and evidence remain off-chain and are
    disclosed only as policy permits.**
14. **Another resolver can reconstruct every trust-bearing commercial fact
    without access to the Provider or Scheduler's private database.**
15. **TOS Edge CDN expands the existing Agent economy; it does not create a
    second CDN-specific economy.**

---

## 25. Completion criterion

The architecture is implemented when an external customer can use a standard
CDN integration to deliver immutable content through independently operated
edge infrastructure, while:

- the customer resolves and pays one verified CDN Provider Agent;
- the Provider resolves and pays independent Worker Agents;
- Workers store and serve exact content-addressed bytes under bounded policy;
- the selected evidence profile objectively supports the charged usage;
- customer and Worker Receipts are independently verifiable;
- settlement is reconstructed from finalized TOS state; and
- replacing the Gateway, Scheduler, or dashboard does not change identity,
  commercial terms, or terminal payment facts.

At that point TOS Edge CDN is not merely a distributed cache demonstration. It
is an open, economically accountable edge-delivery network whose trust-bearing
facts remain portable across operators.