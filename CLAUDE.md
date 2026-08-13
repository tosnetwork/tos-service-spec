# ATOS Specification Contributor Rules

## Read authority in order

Before changing product scope, schemas, or protocol behavior, read completely:

1. `docs/PRODUCT_STRATEGY.md`
2. `docs/ARCHITECTURE.md`
3. `docs/NATIVE_REGISTRY_STATE_MACHINES.md`
4. `docs/ROADMAP.md`

The strategy controls delivery priority and initial market scope. It cannot
weaken architecture or contract safety. The architecture document controls
system boundaries. The state-machine document controls Agent and Capability
transitions. The roadmap controls implementation order and acceptance evidence.

## Greenfield contract

ATOS has one protocol: `atos_native_v1`. Do not add alternate authority paths,
gateway-owned canonical objects, caller-supplied next state, or fields from
abandoned drafts. If an implementation experiment conflicts with
the specification, isolate or remove it; do not weaken the Native schema.

## Schema discipline

- Make normative changes in `proto/atos/native/v1/native.proto` first.
- Use reserved field numbers when removing a field from a frozen message.
- Bound every repeated field, string, byte sequence, cell, response, and retry.
- Specify canonical ordering and rejection behavior.
- Keep transport context outside signed action semantics.
- Keep chain references and network domain explicit.

## Vector discipline

Every canonical encoding or digest change requires independently reproducible
positive vectors and negative mutations. Generate values from implementation;
never transcribe hashes, signatures, BOCs, or addresses manually.

A frozen vector records all inputs needed to reproduce its output, including
network domain, contract code hash, public keys, nonces, ordering, and expected
state or action hashes.

## Atomic-read discipline

Tests and services must not compose one logical result from separately locked
reads when a concurrent transition could occur between them. Expose one
snapshot operation or hold one lock across the complete read. This rule applies
to chain checkpoint views, indexes, stores, and in-memory test doubles.

## Completion discipline

Do not claim completion from source presence or compilation alone. Record:

- normative schema and invariants;
- implementation repositories and commits;
- unit and adversarial tests;
- frozen cross-language vectors;
- local-chain or public-network evidence as appropriate; and
- unresolved operational or audit gates.

Documentation must describe the intended Native system directly. Historical
draft narratives do not belong in the normative repository.

Before adding a new protocol surface, apply the decision filter in
`docs/PRODUCT_STRATEGY.md`. Defer work that does not complete authority safety,
the first software-work commercial lifecycle, interoperability, or measurable
market usage.
