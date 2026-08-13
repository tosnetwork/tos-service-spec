# Native Registry Submission and Resolution V1

Status: **normative Phase 5B contract**

## 1. Authority boundary

`NativeRegistryService` is a relay and exact resolver for the Phase 5A Native
registry contract family. A successful RPC, publisher journal row, gateway database
row or transaction hash is not registry authority. Only a complete action and
event reconstructed from a strict-majority finalized TOS observation, accepted
deterministic object-contract address and allowed code hash, and deterministically replayed predecessor
chain is authoritative.

The relay accepts already bounded and signed `NativeRegistrySubmissionV1`. It
never receives a private key, rewrites an action, selects a controller policy,
supplies chain time or asserts finality. `authority_policy_cbor_base64url` is an
equality assertion against the policy in the canonical predecessor. Transfer
requires separate current-owner and new-owner authorization sets over the same
action bytes.

## 2. Execution envelope and Action ID

The semantic Action ID is the Phase 5A `RegistryAction` digest, rendered as its
canonical lowercase `sha256:<64 hex>` value. The execution envelope contains:

```text
version = tos_native_registry_v1
complete canonical RegistryAction CBOR
canonical authority ControllerPolicy CBOR
strictly ordered current-authority signatures
strictly ordered new-owner signatures (transfer only; empty otherwise)
```

Canonical action/payload/policy limits are defined in
`NATIVE_CAPABILITY_REGISTRY_V1.md` §2.1. The deterministic Phase 5B envelope is
at most 49152 bytes before BOC encoding. Unknown fields, duplicate signatures,
duplicate keys, noncanonical encodings and unused new-owner signatures fail
before journal persistence or broadcast.

The enrolled publisher repeats the complete envelope and live-authority
validation itself before asking custody to prepare a wallet message and again
before the first broadcast. The Unix-socket peer is not trusted merely because
it runs as the same service user. An invalid, stale or purpose-mismatched
request therefore cannot spend publisher fees even if the gateway process is
compromised. An ambiguous recovery may reuse only already-durable identical
prepared bytes; it never creates a fresh custody request.

## 3. Submission operation

The durable publisher identity is `(network/genesis, object contract,
action version, action_id)`. Its journal state is monotonic:

```text
intent_persisted -> reconciling -> broadcast -> canonically_observed -> completed
```

Intent and exact envelope digest are committed and fsynced before broadcast.
The enrolled custody executable then builds and signs the exact external wallet
message without broadcasting it. The publisher commits that canonical
standard-base64 BOC and its SHA-256 digest before marking the broadcast attempt
and submitting those bytes through the pinned RPC client. Crash recovery may
resubmit only the byte-identical message; it MUST NOT ask custody to sign a
second wallet transaction. Wallet sequence and external-message identity make
the retry converge on one canonical mutation while still allowing a crash
before the network call to finish safely.
Exact replay returns the original canonical result. Reusing an Action ID or
idempotency key with different bytes is `IDEMPOTENCY_CONFLICT`. A completed
entry cannot regress. A pending, unknown or ambiguous result remains
reconciling and cannot authorize another broadcast.

Before any mutation the service resolves the Action ID read-only. Only a
versioned typed absence response authenticated by the enrolled journal and
bound to the exact Action ID can authorize first broadcast. Plain/proxy 404,
unsupported route, malformed response, cache miss, timeout, journal loss,
validator disagreement or absent local projection fails closed.

Publisher enrollment binds at least:

```text
network and genesis; Agent/Capability code hashes and address-derivation version
action/envelope version; journal identity and schema
mutation and recovery endpoint set; payer/wallet identity
sender/recovery backend and immutable executable/config digests
```

Normal startup never creates an absent enrolled journal. Readiness validates
the real backend capability, genesis, endpoint identity, wallet and contract
code hash before one-time enrollment.

## 4. Exact resolution

`ResolveNativeRegistryAction` resolves one Action ID. A supplied expected
action is an equality assertion. `ResolveNativeRegistryState` resolves exactly
one Agent or Capability; exactly one object ID is present. An expected state
digest or observation is also only an equality assertion.

A successful result includes the complete action, event, reconstructed state
and observation. The resolver:

1. queries independent configured validators;
2. requires strict-majority agreement on network/genesis, transaction and
   finalized checkpoint;
3. recomputes the deterministic object address and validates its code hash;
4. obtains complete action/envelope bytes from the canonical transaction;
5. rechecks Phase 5A canonical encoding, signatures and policy authority;
6. replays every required predecessor without gaps;
7. derives the complete next state and compares its digest to the event;
8. rejects zero/regressed/stale checkpoints and reorganization ambiguity.

Historical states remain resolvable for authorization-at-time checks. Search,
ranking and discovery are Phase 5C and are not provided by these exact APIs.

## 5. Typed absence and errors

Every Action ID maps to a deterministic immutable Action Anchor account.
Canonical absence is returned only after strict-majority validators agree that
that exact derived account is absent at the same nonzero finalized checkpoint.
A bounded history miss is not absence. A present but pending Anchor is
unavailable, not absent, and never authorizes another mutation.
Transport failure is `NATIVE_FINALITY_UNAVAILABLE`; conflicting evidence is
`NATIVE_INTEGRITY_CONFLICT`; stale or regressed authority is
`NATIVE_STALE_AUTHORITY`.

Verification and resolution are read-only and must never call Publish or any
mutation API.

## 6. Privacy

Consensus, journals and public responses contain only bounded public registry
facts and content commitments. They never contain wallet seeds, private task
data, endpoint credentials, proposal bodies, manifest bodies, HSM/Vault
material or backend command output.
