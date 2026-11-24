#!/usr/bin/env python3
"""Exact rational certificate; Python 3 standard library only.
Scope: IID uniform points in a 4D Minkowski Alexandrov interval.
No network, repository changes, floating point, or external optimizer.
Geometric formulas are justified in the accompanying mathematical derivation;
this script checks their polynomial integrals and finite LP certificates.
"""
from fractions import Fraction as Q
from itertools import combinations, permutations, product
from math import comb, factorial

class Poly:
    def __init__(self, x=0):
        self.d = x if isinstance(x, dict) else {(0,0): Q(x)}
    def __add__(self, y):
        y = y if isinstance(y, Poly) else Poly(y)
        d = self.d.copy()
        for k,v in y.d.items(): d[k] = d.get(k,0)+v
        return Poly({k:v for k,v in d.items() if v})
    __radd__ = __add__
    def __neg__(self): return Poly({k:-v for k,v in self.d.items()})
    def __sub__(self,y): return self+-y
    def __rsub__(self,y): return -self+y
    def __mul__(self,y):
        y = y if isinstance(y, Poly) else Poly(y)
        d = {}
        for (i,j),a in self.d.items():
            for (k,l),b in y.d.items():
                z=(i+k,j+l); d[z]=d.get(z,0)+a*b
        return Poly({k:v for k,v in d.items() if v})
    __rmul__=__mul__
    def __pow__(self,n):
        assert isinstance(n,int) and n>=0
        a=Poly(1)
        for _ in range(n): a=a*self
        return a
    def __truediv__(self,n): return self*Q(1,n)

def avg(p):
    # 96 times integral r^2 dr dt; r <= min(t,1-t).
    p=p if isinstance(p,Poly) else Poly(p)
    return sum((a*Q(96,j+3)*(Q(1,2)**(i+j+4)/ (i+j+4)
           +sum(Q((-1)**k*comb(i,k),k+j+4)*Q(1,2)**(k+j+4)
                for k in range(i+1))) for (i,j),a in p.d.items()),Q(0))

t=Poly({(1,0):Q(1)});r=Poly({(0,1):Q(1)})
A=t*t-r*r;B=(1-t)**2-r*r;k=t*(1-t)+r*r
assert avg(1)==1
et,et2,ew2,eh,eh2,eth=[avg(p) for p in (t,t*t,r*r/3,A,A*A,t*A)]
assert (et,et2,ew2,eh,eh2,eth)==(Q(1,2),Q(4,15),Q(1,30),Q(1,6),Q(1,20),Q(1,10))
F=B**2*(A**2+4*k*k*et2+4*(k*k-A*B)*ew2+B**2*eh2+4*A*k*et+2*A*B*eh+4*k*B*eth)
assert avg(F)==Q(1,105)
alt_moment=avg(B**2*F)
assert alt_moment==Q(953,705600)
assert avg(A**2)==Q(1,20) and avg(A**4)==Q(1,105)
assert avg(A**6)==Q(1,336) and avg(A**4*B**2)==Q(1,35280)
assert avg(A**2*B**2)==Q(1,2100)
chain4=24*Q(1,4)*12**3*Q(6,factorial(7)*factorial(9))
assert chain4==Q(1,29400)

pairs=list(combinations(range(4),2)); perms=list(permutations(range(4)))
def canon(e):
    return min(tuple(int((p[a],p[b]) in e) for a in range(4) for b in range(4) if a!=b) for p in perms)
def prefix(e,n):
    v=[p for p in permutations(range(n)) if all(p.index(a)<p.index(b) for a,b in e)]
    return Q(sum((p[0],p[1]) in e for p in v),len(v))
def triples(e):
    ts=[]
    for sub in combinations(range(4),3):
        ren={v:i for i,v in enumerate(sub)}
        f={(ren[a],ren[b]) for a,b in e if a in ren and b in ren}; n=len(f)
        ts.append(['A','E','V' if prefix(f,3)==1 else 'Lambda','C'][n])
    return [Q(ts.count(k),4) for k in ('A','E','V','Lambda','C')]
classes={};count=0
for states in product(range(3),repeat=6):
    e=frozenset((a,b) if s==1 else (b,a) for (a,b),s in zip(pairs,states) if s)
    if not all((a,c) in e for a,b in e for bb,c in e if b==bb): continue
    count+=1;classes.setdefault(canon(e),e)
E=list(classes.values());assert count==219 and len(E)==16
c=[prefix(e,4) for e in E]
top=[int(any(all((b,a) in e for b in range(4) if b!=a) for a in range(4))) for e in E]
bot=[int(any(all((a,b) in e for b in range(4) if b!=a) for a in range(4))) for e in E]
rows=[[1]*16]+list(map(list,zip(*(triples(e) for e in E))))+[top,bot]
rhs=[1,Q(53,70),Q(33,175),Q(9,350),Q(9,350),Q(1,350),Q(1,84),Q(1,84)]
for i,e in enumerate(E):
    j=list(classes).index(canon(frozenset((b,a) for a,b in e)))
    if j>i:
        row=[0]*16;row[i]=1;row[j]=-1;rows.append(row);rhs.append(0)
rows.append([int(any(sum((a,x) in e for a in range(4))==2 and sum((x,a) in e for a in range(4))==1 for x in range(4))) for e in E]);rhs.append(Q(1,2940))
assert len(rows)==13

def match(e):
    return sum(all((a,b) in e or (b,a) in e for a,b in pp) for pp in [((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))])
