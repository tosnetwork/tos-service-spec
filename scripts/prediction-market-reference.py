#!/usr/bin/env python3
"""Independent PredictionMarket V1 BOC/hash/signature vector verifier."""

import argparse
import base64
import hashlib
import json
import struct


class ConformanceError(ValueError):
    pass


def _read_uint(raw, position, width):
    if width < 1 or position + width > len(raw):
        raise ConformanceError("truncated BOC integer")
    return int.from_bytes(raw[position:position + width], "big"), position + width


def _crc32c(raw):
    crc = 0xFFFFFFFF
    for value in raw:
        crc ^= value
        for _ in range(8):
            crc = (crc >> 1) ^ (0x82F63B78 if crc & 1 else 0)
    return (~crc) & 0xFFFFFFFF


def parse_single_root_ordinary_boc(encoded):
    try:
        raw = base64.b64decode(encoded, validate=True)
    except Exception as error:
        raise ConformanceError("invalid canonical Base64 BOC") from error
    if len(raw) < 10 or raw[:4] != bytes.fromhex("b5ee9c72"):
        raise ConformanceError("unsupported BOC magic")
    flags = raw[4]
    has_index = bool(flags & 0x80)
    has_crc = bool(flags & 0x40)
    has_cache = bool(flags & 0x20)
    size_bytes = flags & 0x07
    if has_cache or not has_crc or size_bytes == 0:
        raise ConformanceError("fixture BOC must use CRC32C without cache bits")
    offset_bytes = raw[5]
    position = 6
    cell_count, position = _read_uint(raw, position, size_bytes)
    root_count, position = _read_uint(raw, position, size_bytes)
    absent_count, position = _read_uint(raw, position, size_bytes)
    total_size, position = _read_uint(raw, position, offset_bytes)
    if not (cell_count > 0 and root_count == 1 and absent_count == 0):
        raise ConformanceError("fixture BOC must have one root and no absent cells")
    root_index, position = _read_uint(raw, position, size_bytes)
    if root_index >= cell_count:
        raise ConformanceError("invalid BOC root index")
    if has_index:
        position += cell_count * offset_bytes
    cells_end = position + total_size
    if cells_end + 4 != len(raw):
        raise ConformanceError("invalid BOC size or trailing bytes")
    expected_crc = struct.unpack("<I", raw[cells_end:])[0]
    if _crc32c(raw[:cells_end]) != expected_crc:
        raise ConformanceError("invalid BOC CRC32C")

    cells = []
    for index in range(cell_count):
        if position + 2 > cells_end:
            raise ConformanceError("truncated cell descriptor")
        descriptor_one, descriptor_two = raw[position], raw[position + 1]
        position += 2
        reference_count = descriptor_one & 0x07
        exotic = bool(descriptor_one & 0x08)
        has_hashes = bool(descriptor_one & 0x10)
        level_mask = descriptor_one >> 5
        if reference_count > 4 or exotic or has_hashes or level_mask != 0:
            raise ConformanceError("fixture contains a non-ordinary level-zero cell")
        data_bytes = (descriptor_two + 1) // 2
        if position + data_bytes + reference_count * size_bytes > cells_end:
            raise ConformanceError("truncated cell payload")
        payload = raw[position:position + data_bytes]
        position += data_bytes
        if descriptor_two & 1:
            if not payload or payload[-1] == 0:
                raise ConformanceError("invalid top-up bit")
            marker = payload[-1] & -payload[-1]
            if marker == 0 or payload[-1] & (marker - 1):
                raise ConformanceError("non-zero bits after top-up marker")
        references = []
        for _ in range(reference_count):
            reference, position = _read_uint(raw, position, size_bytes)
            if reference <= index or reference >= cell_count:
                raise ConformanceError("BOC references are not topologically ordered")
            references.append(reference)
        cells.append((descriptor_one, descriptor_two, payload, references))
    if position != cells_end:
        raise ConformanceError("cell data length mismatch")

    hashes = [None] * cell_count
    depths = [None] * cell_count
    for index in range(cell_count - 1, -1, -1):
        descriptor_one, descriptor_two, payload, references = cells[index]
        representation = bytearray((descriptor_one, descriptor_two))
        representation.extend(payload)
        depth = 0
        for reference in references:
            child_depth = depths[reference]
            if child_depth is None or child_depth >= 1024:
                raise ConformanceError("invalid child depth")
            representation.extend(child_depth.to_bytes(2, "big"))
            depth = max(depth, child_depth + 1)
        for reference in references:
            representation.extend(hashes[reference])
        depths[index] = depth
        hashes[index] = hashlib.sha256(representation).digest()
    return raw, hashes[root_index]


