"""Legacy agent write entrypoint, fail-closed unless a trusted controller approves.

Only disposable worktrees and signed, policy-bound requests are supported.
The CLI and JSON-RPC server do not possess signing authority, and consequently
will DENY their old implicit-write requests rather than use unsafe rollback.
"""
from __future__ import annotations

from .hardened_mutation import governed_patch_mutation
