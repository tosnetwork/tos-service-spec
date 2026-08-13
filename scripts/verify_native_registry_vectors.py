#!/usr/bin/env python3
"""Independent stdlib/OpenSSL verifier for every Phase 5A vector."""
import base64, copy, hashlib, json, pathlib, re, struct, subprocess, tempfile

ROOT=pathlib.Path(__file__).resolve().parents[1]
V=json.loads((ROOT/"test-vectors/native_registry_v1.json").read_text());P=V["positive"]
def head(m,n):
    if n<24:return bytes([(m<<5)|n])
    if n<=255:return bytes([(m<<5)|24,n])
    if n<=65535:return bytes([(m<<5)|25])+struct.pack(">H",n)
    if n<=0xffffffff:return bytes([(m<<5)|26])+struct.pack(">I",n)
    return bytes([(m<<5)|27])+struct.pack(">Q",n)
def cbor(v):
    if isinstance(v,bool):return b"\xf5" if v else b"\xf4"
    if isinstance(v,str):b=v.encode();return head(3,len(b))+b
    if isinstance(v,int) and v>=0:return head(0,v)
    if isinstance(v,list):return head(4,len(v))+b"".join(cbor(x) for x in v)
    if isinstance(v,dict):
        pairs=sorted(((cbor(k),cbor(x)) for k,x in v.items()),key=lambda p:(len(p[0]),p[0]));return head(5,len(pairs))+b"".join(k+x for k,x in pairs)
    raise TypeError(type(v))
def take(data,pos):
    initial=data[pos];pos+=1;major=initial>>5;ai=initial&31
    if ai<24:n=ai
    elif ai==24:n=data[pos];pos+=1
    elif ai==25:n=struct.unpack(">H",data[pos:pos+2])[0];pos+=2
    elif ai==26:n=struct.unpack(">I",data[pos:pos+4])[0];pos+=4
    elif ai==27:n=struct.unpack(">Q",data[pos:pos+8])[0];pos+=8
    else:raise ValueError("indefinite/tagged CBOR")
    if major==0:return n,pos
    if major==3:return data[pos:pos+n].decode(),pos+n
    if major==4:
        out=[]
        for _ in range(n):v,pos=take(data,pos);out.append(v)
        return out,pos
    if major==5:
        out={}
        for _ in range(n):k,pos=take(data,pos);v,pos=take(data,pos);assert k not in out;out[k]=v
        return out,pos
    if major==7 and ai in (20,21):return ai==21,pos
    raise ValueError("unsupported CBOR type")
def canonical_decode(data):
    value,pos=take(data,0)
    if pos!=len(data) or cbor(value)!=data:raise ValueError("noncanonical CBOR")
    return value
def digest(domain,value):
    d=domain.encode();return "sha256:"+hashlib.sha256(b"TOS-PROTOCOL-CBOR\0"+struct.pack(">H",len(d))+d+cbor(value)).hexdigest()
def b64u(raw):return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()
def unb64u(value):return base64.urlsafe_b64decode(value+"="*((4-len(value)%4)%4))
def field(out,raw):out.extend(struct.pack(">H",len(raw)));out.extend(raw)

