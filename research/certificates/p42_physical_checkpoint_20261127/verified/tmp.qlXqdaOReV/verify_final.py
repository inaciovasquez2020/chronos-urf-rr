from fractions import Fraction as Q
from collections import defaultdict
from itertools import combinations, permutations, product
from math import comb

# Exact exponential expansion.
A = {
    (1,0,0): Q(3,2),
    (-1,0,0): Q(1,2),
    (0,1,0): Q(-1),
    (0,-1,0): Q(-1)
}

B = {
    (-7,0,0): Q(1,14),
    (-9,0,0): Q(1,18),
    (-8,0,1): Q(-1,16),
    (-8,0,-1): Q(-1,16)
}

G = defaultdict(Q)

def integ(k,j,v):
    if j == 0:
        G[k,1] += 2*v
    else:
        G[k+j,0] += v/j
        G[k-j,0] -= v/j

for (a,b,c),v in A.items():
    for (d,e,f),w in A.items():
        for (g,h,i),z in B.items():
            j = b+e+h+8
            k = c+f+i-8
            t = a+d+g
            assert j != 0
            integ(t,j+k,2*v*w*z/j)
            integ(t-j,k,-2*v*w*z/j)

G = {k:v for k,v in G.items() if v}

L = {4:243,5:1143,6:513,7:21}
C = {4:-374,5:-162,6:486,7:50}

expected = {
    **{(3-2*n,1):Q(v,3024) for n,v in L.items()},
    **{(3-2*n,0):Q(v,3024) for n,v in C.items()}
}

assert G == expected
assert sum(C.values()) == 0

print("EXPONENTIAL_MONOMIAL_INTEGRATION := PASS")
print("EXPONENTIAL_TERMS := 64")
print("REDUCED_TERMS := 8")

# Each pair represents a*pi^2+b.
# Uses the classical Basel/logarithmic moment identity.

sp = (
    Q(72,3024)*sum(L.values())/12,
    Q(72,3024)*(
        -sum(
            Q(v,2)*sum(
                Q(1,k*k) for k in range(1,n+1)
            )
            for n,v in L.items()
        )
        -sum(
            v*sum(Q(1,k) for k in range(1,n+1))
            for n,v in C.items()
        )
    )
)

assert sp == (Q(80,21),-Q(3316139,88200))

print("SPACELIKE_PI2_COEFFICIENT := ",sp[0])
print("SPACELIKE_RATIONAL_TERM := ",sp[1])

# Comparable contribution:
# 2 E[(t^2-r^2)^2 ((1-t)^2-r^2)^4].

comp = Q(0)

for a in range(3):
    for b in range(5):
        i = 4-2*a
        j = 8-2*b
        k = 2*(a+b)

        def half(i,j):
            return sum(
                Q((-1)**u*comb(j,u),i+u+k+4)
                * Q(1,2)**(i+u+k+4)
                for u in range(j+1)
            )/(k+3)

        comp += (
            2*96*(-1)**(a+b)
            *comb(2,a)*comb(4,b)
            *(half(i,j)+half(j,i))
        )

assert comp == Q(1,17640)

print("COMPARABLE_CONTRIBUTION := ",comp)

M = (sp[0],sp[1]+comp)

assert M == (Q(80,21),-Q(552689,14700))

print("M22_EXACT_ARITHMETIC := PASS")

# Exhaustive enumeration: 3^6 candidate relations.
pairs = list(combinations(range(4),2))
perms = list(permutations(range(4)))

def canon(e):
    return min(
        tuple(
            int((p[a],p[b]) in e)
            for a in range(4)
            for b in range(4)
            if a != b
        )
        for p in perms
    )

def prefix(e,n):
    v = [
        p for p in permutations(range(n))
        if all(
            p.index(a)<p.index(b)
            for a,b in e
        )
    ]
    return Q(
        sum((p[0],p[1]) in e for p in v),
        len(v)
    )

