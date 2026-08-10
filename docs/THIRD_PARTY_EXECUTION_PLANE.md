# ATOS Third-Party Execution Plane Placement

**Status:** Planned cross-repository specification
**Applies to:** routing HTTP/MCP/A2A provider execution and readiness probing behind the execution/data plane, instead of from the ATOS Gateway's Job/economic business logic
**Roadmap phase:** Phase 3A §7.1.1 (3A-A placement rule) and its cross-repository follow-on work

> `docs/ARCHITECTURE_V0.2.md` §18 already places "model/MCP/HTTP/GPU/local/human
> adapters" in the Execution / Data Plane (`tos-ai` + providers), not the
> Gateway/Control Plane. This document does not change that placement -- it
> defines the concrete wire contract and trust boundary that were missing to
> actually implement it, discovered while auditing an ATOS-side implementation
> that (correctly per the roadmap's own honest-gap-reporting rule) built the
> HTTP/MCP/A2A adapters inside the `atos` Gateway process as an interim step
> and flagged the placement violation rather than silently claiming compliance.

---

## 1. Problem

Phase 3A's Capability model lets a third-party provider register a Capability
bound to an arbitrary transport endpoint it controls (`http`/`mcp`/`a2a`
`CapabilityBinding.endpoint_ref`). Executing or health/certification-probing
that Capability means dialing that provider-chosen endpoint.

§7.1.1's placement rule says the ATOS Gateway's Job/economic service must not
perform this dialing itself; it belongs behind the existing execution/data
plane boundary (`tos-protocol` `ExecutionGatewayService` / `tos-ai`).

That boundary exists today, but only for a different, narrower shape of
execution than "dial an arbitrary provider-chosen URL":

- `tos-protocol`'s `atos.tos.v1.ExecutionGatewayService.SubmitJobRequest` has
  no field describing a transport binding or endpoint at all -- it identifies
  a `provider_id`/`capability_id`/`capability_version` and lets the private
  Worker resolve execution from that alone.
- `tos-protocol` → `tos-ai`'s private `tos.edge.v1.WorkerService.InvokeRequest`
  is `service_id` + `operation` + `model` + opaque `payload` -- again no
  endpoint field, and `model` is a required, non-empty selector.
- `tos-ai`'s existing adapter plugin surface (`pkg/runtime.Adapter`, concretely
  implemented by `pkg/adapters/{ollama,openai,mock}`) is deliberately shaped
  for **operator-fixed** model-serving endpoints. `pkg/adapters/openai`'s
  package doc states this as a design invariant, not an oversight: *"Task
  payloads cannot select the endpoint."* `runtime.ValidateCapability` further
  hard-requires a SHA-256 `ModelDigest`, which has no meaning for a
  general-purpose third-party HTTP/MCP/A2A capability.

So closing §7.1.1 is not "route an existing generic call through an existing
generic boundary." It requires reconciling two different trust models:

```text
ATOS Capability model:    endpoint_ref is provider-chosen, per-Capability,
                           effectively business data.

tos-ai adapter model:     endpoint is operator-fixed, chosen once at worker
                           configuration time, never selected by a request.
```

Naively threading a caller/business-supplied `endpoint_ref` into `tos-ai`'s
existing worker process would silently invert that second invariant --
letting Gateway-side data pick a `tos-ai` operator's outbound destination.
That is a real regression in `tos-ai`'s own security posture, not a detail to
paper over while satisfying the letter of §7.1.1's placement rule.

## 2. Resolution: an endpoint allowlist is the trust boundary, not the payload

A `tos-ai` operator remains the sole authority over which third-party
endpoints their worker is permitted to reach. The mechanism is a
**worker-local, operator-curated allowlist**, analogous in spirit to
`pkg/adapters/openai.Config.BaseURL` -- config the operator controls, never
data the invocation controls:

```text
operator config:  a list of (transport, endpoint_ref, capability_id) entries
                   this worker is permitted to dial, provisioned by the
                   operator out of band (static config file at this version --
                   see §5 for why a dynamic sync protocol is explicitly
                   deferred).

per-invocation:    an inbound ThirdPartyExecutionService.Invoke names a
                   transport + endpoint_ref + capability_id/version. The
                   worker looks it up in its own allowlist. A match that is
                   not byte-identical to an allowlisted entry (transport,
                   endpoint_ref, capability_id all match; capability_version
                   MAY differ -- see §4) is rejected before any outbound dial,
                   the same way an unresolved `provideradapter.Resolver`
                   lookup fails closed in the interim ATOS-side implementation.
```

This preserves the existing `tos-ai` invariant exactly: the invocation still
never *picks* an outbound destination, it can only *reference* one the
operator already agreed to. A compromised or buggy ATOS Gateway process can
at most ask a `tos-ai` worker to do something its own operator pre-approved,
never redirect it somewhere new.

## 3. Wire contract additions

### 3.1 `atos` ↔ `tos-protocol` (public, normative -- this repository)

`atos.tos.v1.execution.proto` gains an optional message, attached to the
three RPCs that need to describe or probe a third-party binding:

