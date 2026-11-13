"""Candidate crash/recovery tests: real snapshot files, no model or proof claims."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import pytest
from urf_ai.durable_journal_candidate import DurableJournalOwner, RecoveryRejected

KEY=b"synthetic-only-recovery-secret-2026"*2
ROLES={"author":"AUTHOR"}
ALLOW={}
SRC="from urf_ai.durable_journal_candidate import DurableJournalOwner\n"

def owner(path,key=KEY):
    return DurableJournalOwner(path=str(path),secret=key,roles=ROLES,checker_allowlist=ALLOW)

def claim():
    return {"claim_id":"c","semantic_version":1,"kind":"THEOREM",
            "state":"OPEN","proposition":"synthetic assertion",
            "scope":{"domain":"synthetic"},"assumptions":[],"dependencies":[],
            "frontier":[],"boundaries":[],
            "source_revision":{"repo":"fixture","commit":"a"*40},
            "author":"author"}

def register(o):
    return o.apply(event_id="register",kind="REGISTER",claim_id="c",
                   actor="author",expected_version=0,payload=claim(),reason="test")

@pytest.fixture
def storage(tmp_path):
    os.chmod(tmp_path,0o700)
    return tmp_path/"journal.json"

def test_fsync_snapshot_recovers_after_reinstantiation(storage):
    o=owner(storage)
    register(o)
    assert storage.stat().st_mode & 0o777 == 0o600
    next_owner=owner(storage)
    assert next_owner.journal.audit_events()
    assert next_owner.audited_claim("c")["state"]=="OPEN"
    assert len(next_owner.journal.events)==1

def test_duplicate_event_rejected_after_restart(storage):
    o=owner(storage)
    register(o)
    recovered=owner(storage)
    with pytest.raises(ValueError):
        register(recovered)
    assert len(recovered.journal.events)==1

def test_mutated_snapshot_fails_closed(storage):
    o=owner(storage)
    register(o)
    envelope=json.loads(storage.read_text())
    envelope["data"]["records"]["c"]["state"]="PROVED"
    storage.write_text(json.dumps(envelope))
    with pytest.raises(RecoveryRejected):
        owner(storage)

def test_wrong_key_fails_closed(storage):
    o=owner(storage)
    register(o)
    with pytest.raises(RecoveryRejected):
        owner(storage,key=b"different-synthetic-secret-for-test"*2)

def test_insecure_permissions_fail_closed(storage):
    o=owner(storage)
    register(o)
    os.chmod(storage,0o644)
    with pytest.raises(RecoveryRejected):
        owner(storage)

def test_failed_replace_never_acknowledges(monkeypatch,storage):
    o=owner(storage)
    def denied(*args): raise OSError("synthetic disk failure")
    monkeypatch.setattr("urf_ai.durable_journal_candidate.os.replace",denied)
    with pytest.raises(OSError):
        register(o)
    assert not o.journal.audit_events()
    with pytest.raises(RecoveryRejected):
        o.audited_claim("c")
    assert not storage.exists()

def test_failed_directory_fsync_poisoned_even_after_atomic_replace(monkeypatch,storage):
    o=owner(storage)
    native=os.fsync
    count=[0]
    def fail_after_snapshot_write(fd):
        count[0]+=1
        if count[0]==2:
            raise OSError("synthetic directory fsync failure")
        return native(fd)
    monkeypatch.setattr("urf_ai.durable_journal_candidate.os.fsync",
                        fail_after_snapshot_write)
    with pytest.raises(OSError):
        register(o)
    assert count[0]==2
    assert not o.journal.audit_events()
    with pytest.raises(RecoveryRejected):
        o.audited_claim("c")
    # Restore the real fsync before fresh-process loading.
    monkeypatch.undo()
    fresh=owner(storage)
    assert fresh.journal.audit_events()
    assert fresh.audited_claim("c")["state"]=="OPEN"

def test_real_process_exit_and_fresh_process_replay(storage):
    script=(
        "from urf_ai.durable_journal_candidate import DurableJournalOwner;"
        "import os,sys;"
        "j=DurableJournalOwner(path=sys.argv[1],secret="+repr(KEY)+",roles="+repr(ROLES)+",checker_allowlist={});"
        "j.apply(event_id='register',kind='REGISTER',claim_id='c',actor='author',"
        "expected_version=0,payload="+repr(claim())+",reason='test');"
        "os._exit(19)"
    )
    run=subprocess.run([sys.executable,"-B","-c",script,str(storage)],
                       capture_output=True,text=True,timeout=15)
    assert run.returncode==19, (run.stdout,run.stderr)
    fresh=subprocess.run([sys.executable,"-B","-c",(
        "from urf_ai.durable_journal_candidate import DurableJournalOwner;"
        "import sys;"
        "j=DurableJournalOwner(path=sys.argv[1],secret="+repr(KEY)+",roles="+repr(ROLES)+",checker_allowlist={});"
        "assert j.journal.audit_events();"
        "assert j.audited_claim('c')['state']=='OPEN';"
        "assert len(j.journal.events)==1"
    ),str(storage)],capture_output=True,text=True,timeout=15)
    assert fresh.returncode==0,(fresh.stdout,fresh.stderr)
