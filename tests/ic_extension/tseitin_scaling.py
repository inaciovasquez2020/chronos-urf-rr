#!/usr/bin/env python3
import math
import random
from ic_extension_suite import (
    cycle_graph,
    random_d_regular,
    build_tseitin_cnf,
    balanced_split,
    build_search_function_table,
    fooling_set_greedy,
    log2_ceil
)

def run_instance(name, G):
    f = [0]*G.n
    f[0] = 1
    cnf, m = build_tseitin_cnf(G, f)
    X, Y = balanced_split(m, seed=42)
    table = build_search_function_table(cnf, m, X, Y)
    fs = fooling_set_greedy(table, 1<<len(X), 1<<len(Y))
    return log2_ceil(fs)

def main():
    print("n\tcycle_bits\texpander_bits")
    for n in [6,8,10,12,14]:
        # Cycle
        Gc = cycle_graph(n)
        cycle_bits = run_instance("cycle", Gc)

        # Random 3-regular
        try:
            Gr = random_d_regular(n, 3, seed=n)
            exp_bits = run_instance("rand3", Gr)
        except:
            exp_bits = -1

        print(f"{n}\t{cycle_bits}\t{exp_bits}")

if __name__ == "__main__":
    main()
