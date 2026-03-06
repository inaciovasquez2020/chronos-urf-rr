import json, random, argparse, networkx as nx

def load_graph(path):
    with open(path) as f:
        g=json.load(f)
    G=nx.Graph()
    G.add_edges_from(g["edges"])
    return G

def random_lift(base,n,seed):
    rng=random.Random(seed)
    G=nx.Graph()
    for u,v in base.edges():
        perm=list(range(n))
        rng.shuffle(perm)
        for i in range(n):
            G.add_edge((u,i),(v,perm[i]))
    return G

def short_cycle_sample(G,steps=200000,max_len=12):
    nodes=list(G.nodes())
    cycles=0
    for _ in range(steps):
        v=random.choice(nodes)
        x=v
        seen={v:0}
        for d in range(1,max_len+1):
            nbr=random.choice(list(G[x]))
            if nbr in seen:
                cycles+=1
                break
            seen[nbr]=d
            x=nbr
    return cycles

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--base_json")
    ap.add_argument("--lift_n",type=int)
    ap.add_argument("--seed",type=int)
    ap.add_argument("--steps",type=int,default=200000)
    ap.add_argument("--out")
    args=ap.parse_args()

    base=load_graph(args.base_json)
    G=random_lift(base,args.lift_n,args.seed)

    c=short_cycle_sample(G,args.steps)

    out={
        "lift_n":args.lift_n,
        "steps":args.steps,
        "sampled_cycles":c
    }

    with open(args.out,"w") as f:
        json.dump(out,f,indent=2)

    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
