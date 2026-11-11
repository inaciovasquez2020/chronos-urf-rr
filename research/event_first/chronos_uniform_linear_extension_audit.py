import math,random
from functools import lru_cache

def points(n,rng):
 z=[]
 for _ in range(n):
  a=1-rng.random()**.25;t=a if rng.random()<.5 else -a
  r=(1-a)*rng.random()**(1/3)
  g=[rng.gauss(0,1) for _ in range(3)]; norm=math.sqrt(sum(x*x for x in g));z.append((t,*(r*x/norm for x in g)))
 return sorted(z)
def masks(z):
 p=[0]*len(z)
 for j in range(len(z)):
  for i in range(j):
   dt=z[j][0]-z[i][0]
   if dt*dt>sum((z[j][k]-z[i][k])**2 for k in range(1,4)):p[j]|=1<<i
 return p
def calc(p):
 n=len(p);whole=(1<<n)-1
 @lru_cache(None)
 def e(m):
  if m==whole:return 1
  return sum(e(m|1<<v) for v in range(n) if not (m>>v&1) and not(p[v]&~m))
 total=e(0);pair=0;three=0
 def rec(m,path):
  nonlocal pair,three
  if len(path)==3:return
  for v in range(n):
   if (m>>v&1) or (p[v]&~m):continue
   nex=path+(v,); nm=m|1<<v
   if len(nex)==2 and (p[v]>>path[0]&1):pair+=e(nm)
   if len(nex)==3 and (p[nex[1]]>>nex[0]&1) and (p[v]>>nex[1]&1):three+=e(nm)
   rec(nm,nex)
 rec(0,())
 op=sum(x.bit_count() for x in p)/math.comb(n,2)
 ot=sum(1 for k in range(n) for j in range(k) for i in range(j) if p[j]>>i&1 and p[k]>>j&1)/math.comb(n,3)
 return (pair/total,three/total,op,ot)
rng=random.Random(20261111)
for n,reps in [(8,80),(12,80),(16,80)]:
 v=[calc(masks(points(n,rng))) for _ in range(reps)]
 print(n,reps,tuple(round(sum(z[i] for z in v)/reps,6) for i in range(4)),flush=True)

# Deterministic counterexample to passage of full-sample limits to prefix limits.
# P_N is an ordinal sum of a chain of floor(sqrt(N)) events and an antichain.
for N in (100, 10000, 1000000):
    m=math.isqrt(N)
    assert m>=2
    # First two elements of EVERY natural linear extension form a chain.
    first_two_chain=1
    # In the full finite order, comparable pairs consist of chain-chain
    # and chain-antichain pairs, but no antichain-antichain pairs.
    full_pair=(math.comb(m,2)+m*(N-m))/math.comb(N,2)
    print('ORDINAL_SUM_COUNTEREXAMPLE',N,'prefix_pair',first_two_chain,
          'full_pair',round(full_pair,8))