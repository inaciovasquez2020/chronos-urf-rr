"""No-download DynamoDB protocol tests using a strict in-memory API double.

These are NOT tests of AWS network, IAM, storage durability or deployment.
"""
import os
import pytest

from urf_ai.dynamodb_checkpoint_candidate import DynamoDBCheckpoint
from urf_ai.external_anchor_candidate import (
    ExternalAnchorRejected, ExternallyAnchoredJournal
)
from urf_ai.durable_journal_candidate import DurableJournalOwner


class ConditionalFail(Exception):
    response={"Error":{"Code":"ConditionalCheckFailedException"}}


class StubDynamoDB:
    def __init__(self, *, initial=True):
        self.state={"checkpoint_id":{"S":"journal-a"},
                    "seq":{"N":"0"},"digest":{"S":"GENESIS"}} if initial else None
        self.history=[]
        self.fail_read=False
        self.fail_update=False

    def get_item(self, **kw):
        assert kw["TableName"]=="checkpoints"
        assert kw["Key"]=={"checkpoint_id":{"S":"journal-a"}}
        assert kw["ConsistentRead"] is True
        if self.fail_read:
            raise TimeoutError("synthetic unavailable service")
        return {"Item":dict(self.state)} if self.state is not None else {}

    def update_item(self, **kw):
        assert kw["TableName"]=="checkpoints"
        assert kw["Key"]=={"checkpoint_id":{"S":"journal-a"}}
        assert kw["ConditionExpression"]=="#s = :old_seq AND #d = :old_digest"
        assert kw["UpdateExpression"]=="SET #s = :new_seq, #d = :new_digest"
        assert kw["ReturnValues"]=="NONE"
        assert kw["ExpressionAttributeNames"]=={"#s":"seq","#d":"digest"}
        if self.fail_update:
            raise TimeoutError("synthetic conditional write timeout")
        v=kw["ExpressionAttributeValues"]
        if (self.state is None or self.state["seq"]!=v[":old_seq"]
            or self.state["digest"]!=v[":old_digest"]):
            raise ConditionalFail()
        nxt=dict(self.state)
        nxt["seq"]=v[":new_seq"]
        nxt["digest"]=v[":new_digest"]
        self.state=nxt
        self.history.append(dict(nxt))
        return {"ResponseMetadata":{"HTTPStatusCode":200}}


def anchor(stub):
    return DynamoDBCheckpoint(client=stub,table_name="checkpoints",checkpoint_id="journal-a")


HASH1="a"*64
HASH2="b"*64


def test_provisioned_genesis_then_linearizable_cas():
    server=StubDynamoDB()
    c=anchor(server)
    assert c.read()==(0,None)
    assert c.compare_and_advance((0,None),(1,HASH1)) is True
    assert c.read()==(1,HASH1)
    assert c.compare_and_advance((0,None),(1,HASH2)) is False
    assert c.compare_and_advance((1,HASH1),(2,HASH2)) is True
    assert c.read()==(2,HASH2)


def test_missing_remote_checkpoint_not_initialized_silently():
    with pytest.raises(ExternalAnchorRejected,match="NOT_PROVISIONED"):
        anchor(StubDynamoDB(initial=False)).read()


def test_bad_remote_schema_not_accepted():
    stub=StubDynamoDB()
    for entry in [
        {"checkpoint_id":{"S":"journal-a"},"seq":{"N":"0"},"digest":{"S":HASH1}},
        {"checkpoint_id":{"S":"journal-a"},"seq":{"N":"01"},"digest":{"S":"GENESIS"}},
        {"checkpoint_id":{"S":"journal-a"},"seq":{"N":"1"},"digest":{"S":"GENESIS"}},
        {"checkpoint_id":{"S":"journal-b"},"seq":{"N":"0"},"digest":{"S":"GENESIS"}},
    ]:
        stub.state=entry
        with pytest.raises(ExternalAnchorRejected):
            anchor(stub).read()


def test_uncertain_remote_write_and_read_fail_closed():
    stub=StubDynamoDB()
    checkpoint=anchor(stub)
    stub.fail_update=True
    with pytest.raises(ExternalAnchorRejected,match="ADVANCE_UNCERTAIN"):
        checkpoint.compare_and_advance((0,None),(1,HASH1))
    stub.fail_update=False
    stub.fail_read=True
    with pytest.raises(ExternalAnchorRejected,match="READ_UNAVAILABLE"):
        checkpoint.read()


def test_nonmonotonic_update_rejected_before_network():
    checkpoint=anchor(StubDynamoDB())
    with pytest.raises(ExternalAnchorRejected,match="NONMONOTONIC"):
        checkpoint.compare_and_advance((0,None),(2,HASH1))


