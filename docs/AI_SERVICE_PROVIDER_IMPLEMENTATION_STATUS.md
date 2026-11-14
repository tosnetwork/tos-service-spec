# TOS AI Service Provider — Implementation Status (WP-01)

**Status:** implementation and local-integration record for
[AI Service Provider Requirements V1](AI_SERVICE_PROVIDER_REQUIREMENTS_V1.md).
It is not acceptance evidence: it changes no roadmap gate, and every item below
still needs the independent, current-domain evidence that WP-07 and Gates D–G
require.

**Date:** 2026-11-14

Each row names the pull request, the exact head that was reviewed, and its merge
commit on `main`. "Reviewed" means a non-author review with each finding
re-checked against code and a follow-up review of the fixes; a merge is not a
release or a gate decision.

All four repositories build with Go 1.26.11 (standard-library advisory
GO-2026-6859): `openfox` #34, `tos-service-protocol` #45, `tos-service-gateway`
#25, `tos-ai` #13. Third-party advisories reported by `govulncheck` were fixed in
`tos-service-protocol` #46, `tos-service-gateway` #26 and `tos-ai` #14
(containerd v2.0.13, x/net v0.62.0, grpc v1.83.2, x/text and others);
`govulncheck -show verbose ./...` reports no vulnerabilities in any of the four
at those merges. The containerd upgrade has not been run against a live daemon.

## Work packages

| Work package | Pull request, reviewed head, merge | What it delivers | Verification | Review | Open follow-ups |
|---|---|---|---|---|---|
| WP-02 onboarding and publication | `tos-service-protocol` #44, `dcdd5a0`, merged `b5503e9` | Owner-private, versioned publication journal (prepared → signed → submitting → submitted → finalized → cataloged, plus ambiguous); restart never rebuilds, re-signs or relays a different action; per-record relay lock so a live relay is never taken over; pre-signing preview of every PRV-04 field with explicit unknown/absent/mismatch status; pinned actor release refused before anything is journaled | `make verify` (33 packages, conformance); restart at every phase; real SIGKILL tests inside the relay and with a live second process; 25 first-round mutations and every mutation of the review fixes killed, except one CLI-only fallback with no Gateway end-to-end test | Approved after one round of fixes (1 medium, 7 low) | No end-to-end CLI test against a Connect Gateway; transport binding, publication fee estimate and actor-owner ↔ Agent binding are shown as unknown because no resolver exists for them |
| WP-03 bounded provider execution | `tos-ai` #12, `36ed06d`, merged `3bcbd43` | `software-work-execute paid`: execution only through railgate Admit → pre-execution check → Run → Complete/Fail, distinct exit codes (completed, refused, already taken, not pending now, ambiguous, not admitted, execution failed, refused before execution, unavailable); the sandbox runs under exactly the manifest's CPU, memory, scratch, output and wall-clock limits, and out-of-range manifests are refused before admission; Receipt hash bound to the exact job and result; content-addressed artifact retention with pending records, holds and a crash-safe tombstoned sweep that always makes progress; a record cap on deadline-bearing jobs checked before paid admission; retention lock waits bounded by the deadline slack; `artifacts-gc` operator command | `make verify` on Go 1.26.11; 57 mutations killed; railgate fixtures for every status; tests re-run on the tree merged with current `main` | Approved with nits after four review rounds, including two GitHub Codex findings (manifest limits, GC at the record bound) and one regression they introduced (default-mode jobs exhausting the cap) | Default mode with `--retain-until` on a full store fails after the run (a rerun is safe); leaked pending files slow sweeps without limit; OpenFox should pass `--retain-until` so default-mode objects become collectable; no live paid run through a private containerd yet; no shared multi-worker slot store (EXE-02) |
| WP-04 public interfaces | `tos-service-gateway` #24, `1a85d36`, merged `1327c3e` | Public Native, DNS alias and discovery Connect services capped at the advertised 1 MiB (raw and decoded), 10 s body read deadline, one shared limiter for global and per-client concurrency and rate, clients keyed by the loopback TLS terminator's header (right-most `X-Forwarded-For` by default), IPv6 by /64, overflow bucket instead of refusal, bounded configuration | `make verify`; 30 mutations killed | Approved with nits after two rounds (round one blocking: every caller shared one bucket behind the terminator) | Eviction is linear in the client table while it is full (bounded); Intent Carrier still has body caps only |
| PRV-01/05/06 operator experience | `openfox` #33, `a9aae30`, merged `d8749bf` | `openfox earning service preflight`: 26 side-effect-free checks with a versioned JSON report (pins, permissions, endpoints and genesis, registry/actor/attestor state, clock skew, signer probe that cannot sign); `status` with per-request operator states derived only from finalized evidence (anything uncertain is `outcome_unknown`) and credited revenue labeled apart from wallet receipt; durable `pause`/`resume` of new admission with a separate bound for held tasks | `go test -race` of both touched packages (re-run independently); 36 mutations killed | Approved with nits after one round of fixes (1 medium, 7 low) | Withdrawal submission/finalization and wallet credit are not tracked; pausing stops local admission only, so funded calls during a pause fall to refund unless the owner changes the actor policy |
| WP-06 buyer budgets | no change needed | PAY-01's three budgets are met by existing `buyersdk` reservation: per-call maximum, outstanding calls held whatever their age, and a rolling window (24 h for a daily budget) | Code reading of `pkg/buyersdk/service_actor_journal.go` reservation rules | — | One purchase identity across more than the Agent Packet transport |

