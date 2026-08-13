#!/usr/bin/env python3
"""Independent stdlib verifier for Phase 5A identifier/digest vectors."""
import base64, hashlib, json, pathlib, struct

ROOT = pathlib.Path(__file__).resolve().parents[1]
V = json.loads((ROOT / "test-vectors/native_registry_v1.json").read_text())
P = V["positive"]

def head(major, n):
    if n < 24: return bytes([(major << 5) | n])
    if n <= 0xff: return bytes([(major << 5) | 24, n])
    if n <= 0xffff: return bytes([(major << 5) | 25]) + struct.pack(">H", n)
    if n <= 0xffffffff: return bytes([(major << 5) | 26]) + struct.pack(">I", n)
    return bytes([(major << 5) | 27]) + struct.pack(">Q", n)

def cbor(v):
    if isinstance(v, str):
        b = v.encode(); return head(3, len(b)) + b
    if isinstance(v, int) and v >= 0: return head(0, v)
    if isinstance(v, list): return head(4, len(v)) + b"".join(cbor(x) for x in v)
    if isinstance(v, dict):
        pairs = sorted(((cbor(k), cbor(x)) for k, x in v.items()), key=lambda p:(len(p[0]),p[0]))
        return head(5, len(pairs)) + b"".join(k+x for k,x in pairs)
    raise TypeError(type(v))

def digest(domain, value):
    d = domain.encode()
    return "sha256:" + hashlib.sha256(b"TOS-PROTOCOL-CBOR\0" + struct.pack(">H",len(d)) + d + cbor(value)).hexdigest()

public = base64.urlsafe_b64encode(bytes.fromhex("79b5562e8fe654f94078b112e8a98ba7901f853ae695bed7e0e3910bad049664")).rstrip(b"=").decode()
policy = {"threshold":1,"controllers":[{"key_id":"controller-1","algorithm":"ed25519","public_key_base64url":public,"weight":1,"purposes":["agent_control","recovery"]}],"recovery_key_ids":["controller-1"],"recovery_timelock_seconds":86400}
assert digest(V["domains"]["controller_policy"],policy) == P["controller_policy_digest"]

agent = {"version":"tos_native_registry_v1","network":P["network"],"object_nonce_base64url":P["agent_nonce_base64url"],"initial_controller_policy_digest":P["controller_policy_digest"]}
agent_id = "agent_" + digest(V["domains"]["agent_id"],agent)[7:]
assert agent_id == P["agent_id"] and P["agent_uri"] == "atos://agent/" + agent_id

cap = {"version":"tos_native_registry_v1","network":P["network"],"owner_agent_id":agent_id,"object_nonce_base64url":P["capability_nonce_base64url"]}
cap_id = "cap_" + digest(V["domains"]["capability_id"],cap)[7:]
assert cap_id == P["capability_id"]

action = {"version":"tos_native_registry_v1","kind":"register_capability","network":P["network"],"agent_id":agent_id,"capability_id":cap_id,"capability_version":"1.2.3","generation":1,"sequence":1,"previous_event_digest":"","policy_digest":P["controller_policy_digest"],"payload_digest":"sha256:"+"33"*32,"nonce_base64url":"cHFyc3R1dnd4eXp7fH1-f4CBgoOEhYaHiImKi4yNjo8"}
encoded = cbor(action)
assert base64.b64encode(encoded).decode() == P["registry_action_cbor_base64"]
assert digest(V["domains"]["registry_action"],action) == P["registry_action_digest"]
event = {"version":"tos_native_registry_v1","kind":"register_capability","network":P["network"],"action_digest":P["registry_action_digest"],"agent_id":agent_id,"capability_id":cap_id,"capability_version":"1.2.3","generation":1,"sequence":1,"previous_event_digest":"","finalized_checkpoint":100,"transaction_index":2,"event_index":1}
assert digest(V["domains"]["registry_event"], event) == P["registry_event_digest"]
print("native_registry_v1 vectors: VALID")
