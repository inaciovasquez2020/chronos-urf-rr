#!/usr/bin/env python3
"""Exact 4D p_(4,2) conditional enclosure with mixed ell=1,2,3, U-only ell=4,5.
The four-point reduction, angular HS masses, and zero-mode term remain hypotheses
of this computational certificate. All comparisons of endpoints use rational arithmetic.
"""
from fractions import Fraction as F
from sympy import Matrix
import contextlib,io,importlib.util,pathlib
HERE=pathlib.Path(__file__).resolve().parent

def load(name):
    spec=importlib.util.spec_from_file_location(name,HERE/(name+'.py'))
    mod=importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):spec.loader.exec_module(mod)
    return mod
old=load('chronos_two_sided_harmonic_trace_certificate_20261115')
modules={1:load('chronos_mixed_uv_dipole_exact_20261115'),2:load('chronos_mixed_uv_quadrupole_exact_20261115'),3:load('chronos_mixed_uv_octupole_exact_20261115')}
mons=((0,0),(1,0),(0,1),(2,0),(1,1),(0,2))
def compress(m):
    G=Matrix([[m.gram(*a,*b) for b in mons] for a in mons]); B=Matrix([[m.energy(*a,*b) for b in mons] for a in mons])
    assert G.det()!=0 and G==G.T and B==B.T
    X=G.inv()*B
    return F(str(X.trace())),F(str((X*X).trace()))

Jlo=old.A0;Jhi=old.A0+old.R_hi**2/13
for ell in range(1,6):
    t,s=compress(modules[ell]) if ell<=3 else old.compression(ell,8)
    blo,bhi=old.bounds[ell-1]
    assert 0<s<=t*t and t<blo
    Jlo+=(2*ell+1)*s
    Jhi+=(2*ell+1)*(s+bhi*bhi-t*t)
    print('MODE',ell,'TRACE_COMPRESSION',t,'SQUARE_TRACE',s,'T_DEC',format(float(t),'.15g'),'S_DEC',format(float(s),'.15g'),flush=True)
lo=old.base+F(6,5)*Jlo
hi=old.base+F(6,5)*Jhi
assert 0<lo<hi
assert lo>F('0.0854113582') and hi<F('0.0854281629')
print('LOW',format(float(lo),'.17g'))
print('HIGH',format(float(hi),'.17g'))
print('WIDTH',format(float(hi-lo),'.17g'))
print('EXACT_LOWER',lo)
print('EXACT_UPPER',hi)
print('RESULT := COMPUTATION_PASS; EXACT_P42 := OPEN; LEAN := NOT_RUN')