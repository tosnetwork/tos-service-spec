# Paid-Demand Binding to the Existing Accepted Quote Rail V1

**Status:** incubation design; schema freeze, implementation, and independent
acceptance pending

**Existing-rail status:** the Native commercial rail already supports the
bounded Capability-first lifecycle from Quote Proposal through finalized
Accepted Quote, stablecoin escrow, Native Execution Gate, bounded execution,
Receipt, release or refund, and finalized settlement. This document does not
replace that rail.

**Blocking status:** paid-demand Provider Offer acceptance and execution remain
blocked until the discovery profile's D2 two-source, source-plus-database
shutdown, and independent-verifier gate passes, and until the binding extension,
Provider Offer authorization, per-Offer determinism, Provider-private admission,
and proof-of-possession input-delivery requirements in this document are frozen,
implemented, and independently verified.

## 1. Purpose

This document defines the smallest safe handoff from a selected paid-demand
Provider Offer into the existing TOS Service Accepted Quote lifecycle.

The boundary is:

```text
Paid Demand + active Mutation
  -> Provider Offer + buyer selection
  -> typed paid-demand Quote-binding extension
  -> existing Accepted Quote and escrow rail
  -> existing Native Execution Gate and bounded executor
  -> existing Receipt, release/refund, and settlement rail
```

Only the first three lines add paid-demand semantics. The final three lines are
the existing commercial rail, extended only where it must decode and enforce
the new binding. There is no second Quote, market escrow, execution authority,
Receipt, ledger, settlement protocol, or application-owned commercial truth.

The public discovery and direct response profile is defined in
[`AGENT_PAID_DEMAND_DISCOVERY_V1.md`](AGENT_PAID_DEMAND_DISCOVERY_V1.md).
The existing rail remains governed by:

- [`SETTLEMENT.md`](SETTLEMENT.md);
- [`ACCEPTED_QUOTE_TVM_V1.md`](ACCEPTED_QUOTE_TVM_V1.md);
- [`STABLECOIN_ESCROW_TVM_V1.md`](STABLECOIN_ESCROW_TVM_V1.md);
- [`NATIVE_EXECUTION_GATE_V1.md`](NATIVE_EXECUTION_GATE_V1.md);
- [`SOFTWARE_WORK_EXECUTION_V1.md`](SOFTWARE_WORK_EXECUTION_V1.md);
- [`SOFTWARE_WORK_RECEIPT_TVM_V1.md`](SOFTWARE_WORK_RECEIPT_TVM_V1.md);
- [`SAFE_HANDOFF_V1.md`](SAFE_HANDOFF_V1.md); and
- [`OPENFOX_ECONOMIC_BRIDGE_V1.md`](OPENFOX_ECONOMIC_BRIDGE_V1.md).

Where this document conflicts with an existing rail invariant, the existing
normative specification prevails until an explicit versioned extension is
approved in that specification. Implementations must not silently fork the
rail in application code.

## 2. Why a binding extension is required

The existing Capability-first rail proves that OpenFox can participate in a
narrow paid lifecycle. It already provides canonical Quote construction,
deterministic escrow, finalized funding checks, at-most-once execution,
objective Receipt processing, and finalized settlement recovery.

Paid-demand selection introduces facts that the current Accepted Quote does
not bind completely:

- buyer Agent-to-existing-escrow-wallet binding (the existing escrow terms
  already bind the exact buyer and Provider wallet addresses);
- stable Demand identity and the selected active Mutation;
- the selected Provider Offer and Provider consent;
- exact task input and source commitments;
- task-level output, validator, and evidence profiles;
- the buyer upload proof-of-possession key and Provider-selected ingress;
- Provider Offer delegation and acceptance-time revocation ordering.

Those facts cannot live only in Messenger prose, a Selection Notice, a Gateway
row, an OpenFox journal, or an opaque digest whose typed preimage is unavailable
after the market disappears. The approved solution must therefore be a
versioned extension of the existing Accepted Quote preimage and resolver
surface.

If the existing Quote schema gains a generic, reconstructible typed-extension
mechanism that satisfies every field below, this profile uses it. Otherwise the
existing Accepted Quote, escrow StateInit, resolver, Gate comparison, and safe-
handoff schemas are versioned together. The existing Receipt continues to link
transitively through the Quote commitment unless a separate review proves a
concrete schema gap. Either approach retains one commercial state machine and
one authoritative settlement rail.

