# ATOS Financial Integrity Hardening

**Status:** Planned cross-cutting hardening specification  
**Applies to:** ATOS Managed financial state, provider earnings, payouts, refunds, disputes, and the integrity boundary between `atos.im` and TOS Network  
**Roadmap phase:** Phase 7 — Economy and Proof Hardening

> ATOS financial correctness must not depend on trusting one mutable PostgreSQL
> database, one application server, one database administrator, or one cloud
> account. PostgreSQL remains the operational database for Managed Mode, but
> financial truth must be reconstructible, auditable, tamper-evident, and
> independently anchored outside the database trust domain.

---

## 1. Purpose

ATOS handles financially meaningful state even when a Job uses Managed Mode and
never places the individual task on TOS Network. Examples include:

- principal available balance;
- reserved funds;
- Managed escrow;
- billed amount;
- provider earnings;
- gateway fees;
- refunds and reversals;
- dispute holds;
- payout intent and completion state.

A conventional mutable balance table is not sufficient for this role. If an
attacker obtains application-server root access, database-owner credentials, or
a privileged SQL path, simply replicating the database more reliably does not
protect the system from a malicious but syntactically valid financial update.
A corrupted value can be replicated consistently to every database replica.

This document defines the long-term ATOS financial-integrity architecture for
making such corruption difficult to perform silently, easy to detect, and
recoverable from independently retained evidence.

The design intentionally preserves the ATOS trust-mode model:

```text
Managed
= fast off-chain business execution and accounting inside atos.im,
  with independently anchored integrity evidence

Verified
= atos.im UX plus TOS-verifiable transaction trust/economic checkpoints

Native
= TOS-backed canonical trust/economic state usable without atos.im as a
  mandatory authority
```

Managed Jobs do **not** need to become individually on-chain transactions in
order for the Managed financial ledger to obtain tamper-evident protection.

---

## 2. Threat Model

The architecture MUST assume that any one of the following can eventually
happen:

1. an ATOS API process is compromised;
2. an attacker obtains the runtime PostgreSQL credential;
3. an operator accidentally executes a destructive SQL statement;
4. a privileged DBA account is compromised;
5. an application bug produces an invalid economic transition;
6. a database replica faithfully replicates corrupted financial data;
7. an attacker attempts to rewrite historical ledger rows;
8. an attacker deletes or corrupts the primary database;
9. an attacker attempts to delete local WAL/backups together with the primary;
10. an attacker attempts to forge a new historical financial root after local
    state has been altered.

The system MUST NOT assume that:

- database replication makes malicious updates safe;
- Row-Level Security protects against a database superuser;
- SQL audit logs stored only in the same database/server are immutable;
- encryption at rest prevents an authorized SQL session from modifying rows;
- a hash stored beside the data it protects is sufficient once the same host is
  fully compromised.

The design should tolerate compromise of one operational trust domain without
allowing undetectable rewriting of previously finalized financial history.

---

## 3. Core Invariants

### 3.1 Balance is a projection, not the primary financial fact

A table such as:

```text
accounts(principal_id, balance)
```

MUST NOT be the only authoritative representation of wealth.

The canonical Managed financial record should be an append-oriented ledger from
which account projections can be rebuilt.

Conceptually:

```text
Financial Transaction
        |
        +--> Ledger Entry A
        +--> Ledger Entry B
        +--> ...
        |
        v
Account / escrow / earning projections
```

`accounts.balance`, provider payable totals, escrow totals, and similar values
are operational projections/caches of ledger facts.

If a projection disagrees with the ledger, the discrepancy is an integrity
incident, not a new source of truth.

### 3.2 Double-entry conservation

Every money-changing Managed transaction MUST preserve double-entry
conservation for one currency/asset domain:

```text
sum(debits) == sum(credits)
```

Examples:

Principal reservation:

```text
Debit   principal:available
Credit  gateway:managed_escrow
```

Settlement:

```text
Debit   gateway:managed_escrow
Credit  provider:payable
Credit  gateway:fee_revenue
Credit  principal:refund        (when applicable)
```

Dispute principal-win before payout:

```text
Debit   provider:disputed_payable / reversal source
Credit  principal:available
```

The exact account taxonomy may differ, but every transition must conserve value
and remain bound to its Job/Quote/settlement/dispute identity.

### 3.3 No ad-hoc economic mutation

No service may create a new code path equivalent to:

```text
Get balance
modify balance
Put balance
```

Money-changing operations MUST use purpose-built atomic transaction boundaries
that append the financial transaction/entries and update projections in the
same PostgreSQL transaction, or use an equivalently strong transactional
primitive.

