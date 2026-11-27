from fractions import Fraction as F
from math import factorial
from itertools import combinations, permutations

# Strict transitive relations respecting birth labels 0,1,2.
pairs=list(combinations(range(3),2))
classes={}
for mask in range(8):
    R=frozenset(e for j,e in enumerate(pairs) if mask>>j&1)
    if (0,1) in R and (1,2) in R and (0,2) not in R: continue
    key=min(tuple(sorted((p[a],p[b]) for a,b in R)) for p in permutations(range(3)))
    classes.setdefault(key,[]).append(R)
name=lambda R: {0:'A',1:'E',3:'C'}.get(len(R), 'V' if len({a for a,b in R})==1 else 'W')
weights={name(c[0]):F(sum((0,1) in R for R in c),len(c)) for c in classes.values()}
assert weights=={'A':0,'E':F(1,3),'V':1,'W':0,'C':1},weights
# Normalized null-coordinate integral in dimension four.
# E[J^s] = (d-1)/(s+1) Beta(ds/2+1,d-1).
d=4
def beta(a,b): return F(factorial(a-1)*factorial(b-1),factorial(a+b-1))
def moment(s): return F(d-1,s+1)*beta(d*s//2+1,d-1)
q2=2*moment(1); chain=3*moment(2)*q2; fork=3*moment(2)-chain
edge=3*q2-3*chain-4*fork
q={'A':1-chain-2*fork-edge,'E':edge,'V':fork,'W':fork,'C':chain}
assert q=={'A':F(53,70),'E':F(33,175),'V':F(9,350),'W':F(9,350),'C':F(1,350)}
def tv(p,q): return sum(abs(p[k]-q[k]) for k in p)/2
def prefix(p): return sum(weights[k]*p[k] for k in p)
delta=q2-prefix(q)
assert delta==F(3,350)
# Exact family of attainable error triples: x prefix deficit, y class TV,
# z deviation from uniform natural labels. x+y+z=delta.
# Shift y from A to C, then z inside E from a no-comparability label to yes.
checks=0
for denominator in range(1,101):
    for i in range(denominator+1):
        for j in range(denominator-i+1):
            x=delta*F(i,denominator);y=delta*F(j,denominator);z=delta-x-y
            p=q.copy();p['A']-=y;p['C']+=y
            assert min(p.values())>=0 and sum(p.values())==1
            assert tv(p,q)==y
            assert z<=p['E']/3 # available single donor presentation
            actual=prefix(p)+z
            assert q2-actual==x
            checks+=1
print('NATURAL_TRIPLE_PRESENTATIONS :=',sum(map(len,classes.values())))
print('UNLABELED_CLASSES :=',len(classes))
print('Q2 :=',q2,'Q3 :=',q)
print('Q3_NATURAL_PREFIX :=',prefix(q))
print('SHARP_TOTAL_ERROR :=',delta)
print('SHARP_TWO_ERROR_MINIMAX :=',delta/2)
print('SHARP_THREE_ERROR_MINIMAX :=',delta/3)
print('EXACT_TRADEOFF_CASES :=',checks)
print('COMPUTATION_PASS; LEAN_NOT_RUN; GLOBAL_EMERGENCE_OPEN')
