# OpenFox Agent Gifts V1: first-principles account decision

**Status:** architecture decision; the corresponding normative edits in
`OPENFOX_AGENT_GIFTS_V1.md` replace its former Wallet V5R1 sender profile

**Scope:** native TOS gifts in an existing authenticated direct E2EE
conversation. This decision does not add a Gift contract, registry, recipient
profile, delegation, ticket, escrow, stablecoin, room Gift, or service-payment
semantics.

## 1. Decision

An OpenFox Agent has one automatic-spending account: its deployed TOS Agent
Account. Agent Gifts use that account. They do not create or fund a second
dedicated Wallet V5R1 Gift wallet.

The ordinary Wallet V5R1 held in a `tosctl agent wallet` profile remains the
owner and recovery wallet. It deploys the Agent Account, changes its policy,
rotates its controller, and can fund or recover it. It is not the normal Gift
sender.

The current pre-release Agent Account `task_send` wire form is replaced because
it does not bind the TOS network/global ID in its signed request and always
forwards a referenced body cell. TOS and OpenFox have no production deployment
or real user requiring compatibility. There is one supported Agent Account
contract, one code hash, one parser, and one custody path; no parallel version pair,
migration mode, or legacy opcode acceptance is retained.

The final Agent Account interface has generic operations, not Gift operations:

```text
agent_task_send
agent_native_send
agent_cancel_seqno
```

No operation contains a Gift ID, AgentID, alias, conversation ID, greeting,
memo, or comment. Only `agent_task_send` carries its generic referenced task
body; `agent_native_send` and `agent_cancel_seqno` contain no application
payload. Other protocols may use the same generic native-send profile.

## 2. First-principles derivation

### 2.1 Assets have one owner-visible location

Creating a second Gift-only wallet fragments balances, recovery, backup,
funding, policy, and operator understanding. It also lets an implementation
bypass the Agent Account's on-chain controller limits. The default must be the
existing account the operator understands as the Agent's automatic-spending
account.

### 2.2 Conversation identity, spending authority, and destination authority
are different

- The authenticated direct Messenger session establishes which Agent sent an
  E2EE application event.
- B's intent-bound address response selects the destination. It does not prove
  destination-key ownership.
- A's owner policy or explicit approval permits the spend.
- A's Agent Account controller signature authorizes the exact on-chain action,
  subject to the account's finalized policy and sequence.
- Finalized chain execution and exact destination credit establish payment.

No one authority substitutes for another. In particular, a Native AgentID
record is not currently an Agent Account binding, and this design does not
pretend that it is. The owner-private `tosctl` Agent Wallet profile is the sole
local source of A's Agent Account address. OpenFox receives only a bounded,
verified projection; it has no independently editable address copy. The address
is shown during authorization, committed by the signed BOC, and carried in the
authenticated Gift request. B learns which account A offers to pay from; B does
not infer it from an alias, model, Relay, Gateway, or profile text.

### 2.3 A transferable signed BOC must be self-contained and narrow

B receives immutable authorization that it may submit but cannot modify. A
conforming BOC has one external message to the exact Agent Account, one generic
native send, one destination, one amount, one sequence, one expiry, and no
application payload. The parser reconstructs all semantics without trusting
the builder.

### 2.4 Finality, not intent or submission, is payment

Funds remain unlocked until execution. Chat acknowledgements, node
acknowledgements, mempool observations, transaction hashes, local time, balance
snapshots, and successful sender execution without exact destination credit do
not establish payment.

## 3. Account and identity model

```text
Native AgentID
  identity and controller policy in the Native Registry
  no implicit wallet-address authority

authenticated Messenger direct conversation
  proves the E2EE event participants

tosctl Agent Wallet profile (owner-private local configuration)
  owner Wallet V5R1 key
  Agent Account controller key held behind custody
  deployed Agent Account address
  off-chain approval, rolling-limit, and one-active-action journal

Agent Account (on chain)
  owner address
  controller public key
  controller epoch
  seqno
  max-per-action and daily native-TOS limits
  generic task-send, native-send, and sequence-cancel operations
```

The Gift flow fails closed unless the local profile, finalized Agent Account
address, pinned code hash, owner, controller public key, actual chain global ID,
immutable nonzero deployment ID, controller epoch, policy, seqno, and balance all agree.

## 4. Final Agent Account wire profile

The exact opcodes, code hash, cell encodings, error codes, and BOC vectors are
frozen in G0 before signing is enabled. The semantic preimage is:

```text
AgentNativeSend {
  opcode
  network_global_id: int32
  controller_epoch: uint64
  seqno: uint32
  valid_until: uint32
  destination: MsgAddressInt
  amount_atomic: Grams
}

AgentCancelSeqno {
  opcode
  network_global_id: int32
  controller_epoch: uint64
  seqno: uint32
  valid_until: uint32
}
```

