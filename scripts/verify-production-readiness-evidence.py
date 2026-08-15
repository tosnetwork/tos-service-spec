#!/usr/bin/env python3
"""Fail-closed validator for a completed Gate G evidence record."""

import argparse
import json
import re
import sys
from pathlib import Path

HEX64 = re.compile(r"^(?:sha256|tvm-cell-sha256):[0-9a-f]{64}$")


def reject(message):
    raise ValueError(message)


def require(value, name):
    if not isinstance(value, str) or not value or "REQUIRED" in value or value.startswith("PLACEHOLDER"):
        reject(f"{name} is missing or still a placeholder")
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()
    try:
        raw = args.evidence.read_text(encoding="utf-8")
        value = json.loads(raw)
        if not isinstance(value, dict) or value.get("schema") != "tos.service.production-readiness-evidence.v1":
            reject("unsupported evidence schema")
        if value.get("verdict") != "PASS_PRODUCTION_READINESS_V1":
            reject("evidence is not an accepted production verdict")
        network = value.get("network")
        if not isinstance(network, dict):
            reject("network section is missing")
        for field in ("network_id", "genesis_root_hash", "genesis_file_hash"):
            require(network.get(field), f"network.{field}")
        for field in ("genesis_root_hash", "genesis_file_hash"):
            if not HEX64.fullmatch(network[field]):
                reject(f"network.{field} has invalid digest shape")
        release = value.get("release")
        if not isinstance(release, dict):
            reject("release section is missing")
        for field in ("tos_service_spec_commit", "tos_protocol_commit", "tos_service_gateway_commit", "tos_ai_commit", "signed_manifest_digest"):
            require(release.get(field), f"release.{field}")
        if not HEX64.fullmatch(release["signed_manifest_digest"]):
            reject("signed_manifest_digest has invalid digest shape")
        if release.get("reproducible_builds_match") is not True:
            reject("reproducible builds are not proven identical")
        quorum = value.get("quorum")
        endpoints = quorum.get("endpoints") if isinstance(quorum, dict) else None
        if not isinstance(endpoints, list) or len(endpoints) < 3 or len(set(endpoints)) != len(endpoints):
            reject("quorum requires at least three distinct endpoints")
        if not isinstance(quorum.get("strict_majority"), int) or quorum["strict_majority"] <= len(endpoints) // 2:
            reject("strict majority is invalid")
        if quorum.get("endpoint_diversity_verified") is not True:
            reject("endpoint diversity is not verified")
        controls = value.get("controls")
        required_controls = ("custody_restore_drill", "relay_budget_drill", "load_and_dos_report",
                             "stablecoin_reconciliation", "monitoring_alert_drill", "gateway_failure_drill",
                             "provider_failure_drill", "refund_and_client_recovery_drill")
        if not isinstance(controls, dict):
            reject("controls section is missing")
        for field in required_controls:
            require(controls.get(field), f"controls.{field}")
        signatures = value.get("operator_signatures")
        if not isinstance(signatures, list) or len(signatures) < 3:
            reject("at least three operator signatures are required")
        for index, signature in enumerate(signatures):
            if not isinstance(signature, dict):
                reject(f"operator_signatures[{index}] is invalid")
            for field in ("operator_id", "role", "signature_hex"):
                require(signature.get(field), f"operator_signatures[{index}].{field}")
            if not re.fullmatch(r"[0-9a-f]{128}", signature["signature_hex"]):
                reject(f"operator_signatures[{index}].signature_hex has invalid shape")
        print("PASS production-readiness evidence shape")
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
