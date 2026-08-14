#!/usr/bin/env python3
"""Independent stdlib-only reproducer for the frozen manifest vector."""

import base64
import copy
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VECTOR = ROOT / "test-vectors/software-work-manifest-v1.json"
HEX32 = re.compile(r"^[0-9a-f]{64}$")


def head(major, value):
    if value < 24:
        return bytes([(major << 5) | value])
    if value <= 0xFF:
        return bytes([(major << 5) | 24, value])
    if value <= 0xFFFF:
        return bytes([(major << 5) | 25]) + value.to_bytes(2, "big")
    if value <= 0xFFFFFFFF:
        return bytes([(major << 5) | 26]) + value.to_bytes(4, "big")
    return bytes([(major << 5) | 27]) + value.to_bytes(8, "big")


def cbor(value):
    if isinstance(value, bool):
        return bytes([0xF5 if value else 0xF4])
    if isinstance(value, int):
        return head(0, value) if value >= 0 else head(1, -1 - value)
    if isinstance(value, str):
        encoded = value.encode("utf-8")
        return head(3, len(encoded)) + encoded
    if isinstance(value, list):
        return head(4, len(value)) + b"".join(cbor(item) for item in value)
    if isinstance(value, dict):
        entries = sorted(((cbor(key), cbor(item)) for key, item in value.items()), key=lambda item: (len(item[0]), item[0]))
        return head(5, len(entries)) + b"".join(key + item for key, item in entries)
    raise TypeError(f"unsupported CBOR value {type(value)!r}")


ROOT_KEYS = [
    "protocol", "version", "name", "description", "operation", "accepted_source_kinds",
    "input_schema_digest", "output_schema_digest", "toolchain_digest", "invocation",
    "network_policy", "limits", "artifact_media_types", "report_media_types",
    "success_condition", "refund_conditions", "endpoint_commitment",
    "execution_signer_authorization", "retention_seconds", "supported_assets",
]
INVOCATION_KEYS = ["executable", "arguments", "working_directory"]
LIMIT_KEYS = ["cpu_millis", "memory_bytes", "scratch_bytes", "output_bytes", "wall_clock_millis"]
ASSET_KEYS = ["workchain", "master_account_id", "master_code_hash", "wallet_code_hash", "decimals"]


def exact_keys(value, keys):
    if set(value) != set(keys):
        raise ValueError(f"unexpected or missing fields: {sorted(set(value) ^ set(keys))}")


def integer_map(value, keys):
    exact_keys(value, keys)
    return {index + 1: value[key] for index, key in enumerate(keys)}


def validate(manifest):
    exact_keys(manifest, ROOT_KEYS)
    if manifest["protocol"] != "atos.software-work-manifest.v1":
        raise ValueError("protocol")
    if manifest["invocation"]["executable"].rsplit("/", 1)[-1].lower() in {"sh", "bash", "dash", "zsh", "cmd.exe", "powershell"}:
        raise ValueError("shell")
    if manifest["network_policy"] != "none" or not manifest["limits"]["cpu_millis"]:
        raise ValueError("network or limits")
    if manifest["refund_conditions"] != sorted(set(manifest["refund_conditions"])):
        raise ValueError("refund conditions")
    for asset in manifest["supported_assets"]:
        exact_keys(asset, ASSET_KEYS)
        if asset["workchain"] != 0 or not HEX32.fullmatch(asset["master_account_id"]) or not asset["decimals"]:
            raise ValueError("asset")


def canonical_model(manifest):
    validate(manifest)
    result = integer_map(copy.deepcopy(manifest), ROOT_KEYS)
    result[10] = integer_map(manifest["invocation"], INVOCATION_KEYS)
    result[12] = integer_map(manifest["limits"], LIMIT_KEYS)
    result[20] = [integer_map(asset, ASSET_KEYS) for asset in manifest["supported_assets"]]
    return result


def mutate(manifest, name):
    candidate = copy.deepcopy(manifest)
    if name == "add_capability_id": candidate["capability_id"] = "cap_" + "aa" * 32
    elif name == "wrong_protocol": candidate["protocol"] = "atos.software-work-manifest.v0"
    elif name == "shell_executable": candidate["invocation"]["executable"] = "/bin/sh"
    elif name == "network_enabled": candidate["network_policy"] = "full"
    elif name == "zero_cpu_limit": candidate["limits"]["cpu_millis"] = 0
    elif name == "unsorted_refund_conditions": candidate["refund_conditions"][0:2] = reversed(candidate["refund_conditions"][0:2])
    elif name == "ticker_only_asset": candidate["supported_assets"][0]["master_account_id"] = "USDT"
    elif name == "zero_asset_decimals": candidate["supported_assets"][0]["decimals"] = 0
    else: raise ValueError(f"unknown mutation {name}")
    return candidate


def main():
    vector = json.loads(VECTOR.read_text())
    encoded = cbor(canonical_model(vector["manifest"]))
    digest = "sha256:" + hashlib.sha256(encoded).hexdigest()
    if digest != vector["expected"]["digest"] or base64.b64encode(encoded).decode() != vector["expected"]["canonical_cbor_base64"]:
        raise SystemExit("frozen manifest vector mismatch")
    for name in vector["negative_mutations"]:
        try:
            validate(mutate(vector["manifest"], name))
        except ValueError:
            continue
        raise SystemExit(f"negative mutation accepted: {name}")
    print(f"software-work manifest v1 vector: PASS ({digest})")


if __name__ == "__main__":
    main()
