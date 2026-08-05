#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
source_certificate="$root/artifacts/chronos/gfe_axial_220_projected_eft_certificate.json"
output_certificate="$root/artifacts/chronos/gfe_polar_220_gr_darboux_certificate.json"
runtime_receipt="$root/artifacts/chronos/gfe_polar_220_gr_darboux_runtime_receipt.txt"

[ -f "$source_certificate" ] || {
  printf '%s\n' "MISSING_OBJECT := $source_certificate"
  exit 2
}

SOURCE_CERTIFICATE="$source_certificate" \
OUTPUT_CERTIFICATE="$output_certificate" \
RUNTIME_RECEIPT="$runtime_receipt" \
python3 - <<'PY'
from __future__ import annotations

import cmath
import hashlib
import json
import os
from pathlib import Path
import sys

try:
    import sympy as s
except Exception as exc:
    raise SystemExit(f"MISSING_OBJECT := sympy ({exc})")

if tuple(map(int, s.__version__.split(".")[:2])) < (1, 14):
    raise SystemExit(f"MISSING_OBJECT := sympy>=1.14 (found {s.__version__})")

source_path = Path(os.environ["SOURCE_CERTIFICATE"])
output_path = Path(os.environ["OUTPUT_CERTIFICATE"])
receipt_path = Path(os.environ["RUNTIME_RECEIPT"])

source_bytes = source_path.read_bytes()
source = json.loads(source_bytes)
if source.get("schema") != "chronos.gfe_axial_220_projected_eft_certificate.v1":
    raise SystemExit("MISSING_OBJECT := certified axial 220 source schema")
if source.get("scope", {}).get("ell") != 2 or source.get("scope", {}).get("overtone") != 0:
    raise SystemExit("MISSING_OBJECT := certified axial (ell,n)=(2,0) source")
if source.get("root_tube", {}).get("unique_simple_root_for_each_epsilon") is not True:
    raise SystemExit("MISSING_OBJECT := axial unique-simple-root tube")

x, nu = s.symbols("x nu", positive=True)
psi = s.Function("psi")(x)
f = 1 - 2 / x
v_minus = s.factor(f * (2 * (nu + 1) / x**2 - 6 / x**3))
v_plus = s.factor(
    2
    * f
    * (
        nu**2 * (nu + 1) * x**3
        + 3 * nu**2 * x**2
        + 9 * nu * x
        + 9
    )
    / (x**3 * (nu * x + 3) ** 2)
)
sigma = nu * (nu + 1) / 3
superpotential = s.factor(sigma + 3 * f / (x * (nu * x + 3)))

def dstar(expr: s.Expr) -> s.Expr:
    return s.expand(f * s.diff(expr, x))

def a_op(expr: s.Expr) -> s.Expr:
    return s.expand(dstar(expr) + superpotential * expr)

def adag_op(expr: s.Expr) -> s.Expr:
    return s.expand(-dstar(expr) + superpotential * expr)

def h_minus(expr: s.Expr) -> s.Expr:
    return s.expand(-dstar(dstar(expr)) + v_minus * expr)

def h_plus(expr: s.Expr) -> s.Expr:
    return s.expand(-dstar(dstar(expr)) + v_plus * expr)

def zero(expr: s.Expr) -> bool:
    return s.factor(s.cancel(s.together(expr))) == 0

factorization_minus = zero(
    v_minus - (superpotential**2 - dstar(superpotential) - sigma**2)
)
factorization_plus = zero(
    v_plus - (superpotential**2 + dstar(superpotential) - sigma**2)
)
intertwining_forward = zero(a_op(h_minus(psi)) - h_plus(a_op(psi)))
intertwining_reverse = zero(adag_op(h_plus(psi)) - h_minus(adag_op(psi)))
composition_minus = zero(adag_op(a_op(psi)) - h_minus(psi) - sigma**2 * psi)
composition_plus = zero(a_op(adag_op(psi)) - h_plus(psi) - sigma**2 * psi)

omega = s.symbols("omega")
u = s.Function("u")(x)
v = s.Function("v")(x)
u2 = (v_minus - omega**2) * u
v2 = (v_minus - omega**2) * v
au = a_op(u)
av = a_op(v)
wronskian = lambda left, right: s.expand(
    left * dstar(right) - dstar(left) * right
)
wronskian_residual = wronskian(au, av) - (omega**2 + sigma**2) * wronskian(u, v)
wronskian_residual = s.expand(wronskian_residual).xreplace(
    {s.diff(u, x, 2): s.expand(u2 / f**2 - s.diff(f, x) * s.diff(u, x) / f),
     s.diff(v, x, 2): s.expand(v2 / f**2 - s.diff(f, x) * s.diff(v, x) / f)}
)
wronskian_multiplier = zero(wronskian_residual)

