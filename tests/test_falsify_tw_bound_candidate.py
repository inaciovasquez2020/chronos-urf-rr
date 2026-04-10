import subprocess
import sys

def test_parallel_bundle_candidate():
    proc = subprocess.run(
        [sys.executable, "scripts/falsify_tw_bound.py", "2", "5"],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = proc.stdout
    assert "contains_K4_subgraph_so_treewidth_at_least_3: True" in out
    assert "explicit_width_3_decomposition_verified: True" in out
    assert "bundle_has_no_cycles_at_or_below_cutoff: True" in out
    assert "candidate_falsifies_tw_le_t_bound_at_R: True" in out
