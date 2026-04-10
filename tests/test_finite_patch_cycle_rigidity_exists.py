def test_finite_patch_cycle_rigidity_statement_present():
    with open("URF/Lean/Frontier/FinitePatchCycleRigidity.lean", "r") as f:
        s = f.read()
    assert "finitePatchCycleRigidity" in s
    assert "CycleQuotientDim" in s
    assert "FOHomogeneous" in s