Accepted Quote schema 1 has no extension slot, and its frozen decoders reject
trailing data. An implementation therefore needs an explicit Accepted Quote
schema successor (or a separately approved generic extension), a corresponding
escrow code/parser identity, and resolver, safe-handoff, and Gate support for
that version. Existing schema-1 Quotes and escrow contracts remain unchanged.
This is a versioned payload/parser integration, not an application-side digest
or a second lifecycle.

Schema 1 keeps its frozen deployment-as-acceptance rule and cannot carry this
profile. It is never reinterpreted as having the successor state below.

That successor also needs a recoverable buyer-acceptance transition. Its
deterministic StateInit starts in `pending_acceptance`; deployment alone is not
Quote acceptance. Only a versioned `accept` operation authenticated by the
exact buyer wallet committed in escrow terms may transition the contract once
to `awaiting_funding`. A third party may deploy the public StateInit first, but
cannot consume or block that transition. When the address is undeployed, the
buyer wallet may carry the same StateInit and `accept` operation in one message;
when it was predeployed, the identical operation remains valid. The finalized
`pending_acceptance -> awaiting_funding` transition is the paid-demand Quote
acceptance event. The operation names the expected Quote commitment and Offer
digest; an exact replay after acceptance is an idempotent observation of the
same state, while a different sender or commitment cannot mutate it. Ambiguous
submission resolves the exact escrow state before retry. Funding remains a
later transition.

## 3. Authority boundary

| Decision or fact | Authority |
|---|---|
| demand publication and current observed Mutation | signed paid-demand artifacts plus historical/current Agent authorization checks |
| Provider consent to exact work | canonical Provider Offer authorization over one typed body |
| buyer Agent publication intent and handoff context | exact signed active Demand Mutation and its `BuyerHandoffProfile` |
| buyer commercial acceptance of one exact Provider Offer | finalized versioned escrow `accept` transition authenticated to the exact bound buyer wallet |
| execution funding eligibility | later exact finalized stablecoin funding notification under the existing escrow lifecycle |
| execution admission | existing shared Native Execution Gate after decoding and comparing the extension |
| objective result | existing software-work Receipt bound to the existing Quote commitment and its current input/source/result fields |
| release, refund, and realized revenue | existing finalized escrow and wallet state |

A Provider Offer is not an Accepted Quote. A Demand signature is not commercial
acceptance or payment. A Selection Notice is not selection authority. A buyer-
side preference to choose only one Provider is not a global chain invariant.
Provider-private capacity state is not public acceptance authority. Finalized
TOS state remains the only commercial authority after handoff.

## 4. Typed handoff objects

### 4.1 `BuyerHandoffProfile`

Every active Demand Mutation contains the complete buyer-to-rail context needed
before a Provider signs:

- buyer Agent identity and signed Demand authorization context;
- the exact buyer wallet already represented by the existing typed escrow terms;
- Agent generation, controller-policy/delegation digest, proof profile, portable
  issuance-authority reference, and validity bounds for the Demand;
- the dedicated upload proof-of-possession key/profile and validity bounds; and
- the accepted existing Quote, escrow, task, and private-input profile versions.

The signed Demand Mutation authenticates this profile. V1 does not add a
post-Offer `accepted-work.accept` Agent signature. Buyer commercial acceptance
is the versioned escrow's on-chain `accept` transition authenticated to the
exact bound buyer wallet, and funding is the later exact stablecoin
notification. The wallet transaction authorization stays outside StateInit
identity. This removes a second buyer-controlled signature byte string from
Quote/StateInit identity and keeps a predeployment from consuming acceptance.

### 4.2 `PaidDemandQuoteBindingBodyV1`

The Provider constructs one unsigned canonical binding body from the exact
active Demand Mutation, its `BuyerHandoffProfile`, one preallocated durable
Offer identity, and Provider-selected execution terms. It fixes every semantic
fact that must remain identical through Offer authorization, Quote construction,
execution admission, and settlement recovery.

It includes at least:

- complete network domain and paid-demand Quote-binding profile version;
- the exact `BuyerHandoffProfile`;
- stable Demand identity, terminal-safe active Mutation sequence, and exact
  Mutation digest;
- Provider Offer identity and `max_acceptances = 1`;
- Provider Agent, Capability ID/version, and manifest digest;
- exact Provider `provider-offer.sign` key, delegation/mandate digests,
  validity bounds, proof profile, and portable authority-reference digest;
