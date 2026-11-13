"""Candidate DynamoDB-backed checkpoint with linearizable read and conditional advance.

Backend contract: a *pre-provisioned* record lives in a single-region DynamoDB
BASE TABLE (not a GSI). The operator must provision (seq=0, digest='GENESIS')
out of band. Its immutable partition key is 'checkpoint_id'.

THREAT MODEL: attacker can restore/tamper with local journal snapshots but
cannot read/use controller AWS credentials, call DynamoDB, alter IAM, restore
or delete the table, or control AWS. DynamoDB CAS does NOT protect against a
compromised controller credential: IAM cannot mandate the ConditionExpression
on every UpdateItem. This is not a TPM or independent secure-enclave counter.

Supply an authenticated, configured DynamoDB API client with get_item and
update_item methods (e.g. a preinstalled boto3 client). This module installs
nothing, uses no network at import, and never provisions infrastructure.
"""
from __future__ import annotations
import re

from .external_anchor_candidate import ExternalAnchorRejected, _record

_ID = re.compile(r"^[A-Za-z0-9._:/-]{1,128}$")
_DIGEST = re.compile(r"^[0-9a-f]{64}$")
_GENESIS = "GENESIS"


class DynamoDBCheckpoint:
    """Fail-closed adapter; first load the genesis checkpoint out of band."""
    def __init__(self, *, client, table_name, checkpoint_id):
        if (not isinstance(table_name, str) or not _ID.fullmatch(table_name)
            or not isinstance(checkpoint_id, str) or not _ID.fullmatch(checkpoint_id)
            or not callable(getattr(client,"get_item",None))
            or not callable(getattr(client,"update_item",None))):
            raise ExternalAnchorRejected("INVALID_DYNAMODB_CONFIGURATION")
        self.client=client
        self.table=table_name
        self.key={"checkpoint_id":{"S":checkpoint_id}}

    def _read(self):
        try:
            response=self.client.get_item(TableName=self.table,Key=self.key,
                                          ConsistentRead=True)
        except Exception as exc:
            raise ExternalAnchorRejected("CHECKPOINT_READ_UNAVAILABLE") from exc
        if type(response) is not dict or "Item" not in response:
            raise ExternalAnchorRejected("CHECKPOINT_NOT_PROVISIONED")
        item=response["Item"]
        if (type(item) is not dict or set(item)!={"checkpoint_id","seq","digest"}
            or item.get("checkpoint_id")!=self.key["checkpoint_id"]
            or type(item.get("seq")) is not dict or set(item["seq"])!={"N"}
            or type(item.get("digest")) is not dict or set(item["digest"])!={"S"}):
            raise ExternalAnchorRejected("INVALID_REMOTE_CHECKPOINT_SCHEMA")
        number=item["seq"]["N"]
        h=item["digest"]["S"]
        if (type(number) is not str or not number.isascii()
            or not number.isdecimal() or (len(number)>1 and number[0]=="0")
            or len(number)>18 or type(h) is not str):
            raise ExternalAnchorRejected("INVALID_REMOTE_CHECKPOINT_VALUE")
        seq=int(number)
        if seq==0:
            if h != _GENESIS:
                raise ExternalAnchorRejected("INVALID_REMOTE_GENESIS")
            return (0,None)
        if not _DIGEST.fullmatch(h):
            raise ExternalAnchorRejected("INVALID_REMOTE_DIGEST")
        return _record((seq,h))

    def read(self):
        return self._read()

    def compare_and_advance(self, expected, proposed):
        before=_record(expected)
        after=_record(proposed)
        if before[0] >= 10**18-1 or after[0] != before[0]+1:
            raise ExternalAnchorRejected("NONMONOTONIC_REMOTE_ADVANCE")
        values={":old_seq":{"N":str(before[0])},
                ":old_digest":{"S":before[1] if before[1] is not None else _GENESIS},
                ":new_seq":{"N":str(after[0])},
                ":new_digest":{"S":after[1]}}
        try:
            response=self.client.update_item(
                TableName=self.table,Key=self.key,
                UpdateExpression="SET #s = :new_seq, #d = :new_digest",
                ConditionExpression="#s = :old_seq AND #d = :old_digest",
                ExpressionAttributeNames={"#s":"seq","#d":"digest"},
                ExpressionAttributeValues=values,
                ReturnValues="NONE")
        except Exception as exc:
            # A conditional failure must not be confused with a transport
            # timeout. Both fail the update; the caller poisons its owner.
            code=getattr(exc,"response",{}).get("Error",{}).get("Code")
            if code=="ConditionalCheckFailedException":
                return False
            raise ExternalAnchorRejected("CHECKPOINT_ADVANCE_UNCERTAIN") from exc
        if (type(response) is not dict
            or response.get("ResponseMetadata",{}).get("HTTPStatusCode")!=200):
            raise ExternalAnchorRejected("UNCONFIRMED_CHECKPOINT_UPDATE")
        return True
