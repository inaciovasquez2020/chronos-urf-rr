#!/usr/bin/env python3
import random
from ic_extension_suite import (
    cycle_graph,
    random_d_regular,
    build_tseitin_cnf,
    balanced_split,
    build_search_function_table,
    log2_ceil,
)

def fooling_set_greedy_restarts(table, restarts=64, seed=0):
    items = [(x,y,o) for ((x,y),o) in table.items()]
    best = 0
    rng = random.Random(seed)

    def greedy(order):
        S = []
        for (x,y,o) in order:
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

    base = greedy(sorted(items, key=lambda t: (t[2], t[0], t[1])))
    best = max(best, base)

    for _ in range(restarts):
        rng.shuffle(items)
        best = max(best, greedy(items))

    return best

def cc_lb_bits_for_tseitin(G, split_seed=42, greedy_restarts=64, greedy_seed=0):
    f = [0]*G.n
    f[0] = 1
    cnf, m = build_tseitin_cnf(G, f)
    X, Y = balanced_split(m, seed=split_seed)
    table = build_search_function_table(cnf, m, X, Y)
    fs = fooling_set_greedy_restarts(table, restarts=greedy_restarts, seed=greedy_seed)
    return log2_ceil(fs)

def main():
    Ns = [6,8,10,12,14,16,18]
    EXP_SEEDS = [1,2,3,4,5]
    SPLIT_SEED = 42
    RESTARTS = 96

    print("n\tcycle_bits\texp_min\texp_med\texp_max")

    for n in Ns:
        cycle_bits = cc_lb_bits_for_tseitin(
            cycle_graph(n),
            split_seed=SPLIT_SEED,
            greedy_restarts=RESTARTS,
            greedy_seed=1000+n,
        )

        vals = []
        for s in EXP_SEEDS:
            Gr = random_d_regular(n, 3, seed=10000*n + s)
            vals.append(cc_lb_bits_for_tseitin(
                Gr,
                split_seed=SPLIT_SEED,
                greedy_restarts=RESTARTS,
                greedy_seed=20000*n + s,
            ))
        vals.sort()
        exp_min = vals[0]
        exp_med = vals[len(vals)//2]
        exp_max = vals[-1]

        print(f"{n}\t{cycle_bits}\t{exp_min}\t{exp_med}\t{exp_max}")

if __name__ == "__main__":
    main()
