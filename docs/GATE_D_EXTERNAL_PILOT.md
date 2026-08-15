# Gate D External Pilot

## Purpose

This runbook closes the only remaining Gate D acceptance condition. The local
public-testnet transaction proves that the implementation works; it does not
prove that unrelated parties can use it. Gate D is accepted only after one
buyer outside the core development team pays one independently operated
provider and a third party reconstructs the result from finalized TOS state.

The three roles must not share private keys, a gateway database, a filesystem,
or an operator-controlled source of protocol truth. One organization may not
claim multiple roles under different test identities.

## Required roles

1. The provider generates and retains its Agent controller and execution
   signer keys, publishes the software-work Capability, runs the pinned
   executor, and returns the immutable artifact, report, and Receipt.
2. The buyer generates and retains its wallet and Agent keys, independently
   resolves the Capability and Quote terms, funds the escrow with the exact
   TOS-network stablecoin, checks the returned objects, and authorizes release.
3. The verifier uses independently operated HTTPS JSON-RPC endpoints and a
   clean checkout to reconstruct the Capability, Accepted Quote, escrow,
   Receipt, settlement transaction, and provider-wallet credit.

All test identities must be freshly generated through `tosctl` or another
reviewed Ed25519 custody boundary. The plaintext identities under
`test-vectors/` are local test fixtures and are forbidden in the external
pilot. No seed, mnemonic, private key, vault export, or signing credential may
appear in the evidence bundle.

## Frozen profile

The pilot uses only the V1 software-work profile:

- canonical manifest and Accepted Quote encodings from this repository;
- one exact TOS-network stablecoin master and wallet-code hash;
- fixed-price full release or timeout refund;
- the pinned OCI image and fail-closed containerd isolation policy;
- canonical Receipt and settlement-intent cells; and
- finalized TOS state as the sole payment authority.

Changing the provider Agent, execution signer, endpoint, price, buyer, or
deadline requires a newly encoded Quote and a newly derived escrow StateInit.
Editing a gateway record is never a substitute.

## Execution sequence

1. Record the network ID, genesis hashes, release commits, Registry code hash,
   stablecoin identity, and independently operated endpoint URLs.
2. The provider registers its Agent and Capability, then publishes the exact
   manifest and content digests. The buyer and verifier independently resolve
   the finalized version before payment.
3. The buyer and provider agree on a non-canonical Quote Proposal. Both inspect
   the complete typed Accepted Quote before its escrow StateInit is deployed.
4. The buyer funds the derived escrow wallet with the exact quoted amount.
   Both parties resolve the funded state before execution begins.
5. The provider executes the bound source under the pinned image and retains
   the content-addressed artifact and report. A crash-ambiguous execution is
   not retried under the same execution ID.
6. The execution signer signs only the displayed settlement-intent hash. The
   escrow validates the full Receipt and initiates the stablecoin transfer.
7. The verifier waits for finality and runs the strict evidence checker from a
   clean environment. It must obtain a quorum without a private gateway
   database or files supplied by the gateway.

### Custody-safe Receipt signing

The Receipt tool is deliberately two-stage and never reads a private key. The
provider first builds the canonical Receipt and settlement payload:

```bash
native-receipt-release \
  --outcome OUTCOME.json \
  --quote-vector ACCEPTED_QUOTE.json \
  --escrow ESCROW_ADDRESS \
  --query-id NON_ZERO_RELEASE_QUERY_ID \
  > settlement-prepare.json
```

After inspecting the Receipt, Quote, escrow, amount, query ID, and displayed
execution-signer public key, sign the exact 32-byte payload inside the `tosctl`
vault boundary:

```bash
jq -r .signing_payload_hex settlement-prepare.json \
  | xxd -r -p > settlement-payload.bin
tosctl wallet sign \
  --name EXECUTION_SIGNER_WALLET \
  --message-file settlement-payload.bin \
  > settlement-signature.json
```

Finalize the release body only after the tool verifies that the `tosctl`
signature JSON contains the exact Quote-bound public key and payload:

```bash
native-receipt-release \
  --outcome OUTCOME.json \
  --quote-vector ACCEPTED_QUOTE.json \
  --escrow ESCROW_ADDRESS \
  --query-id NON_ZERO_RELEASE_QUERY_ID \
  --signature-file settlement-signature.json \
  > settlement-release.json
```

The provider must compare the unsigned and signed outputs before broadcasting.
The signing payload is public, but the private key, mnemonic, and vault export
must never be passed to `native-receipt-release`, the gateway, or the buyer.

## Independent verification

Run the verifier with the Python environment frozen by `tos/test/tostester`.
Every placeholder is supplied by the independent parties' pilot, not copied
from the local rehearsal:

```bash
uv run --project test/tostester python \
  scripts/atos-software-work-paid-evidence.py \
  --outcome OUTCOME.json \
  --release RELEASE.json \
  --quote-vector ACCEPTED_QUOTE.json \
  --artifact-root CONTENT_ADDRESSED_OBJECTS \
  --escrow ESCROW_ADDRESS \
  --buyer-wallet BUYER_STABLECOIN_WALLET \
  --provider-wallet PROVIDER_STABLECOIN_WALLET \
  --endpoint https://operator-a.example/jsonRPC \
  --endpoint https://operator-b.example/jsonRPC \
  --endpoint https://operator-c.example/jsonRPC \
  --quorum 2 \
  --funding-query-id NON_ZERO_QUERY_ID \
  --funded-checkpoint FINALIZED_PRE_RELEASE_CHECKPOINT \
  --evidence paid-software-work-evidence.json
```

The checker fails closed unless it can:

- decode the canonical Receipt and match every field to the Quote and outcome;
- rehash the Receipt BOC, artifact, and report;
- match the report to the execution result;
- obtain the required endpoint quorum at one finalized checkpoint;
- prove the escrow was funded but unsettled at the supplied finalized
  pre-release checkpoint;
- match funded and settled amounts to the exact Quote and prove that the
  provider-wallet balance increased by that amount between the funded and
  settlement checkpoints;
- match the on-chain Receipt commitment and release query ID; and
- derive escrow and provider-wallet transaction identities from endpoint
  responses.

The verifier must separately record the legal or organizational operator of
each endpoint. Multiple URLs, processes, containers, or hosts controlled by
one operator do not establish independence.

## Acceptance record

The final immutable record must include participant declarations, release
commits, network and contract identities, the canonical Quote and Receipt,
content-addressed objects, endpoint observations, transaction identities, and
the strict verifier output. Each participant signs the digest of that record
with the public key declared for its role.

Mark Gate D accepted only when all three parties confirm the same record and
the verifier returns `PASS_INDEPENDENT_PAID_SOFTWARE_WORK_SETTLEMENT`. Any
missing object, ambiguous chain outcome, endpoint quorum failure, or private
gateway dependency leaves Gate D open.
