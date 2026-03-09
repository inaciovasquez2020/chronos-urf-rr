#!/usr/bin/env bash
set -e

echo "===== URF / Chronos Lean Verification Test ====="

echo "1. Cleaning previous build..."
lake clean

echo "2. Fetching dependencies..."
lake update

echo "3. Building entire project..."
lake build

echo "4. Verifying key modules..."

lean --run lean/Oblivion/Cycle/CycleIncidenceMatrix.lean
echo "✓ CycleIncidenceMatrix compiled"

lean --run lean/Oblivion/Cycle/CyclePackingBound.lean
echo "✓ CyclePackingBound compiled"

lean --run lean/Oblivion/Cycle/LocalCycleWitness.lean
echo "✓ LocalCycleWitness compiled"

lean --run lean/FOk/Cycle/CycleDefinability.lean
echo "✓ CycleDefinability compiled"

lean --run lean/Chronos/EntropyDepthClosure.lean
echo "✓ Chronos EntropyDepth closure compiled"

echo "5. Running full Lean environment check..."
lean --version

echo "===== ALL TESTS PASSED ====="
