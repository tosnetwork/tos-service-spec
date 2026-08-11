# ATOS Managed Financial Integrity V1

**Status:** Normative  
**Version:** `atos_managed_financial_integrity_v1`  
**Applies to:** Managed economic events emitted by an ATOS gateway

This document freezes the Phase 7A contract shared by `atos`, `blnk`,
`tos-protocol`, retained evidence, and independent verifiers. Implementations
MUST reject unknown versions rather than interpreting them as V1.

## 1. Authority boundary

```text
ATOS business authorization and workflow
        -> ATOSFinancialAdapter
        -> Blnk transaction / balance
        -> rebuildable ATOS projection
```

Blnk is the only mutable Managed financial source of truth. ATOS account,
escrow, earning, dispute, and payout amounts are workflow state or rebuildable
projections. They MUST NOT authorize a financial mutation without a matching
Blnk operation. A mismatch never selects the newest representation; it opens
an integrity incident and enters financial safe mode.

The adapter does not create a second Quote, Job, billing, receipt, earning,
dispute, or payout state machine. It accepts only an already-authorized
transition from those state machines and expresses it in Blnk.

## 2. Asset registry and exact amounts

Every deployment has an immutable asset registry. V1 initially registers:

| asset | decimals | atomic unit | rounding |
|---|---:|---|---|
| `USD` | 2 | cent | reject excess precision |

Amounts in commitments and Adapter requests are unsigned canonical base-10
atomic-unit strings matching `^(0|[1-9][0-9]*)$`. Floating point, exponent
notation, signs, whitespace, localized digits, and implicit rounding are
forbidden. Every posting in one event uses one asset and its configured
precision. Asset-registry changes require a new registry version and MUST NOT
reinterpret committed history.

## 3. Chart of Accounts V1

Account identity is:

```text
atos:<gateway_id>:coa:v1:<asset>:<account_code>:<owner_id>
```

`owner_id` is `_` for singleton gateway accounts. Each identity maps to exactly
one Blnk balance ID; the mapping is insert-only and independently
reconcilable. User-controlled strings are encoded as lowercase base32 of their
UTF-8 bytes when constructing an external identifier; raw IDs remain in the
financial commitment.

| code | owner | purpose | may be negative |
|---|---|---|---:|
| `principal_available` | principal | spendable funds | no |
| `principal_reserved` | principal | authorized but not yet escrowed | no |
| `managed_escrow` | Job | funds backing one Managed Job | no |
| `provider_payable` | provider | matured/unpaid provider liability | no |
| `provider_disputed` | provider | payable held by a dispute | no |
| `gateway_fee_revenue` | `_` | earned gateway fees | no |
| `gateway_refund_liability` | `_` | funded customer refunds/adjustments | no |
| `payout_clearing` | payout | external payout in progress | no |
| `payout_disbursed` | `_` | cumulative externally disbursed value | no |
| `gateway_credit_issuance` | `_` | explicit opening/promotional credit source | yes, only through provisioning policy |

Normal runtime operations set Blnk `allow_overdraft=false`. Only the explicit
`account_genesis` operation may debit `gateway_credit_issuance`, and only up to
the configured issuance ceiling. Production defaults to zero opening credit.
The deployment sets the aggregate ceiling with
`ATOS_FINANCIAL_ISSUANCE_LIMIT`; ATOS passes it as Blnk's overdraft limit on
the shared issuance account. A positive `ATOS_MANAGED_INITIAL_BALANCE` is
invalid when that ceiling is zero.
A zero opening credit is the absence of an economic event: implementations
MUST NOT submit a zero-value ledger transaction or consume a financial
commitment sequence. Until the first non-zero posting creates the balance,
an authoritative Blnk balance lookup returning not-found is read as exact zero.
No principal, escrow, provider, refund-liability, or clearing account may go
negative.

## 4. Economic events and postings

