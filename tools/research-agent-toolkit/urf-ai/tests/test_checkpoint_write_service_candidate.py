"""Trusted-writer policy tests. No AWS/IAM/HTTP deployment is asserted."""
import pytest

from urf_ai.checkpoint_write_service_candidate import CheckpointWriteService
from urf_ai.dynamodb_checkpoint_candidate import DynamoDBCheckpoint
from urf_ai.external_anchor_candidate import ExternalAnchorRejected

class ConditionalCheckFailed(Exception):
    response={"Error":{"Code":"ConditionalCheckFailedException"}}

class StrictBackend:
    """Minimal DynamoDB API emulator: CAS only, no external persistence."""
    def __init__(self):
        self.state={"checkpoint_id":{"S":"audit-a"},
                    "seq":{"N":"0"},"digest":{"S":"GENESIS"}}
        self.calls=[]
    def get_item(self, **kwargs):
        assert kwargs["Key"] == {"checkpoint_id":{"S":"audit-a"}}
        assert kwargs["ConsistentRead"] is True
        return {"Item":{k:dict(v) for k,v in self.state.items()}}
    def update_item(self, **kwargs):
        self.calls.append(kwargs)
        assert kwargs["Key"] == {"checkpoint_id":{"S":"audit-a"}}
        assert kwargs["ConditionExpression"] == "#s = :old_seq AND #d = :old_digest"
        assert kwargs["UpdateExpression"] == "SET #s = :new_seq, #d = :new_digest"
        v=kwargs["ExpressionAttributeValues"]
        if self.state["seq"] != v[":old_seq"] or self.state["digest"] != v[":old_digest"]:
            raise ConditionalCheckFailed()
        self.state["seq"]=v[":new_seq"]
        self.state["digest"]=v[":new_digest"]
        return {"ResponseMetadata":{"HTTPStatusCode":200}}

def service():
    mock=StrictBackend()
    adapter=DynamoDBCheckpoint(client=mock,table_name="checkpoints",
                               checkpoint_id="audit-a")
    return CheckpointWriteService(backend=adapter,checkpoint_id="audit-a"),mock

def test_genesis_step_and_stale_cas():
    srv,mock=service()
    assert srv.read()==(0,None)
    assert srv.advance(expected=(0,None),proposed=(1,"a"*64)) is True
    assert srv.read()==(1,"a"*64)
    assert srv.advance(expected=(0,None),proposed=(1,"b"*64)) is False
    assert len(mock.calls)==2

@pytest.mark.parametrize("before,after",[
    ((0,None),(0,None)), ((0,None),(2,"a"*64)),
    ((1,"a"*64),(0,None)), ((1,"a"*64),(1,"a"*64)),
    ((1,"a"*64),(3,"b"*64)), ((1,"a"*64),(2,None)),
    ((1,"a"*64),(2,"not-a-digest"))
])
def test_reset_skip_and_invalid_digest_never_reach_remote_write(before,after):
    srv,mock=service()
    with pytest.raises(ExternalAnchorRejected):
        srv.advance(expected=before,proposed=after)
    assert mock.calls==[]
    assert srv.read()==(0,None)

def test_wrong_checkpoint_id_rejected():
    mock=StrictBackend()
    adapter=DynamoDBCheckpoint(client=mock,table_name="checkpoints",
                               checkpoint_id="audit-a")
    with pytest.raises(ExternalAnchorRejected,match="WRONG_CHECKPOINT_BINDING"):
        CheckpointWriteService(backend=adapter,checkpoint_id="audit-b")

def test_compromised_caller_can_poison_forward_digest_not_roll_back():
    srv,mock=service()
    # Even an authenticated caller can commit an arbitrary new digest.
    # This is an availability threat; this policy does not authenticate
    # actual local snapshot contents.
    arbitrary="f"*64
    assert srv.advance(expected=(0,None),proposed=(1,arbitrary)) is True
    assert srv.read()==(1,arbitrary)
    with pytest.raises(ExternalAnchorRejected):
        srv.advance(expected=(1,arbitrary),proposed=(0,None))
