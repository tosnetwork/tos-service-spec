#!/usr/bin/env bash
set -euo pipefail

workspace=${TOS_WORKSPACE:-$(cd "$(dirname "$0")/../.." && pwd)}
artifacts=${ACCEPTANCE_ARTIFACT_DIR:-$(mktemp -d /tmp/openfox-autonomous-earning.XXXXXX)}
mkdir -p "$artifacts/logs" "$artifacts/source-loss"
chmod 700 "$artifacts" "$artifacts/logs" "$artifacts/source-loss"

rpc1=${OPENFOX_TOS_RPC_1:-http://127.0.0.1:8011/}
rpc2=${OPENFOX_TOS_RPC_2:-http://127.0.0.1:8012/}
rpc3=${OPENFOX_TOS_RPC_3:-http://127.0.0.1:8013/}
tosctl=${OPENFOX_TOSCTL:-$workspace/tos/tosctl/src/target/debug/tosctl}
tosctl_config=${OPENFOX_TOSCTL_PRIMARY_CONFIG:-$workspace/tos/test/integration/.agent-economic-payment-three-node-e2e/tosctl-node1.json}
vault_url=${VAULT_URL:-file://$workspace/tos/test/integration/.agent-economic-payment-three-node-e2e/e2e-vault.json?master_key=0000000000000000000000000000000000000000000000000000000000000010}

require_file() {
  if [[ ! -f "$1" ]]; then
    printf 'acceptance: required file is missing: %s\n' "$1" >&2
    exit 1
  fi
}

require_file "$tosctl"
require_file "$tosctl_config"

for endpoint in "$rpc1" "$rpc2" "$rpc3"; do
  response=$(curl --fail --silent --show-error --max-time 5 \
    --header 'content-type: application/json' \
    --data '{"jsonrpc":"2.0","id":1,"method":"getMasterchainInfo","params":[]}' \
    "$endpoint")
  if [[ "$response" != *'"result"'* ]]; then
    printf 'acceptance: TOS endpoint is not ready: %s\n' "$endpoint" >&2
    exit 1
  fi
done

python3 "$workspace/tos-service-spec/scripts/agent-commerce-reference.py" \
  | tee "$artifacts/logs/independent-verifier.log"

(cd "$workspace/tos-service-protocol" && go test ./pkg/agentcommerce ./pkg/buyersdk ./pkg/executiongate ./pkg/nativecore ./pkg/paiddemand ./pkg/toschain) \
  | tee "$artifacts/logs/protocol.log"
(cd "$workspace/tos-messenger" && go test ./pkg/economicaction ./pkg/intentcarrier ./pkg/negotiation ./pkg/localapi) \
  | tee "$artifacts/logs/messenger.log"
(cd "$workspace/tos-service-gateway" && go test ./internal/intentcarrier ./internal/quotesource) \
  | tee "$artifacts/logs/gateway.log"
(cd "$workspace/tos-ai" && go test ./pkg/commercegate ./pkg/privateingress ./pkg/messengereventbridge) \
  | tee "$artifacts/logs/executor.log"
(cd "$workspace/openfox" && go test -tags goolm,stdjson ./pkg/earning ./cmd/openfox/internal/earning) \
  | tee "$artifacts/logs/openfox.log"

"$workspace/tos/scripts/test-tos-service-stablecoin-escrow-v2.sh" \
  | tee "$artifacts/logs/escrow-reproducibility.log"
(cd "$workspace/tos/tosctl/src" && cargo test -p contracts --test tos_service_stablecoin_escrow_v2_sandbox) \
  | tee "$artifacts/logs/escrow-sandbox.log"

TOS_WORKSPACE="$workspace" ACCEPTANCE_ARTIFACT_DIR="$artifacts/source-loss" \
  "$workspace/tos-service-spec/scripts/run-independent-carrier-source-loss.sh" \
  | tee "$artifacts/logs/source-loss.log"

(cd "$workspace/openfox" && \
  OPENFOX_PAID_DEMAND_LIFECYCLE_THREE_NODE_E2E=1 \
  OPENFOX_TOS_RPC_1="$rpc1" OPENFOX_TOS_RPC_2="$rpc2" OPENFOX_TOS_RPC_3="$rpc3" \
  OPENFOX_TOS_REPO="$workspace/tos" \
  OPENFOX_TOSCTL="$tosctl" OPENFOX_TOSCTL_PRIMARY_CONFIG="$tosctl_config" \
  VAULT_URL="$vault_url" \
  go test -tags goolm,stdjson ./pkg/earning \
    -run '^TestPaidDemandAutonomousLifecycleThreeNode$' -count=1 -v) \
  | tee "$artifacts/logs/three-node-lifecycle.log"

{
  printf 'schema=tos.openfox.autonomous-earning-acceptance.v1\n'
  printf 'completed_at_utc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  for repository in tos-service-spec tos-service-protocol openfox tos-messenger tos-service-gateway tos-ai tos; do
    printf '%s_commit=%s\n' "$repository" "$(git -C "$workspace/$repository" rev-parse HEAD)"
    if [[ -n "$(git -C "$workspace/$repository" status --porcelain --untracked-files=all)" ]]; then
      printf '%s_worktree=modified\n' "$repository"
    else
      printf '%s_worktree=clean\n' "$repository"
    fi
  done
  printf 'tos_endpoints=%s,%s,%s\n' "$rpc1" "$rpc2" "$rpc3"
  printf 'result=passed\n'
} >"$artifacts/manifest.txt"

printf 'acceptance=passed profile=three-node-paid-demand-v2 artifacts=%s\n' "$artifacts"
