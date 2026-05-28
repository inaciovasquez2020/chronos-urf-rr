import subprocess
import sys

def test_newtonian_equal_opposite_gravity_force_actual_value_test():
    subprocess.run(
        [sys.executable, "tools/verify_newtonian_equal_opposite_gravity_force_actual_value_test.py"],
        check=True,
    )
