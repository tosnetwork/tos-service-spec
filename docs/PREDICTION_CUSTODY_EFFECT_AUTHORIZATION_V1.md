# Prediction Custody Effect Authorization V1

Status: release candidate / incubation profile.

This object is the owner-custody capability for one exact PredictionMarket V1
call sent through an Agent Account checked-contract-call v2 action. It is distinct
from an order authorization, an OpenFox Intent, and the escrow custody effect
schema. No field from an Agreement or escrow obligation is synthesized to use
this profile.

## 1. Security boundary

The authorization permits exactly one semantic action and one TVM effect. It
binds:

- the owner authority, Agent, current writer generation and writer-fence
  digest;
- the full TOS network domain and source Agent Account;
- the audited Agent Account code hash and checked-call v2 transport;
- the immutable market ID, address, config hash and code hash;
- the exact destination value and canonical body cell hash; and
- the stable semantic action ID, exact request digest and expiry.

The destination is necessarily the bound market address. StateInit is forbidden
by the V1 checked-call transport. The signer must resolve finalized chain state
and verify both source and destination code hashes before signing; caller
claims are not proof of deployed code.

## 2. Closed action union

The `effect_kind` and `action_kind` fields must be equal and one of:

```text
prediction.collateral.deposit
prediction.reserve.top-up
prediction.trading-key.rotate
prediction.order.cancel-exact
prediction.order.nonce-floor.raise
prediction.match.submit
prediction.position.split
prediction.position.merge
prediction.position.claim
prediction.collateral.withdraw
prediction.resolution.report
prediction.resolution.challenge
prediction.resolution.finalize
prediction.challenge-bond.withdraw
prediction.market.advance-phase
prediction.market.compact
prediction.terminal-surplus.withdraw
```

`prediction.market.deploy` uses the separately reviewed deployment custody
path because the checked-call transport forbids StateInit. The off-chain-only
`prediction.order.authorize` and `prediction.order.publish` kinds can never
enter this union. Adding a kind requires a new reviewed schema/profile version;
prefix matching `prediction.*` is prohibited.

## 3. Canonical body

The signed JSON representation uses the following exact closed field set in
this order for the binary signature preimage:

```text
schema_version                 uint16 = 1
profile                        UTF-8 = "tos.prediction.checked-call.v1"
authority_id                  LP32 UTF-8
owner_id                      LP32 UTF-8
agent_id                      LP32 UTF-8
source_account                LP32 canonical std address
source_agent_account_code_hash LP32 "tvm-cell-sha256:" + 64 lowercase hex
network_domain                CustodyNetworkDomainV1
action_kind                   LP32 closed token
effect_kind                   LP32, equal to action_kind
stable_action_id              LP32 "sha256:" + 64 lowercase hex
exact_request_digest          LP32 "sha256:" + 64 lowercase hex
writer_generation             uint64, nonzero
writer_fence_digest           LP32 "sha256:" + 64 lowercase hex
policy_revision               uint64, nonzero
mandate_digest                LP32 "sha256:" + 64 lowercase hex
approval_digest_or_zero       LP32 canonical digest or all-zero digest
market_id                     LP32 "sha256:" + 64 lowercase hex
market_address                LP32 canonical std address
market_config_hash            LP32 "tvm-cell-sha256:" + 64 lowercase hex
market_code_hash              LP32 "tvm-cell-sha256:" + 64 lowercase hex
amount_nanotos                uint64, 1..2^48-1
body_hash                     LP32 "tvm-cell-sha256:" + 64 lowercase hex
expires_at_unix               uint64, nonzero
```

`CustodyNetworkDomainV1` is the existing canonical `network_id`, `global_id`,
genesis block root/file hashes and target workchain tuple. Canonical string
limits and address parsing are enforced before signing.

The preimage is:

```text
"TOS-PCEA\0" || fields_above
```

The signature digest is `SHA256(preimage)`. `public_key` is canonical
`ed25519:` plus 64 lowercase hex and `proof` is canonical `ed25519:` plus 128
lowercase hex. Neither is included in the preimage.

## 4. Verification

A production verifier must:

1. strictly decode with unknown fields rejected;
2. validate the closed action union before signature work;
3. resolve the current custody key for the exact authority/owner/Agent tuple;
4. reject at or after `expires_at_unix`;
5. verify the full network domain and finalized source/destination code hashes;
6. rederive the semantic stable ID and exact request digest;
7. parse the actual canonical body cell and compare its cell hash;
8. require Agent Account opcode `0x41475007`, flags `3`, no StateInit, the same
   target/value/body, controller epoch/seqno and expiry; and
9. persist the exact signed external BOC before any broadcast.

An escrow authorization, legacy Agent Account action, Intent signature, order
signature, unmatched body digest, unknown action kind, or code hash claim is
never accepted as a substitute.
