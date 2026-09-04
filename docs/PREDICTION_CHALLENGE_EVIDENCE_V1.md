# Prediction Evidence and Challenge Evidence V1

Status: release candidate. This profile makes a reporter quorum agree on one
reconstructible evidence set rather than on free-form prose.

## 1. Source entries

Source kinds are `HTTPS=1`, `SIGNED_DOCUMENT=2`, and `TOS_FINALIZED=3`.

```text
prediction_text#50545831 schema_version:uint16 length:uint16
  text:(length * 8 bits) = PredictionCanonicalTextV1;

prediction_evidence_meta#50454d54
  schema_version:uint16
  content_digest:uint256
  publication_time_seconds:uint64
  event_time_seconds:uint64
  = PredictionEvidenceMetaV1;

prediction_evidence_entry#50454531
  schema_version:uint16
  source_kind:uint8
  canonical_source_id:^PredictionCanonicalTextV1
  archive_locator:^PredictionCanonicalTextV1
  parser_profile_version:^PredictionCanonicalTextV1
  meta:^PredictionEvidenceMetaV1
  = PredictionEvidenceEntryV1;
```

Text is nonempty printable ASCII `0x21..0x7e`; whitespace, NUL, snake cells and
Unicode aliases are rejected. Maximum lengths are 120 bytes for source ID and
96 bytes each for locator and parser profile.

Canonical source identities are:

- HTTPS: an absolute lowercase-host `https://` URL with no userinfo, port,
  query, fragment, percent-encoded raw path, repeated slash, dot segment, or
  trailing host dot.
- signed document: `ed25519:<64 lowercase hex>`, where the key passes the
  Prediction Ed25519 point and 8-torsion admission profile.
- finalized TOS source: `tos-account:<canonical raw addr_std>` in workchain
  `-1` or `0`.

The only V1 archive locator is
`tos-cas-sha256:<content_digest lowercase hex>`. Replica endpoints are local
policy and cannot change the manifest root. A reporter retrieves the exact
bytes from at least two administratively independent replicas and recomputes
the digest before voting.

`event_time_seconds` and `publication_time_seconds` are authoritative source
metadata, not local fetch times. Both are nonzero and event time cannot exceed
publication time. Parser profiles use
`[a-z][a-z0-9.-]{0,47}/v[1-9][0-9]{0,8}`.

## 2. Canonical bounded tree

Entries sort uniquely by the byte tuple
`(source_kind, canonical_source_id, content_digest)`. Duplicate tuples fail.
The count is `1..32`.

```text
prediction_evidence_leaf#50454c31 schema_version:uint16 is_leaf:Bool=1
  count:uint8=1 entry:^PredictionEvidenceEntryV1 = PredictionEvidenceTreeV1;

prediction_evidence_branch#50454c31 schema_version:uint16 is_leaf:Bool=0
  count:uint8 left:^PredictionEvidenceTreeV1 right:^PredictionEvidenceTreeV1
  = PredictionEvidenceTreeV1;
```

For `n > 1`, the only canonical split is `left_count=floor(n/2)` and
`right_count=n-left_count`, recursively. Count commitments and canonical
re-encoding reject alternate shapes. Any complete evidence object is limited
to 256 distinct cells and depth 16; a 32-entry canonical tree fits both.

## 3. Normal or appellate evidence

```text
prediction_evidence_binding$_
  market_id:uint256 rules_hash:uint256 round_context_hash:uint256
  = PredictionEvidenceBindingV1;

prediction_evidence_manifest#50454d31
  schema_version:uint16 outcome:uint8 entry_count:uint8
  binding:^PredictionEvidenceBindingV1
  entries:^PredictionEvidenceTreeV1
  = PredictionEvidenceManifestV1;
```

All three binding hashes are nonzero. `outcome` is YES, NO or INVALID.
`evidence_root = cell_hash(PredictionEvidenceManifestV1)`.

## 4. Challenge evidence

```text
prediction_challenge_binding$_
  market_id:uint256 rules_hash:uint256 proposed_statement_hash:uint256
  = PredictionChallengeEvidenceBindingV1;

prediction_challenge_evidence#50434531
  schema_version:uint16 counter_outcome:uint8 entry_count:uint8
  binding:^PredictionChallengeEvidenceBindingV1
  entries:^PredictionEvidenceTreeV1
  = PredictionChallengeEvidenceManifestV1;
```

The challenge manifest uses a distinct magic and binds the exact proposed
statement and counter outcome. It intentionally does not contain a review base
or vote-context hash: those objects contain the accepted counter evidence root,
so adding them here would create a recursive hash definition. After acceptance,
the contract-authenticated challenger address and this root enter the review
base context.

V1 challenges only an economically different outcome. The chain validates the
nonzero root and bounded message; reporter policy and monitoring enforce two
replicas through `claim_deadline + AUDIT_RETENTION`.

## 5. What evidence does not prove

A manifest proves byte identity, source identity, frozen parser selection and
quorum agreement. It does not make an HTTPS source truthful, prove that a
language model reasoned correctly, or replace independence among reporter
operators. Market admission must reject ambiguous political questions whose
frozen source hierarchy and rules cannot deterministically select YES, NO, or
factual INVALID.
