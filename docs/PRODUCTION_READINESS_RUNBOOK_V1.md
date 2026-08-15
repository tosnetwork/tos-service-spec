# ATOS Production Readiness Runbook V1

This runbook defines the minimum operational controls for a production Native
deployment. It does not grant a Gateway semantic authority: finalized TOS
state, quorum evidence, and contract code identity remain canonical.

## Key custody and spending

- Registry controller keys, buyer keys, provider keys, and relayer fee-payer
  keys are separate identities and separate custody domains.
- Private keys never enter Gateway, resolver, worker, or CI processes. Signing
  occurs through the reviewed `tosctl` custody boundary and produces an exact
  message package before broadcast.
- Relayers use owner-private journals, atomic state-slot claims, per-target and
  per-wallet action limits, and bounded native-TOS fee budgets. A budget breach
  fails closed and requires an operator-approved policy change.
- Recovery requires a second operator-controlled backup of encrypted key
  material, a tested restore ceremony, and revocation of the old key before
  resuming spend.

## Endpoint and finality incidents

Every resolver records network tuple, Registry/Escrow code hash, quorum,
checkpoint, transaction reference, and typed state hash. Operators must:

1. stop mutations when quorum falls below strict majority;
2. isolate an endpoint that disagrees on network, code, checkpoint, or state;
3. never lower quorum or roll back a durable checkpoint to restore service;
4. retain the conflicting response and endpoint identity for forensics; and
5. resume only after two consecutive finalized observations agree and the
   incident record is signed by the operator.

Gateway outage is handled by portable inputs and another Gateway. It never
permits replacement of an Accepted Quote, Receipt, escrow, or finalized state.

## Monitoring and alerts

Monitor and retain immutable, timestamped records for:

- contract code hash and StateInit identity;
- network genesis tuple and finalized checkpoint monotonicity;
- quorum vote count and endpoint divergence;
- relay journal phase, state-slot conflicts, broadcast leases, and spend
  totals;
- escrow status, funded/settled amounts, Receipt commitment, and pending query;
- stablecoin master/wallet code hashes, owner, balances, and wallet derivation;
- gateway availability, request bounds, error/retry disposition, and latency;
- provider execution count, artifact/report digest, and Receipt binding; and
- storage growth, artifact retention, and failed authentication/rate limits.

Alerts are severity-bounded: a canonical-state or quorum mismatch is a stop-
the-line incident; transport unavailability is isolated and retried only per
the public retry disposition.

## Stablecoin accounting and fee reconciliation

Reconcile each completed purchase from finalized state, never from Gateway
ledgers: buyer debit, escrow funding, escrow settlement/refund, provider credit,
and native-TOS service/relay fees are separate columns. A reconciliation report
must include asset master and wallet code hashes, decimals, transaction hashes,
logical times, checkpoint, and exact atomic amounts. Any unexplained delta
freezes further spending for that wallet.

## Release and rollback

Each release publishes a signed manifest containing repository commits, toolchain
version, source digest, generated contract BOC digest/code hash, dependency
lock data, tests, and deployment configuration schema. Two clean builds must
match byte-for-byte. Rollback may change transport binaries only; it may not
change a frozen contract code hash or reinterpret finalized state.

## Degraded and emergency procedures

- **Quorum loss:** stop relay and settlement broadcasts; retain read-only
  resolution only when its freshness policy permits.
- **Endpoint disagreement:** quarantine the outlier, preserve evidence, and
  require operator review; never majority-switch code identity.
- **Relayer compromise:** disable the wallet, stop its process, preserve the
  journal, rotate custody, and resolve every outstanding slot before recovery.
- **Gateway compromise:** revoke transport credentials and redeploy from a
  signed artifact; canonical chain state and owner-held journals remain valid.
- **Provider failure:** do not fabricate a Receipt; follow escrow timeout or
  objective refund rules from finalized state.
- **Artifact/storage loss:** recover by content digest from an independent
  store; a mismatched byte sequence is invalid and must not be substituted.

Every incident ends with a signed timeline, affected checkpoints and objects,
operator decisions, recovered balances, and an explicit statement of whether
any canonical state was changed.

## Acceptance evidence

Gate G acceptance additionally requires a multi-operator exercise that executes
the Gate D/F lifecycle while injecting gateway failure, provider failure,
endpoint disagreement, refund, key recovery, storage loss, and budget limits.
This document is the operational baseline; it is not evidence that those
external exercises have occurred.

`deployments/production-readiness-evidence.template.json` fixes the machine-
readable evidence shape. It must remain a template until every `REQUIRED`
field is replaced, two reproducible builds match, and each operator signs the
multi-operator exercise record.

Before publication, run
`python3 scripts/verify-production-readiness-evidence.py <evidence.json>`.
The validator intentionally rejects the template and any record that lacks a
strict-majority diverse endpoint set, all operational drills, reproducible
build proof, or three operator signatures.
