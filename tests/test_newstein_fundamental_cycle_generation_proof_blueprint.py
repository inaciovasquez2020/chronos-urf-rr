from pathlib import Path

def test_newstein_fundamental_cycle_generation_proof_blueprint_lock():
    s = Path("docs/math/NEWSTEIN_FUNDAMENTAL_CYCLE_GENERATION_PROOF_BLUEPRINT.md").read_text()
    assert "# Newstein Fundamental Cycle Generation Proof Blueprint" in s
    assert "## Status\nPROVED" in s
    assert "Define the fundamental cycle" in s or "C_e := e + P_T(u,v)." in s
    assert "rooted-local generating family" in s
    assert "NEWSTEIN_ROOTED_LOCAL_TREE_PATH_LEMMA.md" in s
    assert "NEWSTEIN_EXACT_CYCLE_GENERATION_CLOSURE_TARGET.md" in s
