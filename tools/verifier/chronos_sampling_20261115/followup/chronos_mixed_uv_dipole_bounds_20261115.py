#!/usr/bin/env python3
"""Rational two-sided p42 enclosure replacing old dipole compression with dense U,V compression.
Dependent on archived 4-point identity, l0 result, higher ell one-variable compressions
and b_l formulas. Outputs rational floor/ceiling, does not solve exact p42.
"""
from fractions import Fraction as F
from math import factorial
import importlib.util, contextlib, io
from chronos_mixed_uv_dipole_exact_20261115 import gram,energy
from sympy import Matrix,Rational

def import_quiet(path, name):
    spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):spec.loader.exec_module(mod)
    return mod
m=import_quiet('/mnt/data/chronos_two_sided_harmonic_trace_certificate_20261115.py','old')

def mixed_compression(mons):
    G=Matrix([[gram(*x,*y) for y in mons] for x in mons]);B=Matrix([[energy(*x,*y) for y in mons] for x in mons])
    X=G.inv()*B
    t=F(str(X.trace()));s=F(str((X*X).trace()))
    return t,s

lowbase=F(3557,42000)+F(6,5)*F(513,875875)
Rhi=m.R_hi
for degree,mons in [(1,((0,0),(1,0),(0,1))), (2,((0,0),(1,0),(0,1),(2,0),(1,1),(0,2)))]:
    t,s=mixed_compression(mons)
    blo,bhi=m.bounds[0]
    assert 0<t<blo
    Jlo=F(513,875875)+3*s
    Jhi=F(513,875875)+3*(s+bhi*bhi-t*t)+Rhi*Rhi/13
    for ell,(bmin,bmax) in enumerate(m.bounds[1:],start=2):
        tk,sk=m.compression(ell,8)
        assert 0<tk<bmin
        Jlo+=(2*ell+1)*sk
        Jhi+=(2*ell+1)*(sk+bmax*bmax-tk*tk)
    lo=F(3557,42000)+F(6,5)*Jlo
    hi=F(3557,42000)+F(6,5)*Jhi
    assert lo<hi
    print('DEGREE',degree,'DIM',len(mons))
    print('T_RATIONAL',t,'S_RATIONAL',s)
    print('CERTIFIED_LOWER_DECIMAL',format(float(lo),'.15g'))
    print('CERTIFIED_UPPER_DECIMAL',format(float(hi),'.15g'))
    print('WIDTH_DECIMAL',format(float(hi-lo),'.15g'))
    print('OLD_U_ONLY_CERTIFIED_LOWER_DECIMAL',format(float(m.prev_lower),'.15g'))
    print('OLD_U_ONLY_CERTIFIED_UPPER_DECIMAL',format(float(m.prev_upper),'.15g'))
    assert lo>m.prev_lower and hi<m.prev_upper
    if degree==2:
        assert lo>F(854106288,10**10)  # 0.0854106288
        assert hi<F(854289315,10**10)  # 0.0854289315
        print('STRICT_RATIONAL_ENCLOSURE := 0.0854106288 < p42 < 0.0854289315')
print('MIXED_BIVARIATE_BOUNDS := PASS')
print('FULL_EXACT_P42 := OPEN')