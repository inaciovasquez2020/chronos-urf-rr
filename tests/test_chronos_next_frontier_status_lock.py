from pathlib import Path
import subprocess


DOC = Path("docs/status/CHRONOS_NEXT_FRONTIER_STATUS_LOCK_2026_05_04.md")


def test_chronos_next_frontier_status_tokens_present():
    text = DOC.read_text(encoding="utf-8")
    assert "CERTIFIED_FRONTIER_ONLY" in text
    assert "THEOREM_CLOSURE_FALSE" in text
    assert "NO_P_VS_NP_CLAIM" in text
    assert "NO_UNCONDITIONAL_ENTROPYDEPTH_CLAIM" in text
    assert "NO_H4_1_FGL_CLOSURE_CLAIM" in text
    assert "MISSING_OBJECT_EXPLICIT_IC_LOWER_BOUND" in text


def test_chronos_next_frontier_names_weakest_missing_object():
    text = DOC.read_text(encoding="utf-8")
    assert "explicit family \\(F_n\\)" in text
    assert "explicit distribution \\(\\mu_n\\)" in text
    assert "explicit search functional \\(\\operatorname{Search}_{F_n}\\)" in text
    assert "IC_{\\mu_n}(\\operatorname{Search}_{F_n}) \\ge c n" in text


def test_chronos_next_frontier_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_chronos_next_frontier_status_lock.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "CERTIFIED_FRONTIER_ONLY" in result.stdout
