"""Hosted macOS: true cross-UID writer authority, bounded IPC and replay denial.

The writer remains under the runner UID; a distinct sudo user performs
controller requests. The fake DynamoDB backend proves protocol behavior,
NOT AWS credentials, IAM or remote persistence.
"""
import json
import os
from pathlib import Path
import pwd
import shutil
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
# Hosted macOS runner workspace ancestors are private (sudo drops PYTHONPATH).
# Publish only candidate Python SOURCE, never test secrets, journal data,
# AWS configuration or credentials. All temporary bytes remain under /private/tmp.
public_root=directory/"public-source"
package_root=public_root/"urf_ai"
public_root.mkdir(mode=0o755)
package_root.mkdir(mode=0o755)
source_root=Path(__file__).resolve().parents[1]/"urf_ai"
for source in sorted(source_root.glob("*.py")):
    target=package_root/source.name
    shutil.copyfile(source,target)
    os.chmod(target,0o644)

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
import json,os,sys
endpoint,credential,writer_uid_arg,source_root=sys.argv[1:]
sys.path.insert(0, source_root)
from urf_ai.checkpoint_unix_transport_candidate import UnixCheckpointClient,TransportRejected
writer_uid=int(writer_uid_arg)
denied=False
try:
    with open(credential,"rb") as f: f.read()
except PermissionError:
    denied=True
wrong_uid=writer_uid+1
if wrong_uid == os.getuid():
    wrong_uid+=1
try:
    UnixCheckpointClient(endpoint,expected_writer_uid=wrong_uid).read()
except TransportRejected:
    wrong_writer_denied=True
else:
    wrong_writer_denied=False
client=UnixCheckpointClient(endpoint,expected_writer_uid=writer_uid)
read=client.read()
first=client.compare_and_advance((0,None),(1,"a"*64))
replay=client.compare_and_advance((0,None),(1,"a"*64))
print(json.dumps({"credential_denied":denied,
                  "wrong_writer_denied":wrong_writer_denied,
                  "read":list(read),"first":first,"replay":replay}))
"""
proc=subprocess.run(["sudo","-n","-u",controller_account,sys.executable,
                     "-B","-c",client_script,endpoint,str(credential),str(writer_uid),str(public_root)],
                    text=True,capture_output=True,timeout=25)
assert proc.returncode==0,(proc.returncode,proc.stdout,proc.stderr)
result=json.loads(proc.stdout)
assert result["credential_denied"] is True,result
assert result["wrong_writer_denied"] is True,result
assert result["read"]==[0,None],result
assert result["first"] is True,result
assert result["replay"] is False,result
thread.join(timeout=5)
assert not thread.is_alive() and not exceptions,exceptions
assert backend.read()==(1,"a"*64)
print("MACOS_WRITER_KERNEL_PEER_AUTH := PASS")
print("MACOS_CONTROLLER_CREDENTIAL_DENIAL := PASS")
print("MACOS_CHECKPOINT_CAS_REPLAY_DENIAL := PASS")
print("MACOS_CLIENT_WRITER_UID_AUTH := PASS")
print("MACOS_FALSE_WRITER_IDENTITY_DENIED := PASS")
print("AWS_IAM_AND_REMOTE_DURABILITY := NOT_RUN")
