# Native Registry TVM Representation V1

## Cell families

The registry uses versioned typed cells:

| Magic | Meaning |
|---|---|
| `NVD1` | deterministic account data and network configuration |
| `NVS1` | canonical Agent or Capability state |
| `NVA1` | canonical signed action semantics |
| `NVP1` | canonical ML-DSA-44 controller policy |
| `NVI1` | deterministic registration identity |

Decoders require exact magic, version, bit lengths, reference shape, ordering,
and exhaustion. Unknown versions fail closed.

## Account data

The root data cell binds object kind, object ID, registry code hash, network
domain, and optional current state. The contract reconstructs StateInit and
verifies its running address before processing mutation.

## Action cell

The action root commits to domain, target, ordering, predecessor, nonce, and
typed payload. The canonical action hash is its TVM cell hash. Signature cells
are separate transport arguments so the signed semantic cell is identical for
all relayers.

The root and referenced cells have fixed layouts and bounded contents. Variable
text uses the specified snake-cell encoding and is checked against any digest
stored in the fixed portion.

## State cell

Agent and Capability states are disjoint typed variants. The state cell hash is
the predecessor used for the next action. Contracts construct the next state
internally from current state and validated payload; callers cannot supply a
replacement state cell.

## Forwarded authorization

The contract recognizes direct submission and Agent-authorized forwarding
opcodes. Forwarding preserves the exact action and signature cells. Receiving
contracts authenticate the deterministic sender address and reject unexpected
sender chains.

## Policy and signature cells

Controllers are ML-DSA-44 keys only. Registry objects exist in workchain 0
only; the contract refuses to run in any other workchain.

```text
policy           = "NVP1":uint32 schema:uint16(=1) threshold:uint32
                   recovery_threshold:uint32 recovery_timelock:uint64
                   count:uint8 ^controller
controller       = key_id:uint256 weight:uint32 purposes:uint16 recovery:Bool
                   ^stored_key [^controller]
stored_key       = len:uint32(=1312) ^chain

signatures       = count:uint8 [^entry]
entry            = key_id:uint256 ^stored_signature [^entry]
stored_signature = len:uint32(=2420) ^chain
```

- `key_id` is the 32-byte controller key ID of `NATIVE_IDENTIFIERS_V1.md`,
  derived from the stored key bytes.
- A policy holds 1 to 8 controllers; a signature set holds 0 to 8 entries. A
  wider policy or set is refused with `NATIVE_POLICY_TOO_WIDE` (2215) before
  any entry is read.
- Controllers and signature entries are linked through their last reference
  and are strictly ascending by `key_id`; the last element has no `^next`
  reference.
- The empty signature set is exactly `count = 0` with no reference; it is the
  only encoding of "no signatures".
- `chain` is canonical: byte-aligned ordinary cells, each full cell holding
  exactly 127 bytes and exactly one continuation reference, and a final cell
  holding 1 to 127 bytes and no reference. The total equals `len`. Library and
  other exotic cells are refused at the wrapper and at every chain cell.
- Signatures are Pure ML-DSA-44 (FIPS 204, no pre-hash) over the 32 raw bytes
  of the `NVA1` action cell hash with context `TOS-NATIVE-REGISTRY` (19 bytes).
- A policy submitted for installation (registration, policy update, recovery
  initiation) is admitted once: shape, then a possession signature from exactly
  every controller in key-ID order, then each declared `key_id` must equal the
  ID derived from the key the signature verified against. A stored policy is not
  re-validated; recovery completion promotes the admitted pending policy.

The design rationale and measurements are in `NATIVE_REGISTRY_PQ_DESIGN.md`
(tosnetwork/tos-service-spec#60). Measured at 8 controllers with full
transactions, the most expensive path (recovery initiation) uses at most
177,113 gas, and the largest relayer external message is 52,506 bytes against
the 65,535-byte external message limit.

## Storage rules

- dictionaries use canonical fixed-size keys;
- controller and signature entries are strictly ascending by key ID;
- immutable version entries cannot be replaced;
- absent optional recovery state has one encoding;
- empty and zero values are accepted only where explicitly defined; and
- no trailing bits or references are ignored.

## Code identity

Clients, relayers, and resolvers pin the released code BOC and expected code
hash. A contract at the expected deterministic address with different code is
not a valid registry object.

The current code identity (tos commit `c17d3fca5`) is:

```text
code hash   tvm-cell-sha256:d3bb66d0011a1f362dd0be8408ed688f4e740d096a0e2dc2a79fc0ffc628b28a
BOC sha256  sha256:dcf41afaa7da7761839f3d26955ebab8dcd8adfe1d428b89229780c6647cdb9b
BOC size    4,143 bytes
```

The independent security review of this code is open
(`NATIVE_REGISTRY_SECURITY_REVIEW.md`), and it is not deployed on any network.

Changing contract code requires a new frozen code identity, vectors, security
review, and explicit protocol deployment decision.

The reproducible release is defined by
`tos/crypto/smartcont/tos-service-native-registry-v1.release.json`, and the
code artifact is
`tos/crypto/smartcont/tos-service-native-registry-v1.boc.base64`. The canonical
source is `tos/crypto/smartcont/native-registry-code.fc`; there is no parallel
legacy or `v2` Registry source.
