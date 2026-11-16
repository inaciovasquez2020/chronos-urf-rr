# Expanding-circle scalar signal benchmark

The expanding-circle model gives two signal cases with identical visible coordinates. A modeled scalar pulse reaches the near detector by the deadline. The far detector is outside the pulse's light cone. The finite-support benchmark checks the separation and response bounds in conformal coordinates.

Replay from the repository root with `python3 -B research/event_first/chronos_signal_benchmark.py`. The standalone script uses Python's standard library. It embeds and checks the model note from DFM–MKC revision `1714d0e17ed4c4bfa7aff01019ffacca23397aaf` and the evidence and classifier modules from URF-AI revision `b0fd6ef97cf0b73658ad7067d0272084c2d60622`.

The standalone replay passed all 50 exact arithmetic cases, verified all three source blobs, and produced `BENCHMARK_MATCH_ONLY`. The rational detector threshold is `1/240` in the normalized rescaled field units. The evidence digest is `4c7e2db5f9ad9fd8a9439dc1169eda75cbbe80524c8bb247ac220e7fcb558f90`.

The replay checks the finite-support geometry and the arithmetic used in the response bound under the assumed retarded scalar kernel. Physical coupling and detector calibration remain open. Lean verification was not run.

## What the detector can distinguish

Write the rescaled field and source as Fourier series on the circle, using modes `exp(i n y)` for integer `n`. The circle derivative acts on mode `n` by multiplication by `-n²`. The retarded field equation for each coefficient is therefore

```text
(∂η² − Δx + n²) χ_n = J_n.
```

For a real field, negative modes are the complex conjugates of positive modes. With the same retarded conditions, a 4D model containing this tower has the same mode solutions. A translated source profile centered at `y_S` contributes Fourier phases `exp(−i n y_S)`. A detector translated to `y_D` applies phases `exp(i n y_D)` along with its profile weights. Summing the 4D responses against the same detector weights gives exactly the 5D readout for the smooth profiles in the linear benchmark. The `n = 0` term is independent of the separation around the circle.

The deadline test distinguishes the specified signals from the matched zero-mode response. The full 4D tower with matched couplings reproduces the linear detector data. A physical interpretation of those modes requires additional evidence.
