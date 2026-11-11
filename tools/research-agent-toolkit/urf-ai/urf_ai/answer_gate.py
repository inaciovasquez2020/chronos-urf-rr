"""Read-only CSTS answer gate: claim status, never independent theorem certification.

Only accepts a live controller-owned ClaimJournal, not model-supplied records,
caller-supplied integrity flags, or user-provided HMAC receipts.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .csts import ClaimJournal
from .evidence import digest


@dataclass(frozen=True)
class Verdict:
    allowed: bool
    level: str
    reasons: tuple[str, ...]


def _deny(*reasons: str) -> Verdict:
    return Verdict(False, "BLOCKED", tuple(sorted(set(reasons))))


def assess_from_journal(journal: ClaimJournal, proposal: dict[str, Any]) -> Verdict:
    """Check a proposed answer against the authenticated journal's exact claim."""
    if type(journal) is not ClaimJournal:
        return _deny("UNTRUSTED_JOURNAL_TYPE")
    if not isinstance(proposal, dict):
        return _deny("INVALID_PROPOSAL")
    fields = ("claim_id", "semantic_version", "proposition_digest",
              "scope_digest", "source_revision", "assertion")
    if any(k not in proposal for k in fields):
        return _deny("MISSING_BINDING")
    cid = proposal["claim_id"]
    if type(cid) is not str or not cid:
        return _deny("INVALID_CLAIM_ID")
    try:
        if not journal.audit_events():
            return _deny("JOURNAL_INTEGRITY_FAILED")
        record = journal.claim(cid)
    except (KeyError, ValueError, TypeError, AttributeError, RecursionError):
        return _deny("MISSING_OR_INVALID_CLAIM")
    if not journal.events or not isinstance(record, dict):
        return _deny("EMPTY_OR_INVALID_JOURNAL")
    required = ("claim_id", "semantic_version", "proposition", "scope",
                "source_revision", "state", "stale", "kind", "assumptions",
                "frontier", "boundaries", "dependencies")
    if any(k not in record for k in required):
        return _deny("INVALID_RECORD")
    if type(record["semantic_version"]) is not int or type(proposal["semantic_version"]) is not int:
        return _deny("INVALID_VERSION_TYPE")
    try:
        expected = {
            "claim_id": record["claim_id"],
            "semantic_version": record["semantic_version"],
            "proposition_digest": digest(record["proposition"]),
            "scope_digest": digest(record["scope"]),
            "source_revision": record["source_revision"],
        }
        if any(type(record[k]) is not list for k in ("assumptions", "frontier", "boundaries", "dependencies")):
            return _deny("INVALID_RECORD_SHAPE")
        if any(proposal[k] != v for k, v in expected.items()):
            return _deny("BINDING_MISMATCH")
        if type(proposal["assertion"]) is not str:
            return _deny("INVALID_ASSERTION_TYPE")
        if record["stale"] is not False:
            return _deny("STALE_DEPENDENCY")
        status = record["state"]
        assertion = proposal["assertion"]
        if status not in ("OPEN", "CONDITIONAL", "PROVED", "WITHDRAWN"):
            return _deny("INVALID_LEDGER_STATE")
        if assertion == "PROVED":
            if status != "PROVED" or record["kind"] != "THEOREM":
                return _deny("NOT_PROVED_THEOREM")
            if any(type(a) is not dict or a.get("status") != "DISCHARGED" for a in record["assumptions"]):
                return _deny("UNDISCHARGED_ASSUMPTION")
            if any(type(f) is not dict or (f.get("status") == "OPEN" and f.get("blocking", True)) for f in record["frontier"]):
                return _deny("OPEN_FRONTIER")
            if any(type(b) is not dict or (b.get("active", False) and b.get("blocks_proved", False)) for b in record["boundaries"]):
                return _deny("ACTIVE_BOUNDARY")
        elif assertion == "CONDITIONAL":
            if status not in ("CONDITIONAL", "PROVED"):
                return _deny("CONDITIONAL_UNSUPPORTED")
        elif assertion == "OPEN":
            if status == "WITHDRAWN":
                return _deny("WITHDRAWN_CLAIM")
        else:
            return _deny("UNSUPPORTED_ASSERTION")
        return Verdict(True, assertion, ("AUTHENTICATED_CSTS_STATUS_ONLY",))
    except (TypeError, ValueError, KeyError, RecursionError):
        return _deny("MALFORMED_DATA")
