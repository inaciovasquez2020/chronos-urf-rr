# docs/oblivion_atom/experiment_summary_R6.md

Experiment Summary (R=6)

1. COR↔FO^k coupling proxy (ball-signature) artifacts

- toolkit/oblivion/results/cor_fok_coupling_rr_R6.json
- toolkit/oblivion/results/cor_fok_coupling_twolift_R6.json
- tag: oblivion-cor-fok-coupling-v1

2. Random-lift COR growth scan (lower bound via BFS cycle packing)

Commands (example)

python3 toolkit/oblivion/scripts/random_lift_cor_scan.py \
  --base_json toolkit/oblivion/results/rr_base_d4.json \
  --lift_n 10000 \
  --seed 7 \
  --R 6 --L 12 \
  --target_cycles 4000 \
  --vertex_sample 60000 \
  --rank_trials 3 --rank_block 16 --rank_steps 64 \
  --out toolkit/oblivion/results/cor_scan_lift_n10000_R6.json

python3 toolkit/oblivion/scripts/random_lift_cor_scan.py \
  --base_json toolkit/oblivion/results/rr_base_d4.json \
  --lift_n 100000 \
  --seed 7 \
  --R 6 --L 12 \
  --target_cycles 25000 \
  --vertex_sample 200000 \
  --rank_trials 3 --rank_block 16 --rank_steps 64 \
  --out toolkit/oblivion/results/cor_scan_lift_n100000_R6.json

Outputs

- packed_cycles: m
- cor_lb_from_packing: m
- rank_lb_incidence: (heuristic lower bound; here equals m under diagonal assignment)

3. FO^k signature collisions integrated into cor_fok_coupling_test.py

New fields (in fok_proxy)

- collisions
- multiplicity_histogram
- top_collisions
