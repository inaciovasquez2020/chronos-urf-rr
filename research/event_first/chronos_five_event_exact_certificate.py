from fractions import Fraction as F
from itertools import permutations, combinations
from collections import defaultdict

N=5
# transitive past-set natural labeled posets (each integer j predecessor bitmask)
def ext(p):
    n=len(p)
    for m in range(1<<n):
        if all((m & p[i])==p[i] for i in range(n) if m>>i&1):
            yield p+(m,)

def closure(p):
    n=len(p)
    return tuple(sum(1<<i for i in range(n) if (p[j]>>i)&1) for j in range(n))

def canon(p):
    n=len(p)
    # unordered isomorphism key via all n! vertex relabelings, 25-bit adjacency
    def code(q):
        s=0
        for i in range(n):
            for j in range(n):
                if (p[j]>>i)&1:s|=1<<(q[i]*n+q[j])
        return s
    return min(code(q) for q in permutations(range(n)))

states=[()]
for n in range(N):
    states=[q for p in states for q in ext(p)]
    print('N',n+1,'LABELED',len(states))
assert len(states)==357
C=defaultdict(list)
for p in states:C[canon(p)].append(p)
print('UNLABELED',len(C))
assert len(C)==63

def edges(p):return [(i,j) for j in range(len(p)) for i in range(j) if p[j]>>i&1]
def typ(p):
    E=edges(p)
    if len(E)==0:return 'empty'
    if len(E)==1:return 'one_edge'
    if len(E)==3 and any((i,j) in E and (j,k) in E and (i,k) in E for i,j,k in combinations(range(len(p)),3)):
        return 'chain3'
    if len(E)==2:
        a,b=E
        if len(set(a+b))==4:return 'two_chains2'
    return 'other'

class_sizes=defaultdict(list)
for k,V in C.items():class_sizes[typ(V[0])].append(len(V))
print('SPECIAL_CLASS_SIZES',{k:v for k,v in class_sizes.items() if k in ('empty','one_edge','chain3','two_chains2')})
weights={'empty':F(11,70),'one_edge':F(5,7),'chain3':F(1,35),'two_chains2':F(1,10)}
assert all(len(class_sizes[k])==1 for k in weights)
assert [class_sizes[k][0] for k in weights]==[1,10,10,15]
assert sum(weights.values())==1

# All 357 labelled terminal posets, probability = class mass / number of naturally labeled representatives.
T={p:weights.get(typ(p),F(0))/len(C[canon(p)]) for p in states}
assert sum(T.values())==1
print('POSITIVE_TERMINAL_SUPPORT',sum(v>0 for v in T.values()))
assert sum(v>0 for v in T.values())==36

def pairfraction(p):return F(len(edges(p)),10)
def triplefraction(p):
    e=set(edges(p)); n=len(p)
    return F(sum((i,j) in e and (j,k) in e for i,j,k in combinations(range(n),3)),10)
def two2fraction(p):
    n=len(p); e=set(edges(p));count=0
    for S in combinations(range(n),4):
        sub=[(i,j) for (i,j) in e if i in S and j in S]
        if len(sub)==2 and len(set(sum(([i,j] for i,j in sub),[])))==4:count+=1
    return F(count,5)
for name,fn,expected in [('P2',pairfraction,F(1,10)),('P3',triplefraction,F(1,350)),('2+2',two2fraction,F(1,50))]:
    value=sum(v*fn(p) for p,v in T.items())
    print(name,value,'EXPECTED',expected)
    assert value==expected

# Prefix masses and normalized transition probabilities.
M=[]
for n in range(N+1):
    q=defaultdict(F)
    for p, v in T.items():q[p[:n]]+=v
    M.append(dict(q))
print('NONZERO_PREFIX_MASS_COUNTS',[sum(v>0 for v in Q.values()) for Q in M])
for n in range(N):
    for p,v in M[n].items():
        if not v:continue
        successors=[s for s in M[n+1] if s[:-1]==p]
        assert sum(M[n+1][s]/v for s in successors)==1

squares=0
for n in range(N-1):
    for p,mp in M[n].items():
        if not mp:continue
        # covariance squares when two new vertices a,b incomparably added
        for a in range(1<<n):
            pa=p+(a,)
            if M[n+1].get(pa,F(0))==0:continue
            for b in range(1<<n):
                pb=p+(b,)
                if M[n+1].get(pb,F(0))==0:continue
                # x,y unordered relative; valid final order p + a + b (b not > a)
                pab=p+(a,b)
                pba=p+(b,a)
                if M[n+2].get(pab,F(0)) and M[n+2].get(pba,F(0)):
                    assert M[n+2][pab]==M[n+2][pba],(p,a,b)
                    squares+=1
print('SQUARES_DIRECTED',squares)
print('PASS')
for p,probes in [((0,), (0,1)), ((0,0), (0,1))]:
    n=len(p)
    print('BELL_PARENT',p,'MASS',M[n][p])
    for a in probes:
        print('PRECURSOR',a,'WEIGHT',M[n+1].get(p+(a,),F(0))/M[n][p])
a=M[3][(0,0,0)]/M[2][(0,0)]
b=M[3][(0,0,1)]/M[2][(0,0)]
c=M[2][(0,0)]/M[1][(0,)]
d=M[2][(0,1)]/M[1][(0,)]
assert a==F(247,315) and b==F(34,315)
assert c==F(9,10) and d==F(1,10)
assert a*d-b*c == F(-59,3150)
print('BELL_CROSS',a*d-b*c)
print('CERTIFICATE := COMPUTATION_PASS; FINITE_N_ONLY; LEAN_NOT_RUN')

# Independent exhaustive square census, including zero-mass natural-labeling histories.
# A pair of incomparable newly appended elements may be swapped; both resulting
# naturally labeled posets must have equal mass by the terminal class assignment.
census=[]
for n in range(N-1):
    all_valid=positive=unique_positive=0
    unordered=set()
    for parent in M[n]:
        for a in range(1<<n):
            for b in range(1<<n):
                ab=parent+(a,b)
                ba=parent+(b,a)
                if ab not in M[n+2] or ba not in M[n+2]:
                    continue
                all_valid+=1
                assert M[n+2][ab]==M[n+2][ba]
                if M[n+2][ab]>0:
                    assert M[n][parent]>0
                    assert M[n+1][parent+(a,)]>0
                    assert M[n+1][parent+(b,)]>0
                    positive+=1
                    unordered.add((parent, tuple(sorted((a,b)))))
                    left=(M[n+1][parent+(a,)]/M[n][parent])*(M[n+2][ab]/M[n+1][parent+(a,)])
                    right=(M[n+1][parent+(b,)]/M[n][parent])*(M[n+2][ba]/M[n+1][parent+(b,)])
                    assert left==right
    unique_positive=len(unordered)
    census.append((n,all_valid,positive,unique_positive))
    print('SQUARE_CENSUS',n,'ALL',all_valid,'POSITIVE_DIRECTED',positive,'POSITIVE_UNORDERED',unique_positive)
assert [row[1] for row in census]==[1,4,25,238]
assert [row[2] for row in census]==[1,3,10,29]
assert sum(row[1] for row in census)==268
assert sum(row[2] for row in census)==43
assert sum(row[3] for row in census)==26
print('ALL_268_ADJACENT_SWAP_EQUALITIES := PASS')
print('ALL_43_POSITIVE_HISTORY_COVARIANCE_SQUARES := PASS')
print('REPORTED_218_SQUARES := UNRECONCILED_DIFFERENT_COUNTING_CONVENTION')
