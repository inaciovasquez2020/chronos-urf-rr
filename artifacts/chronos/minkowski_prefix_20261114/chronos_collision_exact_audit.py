import itertools,time
from functools import lru_cache

def calc(p):
 n=len(p); pred=[sum(1<<i for i in range(j) if p[i]<p[j]) for j in range(n)]; full=(1<<n)-1
 @lru_cache(None)
 def e(mask):
  if not mask:return 1
  return sum(e(mask^(1<<i)) for i in range(n) if mask>>i&1 and not pred[i]&mask)
 total=e(full); first=[i for i in range(n) if pred[i]==0]
 nums=[e(full^(1<<i)) for i in first]
 C_num=sum(x*x for x in nums)
 A_num=sum(e(full^(1<<i)^(1<<j)) for i in first for j in range(n) if pred[j]==(1<<i))
 return A_num/total,C_num/(total*total),max(nums)/total,len(first)
for n in range(2,9):
 s=[0]*4; t=time.time()
 for p in itertools.permutations(range(n)):
  v=calc(p)
  for i,x in enumerate(v):s[i]+=x
 print(n, 'perms',__import__('math').factorial(n),'A,C,maxp,Emin',*[round(x/__import__('math').factorial(n),8) for x in s],'sec',round(time.time()-t,2),flush=True)