#!/usr/bin/env python3
"""Independent, dependency-free verifier for the V1 wrapper/digest vectors."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, struct, unicodedata
from pathlib import Path

PROFILE = b"tos.trusted-capability-owner-control.v1/"
MAX = 1 << 20

def encode_head(major, value):
    if value < 24: return bytes([(major << 5) | value])
    if value <= 0xff: return bytes([(major << 5) | 24, value])
    if value <= 0xffff: return bytes([(major << 5) | 25]) + struct.pack(">H", value)
    if value <= 0xffffffff: return bytes([(major << 5) | 26]) + struct.pack(">I", value)
    return bytes([(major << 5) | 27]) + struct.pack(">Q", value)

def encode(value):
    if value is None: return b"\xf6"
    if value is False: return b"\xf4"
    if value is True: return b"\xf5"
    if isinstance(value, int) and value >= 0: return encode_head(0, value)
    if isinstance(value, bytes): return encode_head(2, len(value)) + value
    if isinstance(value, str):
        raw=value.encode("utf-8"); return encode_head(3,len(raw))+raw
    if isinstance(value, list): return encode_head(4,len(value))+b"".join(encode(item) for item in value)
    if isinstance(value, dict):
        items=[(encode(key),encode(item)) for key,item in value.items()]
        items.sort(key=lambda item:(len(item[0]),item[0]))
        return encode_head(5,len(items))+b"".join(key+item for key,item in items)
    raise DecodeError("unsupported encode type")

class DecodeError(ValueError): pass

def head(data: bytes, at: int):
    if at >= len(data): raise DecodeError("truncated")
    first=data[at]; major=first>>5; ai=first&31; at+=1
    if ai < 24: return major,ai,at
    widths={24:1,25:2,26:4,27:8}
    if ai not in widths: raise DecodeError("indefinite/reserved")
    width=widths[ai]
    if at+width>len(data): raise DecodeError("truncated integer")
    value=int.from_bytes(data[at:at+width],"big")
    if value < (24 if width==1 else 1<<(8*(width-1))): raise DecodeError("non-minimal integer")
    return major,value,at+width

def decode(data: bytes, at=0, depth=0):
    if depth>16: raise DecodeError("depth")
    major,n,at=head(data,at)
    if major==0: return n,at
    if major==2:
        if at+n>len(data): raise DecodeError("truncated bytes")
        return data[at:at+n],at+n
    if major==3:
        if at+n>len(data): raise DecodeError("truncated text")
        try: value=data[at:at+n].decode("utf-8")
        except UnicodeDecodeError as exc: raise DecodeError("utf8") from exc
        if unicodedata.normalize("NFC",value)!=value: raise DecodeError("not NFC")
        return value,at+n
    if major==4:
        if n>4096: raise DecodeError("array")
        out=[]
        for _ in range(n): value,at=decode(data,at,depth+1); out.append(value)
        return out,at
    if major==5:
        if n>4096: raise DecodeError("map")
        out={}; prior=None
        for _ in range(n):
            key,start=decode(data,at,depth+1); keywire=data[at:start]; at=start
            if not isinstance(key,int) or key<0: raise DecodeError("map key")
            if prior is not None and (len(keywire),keywire) <= (len(prior),prior): raise DecodeError("map order/duplicate")
            prior=keywire; value,at=decode(data,at,depth+1); out[key]=value
        return out,at
    if major==7 and n==22: return None,at
    if major==7 and n in (20,21): return n==21,at
    raise DecodeError("unsupported CBOR type")

def matches_wire_type(value, declared, definitions):
    if declared.startswith("nullable:"):
        return value is None or matches_wire_type(value, declared.removeprefix("nullable:"), definitions)
    if declared.startswith("array:"):
        return isinstance(value, list) and all(matches_wire_type(item, declared.removeprefix("array:"), definitions) for item in value)
    if declared.startswith("object:"):
        type_name=declared.removeprefix("object:")
        fields=definitions.get(type_name)
        if fields is None or not isinstance(value,dict): return False
        by_key={field["cbor_key"]:field for field in fields}
        return set(value)==set(by_key) and all(matches_wire_type(value[key],field["type"],definitions) for key,field in by_key.items())
    if declared == "uint": return isinstance(value, int) and not isinstance(value, bool) and value >= 0
    if declared == "bool": return isinstance(value, bool)
    if declared == "text": return isinstance(value, str)
    if declared == "bytes": return isinstance(value, bytes)
    return False

def verify_body_schema(kind, body, schemas):
    schema=schemas.get(kind)
    if schema is None or not isinstance(body,dict): raise DecodeError("missing body schema")
    definitions={item["type_name"]:item["fields"] for item in schema.get("definitions",[])}
    definitions[schema["go_type"]]=schema["fields"]
    fields={field["cbor_key"]:field for field in schema["fields"]}
    if set(body) != set(fields): raise DecodeError("body required/unknown field mismatch")
    for key,field in fields.items():
        if not matches_wire_type(body[key],field["type"],definitions): raise DecodeError("body field type mismatch")

def framed_digest(domain, *fields):
    value=hashlib.sha256(); value.update(domain.encode()); value.update(b"\0")
    for field in fields: value.update(struct.pack(">I",len(field))); value.update(field)
    return value.digest()

def verify_body_semantics(kind, body, command_kinds):
    digest=lambda value: isinstance(value,bytes) and len(value)==32
    subject=lambda value: isinstance(value,dict) and bool(value.get(1)) and bool(value.get(2)) and bool(value.get(3))
    def reference(value):
        return isinstance(value,dict) and value.get(1,0)>0 and bool(value.get(2)) and bool(value.get(3)) and bool(value.get(4)) and value.get(5)==1 and digest(value.get(6)) and value.get(7,0)>0 and bool(value.get(8)) and digest(value.get(9)) and value.get(10)==sorted(set(value.get(10,[])))
    command_targets={
        "agreement.amendment.propose":"agreement","agreement.approve":"agreement","agreement.reject":"agreement",
        "capability.admit":"capability","capability.promotion.activate":"capability","capability.promotion.revoke":"capability",
        "capability.remove":"capability","capability.resume":"capability","capability.revoke":"capability","capability.suspend":"capability",
        "credential.revoke":"credential","delegation.revoke":"delegation","device-session.revoke":"device-session",
        "evidence.export":"evidence-export","intent.publish":"intent","intent.revise":"intent","intent.withdraw":"intent",
        "owner.exit":"owner","owner.pause":"agent","owner.policy.propose":"owner-policy","owner.resume":"agent",
        "reconcile.apply":"portfolio","reconcile.dry-run":"portfolio","session.revoke":"device-session","steering.bounded":"owner-policy"}
    if kind == "artifact":
        if body[1]!=1 or body[2] not in {"builtin","skill","mcp-local","mcp-remote","model-adapter","tool-bundle","local-adapter"}: raise DecodeError("artifact semantic kind")
        if any(not body[key] for key in (3,4,5)) or not all(digest(body[key]) for key in (7,8,9,10,13,14,15,16)) or body[18]==0: raise DecodeError("artifact semantic fields")
        if any(body[key] is not None and not digest(body[key]) for key in (11,12,17)): raise DecodeError("artifact optional digest")
    elif kind == "content-manifest":
        prior=""
        for entry in body[2]:
            path,object_type,mode,size,content=entry[1],entry[2],entry[3],entry[4],entry[5]
            if not path or path=="." or path.startswith("/") or "\\" in path or "/../" in "/"+path+"/" or path<=prior or object_type not in {"directory","regular"} or mode & ~0o755: raise DecodeError("manifest entry")
            if object_type=="regular" and not digest(content) or object_type=="directory" and (size!=0 or content is not None): raise DecodeError("manifest object")
            prior=path
        root=framed_digest("tos.capability-content-closure.v1",encode(body[2]))
        if body[1]!=1 or body[3]!=root: raise DecodeError("manifest closure")
    elif kind == "entrypoint-descriptor":
        if body[1]!=1 or not all(digest(body[key]) for key in (2,4,5,6,7,8,9,10)) or body[11] is not None and not digest(body[11]): raise DecodeError("entrypoint semantics")
        if any("\0" in argument for argument in body[3]): raise DecodeError("entrypoint NUL")
    elif kind == "permission-manifest":
        if body[1]!=1 or not digest(body[2]) or body[15]==0 or not body[14].isdigit() or len(body[14])>1 and body[14].startswith("0"): raise DecodeError("permission semantics")
        for key in (3,4,8,9,12):
            if body[key] != sorted(set(body[key])): raise DecodeError("permission set order")
    elif kind == "dependency-manifest":
        closure=framed_digest("tos.capability-dependency-closure.v1",encode({1:body[6],2:body[7]}))
        if body[1]!=1 or not all(digest(body[key]) for key in (2,3,4,5,8)) or body[8]!=closure or body[6] or body[7]: raise DecodeError("dependency semantics")
    elif kind == "publisher-envelope":
        if body[1]!=1 or body[3]!="skill" or not all(body[key] for key in (4,5,6)) or not subject(body[7]) or not all(digest(body[key]) for key in (2,8,9,10,11)) or not (0<body[13]<body[14]) or body[12]<body[13] or body[16]==0: raise DecodeError("publisher semantics")
    elif kind == "publisher-revocation-observation":
        if body[1]!=1 or not subject(body[2]) or not all(digest(body[key]) for key in (3,4,9)) or not body[7] or body[5]==0 or body[8]==0 or not (0<body[10]<body[11]): raise DecodeError("publisher revocation semantics")
    elif kind == "capability-requirement":
        allowed={"builtin","skill","mcp-local","mcp-remote","model-adapter","tool-bundle","local-adapter"}
        if body[1]!=1 or not all(digest(body[key]) for key in (2,3,4,5,6,7,8,14)) or not body[9].isdigit() or len(body[9])>1 and body[9].startswith("0") or body[10]==0 or not body[11] or body[11]!=sorted(set(body[11])) or not set(body[11])<=allowed or body[12]==0 or body[13]==0 or not (0<body[15]<body[16]): raise DecodeError("requirement semantics")
    elif kind == "sourcing-decision":
        if body[1]!=1 or not body[2] or not body[3] or not digest(body[4]) or not digest(body[5]) or len(body[6])<2 or body[8] is None or not digest(body[8]) or body[9]!="request-admission" or body[10]==0 or not (0<body[11]<body[12]): raise DecodeError("sourcing decision semantics")
        prior=None; sources=set(); admins=set(); failures=set()
        for attempt in body[6]:
            encoded=encode(attempt)
            if not attempt[1] or attempt[1] in sources or not digest(attempt[4]) or not digest(attempt[8]) or attempt[5]==0 or attempt[6]<attempt[5] or attempt[7]!="complete" or attempt[9]==0 or not digest(attempt[10]) or not digest(attempt[11]) or prior is not None and encoded<=prior: raise DecodeError("sourcing attempt semantics")
            sources.add(attempt[1]); admins.add(attempt[10]); failures.add(attempt[11]); prior=encoded
        if len(admins)<2 or len(failures)<2: raise DecodeError("sourcing independence")
        if not any(decision[1]==body[8] and decision[2]=="eligible" and decision[3]==sorted(set(decision[3])) and digest(decision[4]) for decision in body[7]): raise DecodeError("sourcing selected candidate")
    elif kind == "evaluation-manifest":
        if body[1]!=1 or body[6]==0 or not (0<body[20]<body[21]) or not all(digest(body[key]) for key in range(2,6)) or not all(digest(body[key]) for key in range(7,19)): raise DecodeError("evaluation manifest semantics")
        if len(body[19])<8 or body[19] != sorted(set(body[19])) or not all(digest(value) for value in body[19]): raise DecodeError("evaluation evidence closure")
    elif kind == "evaluation-result":
        if body[1]!=1 or not all(digest(body[key]) for key in (2,3,4,5,6,7,9,10,11,12,13,14)) or not reference(body[8]) or body[15]==0 or not (0<body[16]<body[17]): raise DecodeError("evaluation result semantics")
    elif kind == "evaluation-evidence":
        if body[1]!=1 or body[2] not in {"candidate-origin","permission","evaluation-result","retained-control","rollback"} or not all(digest(body[key]) for key in (3,4,5,6,7)) or not (0<body[8]<body[9]): raise DecodeError("evaluation evidence semantics")
    elif kind == "authorization-envelope":
        if body[1][1]!=1 or len(body[2])!=1 or not all(digest(body[1][key]) for key in (7,15,22,23)) or not subject(body[1][16]) or not (0<body[1][19]<body[1][20]): raise DecodeError("authorization envelope semantics")
    elif kind == "owner-policy":
        if not body[1] or not body[2] or body[3]==0 or body[5]==0 or not all(digest(body[key]) for key in (6,7,8,9,10,11)) or not (0<body[12]<body[13]) or body[3]==1 and body[4] is not None: raise DecodeError("owner policy semantics")
    elif kind == "capability-admission":
        if body[1]!=1 or len(body[2])!=16 or not body[3] or not body[4] or not all(digest(body[key]) for key in (5,6,12)) or body[11]==0 or body[18]==0 or body[16]>=body[17] or body[19] not in {"kill-and-reconcile","checkpoint-and-stop","drain"}: raise DecodeError("admission semantics")
    elif kind in {"admission-mutation","promotion-mutation"}:
        if not body[1] or body[2]==0 or body[3]!=body[2]+1 or not digest(body[4]) or body[5]!="revoke" or not body[6] or body[7]==0 or not digest(body[8]) or body[9]==0: raise DecodeError("authority mutation semantics")
    elif kind == "promotion-authority":
        if body[1]!=1 or len(body[2])!=16 or not body[5] or not body[6] or not all(digest(body[key]) for key in (7,8,9,10,11,12,15,16,17,18,19,20,23,24,26,29,30)) or not reference(body[13]) or not reference(body[14]) or not subject(body[21]) or not subject(body[22]) or body[21]==body[22] or body[25]==0 or not (0<body[27]<body[28]) or body[31]==0: raise DecodeError("promotion semantics")
    elif kind == "use-lease":
        if body[1]!=1 or not all(digest(body[key]) for key in (2,6,7,8,9,10,15,20)) or body[14]==0 or body[16]==0 or body[21]==0 or body[23]==0 or body[24]==0 or body[25]==0 or not (body[17]<=body[18]<=body[19]): raise DecodeError("use lease semantics")
        if not (body[12] is None and body[13] is None and body[22] is None or body[12] is not None and body[13] is not None and body[22] is not None and body[22]>0): raise DecodeError("use lease promotion")
    elif kind == "installation-transaction":
        if body[1]!=1 or len(body[2])!=16 or not reference(body[4]) or not all(digest(body[key]) for key in (3,5,6,8,9,10,11,12,13,14)) or body[7]==0 or body[15]==0 or body[16]!="prepared": raise DecodeError("installation semantics")
    elif kind == "capability-use-binding":
        if not all(digest(body[key]) for key in (3,4,5,6,7,9,10,11,19,21,24,25,26,27,28,31)) or body[9]!=body[7]: raise DecodeError("use binding semantics")
        all_promotion=all(body[key] is not None for key in (15,16,17)); no_promotion=all(body[key] is None for key in (15,16,17))
        if body[14] and not all_promotion or not body[14] and not no_promotion: raise DecodeError("use binding promotion")
    elif kind == "inventory-snapshot":
        if not body[1] or not body[2] or body[3]==0 or body[4]==0 or body[5]==0 or not digest(body[6]) or not body[8] or body[9]>=body[10]: raise DecodeError("inventory semantics")
        prior=None
        for entry in body[11]:
            if not digest(entry[1]) or entry[3]==0 or entry[4]==0 or prior is not None and entry[1]<=prior: raise DecodeError("inventory entry semantics")
            prior=entry[1]
    elif kind == "owner-report":
        if not body[1] or not body[2] or body[3]!=0 or not body[4] or not body[5] or body[6]==0 or body[7]!="finance-daily" or body[9]==0 or not all(digest(body[key]) for key in (8,10,15,16,17,18,19,20,21,22,23)) or not (0<body[11]<body[12]<=body[13]<=body[28]) or body[24]!="complete" or body[25] is not None or body[26] is not None: raise DecodeError("owner report semantics")
    elif kind == "report-source-coverage":
        if body[1]!=1 or not body[2] or body[6]==0 or body[7]!="complete" or body[5] or not digest(body[8]): raise DecodeError("coverage semantics")
    elif kind == "projection-event":
        if body[1]!=1 or not body[2] or not body[3] or not all(digest(body[key]) for key in (4,12,13,14)) or body[5]!=0 or body[18] is not None or not body[6] or not body[7] or body[8]==0 or not body[9] or body[15]>body[17] or body[16]>body[17]: raise DecodeError("projection event semantics")
    elif kind == "projection-snapshot":
        if body[1]!=1 or body[2]==0 or not body[3] or not body[4] or body[5]==0 or not all(digest(body[key]) for key in (6,7,9,11,12,13,14)) or not body[8] or not body[10] or body[15]==0: raise DecodeError("projection snapshot semantics")
        prior=None
        for source in body[8]:
            if not source[1] or source[2]==0 or not digest(source[4]) or prior is not None and source[1]<=prior: raise DecodeError("projection source semantics")
            prior=source[1]
        if body[5]==1 and body[16] is not None or body[5]>1 and (body[16] is None or not digest(body[16])): raise DecodeError("projection snapshot predecessor semantics")
    elif kind == "owner-bootstrap":
        if body[1]!=1 or body[2]==0 or not body[3] or not body[4] or not subject(body[5]) or not all(digest(body[key]) for key in (7,8,9,10,11)) or body[12]!=0 or body[13]!="owner-confirmed" or not (0<body[14]<body[15]): raise DecodeError("bootstrap semantics")
    elif kind == "owner-recovery":
        if not body[1] or not body[2] or body[5]==0 or not all(digest(body[key]) for key in (3,4,6,7,8)) or not (0<body[9]<body[10]): raise DecodeError("recovery semantics")
    elif kind == "device-enrollment":
        if len(body[1])!=16 or not body[2] or not body[3] or len(body[4])!=32 or not all(digest(body[key]) for key in (5,6,8,9)) or not body[7] or body[10]==0 or not (0<body[11]<body[12]): raise DecodeError("enrollment semantics")
    elif kind == "device-session":
        if len(body[1])!=16 or not subject(body[2]) or not body[3] or len(body[4])!=32 or not all(digest(body[key]) for key in (5,7,13)) or not body[6] or body[8]==0 or body[9]==0 or body[12]==0 or body[14]==0 or not reference(body[17]) or not (0<body[15]<body[16]): raise DecodeError("device session semantics")
    elif kind == "owner-command-lease":
        if body[1]!=1 or not digest(body[2]) or body[3]==0 or not body[4] or not body[5] or not all(digest(body[key]) for key in (6,7,13)) or not body[8] or not body[9] or body[10]==0 or body[11]==0 or body[12]==0 or body[14]==0 or not (0<body[15]<body[16]): raise DecodeError("command lease semantics")
    elif kind == "owner-command-effect":
        if body[1]!=1 or body[6] not in command_kinds or body[6] not in command_targets or body[8]!=command_targets[body[6]] or body[5] is None or len(body[7])!=16 or not all(digest(body[key]) for key in (12,15,17,18,19)) or body[20]>=body[21]: raise DecodeError("owner command effect semantics")
        if body[8]=="agent" and body[9]!=body[5] or body[8]=="owner" and body[9]!=body[4]: raise DecodeError("owner command target identity semantics")
    elif kind == "owner-command-attempt":
        if not all(digest(body[key]) for key in (1,2,3,4,8)) or body[5]==0 or body[6]==0 or body[7]==0 or not (0<body[10]<body[11]): raise DecodeError("owner command attempt semantics")
    elif kind == "semantic-confirmation":
        if body[1]!="tos.owner-command-confirmation.v1" or body[2]!=1 or body[3] not in {"bounded","high"} or not body[4] or not body[5] or not digest(body[6]) or body[7] not in command_kinds or not body[8] or not isinstance(body[10],bytes) or not isinstance(body[12],bytes) or len(body[13])!=3 or body[14]==0: raise DecodeError("semantic confirmation semantics")
    elif kind == "owner-command-resolution":
        states={"prepared","admitted","submitted","ambiguous","applied","rejected","conflict","expired","terminal"}
        if body[1] not in states or not digest(body[2]) or not digest(body[4]) or not digest(body[5]) or not body[9] or body[12]==0 or body[3] is not None and not digest(body[3]) or body[8] is not None and not digest(body[8]): raise DecodeError("owner command resolution semantics")
        if body[1]=="prepared" and (body[3] is not None or body[7] is not None or body[11] is not None): raise DecodeError("prepared resolution terminal fields")
        if body[1]=="applied" and (body[3] is None or body[7] is None or body[11] is not None): raise DecodeError("applied resolution evidence")
    elif kind == "owner-exit-plan":
        if len(body[1])!=16 or not body[2] or not all(digest(body[key]) for key in (3,5,6,7,8)) or body[4]!="fence-new-work" or body[9] is not None or body[10]!=1: raise DecodeError("owner exit semantics")
    elif kind == "migration":
        if body[1]!=1 or len(body[2])!=16 or not body[3] or not body[4] or len(body[5])!=16 or body[6]==0 or body[7]==0 or not all(digest(body[key]) for key in (8,9,11,12,15,16,19,21)) or body[10]==0 or body[13]==0 or body[14]==0 or body[17]==0 or body[18]<=body[17] or not body[20] or body[22] is not None or body[23]!="prepared" or body[24]==0: raise DecodeError("migration semantics")
    elif kind == "action-outcome-evidence":
        if body[1]!=1 or len(body[2])!=16 or not body[3] or not body[4] or body[5] not in {"mcp-tool","capability-use"} or not all(digest(body[key]) for key in (6,7,10)) or not body[11] or body[12]==0 or body[9] not in {"succeeded","failed","killed","rejected"} or not (0<body[14]<=body[13]<body[15]): raise DecodeError("action outcome evidence semantics")
        if body[5]=="mcp-tool" and body[8] is not None or body[5]=="capability-use" and not digest(body[8]): raise DecodeError("action outcome execution identity")
    else:
        raise DecodeError("released body kind lacks an independent semantic verifier")

def verify_vector(vector, registry_digest, ed25519, schemas, command_kinds):
    raw=bytes.fromhex(vector["canonical_cbor_hex"])
    if not raw or len(raw)>MAX: raise DecodeError("size")
    wrapper,end=decode(raw)
    if end!=len(raw) or not isinstance(wrapper,dict) or set(wrapper)!={1,2,3,4,5,6,7,8,9}: raise DecodeError("wrapper shape")
    if wrapper[1]!=1 or wrapper[2]!="tos.trusted-capability-owner-control.v1" or wrapper[3]!=1 or wrapper[4]!=1: raise DecodeError("profile")
    if wrapper[5] != registry_digest: raise DecodeError("registry digest")
    if wrapper[8]!=vector["object_kind"]: raise DecodeError("kind")
    body,end=decode(wrapper[9])
    if end!=len(wrapper[9]): raise DecodeError("body trailing")
    verify_body_schema(wrapper[8],body,schemas)
    verify_body_semantics(wrapper[8],body,command_kinds)
    preimage=PROFILE + (vector["object_kind"]+".v1").encode() + b"\0" + struct.pack(">I",len(raw)) + raw
    if preimage.hex()!=vector["digest_preimage_hex"]: raise DecodeError("preimage")
    if hashlib.sha256(preimage).hexdigest()!=vector["object_digest_hex"]: raise DecodeError("digest")
    if wrapper[8] == "authorization-envelope":
        if not isinstance(body,dict) or set(body)!={1,2} or len(body[2]) != 1: raise DecodeError("authorization envelope shape")
        auth=body[1]; proof=body[2][0]
        if not isinstance(auth,dict) or not isinstance(proof,dict): raise DecodeError("authorization fields")
        public=proof[3]; signature=proof[4]
        keyref=hashlib.sha256(b"tos.profile-proof.ed25519.v1/key-reference\0"+public).digest()
        if proof[1] != "tos.profile-proof.ed25519.v1" or proof[2] != keyref: raise DecodeError("proof key reference")
        if auth[16] != {1:"verification-key",2:"tos.profile-proof.ed25519.v1",3:keyref}: raise DecodeError("issuer subject")
        unsigned=dict(proof); unsigned[4]=None
        proofset=hashlib.sha256(encode([unsigned])).digest()
        if auth[22] != proofset: raise DecodeError("proof set digest")
        authwire=encode(auth)
        message=hashlib.sha256(b"tos.profile-authorization-envelope.v1/signature\0"+struct.pack(">I",len(authwire))+authwire).digest()
        if not ed25519(public,message,signature): raise DecodeError("authorization signature")

def main():
    root=Path(__file__).resolve().parents[1]; parser=argparse.ArgumentParser(); parser.add_argument("--vectors",type=Path,default=root/"test-vectors/trusted-capability-owner-control-v1.json"); parser.add_argument("--registry",type=Path,default=root/"schemas/trusted-capability-owner-control-v1.json"); parser.add_argument("--body-schemas",type=Path,default=root/"schemas/trusted-capability-bodies-v1.json"); args=parser.parse_args()
    doc=json.loads(args.vectors.read_text())
    registry_doc=json.loads(args.registry.read_text())
    if doc.get("schema")!="tos.trusted-capability-owner-control-conformance.v1": raise SystemExit("wrong schema")
    kinds=registry_doc["properties"]["object_kinds"]["const"]
    if doc.get("registry_object_kinds") != kinds: raise DecodeError("schema/codec object-kind registry mismatch")
    command_kinds=registry_doc["properties"]["owner_command_kinds"]["const"]
    if doc.get("owner_command_kinds") != command_kinds: raise DecodeError("owner-command registry mismatch")
    command_profiles=registry_doc["properties"]["owner_command_profiles"]["const"]
    if doc.get("owner_command_profiles") != command_profiles or [item["command_kind"] for item in command_profiles] != command_kinds: raise DecodeError("owner-command profile registry mismatch")
    registry=bytes.fromhex(doc["registry_canonical_cbor_hex"])
    expected_registry=encode([{1:kind,2:kind+".v1",3:1} for kind in kinds])
    if registry != expected_registry: raise DecodeError("Go/Python registry bytes differ")
    registry_digest=hashlib.sha256(b"tos.trusted-capability-owner-control.v1/registry\0"+registry).digest()
    if registry_digest.hex()!=doc["registry_digest_hex"]: raise DecodeError("registry commitment")
    sibling=Path(__file__).with_name("agent-commerce-reference.py")
    spec=importlib.util.spec_from_file_location("agent_commerce_reference", sibling)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    body_schema_doc=json.loads(args.body_schemas.read_text())
    if body_schema_doc.get("schema") != "tos.trusted-capability-body-schemas.v1" or body_schema_doc.get("registry_digest_hex") != doc["registry_digest_hex"]: raise DecodeError("body-schema registry binding mismatch")
    if body_schema_doc.get("body_schemas") != doc.get("body_schemas"): raise DecodeError("fixture/published body schemas differ")
    schemas={schema["object_kind"]:schema for schema in body_schema_doc["body_schemas"]}
    if set(schemas) != set(kinds): raise DecodeError("body-schema coverage mismatch")
    for schema in schemas.values():
        keys=[field["cbor_key"] for field in schema["fields"]]
        if not keys or keys != list(range(1,len(keys)+1)): raise DecodeError("body-schema CBOR keys are not contiguous")
    covered={vector["object_kind"] for vector in doc["vectors"]}
    if covered != set(kinds): raise DecodeError("object-kind fixture coverage mismatch")
    command_covered={vector["name"].removeprefix("owner-command-") for vector in doc["vectors"] if vector["name"].startswith("owner-command-")}
    if command_covered != set(command_kinds): raise DecodeError("owner-command fixture coverage mismatch")
    for vector in doc["vectors"]: verify_vector(vector, registry_digest, module.verify_ed25519, schemas, command_kinds)
    for mutation in doc.get("negative_vectors", []):
        try:
            raw=bytes.fromhex(mutation["canonical_cbor_hex"])
            wrapper,end=decode(raw)
            if end != len(raw): raise DecodeError("trailing")
            body,end=decode(wrapper[9])
            if end != len(wrapper[9]): raise DecodeError("body trailing")
            verify_body_schema(mutation["object_kind"],body,schemas)
            verify_body_semantics(mutation["object_kind"],body,command_kinds)
        except (DecodeError, IndexError, KeyError, ValueError):
            continue
        raise DecodeError("negative vector accepted: "+mutation["name"])
    print(f"verified {len(doc['vectors'])} trusted-capability vectors and {len(doc.get('negative_vectors', []))} executable negative mutations")

if __name__=="__main__": main()
