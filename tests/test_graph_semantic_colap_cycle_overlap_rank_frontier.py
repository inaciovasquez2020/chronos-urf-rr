import subprocess
import sys

def test_graph_semantic_colap_cycle_overlap_rank_frontier_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_graph_semantic_colap_cycle_overlap_rank_frontier.py"],
        check=True,
    )
