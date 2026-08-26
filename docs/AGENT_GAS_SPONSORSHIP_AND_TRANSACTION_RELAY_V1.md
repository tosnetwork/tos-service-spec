<!-- markdownlint-disable MD013 -->

# Decentralized Agent Gas Sponsorship and Transaction Relay V1

**Status:** normative V1 application-profile release candidate. A runtime
enables each service-mode/assurance-level pair from its current capabilities
and owner configuration as defined in §2.2. Prior production deployment,
transaction volume, campaign completion, or external certification is not a
readiness prerequisite.

**Profile URI:** `tos.agent-service.transaction-relay.v1`

**Media types:**

| Object | Media type |
| --- | --- |
| service profile | `application/vnd.tos.agent-relay-service-profile.v1+cbor` |
| signed requester quote object | `application/vnd.tos.agent-relay-quote-request.v1+cbor` |
| signed Provider quote object | `application/vnd.tos.agent-relay-provider-quote.v1+cbor` |
| execution-request object | `application/vnd.tos.agent-relay-execution-request.v1+cbor` |
| side-effect admission request | `application/vnd.tos.agent-relay-side-effect-admission-request.v1+cbor` |
| signed side-effect admission receipt | `application/vnd.tos.agent-relay-side-effect-admission-receipt.v1+cbor` |
| ResolveAdmission call/result | `application/vnd.tos.agent-relay-resolve-admission-call.v1+cbor` / `application/vnd.tos.agent-relay-resolve-admission-result.v1+cbor` |
| signed resolution object | `application/vnd.tos.agent-relay-resolution.v1+cbor` |
| nonterminal sponsorship-credit observation | `application/vnd.tos.agent-relay-sponsorship-credit-observation.v1+cbor` |
| signed terminal-evidence object (V1 wire name retains `finality`) | `application/vnd.tos.agent-relay-finality-evidence.v1+cbor` |
| Agreement binding | `application/vnd.tos.agent-relay-agreement-binding.v1+cbor` |
| Quote HTTP call/result | `application/vnd.tos.agent-relay-quote-call.v1+cbor` / `application/vnd.tos.agent-relay-quote-result.v1+cbor` |
| Submit HTTP call/result | `application/vnd.tos.agent-relay-submit-call.v1+cbor` / `application/vnd.tos.agent-relay-submit-result.v1+cbor` |
| Resolve HTTP call/result | `application/vnd.tos.agent-relay-resolve-call.v1+cbor` / `application/vnd.tos.agent-relay-resolve-result.v1+cbor` |
| Evidence HTTP call/result | `application/vnd.tos.agent-relay-evidence-call.v1+cbor` / `application/vnd.tos.agent-relay-evidence-result.v1+cbor` |

The eight Provider HTTP envelope media types and the Action Authority admission
media types are normative and are never substituted with an embedded object's
media type. In particular, Submit transports
`SubmitCallV1 { request, agreement }`, and every response transports its typed
Result wrapper rather than a bare signed object. This prevents two independent
implementations from decoding different canonical CBOR shapes at the same
endpoint.

**Composes:**
[`AGENT_INTENT_EXCHANGE_V1.md`](AGENT_INTENT_EXCHANGE_V1.md),
[`SEMANTIC_ACTION_IDENTITY_V1.md`](SEMANTIC_ACTION_IDENTITY_V1.md), and
[`OPENFOX_AGENT_GIFTS_V1.md`](OPENFOX_AGENT_GIFTS_V1.md)

## 1. Purpose

An Agent may possess a completely authorized, client-signed TOS transaction
but lack native TOS in its source Agent Account for network gas. It may also
need an independently operated service to submit the exact transaction and to
resolve a broadcast whose response was lost.

This optional profile permits a Provider to:

- make an ordinary bounded native-TOS top-up to the source Agent Account;
- submit exact client-signed transaction bytes without rebuilding or
  re-signing them; or
- do both, provided the top-up satisfies the exact signed release threshold
  before the client transaction is relayed; each obligation then closes only
  under the exact terminal evidence predicate signed before Agreement
  authorization.

It creates no central market, shared database, global action head, privileged
Gateway, chain opcode, paymaster contract, bridge, or alternative transaction
truth. Providers advertise through ordinary signed supply Intents and contract
through generic Agreements. Direct self-funded submission remains valid.

The keywords MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT,
RECOMMENDED, NOT RECOMMENDED, MAY, and OPTIONAL are interpreted as BCP 14.

## 2. Authority and implementation boundary

This is an Agent Commerce application profile above Native transactions. It
adds no `NativeActionV1` variant and changes no Registry state machine.

The containing signed Intent authenticates an advertised
`RelayServiceProfileV1`. A signed requester quote request authenticates the
requested bounds and exact signed-byte digest. A signed Provider quote
authenticates price, exposure, finality, endpoint, policy revision, and
validity. A generic Agreement separately authorizes Provider delivery and each
fee. `AuthorizedActionV1`, `WriterFenceV1`, the transaction inspector, and any
custody profile authorize the underlying client action. Only independently
verified evidence satisfying the exact pre-authorized predicate proves the
outcome. Relay and sponsorship terminal assurance are selected independently:

- relay terminal evidence is `validator_finality` or the lower-assurance
  `provider_corroborated`; and
- sponsorship terminal evidence is `validator_finality` or the
  lower-assurance `client_corroborated`.

Only `validator_finality` is a validator-authenticated chain-finality claim.
`provider_corroborated` authenticates a relay conclusion through the selected
Provider evidence source, while `client_corroborated` authenticates a
sponsorship conclusion through the independently re-querying client. Neither
lower class may be presented as validator or network-wide finality.

Every relay signature authority lookup is scoped by the complete
`NetworkDomainV1`, not only `network_id`. An Agent key authorized for one
genesis domain is not implicitly authorized for another domain that reuses the
same display ID. A multi-network Provider must have an owner-resolved authority
binding for every advertised domain.

A Provider HTTP response, quote, signature, journal row, submission receipt,
transaction hash, mempool observation, or node acknowledgement is not
canonical chain evidence. The bridge relayer and the Native Registry relayer
have different input and completion semantics and MUST NOT be reused by
reinterpretation for this service.

### 2.1 Service mode and assurance level are orthogonal

The selected service **mode** states which side effects are requested:

| Mode | Side effects |
| --- | --- |
| `relay_exact` | submit the byte-identical already signed client transaction |
| `sponsor_only` | create the separately authorized Provider top-up only |
| `sponsor_and_relay` | finalize the top-up, then submit the byte-identical client transaction |

The selected **assurance level** states which operational trust and recovery
claim the runtime makes:

| Assurance level | Required operational claim |
| --- | --- |
| `trusted-local` | one owner-selected local or explicitly trusted Provider binding; no independent-Provider or decentralized-resilience claim |
| `authorized-single-provider` | signed profile, quote, Agreement and admission evidence plus an authenticated Provider transport and exact Resolve; no failover or decentralized-resilience claim |
| `autonomous-decentralized` | the authorized-single-provider requirements plus at least two owner-pinned, independently operated Provider choices, portable independently verifiable evidence, and durable recovery; `relay_exact` additionally supports the released route-successor failover |

Every mode can be paired with every assurance level when the exact pair passes
§2.2. Choosing a lower assurance level never weakens the complete network pin,
exact signed bytes, underlying action authority, fee/exposure bounds,
single-primary write, durable ambiguity journal, or truthful-resolution rules.
It changes only which Provider identity, transport, provenance and recovery
properties are claimed.

`RelayServiceProfileV1` advertises `supported_assurance_levels[]`. The requester
selects one exact `assurance_level`; the signed Provider quote, generic
Agreement binding, side-effect admission request and receipt, ResolveAdmission
lookup, signed resolution and every route successor preserve it. It is not a
mutable preference or an ordered fallback. Changing it requires a new quote
and a newly authorized Agreement. A client MUST NOT create that replacement
while any prior side effect for the same underlying action is ambiguous; it
first resolves the admitted route to profile-qualified terminal evidence or
continues querying without changing semantic identity.

For `trusted-local`, the trusted binding comes only from explicit owner
configuration. An in-process adapter or local IPC transport may be used; IPC
peer identity and filesystem permissions are verified by the owner runtime and
are never selected from an untrusted Intent locator. The wire objects remain
typed and digest-bound so moving the same request to a remote Provider cannot
silently inherit local trust.

For sponsorship modes, two configured Providers permit competitive selection
before the first admission; they do not authorize a second top-up after an
ambiguous or completed write. V1 intentionally keeps sponsorship
`route_attempt = 1`. Portable evidence makes the selected route independently
recoverable after Provider loss, but automatic sponsorship failover requires a
future profile revision that binds the exact predecessor proof into admission.

### 2.2 Capability-based readiness

Readiness is evaluated independently at startup and again immediately before
admission. It is not a coarse process-wide flag. The cache and query key is the
complete current `RelayEvidenceCapability` tuple:

```text
network                                  # complete NetworkDomainV1
transaction_profile_uri
transaction_profile_digest
underlying_action_kind
mode
assurance_level
relay_terminal_evidence_class?           # relay modes only
relay_finality_profile?                  # complete URI, digest, class, thresholds
sponsorship_terminal_evidence_class?     # sponsorship modes only
sponsorship_terminal_profile?            # complete URI, digest, class, thresholds
sponsorship_release_evidence_class?      # sponsorship modes only
sponsorship_release_profile_uri?
sponsorship_release_profile_digest?
```

An absent component is canonical only when the selected mode does not request
that side effect. No answer may be reused for another network, transaction
profile, action kind, mode, assurance level, evidence class, profile digest,
or release predicate. For the currently implemented direct enablement path,
`underlying_action_kind` is exactly `payment.direct`. A future released action
kind is a different capability tuple and requires its own inspector and Action
Authority support.

The deterministic inputs are:

- owner enablement for the exact pair;
- the Provider profile's advertised mode and assurance level;
- the current configured network, transaction inspector, Action Authority,
  custody, journal, broadcaster, resolver and transport capabilities; and
- for `autonomous-decentralized`, the current owner-pinned Provider and failure
  domains.

The runtime MAY advertise, quote, and enable a tuple immediately when the
owner has enabled it and every exact dependency above passes its current
query, including mode-specific absence-proof support. It does not wait for a
production deployment, live transaction count, campaign, certification, or
calendar age. If any dependency is missing, stale, substituted, unknown, or
inconsistent, that exact tuple is `not_ready` and all side effects for it fail
closed. Other exact tuples remain independently eligible.

All pairs require a complete network-domain pin, exact transaction inspection,
underlying-action authority, one single-primary Submit boundary, a durable
ambiguity journal, and truthful resolution that never upgrades an
acknowledgement into finality. Sponsorship pairs additionally require active
sponsorship custody, a linearizable exposure ledger and an exact durable
sponsorship-transaction journal, plus a concrete terminal-evidence resolver
and verifier that can eventually close the obligation, accounting, and
exposure under the terminal predicate signed before authorization. A
Provider-local observation Adapter alone is never a complete sponsorship
capability. `trusted-local`
requires an explicit trusted Provider binding. `authorized-single-provider` requires verified
profile/quote/Agreement signatures, authenticated transport and exact Provider
Resolve. `autonomous-decentralized` requires those controls plus pinned
provenance, portable independently verifiable evidence, rollback-resistant
linearizable side-effect admission, a rollback-resistant owner-wide route
journal with monotonic generation/sequence, a rollback-resistant Provider
journal for quote/stage consumption and exposure, and at least two distinct
Provider and operator failure domains. A same-host file lock or restorable JSON
journal does not provide those rollback-resistant capabilities. For `relay_exact`,
autonomous readiness also requires route-chain successor recovery. For
sponsorship, it requires competitive initial selection and Provider-loss
evidence recovery, while the V1 action remains single-route after admission.

Every selected `FinalityProfileV1` contains its own
`terminal_evidence_class`. The signed class scalar and the class inside the
selected profile MUST match. The class namespaces are component-specific and
are never interchangeable:

| Component | Signed class field | Allowed classes | Exact lower-assurance profile URI |
| --- | --- | --- | --- |
| relay | `relay_terminal_evidence_class` | `validator_finality`, `provider_corroborated` | `tos.relay.provider-corroborated-terminal.v1` |
| sponsorship | `sponsorship_terminal_evidence_class` | `validator_finality`, `client_corroborated` | `tos.sponsorship.client-corroborated-terminal.v1` |

`relay_exact` selects only the relay class/profile;
`sponsor_only` selects only the sponsorship class/profile and release
descriptor; `sponsor_and_relay` selects both class/profile pairs plus the
release descriptor. `autonomous-decentralized` requires
`validator_finality` for every selected component. A lower class is valid only
for `trusted-local` or `authorized-single-provider` and only under its exact
URI, digest, thresholds, authentication flag, and owner-enabled verifier.

The current TOS RPC-backed relay evidence source is explicitly
lower-assurance. It may advertise
`relay_terminal_evidence_class = provider_corroborated` only with the exact
`tos.relay.provider-corroborated-terminal.v1` profile and reports
`relay_validator_authenticated_portable_proof = false`. It may support direct
`trusted-local` or `authorized-single-provider` enablement when the complete
capability tuple passes, but it does not satisfy or advertise an
`autonomous-decentralized` relay claim. A validator-authenticated portable
source is a separate capability, not a relabelling of this RPC result.

For sponsorship, `trusted-local` and `authorized-single-provider` may satisfy
the release threshold with either portable validator-authenticated finality or
an owner-enabled, bounded `agreement-payment-rpc-corroboration.v1` Adapter.
The first bounded observation remains `observed_unproven`: it may advance the
local `sponsorship_credit_observed_unproven` substate and, after a fresh
balance, sequence and expiry recheck, permit the byte-exact client relay. It
does not itself terminalize work, recognize revenue, release exposure, or
authorize another top-up. A later independent client re-query may close the
exact sponsorship obligation as `corroborated_terminal` only when the signed
sponsorship terminal profile URI is exactly
`tos.sponsorship.client-corroborated-terminal.v1` and its canonical digest
commits the complete threshold, history, maturity, destination-credit, and
reorg predicate. The resulting evidence class is `client_corroborated`; it may
release local exposure and settle accounting under that owner-selected lower
assurance, but it is not validator finality. `autonomous-decentralized`
requires portable validator-authenticated sponsorship finality and rejects
`client_corroborated` evidence.

