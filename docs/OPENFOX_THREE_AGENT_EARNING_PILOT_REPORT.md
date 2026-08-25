<!-- markdownlint-disable MD013 -->

# OpenFox Three-Agent Earning Pilot Report

Status: completed controlled pilot on 2026-08-25

## 1. Executive result

Three isolated OpenFox seller identities published owner-bounded service offers through two Carrier implementations, completed one paid job each, and received Agreement-bound native TOS payments finalized by the local three-node network.

The controlled seller transaction path passed. The pilot does **not** establish production readiness or prove fully autonomous customer acquisition: the buyer was a deterministic test principal, Agreement negotiation was driven by the test coordinator instead of a live Messenger conversation, both Carriers ran on one host under one operator, and the funds were local-network test TOS.

## 2. Repository heads used

The autonomous-earning feature branches were merged to each repository's `main` branch in dependency order.

| Order | Repository | Tested `main` commit |
| ---: | --- | --- |
| 1 | `tos-service-spec` | `471a8657451ab1fa1834e1abbe2a08c0f5bdbf0a` |
| 2 | `tos-service-protocol` | `0cd6b53f2c35b29779f68c131389a2f52d778927` |
| 3 | `tos` | `4b31f720a121be5c936012f40b89ffee1c693507` |
| 4 | `tos-messenger` | `7c5759f44d7196e5f1304e243a0772c2e95eb33e` |
| 5 | `tos-service-gateway` | `f99830900e348478e4023f2db8dc3b52344de5ef` |
| 6 | `tos-ai` | `ff7607d532b4530d6e900ffdfd46a0808caffa90` |
| 7 | `openfox` | `0cafc1c14d9478edeb65a6a281939e244b5538c0` |

## 3. Deployed topology

Two Carrier processes remained active after the pilot:

| Carrier | Implementation | Endpoint | State store |
| --- | --- | --- | --- |
| `carrier:gateway-local-pilot` | gateway Carrier | `http://127.0.0.1:18191/v1/intents` | isolated gateway store |
| `carrier:messenger-local-pilot` | Messenger Carrier | `http://127.0.0.1:18192/v1/intents` | isolated Messenger journal |

They use distinct implementations, processes, ports, and stores. Because they share a host and operator, they are not independent production failure domains and do not satisfy a production two-operator resilience claim.

Three OpenFox configurations used separate Agent, owner, authority, identity-key, state, workspace, and seller-account boundaries:

| Role | Agent | AI kernel | Offered skill | Price |
| --- | --- | --- | --- | ---: |
| Security auditor | `agent:security-auditor` | Claude Code local personal subscription | secure code review | 500,000 nanotos |
| Software builder | `agent:software-builder` | Codex app-server with a ChatGPT local personal subscription | bounded code implementation | 750,000 nanotos |
| Evidence verifier | `agent:evidence-verifier` | Codex app-server with a ChatGPT local personal subscription | release-evidence verification | 200,000 nanotos |

Persistent deployment configurations remain publication-only and fail closed for contact, Agreement, execution, and payment. The controlled pilot enabled those later stages only inside the exact test coordinator after it created typed Agreement authorization evidence. This prevents the demonstration configuration from becoming an unattended payment-capable production deployment.

## 4. Executed lifecycle

Each job exercised this sequence:

```text
owner-bounded capability and offer policy
-> AI-drafted signed Intent
-> publication to both Carriers
-> canonical Agreement body
-> typed buyer and provider authorization evidence
-> provider exposure reservation
-> one-shot local Execution Gate
-> subscription-backed LLM deliverable
-> delivery evidence
-> billing obligation
-> Agreement-bound TOS payment authorization
-> exact signed transfer
-> 2-of-3-or-better finalized RPC evidence
-> provider reconciliation to SETTLED
```

All three nodes returned the same transaction hash, logical time, and timestamp for each payment.

## 5. Financial report

All amounts below are exact Agreement payment amounts. Seller balances began at 0.5 test TOS. The displayed ending balances are rounded by `tosctl`; custody journals retain exact nanotos values.

