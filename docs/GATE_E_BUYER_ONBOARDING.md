# Gate E Buyer Onboarding

## Status

The buyer SDK and wallet-budget foundation is implemented. This is not Gate E
acceptance: a fresh buyer must still complete the purchase from public
documentation with a production TOS stablecoin sender, and the same session
must include the fresh-provider sale required by the Gate.

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
- canonical Quote and escrow rules: `docs/ACCEPTED_QUOTE_TVM_V1.md` and
  `docs/STABLECOIN_ESCROW_TVM_V1.md`
- external commercial lifecycle: `docs/GATE_D_EXTERNAL_PILOT.md`

Before the buyer item can be complete, provide a production adapter that sends
the exact wallet transfer through `tosctl`, then run a fresh-buyer session with
no source edits, hidden database changes, developer-only instructions, or key
material outside custody. Record release commits, network/genesis tuple,
Capability/version, manifest digest, Quote commitment, escrow, exact asset and
amount, budget policy, funding transaction, finalized checkpoint, Receipt, and
settlement. Never record tokens, mnemonics, private keys, or wallet seeds.
