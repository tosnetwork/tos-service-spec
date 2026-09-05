#!/usr/bin/env python3
"""Fail closed on accidental edits to the PredictionMarket V1 release tuple."""

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "prediction-market-v1-compatibility.json"
VECTOR_DIRECTORY = ROOT / "test-vectors"
CELL_HASH = re.compile(r"^tvm-cell-sha256:[0-9a-f]{64}$")
OPCODE = re.compile(r"^0x[0-9a-f]{8}$")

RISK_INCREASING = ["0x504d0001", "0x504d0002", "0x504d0003", "0x504d0007", "0x504d0009"]
EXIT_OPCODES = [f"0x504d{value:04x}" for value in range(4, 7)] + [
    "0x504d0008",
    *[f"0x504d{value:04x}" for value in range(10, 26)],
]
EXPECTED_ACTIONS = [
    "prediction.challenge-bond.withdraw", "prediction.collateral.deposit",
    "prediction.collateral.withdraw", "prediction.market.advance-phase",
    "prediction.market.compact", "prediction.market.deploy", "prediction.match.submit",
    "prediction.order.authorize", "prediction.order.cancel-exact",
    "prediction.order.nonce-floor.raise", "prediction.order.publish", "prediction.position.claim",
    "prediction.position.merge", "prediction.position.split", "prediction.reserve.top-up",
    "prediction.resolution.challenge", "prediction.resolution.finalize",
    "prediction.resolution.report", "prediction.terminal-surplus.withdraw",
    "prediction.trading-key.rotate",
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256_file(path):
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def run_json(command, cwd=None):
    completed = subprocess.run(command, cwd=cwd, check=False, text=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if completed.returncode:
        raise ValueError(f"command failed ({' '.join(command)}): {completed.stderr.strip()}")
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise ValueError(f"command did not return JSON ({' '.join(command)}): {error}") from error


def verify_checkout_tuple(document, tosctl, protocol_root, openfox_root):
    market = document["prediction_market"]
    account = document["agent_account"]
    capabilities = run_json([str(tosctl), "agent", "prediction", "capabilities"])
    require(capabilities == {
        "schema": "tos.prediction-market-cli-capabilities.v1",
        "contract_version": market["contract_code_version"], "code_hash": market["code_hash"],
        "minimum_global_version": market["minimum_global_version"],
        "full_risk_global_versions": market["full_risk_global_versions"],
        "prepared_artifact": "exact-signed-external-message-boc",
        "get_methods": ["get_prediction_state", "get_prediction_accounting", "get_prediction_account",
                        "get_prediction_order", "get_market_phase", "get_resolution_contexts"],
    }, "tosctl Prediction capability tuple drifted")
    template = run_json([str(tosctl), "agent", "account", "show-template", "--format", "json"])
    require(template.get("code_hash") == account["code_hash"].removeprefix("tvm-cell-sha256:") and
            template.get("checked_contract_call_v2_opcode") == account["checked_contract_call"]["opcode"],
            "Agent Account template tuple drifted")

    registry = protocol_root / "pkg" / "agentcommerce" / "semantic_action.go"
    registered = re.findall(r'entry\("(prediction\.[a-z0-9.-]+)"', registry.read_text(encoding="utf-8"))
    require(sorted(registered) == [entry["action_kind"] for entry in document["semantic_action_registry"]["entries"]],
            "protocol Prediction semantic registry drifted")
    for root, packages in ((protocol_root, ["./pkg/predictionmarket", "./pkg/agentcommerce"]),
                           (openfox_root, ["./pkg/prediction", "./pkg/earning"])):
        completed = subprocess.run(["go", "test", *packages], cwd=root, check=False, text=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if completed.returncode:
            raise ValueError(f"cross-repository tests failed in {root}: {completed.stderr.strip()}")


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tosctl", type=Path, help="current tosctl binary")
    parser.add_argument("--protocol-root", type=Path, help="tos-service-protocol checkout")
    parser.add_argument("--openfox-root", type=Path, help="OpenFox checkout")
    args = parser.parse_args()
    supplied = [args.tosctl, args.protocol_root, args.openfox_root]
    if any(supplied) and not all(supplied):
        parser.error("--tosctl, --protocol-root, and --openfox-root must be supplied together")
    return args


def main():
    args = parse_args()
    document = json.loads(MANIFEST.read_text(encoding="utf-8"))
    require(set(document) == {
        "schema", "manifest_version", "prediction_market", "agent_account",
        "semantic_action_registry", "protocol_vectors",
    }, "manifest fields are not closed")
    require(document["schema"] == "tos.prediction-market-compatibility.v1" and
            document["manifest_version"] == 1, "unsupported manifest version")

    market = document["prediction_market"]
    require(set(market) == {
        "contract_code_version", "code_hash", "minimum_global_version",
        "full_risk_global_versions", "risk_increasing_opcodes",
        "unknown_higher_version_exit_opcodes",
    }, "PredictionMarket fields are not closed")
    require(market["contract_code_version"] == 1 and CELL_HASH.fullmatch(market["code_hash"]),
            "invalid PredictionMarket identity")
    require(market["minimum_global_version"] == 14 and
            market["full_risk_global_versions"] == [14, 15], "invalid audited global-version set")
    require(market["risk_increasing_opcodes"] == RISK_INCREASING,
            "risk-increasing opcode set changed")
    require(market["unknown_higher_version_exit_opcodes"] == EXIT_OPCODES and
            all(OPCODE.fullmatch(opcode) for opcode in EXIT_OPCODES),
            "unknown-version exit opcode set changed")
    require(not set(RISK_INCREASING) & set(EXIT_OPCODES), "risk and exit opcode sets overlap")

    account = document["agent_account"]
    require(set(account) == {"code_hash", "checked_contract_call"} and
            CELL_HASH.fullmatch(account["code_hash"]), "invalid Agent Account identity")
    checked_call = account["checked_contract_call"]
    require(checked_call == {"opcode": "0x41475007", "extra_flags": 3,
                             "state_init_forbidden": True},
            "checked-call transport changed")

    registry = document["semantic_action_registry"]
    require(set(registry) == {"registry_version", "entries"} and registry["registry_version"] == 1,
            "invalid semantic registry version")
    entries = registry["entries"]
    require(isinstance(entries, list) and len(entries) == len(EXPECTED_ACTIONS),
            "semantic registry entry count changed")
    actions = [entry.get("action_kind") for entry in entries if set(entry) == {"action_kind", "entry_version"} and
               entry.get("entry_version") == 1]
    require(actions == EXPECTED_ACTIONS and actions == sorted(actions),
            "semantic registry entries changed or are not canonical")

    vectors = document["protocol_vectors"]
    require(set(vectors) == {"prediction-market-v1.json", "agent-commerce-semantic-action-v1.json"},
            "protocol vector set changed")
    for name, digest in vectors.items():
        require(sha256_file(VECTOR_DIRECTORY / name) == digest, f"vector digest drifted: {name}")

    if args.tosctl:
        require(args.tosctl.is_file() and args.tosctl.is_absolute(), "tosctl must be an absolute regular file")
        require(args.protocol_root.is_dir() and args.openfox_root.is_dir(), "checkout root is unavailable")
        verify_checkout_tuple(document, args.tosctl, args.protocol_root, args.openfox_root)

    print("prediction-market compatibility manifest: PASS" +
          (" (cross-repository tuple verified)" if args.tosctl else ""))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise SystemExit(f"prediction-market compatibility manifest: FAIL: {error}")