| Seller | Gross revenue | Maximum internal cost reserve | Projected net | Payment transaction | Final state |
| --- | ---: | ---: | ---: | --- | --- |
| Security auditor | 500,000 nanotos | 80,000 nanotos | 420,000 nanotos | `sha256:e7b7ca7276f60981360c65890429a1eb80f89a4638ee4ca6f7dbb202937417d6` | `settled` |
| Software builder | 750,000 nanotos | 150,000 nanotos | 600,000 nanotos | `sha256:558df1df31ecd61c317f56250ba283021d28e7693a10cf5604494ede6e7ed84f` | `settled` |
| Evidence verifier | 200,000 nanotos | 30,000 nanotos | 170,000 nanotos | `sha256:e5014f474dc0ebed2f58da5070012c756d52126a40ed55819a8087cba37ccaaf` | `settled` |
| **Total** | **1,450,000 nanotos (0.00145 TOS)** | **260,000 nanotos** | **1,190,000 nanotos (0.00119 TOS)** | 3 finalized transfers | 3 settled jobs |

`maximum internal cost reserve` is an owner policy estimate used for admission and projected profit. A personal AI subscription does not expose a per-job invoice, so it must not be reported as measured cash expense.

## 6. Deliverable and user-experience review

### Security auditor

The output identified silent truncation, stale destination bytes, secret lifetime, missing validation, and constant-time handling concerns, then proposed safer APIs. The substance was useful and severity-ranked.

The first output also contained unwanted planning-mode narration. Root cause was the CLI `plan` permission mode: tools were empty and side effects remained impossible, but the hidden planning context leaked into the deliverable. OpenFox now uses the default permission mode with an empty tool set, safe mode, empty setting sources, a sterile workspace, no session persistence, and native tools disabled. A real subscription-backed exact-response integration test passed after this change.

### Software builder

The output contained a self-contained Go implementation and table-driven tests. It handled ASCII trimming, ASCII lowercasing, the 32-byte bound, invalid characters, and error cases. The artifact was directly usable after normal human review.

### Evidence verifier

The output failed the release claim because the input contained assertions rather than attached proof artifacts and explicitly lacked an artifact digest and reproducible build command. This is intentionally conservative. A production user experience should present the verifier with signed evidence bundles, not prose claims, so it can distinguish “claimed passed” from “cryptographically or independently evidenced passed.”

### Operator experience

Positive observations:

- One generic Intent format represented all three service types; no industry-specific opcode or contract was added.
- Owner offer policies bounded asset, unit, price, cost, taxonomy, keywords, settlement Adapter, and TTL while leaving description generation to AI.
- Signed publications were locally inspectable and searchable through both Carriers.
- Agreement, execution, payment, and accounting IDs were content-bound and recoverable.
- Seller receipts appeared in their separate Agent Accounts after three-node finality.

Friction and fixes discovered during the pilot:

- Capability Inventory alone did not authorize an AI to invent a price. A typed owner offer envelope was added.
- Initial prices exceeded the provider portfolio limits. Pilot prices were reduced instead of weakening the limits.
- A withdrawal crash exposed a journal-before-side-effect ordering bug. OpenFox now persists the exact signed tombstone first, reuses the same bytes on retry, initializes legacy maps, and can recover an older signed tombstone from Carrier operation streams.
- The initial payment expiry exceeded the Agent Account task timeout. Agreement and obligation validity windows are now constrained below that on-chain policy bound.
- Agreement participants are canonically sorted before digest construction.
- Failed aggregate test execution can resume only selected unfinished roles, avoiding duplicate payment during recovery.

## 7. Evidence locations

Local pilot root:

```text
/home/tomi/.local/share/openfox-autonomous-earning-pilot-20260825
```

Consolidated machine-readable financial report:

```text
/home/tomi/.local/share/openfox-autonomous-earning-pilot-20260825/reports/consolidated-financial-report.json
```

The local evidence includes Agent configurations, signed publication journals, two Carrier stores, one-shot Execution Gate journals, content-addressed deliverables, payer custody journals, and the completed evidence-verifier report. Tokens and private keys are owner-only files and are intentionally not copied into this repository.

## 8. Acceptance boundary and next gate

This pilot proves that three isolated OpenFox seller identities can advertise generic skills, execute controlled accepted work with two subscription-backed AI integrations, and receive reconciled local TOS revenue.

It does not yet prove the complete unattended business loop. The next acceptance campaign must add:

1. a live buyer OpenFox that discovers the offers from Carrier data rather than test fixtures;
2. typed proposal and acceptance exchange over a real Messenger transport;
3. two Carrier operators on independent hosts and storage failure domains;
4. source-loss recovery after deleting one Carrier database;
5. long-running scheduling, renewal, cancellation, dispute, and crash/takeover campaigns;
6. external-value settlement only after separate legal, custody, and production security approval.

Until those gates pass, the accurate claim is **controlled autonomous seller execution and local-network earning**, not fully autonomous production income.
