# Rate-Thick Binary Kappa Candidate

Status: FRONTIER_OPEN / BINARY_KAPPA_POSITIVITY_PROVED

## Candidate coefficient

```lean
binaryKappaCandidate λ =
  - (1 - λ) * Real.log (1 - λ) - λ * Real.log λ
General m-ary coefficient
mAryKappaCandidate m λ =
  - (1 - ((m : ℝ) - 1) * λ) *
      Real.log (1 - ((m : ℝ) - 1) * λ)
    - ((m : ℝ) - 1) * λ * Real.log λ
Isolated targets
BinaryKappaPositiveTarget λ
EntropyMinDominatesBinaryCoefficientTarget m λ
BinaryCandidateUniformFiberMassBound λ
Closed conditional consequences
BinaryKappaCandidateCertificateInputs λ →
UniformRateThickFiberLowerBoundCertificate λ
BinaryKappaCandidateCertificateInputs λ →
RateThickFiberCoercivity λ
RankRateBridgeLaw λ →
BinaryKappaCandidateCertificateInputs λ →
UniversalFiberEntropyGap λ
Boundary
Binary kappa positivity proved under `BinaryKappaAdmissible λ`.
Does not prove:
positivity of binaryKappaCandidate λ
entropy-minimum domination
uniform fiber-mass bound
unrestricted certificate construction
unrestricted RateThickFiberCoercivity λ
unrestricted UniversalFiberEntropyGap λ
unrestricted Chronos-RR
H4.1/FGL
P vs NP
any Clay problem
