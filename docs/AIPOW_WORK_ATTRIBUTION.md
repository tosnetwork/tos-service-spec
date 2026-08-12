# AIPoW Work Attribution and the Capability-Class Vocabulary

Status: v0 draft. Normative for the `AipowWorkAttribution` message and the
capability-class vocabulary; the scoring rules that consume these fields
are owned by the AIPoW methodology (the `aipow-scorer` repository's
`docs/methodology.md`), not by this document.

## Purpose

Artificial Intelligence Proof of Work (AIPoW) scores settled, evidence-graded work.
Until now the scorer applied an interim mapping (the settled amount as
both valuation and price cap, a single default capability class, evidence
inferred from attestor keying). `AipowWorkAttribution` puts the
scoring-relevant facts inside the signed receipt itself, so no consumer
ever infers them:

- `capability_class` + `unit` + `work_units`: what work, in which
  normalized billing unit, how much — per the vocabulary below;
- `rate_card_version`: which vocabulary/rate-card revision normalization
  followed;
- `evidence_level`: the AIPoW evidence ladder (Declared earns zero by
  methodology rule; issuers state the strongest level they can
  substantiate, verifiers may downgrade, never upgrade);
- `earner_identity_commitment` / `payer_identity_commitment`: sha256
  commitments to the 32-byte chain accounts (bonded Capability Registry
  identities) the work is attributed to;
- `challenge_task`: protocol-issued challenge work scores normally but
  never counts toward organic settled value.

The message is descriptive only. It grants no authority, moves no funds,
and does not by itself prove the work happened — the evidence level says
what backs the claim, and the receipt signature says who claims it.

## Placement

- `ExecutionReceiptEnvelope.aipow` (field 25): part of the signed receipt
  content when present; omitted from the canonical encoding when absent,
  so pre-existing receipts keep their signatures and digests unchanged.
- `ProofOfServiceEvidenceInput.aipow` (field 13): mirrored from the
  underlying receipt so evidence streams are scoreable without
  re-fetching every receipt. On any disagreement the receipt governs.

## Capability-class vocabulary v0

Classes are lowercase-kebab-case, stable once published. `work_units` is
always an integer count of the class's unit, floored. A measurement that
cannot be normalized under these rules must be reported under `default`,
never approximated under a specific class.

| Class | Unit | Normalization rule |
|---|---|---|
| `text-generation` | `kilo-output-tokens` | floor(output tokens / 1000); a nonzero output below 1000 tokens reports 1 |
| `embedding` | `call` | 1 per completed embedding/rerank invocation |
| `image-generation` | `image` | count of images produced at the negotiated resolution |
| `speech-recognition` | `audio-second` | floor of processed input audio duration in seconds |
| `speech-synthesis` | `audio-second` | floor of produced audio duration in seconds |
| `storage-byte-hour` | `byte-hour` | floor(bytes stored × hours proven); retrievability-probe failures exclude the probed interval |
| `verification-replication` | `replicated-call` | 1 per independent re-execution whose output matched the original commitment |
| `default` | `settled-nanotos` | the settled amount in nanoTOS — the interim fallback; under this class `work_units` equals the settled amount and carries no independent measurement |

Adding a class, changing a unit, or changing a normalization rule is a
new `rate_card_version` and follows the AIPoW methodology's governance
process (advance publication; scorers reject unknown versions rather
than guess).

## Conformance notes

- Example digests or worked vectors added to this document later must be
  generated from a passing run of the reference implementation, never
  hand-computed (see this repo's CLAUDE.md, lesson 1).
- A receipt whose `aipow.capability_class` is not in the vocabulary for
  the stated `rate_card_version`, whose `unit` mismatches the class, or
  whose commitments are not 32-byte sha256 digests is malformed: verifiers
  reject it rather than repair it, and scorers treat it as a hard error,
  never a silent skip.
