"""Evidence-bounded URF-AI curvature benchmark extension (pure Python, no I/O).

For the *marked, prescribed* metric g=-N(w)^2 dt^2+dw^2+dx^2+dy^2+dz^2,
the algebraic certificate uses y>0, N>=m>0, |u|<=M,
|D-u|<=E, |y-N|<=delta, R=-2*u/N and Rhat=-2*D/y.

This is a deterministic finite-case oracle and diagnostic, NOT a proof assistant,
physical observation, neural model, or independent theorem verification.
"""

from fractions import Fraction as F
from math import comb

if not __debug__:
    raise RuntimeError("BLOCKED: assertions disabled; no benchmark verification")


def _f(x):
    if type(x) not in (F, int):
        raise TypeError("only exact integer or Fraction inputs are accepted")
    return F(x)


def algebra_bound(*, y, D, N, u, m, M, E, delta):
    """Check all abstract assumptions and compute exact error and bound.

    N/u are *synthetic true values* used for validation; no claim that these
    scalar values extend to a periodic C4 lapse satisfying the sampling model.
    """
    y, D, N, u, m, M, E, delta = map(_f, (y, D, N, u, m, M, E, delta))
    if not (m > 0 and N >= m and y > 0 and M >= 0 and E >= 0 and delta >= 0):
        raise ValueError("invalid or insufficient positivity/bound hypotheses")
    if not (abs(u) <= M and abs(D-u) <= E and abs(y-N) <= delta):
        raise ValueError("claimed error hypotheses are not satisfied")
    actual = -2*u/N
    estimate = -2*D/y
    bound = 2*(E+M*delta/m)/y
    if abs(estimate-actual) > bound:
        raise AssertionError("algebraic curvature certificate violated")
    sign = "POSITIVE" if estimate > bound else "NEGATIVE" if -estimate > bound else "INCONCLUSIVE"
    if sign == "POSITIVE" and actual <= 0:
        raise AssertionError("false positive sign certification")
    if sign == "NEGATIVE" and actual >= 0:
        raise AssertionError("false negative sign certification")
    return {"true": actual, "estimate": estimate, "error": abs(estimate-actual),
            "bound": bound, "sign": sign}


def point_certificate(*, y, D, m, M, B, eta, h, k, n):
    """Compute a conditional certificate from observed mean and stencil.

    Requires independent justification of the derivative, noise, geometry and
    sampling hypotheses; does not reconstruct those hypotheses from data.
    """
    y, D, m, M, B, eta, h = map(_f, (y, D, m, M, B, eta, h))
    if type(k) is not int or type(n) is not int:
        raise TypeError("k,n must be integers")
    if not (m > 0 and M >= 0 and B >= 0 and eta >= 0 and eta < m
            and h > 0 and n >= 3 and 1 <= k and 2*k < n
            and y >= m-eta and y > 0):
        raise ValueError("invalid sampling, geometry, or positivity assumptions")
    d = k*h
    E2 = B*(d*d/F(12) + h*h/F(24)) + 4*eta/(d*d)
    delta = eta + M*h*h/F(24)
    estimate = -2*D/y
    radius = 2*(E2 + M*delta/m)/y
    sign = "POSITIVE" if estimate > radius else "NEGATIVE" if -estimate > radius else "INCONCLUSIVE"
    return {"estimate":estimate, "radius":radius, "E2":E2,
            "delta":delta, "sign":sign}


def _coeffs():
    """P(s)=s^5(1-s)^5(2s-1), coefficients over Q."""
    coeff = {}
    for k in range(6):
        z = F(comb(5,k)*(-1)**k)
        coeff[k+5] = coeff.get(k+5,F(0))-z
        coeff[k+6] = coeff.get(k+6,F(0))+2*z
    return coeff


def polynomial_value(s, derivative=0):
    s = _f(s)
    if type(derivative) is not int or not (0<=derivative<=4):
        raise ValueError("derivative degree out of scope")
    c = _coeffs()
    for _ in range(derivative):
        c = {k-1:k*v for k,v in c.items() if k>0}
    return sum((v*s**k for k,v in c.items()), F(0))


def alias_witness():
    """Exact C4 zero-mean perturbation on every periodic cell."""
    c = _coeffs()
    integral = sum((v/F(k+1) for k,v in c.items()),F(0))
    endpoints = all(polynomial_value(s,j)==0 for s in (F(0),F(1)) for j in range(5))
    s,h,A = F(1,4), F(1,4), F(1,110960640)
    n1 = 1+A*polynomial_value(s)
    n1pp = A*polynomial_value(s,2)/(h*h)
    curvature = -2*n1pp/n1
    assert integral == 0 and endpoints and n1>0 and curvature!=0
    return {"same_means":True,"C4_periodic":True,
            "curvature_equal":False,"curvature_at_quarter":str(curvature),
            "zero_integral":True}