The release threshold is not inferred from assurance and is not selected by a
Provider response. The requester freezes one exact descriptor in its signed
quote request, the Provider copies it byte-for-byte into its signed quote, and
the Agreement binding copies it again:

```text
sponsorship_release_evidence_class       # validator_finality | observed_unproven
sponsorship_release_profile_uri
sponsorship_release_profile_digest
```

Those three fields are absent for `relay_exact` and required for sponsorship
modes. They are separate from the component terminal selections, which are
also frozen before authorization:

```text
relay_terminal_evidence_class?
relay_finality_profile_uri?
relay_finality_profile_digest?
sponsorship_terminal_evidence_class?
sponsorship_terminal_profile_uri?
sponsorship_terminal_profile_digest?
```

The relay triplet is present exactly for `relay_exact` and
`sponsor_and_relay`. The sponsorship triplet is present exactly for
`sponsor_only` and `sponsor_and_relay`. The Provider Quote embeds the complete
selected profiles as `relay_finality_profile` and
`sponsorship_terminal_profile`; the Agreement binding copies both scalar
triplets and the sponsorship release descriptor. Missing fields, extra
mode-inapplicable fields, class/profile disagreement, or a changed digest fail
before reservation or any side effect.

`sponsorship_release_evidence_class = validator_finality` requires the release
URI and digest to equal the selected sponsorship terminal profile.
`observed_unproven` is permitted only for `trusted-local` or
`authorized-single-provider`; its URI is exactly
`agreement-payment-rpc-corroboration.v1` and its digest is an owner-pinned
concrete Adapter capability. A missing, substituted, unknown, downgraded, or
late-selected descriptor fails before reservation or any side effect.

Each signed component profile is its terminal predicate; neither is chosen
after either party accepts. When the release class is `observed_unproven`, the
sponsorship terminal class MUST be `client_corroborated` and the sponsorship
terminal profile URI MUST be exactly
`tos.sponsorship.client-corroborated-terminal.v1`. Its complete parameters and
digest are copied through the requester object, Provider Quote, Agreement
binding, execution, and side-effect admission. An earlier object selecting a
different or observation-only profile cannot later gain `client_corroborated`
terminal meaning. When the release class is `validator_finality`, the
sponsorship terminal class is `validator_finality` and the selected
sponsorship profile governs the portable chain proof. The relay profile remains
independent in combined mode. Mixed components are allowed only when each was
pre-authorized and the terminal outcome truthfully uses the lower whole-result
label defined in §14; mixed or late-selected classes otherwise fail closed.

For the released bounded-RPC Adapter, the digest is derived from the concrete
descriptor, not copied from a configuration string. The descriptor commits the
full network domain, the sorted canonical public-origin/locator-identity/
operator-provenance member set, strict-majority threshold,
`maximum_history_transactions` in the inclusive range `1..10000`, exact
submitted-message and destination-credit requirements, and
`validator_finality_proven = false`. A member's `endpoint` is its canonical
public origin only: scheme, DNS name or IP literal, and the canonical effective
port representation (default ports are omitted). It contains no user
information, path, query, or fragment. The `locator_identity_digest` commits
the credential-independent canonical full RPC locator, including its path,
without publishing that locator. API keys, credentials, unrelated local
configuration and byte formatting are excluded. They remain bound only by the
owner-private snapshot identity. Provider and client configurations that use
the same canonical locator and operator therefore reproduce the same release
profile even when their credentials and configuration bytes differ. A
query-only preflight computes this same descriptor from the owner configuration
before readiness, Quote, and admission. A runtime that cannot reproduce the
configured digest is `not_ready` for that exact pair.

The locator identity is exactly
`sha256(locator_domain || uint64be(locator_length) || canonical_locator)`, where
`locator_domain` is the ASCII bytes
`tosctl.agreement-payment-rpc-locator-identity.v1\0` and
`canonical_locator` is UTF-8. The canonical locator has a lowercase canonical
host, canonical effective-port representation, no user information, query,
fragment, percent encoding, backslash, dot segment, empty interior segment, or
redundant trailing slash. The configured locator MUST already equal this
canonical representation; parser-normalized aliases are rejected. Changing its
origin or path changes the identity; changing only a credential or local file
representation does not. V1 treats the path as non-secret routing
metadata: bearer tokens, API keys and other credentials MUST NOT be encoded in
it and instead use the private credential field/header. A deployment whose path
is itself a bearer capability is `not_ready` for this profile until a future
blinded, operator-authenticated service-identity profile is selected.

The V1 descriptor digest is exactly
`sha256(domain || uint64be(json_length) || compact_json)`, where `domain` is
the ASCII bytes `tosctl.agreement-payment-rpc-corroboration-profile.v1\0`.
The compact UTF-8 JSON recursively sorts every object key by Unicode code
point. Arrays retain order; members are already sorted by public-origin
`endpoint`, then `locator_identity_digest`, then operator provenance. The
descriptor has exactly this field set:

```text
profile_uri
network_domain { network_id, global_id, zero_state_root_hash,
                 zero_state_file_hash, workchain_id }
members[] { endpoint, locator_identity_digest, operator_provenance }
threshold
maximum_history_transactions
strict_majority
exact_submitted_message
exact_destination_credit
validator_finality_proven
```

There is no whitespace, HTML escaping, alternate numeric representation,
unknown field, or platform-dependent URL rendering. Implementations MUST
reproduce the released cross-language descriptor/digest vector before
advertising the capability.

Preflight does not create a check/use gap. Before the first sponsorship write,
the owner runtime durably freezes the exact configuration snapshot or its
content-addressed bytes and all descriptor inputs with the route and
sponsorship journals. Every later Resolve for that action uses that frozen
snapshot. Configuration rotation applies only to new quote requests; it cannot
change the evidence profile of an admitted or ambiguously funded action.
The private snapshot identity commits the release-profile digest, the exact
member-configuration content digests, and a fresh cryptographically random
256-bit snapshot nonce. The nonce stays in the owner-private manifest and is
never emitted with the public identity, so that identity is not an offline
oracle for API keys or other configuration secrets.
Its V1 digest uses the same framed compact-JSON construction with domain
`tosctl.agreement-payment-rpc-corroboration-snapshot.v1\0` and the exact object
fields `config_content_digests`, `evidence_profile_digest`, and
`snapshot_nonce`; member content digests retain the profile member order and
the nonce is exactly 64 lowercase hexadecimal digits.
The exact locator, configuration bytes, credentials and absolute paths remain
owner-private. A snapshot manifest uses only single-component relative member
names, and the preflight capability returns a bounded relative
`corroboration_snapshot_handle` that the owner resolves beneath the exact
configured snapshot root. Absolute paths and traversal components are invalid.
The V1 handle is exactly
`corroboration-<snapshot-identity hex>/manifest.json`; the embedded lowercase
hex equals the 64 hexadecimal digits after `sha256:` in the accompanying
snapshot identity. It is not accepted as an ambient filesystem path.
Capability documents, signed profiles, observation objects, errors, and logs
expose only the canonical public origin and locator identity digest. RPC
failures expose one bounded protocol category and, when useful, that public
origin; they never include the raw transport error or request URL.

The bounded-RPC release descriptor's verifier enforces its member set,
operator-provenance uniqueness and strict-majority threshold for the initial
`observed_unproven` gate. The separately signed sponsorship terminal profile
governs the later sponsorship predicate. Under
`tos.sponsorship.client-corroborated-terminal.v1`, its observer, operator,
confirmation/maturity, reorg, and resolution bounds are evaluated by the
client over its pre-Quote frozen query snapshot. Under a validator profile,
they govern portable validator-authenticated sponsorship finality. The relay
terminal profile, when selected, independently governs the client transaction.
The stages remain
separate: an initial observation cannot claim terminality, while terminal
semantics cannot be selected after authorization.

The result is `ready` only when every required capability is presently true;
otherwise it is `not_ready` with bounded reason codes. Deployment age, a
"production" label, completed transaction count, prior campaign, external
certification and CI history MUST NOT be readiness inputs. They are useful
quality evidence, not protocol authority. Conversely, `ready` authorizes only
the selected pair; it does not predict inclusion, payment, profitability or
finality and cannot be copied to another network, mode or assurance level.

## 3. Original action identity never changes

The client transaction already implements an economic or externally visible
action. Its released `underlying_action_kind`, `stable_action_id`, and
`exact_request_digest` remain identical across exact retry, writer takeover,
Provider failure, and Provider failover.

Provider ID, quote ID, Agreement ID, endpoint, route, retry, RPC/session ID,
writer generation, lease, wall time, and local journal key are admission or
transport facts. They MUST NOT enter the underlying semantic-action
projection. V1 therefore adds no `transaction.relay`, `gas.sponsor`, or other
relay entry to the Semantic Action Identity registry.

Sponsorship is a separate economic side effect: an ordinary Provider-to-source
top-up obligation, normally implemented with released `payment.direct`. It has
its own stable action, exact request, custody authorization, ambiguity journal,
and profile-qualified terminal evidence. The sponsorship fee and transaction-relay fee are
also separate value obligations.

Any `payment.direct` action carried by this relay profile MUST use
`AgreementPaymentRequestV3`, the domain-bound payment form. Its exact request carries
`network_domain_digest = Digest(NetworkDomainV1)`, and its
`destination_digest` semantic field commits that digest together with the
display network ID, Adapter URI, and exact destination. Legacy direct-payment
V1 requests that bind only `network_id` remain valid outside this profile but are
not relay-eligible. Thus equal display IDs on different genesis domains derive
different stable actions and exact requests before a Provider sees a BOC.

`Resolve(stable_action_id, exact_request_digest)` deliberately has no network
selector. A Provider therefore keys the stable action ID provider-wide, not
per network, and treats these as conflict:

- same stable action ID, different network or exact request digest;
- same stable action and request, different `signed_transaction_digest`; or
- same stable action, request, and transaction bytes, different
  `relay_execution_request_digest`.

The conflicting submission never overwrites the admitted record. A different
Provider may use a different Provider-specific quote, Agreement, and execution
digest while retaining the same underlying identity and exact transaction
bytes. There is no shared head.

## 4. Canonical encoding, digests, and signatures

The JSON model is
[`agent-relay-service-v1.json`](../schemas/agent-relay-service-v1.json). Wire
objects use RFC 8949 Core Deterministic CBOR. Maps have text keys only and are
ordered by encoded-key length then encoded-key bytes. Integers use their
shortest representation. Indefinite values, floats, tags, duplicate keys,
invalid UTF-8, noncanonical Base64, unknown fields, and alternate spellings
fail closed.

All repeated collections described as sets are strictly sorted by the released
key and reject duplicates. The implementation limits are:

- signed transaction: 65,536 decoded bytes;
- underlying canonical action request in this profile: 192 KiB raw, whose
  canonical JSON-model base64 spelling is exactly 256 KiB at the boundary;
- complete canonical object or HTTP request/response body: 1 MiB;
- quote/execution lifetime: 900 seconds;
- service-profile lifetime: 90 days;
- service endpoints: four;
- fee lines and fee obligation IDs: two; and
- evidence references or observation digests: 64 total after merging any
  sponsorship-action and client-transaction absence sets; and
- Provider route attempts for one underlying stable action: 32.

The common digest formula is:

```text
Digest(domain, value) = "sha256:" || lower_hex(SHA-256(
  "TOS-PROTOCOL-CBOR\0" ||
  uint16_big_endian(len(domain)) || domain || canonical_cbor(value)))
```

The frozen digest domains are:

| Value | Domain |
| --- | --- |
| `NetworkDomainV1` | `tos.agent-relay-network-domain.v1` |
| `RelayTransactionIdentityV1` | `tos.agent-relay-transaction-identity.v1` |
| `RelayServiceProfileV1` | `tos.agent-relay-service-profile.v1` |
| `RelayQuoteRequestV1.body` | `tos.agent-relay-quote-request.v1` |
| `ProviderRelayQuoteV1.body` | `tos.agent-relay-provider-quote.v1` |
| `RelayAgreementBindingV1` | `tos.agent-relay-agreement-binding.v1` |
| execution-request projection in §9 | `tos.agent-relay-execution-request.v1` |
| complete signed `AuthorizedActionV1` | `tos.authorized-action-envelope.v1` |
| `RelaySideEffectAdmissionReceiptBodyV1` | `tos.agent-relay-side-effect-admission-receipt.v1` |
| `RelayResolutionV1.body` | `tos.agent-relay-resolution.v1` |
| `RelayAbsenceObservationReferenceV1` | `tos.agent-relay-absence-observation-reference.v1` |
| `RelayFinalityEvidenceV1.body` | `tos.agent-relay-finality-evidence.v1` |

`signed_transaction_digest` is instead
`sha256:` plus the raw SHA-256 of the exact signed bytes. The immutable
transaction profile separately computes `signed_transaction_cell_hash` as
`tvm-cell-sha256:<64 lowercase hex>` and `transaction_intent_digest`. The
underlying `exact_request_digest` retains its
released formula:

```text
"sha256:" || lower_hex(SHA-256(
  "tos.action-request.v1\0" || uint32_big_endian(length) ||
  underlying_action_request))
```

Those four values have different purposes and are never substituted.

### 4.1 Signature domains

Requester quote requests, Provider quotes, Action Authority admission receipts,
Provider resolutions, and Provider terminal evidence use Ed25519 over:

```text
message = SHA-256(domain_with_trailing_NUL ||
                 uint32_big_endian(len(canonical_body)) || canonical_body)
```

| Signed object | Domain including its final NUL |
| --- | --- |
| requester quote request | `tos.agent-relay-quote-request-signature.v1\0` |
| Provider quote | `tos.agent-relay-provider-quote-signature.v1\0` |
| Action Authority side-effect admission receipt | `tos.agent-relay-side-effect-admission-receipt-signature.v1\0` |
| Provider resolution | `tos.agent-relay-resolution-signature.v1\0` |
| Provider terminal evidence (V1 domain name retained) | `tos.agent-relay-finality-evidence-signature.v1\0` |

