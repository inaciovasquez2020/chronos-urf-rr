import networkx as nx

def radius_signature(G, v, R):
    lengths = nx.single_source_shortest_path_length(G, v, cutoff=R)
    sub = G.subgraph(lengths.keys())
    degs = sorted([d for _, d in sub.degree()])
    return tuple(degs)

def detect_collisions(G, R):
    sigs = {}
    for v in G.nodes():
        s = radius_signature(G, v, R)
        sigs.setdefault(s, []).append(v)
    return {k:v for k,v in sigs.items() if len(v) > 1}

if __name__ == "__main__":
    G = nx.random_regular_graph(3, 60)
    collisions = detect_collisions(G, 2)
    print("collision_types:", len(collisions))
    for k,v in collisions.items():
        print(len(v))
