"""Read-only OS-credential controller transport; experimental, not deployment approval.

Controller and worker must have different UIDs. The controller must be the sole
owner of journal objects and keys. This module never accepts a state transition.
"""
from __future__ import annotations
from dataclasses import dataclass
import ctypes
import errno
import json
import os
import socket
import stat
import struct
import sys
import secrets

MAX_REQUEST = 16384

class BoundaryError(ValueError):
    pass

@dataclass(frozen=True)
class IdentityPolicy:
    controller_uid: int
    worker_uid: int

    def __post_init__(self):
        if (type(self.controller_uid) is not int or type(self.worker_uid) is not int
            or self.controller_uid < 0 or self.worker_uid < 0
            or self.controller_uid == self.worker_uid):
            raise BoundaryError("INVALID_OR_SHARED_UID")

    def authorize_worker(self, uid: int) -> bool:
        return type(uid) is int and uid == self.worker_uid

def peer_uid(conn: socket.socket) -> int:
    """Kernel-attested Unix peer UID; never use caller-declared identity."""
    if sys.platform == "darwin":
        libc = ctypes.CDLL(None, use_errno=True)
        fn = libc.getpeereid
        fn.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_uint),
                       ctypes.POINTER(ctypes.c_uint))
        fn.restype = ctypes.c_int
        uid = ctypes.c_uint()
        gid = ctypes.c_uint()
        if fn(conn.fileno(), ctypes.byref(uid), ctypes.byref(gid)) != 0:
            code = ctypes.get_errno()
            raise OSError(code, "getpeereid failed")
        return uid.value
    if sys.platform.startswith("linux") and hasattr(socket, "SO_PEERCRED"):
        data = conn.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED,
                               struct.calcsize("3i"))
        return struct.unpack("3i", data)[1]
    raise BoundaryError("PEER_CREDENTIALS_UNSUPPORTED")

def read_request(conn: socket.socket) -> dict:
    conn.settimeout(2.0)
    data = bytearray()
    while len(data) <= MAX_REQUEST:
        chunk = conn.recv(min(2048, MAX_REQUEST + 1 - len(data)))
        if not chunk:
            break
        data.extend(chunk)
        if b"\n" in chunk:
            break
    if len(data) > MAX_REQUEST or data.count(b"\n") != 1 or not data.endswith(b"\n"):
        raise BoundaryError("INVALID_REQUEST_FRAME")
    try:
        request = json.loads(bytes(data[:-1]).decode("utf-8"))
    except (UnicodeError, ValueError) as exc:
        raise BoundaryError("INVALID_JSON") from exc
    if (type(request) is not dict or set(request) != {"op", "claim_id", "proposal"}
        or request["op"] != "assess"
        or type(request["claim_id"]) is not str
        or not (0 < len(request["claim_id"]) <= 256)
        or type(request["proposal"]) is not dict
        or request["proposal"].get("claim_id") != request["claim_id"]):
        raise BoundaryError("INVALID_REQUEST_SCHEMA")
    return request

def make_urf_assessor(journal):
    from urf_ai.csts import ClaimJournal
    from urf_ai.answer_gate import assess_from_journal
    if type(journal) is not ClaimJournal:
        raise BoundaryError("UNTRUSTED_JOURNAL_TYPE")

    def assess(proposal):
        verdict = assess_from_journal(journal, proposal)
        return {"allowed": verdict.allowed, "level": verdict.level}
    return assess

def process_connection(conn: socket.socket, policy: IdentityPolicy, assessor) -> None:
    try:
        if not policy.authorize_worker(peer_uid(conn)):
            result = {"allowed": False, "reason": "UNAUTHORIZED_PEER"}
        else:
            request = read_request(conn)
            assessed = assessor(request["proposal"])
            if (type(assessed) is not dict or type(assessed.get("allowed")) is not bool
                or type(assessed.get("level")) is not str):
                raise BoundaryError("INVALID_ASSESSOR_RESULT")
            result = {"allowed": assessed["allowed"], "level": assessed["level"],
                      "reason": ("AUTHENTICATED_CSTS_STATUS_ONLY"
                                 if assessed["allowed"] else "DENIED")}
    except Exception:
        result = {"allowed": False, "reason": "DENIED"}
    try:
        conn.sendall((json.dumps(result, separators=(",", ":")) + "\n").encode("utf-8"))
    except (BrokenPipeError, ConnectionResetError, OSError):
        # Disconnected clients must not terminate the server.
        return

