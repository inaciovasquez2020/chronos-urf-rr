"""Conditional external anti-rollback checkpoint acceptance, no trusted service claimed."""
import os
from pathlib import Path

import pytest

from urf_ai.durable_journal_candidate import DurableJournalOwner
from urf_ai.external_anchor_candidate import ExternallyAnchoredJournal, ExternalAnchorRejected

KEY = b"synthetic-anchoring-secret-key-2026" * 2
ROLES = {"author": "AUTHOR"}
CLAIM = {"claim_id":"c","semantic_version":1,"kind":"THEOREM",
         "state":"OPEN","proposition":"synthetic statement",
         "scope":{"domain":"synthetic"},"assumptions":[],
         "dependencies":[],"frontier":[],"boundaries":[],
         "source_revision":{"repo":"fixture","commit":"a"*40},
         "author":"author"}

class SimulatedTrustedCheckpoint:
    """Test double only. Volatile Python state is NOT a trusted deployment anchor."""
    def __init__(self, initial=(0, None)):
        self.current = initial
        self.fail_next = False
    def read(self):
        return self.current
    def compare_and_advance(self, expected, proposed):
        if self.fail_next:
            self.fail_next = False
            return False
        if self.current != expected:
            return False
        self.current = proposed
        return True

def open_owner(path):
    return DurableJournalOwner(path=str(path), secret=KEY, roles=ROLES,
                               checker_allowlist={})

def register(anchored, event_id):
    return anchored.apply(event_id=event_id, kind="REGISTER", claim_id="c",
                          actor="author", expected_version=0,
                          payload=CLAIM, reason="synthetic test")

@pytest.fixture
def path(tmp_path):
    os.chmod(tmp_path, 0o700)
    return tmp_path/"snapshot.json"

def test_advance_and_restart_after_ack(path):
    checkpoint = SimulatedTrustedCheckpoint()
    first = ExternallyAnchoredJournal(owner=open_owner(path),checkpoint=checkpoint)
    register(first,"r1")
    assert checkpoint.current[0] == 1
    assert first.audited_claim("c")["state"] == "OPEN"
    first.close()
    second = ExternallyAnchoredJournal(owner=open_owner(path),checkpoint=checkpoint)
    assert second.audited_claim("c")["state"] == "OPEN"
    second.close()

def test_old_valid_authenticated_snapshot_is_rejected(path):
    checkpoint = SimulatedTrustedCheckpoint()
    first = ExternallyAnchoredJournal(owner=open_owner(path),checkpoint=checkpoint)
    register(first,"r1")
    old_valid = path.read_bytes()
    # A second valid journal event produces a newer authenticated snapshot.
    first.apply(event_id="revise",kind="REVISE",claim_id="c",
                actor="author",expected_version=1,
                payload={"changes":{"proposition":"synthetic statement revised"}},
                reason="synthetic revision")
    assert checkpoint.current[0] == 2
    first.close()
    path.write_bytes(old_valid)
    with pytest.raises(ExternalAnchorRejected,match="CHECKPOINT_SNAPSHOT_MISMATCH"):
        ExternallyAnchoredJournal(owner=open_owner(path),checkpoint=checkpoint)

def test_missing_checkpoint_fails_closed_even_with_valid_snapshot(path):
    checkpoint = SimulatedTrustedCheckpoint()
    first = ExternallyAnchoredJournal(owner=open_owner(path),checkpoint=checkpoint)
    register(first,"r1")
    first.close()
    class MissingCheckpoint:
        def read(self):
            raise RuntimeError("missing trusted service")
    with pytest.raises(RuntimeError,match="missing trusted service"):
        ExternallyAnchoredJournal(owner=open_owner(path),checkpoint=MissingCheckpoint())

def test_deleted_snapshot_is_not_fresh_genesis(path):
    checkpoint = SimulatedTrustedCheckpoint()
    first = ExternallyAnchoredJournal(owner=open_owner(path),checkpoint=checkpoint)
    register(first,"r1")
    first.close()
    path.unlink()
    with pytest.raises(ExternalAnchorRejected,match="CHECKPOINT_SNAPSHOT_MISMATCH"):
        ExternallyAnchoredJournal(owner=open_owner(path),checkpoint=checkpoint)

def test_failed_checkpoint_advance_never_acknowledges_and_poisoned(path):
    checkpoint = SimulatedTrustedCheckpoint()
    owner = open_owner(path)
    anchored = ExternallyAnchoredJournal(owner=owner,checkpoint=checkpoint)
    checkpoint.fail_next = True
    with pytest.raises(ExternalAnchorRejected,match="CHECKPOINT_ADVANCE_FAILED"):
        register(anchored,"r1")
    assert checkpoint.current == (0,None)
    with pytest.raises(ExternalAnchorRejected,match="OWNER_UNAVAILABLE"):
        anchored.audited_claim("c")
    anchored.close()
    # The snapshot may already have been persisted; recovery MUST fail closed.
    with pytest.raises(ExternalAnchorRejected,match="CHECKPOINT_SNAPSHOT_MISMATCH"):
        ExternallyAnchoredJournal(owner=open_owner(path),checkpoint=checkpoint)

def test_anchored_socket_service_rejects_rollback_before_bind(path,tmp_path):
    from urf_ai.controller_boundary_candidate import IdentityPolicy, serve_owned_urf
    checkpoint = SimulatedTrustedCheckpoint()
    owner = open_owner(path)
    anchored = ExternallyAnchoredJournal(owner=owner,checkpoint=checkpoint)
    register(anchored,"r1")
    old_valid = path.read_bytes()
    anchored.apply(event_id="revise",kind="REVISE",claim_id="c",
                   actor="author",expected_version=1,
                   payload={"changes":{"proposition":"synthetic statement revised"}},
                   reason="synthetic revision")
    sockdir = tmp_path/"socket"
    sockdir.mkdir()
    os.chmod(sockdir,0o711)
    endpoint = sockdir/"controller.sock"
    # Adversarial restoration of an old, correctly MAC-authenticated snapshot
    # after startup but before the controller begins serving.
    path.write_bytes(old_valid)
    with pytest.raises(ExternalAnchorRejected,match="CHECKPOINT_SNAPSHOT_MISMATCH"):
        serve_owned_urf(str(endpoint),IdentityPolicy(os.getuid(),os.getuid()+1),
                        owner,max_connections=1,external_anchor=anchored)
    assert not endpoint.exists()
    with pytest.raises(ExternalAnchorRejected,match="OWNER_UNAVAILABLE"):
        anchored.audited_claim("c")
    owner.close()

def test_anchored_socket_service_refuses_wrong_owner(path,tmp_path):
    from urf_ai.controller_boundary_candidate import IdentityPolicy, serve_owned_urf, BoundaryError
    checkpoint = SimulatedTrustedCheckpoint()
    first = open_owner(path)
    anchored = ExternallyAnchoredJournal(owner=first,checkpoint=checkpoint)
    first.close()
    another = open_owner(path)
    sockdir = tmp_path/"socket"
    sockdir.mkdir()
    os.chmod(sockdir,0o711)
    with pytest.raises(BoundaryError,match="INVALID_EXTERNAL_ANCHOR"):
        serve_owned_urf(str(sockdir/"controller.sock"),
                        IdentityPolicy(os.getuid(),os.getuid()+1),
                        another,max_connections=1,external_anchor=anchored)
    another.close()