- task profile/version and operation descriptor;
- exact input digest, source digest, media type, and byte/file bounds;
- required output, validator, and evidence profiles;
- Provider-selected transport, private-input ingress, and execution-signer
  commitments;
- exact TOS-network asset and Provider price in atomic units;
- Offer acceptance and any additional input/work delivery deadlines; and
- equality commitments to every existing typed Quote/escrow preimage:
  network, Provider Agent, Capability/version/manifest, transport, asset/amount,
  buyer/Provider wallets, funding/refund deadlines, execution signer, and
  objective release/timeout-refund profile encoded by the existing dispute-
  policy cell; V1 has no dispute state.

Repeated values are equality constraints, never second authorities. Existing
Quote and escrow fields remain authoritative for their native meanings.

The body fixes semantic fields but does not alone derive the final Quote or
StateInit. The complete canonical Provider Offer, including its one exact proof,
plus the existing typed rail preimages determine those bytes. Provider-private
writer generations and reservation/admission identifiers never appear in the
public body or proof.

### 4.3 `ProviderOfferV1` and Quote binding

The Provider authorizes the body once:

```text
paid_demand_binding_body_digest
  = H(body-domain || canonical PaidDemandQuoteBindingBodyV1)

provider_offer_authorization
  = canonical ProviderProofContext
      || Sign_provider(provider-domain || paid_demand_binding_body_digest
                       || H(canonical ProviderProofContext))

provider_offer_digest
  = H(offer-domain || canonical PaidDemandQuoteBindingBodyV1
      || canonical provider_offer_authorization)

PaidDemandQuoteBindingV1
  = PaidDemandQuoteBindingBodyV1
  + canonical provider_offer_authorization
```

`ProviderOfferV1` is the body plus that exact Provider proof.
`PaidDemandQuoteBindingV1` is the same exact-byte object carried by the
versioned existing Accepted Quote. It is a Quote extension payload, not separate
accepted state.

The exact Provider proof bytes are part of one exact Provider Offer identity.
A different valid signature over the same body is a different, conflicting
Offer, not a second encoding of the same Offer. The buyer cannot substitute or
re-wrap the proof while preserving Offer identity.

The finalized buyer-wallet-authenticated `accept` transition on the
deterministic escrow carrying this exact binding is buyer commercial
acceptance. No additional buyer Agent signature is required or embedded. Exact
stablecoin funding remains a later existing-rail transition.

## 5. Construction and handoff sequence

The only valid fixed-price handoff sequence is:

1. Resolve and verify the exact active Demand Mutation, mutation history,
   `BuyerHandoffProfile`, authority references, expiry, and observed fork
   evidence under the discovery profile.
2. Preallocate one durable Provider Offer identity and construct the complete
   canonical `PaidDemandQuoteBindingBodyV1` without signatures.
3. Derive the stable body digest and semantic action ID.
4. Reserve owner-private portfolio exposure and obtain the exact runtime
   capacity lease for that body.
5. Pass Provider-wide custody admission, then create the Provider authorization
   and signed Provider Offer.
6. Deliver the exact signed Offer bytes through an ambiguity-resolving response
   transport.
7. The buyer verifies the exact Provider Offer and selects it locally. A
   Selection Notice is optional and non-authoritative.
8. The deterministic escrow StateInit embeds the versioned Accepted Quote,
   complete `PaidDemandQuoteBindingV1`, exact buyer wallet, and
   `pending_acceptance` state. Deployment creates no Accepted Quote authority
   and may safely occur before the buyer acts.
9. The exact bound buyer wallet sends the versioned `accept` operation. The
   contract authenticates the sender and transitions once from
   `pending_acceptance` to `awaiting_funding`; wrong senders cannot consume or
   disable that transition. Finality of this state transition is Quote
   acceptance.
10. The buyer funds that exact escrow through the existing asynchronous
   stablecoin transfer-notification path. A broadcast acknowledgement is not
   funding; the Provider waits for exact finalized funded state.
11. Finalized resolution returns the existing Accepted Quote and escrow state
    plus the complete typed binding and Provider proof without a market
    database.
12. The existing Native Execution Gate verifies its normal Capability, Quote,
    escrow, signer, and replay invariants and additionally compares every
    paid-demand binding field.
13. The existing bounded executor, objective Receipt, release/refund, and
    settlement paths continue under their governing specifications.

