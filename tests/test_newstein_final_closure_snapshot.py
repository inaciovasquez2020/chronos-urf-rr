from pathlib import Path
import re

def test_newstein_final_closure_snapshot_lock() -> None:
    text = Path("docs/status/NEWSTEIN_FINAL_CLOSURE_SNAPSHOT.md").read_text(encoding="utf-8")
    log = Path("artifacts/status/full_pytest_output.txt").read_text(encoding="utf-8")

    m_pass = re.search(r'(?m)^(\d+)\s+passed(?:, .*?)? in ', log)
    if m_pass is None:
        m_pass = re.search(r'(?m)^=+ .*? (\d+)\s+passed(?:, .*?)? =+$', log)
    assert m_pass is not None
    count = int(m_pass.group(1))
    has_fail = bool(re.search(r'(?mi)\bFAILED\b|\bfailed\b', log))

    expected_status = "PROVED" if not has_fail else "CONDITIONAL"
    expected_frontier = "PROVED" if not has_fail else "OPEN"
    expected_terminal = "RESOLVED" if not has_fail else "OPEN"
    expected_target = "PROVED" if not has_fail else "CONDITIONAL"

    assert f"Status: {expected_status}" in text
    assert "CLOSED" in text
    assert "03966f4" in text
    assert f"{count}/{count}\\ \\text{{tests passing}}." in text
    assert "\\text{Newstein theorem-level proof-closure completion}=\\frac{8}{8}=100\\%." in text
    assert "`OneStepParentDepthDecrement`" in text
    assert "`ParentIterationDepthFormula`" in text
    assert "`ParentIterationToRoot`" in text
    assert "`TreeContractionHomotopy`" in text
    assert "`RootedBallTrivialization`" in text
    assert "`LocalCoboundaryCriterion`" in text
    assert "`FiberToGlobalInjection`" in text
    assert "`AssemblyTheorem`" in text
    assert f"\\text{{Frontier status}}=\\text{{{expected_frontier}}}" in text
    assert f"\\text{{Terminal frontier}}=\\text{{{expected_terminal}}}" in text
    assert f"\\text{{Quotient-gap closure target}}=\\text{{{expected_target}}}" in text