def alt(e):
    return Q(sum(all(z in e for z in [(p[0],p[1]),(p[2],p[1]),(p[2],p[3])]) for p in perms),24)
rows.extend([[match(e) for e in E],[int(len(e)==6) for e in E],[alt(e) for e in E]])
rhs.extend([Q(3,100),chain4,alt_moment]);assert len(rows)==16

def qs(s): return [Q(v) for v in s.split()]
def verify(x,y,obj,expected):
    assert len(x)==16 and len(y)==len(rows)
    assert all(v>=0 for v in x)
    assert all(sum(a*t for a,t in zip(row,x))==v for row,v in zip(rows,rhs))
    assert all(sum(yj*row[i] for yj,row in zip(y,rows))<=obj[i] for i in range(16))
    assert sum(a*t for a,t in zip(obj,x))==sum(a*t for a,t in zip(rhs,y))==expected
    return expected
lo=verify(qs('35489/58800 629/2450 381/9800 381/9800 37/3675 17/1470 0 27/980 0 17/1470 0 11/19600 3/9800 0 3/9800 1/29400'),qs('1/3 -1/3 0 0 0 2/3 1/2 0 -1/4 -3/4 -8/15 -2/3 -1/6 -1/10 2/15 -4/5'),c,Q(4979,58800))
hi=-verify(qs('17947/29400 1123/4900 129/2450 129/2450 37/3675 17/1470 27/1960 0 0 17/1470 0 73/9800 3/9800 0 3/9800 1/29400'),qs('-1/3 1/3 0 0 0 -2/3 -1/2 0 1/4 3/4 7/12 2/3 1/6 0 -1/12 2'),[-v for v in c],-Q(253,2940))

def rank(a):
    a=[list(map(Q,row)) for row in a];j=0
    for k in range(len(a[0])):
        p=next((i for i in range(j,len(a)) if a[i][k]),None)
        if p is None:continue
        a[j],a[p]=a[p],a[j];v=a[j][k];a[j]=[z/v for z in a[j]]
        for i in range(j+1,len(a)):
            v=a[i][k];a[i]=[u-v*w for u,w in zip(a[i],a[j])]
        j+=1
    return j
assert rank(rows)==13 and rank(rows[:13])==10
print('LABELED_POSETS :=',count)
print('UNLABELED_CLASSES :=',len(E))
print('GEOMETRIC_MOMENTS := EXACT_RATIONAL_PASS')
print('ALTERNATING_MOMENT :=',alt_moment)
print('CONSTRAINT_ROWS :=',len(rows))
print('CONSTRAINT_RANK :=',rank(rows))
print('EXACT_PRIMAL_DUAL_CERTIFICATES := PASS')
print('LOWER :=',lo,'UPPER :=',hi,'WIDTH :=',hi-lo)
print('ACTUAL_P_4_2 := OPEN')
print('LEAN := NOT_RUN')

# Extension: two exact subdiamond moments and one free parameter.
def motif(e):
    return [Q(sum(all((p[a],p[b]) in f for a,b in e) for p in perms),24) for f in E]
rows += [motif({(0,3),(1,2),(2,3),(1,3)}),motif({(3,0),(3,1),(0,2),(1,2),(3,2)})]
rhs += [Q(1,6720),Q(1,35280)]
m=motif({(0,2),(0,3),(1,2),(1,3)})
assert rank(rows)==15 and rank(rows+[m])==16
z=qs('1 -1 -2/3 -1/3 -1 0 0 1/2 -1/6 0 1/30 0 -11/30 0 2/15 -16/5 12/5 -6/5')
assert all(sum(y*row[i] for y,row in zip(z,rows))+Q(6,5)*m[i]==c[i] for i in range(16))
assert sum(y*b for y,b in zip(z,rhs))==Q(3557,42000)
u=qs('2216/3675 71/280 8/175 8/175 73/14700 53/5880 -11/9800 121/4900 11/4900 53/5880 11/4900 0 3/9800 3/9800 3/9800 1/29400')
w=[1,-4,2,2,0,0,2,-4,0,0,0,1,0,0,0,0]
assert all(sum(a*t for a,t in zip(row,u))==b and sum(a*t for a,t in zip(row,w))==0 for row,b in zip(rows,rhs))
low=max(-a/b for a,b in zip(u,w) if b>0); high=min(-a/b for a,b in zip(u,w) if b<0)
assert (low,high)==(Q(11,19600),Q(121,19600))
for a,b in zip(u,w): assert a or b; assert min(a+b*low,a+b*high)>=0
assert sum(a*t for a,t in zip(m,u))==Q(19,176400)
assert sum(a*t for a,t in zip(m,w))==Q(1,6)
assert sum(a*t for a,t in zip(c,u))==Q(24937,294000)
assert sum(a*t for a,t in zip(c,w))==Q(1,5)
L=sum(a*(t+low*k) for a,t,k in zip(c,u,w)); H=sum(a*(t+high*k) for a,t,k in zip(c,u,w))
assert (L,H)==(Q(2497,29400),Q(253,2940))
print('EXTENDED_RANK :=',rank(rows))
print('RANK_WITH_M22 :=',rank(rows+[m]))
print('SINGLE_MOMENT_IDENTITY := PASS')
print('AFFINE_FAMILY := PASS')
print('NEW_LOWER :=',L,'NEW_UPPER :=',H)
print('M22 := OPEN')
