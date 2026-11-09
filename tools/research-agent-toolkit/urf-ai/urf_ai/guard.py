"""Fail-closed bounded mutation adapter for disposable worktrees only.

No git reset, git clean, checkout, or broad deletion. Does NOT sandbox subprocesses.
"""
from __future__ import annotations
import ast
import secrets
import fnmatch
import hashlib
import hmac
import json
import os
import re
import stat
import time
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path
from .evidence import canonical, digest
from .approval_ledger import LedgerError, ledger_identity, consume_approval

@dataclass(frozen=True)
class MutationResult:
    status: str
    stage: str
    returncode: int
    residue: tuple[str, ...] = ()
    detail: str = ""
    def to_dict(self): return asdict(self)

def git(root: Path, *args: str, input_bytes: bytes | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], input=input_bytes, capture_output=True)

def modified_paths(root: Path) -> set[str]:
    parts = []
    for args in [("diff", "--name-only", "-z"), ("diff", "--cached", "--name-only", "-z"), ("ls-files", "--others", "--exclude-standard", "-z"), ("ls-files", "--others", "--ignored", "--exclude-standard", "-z")]:
        r = git(root, *args)
        if r.returncode:
            raise RuntimeError("git inventory failed")
        parts.extend(p.decode("utf-8", "surrogateescape") for p in r.stdout.split(b"\0") if p)
    return set(parts)

def patch_paths(root: Path, patch: bytes) -> set[str]:
    r = git(root, "apply", "--numstat", "-z", "-", input_bytes=patch)
    if r.returncode or not r.stdout:
        raise ValueError("malformed or empty unified patch")
    out = set()
    for entry in r.stdout.split(b"\0"):
        if not entry: continue
        fields = entry.split(b"\t", 2)
        if len(fields) != 3 or not fields[0].isdigit() or not fields[1].isdigit():
            raise ValueError("binary or rename patches unsupported")
        p = fields[2].decode("utf-8", "surrogateescape")
        if p.startswith("/") or ".." in Path(p).parts or p.startswith(".git/") or not p:
            raise ValueError("unsafe patch path")
        out.add(p)
    return out

def _restore(root: Path, snapshots: dict[str, tuple[bytes,int]]):
    for rel, (data, mode) in snapshots.items():
        p = root / rel
        if p.is_symlink(): p.unlink()
        if p.is_dir():
            raise RuntimeError(f"refuse to remove a directory at {rel}")
        p.write_bytes(data)
        os.chmod(p, mode)

def issue_approval(root: str | Path, patch: bytes, closure: set[str], config: dict, verifier: list[str], secret: bytes, *, approval_ledger: str | Path, ttl_seconds: int = 300) -> dict:
    """For trusted human authorization controller ONLY; never expose this to an agent."""
    if len(secret)<32 or ttl_seconds<1 or ttl_seconds>900: raise ValueError("unsafe approval arguments")
    root=Path(root).resolve()
    head=git(root,"rev-parse","HEAD")
    if head.returncode: raise ValueError("unavailable HEAD")
    req={"root":str(root),"head":head.stdout.decode().strip(),
         "patch_sha256":hashlib.sha256(patch).hexdigest(),
         "closure_digest":digest(sorted(closure)),"config_digest":digest(config),
         "verifier_digest":digest(verifier),"expires_unix":int(time.time())+ttl_seconds,
         "ledger_id":ledger_identity(approval_ledger),"nonce":secrets.token_hex(32),
         "session_id":digest({"root":str(root),"head":head.stdout.decode().strip(),"config":digest(config)}),
         "budget_cap":config.get("budgets",{}).get("mutations",0)}
    mac=hmac.new(secret,canonical(req),hashlib.sha256).hexdigest()
    return {"request":req,"mac":mac}

