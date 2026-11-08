#!/usr/bin/env python3
"""Independent stdlib-only reproducer for the frozen transport binding vectors.

It recomputes every valid binding's cell hash from its fields and checks the
validity rules of ACCEPTED_QUOTE_TVM_V1 for every valid and invalid entry.
"""

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VECTOR = ROOT / "test-vectors/transport-binding-v1.json"
AGENT_PACKET = re.compile(r"^agent-packet:agent_[0-9a-f]{64}$")
MAX_REQUEST = 16 << 20
MAX_AGENT_PACKET_REQUEST = 1 << 20


def cell_hash(data_bits: str, refs: list) -> bytes:
    """Hash of an ordinary level-0 cell: sha256(d1 d2 data depths hashes)."""
    bit_length = len(data_bits)
    d1 = len(refs)
    d2 = (bit_length + 7) // 8 + bit_length // 8
    padded = data_bits
    if bit_length % 8:
        padded += "1" + "0" * (7 - bit_length % 8)
    data = int(padded, 2).to_bytes(len(padded) // 8, "big") if padded else b""
    representation = bytes([d1, d2]) + data
    for depth, _ in refs:
        representation += depth.to_bytes(2, "big")
    for _, digest in refs:
        representation += digest
    return hashlib.sha256(representation).digest()


def bits(value: int, width: int) -> str:
    return format(value, f"0{width}b")


def binding_hash(mode: int, maximum: int, base_url: str) -> str:
    encoded = base_url.encode("ascii")
    if len(encoded) > 127:
        raise ValueError("base URL does not fit one cell")
    url_hash = cell_hash("".join(bits(byte, 8) for byte in encoded), [])
    root = bits(0x4E544231, 32) + bits(1, 16) + bits(mode, 8) + bits(maximum, 32)
    return "sha256:" + cell_hash(root, [(0, url_hash)]).hex()


def valid(mode: int, maximum: int, base_url: str) -> bool:
    if maximum == 0 or maximum > MAX_REQUEST or len(base_url) > 120 or base_url.endswith("/"):
        return False
    if not all(0x20 < ord(char) < 0x7F for char in base_url):
        return False
    if mode == 2:
        return maximum <= MAX_AGENT_PACKET_REQUEST and bool(AGENT_PACKET.match(base_url))
    if mode == 0:
        return re.match(r"^http://(127\.0\.0\.1|localhost|\[::1\])(:[0-9]+)?$", base_url) is not None
    if mode == 1:
        return re.match(r"^https://[a-z0-9.-]+(:[0-9]+)?$", base_url) is not None
    return False


def main() -> int:
    vector = json.loads(VECTOR.read_text())
    if vector["schema"] != "tos.service.transport-binding.v1.vectors":
        print("unexpected schema", file=sys.stderr)
        return 1
    failures = 0
    for entry in vector["valid"]:
        digest = binding_hash(entry["security_mode"], entry["max_request_bytes"], entry["base_url"])
        if digest != entry["transport_binding_digest"] or not valid(
                entry["security_mode"], entry["max_request_bytes"], entry["base_url"]):
            print(f"valid entry {entry['name']} does not reproduce", file=sys.stderr)
            failures += 1
    for entry in vector["invalid"]:
        if valid(entry["security_mode"], entry["max_request_bytes"], entry["base_url"]):
            print(f"invalid entry {entry['name']} passes the rules", file=sys.stderr)
            failures += 1
    if failures:
        return 1
    print(f"reproduced {len(vector['valid'])} valid and refused {len(vector['invalid'])} invalid transport bindings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
