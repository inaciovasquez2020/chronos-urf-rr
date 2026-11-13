"""Offline IAM policy candidates for an independently hosted checkpoint writer.

No AWS calls, credentials, role creation, policy attachment or deployment.
A successful static check cannot establish effective IAM permissions, because
resource policies, other identity policies, role trust, SCPs, permission
boundaries, and credential delivery also affect authorization.

References:
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/specifying-conditions.html
https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html
"""
from __future__ import annotations

import re


class PolicyCandidateRejected(ValueError):
    pass


_ACCOUNT = re.compile(r"^[0-9]{12}$")
_REGION = re.compile(r"^[a-z]{2}-[a-z]+-[0-9]$")
_TABLE = re.compile(r"^[A-Za-z0-9_.-]{3,255}$")
_KEY = re.compile(r"^[A-Za-z0-9._:/-]{1,128}$")
_ROLE_ARN = re.compile(r"^arn:aws:iam::[0-9]{12}:role/[A-Za-z0-9_+=,.@/-]{1,128}$")


def checkpoint_policy_candidates(*, account_id, region, table_name, checkpoint_id,
                                 writer_role_arn):
    """Return narrow identity-policy candidates, not AWS-authorized roles."""
    if (type(account_id) is not str or not _ACCOUNT.fullmatch(account_id)
        or type(region) is not str or not _REGION.fullmatch(region)
        or type(table_name) is not str or not _TABLE.fullmatch(table_name)
        or type(checkpoint_id) is not str or not _KEY.fullmatch(checkpoint_id)
        or type(writer_role_arn) is not str
        or not _ROLE_ARN.fullmatch(writer_role_arn)
        or writer_role_arn.split("::", 1)[1][:12] != account_id):
        raise PolicyCandidateRejected("INVALID_DEPLOYMENT_IDENTIFIER")
    table = "arn:aws:dynamodb:%s:%s:table/%s" % (region, account_id, table_name)
    item_condition = {
        "ForAllValues:StringEquals": {"dynamodb:LeadingKeys": [checkpoint_id]},
        "Null": {"dynamodb:LeadingKeys": "false"},
    }
    writer = {
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "SingleCheckpointReadAndConditionalUpdate",
            "Effect": "Allow",
            "Action": ["dynamodb:GetItem", "dynamodb:UpdateItem"],
            "Resource": table,
            "Condition": item_condition,
        }],
    }
    controller = {
        "Version": "2012-10-17",
        "Statement": [
            {"Sid": "DenyAllCheckpointTableAccess",
             "Effect": "Deny", "Action": "dynamodb:*", "Resource": table},
            {"Sid": "DenyAssumptionOfCheckpointWriterRole",
             "Effect": "Deny", "Action": "sts:AssumeRole",
             "Resource": writer_role_arn},
        ],
    }
    return {"writer_identity": writer, "controller_identity": controller}


def audit_candidate_policies(candidates, *, table_arn, checkpoint_id, writer_role_arn):
    """Exact-shape offline regression, deliberately NOT a full IAM evaluator."""
    if type(candidates) is not dict or set(candidates) != {
        "writer_identity", "controller_identity"
    }:
        raise PolicyCandidateRejected("INVALID_POLICY_SET")
    writer = candidates["writer_identity"]
    controller = candidates["controller_identity"]
    expected_writer = {
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "SingleCheckpointReadAndConditionalUpdate",
            "Effect": "Allow",
            "Action": ["dynamodb:GetItem", "dynamodb:UpdateItem"],
            "Resource": table_arn,
            "Condition": {
                "ForAllValues:StringEquals": {
                    "dynamodb:LeadingKeys": [checkpoint_id]},
                "Null": {"dynamodb:LeadingKeys": "false"},
            },
        }],
    }
    expected_controller = {
        "Version": "2012-10-17",
        "Statement": [
            {"Sid": "DenyAllCheckpointTableAccess",
             "Effect": "Deny", "Action": "dynamodb:*", "Resource": table_arn},
            {"Sid": "DenyAssumptionOfCheckpointWriterRole",
             "Effect": "Deny", "Action": "sts:AssumeRole",
             "Resource": writer_role_arn},
        ],
    }
    if writer != expected_writer or controller != expected_controller:
        raise PolicyCandidateRejected("UNEXPECTED_POLICY_GRANT_OR_DENY")
    return True