def approval_valid(root: Path, patch: bytes, closure: set[str], config: dict, verifier: list[str], approval: object, secret: bytes, *, approval_ledger: str | Path) -> bool:
    if not isinstance(secret,bytes) or len(secret)<32 or not isinstance(approval,dict) or set(approval)!={"request","mac"}: return False
    req=approval["request"]
    if not isinstance(req,dict) or not isinstance(approval["mac"],str) or set(req)!={"root","head","patch_sha256","closure_digest","config_digest","verifier_digest","expires_unix","ledger_id","nonce","session_id","budget_cap"}: return False
    if type(req.get("expires_unix")) is not int or not (time.time()<req["expires_unix"]<=time.time()+900): return False
    if not isinstance(req.get("nonce"),str) or len(req["nonce"])!=64: return False
    if not isinstance(req.get("session_id"),str) or len(req["session_id"])!=64: return False
    if type(req.get("budget_cap")) is not int or req["budget_cap"] != config.get("budgets",{}).get("mutations",0): return False
    try:
        if req["ledger_id"]!=ledger_identity(approval_ledger): return False
    except LedgerError:
        return False
    try:
        if not hmac.compare_digest(hmac.new(secret,canonical(req),hashlib.sha256).hexdigest(),approval["mac"]): return False
        head=git(root,"rev-parse","HEAD")
        return (head.returncode==0 and req["head"]==head.stdout.decode().strip()
                and req["root"]==str(root)
                and req["patch_sha256"]==hashlib.sha256(patch).hexdigest()
                and req["closure_digest"]==digest(sorted(closure))
                and req["config_digest"]==digest(config)
                and req["verifier_digest"]==digest(verifier))
    except (TypeError,ValueError): return False

