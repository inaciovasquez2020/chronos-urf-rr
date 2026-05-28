import subprocess
import sys

def test_gdm_empirical_mass_map_binding_theorem():
    subprocess.run([sys.executable, "tools/verify_gdm_empirical_mass_map_binding_theorem.py"], check=True)
