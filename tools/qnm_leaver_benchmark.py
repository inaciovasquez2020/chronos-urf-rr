#!/usr/bin/env python3
"""Reproducible Schwarzschild l=2, n=0 Leaver QNM benchmark.

qnm returns M*omega. The selected published reference is quoted in 2M*omega,
so the comparison below multiplies the package result by two. This is a
frequency-comparison residual, not the raw continued-fraction function value.
"""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import platform
import sys

import qnm

REFERENCE_2M_OMEGA = complex(0.747343, -0.177925)
ABS_TOL = 1.0e-6


def main() -> int:
    sequence = qnm.modes_cache(s=-2, l=2, m=2, n=0)
    omega_M, separation_constant, mixing = sequence(a=0.0)
    computed = 2.0 * complex(omega_M)
    residual = computed - REFERENCE_2M_OMEGA
    receipt = {
        "benchmark": "Schwarzschild gravitational QNM l=2 m=2 n=0",
        "solver": "qnm Leaver solver",
        "qnm_version": importlib.metadata.version("qnm"),
        "python": sys.version,
        "platform": platform.platform(),
        "mode": {"s": -2, "l": 2, "m": 2, "n": 0, "a_over_M": 0.0},
        "convention": "qnm returns M*omega; multiplied by 2 for 2M*omega",
        "reference_2M_omega": [REFERENCE_2M_OMEGA.real, REFERENCE_2M_OMEGA.imag],
        "computed_2M_omega": [computed.real, computed.imag],
        "complex_frequency_residual": [residual.real, residual.imag],
        "absolute_residual": abs(residual),
        "absolute_tolerance": ABS_TOL,
        "separation_constant": [complex(separation_constant).real, complex(separation_constant).imag],
        "mixing_coefficients_count": len(mixing),
        "dependency_versions": {
            name: importlib.metadata.version(name)
            for name in ("numpy", "scipy", "numba", "llvmlite", "tqdm")
        },
        "status": "PASS" if abs(residual) <= ABS_TOL else "FAIL",
        "note": "Rounded reference comparison only; not a continued-fraction equation residual.",
    }
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if abs(residual) <= ABS_TOL else 1


if __name__ == "__main__":
    raise SystemExit(main())