No step may construct a second Quote or escrow identity from a different nonce,
wallet, proof wrapper, input, deadline, transport, or application journal field.
Retries reuse the same canonical bytes and stable semantic action identity.

## 6. Binding sufficiency matrix

| Fact | Pre-acceptance artifact | Existing-rail accepted authority | Enforcement |
|---|---|---|---|
| display summary, topics, hints, rank | Demand/index only | none | local presentation only |
| buyer Agent-to-wallet context and upload key | active Demand Mutation | exact body plus finalized versioned escrow `accept` transition authenticated to the bound wallet | authority resolver, escrow, ingress |
| Demand identity/sequence/digest | Demand Mutation | body provenance link, not a claim of a global feed head | resolver and Gate compare exact values |
| Quote acceptance for one Offer | exact Offer identity, body, and Provider proof | finalized `pending_acceptance -> awaiting_funding` transition authenticated to the bound buyer wallet | versioned escrow and resolver |
| execution funding eligibility | existing Quote | later exact finalized funded escrow state | existing resolver and Gate |
| Provider Offer identity and consent | Provider Offer | body Offer identity plus Provider proof | resolver, Gate, private admission journal |
| Provider Capability/version/manifest | Demand predicate and Offer | body plus existing Quote/Registry fields | existing finalized Registry checks |
| task profile and operation | Demand and Offer | body | spec-defined executor mapping |
| input/source commitments and bounds | Demand and Offer | body | ingress and Gate |
| output, validator, evidence | Demand and Offer | body transitively committed by the existing Quote | validator; existing Receipt remains bound through Quote commitment and its existing fields |
| transport, ingress, execution signer | Offer | body | transport, ingress, Gate |
| asset, amount, deadlines, objective release/timeout refund | Demand and Offer | body plus existing Quote/escrow fields | custody, escrow, Gate, settlement |
| Provider consent and buyer commercial acceptance | Provider Offer plus signed Demand context | exact Provider proof plus finalized buyer-wallet-authenticated `accept` transition | resolver and Gate |
| Selection Notice | negotiation only | none | correlation only |
| skill internals, cost, margin, model rank | none | none | owner-private OpenFox policy |
| source coverage or moderation | index observation only | none | local discovery policy |

Existing rail fields are reused as follows:

| Semantic value | Existing authoritative preimage |
|---|---|
| network | Accepted Quote `network_domain` |
| Provider Agent, Capability/version, manifest | Quote identity/version cells |
| endpoint, transport security, request bound | typed Native transport binding |
| asset and fixed Offer price | Quote economic asset and maximum amount; the fixed-price escrow requires that exact amount |
| buyer/Provider wallets and funding/refund deadlines | typed existing escrow terms |
| execution signer | Quote authority and escrow execution authorization |
| objective release/refund mode | existing Native objective dispute-policy cell |

The only paid-demand acceptance-state delta is the successor's
`pending_acceptance -> awaiting_funding` transition. After that transition, the
existing asynchronous funding, execution admission, objective release, timeout
refund, and settlement semantics continue unchanged. Schema 1 is not used or
reinterpreted for this paid-demand path.

The extension adds only buyer Agent-to-wallet context, Demand/Mutation/Offer
provenance, Provider Offer proof, task/input/source and
output/validator/evidence commitments required before first claim, upload
proof-of-possession/ingress context, and any non-escrow deadline not already
bound by the existing rail.

No field may have two inconsistent authoritative sources. Every execution input
must trace to the finalized existing Quote and its reconstructible extension.

## 7. Per-Offer single acceptance and multi-Offer semantics

V1 Provider Offers are buyer-specific and single-use. One exact Demand Mutation,
buyer Agent/wallet, Provider terms, binding body, and exact Provider proof
determine one `PaidDemandQuoteBindingV1`, one existing Quote commitment, and one
existing escrow StateInit/address.

The existing rail has no cross-escrow atomic selection primitive. For the
versioned paid-demand successor, deterministic deployment creates only
`pending_acceptance`; the bound buyer wallet's finalized `accept` transition
creates Quote acceptance, and stablecoin funding arrives later through an
asynchronous transfer notification. This profile therefore does not claim that
one on-chain operation can select a demand-wide winner and fund the escrow
atomically.

After Quote acceptance but before funding, the Provider retains the obligation
and capacity through the funding deadline. If finalized resolution then proves
that no exact funding notification can still become authoritative, OpenFox may
project `unfunded_expired` and release capacity. No money was accepted, so this
is not a refund or a new escrow terminal state, and execution never begins.

