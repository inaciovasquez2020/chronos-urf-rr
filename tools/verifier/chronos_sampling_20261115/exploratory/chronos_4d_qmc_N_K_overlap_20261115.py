#!/usr/bin/env python3
"""QMC 4D causal diamond four-point posets; numerical evidence, NOT exact integral proof."""
import numpy as np
from scipy.stats import qmc
from itertools import combinations, permutations
from fractions import Fraction as F
import argparse

def one_replicate(seed, power):
    raw=qmc.Sobol(d=16,scramble=True,seed=seed).random_base2(power).reshape(-1,4,4)
    q=raw[:,:,0]
    t=np.where(q<.5, .5*np.power(2*q,.25),1-.5*np.power(2*(1-q),.25))
    r=np.minimum(t,1-t)*np.cbrt(raw[:,:,1]); c=2*raw[:,:,2]-1; a=2*np.pi*raw[:,:,3]
    v=np.stack((r*np.sqrt(1-c*c)*np.cos(a),r*np.sqrt(1-c*c)*np.sin(a),r*c),axis=2)
    dt=t[:,:,None]-t[:,None,:]
    dx=np.linalg.norm(v[:,:,None,:]-v[:,None,:,:],axis=-1)
    rel=dt>dx
    # rel[:,b,c] is c < b. Define order matrix le[:,i,j]: i < j.
    le=rel.transpose(0,2,1)
    K=np.zeros(len(raw),dtype=bool)
    cross=np.zeros(len(raw),dtype=bool)
    for bottom in combinations(range(4),2):
        top=tuple(x for x in range(4) if x not in bottom)
        allbelow=le[:,bottom[0],top[0]]&le[:,bottom[0],top[1]]&le[:,bottom[1],top[0]]&le[:,bottom[1],top[1]]
        cross |= allbelow
        K |= allbelow & ~le[:,bottom[0],bottom[1]] & ~le[:,bottom[1],bottom[0]] & ~le[:,top[0],top[1]] & ~le[:,top[1],top[0]]
    N=np.zeros(len(raw),dtype=bool)
    nassign=np.zeros(len(raw),dtype=np.uint8)
    for a,b,c,d in permutations(range(4)):
        test=(le[:,a,b]&le[:,c,b]&le[:,c,d]&
              ~le[:,a,c]&~le[:,c,a]&~le[:,a,d]&~le[:,d,a]&~le[:,b,d]&~le[:,d,b])
        N |= test
        nassign+=test
    assert np.max(nassign)<=1
    assert not np.any(K & N)
    eJ2=np.mean(cross)/6
    return float(np.mean(K)),float(np.mean(N)),float(eJ2),float(np.mean(N+4*K)),float(np.mean(cross))

if __name__=='__main__':
    pa=argparse.ArgumentParser(); pa.add_argument('--power',type=int,default=17); pa.add_argument('--reps',type=int,default=8);args=pa.parse_args()
    data=np.array([one_replicate(20261115+113*i,args.power) for i in range(args.reps)])
    print('REPLICATES',args.reps,'SAMPLES_PER_REPLICATE',2**args.power,'TOTAL',args.reps*2**args.power)
    for i,name in enumerate(['K22','N4','EJ2','N+4K','CUT']):
        print(name,'estimate',f'{data[:,i].mean():.11g}', 'REPLICATE_SD',f'{data[:,i].std(ddof=1):.4g}', 'REPLICATE_SE',f'{data[:,i].std(ddof=1)/np.sqrt(args.reps):.4g}')
    print('N+4K EXACT',float(F(121,4900)))
    print('IDENTITY_EMPIRICAL_RESIDUAL',float(np.mean(data[:,1]+4*data[:,0])-F(121,4900)))
    print('ESTIMATED_p42',float(F(3557,42000))+1.2*data[:,2].mean())
    print('STATUS := QMC_ESTIMATE_NOT_PROOF')
