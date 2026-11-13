"""Hosted macOS: kill controller with live socket, then recover locked owner and endpoint."""
from __future__ import annotations
import json
import os
from pathlib import Path
import signal
import socket
import stat
import subprocess
import sys
import tempfile
import time

if sys.platform != "darwin":
    raise AssertionError("MACOS_ONLY_TEST")

from urf_ai.durable_journal_candidate import DurableJournalOwner

KEY = b"synthetic-restart-key-controller-2026" * 2
ROLES = {"author": "AUTHOR"}
CLAIM = {"claim_id":"c", "semantic_version":1, "kind":"THEOREM",
         "state":"OPEN", "proposition":"synthetic restart",
         "scope":{"domain":"synthetic"}, "assumptions":[],
         "dependencies":[], "frontier":[], "boundaries":[],
         "source_revision":{"repo":"synthetic","commit":"a"*40},
         "author":"author"}
private=Path(tempfile.mkdtemp(prefix="urf-ai-owned-journal-"))
os.chmod(private,0o700)
sockdir=Path(tempfile.mkdtemp(prefix="urf-ai-owned-socket-",dir="/private/tmp"))
os.chmod(sockdir,0o711)
journal=str(private/"journal.json")
endpoint=str(sockdir/"service.sock")
marker=str(private/"recovered-marker")

child_script = """
import os,sys
from urf_ai.durable_journal_candidate import DurableJournalOwner
from urf_ai.controller_boundary_candidate import serve_owned_urf, IdentityPolicy
path, sock, marker, phase = sys.argv[1:]
secret=%r
roles=%r
claim=%r
j=DurableJournalOwner(path=path,secret=secret,roles=roles,checker_allowlist={})
if phase == 'initial':
    j.apply(event_id='register',kind='REGISTER',claim_id='c',actor='author',
            expected_version=0,payload=claim,reason='synthetic')
else:
    assert j.journal.audit_events()
    assert j.audited_claim('c')['state']=='OPEN'
    with open(marker,'w') as f: f.write('REPLAY_VERIFIED')
# The test client shares the controller UID and must always be denied.
policy=IdentityPolicy(os.getuid(),os.getuid()+1)
serve_owned_urf(sock,policy,j,max_connections=1)
""" % (KEY, ROLES, CLAIM)

def spawn(phase):
    return subprocess.Popen([sys.executable,"-B","-c",child_script,
                             journal, endpoint, marker, phase],
                            stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                            text=True)

def wait_for(test, process, label):
    for _ in range(120):
        if process.poll() is not None:
            out,err=process.communicate()
            raise AssertionError(label+" exited: "+repr((process.returncode,out,err)))
        if test():
            return
        time.sleep(0.05)
    raise AssertionError(label+" timeout")

first=spawn("initial")
try:
    wait_for(lambda: os.path.exists(endpoint) and os.path.exists(journal),
             first,"initial controller")
    initial_inode=os.lstat(endpoint).st_ino
    os.kill(first.pid,signal.SIGKILL)
    first.wait(timeout=5)
    assert os.path.exists(endpoint)
    assert stat.S_ISSOCK(os.lstat(endpoint).st_mode)
    recovered=spawn("recovered")
    try:
        wait_for(lambda: os.path.isfile(marker),recovered,"recovered journal")
        response=None
        for _ in range(120):
            if recovered.poll() is not None:
                break
            try:
                with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as c:
                    c.settimeout(1)
                    c.connect(endpoint)
                    response=json.loads(c.recv(4096))
                break
            except (ConnectionRefusedError,FileNotFoundError):
                time.sleep(0.05)
        assert response=={"allowed":False,"reason":"UNAUTHORIZED_PEER"},response
        recovered.wait(timeout=5)
        assert recovered.returncode==0,recovered.stderr.read()
        assert os.lstat(endpoint).st_ino != initial_inode
        assert Path(marker).read_text()=="REPLAY_VERIFIED"
    finally:
        if recovered.poll() is None:
            recovered.kill()
            recovered.wait(timeout=5)
finally:
    if first.poll() is None:
        first.kill()
        first.wait(timeout=5)
print("MACOS_CRASHED_SOCKET_REBIND := PASS")
print("MACOS_OWNED_JOURNAL_REPLAY := PASS")
print("MACOS_RESTART_UNAUTHORIZED_DENIAL := PASS")
print("VALID_SNAPSHOT_ROLLBACK := OPEN")
