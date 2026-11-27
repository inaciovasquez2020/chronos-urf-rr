# Cosmology–Chronos causal projection obstruction

## Classification

Scoped mathematical certificate: LEAN_VERIFIED on macOS.
Fresh CI reproduction required before integration.

Continuum measure formalization, physical extra-dimension
detection and independent novelty remain OPEN.

## Mathematical results

For a five-dimensional flat-coordinate causal diamond,
projection onto time and three spatial coordinates loses
information about causal comparability.

The certificate establishes:

- An explicit collision between comparable and incomparable
  event pairs with identical visible coordinates.
- Impossibility of a universally correct visible decoder.
- Algebraic equivalence of the piecewise strip-area expression
  and its positive-part closed form.
- Probability bounds under positive interval widths and
  nonnegative separation threshold.
- Optimal binary pointwise decision loss min(p,1-p).

For positive hidden-coordinate half-widths a,b and d >= 0,
the algebraic strip probability is

    p = 1 - ((a+b-d)_+^2 - (|a-b|-d)_+^2)/(4*a*b).

The source defines the piecewise strip-area expression
algebraically. Its identification with Lebesgue rectangle
strip area is a separate geometric integration argument,
not a theorem formalized by this Lean certificate.

The pointwise decision rule is verified, not a full
measure-theoretic Bayes-risk theorem.

## Pinned mathematical antecedents

DFM-MKC Cosmology expanding-circle geometry:
https://github.com/inaciovasquez2020/dfm-mkc-cosmology/blob/bda11ce1347aeda076571de137e99ac93cd7e723/research/5d/EXPANDING_CIRCLE_STATUS.md

Chronos direct 5D comparable-pair calculation:
https://github.com/inaciovasquez2020/chronos-urf-rr/blob/5a88ac8e790a2bef5da5b03b538a64ce08afdf12/docs/status/CHRONOS_DIRECT_5D_COMPARABLE_PAIRS.md

URF-Core information-recovery methodology:
https://github.com/inaciovasquez2020/urf-core/blob/9b9e2d7cbc59c466009c659de53a03985858cc51/lean/URF/Foundation/CyclePartitionRadiusMinimax.lean

These are mathematical antecedents, not imported software
dependencies of this standalone certificate.

## Verification

Lean 4.29.0
Mathlib 69cbc416b3f58ba11e331db067644d0508e78341
Original Mac Chronos HEAD:
a999b816df08bc393036cc7ebe8d0a6ed1939b6b

11 declarations verified using only standard Lean axioms.
Original verified source and receipt preserved byte-for-byte.

With pinned dependencies available:

    (cd receipt && shasum -a 256 -c SHA256SUMS)
    lake build
    lake env lean receipt/CausalProjection.lean > fresh.log 2>&1
    python3 audit.py fresh.log

## Non-claims

No physical fifth dimension, emergent spacetime derivation,
cosmological observation fit, exact integrated Bayes risk,
or rejection of four-dimensional relativity is established.

Repository-wide research status remains unchanged.
