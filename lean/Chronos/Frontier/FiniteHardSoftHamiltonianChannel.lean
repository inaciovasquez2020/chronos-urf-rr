import Mathlib
import Chronos.Frontier.FiniteHardSoftEmissionChannel

namespace Chronos.Frontier

noncomputable section

inductive FiniteExchangeBasis where
  | vacuum
  | residual
  | hard
  | soft
deriving DecidableEq, Fintype

structure FiniteChargeConservingExchangeHamiltonian where
  frequency : Nat → ℝ
  duration : Nat → ℝ
  hardMixing : Nat → ℝ
  softMixing : Nat → ℝ
  mixingNormalization :
    ∀ k : Nat,
      hardMixing k ^ 2 + softMixing k ^ 2 = 1

def finiteExchangeCharge :
    FiniteExchangeBasis → ℝ
  | .vacuum => 0
  | .residual => 1
  | .hard => 1
  | .soft => 1

def finiteExchangeHamiltonianEntry
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat) :
    FiniteExchangeBasis →
      FiniteExchangeBasis →
        ℝ
  | .residual, .hard =>
      H.frequency k * H.hardMixing k
  | .hard, .residual =>
      H.frequency k * H.hardMixing k
  | .residual, .soft =>
      H.frequency k * H.softMixing k
  | .soft, .residual =>
      H.frequency k * H.softMixing k
  | _, _ => 0

theorem finiteExchangeHamiltonian_chargeCommutatorEntry
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat)
    (i j : FiniteExchangeBasis) :
    finiteExchangeHamiltonianEntry H k i j *
          finiteExchangeCharge j -
        finiteExchangeCharge i *
          finiteExchangeHamiltonianEntry H k i j =
      0 := by
  cases i <;> cases j <;>
    simp [
      finiteExchangeHamiltonianEntry,
      finiteExchangeCharge
    ]

def finiteExchangeAngle
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat) : ℝ :=
  H.frequency k * H.duration k

def finiteExchangeResidualStepAmplitude
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat) : ℝ :=
  Real.cos (finiteExchangeAngle H k)

def finiteExchangeHardStepAmplitude
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat) : ℝ :=
  H.hardMixing k *
    Real.sin (finiteExchangeAngle H k)

def finiteExchangeSoftStepAmplitude
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat) : ℝ :=
  H.softMixing k *
    Real.sin (finiteExchangeAngle H k)

theorem finiteExchangeLocalNormalization
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat) :
    finiteExchangeResidualStepAmplitude H k ^ 2 +
          finiteExchangeHardStepAmplitude H k ^ 2 +
          finiteExchangeSoftStepAmplitude H k ^ 2 =
      1 := by
  change
    Real.cos (H.frequency k * H.duration k) ^ 2 +
          (H.hardMixing k *
            Real.sin (H.frequency k * H.duration k)) ^ 2 +
          (H.softMixing k *
            Real.sin (H.frequency k * H.duration k)) ^ 2 =
      1
  calc
    Real.cos (H.frequency k * H.duration k) ^ 2 +
          (H.hardMixing k *
            Real.sin (H.frequency k * H.duration k)) ^ 2 +
          (H.softMixing k *
            Real.sin (H.frequency k * H.duration k)) ^ 2 =
        Real.cos (H.frequency k * H.duration k) ^ 2 +
          (H.hardMixing k ^ 2 + H.softMixing k ^ 2) *
            Real.sin (H.frequency k * H.duration k) ^ 2 := by
              ring
    _ =
        Real.cos (H.frequency k * H.duration k) ^ 2 +
          Real.sin (H.frequency k * H.duration k) ^ 2 := by
            rw [H.mixingNormalization k]
            ring
    _ = 1 :=
      Real.cos_sq_add_sin_sq
        (H.frequency k * H.duration k)

def finiteExchangeEmissionData
    (H : FiniteChargeConservingExchangeHamiltonian) :
    FiniteHardSoftEmissionData where
  residualStepAmplitude :=
    finiteExchangeResidualStepAmplitude H
  hardStepAmplitude :=
    finiteExchangeHardStepAmplitude H
  softStepAmplitude :=
    finiteExchangeSoftStepAmplitude H
  localNormalization :=
    finiteExchangeLocalNormalization H

def finiteExchangeResidualProbability
    (H : FiniteChargeConservingExchangeHamiltonian)
    (N : Nat) : ℝ :=
  finiteResidualAmplitudeModulusSq
    (finiteExchangeEmissionData H)
    N

def finiteExchangeHardProbability
    (H : FiniteChargeConservingExchangeHamiltonian)
    (N : Nat) : ℝ :=
  finiteHardEmissionProbability
    (finiteExchangeEmissionData H)
    N

def finiteExchangeSoftProbability
    (H : FiniteChargeConservingExchangeHamiltonian)
    (N : Nat) : ℝ :=
  finiteSoftEmissionProbability
    (finiteExchangeEmissionData H)
    N

