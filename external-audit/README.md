# Independent Verification Protocol

## Goal
Replay the full Chronos core build from a clean clone and confirm:
1. coercivity layer compiles
2. spectral gap layer compiles
3. normalization layer compiles
4. entropy model layer compiles
5. ED Omega(n) layer compiles

## Independent Verifier Commands
```bash
git clone https://github.com/inaciovasquez2020/chronos-urf-rr.git
cd chronos-urf-rr
git checkout audit-ready-2026-03-31
lake update
lake build
Expected Modules
lean/Chronos/FinalCoercivity.lean
lean/Chronos/SpectralGap.lean
lean/Chronos/SpectralGapAxiomReplacement.lean
lean/Chronos/EntropyModelGeneral.lean
lean/Chronos/EDOmegaN.lean
lean/Chronos.lean
Pass Criterion
lake build exits successfully with no source modifications.
