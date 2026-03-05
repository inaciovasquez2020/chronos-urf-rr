import argparse, json, random

def random_lift(base_cycle, lift_size):
    edges = []
    for i in range(base_cycle):
        perm = list(range(lift_size))
        random.shuffle(perm)
        for j in range(lift_size):
            u = i*lift_size + j
            v = ((i+1)%base_cycle)*lift_size + perm[j]
            edges.append((u,v))
    return edges

def run(base_cycle, lift_size, samples):
    results = []
    for _ in range(samples):
        edges = random_lift(base_cycle,lift_size)
        results.append(len(edges))
    return results

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--base-cycle",type=int)
    p.add_argument("--lift-size",type=int)
    p.add_argument("--samples",type=int)
    p.add_argument("--R",type=int)
    p.add_argument("--out")
    a=p.parse_args()
    res=run(a.base_cycle,a.lift_size,a.samples)
    json.dump(res,open(a.out,"w"))
