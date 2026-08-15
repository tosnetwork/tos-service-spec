# Gate E Provider Onboarding

## Status

This is the first active Gate E slice. Gate D external acceptance remains open
and proceeds independently. This workflow does not change Gate D evidence or
weaken Gate E acceptance: a genuinely new provider must still publish and sell
the Capability from public documentation in one working session.

## Authority boundary

- finalized typed TOS state is the sole authority for Agent and Capability
  publication;
- `tos-protocol/pkg/providersdk` prepares canonical bytes, verifies external
  controller signatures, relays an exact reviewed action, and waits for the
  matching finalized state;
- `tos-protocol/pkg/nativeclient` transports Native Submit/Resolve requests and
  requires HTTPS unless loopback development is explicitly selected;
- neither SDK accepts a private key or stores canonical provider state;
- a relay acknowledgement is not publication success;
- manifest CBOR is content-addressed off-chain data, never a consensus input;
- the provider executor and `tosctl` signing custody remain separate; and
- no gateway database edit is part of onboarding.

## Provider sequence

1. Generate the provider Agent controller and execution signer through the
   reviewed `tosctl` custody boundary. Register the Agent and resolve its exact
   finalized state.
2. Fill the frozen software-work manifest JSON. Use the provider SDK to
   strictly decode it, produce canonical CBOR and its digest, generate the
   Capability registration, and display the derived Capability ID and action
   hash.
3. Review and sign the action outside the SDK. Submit the signatures through
   the SDK with one durable idempotency key.
4. Accept publication only when the SDK returns finalized typed Capability
   state containing the exact owner, version, manifest digest, action hash,
   Registry code hash, network, and checkpoint.
5. Serve the canonical manifest bytes under their digest. Search caches may
   index the chain-derived association but cannot create or replace it.
6. Install the dedicated provider runtime from `tos-ai/deploy/provider`. The
   private containerd socket stays root-owned and unavailable to the gateway;
   the executor has no signing key.
7. Complete the existing direct Accepted Quote, funded escrow, bounded
   execution, Receipt, and settlement flow. Until the commercial Native RPC is
   frozen, local tools may orchestrate this step but cannot add protocol facts.

## Current implementation

- Go SDK guide: `tos-protocol/docs/provider-sdk.md`
- public transport: `tos-protocol/pkg/nativeclient`
- provider publication: `tos-protocol/pkg/providersdk`
- runtime deployment: `tos-ai/deploy/provider`
- canonical manifest: `docs/SOFTWARE_WORK_MANIFEST_V1.md`
- commercial lifecycle: `docs/GATE_D_EXTERNAL_PILOT.md`

## First-slice acceptance record

Record the provider organization, start/end time, release commits, public
gateway URL, network/genesis tuple, Agent ID, Capability ID/version, manifest
digest, action hash, finalized checkpoint, Registry code hash, deployment host
profile, executor conformance result, Quote commitment, escrow, Receipt,
settlement transaction, and provider-wallet balance delta. Do not include a
token, source credential, mnemonic, private key, vault export, or containerd
socket.

The provider item remains in progress until a clean operator environment can
follow only public documentation, publish the exact Capability, deploy the
runtime, and complete the sale without repository edits or private developer
instructions.