`max_acceptances = 1` means one exact Provider Offer can derive only one Quote
commitment and one escrow address. Exact retry resolves that same identity; a
buyer-selected nonce, wallet, proof wrapper, or other variant cannot create a
second purchase from the Offer.

Different Provider Offers for the same Demand remain independent commercial
offers. If a buyer finalizes and funds more than one, every exact funded Quote
is independently valid and every Provider may perform the work. The buyer's
custody policy and local journal may enforce an owner preference such as
"accept one Provider", but that preference is not global authority and cannot
invalidate another finalized funded Quote.

A future auction or exclusive-work profile may add a dedicated coordinator
contract with a demand-wide compare-and-set. That is a separate protocol and
contract change, not part of this minimal binding extension. Until then, user
interfaces must say `selected locally` or `accepted and funded`; they must not
claim `unique global winner`.

## 8. Provider-private reservation and admission

Before Provider authorization, OpenFox atomically reserves local portfolio
exposure and obtains a runtime lease bound to Provider scope, stable action ID,
Offer identity, body digest, Demand/Mutation, resources, exact-asset exposure,
expiry, and `max_acceptances = 1`.

One local reservation is insufficient when several OpenFox instances, signer
keys, mandates, or runtimes share a Provider identity. Every production
`provider-offer.sign` path therefore passes through one Provider-private
admission authority, normally inside purpose-limited custody. It maintains:

- an exclusive writer lease with Provider scope, instance identity, expiry,
  and monotonically increasing fencing generation;
- a rollback-resistant generation high-water mark and authorization issuance
  ledger in one linearizable persistence domain;
- every signed/unexpired Offer and accepted/unsettled obligation;
- aggregate exact-asset exposure and runtime capacity;
- one unresolved Offer constraint for each `(provider scope, demand identity,
  active Mutation digest)` tuple; and
- stable semantic action IDs, canonical request digests, signatures,
  dispositions, and deterministic Quote/escrow resolution results.

Lease acquire, renewal, and takeover use compare-and-swap. Takeover increments
the fencing generation before a new writer may sign. Custody atomically rejects
an expired or stale generation, conflicting body/action, missing runtime lease,
unresolved tuple conflict, or aggregate policy violation. It commits the
high-water mark, admission result, signature result, and exposure before
returning signature bytes. Exact retry returns the recorded result. Writer
generation and retry attempt are private audit fields and never alter public
canonical bytes.

A replacement writer inherits unresolved Offers and obligations. A partitioned
old writer cannot sign with its stale generation. Even a single-process
deployment holds an operating-system lock on the canonical private state
directory for the daemon lifetime and still uses custody-side fencing.

After restore or migration, custody must prove that its generation high-water
mark and complete issuance ledger are at least as recent as every authorization
it emitted. If it cannot, it disables affected Offer keys and mandates. Recovery
requires finalized revocation or rotation, reservation of the old mandate's
maximum possible exposure/capacity, and resolution of every known on-chain
obligation. Because no global Offer source exists and an unknown deterministic
escrow address cannot be scanned, external observations cannot prove the
escaped-Offer set complete. Fresh signing remains blocked until all protocol-
and mandate-bounded Offer-acceptance, funding, obligation, and refund
windows have elapsed after finalized revocation and all known Quotes/escrows are
resolved. A copied subset, a claimed exhaustive index, or an incremented stale
counter is insufficient.

This ledger prevents Provider overcommitment. It is not a public market
database, transaction authority, or settlement authority.

## 9. Private input delivery

V1 uses buyer push to a Provider-selected, Offer-bound ingress. A Provider never
fetches a URL, host, repository, object store, or credential selected by remote
Demand text, buyer messages, model output, or task content.

The active Demand Mutation binds the buyer upload proof-of-possession key and
profile in `BuyerHandoffProfile`. The Offer and body copy that exact value;
the finalized extension also binds the Provider-selected ingress and TLS
identity. The upload key has no wallet, Agent-control, or market-signing power.

Only after the existing Quote and escrow are finalized and exactly funded:

1. the Provider issues a short-lived single-task challenge outside model/task
   content, bound to Quote, escrow, execution ID, input/source digests, bounds,
   expiry, stable upload action ID, and buyer upload key;