## M1 — local settlement lifecycle

Local integration evidence only: one host runs every validator and endpoint,
so none of it qualifies as public or independent acceptance. Each run boots a
fresh three-validator ML-DSA-44 network from `tos` `5af405dcb` (tosctl sha256
`6de21cb2…`, Service Actor release code hash `…d63e09428e42aa0c`) and drives
the real `tosctl agent service` and `tos-service-buyer` commands through
`tos-service-protocol` `scripts/service-actor-buyer-e2e.sh` (PR #47).

| Record | What it proves | Script commit | Result |
|---|---|---|---|
| [`local-service-actor-provider-m1-20261114.json`](../deployments/local-service-actor-provider-m1-20261114.json) | **M1 record.** `E2E_LIFECYCLE=1 E2E_EXECUTE=1` in one run, 13:33–15:37 UTC, with the checks hardened by the review of PR #47: real paid execution and its attested Receipt, rerun and failing-test controls; crash before broadcast (the buyer's whole process group killed, no request created) and after broadcast (journal resolved to `admitted`, settled once); `withdraw_revenue`; after the real one-hour deadline `expire` and `claim_refund` for the lifecycle request and for the request whose execution failed; after the real refund-claim deadline `sweep_expired_request`. Every payout is checked against its payout message value and every wallet reconciles exactly | `3eb4dd3` (clean tree; merged as `49a2571` via PR #47, whose head `95f203a` differs only in comments) | ALL PASS, 66 of 66 |
| [`local-service-actor-settlement-lifecycle-20261114.json`](../deployments/local-service-actor-settlement-lifecycle-20261114.json) | `E2E_LIFECYCLE=1`, 09:47–11:50 UTC: crash before broadcast (no request, quarantined as ambiguous, never re-sent, no funds moved); crash after broadcast (one finalized call resolved, never re-sent, settled once); `withdraw_revenue`; after the real one-hour deadline `expire` then `claim_refund` (price returned, storage fee credited to the provider); after the real refund-claim deadline `sweep_expired_request` (the payout message carries exactly the price, the provider is credited storage fee less bounty, the sweeper receives the bounty) | `8e6e50f` | ALL PASS, 38 of 38 |
| [`local-service-actor-paid-execution-20261114.json`](../deployments/local-service-actor-paid-execution-20261114.json) | `E2E_EXECUTE=1`: the provider runs `software-work-execute paid` (tos-ai `3bcbd43`, executor sha256 `26801be5…`) against the private containerd with the frozen image `sha256:9624bca7…`; railgate admits the finalized request, the buyer's Go module is tested in the sandbox, the attestor's check anchors every Receipt binding to the finalized request snapshot, and the buyer resolves exactly that Receipt hash; reruns while pending and after respond are refused with the slot and journal unchanged; a failing test ends `execution_failed` and is never responded; every wallet involved reconciles exactly | `ef3c03c` (clean tree) | ALL PASS, 37 of 37 |

The two earlier records are kept as supporting runs: the settlement-lifecycle
record predates the review of PR #47, whose fixes replaced its bounded refund
and withdrawal checks with exact payout-message checks and made the
crash-before-broadcast case kill the whole buyer process group; the
paid-execution record covers the execution phase alone. A combined run at
`f97420b`, before those fixes, also caught a test-ordering defect (the
failed-execution refund was attempted after its refund window had closed,
which the contract correctly refused), fixed in `3eb4dd3` before the M1 record.

The private containerd host deployment used for these runs was installed from
`tos-ai` `deploy/provider` and surfaced three defects that are fixed in
`tos-ai` #15 (socket mode, layer-root permissions under the unit umask, and
the digest-qualified image name); the live backend conformance suite now passes
on containerd v2.0.13.

## Not delivered by these changes

- WP-07 independent commercial acceptance: a provider and buyer outside the
  core team, independent resolution, and Gate D/E submission.
- WP-08 inference profile and adapters: locked until the expansion gate opens.
- A live paid run through the private containerd deployment of `tos-ai`.
- Gate F/G operation, independent operators, and production controls.