The frozen single-cell signed body permits
`1 <= amount_atomic <= 2^48 - 1` (`281474976710655` nanoTOS). Policy creation,
Gift canonical validation, and both controller payload builders reject larger
values before a custody claim is acquired.

`agent_task_send` is retained for task-contract calls, but its pre-release
encoding is replaced and also carries `network_global_id`. Only that operation
may carry a referenced task body. Gift verification rejects it.

The controller signs a hash domain-bound to:

```text
agent-account signature domain
network_global_id
exact Agent Account address
exact canonical payload hash
```

Account data contains an immutable random `deployment_id:uint256`, generated
by `tosctl` at creation and exposed by the finalized data getter. It is part of
the account's StateInit/address and is never mutated by policy or controller
operations. Gift preparation and finality bind this value. The supported
`tosctl agent-account deploy --new-generation` replacement flow refuses an
active or frozen predecessor, waits until outstanding controller signatures
have expired, retires its custody records, and
persists a fresh deployment ID/address after owner confirmation but before
broadcast. Reusing an identical StateInit outside that flow is prohibited: the
chain cannot distinguish it from the old generation, while custody's durable
epoch/sequence high-water mark treats the resulting rollback as recovery and
fails closed.

The contract executes TVM `GLOBALID` and compares it directly with the signed
`network_global_id` before checking the signature, sequence, expiry, and policy.
Custody and recipient verification independently obtain the connected chain's
global ID from pinned genesis and finalized configuration and require the same
value. Agreement with local configuration alone is never sufficient.
The contract also enforces
`now < valid_until <= now + default_task_timeout`. Every signed payload carries
the exact on-chain `controller_epoch:uint64`. Rotating the controller increments
both the epoch and `seqno`; restoring an old key cannot revive a signature from
that key's retired epoch even if a future sequence was pre-signed.

The account's native value limits do not account for token or contract-defined
assets reachable through the generic `agent_task_send` body. Gift never uses
that operation. Operators must not interpret the native-TOS daily limit as a
general token allowance or keep such assets under this controller without
independent callee-side policy.

`agent_native_send` attempts exactly one internal message with:

```text
IHR disabled
bounce false
destination = signed destination
value = signed amount_atomic
send mode = 3 (pay fees separately and ignore action error)
StateInit absent
body absent, canonically encoded as the inline-empty `Either` branch
no extra currencies
```

Mode 3 prevents a recipient holding an insufficient-balance BOC from repeatedly
charging accepted-message gas while leaving the sequence unchanged. If the
send action cannot be created, the finalized transaction still consumes the
sequence but produces no destination credit and resolves to
`invalidated-unpaid`, never paid. The contract conservatively commits the
attempted amount to `spent_today` even when the mode-3 output action fails.

`agent_cancel_seqno` increments the same sequence without emitting an
internal message. It requires separate owner authorization in custody. It is a
generic stale-authorization invalidation mechanism and carries no Gift data.

Both operations reject trailing bits, trailing references, unknown fields,
expired requests, wrong network, wrong sequence, and non-canonical addresses;
native-send additionally rejects zero or unrepresentable amounts. The account
remains a standard TVM account but is not mislabeled as Wallet V5R1.

## 5. Custody and owner authorization

OpenFox never holds the owner or controller private key. A hardened `tosctl`
custody boundary owns the controller signer and one process-independent durable
journal for every Agent Account action, including non-Gift actions.

Before signing, custody durably records:

- the exact authenticated Gift request and address-response digests;
- the owner-policy or explicit-approval digest;
- finalized account code, owner, controller, network, policy, seqno, balance,
  and checkpoint;
- destination, amount, fee reserve, and validity;
- the unsigned transfer digest; and
- a claim on the exact account sequence.

The sequence claim is shared by all users of the controller, not merely the
Gift subsystem. At most one primary signed action may be active for one Agent
Account sequence. An exact retry returns the same persisted BOC. A semantic
change is a conflict. Custody may additionally sign at most one separately
owner-authorized cancellation for that primary action and records both exact
BOCs as a finalized-state-resolved race.

This requires an enforceable `tosctl` architecture change: the Agent Account
controller vault key is non-extractable and is not accepted by raw-hash,
ordinary-wallet, or unjournaled task-send commands. Every controller operation,
including task actions, enters through the same account journal and policy
engine. Pre-release direct signing command paths are removed, not merely
discouraged.

Owner authorization independently displays A, B, network, amount, exact
destination, Agent Account, owner wallet, controller key ID, seqno,
`valid_until`, fee reserve, request/response digests, and the warning that funds
are not locked. Standing policy may authorize within exact bounds; otherwise a
one-shot explicit approval is required.

## 6. Gift flow

1. A resolves B once and selects an existing authenticated direct conversation.
2. A generates a fresh random 256-bit intent outside the model.
3. A sends an E2EE request committing A's configured Agent Account address,
   network, participants, amount, and requested expiry.
