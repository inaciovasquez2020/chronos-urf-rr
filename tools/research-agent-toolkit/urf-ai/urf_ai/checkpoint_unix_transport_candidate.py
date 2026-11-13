"""Experimental local checkpoint writer IPC using kernel peer UID.

The writer and controller MUST run as distinct OS UIDs, and only the writer
process receives DynamoDB UpdateItem credentials. A 0711 writer-owned directory
and 0666 socket permit connect; OS peer credentials provide authorization.
This module does not configure processes, provision AWS, or establish remote TLS.
OS credential auth binds a UID, NOT a specific executable or human caller.
CAS prevents replay of an already applied update; it does not prevent arbitrary
forward digest poisoning by a compromised authorized controller.
"""
from __future__ import annotations

import json
import os
import socket
import stat
from .controller_boundary_candidate import peer_uid
from .external_anchor_candidate import ExternalAnchorRejected, _record
from .checkpoint_write_service_candidate import CheckpointWriteService

MAX_WIRE = 4096
class TransportRejected(ExternalAnchorRejected):
    pass


def _line(conn):
    conn.settimeout(3)
    chunks=bytearray()
    while len(chunks) <= MAX_WIRE:
        part=conn.recv(min(512, MAX_WIRE+1-len(chunks)))
        if not part:
            break
        chunks.extend(part)
        if b"\n" in part:
            break
    if (len(chunks)>MAX_WIRE or chunks.count(b"\n")!=1
        or not chunks.endswith(b"\n")):
        raise TransportRejected("BAD_FRAME")
    try:
        return json.loads(chunks[:-1].decode("utf-8"))
    except (ValueError,UnicodeError) as exc:
        raise TransportRejected("BAD_JSON") from exc


def _send(conn, value):
    raw=json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False).encode()+b"\n"
    if len(raw)>MAX_WIRE:
        raise TransportRejected("RESPONSE_TOO_LARGE")
    conn.sendall(raw)


def _tuple(value):
    if type(value) is not list or len(value)!=2:
        raise TransportRejected("BAD_CHECKPOINT_TUPLE")
    return _record(tuple(value))


def handle_checkpoint_connection(conn, *, controller_uid, service):
    """One bounded connection, no authorization from caller-supplied fields."""
    try:
        if (type(controller_uid) is not int or controller_uid < 0
            or controller_uid == os.getuid()
            or peer_uid(conn)!=controller_uid):
            raise TransportRejected("UNAUTHORIZED_PEER")
        msg=_line(conn)
        if type(msg) is not dict or set(msg) not in (
            {"op"}, {"op","expected","proposed"}):
            raise TransportRejected("INVALID_REQUEST")
        if msg["op"]=="read" and set(msg)=={"op"}:
            result=service.read()
            reply={"ok":True,"checkpoint":list(_record(result))}
        elif msg["op"]=="advance" and set(msg)=={"op","expected","proposed"}:
            before=_tuple(msg["expected"])
            after=_tuple(msg["proposed"])
            result=service.advance(expected=before,proposed=after)
            if type(result) is not bool:
                raise TransportRejected("INVALID_SERVICE_RESULT")
            reply={"ok":True,"advanced":result}
        else:
            raise TransportRejected("INVALID_OPERATION")
    except Exception:
        reply={"ok":False,"error":"DENIED"}
    try:
        _send(conn,reply)
    except OSError:
        pass


def serve_checkpoint_unix(*, socket_path, controller_uid, service, max_connections=None):
    if type(service) is not CheckpointWriteService:
        raise TransportRejected("INVALID_WRITER_SERVICE")
    if (type(controller_uid) is not int or controller_uid < 0
        or controller_uid == os.getuid()):
        raise TransportRejected("INVALID_CONTROLLER_UID")
    if (max_connections is not None and
        (type(max_connections) is not int or max_connections < 1)):
        raise TransportRejected("INVALID_CONNECTION_LIMIT")
    parent=os.path.dirname(os.path.abspath(socket_path))
    meta=os.lstat(parent)
    if (not stat.S_ISDIR(meta.st_mode) or meta.st_uid!=os.getuid()
        or stat.S_IMODE(meta.st_mode)!=0o711):
        raise TransportRejected("UNTRUSTED_WRITER_DIRECTORY")
    if os.path.lexists(socket_path):
        raise TransportRejected("WRITER_ENDPOINT_EXISTS")
    old_umask=os.umask(0o077)
    listener=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
    try:
        listener.bind(socket_path)
        os.chmod(socket_path,0o666)
        listener.listen(8)
        accepted=0
        while max_connections is None or accepted<max_connections:
            conn,_=listener.accept()
            with conn:
                handle_checkpoint_connection(conn,controller_uid=controller_uid,
                                             service=service)
            accepted+=1
    finally:
        listener.close()
        os.umask(old_umask)
        # Persistent endpoint is fail-closed on restart, not auto-unlinked.


class UnixCheckpointClient:
    """Unprivileged transport client; holds no AWS credentials."""
    def __init__(self, socket_path, *, expected_writer_uid):
        if type(socket_path) is not str or not socket_path or len(socket_path)>100:
            raise TransportRejected("INVALID_SOCKET_PATH")
        if (type(expected_writer_uid) is not int or expected_writer_uid < 0
            or expected_writer_uid == os.getuid()):
            raise TransportRejected("WRITER_UID_NOT_SEPARATED")
        self.socket_path=os.path.abspath(socket_path)
        self.writer_uid=expected_writer_uid

    def _request(self, payload):
        parent=os.path.dirname(self.socket_path)
        try:
            parent_stat=os.lstat(parent)
            socket_stat=os.lstat(self.socket_path)
        except OSError as exc:
            raise TransportRejected("WRITER_UNAVAILABLE") from exc
        if (not stat.S_ISDIR(parent_stat.st_mode)
            or parent_stat.st_uid != self.writer_uid
            or stat.S_IMODE(parent_stat.st_mode) != 0o711
            or not stat.S_ISSOCK(socket_stat.st_mode)
            or socket_stat.st_uid != self.writer_uid):
            raise TransportRejected("UNTRUSTED_WRITER_ENDPOINT")
        try:
            with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as conn:
                conn.settimeout(3)
                conn.connect(self.socket_path)
                # The kernel attests the connected peer; ownership of a
                # pathname alone is insufficient to authenticate the server.
                if peer_uid(conn) != self.writer_uid:
                    raise TransportRejected("WRITER_IDENTITY_MISMATCH")
                _send(conn,payload)
                response=_line(conn)
        except OSError as exc:
            raise TransportRejected("WRITER_UNAVAILABLE") from exc
        if type(response) is not dict or response.get("ok") is not True:
            raise TransportRejected("WRITER_DENIED")
        return response

    def read(self):
        reply=self._request({"op":"read"})
        if set(reply)!={"ok","checkpoint"}:
            raise TransportRejected("INVALID_WRITER_REPLY")
        return _tuple(reply["checkpoint"])

    def compare_and_advance(self, expected, proposed):
        a=_record(expected)
        b=_record(proposed)
        reply=self._request({"op":"advance","expected":list(a),"proposed":list(b)})
        if set(reply)!={"ok","advanced"} or type(reply["advanced"]) is not bool:
            raise TransportRejected("INVALID_WRITER_REPLY")
        return reply["advanced"]