The public key in an envelope is not self-authorizing. A verifier resolves the
named requester, Provider Agent, or owner Action Authority as appropriate and
proves that the exact key was authorized at the signed object's validation
time.

## 5. Discovery: `RelayServiceProfileV1`

A Provider places the exact profile bytes in the detail of a normal signed
Intent whose discovery card contains `OFFER` and `SERVICE`. The Intent issuer
equals `provider_agent_id`; its detail descriptor commits the bytes and the
content type above. A new offer is a normal Intent revision or new Intent, not
an entry in a special relayer registry.

The object fields are exactly those represented by `RelayServiceProfile` in
`pkg/agentrelay`:

```text
schema_version = 1
profile_id, revision, provider_agent_id
network_domains[]
supported_modes[]
supported_assurance_levels[]
transaction_profiles[]
finality_profiles[]
fee_assets[]
exposure_limits[]
maximum_request_bytes
admission_limits {
  maximum_quote_reservations,
  maximum_active_executions,
  maximum_active_per_requester,
  maximum_quote_requests_per_window,
  maximum_quote_requests_per_requester_window,
  quote_request_window_seconds
}
endpoints { quote_url, submit_url, resolve_url, evidence_url }
policy_revision
created_at_unix, expires_at_unix
```

Network domains sort by network ID, global ID, both zero-state hashes, then
workchain. Modes and assurance levels sort lexicographically. Transaction and
finality profiles sort by URI then digest. Fee assets and exposure limits sort by namespace,
identifier, then unit. Every transaction profile MUST permit independent
inspection of source sequence and transaction expiry and have a byte cap no
larger than the service cap.

Each `finality_profiles[]` entry contains exactly:

```text
profile_uri, profile_digest
terminal_evidence_class
minimum_confirmation_depth
minimum_observers
minimum_operator_domains
reorg_window_seconds
maximum_resolution_seconds
```

The array is a set of individually selectable component predicates, not one
global service finality setting. A Provider may advertise validator and lower
profiles together, but a signed request selects the exact relay and/or
sponsorship entry required by its mode.

Exposure limits bind exact assets and separate per-request and outstanding
atomic maxima. They are not a promise to accept every request below the limit.
Admission limits are positive signed policy bounds. Count fields do not exceed
1,000,000, the rate window does not exceed 86,400 seconds, per-requester active
work does not exceed the Provider-global active limit, and per-requester quote
rate does not exceed the Provider-global quote rate. Quote-rate counters,
quote reservations, active executions, and sponsorship exposure are admitted
in the same Provider-wide linearizable policy domain described in §11.
Local reputation, selection, and ranking remain advisory. An
`autonomous-decentralized` client requires at least two independently operated
Providers; the other assurance levels may use one.

Distinct Agent IDs or Intent digests do not prove independent operation. A
client selecting `autonomous-decentralized` MUST resolve owner-trusted provenance
for every candidate and bind it into its durable route journal before the
first Submit. At minimum, the selected candidates have distinct operator and
failure domains, canonical endpoint origins, TLS SPKI pins, storage/authority
domains, and implementation-evidence digests. The client verifies these facts
against local configuration or separately authenticated attestations; fields
self-asserted by the Provider's own Intent are advisory. The HTTP transport
enforces the same origin and SPKI pin that the route journal records. A client
without this evidence may select `authorized-single-provider` or
`trusted-local`, but MUST NOT claim decentralized resilience.

## 6. Complete `NetworkDomainV1`

```text
network_id
global_id                  # signed int32
zero_state_root_hash       # canonical sha256 digest
zero_state_file_hash       # canonical sha256 digest
workchain_id               # signed int32
```

All fields compare exactly. A display network name, `network_id` alone, an
endpoint's report, or one zero-state hash is insufficient. The transaction
inspector proves the BOC-visible coordinates, source authority, transaction
intent, and exact signed bytes. Separately, the owner-pinned chain adapter
recomputes the digest under `tos.agent-relay-network-domain.v1` and verifies
both zero-state hashes against the selected primary and corroborating endpoints
immediately before the one permitted write. A BOC does not itself prove its
genesis hashes.

For the released TOS Agent Account transaction profile,
`source_account_authority_digest` is the digest under
`tos.agent-relay-source-authority.agent-account.v1` of the schema version,
network digest, source and owner addresses, exact Agent Account code hash and
deployment ID, global ID, TVM version, authorized Agent ID, controller public
key, and controller epoch. It deliberately excludes balance, seqno, daily
remaining allowance, and other mutable execution state: those values are read
again from finalized state at admission and immediately before broadcast.
Thus an ordinary incoming sponsorship credit does not change authority, while
a deployment, controller, epoch, Agent, owner, code, or network substitution
does.

## 7. `RelayQuoteRequestV1`

The requester sends a `SignedRelayQuoteRequest` containing only the body,
resolved requester public key, and requester signature. It MUST NOT contain,
attach, link to, or disclose the bearer-executable signed transaction bytes.
The body binds:

```text
schema_version = 1
request_id
requester_agent_id, provider_agent_id
network, mode, assurance_level, source_account, source_account_authority_digest
transaction_profile_uri, transaction_profile_digest
underlying_action_kind, stable_action_id, exact_request_digest
signed_transaction_digest, signed_transaction_cell_hash
signed_transaction_size, transaction_intent_digest
source_sequence, transaction_valid_until_unix
requested_sponsorship?                 # sponsorship modes only
sponsorship_release_evidence_class?    # sponsorship modes only
sponsorship_release_profile_uri?       # sponsorship modes only
sponsorship_release_profile_digest?    # sponsorship modes only
relay_terminal_evidence_class?         # relay modes only
relay_finality_profile_uri?            # relay modes only
relay_finality_profile_digest?         # relay modes only
sponsorship_terminal_evidence_class?   # sponsorship modes only
sponsorship_terminal_profile_uri?      # sponsorship modes only
sponsorship_terminal_profile_digest?   # sponsorship modes only
maximum_service_fee
maximum_network_fee_atomic
maximum_transaction_value_atomic
created_at_unix, expires_at_unix
```

`relay_exact` omits `requested_sponsorship`, all release-descriptor fields,
and the sponsorship terminal triplet, while requiring the relay triplet.
`sponsor_only` omits the relay triplet and requires an exact positive
`AssetAmount`, the sponsorship terminal triplet, and release descriptor.
`sponsor_and_relay` requires both terminal triplets plus the sponsorship amount
and release descriptor. Every selected class equals the class embedded in the
profile identified by its exact URI and digest. Asset amounts use:

```text
asset { asset_namespace, asset_identifier, unit }
amount_atomic
```

A ticker or decimal display amount is insufficient asset identity. Before
quoting, the Provider verifies the requester signature, complete network and
profile selection, declared byte size, sponsorship and fee/exposure ceilings,
released action-kind and digest shapes, time-window satisfiability, and local
admission policy. The
signed transaction digest, cell hash, source authority, sequence, expiry,
intent, gas, and value fields are requester commitments at this stage because
the Provider intentionally does not possess the exact bytes.

The V1 logical interface is:

```text
Quote(exact SignedRelayQuoteRequest) -> SignedProviderRelayQuote
```

A mutually authenticated, bounded HTTP `422` may report that no quote was
issued. It is a transport outcome, not a signed protocol object and not
evidence of rejection, absence, retry safety, solvency, or future capacity.
V1 deliberately does not claim a typed refusal envelope that its schema and
codec do not define.

Every Provider quote is conditional on Submit-time disclosure and independent
inspection of bytes matching every signed commitment. A Provider MUST NOT
fetch or demand the exact signed transaction during Quote. This allows a
requester to compare Providers without disclosing a bearer transaction to
parties it did not select. Only `autonomous-decentralized` requires at least
two independent candidates.

## 8. `SignedProviderRelayQuoteV1`

The signed quote body binds the exact quote-request and service-profile
digests, Provider, mode, assurance level, both component evidence-class
scalars when applicable, sorted fee lines, reserved sponsorship, exact
sponsorship-release descriptor, maximum network fee and transaction value,
accepted request size, the complete selected `relay_finality_profile` and/or
`sponsorship_terminal_profile`, status endpoint, Provider policy revision,
optional offer Intent digest, and validity.
It is a conditional commercial commitment, not proof that the Provider has
inspected or accepted the undisclosed transaction.

Fee and obligation kind strings are frozen:

```text
transaction_relay
gas_sponsorship
transaction_relay_fee
gas_sponsorship_fee
```

Required fee-line sets are:

| Mode | Fee lines in exact order |
| --- | --- |
| `relay_exact` | `transaction_relay_fee` |
| `sponsor_only` | `gas_sponsorship_fee` |
| `sponsor_and_relay` | `gas_sponsorship_fee`, `transaction_relay_fee` |

A free service still carries its separate zero-valued line. Sponsorship value
is not a fee. Fee assets equal the request's exact `maximum_service_fee` asset,
are advertised by the profile, and their checked sum does not exceed the
requester maximum. Reserved sponsorship, `maximum_network_fee_atomic`, and
`maximum_transaction_value_atomic` MUST equal the request exactly in V1; a
Provider that needs narrower bounds refuses the request and the requester
creates a new signed request. Each embedded component profile equals the exact
service-profile entry selected by the corresponding request URI and digest,
and its internal `terminal_evidence_class` equals the request and quote class
scalar. The status endpoint and policy revision equal the selected service
profile values. For sponsorship modes, all three release-descriptor fields
equal the signed request exactly; `relay_exact` omits them. Mode-inapplicable
profiles and class scalars are forbidden.

## 9. Agreement and `RelayExecutionRequestV1`

The Provider quote authorizes nothing by itself. Submit receives both the exact
`RelayExecutionRequestV1` and the complete generic `AgentAgreementV1`. The
execution request carries the Agreement body digest and expiry rather than
duplicating the Agreement inside its canonical body; the Provider recomputes
both from the accompanying exact Agreement before admission.

`RelayAgreementBindingV1` is encoded once and placed byte-for-byte in the
Agreement terms and every service obligation subject with content type:

```text
application/vnd.tos.agent-relay-agreement-binding.v1+cbor
```

It binds the quote-request, Provider-quote, and service-profile digests, mode,
assurance level, the mode-applicable relay and sponsorship evidence-class
scalars and profile URI/digest pairs, the exact sponsorship-release descriptor
when applicable, requester, Provider, underlying action ID/request, and exact
signed-transaction digest without a circular Agreement reference. The binding
copies these selections from the requester body rather than allowing the
Agreement compiler to choose a new predicate.

The Submit transport contains `{ request, agreement }`. Validation is against
the complete accompanying `AgentAgreementV1`, not an isolated binding object:
the Provider recomputes the Agreement body digest, requires its expiry to equal
the execution field, and compares the top-level `terms_content_type` and
`terms` byte-for-byte before inspecting obligations. An otherwise valid set of
obligation subjects cannot compensate for missing or different top-level
terms. Conversely, correct top-level terms cannot compensate for a missing,
duplicated, wrong-kind, wrong-party, wrong-amount, or wrong-Adapter obligation.

Applicable generic obligations are:

| Kind | Obligor | Beneficiary | Additional rule |
| --- | --- | --- | --- |
| `gas_sponsorship` | Provider | requester/source | exact reserved sponsorship amount; `tos.payment.direct.v1` adapter |
| `transaction_relay` | Provider | requester | no value amount; exact bytes and evidence profile |
| `gas_sponsorship_fee` | requester | Provider | exact corresponding quote fee |
| `transaction_relay_fee` | requester | Provider | exact corresponding quote fee |

Each obligation has the exact binding subject and complete authorization
predicates/evidence. `fee_obligation_ids` is strictly sorted, has the same
cardinality as the quote fee lines, and maps by the unique frozen obligation
kind rather than by an implementation-dependent identifier order. Combined
mode requires both delivery obligation IDs and requires sponsorship to
finalize before relay. The complete Agreement remains recoverable without a
Provider database.

The execution-request fields are exactly:

```text
schema_version = 1
quote_request, provider_quote
signed_transaction_bytes
agreement_body_digest, agreement_expires_at_unix
relay_obligation_id?
sponsorship_obligation_id?
fee_obligation_ids[]
underlying_action_request
semantic_fields[]
authorized_action
writer_fence
admission_receipt
created_at_unix, expires_at_unix
```

Only after one Provider is selected and the complete Agreement is authorized
does Submit disclose `signed_transaction_bytes` to that Provider. Before any
sponsorship, journal admission, network write, or other side effect, the
Provider MUST recompute the raw byte digest and size and MUST reparse the exact
bytes with the immutable transaction inspector. The inspected network, source,
source-account authority digest, authorized requester Agent, sequence, expiry,
cell hash, intent digest, network fee, transaction value, destination, and
payload MUST match the signed request or remain below its ceilings as
applicable. Blind broadcasting is forbidden.

The released verifier also checks quote signatures, Agreement authorization
and obligations, exact request digest, registry-ordered semantic fields,
`AuthorizedActionV1`, `WriterFenceV1`, finalized authority keys, modes, IDs,
amounts, expiries, and byte caps.

### 9.1 Execution digest deliberately excludes admission credentials

`relay_execution_request_digest` is computed over this exact projection:

```text
{
  schema_version,
  quote_request,
  provider_quote,
  agreement_body_digest,
  agreement_expires_at_unix,
  relay_obligation_id?,
  sponsorship_obligation_id?,
  fee_obligation_ids,
  signed_transaction_bytes,
  underlying_action_request,
  semantic_fields,
  created_at_unix,
  expires_at_unix
}
```

It explicitly excludes the entire `authorized_action`, `writer_fence`, and
`admission_receipt`, not only their signature fields. They are admission
credentials attached after the economic request is frozen. The Action
Authority can therefore compute and register the immutable execution digest
before issuing the receipt. Changing any projected execution field changes the
digest and conflicts with an admitted Provider record.

The exclusion does not remove authority. The receipt contract in §9.2 makes
issuance the linearization point at which the Action Authority atomically
validates current writer ownership and registers the exact Provider route and
stage mask. A stale generation cannot obtain a receipt even while its fence
signature and lease expiry remain valid. Once the receipt is issued, exactly
the stages already present in that receipt may drain after writer takeover;
takeover alone cannot add a stage, change a request, or mint a replacement
receipt. A current successor writer may admit only the byte-identical
`relay_exact` route-head transition defined in §9.2; it cannot extend an old
receipt or create a sponsorship successor. This rule avoids both
check-to-side-effect races and cancellation by an unrelated later writer
generation.

