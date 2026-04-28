from pathlib import Path
MANIFEST = Path("docs/status/URF_STATUS_VERIFICATION_MANIFEST_2026_04_28.md")
def test_urf_status_verification_manifest_exists():
assert MANIFEST.exists()
def test_urf_status_verification_manifest_has_boundary():
text = MANIFEST.read_text(encoding="utf-8")
assert "status-only verification manifest" in text
assert "Build success verifies artifact integrity only" in text
assert "does not imply theorem-level closure" in text
def test_urf_status_verification_manifest_tracks_suite_command():
text = MANIFEST.read_text(encoding="utf-8")
assert "python3 tools/verify_urf_status_suite.py" in text
assert "URF status export verification PASS" in text
assert "URF status language guard PASS" in text
assert "URF status suite PASS" in text
def test_urf_status_verification_manifest_preserves_boundary_classification():
text = MANIFEST.read_text(encoding="utf-8")
assert "Conditional repositories remain conditional" in text
assert "Open formalizations remain open" in text
assert "must not be classified as solved theorem surfaces" in text