theorem finiteExchangeProbabilityPartition
    (H : FiniteChargeConservingExchangeHamiltonian)
    (N : Nat) :
    finiteExchangeResidualProbability H N +
          finiteExchangeHardProbability H N +
          finiteExchangeSoftProbability H N =
      1 := by
  unfold
    finiteExchangeResidualProbability
    finiteExchangeHardProbability
    finiteExchangeSoftProbability
  nlinarith [
    finiteHardSoftEmissionProbabilityIdentity
      (finiteExchangeEmissionData H)
      N
  ]

structure FiniteHardSoftIsometryCertificate where
  residualProbability : ℝ
  hardProbability : ℝ
  softProbability : ℝ
  normalization :
    residualProbability +
          hardProbability +
          softProbability =
      1

def finiteExchangeIsometryCertificate
    (H : FiniteChargeConservingExchangeHamiltonian)
    (N : Nat) :
    FiniteHardSoftIsometryCertificate where
  residualProbability :=
    finiteExchangeResidualProbability H N
  hardProbability :=
    finiteExchangeHardProbability H N
  softProbability :=
    finiteExchangeSoftProbability H N
  normalization :=
    finiteExchangeProbabilityPartition H N

def finiteExchangeHardOnlyChannel
    (H : FiniteChargeConservingExchangeHamiltonian)
    (N : Nat) :
    FiniteLogicalDensityMatrix →
      FiniteLogicalDensityMatrix :=
  finiteDecodedHardOnlyChannel
    (finiteExchangeHardProbability H N)

def finiteExchangeSoftOnlyChannel
    (H : FiniteChargeConservingExchangeHamiltonian)
    (N : Nat) :
    FiniteLogicalDensityMatrix →
      FiniteLogicalDensityMatrix :=
  finiteDecodedHardOnlyChannel
    (finiteExchangeSoftProbability H N)

def finiteExchangeHardComplementChannel
    (H : FiniteChargeConservingExchangeHamiltonian)
    (N : Nat) :
    FiniteLogicalDensityMatrix →
      FiniteLogicalDensityMatrix :=
  finiteDecodedHardOnlyChannel
    (1 - finiteExchangeHardProbability H N)

def singleRecordQubitKnillLaflammeCondition
    (q : ℝ) : Prop :=
  ∃ c : ℝ,
    0 = c ∧
    1 - q = c

theorem singleRecordQubitKnillLaflammeCondition_iff
    (q : ℝ) :
    singleRecordQubitKnillLaflammeCondition q ↔
      q = 1 := by
  constructor
  · rintro ⟨c, hZero, hLoss⟩
    nlinarith
  · intro hq
    subst q
    exact ⟨0, rfl, by norm_num⟩

theorem finiteExchangeHardOnlyKnillLaflamme_iff
    (H : FiniteChargeConservingExchangeHamiltonian)
    (N : Nat) :
    singleRecordQubitKnillLaflammeCondition
          (finiteExchangeHardProbability H N) ↔
      finiteExchangeHardProbability H N = 1 :=
  singleRecordQubitKnillLaflammeCondition_iff
    (finiteExchangeHardProbability H N)

theorem finiteExchangeSoftOnlyKnillLaflamme_iff
    (H : FiniteChargeConservingExchangeHamiltonian)
    (N : Nat) :
    singleRecordQubitKnillLaflammeCondition
          (finiteExchangeSoftProbability H N) ↔
      finiteExchangeSoftProbability H N = 1 :=
  singleRecordQubitKnillLaflammeCondition_iff
    (finiteExchangeSoftProbability H N)

def finiteCoherentSoftMemoryVisibility
    (memoryShift : ℝ) : ℝ :=
  Real.exp (-(memoryShift ^ 2) / 4)

def finiteSoftMemoryDiscriminator
    (visibility memoryShift : ℝ) : ℝ :=
  -2 * Real.log visibility -
    memoryShift ^ 2 / 2

theorem finiteCoherentSoftMemoryDiscriminator_zero
    (memoryShift : ℝ) :
    finiteSoftMemoryDiscriminator
          (finiteCoherentSoftMemoryVisibility memoryShift)
          memoryShift =
      0 := by
  unfold
    finiteSoftMemoryDiscriminator
    finiteCoherentSoftMemoryVisibility
  rw [Real.log_exp]
  ring

theorem finiteGenericDephasingZeroMemoryDiscriminator
    (visibility : ℝ) :
    finiteSoftMemoryDiscriminator visibility 0 =
      -2 * Real.log visibility := by
  simp [finiteSoftMemoryDiscriminator]

def finiteHardSoftHamiltonianChannelStatus : String :=
  "FINITE_CHARGE_CONSERVING_HAMILTONIAN_CHANNEL_PACKAGE"

def finiteHardSoftHamiltonianChannelBoundary : String :=
  "PHYSICAL_BMS_OR_REGGE_WHEELER_MEMORY_CALIBRATION_NOT_PROVED"

end

end Chronos.Frontier
