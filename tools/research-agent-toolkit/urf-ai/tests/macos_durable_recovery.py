"""No-download macOS process-crash and authenticated snapshot recovery acceptance."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from urf_ai.durable_journal_candidate import DurableJournalOwner, RecoveryRejected

if sys.platform!="darwin":
    raise AssertionError("must run on macOS")

key=b"synthetic-only-macos-recovery-2026"*2
roles={"author":"AUTHOR"}
claim={"claim_id":"c","semantic_version":1,"kind":"THEOREM","state":"OPEN",
       "proposition":"synthetic test","scope":{"domain":"synthetic"},
       "assumptions":[],"dependencies":[],"frontier":[],"boundaries":[],
       "source_revision":{"repo":"synthetic","commit":"a"*40},"author":"author"}
parent=Path(tempfile.mkdtemp(prefix="urf-ai-recovery-"))
os.chmod(parent,0o700)
path=parent/"journal.json"
script="""import os,sys
from urf_ai.durable_journal_candidate import DurableJournalOwner
j=DurableJournalOwner(path=sys.argv[1],secret=%r,roles=%r,checker_allowlist={})
j.apply(event_id="r1",kind="REGISTER",claim_id="c",actor="author",
        expected_version=0,payload=%r,reason="synthetic")
os._exit(27)
""" % (key,roles,claim)
r=subprocess.run([sys.executable,"-B","-c",script,str(path)],
                 capture_output=True,text=True,timeout=20)
if r.returncode!=27:
    raise AssertionError("child did not exit after fsync: "+repr(r.stderr))
j=DurableJournalOwner(path=str(path),secret=key,roles=roles,checker_allowlist={})
if not j.journal.audit_events() or j.audited_claim("c")["state"]!="OPEN":
    raise AssertionError("authenticated replay after process crash failed")
if len(j.journal.events)!=1:
    raise AssertionError("unexpected event count")
try:
    j.apply(event_id="r1",kind="REGISTER",claim_id="c",
            actor="author",expected_version=0,payload=claim,reason="synthetic")
except ValueError:
    pass
else:
    raise AssertionError("duplicate event accepted after restart")
tampered=json.loads(path.read_text())
tampered["data"]["records"]["c"]["state"]="PROVED"
path.write_text(json.dumps(tampered))
try:
    DurableJournalOwner(path=str(path),secret=key,roles=roles,checker_allowlist={})
except RecoveryRejected:
    pass
else:
    raise AssertionError("modified snapshot accepted")
print("MACOS_FSYNC_CRASH_RESTART := PASS")
print("MACOS_EVENT_REPLAY_PROTECTION := PASS")
print("MACOS_TAMPERED_SNAPSHOT_DENIAL := PASS")
print("POWER_LOSS_HARDWARE_TEST := NOT_RUN")
print("ROLLBACK_WITH_VALID_OLD_SNAPSHOT := OPEN")
