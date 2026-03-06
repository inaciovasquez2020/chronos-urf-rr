#!/usr/bin/env bash
set -euo pipefail

python3 scripts/oblivion_atom/random_lift_cor_experiment.py
python3 scripts/oblivion_atom/random_lift_cor_rank_proxy.py
python3 scripts/oblivion_atom/cor_growth_scan.py
python3 scripts/oblivion_atom/expander_cor_test.py
