#!/usr/bin/env python3
"""Independent finite four-event 4D Minkowski prefix audit; QMC is not proof."""
import itertools
import numpy as np
from scipy.stats import qmc

PERMS=list(itertools.permutations(range(4)))
PAIRS=list(itertools.permutations(range(4),2))
lookup=np.full(1<<12,np.nan)
for mask in range(1<<12):
    adj=np.zeros((4,4),dtype=bool)
    for k,(i,j) in enumerate(PAIRS): adj[i,j]=bool((mask>>k)&1)
    if np.any(adj&adj.T): continue
    valid=[perm for perm in PERMS if all(not adj[perm[j],perm[i]] for i in range(4) for j in range(i+1,4))]
    if valid: lookup[mask]=sum(adj[p[0],p[1]] for p in valid)/len(valid)

# Sobol scrambled replicates, within-replicate standard deviation is descriptive only.
for exponent in (14,17):
    estimates=[]; fraction_of_orders=[]
    for seed in range(8):
        raw=qmc.Sobol(d=16,scramble=True,seed=20261114+seed).random_base2(exponent).reshape(-1,4,4)
        q=raw[:,:,0]
        t=np.where(q<.5,.5*np.power(2*q,.25),1-.5*np.power(2*(1-q),.25))
        h=np.minimum(t,1-t)
        r=h*np.cbrt(raw[:,:,1]); c=2*raw[:,:,2]-1; a=2*np.pi*raw[:,:,3]
        v=np.stack((r*np.sqrt(1-c*c)*np.cos(a),r*np.sqrt(1-c*c)*np.sin(a),r*c),axis=2)
        dt=t[:,:,None]-t[:,None,:]
        dx=np.linalg.norm(v[:,:,None,:]-v[:,None,:,:],axis=-1)
        adj=(dt>dx)
        mask=np.zeros(len(raw),dtype=np.int32)
        for k,(i,j) in enumerate(PAIRS): mask|=adj[:,i,j].astype(np.int32)<<k
        val=lookup[mask]
        assert np.isfinite(val).all()
        estimates.append(float(np.mean(val)))
        fraction_of_orders.append(float(np.mean(np.sum(adj,axis=(1,2)))/6))
    print('2^',exponent,'REPLICATES',len(estimates),'TOTAL',8*2**exponent)
    print('PREFIX_P',estimates,'MEAN',float(np.mean(estimates)),'REPLICA_SD',float(np.std(estimates,ddof=1)))
    print('FULL_PAIR',fraction_of_orders,'MEAN',float(np.mean(fraction_of_orders)))
    print('BOUNDS',157/2100,1303/14700)
    assert min(estimates)>157/2100 and max(estimates)<1303/14700
print('STATUS := COMPUTATION_PASS; NOT_A_PROOF_OF_EXACT_VALUE_OR_LIMIT')
