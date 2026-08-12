# ATOS Proof Profiles v0.2

> Phase 4C addition: a completed `tos_verified_v1` transaction is portable
> only through the canonical package in `VERIFIED_PROOF_PACKAGE_V1.md`.
> Local proof-status flags and deterministic protobuf bytes are not canonical
> evidence. Independent verification requires read-only live resolution of
> identity, ownership, Quote, TaskEscrow, Receipt, outcome and Proof-of-Service
> references.

## 1. Purpose

A trust-mode label is useful only if independent implementations agree on what it guarantees.

ATOS therefore separates:

- `trust_mode` — the user-visible transaction mode;
- `proof_profile` — the normative machine-verifiable guarantee set used to implement that mode.

Initial standard profiles:

```text
tos_verified_v1
tos_native_v1
```

Managed Mode does not require a standard network proof profile.

## 2. General Rules

1. A Quote locks one concrete `trust_mode` and, when required, one `proof_profile`.
2. The proof profile cannot change after Quote issuance without a new Quote.
3. A standard profile name MUST have the same minimum meaning across gateways.
4. A gateway may provide stronger guarantees than the profile minimum but MUST NOT provide weaker guarantees under the same name.
5. Private/bulk payloads remain off-chain; cryptographic commitments represent them when proof is required.
6. Economic guarantees require enforceable TOS-backed state, not merely a hash of a private gateway ledger.
7. Evidence may be batched/aggregated only when independent inclusion/finality verification remains possible.
8. A failure to satisfy a required proof checkpoint fails/requotes the transaction; it never silently downgrades the trust mode.
9. For `tos_verified_v1`, execution admission requires the exact finalized
   Quote commitment and an independently observed finalized TaskEscrow
   reservation defined by `VERIFIED_TASK_ESCROW_V1.md`. Publisher or journal
   evidence without canonical contract observation is insufficient. Released,
   expired, disputed, ambiguous and non-final escrow states close the gate.

## 3. Authorized Execution Signer

A receipt signer may be the provider itself or an authorized delegate/runtime.

Examples:

- provider agent key;
- `tos-ai` worker/runtime key;
- enterprise delegated key;
- MCP/HTTP execution adapter key;
- gateway adapter authorized for a human-backed capability.

The proof package must establish an authorization chain:

```text
Provider / Capability ownership
          |
          v
Execution-signer authorization
          |
          v
Signed Execution Receipt
```

Conceptual fields:

```json
{
  "execution_signer_id":"sig_...",
  "signer_authorization_ref":"tos:...",
  "signature":"..."
}
```

The authorization scope should bind at least the provider and capability, and SHOULD bind capability version and validity interval where possible.

## 4. `tos_verified_v1`

`tos_verified_v1` is the standard transaction-proof profile for `trust_mode=verified`.

### Required guarantees

#### Identity and ownership

- provider identity is TOS-verifiable;
- capability ownership is TOS-verifiable;
- quoted capability version resolves to an immutable manifest commitment.

#### Quote

- Quote/terms commitment is TOS-verifiable;
- Quote binds provider, capability/version, concrete trust mode, maximum price, expiry, settlement model, proof profile, and dispute policy commitment.

#### Economic reservation

For paid committed work:

- an enforceable TOS-backed escrow/reservation exists before billable execution proceeds;
- the reserved amount/asset mapping is provable;
- a mere commitment to a centrally controlled balance is not sufficient to claim TOS-backed escrow.

A gateway may sponsor/fund the network-side escrow on behalf of a fiat/credit-paying client. The Quote/settlement descriptor should identify that funding model when relevant.

#### Execution Receipt

- an authorized execution signer signs the receipt;
- signer authorization is verifiable;
- receipt binds Quote, provider, capability/version, result, usage/charge basis, and relevant input/output/artifact commitments;
- receipt commitment/inclusion is TOS-verifiable.

#### Settlement