`debit` means value leaves the named account; `credit` means value enters it.
For every event and asset:

```text
sum(debit atomic amounts) == sum(credit atomic amounts)
```

The stable identity in the last column is scoped by `gateway_id`, `network_id`,
event type, and the named business ID. A retry with identical canonical content
returns the original result. Changed content under that identity is
`idempotency_conflict`.

| event | debit | credit | stable identity suffix |
|---|---|---|---|
| `account_genesis` | `gateway_credit_issuance` | `principal_available` | `principal:<principal_id>:genesis:v1` |
| `reserve` | `principal_available` | `principal_reserved` | `job:<job_id>:reserve:v1` |
| `reservation_release` | `principal_reserved` | `principal_available` | `job:<job_id>:reservation-release:v1` |
| `escrow_fund` | `principal_reserved` | `managed_escrow` | `job:<job_id>:escrow-fund:v1` |
| `escrow_release` | `managed_escrow` | `principal_available` | `job:<job_id>:escrow-release:v1` |
| `settlement_provider` | `managed_escrow` | `provider_payable` | `settlement:<settlement_id>:provider:v1` |
| `settlement_fee` | `managed_escrow` | `gateway_fee_revenue` | `settlement:<settlement_id>:fee:v1` |
| `settlement_refund` | `managed_escrow` | `principal_available` | `settlement:<settlement_id>:refund:v1` |
| `partial_refund` | `provider_payable` or `provider_disputed` | `principal_available` | `refund:<dispute_id>:<ordinal>:v1` |
| `full_refund` | `provider_payable` or `provider_disputed` | `principal_available` | `refund:<dispute_id>:full:v1` |
| `gateway_refund_fund` | `gateway_fee_revenue` | `gateway_refund_liability` | `refund:<dispute_id>:gateway-fee-fund:v1` |
| `gateway_refund_pay` | `gateway_refund_liability` | `principal_available` | `refund:<dispute_id>:gateway-fee-pay:v1` |
| `compensating_reversal` | exact opposite accounts/amount of referenced event | exact opposite | `reversal:<original_event_id>:<reason_id>:v1` |
| `dispute_hold` | `provider_payable` | `provider_disputed` | `dispute:<dispute_id>:hold:v1` |
| `dispute_release` | `provider_disputed` | `provider_payable` | `dispute:<dispute_id>:release:v1` |
| `payout_intent` | `provider_payable` | `payout_clearing` | `payout:<payout_id>:intent:v1` |
| `payout_success` | `payout_clearing` | `payout_disbursed` | `payout:<payout_id>:success:v1` |
| `payout_failure` | `payout_clearing` | `provider_payable` | `payout:<payout_id>:failure:<attempt_generation>:v1` |
| `manual_adjustment` | policy-selected explicit source | policy-selected explicit destination | `adjustment:<adjustment_id>:v1` |

A settlement is complete only when its provider, fee, and refund legs sum to
the escrowed maximum and all legs are durably observable. The adapter uses a
durable settlement intent and deterministic leg identities; a partially
observed multi-leg response remains reconciling and cannot authorize a second
semantic settlement. `ProviderEarning.NetAmount` equals the provider leg.

Refunds and reversals are new transactions. Committed Blnk transactions and
financial commitments are never edited in place. A paid payout is not treated
as refundable without an independently verified external clawback result.
A `compensating_reversal` MUST reference one finalized event and exactly swap
that event's debit/credit accounts and owners while preserving its asset and
atomic amount. At most one full compensating reversal may reference a given
event; PostgreSQL uniqueness, not an in-process check, enforces this under
concurrency.

## 5. ATOSFinancialAdapter V1

The implementation boundary exposes these semantic operations:

```text
ProvisionAccount, Balance
Reserve, ReleaseReservation, FundEscrow, ReleaseEscrow
Settle, PartialRefund, FullRefund, CompensatingReversal
FundGatewayRefund, PayGatewayRefund
HoldDispute, ReleaseDispute
BeginPayout, CompletePayout, FailPayout
Lookup, Reconcile
```

