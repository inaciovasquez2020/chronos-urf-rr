#!/usr/bin/env python3
"""Read-only exact linear-extension-weight audit; geometry sampled by deterministic RNG."""
import sys, math, random, statistics
from fractions import Fraction
from functools import lru_cache
MAX_STATES=150000
sys.path.insert(0,'/mnt/data')
def sprinkle(n,rng):
    points=[]
    for _ in range(n):
        a=1-rng.random()**.25
        t=a*(1 if rng.random()<.5 else -1)
        r=(1-a)*rng.random()**(1/3)
        v=[rng.gauss(0,1) for _ in range(3)]
        norm=math.sqrt(sum(z*z for z in v))
        points.append((t,*(r*z/norm for z in v)))
    points.sort()
    preds=[]
    for j,y in enumerate(points):
        mask=0
        for i,x in enumerate(points[:j]):
            if (y[0]-x[0])**2>sum((y[q]-x[q])**2 for q in range(1,4)):
                mask|=1<<i
        preds.append(mask)
    return points,preds

def prefix_weights(pred,n):
    N=len(pred);top=(1<<N)-1
    @lru_cache(None)
    def E(mask):
        if E.cache_info().currsize>MAX_STATES:raise RuntimeError('STATE_GUARD')
        if mask==top:return 1
        return sum(E(mask|1<<j) for j in range(N) if not(mask>>j&1) and not(pred[j]&~mask))
    total=E(0)
    F={0:1}
    for _ in range(n):
        nxt={}
        for mask,c in F.items():
            for j in range(N):
                if not(mask>>j&1) and not(pred[j]&~mask):
                    new=mask|1<<j
                    nxt[new]=nxt.get(new,0)+c
        F=nxt
    assert sum(c*E(mask) for mask,c in F.items())==total
    counts=[0]*N
    for mask,c in F.items():
        w=c*E(mask)
        for j in range(N):
            if mask>>j&1: counts[j]+=w
    return [Fraction(x,total) for x in counts],len(F),E.cache_info().currsize

def test():
    rng=random.Random(SEED);start=time.monotonic()
    for N,reps in SIZES:
        for alpha in ALPHAS:
            n=round(alpha*N)
            if not (2<=n<N):continue
            vals=[]; mvals=[]; states=[]
            for iteration in range(reps):
                if time.monotonic()-start>MAX_SEC:
                    print('INCOMPLETE_TIMEOUT',N,alpha,iteration,flush=True);return
                pts,pred=sprinkle(N,rng)
                try: ranks,_,state=prefix_weights(pred,n)
                except RuntimeError:
                    print('INCOMPLETE_STATE_GUARD',N,alpha,iteration,flush=True);return
                s=(n/N)**.25
                apex=-1+2*s
                A=[j for j,x in enumerate(pts) if x[0]<apex and
                   sum(z*z for z in x[1:])<(apex-x[0])**2]
                expected=sum(1-ranks[j] if j in A else ranks[j] for j in range(N))
                vals.append(float(expected/n));mvals.append(len(A));states.append(state)
            mean=statistics.mean(vals);se=statistics.stdev(vals)/math.sqrt(reps)
            print('N',N,'n',n,'reps',reps,'mismatch_over_n',round(mean,6),
                  'SE',round(se,6),'mean_diamond_count',round(statistics.mean(mvals),3),
                  'max_states',max(states),flush=True)


rng=random.Random(20261111)
for N,reps in [(8,120),(12,120),(16,100)]:
 for frac in (0.25,0.50,0.75):
  n=round(N*frac)
  if not 2<=n<N: continue
  data=[]; fixed_data=[]; refinements=[]; polarized=[]
  for _ in range(reps):
   pts,pred=sprinkle(N,rng)
   q,*_=prefix_weights(pred,n)
   # Threshold set is an ideal (including ties) for every natural-extension distribution.
   threshold=[i for i,x in enumerate(q) if x>Fraction(1,2)]
   assert all((pred[i] & ~sum(1<<j for j in threshold))==0 for i in threshold)
   opt=sum(min(x,1-x) for x in q)
   fixed=2*(n-sum(sorted(q,reverse=True)[:n]))
   assert opt<=fixed
   root=-1+2*(n/N)**.25
   geo=[i for i,x in enumerate(pts) if x[0]<root and sum(z*z for z in x[1:])<(root-x[0])**2]
   geom=sum(1-q[i] if i in geo else q[i] for i in range(N))
   assert opt<=geom
   data.append(float(opt/n));fixed_data.append(float(fixed/n));refinements.append(float(geom/n));polarized.append(len(threshold)/n)
  print('N=%d n=%d reps=%d opt=%.6f fixed_n_opt=%.6f geo=%.6f threshold_size/n=%.6f optSE=%.5f' %(N,n,reps,statistics.mean(data),statistics.mean(fixed_data),statistics.mean(refinements),statistics.mean(polarized),statistics.stdev(data)/math.sqrt(reps)),flush=True)