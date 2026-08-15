# Gate E Buyer Onboarding

## Status

The buyer SDK, wallet-budget foundation, and production `tosctl` stablecoin
sender are implemented. This is not Gate E acceptance: a fresh buyer must
still complete the purchase from public documentation, and the same session
must include the fresh-provider sale required by the Gate.

A same-host three-validator rehearsal has additionally funded a new escrow
from a `tosctl`-native V1R3 wc=0 buyer. It verified the exact signed-message
prepare/broadcast boundary and the post-payment escrow and stablecoin-wallet
state with three agreeing endpoints. The record is
`deployments/local-gate-e-tosctl-buyer-funding-2026-08-15.json`. This is
implementation evidence only: it did not exercise the complete public buyer
SDK session or establish external operator independence.

The production asset read no longer requires a caller-supplied balance view.
`tos-protocol/pkg/toschain.StablecoinResolver` authenticates the master code,
extracts and verifies its wallet-code preimage, derives the buyer wallet, and
checks the wallet code, owner, master, unlocked status, balance, genesis, and
monotonic finalized checkpoint through strict-majority TOS RPC. Its local live
result is included in the same deployment record.

The complete buyer preflight was also run against that live state through the
production SDK and the in-process `toschain.DirectNativeClient`. It resolved
the finalized Capability directly from the three TOS nodes, reproduced the
manifest digest, Quote commitment, deterministic escrow and buyer stablecoin
wallet, and accepted the exact finalized funded amount at checkpoint `143512`.
Because the escrow was already funded, this was deliberately a read-only
idempotency check and caused no second wallet broadcast. It closes the
integration gap between the production resolvers and Buyer SDK, but it is not
the required fresh-buyer onboarding session.

## Authority and custody boundary

- a Quote Proposal is discovery input and is never canonical;
- the buyer independently verifies the manifest and finalized typed Capability;
- the Accepted Quote becomes canonical only through the exact TOS escrow;
- the exact TOS-network stablecoin master and wallet code hash identify the
  payment asset; a ticker or gateway balance is insufficient;
- escrow deployment is finalized before any stablecoin funding attempt;
- the wallet signer remains behind the reviewed `tosctl` custody boundary;
- gateway, resolver, and sender responses are transport observations only; and
- payment success means finalized escrow state contains the exact funded amount.

## Buyer sequence

1. Create an owner-private `0700` budget directory and choose explicit window,
   purchase-count, per-purchase, and total atomic-unit limits.
2. Obtain a Quote Proposal and retrieve the manifest independently by its
   digest. Use `tos-protocol/pkg/buyersdk` to strictly decode the manifest and
   verify the exact finalized Capability version and provider ownership.
3. Resolve the quoted TOS stablecoin through finalized TOS state. Verify its
   master identity, wallet code, buyer wallet, balance, and checkpoint.
4. Build the exact Accepted Quote and deterministic escrow. Review the buyer,
   provider, amount, asset, deadlines, execution signer, transport commitment,
   Quote commitment, and escrow address.
5. Deploy the reviewed StateInit through the buyer custody boundary. Wait for
   the exact code hash and data to be finalized in `awaiting_funding` state.
6. Call `FundPurchase` with a durable retry key. Immediately before wallet use,
   the SDK reconstructs every commitment and repeats all authoritative reads.
   The production sender asks `tosctl` to build and sign once, validates the
   exact signed BOC before acquiring the broadcast lease, and then broadcasts
   those same bytes without rebuilding or re-signing.
7. Treat the stablecoin sender result as ambiguous until the exact escrow and
   amount are finalized. Continue to Receipt and settlement only from that
   finalized funded state.

## Crash and budget rules

The durable purchase record contains the network, escrow, Quote commitment,
exact asset, buyer wallet, amount, and deterministic query ID. One atomic claim
both reserves budget and records the full intent. Only `prepared` can acquire a
single broadcast lease. A pre-send crash is recoverable; a crash or error after
the record reaches `broadcasting` is read-only recovery and cannot trigger an
automatic second payment. Request keys are retry aliases and do not define the
payment identity.

Budget records are owner-only regular files and are counted for the entire
configured window, including unresolved reservations. Operators must not
delete, weaken, or edit the journal to recover capacity. Ambiguous entries are
reconciled against finalized chain history under an explicit operational
procedure.

## Current implementation and remaining acceptance

- buyer safety boundary: `tos-protocol/pkg/buyersdk`
- Go guide: `tos-protocol/docs/buyer-sdk.md`
- exact prepared-message broadcast boundary: `tos` commit
  `d9d725534cb1a9120b1e49854b360c01f043c22a`
- production `tosctl` funding adapter: `tos-protocol` commit
  `d1a845eb7808365a413106d075c7c6316be67e27`
- production finalized stablecoin resolver: `tos-protocol` commit
  `57f6429f2a0dc21b3292de8a27fa5d3a26255dd4`
- direct finalized Native SDK adapter and full live Buyer SDK revalidation:
  `tos-protocol` commit `a18162af3df971af265bf101ae9d40396e3c1370`
- verified test-fixture custody import and exact-message submit CLI: `tos`
  commit `c8fbead6851cf63c4858035195045b4de0406302`
- canonical Quote and escrow rules: `docs/ACCEPTED_QUOTE_TVM_V1.md` and
  `docs/STABLECOIN_ESCROW_TVM_V1.md`
- external commercial lifecycle: `docs/GATE_D_EXTERNAL_PILOT.md`

Before the buyer item can be complete, run a fresh-buyer session with no source
edits, hidden database changes, developer-only instructions, or key material
outside custody. Record release commits, network/genesis tuple,
Capability/version, manifest digest, Quote commitment, escrow, exact asset and
amount, budget policy, funding transaction, finalized checkpoint, Receipt, and
settlement. Never record tokens, mnemonics, private keys, or wallet seeds.
