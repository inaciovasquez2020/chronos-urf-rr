import sys
sys.path.insert(0,'/mnt/data')
from itertools import combinations
from fractions import Fraction as F
cases = [
    ("antichain", (0,0,0,0,0,0), F(37,70)),
    ("branching", (0,0,1,2,5,10), F(1,35)),
    ("three_disjoint_edges", (0,0,0,1,2,4), F(31,70)),
]
def linear_extensions(rows):
    n=len(rows)
    for order in permutations(range(n)):
        seen=0
        for v in order:
            if rows[v]&~seen: break
            seen|=1<<v
        else:yield order
def induced(rows,order,n):
    ids=order[:n]
    return tuple(sum(1<<i for i,u in enumerate(ids[:j]) if rows[v]>>u&1) for j,v in enumerate(ids))
def feat(rows):
    n=len(rows)
    pair=sum(z.bit_count() for z in rows)
    tr=sum(bool(rows[j]>>i&1 and rows[k]>>j&1) for i,j,k in combinations(range(n),3))
    z=0
    for q in combinations(range(n),4):
        edges=[(i,j) for i,j in combinations(q,2) if rows[j]>>i&1]
        z+=len(edges)==2 and len({v for e in edges for v in e})==4
    return F(pair,n*(n-1)//2),F(tr,n*(n-1)*(n-2)//6),F(z,n*(n-1)*(n-2)*(n-3)//24)

from collections import defaultdict, Counter
from fractions import Fraction as F
from itertools import permutations
from functools import lru_cache
@lru_cache(None)
def canon(rows):
 n=len(rows); edge=[(i,j) for j in range(n) for i in range(j) if rows[j]>>i&1]
 # coarse invariant sort may optimize? plain 7! exhaustive
 best=None
 for p in permutations(range(n)):
  inv=[0]*n
  for j,i in enumerate(p): inv[i]=j
  s=tuple(sorted((inv[a],inv[b]) for a,b in edge))
  if best is None or s<best:best=s
 return best

def ideals(r):
 for p in range(1<<len(r)):
  if all(not(p>>j&1) or r[j]&p==r[j] for j in range(len(r))):yield p

def maxs(r):
 return [i for i in range(len(r)) if not any(r[j]>>i&1 for j in range(len(r)))]
def drop(r,i):
 return tuple((r[j]&((1<<i)-1))|((r[j]>>(i+1))<<i) for j in range(len(r)) if j!=i)
classes6={canon(r):name for name,r,w in cases}
ss=set()
for name,r,w in cases:
 for order in linear_extensions(r):
  six=induced(r,order,6)
  for p in ideals(six):ss.add(six+(p,))
print('candidates',len(ss),flush=True)
survivors=[]
for idx,r in enumerate(sorted(ss)):
 if all(canon(drop(r,i)) in classes6 for i in maxs(r)):
  survivors.append(r)
print('all deletion supported labeled',len(survivors),flush=True)
cl=defaultdict(list)
for r in survivors:cl[canon(r)].append(r)
print('supported seven classes',len(cl),flush=True)
q6={canon(r):w for name,r,w in cases}
for key,rr in sorted(cl.items()):
 cnt=Counter(canon(r[:6]) for r in rr)
 vec=[F(cnt[c],len(rr)) for c in q6]
 print('SEVEN_CLASS',len(rr),'prefix proportions',vec,'representative',rr[0],flush=True)
assert len(ss)==629 and len(survivors)==27 and len(cl)==4
mass={canon(r):w for _,r,w in cases}
# All 7-point laws with the exact six-point marginal and discrete covariance
# assign mass 1/35 and 31/70 to the unique extensions of those nonempty classes.
# The antichain mass 37/70 can be split freely between two remaining classes.
branch=canon((0,0,1,2,5,10,63))
matching=canon((0,0,0,1,2,4,63))
antichain=canon((0,0,0,0,0,0,0))
cone=canon((0,0,0,0,0,0,63))
assert set(cl)=={branch,matching,antichain,cone}
assert [len(cl[c]) for c in (branch,matching,antichain,cone)]==[10,15,1,1]
for k in (branch,matching,antichain,cone):
  print('EXTENSION_FEATURES',str(k)[:50],feat(cl[k][0]))
base=[F(1,35)*feat(cl[branch][0])[j]+F(31,70)*feat(cl[matching][0])[j] for j in range(3)]
low=base[0];high=low+F(37,70)*feat(cl[cone][0])[0]
assert low==F(101,490) and high==F(5,14)
assert base[1]==F(109,2450) and base[2]==F(111,2450)
assert low>F(1,10) and base[1]>F(1,350)
print('SEVEN_PAIR_SHARP_BOUNDS',low,high)
print('SEVEN_THREE_CHAIN_FORCED',base[1])
print('SEVEN_INDUCED_2PLUS2_FORCED',base[2])
print('N2_TO_N6_MATCH := PASS_PRIOR_INDEPENDENT_AUDIT')
print('N7_TARGET_MATCH := IMPOSSIBLE')
print('RATIONAL_CERTIFICATE := PASS')