#!/usr/bin/env python3
"""Independent ML-DSA-44 (FIPS 204) reference for the TOS service vectors.

Only the Python standard library is used (SHAKE-128/256 from hashlib). The
module implements key generation from a 32-byte seed, the deterministic
signing variant (rnd = 32 zero bytes), and verification, for Pure ML-DSA-44
with a context string. HashML-DSA verification with SHA-256 is included only
so a refusal vector can prove that a pre-hash signature is a valid signature
in its own mode and is still refused as a Pure one.

It is a conformance reference, not a production signer: it is not constant
time and must never hold a real key.

Run with `--self-test VECTOR.json ...` to reproduce signature vectors of the
`tos.agent-guarantor-signature-vector.v1` or
`tos.action-authority-signature-vector.v1` shape byte for byte.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

Q = 8380417
N = 256
D = 13
TAU = 39
LAMBDA_BYTES = 32  # lambda / 4 for lambda = 128
GAMMA1 = 1 << 17
GAMMA2 = (Q - 1) // 88
K = 4
L = 4
ETA = 2
BETA = TAU * ETA
OMEGA = 80

PUBLIC_KEY_BYTES = 32 + 32 * K * 10
SIGNATURE_BYTES = LAMBDA_BYTES + L * 32 * 18 + OMEGA + K
MAX_CONTEXT_BYTES = 255
SHA256_OID = bytes.fromhex("0609608648016503040201")

assert PUBLIC_KEY_BYTES == 1312
assert SIGNATURE_BYTES == 2420


class MLDSAError(ValueError):
    """A malformed ML-DSA-44 input."""


def _shake256(data: bytes, length: int) -> bytes:
    return hashlib.shake_256(data).digest(length)


def _bitrev8(value: int) -> int:
    result = 0
    for _ in range(8):
        result = (result << 1) | (value & 1)
        value >>= 1
    return result


ZETAS = [pow(1753, _bitrev8(index), Q) for index in range(N)]
INVERSE_N = pow(256, Q - 2, Q)


def ntt(poly: list[int]) -> list[int]:
    w = list(poly)
    m = 0
    length = 128
    while length >= 1:
        start = 0
        while start < N:
            m += 1
            zeta = ZETAS[m]
            for j in range(start, start + length):
                t = zeta * w[j + length] % Q
                w[j + length] = (w[j] - t) % Q
                w[j] = (w[j] + t) % Q
            start += 2 * length
        length //= 2
    return w


def inverse_ntt(poly: list[int]) -> list[int]:
    w = list(poly)
    m = N
    length = 1
    while length < N:
        start = 0
        while start < N:
            m -= 1
            zeta = -ZETAS[m] % Q
            for j in range(start, start + length):
                t = w[j]
                w[j] = (t + w[j + length]) % Q
                w[j + length] = zeta * ((t - w[j + length]) % Q) % Q
            start += 2 * length
        length *= 2
    return [value * INVERSE_N % Q for value in w]


def _pointwise(a: list[int], b: list[int]) -> list[int]:
    return [x * y % Q for x, y in zip(a, b)]


def _add(a: list[int], b: list[int]) -> list[int]:
    return [(x + y) % Q for x, y in zip(a, b)]


def _sub(a: list[int], b: list[int]) -> list[int]:
    return [(x - y) % Q for x, y in zip(a, b)]


def _centered(value: int, modulus: int) -> int:
    """value mod± modulus: the representative in (-modulus/2, modulus/2]."""
    r = value % modulus
    if r > modulus // 2:
        r -= modulus
    return r


def _infinity_norm(vector: list[list[int]]) -> int:
    return max(abs(_centered(c, Q)) for poly in vector for c in poly)


def _rej_ntt_poly(seed: bytes) -> list[int]:
    stream = hashlib.shake_128(seed).digest(3 * 1024)
    coefficients: list[int] = []
    offset = 0
    while len(coefficients) < N:
        if offset + 3 > len(stream):
            raise MLDSAError("rejection sampling exhausted its stream")
        b0, b1, b2 = stream[offset], stream[offset + 1], stream[offset + 2]
        offset += 3
        z = ((b2 & 0x7F) << 16) | (b1 << 8) | b0
        if z < Q:
            coefficients.append(z)
    return coefficients


def _coefficient_from_half_byte(value: int) -> int | None:
    if value < 15:
        return 2 - (value % 5)
    return None


def _rej_bounded_poly(seed: bytes) -> list[int]:
    stream = _shake256(seed, 1024)
    coefficients: list[int] = []
    offset = 0
    while len(coefficients) < N:
        if offset >= len(stream):
            raise MLDSAError("bounded sampling exhausted its stream")
        byte = stream[offset]
        offset += 1
        for half in (byte & 0x0F, byte >> 4):
            coefficient = _coefficient_from_half_byte(half)
            if coefficient is not None and len(coefficients) < N:
                coefficients.append(coefficient % Q)
    return coefficients


def _expand_a(rho: bytes) -> list[list[list[int]]]:
    return [[_rej_ntt_poly(rho + bytes([s, r])) for s in range(L)] for r in range(K)]


def _expand_s(rho_prime: bytes) -> tuple[list[list[int]], list[list[int]]]:
    s1 = [_rej_bounded_poly(rho_prime + r.to_bytes(2, "little")) for r in range(L)]
    s2 = [_rej_bounded_poly(rho_prime + (r + L).to_bytes(2, "little")) for r in range(K)]
    return s1, s2


def _bit_pack(values: list[int], bits: int) -> bytes:
    accumulator = 0
    for index, value in enumerate(values):
        if value < 0 or value >= (1 << bits):
            raise MLDSAError("coefficient does not fit its bit width")
        accumulator |= value << (index * bits)
    return accumulator.to_bytes(len(values) * bits // 8, "little")


def _bit_unpack(data: bytes, bits: int) -> list[int]:
    accumulator = int.from_bytes(data, "little")
    mask = (1 << bits) - 1
    return [(accumulator >> (index * bits)) & mask for index in range(len(data) * 8 // bits)]


def _power2round(value: int) -> tuple[int, int]:
    r = value % Q
    r0 = _centered(r, 1 << D)
    return (r - r0) >> D, r0


def _decompose(value: int) -> tuple[int, int]:
    r = value % Q
    r0 = _centered(r, 2 * GAMMA2)
    if r - r0 == Q - 1:
        return 0, r0 - 1
    return (r - r0) // (2 * GAMMA2), r0


def _high_bits(value: int) -> int:
    return _decompose(value)[0]


def _low_bits(value: int) -> int:
    return _decompose(value)[1]


def _use_hint(hint: int, value: int) -> int:
    m = (Q - 1) // (2 * GAMMA2)
    r1, r0 = _decompose(value)
    if hint == 1 and r0 > 0:
        return (r1 + 1) % m
    if hint == 1:
        return (r1 - 1) % m
    return r1


def _w1_encode(w1: list[list[int]]) -> bytes:
    return b"".join(_bit_pack(poly, 6) for poly in w1)


def _sample_in_ball(seed: bytes) -> list[int]:
    stream = _shake256(seed, 8 + 1024)
    signs = int.from_bytes(stream[:8], "little")
    offset = 8
    c = [0] * N
    for i in range(N - TAU, N):
        while True:
            if offset >= len(stream):
                raise MLDSAError("challenge sampling exhausted its stream")
            j = stream[offset]
            offset += 1
            if j <= i:
                break
        c[i] = c[j]
        c[j] = Q - 1 if (signs >> (i + TAU - N)) & 1 else 1
    return c


def _expand_mask(rho: bytes, kappa: int) -> list[list[int]]:
    vector = []
    for r in range(L):
        stream = _shake256(rho + (kappa + r).to_bytes(2, "little"), 32 * 18)
        vector.append([(GAMMA1 - value) % Q for value in _bit_unpack(stream, 18)])
    return vector


def _matrix_times(a_hat: list[list[list[int]]], vector_hat: list[list[int]]) -> list[list[int]]:
    result = []
    for row in a_hat:
        accumulator = [0] * N
        for entry, poly in zip(row, vector_hat):
            accumulator = _add(accumulator, _pointwise(entry, poly))
        result.append(accumulator)
    return result


class PrivateKey:
    """The expanded signing state derived from a seed (test vectors only)."""

    def __init__(self, seed: bytes) -> None:
        if len(seed) != 32:
            raise MLDSAError("ML-DSA-44 seed must be 32 bytes")
        expanded = _shake256(seed + bytes([K, L]), 128)
        self.rho, rho_prime, self.key = expanded[:32], expanded[32:96], expanded[96:]
        self.a_hat = _expand_a(self.rho)
        s1, s2 = _expand_s(rho_prime)
        self.s1_hat = [ntt(poly) for poly in s1]
        self.s2_hat = [ntt(poly) for poly in s2]
        t = [_add(inverse_ntt(poly), s2[index]) for index, poly in enumerate(_matrix_times(self.a_hat, self.s1_hat))]
        t1, t0 = [], []
        for poly in t:
            pairs = [_power2round(c) for c in poly]
            t1.append([pair[0] for pair in pairs])
            t0.append([pair[1] % Q for pair in pairs])
        self.t0_hat = [ntt(poly) for poly in t0]
        self.public_key = self.rho + b"".join(_bit_pack(poly, 10) for poly in t1)
        self.tr = _shake256(self.public_key, 64)

    def sign_internal(self, formatted_message: bytes, randomness: bytes = bytes(32)) -> bytes:
        mu = _shake256(self.tr + formatted_message, 64)
        rho_second = _shake256(self.key + randomness + mu, 64)
        kappa = 0
        while True:
            y = _expand_mask(rho_second, kappa)
            kappa += L
            w = [inverse_ntt(poly) for poly in _matrix_times(self.a_hat, [ntt(poly) for poly in y])]
            w1 = [[_high_bits(c) for c in poly] for poly in w]
            c_tilde = _shake256(mu + _w1_encode(w1), LAMBDA_BYTES)
            c_hat = ntt(_sample_in_ball(c_tilde))
            cs1 = [inverse_ntt(_pointwise(c_hat, poly)) for poly in self.s1_hat]
            cs2 = [inverse_ntt(_pointwise(c_hat, poly)) for poly in self.s2_hat]
            z = [_add(a, b) for a, b in zip(y, cs1)]
            w_minus = [_sub(a, b) for a, b in zip(w, cs2)]
            r0 = [[_low_bits(c) for c in poly] for poly in w_minus]
            if _infinity_norm(z) >= GAMMA1 - BETA or max(abs(c) for poly in r0 for c in poly) >= GAMMA2 - BETA:
                continue
            ct0 = [inverse_ntt(_pointwise(c_hat, poly)) for poly in self.t0_hat]
            hints = []
            for ct0_poly, w_poly in zip(ct0, w_minus):
                hints.append([int(_high_bits(w_c) != _high_bits((w_c + c) % Q))
                              for c, w_c in zip(ct0_poly, w_poly)])
            if _infinity_norm(ct0) >= GAMMA2 or sum(map(sum, hints)) > OMEGA:
                continue
            return _encode_signature(c_tilde, z, hints)

    def sign(self, message: bytes, context: bytes) -> bytes:
        return self.sign_internal(_pure_message(message, context))

    def sign_hash_sha256(self, message: bytes, context: bytes) -> bytes:
        return self.sign_internal(_prehash_message(message, context))


def _encode_signature(c_tilde: bytes, z: list[list[int]], hints: list[list[int]]) -> bytes:
    packed = [_bit_pack([(GAMMA1 - _centered(c, Q)) for c in poly], 18) for poly in z]
    hint_bytes = bytearray(OMEGA + K)
    index = 0
    for i, poly in enumerate(hints):
        for j, bit in enumerate(poly):
            if bit:
                hint_bytes[index] = j
                index += 1
        hint_bytes[OMEGA + i] = index
    return c_tilde + b"".join(packed) + bytes(hint_bytes)


def _decode_hints(data: bytes) -> list[list[int]] | None:
    hints = [[0] * N for _ in range(K)]
    index = 0
    for i in range(K):
        end = data[OMEGA + i]
        if end < index or end > OMEGA:
            return None
        first = index
        while index < end:
            if index > first and data[index - 1] >= data[index]:
                return None
            hints[i][data[index]] = 1
            index += 1
    if any(data[position] != 0 for position in range(index, OMEGA)):
        return None
    return hints


def _pure_message(message: bytes, context: bytes) -> bytes:
    if len(context) > MAX_CONTEXT_BYTES:
        raise MLDSAError("ML-DSA context is longer than 255 bytes")
    return bytes([0, len(context)]) + context + message


def _prehash_message(message: bytes, context: bytes) -> bytes:
    if len(context) > MAX_CONTEXT_BYTES:
        raise MLDSAError("ML-DSA context is longer than 255 bytes")
    return bytes([1, len(context)]) + context + SHA256_OID + hashlib.sha256(message).digest()


def _verify_internal(public_key: bytes, formatted_message: bytes, signature: bytes) -> bool:
    if len(public_key) != PUBLIC_KEY_BYTES or len(signature) != SIGNATURE_BYTES:
        return False
    rho = public_key[:32]
    t1 = [_bit_unpack(public_key[32 + 320 * i: 32 + 320 * (i + 1)], 10) for i in range(K)]
    c_tilde = signature[:LAMBDA_BYTES]
    offset = LAMBDA_BYTES
    z = []
    for _ in range(L):
        z.append([(GAMMA1 - value) % Q for value in _bit_unpack(signature[offset: offset + 576], 18)])
        offset += 576
    hints = _decode_hints(signature[offset:])
    if hints is None or _infinity_norm(z) >= GAMMA1 - BETA:
        return False
    a_hat = _expand_a(rho)
    tr = _shake256(public_key, 64)
    mu = _shake256(tr + formatted_message, 64)
    c_hat = ntt(_sample_in_ball(c_tilde))
    az = _matrix_times(a_hat, [ntt(poly) for poly in z])
    w1 = []
    for i in range(K):
        ct1 = _pointwise(c_hat, ntt([(c << D) % Q for c in t1[i]]))
        w_approx = inverse_ntt(_sub(az[i], ct1))
        w1.append([_use_hint(h, c) for h, c in zip(hints[i], w_approx)])
    return c_tilde == _shake256(mu + _w1_encode(w1), LAMBDA_BYTES)


def verify(public_key: bytes, message: bytes, signature: bytes, context: bytes) -> bool:
    """Pure ML-DSA-44 verification of `message` under `context`."""
    try:
        formatted = _pure_message(message, context)
    except MLDSAError:
        return False
    return _verify_internal(public_key, formatted, signature)


def verify_hash_sha256(public_key: bytes, message: bytes, signature: bytes, context: bytes) -> bool:
    """HashML-DSA-44 with SHA-256 verification (refusal vectors only)."""
    try:
        formatted = _prehash_message(message, context)
    except MLDSAError:
        return False
    return _verify_internal(public_key, formatted, signature)


KEY_ID_DOMAIN = b"TOS-PQ-CONSENSUS-KEY-v1"
KEY_ID_SUITE = b"\x01\x00"


def key_id(public_key: bytes) -> bytes:
    """The controller key ID: SHA-256(domain || 0x01 0x00 || public key)."""
    if len(public_key) != PUBLIC_KEY_BYTES:
        raise MLDSAError("ML-DSA-44 public key must be 1,312 bytes")
    return hashlib.sha256(KEY_ID_DOMAIN + KEY_ID_SUITE + public_key).digest()


def _check_refusals(path: Path, secret: PrivateKey, refusals: list, message: bytes, context: bytes) -> None:
    for refusal in refusals:
        refused = bytes.fromhex(refusal["signature_hex"])
        own_message = bytes.fromhex(refusal["message_hex"])
        own_context = refusal["context"].encode()
        if refusal["mode"] == "pure":
            produced = secret.sign(own_message, own_context)
            own_valid = verify(secret.public_key, own_message, refused, own_context)
        elif refusal["mode"] == "hash-sha256":
            produced = secret.sign_hash_sha256(own_message, own_context)
            own_valid = verify_hash_sha256(secret.public_key, own_message, refused, own_context)
        else:
            raise SystemExit(f"{path}: unknown refusal mode {refusal['mode']!r}")
        if produced != refused or not own_valid:
            raise SystemExit(f"{path}: refusal {refusal['name']} does not reproduce in its own mode")
        if verify(secret.public_key, message, refused, context):
            raise SystemExit(f"{path}: refusal {refusal['name']} verified as the vector's own use")


def _check_malformed_signatures(path: Path, public_key: bytes, message: bytes, signature: bytes,
                                context: bytes) -> int:
    """Every structural corruption of a valid signature or key is refused."""
    hint_offset = LAMBDA_BYTES + L * 576
    cases: list[tuple[str, bytes, bytes]] = []

    def flipped(position: int) -> bytes:
        mutated = bytearray(signature)
        mutated[position] ^= 1
        return bytes(mutated)

    cases.append(("flipped challenge", public_key, flipped(0)))
    cases.append(("flipped response", public_key, flipped(LAMBDA_BYTES + 100)))
    cases.append(("flipped hint", public_key, flipped(hint_offset)))
    cases.append(("truncated signature", public_key, signature[:-1]))
    cases.append(("oversized signature", public_key, signature + b"\x00"))
    cases.append(("truncated key", public_key[:-1], signature))
    cases.append(("oversized key", public_key + b"\x00", signature))
    hints = bytearray(signature[hint_offset:])
    counts = list(hints[OMEGA:])
    total = counts[-1]
    if total >= 2:
        swapped = bytearray(hints)
        swapped[0], swapped[1] = swapped[1], swapped[0]
        cases.append(("non-increasing hint indices", public_key, signature[:hint_offset] + bytes(swapped)))
    padded = bytearray(hints)
    if total < OMEGA:
        padded[OMEGA - 1] = 1
        cases.append(("non-zero hint padding", public_key, signature[:hint_offset] + bytes(padded)))
    excessive = bytearray(hints)
    excessive[OMEGA + K - 1] = OMEGA + 1
    cases.append(("hint count above omega", public_key, signature[:hint_offset] + bytes(excessive)))
    if counts[0] > 0:
        decreasing = bytearray(hints)
        decreasing[OMEGA + 1] = counts[0] - 1
        cases.append(("decreasing cumulative hint counts", public_key, signature[:hint_offset] + bytes(decreasing)))
    # A response coefficient at the bound gamma1 - beta (and its negative) is
    # re-encoded in place of the first coefficient; both must be refused.
    for bound in (GAMMA1 - BETA, -(GAMMA1 - BETA)):
        first = _bit_unpack(signature[LAMBDA_BYTES: LAMBDA_BYTES + 576], 18)
        first[0] = GAMMA1 - bound
        cases.append((f"response coefficient {bound}", public_key,
                      signature[:LAMBDA_BYTES] + _bit_pack(first, 18) + signature[LAMBDA_BYTES + 576:]))
    cases.append(("changed message", public_key, signature))
    for name, key, candidate in cases:
        candidate_message = message if name != "changed message" else bytes([message[0] ^ 1]) + message[1:]
        if verify(key, candidate_message, candidate, context):
            raise SystemExit(f"{path}: {name} verified")
    if verify_hash_sha256(public_key, message, signature, context):
        raise SystemExit(f"{path}: a Pure signature verified as HashML-DSA")
    return len(cases)


def _differential_message(seed: bytes, length: int) -> bytes:
    out = b""
    counter = 0
    while len(out) < length:
        out += hashlib.sha256(b"tos.mldsa44-differential.v1" + seed + length.to_bytes(4, "big") +
                              counter.to_bytes(4, "big")).digest()
        counter += 1
    return out[:length]


def _check_differential(path: Path, differential: dict) -> int:
    keys: dict[bytes, PrivateKey] = {}
    for entry in differential["entries"]:
        seed = bytes.fromhex(entry["seed_hex"])
        secret = keys.setdefault(seed, PrivateKey(seed))
        if hashlib.sha256(secret.public_key).hexdigest() != entry["public_key_sha256"]:
            raise SystemExit(f"{path}: differential key for seed {entry['seed_hex'][:2]} differs")
        message = _differential_message(seed, entry["message_length"])
        context = entry["context"].encode()
        if entry["mode"] == "pure":
            signature = secret.sign(message, context)
            valid = verify(secret.public_key, message, signature, context)
            cross = verify_hash_sha256(secret.public_key, message, signature, context)
        elif entry["mode"] == "hash-sha256":
            signature = secret.sign_hash_sha256(message, context)
            valid = verify_hash_sha256(secret.public_key, message, signature, context)
            cross = verify(secret.public_key, message, signature, context)
        else:
            raise SystemExit(f"{path}: unknown differential mode")
        if hashlib.sha256(signature).hexdigest() != entry["signature_sha256"] or not valid or cross:
            raise SystemExit(f"{path}: differential signature for seed {entry['seed_hex'][:2]}, "
                             f"length {entry['message_length']}, context {len(context)} bytes differs")
    return len(differential["entries"])


def _self_test(path: Path) -> None:
    vector = json.loads(path.read_text(encoding="utf-8"))
    seed = bytes.fromhex(vector["seed_hex"])
    context = vector["context"].encode()
    secret = PrivateKey(seed)
    if secret.public_key.hex() != vector["public_key_hex"]:
        raise SystemExit(f"{path}: public key does not reproduce from the seed")
    if key_id(secret.public_key).hex() != vector["key_id_hex"]:
        raise SystemExit(f"{path}: key ID does not reproduce")
    if vector["schema"] == "tos.agent-guarantor-signature-vector.v1":
        signed = [(bytes.fromhex(vector["message_hex"]), vector["signature_hex"])]
    elif vector["schema"] == "tos.action-authority-signature-vector.v1":
        signed = []
        for entry in vector["messages"]:
            canonical = bytes.fromhex(entry["canonical_cbor_hex"])
            framed = hashlib.sha256(entry["signature_domain"].encode() + b"\x00" +
                                    len(canonical).to_bytes(4, "big") + canonical).digest()
            if framed.hex() != entry["message_hex"]:
                raise SystemExit(f"{path}: {entry['name']} message is not the framed digest of its object")
            signed.append((framed, entry["signature_hex"]))
    else:
        raise SystemExit(f"{path}: unknown vector schema {vector['schema']!r}")
    for index, (message, expected) in enumerate(signed):
        signature = secret.sign(message, context)
        if signature.hex() != expected:
            raise SystemExit(f"{path}: deterministic signature {index} does not reproduce")
        if not verify(secret.public_key, message, signature, context):
            raise SystemExit(f"{path}: signature {index} does not verify")
        for other_index, (other, _) in enumerate(signed):
            if other_index != index and verify(secret.public_key, other, signature, context):
                raise SystemExit(f"{path}: signature {index} verified for message {other_index}")
    primary_message, primary_hex = signed[0]
    _check_refusals(path, secret, vector.get("refusals", []), primary_message, context)
    malformed = _check_malformed_signatures(path, secret.public_key, primary_message, bytes.fromhex(primary_hex), context)
    differential = _check_differential(path, vector["differential"]) if "differential" in vector else 0
    print(f"PASS: {path.name} reproduces byte for byte ({len(signed)} signatures, "
          f"{len(vector.get('refusals', []))} refusals, {malformed} malformed inputs refused, "
          f"{differential} differential signatures)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--self-test", nargs="+", type=Path, required=True, metavar="VECTOR")
    arguments = parser.parse_args()
    for path in arguments.self_test:
        _self_test(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
