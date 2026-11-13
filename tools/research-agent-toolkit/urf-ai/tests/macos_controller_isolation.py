"""Hosted macOS genuine peer-UID and key permissions acceptance (no pytest)."""
from __future__ import annotations
import json
import os
from pathlib import Path
import pwd
import socket
import subprocess
import sys
import tempfile
import threading
from urf_ai.csts import ClaimJournal
from urf_ai.controller_boundary_candidate import IdentityPolicy, serve_urf
from urf_ai.evidence import digest

def fail(msg):
    raise AssertionError(msg)

if os.uname().sysname != "Darwin":
    fail("macOS-only gate cannot pass elsewhere")
uid=os.getuid()
candidates=("nobody","_www","_daemon","daemon")
worker_account=None
worker_uid=None
for candidate in candidates:
    try:
        entry=pwd.getpwnam(candidate)
    except KeyError:
        continue
    if entry.pw_uid not in (0,uid):
        worker_account=candidate
        worker_uid=entry.pw_uid
        break
if worker_account is None:
    fail("NO_DISTINCT_NONROOT_WORKER_ACCOUNT")

root=Path(tempfile.mkdtemp(prefix="urf-ai-macos-"))
os.chmod(root,0o711)
keyfile=root/"key"
keyfile.write_bytes(os.urandom(32))
os.chmod(keyfile,0o600)
socket_path=str(root/"controller.sock")
j=ClaimJournal(keyfile.read_bytes(),{"curator":"AUTHOR"},{})
claim={"claim_id":"c","semantic_version":1,"kind":"THEOREM","state":"OPEN",
       "proposition":"test statement","scope":{"domain":"synthetic"},
       "assumptions":[],"dependencies":[],"frontier":[],"boundaries":[],
       "source_revision":{"repo":"test","commit":"a"*40},"author":"curator"}
j.apply(event_id="r1",kind="REGISTER",claim_id="c",actor="curator",
        expected_version=0,payload=claim,reason="synthetic acceptance")
req={"op":"assess","claim_id":"c",
     "proposal":{"claim_id":"c","semantic_version":1,
                 "proposition_digest":digest(claim["proposition"]),
                 "scope_digest":digest(claim["scope"]),
                 "source_revision":claim["source_revision"],"assertion":"OPEN"}}
policy=IdentityPolicy(uid,worker_uid)
errors=[]
def run():
    try:
        serve_urf(socket_path,policy,j,max_connections=2)
    except Exception as exc:
        errors.append(repr(exc))
thread=threading.Thread(target=run,daemon=True)
thread.start()

# Wait for bound listener, bounded by active attempt count.
import time
for _ in range(100):
    if os.path.exists(socket_path):
        break
    if errors:
        fail("listener failed: "+repr(errors))
    time.sleep(0.05)
else:
    fail("listener did not start")

def send(payload):
    with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as client:
        client.settimeout(3)
        client.connect(socket_path)
        client.sendall((json.dumps(payload)+"\n").encode("utf-8"))
        data=client.recv(4096)
        return json.loads(data)

same_uid=send(req)
if same_uid.get("allowed") is not False or same_uid.get("reason")!="UNAUTHORIZED_PEER":
    fail("same-UID request not denied: "+repr(same_uid))

worker_program = r"""
import json, socket, sys
sockpath, keypath, wire=sys.argv[1:]
key_denied=False
try:
    with open(keypath,"rb") as stream: stream.read()
except PermissionError:
    key_denied=True
with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as c:
    c.settimeout(5)
    c.connect(sockpath)
    c.sendall((wire+"\n").encode())
    response=json.loads(c.recv(4096))
print(json.dumps({"key_denied":key_denied,"response":response}))
"""
proc=subprocess.run(["sudo","-n","-u",worker_account,sys.executable,"-c",
                     worker_program,socket_path,str(keyfile),json.dumps(req)],
                    capture_output=True,text=True,timeout=20,check=False)
if proc.returncode != 0:
    fail("CROSS_UID_WORKER_FAILED: returncode=%d stderr=%r stdout=%r" %
         (proc.returncode, proc.stderr[-2000:], proc.stdout[-1000:]))
result=json.loads(proc.stdout)
if result["key_denied"] is not True:
    fail("worker could read controller key")
if result["response"].get("allowed") is not True or result["response"].get("level")!="OPEN":
    fail("real cross-UID assessment failed: "+repr(result))
thread.join(timeout=5)
if thread.is_alive() or errors:
    fail("listener did not exit cleanly: "+repr(errors))
if j.claim("c")["state"]!="OPEN":
    fail("read-only channel changed claim status")
print("MACOS_KERNEL_CROSS_UID := PASS")
print("MACOS_SYNTHETIC_KEY_ISOLATION := PASS")
print("MACOS_REAL_JOURNAL_READ_ONLY := PASS")
print("MACOS_CRASH_RECOVERY := OPEN (in-memory journal has no durable replay)")
