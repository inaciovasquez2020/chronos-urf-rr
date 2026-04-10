from pathlib import Path

def test_nonfactorization_reduction_present():
    s = Path("docs/specs/NONFACTORIZATION_REDUCTION.md").read_text()
    assert "IR_not_FOkR_definable" in s
    assert "tp_k_R(G^+) = tp_k_R(G^-)" in s
    assert "IR(R,G^+) \\neq IR(R,G^-)." in s
    assert "Everything else is propositional reduction." in s
