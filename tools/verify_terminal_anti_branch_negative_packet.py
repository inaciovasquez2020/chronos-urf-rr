#!/usr/bin/env python3
import hashlib
import json
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/terminal_anti_branch_negative_packet_2026_06_01"

FILES = {
    "result": ART / "terminal_anti_branch_status_certificate_result.json",
    "certificate": ART / "terminal_branch_closed_negative_result_certificate.json",
    "final_validation": ART / "publication_ready_case_report_or_branch_closed_validation.json",
    "formal_negative_result_packet": ART / "formal_negative_result_packet.json",
    "packet_audit": ART / "terminal_anti_branch_certificate_packet_audit.json",
    "freeze_manifest": ART / "TERMINAL_ANTI_BRANCH_CERTIFICATE_PACKET_FREEZE_MANIFEST.json",
    "archive_manifest": ART / "TERMINAL_ANTI_BRANCH_CERTIFICATE_PACKET_ARCHIVE_MANIFEST.json",
    "archive_extraction_audit": ART / "terminal_anti_branch_certificate_packet_archive_extraction_audit.json",
    "handoff_index": ART / "TERMINAL_ANTI_BRANCH_CERTIFICATE_PACKET_HANDOFF_INDEX.json",
    "archive": ART / "terminal_anti_branch_negative_packet_20260530T230006Z.tar.gz",
    "archive_sha256_file": ART / "terminal_anti_branch_negative_packet_20260530T230006Z.tar.gz.sha256",
}

missing = {k: str(v) for k, v in FILES.items() if not v.exists()}
if missing:
    raise SystemExit("MISSING_TERMINAL_ANTI_BRANCH_PACKET_FILES: " + json.dumps(missing, indent=2, sort_keys=True))

loaded = {
    k: json.loads(v.read_text())
    for k, v in FILES.items()
    if k not in {"archive", "archive_sha256_file"}
}

archive_digest = hashlib.sha256(FILES["archive"].read_bytes()).hexdigest()
archive_sha_line = FILES["archive_sha256_file"].read_text().strip()

checks = {
    "result_pass": loaded["result"].get("decision") == "PASS",
    "result_route": loaded["result"].get("route") == "branch_closed_negative_result",
    "result_status": loaded["result"].get("reason") == "TERMINAL_BRANCH_CLOSED_NEGATIVE_RESULT",
    "certificate_pass": loaded["certificate"].get("decision") == "PASS",
    "certificate_route": loaded["certificate"].get("route") == "branch_closed_negative_result",
    "certificate_status": loaded["certificate"].get("reason") == "TERMINAL_BRANCH_CLOSED_NEGATIVE_RESULT",
    "final_validation_negative_pass": loaded["final_validation"].get("decision") == "PASS_BRANCH_CLOSED_NEGATIVE_RESULT",
    "formal_negative_result_pass": loaded["formal_negative_result_packet"].get("decision") == "PASS_BRANCH_CLOSED_NEGATIVE_RESULT",
    "packet_audit_pass": loaded["packet_audit"].get("decision") == "PASS",
    "freeze_manifest_pass": loaded["freeze_manifest"].get("decision") == "PASS",
    "archive_manifest_pass": loaded["archive_manifest"].get("decision") == "PASS",
    "archive_extraction_audit_pass": loaded["archive_extraction_audit"].get("decision") == "PASS",
    "handoff_index_pass": loaded["handoff_index"].get("decision") == "PASS",
    "archive_sha256_matches_manifest": archive_digest == loaded["archive_manifest"].get("archive_sha256"),
    "archive_sha256_matches_sha_file": archive_digest in archive_sha_line,
    "expected_archive_sha256": archive_digest == "b931a7442d5ace28b2658bf70151276211e61b5f20d2d8fa2abd248551e1ed52",
    "expected_freeze_collection_sha256": loaded["handoff_index"].get("freeze_collection_sha256") == "a27e7a6da39cbc8a2b9acb52e6edb53ecadcae8164c5eb3691e14356d1a2541b",
}

with tarfile.open(FILES["archive"], "r:gz") as tar:
    members = sorted(m.name for m in tar.getmembers() if m.isfile())

expected_members = sorted([
    "input_final_report_validation/formal_negative_result_packet/formal_negative_result_packet.json",
    "input_final_report_validation/publication_ready_case_report_or_branch_closed_validation.json",
    "results/terminal_anti_branch_status_certificate_result.json",
    "terminal_anti_branch_certificate_packet_audit/terminal_anti_branch_certificate_packet_audit.json",
    "terminal_certificate/terminal_branch_closed_negative_result_certificate.json",
])

checks["archive_members_exact"] = members == expected_members

boundary_terms = [
    "no physical anti-gravity mechanism identified",
    "no new gravity claim",
    "no GR failure claim",
    "no dark matter replacement claim",
    "no Lambda-CDM failure claim",
    "no quantum gravity claim",
    "no Clay problem claim",
]

for name in ["result", "certificate", "packet_audit", "handoff_index"]:
    boundary = loaded[name].get("boundary", [])
    for term in boundary_terms:
        checks[f"{name}_boundary_contains_{term}"] = term in boundary

failed = [k for k, v in checks.items() if not v]
if failed:
    print("TERMINAL_ANTI_BRANCH_NEGATIVE_PACKET_FAIL")
    print(json.dumps(failed, indent=2, sort_keys=True))
    raise SystemExit(1)

print("TERMINAL_ANTI_BRANCH_NEGATIVE_PACKET_OK")
print(json.dumps({
    "decision": "PASS",
    "route": loaded["result"].get("route"),
    "terminal_status": loaded["result"].get("reason"),
    "archive_sha256": archive_digest,
    "freeze_collection_sha256": loaded["handoff_index"].get("freeze_collection_sha256"),
}, indent=2, sort_keys=True))