- final settlement/release/refund transition is TOS-backed and independently verifiable;
- actual charge does not exceed the Quote maximum;
- unused reservation is released according to the Quote;
- dispute corrections use auditable state transitions rather than hidden balance edits.

#### Proof-of-Service

- the completed outcome can produce portable Proof-of-Service evidence attributable to the provider/capability;
- evidence need not expose raw private payloads.

### Not required

`tos_verified_v1` does not require:

- `atos.im` independence;
- decentralized semantic search;
- global capability resolution through multiple gateways;
- raw prompts/files/results on-chain;
- model execution inside TOS consensus.

## 5. `tos_native_v1`

`tos_native_v1` is the standard profile for `trust_mode=native`.

It **extends all guarantees of `tos_verified_v1`** and adds gateway/namespace independence.

### Additional required guarantees

#### Global identity and capability resolution

- provider/Agent identity is globally resolvable through the protocol/TOS model;
- capability ID is federation-safe;
- ownership and quoted manifest/version can be resolved without querying an `atos.im` canonical database.

#### Gateway independence

- `atos.im` is not required to verify canonical trust/economic/proof facts;
- another compatible gateway/resolver can validate the provider, capability, receipt, and settlement proof;
- gateway-local aliases, rankings, accounts and caches are clearly distinguished from canonical Native facts.

#### Registry/index reconstruction

- Native capability registry events/commitments are available in a form from which independent indexers can reconstruct the relevant supply/trust projection;
- semantic ranking remains off-chain and gateway-specific.

#### Replay/domain separation

- signatures/commitments used across gateways include sufficient domain/network/quote binding to prevent replay into a different capability, Quote, gateway context, or network where the protocol requires separation.

### Native does not mean bulk data on-chain

Provider execution and Artifact transport may remain off-chain.

Native means the **trust, namespace, proof and economic contract** is independently verifiable and not owned by `atos.im`.

## 6. Proof Package

A gateway/verifier SHOULD be able to materialize a normalized proof package for completed Verified/Native work.

Conceptually:

```json
{
  "proof_profile":"tos_verified_v1",
  "trust_mode":"verified",
  "network":"tos",
  "provider_identity_proof":"tos:...",
  "capability_ownership_proof":"tos:...",
  "manifest_commitment":"sha256:...",
  "quote_commitment":"tos:...",
  "escrow_proof":"tos:...",
  "execution_signer_id":"sig_...",
  "signer_authorization_ref":"tos:...",
  "receipt_commitment":"tos:...",
  "settlement_proof":"tos:...",
  "proof_of_service_ref":"tos:..."
}
```

The public MCP response normally returns compact proof status/references. Advanced REST/provider tooling may materialize the full proof package.

## 7. Batching and Aggregation

ATOS expects high transaction volume. It is valid to aggregate evidence efficiently.

Examples may include:

- batched registry commitments;
- Merkle inclusion commitments;
- aggregated receipt commitments;
- rollup-style proof structures;
- other TOS-native aggregation mechanisms.

However, batching must not reduce the promised guarantee.

For proof/evidence records, an independent verifier must be able to prove inclusion and relevant ordering/finality.

For escrow/settlement, the underlying value state must remain economically enforceable according to the profile. Publishing only a Merkle root of a private custodial database does **not** turn that database into TOS-backed escrow.

## 8. Failure Semantics

If a proof checkpoint fails:

```text
pending -> verified
pending -> failed
```

The system MUST NOT convert:

```text
verified -> managed
native   -> verified
native   -> managed
```

under the same Quote.

Recovery requires retry within the same guarantees when valid, or a new Quote.

## 9. Extensibility

Future profiles may add:

- privacy-preserving/ZK execution evidence;
- trusted-execution-environment attestations;
- deterministic/reproducible execution proof;
- multi-party validation;
- specialized dispute/arbitration proofs;
- regulated enterprise attestations.

New profile names must be versioned. A breaking change to guarantees requires a new profile identifier.