### 9.2 Side-effect admission receipt

Before Submit crosses the Provider socket, the current runtime sends this
canonical request over an owner-authenticated channel to the rollback-resistant,
linearizable Action Authority:

```text
RelaySideEffectAdmissionRequestV1 {
  schema_version = 1
  owner_id, agent_id, authenticated_principal_id
  provider_agent_id, service_profile_digest, provider_quote_digest
  network_digest, transaction_identity_digest
  mode, assurance_level, stage_mask[]
  route_attempt
  predecessor_receipt_digest?
  stable_action_id, exact_request_digest
  relay_execution_request_digest
  authorized_action, writer_fence
  underlying_action_request, semantic_fields[]
  requested_start_not_after_unix
}
```

`authenticated_principal_id` is compared with the authenticated transport
principal and with owner policy; carrying the string is not authentication.
The Authority imports the registry-ordered semantic fields, recomputes the
underlying exact request, stable action, action-envelope, and fence digests,
and verifies the complete action and fence. It deliberately does not receive
the bearer-executable signed BOC. The Provider-route, network,
transaction-identity, and execution digests are frozen opaque commitments at
this boundary; the Provider MUST recompute all four from the full Submit before
consuming a stage. An Authority receipt cannot make an inconsistent commitment
valid. The Authority derives the stage mask rather than accepting an arbitrary
capability:

| Mode | Exact canonical `stage_mask` |
| --- | --- |
| `relay_exact` | `["broadcast"]` |
| `sponsor_only` | `["sponsorship"]` |
| `sponsor_and_relay` | `["broadcast", "sponsorship"]` |

The lexical ordering above is normative. Unknown, duplicate, missing, reordered,
or mode-incompatible stages fail closed.

`transaction_identity_digest` is the digest under
`tos.agent-relay-transaction-identity.v1` of this Provider-independent
projection of the signed Quote request:

```text
RelayTransactionIdentityV1 {
  schema_version = 1
  network
  source_account, source_account_authority_digest
  transaction_profile_uri, transaction_profile_digest
  underlying_action_kind, stable_action_id, exact_request_digest
  signed_transaction_digest, signed_transaction_cell_hash
  signed_transaction_size, transaction_intent_digest
  source_sequence, transaction_valid_until_unix
}
```

The Authority recomputes it from the complete execution request. It binds the
exact signed BOC without disclosing bearer-executable bytes to the Authority.

`route_attempt` is a positive `uint32` bounded to 32 in V1. The first route is
exactly `1` and omits `predecessor_receipt_digest`. A successor is exactly the
preceding attempt plus one and binds the body digest of the immediately
preceding signed admission receipt. A skipped attempt, a fork from an older
receipt, a missing or extra predecessor digest, or arithmetic overflow fails
closed. `trusted-local` and `authorized-single-provider` are restricted to
attempt `1`; only an `autonomous-decentralized` `relay_exact` route may create
a Provider successor. The successor preserves the exact assurance level as an
immutable route-head field. An assurance change is a new commercial request,
not a successor.

In one serializable transaction, the Authority:

1. authenticates the principal and resolves the exact owner, Agent, authority,
   mandate, optional approval, and policy revision;
2. verifies the complete `AuthorizedActionV1` and `WriterFenceV1`, confirms the
   lease is still current, and advances or checks the owner/Agent writer-
   generation high-water;
3. registers the exact network, transaction identity, Provider Agent, service
   profile, Provider quote, mode, assurance level, stage mask, route attempt, predecessor,
   stable action, exact request, and relay execution digest; and
4. allocates a never-reused, strictly increasing `admission_sequence` in the
   same rollback-resistant owner/Agent authority domain, signs and durably
   stores this receipt before returning it:

```text
RelaySideEffectAdmissionReceiptBodyV1 {
  schema_version = 1
  owner_id, agent_id, authenticated_principal_id, authority_id
  provider_agent_id, service_profile_digest, provider_quote_digest
  network_digest, transaction_identity_digest
  mode, assurance_level, stage_mask[]
  route_attempt
  predecessor_receipt_digest?
  stable_action_id, exact_request_digest
  relay_execution_request_digest
  authorized_action_digest
  writer_fence_digest, writer_lease_id, writer_generation
  policy_revision, mandate_digest, approval_digest?
  admission_sequence
  issued_at_unix, start_not_after_unix
}

SignedRelaySideEffectAdmissionReceiptV1 {
  body
  public_key
  signature
}
```

`authorized_action_digest` is the released protocol digest over the complete
signed `AuthorizedActionV1` under `tos.authorized-action-envelope.v1`.
`writer_fence_digest` is the digest already bound by that action. The receipt
body digest uses `tos.agent-relay-side-effect-admission-receipt.v1`; its
signature uses the domain in §4.1. The receipt signer MUST be the same resolved
Action Authority and key as the action and fence.

The coordinator requests the minimum of every signed prerequisite. The
Authority sets and verifies:

```text
issued_at_unix < start_not_after_unix
start_not_after_unix <= issued_at_unix + 60
start_not_after_unix <= min(AuthorizedAction, WriterFence)
```

The Provider independently rejects unless the same boundary is also no later
than the execution, quote, Agreement, and transaction-validity expiries.
Checked arithmetic is mandatory. `start_not_after_unix` is a first-consumption
boundary, not a new economic expiry and never extends a prerequisite. The
Provider MUST verify and persist the receipt before that boundary. Once that
exact receipt is durably consumed in time, its already admitted stages may
continue under the original Agreement and transaction windows even if the
writer lease later changes; an unconsumed or late receipt authorizes nothing.

The exact-admission key is the complete tuple from `owner_id` through
`relay_execution_request_digest`, including the exact route, mode, assurance level, stage mask,
route attempt, and predecessor. Exact retry returns the byte-identical stored
signed receipt with the same `admission_sequence` and times.

The Authority additionally keeps one owner/Agent/stable-action route head. A
different exact request, network, transaction identity, mode, assurance level, stage mask,
principal, Action Authority ID/high-water domain, policy revision, mandate,
approval, or non-successor route is `conflict`. Writer lease ID, writer
generation, fence digest, and action-envelope digest may change after a valid
takeover, but this never permits changing that Authority domain or economic
policy context. The only V1 exception is an `autonomous-decentralized`
`relay_exact` successor whose exact
request, network, transaction identity, Authority ID, policy revision, mandate,
and optional approval are unchanged, whose stage mask is exactly
`["broadcast"]`, whose `route_attempt` is the current head plus one, and whose
predecessor digest is the current receipt body digest. The Authority advances
that head atomically with receipt issuance. On restart it authenticates every
stored receipt and reconstructs the complete consecutive predecessor chain
before trusting its last receipt as the route head; a truncated, forked, or
invariant-changing chain fails closed. `sponsor_only` and
`sponsor_and_relay` can only use attempt `1`; no V1 evidence can authorize a
second Provider-funded top-up.

After an ambiguous Admit response or crash, the runtime calls
`ResolveAdmissionV1` with the exact identity tuple over the authenticated
channel. A found result returns the same stored receipt. An authenticated
not-found from the same linearizable, rollback-resistant Authority permits only
an exact replay of the original Admit request; the atomic key still creates at
most one receipt and never a new semantic action. A timeout, unauthenticated
response, restored/older Authority database, or different Authority is
ambiguous and cannot authorize Submit.

The exact lookup is `ResolveAdmissionCallV1`, containing schema version, owner,
Agent, authenticated principal, authority, Provider Agent, service-profile
digest, Provider-quote digest, network and transaction-identity digests, mode,
assurance level,
canonical stage mask, route attempt, optional predecessor receipt digest,
stable action ID, exact request digest, and relay execution digest.
`ResolveAdmissionResultV1 { receipt }` returns only the stored signed receipt;
it cannot mint or refresh one. The authenticated transport identity must again
equal the lookup principal.

The Provider verifies all receipt bindings against the complete Submit request,
compares `authenticated_principal_id` with the authenticated Submit-channel
principal, resolves the Authority key at `issued_at_unix`, and in one journal
transaction stores the complete receipt, its body digest, and a per-stage
unconsumed bitset.
Exact receipt replay returns the existing record. A different receipt or digest
for the same Provider route/action tuple conflicts. Each stage changes its bit
at most once before the corresponding payment-custody or network sink call; a
crash resolves that same stage record and never allocates a new semantic
action. The Provider journal and every downstream sink treat the receipt digest
as an idempotency and audit binding, not as a bearer token for any other request.
The `sponsorship` stage bit authorizes entry into the frozen relay workflow; it
does not authorize value by itself. The exact Provider-funded top-up still
requires its own `payment.direct` stable action, request, custody admission, and
profile-qualified terminal evidence under §13.

### 9.3 Domain-bound custody authorization V2 and payment authorization V3

Any `tosctl` or equivalent custody boundary that signs a transaction used by
this profile MUST consume a domain-bound form of its purpose-limited
authorization. A legacy V1 authorization containing only `network_id` and
`network_global_id` may remain decodable for an explicitly non-relay migration
path, but it is never relay-eligible. The generic contract-effect form uses V2.
The sponsorship payment form MUST use V3 so custody also commits the complete
`AgreementPaymentRequestV3` digest. Both forms add exactly this object:

```text
CustodyNetworkDomainV1 {
  network_id
  global_id
  zero_state_root_hash
  zero_state_file_hash
  workchain_id
}
```

It equals the selected `NetworkDomainV1`; `workchain_id` equals the workchain
of the source Agent Account whose key custody will use. The zero-state's own
masterchain `BlockIdExt` coordinate is separately required to be canonical
`(-1, -2^63, 0)` when custody reads it from RPC and MUST NOT be confused with
the source workchain.

`CustodyActionAuthorizationV2` and `CustodyEffectAuthorizationV2` retain their
released V1 fields, set `schema_version = 2`, and insert the complete domain
immediately after the existing big-endian `network_global_id` in their signed
preimage. The inserted encoding is exactly:

```text
LP32(network_id) || i32_be(global_id) ||
LP32(zero_state_root_hash) || LP32(zero_state_file_hash) ||
i32_be(workchain_id)
```

`CustodyActionAuthorizationV3` retains the V2 payment fields, sets
`schema_version = 3`, and inserts
`LP32(agreement_payment_request_digest)` immediately after
`LP32(exact_request_digest)`. The value is the independently recomputed digest
of the exact complete `AgreementPaymentRequestV3` stored in the custody
journal. A relay sponsorship MUST NOT use payment authorization V2, because V2
does not bind that complete request.

A sponsorship V3 authorization additionally carries this all-or-none group:

```text
sponsorship_finality_profile_cbor_digest
sponsorship_release_profile_digest
sponsorship_corroboration_snapshot_identity
```

The legacy-named first value is SHA-256 over the exact deterministic-CBOR bytes
of the complete **sponsorship terminal profile** selected by the signed
Provider Quote; it never refers to the separately selected relay profile. The
other two values bind the owner-selected release Adapter and its immutable
observer snapshot. When present, their three `LP32` encodings are appended in
the order shown immediately after
`LP32(agreement_payment_request_digest)` and before `writer_generation`.
Partial presence is invalid. Ordinary V3 direct payments omit all three and
retain their original preimage bytes. A sponsorship resolver MUST compare all
three stored values before querying or resolving; the profile's external
`profile_digest` is not a self-digest and cannot by itself prevent threshold
substitution.

`LP32(x)` is an unsigned big-endian 32-bit byte length followed by the UTF-8
bytes. Every duplicated top-level network field equals the corresponding
domain field. Payment authorization retains prefix `TOS-EAA\0`; effect
authorization retains prefix `TOS-CEA\0`; both continue to sign the SHA-256 of
their complete preimage with the owner-pinned Ed25519 Action Authority key.
The fixed cross-language preimage SHA-256 fixtures are:

```text
payment V2: 8b2d089f841741ea4157783d141107b49420b98bbe5cae5c0aa74591b14e0502
payment V3: 007e848255182c6b9129c98138275540a9551ac8d0d742e8544ee0d0c51af749
sponsorship payment V3: bf8b0b09ec57d200f745e2f170abe10c8c3bc6fd3b78e442829d9ef105524ce2
effect V2:  fe281488a120f3a60e0d7584f5f9a286071df82e7a477acd990d067fc3f8ca47
```

The Go protocol and Rust custody implementations MUST reproduce those values
and reject network ID, global ID, either zero-state hash, workchain, source
account, action, complete payment-request digest, Agreement, amount,
destination, fence, mandate, approval, expiry, or signature substitution.
Custody rechecks the complete domain against its owner-pinned primary
immediately before the sole network write; the Action Authority or Provider
cannot choose the remaining coordinates from an RPC response.

## 10. Time-window satisfiability

Profiles live no longer than 90 days. Quote requests, Provider quotes, and
execution requests live no longer than 900 seconds. At admission:

```text
profile.created <= request.created < request.expires <= profile.expires
request.created <= quote.valid_from <= now < quote.expires <= request.expires
execution.created <= now < execution.expires
execution.expires <= min(quote.expires, Agreement.expires,
                         AuthorizedAction.expires, WriterFence.expires,
                         transaction_valid_until)
receipt.issued <= now < receipt.start_not_after <= execution.expires
```

For a sponsorship mode:

```text
request.created_at_unix +
  sponsorship_terminal_profile.maximum_resolution_seconds + 30
  < transaction_valid_until_unix
```

`maximum_resolution_seconds` is selected for the complete requested mode,
including sequential sponsorship and relay when combined. Before beginning
each unresolved stage, the Provider recomputes that the remaining signed
windows can still satisfy the profile. Checked arithmetic is mandatory. A task
timeout, retry policy, or later quote cannot extend signed transaction bytes,
an Agreement, an action authorization, or a fence.

## 11. Atomic journal and admission

The Provider maintains a process-independent local journal; it is not a
network or market fact. One serializable admission transaction:

1. verifies the signed admission receipt, its Action Authority and start
   boundary, and every binding to the full Submit request;