### 3.4 Historical ledger records are append-only

Once a financial transaction reaches its committed state, its economic content
MUST NOT be modified in place.

Corrections are represented as new compensating/reversal transactions, never by
rewriting historical entries.

The runtime application role should not possess general `UPDATE`, `DELETE`,
`TRUNCATE`, `ALTER`, or `DROP` authority over immutable ledger tables.

### 3.5 Every economic event is strongly bound

Ledger transactions SHOULD bind all relevant immutable identities, including
where applicable:

- ledger transaction ID;
- principal/provider account identity;
- Job ID;
- Quote ID;
- Capability ID/version;
- execution receipt ID;
- settlement receipt ID;
- BillingSnapshot identity/commitment;
- ProviderEarning ID;
- dispute ID;
- payout idempotency identity;
- asset/currency;
- exact amount;
- event type;
- canonical timestamp/sequence.

A ledger transaction for one economic history must never be reusable as proof
for another.

---

## 4. Recommended Managed Financial Model

ATOS should converge toward a model similar to:

```text
ledger_accounts
ledger_transactions
ledger_entries
ledger_batches
ledger_anchors

accounts                  # principal projection
managed_escrows           # escrow projection / existing durable state
billing_snapshots         # immutable billing evidence
provider_earnings         # provider liability projection
receipts                   # settlement evidence
payout state              # external side-effect checkpoint
```

### 4.1 `ledger_accounts`

Represents accounting buckets rather than end-user authentication identities.
Examples:

```text
principal_available:<principal_id>
principal_reserved:<principal_id>
managed_escrow:<job_id>
provider_payable:<provider_id>
provider_disputed:<provider_id>
gateway_fee_revenue
gateway_refund_liability
payout_clearing
```

The final chart of accounts must be explicitly versioned and documented before
production accounting/reporting depends on it.

### 4.2 `ledger_transactions`

One durable economic event.

Recommended fields include:

```text
id
sequence
transaction_type
currency / asset
job_id
quote_id
settlement_id
dispute_id
idempotency_key
created_at
previous_transaction_hash
content_hash
batch_id
```

Economic identity fields are immutable after insertion.

### 4.3 `ledger_entries`

Each transaction contains two or more entries whose signed amounts net to zero.
Recommended fields:

```text
transaction_id
entry_index
ledger_account_id
direction  (debit | credit)
amount
currency / asset
```

Use exact integer/fixed-point arithmetic. Floating point is forbidden for
financial balances.

### 4.4 Projections

Current account/escrow/earning values are maintained for fast reads and existing
ATOS APIs, but the system MUST be able to recompute them from the ledger.

A projection rebuild tool should support:

```text
ledger history
    -> deterministic replay
    -> rebuilt projections
    -> compare against production projections
```

A mismatch is a reconciliation failure.

---

## 5. Cryptographic Tamper Evidence

Database permissions and audit logs reduce the probability of unauthorized
changes but do not provide an independent historical truth after total host/DB
compromise. ATOS therefore adds cryptographic integrity evidence.

### 5.1 Canonical financial transaction digest

Every committed financial transaction should have a deterministic,
domain-separated digest over its immutable economic fields and ordered ledger
entries.

Conceptually:

```text
H_n = SHA256(
  "ATOS-FINANCIAL-LEDGER-V1" ||
  sequence ||
  H_(n-1) ||
  canonical_transaction_payload
)
```

The exact canonical encoding MUST be frozen in `atos-spec` before independent
implementations rely on it. JSON serialization with implementation-dependent
map ordering is not an acceptable long-term commitment format.

### 5.2 Hash chain

Each ledger transaction or finalized batch should commit to the previous
sequence/root so deletion, insertion, reordering, or historical rewriting is
detectable.

A local hash chain alone is **not** sufficient if an attacker controls both the
database and the process that computes it; the attacker could rewrite the
history and recompute the chain. External anchoring is therefore mandatory for
the strongest Managed integrity claim.

### 5.3 Merkle batches

Ledger transactions are grouped into deterministic batches, for example by:

- fixed sequence range;
- maximum transaction count;
- bounded time window;
- or a deterministic combination of these.

For each finalized batch compute at least:

```text
batch_sequence
first_ledger_sequence
last_ledger_sequence
transaction_count
previous_batch_root
merkle_root
created_at
canonicalization_version
```

Batch construction MUST be deterministic so an independent verifier can rebuild
the same root from retained ledger entries.

### 5.4 External signing key

A finalized batch root should be signed by a key whose private material is not
stored on the ATOS database/application host.

Preferred production shape:

