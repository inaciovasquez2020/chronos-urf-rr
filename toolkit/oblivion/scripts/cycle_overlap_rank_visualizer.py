import argparse, json, random

def random_regular_graph(n, d):
    stubs = []
    for v in range(n):
        stubs += [v]*d
    random.shuffle(stubs)
    edges = []
    for i in range(0, len(stubs), 2):
        if i+1 < len(stubs):
            u = stubs[i]
            v = stubs[i+1]
            if u != v:
                edges.append((u,v))
    return edges

def cycle_overlap_rank(edges, R):
    return len(edges)

def run(n, d, R):
    edges = random_regular_graph(n,d)
    cor = cycle_overlap_rank(edges,R)
    return {"n": n, "degree": d, "R": R, "cycle_overlap_rank": cor}

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int)
    p.add_argument("--degree", type=int)
    p.add_argument("--R", type=int)
    p.add_argument("--out", required=True)
    a = p.parse_args()

    result = run(a.n, a.degree, a.R)

    with open(a.out,"w") as f:
        json.dump(result,f)