2. checks network/stable-ID, exact-request, signed-byte, execution-digest,
   receipt-digest, stage-mask, and quote conflicts;
3. consumes the receipt and quote once and initializes exactly the receipt's
   per-stage unconsumed bits;
4. validates fee, network-fee, transaction-value, source-balance, rate, and
   concurrency bounds, then atomically reserves the active quote/work slots
   and every Provider-funded sponsorship exposure; and
5. stores the complete immutable request, receipt, exact transaction bytes,
   selected sponsorship-release descriptor, and, for bounded RPC, the
   owner-private frozen snapshot locator plus manifest/content digest as
   `prepared` before returning.

Concurrent admission has one winner. Exact retry with the byte-identical
receipt returns the durable record without consuming another quote, receipt,
or exposure. A takeover writer recovers the same receipt from the Authority;
it does not replace admission credentials or obtain a new sequence. Exposure
is released only by its policy-defined terminal state, not by a process timeout
or lost response.

“Local” describes authority, not a single uncoordinated file. Every process or
host using the same Provider Agent, signing authority, custody account, or
exposure pool MUST share one linearizable, rollback-resistant admission,
receipt-consumption, stage-bit, and exposure domain. Each downstream
side-effect sink checks the exact receipt digest and stage and deduplicates its
own stable action/request identity. A same-host file lock is conformant only
for an explicitly single-host Provider. Copying or restoring an older journal,
or starting another host with an empty path, cannot lower writer generation,
forget an attempted sponsorship, or recreate exposure. Custody independently
enforces the same stable sponsorship action and aggregate spend limits, so a
rolled-back coordinator still cannot pay twice.

Before invoking the sponsorship payment Adapter, the relay journal durably
marks the record `sponsorship_resolving`; this is an internal substate of public
`prepared`. A crash between that checkpoint and the payment journal is safe:
recovery queries or recreates only the same deterministic payment action.
The snapshot locator is part of this action record, not a mutable process-wide
setting. Restart or configuration rotation loads it by the admitted action's
exact identity and verifies its manifest/content digest before any Resolve.
The protected action record also freezes every local Adapter namespace needed
to find and interpret that state, including the owner-private registry root,
custody wallet or account namespace, Provider source account, network domain,
and the exact configuration locators referenced by the manifest. These local
locators are not public wire authority, but they are part of the recovery
identity: mutable process defaults may select configuration for a new Quote and
MUST NOT redirect, strand, or reinterpret an admitted action. Recovery checks
the signed execution against the frozen manifest and invokes only the frozen
custody identity; a missing or changed locator leaves the action ambiguous and
cannot authorize a replacement top-up.
Custody first prepares, signs, and durably journals the one exact top-up BOC
while the payment Action Authority remains `prepared`. Exact prepare replay
must return that same BOC, stable action, request digest, account sequence, and
expiry. After custody confirms this durable record, the payment Action
Authority separately persists `submitted` before the first broadcast call or
network socket write. A crash before that transition may repeat exact prepare;
custody still cannot construct a second transaction. A crash after the
transition MUST invoke custody's idempotent exact-broadcast resume operation,
not payment prepare: custody atomically changes `Signed -> Broadcasting` and
submits its stored bytes, or, when already `Broadcasting`, resubmits only those
identical bytes for the same account sequence. This closes crashes on either
side of the custody `begin_broadcast` checkpoint without authorizing a new BOC,
signature, sequence, amount, or top-up. An unresolved custody query, lost
custody database, or missing row remains ambiguous and MUST NOT call payment
prepare or create a replacement transaction. If the original signed bytes
cannot be recovered, the action remains blocked until profile-qualified
terminal or non-inclusion evidence resolves that exact transaction.
Expiry cannot release a resolving sponsorship because a write may be
ambiguous. Once a sponsorship credit meets its selected terminal predicate, its amount remains charged to
the Provider's aggregate financial exposure even when the relay record becomes
terminal. A separate, idempotent local accounting release requires exact
finalized reimbursement evidence or an explicitly authorized write-off; relay
completion alone cannot replenish Provider liquidity.

## 12. State and ambiguity

The public states are:

```text
prepared submitted accepted rejected conflict terminal
```

Both `ResolveCall` and `EvidenceCall` contain exactly
`stable_action_id, exact_request_digest`; their distinct media types select the
operation without adding a mutable route or network selector to the body.

Stored transitions are:

```text
prepared  -> submitted | rejected | conflict | terminal
submitted -> accepted | rejected | conflict | terminal
accepted  -> submitted | terminal
```

`unknown` is not a signed relay state. An authenticated HTTP `404` lookup
outcome means only that this Provider has no record visible to the authenticated
requester; it carries no network, action, absence, retry, or failover authority.
The Provider MUST NOT sign a synthetic resolution for a missing row because the
two-field lookup body cannot supply the frozen network and execution context.
Resolution uses the provider-wide `(stable_action_id, exact_request_digest)`
key; an implementation MUST NOT create otherwise unresolvable per-network
duplicates for the same stable action ID.

A local query Adapter may return a typed nonterminal result with one of
`not_found`, `not_mature`, or `temporarily_unavailable`; this is diagnostic
output, not a signed service state or absence proof. Only those exact outcomes
map to an unchanged local `unknown`. Request/profile/snapshot substitution,
noncanonical input, journal conflict or corruption, replay conflict, and
malformed Adapter output are integrity errors and MUST be surfaced rather than
silently converted into `unknown`.
`accepted` is tentative. `accepted -> submitted` is allowed only after
corroborated reorg/conflicting-node evidence invalidates the observation while
preserving exact bytes. `rejected`, `conflict`, and `terminal` are immutable.
A conflict response never overwrites the original record.

The Provider persists `submitted` before the first network write. Timeout,
EOF, crash, and endpoint disagreement after that point are ambiguous, not
failure. Recovery MUST query the exact transaction hash, source account and
sequence, source execution, and destination credits before retry. It may
rebroadcast only the identical journaled bytes, only when the resolver reports
`SafeToRebroadcastExact`, and only while all signed windows remain live.

For the released TOS `sendBocReturnHash` adapter, only documented `status = 1`
plus a response hash equal to the locally computed canonical cell hash is a
tentative `accepted` result. Status zero, any other integer, a malformed or
mis-correlated JSON-RPC envelope, and every transport failure remain
`submitted`/ambiguous. No undocumented status creates `rejected` or permission
to retry. A profile may use `rejected` only when it freezes and verifies an
explicit side-effect-free rejection proof.

No ambiguous action receives new transaction bytes, sequence, signature,
request digest, or stable ID. For `relay_exact` only, after an authenticated
exact query to the selected Provider returns unavailable or leaves the prior
submission ambiguous, the current writer may select a different Provider under
the route-head transition in §9.2. That transition is a route successor, not a
new semantic or transaction successor: it preserves the byte-identical BOC,
transaction identity, Authority domain, policy, mandate, approval, request
digest, and stable ID. `sponsor_only` and `sponsor_and_relay` never gain such
permission from an unavailable or ambiguous query; they remain single-route
after admission, and §13 defines their exact evidence and recovery boundary.
This does not block a first
sponsorship attempt whose selected `(mode, assurance_level)` is currently
ready; it blocks only an unsafe second Provider-funded top-up.

## 13. Sponsorship sequencing, recovery, and future failover boundary

### 13.1 Release boundary for the exact sponsor transaction

The V1 control-plane objects and state transitions below freeze the exact
Provider-funded top-up proof needed by a conforming implementation. A public
sponsorship identity or opaque Provider recovery token is insufficient: the
evidence also commits the complete domain-bound PaymentRequest, exact signed
top-up BOC digest and cell hash, source account and sequence, destination
credit, selected terminal predicate, checkpoint, and proof bytes or
content-addressed locator.

This is a capability gate, not a deployment-history gate. Every sponsorship
pair first requires custody to persist the exact domain-bound
`AgreementPaymentRequestV3`, signed top-up bytes, source sequence and expiry in
its ambiguity journal before Submit. For `trusted-local` and
`authorized-single-provider`, the owner may then select either validator
evidence or bounded `agreement-payment-rpc-corroboration.v1` as the sponsorship
release threshold. A successful first RPC query returns structured
`observed_unproven` with process success because the query itself succeeded;
custody remains `Broadcasting`. This is not chain finality or terminal evidence.
OpenFox consumes it only through a separate observation interface, records
`sponsorship_credit_observed_unproven`, rechecks balance/sequence/expiry, and
may continue the exact relay without releasing exposure or recognizing
settlement. A later query-only verification using the client's independently
owned, pre-Quote frozen snapshot may return `corroborated_terminal` only under
the exact signed `tos.sponsorship.client-corroborated-terminal.v1` predicate.
That result closes the selected lower-assurance obligation but makes no
validator-finality or decentralized-resilience claim.

The Provider top-up reuses the generic Agent `task_send` opcode
`0x41475003`; this profile adds no consensus opcode or market-specific
contract method. Its referenced commitment cell has exactly 544 bits and zero
references:

```text
uint32  0x53504e31                       # ASCII "SPN1"
bits256 sha256(AgreementPaymentRequestV3 canonical body)
bits256 stable_action_id raw SHA-256 payload
```

Both digests are raw 32-byte SHA-256 payloads, not their textual prefixes or
hex characters. There are no trailing bits or references. For request digest
`0x11` repeated 32 times and action digest `0x22` repeated 32 times, the exact
cell hash is
`tvm-cell-sha256:00fa7b6beeb7e8ec086d2eff5fd9bff0136c4cdf8d3428c09db2b32d0a0d87a3`.
Custody reconstructs and verifies this cell before signing and the client
reconstructs it again from the embedded PaymentRequest. Thus an older genuine
same-source, same-destination, same-amount transfer cannot settle a newer
Agreement.

That cross-component observation is canonical deterministic CBOR:

```text
RelaySponsorshipCreditObservationV1 {
  schema_version = 1
  network_digest
  agreement_payment_request             # complete canonical AgreementPaymentRequestV3
  agreement_payment_request_digest
  sponsorship_stable_action_id, sponsorship_exact_request_digest
  provider_sponsor_source_account, provider_sponsor_source_sequence
  provider_sponsor_valid_until_unix
  signed_top_up_transaction_digest, signed_top_up_transaction_cell_hash
  sponsorship_payment_commitment_cell_hash
  destination_source_account, amount
  submitted_transaction_hash, source_execution_reference
  destination_credit_references[]
  evidence_profile_uri = "agreement-payment-rpc-corroboration.v1"
  evidence_profile_digest
  observed_checkpoint_id, observed_checkpoint_sequence
  observed_checkpoint_unix
  observation_digests[]
  observed_at_unix
}
```

Its digest domain is
`tos.agent-relay-sponsorship-credit-observation.v1`. It has no standalone
signature: it is returned through the authenticated, owner-pinned observation
interface and persisted in the Provider-private journal. A signed nonterminal
`RelayResolutionBodyV1` may expose only
`sponsorship_status = observed_unproven` and the exact
`sponsorship_observation_digest`, together with the sponsorship identity and
validity. Its state is `prepared`, `submitted`, or, after a combined client-
transaction submission, `accepted`; it carries no transfer reference,
terminal outcome or evidence-set digest. `prepared` covers a persisted
observation whose fresh balance/sequence/expiry recheck did not authorize the
next stage.

The observation repeats the full PaymentRequest, BOC/cell/source sequence and
expiry, network, destination, amount, evidence profile, checkpoint and
observation digests so an OpenFox instance can verify the exact bounded claim
without trusting an opaque local row. The profile digest must equal the
owner-pinned bounded-RPC Adapter capability selected at readiness and cannot be
selected by the Provider response. Its PaymentRequest binding rules are the
same as the terminal object below. It is explicitly forbidden inside
`RelayFinalityEvidenceV1`, cannot be relabelled as validator finality, and
cannot recognize revenue, release exposure, terminalize work or authorize a
second top-up.

Both sponsorship terminal classes use
`RelaySponsorshipTransactionEvidenceV1` below.
`autonomous-decentralized` requires `terminal_evidence_class =
validator_finality`, a validator-authenticated content-addressed portable proof
bundle, and an independent verifier. The two lower assurance levels may use
`terminal_evidence_class = client_corroborated` only after the independent
client re-query satisfies the exact signed client-corroborated sponsorship
terminal profile. No prior production endpoint, transaction
campaign, or external certification is required for either path.
When the selected path lacks a current required capability, only that
sponsorship pair is `not_ready`; `relay_exact` remains independently eligible. A
`RelayAbsenceObservationReferenceV1` wrapper or Provider signature alone does
not satisfy this gate and MUST NOT authorize a second top-up. Portable
database-loss vectors measure interoperability and autonomous Provider-loss
recovery; they are not proof that a configured implementation has or has not
been deployed before.

The terminal evidence object is canonical deterministic CBOR and contains:

```text
RelaySponsorshipTransactionEvidenceV1 {
  schema_version = 1
  terminal_evidence_class              # validator_finality | client_corroborated
  validator_authenticated_portable_proof
  network_digest
  agreement_payment_request             # complete canonical AgreementPaymentRequestV3
  agreement_payment_request_digest
  sponsorship_stable_action_id, sponsorship_exact_request_digest
  provider_sponsor_source_account, provider_sponsor_source_sequence
  provider_sponsor_valid_until_unix
  signed_top_up_transaction_digest
  signed_top_up_transaction_cell_hash
  sponsorship_payment_commitment_cell_hash
  destination_source_account
  amount
  submitted_transaction_hash, source_execution_reference
  destination_credit_references[]
  finalized_checkpoint_id, finalized_checkpoint_sequence
  finalized_checkpoint_unix
  confirmation_depth
  sponsorship_terminal_profile_digest
  observation_digests[]
  proof_bundle_digest
  proof_bundle?                         # bounded deterministic-CBOR bytes
  portable_proof_locator?
  observed_at_unix
}
```

