#!/usr/bin/env bash
set -e

GRAPH=toolkit/oblivion/results/rr_n12000_d4_seed9.json
R=6

echo "=== Cycle overlap structure ==="
python3 toolkit/oblivion/scripts/cycle_overlap_graph.py \
  --graph_json $GRAPH \
  --R $R

echo "=== Component rank decomposition ==="
python3 toolkit/oblivion/scripts/cycle_component_rank.py \
  --graph_json $GRAPH \
  --R $R

echo "=== WL² visibility (sample 250) ==="
python3 toolkit/oblivion/scripts/wl_k_test.py \
  --graph_json $GRAPH \
  --k 2 \
  --sample 250

echo "=== WL² visibility (sample 500) ==="
python3 toolkit/oblivion/scripts/wl_k_test.py \
  --graph_json $GRAPH \
  --k 2 \
  --sample 500