```text
ATOS financial root builder
        |
        v
KMS / HSM Sign
        |
        v
signed ledger batch
```

The application should receive only narrowly scoped signing permission. Key
administration, policy changes, deletion, and recovery authority should reside
in a separate administrative/security trust domain.

The signature does not replace TOS anchoring; it gives an additional identity
and operational-control boundary.

### 5.5 TOS Network integrity anchor

ATOS Managed ledger batches SHOULD periodically anchor their signed Merkle root
to TOS Network.

This does **not** mean every Managed Job or every ledger transaction executes on
chain.

Conceptually:

```text
Managed A2A Jobs
      |
      v
ATOS double-entry ledger
      |
      v
batch / Merkle root
      |
      v
KMS/HSM signature
      |
      v
TOS Network integrity anchor
```

The anchor should bind at least:

```text
domain = ATOS_MANAGED_FINANCIAL_LEDGER_V1
atos/gateway identity
batch_sequence
first/last ledger sequence
transaction count
previous anchored root
current Merkle root
canonicalization version
signature/key identifier or commitment
timestamp / network identity
```

An independent verifier must be able to detect that a locally reconstructed
historical root differs from the finalized TOS anchor.

### 5.6 Trust-mode semantics

The TOS ledger anchor must not blur the distinction among Managed, Verified,
and Native transaction guarantees.

For **Managed** Jobs:

```text
PostgreSQL append-only ledger
= operational Managed financial source of truth

TOS batch anchor
= tamper-evident audit/integrity commitment
```

Anchoring the Managed ledger root does **not** retroactively make each Managed
Job `trust_mode=verified` and does not satisfy `tos_verified_v1` transaction
requirements by itself.

For **Verified** Jobs, the individual transaction's required TOS-backed escrow,
receipt/settlement/proof guarantees remain authoritative under the proof
profile.

For **Native** Jobs, canonical economic/trust facts must remain independently
usable without the `atos.im` Managed database.

---

## 6. Privilege Separation

ATOS must assume that excessive database privilege is itself a financial risk.

Recommended production roles:

### 6.1 `atos_app`

Runtime application credential.

Properties:

```text
NOSUPERUSER
NOCREATEDB
NOCREATEROLE
NOBYPASSRLS
```

It receives only the table/procedure privileges required by normal ATOS
runtime operations.

It MUST NOT own the database/schema and MUST NOT possess general mutation
rights over immutable ledger/audit history.

### 6.2 `atos_migrator`

Used only during controlled schema deployment.

The credential should not be permanently available to the API runtime host.

### 6.3 `atos_auditor`

Read-only access to ledger, anchor and audit evidence sufficient for independent
reconciliation.

It must not be able to modify production financial state.

### 6.4 Security / database administration

Database administration, privilege administration, security/audit access and
financial-operations approval SHOULD be separated operationally where
practical.

No routine operator identity should simultaneously have unrestricted ability
to:

```text
change financial rows
+
grant itself new permissions
+
delete/alter audit evidence
+
destroy all backups/anchors
```

Break-glass privileges should be exceptional, strongly authenticated,
short-lived, fully audited, and excluded from normal application credentials.

---

## 7. Database and Infrastructure Controls

Financial integrity is not only a ledger problem. PostgreSQL and its surrounding
infrastructure must still be hardened.

Minimum controls include:

- TLS for remote database connections;
- secret rotation and short-lived credentials where possible;
- no PostgreSQL superuser credential in application configuration;
- network isolation and explicit database ingress policy;
- encryption at rest;
- full SQL/DDL/security audit outside the ordinary application log stream;
- database statement/role monitoring;
- point-in-time recovery;
- replica/failover architecture appropriate to the production RPO/RTO;
- periodic restore drills;
- independent monitoring of replication/backup/anchor health.

Strong replication protects availability and accidental loss. It does not
replace ledger integrity/reconciliation because a malicious committed SQL
transaction can be faithfully replicated.

---

## 8. Backups, WAL and Independent Retention

Backups must survive compromise of the primary ATOS server and preferably
compromise of the primary application cloud account.

Recommended shape:

```text
PostgreSQL primary
      |
      +--> replica / HA domain
      |
      +--> WAL archive
      |        |
      |        v
      |   separate backup trust domain
      |
      +--> periodic base backups
               |
               v
        immutable/WORM retention
```

Requirements:

- WAL/base backups must not exist only on the primary host;
- backup deletion authority should be separate from runtime application
  authority;
- retention should include immutable/WORM controls where supported;
- restoration to an arbitrary point in the retention window must be tested;
- signed ledger batch manifests/roots should be retained independently of the
  production database;
