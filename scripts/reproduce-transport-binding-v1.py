#!/usr/bin/env python3
"""Independent stdlib-only reproducer for the frozen transport binding vectors.

It rebuilds every entry's two cells from its fields, recomputes the cell hash,
serializes the bag of cells (with CRC32C) and compares it with the frozen BOC,
and checks the validity rules of ACCEPTED_QUOTE_TVM_V1 for every entry.
"""

import base64
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


def cells(mode: int, maximum: int, base_url: str):
    encoded = base_url.encode("ascii")
    if len(encoded) > 127:
        raise ValueError("base URL does not fit one cell")
    url_bits = "".join(bits(byte, 8) for byte in encoded)
    root_bits = bits(0x4E544231, 32) + bits(1, 16) + bits(mode, 8) + bits(maximum, 32)
    return root_bits, url_bits


def binding_hash(mode: int, maximum: int, base_url: str) -> str:
    root_bits, url_bits = cells(mode, maximum, base_url)
    url_hash = cell_hash(url_bits, [])
    return "sha256:" + cell_hash(root_bits, [(0, url_hash)]).hex()


def crc32c(data: bytes) -> int:
    crc = 0xFFFFFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            crc = (crc >> 1) ^ (0x82F63B78 if crc & 1 else 0)
    return crc ^ 0xFFFFFFFF


def serialized(data_bits: str, refs: list) -> bytes:
    bit_length = len(data_bits)
    padded = data_bits
    if bit_length % 8:
        padded += "1" + "0" * (7 - bit_length % 8)
    data = int(padded, 2).to_bytes(len(padded) // 8, "big") if padded else b""
    return bytes([len(refs), (bit_length + 7) // 8 + bit_length // 8]) + data + bytes(refs)


def binding_boc(mode: int, maximum: int, base_url: str) -> bytes:
    """Bag of cells: root first, then the URL cell; one-byte sizes, CRC32C."""
    root_bits, url_bits = cells(mode, maximum, base_url)
    body = serialized(root_bits, [1]) + serialized(url_bits, [])
    offset_bytes = max(1, (len(body).bit_length() + 7) // 8)
    header = bytes.fromhex("b5ee9c72") + bytes([0x40 | 1, offset_bytes]) + bytes([2, 1, 0])
    header += len(body).to_bytes(offset_bytes, "big") + bytes([0])
    boc = header + body
    return boc + crc32c(boc).to_bytes(4, "little")


def valid(mode: int, maximum: int, base_url: str) -> bool:
    if maximum == 0 or maximum > MAX_REQUEST or len(base_url) > 120 or base_url.endswith("/"):
        return False
    if not all(0x20 < ord(char) < 0x7F for char in base_url):
        return False
    if mode == 2:
        return maximum <= MAX_AGENT_PACKET_REQUEST and bool(AGENT_PACKET.match(base_url))
    if mode == 0:
        match = re.match(r"^http://(127\.0\.0\.1|localhost|\[::1\])(:[0-9]+)?(?P<path>.*)$", base_url)
    elif mode == 1:
        match = re.match(r"^https://[a-z0-9.-]+(:[0-9]+)?(?P<path>.*)$", base_url)
    else:
        return False
    return match is not None and valid_path_prefix(match.group("path"))


def valid_path_prefix(path: str) -> bool:
    """An optional path prefix: "/"-separated non-empty segments of RFC 3986
    unreserved characters with no dot segments. Credentials, query, fragment,
    escapes and a trailing slash are refused."""
    if re.fullmatch(r"(/[A-Za-z0-9._~-]+)*", path) is None:
        return False
    return all(segment not in (".", "..") for segment in path.split("/")[1:])


def main() -> int:
    vector = json.loads(VECTOR.read_text())
    if vector["schema"] != "tos.service.transport-binding.v1.vectors":
        print("unexpected schema", file=sys.stderr)
        return 1
    failures = 0
    for entry in vector["valid"] + vector["invalid"]:
        boc = binding_boc(entry["security_mode"], entry["max_request_bytes"], entry["base_url"])
        if base64.b64decode(entry["boc_base64"], validate=True) != boc:
            print(f"entry {entry['name']} BOC does not reproduce", file=sys.stderr)
            failures += 1
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
