# Testing Lessons Shared Across the TOS Repos

This file tracks recurring bug classes found in the implementation
repositories (`atos`, `tos-protocol`, `tos`) whose lesson is relevant to
what this repo specifies or documents — kept here so anyone writing or
reviewing a normative contract in `atos-spec` knows what implementation-side
mistakes it should help prevent. The canonical, more detailed log lives in
`atos/CLAUDE.md` (Phase 4A's 10-round review retrospective); this file
mirrors only the entries with a specification-level angle.

## 1. Hardcoded golden/vector test values transcribed incorrectly at commit time

Found in `atos/internal/financial`'s V2 batch golden CBOR test vector: it
was wrong from the moment it was hardcoded, not a later regression — a
transcription error at commit time that nothing caught because the test
only ever compared against itself.

**Relevance to this repo:** any normative doc that specifies a canonical
encoding or a worked example digest (e.g. `docs/FINANCIAL_INTEGRITY.md`,
`docs/PROOF_PROFILES.md`, or a schema's example vectors) should state
plainly that such example values must be generated from a real, passing run
of the reference implementation, never hand-computed or hand-copied — and
implementers should treat "does this match the frozen example" test
failures as a signal to re-verify the example itself before assuming their
own code regressed.

## 2. Two independently-locked reads composed to test (or serve) one atomic write

Found in `atos/internal/service`'s dispute-resolution test suite: a caller
polled two related pieces of state (a dispute and its earning) via two
separate, independently-locked reads. The underlying write of both was
atomic, but two independent reads are never atomic with respect to each
other regardless of how well-locked the write is.

**Relevance to this repo:** whenever a normative RPC/API contract describes
two-or-more fields or resources that a single operation updates together
(e.g. a Capability's `mode_support` alongside its `ownership` projection, or
an identity-binding operation's durable journal alongside the live binding
row), the spec should be explicit about whether callers are guaranteed a
consistent combined view, and if so, require the implementation expose a
genuinely combined atomic read for that pairing rather than leaving callers
to compose two separate reads and assume consistency.
