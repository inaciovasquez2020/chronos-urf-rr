# Premature response of a finite circle-mode tower

This extends [the scalar signal benchmark](chronos_signal_benchmark.md). For each integer cutoff N ≥ 1, the construction below gives a local scalar readout that vanishes in the full expanding-circle model and has magnitude greater than N(N+1)(2N+1)/600 in its Fourier truncation. The profiles and deadline depend on N.

## Source and detector

Use the rescaled retarded wave equation in conformal coordinates. Center the source and detector at the same visible spatial position and separate their circle centers by δ = 1/(2N). Set the nominal conformal time separation to T = 1/(4N). Take matching, separable, nonnegative smooth profiles of unit integral, with time half-width and combined spatial support radius bounded by 1/(64N). Place the supports within the conformal time domain.

The pointwise time separation is between 7/(32N) and 9/(32N). The visible spatial separation is at most 1/(32N), while the shortest circle separation is at least 15/(32N). Every pair is therefore strictly inside the visible light cone and outside the full light cone. The full retarded response is zero.

## Finite tower

The zero-mode kernel is supported on the visible light cone and gives zero on these supports. For n ≥ 1, the massive retarded kernel inside that cone is

```text
−n² J₁(z)/(4π z),   z = n sqrt((actual time separation)² − (visible separation)²).
```

For 1 ≤ n ≤ N, we have 0 < z ≤ 9/32 and J₁(z)/z ≥ 1/2 − z²/16 > 49/100 by the alternating series. With Fourier coefficients defined by the unnormalized integral of the unit-mass circle profile p, the paired modes n and −n have the angular prefactor |p̂(n)|² cos(nδ)/π. The circle support gives |p̂(n)| ≥ cos(1/64) > 99/100. Also cos(nδ) ≥ 7/8 since nδ ≤ 1/2. The prefactors are positive and all massive contributions have negative sign. Their individual magnitudes exceed n²/100, using π² < 10 and the exact arithmetic below. The magnitude of the sum consequently exceeds N(N+1)(2N+1)/600.

A magnitude threshold of 1/200 distinguishes the two model responses for every N ≥ 1 when the absolute readout error is below 1/480 in the normalized rescaled units.

## Exact arithmetic replay

```python
from fractions import Fraction as F

assert 0 < F(1, 32) < F(7, 32) <= F(9, 32) < F(15, 32)
assert F(1, 2) - F(9, 32)**2 / 16 > F(49, 100)
assert 1 - F(1, 64)**2 / 2 > F(99, 100)
assert 1 - F(1, 2)**2 / 2 == F(7, 8)
assert F(22, 7)**2 < 10
assert F(49, 100) * F(99, 100)**2 * F(7, 8) / 40 > F(1, 100)
assert F(1, 480) < F(1, 200) < F(1, 100) - F(1, 480)
print("FINITE_TOWER_LEAKAGE_MARGINS = PASS")
```

The replay checks the rational inequalities used in the analytic argument. This benchmark concerns the rescaled linear scalar field and a cutoff-dependent experimental design. The minimum cutoff for a fixed detector, physical circle coupling, and detector calibration remain open.