policy=canonical_decode(unb64u(P["controller_policy_cbor_base64url"]));pub=unb64u(policy["controllers"][0]["public_key_base64url"])
assert digest(V["domains"]["controller_policy"],policy)==P["controller_policy_digest"]
agent={"version":"tos_native_registry_v1","network":P["network"],"object_nonce_base64url":P["agent_nonce_base64url"],"initial_controller_policy_digest":P["controller_policy_digest"]};agent_id="agent_"+digest(V["domains"]["agent_id"],agent)[7:];assert agent_id==P["agent_id"]
cap={"version":"tos_native_registry_v1","network":P["network"],"owner_agent_id":agent_id,"object_nonce_base64url":P["capability_nonce_base64url"]};cap_id="cap_"+digest(V["domains"]["capability_id"],cap)[7:];assert cap_id==P["capability_id"]
payload=canonical_decode(unb64u(P["payload_cbor_base64url"]));assert digest("tos.native.registry-payload.register-capability.v1",payload)==P["payload_digest"]
action={"version":"tos_native_registry_v1","kind":"register_capability","network":P["network"],"agent_id":agent_id,"capability_id":cap_id,"capability_version":"1.2.3","generation":1,"sequence":1,"previous_state_digest":"","policy_digest":P["controller_policy_digest"],"payload_digest":P["payload_digest"],"payload_cbor_base64url":P["payload_cbor_base64url"],"nonce_base64url":"cHFyc3R1dnd4eXp7fH1-f4CBgoOEhYaHiImKi4yNjo8"}
action_bytes=cbor(action);assert base64.b64encode(action_bytes).decode()==P["registry_action_cbor_base64"];assert digest(V["domains"]["registry_action"],action)==P["registry_action_digest"]
state={"version":"tos_native_registry_v1","network":P["network"],"object_kind":"capability","agent_id":"","capability_id":cap_id,"generation":1,"sequence":1,"predecessor_state_digest":"","last_action_digest":P["registry_action_digest"],"current_policy_digest":"","current_policy_cbor_base64url":"","owner_agent_id":agent_id,"capability_bootstrap_owner_agent_id":agent_id,"capability_nonce_base64url":P["capability_nonce_base64url"],"capability_versions":[{"version":"1.2.3","payload_digest":P["payload_digest"],"revoked":False}],"delegation_action_digests":[],"pending_recovery":{"initiation_action_digest":"","new_policy_digest":"","new_policy_cbor_base64url":"","execute_after_unix_seconds":0},"tombstoned":False,"agent_nonce_base64url":"","agent_bootstrap_policy_digest":""};assert digest(V["domains"]["registry_state"],state)==P["registry_state_digest"]
event={"version":"tos_native_registry_v1","kind":"register_capability","network":P["network"],"action_digest":P["registry_action_digest"],"agent_id":agent_id,"capability_id":cap_id,"capability_version":"1.2.3","generation":1,"sequence":1,"previous_state_digest":"","state_digest":P["registry_state_digest"]};assert digest(V["domains"]["registry_event"],event)==P["registry_event_digest"]
assert digest(V["domains"]["event_observation"],P["event_observation"])==P["event_observation_digest"]
signature=P["signature"]
def verify_signature(value):
    message=bytearray(b"TOS-NATIVE-SEMANTIC-SIGNATURE\0")
    for item in (V["domains"]["semantic_signature"],value["version"],value["algorithm"],value["key_id"],V["domains"]["registry_action"]):field(message,item.encode())
    message.extend(hashlib.sha256(action_bytes).digest())
    with tempfile.TemporaryDirectory() as directory:
        d=pathlib.Path(directory);(d/"pub.der").write_bytes(bytes.fromhex("302a300506032b6570032100")+pub);(d/"msg").write_bytes(message);(d/"sig").write_bytes(unb64u(value["signature_base64url"]))
        result=subprocess.run(["openssl","pkeyutl","-verify","-pubin","-inkey",str(d/"pub.der"),"-keyform","DER","-rawin","-in",str(d/"msg"),"-sigfile",str(d/"sig")],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        return result.returncode==0
assert verify_signature(signature)

def patch(document,operation):
    parts=operation["path"].strip("/").split("/");target=document
    for part in parts[:-1]:target=target[int(part)] if isinstance(target,list) else target[part]
    key=parts[-1];value=copy.deepcopy(operation["value"])
    if operation["op"]=="replace":
        if isinstance(target,list):target[int(key)]=value
        else:target[key]=value
    elif operation["op"]=="add":target.insert(int(key),value) if isinstance(target,list) else target.__setitem__(key,value)
def error(code,field):return code,field
def validate_event(value):
    cap=value["kind"].endswith("capability")
    if not cap and (value.get("capability_id") or value.get("capability_version")):return error("NATIVE_CROSS_DOMAIN_REPLAY","registry_event.capability")
    if cap and (not re.fullmatch(r"cap_[0-9a-f]{64}",value.get("capability_id",""))):return error("NATIVE_INVALID_IDENTIFIER","registry_event.object")
    version=value.get("capability_version","")
    if cap and version and not re.fullmatch(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?",version):return error("NATIVE_INVALID_IDENTIFIER","capability_version")
    return "",""
def validate_observation(value):
    ref=value["reference"]
    if not ref.get("transaction_hash") or value.get("finalized_checkpoint",0)==0:return error("NATIVE_FINALITY_UNAVAILABLE","event_observation")
    return "",""
def validate_action(value):
    try:decoded=canonical_decode(unb64u(value["payload_cbor_base64url"]))
    except Exception:return error("NATIVE_CANONICAL_ENCODING","payload_digest")
    if value["kind"]=="register_capability":
        bootstrap={"version":"tos_native_registry_v1","network":value["network"],"owner_agent_id":decoded["version"]["owner_agent_id"],"object_nonce_base64url":decoded["object_nonce_base64url"]}
        if value["capability_id"]!="cap_"+digest(V["domains"]["capability_id"],bootstrap)[7:]:return error("NATIVE_INVALID_IDENTIFIER","capability_id")
    return "",""
def validate_reference(value):
    if value["account"].split(":",1)[0]!=str(value["workchain"]):return error("NATIVE_CANONICAL_ENCODING","reference.workchain")
    return "",""
def validate_capability_payload(value):
    locations=value["version"]["manifest"]["locations"]
    if any(not x or any(ord(c)<0x21 or ord(c)>0x7e for c in x) for x in locations):return error("NATIVE_CANONICAL_ENCODING","payload.register_capability")
    if set(value["version"]["quote_signer_key_ids"])&set(value["version"]["receipt_signer_key_ids"]):return error("NATIVE_CANONICAL_ENCODING","payload.register_capability")
    return "",""
def execute(vector):
    fixture=vector["fixture"];op=vector["operation"]
    if fixture=="signature":
        document={"signature":copy.deepcopy(signature)};patch(document,op);return ("","") if verify_signature(document["signature"]) else error("NATIVE_POLICY_UNAUTHORIZED","signature")
    if fixture=="policy":
        document={"policy":copy.deepcopy(policy)};operation=copy.deepcopy(op);operation["value"]={**operation["value"],"public_key_base64url":policy["controllers"][0]["public_key_base64url"]};del operation["value"]["public_key_source"];patch(document,operation);keys=[x["public_key_base64url"] for x in document["policy"]["controllers"]];return error("NATIVE_CANONICAL_ENCODING","controller_policy.duplicate_public_key") if len(keys)!=len(set(keys)) else ("","")
    if fixture=="authorization":
        document={"signatures":[copy.deepcopy(signature)]};operation=copy.deepcopy(op)
        if operation["value"]=="copy_0":operation["value"]=copy.deepcopy(document["signatures"][0])
        patch(document,operation);ids=[x["key_id"] for x in document["signatures"]];return error("NATIVE_CANONICAL_ENCODING","signatures.duplicate") if len(ids)!=len(set(ids)) else ("","")
    if fixture=="agent_event":
        document={"event":copy.deepcopy(event)};document["event"]["kind"]="register_agent";document["event"]["capability_id"]="";document["event"]["capability_version"]="";patch(document,op);return validate_event(document["event"])
    if fixture=="revoke_capability_event":
        document={"event":copy.deepcopy(event)};document["event"]["kind"]="revoke_capability";patch(document,op);return validate_event(document["event"])
    if fixture=="observation":
        observation={"version":"tos_native_registry_v1","network":P["network"],"event_digest":P["registry_event_digest"],"reference":{"workchain":0,"account":"0:"+"66"*32,"logical_time":42,"transaction_hash":"sha256:"+"77"*32,"contract_code_hash":"tvm-cell-sha256:"+"88"*32,"event_index":1},"finalized_checkpoint":100,"finalized_root_hash":"sha256:"+"99"*32,"finalized_file_hash":"sha256:"+"aa"*32,"block_unix_seconds":1800000000,"inclusion_proof_digest":"sha256:"+"bb"*32}
        document={"observation":observation};patch(document,op);return validate_observation(document["observation"])
    if fixture=="action":
        changed=copy.deepcopy(action);patch({"action":changed},op)
        return validate_action(changed)
    if fixture=="network":
        changed=copy.deepcopy(P["network"]);patch({"network":changed},op);return error("NATIVE_INVALID_NETWORK","network") if not re.fullmatch(r"[a-z0-9](?:[a-z0-9.-]{0,61}[a-z0-9])?",changed["network_id"]) else ("","")
    if fixture=="authorization_context":
        document={"expected_policy_digest":P["controller_policy_digest"]};patch(document,op);return error("NATIVE_POLICY_UNAUTHORIZED","current_controller_policy") if document["expected_policy_digest"]!=P["controller_policy_digest"] else ("","")
    if fixture=="event_state":
        changed=copy.deepcopy(event);patch({"event":changed},op);return error("NATIVE_CROSS_DOMAIN_REPLAY","registry_event.state_tuple") if changed["state_digest"]!=digest(V["domains"]["registry_state"],state) else ("","")
    if fixture=="reference":
        changed=copy.deepcopy(P["event_observation"]["reference"]);patch({"reference":changed},op);return validate_reference(changed)
    if fixture=="capability_payload":
        changed=copy.deepcopy(payload);patch({"payload":changed},op);return validate_capability_payload(changed)
    return "",""
for vector in V["negative"]:
    actual=execute(vector);expected=(vector["expected_code"],vector["expected_field"])
    assert actual==expected,(vector["name"],actual,expected)
print(f"native_registry_v1 vectors: VALID ({len(V['negative'])} negative mutations executed)")
