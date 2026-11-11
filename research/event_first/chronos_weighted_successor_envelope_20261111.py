#!/usr/bin/env python3
"""Geometry-weighted first birth envelope. Numeric is evidence, not proof.
Read-only; bounded Gauss-Legendre quadrature; fixed inputs; scipy/numpy existing environment.
"""
import numpy as np
from scipy.special import bdtr
from numpy.polynomial.legendre import leggauss
from math import sqrt, pi

def weighted_count(N,K,nodes=112):
    assert 1 <= K < N and N >= 4
    m=N-1
    # t=1-u, w; t in [0,1], 0<=w<=1-t; null-rim scales.
    vscale=sqrt(K/N)
    vmax=min(4.0,1.0/vscale)
    ymax=5.0
    xs,ws=leggauss(nodes)
    vs=(xs+1)*vmax/2
    weights_v=ws*vmax/2
    ys=(xs+1)*ymax/2
    weights_y=ws*ymax/2
    ans=0.0
    for v,wv in zip(vs,weights_v):
        t=v*vscale
        u=1-t
        # domain w<=u; y=w sqrt(N)
        yy=ys
        ww=yy/sqrt(N)
        good=ww<=u
        ss=(u*ww)**2
        ff=(t*(1-ww))**2
        aa=np.maximum(1-ss-ff,0)
        # conditional given minimal: V ~ bin(m, f/(1-s))
        pp=np.divide(ff,1-ss,out=np.zeros_like(ff),where=ss<1)
        cond0=bdtr(K,m,pp)
        cond1= m*pp*bdtr(K-1,m-1,pp)
        val=np.where(good, (1-ss)**m*(cond0+cond1),0)
        ans+=wv*np.dot(weights_y, 12*(u-ww)**2*val)
    # full expectation N*int dt dw = sqrt(K)*int dv dy
    return sqrt(K)*ans

def main():
    print('BOUNDARY_CUTOFFS := vmax=4, ymax=5; quadrature nodes=112')
    for N,K in [(3000,15),(10000,40),(30000,100),(100000,220)]:
        val=weighted_count(N,K)
        ratio=val/(K**1.5)
        print('N=',N,'K=',K,'EXPECTED_WEIGHTED_MINIMAL_COUNT=',format(val,'.9f'),
              'RATIO_TO_K_3_2=',format(ratio,'.9f'), 'LIMIT=',format(2*sqrt(pi),'.9f'),flush=True)
        assert 0<ratio<9
    print('WEIGHTED_ENVELOPE_NUMERIC := PASS')
    print('N_K_LIMIT := ANALYTICAL_CLAIM_REQUIRES_PROOF')
    print('ACTUAL_FIRST_BIRTH_LIMIT := OPEN')

if __name__=='__main__':main()
