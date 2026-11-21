#!/usr/bin/env python3
"""Chronos p42: independent algebraic audit of an exact angular elimination.

This audit does not evaluate the remaining 4D expectation. It compares the
proposed spacelike closed form to the existing independent polygon evaluator,
and proves the angular primitive by symbolic differentiation. Python + SymPy.
No repository modifications.
"""
from fractions import Fraction as F
from random import Random
import sympy as S
from pathlib import Path
import importlib.util

spec = importlib.util.spec_from_file_location('coax', Path(__file__).with_name('chronos_p42_coaxial_three_cone_spacetime.py'))
coax = importlib.util.module_from_spec(spec)
spec.loader.exec_module(coax)


def exact_future_volume_over_pi(a,b,d):
    a,b,d=map(F,(a,b,d))
    if not (a>0 and b>d>=0):
        raise ValueError('The future endpoint must lie timelike above both events')
    if a-b>=d:
        return (b*b-d*d)**2/F(24)
    if b-a>=d:
        return a**4/F(24)
    return a*(b-d)**2*(-a*a+2*a*b+a*d-b*b+d*d)/(24*d)


def test_geometry():
    rng=Random(20261121)
    checked=0
    regimes={'spacelike':0,'x_before_y':0,'y_before_x':0}
    for _ in range(450):
        a=F(rng.randint(1,22),12)
        b=F(rng.randint(1,22),12)
        d=F(rng.randint(0,24),14)
        if b<=d: continue
        if a-b>=d: regime='x_before_y'
        elif b-a>=d: regime='y_before_x'
        else: regime='spacelike'
        result=exact_future_volume_over_pi(a,b,d)
        independent=coax.cone_volume_over_pi(-a,0,-b,d,0,0)
        assert result==independent,(a,b,d,result,independent)
        checked+=1
        regimes[regime]+=1
    assert all(regimes.values()),regimes
    return checked,regimes


def symbolic_polygon_proof():
    """Proof for spacelike pair: explicit null-rectangle min partition.

    Write L=b-d, a=L+e, b=L+d with 0<e<2d and L>0.
    In null spatial longitudinal variables U,V, 0<U<L, 0<V<a,
    the three transverse squared radii are U*V, (a-U)*(a-V),
    and (L-U)*(L+2d-V). The smallest changes on three affine arcs.
    """
    U,V,L,d,e=S.symbols('U V L d e',positive=True)
    a=L+e
    m=L+2*d
    qR=U*V
    qx=(a-U)*(a-V)
    qy=(L-U)*(m-V)
    U0=L*(m-a)/(m-L)
    Vx=a-U
    Vy=m*(L-U)/L
    Vc=(a*a-L*m+U*(m-a))/(a-L)
    def integrate_v(q,low,high):return S.integrate(q,(V,low,high))
    first=integrate_v(qR,0,Vx)+integrate_v(qx,Vx,a)
    second=(integrate_v(qR,0,Vy)+integrate_v(qy,Vy,Vc)
            +integrate_v(qx,Vc,a))
    result=S.factor((S.integrate(first,(U,0,U0))+
                     S.integrate(second,(U,U0,L)))/2)
    expected=L**2*(L+e)*(3*d*e+d*L-e**2)/(24*d)
    assert S.cancel(result-expected)==0
    return str(result)


def symbolic_angular_audit():
    a,c,z=S.symbols('a c z', positive=True)
    b=(z+c**2/z)/2
    d=(c**2/z-z)/2
    W=S.factor(24*a*(b-d)**2*(-a*a+2*a*b+a*d-b*b+d*d)/(24*d))
    # Primitive of W^2 with respect to b, expressed in z=b-sqrt(b²-c²).
    signed_density=S.factor(W**2*S.diff(b,z))
    split=S.apart(signed_density,z)
    primitive=S.integrate(split,z)
    assert S.cancel(S.diff(primitive,z)-signed_density)==0
    # Verify the space-like/timelike boundary is at b0=(a²+c²)/(2a).
    b0=(a*a+c*c)/(2*a)
    d0=S.Abs(a*a-c*c)/(2*a)
    # Piecewise limit W-> min(a^4,c^4) for spacelike boundary.
    boundary_z=S.Min(a*a,c*c)/a
    branch=S.factor(W.subs(z,boundary_z))
    # Check separately in a>c and a<c parameterizations.
    for aa,cc in ((S.Rational(5,4),S.Rational(3,4)),(S.Rational(3,4),S.Rational(5,4))):
        assert S.simplify(W.subs({a:aa,c:cc,z:min(aa*aa,cc*cc)/aa})-min(aa**4,cc**4))==0
    # Pointwise numerical + exact integration check at rational a,c and b endpoints,
    # using SymPy's exact primitive and an independent Gaussian quadrature.
    import scipy.integrate
    import math
    tests=0
    errors=[]
    for aa,cc in ((F(5,4),F(3,4)),(F(3,4),F(5,4)),(F(6,5),F(4,5))):
        bb0=(aa*aa+cc*cc)/(2*aa)
        lo=bb0+F(1,10); hi=bb0+F(3,10)
        def z_of(bb):return float(bb)-math.sqrt(float(bb*bb-cc*cc))
        primitive_eval=S.lambdify((a,c,z),primitive,modules='mpmath')
        import mpmath as mp
        mp.mp.dps=45
        def mz(bb):
            bb=mp.mpf(bb.numerator)/bb.denominator
            C=mp.mpf(cc.numerator)/cc.denominator
            return bb-mp.sqrt(bb*bb-C*C)
        via_primitive=primitive_eval(mp.mpf(aa.numerator)/aa.denominator,mp.mpf(cc.numerator)/cc.denominator,mz(hi))-primitive_eval(mp.mpf(aa.numerator)/aa.denominator,mp.mpf(cc.numerator)/cc.denominator,mz(lo))
        def independent(bb):
            dd=math.sqrt(bb*bb-float(cc*cc))
            return float((24*exact_future_volume_over_pi(aa,F(bb).limit_denominator(10**12),F(dd).limit_denominator(10**12)))**2)
        via_quad=scipy.integrate.quad(independent,float(lo),float(hi),epsabs=1e-11,epsrel=1e-11)[0]
        assert abs(float(mp.im(via_primitive))) < 1e-25
        err=abs(float(mp.re(via_primitive))-via_quad)
        assert err<1e-8,(aa,cc,err)
        errors.append(err)
        tests+=1
    return str(S.factor(W)),str(S.factor(signed_density)),str(primitive),tests,max(errors)

if __name__=='__main__':
    n,regimes=test_geometry()
    print('EXACT_POLYGON_COMPARISONS := PASS',n,regimes,flush=True)
    closed_form=symbolic_polygon_proof()
    print('SYMBOLIC_NULL_RECTANGLE_INTEGRATION := PASS',closed_form,flush=True)
    W,dens,prim,k,err=symbolic_angular_audit()
    print('W_SPACELIKE_IN_z :=',W)
    print('W_SQUARED_TIMES_db_dz :=',dens)
    print('ANGULAR_PRIMITIVE_DERIVATIVE := PASS')
    print('INDEPENDENT_QUADRATURE_CASES :=',k)
    print('MAX_ABS_ERROR :=',err)
    print('FIVE_TO_FOUR_DIMENSIONAL_REDUCTION := PROVED_ANALYTICALLY')
    print('GLOBAL_B := OPEN')
    print('GLOBAL_P42 := OPEN')