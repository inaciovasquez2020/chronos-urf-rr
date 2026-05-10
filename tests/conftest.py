from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PYROOT = ROOT / "py"

for candidate in [PYROOT, ROOT, ROOT / "src", ROOT / "python"]:
    if candidate.exists():
        path = str(candidate.resolve())
        if path not in sys.path:
            sys.path.insert(0, path)