horizon_limit = s.simplify(s.limit(superpotential, x, 2, dir="+"))
infinity_limit = s.simplify(s.limit(superpotential, x, s.oo))
endpoint_limits = horizon_limit == sigma and infinity_limit == sigma

identity_flags = {
    "factorization_minus": factorization_minus,
    "factorization_plus": factorization_plus,
    "intertwining_forward": intertwining_forward,
    "intertwining_reverse": intertwining_reverse,
    "composition_minus": composition_minus,
    "composition_plus": composition_plus,
    "wronskian_multiplier": wronskian_multiplier,
    "endpoint_limits": endpoint_limits,
}
failed = [name for name, value in identity_flags.items() if not value]
if failed:
    raise SystemExit("FAILED_IDENTITY := " + ",".join(failed))

root = source["root_tube"]
center_re, center_im = root["omega_center_at_epsilon_0"]
center = complex(center_re, center_im)
radius = float(root["disk_radius"])
sigma_ell2 = 2.0

distance_to_plus_i_sigma = abs(center - 1j * sigma_ell2) - radius
distance_to_minus_i_sigma = abs(center + 1j * sigma_ell2) - radius
if min(distance_to_plus_i_sigma, distance_to_minus_i_sigma) <= 0:
    raise SystemExit("FAILED_BOUND := axial root disk intersects algebraically-special points")

horizon_factor_lower = abs(sigma_ell2 - 1j * center) - radius
infinity_factor_lower = abs(sigma_ell2 + 1j * center) - radius
inverse_factor_lower = (
    distance_to_plus_i_sigma * distance_to_minus_i_sigma
)
if min(horizon_factor_lower, infinity_factor_lower, inverse_factor_lower) <= 0:
    raise SystemExit("FAILED_BOUND := Darboux map not certified invertible on root disk")

def canonical(expr: s.Expr) -> str:
    return s.sstr(s.factor(s.cancel(s.together(expr))))

def digest(payload: object) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

formula_payload = {
    "f": canonical(f),
    "V_minus": canonical(v_minus),
    "V_plus": canonical(v_plus),
    "sigma": canonical(sigma),
    "W": canonical(superpotential),
}
identity_payload = {
    "formula_hash": digest(formula_payload),
    "identity_flags": identity_flags,
    "wronskian_factor": "omega^2+sigma^2",
}
root_transfer_payload = {
    "source_matching_hash": source["certificate_hashes"]["matching_interval_newton"],
    "center": [center_re, center_im],
    "radius": radius,
    "sigma_ell2": sigma_ell2,
    "distance_to_plus_i_sigma_lower": distance_to_plus_i_sigma,
    "distance_to_minus_i_sigma_lower": distance_to_minus_i_sigma,
    "horizon_factor_lower": horizon_factor_lower,
    "infinity_factor_lower": infinity_factor_lower,
    "inverse_factor_lower": inverse_factor_lower,
}

