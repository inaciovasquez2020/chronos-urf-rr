#!/usr/bin/env python3

from cfi_pair_generator import cfi_pair_on_cycle

def cycle_parity(G):
    visited = set()
    parent = {}
    parity = {}

    for start in G:
        if start in visited:
            continue

        stack = [(start, None)]
        parity[start] = 0

        while stack:
            v, p = stack.pop()
            if v in visited:
                continue
            visited.add(v)

            for u in G[v]:
                if u == p:
                    continue
                if u not in parity:
                    parity[u] = parity[v] ^ 1
                    parent[u] = v
                    stack.append((u, v))
                else:
                    # detect cycle parity
                    if parity[u] == parity[v]:
                        return 1  # odd cycle / twist detected

    return 0

def run():
    G0, G1 = cfi_pair_on_cycle(6, {(0,1)})

    print("cycle_parity G0:", cycle_parity(G0))
    print("cycle_parity G1:", cycle_parity(G1))

if __name__ == "__main__":
    run()
