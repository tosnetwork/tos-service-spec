# A2A Software-Work Adapter V1

## Scope

This adapter maps the Linux Foundation A2A 1.0 Task model into the existing
ATOS Native software-work lifecycle. A2A remains transport. It cannot create an
Agent, Capability, Accepted Quote, funded escrow, Receipt, balance, or
settlement fact.

The implementation uses the official Go SDK module
`github.com/a2aproject/a2a-go/v2` and extension URI:

```text
https://atos.im/extensions/native-software-work/v1
```

V1 is a synchronous `SendMessage` mapping. Streaming, push notifications,
multi-turn input, arbitrary tools, and remote-selected execution policy are not
part of this profile.

## Request mapping

The user-role A2A Message contains exactly two Parts and exactly the extension
URI above:

1. `application/vnd.atos.a2a.software-work-task.v1+json` Data containing only
   `protocol`, `escrow_address`, `quote_commitment`, `execution_id`,
   `input_digest`, and `source_digest`;
2. `application/vnd.atos.software-source.v1+tar` raw bytes named `source.tar`.

`protocol` is exactly `atos_native_v1`. Quote and SHA-256 digests use their
canonical lowercase forms. The source digest is SHA-256 over the exact raw
Part. The input digest is SHA-256 over this domain prefix plus canonical JSON
of protocol, escrow address, Quote commitment, execution ID, and source digest:

```text
atos.a2a.software-work-input.v1 || 0x00 || canonical_binding_json
```

Unknown binding fields, additional Parts, alternate media types, Part metadata,
changed source bytes, malformed digests, agent-role requests, or multiple ATOS
extension declarations fail before any authoritative read or execution lease.

## Authority gate

Before the runner is called, the provider adapter must independently verify
from finalized TOS state and atomically claim the Quote/escrow execution slot:

- exact network and Registry identity;
- live provider Agent, plus active Capability and version and manifest digest;
- Accepted Quote commitment and execution authorization;
- exact funded stablecoin escrow; and
- authenticated chain references and nonzero finalized checkpoints for escrow,
  Agent, and Capability.

The shared Native Execution Gate binds Quote commitment, escrow, execution ID,
input digest, and source digest in one atomic record. A second execution intent
or a claim through another transport for one paid purchase is a conflict, even
if the escrow remains funded. `NATIVE_EXECUTION_GATE_V1.md` freezes this rule.

The A2A sender, Message metadata, bearer credential, task ID, endpoint, and
gateway are not evidence for any of these facts. Failure is fail-closed and no
container starts.

## Result mapping

Objective execution failure produces a terminal A2A failed Task without a
result artifact. Success produces a terminal completed Task with one Artifact,
extension URI above, and one
`application/vnd.atos.a2a.software-work-result.v1+json` Data Part. It contains:

- the finalized authorization evidence;
- Quote, execution, input, result, source, toolchain, and sandbox digests;
- exit code and completion time; and
- artifact/report media type, byte size, SHA-256 digest, and HTTPS retrieval
  URL.

The retrieval URL is transport metadata. The digest authenticates downloaded
bytes. An A2A completed Task means the bounded provider execution completed; it
is not a signed Receipt and does not release escrow. Receipt signing and TOS
settlement remain the canonical post-execution flow.

The A2A task ID is provider-derived from the Quote commitment and execution ID.
The existing execution journal remains the at-most-once authority: completed
replay returns the immutable prior outcome, while ambiguous running state is
never executed again automatically.

## Acceptance

Unit and race tests must prove exact request mapping, mutation rejection before
authority reads, finalized authorization before execution, terminal failure
mapping, conflicting-runner rejection, HTTPS-only result locations, and exact
result commitments. The official synchronous JSON-RPC server binding and the
production finalized-state Gate are implemented. Gate E additionally requires
operator listener hardening and a fresh buyer/provider interoperability
session.
