#!/usr/bin/env python3
"""Rotational reduction of the 4D Minkowski-diamond future overlap.
Independent deterministic Sobol quadrature of conditional common-future fractions.
Not an exact evaluation of E[J_+^2] and not Lean verification.
"""
import numpy as np
from scipy.stats import qmc

def overlap_by_caps(t,r,s,q,c,m=17,seed=20261114):
    assert 0<=r<=min(t,1-t) and 0<=q<=min(s,1-s) and -1<=c<=1
    lo=max(t,s)
    if lo>=1: return 0.0
    z=qmc.Sobol(d=3,scramble=True,seed=seed).random_base2(m)
    tau=lo+(1-lo)*z[:,0]
    R=np.minimum(tau,1-tau)
    rho=R*np.cbrt(z[:,1])
    mu=2*z[:,2]-1
    # Spherical directions around the axis of the first point.
    # Handle zero radii with the exact angle-independent constraint.
    AX=np.where((tau-t)>=np.abs(rho-r), -np.inf, np.inf)
    if r>0:
        mask=rho>0
        AX[mask]=(rho[mask]**2+r*r-(tau[mask]-t)**2)/(2*rho[mask]*r)
    BX=np.where((tau-s)>=np.abs(rho-q), -np.inf, np.inf)
    if q>0:
        mask=rho>0
        BX[mask]=(rho[mask]**2+q*q-(tau[mask]-s)**2)/(2*rho[mask]*q)
    good=mu>=AX
    if q==0:
        fraction=(BX<=-1).astype(float)
    else:
        denom=np.sqrt(np.maximum(0,1-c*c))*np.sqrt(np.maximum(0,1-mu*mu))
        numer=BX-c*mu
        fraction=np.empty(len(mu))
        ok=denom>1e-14
        fraction[ok]=np.arccos(np.clip(numer[ok]/denom[ok],-1,1))/np.pi
        fraction[~ok]=(numer[~ok]<=0).astype(float)
    # Volume normalized by Vol(D)=pi/24. Sampling spherical volume uniform at each tau.
    # 4pi/3 R^3 * 24/pi = 32 R^3.
    return float((1-lo)*np.mean(32*R**3 * good*fraction))

if __name__=='__main__':
    for t,r,s,q,c in [(0,0,0,0,1),(.25,0,.25,0,1),(.1,0,.3,0,1),(.2,.1,.2,.1,1),(.2,.1,.2,.1,-1)]:
        out=overlap_by_caps(t,r,s,q,c)
        exact=None
        if r==0 and q==0: exact=(1-max(t,s))**4
        if t==s and r==q and c==1: exact=((1-t)**2-r*r)**2
        print('pair',t,r,s,q,c,'reduced J',round(out,8),'benchmark',exact,'abs_error',None if exact is None else abs(out-exact))
        if exact is not None: assert abs(out-exact)<0.003
    print('ROTATIONAL_REDUCTION_NUMERICAL_CHECK := PASS')
    print('EXACT_ENSEMBLE_OVERLAP_MOMENT := OPEN')
