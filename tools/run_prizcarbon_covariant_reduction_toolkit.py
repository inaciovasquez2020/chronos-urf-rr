#!/usr/bin/env python3

from pathlib import Path
import sys


repository_root = Path(__file__).resolve().parents[1]

if str(repository_root) not in sys.path:
    sys.path.insert(0, str(repository_root))

from toolkit.prizcarbon_covariant_reduction.audit import main


if __name__ == "__main__":
    raise SystemExit(main())