It appears as `sponsorship_transaction_evidence` inside the signed
`RelayFinalityEvidenceV1.body` whenever
`sponsorship_transfer_reference` is present and is absent for a finalized-
absence result or relay-only result. The enclosing signature authenticates the
complete nested bytes. The legacy sponsorship stable action, exact request and
expiry equal the nested values. The complete canonical
`agreement_payment_request` is schema version 3; its digest is recomputed and
equals `agreement_payment_request_digest`. Its Agreement body digest and
obligation ID equal the selected execution's `agreement_body_digest` and
`sponsorship_obligation_id`; its payer/Agent is the Provider, its payee is the
requester, and its Adapter is exactly `tos.payment.direct.v1`.
`network_digest`, destination source account, amount and expiry equal the
selected complete network, source account, domain-bound PaymentRequest,
reserved quote and signed sponsorship validity exactly. The PaymentRequest
stable action and exact canonical-byte digest are independently recomputed.
The top-up transaction digest, cell hash, SPN1 commitment cell hash, Provider
source/sequence/expiry,
transaction hash, execution, destination credit, checkpoint, confirmation
depth, sponsorship terminal profile, observations and proof bundle are
independently verified before the selected terminal outcome.
`confirmation_depth` is a positive `uint32` no smaller than the selected
sponsorship terminal profile's minimum, and
`sponsorship_terminal_profile_digest` equals that profile's exact signed
digest.

`proof_bundle_digest` is
`Digest("tos.agent-relay-sponsorship-proof-bundle.v1", proof_bundle)` using the
released deterministic protocol-CBOR framing. An in-band `proof_bundle` is at
most 128 KiB and, when present, its digest MUST be recomputed. At least one of
the in-band bytes or `portable_proof_locator` is present. A lower-assurance
remote client cannot treat a Provider-local cache as independent verification:
it either verifies the signed in-band bundle or independently reconstructs the
same evidence from owner-pinned sources. `autonomous-decentralized` continues
to require the portable content-addressed locator even when in-band bytes are
also supplied.

The released TOS bounded-RPC bundle includes the complete PaymentRequestV3,
Provider source account, source sequence, transaction expiry, destination
source account, exact signed top-up BOC bytes, byte digest and TVM cell hash,
the SPN1 commitment cell hash, network and both selected profiles, frozen
snapshot identity, quorum observations and the selected predicate's terminal
checkpoint. The client recomputes and parses the canonical BOC, then re-queries
its own frozen private configuration set whose public origins,
locator-identity digests, and operator provenance equal the signed
descriptor, for that same inbound message, exact destination credit and mature
checkpoint. A set of
unsigned observation objects supplied by the Provider, even when internally
consistent and covered by the Provider's outer signature, is not independent
chain verification and MUST leave the client pair `not_ready`.

The frozen client snapshot also binds a checkpoint namespace derived from the
complete network-domain digest. The owner supplies one stable private
checkpoint storage root; the verifier derives a distinct rollback high-water
path for every full network domain. Recovery of an admitted network-A action
after the runtime is reconfigured for network B reconstructs A from the frozen
snapshot and uses A's namespace. It MUST NOT require A to equal the runtime's
current network and MUST NOT reuse B's checkpoint file. The snapshot carries
only the deterministic namespace digest, never an attacker-selected filesystem
path.

Every TOS observation binds the source transaction and the actual destination-
account transaction, not merely the source transaction's outbound message:

```text
transaction_hash, transaction_lt, transaction_utime
transaction_boc_digest
source_outbound_message_hash
destination_credit_reference
destination_transaction_hash, destination_transaction_lt
destination_transaction_utime, destination_transaction_boc_digest
destination_block_workchain, destination_block_shard, destination_block_seqno
destination_block_root_hash, destination_block_file_hash
destination_credit_atomic, destination_credit_first
destination_transaction_aborted, destination_bounce_present
destination_credit_observed_exact
```

The destination transaction MUST be ordinary, consume the exact source
outbound message, use `credit_first = true`, contain an exact credit phase for
the authorized value, and contain no bounce phase. Its transaction and block
proofs are quorum-bound. Maturity is measured from the later of the source and
destination transaction times. The current Agent Account may abort compute on
the unknown optional SPN1 body; because the internal transfer is non-bounce,
the exact credit-first credit remains economically applied. Such evidence MUST
record `destination_transaction_aborted = true` and MUST NOT claim successful
destination application execution. Any missing credit phase, wrong value,
non-credit-first transaction, bounce phase, wrong inbound message, or absent
destination transaction fails closed.

The field names `finalized_checkpoint_id`, `finalized_checkpoint_sequence`,
and `finalized_checkpoint_unix` are retained inside the sponsorship evidence
object. Their meaning is the checkpoint that makes the **selected signed
sponsorship terminal predicate** true. They do not imply validator
authentication. Only
`terminal_evidence_class = validator_finality` together with
`validator_authenticated_portable_proof = true` may make that claim. Under
`client_corroborated` they identify a client-observed maturity checkpoint and
the client-corroborated profile; the authentication flag is false.

The released TOS CLI Adapter exposes two deliberately different operations:

- Provider terminalization:
  `agent account economic-payment-sponsorship-corroborated-terminal`, returning
  schema
  `tosctl.agent-account.agreement-payment-sponsorship-corroborated-terminal.v1`,
  state `corroborated_terminal`, `chain_side_effect = false`, and
  `custody_side_effect = true` because it atomically resolves the exact custody
  journal before output.
- Client verification:
  `agent account economic-payment-sponsorship-proof-verify`, returning schema
  `tosctl.agent-account.agreement-payment-sponsorship-proof-verification.v1`,
  state `corroborated_terminal_verified`, with both side-effect flags false.

The client operation is query-only and receives the frozen proof,
PaymentRequest, sponsorship terminal profile, and client snapshot explicitly;
it receives no Provider custody or credential state. Only exact typed
categories
`not_found`, `not_mature`, and `temporarily_unavailable` map to unchanged
`unknown`. A nonzero process result, malformed envelope, unknown category,
profile/snapshot substitution, BOC conflict, or journal conflict is a hard
integrity error and MUST NOT be converted to `unknown`.

The Provider and client snapshot identities are distinct audit facts. Each
identity commits its local configuration bytes and credentials; the identities
MUST NOT be required to match or be exchanged. Both snapshots instead
reproduce the same signed release-profile descriptor and digest, including the
network and public-origin/locator-identity/operator-provenance set. The
Provider identity remains bound by its custody authorization and proof bundle;
the client identity remains local to the independent verification result.

Nested destination-credit references prove the top-up credit to the requester
source account. They are distinct from the enclosing
`destination_credit_references`, which prove the relayed client transaction's
own intended value effects in `sponsor_and_relay`; the two sets MUST NOT be
conflated or required to be equal. Relay checkpoint, confirmation,
profile, and observation fields are separately named with the `relay_` prefix
in the parent evidence body. They are verified against the relay profile and
are never inferred from, aliased to, or required to equal the nested
sponsorship fields, even when one proof bundle happens to cover both effects. An
`autonomous-decentralized` result requires `portable_proof_locator` and an
owner-pinned independent verifier. Lower assurance levels may retain the exact
proof bundle in an owner-local content-addressed store and may call the result
`corroborated_terminal` only when the independent client query validates the
prebound predicate. They MUST NOT call it finalized or use it as validator
finality.

Sponsorship uses a separate idempotent payment journal. It creates and stores
one exact Provider-signed top-up transaction before send. On an ambiguous
result it queries before replay and replays only those bytes.

The client also persists an owner-wide route substate before the first Submit.
`submit_started=false -> true` is the only local admission that permits the
first sponsorship request to cross the socket. After restart, a Provider 404,
`unknown`, missing database row, timeout, or unavailable endpoint is ambiguous
and MUST NOT authorize another sponsorship Submit. An authentic, exact
`prepared` Provider resolution may resume the same request because it proves
that the Provider has already admitted the stable identity and will enforce its
payment journal. `relay_exact` may instead retry the identical BOC because the
chain transaction identity itself is unchanged. A provider-scoped client API
without the owner route transition MUST reject first sponsorship dispatch.

In `sponsor_only`, terminal sponsorship evidence transitions the service
directly from `prepared` to `finalized_sponsorship_only` for
validator-authenticated evidence or to `corroborated_sponsorship_only` for the
prebound lower-assurance predicate. The client transaction is never broadcast.

The corresponding sponsorship-only terminal outcome also records either of
two partial `sponsor_and_relay` results:

- **pre-submit sponsorship-only:** the top-up met its selected terminal
  predicate, but a subsequent authorization, sequence, balance, policy, or
  remaining-window recheck failed before the first client-transaction write;
  no relay terminal-result fields or transaction-absence observations exist;
- **post-submit sponsorship-only:** the top-up met its selected terminal
  predicate, the exact client transaction crossed the write boundary, and the
  selected relay predicate later proved it absent, expired without inclusion,
  or irreversibly invalidated without inclusion; the evidence carries the
  complete transaction-only absence set and no relay-success references.

The Provider durably stores the sponsorship transfer reference and evidence
before either terminal transition and exposes them through the terminal
evidence endpoint. It MUST NOT report `rejected`, release the record as
side-effect-free, or erase a completed component merely because the other
component failed. Accounting treats sponsorship as fulfilled and relay as
unfulfilled, including the exact relay-negative reason when one exists. Any
later continuation is relay-only and is a new owner-authorized action; it is
not a sponsorship successor for this V1 stable action.

In `sponsor_and_relay` with
`sponsorship_release_evidence_class = validator_finality`, the relay remains
`prepared` until the Provider proves the exact top-up finalized as a
source-account credit under the selected sponsorship terminal profile. With a
signed `observed_unproven` release
descriptor, a lower-assurance service may move to nonterminal `submitted` or
`accepted` after verifying the exact observation and freshly rechecking
source balance, sequence, authority, expiry and remaining policy window. An
acknowledgement, Provider debit, mempool entry, transaction hash, or unverified
balance never satisfies either threshold. The initial observed path keeps
sponsorship exposure and the one-top-up ambiguity lock until the exact signed
terminal predicate or profile-qualified absence is proved. A later
`client_corroborated` top-up plus a validator-finalized client relay terminates
as `corroborated_success`; it MUST NOT be collapsed into
`finalized_success`. The same `corroborated_success` label applies when the
sponsorship is validator-finalized but the relay uses the pre-authorized
`provider_corroborated` class. Only validator-finalized evidence for every
requested component may use `finalized_success`.

The combined terminal matrix is exhaustive. A Provider MUST retain a
nonterminal component result until the other component reaches one of these
cells; arrival order does not change the result:

When sponsorship absence arrives first in `sponsor_and_relay`, its exact
`sponsorship_only` bundle is an immutable, durable nonterminal checkpoint; it
does not by itself create signed terminal evidence for the combined action.
If the relay later succeeds, that bundle is used unchanged by the relay-only
cell. If the relay later reaches a terminal-negative predicate, the Provider
creates one new `dual` bundle whose sponsorship references are byte-for-byte
identical to the checkpoint and whose only added material is the complete
transaction-absence set and its adapter payload. The journal advances this
checkpoint by expected revision, retains the superseded bundle digest for
audit, and rejects changed sponsorship references, a second promotion, or any
attempt to submit another top-up. This monotonic evidence aggregation is not a
sponsorship successor and grants no new economic authority. This also covers
the case where the remaining relay window closes before the client transaction
crosses its first-write boundary: the exact frozen transaction must reach its
selected expiry/invalidation absence predicate and be included in the dual
proof. The Provider must not discard the sponsorship checkpoint or relabel the
combined action as side-effect-free rejection.
The protected sponsorship recovery handle and frozen Provider snapshot remain
available to this query-only aggregation across a crash, but a separate durable
`sponsorship_attempt_consumed` fence is set before the original top-up write
and never clears. Holding the recovery material therefore permits only exact
resolution and proof reproduction; it cannot re-enter preparation, signing,
or submission. The protected handle is destroyed only after the combined
terminal record and evidence digest are durable.

| Sponsorship component | Relay component | Required combined evidence | Terminal outcome |
| --- | --- | --- | --- |
| success | success | sponsorship transaction evidence plus relay-success evidence | `*_success` |
| success | not started | sponsorship transaction evidence; no relay terminal fields | `*_sponsorship_only` |
| success | terminal negative after submit | sponsorship transaction evidence plus transaction-only absence observations | `*_sponsorship_only` |
| expired without inclusion | success | sponsorship-only absence observations plus relay-success evidence | `*_relay_only` |
| expired without inclusion | terminal negative | both typed absence sets | `*_expired`, `*_absent`, or `*_invalidated` according to the relay conclusion |

Here `*` is `finalized` only when every evidence class actually used by the
cell is `validator_finality`; otherwise it is `corroborated`. Corroborated
cells are forbidden for `autonomous-decentralized`. A top-up attempt consumes
the sole V1 sponsorship side-effect opportunity even when its terminal result
is absence and the relay succeeds: no terminal cell authorizes another
sponsorship Submit for the same stable action.

Accounting projects the two component obligations independently and
idempotently: `*_success` fulfills both; `*_sponsorship_only` fulfills only
sponsorship and records relay as not-started or terminal-negative;
`*_relay_only` fulfills only relay and records sponsorship as expired without
inclusion; a whole negative fulfills neither. The terminal evidence digest and
stable action identify one durable handoff, so restart or takeover cannot
double-credit either component.

The sponsorship payment Adapter's ordinary `finalized` or `corroborated`
label is not enough by itself. The Provider and client independently verify
that the exact credit evidence meets this relay quote's complete signed
`sponsorship_terminal_profile`, including checkpoint, observer,
operator-domain, confirmation/maturity, and reorg-window requirements.
It also verifies the payment sink's pinned full `NetworkDomainV1` -- network
ID, global ID, both zero-state hashes, and workchain -- against the quote. A
payment request carrying only a display network ID cannot authorize the
Provider to select the remaining network coordinates. Weaker or
network-mismatched evidence leaves the relay `prepared` and never authorizes a
broadcast.

The admission inspector may project only the exact native-asset sponsorship
already bound by the request, quote, and Agreement when deciding whether the
future transaction can have sufficient balance. This projection is not chain
state and never authorizes broadcast. After the top-up meets the selected
release threshold, the Provider MUST resolve the source account again and
recheck its authority, controller
epoch, sequence, expiry, limits, and actual balance under the selected release
evidence with zero projected credit. It then repeats the action-to-transaction binding immediately
before the first write. A wrong-asset credit, promised-but-unobserved credit,
or double-counted credit fails closed.

