"""Offline IAM candidate structure checks. Never presented as AWS simulation."""
from copy import deepcopy

import pytest

from urf_ai.checkpoint_iam_policy_candidate import (
    PolicyCandidateRejected, audit_candidate_policies,
    checkpoint_policy_candidates,
)

ACCOUNT="123456789012"
REGION="us-east-1"
TABLE="URFAuditCheckpoints"
KEY="journal-a"
ROLE=f"arn:aws:iam::{ACCOUNT}:role/urf-ai-separate-writer"
TABLE_ARN=f"arn:aws:dynamodb:{REGION}:{ACCOUNT}:table/{TABLE}"

def generate():
    return checkpoint_policy_candidates(account_id=ACCOUNT,region=REGION,
        table_name=TABLE,checkpoint_id=KEY,writer_role_arn=ROLE)

def audit(policies):
    return audit_candidate_policies(policies,table_arn=TABLE_ARN,
        checkpoint_id=KEY,writer_role_arn=ROLE)

def test_exact_scoped_policy_candidate_accepts():
    p=generate()
    assert audit(p) is True
    assert p["writer_identity"]["Statement"][0]["Action"]==[
        "dynamodb:GetItem","dynamodb:UpdateItem"]
    assert p["controller_identity"]["Statement"][0]["Effect"]=="Deny"

@pytest.mark.parametrize("field,bad",[
    ("account_id","123"),
    ("region","*"),
    ("table_name","*"),
    ("checkpoint_id",""),
    ("writer_role_arn","arn:aws:iam::999999999999:role/urf-ai-writer"),
])
def test_bad_identifiers_rejected(field,bad):
    params=dict(account_id=ACCOUNT,region=REGION,table_name=TABLE,
                checkpoint_id=KEY,writer_role_arn=ROLE)
    params[field]=bad
    with pytest.raises(PolicyCandidateRejected):
        checkpoint_policy_candidates(**params)

@pytest.mark.parametrize("mutation",[
    lambda p: p["writer_identity"]["Statement"][0]["Action"].append("dynamodb:PutItem"),
    lambda p: p["writer_identity"]["Statement"][0].update(Resource="*"),
    lambda p: p["writer_identity"]["Statement"][0].pop("Condition"),
    lambda p: p["writer_identity"]["Statement"][0]["Condition"].pop("Null"),
    lambda p: p["writer_identity"]["Statement"][0]["Condition"]["ForAllValues:StringEquals"].update(
        {"dynamodb:LeadingKeys":["*"]}),
    lambda p: p["controller_identity"]["Statement"][0].update(Effect="Allow"),
    lambda p: p["controller_identity"]["Statement"].pop(),
    lambda p: p["controller_identity"]["Statement"][1].update(Resource="*"),
])
def test_grant_expansion_or_boundary_removal_rejected(mutation):
    p=deepcopy(generate())
    mutation(p)
    with pytest.raises(PolicyCandidateRejected,match="UNEXPECTED_POLICY"):
        audit(p)

def test_no_claim_about_live_effective_permissions():
    # These are merely JSON candidates. Role trust, service permissions,
    # credential delivery, other IAM grants and AWS behavior are NOT tested.
    assert audit(generate()) is True
