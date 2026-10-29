#!/usr/bin/env python3
"""Run the pinned qnm==0.4.4 Leaver continued-fraction residual check."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

from qnm.radial import leaver_cf_inv_lentz

OMEGA = complex(0.37367168441804177, -0.08896231568893546)
PARAMS = {
    "omega_real": OMEGA.real,
    "omega_imag": OMEGA.imag,
    "a": 0.0,
    "s": -2,
    "m": 2,
    "A_real": 4.0,
    "A_imag": 0.0,
    "n_inv": 0,
    "tol": 1e-10,
    "N_min": 0,
    "N_max": "inf",
}

residual, estimated_error, iterations = leaver_cf_inv_lentz(
    omega=OMEGA,
    a=PARAMS["a"],
    s=PARAMS["s"],
    m=PARAMS["m"],
    A=complex(PARAMS["A_real"], PARAMS["A_imag"]),
    n_inv=PARAMS["n_inv"],
    tol=PARAMS["tol"],
    N_min=PARAMS["N_min"],
    N_max=float("inf"),
)

payload = {
    "schema": "urf.leaver-residual-receipt.v1",
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "executable": os.path.realpath(sys.executable),
    "python_version": sys.version,
    "platform": platform.platform(),
    "package": "qnm",
    "package_version": importlib.metadata.version("qnm"),
    "function": "qnm.radial.leaver_cf_inv_lentz",
    "input": PARAMS,
    "raw_output": {
        "residual_repr": repr(complex(residual)),
        "residual_real": float(complex(residual).real),
        "residual_imag": float(complex(residual).imag),
        "estimated_error": float(estimated_error),
        "iterations": int(iterations),
    },
    "derived": {
        "absolute_residual": abs(complex(residual)),
        "acceptance_threshold_absolute_residual": 1e-8,
        "passed_threshold": abs(complex(residual)) < 1e-8,
    },
}
canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
payload["receipt_sha256"] = hashlib.sha256(canonical).hexdigest()
out = Path("leaver_residual_receipt.json")
out.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
print(out.read_text(encoding="utf-8"), end="")
if payload["package_version"] != "0.4.4":
    raise SystemExit(f"expected qnm==0.4.4, got {payload['package_version']}")
if not payload["derived"]["passed_threshold"]:
    raise SystemExit("continued-fraction residual exceeded the predeclared threshold")
