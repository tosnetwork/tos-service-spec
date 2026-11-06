# Native Registry: post-quantum controllers (design)

**Status:** design, revision 4. It changes the existing Native Registry in place. TOS is
pre-launch and no registry object exists on any public network (inventory memo
7e540d9), so there is no earlier registry to keep, migrate or tell apart: the
Ed25519 controller scheme is replaced, not versioned. The changed contract still needs
the gates of section 7, a frozen code identity with vectors, a security review and a
deployment decision, as `NATIVE_REGISTRY_TVM_V1.md` requires for any code change.

**Owner decisions it implements (2026-11-06):** post-quantum service-layer signatures
are a priority; public Native Registry registration waits for this change; a policy
holds at most **8** controllers, with the contract optimized as specified in section 4.2
(the earlier cap of 16 was withdrawn after the lifecycle measurement in section 5); no
V1/V2 split, the existing registry is changed in place.

## 1. Why

TOS consensus finalizes with ML-DSA-44 certificates and TOS wallets have post-quantum
variants, but every service contract (Native Registry, Service Actor, Task Escrow,
Proof Attestation, Agent Account, Dispute) authorizes with Ed25519 `CHKSIGNU` only.
Registry policies publish their controller public keys on chain, so an adversary able
to forge Ed25519 from a public key could take over every Agent and Capability at once.
This change replaces the controller signature scheme of the Native Registry. The other
service contracts follow in their own designs; Service Actor, the chosen settlement
rail, comes next.

## 2. What does not change

The object model, identifiers, state machines and routing stay as specified in
`NATIVE_REGISTRY_STATE_MACHINES.md` and `NATIVE_REGISTRY_TVM_V1.md`:

- Agents and Capabilities as deterministic accounts, one object per account;
- the ten action kinds and their payloads (except where they carry a policy),
  generation, sequence and predecessor rules, replay of the stored action hash as a no-op,
  tombstones, delegation, the recovery timelock, Capability routing through the owner
  Agent and the two-owner transfer;
- purposes (Agent control, delegation, Capability control, recovery), purpose isolation,
  per-purpose threshold reachability, and possession: installing a policy (registration,
  policy update, recovery initiation) needs a signature from every controller of the
  installed policy; registration consent is the agent-control weight among them
  (`verify_registration_consent`, as in the current release `c7958fb6`);
- the cell families and their magics and schema values (`NVD1`, `NVS1`, `NVA1`, `NVP1`,
  `NVI1`, schema 1), and the identity, action, state and data layouts.

## 3. What changes

### 3.1 One admitted suite

Controllers are ML-DSA-44 keys only (FIPS 204 Pure ML-DSA-44, `PQCHECKSIG_MLDSA44`, TVM
global version 16). There is no Ed25519 controller and no mixed policy. A second
algorithm is a protocol change, as `crypto/smartcont/pq-bytes.fc` already rules.

A mixed policy keeps the weaker scheme's forgery power over every purpose whose
threshold it can reach, so it buys no security.

### 3.2 Key material and key identity

- **Stored key:** the `pq-bytes.fc` stored shape, `len:uint32 ^chain`, `len` = 1,312, the
  chain canonical as `PQCHECKSIG_MLDSA44` requires (ordinary level-zero cells,
  byte-aligned, 127-byte full chunks with exactly one continuation, a final chunk of
  1..127 bytes and no reference). The wrapper cell and every chain cell are parsed as
  ordinary cells; library and other exotic cells are refused at every container boundary.
- **Key id:** `SHA-256("TOS-PQ-CONSENSUS-KEY-v1" || u16_le(1) || key bytes)`, the value
  `pq::key_id` computes, the identity a post-quantum key already has in every TOS role.
  Reusing the domain links one key's identity across roles on purpose; authority stays
  separated by the signature context (3.4) and the fully bound action preimage.
- **Text form** (replaces `ed25519:<public key hex>` in `NATIVE_IDENTIFIERS_V1.md`):
  `mldsa44:<64 lowercase hex key id>`.

### 3.3 Changed layouts

Only the policy, its controllers and the signature sets change; every other layout keeps
its current form.

```text
policy     = "NVP1":uint32 schema:uint16(=1) threshold:uint32 recovery_threshold:uint32
             recovery_timelock:uint64 count:uint8 ^controller
controller = key_id:uint256 weight:uint32 purposes:uint16 recovery:Bool
             ^stored_key [^controller]                -- strictly ascending key_id
signatures = count:uint8 [^entry]       -- count = 0 has no reference
entry      = key_id:uint256 ^stored_signature [^entry]   -- strictly ascending key_id
stored_signature = len:uint32(=2420) ^chain
```

- `1 <= policy count <= 8`; a signature set holds at most 8 entries. A wider policy or
  set is refused with `policy_too_wide` before any entry is read.
- The empty signature set (`count = 0`, no reference) is the only encoding of "no
  signatures" and is what kinds without counterparty consent carry.
- Agent ids change because the policy hash they commit to changes; Capability ids change
  with their owner Agent's id. The exact preimages and their test vectors are frozen with
  the contract.