def test_authenticated_old_snapshot_rejected_by_independent_remote_digest(tmp_path):
    os.chmod(tmp_path,0o700)
    snapshot=tmp_path/"snapshot.json"
    key=b"synthetic-dynamodb-journal-key-2026"*2
    roles={"author":"AUTHOR"}
    stub=StubDynamoDB()
    checkpoint=anchor(stub)
    def owner():
        return DurableJournalOwner(path=str(snapshot),secret=key,
                                   roles=roles,checker_allowlist={})
    first=ExternallyAnchoredJournal(owner=owner(),checkpoint=checkpoint)
    claim={"claim_id":"c","semantic_version":1,"kind":"THEOREM",
           "state":"OPEN","proposition":"synthetic","scope":{"domain":"synthetic"},
           "assumptions":[],"dependencies":[],"frontier":[],"boundaries":[],
           "source_revision":{"repo":"test","commit":"a"*40},"author":"author"}
    first.apply(event_id="r1",kind="REGISTER",claim_id="c",actor="author",
                expected_version=0,payload=claim,reason="synthetic")
    older=snapshot.read_bytes()
    first.apply(event_id="r2",kind="REVISE",claim_id="c",actor="author",
                expected_version=1,
                payload={"changes":{"proposition":"synthetic updated"}},
                reason="synthetic")
    assert checkpoint.read()[0]==2
    first.close()
    snapshot.write_bytes(older)
    with pytest.raises(ExternalAnchorRejected,match="CHECKPOINT_SNAPSHOT_MISMATCH"):
        ExternallyAnchoredJournal(owner=owner(),checkpoint=checkpoint)

def test_remote_committed_but_ack_lost_is_uncertain_and_recoverable(tmp_path):
    """The write may commit remotely before a transport failure is reported."""
    os.chmod(tmp_path,0o700)
    snapshot=tmp_path/"snapshot.json"
    key=b"synthetic-uncertain-commit-key-2026"*2
    roles={"author":"AUTHOR"}
    class LostAcknowledgement(StubDynamoDB):
        def __init__(self):
            super().__init__()
            self.lose_once=True
        def update_item(self, **kwargs):
            result=super().update_item(**kwargs)
            if self.lose_once:
                self.lose_once=False
                raise TimeoutError("response lost after successful commit")
            return result
    backend=LostAcknowledgement()
    checkpoint=anchor(backend)
    def new_owner():
        return DurableJournalOwner(path=str(snapshot),secret=key,
                                   roles=roles,checker_allowlist={})
    anchored=ExternallyAnchoredJournal(owner=new_owner(),checkpoint=checkpoint)
    claim={"claim_id":"c","semantic_version":1,"kind":"THEOREM",
           "state":"OPEN","proposition":"synthetic",
           "scope":{"domain":"synthetic"},"assumptions":[],
           "dependencies":[],"frontier":[],"boundaries":[],
           "source_revision":{"repo":"test","commit":"a"*40},"author":"author"}
    with pytest.raises(ExternalAnchorRejected,match="ADVANCE_UNCERTAIN"):
        anchored.apply(event_id="r1",kind="REGISTER",claim_id="c",
                       actor="author",expected_version=0,payload=claim,
                       reason="synthetic")
    assert checkpoint.read()[0]==1
    with pytest.raises(ExternalAnchorRejected,match="OWNER_UNAVAILABLE"):
        anchored.audited_claim("c")
    anchored.close()
    recovered=ExternallyAnchoredJournal(owner=new_owner(),checkpoint=checkpoint)
    assert recovered.audited_claim("c")["state"]=="OPEN"
    recovered.close()


def test_full_trust_domain_rollback_counterexample(tmp_path):
    """Rollback of both matching states cannot be detected locally."""
    os.chmod(tmp_path,0o700)
    snapshot=tmp_path/"snapshot.json"
    key=b"synthetic-double-rollback-key-2026"*2
    roles={"author":"AUTHOR"}
    server=StubDynamoDB()
    checkpoint=anchor(server)
    def new_owner():
        return DurableJournalOwner(path=str(snapshot),secret=key,
                                   roles=roles,checker_allowlist={})
    anchored=ExternallyAnchoredJournal(owner=new_owner(),checkpoint=checkpoint)
    claim={"claim_id":"c","semantic_version":1,"kind":"THEOREM",
           "state":"OPEN","proposition":"original",
           "scope":{"domain":"synthetic"},"assumptions":[],
           "dependencies":[],"frontier":[],"boundaries":[],
           "source_revision":{"repo":"test","commit":"a"*40},"author":"author"}
    anchored.apply(event_id="r1",kind="REGISTER",claim_id="c",
                   actor="author",expected_version=0,payload=claim,
                   reason="synthetic")
    old_snapshot=snapshot.read_bytes()
    old_anchor={name:dict(value) for name,value in server.state.items()}
    anchored.apply(event_id="r2",kind="REVISE",claim_id="c",
                   actor="author",expected_version=1,
                   payload={"changes":{"proposition":"revised"}},
                   reason="synthetic")
    assert checkpoint.read()[0]==2
    anchored.close()
    snapshot.write_bytes(old_snapshot)
    server.state=old_anchor  # Attacker compromises remote trust boundary.
    reopened=ExternallyAnchoredJournal(owner=new_owner(),checkpoint=checkpoint)
    assert reopened.audited_claim("c")["proposition"]=="original"
    reopened.close()