record = {
    "schema": "chronos.gfe_polar_220_gr_darboux_certificate.v1",
    "date": "2026-08-05",
    "status": "certified_gr_epsilon0_polar_220_root_via_exact_darboux_transfer",
    "scope": {
        "parity": "polar",
        "ell": 2,
        "overtone": 0,
        "epsilon": 0.0,
        "dimensionless_frequency": "Omega=M*omega",
        "branch": "Schwarzschild GR baseline inherited from the projected axial certificate",
        "beta2_polar_correction": False,
        "unreduced_trace_log_spectrum": False,
    },
    "source_axial_certificate": {
        "path": "artifacts/chronos/gfe_axial_220_projected_eft_certificate.json",
        "sha256": hashlib.sha256(source_bytes).hexdigest(),
        "matching_interval_newton_hash": source["certificate_hashes"][
            "matching_interval_newton"
        ],
    },
    "darboux": {
        "coordinate": "x=r/M",
        "nu": "(ell-1)*(ell+2)/2",
        "sigma": "nu*(nu+1)/3",
        "superpotential": "sigma+3*f/(x*(nu*x+3))",
        "factorization": {
            "minus": "H_minus+sigma^2=A_dagger*A",
            "plus": "H_plus+sigma^2=A*A_dagger",
            "A": "D_star+W",
            "A_dagger": "-D_star+W"
        },
        "wronskian_transfer": "Wr(Au,Av)=(Omega^2+sigma^2)*Wr(u,v)",
        "identity_flags": identity_flags,
        "formula_hash": identity_payload["formula_hash"],
        "identity_hash": digest(identity_payload),
    },
    "polar_root_at_epsilon_0": {
        "unique_simple_root": True,
        "disk_center": [center_re, center_im],
        "disk_radius": radius,
        "same_disk_as_axial": True,
        "multiplicity_preserved": True,
        "endpoint_conditions_preserved": True,
        "algebraically_special_points": [
            [0.0, sigma_ell2],
            [0.0, -sigma_ell2],
        ],
        "distance_to_plus_i_sigma_lower": distance_to_plus_i_sigma,
        "distance_to_minus_i_sigma_lower": distance_to_minus_i_sigma,
        "horizon_map_factor_abs_lower": horizon_factor_lower,
        "infinity_map_factor_abs_lower": infinity_factor_lower,
        "inverse_multiplier_abs_lower": inverse_factor_lower,
        "transfer_hash": digest(root_transfer_payload),
    },
    "claim_boundary": [
        "This certificate proves only the Schwarzschild GR polar (ell,n)=(2,0) root at epsilon=0 by exact Darboux transfer from the certified axial root.",
        "It does not derive the relative O(beta^2) polar quadratic action, polar master potential, polar root continuation, or polar frequency derivative.",
        "It does not certify axial-polar splitting for epsilon>0.",
        "The unreduced trace-log spectrum and its additional massive mode remain outside this certificate.",
    ],
}

output_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
receipt_lines = [
    f"SYMPY_VERSION := {s.__version__}",
    "GFE_POLAR_220_GR_DARBOUX",
    "SCOPE := Schwarzschild GR epsilon=0 polar root transfer",
    "ELL2_GR_DARBOUX_FACTORIZATION := certified",
    "ELL2_GR_DARBOUX_INTERTWINING := certified",
    "ELL2_GR_DARBOUX_WRONSKIAN_MULTIPLIER := certified",
    "ELL2_GR_DARBOUX_ENDPOINT_MAP := certified",
    f"ELL2_GR_DARBOUX_FORMULA_HASH := {record['darboux']['formula_hash']}",
    f"ELL2_GR_DARBOUX_IDENTITY_HASH := {record['darboux']['identity_hash']}",
    f"ELL2_POLAR_GR_ROOT_TRANSFER_HASH := {record['polar_root_at_epsilon_0']['transfer_hash']}",
    f"ELL2_POLAR_GR_ROOT_DISK_CENTER := [{center_re},{center_im}]",
    f"ELL2_POLAR_GR_ROOT_DISK_RADIUS := {radius}",
    f"ELL2_POLAR_GR_DISTANCE_TO_PLUS_2I_LOWER := {distance_to_plus_i_sigma}",
    f"ELL2_POLAR_GR_DISTANCE_TO_MINUS_2I_LOWER := {distance_to_minus_i_sigma}",
    f"ELL2_POLAR_GR_HORIZON_MAP_FACTOR_ABS_LOWER := {horizon_factor_lower}",
    f"ELL2_POLAR_GR_INFINITY_MAP_FACTOR_ABS_LOWER := {infinity_factor_lower}",
    f"ELL2_POLAR_GR_INVERSE_MULTIPLIER_ABS_LOWER := {inverse_factor_lower}",
    "ELL2_POLAR_GR_UNIQUE_SIMPLE_ROOT := certified",
    "ELL2_POLAR_BETA2_ROOT_CONTINUATION := unproved",
]
receipt_path.write_text("\n".join(receipt_lines) + "\n", encoding="utf-8")

print("RESULT := exact GR Darboux transfer certifies the polar (ell,n)=(2,0) root at epsilon=0")
print(f"CERTIFICATE := {output_path.relative_to(output_path.parents[2])}")
print(f"RUNTIME_RECEIPT := {receipt_path.relative_to(receipt_path.parents[2])}")
print("BOUNDARY := relative O(beta^2) polar master equation and root continuation remain unproved")
PY
