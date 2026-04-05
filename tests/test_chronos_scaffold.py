import subprocess
import shutil

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def lake_available():
    return shutil.which("lake") is not None

def test_ep2_bundle_file_compiles():
    if not lake_available(): return
    proc = run(["lake", "env", "lean", "lean/Chronos/EP2Bundle.lean"])
    assert proc.returncode == 0, proc.stdout + proc.stderr

def test_full_repo_builds():
    if not lake_available(): return
    proc = run(["lake", "build"])
    assert proc.returncode == 0, proc.stdout + proc.stderr

def test_single_remaining_axiom_in_chronos():
    proc = run(["grep", "-RIn", r"^[[:space:]]*axiom\b", "lean/Chronos"])
    lines = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    assert len(lines) == 1, f"Unexpected axiom count: {lines}"

def test_xornorm_file_compiles():
    if not lake_available(): return
    proc = run(["lake", "env", "lean", "lean/Chronos/XorNorm.lean"])
    assert proc.returncode == 0, proc.stdout + proc.stderr

def test_xorreduce_file_compiles():
    if not lake_available(): return
    proc = run(["lake", "env", "lean", "lean/Chronos/XorReduce.lean"])
    assert proc.returncode == 0, proc.stdout + proc.stderr
