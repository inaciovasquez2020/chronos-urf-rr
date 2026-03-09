#!/usr/bin/env bash
set -euo pipefail

lake clean
lake update
lake build

for f in \
  lean/Oblivion/Cycle/CycleIncidenceMatrix.lean \
  lean/Oblivion/Cycle/CyclePackingBound.lean \
  lean/Oblivion/Cycle/LocalCycleWitness.lean \
  lean/Oblivion/Cycle/CycleBasisExtraction.lean \
  lean/Oblivion/Cycle/CycleBasisLinearIndependence.lean \
  lean/Oblivion/Cycle/TwoCycleLocalWitness.lean \
  lean/FOk/Cycle/CycleDefinability.lean \
  lean/FOk/Cycle/CycleWitnessFormula.lean \
  lean/FOk/Cycle/CycleWitnessCorrectness.lean \
  lean/Oblivion/Rigidity/LocalTypeExplosionProof.lean \
  lean/Oblivion/Rigidity/CycleOverlapRankRigidity_Strong.lean \
  lean/Chronos/EntropyDepthClosure.lean \
  lean/Chronos/EntropyDepthExplosion.lean
do
  lean "$f" >/dev/null
  echo "PASS $f"
done
