from pathlib import Path

def test_newstein_rooted_ball_trivialization_doc():
    s = Path("docs/math/NEWSTEIN_ROOTED_BALL_TRIVIALIZATION.md").read_text()
    assert "Conditional target." in s
    assert "L > 2r+1" in s
    assert "girth \(> 2r+1\)" in s
    assert "\\widetilde B_r^{\\,\\mathrm{tw}}(x)\\cong \\widetilde B_r^{\\,\\mathrm{triv}}(x)." in s
    assert "\\operatorname{Type}_{k,r}(G_n)=\\operatorname{Type}_{k,r}(H_n)." in s
    assert "No proof of the lemma is claimed here." in s