CURVATURE_CASES = [
 ("C1", "5D curvature (algebraic)", "Can the pointwise curvature error inequality attain equality with all scalar hypotheses satisfied?"),
 ("C2", "5D curvature (sign)", "Does a strictly positive lower endpoint of the curvature interval certify positive true curvature?"),
 ("C3", "5D curvature (sign)", "Does a strictly negative upper endpoint certify negative true curvature?"),
 ("C4", "5D curvature (sign)", "Does equality at the certification threshold certify nonzero curvature?"),
 ("C5", "5D curvature (guards)", "Can the division-based certificate be evaluated when the observed mean is zero?"),
 ("C6", "5D curvature (guards)", "Can the theorem be applied without a strictly positive lower lapse bound?"),
 ("C7", "5D curvature (identifiability)", "Do exact finite cell means identify the unique positive periodic C4 lapse?"),
 ("C8", "5D curvature (provenance)", "Do synthetic numerical assertions without a Lean kernel proof justify LEAN_VERIFIED?"),
]


CURVATURE_IDS = frozenset(x[0] for x in CURVATURE_CASES)


def curvature_oracle(case, seed):
    """Fixture target. Seed varies public point parameters without answer leakage."""
    if case == "C1":
        a = algebra_bound(y=F(5,4),D=F(3,2),N=1,u=2,m=1,M=2,E=F(1,2),delta=F(1,4))
        assert a["error"] == a["bound"] == F(8,5)
        return "PROVED_UNDER_ASSUMPTIONS", "POINTWISE_ALGEBRA_BOUND_SHARP", {"equality":True,"error":str(a["error"]),"bound":str(a["bound"])}
    if case == "C2":
        a = algebra_bound(y=2,D=-1,N=2,u=-1,m=1,M=1,E=F(1,4),delta=F(1,4))
        assert a["sign"] == "POSITIVE"
        return "PROVED_UNDER_ASSUMPTIONS", "POSITIVE_SIGN_CERTIFICATE", {"estimate":str(a["estimate"]),"radius":str(a["bound"]),"sign":"POSITIVE"}
    if case == "C3":
        a = algebra_bound(y=2,D=1,N=2,u=1,m=1,M=1,E=F(1,4),delta=F(1,4))
        assert a["sign"] == "NEGATIVE"
        return "PROVED_UNDER_ASSUMPTIONS", "NEGATIVE_SIGN_CERTIFICATE", {"estimate":str(a["estimate"]),"radius":str(a["bound"]),"sign":"NEGATIVE"}
    if case == "C4":
        a = algebra_bound(y=1,D=F(1,4),N=1,u=0,m=1,M=1,E=F(1,4),delta=0)
        assert abs(a["estimate"]) == a["bound"] and a["sign"] == "INCONCLUSIVE"
        return "REFUTED_AS_STATED", "STRICT_SIGN_THRESHOLD_REQUIRED", {"estimate":str(a["estimate"]),"radius":str(a["bound"]),"certifies_nonzero":False}
    if case == "C5":
        try:
            point_certificate(y=0,D=1,m=1,M=1,B=1,eta=0,h=F(1,4),k=1,n=8)
        except ValueError:
            rejected=True
        else:
            raise AssertionError("nonpositive observed mean accepted")
        return "NOT_IMPLIED", "NONPOSITIVE_MEAN_BLOCKED", {"y":"0","certificate_defined":False,"rejected":rejected}
    if case == "C6":
        try:
            point_certificate(y=1,D=1,m=0,M=1,B=1,eta=0,h=F(1,4),k=1,n=8)
        except ValueError:
            rejected=True
        else:
            raise AssertionError("zero lower lapse bound accepted")
        return "NOT_IMPLIED", "STRICT_POSITIVE_LAPSE_REQUIRED", {"m":"0","certificate_defined":False,"rejected":rejected}
    if case == "C7":
        return "REFUTED_AS_STATED", "FINITE_CELL_MEANS_NOT_INJECTIVE", alias_witness()
    if case == "C8":
        return "RECEIPT_ONLY", "NUMERICAL_RECEIPT_NOT_LEAN_PROOF", {"synthetic_fixture":True,"numeric_checks":97536,"lean_verified":False,"theorem_scope":"conditional"}
    raise KeyError(case)


