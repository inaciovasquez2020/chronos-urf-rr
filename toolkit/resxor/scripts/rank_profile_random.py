import argparse, json, random
import numpy as np
from collections import deque

def random_regular(n: int, d: int, seed: int):
  rng = random.Random(seed)
  while True:
    stubs = []
    for v in range(n):
      stubs += [v]*d
    rng.shuffle(stubs)
    edges = set()
    ok = True
    for i in range(0, len(stubs), 2):
      a,b = stubs[i], stubs[i+1]
      if a==b:
        ok=False; break
      e = (a,b) if a<b else (b,a)
      edges.add(e)
    if ok and len(edges)==(n*d)//2:
      return sorted(edges)
    seed += 1
    rng = random.Random(seed)

def adj(n, edges):
  A=[[] for _ in range(n)]
  for u,v in edges:
    A[u].append(v); A[v].append(u)
  return A

def bfs(n, A, root=0):
  q=deque([root]); seen=[False]*n; seen[root]=True; order=[root]
  while q:
    u=q.popleft()
    for v in A[u]:
      if not seen[v]:
        seen[v]=True; q.append(v); order.append(v)
  if len(order)!=n:
    for v in range(n):
      if not seen[v]:
        order.append(v)
  return order

def cut_vec(n, U):
  v = np.zeros(n, dtype=np.uint8)
  v[list(U)] = 1
  return v

def gf2_rank(M):
  M = M.copy().astype(np.uint8)
  r=0
  rows, cols = M.shape
  c=0
  for c in range(cols):
    piv = None
    for i in range(r, rows):
      if M[i,c]:
        piv=i; break
    if piv is None:
      continue
    if piv!=r:
      M[[r,piv]] = M[[piv,r]]
    for i in range(rows):
      if i!=r and M[i,c]:
        M[i,:] ^= M[r,:]
    r += 1
    if r==rows:
      break
  return r

def main():
  ap=argparse.ArgumentParser()
  ap.add_argument("--trials", type=int, default=10)
  ap.add_argument("--n", type=int, default=200)
  ap.add_argument("--d", type=int, default=4)
  ap.add_argument("--seed", type=int, default=0)
  ap.add_argument("--out", required=True)
  args=ap.parse_args()

  rows=[]
  for t in range(args.trials):
    seed=args.seed+t
    edges=random_regular(args.n,args.d,seed)
    A=adj(args.n,edges)
    order=bfs(args.n,A,0)
    # sequential Res(⊕): live set = {acc, axiom} so rank ≤ 2 always; compute exact rank trace of vertex-cut vectors
    acc=set()
    trace=[]
    for i,v in enumerate(order):
      ax={v}
      if i==0:
        acc=set(ax)
        M=np.vstack([cut_vec(args.n,acc)])
        trace.append({"i":i,"rank":gf2_rank(M),"acc_size":len(acc),"live":1})
      else:
        acc = acc.symmetric_difference(ax)
        M=np.vstack([cut_vec(args.n,acc), cut_vec(args.n,ax)])
        trace.append({"i":i,"rank":gf2_rank(M),"acc_size":len(acc),"live":2})
    rows.append({"trial":t,"seed":seed,"max_rank":max(x["rank"] for x in trace),"trace":trace[:200]})
  with open(args.out,"w") as f:
    json.dump({"n":args.n,"d":args.d,"trials":args.trials,"rows":rows}, f, indent=2)

if __name__=="__main__":
  main()
