"""Bounded Unix IPC protocol checks; authorized UID is simulated in these unit tests.

Actual kernel cross-UID process testing belongs to the hosted macOS gate.
No AWS connection and no deployment claims.
"""
import json
import os
import socket
import threading

import pytest

from urf_ai.checkpoint_unix_transport_candidate import (
    handle_checkpoint_connection, UnixCheckpointClient, TransportRejected,
    MAX_WIRE,
)
from urf_ai.checkpoint_write_service_candidate import CheckpointWriteService
from urf_ai.dynamodb_checkpoint_candidate import DynamoDBCheckpoint

class ConditionalFailed(Exception):
    response={"Error":{"Code":"ConditionalCheckFailedException"}}

class Stub:
    def __init__(self):
        self.state={"checkpoint_id":{"S":"audit"},
                    "seq":{"N":"0"},"digest":{"S":"GENESIS"}}
        self.calls=0
    def get_item(self,**kw):
        assert kw["ConsistentRead"] is True
        return {"Item":self.state.copy()}
    def update_item(self,**kw):
        self.calls+=1
        v=kw["ExpressionAttributeValues"]
        if self.state["seq"]!=v[":old_seq"] or self.state["digest"]!=v[":old_digest"]:
            raise ConditionalFailed()
        self.state["seq"]=v[":new_seq"]
        self.state["digest"]=v[":new_digest"]
        return {"ResponseMetadata":{"HTTPStatusCode":200}}

def service():
    mock=Stub()
    db=DynamoDBCheckpoint(client=mock,table_name="checkpoints",checkpoint_id="audit")
    return CheckpointWriteService(backend=db,checkpoint_id="audit"),mock

def session(svc,wire,controller_uid,monkeypatch,peer=None):
    import urf_ai.checkpoint_unix_transport_candidate as m
    if peer is not None:
        monkeypatch.setattr(m,"peer_uid",lambda sock:peer)
    left,right=socket.socketpair()
    result=[]
    def server():
        with left:
            handle_checkpoint_connection(left,controller_uid=controller_uid,service=svc)
    t=threading.Thread(target=server)
    t.start()
    with right:
        right.settimeout(3)
        if wire is not None:
            try:
                right.sendall(wire)
            except BrokenPipeError:
                pass
        data=right.recv(4096)
        result.append(json.loads(data))
    t.join(timeout=3)
    assert not t.is_alive()
    return result[0]

def test_unauthorized_same_uid_rejected_before_parsing():
    svc,mock=service()
    left,right=socket.socketpair()
    try:
        # The kernel attests this process's UID; same-UID writer/controller
        # is explicitly prohibited.
        with left:
            response=None
            worker=threading.Thread(target=lambda:handle_checkpoint_connection(
                left,controller_uid=os.getuid(),service=svc))
            worker.start()
            response=json.loads(right.recv(4096))
            worker.join(timeout=3)
        assert response=={"ok":False,"error":"DENIED"}
        assert mock.calls==0
    finally:
        right.close()

def test_valid_simulated_peer_can_advance_once_only(monkeypatch):
    svc,mock=service()
    other_uid=os.getuid()+1
    first=session(svc,b'{"op":"read"}\n',other_uid,monkeypatch,peer=other_uid)
    assert first=={"ok":True,"checkpoint":[0,None]}
    payload={"op":"advance","expected":[0,None],"proposed":[1,"a"*64]}
    wire=(json.dumps(payload)+"\n").encode()
    one=session(svc,wire,other_uid,monkeypatch,peer=other_uid)
    replay=session(svc,wire,other_uid,monkeypatch,peer=other_uid)
    assert one=={"ok":True,"advanced":True}
    assert replay=={"ok":True,"advanced":False}
    assert mock.calls==2

@pytest.mark.parametrize("wire",[
    b'{"op":"delete"}\n',
    b'{"op":"read","expected":[],"proposed":[]}\n',
    b'{"op":"read","uid":123}\n',
    b'{"op":"advance","expected":[0,null],"proposed":[2,"'+b"a"*64+b'"]}\n',
    b'{\n',
    b'{"op":"read"}\n{"op":"read"}\n',
    b"x"*(MAX_WIRE+1),
])
def test_malformed_request_fails_closed(wire,monkeypatch):
    svc,mock=service()
    uid=os.getuid()+1
    result=session(svc,wire,uid,monkeypatch,peer=uid)
    assert result=={"ok":False,"error":"DENIED"}
    assert mock.calls==0

def test_client_denies_missing_unix_server(tmp_path):
    c=UnixCheckpointClient(str(tmp_path/"missing.sock"))
    with pytest.raises(TransportRejected,match="WRITER_UNAVAILABLE"):
        c.read()

def test_client_never_accepts_malformed_server_reply(tmp_path):
    path=str(tmp_path/"server.sock")
    listener=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
    listener.bind(path)
    listener.listen(1)
    def responder():
        conn,_=listener.accept()
        with conn:
            conn.recv(4096)
            conn.sendall(b'{"ok":true,"checkpoint":[0,null],"extra":1}\n')
        listener.close()
    t=threading.Thread(target=responder)
    t.start()
    with pytest.raises(TransportRejected,match="INVALID_WRITER_REPLY"):
        UnixCheckpointClient(path).read()
    t.join(timeout=3)
    assert not t.is_alive()
