from pathlib import Path

def test_newstein_global_direct_sum_embedding_corollary_lock() -> None:
    s = Path("docs/math/NEWSTEIN_GLOBAL_DIRECT_SUM_EMBEDDING_COROLLARY.md").read_text()
    assert "# Newstein Global Direct-Sum Embedding Corollary" in s
    assert "Status: OPEN" in s
    assert r"\iota_u([c_u])=\iota_v([c_v])" in s
    assert r"\bigoplus_{u}\bigl(Z_1(B_r(u);\mathbf F_2)/W_u\bigr)" in s
    assert "exact corollary turning pairwise injectivity into a global direct-sum lower bound" in s