Every mutation carries `gateway_id`, `network_id`, `principal_id`,
`provider_id`, `job_id`, `quote_id`, `capability_id`, `capability_version`,
`billing_snapshot_id`, `execution_receipt_id`, `settlement_id`,
`provider_earning_id`, `dispute_id`, `payout_id`, asset, atomic amount,
economic event type, and stable idempotency identity where applicable.
Inapplicable identities are the empty string and remain explicit in the
canonical commitment. Confidential fields, prompts, artifacts, tokens,
credentials, payout-rail secrets, wallet material, and private keys are
forbidden.
Posting owners are not free-form aliases: validation binds principal accounts
to `principal_id`, escrow to `job_id`, payable/disputed accounts to
`provider_id`, clearing to `payout_id`, and singleton gateway accounts to `_`.
An identity-bearing request with substituted posting owners is invalid before
an intent or sequence is allocated.

External side effects follow:

```text
durable ATOS intent -> Blnk/external call -> durable observed outcome
```

A timeout is uncertain. Recovery first looks up the exact stable identity.
No correctness property may depend on a process-local mutex.

## 6. Financial Commitment V1

### 6.1 Canonical value

The canonical value is an RFC 8949 Core Deterministic CBOR map over the JSON
data model below. It uses the exact bounded encoder defined by
`tos-protocol/pkg/codec`: UTF-8 string map keys, no floats, tags, indefinite
items, duplicate keys, non-string keys, or unknown fields. Implementations
MUST decode and re-encode to the identical bytes before accepting retained
evidence.

```json
{
  "version":"atos_financial_commitment_v1",
  "canonicalization":"rfc8949_core_deterministic_cbor",
  "gateway_id":"gateway.example",
  "network_id":"tos-localnet-1",
  "sequence":1,
  "previous_commitment":"sha256:0000000000000000000000000000000000000000000000000000000000000000",
  "event_id":"fevt_01",
  "event_type":"reserve",
  "idempotency_identity":"gateway.example:job:job_01:reserve:v1",
  "occurred_unix_millis":1786420800000,
  "ledger_reference":"atos-fevt-fevt_01",
  "ledger_transaction_ids":["txn_01"],
  "asset":"USD",
  "atomic_amount":"125",
  "identities":{
    "principal_id":"principal_01","provider_id":"provider_01",
    "job_id":"job_01","quote_id":"quote_01",
    "capability_id":"capability_01","capability_version":"1.0.0",
    "billing_snapshot_id":"","execution_receipt_id":"",
    "settlement_id":"","provider_earning_id":"",
    "dispute_id":"","payout_id":""
  },
  "postings":[
    {"entry_index":0,"account_code":"principal_available","account_owner_id":"principal_01","direction":"debit","atomic_amount":"125"},
    {"entry_index":1,"account_code":"principal_reserved","account_owner_id":"principal_01","direction":"credit","atomic_amount":"125"}
  ],
  "reverses_event_id":""
}
```

`postings` are ordered by contiguous `entry_index` starting at zero.
`ledger_transaction_ids` are lexicographically sorted. ATOS derives each ID
from the stable idempotency identity and supplies it through Blnk's bounded
caller-assigned `transaction_id` contract, so the durable intent can bind the
final ledger identity before submission. Blnk MUST preserve a supplied ID and
MUST reject a duplicate ID/reference rather than generate a replacement.
ATOS `decimals` is a count of decimal places; Blnk's legacy `precision` wire
field is the integer scale factor. The adapter MUST therefore send
`precision = 10^decimals` (for example, USD `decimals=2` maps to Blnk
`precision=100`) while `precise_amount` carries the exact atomic integer.
Sequence allocation and the previous digest advance in one PostgreSQL
transaction under a locked singleton state; two replicas cannot allocate the
same sequence.