### 3.4 Signatures

- **Scheme:** Pure ML-DSA-44 over the 32 raw bytes of the canonical action hash (the TVM
  cell hash of the `NVA1` action cell), with the context string `TOS-NATIVE-REGISTRY`
  (19 bytes, within the instruction's 0..255). No prehash, no external-mu.
- **Threshold authorization:** every signer is a controller of the current policy with
  the required purpose (and the recovery designation for recovery actions); weights of
  distinct signers sum to the threshold.
- **Possession:** exactly the installed policy's controllers, in key-id order, each
  verified against the stored key cell carried in the installed policy.
- **Non-determinism:** ML-DSA signing may be randomized (hedged), so two valid signature
  sets for one action differ byte for byte. Replay detection and the stored last action
  use the action hash and are unaffected. Consumers must identify a registry operation by
  its action hash (section 6) and freeze signatures as data in vectors.

### 3.5 Workchain

Registry objects live in the basechain only (workchain 0), and the contract refuses to
run elsewhere. This is a deliberate constraint, consistent with the PQ multisig, not a
sizing necessity: the basechain gas limit and the per-account state limits (65,536 cells
against 2,048 in the masterchain) leave room for later growth of policy state.

## 4. Delivery route and contract rules that keep it affordable

### 4.1 Route

A registry action is submitted as one internal message sent by a **relayer wallet**,
delivered to that wallet by one external message: the route tos-service-protocol already
uses (`pkg/chainactionpublisher`, which prepares the exact message with
`tosctl wallet send --build-only` from an ordinary wallet and broadcasts only those
bytes). A registration's internal message carries the StateInit with the registry code
and its account data.

The relayer wallet pays fees and holds **no registry authority**: an action is authorized
only by the ML-DSA-44 controller signatures inside its body, which bind the action hash,
the network and the registry code. A compromised transport key can therefore drop,
delay or pay for submissions, but cannot forge or alter a registry action, so the
transport key need not be post-quantum for the registry to be. (A post-quantum user
wallet can carry the same message once one is released for submission; the Quantum
wallet is merged but not released, and `tosctl` cannot yet deploy or broadcast with it.)

The route's binding limit is genesis ConfigParam 43 `max_ext_msg_size` = **65,535
bytes**; internal messages (`max_msg_cells` 8,192, `max_msg_bits` 2^21) are well inside
their limits.

### 4.2 Validation once, native operand checks

Measured cost is dominated not by signature checks but by FunC-level canonical-chain
walks repeated per key, per signature and per policy walk (section 5). The contract
therefore:

1. reads stored keys and stored signatures without a FunC chain walk and lets
   `PQCHECKSIG_MLDSA44` enforce exact lengths and canonical chains (it throws exit 9 on
   any malformed operand, and refuses exotic and library cells);
2. **admits** a new policy only when one is submitted for installation (registration,
   policy update, recovery initiation): it checks every stored-key wrapper (ordinary cell,
   declared length 1,312, exact references, exhaustion), verifies every possession
   signature against the key chain that wrapper carries, and only then derives each key
   id with one SHA256C over the domain, the suite and that same chain, requiring it to
   equal the controller's declared id;
3. **promotes** without re-admission: recovery completion is authorized by the current
   policy's recovery signers, keeps the existing initiation-hash, policy-hash and timelock
   checks, carries an empty counterparty set, and installs the pending policy exactly as
   it was admitted and possession-proven at initiation;
4. admits each submitted policy at most once per transaction;
5. trusts the stored, already admitted ids and keys of the current policy for threshold
   authorization, and never re-derives them.

## 5. Limits and cost (measured)

Measured with a lifecycle probe (tos branch `test/pq-registry-gas`, commit `b1337ec4e`).
What it measures, and what it does not:

- **Probe gas:** the cryptographic and codec work of one registry transaction per path,
  i.e. its ML-DSA-44 verifications against stored keys and its key-id derivations, once
  with the unoptimized codec (`pq::stored_key`, `pq::stored_signature`, `pq::key_id`,
  repeated as often as the current contract walks each policy) and once as section 4.2
  specifies. It is not full-transaction gas: the contract's own parsing, state writes and
  outgoing messages are not included, and the optimized variant does not exercise the
  wrapper checks of 4.2 rule 2. The Rust VM and the C++ transaction emulator agree to the
  gas unit on every case within the emulator fixture's 1,000,000 limit.
- **Message size:** the serialized BOC of the route's whole external message: the relayer
  wallet's external message (real `ext_in` header, wallet v3r2 body) carrying the
  internal message with the action, payload, both signature sets over the exact action
  hash, and, for a registration, the StateInit with the current registry code and account
  data. It is a **structurally representative serialized estimate**, not a broadcast and
  not the exact route encoding: the relayer's signature and seqno are placeholders of the
  right width; the wallet body omits the 4-byte `global_id` field TOS's v3r2 request
  carries; the action uses one kind and placeholder state and domain fields for every
  path; controller and signature lists are not in canonical key-id order; and the current
  registry code stands in for the changed code. None of these changes the size by more
  than a few bytes per message, except the changed code for a registration.
- **Not measured:** the second transfer leg is not executed separately (it verifies the
  receiving owner's threshold signatures, the same workload as the first leg), and neither
  leg's sender authentication or forwarding is executed.

| Controllers | Path | Probe gas, unoptimized | Probe gas, section 4.2 | Serialized external message |
|---|---|---|---|---|
| 8 | registration | 429,670 | 51,033 | 36,465 B |
| 8 | policy update (8 old + 8 new signatures) | 790,678 | 114,449 | 52,493 B |
| 8 | recovery initiation | 880,710 | 114,449 | 52,501 B |
| 8 | recovery completion | 441,854 | 47,761 | 20,703 B |
| 8 | one transfer leg | 339,638 | 41,521 | 41,274 B |
| 10 | policy update / recovery initiation | 997,690 / 1,110,230 | 152,535 | 65,483 B / 65,491 B |
| 12 | policy update / recovery initiation | 1,204,702 / 1,339,750 | 190,621 | 78,474 B / 78,482 B |

- With section 4.2, probe gas stays far below the 800,000 registry ceiling at every
  width measured; the unoptimized codec would exceed it at 8 for recovery initiation.
- **Message size sets the cap.** A disjoint policy update or a recovery initiation
  carries the old threshold signatures, a possession signature for every new controller
  and every new key, and no code. At 10 controllers the estimates leave 52 bytes (update)
  and 44 bytes (recovery initiation) under `max_ext_msg_size`, which the omitted
  `global_id` and any growth of the envelope or payload fields would erase; at 12 they no
  longer fit. Registration carries the code instead and is about 16 KB lighter at 8, so
  code growth is checked against registration separately. In these estimates eight
  controllers fit every path with about 13 KB of margin, pending the real-message gate of
  section 7.
- These are gates for the changed contract, not results: it must be re-measured on both
  VMs for every policy-walking path at 8 controllers, with full-transaction gas at or below
  800,000 and every path's real relayer message at or below 65,535 bytes.

## 6. Consumers to change

| Component | Change |
|---|---|
| tos `crypto/smartcont/native-registry-code.fc` | ML-DSA-44 policy and signatures with section 4.2 rules, cap 8, basechain only |
| tos `contracts::native_registry` and its sandbox suites | ML-DSA-44 policy and signature encoders, key ids, test signer |
| tos-service-protocol `pkg/nativecore`, `internal/referencecodec` | policy and signature encoders, key-id derivation, ML-DSA-44 verification |
| tos-service-protocol relayer and journal | registration preflight: possession for every controller plus agent-control consent weight (fixed in tos-service-protocol `#28`); operation identity = action hash, while a broadcast attempt keeps its exact body, funding, destination and StateInit; a re-signed body for the same action must neither be rejected after completion nor broadcast twice |
| tos-service-protocol wallet, tosctl vault | ML-DSA-44 controller keys and signing; no private key leaves custody |
| tos-service-spec | `NATIVE_IDENTIFIERS_V1.md`, `NATIVE_IDENTITY_V1.md`, `NATIVE_REGISTRY_TVM_V1.md` code identity, frozen vectors, edited in place |
| gateway, tos-ai, openfox | follow the protocol release that ships the change |

## 7. Verification before freeze

- Contract sandbox on both VMs: every current lifecycle and refusal case re-run with
  ML-DSA-44, including a mixed-purpose registration (a controller isolated to delegation,
  Capability control or recovery signs for possession only) accepted by the contract and
  by the protocol relayer preflight, and recovery completion promoting the pending policy
  with an empty counterparty set.
- Adversarial cases: wrong context; a cross-role signature (same key, consensus or quorum
  context); signature by a non-member; a stored key whose id does not match; library or
  exotic cells substituted for the wrapper and for continuation cells of keys and
  signatures; trailing bits or references; malformed lengths; 9 controllers; 9 signature
  entries; duplicate and out-of-order entries; possession missing one controller; two
  valid randomized signature sets for one action producing exactly one state transition;
  Ed25519-shaped policies and signature entries refused; deployment outside workchain 0.
- Gas at 8 controllers for every policy-walking path (registration, disjoint 8-to-8
  update, 8-to-8 recovery initiation and completion, both transfer legs) at or below
  800,000 on both VMs.
- Every path's real relayer external message at 8 controllers, produced by
  `tosctl wallet send --build-only` and broadcast on a test network, within 65,535 bytes,
  and the 9-controller policy refused by the contract.
- Both transfer legs executed separately, including sender authentication and forwarding.
- Frozen vectors produced by executing the contract: key-id preimages (including the
  little-endian suite number), identity preimages, action hashes, signatures over the
  exact 32 raw hash bytes; reproduced by the tos Rust builders, `nativecore` and the
  independent reference codec.
- Relayer journal tests: randomized re-signatures of one action across prepared,
  broadcasting, completed, concurrent and restarted states.
- Independent security review of the changed contract and the protocol changes.
