# Public Error and Retry Semantics V1

## Purpose

Public clients must never infer retry safety from HTTP status, Connect code, or
human-readable text alone. Every conforming Native Connect error carries one
`NativeErrorV1` detail. Clients branch only on its numeric code, stable
identifier, and retry disposition.

Diagnostics are non-normative and may change. Authentication failures must not
leak private configuration.

## Retry dispositions

`NEVER` forbids automatic replay. The caller may correct input, credentials, or
policy and create a new deliberate request.

`SAME_REQUEST_AFTER_BACKOFF` permits only the byte-identical logical request,
with the same mutation idempotency key where applicable, after the bounded
`retry_after_millis`. The delay is between 100 and 300,000 milliseconds. It is
used only when the server knows no ambiguous paid or externally visible action
was created.

`RESOLVE_BEFORE_RETRY` forbids immediate replay. The client first queries the
authoritative finalized Native, escrow, wallet, Receipt, or execution journal
state. It retries only if that read proves the original effect did not occur
and the relevant owner-held journal grants a new lease.

`UNSPECIFIED`, missing details, multiple details, unknown codes, conflicting
Connect codes, forbidden delays, and out-of-range delays all fail closed as
`NEVER`.

## Canonical matrix

| Stable identifier | Connect code | Disposition |
|---|---|---|
| `PUBLIC_BAD_REQUEST` | `invalid_argument` | `NEVER` |
| `PUBLIC_NOT_FOUND` | `not_found` | `NEVER` |
| `PUBLIC_CONFLICT` | `failed_precondition` | `NEVER` |
| `PUBLIC_DEPENDENCY_UNAVAILABLE` | `unavailable` | `SAME_REQUEST_AFTER_BACKOFF` |
| `PUBLIC_CAPACITY` | `resource_exhausted` | `SAME_REQUEST_AFTER_BACKOFF` |
| `PUBLIC_AMBIGUOUS_OUTCOME` | `aborted` | `RESOLVE_BEFORE_RETRY` |
| `PUBLIC_DEADLINE` | `deadline_exceeded` | `NEVER` |
| `PUBLIC_UNAUTHENTICATED` | `unauthenticated` | `NEVER` |
| `PUBLIC_PERMISSION_DENIED` | `permission_denied` | `NEVER` |

Native Registry validation codes `2200..2213` retain their existing stable
identifiers and use `NEVER`: the exact action is deterministically invalid at
the checked state. A newly constructed action may be valid only after the
caller resolves current state and deliberately reviews and signs it.

## Mutation rule

An unknown relay, wallet broadcast, execution, Receipt submission, or
settlement failure is never downgraded to ordinary unavailability. It is
`PUBLIC_AMBIGUOUS_OUTCOME` and requires authoritative resolution before any
retry. Read-only dependency failure may use
`PUBLIC_DEPENDENCY_UNAVAILABLE`.

Gateways preserve a valid upstream detail. They replace missing, malformed, or
conflicting details with a safe locally known classification; they never copy
an upstream diagnostic into a retry decision.
