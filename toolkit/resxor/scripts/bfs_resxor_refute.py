import argparse, json
from collections import deque, defaultdict
import random

def torus(n_side: int):
  n = n_side * n_side
  def vid(i,j): return (i % n_side) * n_side + (j % n_side)
  edges = []
  for i in range(n_side):
    for j in range(n_side):
      v = vid(i,j)
      edges.append((v, vid(i+1,j)))
      edges.append((v, vid(i,j+1)))
  edges = list({tuple(sorted(e)) for e in edges})
  return n, edges

def random_regular(n: int, d: int, seed: int):
  rng = random.Random(seed)
  stubs = []
  for v in range(n):
    stubs += [v]*d
  rng.shuffle(stubs)
  edges = set()
  for i in range(0, len(stubs), 2):
    a, b = stubs[i], stubs[i+1]
    if a == b:
      return random_regular(n, d, seed+1)
    e = (a,b) if a < b else (b,a)
    edges.add(e)
  if len(edges) != (n*d)//2:
    return random_regular(n, d, seed+2)
  return n, sorted(edges)

def build_adj(n, edges):
  adj = [[] for _ in range(n)]
  for (u,v) in edges:
    adj[u].append(v)
    adj[v].append(u)
  return adj

def bfs_order(n, adj, root=0):
  seen = [False]*n
  q = deque([root])
  seen[root] = True
  order = [root]
  while q:
    u = q.popleft()
    for v in adj[u]:
      if not seen[v]:
        seen[v] = True
        q.append(v)
        order.append(v)
  if len(order) != n:
    for v in range(n):
      if not seen[v]:
        order.append(v)
  return order

def boundary_edges(Uset, edges):
  U = set(Uset)
  bd = []
  for (a,b) in edges:
    if (a in U) ^ (b in U):
      bd.append((a,b))
  return bd

def xor_clause(Sa, ba, Sb, bb):
  Sa = set(Sa); Sb = set(Sb)
  S = list(Sa.symmetric_difference(Sb))
  return S, (ba ^ bb)

def main():
  ap = argparse.ArgumentParser()
  ap.add_argument("--graph", choices=["torus","rr"], required=True)
  ap.add_argument("--n_side", type=int, default=20)
  ap.add_argument("--n", type=int, default=200)
  ap.add_argument("--d", type=int, default=4)
  ap.add_argument("--seed", type=int, default=0)
  ap.add_argument("--root", type=int, default=0)
  ap.add_argument("--out", required=True)
  args = ap.parse_args()

  if args.graph == "torus":
    n, edges = torus(args.n_side)
  else:
    n, edges = random_regular(args.n, args.d, args.seed)

  adj = build_adj(n, edges)
  order = bfs_order(n, adj, args.root)

  # Tseitin labeling f: V -> {0,1} with XOR f = 1 (unsat on connected graph)
  f = [0]*n
  f[0] = 1

  steps = []
  U = set()
  # accumulator clause for current U: [∂(U), c_U]
  acc_S = []
  acc_b = 0

  def c_of(Uset):
    x = 0
    for v in Uset:
      x ^= f[v]
    return x

  for i,v in enumerate(order):
    ax_U = {v}
    ax_S = boundary_edges(ax_U, edges)
    ax_b = f[v]
    steps.append({"op":"axiom","v":v,"S":ax_S,"b":ax_b,"rank_upper":2})
    if i == 0:
      U = {v}
      acc_S = ax_S
      acc_b = ax_b
      steps.append({"op":"set_acc","U_size":len(U),"acc_S":acc_S,"acc_b":acc_b})
      continue

    # XOR-resolve accumulator with axiom
    new_S, new_b = xor_clause(acc_S, acc_b, ax_S, ax_b)
    U = U.symmetric_difference(ax_U)
    steps.append({"op":"xor_res","U_size":len(U),"acc_S_len":len(acc_S),"ax_S_len":len(ax_S),
                  "new_S_len":len(new_S),"new_b":new_b,"c_U":c_of(U)})
    acc_S, acc_b = new_S, new_b
    steps.append({"op":"drop_parents_keep_acc","rank_upper":1})

  final = {"final_S_len":len(acc_S),"final_b":acc_b,"expect_S_len":0,"expect_b":1}
  ok = (len(acc_S) == 0 and acc_b == 1)
  out = {
    "graph": args.graph,
    "n": n,
    "m": len(edges),
    "d": args.d if args.graph=="rr" else 4,
    "seed": args.seed,
    "root": args.root,
    "order_prefix": order[:20],
    "final": final,
    "ok": ok,
    "steps": steps[:2000],
  }
  with open(args.out, "w") as f_out:
    json.dump(out, f_out, indent=2)
  if not ok:
    raise SystemExit("refutation did not end at [∅,1]")

if __name__ == "__main__":
  main()