- verifier tooling must be able to rebuild historical ledger roots from a
  restored backup and compare them with external signatures/TOS anchors.

---

## 9. Continuous Reconciliation

ATOS should continuously reconcile independent representations of the same
financial reality.

At minimum:

```text
ledger entries
    <-> account projections

ledger settlement entries
    <-> BillingSnapshot / Receipt / ProviderEarning

payout clearing ledger
    <-> external payout rail results

refund/reversal ledger
    <-> dispute/economic state

finalized ledger batches
    <-> KMS/HSM signatures
    <-> TOS Network anchors
```

Reconciliation must be deterministic and independently runnable.

A mismatch MUST NOT be silently repaired by overwriting the ledger to match a
projection. The system should stop or quarantine affected money-moving flows,
produce an incident record, and require an explicitly authorized recovery
procedure.

### 9.1 Conservation checks

Examples of invariants that can be checked continuously:

```text
sum(all entries per transaction) == 0

principal projection
== replayed principal ledger position

provider payable projection
== replayed provider ledger position

payout marked paid
=> corresponding external rail reference exists

ledger batch root
== independently reconstructed root

anchored root
== finalized TOS commitment
```

### 9.2 Reconciliation cadence

Different checks may run at different frequencies, but high-value economic
invariants should be checked continuously or in short bounded intervals.

The time between local commit and external root anchor defines a residual
historical-rewrite detection window and must be explicitly measured and
operationally bounded.

---

## 10. Financial Safety Modes and Incident Response

ATOS should support an explicit financial safe mode independent of general API
availability.

Triggers may include:

- double-entry conservation failure;
- projection mismatch;
- duplicate economic identity;
- signed batch verification failure;
- TOS anchor mismatch;
- unexpected ledger sequence gap;
- payout rail reconciliation mismatch;
- database audit evidence indicating unauthorized financial mutation;
- inability to produce/retain integrity anchors beyond a configured maximum
  interval.

Safe mode may allow read-only account access while blocking new high-risk money
movement such as:

```text
new payout
settlement finalization
manual balance adjustment
ledger correction
withdrawal
```

The system must prefer temporary financial unavailability over continuing to
move money after integrity has become uncertain.

Incident recovery should be based on independently retained evidence:

1. isolate affected writers;
2. identify last independently verified ledger sequence/root;
3. restore/replay from trusted backup/WAL when necessary;
4. rebuild projections from the immutable ledger;
5. compare reconstructed batches to signatures and TOS anchors;
6. reconcile external payout/payment rails;
7. create explicit compensating transactions for legitimate corrections;
8. never rewrite already anchored history to make the incident disappear.

---

## 11. Manual Adjustments

Financial operations occasionally require manual correction, but direct SQL
balance edits are forbidden as a business process.

A manual adjustment must itself be a first-class ledger transaction with:

- adjustment ID;
- reason code;
- human/operator identity;
- approval evidence;
- affected accounts;
- exact amount/currency;
- related incident/ticket/reference;
- timestamp;
- immutable audit record.

For high-risk amounts, policy SHOULD support multi-party approval before the
adjustment transaction can commit.

The ledger must show both the original history and the explicit correction.

---

## 12. Migration from the Existing ATOS Account Model

Financial integrity hardening should be introduced without breaking existing
Phase 1/2 APIs.

A safe migration plan is:

### FI-0 — Specification freeze

Define:

- canonical chart of accounts;
- ledger transaction types;
- exact amount arithmetic/precision;
- canonical ledger serialization;
- transaction/hash/batch domain separation;
- Merkle construction;
- external-signature format;
- TOS anchor payload and network/domain binding;
- reconciliation and safe-mode semantics.

### FI-1 — Shadow double-entry ledger

For every existing money-changing ATOS transition, atomically append the
corresponding ledger transaction while continuing to serve the existing
projections.

The shadow ledger must initially be observational: any mismatch fails tests and
staging reconciliation before it becomes authoritative.

### FI-2 — Projection rebuild and continuous reconciliation

Implement deterministic rebuilders and compare current accounts/escrows/
earnings against ledger-derived state.

Run continuously in staging and then production with alerting.

### FI-3 — Ledger becomes Managed accounting authority

Treat current balance tables as projections. New economic code must originate
through ledger-backed transactional primitives.

Direct balance adjustment is removed from normal operational procedures.

### FI-4 — Signed immutable batches and independent retention

Add deterministic batch roots, external KMS/HSM signatures, independent
archive storage and verification tooling.

### FI-5 — TOS Network financial-integrity anchors

