from collections import deque
import json

ADJ_PLUS = {
    0: [1, 4, 5],
    1: [0, 2, 6],
    2: [1, 3, 7],
    3: [2, 4, 8],
    4: [0, 3, 9],
    5: [0, 7, 8],
    6: [1, 8, 9],
    7: [2, 5, 9],
    8: [3, 5, 6],
    9: [4, 6, 7],
}

ADJ_MINUS = {
    0: [1, 4, 5],
    1: [0, 2, 6],
    2: [1, 3, 7],
    3: [2, 4, 8],
    4: [0, 3, 9],
    5: [0, 6, 7],
    6: [1, 5, 8],
    7: [2, 5, 9],
    8: [3, 6, 9],
    9: [4, 7, 8],
}

PAIRING = {v: v for v in ADJ_PLUS}
RADIUS = 2

def ball_profile(adj, root, radius):
    dist = {root: 0}
    q = deque([root])
    while q:
        u = q.popleft()
        if dist[u] == radius:
            continue
        for w in adj[u]:
            if w not in dist:
                dist[w] = dist[u] + 1
                q.append(w)
    layers = {}
    for v, d in dist.items():
        layers.setdefault(d, 0)
        layers[d] += 1
    return tuple(sorted(layers.items()))

def main():
    cert = []
    ok = True
    for v_plus, v_minus in sorted(PAIRING.items()):
        p_plus = ball_profile(ADJ_PLUS, v_plus, RADIUS)
        p_minus = ball_profile(ADJ_MINUS, v_minus, RADIUS)
        same = p_plus == p_minus
        ok = ok and same
        cert.append({
            "v_plus": v_plus,
            "v_minus": v_minus,
            "same_profile": same,
            "profile_plus": p_plus,
            "profile_minus": p_minus,
        })

    out = {
        "radius": RADIUS,
        "local_property_checked": ok,
        "pairs_checked": len(cert),
        "certificate": cert,
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    # observational certificate only; do not fail
    return

if __name__ == "__main__":
    main()
