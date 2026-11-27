"""Trusted, durable, single-use signed-approval ledger.

NOT a same-UID adversarial sandbox. Operate in a separate trusted-controller
security principal with a protected parent directory, outside all worktrees.
An approval is consumed with BEGIN IMMEDIATE + UNIQUE constraints BEFORE writes.
Failed/rolled-back/time-limited attempts remain spent; never auto-reset the DB.
"""
from __future__ import annotations
import hashlib
from contextlib import closing
import os
import secrets
import sqlite3
import stat
import time
from pathlib import Path
from .evidence import canonical

class LedgerError(RuntimeError):
    pass

def _checked_path(path: str | Path) -> Path:
    p = Path(path)
    if not p.is_absolute() or p.is_symlink() or not p.parent.is_dir() or p.parent.is_symlink():
        raise LedgerError("approval ledger requires a non-symlink absolute path in an existing directory")
    parent = p.parent.stat()
    if parent.st_uid != os.geteuid() or parent.st_mode & 0o022:
        raise LedgerError("untrusted writable ledger parent")
    return p

def _existing(path: str | Path) -> Path:
    p = _checked_path(path)
    try:
        st = p.lstat()
    except FileNotFoundError as exc:
        raise LedgerError("approval ledger does not exist; a trusted controller must create it") from exc
    if not stat.S_ISREG(st.st_mode) or st.st_uid != os.geteuid() or stat.S_IMODE(st.st_mode) & 0o077:
        raise LedgerError("approval ledger ownership/mode invalid")
    return p

def _connect(p: Path) -> sqlite3.Connection:
    db = sqlite3.connect(str(p), timeout=5.0, isolation_level=None)
    db.execute("PRAGMA busy_timeout=5000")
    db.execute("PRAGMA synchronous=FULL")
    db.execute("PRAGMA journal_mode=DELETE")
    return db

def create_ledger(path: str | Path) -> str:
    """Creation by a trusted authorization controller only; will never replace."""
    p = _checked_path(path)
    flags = os.O_CREAT | os.O_EXCL | os.O_RDWR
    if hasattr(os, "O_NOFOLLOW"): flags |= os.O_NOFOLLOW
    fd = os.open(p, flags, 0o600)
    os.close(fd)
    with _connect(_existing(p)) as db:
        db.execute("CREATE TABLE ledger_identity (id TEXT PRIMARY KEY)")
        db.execute("CREATE TABLE spends (mac TEXT PRIMARY KEY, nonce TEXT UNIQUE NOT NULL, session_id TEXT NOT NULL, request_sha256 TEXT NOT NULL, consumed_ns INTEGER NOT NULL)")
        identity = secrets.token_hex(32)
        db.execute("INSERT INTO ledger_identity (id) VALUES (?)", (identity,))
    return identity

def ledger_identity(path: str | Path) -> str:
    p = _existing(path)
    try:
        with _connect(p) as db:
            rows = db.execute("SELECT id FROM ledger_identity").fetchall()
    except sqlite3.Error as exc:
        raise LedgerError("unreadable or uninitialized approval ledger") from exc
    if len(rows) != 1 or not isinstance(rows[0][0], str) or len(rows[0][0]) != 64:
        raise LedgerError("approval ledger identity malformed")
    return rows[0][0]

def consume_approval(path: str | Path, approval: dict) -> bool:
    """Atomic, persistent, one-use claim. True only for the first committed spend."""
    p = _existing(path)
    try:
        req = approval["request"]
        mac = approval["mac"]
        nonce = req["nonce"]
        request_sha256 = hashlib.sha256(canonical(req)).hexdigest()
        if req["ledger_id"] != ledger_identity(p):
            return False
        with closing(_connect(p)) as db:
            db.execute("BEGIN IMMEDIATE")
            try:
                session_id = req["session_id"]
                budget_cap = req["budget_cap"]
                if type(budget_cap) is not int or not 1 <= budget_cap <= 1000000:
                    db.execute("ROLLBACK")
                    return False
                used = db.execute("SELECT COUNT(*) FROM spends WHERE session_id=?", (session_id,)).fetchone()[0]
                if used >= budget_cap:
                    db.execute("ROLLBACK")
                    return False
                db.execute("INSERT INTO spends (mac,nonce,session_id,request_sha256,consumed_ns) VALUES (?,?,?,?,?)",
                           (mac, nonce, session_id, request_sha256, time.time_ns()))
                db.execute("COMMIT")
            except Exception:
                db.execute("ROLLBACK")
                raise
        return True
    except (sqlite3.IntegrityError, KeyError, TypeError, ValueError):
        return False
    except sqlite3.Error as exc:
        raise LedgerError("durable approval consumption failed") from exc