def triples(e):
    ts = []
    for sub in combinations(range(4),3):
        ren = {v:i for i,v in enumerate(sub)}
        f = {
            (ren[a],ren[b])
            for a,b in e
            if a in ren and b in ren
        }
        n = len(f)
        ts.append([
            'A','E',
            'V' if prefix(f,3)==1 else 'Lambda',
            'C'
        ][n])
    return [
        Q(ts.count(k),4)
        for k in ('A','E','V','Lambda','C')
    ]

classes = {}
count = 0

for states in product(range(3),repeat=6):
    e = frozenset(
        (a,b) if s==1 else (b,a)
        for (a,b),s in zip(pairs,states)
        if s
    )

    if not all(
        (a,c) in e
        for a,b in e
        for bb,c in e
        if b==bb
    ):
        continue

    count += 1
    classes.setdefault(canon(e),e)

E = list(classes.values())
assert (count,len(E)) == (219,16)

c = [prefix(e,4) for e in E]

top = [
    int(any(
        all((b,a) in e for b in range(4) if b!=a)
        for a in range(4)
    ))
    for e in E
]

bot = [
    int(any(
        all((a,b) in e for b in range(4) if b!=a)
        for a in range(4)
    ))
    for e in E
]

rows = (
    [[1]*16]
    +list(map(list,zip(*(triples(e) for e in E))))
    +[top,bot]
)

rhs = [
    1,Q(53,70),Q(33,175),
    Q(9,350),Q(9,350),Q(1,350),
    Q(1,84),Q(1,84)
]

for i,e in enumerate(E):
    j = list(classes).index(
        canon(frozenset((b,a) for a,b in e))
    )
    if j>i:
        row = [0]*16
        row[i] = 1
        row[j] = -1
        rows.append(row)
        rhs.append(0)

rows.append([
    int(any(
        sum((a,x) in e for a in range(4))==2
        and
        sum((x,a) in e for a in range(4))==1
        for x in range(4)
    ))
    for e in E
])

rhs.append(Q(1,2940))

def motif(e):
    return [
        Q(sum(
            all((p[a],p[b]) in f for a,b in e)
            for p in perms
        ),24)
        for f in E
    ]

matchings = [
    ((0,1),(2,3)),
    ((0,2),(1,3)),
    ((0,3),(1,2))
]

rows.extend([
    [
        sum(all(
            (a,b) in e or (b,a) in e
            for a,b in pp
        ) for pp in matchings)
        for e in E
    ],
    [int(len(e)==6) for e in E],
    motif({(0,1),(2,1),(2,3)}),
    motif({(0,3),(1,2),(2,3),(1,3)}),
    motif({(3,0),(3,1),(0,2),(1,2),(3,2)})
])

rhs.extend([
    Q(3,100),
    Q(1,29400),
    Q(953,705600),
    Q(1,6720),
    Q(1,35280)
])

m = motif({(0,2),(0,3),(1,2),(1,3)})

z = list(map(Q,(
    '1 -1 -2/3 -1/3 -1 0 0 1/2 '
    '-1/6 0 1/30 0 -11/30 0 '
    '2/15 -16/5 12/5 -6/5'
).split()))

assert len(rows)==len(z)==18

assert all(
    sum(y*row[i] for y,row in zip(z,rows))
    +Q(6,5)*m[i] == c[i]
    for i in range(16)
)

base = sum(y*b for y,b in zip(z,rhs))
assert base == Q(3557,42000)

p = (Q(6,5)*M[0],base+Q(6,5)*M[1])

assert p == (Q(32,7),-Q(13239637,294000))

print("CANDIDATE_RELATIONS := 729")
print("LABELED_POSETS := ",count)
print("UNLABELED_CLASSES := ",len(E))
print("FINITE_OBJECTIVE_IDENTITY := PASS")
print("P42_PI2_COEFFICIENT := ",p[0])
print("P42_RATIONAL_TERM := ",p[1])
print("P42_EXACT_ARITHMETIC := PASS")
print("FINAL_COMPUTATIONAL_TEST := PASS")
print("ANALYTIC_EVALUATION_LEAN := OPEN")
print("FULL_PROBABILITY_THEOREM := OPEN")
