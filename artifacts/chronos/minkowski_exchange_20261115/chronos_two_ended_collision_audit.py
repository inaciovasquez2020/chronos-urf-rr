from itertools import permutations
from functools import lru_cache
from fractions import Fraction
from math import factorial

def calc(pi):
 n=len(pi); full=(1<<n)-1
 pred=[sum(1<<i for i in range(j) if pi[i]<pi[j]) for j in range(n)]
 succ=[sum(1<<j for j in range(i+1,n) if pi[i]<pi[j]) for i in range(n)]
 @lru_cache(None)
 def E(mask):
  if mask==0:return 1
  return sum(E(mask^(1<<i)) for i in range(n) if mask>>i&1 and pred[i]&mask==0)
 tot=E(full)
 mins=[i for i in range(n) if not pred[i]]
 maxs=[i for i in range(n) if not succ[i]]
 p={i:Fraction(E(full^(1<<i)),tot) for i in mins}
 q={j:Fraction(E(full^(1<<j)),tot) for j in maxs}
 joint={(i,j):Fraction(E(full^(1<<i)^(1<<j)),tot) for i in mins for j in maxs if i!=j}
 assert sum(joint.values())==1
 assert all(sum(v for (i,j),v in joint.items() if i==a)==p[a] for a in mins)
 assert all(sum(v for (i,j),v in joint.items() if j==b)==q[b] for b in maxs)
 cp=sum(x*x for x in p.values());cm=sum(x*x for x in q.values());J=sum(x*x for x in joint.values());return cp,cm,J,tuple(p.values()),tuple(q.values())
for n in range(2,8):
 neg=pos=zero=0; witness_neg=witness_pos=None; s=[0.,0.,0.];mi=1.;ma=-1.
 for pi in permutations(range(n)):
  cp,cm,j,p,q=calc(pi);d=j-cp*cm
  if d<0:neg+=1;witness_neg=witness_neg or (pi,str(d),str(cp),str(cm),str(j))
  elif d>0:pos+=1;witness_pos=witness_pos or (pi,str(d),str(cp),str(cm),str(j))
  else:zero+=1
  for i,v in enumerate((cp,cm,j)):s[i]+=float(v)
 print('n',n,'negative',neg,'positive',pos,'zero',zero,'E_C+',s[0]/factorial(n),'E_C-',s[1]/factorial(n),'E_J',s[2]/factorial(n), 'negative witness',witness_neg,'positive witness',witness_pos,flush=True)