### 6.2 Digest

The domain is the ASCII string:

```text
tos.atos.financial.commitment.v1
```

The digest is:

```text
SHA-256(
  "TOS-PROTOCOL-CBOR" || 0x00 ||
  uint16_be(len(domain)) || domain ||
  canonical_cbor(value)
)
```

and is rendered `sha256:<lowercase hex>`. Blnk `reference` carries the stable
event identity and immutable Blnk `description` carries
`atos-financial-v1:<digest>`. Mutable Blnk `meta_data` is never evidence.

The genesis previous commitment is 32 zero bytes. A verifier rejects mutation,
deletion, insertion, reordering, a sequence gap, changed amount/identity,
changed version, or gateway/network substitution.

Normative bytes and digests are in
`schemas/managed-financial-integrity-v1-vectors.json`.

## 7. Deterministic Merkle batch V1

Finalized commitment leaves are strictly ordered by contiguous financial
sequence. A batch contains 1..4096 leaves and does not overlap another batch.
The leaf hash is `SHA256(0x00 || commitment_digest_bytes)`. The internal node is
`SHA256(0x01 || left || right)`. An unpaired final node is duplicated as both
left and right at every level. A one-leaf root is its leaf hash.

The batch manifest is canonical CBOR with domain
`tos.atos.financial.batch.v1` and fields:

```text
version, canonicalization, gateway_id, network_id, batch_sequence,
batch_id, first_sequence, last_sequence, commitment_count,
previous_batch_id, previous_merkle_root, merkle_root,
commitment_digests, created_unix_millis
```

`batch_id` is `fbat_` plus lowercase SHA-256 of the canonical CBOR batch
identity containing every field above except `batch_id` and
`created_unix_millis`. The creation time is allocated once and is not part of
retry identity. Batch state advances in one transaction; finalized manifests
are append-only.

## 8. External signature and immutable retention

The signed payload is the canonical batch manifest bytes under domain
`tos.atos.financial.batch-signature.v1`. A signature envelope binds:

```text
version, batch_id, manifest_digest, signing_digest, gateway_id, network_id,
signing_key_id, signing_algorithm, signature, public_key, signed_unix_millis
```

Supported V1 verification algorithms are `ed25519` and
`ecdsa_p256_sha256`. Production signing is through a KMS/HSM/Vault boundary;
the normal ATOS/Blnk host receives Sign/Verify/PublicKey capability only and
never private key bytes. `(batch_id, manifest_digest)` is the stable signing
identity. A substituted digest under the same batch is a conflict. Key
rotation atomically changes `signing_key_id` and the deployment-pinned
`ATOS_FINANCIAL_SIGNING_PUBLIC_KEY`; online sealing rejects a signer response
whose public key differs before retention or anchoring. Historical public keys
and validity windows remain retained and independently verifiable.

The exact manifest bytes, signature envelope, public-key evidence, and ledger
evidence are written to an independently administered append-only object key:

```text
atos-financial/v1/<gateway_id>/<network_id>/<batch_sequence>-<batch_id>.json
```

Production storage MUST enforce bucket versioning plus Object Lock compliance
mode (or a reviewed equivalent WORM control). A successful ordinary overwrite
or delete is a failed deployment check. Database state alone never marks a
batch independently retained.

## 9. Managed Financial Ledger Anchor V1

The anchor payload uses canonical CBOR domain
`tos.atos.managed-financial-anchor.v1` and binds:

```text
version, anchor_id, batch_id, batch_sequence, first_sequence, last_sequence,
commitment_count, previous_anchor_id, previous_merkle_root, merkle_root,
manifest_digest, signature_digest, signing_key_id, canonicalization,
gateway_id, network_id
```

`anchor_id` is `fanchor_` plus SHA-256 of the canonical payload with
`anchor_id` omitted. It is the stable TOS publication identity. The normal
path is:

```text
atos -> tos-protocol FinancialIntegrityService -> TOS ActionPublisher
     -> quorum/finality observation
```

`PublishManagedFinancialAnchor` persists the exact payload before publication,
publishes with kind `managed-financial-ledger-root`, and returns the same
finalized reference for an exact retry. Changed semantics under the same
`anchor_id` conflict. A lost response is recovered through
`ResolveManagedFinancialAnchor`; it never authorizes a new anchor identity.
Resolution returns network, reference, finalized status, observed finalized
checkpoint, and the exact stored payload digest. Wrong/unfinalized/reorganized
network observations fail closed.

This anchor proves only the integrity of Managed aggregate history. It MUST NOT
change a Quote/Job trust mode, populate `tos_verified_v1` escrow/settlement
proof fields, or be described as a Verified transaction.

## 10. Reconciliation, rebuild, and safe mode

Rebuild reads sealed Blnk transactions and replays the account postings in
financial sequence into an empty projection. Comparison is deterministic and
classifies at least:

```text
missing_ledger_event, unexpected_ledger_event, semantic_conflict,
projection_mismatch, conservation_failure, sequence_gap,
commitment_mismatch, batch_mismatch, signature_mismatch,
retention_missing, anchor_missing, anchor_mismatch,
payout_rail_mismatch
```

Reconciler ownership uses a PostgreSQL lease/advisory lock and a durable
cursor. A crash releases/expires the lease and another replica resumes from the
last completed checkpoint. Lost Blnk, signer, archive, payout, or TOS responses
are resolved by stable identity lookup.

The ATOS connector MUST also submit its reconstructed ledger rows to Blnk's
generic reconciliation engine as an exact, dry-run `one_to_one` reconciliation
over amount, reference, currency, and immutable description. Its caller-supplied
reconciliation identity is derived from the ordered commitment digests. A retry
with the same identity and input converges; changed input under that identity
conflicts. Blnk persists engine progress/status for crash recovery. This engine
cross-check supplements, and never replaces, exact `precise_amount`, balance,
commitment-chain, projection, signature, retention, and anchor verification.

Any conservation, sealed-history, signature, retained-manifest, anchor, or
payout mismatch enters `financial_safe_mode`. In safe mode, public balance and
history reads remain available with an integrity status; new reserve,
settlement, refund, reversal, dispute release, and payout mutations fail with
`financial_safe_mode`. Reconciliation and independently authorized recovery
remain available. Exit requires a complete successful verification through the
latest required anchor and an audited break-glass recovery identity; it is not
an ordinary runtime endpoint.

## 11. Independent verifier

The verifier consumes retained evidence and configured public/network trust
roots. It MUST NOT query or trust current mutable ATOS tables. It verifies:

```text
Blnk sealed ledger evidence -> commitments/hash chain -> Merkle manifest
-> external signature/public key -> retained object identity -> finalized TOS anchor
```

It fails on substituted roots/keys/domains/networks, deletion or reordering,
changed sealed fields, non-contiguous sequence, wrong previous root, mismatched
Object Lock evidence, anchor disagreement, or an unfinalized/wrong-network
anchor.

## 12. Database and operational roles

Normal credentials are `NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS`.
`atos_runtime` and `blnk_runtime` cannot `UPDATE`/`DELETE` sealed history or
grant privileges. `atos_migrator`/`blnk_migrator` own schema changes but are
absent from long-running services. `atos_auditor`/`blnk_auditor` are read-only.
Backup and archive credentials can create retained objects but cannot shorten
retention or delete locked versions. Break-glass is time-bounded, separately
approved, externally audited, and never stored in application configuration.

Deployment verification includes PostgreSQL 16 PITR with WAL archiving,
independent base/WAL retention, arbitrary-point restore, WORM overwrite/delete
denial, role capability assertions, and reconstruction through the signed TOS
anchor. No production infrastructure mutation is implied by this contract.