_P = 2**255 - 19
_L = 2**252 + 27742317777372353535851937790883648493
_D = -121665 * pow(121666, _P - 2, _P) % _P
_I = pow(2, (_P - 1) // 4, _P)


def _recover_x(y, sign):
    if y >= _P:
        return None
    x2 = (y * y - 1) * pow(_D * y * y + 1, _P - 2, _P) % _P
    x = pow(x2, (_P + 3) // 8, _P)
    if (x * x - x2) % _P:
        x = x * _I % _P
    if (x * x - x2) % _P:
        return None
    if (x & 1) != sign:
        x = _P - x
    if x == 0 and sign:
        return None
    return x


def _decode_point(raw):
    if len(raw) != 32:
        return None
    value = int.from_bytes(raw, "little")
    y, sign = value & ((1 << 255) - 1), value >> 255
    x = _recover_x(y, sign)
    return None if x is None else (x, y, 1, x * y % _P)


def _add(left, right):
    x1, y1, z1, t1 = left
    x2, y2, z2, t2 = right
    a = (y1 - x1) * (y2 - x2) % _P
    b = (y1 + x1) * (y2 + x2) % _P
    c = 2 * _D * t1 * t2 % _P
    d = 2 * z1 * z2 % _P
    e, f, g, h = b - a, d - c, d + c, b + a
    return e * f % _P, g * h % _P, f * g % _P, e * h % _P


def _multiply(point, scalar):
    result = (0, 1, 1, 0)
    while scalar:
        if scalar & 1:
            result = _add(result, point)
        point = _add(point, point)
        scalar >>= 1
    return result


_BASE = (_recover_x(4 * pow(5, _P - 2, _P) % _P, 0), 4 * pow(5, _P - 2, _P) % _P, 1, 0)
_BASE = (_BASE[0], _BASE[1], 1, _BASE[0] * _BASE[1] % _P)


def _equal(left, right):
    return (left[0] * right[2] - right[0] * left[2]) % _P == 0 and (left[1] * right[2] - right[1] * left[2]) % _P == 0


def verify_ed25519(public_key, message, signature):
    if len(signature) != 64:
        return False
    public = _decode_point(public_key)
    r_point = _decode_point(signature[:32])
    scalar = int.from_bytes(signature[32:], "little")
    if public is None or r_point is None or scalar >= _L:
        return False
    challenge = int.from_bytes(hashlib.sha512(signature[:32] + public_key + message).digest(), "little") % _L
    # RFC 8032 verification clears the cofactor on both sides.
    left = _multiply(_BASE, scalar * 8)
    right = _multiply(_add(r_point, _multiply(public, challenge)), 8)
    return _equal(left, right)


def verify(path):
    with open(path, "r", encoding="utf-8") as handle:
        document = json.load(handle)
    if set(document) != {"schema", "schema_version", "price_scale", "order_digest", "public_key_hex", "signature_hex", "positive_vectors", "negative_vectors"}:
        raise ConformanceError("unknown or missing vector document field")
    if document["schema"] != "tos.prediction-market-conformance.v1" or document["schema_version"] != 1 or document["price_scale"] != 10000:
        raise ConformanceError("unsupported prediction vector profile")
    names = set()
    positive = {}
    for vector in document["positive_vectors"]:
        if set(vector) != {"name", "logical_fields", "boc_base64", "cell_hash", "boc_sha256"} or vector["name"] in names:
            raise ConformanceError("invalid or duplicate positive vector")
        names.add(vector["name"])
        raw, root_hash = parse_single_root_ordinary_boc(vector["boc_base64"])
        if vector["cell_hash"] != "tvm-cell-sha256:" + root_hash.hex():
            raise ConformanceError("independent cell hash mismatch: " + vector["name"])
        if vector["boc_sha256"] != "sha256:" + hashlib.sha256(raw).hexdigest():
            raise ConformanceError("BOC container digest mismatch: " + vector["name"])
        positive[vector["name"]] = vector
    required = {"prediction-order", "order-authorization", "signed-prediction-order", "normal-round-context",
                "normal-evidence-manifest", "challenge-evidence-manifest", "review-base-context",
                "review-vote-context", "resolution-statement"}
    if names != required:
        raise ConformanceError("positive vector set is not exact")
    authorization_hash = bytes.fromhex(positive["order-authorization"]["cell_hash"].split(":", 1)[1])
    if document["order_digest"] != positive["order-authorization"]["cell_hash"]:
        raise ConformanceError("order digest is not the authorization cell hash")
    public_key = bytes.fromhex(document["public_key_hex"])
    signature = bytes.fromhex(document["signature_hex"])
    if not verify_ed25519(public_key, authorization_hash, signature):
        raise ConformanceError("independent Ed25519 order signature verification failed")
    negative_names = {item.get("name") for item in document["negative_vectors"]}
    if len(negative_names) != len(document["negative_vectors"]) or any(item.get("expected") != "reject" for item in document["negative_vectors"]):
        raise ConformanceError("invalid negative-vector set")
    for item in document["negative_vectors"]:
        if item.get("boc_base64"):
            parse_single_root_ordinary_boc(item["boc_base64"])
    print("PASS: independent PredictionMarket V1 BOC, hash, and Ed25519 vectors")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--vectors", required=True)
    verify(parser.parse_args().vectors)
