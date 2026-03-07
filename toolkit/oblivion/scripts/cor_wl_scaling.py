#!/usr/bin/env python3
import json
import argparse
import random
from collections import Counter

from wl_k_test import load_graph, wl2

def sample_subgraph(adj,size):
    nodes=random.sample(range(len(adj)),size)
    idmap={v:i for i,v in enumerate(nodes)}
    new=[set() for _ in nodes]
    for v in nodes:
        for w in adj[v]:
            if w in idmap:
                new[idmap[v]].add(idmap[w])
    return new

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--graph_json",required=True)
    p.add_argument("--samples",default="50,100,200,400")
    args=p.parse_args()

    adj=load_graph(args.graph_json)

    sizes=[int(x) for x in args.samples.split(",")]

    for s in sizes:
        sub=sample_subgraph(adj,s)
        colors=wl2(sub)
        print(json.dumps({
            "sample":s,
            "distinct_colors":len(set(colors))
        }))

if __name__=="__main__":
    main()
