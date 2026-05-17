import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Chronos.Frontier.RateThickFiberCoercivityCertificate

namespace Chronos
namespace Frontier
namespace RateThickBinaryKappaCandidate

noncomputable def binaryKappaCandidate (lam : ℝ) : ℝ :=
  - (1 - lam) * Real.log (1 - lam) - lam * Real.log lam

noncomputable def mAryKappaCandidate (m : Nat) (lam : ℝ) : ℝ :=
  - (1 - ((m : ℝ) - 1) * lam) *
      Real.log (1 - ((m : ℝ) - 1) * lam)
    - ((m : ℝ) - 1) * lam * Real.log lam

def BinaryKappaAdmissible (lam : ℝ) : Prop :=
  0 < lam ∧ lam ≤ (1 : ℝ) / 2

def MAryKappaAdmissible (m : Nat) (lam : ℝ) : Prop :=
  2 ≤ m ∧ 0 < lam ∧ lam ≤ (1 : ℝ) / (m : ℝ)

def BinaryKappaPositiveTarget (lam : ℝ) : Prop :=
  BinaryKappaAdmissible lam → 0 < binaryKappaCandidate lam

def MAryKappaPositiveTarget (m : Nat) (lam : ℝ) : Prop :=
  MAryKappaAdmissible m lam → 0 < mAryKappaCandidate m lam

def EntropyMinDominatesBinaryCoefficientTarget (m : Nat) (lam : ℝ) : Prop :=
  MAryKappaAdmissible m lam →
    mAryKappaCandidate m lam ≥ binaryKappaCandidate lam

def BinaryCandidateUniformFiberMassBound (lam : ℝ) : Prop :=
  ∀ sys : DynamicalSystem,
    RateThickClass lam sys →
      NonNullFiberWitness sys →
        sys.fiberEntropyMass ≥ binaryKappaCandidate lam

def BinaryKappaCandidateCertificateInputs (lam : ℝ) : Prop :=
  0 < binaryKappaCandidate lam ∧
    BinaryCandidateUniformFiberMassBound lam

theorem uniformLowerBoundCertificate_from_binaryCandidateInputs
    (lam : ℝ)
    (h : BinaryKappaCandidateCertificateInputs lam) :
    RateThickFiberCoercivityCertificate.UniformRateThickFiberLowerBoundCertificate lam := by
  rcases h with ⟨hpos, hbound⟩
  exact ⟨binaryKappaCandidate lam, hpos, hbound⟩

theorem rateThickFiberCoercivity_from_binaryCandidateInputs
    (lam : ℝ)
    (h : BinaryKappaCandidateCertificateInputs lam) :
    RateThickFiberCoercivity lam := by
  exact
    RateThickFiberCoercivityCertificate.rateThickFiberCoercivity_from_uniformLowerBoundCertificate
        lam
        (uniformLowerBoundCertificate_from_binaryCandidateInputs lam h)

theorem universalFiberEntropyGap_from_binaryCandidateInputs
    (lam : ℝ)
    (h_bridge : RankRateBridgeLaw lam)
    (h : BinaryKappaCandidateCertificateInputs lam) :
    UnrestrictedRateThickCoercivityRoute.UniversalFiberEntropyGap lam := by
  exact
    RateThickFiberCoercivityCertificate.universalFiberEntropyGap_from_uniformLowerBoundCertificate
        lam
        h_bridge
        (uniformLowerBoundCertificate_from_binaryCandidateInputs lam h)

def FrontierStatus : String :=
  "FRONTIER_OPEN / BINARY_KAPPA_CANDIDATE_ONLY"

def Boundary : String :=
  "Candidate coefficient surface only; does not prove positivity of the candidate, does not prove entropy-minimum domination, does not prove the uniform fiber-mass bound, does not construct the unrestricted certificate, does not prove unrestricted RateThickFiberCoercivity, unrestricted UniversalFiberEntropyGap, unrestricted Chronos-RR, H4.1/FGL, P vs NP, or any Clay problem."

end RateThickBinaryKappaCandidate
end Frontier
end Chronos
