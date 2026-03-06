# Geometry Signature Usage

The geometry signature tools allow classification of graph geometry
via local cycle structure.

## 1. Compute signature

python3 toolkit/oblivion/scripts/geometry_signature_scan.py \
--graph_json GRAPH.json \
--root 0 \
--Rmax 12 \
> signature.json

Output entries:

{
  "R": R,
  "|B_R|": vertex_count,
  "beta1": cycle_rank,
  "rho": cycle_density
}

## 2. Plot geometry profile

python3 toolkit/oblivion/scripts/graph_geometry_plot.py \
--graph_json GRAPH.json \
--max_R 12 \
--out geometry.png

## 3. Interpret

Tree regime
beta1 ≈ 0

Sheet regime
|B_R| ~ R²

Expander regime
|B_R| ~ Δ^R and rho stabilizes

## 4. Role in Oblivion Atom

Large cycle density across growing balls indicates
cycle-overlap rank expansion, which drives FO^k type diversity.

