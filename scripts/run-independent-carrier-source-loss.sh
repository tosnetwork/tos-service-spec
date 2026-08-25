#!/usr/bin/env bash
set -euo pipefail

workspace=${TOS_WORKSPACE:-$(cd "$(dirname "$0")/../.." && pwd)}
artifacts=${ACCEPTANCE_ARTIFACT_DIR:-$(mktemp -d /tmp/tos-carrier-source-loss.XXXXXX)}
mkdir -p "$artifacts/bin" "$artifacts/logs"
chmod 700 "$artifacts" "$artifacts/bin" "$artifacts/logs"

gateway_pid=
messenger_pid=
stop_processes() {
  if [[ -n "$gateway_pid" ]]; then kill "$gateway_pid" 2>/dev/null || true; fi
  if [[ -n "$messenger_pid" ]]; then kill "$messenger_pid" 2>/dev/null || true; fi
  if [[ -n "$gateway_pid" ]]; then wait "$gateway_pid" 2>/dev/null || true; fi
  if [[ -n "$messenger_pid" ]]; then wait "$messenger_pid" 2>/dev/null || true; fi
}
trap stop_processes EXIT INT TERM

(cd "$workspace/tos-service-protocol" && go build -o "$artifacts/bin/campaign" ./cmd/agent-commerce-carrier-campaign)
(cd "$workspace/tos-service-gateway" && go build -o "$artifacts/bin/gateway-carrier" ./cmd/tos-service-intent-carrierd)
(cd "$workspace/tos-messenger" && go build -o "$artifacts/bin/messenger-carrier" ./cmd/tos-intent-carrierd)

init_output=$($artifacts/bin/campaign --init-dir "$artifacts/control")
printf '%s\n' "$init_output" >"$artifacts/logs/init.log"
pin=$(printf '%s\n' "$init_output" | sed -n 's/.*authority_pin=\([^ ]*\).*/\1/p')
if [[ -z "$pin" ]]; then
  echo "carrier acceptance: campaign did not produce an authority pin" >&2
  exit 1
fi

gateway_id=carrier:gateway-independent
messenger_id=carrier:messenger-independent
gateway_endpoint=http://127.0.0.1:18091
messenger_endpoint=http://127.0.0.1:18092
read_token=$artifacts/control/read.token
write_token=$artifacts/control/write.token

"$artifacts/bin/gateway-carrier" \
  --state "$artifacts/gateway" --carrier-id "$gateway_id" --listen 127.0.0.1:18091 \
  --read-token-file "$read_token" --write-token-file "$write_token" \
  --authority "authority:carrier-campaign=$pin" >"$artifacts/logs/gateway.log" 2>&1 &
gateway_pid=$!
"$artifacts/bin/messenger-carrier" \
  --state "$artifacts/messenger" --carrier-id "$messenger_id" --listen 127.0.0.1:18092 \
  --read-token-file "$read_token" --write-token-file "$write_token" \
  --authority "authority:carrier-campaign=$pin" >"$artifacts/logs/messenger.log" 2>&1 &
messenger_pid=$!

for _ in $(seq 1 100); do
  if grep -q 'ready=true' "$artifacts/logs/gateway.log" 2>/dev/null && grep -q 'ready=true' "$artifacts/logs/messenger.log" 2>/dev/null; then
    break
  fi
  if ! kill -0 "$gateway_pid" 2>/dev/null || ! kill -0 "$messenger_pid" 2>/dev/null; then
    echo "carrier acceptance: a Carrier exited before readiness" >&2
    exit 1
  fi
  sleep 0.05
done
grep -q 'ready=true' "$artifacts/logs/gateway.log"
grep -q 'ready=true' "$artifacts/logs/messenger.log"

common=(--authority-key "$artifacts/control/authority.key" --issuer-key "$artifacts/control/issuer.key"
  --digest-file "$artifacts/control/intent.digest")
gateway=(--carrier "$gateway_id,$gateway_endpoint,$read_token,$write_token")
messenger=(--carrier "$messenger_id,$messenger_endpoint,$read_token,$write_token")
"$artifacts/bin/campaign" "${common[@]}" "${gateway[@]}" "${messenger[@]}" | tee "$artifacts/logs/publish-and-verify.log"

# Remove the entire first Carrier store from its active failure domain. Moving
# it preserves forensic evidence while proving the second implementation does
# not depend on the first database.
kill "$gateway_pid"
wait "$gateway_pid" || true
gateway_pid=
mv "$artifacts/gateway" "$artifacts/gateway.database-removed"

"$artifacts/bin/campaign" --verify-only --digest-file "$artifacts/control/intent.digest" \
  "${messenger[@]}" | tee "$artifacts/logs/after-source-loss.log"

kill "$messenger_pid"
wait "$messenger_pid" || true
messenger_pid=
"$artifacts/bin/messenger-carrier" \
  --state "$artifacts/messenger" --carrier-id "$messenger_id" --listen 127.0.0.1:18092 \
  --read-token-file "$read_token" --write-token-file "$write_token" \
  --authority "authority:carrier-campaign=$pin" >>"$artifacts/logs/messenger.log" 2>&1 &
messenger_pid=$!
for _ in $(seq 1 100); do
  if [[ $(grep -c 'ready=true' "$artifacts/logs/messenger.log" 2>/dev/null || true) -ge 2 ]]; then break; fi
  sleep 0.05
done
"$artifacts/bin/campaign" --verify-only --digest-file "$artifacts/control/intent.digest" \
  "${messenger[@]}" | tee "$artifacts/logs/after-restart.log"

printf 'acceptance=passed independent_carriers=2 removed_store=gateway surviving_store=messenger artifacts=%s\n' "$artifacts"