Anchor signed batch roots to TOS Network at a bounded cadence and ship an
independent verifier that reconstructs a batch/root from exported/restored
ledger data and compares it to the finalized TOS anchor.

The anchor path must be replay-safe and must never convert a Managed Job into a
Verified Job merely because its batch root was anchored.

---

## 13. Required Acceptance Tests

The implementation is not complete until the following classes of tests exist.

### 13.1 Ledger correctness

- balanced transaction succeeds;
- unbalanced transaction is rejected atomically;
- duplicate semantic transaction is idempotent;
- same idempotency identity with changed semantics conflicts;
- immutable economic fields cannot be updated;
- reversal is represented as a new transaction;
- projection rebuild exactly reproduces balances/escrows/provider liabilities.

### 13.2 Multi-replica PostgreSQL

Using real PostgreSQL and independent service/store instances:

- concurrent debits cannot overspend;
- duplicate settlement produces one ledger economic effect;
- concurrent payout/refund/dispute transitions conserve value;
- ledger + projection commit atomically;
- crash/restart at each durable boundary converges to one outcome.

### 13.3 Tamper detection

In an isolated test environment deliberately mutate:

- a projection row;
- a historical ledger entry;
- transaction ordering;
- a ledger sequence;
- a batch manifest/root.

Verify that reconciliation/hash/root verification detects each mutation.

### 13.4 External signature

- valid batch signature verifies;
- changed root fails verification;
- wrong key/domain fails verification;
- signing failure does not mark the batch externally finalized;
- key rotation preserves historical verification.

### 13.5 TOS anchor

Using a real TOS localnet/test environment where feasible:

- batch root anchors with stable idempotent identity;
- lost response is recovered without creating a conflicting second anchor;
- same anchor identity with changed root is rejected;
- local reconstructed root equals finalized TOS root;
- altered historical ledger produces a mismatch;
- TOS network/domain mismatch is rejected.

### 13.6 Backup and restore

- fresh database + archived WAL/base backup restores to a chosen point;
- ledger replay rebuilds projections;
- restored batch roots verify against retained signatures/TOS anchors;
- backup deletion from the application trust domain is not sufficient to
  destroy independently retained recovery evidence.

### 13.7 Financial safe mode

- reconciliation failure blocks configured money-moving operations;
- read-only investigation paths remain available as designed;
- authorized recovery exits safe mode only after invariant checks pass.

---

## 14. Operational Metrics

Production monitoring should expose privacy-safe aggregate metrics such as:

```text
ledger commit failures
ledger/projection reconciliation mismatches
unbalanced transaction attempts
last finalized ledger sequence
last signed batch sequence
last TOS-anchored batch sequence
anchor lag seconds
backup/WAL archive lag
restore-test freshness
payout reconciliation lag
financial safe-mode state
```

Metrics must not expose private prompts, account credentials, secrets, or
sensitive payment-rail data.

Alerting thresholds for integrity/anchor failures should be stricter than
ordinary availability alerts because continuing financial writes under unknown
integrity can increase loss.

---

## 15. Non-Goals

This specification does **not** require:

- putting every Managed Job on chain;
- storing prompts, source files, model outputs or private artifacts on TOS;
- turning Managed Mode into Verified Mode;
- making PostgreSQL unnecessary;
- replacing existing Phase 2 settlement/dispute state machines with blockchain
  calls;
- exposing internal ledger implementation details in ordinary Agent-facing
  APIs;
- treating a Merkle root of a private ledger as equivalent to enforceable
  TOS-backed escrow/settlement promised by `tos_verified_v1`.

---

## 16. Completion Criterion

ATOS Financial Integrity Hardening is complete when all of the following are
true:

```text
append-oriented double-entry ledger                 ✅
current balances/earnings are rebuildable projections ✅
all amount-changing Managed paths are ledger-backed ✅
immutable historical financial entries              ✅
privilege-separated runtime/migration/audit roles   ✅
continuous ledger/projection/rail reconciliation    ✅
PITR + independent immutable backup retention       ✅
deterministic financial hash chain / Merkle batches ✅
external KMS/HSM signatures                         ✅
periodic TOS Network ledger-root anchoring           ✅
independent root verifier                            ✅
financial safe mode + tested recovery procedure     ✅
real PostgreSQL multi-replica adversarial tests      ✅
real TOS anchor recovery/tamper-detection tests      ✅
```

The final security property is:

> Compromise of the normal ATOS application/database host must not allow an
> attacker to silently rewrite previously externally finalized financial
> history. Current operational state must be reconstructible from immutable
> ledger facts and independently retained evidence, and any divergence from the
> externally signed/TOS-anchored history must be detectable and actionable.
