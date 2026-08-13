# Native Registry TVM Representation V1

## Cell families

The registry uses versioned typed cells:

| Magic | Meaning |
|---|---|
| `NVD1` | deterministic account data and network configuration |
| `NVS1` | canonical Agent or Capability state |
| `NVA1` | canonical signed action semantics |
| `NVP1` | canonical controller policy |
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

## Storage rules

- dictionaries use canonical fixed-size keys;
- controller and signature entries are strictly ordered;
- immutable version entries cannot be replaced;
- absent optional recovery state has one encoding;
- empty and zero values are accepted only where explicitly defined; and
- no trailing bits or references are ignored.

## Code identity

Clients, relayers, and resolvers pin the reviewed code BOC and expected code
hash. A contract at the expected deterministic address with different code is
not a valid registry object.

The current reviewed hash is:

```text
tvm-cell-sha256:c4af55e476c296c8a1dc7985e82db42218475b9e3864b7c733351bab526ab23d
```

Changing contract code requires a new frozen code identity, vectors, security
review, and explicit protocol deployment decision.
