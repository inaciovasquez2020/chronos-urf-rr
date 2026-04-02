#!/usr/bin/env bash
set -euo pipefail
repo_url="${1:-https://github.com/inaciovasquez2020/chronos-urf-rr.git}"
tag="${2:-audit-ready-2026-03-31}"
workdir="$(mktemp -d)"
trap 'rm -rf "$workdir"' EXIT
cd "$workdir"
git clone "$repo_url" chronos-urf-rr
cd chronos-urf-rr
git checkout "$tag"
lake update
lake build
echo "INDEPENDENT_VERIFICATION_PASS"
