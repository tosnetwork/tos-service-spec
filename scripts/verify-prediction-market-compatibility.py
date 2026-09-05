#!/usr/bin/env python3
"""Fail closed on accidental edits to the PredictionMarket V1 release tuple."""

import hashlib
import json
import re
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


def main():
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

    print("prediction-market compatibility manifest: PASS")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise SystemExit(f"prediction-market compatibility manifest: FAIL: {error}")