2. the buyer signs the canonical request/body digest and pushes the committed
   bytes to the bound ingress;
3. ingress authenticates Quote, escrow, proof of possession, Provider/TLS
   identity, challenge scope, expiry, operation, and body; bearer-only access is
   insufficient;
4. ingress checks ciphertext/plaintext digest as applicable, media type,
   compressed and decompressed sizes, file count, canonical paths, and archive
   rules;
5. one atomic durable operation consumes the challenge and binds the accepted
   immutable bytes to the existing Gate claim fields: Quote commitment, escrow
   address, execution ID, input digest, and source digest; and
6. the ingress maps into an existing task-admitting transport and the shared
   Native Execution Gate before the bounded executor. It creates no pre-Gate
   execution slot.

Exact retry returns the same delivery receipt. Conflicting bytes, proof,
identity, or concurrent claimant fail without replacement. Ambiguous delivery
uses a bounded status query before retry. Credentials and private source never
enter public artifacts, Opportunity Magnets, model context, Receipt, logs, or
evidence. Redirects, arbitrary DNS, proxies, credential forwarding, buyer-
selected egress, and pull fallback are forbidden.

## 10. Existing Gate, Receipt, and recovery integration

The Native Execution Gate retains its existing authority, claim fields, and
at-most-once record keyed by `(Quote commitment, escrow address)`. The versioned
paid-demand profile adds field-by-field checks over the signed Demand Mutation,
Provider Offer proof, authority bounds, acceptance-time revocation ordering,
the exact buyer-wallet-authenticated escrow `accept` transition, task/input/source,
validation/evidence, transport, signer, amount, and deadlines. The Gate may
record execution identity on first claim; it cannot choose a missing expected
value or create a second admission slot.

The existing software-work Receipt remains the objective result and release
input. Its existing Quote commitment transitively binds the versioned paid-
demand payload, and its current schema already binds input/source and objective
result fields. This profile does not require a second Receipt field unless a
separate concrete binding-sufficiency review proves one is missing.

After Quote finality, public-feed state is irrelevant to recovery. Existing
safe handoff and finalized escrow/wallet resolution must reconstruct the Quote,
typed extension, signed Demand context, Provider proof, Receipt,
release/refund, and settlement
without a Gateway, Messenger database, market index, OpenFox journal, or
Provider-private admission ledger.

## 11. Repository ownership

| Repository or component | Extension responsibility |
|---|---|
| `tos-service-spec` | paid-demand Quote-binding fields, proof contexts, private-input profile, mappings into existing rail schemas, vectors, and invariants |
| `tos-service-protocol` | canonical construction/verification, deterministic handoff into the existing Quote builder, finalized resolver output, Gate comparisons, reuse of the existing Receipt binding, and safe-handoff helpers |
| `tos` | versioned existing Accepted Quote/escrow representation; no market database or new selection coordinator in this profile |
| `openfox` | body proposal, private reservations, custody admission client, Offer orchestration, and recovery; no custody or settlement authority |
| `tos-ai` | Offer-bound capacity lease, private ingress profile, existing bounded execution, validation, evidence, and artifacts |
| custody tools | Provider-wide writer fencing, aggregate admission, exact semantic confirmation, purpose-limited signing, and rollback-safe issuance history |
| `tos-messenger` and Gateways | exact-byte Offer/selection transport only; no accepted-state authority |

No repository may implement an application-private paid-demand transaction
and later present it as the canonical TOS Service rail.

## 12. Conformance and adversarial tests

The extension requires frozen positive vectors and mutations for:

- complete body, signed Demand context, and Provider proof context/signature;
- acyclic digest and deterministic existing Quote/StateInit reproduction in two
  independent implementations;
- wrong Demand, Mutation, Offer, Agent, buyer wallet, `accept` sender,
  Capability, input/source, task,
  validator/evidence, transport, signer, asset/amount, or deadline;
- missing, detached, wrong-body, wrong-scope, expired, or revoked proofs;
- alternate otherwise authorized key, threshold subset, proof path/wrapper,
  portable authority reference, or non-canonical signature;
- buyer context or upload key differing from the active Mutation;
- public bytes containing Provider-private fencing or reservation data;
- opaque digest without reconstructible typed body and Provider proof;
- two Quotes/escrows from one Offer and any buyer-controlled construction
  variance;
- third-party predeployment followed by successful bound-wallet acceptance;
  rejection of a wrong-sender `accept`, duplicate/conflicting `accept`, funding
  before acceptance, and acceptance after its deadline;