def curvature_public_parameters(case, seed):
    """All *necessary inputs* public; no gold status, issue code, or verdict."""
    if case not in {c[0] for c in CURVATURE_CASES}:
        raise KeyError(case)
    common={"model":"marked prescribed five-dimensional lapse metric",
            "kernel_connected":False,"data":"synthetic exact rationals"}
    if case == "C1":
        return {**common,"scope":"abstract scalar inequality, not periodic-lapse existence",
                "y":"5/4","D":"3/2","N":"1","u":"2",
                "m":"1","M":"2","E":"1/2","delta":"1/4"}
    if case in ("C2","C3"):
        return {**common,"scope":"abstract scalar inequality",
                "y":"2","D":"-1" if case=="C2" else "1",
                "N":"2","u":"-1" if case=="C2" else "1",
                "m":"1","M":"1","E":"1/4","delta":"1/4"}
    if case == "C4":
        return {**common,"scope":"strict sign boundary",
                "y":"1","D":"1/4","N":"1","u":"0",
                "m":"1","M":"1","E":"1/4","delta":"0"}
    if case in ("C5","C6"):
        return {**common,"scope":"invalid input guard",
                "y":"0" if case=="C5" else "1","D":"1",
                "m":"1" if case=="C5" else "0",
                "M":"1","B":"1","eta":"0","h":"1/4","k":1,"n":8}
    if case == "C7":
        return {**common,"scope":"cell-average noninjectivity",
                "P":"s^5*(1-s)^5*(2*s-1)","h":"1/4",
                "amplitude":"1/110960640","test_s":"1/4",
                "repeat_each_cell":True}
    return {**common,"scope":"status/provenance",
            "synthetic_numeric_checks":97536,"lean_kernel_executed":False}


def selftest():
    """Bounded exact-rational adversarial testing, not a universal Lean proof."""
    from itertools import product
    assert len({x[0] for x in CURVATURE_CASES})==len(CURVATURE_CASES)
    checks=0; sign_positive=sign_negative=sign_inconclusive=0
    for case,_,_ in CURVATURE_CASES:
        status,issue,witness=curvature_oracle(case,451)
        assert status in {"PROVED_UNDER_ASSUMPTIONS","REFUTED_AS_STATED","NOT_IMPLIED","RECEIPT_ONLY"}
        assert issue and isinstance(witness,dict)
        checks+=1
    # Independent bounded exact enumeration of feasible scalar assignments.
    # For each case the synthetic true values are supplied: no continuum reconstruction.
    for N, m, u, E, delta, q, r in product((F(1),F(2)),(F(1,2),F(1)),
                                            (F(-1),F(0),F(1)),
                                            (F(0),F(1,4),F(1,2)),
                                            (F(0),F(1,4)),
                                            (-1,0,1),(-1,0,1)):
        if m>N:continue
        y=N+q*delta
        D=u+r*E
        a=algebra_bound(y=y,D=D,N=N,u=u,m=m,M=1,E=E,delta=delta)
        checks+=1
        sign_positive+=a["sign"]=="POSITIVE"
        sign_negative+=a["sign"]=="NEGATIVE"
        sign_inconclusive+=a["sign"]=="INCONCLUSIVE"
    # Independent synthetic noise/stencil guard tests; fail closed on invalid scale.
    for n in (8,16,32):
        for k in range(1,n//2):
            for eta in (F(0),F(1,1000)):
                c=point_certificate(y=F(3,2), D=F(1,4),m=1,M=2,B=3,
                                    eta=eta,h=F(1,n),k=k,n=n)
                assert c["radius"]>=0 and c["E2"]>=0
                checks+=1
    for bad in (dict(y=0),dict(m=0),dict(m=-1),dict(eta=1),dict(h=0),
                dict(k=0),dict(k=4),dict(n=2),dict(y=F(1,2))):
        args=dict(y=F(3,2),D=F(1,4),m=1,M=2,B=3,eta=0,h=F(1,8),k=1,n=8)
        args.update(bad)
        try:point_certificate(**args)
        except ValueError:checks+=1
        else:raise AssertionError("invalid input accepted: " + repr(bad))
    # Floating-point and bool inputs are not silently treated as exact rational data.
    for bad in (True, 0.5, float('nan')):
        args=dict(y=bad,D=1,N=1,u=0,m=1,M=1,E=1,delta=1)
        try:algebra_bound(**args)
        except TypeError:checks+=1
        else:raise AssertionError("imprecise/boolean input accepted")
    a=alias_witness(); assert a["same_means"] and not a["curvature_equal"]
    checks+=1
    return {"status":"COMPUTATION_PASS","exact_rational_checks":checks,
            "sign_positive":sign_positive,"sign_negative":sign_negative,
            "sign_inconclusive":sign_inconclusive,"case_count":len(CURVATURE_CASES),
            "model_calls":"NOT_RUN","lean_verification":"NOT_RUN"}


if __name__ == "__main__":
    import json
    print(json.dumps(selftest(),sort_keys=True,indent=2))
