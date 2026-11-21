"""A deliberately MINIMAL implementation of proposed CSTS v0.1 semantics.

Not CSTS v0.1 conformance, a theorem prover, or evidence of mathematics.
The controller authenticates events and delegated proof receipts using HMAC.
"""
from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass
import hashlib
import hmac
from .evidence import canonical, digest, attest, authenticate, validated_receipt

class TransitionRejected(ValueError):
    pass

@dataclass(frozen=True)
class Decision:
    claim_id: str
    version: int
    state: str
    event_hash: str

class ClaimJournal:
    """Append-only in-memory demonstration; no disk durability guarantee."""
    def __init__(self, secret: bytes, roles: dict[str,str], checker_allowlist: dict[str,str], policy_version: str="candidate.v0.1"):
        if len(secret) < 32: raise ValueError("secret too short")
        self._secret = secret
        self.roles = deepcopy(roles)
        self.allowlist = deepcopy(checker_allowlist)
        self.policy_version = policy_version
        self.records: dict[str,dict] = {}
        self.history: dict[str,list[dict]] = {}
        self.events: list[dict] = []
        self.event_ids: set[str] = set()

    def claim(self, cid: str) -> dict:
        result=deepcopy(self.records[cid])
        result["stale"] = self._is_stale(cid, set())
        return result

    def _is_stale(self, cid: str, trail: set[str]) -> bool:
        if cid in trail: return True
        rec=self.records[cid]
        for d in rec.get("dependencies",[]):
            did=d.get("claim_id")
            if did not in self.records: return True
            dep=self.records[did]
            if (d.get("semantic_version")!=dep["semantic_version"] or
                d.get("proposition_digest")!=digest(dep["proposition"]) or
                dep["state"]!="PROVED" or self._is_stale(did,trail|{cid})):
                return True
        return False

    def _verified_dependencies(self, claim: dict) -> bool:
        for dep in claim.get("dependencies", []):
            cid=dep.get("claim_id")
            if not isinstance(cid,str) or cid == claim["claim_id"] or cid not in self.records: return False
            current=self.records[cid]
            if (current["state"]!="PROVED" or self._is_stale(cid,set()) or
                dep.get("semantic_version")!=current["semantic_version"] or
                dep.get("proposition_digest")!=digest(current["proposition"])):
                return False
        return True

    def apply(self, *, event_id: str, kind: str, claim_id: str, actor: str, expected_version: int, payload: dict, reason: str, expected_prev_hash: str | None=None) -> Decision:
        if event_id in self.event_ids or not event_id or not reason:
            raise TransitionRejected("duplicate/invalid event identity or reason")
        prev = self.events[-1]["event_hash"] if self.events else "0"*64
        if expected_prev_hash is not None and prev != expected_prev_hash:
            raise TransitionRejected("event chain is stale")
        role = self.roles.get(actor)
        permitted = {
            "REGISTER": {"AUTHOR","MAINTAINER"},
            "ATTACH_EVIDENCE": {"AUTHOR","VERIFIER"},
            "PROMOTE_PROVED": {"REVIEWER"},
            "SET_CONDITIONAL": {"REVIEWER"},
            "REVISE": {"AUTHOR","MAINTAINER"},
            "REVOKE": {"MAINTAINER"},
        }
        if kind not in permitted or role not in permitted[kind]:
            raise TransitionRejected("actor not authorized for transition")
        if not isinstance(payload, dict): raise TransitionRejected("payload must be an object")
        old = self.records.get(claim_id)
        if kind == "REGISTER":
            if old or expected_version != 0: raise TransitionRejected("registration conflict")
            nxt=deepcopy(payload)
            required={"claim_id","semantic_version","kind","state","proposition","scope","assumptions","dependencies","frontier","boundaries","source_revision","author"}
            if not required <= set(nxt) or nxt["claim_id"] != claim_id or nxt["semantic_version"] != 1 or nxt["state"] != "OPEN" or nxt["kind"] not in {"THEOREM","FRONTIER","CERTIFICATE","INTERFACE"}:
                raise TransitionRejected("invalid initial claim identity/scope")
            if nxt["author"] != actor or not isinstance(nxt["scope"],dict) or not nxt["scope"].get("domain") or not nxt["proposition"] or not isinstance(nxt["dependencies"],list):
                raise TransitionRejected("registration has incomplete scope/author/proposition")
            if nxt["kind"] == "THEOREM" and any(x.get("claim_id")==claim_id for x in nxt["dependencies"]):
                raise TransitionRejected("self dependency forbidden")
            nxt["evidence"] = []
            nxt["stale"] = False
        else:
            if not old or old["semantic_version"] != expected_version:
                raise TransitionRejected("claim absent or semantic version changed")
            nxt=deepcopy(old)
            if kind == "ATTACH_EVIDENCE":
                if old["state"] == "WITHDRAWN": raise TransitionRejected("withdrawn claim immutable")
                env=payload.get("receipt")
                ok,detail=validated_receipt(env,nxt,self._secret,self.allowlist,self.roles)
                if not ok: raise TransitionRejected("unbound evidence: "+detail)
                nxt["evidence"].append(deepcopy(env))
            elif kind == "SET_CONDITIONAL":
                if nxt["kind"] != "THEOREM" or nxt["state"] != "OPEN": raise TransitionRejected("invalid conditional transition")
                if not nxt["assumptions"] or not any(a.get("status") != "DISCHARGED" for a in nxt["assumptions"]):
                    raise TransitionRejected("no explicitly conditional assumptions")
                # A conditional proof receipt must still bind exactly, and must be endorsed by this reviewer.
                env=payload.get("receipt")
                ok,detail=validated_receipt(env,nxt,self._secret,self.allowlist,self.roles)
                if not ok or env["payload"]["reviewer"]!=actor: raise TransitionRejected(detail)
                nxt["evidence"].append(deepcopy(env))
                nxt["state"]="CONDITIONAL"
            elif kind == "PROMOTE_PROVED":
                if nxt["kind"]!="THEOREM" or nxt["state"] not in {"OPEN","CONDITIONAL"} or nxt.get("stale",False):
                    raise TransitionRejected("invalid theorem promotion source")
                if any(a.get("status")!="DISCHARGED" for a in nxt["assumptions"]): raise TransitionRejected("undischarged assumption")
                if any(f.get("status")=="OPEN" and f.get("blocking",True) for f in nxt["frontier"]): raise TransitionRejected("open blocking frontier")
                if any(b.get("active",False) and b.get("blocks_proved",False) for b in nxt["boundaries"]): raise TransitionRejected("active boundary lock")
                if not self._verified_dependencies(nxt): raise TransitionRejected("stale or unproved dependencies")
                env=payload.get("receipt")
                ok,detail=validated_receipt(env,nxt,self._secret,self.allowlist,self.roles)
                if not ok or env["payload"]["reviewer"] != actor: raise TransitionRejected(detail)
                nxt["evidence"].append(deepcopy(env))
                nxt["state"] = "PROVED"
            elif kind == "REVISE":
                if nxt["state"]=="WITHDRAWN": raise TransitionRejected("withdrawn claim cannot be revised")
                if not isinstance(payload.get("changes"),dict) or not payload["changes"]: raise TransitionRejected("revision changes required")
                allowed={"proposition","scope","assumptions","dependencies","frontier","boundaries","source_revision"}
                if not set(payload["changes"]) <= allowed: raise TransitionRejected("revision attempted to modify protected identity")
                nxt.update(deepcopy(payload["changes"]))
                nxt["semantic_version"]+=1
                nxt["state"]="OPEN"
                nxt["evidence"]=[]
                nxt["stale"]=False
                if not nxt["proposition"] or not nxt["scope"].get("domain"): raise TransitionRejected("invalid revised statement/scope")
            elif kind == "REVOKE":
                if nxt["state"] not in {"PROVED","CONDITIONAL"}: raise TransitionRejected("not a verified state")
                nxt["state"]="OPEN"
                nxt["evidence"]=[]
                nxt["stale"]=False
        # Forbid dangling references and cycles in the candidate dependency graph.
        deps={cid:r.get("dependencies",[]) for cid,r in self.records.items()}
        deps[claim_id]=nxt.get("dependencies",[])
        for cid,edges in deps.items():
            if not isinstance(edges,list) or any(not isinstance(x,dict) or x.get("claim_id") not in deps for x in edges):
                raise TransitionRejected("missing or malformed dependency")
        def visit(cid,active,completed):
            if cid in active: raise TransitionRejected("dependency cycle")
            if cid in completed: return
            active.add(cid)
            for d in deps[cid]: visit(d["claim_id"],active,completed)
            active.remove(cid);completed.add(cid)
        completed=set()
        for cid in deps: visit(cid,set(),completed)
        # All mutations below are applied only after every guard has succeeded.
        event = {"event_id":event_id,"kind":kind,"claim_id":claim_id,"actor":actor,"role":role,"expected_version":expected_version,
                 "payload_digest":digest(payload),"payload":deepcopy(payload),"post_state_digest":digest(nxt),
                 "reason":reason,"policy_version":self.policy_version,
                 "previous_event_hash":prev,"seq":len(self.events)+1}
        event["event_hash"]=digest(event)
        event["mac"]=hmac.new(self._secret,canonical(event),hashlib.sha256).hexdigest()
        if old: self.history.setdefault(claim_id,[]).append(deepcopy(old))
        self.records[claim_id]=nxt
        self.events.append(event)
        self.event_ids.add(event_id)
        return Decision(claim_id,nxt["semantic_version"],nxt["state"],event["event_hash"])

    def audit_events(self) -> bool:
        prev="0"*64
        seen=set()
        for n,item in enumerate(self.events,1):
            e=deepcopy(item)
            supplied=e.pop("mac",None)
            provided_hash=e.pop("event_hash",None)
            if (e.get("seq")!=n or e.get("previous_event_hash")!=prev or
                e.get("event_id") in seen or digest(e.get("payload"))!=e.get("payload_digest") or digest(e)!=provided_hash):
                return False
            e["event_hash"]=provided_hash
            expected=hmac.new(self._secret,canonical(e),hashlib.sha256).hexdigest()
            if not isinstance(supplied,str) or not hmac.compare_digest(expected,supplied): return False
            prev=provided_hash
            seen.add(e["event_id"])
        # The last event for each claim must bind to its current unmodified record.
        last={}
        for event in self.events: last[event["claim_id"]]=event["post_state_digest"]
        if any(digest(self.records[cid])!=state_hash for cid,state_hash in last.items()):
            return False
        return True
