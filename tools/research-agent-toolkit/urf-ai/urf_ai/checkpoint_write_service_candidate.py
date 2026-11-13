"""A policy boundary for a separately deployed checkpoint writer.

This is a transport-free command handler, NOT a deployed network service.
Its AWS credentials must be available ONLY to this separate process/identity.
The controller may submit expected/proposed checkpoints through a separately
authenticated channel, but must not receive DynamoDB UpdateItem credentials.

The handler prevents backwards moves, skips, record deletion, and stale
overwrites even for a caller allowed to request advancement. It cannot
prevent malicious *forward* digests (denial of service) or an administrator
who can overwrite DynamoDB records. Do not expose untrusted Python objects
to this handler: parsing/authentication are the deployment transport's duty.
"""
from __future__ import annotations

from .dynamodb_checkpoint_candidate import DynamoDBCheckpoint
from .external_anchor_candidate import ExternalAnchorRejected, _record


class CheckpointWriteService:
    """Server-side domain policy, separate from the read/advance client."""
    def __init__(self, *, backend, checkpoint_id):
        if type(backend) is not DynamoDBCheckpoint:
            raise ExternalAnchorRejected("UNTRUSTED_CHECKPOINT_BACKEND")
        if backend.key != {"checkpoint_id": {"S": checkpoint_id}}:
            raise ExternalAnchorRejected("WRONG_CHECKPOINT_BINDING")
        self._backend = backend

    def read(self):
        return self._backend.read()

    def advance(self, *, expected, proposed):
        before = _record(expected)
        after = _record(proposed)
        if (before[0] >= 10**18 - 1 or after[0] != before[0] + 1
            or after[1] is None):
            raise ExternalAnchorRejected("NONMONOTONIC_CHECKPOINT_REQUEST")
        # Backend performs DynamoDB conditional update; its compare-and-
        # advance has no unconditional overwrite fallback.
        return self._backend.compare_and_advance(before, after)
