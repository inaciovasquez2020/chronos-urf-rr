"""Conditional anti-rollback boundary for a trusted external checkpoint service.

THREAT MODEL: checkpoint.read and checkpoint.compare_and_advance are atomic,
persistent, rollback-resistant, and outside the snapshot attacker's control.
No implementation of that trusted service is supplied here. An ordinary
local file, HMAC, or same-UID database does NOT satisfy this contract.

A missing checkpoint is never treated as an empty/genesis checkpoint.
The caller must provision the trusted checkpoint explicitly as (0, None)
before creating the first journal snapshot. Not production approval.
"""
from __future__ import annotations

import hashlib
import os
import stat

from .durable_journal_candidate import DurableJournalOwner, RecoveryRejected, MAX_SNAPSHOT_BYTES


class ExternalAnchorRejected(RecoveryRejected):
    pass


def _fingerprint(path):
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        fd = os.open(path, flags)
    except FileNotFoundError:
        return None
    try:
        meta = os.fstat(fd)
        if (not stat.S_ISREG(meta.st_mode) or meta.st_uid != os.getuid()
            or stat.S_IMODE(meta.st_mode) != 0o600
            or not 0 < meta.st_size <= MAX_SNAPSHOT_BYTES):
            raise ExternalAnchorRejected("UNSAFE_SNAPSHOT_FILE")
        h = hashlib.sha256()
        remaining = MAX_SNAPSHOT_BYTES + 1
        count = 0
        while remaining:
            chunk = os.read(fd, min(remaining, 65536))
            if not chunk:
                break
            h.update(chunk)
            count += len(chunk)
            remaining -= len(chunk)
        if count != meta.st_size:
            raise ExternalAnchorRejected("SNAPSHOT_SIZE_CHANGED")
        return h.hexdigest()
    finally:
        os.close(fd)


def _record(value):
    if (type(value) is not tuple or len(value) != 2
        or type(value[0]) is not int or value[0] < 0
        or (value[1] is not None and
            (type(value[1]) is not str or len(value[1]) != 64
             or any(c not in "0123456789abcdef" for c in value[1])))
        or (value[0] == 0) != (value[1] is None)):
        raise ExternalAnchorRejected("INVALID_TRUSTED_CHECKPOINT")
    return value


class ExternallyAnchoredJournal:
    """Trust-restricted facade; do not expose its raw owner to untrusted code.

    checkpoint.read() -> (nonnegative sequence, optional SHA-256)
    checkpoint.compare_and_advance(expected, proposed) -> exactly True

    Both operations MUST be linearizable and durable against adversarial
    rollback. Any failure or uncertainty poisons the owner. Not a proof
    of the external service or of hardware power-loss persistence.
    """
    def __init__(self, *, owner, checkpoint):
        if type(owner) is not DurableJournalOwner:
            raise ExternalAnchorRejected("UNTRUSTED_OWNER")
        self._owner = owner
        self._checkpoint = checkpoint
        try:
            self._check()
        except BaseException:
            self._poison()
            raise

    def _poison(self):
        with self._owner._lock:
            self._owner._poisoned = True

    def _check(self):
        with self._owner._lock:
            if (self._owner._closed or self._owner._poisoned
                or self._owner._lock_fd is None):
                raise ExternalAnchorRejected("OWNER_UNAVAILABLE")
            try:
                record = _record(self._checkpoint.read())
                observed = _fingerprint(self._owner.path)
                if observed != record[1]:
                    raise ExternalAnchorRejected("CHECKPOINT_SNAPSHOT_MISMATCH")
                return record
            except BaseException:
                self._poison()
                raise

    def apply(self, **kwargs):
        with self._owner._lock:
            before = self._check()
            decision = self._owner.apply(**kwargs)
            try:
                after = (before[0] + 1, _fingerprint(self._owner.path))
                if after[1] is None:
                    raise ExternalAnchorRejected("MISSING_COMMITTED_SNAPSHOT")
                if self._checkpoint.compare_and_advance(before, after) is not True:
                    raise ExternalAnchorRejected("CHECKPOINT_ADVANCE_FAILED")
                # Ensure the externally trusted checkpoint actually reports it.
                if _record(self._checkpoint.read()) != after:
                    raise ExternalAnchorRejected("CHECKPOINT_ADVANCE_UNCONFIRMED")
            except BaseException:
                self._poison()
                raise
            return decision

    def audited_claim(self, claim_id):
        with self._owner._lock:
            self._check()
            return self._owner.audited_claim(claim_id)

    def close(self):
        self._owner.close()
