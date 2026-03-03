#!/usr/bin/env python3
import math
from ic_extension_suite import (
    cycle_graph,
    build_tseitin_cnf,
    balanced_split,
    build_search_function_table,
    log2_ceil,
)

# Deterministic 3-regular circulant graph
def circulant_3_regular(n):
    edges = set()
    for i in range(n):
        edges.add(tuple(sorted((i, (i+1) % n))))
        edges.add(tuple(sorted((i, (i-1) % n))))
        if n % 2 == 0:
            edges.add(tuple(sorted((i, (i + n//2) % n))))
    class G:
        pass
    G.n = n
    G.edges = list(edges)
    return G

def fooling_set_greedy(table):
    items = [(x,y,o) for ((x,y),o) in table.items()]
    S = []
    for (x,y,o) in items:
        good = True
        for (x1,y1,o1) in S:
            if o1 == o:
                good = False
                break
            if table.get((x1,y), None) == o1 and table.get((x,y1), None) == o:
                good = False
                break
        if good:
            S.append((x,y,o))
    return len(S)

def cc_lb_bits(G):
    f = [0]*G.n
    f[0] = 1
    cnf, m = build_tseitin_cnf(G, f)
    X, Y = balanced_split(m, seed=42)
    table = build_search_function_table(cnf, m, X, Y)
    fs = fooling_set_greedy(table)
    return log2_ceil(fs)

def main():
    print("n\tcycle_bits\texpander_bits")
    for n in [6,8,10,12,14,16,18]:
        cycle_bits = cc_lb_bits(cycle_graph(n))
        exp_bits   = cc_lb_bits(circulant_3_regular(n))
        print(f"{n}\t{cycle_bits}\t{exp_bits}")

if __name__ == "__main__":
    main()
