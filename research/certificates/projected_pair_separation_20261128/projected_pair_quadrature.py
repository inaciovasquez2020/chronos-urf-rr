import numpy as np
from scipy.special import roots_jacobi, roots_legendre

def rule(n,m,eps):
    t,wt=roots_legendre(n)
    s=np.concatenate(((t-1)/2,(t+1)/2))
    w=np.tile(wt/2,2)*(1-np.abs(s))**4/(1-eps*s)**5
    w/=w.sum()
    x,v=roots_jacobi(m,.5,.5)
    u=np.sqrt((x+1)/2); v/=v.sum()
    return np.repeat(s,m),((1-np.abs(s[:,None]))*u).ravel(),(w[:,None]*v).ravel()

def calc(n,m,e):
    t,r,w=rule(n,m,e); ans=0.
    for k in range(0,len(t),128):
        tt=t[k:k+128,None]-t[None,:]; rr=r[k:k+128,None]-r[None,:]
        p=np.clip((tt*tt-rr*rr)/(4*r[k:k+128,None]*r[None,:]),0,1)
        ans+=w[k:k+128]@(p@w)
    return ans
if __name__=='__main__':
    for n,m in [(12,12),(24,24),(48,32),(64,64)]:
        print(n,m,[(e,calc(n,m,e)) for e in (0,.25,.5)],flush=True)
