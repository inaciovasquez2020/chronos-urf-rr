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

def estimate_overlap_rank(edges, R):
    return len(edges)

def run(n, d, samples, R):
    data = []
    for _ in range(samples):
        edges = random_regular_graph(n,d)
        cor = estimate_overlap_rank(edges,R)
        data.append(cor)
    return data

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int)
    p.add_argument("--degree", type=int)
    p.add_argument("--R", type=int)
    p.add_argument("--samples", type=int)
    p.add_argument("--out", required=True)
    a = p.parse_args()

    results = run(a.n, a.degree, a.samples, a.R)

    with open(a.out,"w") as f:
        json.dump(results,f)