```protobuf
message ThirdPartyBinding {
  EndpointAdapterType transport = 1;   // HTTP | MCP | A2A
  string endpoint_ref = 2;             // opaque identifier/config reference,
                                        // never a bearer credential -- same
                                        // rule as CapabilityBinding.endpoint_ref
  Digest binding_commitment = 3;       // commitment to the frozen
                                        // CapabilityBinding this Job's Quote
                                        // resolved, so tos-protocol/tos-ai can
                                        // detect a mismatched replay without
                                        // re-deriving ATOS's own binding-freeze
                                        // logic
}

enum EndpointAdapterType {
  ENDPOINT_ADAPTER_TYPE_UNSPECIFIED = 0;
  ENDPOINT_ADAPTER_TYPE_HTTP = 1;
  ENDPOINT_ADAPTER_TYPE_MCP = 2;
  ENDPOINT_ADAPTER_TYPE_A2A = 3;
}
```

Added as field 20 (`ThirdPartyBinding third_party_binding = 20;`, unset for an
ordinary tos-native/model Job) to `SubmitJobRequest`, `QuoteExecutionRequest`
and `GetProviderStatusRequest`. This is purely additive -- existing native-Job
callers and implementations are unaffected, matching this repository's
existing precedent of adding new optional surface rather than mutating a
message a v0.1/v0.2 implementation already depends on (see
`WorkerStreamService`'s own doc comment on preserving the frozen unary
`WorkerService` interface).

`GetProviderStatusResponse`'s existing `ProviderReadiness` enum is reused
unchanged for third-party health/certification results -- there is no new
readiness vocabulary, only a new way to ask the question.

### 3.2 `tos-protocol` ↔ `tos-ai` (private, `tos-protocol`'s own implementation concern)

`tos.edge.v1.worker.proto`'s doc comment already establishes that this is
*"the private, versioned boundary between Edge Core and a vertical worker...
not direct Internet exposure"* -- an implementation detail of `tos-protocol`,
not something this repository normatively pins field-by-field, the same way
it does not pin `WorkerService`'s existing message shapes today.

What this repository DOES require normatively, because it is a
cross-repository security invariant rather than a wire-format detail: any
private extension `tos-protocol` adds for third-party execution (a new
sibling service alongside `WorkerService`/`WorkerStreamService` is the
natural shape, consistent with how streaming was added as
`WorkerStreamService` rather than a `WorkerService` mutation) MUST enforce the
operator-allowlist model from §2 on the worker side, and MUST NOT let an
inbound request's `endpoint_ref` be dialed unless it matches a
worker-operator-curated entry. A `tos-protocol`/`tos-ai` implementation that
satisfies §7.1.1 without this property does not actually satisfy it --
routing through the execution/data plane is meaningless if that plane simply
forwards Gateway-chosen URLs unchecked.

## 4. Binding-freeze interaction

Phase 3A's `atos`-side binding freeze (§7.1.0 3A-S: a Job's `CapabilityBinding`
is resolved once at Job creation and never re-resolved from a live
Capability) is unaffected and remains the sole source of truth for *which*
binding a Job uses. `ThirdPartyBinding.binding_commitment` lets
`tos-protocol`/`tos-ai` detect a replay whose semantic binding changed (an
`idempotency_conflict`, per §3.3's universal rule) without needing to
re-implement `domain.SelectBinding` on that side; it is a consistency check,
not a second source of truth. `capability_version` MAY differ between the
Job's frozen commitment and the worker's currently-allowlisted entry for the
same `endpoint_ref` -- version currency is a certification/health-freshness
question (§7.1.3), not this boundary's concern.

## 5. Explicitly deferred: dynamic allowlist sync

A future phase MAY let a `tos-ai` operator subscribe to allowlist updates
(e.g. synced from `atos`'s provider directory) instead of maintaining static
config. That sync protocol is intentionally **not** specified here: it is not
required to close §7.1.1 for a single-operator/co-located Managed deployment
(the common case today), and specifying a distribution/trust protocol for
endpoint allowlists before there is a concrete multi-operator deployment
driving requirements would be exactly the kind of premature-generality this
roadmap's own rules warn against elsewhere. §7.1.1 is closed once execution
and probing genuinely happen behind the execution/data-plane boundary under
an operator-controlled allowlist -- how that allowlist gets populated across
more than one operator is future scope.

## 6. Acceptance

§7.1.1 is closed when:

1. `atos`'s Job/economic service issues `SubmitJob`/`QuoteExecution`/
   `GetProviderStatus` carrying `ThirdPartyBinding` and never dials the
   provider endpoint itself;
2. `tos-protocol` routes a request carrying `ThirdPartyBinding` to the
   execution/data-plane boundary rather than executing it locally;
3. `tos-ai` (or an explicitly specified equivalent execution-side component)
   performs the actual dial, gated by a worker-operator-curated allowlist that
   an invocation cannot expand;
4. an end-to-end test demonstrates a third-party Managed Capability executing
   through this full path and landing in the existing Receipt/settlement
   pipeline unchanged, per §7.1.5's cross-repository acceptance criterion;
5. an invocation naming an endpoint_ref/transport/capability_id combination
   the worker's operator did not allowlist is rejected before any outbound
   network call, with a regression test proving it.
