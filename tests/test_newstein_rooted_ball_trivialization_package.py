from pathlib import Path

def test_newstein_simplicial_admissibility_package_lock():
    text = Path("docs/math/NEWSTEIN_SIMPLICIAL_ADMISSIBILITY_PACKAGE.md").read_text(encoding="utf-8")
    assert "One-vertex parent replacement" in text
    assert "Full vertexwise parent image" in text
    assert "B_R(r)\\ \\text{is a full simplicial subcomplex" in text
    assert "Status: OPEN." in text

def test_newstein_rooted_ball_trivialization_theorem_lock():
    text = Path("docs/math/NEWSTEIN_ROOTED_BALL_TRIVIALIZATION_THEOREM.md").read_text(encoding="utf-8")
    assert "\\partial K_k+K_{k-1}\\partial=\\operatorname{id}-p_{\\#}" in text
    assert "L_k^{(R)}:=\\sum_{t=0}^{R-1}p_{\\#}^{\\,t}K_k" in text
    assert "\\forall c\\in Z_k(B_R(r)),\\ k\\ge 1,\\ \\exists b=L_k^{(R)}(c)\\in C_{k+1}(B_R(r))" in text
    assert "Status: CONDITIONAL on (S0)--(S2)." in text
