"""Exact integer enclosure of flat-limit projected comparable-pair probability.
No floating point arithmetic is used in the proof calculation. Requires NumPy.
"""
from math import isqrt
from fractions import Fraction as Q
import numpy as np

# Radial law proportional to u^2 sqrt(1-u^2) on [0,1].
# Integrate a rational lower/upper step function on a finer uniform mesh.
def radial_bounds(m, subdivisions=128, scale=10**9):
    B=m*subdivisions
    lo=[]; hi=[]
    for j in range(m):
        l=h=0
        for k in range(j*subdivisions,(j+1)*subdivisions):
            v0=isqrt((B*B-k*k)*scale*scale)
            v1=isqrt((B*B-(k+1)*(k+1))*scale*scale)
            l+=k*k*v1
            h+=(k+1)*(k+1)*(v0+1)
        lo.append(l); hi.append(h)
    # Shared factors B^-4 and scale^-1 cancel on normalization.
    return [(Q(l,sum(hi)),Q(h,sum(lo))) for l,h in zip(lo,hi)]

def bounds(n,m):
    if not (1 <= n <= 128 and 1 <= m <= 128 and (2*n*m)**2 <= 100_000_000):
        raise SystemExit("INCOMPLETE: resource guard")
    W=10**7; P=10**4
    rad=radial_bounds(m)
    # signed time bins [i/n,(i+1)/n], with the flat marginal density 5/2*(1-|s|)^4.
    # r=(1-|s|)*u; radius and time endpoints use common denominator n*m.
    tl=[]; th=[]; rl=[]; rh=[]; wl=[]; wh=[]
    for i in range(-n,n):
        l=n-max(abs(i),abs(i+1)); h=n-min(abs(i),abs(i+1))
        tw=Q(h**5-l**5,2*n**5)
        for j,(low,high) in enumerate(rad):
            tl.append(i*m); th.append((i+1)*m)
            rl.append(l*j); rh.append(h*(j+1))
            lo=tw*low*W; hi=tw*high*W
            wl.append(lo.numerator//lo.denominator)
            wh.append(-(-hi.numerator//hi.denominator))
    tl,th,rl,rh,wl,wh=map(lambda a:np.asarray(a,dtype=np.int64),(tl,th,rl,rh,wl,wh))
    assert int(wh.sum())**2*P < 2**63
    # prevent overflow in squared endpoints and scaled angular fractions
    assert (2*n*m)**2*P < 2**63
    lower=upper=0
    for k in range(len(tl)):
        dmin=np.maximum(0,np.maximum(tl[k]-th,tl-th[k])); dmax=np.maximum(th[k]-tl,th-tl[k])
        rmin=np.maximum(0,np.maximum(rl[k]-rh,rl-rh[k])); rmax=np.maximum(rh[k]-rl,rh-rl[k])
        ln=np.maximum(0,dmin*dmin-rmax*rmax)
        un=np.maximum(0,dmax*dmax-rmin*rmin)
        ld=4*rh[k]*rh; ud=4*rl[k]*rl
        low=np.minimum(P,(ln*P)//np.maximum(1,ld))
        high=np.where(ud==0,np.where(un==0,0,P),np.minimum(P,(un*P+np.maximum(1,ud)-1)//np.maximum(1,ud)))
        lower+=int(wl[k])*int(low@wl)
        upper+=int(wh[k])*int(high@wh)
    return Q(lower,W*W*P),Q(upper,W*W*P),len(tl)
if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument('--n',type=int,default=64); ap.add_argument('--m',type=int,default=48); args=ap.parse_args()
    lo,hi,count=bounds(args.n,args.m)
    print('CELLS :=',count,'ORDERED_PAIRS :=',count**2)
    print('LOWER :=',lo, float(lo)); print('UPPER :=',hi,float(hi))
    print('STRICT_BELOW_4D_FLAT :=', 'PASS' if hi<Q(1,10) else 'NOT_ESTABLISHED')
    print('STRICT_ABOVE_5D_FLAT :=', 'PASS' if lo>Q(128,3003) else 'NOT_ESTABLISHED')
    e=Q(1,50)
    A=lambda k: ((1-e)**(-k)+(1+e)**(-k))/2
    u=hi*A(10); l=Q(1,10)/A(6)**2
    print('EPS_MAX :=',e)
    print('PROJECTED_5D_UPPER :=',u,float(u))
    print('MATCHED_4D_LOWER :=',l,float(l))
    print('UNIFORM_SEPARATION :=', 'PASS' if u<l else 'NOT_ESTABLISHED')
    if not (hi<Q(1,10) and lo>Q(128,3003) and u<l):
        raise SystemExit('INCOMPLETE: target inequalities not certified')
