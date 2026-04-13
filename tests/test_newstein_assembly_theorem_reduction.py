from pathlib import Path

def test_newstein_assembly_theorem_reduction_lock() -> None:
    text = Path("docs/math/NEWSTEIN_ASSEMBLY_THEOREM_REDUCTION.md").read_text(encoding="utf-8")
    assert "Status: PROVED" in text
    assert "FiberQuotientRank" in text
    assert "DirectSumIndependence" in text
    assert "PerStepInformationBound" in text
    assert "FiberToGlobalInjection" in text
    assert "\\dim_{\\mathbf F_2} Q_{\\mathrm{fib}} \\ge 4" in text
    assert "Q_{\\mathrm{fib}} \\longrightarrow Q_{\\mathrm{glob}}" in text
    assert "\\dim_{\\mathbf F_2} Q_{\\mathrm{glob}} \\ge 4" in text
    assert "leaks at most \\(V_C\\) information" in text
    assert "AssemblyTheorem is reduced to FiberQuotientRank plus DirectSumIndependence plus PerStepInformationBound plus FiberToGlobalInjection." in text
    assert "Proved from FiberQuotientRank plus DirectSumIndependence plus PerStepInformationBound plus FiberToGlobalInjection." in text
