"""Experimental authenticated atomic snapshot for a single trusted controller.

A verified write is durable before its result is acknowledged. This provides
crash recovery for this bounded candidate, NOT an externally protected anti-
rollback mechanism or a claim that any mathematical result has been checked.
Only the controller UID may access the private parent directory.
"""
from __future__ import annotations
from copy import deepcopy
import hashlib
import hmac
import json
import os
import stat
import tempfile
from threading import RLock
from .csts import ClaimJournal, TransitionRejected
from .evidence import canonical

MAX_SNAPSHOT_BYTES = 8 * 1024 * 1024

class RecoveryRejected(ValueError):
    pass

def _private_directory(path):
    d=os.path.dirname(os.path.abspath(path))
    s=os.lstat(d)
    if not stat.S_ISDIR(s.st_mode) or s.st_uid!=os.getuid() or stat.S_IMODE(s.st_mode)!=0o700:
        raise RecoveryRejected("UNTRUSTED_STORAGE_DIRECTORY")
    return d

def _read_snapshot(path):
    flags=os.O_RDONLY
    if hasattr(os,"O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd=os.open(path,flags)
    try:
        s=os.fstat(fd)
        if (not stat.S_ISREG(s.st_mode) or s.st_uid != os.getuid()
            or stat.S_IMODE(s.st_mode) != 0o600 or not 0 < s.st_size <= MAX_SNAPSHOT_BYTES):
            raise RecoveryRejected("UNSAFE_SNAPSHOT_FILE")
        with os.fdopen(fd,"rb",closefd=False) as f:
            raw=f.read(MAX_SNAPSHOT_BYTES+1)
        if len(raw)!=s.st_size or len(raw)>MAX_SNAPSHOT_BYTES:
            raise RecoveryRejected("INVALID_SNAPSHOT_LENGTH")
        return json.loads(raw)
    finally:
        os.close(fd)

class DurableJournalOwner:
    """Single-process owner. Never give this object to an untrusted worker."""

    def __init__(self, *, path, secret, roles, checker_allowlist, policy_version="candidate.v0.1"):
        if type(secret) is not bytes or len(secret)<32:
            raise RecoveryRejected("INVALID_SECRET")
        self.path=os.path.abspath(path)
        self.directory=_private_directory(self.path)
        self.secret=secret
        self.roles=deepcopy(roles)
        self.allowlist=deepcopy(checker_allowlist)
        self.policy_version=policy_version
        self._lock=RLock()
        self._poisoned=False
        self.journal=ClaimJournal(secret,roles,checker_allowlist,policy_version)
        if os.path.lexists(self.path):
            self._restore(_read_snapshot(self.path))

    def _fields(self, journal):
        return {"schema":"urf-ai.snapshot.v1","policy_version":self.policy_version,
                "roles":deepcopy(self.roles),"allowlist":deepcopy(self.allowlist),
                "records":deepcopy(journal.records),"history":deepcopy(journal.history),
                "events":deepcopy(journal.events),
                "event_ids":sorted(journal.event_ids)}

    def _candidate(self, data):
        if type(data) is not dict or set(data)!={"schema","policy_version","roles",
              "allowlist","records","history","events","event_ids"}:
            raise RecoveryRejected("INVALID_SNAPSHOT_SCHEMA")
        if (data["schema"]!="urf-ai.snapshot.v1" or data["roles"]!=self.roles
            or data["allowlist"]!=self.allowlist or data["policy_version"]!=self.policy_version):
            raise RecoveryRejected("SCOPE_OR_POLICY_MISMATCH")
        if (type(data["records"]) is not dict or type(data["events"]) is not list
            or type(data["history"]) is not dict or type(data["event_ids"]) is not list):
            raise RecoveryRejected("INVALID_SNAPSHOT_SHAPE")
        j=ClaimJournal(self.secret,self.roles,self.allowlist,self.policy_version)
        j.records=deepcopy(data["records"])
        j.events=deepcopy(data["events"])
        j.history=deepcopy(data["history"])
        j.event_ids=set(data["event_ids"])
        if (len(j.event_ids)!=len(data["event_ids"])
            or j.event_ids!={e["event_id"] for e in j.events}
            or not j.audit_events()):
            raise RecoveryRejected("INVALID_EVENT_LEDGER")
        return j

    def _restore(self, envelope):
        if type(envelope) is not dict or set(envelope)!={"data","mac"}:
            raise RecoveryRejected("INVALID_ENVELOPE")
        data=envelope["data"]
        supplied=envelope["mac"]
        if type(supplied) is not str:
            raise RecoveryRejected("INVALID_MAC")
        try:
            expect=hmac.new(self.secret,canonical(data),hashlib.sha256).hexdigest()
            if not hmac.compare_digest(expect,supplied):
                raise RecoveryRejected("AUTHENTICATION_FAILED")
            candidate=self._candidate(data)
        except (ValueError,TypeError,KeyError,RecursionError) as e:
            raise RecoveryRejected("RECOVERY_FAILED") from e
        self._swap(candidate)

    def _swap(self, candidate):
        with self.journal._lock:
            self.journal.records=deepcopy(candidate.records)
            self.journal.history=deepcopy(candidate.history)
            self.journal.events=deepcopy(candidate.events)
            self.journal.event_ids=set(candidate.event_ids)

    def _persist(self, candidate):
        data=self._fields(candidate)
        tag=hmac.new(self.secret,canonical(data),hashlib.sha256).hexdigest()
        encoded=canonical({"data":data,"mac":tag})
        if len(encoded)>MAX_SNAPSHOT_BYTES:
            raise RecoveryRejected("SNAPSHOT_SIZE_LIMIT")
        fd,temp=tempfile.mkstemp(prefix=".urf-ai-snapshot-",dir=self.directory)
        try:
            with os.fdopen(fd,"wb") as file:
                file.write(encoded)
                file.flush()
                os.fsync(file.fileno())
            os.replace(temp,self.path)
            dfd=os.open(self.directory,os.O_RDONLY)
            try:
                os.fsync(dfd)
            finally:
                os.close(dfd)
        finally:
            if os.path.lexists(temp):
                os.unlink(temp)

    def apply(self, **kwargs):
        with self._lock, self.journal._lock:
            if self._poisoned:
                raise RecoveryRejected("OWNER_POISONED")
            candidate=self._candidate(self._fields(self.journal))
            decision=candidate.apply(**kwargs)
            if self._poisoned:
                raise RecoveryRejected("OWNER_POISONED")
            try:
                self._persist(candidate)
            except BaseException:
                # If rename succeeded but directory fsync failed, disk and
                # memory may disagree. Poison the in-memory event audit.
                self._poisoned=True
                self.journal.records["__storage_unavailable__"] = {
                    "state":"WITHDRAWN"
                }
                raise
            self._swap(candidate)
            return decision

    def audited_claim(self, cid):
        with self._lock:
            if self._poisoned:
                raise RecoveryRejected("OWNER_POISONED")
            return self.journal.audited_claim(cid)
