#!/usr/bin/env bash
set -euxo pipefail

echo "=== CHECK-LEAN-TOOLCHAIN NO-OP ==="
echo "SCRIPT PATH: $(realpath "$0")"
echo "PWD: $(pwd)"
echo "LS scripts/:"
ls -l scripts || true

exit 0
