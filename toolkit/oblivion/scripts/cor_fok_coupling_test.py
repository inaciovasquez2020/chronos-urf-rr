#!/usr/bin/env python3
import json, argparse, hashlib, collections

def load_graph(path):
  with open(path) as f: G=json.load(f)
  n=G.get("n",len(G["adj"])); adj=G["adj"]; return n,adj

def bfs_ball(adj, s, R):
  seen={s}; q=[(s,0)]
  for v,d in q:
    if d==R: continue
    for u in adj[v]:
      if u not in seen:
        seen.add(u); q.append((u,d+1))
  return seen

def sig_ball(adj, S):
  E=[]
  for v in S:
    for u in adj[v]:
      if u in S and v<u: E.append((v,u))
  E.sort()
  h=hashlib.blake2s(digest_size=16)
  h.update(str(len(S)).encode()); h.update(str(len(E)).encode())
  for a,b in E: h.update(f"{a},{b};".encode())
  return h.hexdigest()

def main():
  ap=argparse.ArgumentParser()
  ap.add_argument("--graph_json", required=True)
  ap.add_argument("--R", type=int, default=6)
  ap.add_argument("--limit", type=int, default=2000)
  ap.add_argument("--out", required=True)
  args=ap.parse_args()

  n,adj=load_graph(args.graph_json)
  lim=min(args.limit,n)

  ball_sig=[]  # proxy FO^k_R type signature = hashed induced ball
  for v in range(lim):
    S=bfs_ball(adj,v,args.R)
    ball_sig.append(sig_ball(adj,S))

  mult=collections.Counter(ball_sig)
  max_mult=max(mult.values()) if mult else 0

  # COR-proxy: count unique ball signatures among radius-R patches
  # (if COR large, we expect many distinct signatures; if FO^k homogeneous, few)
  distinct=len(mult)

  out={
    "meta":{"graph_json":args.graph_json,"n":n,"R":args.R,"limit":lim},
    "fok_proxy":{"distinct":distinct,"max_multiplicity":max_mult},
    "histogram":dict(sorted(collections.Counter(mult.values()).items()))
  }
  with open(args.out,"w") as f: json.dump(out,f,indent=2)
  print(json.dumps(out,indent=2))

if __name__=="__main__": main()
