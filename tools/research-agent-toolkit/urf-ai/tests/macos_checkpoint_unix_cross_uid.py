"""Hosted macOS: true cross-UID writer authority, bounded IPC and replay denial.

The writer remains under the runner UID; a distinct sudo user performs
controller requests. The fake DynamoDB backend proves protocol behavior,
NOT AWS credentials, IAM or remote persistence.
"""
import json
import os
from pathlib import Path
import pwd
import socket
import subprocess
import sys
import tempfile
import threading
import time

from urf_ai.checkpoint_write_service_candidate import CheckpointWriteService
from urf_ai.checkpoint_unix_transport_candidate import serve_checkpoint_unix
from urf_ai.dynamodb_checkpoint_candidate import DynamoDBCheckpoint

if sys.platform!="darwin":
    raise AssertionError("MACOS_ONLY")
writer_uid=os.getuid()
controller_account=None
controller_uid=None
for name in ("nobody","_www","_daemon","daemon"):
    try: account=pwd.getpwnam(name)
    except KeyError: continue
    if account.pw_uid not in (0,writer_uid):
        controller_account=name
        controller_uid=account.pw_uid
        break
if controller_account is None:
    raise AssertionError("NO_DISTINCT_UNPRIVILEGED_UID")

class CASFailed(Exception):
    response={"Error":{"Code":"ConditionalCheckFailedException"}}

class FakeDynamoDB:
    def __init__(self):
        self.item={"checkpoint_id":{"S":"fixture"},"seq":{"N":"0"},
                   "digest":{"S":"GENESIS"}}
    def get_item(self,**args):
        assert args["ConsistentRead"] is True
        return {"Item":dict(self.item)}
    def update_item(self,**args):
        assert args["ConditionExpression"]=="#s = :old_seq AND #d = :old_digest"
        values=args["ExpressionAttributeValues"]
        if (values[":old_seq"]!=self.item["seq"]
            or values[":old_digest"]!=self.item["digest"]):
            raise CASFailed()
        self.item["seq"]=values[":new_seq"]
        self.item["digest"]=values[":new_digest"]
        return {"ResponseMetadata":{"HTTPStatusCode":200}}

directory=Path(tempfile.mkdtemp(prefix="urf-ai-writer-",dir="/private/tmp"))
os.chmod(directory,0o711)
credential=directory/"synthetic-writer-credential"
credential.write_bytes(os.urandom(32))
os.chmod(credential,0o600)
endpoint=str(directory/"checkpoint.sock")
backend=DynamoDBCheckpoint(client=FakeDynamoDB(),table_name="fixture",
                            checkpoint_id="fixture")
service=CheckpointWriteService(backend=backend,checkpoint_id="fixture")
exceptions=[]
def run():
    try:
        serve_checkpoint_unix(socket_path=endpoint,controller_uid=controller_uid,
                              service=service,max_connections=4)
    except BaseException as exc:
        exceptions.append(repr(exc))
thread=threading.Thread(target=run,daemon=True)
thread.start()
for _ in range(100):
    if os.path.exists(endpoint):
        break
    if exceptions:
        raise AssertionError("WRITER_FAILED: "+repr(exceptions))
    time.sleep(0.05)
else:
    raise AssertionError("WRITER_TIMEOUT")

# Writer's own UID is not authorized as the designated controller.
with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as c:
    c.settimeout(3)
    c.connect(endpoint)
    unauthorized=json.loads(c.recv(4096))
assert unauthorized=={"ok":False,"error":"DENIED"},unauthorized

client_script=r"""
import json,socket,sys
endpoint,credential=sys.argv[1:]
denied=False
try:
    with open(credential,"rb") as f: f.read()
except PermissionError:
    denied=True
def request(payload):
    with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as conn:
        conn.settimeout(5)
        conn.connect(endpoint)
        conn.sendall((json.dumps(payload)+"\n").encode())
        return json.loads(conn.recv(4096))
read=request({"op":"read"})
advance={"op":"advance","expected":[0,None],"proposed":[1,"a"*64]}
first=request(advance)
replay=request(advance)
print(json.dumps({"credential_denied":denied,"read":read,
                  "first":first,"replay":replay}))
"""
proc=subprocess.run(["sudo","-n","-u",controller_account,sys.executable,
                     "-B","-c",client_script,endpoint,str(credential)],
                    text=True,capture_output=True,timeout=25)
assert proc.returncode==0,(proc.returncode,proc.stdout,proc.stderr)
result=json.loads(proc.stdout)
assert result["credential_denied"] is True,result
assert result["read"]=={"ok":True,"checkpoint":[0,None]},result
assert result["first"]=={"ok":True,"advanced":True},result
assert result["replay"]=={"ok":True,"advanced":False},result
thread.join(timeout=5)
assert not thread.is_alive() and not exceptions,exceptions
assert backend.read()==(1,"a"*64)
print("MACOS_WRITER_KERNEL_PEER_AUTH := PASS")
print("MACOS_CONTROLLER_CREDENTIAL_DENIAL := PASS")
print("MACOS_CHECKPOINT_CAS_REPLAY_DENIAL := PASS")
print("AWS_IAM_AND_REMOTE_DURABILITY := NOT_RUN")