4. B returns an intent-bound native TOS address. By default this is B's
   finalized Agent Account address, but B may choose another local-custody
   native address. The E2EE response, not the address type, is destination
   authority.
5. A obtains owner authorization. Custody resolves finalized Agent Account
   state, claims its sequence, builds, signs, and fsyncs the exact BOC.
6. A sends the unchanged BOC through generic padded E2EE application data.
7. B independently parses the BOC and resolves the exact finalized Agent
   Account code, controller, network, policy, sequence, and balance. B checks
   the request/response/destination/amount/expiry bindings.
8. B submits the unchanged bytes. The first accepted execution consumes the
   account sequence even if its mode-3 output action fails; later duplicates
   fail before `accept_message` and cannot repeatedly charge account gas.
9. Both sides resolve finality from the exact external BOC to successful exact
   Agent Account sequence execution and its exact internal destination credit.

The Relay-visible envelope and push metadata remain generic and content-free.

## 7. Cancellation, expiry, and concurrency

Signing reserves an Agent Account sequence in custody but does not lock chain
funds. No replacement is signed while the original action may execute.

A cancellation is a separately owner-authorized `agent_cancel_seqno` for
the same sequence. Gift and cancellation BOCs race; finalized chain state
decides which executed. `invalidated-unpaid` requires finalized cancellation or
another finalized sequence consumption plus proof that no matching destination
credit exists. Finalized controller rotation consumes sequence and permanently
invalidates outstanding controller signatures. Policy tightening without
sequence consumption is reversible and therefore yields only the non-terminal
`currently-unexecutable` observation. Custody retains the original sequence
claim because loosening policy before expiry can make the BOC executable again.
Terminal invalidation requires finalized sequence consumption; otherwise the
flow remains non-terminal until finalized expiry evidence exists.

Local time never creates `expired-unpaid`. Expiry requires finalized chain time
past `valid_until`, unchanged finalized sequence or otherwise reconstructed
sequence history, and absence of both successful Gift execution and matching
destination credit. Missing history or ambiguous submission remains
`finality-unknown`.

Gift V1 intentionally permits only one active primary Agent Account action.
This may temporarily block unrelated automated spending from the account. Later
parallelism requires a separately reviewed account profile; it is not solved by
pre-signing multiple competing sequence values.

## 8. Pre-release replacement and privacy trade-off

- The pre-release Agent Account code, generated artifacts, test deployments,
  opcodes, builders, parsers, and task tooling are replaced in place. There is
  no legacy acceptance mode. Disposable local or testnet accounts are
  redeployed at the new deployment-ID-derived address only after explicit operator
  action.
- OpenFox Gift support is disabled for profiles without a finalized matching
  Agent Account. It never silently creates, deploys, or funds one.
- Wallet V5R1 remains an owner/recovery and ordinary user-payment mechanism. It
  is not a second Agent Gift balance.

Using one Agent Account deliberately trades unlinkability for coherent custody:
every Gift is publicly linkable to that account's task and payment history, and
B learns A's primary operating account, balance, and on-chain policy before
choosing whether to submit. Fresh recipient addresses cannot hide A's sender
history. The UI and operator documentation disclose this; V1 claims neither
relationship privacy nor transaction anonymity.

This ADR amends the main Gift specification's Wallet V5R1 and dedicated-wallet
language, wallet-ID checks, body terminology, and dedicated-Gift-wallet
invariant. The main document is changed in the same patch so only one normative
sender profile exists.

## 9. Required evidence before enablement

- reproducible Agent Account code and pinned code hash;
- a pinned minimum TVM/global version of 4 or newer, required by `GLOBALID`;
- independent Rust and Go builders/parsers with shared positive and adversarial
  vectors;
- TVM tests for signature domain, wrong-network replay, sequence, expiry,
  policy, zero amount, insufficient execution balance, exact output shape,
  mode-3 failed output and conservative daily-limit accounting, cancellation,
  controller rotation with sequence invalidation, reversible policy tightening,
  day rollover, uninitialized destination credit, and malformed cells;
- custody tests for shared sequence claims, owner authorization, crash recovery,
  ambiguous broadcast, and lower-level signer inaccessibility;
- Messenger refusal tests for unauthenticated, first-contact, room, model,
  Relay, Gateway, stale, and substituted address data;
- finalized resolver tests linking exact external BOC, exact account execution,
  and exact destination credit;
- a real local-validator run covering payment, expiry, cancellation, duplicate
  submission, ambiguous recovery, and full process restart; and
- diagnostics tests proving addresses, AgentIDs, amount, authorization, and BOC
  bytes do not enter model input, logs, labels, traces, push, or Relay metadata.

Until all evidence exists, the feature remains disabled and no mock result is
reported as chain acceptance.