Relay-only failover may send the same exact bytes through another Provider
after querying first. An ambiguous or unavailable prior Provider does not
assert absence, but it also cannot make byte-identical TOS transaction bytes
execute twice: source account and sequence remain inside the signed transaction
and the stable semantic action is unchanged. The current writer may therefore
negotiate a new route-specific Agreement, subject to Portfolio cumulative-fee
and attempt limits, and request the next admission receipt under the route-head
rule in §9.2. The old receipt may still drain; both Providers can only submit
the BOC committed by the same `transaction_identity_digest`. Provider service
fees remain distinct, explicitly accepted Agreement obligations and are never
inferred from the underlying payment. A route change that alters the BOC,
network, source sequence, stable action, exact request, or broadcast-only stage
is not failover and conflicts.

V1 does not admit an automatic sponsorship route successor. After the first
sponsorship admission, every ambiguous, finalized, expired or absent result is
resolved and accounted on that route; it never grants implicit permission for
a second Provider-funded top-up. Point-in-time `absent`, a missing Provider
record, an unobserved mempool entry, or absence at a checkpoint before signed
expiry is never sufficient even for a future profile. A successful earlier
credit may permit an explicitly negotiated relay-only continuation; it never
permits duplicate sponsorship or hidden duplicate fees. Any prior evidence
containing a sponsorship transfer reference forbids a new `sponsor_only` or
`sponsor_and_relay` attempt for that underlying action, even if the client-
transaction outcome is expired, absent, or invalidated.

A future profile may define a newly owner-authorized quote and Agreement after
portable `expired_without_inclusion` evidence, but only after it freezes the
exact predecessor-evidence digest and transition in Action Authority
admission. This V1 deliberately provides no implicit successor semantics.

Once an exact terminal non-execution proof has been durably stored and remains
independently verifiable under every applicable selected terminal profile, any
later owner-authorized transition defined by a future profile MUST NOT require
another
response from the prior Provider or its database. The client
revalidates the stored route, evidence signature, historical Agent-key
authority, checkpoints, and chain facts locally. Requiring the failed Provider
to refresh an already terminal result would make that Provider an implicit
online relay head and would violate Provider-loss recovery.

Before returning any terminal service result to accounting, the client
atomically stores the complete signed resolution and signed terminal-evidence object
on the current durable route hop. A restart first loads that exact pair,
validates its content digests and binding to the frozen execution, resolves the
Provider key through the anchored signing-authority epoch, and independently rechecks
the referenced chain evidence. Only then may it reconstruct the terminal
result or use a qualifying non-execution result for failover. This recovery
does not query the prior Provider and remains valid after its endpoint and
status database disappear. A future sponsorship failover hop can be admitted
only from exact terminal evidence already stored on its predecessor; caller-
supplied evidence cannot replace it. The portable proof supports recovery and
a future explicitly versioned transition; it does not enable a sponsorship
successor in this V1. Relay-only
failover instead uses the byte-identical route-head transition in §9.2 and does
not manufacture an absence claim.

## 14. Signed resolution and terminal evidence

`SignedRelayResolutionV1.body` binds Provider, the full network domain,
selected assurance level, underlying stable ID and exact request, execution
digest, state, monotonic revision, optional terminal
outcome, transaction reference, the exact sponsorship stable action ID, exact
sponsorship request digest, signed sponsorship expiry and transfer reference,
terminal evidence-set digest, observation time, and response expiry. The three
sponsorship identity/expiry fields are all present or all absent; a sponsorship
transfer reference requires them. Nonterminal states omit terminal outcome and
evidence-set digest. A terminal state requires one of:

```text
finalized_success
corroborated_success
finalized_expired
finalized_absent
finalized_invalidated
corroborated_expired
corroborated_absent
corroborated_invalidated
finalized_sponsorship_only
corroborated_sponsorship_only
finalized_relay_only
corroborated_relay_only
```

`finalized_success` means every requested component succeeded under
`validator_finality`. `corroborated_success` means every requested component
succeeded, but at least one selected component used its exact lower-assurance
class: relay `provider_corroborated` and/or sponsorship
`client_corroborated`. It is component-qualified success, not a claim that the
combined action has validator-authenticated finality, and it is forbidden for
`autonomous-decentralized`.

`finalized_sponsorship_only` and `corroborated_sponsorship_only` are used for
a completed `sponsor_only` request and for either partial
`sponsor_and_relay` sponsorship-only cell. The pre-submit form carries no
relay terminal evidence. The post-submit form carries a complete
transaction-only absence set but no relay-success references. The outcome is
`finalized_sponsorship_only` only when the nested sponsorship evidence and,
when present, every transaction-absence reference use `validator_finality`;
otherwise it is `corroborated_sponsorship_only`. Such a resolution's
`transaction_reference` is the exact `sponsorship_transfer_reference`, not an
absent client-transaction hash.

`finalized_relay_only` and `corroborated_relay_only` are partial
`sponsor_and_relay` results in which the exact client transaction succeeded
but the sponsorship action expired without inclusion. They require complete
relay-success evidence plus the sponsorship-only absence set, and forbid the
transaction-absence set and positive sponsorship transaction evidence. The
outcome is `finalized_relay_only` only when both the relay-success evidence
and every sponsorship-absence reference use `validator_finality`; otherwise
it is `corroborated_relay_only`. Their `transaction_reference` is the exact
submitted client-transaction hash.

The negative label is `finalized_*` only when every selected predicate used by
that negative proof is `validator_finality`. If any required predicate is
`provider_corroborated` or `client_corroborated`, the corresponding label is
`corroborated_expired`, `corroborated_absent`, or
`corroborated_invalidated`. Corroborated negatives are forbidden for
`autonomous-decentralized`. Negative resolutions omit
`transaction_reference`; full and relay-only relay-success resolutions bind
it to the exact submitted client-transaction hash.

The Provider-private sponsorship resolver uses the exact statuses `unknown`,
`observed_unproven`, `corroborated_terminal`, `corroborated_absent`,
`finalized`, and `finalized_absent`. Only the latter four are terminal under
their selected predicates. `observed_unproven` remains nonterminal and cannot
be translated to any terminal outcome.

The evidence-set digest is the released underlying exact-request digest over
strictly sorted evidence digest strings, each followed by one NUL byte.

`SignedRelayFinalityEvidenceV1.body` binds the Provider, full network domain,
selected assurance level, underlying action/request, execution digest,
signed-byte digest and cell hash, the exact signed QuoteRequest
`transaction_valid_until_unix`, source account and sequence, outcome,
observation time, and `signing_authority_at_unix`. The validity value is present
in every mode, is covered by the evidence digest and Provider signature, and
MUST equal the QuoteRequest value exactly. It also carries the complete profiles
selected by the service mode:

```text
relay_finality_profile?                 # relay_exact | sponsor_and_relay
sponsorship_terminal_profile?           # sponsor_only | sponsor_and_relay
transaction_valid_until_unix            # every mode; exact QuoteRequest value

relay_terminal_evidence_class?          # only when a relay terminal result exists
relay_validator_authenticated_portable_proof?
relay_finalized_checkpoint_id?
relay_finalized_checkpoint_sequence?
relay_finalized_checkpoint_unix?
relay_confirmation_depth?
relay_observation_digests[]?

sponsorship_stable_action_id?
sponsorship_exact_request_digest?
sponsorship_valid_until_unix?
sponsorship_transfer_reference?
sponsorship_transaction_evidence?
sponsorship_absence_observations[]?
transaction_absence_observations[]?

submitted_transaction_hash?             # relay success only
source_execution_reference?             # relay success only
destination_credit_references[]?        # relay success, as required by profile
```

The profile presence matrix follows the selected mode even when the terminal
result is partial: every combined result carries both selected profiles. A
pre-submit sponsorship-only result carries no relay terminal-result fields. A
post-submit sponsorship-only result carries the complete transaction-only
absence set, but no relay terminal-result fields and no relay-success
references. A relay-only result carries the complete sponsorship-only absence
set plus relay terminal-result fields and relay-success references, but no
transaction-absence set or positive sponsorship transaction evidence. A whole
negative carries both absence sets and no positive component evidence. A relay
terminal result is complete only when all seven
`relay_` class/authentication/checkpoint/depth/observation fields above are
present. Its class is `validator_finality` exactly when the authentication
boolean is true; `provider_corroborated` requires false and the exact lower
relay profile. The nested sponsorship evidence makes the corresponding
`validator_finality`/true or `client_corroborated`/false assertion against the
separate sponsorship terminal profile. A selected profile, class, or boolean
cannot be inferred from the other component.

Terminal evidence is durable beyond the short response lifetime of
`SignedRelayResolutionV1`. `observed_at_unix` is chain-evidence time;
`signing_authority_at_unix` selects the Provider key-authorization epoch. The
two are deliberately distinct so evidence first materialized after an honest
key rotation is not checked against the wrong historical key.

A signer-provided time is not a trusted timestamp. Any claim of portable
validator-authenticated terminal evidence therefore additionally requires the
exact signed-evidence digest and signing
authority epoch to be atomically committed with terminal state in a
rollback-resistant monotonic journal, authority log, or chain anchor. The
client verifies that commitment as well as historical Agent authority. Without
that anchor, a later-compromised revoked key could backdate newly forged
wrappers; such a source MUST report its portable terminal-commitment
capability as false. Historical evidence reads validate the immutable stored
checkpoint binding and MUST NOT compare it with or advance the moving global
checkpoint high-water.

A successful relay requires a submitted transaction reference and source
execution reference. A transaction profile additionally requires every exact
destination credit necessary to prove its intended value effect. A relay
negative carries its typed transaction-absence references and no success
references. Sponsorship-positive evidence requires the exact sponsorship
identity, signed sponsorship expiry, transfer reference, and nested transaction
evidence. It may coexist only with no relay evidence (pre-submit) or with the
transaction-only absence set (post-submit); it never coexists with the
sponsorship-absence set. Sponsorship-absence evidence may coexist only with no
relay success in `sponsor_only`, with relay-success evidence in a combined
relay-only result, or with the transaction-absence set in a whole combined
negative. No terminal outcome may omit the evidence for either component it
claims to resolve.

For `relay_exact`, sponsorship identity, transfer, nested transaction evidence,
and sponsorship-absence sets are all forbidden. For either sponsorship mode,
terminal evidence MUST contain either the exact nested sponsorship transaction
evidence or the complete sponsorship-absence set. A combined result that
resolves the relay negatively additionally carries the transaction-absence
set. A Provider cannot delete the paid sponsorship obligation and sign an
ordinary relay-only `finalized_success` wrapper.

### 14.1 Typed terminal-absence references

`RelayAbsenceObservationReferenceV1` contains exactly:

```text
schema_version = 1
observation_kind               # sponsorship_action | client_transaction
conclusion                     # absent | expired_without_inclusion |
                               # invalidated_without_inclusion
provider_agent_id
network_digest
relay_stable_action_id, relay_exact_request_digest
relay_execution_request_digest
sponsorship_stable_action_id, sponsorship_exact_request_digest
sponsorship_valid_until_unix
signed_transaction_digest, signed_transaction_cell_hash
terminal_profile_uri, terminal_profile_digest
terminal_evidence_class
finalized_checkpoint_id, finalized_checkpoint_sequence
finalized_checkpoint_unix
observer_id, operator_domain_id
observation_evidence_profile_uri
observation_evidence_profile_digest
observation_digest
observed_at_unix
```

Every present absence set is also carried in one
`RelayAbsenceProofBundleV1`:

```text
schema_version = 1
proof_scope                    # sponsorship_only | transaction_only | dual
proof_profile_uri
proof_profile_digest
proof_payload_digest
proof_payload                  # exact Core Deterministic CBOR adapter bytes
sponsorship_absence_observations[]?
transaction_absence_observations[]?
```

The wrapper's digest domain is
`tos.agent-relay-absence-proof-bundle.v1`. The payload digest domain is
`tos.agent-relay-absence-proof-payload.v1`. The finality-evidence body carries
both `absence_proof_bundle_digest` and the exact in-band Core Deterministic
CBOR bundle bytes; both fields are mandatory whenever either absence array is
present and forbidden otherwise. The decoded wrapper, including its payload,
is at most 128 KiB. `proof_scope` and the wrapper arrays MUST exactly match the
arrays in the signed finality-evidence body. The adapter payload is itself one
bounded Core Deterministic CBOR object and its digest MUST match the exact
payload bytes. Large validator proofs may remain content-addressed locators
inside that payload, but all raw transaction/source/sequence/query material
needed for an independent adapter re-query is in-band.

The wrapper proof-profile URI and digest are not Provider-selected metadata.
For each signed component terminal-profile digest, the owner configuration
deterministically registers one enabled absence verifier profile before the
Agreement is authorized. The wrapper pair MUST equal that registry entry, and
every nested observation-evidence profile MUST be accepted by the same entry.
An unknown profile, a profile selected after Agreement authorization, mixed
nested profiles, or any URI/digest substitution fails closed.

The stock TOS RPC absence-verifier profile
`tos.relay-absence.tosctl-rpc-snapshot.v1` is lower-assurance only. It is
distinct from the sponsorship release-observation profile
`agreement-payment-rpc-corroboration.v1`: the former authorizes an independent
bounded-snapshot absence query, while the latter describes a positive or
nonterminal sponsorship-credit observation. Reusing either URI/digest in the
other role is profile substitution and fails closed. The absence profile
descriptor is canonical CBOR with digest domain
`tos.agent-relay-absence-proof-profile.v1` and fields
`schema_version = 1`, the exact `profile_uri`,
`independent_snapshot_query = true`, `maximum_bundle_bytes = 131072`, and
`chain_side_effect = false`. Its
sponsorship references use `client_corroborated`, its transaction references
use `provider_corroborated`, and it is forbidden for validator-finality or
`autonomous-decentralized` evidence. V1 releases no portable validator
sponsorship-absence profile, so stock autonomous sponsorship capability remains
`not_ready`; this does not affect autonomous `relay_exact` capability.
For this stock entry, each nested `observation_evidence_profile_uri` is exactly
`agreement-payment-rpc-corroboration.v1` and its digest identifies the frozen
RPC snapshot descriptor actually re-queried. Thus the outer profile selects
the absence-verification algorithm while the nested profile identifies its
input evidence source; their URI/digest pairs are intentionally unequal.