def serve_urf(socket_path: str, policy: IdentityPolicy, journal, max_connections=None):
    # Candidate startup entry point. Never expose generic assessor callbacks.
    assessor = make_urf_assessor(journal)
    if os.getuid() != policy.controller_uid:
        raise BoundaryError("INCORRECT_CONTROLLER_UID")
    parent = os.path.dirname(os.path.abspath(socket_path))
    st = os.lstat(parent)
    if not stat.S_ISDIR(st.st_mode) or st.st_uid != os.getuid() or stat.S_IMODE(st.st_mode) != 0o711:
        raise BoundaryError("UNTRUSTED_SOCKET_DIRECTORY")
    if os.path.lexists(socket_path):
        raise BoundaryError("SOCKET_EXISTS")
    old_umask = os.umask(0o077)
    listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        listener.bind(socket_path)
        os.chmod(socket_path, 0o666)
        listener.listen(8)
        count = 0
        while max_connections is None or count < max_connections:
            conn, _ = listener.accept()
            with conn:
                process_connection(conn, policy, assessor)
            count += 1
    finally:
        os.umask(old_umask)
        listener.close()
        # Socket deletion is deliberately not automated.

def serve_owned_urf(socket_path: str, policy: IdentityPolicy, owner, max_connections=None, *, external_anchor=None):
    """Restartable socket service tied to an exclusively locked durable owner.

    Limited threat model: only the controller UID may change the 0711
    socket directory. A distinct untrusted worker UID cannot replace entries.
    Snapshot rollback and hostile same-UID mutation remain out of scope.
    """
    from .durable_journal_candidate import DurableJournalOwner
    from .answer_gate import assess_from_journal
    if type(owner) is not DurableJournalOwner:
        raise BoundaryError("INVALID_DURABLE_OWNER")
    if external_anchor is not None:
        from .external_anchor_candidate import ExternallyAnchoredJournal
        if (type(external_anchor) is not ExternallyAnchoredJournal
            or external_anchor._owner is not owner):
            raise BoundaryError("INVALID_EXTERNAL_ANCHOR")
    if os.getuid() != policy.controller_uid:
        raise BoundaryError("INCORRECT_CONTROLLER_UID")
    path = os.path.abspath(socket_path)
    parent = os.path.dirname(path)
    pst = os.lstat(parent)
    if (not stat.S_ISDIR(pst.st_mode) or pst.st_uid != os.getuid()
        or stat.S_IMODE(pst.st_mode) != 0o711):
        raise BoundaryError("UNTRUSTED_SOCKET_DIRECTORY")
    if not isinstance(max_connections, (int, type(None))) or (
        max_connections is not None and (type(max_connections) is not int or max_connections < 1)
    ):
        raise BoundaryError("INVALID_CONNECTION_BOUND")

    # Do not use a raw journal after a persistence failure or after releasing
    # the journal ownership lock. This check is repeated per request.
    with owner._lock:
        if owner._closed or owner._poisoned or owner._lock_fd is None:
            raise BoundaryError("OWNER_NOT_ACTIVE")
        if not owner.journal.audit_events():
            raise BoundaryError("INVALID_JOURNAL")
        if external_anchor is not None:
            external_anchor._check()

        def owned_assessor(proposal):
            with owner._lock:
                if owner._closed or owner._poisoned or owner._lock_fd is None:
                    return {"allowed": False, "level": "BLOCKED"}
                if external_anchor is not None:
                    external_anchor._check()
                verdict = assess_from_journal(owner.journal, proposal)
                return {"allowed": verdict.allowed, "level": verdict.level}

        # A fresh random pathname prevents accidental bind collisions.
        temporary = os.path.join(parent, ".urf-ai-" + secrets.token_hex(16) + ".sock")
        old_umask = os.umask(0o077)
        listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        installed = False
        try:
            listener.bind(temporary)
            os.chmod(temporary, 0o666)
            listener.listen(8)
            if os.path.lexists(path):
                prior = os.lstat(path)
                if (not stat.S_ISSOCK(prior.st_mode)
                    or prior.st_uid != os.getuid()):
                    raise BoundaryError("UNTRUSTED_EXISTING_ENDPOINT")
                probe = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                try:
                    result = probe.connect_ex(path)
                finally:
                    probe.close()
                if result == 0:
                    raise BoundaryError("LIVE_ENDPOINT_EXISTS")
                if result != errno.ECONNREFUSED:
                    raise BoundaryError("ENDPOINT_STATUS_UNCERTAIN")
                again = os.lstat(path)
                if (again.st_dev, again.st_ino) != (prior.st_dev, prior.st_ino):
                    raise BoundaryError("ENDPOINT_CHANGED")
            # Journal lock serializes controller owners; OS rename swaps
            # only the verified stale socket, never an arbitrary file.
            os.replace(temporary, path)
            installed = True
            count = 0
            while max_connections is None or count < max_connections:
                conn, _ = listener.accept()
                with conn:
                    process_connection(conn, policy, owned_assessor)
                count += 1
        finally:
            os.umask(old_umask)
            listener.close()
            # Endpoint remains on disk intentionally; next locked owner
            # verifies it is stale before atomic replacement.
            # Remove only our uninstalled random socket candidate.
            if not installed and os.path.lexists(temporary):
                os.unlink(temporary)
