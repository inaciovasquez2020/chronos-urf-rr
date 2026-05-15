import subprocess
import sys

def test_finite_noncollapsed_energy_budget_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_finite_noncollapsed_energy_budget.py"],
        check=True,
    )
