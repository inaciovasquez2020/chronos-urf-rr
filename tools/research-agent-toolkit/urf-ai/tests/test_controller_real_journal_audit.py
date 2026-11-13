"""Runs with actual URF-AI modules in repository CI; never skip missing imports."""
import json, os, socket
from copy import deepcopy
from urf_ai.csts import ClaimJournal
from urf_ai.evidence import attest, bindings, digest
from urf_ai.controller_boundary_candidate import IdentityPolicy, BoundaryError, make_urf_assessor, process_connection

KEY=b"synthetic-only-local-research-gate-2026"*2
BINARY="f"*64
ROLES={"author":"AUTHOR","verifier":"VERIFIER","reviewer":"REVIEWER"}
ALLOW={"lean":BINARY}

def make_journal():
    j=ClaimJournal(KEY, ROLES, ALLOW)
    claim=dict(claim_id="fixture", semantic_version=1, kind="THEOREM", state="OPEN",
               proposition="synthetic proposition", scope={"domain":"synthetic"},
               assumptions=[], dependencies=[], frontier=[], boundaries=[],
               source_revision={"repo":"fixture","commit":"a"*40},author="author")
    j.apply(event_id="register",kind="REGISTER",claim_id="fixture",actor="author",
            expected_version=0,payload=claim,reason="synthetic")
    return j

def proposal(j, assertion="PROVED"):
    c=j.claim("fixture")
    return dict(claim_id="fixture",semantic_version=c["semantic_version"],
                proposition_digest=digest(c["proposition"]),scope_digest=digest(c["scope"]),
                source_revision=deepcopy(c["source_revision"]),assertion=assertion)

def rpc(assessor, req, authorized=True):
    a,b=socket.socketpair()
    try:
        uid=os.getuid()
        policy=IdentityPolicy(uid+1,uid if authorized else uid+2)
        b.settimeout(3)
        b.sendall((json.dumps(req,separators=(",",":"))+"\n").encode())
        process_connection(a,policy,assessor)
        return json.loads(b.recv(4096))
    finally:
        a.close();b.close()

def request(j,assertion="PROVED"):
    return {"op":"assess","claim_id":"fixture","proposal":proposal(j,assertion)}

def test_open_denies_proved_allows_open():
    j=make_journal(); a=make_urf_assessor(j)
    assert not rpc(a,request(j))["allowed"]
    assert rpc(a,request(j,"OPEN"))["allowed"]
    assert j.claim("fixture")["state"]=="OPEN"

def test_promote_rpc_denied():
    j=make_journal(); req=request(j);req["op"]="PROMOTE_PROVED"
    assert not rpc(make_urf_assessor(j),req)["allowed"]
    assert j.claim("fixture")["state"]=="OPEN"

def test_role_and_key_injection_denied():
    j=make_journal();a=make_urf_assessor(j)
    for name,value in (("roles",{"worker":"REVIEWER"}),("secret",KEY.hex())):
        req=request(j);req[name]=value
        assert not rpc(a,req)["allowed"]
    assert j.roles==ROLES

def test_untrusted_peer_denied():
    j=make_journal()
    r=rpc(make_urf_assessor(j),request(j,"OPEN"),authorized=False)
    assert r["allowed"] is False and r["reason"]=="UNAUTHORIZED_PEER"

def test_signed_synthetic_status_only_and_forgery_denied():
    j=make_journal();c=j.claim("fixture")
    envelope=attest({**bindings(c),"schema":"urf-ai.receipt.v1",
                     "checker":{"name":"lean","binary_digest":BINARY},
                     "checker_result":"PASS","proof_digest":"e"*64,
                     "axioms":["Classical.choice","Quot.sound","propext"],
                     "author":"author","verifier":"verifier","reviewer":"reviewer"},KEY)
    j.apply(event_id="promote",kind="PROMOTE_PROVED",claim_id="fixture",
            actor="reviewer",expected_version=1,payload={"receipt":envelope},
            reason="synthetic signed status not theorem proof")
    a=make_urf_assessor(j)
    r=rpc(a,request(j))
    assert r["allowed"] is True and r["reason"]=="AUTHENTICATED_CSTS_STATUS_ONLY"
    j.records["unlogged"]={**j.records["fixture"],"claim_id":"unlogged"}
    assert rpc(a,request(j))["allowed"] is False

def test_error_fails_closed():
    j=make_journal()
    def assessor(_): raise KeyError("unexpected")
    assert rpc(assessor,request(j))["allowed"] is False

def test_same_uid_rejected():
    import pytest
    with pytest.raises(BoundaryError):
        IdentityPolicy(os.getuid(),os.getuid())

def test_disconnected_client_does_not_raise():
    j=make_journal();a,b=socket.socketpair()
    try:
        b.sendall((json.dumps(request(j))+"\n").encode());b.close()
        process_connection(a,IdentityPolicy(os.getuid()+1,os.getuid()),make_urf_assessor(j))
    finally:
        a.close()
