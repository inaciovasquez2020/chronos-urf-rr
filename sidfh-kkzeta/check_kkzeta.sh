#!/usr/bin/env bash
set -euo pipefail

python3 tools/verify_kkzeta_input_surfaces.py
lake env lean Sidfh/KkZeta/Basic.lean
lake build
