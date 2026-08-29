#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 "$root/scripts/trusted-capability-reference.py" \
	--vectors "$root/test-vectors/trusted-capability-owner-control-v1.json" \
	--registry "$root/schemas/trusted-capability-owner-control-v1.json"
python3 "$root/scripts/agent-commerce-reference.py" \
  --registry "$root/schemas/semantic-action-identity-v1.json" \
  --vectors "$root/test-vectors/agent-commerce-semantic-action-v1.json"
python3 -m json.tool "$root/schemas/trusted-capability-owner-control-v1.json" >/dev/null
python3 -m json.tool "$root/schemas/trusted-capability-compatibility-v1.json" >/dev/null
echo "trusted capability V1 specification artifacts verified"
