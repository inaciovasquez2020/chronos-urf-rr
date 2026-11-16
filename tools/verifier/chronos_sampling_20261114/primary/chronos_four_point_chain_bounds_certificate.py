#!/usr/bin/env python3
"""Exact four-event prefix bounds from the 4D Minkowski three-event census.
Python 3 stdlib only; no repo writes, network, or floating-point arithmetic.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import combinations, permutations, product


def posets(n):
    pairs = list(combinations(range(n), 2))
    for states in product(range(3), repeat=len(pairs)):
        edges = {(a,b) for (a,b),st in zip(pairs,states) if st==1}
        edges |= {(b,a) for (a,b),st in zip(pairs,states) if st==2}
        if all((a,c) in edges for a,b in edges for bb,c in edges if bb==b):
            yield frozenset(edges)


def canonical(edges,n):
    return min(tuple(int((p[a],p[b]) in edges)
                     for a in range(n) for b in range(n) if a!=b)
               for p in permutations(range(n)))


def prefix_probability(edges,n):
    valid = [perm for perm in permutations(range(n))
             if all(perm.index(a)<perm.index(b) for a,b in edges)]
    return Q(sum((perm[0],perm[1]) in edges for perm in valid),len(valid))


def triple_type(edges):
    k=len(edges)
    if k==0: return 'A'
    if k==1: return 'E'
    if k==3: return 'C'
    assert k==2
    return 'V' if prefix_probability(edges,3)==1 else 'Lambda'


def induced(edges,sub):
    index={v:i for i,v in enumerate(sub)}
    return frozenset((index[a],index[b]) for a,b in edges if a in index and b in index)


def triple_frequencies(edges):
    counts=Counter(triple_type(induced(edges,sub))
                   for sub in combinations(range(4),3))
    return {k:Q(counts[k],4) for k in ('A','E','C','V','Lambda')}



# Four-point geometry: W is the conditional fraction of the diamond in a point's past.
# E[W^k] = 12/((2k+1)(2k+3)) - 3/(k+1)^2.
assert Q(12,7*9)-Q(3,16)==Q(1,336)
top_probability=bottom_probability=Q(4,336)  # unique greatest/least among four points

def greatest(e):
    return int(any(all((b,a) in e for b in range(4) if b!=a) for a in range(4)))
def least(e):
    return int(any(all((a,b) in e for b in range(4) if b!=a) for a in range(4)))

four=list(posets(4))
assert len(four)==219
classes={}
for e in four:
    p=prefix_probability(e,4); q=triple_frequencies(e)
    t=greatest(e); b=least(e)
    lower=q['E']/3-q['C']/3+2*q['V']/3-2*q['Lambda']/3+Q(t+b,2)
    upper=q['E']/3+q['C']+4*q['V']/3-2*q['Lambda']/3+Q(t,2)
    assert lower<=p<=upper, (e,p,lower,upper)
    key=canonical(e,4)
    assert key not in classes or classes[key][1:]==(p,q,t,b)
    classes[key]=(e,p,q,t,b)
assert len(classes)==16
q3={'A':Q(53,70),'E':Q(33,175),'Lambda':Q(9,350),
    'V':Q(9,350),'C':Q(1,350)}
assert sum(q3.values())==1
lo=q3['E']/3-q3['C']/3+2*q3['V']/3-2*q3['Lambda']/3+(top_probability+bottom_probability)/2
hi=q3['E']/3+q3['C']+4*q3['V']/3-2*q3['Lambda']/3+top_probability/2
assert (lo,hi)==(Q(31,420),Q(373,4200))

# Exact primal rational witnesses for each endpoint, independent of floating point LP.
ordered=list(classes.values())
low_support={0:Q(631,840),2:Q(1,175),5:Q(13,2100),6:Q(13,70),9:Q(1,84),11:Q(47,1400),12:Q(1,175)}
high_support={0:Q(1507,2100),2:Q(47,700),3:Q(11,140),5:Q(1,84),6:Q(79,700),9:Q(1,2100),10:Q(2,175)}
for support,target in ((low_support,lo),(high_support,hi)):
    assert sum(support.values())==1
    assert all(sum((weight*ordered[i][2][k] for i,weight in support.items()),Q(0))==q3[k] for k in q3)
    assert sum((weight*ordered[i][3] for i,weight in support.items()),Q(0))==top_probability
    assert sum((weight*ordered[i][4] for i,weight in support.items()),Q(0))==bottom_probability
    assert sum((weight*ordered[i][1] for i,weight in support.items()),Q(0))==target


# Time-reversal symmetry holds for the Minkowski diamond.
for e in four:
    rev=frozenset((b,a) for a,b in e)
    psym=(prefix_probability(e,4)+prefix_probability(rev,4))/2
    q=triple_frequencies(e)
    t=greatest(e); b=least(e)
    low_sym=q['E']/3+Q(t+b,2)
    high_sym=q['E']/3+q['C']+(q['V']+q['Lambda'])/3+Q(t+b,4)
    assert low_sym<=psym<=high_sym
sym_lo=q3['E']/3+(top_probability+bottom_probability)/2
sym_hi=q3['E']/3+q3['C']+(q3['V']+q3['Lambda'])/3+(top_probability+bottom_probability)/4
assert (sym_lo,sym_hi)==(Q(157,2100),Q(373,4200))

# Attaining symmetry-respecting distributions (canonical class indices).
sym_low={0:Q(3161,4200),5:Q(19,2100),6:Q(33,175),9:Q(19,2100),11:Q(7,200),12:Q(1,350),14:Q(1,350)}
sym_high={0:Q(1507,2100),2:Q(47,700),3:Q(47,700),4:Q(2,175),5:Q(1,84),6:Q(79,700),9:Q(1,84)}
for support,target in ((sym_low,sym_lo),(sym_high,sym_hi)):
    assert sum(support.values())==1
    assert all(sum((weight*ordered[i][2][k] for i,weight in support.items()),Q(0))==q3[k] for k in q3)
    assert sum((weight*ordered[i][3] for i,weight in support.items()),Q(0))==top_probability
    assert sum((weight*ordered[i][4] for i,weight in support.items()),Q(0))==bottom_probability
    assert sum((weight*ordered[i][1] for i,weight in support.items()),Q(0))==target
    for i,weight in support.items():
        rev=frozenset((b,a) for a,b in ordered[i][0])
        j=next(k for k,v in enumerate(ordered) if canonical(v[0],4)==canonical(rev,4))
        assert support.get(j,Q(0))==weight

print('STATUS := COMPUTATION_PASS')
print('FOUR_LABELED_POSETS :=',len(four))
print('UNLABELED_CLASSES :=',len(classes))
print('FOUR_POINT_MOMENT := 1/336')
print('GREATEST_AND_LEAST_PROBABILITY := 1/84 EACH')
print('LOWER :=',lo,'UPPER :=',hi)
print('TIME_REVERSAL_SHARP_LOWER :=',sym_lo,'TIME_REVERSAL_SHARP_UPPER :=',sym_hi)
print('DUAL_BOUNDS := VERIFIED_ALL_POSETS')
print('PRIMAL_EXTREMIZERS := VERIFIED_EXACT_RATIONAL')
print('INTERVAL_OPTIMALITY := ONLY_GIVEN_LISTED_MARGINALS')
print('ACTUAL_P_4_2 := OPEN')
print('LEAN := NOT_RUN')

# New genuinely four-event statistic: two events below one event, which
# itself precedes the remaining event. The middle event is unique.
# For four independent points, probability = 12 E[W_past^2 W_future]
# = 12/35280 = 1/2940. The moment is obtained by exact polynomial
# integration over the two halves of a 4D causal diamond.
MIXED_MOMENT = Q(1,35280)
CENTER_PROB = 12*MIXED_MOMENT
assert CENTER_PROB == Q(1,2940)

def central_2past_1future(edges):
    return int(any(sum((a,x) in edges for a in range(4) if a!=x)==2 and
                   sum((x,b) in edges for b in range(4) if b!=x)==1
                   for x in range(4)))

# Exact linear-program dual certificate, including time reversal and center.
rows = [[Q(1) for _ in ordered]]
bs = [Q(1)]
for key in ('A','E','V','Lambda','C'):
    rows.append([v[2][key] for v in ordered]); bs.append(q3[key])
for idx in (3,4):
    rows.append([Q(v[idx]) for v in ordered]); bs.append(top_probability)
for i,(edges,*_) in enumerate(ordered):
    rev=frozenset((b,a) for a,b in edges)
    j=next(k for k,v in enumerate(ordered)
           if canonical(v[0],4)==canonical(rev,4))
    if j>i:
        row=[Q(0) for _ in ordered]
        row[i],row[j]=Q(1),Q(-1)
        rows.append(row);bs.append(Q(0))
rows.append([Q(central_2past_1future(v[0])) for v in ordered])
bs.append(CENTER_PROB)
assert len(rows)==13
# y.A_col >= prefix_probability; y.b is the exact objective upper bound.
dual={0:Q(1,3),1:Q(-1,3),5:Q(2,3),6:Q(1,2),
      8:Q(-1,4),9:Q(-3,4),10:Q(-2,3),11:Q(-1,3),12:Q(-1,2)}
y=[dual.get(i,Q(0)) for i in range(len(rows))]
for i,v in enumerate(ordered):
    assert sum((y[j]*rows[j][i] for j in range(len(rows))),Q(0)) >= v[1]
upper=sum((y[j]*bs[j] for j in range(len(rows))),Q(0))
assert upper==Q(1303,14700)

# Exact primal mixture verifies optimality under precisely these constraints.
primal={0:Q(1777,2940),1:Q(79,350),2:Q(167,2450),
        3:Q(167,2450),4:Q(37,3675),5:Q(17,1470),
        9:Q(17,1470),15:Q(1,2940)}
x=[primal.get(i,Q(0)) for i in range(len(ordered))]
assert sum(x)==1 and all(v>=0 for v in x)
assert all(sum((rows[j][i]*x[i] for i in range(len(x))),Q(0))==bs[j]
           for j in range(len(rows)))
assert sum((x[i]*ordered[i][1] for i in range(len(x))),Q(0))==upper
# Previous exact lower witness remains feasible for the new center constraint?
# Not assumed; find an exact lower witness rather than declare sharpness.
print('MIXED_PAST2_FUTURE1 :=',MIXED_MOMENT)
print('FOUR_EVENT_2PAST_1FUTURE :=',CENTER_PROB)
print('NEW_UPPER :=',upper)
print('EXACT_DUAL_PRIMAL_UPPER := PASS')
print('LOWER :=',sym_lo,'(conservative bound; sharpness with new moment not audited)')
print('ACTUAL_MINKOWSKI_P_4_2 := OPEN')


# Independent exact geometric-moment integration using null coordinates
# a=t-r, b=t+r; 0<=a<=b<=1. Normalized volume density:
# 12 (b-a)^2 da db. Wpast=a^2*b^2, Wfuture=(1-a)^2*(1-b)^2.
from math import comb

def geometric_joint_moment(past_power, future_power):
    r,s=past_power,future_power
    answer=Q(0)
    for i in range(2*s+1):
        for j in range(2*s+1):
            inner=sum((Q(c,2*r+i+k+1)
                       for k,c in enumerate((1,-2,1))), Q(0))
            answer+=Q(12*(-1)**(i+j)*comb(2*s,i)*comb(2*s,j),
                      4*r+i+j+4)*inner
    return answer

assert geometric_joint_moment(0,0)==1
assert geometric_joint_moment(1,0)==Q(1,20)
assert geometric_joint_moment(2,0)==Q(1,105)
assert geometric_joint_moment(3,0)==Q(1,336)
assert geometric_joint_moment(1,1)==Q(1,2100)
assert geometric_joint_moment(2,1)==MIXED_MOMENT
print('INDEPENDENT_MINKOWSKI_MOMENT_INTEGRATION := PASS')

# Additional independently published Myrheim--Meyer / Meyer chain-abundance
# formula, specialized to four points in dimension d=4:
#    Pr(four-point chain) = 4! * (1/4) * 12**3 * Gamma(2)*Gamma(4)
#                          / (Gamma(8)*Gamma(10)) = 1/29400.
from math import factorial
FOUR_CHAIN_PROB = Q(factorial(4),4)*Q(12**3*factorial(1)*factorial(3),factorial(7)*factorial(9))
assert FOUR_CHAIN_PROB == Q(1,29400)
rows.append([Q(int(len(v[0])==6)) for v in ordered])
bs.append(FOUR_CHAIN_PROB)

# Exact rational feasible primal witnesses and dual inequalities.
low_support = {0:Q(277,490),1:Q(66,175),5:Q(8,1225),9:Q(8,1225),
               11:Q(163,4200),12:Q(3,9800),13:Q(37,7350),
               14:Q(3,9800),15:Q(1,29400)}
high_support = {0:Q(17761,29400),1:Q(278,1225),2:Q(331,4900),
                3:Q(331,4900),4:Q(37,3675),5:Q(17,1470),
                9:Q(17,1470),12:Q(3,9800),14:Q(3,9800),
                15:Q(1,29400)}
low_dual = {2:Q(1,3),6:Q(1),8:Q(-1,6),9:Q(-1),10:Q(-3,4),11:Q(-1)}
high_dual = {0:Q(1,3),1:Q(-1,3),5:Q(2,3),6:Q(1,2),
             8:Q(-1,4),9:Q(-3,4),10:Q(-2,3),11:Q(-1,3),
             12:Q(-5,6),13:Q(1,3)}

for label, witness, dual, direction, target in (
    ('LOWER',low_support,low_dual,'min',Q(157,2100)),
    ('UPPER',high_support,high_dual,'max',Q(2603,29400)),
):
    x=[witness.get(i,Q(0)) for i in range(len(ordered))]
    y=[dual.get(j,Q(0)) for j in range(len(rows))]
    assert all(z>=0 for z in x)
    assert all(sum(row[i]*x[i] for i in range(len(x)))==b
               for row,b in zip(rows,bs)),label
    objective=sum(x[i]*ordered[i][1] for i in range(len(x)))
    bound=sum(y[j]*bs[j] for j in range(len(rows)))
    assert objective==bound==target,(label,objective,bound,target)
    lhs=[sum(y[j]*rows[j][i] for j in range(len(rows)))
         for i in range(len(ordered))]
    assert all((lhs[i]<=ordered[i][1] if direction=='min' else
                lhs[i]>=ordered[i][1]) for i in range(len(ordered)))
    print('NEW_EXACT_'+label+' :=',target)

print('FOUR_CHAIN_MINKOWSKI :=',FOUR_CHAIN_PROB)
print('CERTIFICATE := COMPUTATION_PASS')
print('BOUND_SHARPNESS := GIVEN_CONSTRAINTS_ONLY')
print('ACTUAL_MINKOWSKI_P_4_2 := OPEN')
print('INFINITE_GROWTH_SAMPLING_STABILITY := OPEN')
print('LEAN := NOT_RUN')