`RelayAbsenceObservationReferenceV1` uses digest domain
`tos.agent-relay-absence-observation-reference.v1`. The wrapper has no
standalone relay signature or separate HTTP media type: it is embedded in the
Provider-signed finality-evidence body. `observation_digest` addresses the
separately authenticated proof selected by
`observation_evidence_profile_uri` and digest. Implementations MUST retrieve
and verify that proof, its observer authority, and its operator provenance;
the wrapper or Provider signature cannot make arbitrary proof bytes true.

Each absence set separately meets its selected observer and operator-domain
thresholds. Every entry binds both exact side-effect identities so it cannot
be reused for another relay. The sponsorship set has
`observation_kind = sponsorship_action`, binds the selected sponsorship
terminal profile URI, digest, and class, and MUST conclude
`expired_without_inclusion`; `absent` is intentionally insufficient. The
client-transaction set has `observation_kind = client_transaction`, binds the
selected relay profile, and concludes `absent`,
`expired_without_inclusion`, or `invalidated_without_inclusion`.

Set presence is component-qualified:

- a `sponsor_only` negative and a combined relay-only result carry only the
  sponsorship set;
- a post-submit combined sponsorship-only result carries only the
  client-transaction set;
- a whole combined negative carries both sets;
- a pre-submit sponsorship-only result carries neither set.

No transaction-absence set exists in `sponsor_only`, because no client
transaction is selected or broadcast. No result may add an absence set for a
component whose positive evidence is present.

Within each set, every wrapper uses one identical checkpoint ID, sequence, and
time; wrapper digests are strictly sorted; observer IDs and proof digests are
unique; and operator diversity meets that set's bound profile. The sponsorship
checkpoint time MUST be at or after `sponsorship_valid_until_unix` plus the
selected sponsorship terminal profile's `reorg_window_seconds`. The two sets
MAY use different checkpoints because they apply different selected component
profiles, but they cannot reuse one underlying `observation_digest`. For
`absent` or `expired_without_inclusion`, the client-transaction checkpoint time
MUST also be at or after the evidence body's exact
`transaction_valid_until_unix` plus the selected relay terminal profile's
`reorg_window_seconds`. An
`invalidated_without_inclusion` conclusion instead proves the profile-defined
irreversible invalidation condition and does not wait for the transaction
expiry. Addition overflow fails closed. The enclosing evidence-set digest is
computed over the strictly sorted absence-wrapper digests from every present
array—not the underlying proof digests—and the merged set has at most 64
entries. There
is no generic top-level `observation_digests[]` field for the absence path. Any
missing required set, forbidden extra set, mixed kind, changed action ID,
changed validity, changed profile or class, within-set checkpoint disagreement,
applicable pre-terminal-window checkpoint, or relabelled proof fails closed.

A terminal outcome uses the `finalized_` prefix only when every positive and
negative evidence class used by that exact matrix cell is
`validator_finality`. If any used component is `provider_corroborated` or
`client_corroborated`, the matching result is `corroborated_*`; such evidence
is lower-assurance and cannot satisfy an `autonomous-decentralized` claim. The
historical field name
`finalized_checkpoint_*` inside an absence wrapper identifies the bounded
checkpoint inspected. It does not by itself assert validator finality.

`minimum_observers` observations must agree, cover at least
`minimum_operator_domains` independently operated domains, meet confirmation
depth, remain inside the reorg policy, and advance a process-independent
monotonic checkpoint fence. Operator provenance is resolved alongside each
content-addressed observation; a list of Provider-created digests cannot prove
independence.

The Provider-produced sponsorship-only component absence atomically commits
its exact bundle digest to the terminal sponsorship custody tombstone before
returning evidence; that operation has `custody_side_effect = true` and is the
permanent no-successor fence for the top-up action. A later dual aggregation
must resolve that exact tombstone and reproduce its sponsorship references; it
must not replace the tombstone or perform another custody mutation. The dual
bundle is committed with the combined terminal transition in the relay journal
before it is returned. Consequently dual aggregation, transaction-only absence
production, and every independent client verification are query-only and have
both side-effect flags false. A nonterminal result, malformed bundle, profile
disagreement, changed component checkpoint, or query disagreement makes no
new custody or terminal-journal mutation.

Provider signatures authenticate reports but are not finality. Clients
independently retrieve and verify the chain proof and corroboration. One node,
one Provider, an HTTP acknowledgement, a transaction hash, or a source debit
without the exact required credit never establishes terminal success.

## 15. Endpoints, SSRF, and bounds

All four public service URLs and quote status endpoints are HTTPS origin paths
without user information, query, or fragment. Loopback HTTP is allowed only by
a separately enabled local-development profile and never because a remote
Intent or quote asks for it.

For every DNS resolution, connection, redirect, and retry, implementations
reject loopback, private, link-local, multicast, unspecified, carrier-grade
NAT, metadata-service, Unix-socket, alternate IP spelling, and other
owner-forbidden targets. DNS/IP classification repeats after resolution to
prevent rebinding. TLS binds hostname, SNI, certificate policy, and connected
address. Redirects and ambient proxies are disabled by default; credentials
are never copied from an Intent, URL, model output, environment, or other
origin.

Headers, compressed/decoded response bytes, connections, DNS answers,
concurrency, retries, parser time, and total wall time are bounded before
content verification. Every complete canonical object and HTTP request or
response, including status/evidence retrieval, is capped at 1 MiB. The
embedded underlying action request is capped at 192 KiB raw and the exact signed
transaction at 65,536 bytes, leaving deterministic envelope headroom.

## 16. Rate, exposure, fee, and privacy policy

Providers enforce per requester, source, network, recipient, transaction
profile, and aggregate controls for request/refusal rate, concurrent
prepared/submitted work, fee, sponsor, client-transaction gas, transaction
value, Provider balance/reserve, validity window, stable-ID replay,
destination, amount, and payload. Active quote/work-slot admission and
Provider-funded exposure reservation are durable and atomic. A service fee is
a receivable, not Provider spend; the relayed transaction value and its gas
are debited by the signed source transaction, not by the HTTP relayer.

Atomic amounts are canonical unsigned decimal strings up to 78 digits. All
addition and comparison uses arbitrary or at least 256-bit checked arithmetic.
Admission and exposure reservation are atomic. A post-quote gas-price change
cannot increase the signed client charge or mutate bytes; the Provider rejects
before a side effect or absorbs the difference according to the Agreement.

`maximum_network_fee_atomic` is an admission ceiling for the
profile-specific, independently computed balance reserve required by the
client-signed transaction. It is not represented by a chain-enforced gas-cap
field in the V1 Agent Account native-send BOC and MUST NOT be presented as one.
It neither authorizes a separate charge to the requester nor proves the fee
ultimately consumed by the chain. The signed source account pays that
transaction fee. In a sponsorship mode, the Provider chooses whether the exact
requested top-up can cover the source's currently verified balance shortfall, including
this conservative reserve; it never silently increases the sponsorship or
rewrites the client transaction. The Provider also prices and reserves the gas
for its own separate top-up transaction under its local custody policy.

Ordinary logs MUST NOT contain private keys, raw signed transactions, complete
BOCs, Agreement attachments, authorization evidence, source/destination
addresses, or amounts. Operational logs use bounded digests and typed error
classes. Access-controlled ambiguity journals retain exact bytes only for the
agreed recovery, accounting, and retention interval.

## 17. Conformance and scoped assurance claims

The frozen vectors are
[`agent-relay-service-v1.json`](../test-vectors/agent-relay-service-v1.json),
and the independent standard-library verifier is
[`agent-relay-service-reference.py`](../scripts/agent-relay-service-reference.py).

Implementations pass positive cross-language reproduction and negative tests
for:

- canonical CBOR, all digest/signature domains, wrong keys, noncanonical bytes,
  unknown fields, ordering, duplicates, and size limits;
- unsupported assurance levels, request/quote/Agreement/admission/resolution
  downgrade attempts, assurance changes across route successors, and all
  service-mode/assurance-level readiness combinations;
- network/global ID/zero-state/workchain, requester, Provider, source, profile,
  sequence, QuoteRequest/evidence validity substitution, intent, cell-hash,
  recipient, value, and payload changes;
- missing/duplicate/reordered fee lines, fee overflow, sponsorship mismatch,
  gas/value increase, balance, rate, concurrency, and aggregate exposure;
- unsatisfiable request/quote/Agreement/action/fence/transaction windows;
- exact retry, ID/request conflict, changed signed bytes, changed execution
  digest, changed transaction identity, changed route or stage mask, and
  receipt recovery after takeover;
- stale-writer receipt refusal, receipt signature/authority/principal/sequence/
  start-window mutation, byte-identical ResolveAdmission recovery, forked or
  skipped route-attempt refusal, a 32-attempt cap, single receipt consumption,
  and one-shot sponsorship/broadcast stage bits;
- crash after prepare, crash after submitted-before-send, ambiguous send,
  query-before-retry, and byte-identical rebroadcast;
- sponsorship release before combined relay, crash after top-up send,
  old-transfer replay against a new Agreement, SPN1 mutation, and
  duplicate-top-up prevention;
- stale writer, concurrent admission, quote reuse, Provider restart/loss,
  byte-identical relay-only successor admission through a second Provider, and
  refusal of every automatic V1 sponsorship successor, including after
  profile-qualified terminal absence; a future profile must separately bind
  the predecessor evidence and define its own transition;
- source-output without destination-account inclusion, wrong inbound message,
  missing/wrong credit phase, bounce, non-credit-first credit, and truthful
  destination compute-abort recording;
- quorum disagreement, insufficient operator diversity, checkpoint rollback,
  reorg, accepted-to-submitted recovery, bounded typed sponsorship-only,
  transaction-only, and dual absence proof bundles; exact Core Deterministic
  bytes, wrapper/payload digest, scope, array, size, proof-profile registry,
  and nested-profile substitutions;
- all four combined component cells, including relay success plus sponsorship
  absence and sponsorship success plus post-submit relay absence; finalized/
  corroborated prefix derivation from every evidence class actually used,
  exact outcome-qualified resolution reference, component-qualified
  accounting, and no V1 sponsorship successor after any top-up attempt;
- per-component checkpoint independence, sponsorship and client-transaction
  pre-expiry-plus-reorg rejection, point-in-time-absence rejection, cross-kind
  proof-reuse rejection, relay-only validator/corroborated negative outcomes,
  and refusal to terminalize an acknowledgement, single initial observation,
  or negative result with no terminal evidence;
- pre-authorization terminal-profile substitution, replay of an old
  observed-only Agreement into `client_corroborated`, mixed-profile evidence,
  false `finalized_success`, stripped sponsorship evidence, missing frozen
  client snapshots, configuration rotation, component-qualified
  `corroborated_success`, and validator- and client-corroborated
  sponsorship-only outcomes; and
- SSRF literals, DNS rebinding, redirects, proxy/TLS/SNI failures,
  decompression, oversized responses, retry amplification, and log redaction.

Only an `autonomous-decentralized` runtime claim requires two independently
operated Providers. Current configuration and authenticated provenance are the
readiness authority. A shared market database, journal, global head, privileged
Gateway, common operator, common failure domain, shared authority/store, or two
Sybil Agent identities does not satisfy independence. The owner-pinned
provenance used for this decision is included in the crash-recoverable route
record and is not inferred from Provider names.

An interoperability or resilience report SHOULD additionally exercise bounded
refusal handling, failover and ambiguous recovery, remove either Provider and
its database, and reconstruct the result from the surviving Provider plus
independently verified chain evidence. Such a campaign measures implementation
quality; it MUST NOT be treated as a protocol authorization bit or as a
prerequisite for enabling a presently capable and configured runtime.

An evidence source claiming portable validator-authenticated terminal evidence
additionally MUST:

- expose the frozen proof bytes or content-addressed locator used by every
  observation digest and a concrete independent client verifier;
- maintain its finalized checkpoint high-water in rollback-resistant monotonic
  CAS storage shared with custody or Action Authority, rather than only an
  owner-private file that can be restored from an old snapshot;
- atomically anchor the exact signed finality-evidence digest and
  `signing_authority_at_unix` with terminal action state in rollback-resistant
  authority storage, and expose a verifier for that anchor;
- reject stale or future consensus observations at every account,
  authorization, expiry, balance, and finality read using the operation's
  current clock, not only at process readiness;
- complete a crash-safe accounting handoff before compacting client route
  records, retain permanent stable-action conflict tombstones plus
  content-addressed terminal proof locators, and demonstrate that bounded
  storage cannot permanently stop new work after a fixed number of terminals;
- declare and test every terminal outcome reachable for every advertised mode;
  and
- for sponsorship modes, satisfy §13.1's exact top-up transaction profile.

The current TOS RPC corroboration adapters provide owner-local evidence;
its observation and checkpoint files are not portable
validator-authenticated proofs and are rollbackable with the host filesystem.
An owner may explicitly select it for a scoped `trusted-local` or
`authorized-single-provider` capability, and
an implementation may use its first observation for nonterminal
`submitted`/`accepted`. Its independent client-owned re-query may terminalize
the exact lower-assurance obligation as `corroborated_terminal` when the
prebound client-corroborated profile is satisfied. It MUST NOT label either
result portable or validator finality or use it to satisfy an
`autonomous-decentralized` claim. The relay-side RPC source is likewise limited
to `provider_corroborated` under the exact
`tos.relay.provider-corroborated-terminal.v1` profile and reports
`relay_validator_authenticated_portable_proof = false`. A full requested
success with either lower component emits `corroborated_success`; a completed
sponsorship with no relay terminal result emits
`corroborated_sponsorship_only`. The source cannot merely sign an opaque digest
wrapper or convert either result into `finalized_*`.

## 18. Explicit non-goals

This profile does not make sponsorship mandatory, expose a client private key,
authorize Provider transaction mutation, add account abstraction or a chain
opcode, make discovery/ranking/status canonical, replace generic Agreement or
economic-action authority, make a Provider signature sufficient finality, or
make `relay_accepted` mean finalized execution. It is one optional service
composed from released generic Agent operations.