- deterministic one-Offer/one-Quote reproduction; independent acceptance of two
  different Provider Offers; and rejection of a second Quote identity derived
  from one Offer;
- Provider writer takeover, stale generation, aggregate exposure overflow,
  storage rollback, incomplete restore, and escaped-signature recovery;
- private-input bearer theft, wrong proof key, concurrent overwrite, exact
  retry, conflicting body, ambiguous acknowledgement, and status recovery;
- Gate field substitution and cross-transport replay; and
- restart before and after reservation, Offer delivery, predeployment, the
  buyer-wallet `accept` transition, Quote finality, reservation conversion,
  input admission, Gate claim, Receipt, and settlement.

Existing rail conformance tests remain mandatory and must pass unchanged except
where an explicitly versioned vector is added. Passing the paid-demand extension
tests cannot waive any existing Quote, escrow, Gate, execution, Receipt, refund,
safe-handoff, or settlement invariant.

## 13. Acceptance criteria

The paid-demand binding is accepted only when:

1. the existing commercial rail is identified by exact released versions and
   its current conformance suite remains green;
2. two independent implementations reproduce every extension digest, Provider
   proof, existing Quote commitment, and escrow StateInit;
3. the selected body, signed Demand context, and Provider proof are
   reconstructible from finalized state without market infrastructure;
4. one Offer cannot yield two Quotes or escrows, while separately accepted and
   funded Provider Offers remain independently valid under the existing rail;
5. third-party predeployment cannot create acceptance or block the exact bound
   buyer wallet from completing the one canonical `accept` transition;
6. Provider-private fencing prevents stale or partitioned writers and aggregate
   overcommitment without entering public canonical bytes;
7. private input reaches only the bound proof-of-possession ingress after exact
   finalized funding;
8. the existing Gate rejects every extension-field substitution and executes
   each exact funded Quote at most once;
9. the existing Receipt/release/refund and finalized provider-credit paths
   remain authoritative; and
10. crash recovery at every handoff boundary creates no duplicate commercial
    action.

Until these criteria are met, discovery and local simulation may proceed, but
paid-demand-sourced Provider Offer acceptance and automatic execution remain
disabled. The existing Capability-first commercial rail is unaffected.
Passing this binding profile is necessary but not sufficient for commercial
use: the complete D2 gate in
[`AGENT_PAID_DEMAND_DISCOVERY_V1.md`](AGENT_PAID_DEMAND_DISCOVERY_V1.md)
must also pass.

## 14. Explicit non-goals

This profile does not create:

- a second Quote, escrow, Execution Gate, Receipt, ledger, or settlement state
  machine;
- an application database that can declare accepted work or payment;
- a globally authoritative market head, index, or order book;
- a globally unique Provider winner or atomic cross-escrow selection contract;
- natural-language authority for work, signatures, execution, or payment;
- public storage of private task input or Provider-private admission state;
- a replacement for existing Capability, custody, objective refund, or safe-
  handoff rules; or
- proof that a task is profitable, lawful, safe, or successfully completed
  merely because its Offer or Quote is valid.

## 15. Open schema decisions

Before implementation, the specification PR must freeze:

1. the exact `PaidDemandQuoteBindingBodyV1` and Provider proof protobuf fields,
   bounds, canonical ordering, digest domains, and positive/negative vectors;
2. the Accepted Quote successor or generic typed-extension mechanism, including
   unknown-version and trailing-data behavior while schema 1 remains unchanged;
3. the corresponding escrow StateInit/code identity, deterministic address
   derivation for one exact Provider Offer, initial `pending_acceptance` state,
   buyer-wallet-authenticated `accept` message and transition, wrong-sender and
   duplicate behavior, deadline, predeployment recovery, and funding rejection
   before acceptance;
4. resolver, safe-handoff, and Native Execution Gate version dispatch and exact
   field-by-field comparison rules;
5. historical Provider delegation proof, current eligibility, revocation/
   expiry ordering at Quote acceptance, and canonical proof representation;
6. the buyer-push challenge, proof-of-possession, encryption, retention, status,
   and existing Gate-claim mapping; and
7. the Provider-private fencing/admission interface and rollback-safe recovery
   evidence required before custody can release a signature.

None of these decisions may introduce a second settlement lifecycle or claim
demand-wide exclusivity without a separately specified coordinator contract.
