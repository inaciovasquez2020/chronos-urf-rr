#!/usr/bin/env python3
"""Exact symbolic-M check for the corrected GfE Riesz resolvent at fixed r,lambda,omega."""
import json, hashlib
from pathlib import Path
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_laurent_generator.json"
OUT = ROOT / "artifacts/chronos/gfe_symbolic_M_riesz_check.json"
M, beta, z, r, lam, omega = s.symbols("M beta z r lam omega")
I = s.I
loc = {"M": M, "beta": beta, "z": z, "I": I, "r": r, "lam": lam, "lambda": lam, "omega": omega}
data = json.loads(ART.read_text())
def parse(v):
    return s.sympify(v, locals=loc).subs({r: 3, lam: 6, omega: I/4}, simultaneous=True)
def poly_expr(coeffs):
    return sum((parse(c) * beta**j for j,c in enumerate(coeffs)), s.Integer(0))
N = s.Matrix(6, 6, lambda i,j: poly_expr([a[i][j] for a in data["reduced_numerator_beta_coefficients"]]))
D = poly_expr(data["reduced_denominator_beta_coefficients"])
N = N.applyfunc(s.cancel)
D = s.cancel(D)
F = (z*D*s.eye(6)-N).applyfunc(s.cancel)
def valuation(expr):
    p=s.Poly(s.cancel(expr), beta)
    for k in range(p.degree()+1):
        if s.cancel(p.nth(k)) != 0:
            return k
    return None
print("computing determinant", flush=True)
detF = s.factor(F.det(method="domain-ge"))
vdet=valuation(detF)
print("det valuation",vdet, flush=True)
print("computing resolvent numerator entries", flush=True)
vals=[]
for i in range(6):
    row=[]
    for j in range(6):
        # (adj F)[i,j] is cofactor F[j,i].
        minor=F.minor_submatrix(j,i)
        cofactor=(-1)**(i+j)*minor.det(method="domain-ge")
        entry=s.cancel(D*cofactor)
        row.append(valuation(entry))
        print(f"entry {i},{j}: valuation {row[-1]}", flush=True)
    vals.append(row)
report={
 "scope":"exact symbolic M; r=3, lambda=6, omega=i/4",
 "source_sha256":hashlib.sha256(ART.read_bytes()).hexdigest(),
 "determinant_beta_valuation":vdet,
 "resolvent_numerator_entry_valuations":vals,
 "all_entries_at_least_determinant_order":all(v is None or v>=vdet for row in vals for v in row),
 "determinant_after_beta_cancellation":str(s.factor(detF/beta**vdet)) if vdet is not None else None,
}
report["payload_sha256"]=hashlib.sha256(json.dumps(report,sort_keys=True,separators=(",",":")).encode()).hexdigest()
OUT.write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2),flush=True)
if vdet != 4 or not report["all_entries_at_least_determinant_order"]:
    raise SystemExit("symbolic-M cancellation gate failed")
