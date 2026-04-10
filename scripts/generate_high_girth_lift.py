import random
import json

def random_lift(n):
    # 3-regular base: simple cycle with chords → approximate expander seed
    edges = [(i, (i+1)%n) for i in range(n)]
    edges += [(i, (i+2)%n) for i in range(n)]
    lift_edges = []
    for u,v in edges:
        if random.choice([0,1]):
            lift_edges.append((u, v))
            lift_edges.append((u+n, v+n))
        else:
            lift_edges.append((u, v+n))
            lift_edges.append((u+n, v))
    return lift_edges

def main():
    n = 20
    edges = random_lift(n)
    out = {"n": n, "edges": edges}
    with open("artifacts/high_girth_lift.json","w") as f:
        json.dump(out,f,indent=2)

if __name__ == "__main__":
    main()