def run_mutation(root: str | Path, patch: bytes, closure: set[str], config: dict, verifier: list[str], *, approval: dict | None=None, authorization_key: bytes | None=None, approval_ledger: str | Path | None=None, timeout_seconds: int = 10) -> MutationResult:
    """Mutate an explicitly disposable, clean worktree; only tracked regular files.

    Not suitable as a security sandbox for an untrusted verifier executable.
    Outside-closure mutations are NEVER deleted, and are reported as residue.
    """
    root = Path(root)
    if root.is_symlink() or not root.is_dir():
        return MutationResult("DENY", "preflight", 2, detail="root must be a real directory")
    root = root.resolve()
    if git(root, "rev-parse", "--is-inside-work-tree").stdout.strip() != b"true":
        return MutationResult("DENY", "preflight", 2, detail="not a git worktree")
    toplevel=git(root,"rev-parse","--show-toplevel")
    if toplevel.returncode or Path(toplevel.stdout.decode().strip()).resolve()!=root:
        return MutationResult("DENY", "preflight", 2, detail="root must be top-level worktree")
    if not config.get("disposable_worktree_confirmed"):
        return MutationResult("DENY", "preflight", 2, detail="requires explicitly disposable worktree")
    if not config.get("explicit_write_approval"):
        return MutationResult("DENY", "preflight", 2, detail="requires explicit write approval")
    if approval_ledger is None:
        return MutationResult("DENY", "authorization", 2, detail="trusted durable approval ledger required")
    # The durable ledger must never be part of the mutable research worktree.
    try:
        ledgerpath=Path(approval_ledger).resolve(strict=True)
        if ledgerpath.is_relative_to(root):
            return MutationResult("DENY", "authorization", 2, detail="approval ledger must be external to the worktree")
    except (OSError, RuntimeError, ValueError):
        return MutationResult("DENY", "authorization", 2, detail="unavailable trusted approval ledger")
    if not approval_valid(root,patch,closure,config,verifier,approval,authorization_key,approval_ledger=approval_ledger):
        return MutationResult("DENY", "authorization", 2, detail="missing or invalid scoped signed approval")
    if modified_paths(root):
        return MutationResult("DENY", "preflight", 2, detail="worktree is dirty or has untracked files")
    if not isinstance(patch, bytes) or not patch or not isinstance(closure, set):
        return MutationResult("DENY", "preflight", 2, detail="invalid patch or closure")
    try: paths = patch_paths(root, patch)
    except ValueError as exc: return MutationResult("DENY", "preflight", 2, detail=str(exc))
    if not paths <= closure:
        return MutationResult("DENY", "preflight", 2, detail="patch escapes provenance closure")
    policy = config.get("policy", {})
    if not config.get("scope", {}).get("allow"):
        return MutationResult("DENY", "policy", 2, detail="explicit allowlist required")
    for rel in paths:
        deny = config["scope"].get("deny", [])
        allow = config["scope"]["allow"]
        if (any(fnmatch.fnmatchcase(rel,p) for p in deny)
            or not any(fnmatch.fnmatchcase(rel,p) for p in allow)):
            return MutationResult("DENY", "policy", 2, detail=f"path not authorized: {rel}")
        p = root / rel
        if p.is_symlink() or not p.is_file() or not stat.S_ISREG(p.lstat().st_mode) or not p.resolve().is_relative_to(root):
            return MutationResult("DENY", "preflight", 2, detail=f"not an ordinary tracked file: {rel}")
        if git(root,"ls-files","--error-unmatch","--",rel).returncode:
            return MutationResult("DENY", "preflight", 2, detail=f"untracked patch path: {rel}")
    # Only in-process, side-effect-free checks are permitted. No user-provided
    # argv is ever launched. OS sandboxing is NOT supplied by this tool.
    INTERNAL = (["RAT_INTERNAL_DIFF_CHECK"], ["RAT_INTERNAL_PYTHON_SYNTAX"])
    if verifier not in INTERNAL:
        return MutationResult("DENY", "verifier", 2, detail="external or untrusted verifier execution prohibited")
    if (not isinstance(verifier,list) or verifier not in config.get("verifier_commands", []) or not all(isinstance(s,str) and s for s in verifier)):
        return MutationResult("DENY", "policy", 2, detail="verifier argv not explicitly allowlisted")
    if config.get("budgets", {}).get("mutations",0)<1 or not (0<timeout_seconds<=config.get("budgets",{}).get("max_verifier_seconds",0)):
        return MutationResult("DENY", "budget", 2, detail="mutation/time budget not granted")
    if "modify" not in config.get("gates", {}).get("verify_actions", []) or "modify" in config.get("gates", {}).get("deny_actions", []):
        return MutationResult("DENY", "policy", 2, detail="required verification gate missing")
    additions = "\n".join(line[1:] for line in patch.decode("utf-8", "replace").splitlines() if line.startswith("+") and not line.startswith("+++"))
    try:
        if any(re.search(pattern, additions) for pattern in policy.get("forbidden_patterns", [])):
            return MutationResult("DENY", "policy", 2, detail="forbidden source pattern in patch additions")
    except re.error:
        return MutationResult("DENY", "policy", 2, detail="invalid policy regex")
    if git(root,"apply","--check","--whitespace=error-all","-",input_bytes=patch).returncode:
        return MutationResult("DENY", "preflight", 2, detail="patch did not pass git apply --check")
    # Each approved attempt is irreversibly consumed BEFORE the first write;
    # crashes, failures and exact rollbacks do not replenish the budget.
    try:
        consumed = consume_approval(approval_ledger, approval)
    except LedgerError as exc:
        return MutationResult("DENY", "authorization", 2, detail=str(exc))
    if not consumed:
        return MutationResult("DENY", "replay", 2, detail="approval already spent or ledger rejected request")
    snapshots = {rel: ((root/rel).read_bytes(), stat.S_IMODE((root/rel).stat().st_mode)) for rel in paths}
    def fail(stage: str, code: int, detail: str):
        before_restore=modified_paths(root)
        outsider=tuple(sorted(before_restore-set(snapshots)))
        try: _restore(root,snapshots)
        except Exception as exc: return MutationResult("INCOMPLETE_ROLLBACK",stage,code, outsider, str(exc))
        residue=tuple(sorted(modified_paths(root)))
        if residue or outsider:
            return MutationResult("INCOMPLETE_UNAUTHORIZED_RESIDUE",stage,code,tuple(sorted(set(residue)|set(outsider))),detail)
        return MutationResult("FAILED_ROLLED_BACK",stage,code,detail=detail)
    apply=git(root,"apply","--whitespace=error-all","-",input_bytes=patch)
    if apply.returncode:
        return fail("mutation",apply.returncode,apply.stderr.decode("utf-8","replace")[:500])
    outside=modified_paths(root)-paths
    if outside:
        return fail("scope",3,"post-mutation changed path outside closure")
    if any(not (root/rel).is_file() or (root/rel).is_symlink() for rel in paths):
        return fail("scope",3,"deletion or symlink creation prohibited")
    applied={(rel):((root/rel).read_bytes(),stat.S_IMODE((root/rel).stat().st_mode)) for rel in paths}
    # Do not execute *any* external verifier. Builtin checks are restricted
    # to integrity/inventory and (optionally) Python syntax, not theorem truth.
    if verifier == ["RAT_INTERNAL_PYTHON_SYNTAX"]:
        try:
            for rel in sorted(paths):
                if rel.endswith(".py"):
                    ast.parse((root/rel).read_text(encoding="utf-8"), filename=rel)
        except (SyntaxError, UnicodeError, OSError) as exc:
            return fail("verification",7,"internal syntax failure: "+str(exc)[:500])
    outside=modified_paths(root)-paths
    if outside:
        return fail("verification",3,"internal check found outside changed paths")
    if any(not (root/rel).is_file() or (root/rel).is_symlink() or
           ((root/rel).read_bytes(),stat.S_IMODE((root/rel).stat().st_mode))!=applied[rel]
           for rel in paths):
        return fail("verification",3,"verifier modified the candidate patch files")
    return MutationResult("STRUCTURAL_CANDIDATE_NOT_PROMOTED","structural-check",0,
                          detail="authorized patch passed internal structural checks only; no theorem verifier executed")
