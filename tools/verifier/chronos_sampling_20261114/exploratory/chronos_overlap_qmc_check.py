#!/usr/bin/env python3
"""4D diamond: QMC estimate of crossing-cut probability; no exact-integration claim."""
import numpy as np
from scipy.stats import qmc
from itertools import combinations
NPOWER=16
pairs=list(combinations(range(4),2))
res=[];bs=[]
for rep in range(8):
    raw=qmc.Sobol(d=16,scramble=True,seed=20261114+rep).random_base2(NPOWER).reshape(-1,4,4)
    q=raw[:,:,0]
    t=np.where(q<.5,.5*np.power(2*q,.25),1-.5*np.power(2*(1-q),.25))
    h=np.minimum(t,1-t)
    r=h*np.cbrt(raw[:,:,1]); c=2*raw[:,:,2]-1; a=2*np.pi*raw[:,:,3]
    v=np.stack((r*np.sqrt(1-c*c)*np.cos(a),r*np.sqrt(1-c*c)*np.sin(a),r*c),axis=2)
    dt=t[:,:,None]-t[:,None,:]; dx=np.linalg.norm(v[:,:,None,:]-v[:,None,:,:],axis=-1)
    adj=dt>dx
    cuts=np.zeros(len(raw),dtype=np.int8); bottom=np.zeros(len(raw),dtype=np.int8)
    for s in pairs:
        top=[z for z in range(4) if z not in s]
        yes=adj[:,s[0],top[0]] & adj[:,s[0],top[1]] & adj[:,s[1],top[0]] & adj[:,s[1],top[1]]
        cuts+=yes
        bottom+=yes & (adj[:,s[0],s[1]]|adj[:,s[1],s[0]])
    assert np.max(cuts)<=1 and np.max(bottom)<=1
    res.append(float(cuts.mean()))
    bs.append(float((cuts-bottom).mean()))
print('N_each',2**NPOWER,'replicates',8)
print('Pr(cut):',res,'mean',np.mean(res),'sd',np.std(res,ddof=1))
print('Pr(bottom antichain cut):',bs,'mean',np.mean(bs))
print('E[J_+^2] estimate',np.mean(res)/6)
print('Known exact bottom comparable cut',1/2940,'observed',np.mean(res)-np.mean(bs))
print('STATUS COMPUTATION_PASS_QMC_ONLY')
