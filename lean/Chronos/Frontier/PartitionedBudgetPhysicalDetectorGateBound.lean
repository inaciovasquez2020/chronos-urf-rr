import Chronos.Frontier.RestrictedPhysicalDetectorFieldExtractionMap

namespace Chronos
namespace Frontier
namespace RestrictedPhysicalDetectorFieldExtractionMap

/--
A partitioned budget certificate derives the aggregate gate bound from
per-active-detector budget control.

The key non-circular condition is `budget_le_partition`: every active detector's
budget is small enough that, after multiplying by the number of active detectors,
it still fits under the extracted radius floor.
-/
structure PartitionedPhysicalDetectorBudgetCertificate
    {Detector : Type*} [Fintype Detector] [DecidableEq Detector]
    (F : PhysicalDetectorField Detector) where
  budget : Detector → ℕ
  reading_le_budget :
    ∀ d, d ∈ activeDetectors F → F.reading d ≤ budget d
  budget_le_partition :
    ∀ d, d ∈ activeDetectors F →
      budget d * (activeDetectors F).card ≤ extractedRadiusFloor F

/--
A partitioned physical detector budget certificate implies the restricted
finite detector gate bound.

This replaces the previous circular use of `gate_bound` by deriving the bound
from two certificate clauses:
1. active readings are bounded by allocated budgets;
2. each allocated budget fits into a cardinality-scaled share of the radius floor.
-/
theorem partitionedBudgetCertificate_implies_gate_bound
    {Detector : Type*} [Fintype Detector] [DecidableEq Detector]
    (F : PhysicalDetectorField Detector)
    (c : PartitionedPhysicalDetectorBudgetCertificate F) :
    RestrictedFiniteDetectorGate
      (extractedActiveMass F)
      (extractedRadiusFloor F) := by
  have h_mass :
      extractedActiveMass F = (activeDetectors F).sum F.reading :=
    physicalExtraction_atomMass_coherent F
  have h_reading_le_budget :
      (activeDetectors F).sum F.reading
        ≤ (activeDetectors F).sum c.budget := by
    exact Finset.sum_le_sum (fun d hd => c.reading_le_budget d hd)
  by_cases h_card_zero : (activeDetectors F).card = 0
  · have h_empty : activeDetectors F = ∅ :=
      Finset.card_eq_zero.mp h_card_zero
    rw [h_mass, h_empty, Finset.sum_empty]
    exact Nat.zero_le _
  · have h_partition_sum :
        (activeDetectors F).sum
            (fun d => c.budget d * (activeDetectors F).card)
          ≤
        (activeDetectors F).sum
            (fun _ => extractedRadiusFloor F) := by
      exact Finset.sum_le_sum (fun d hd => c.budget_le_partition d hd)
    have h_budget_mul :
        ((activeDetectors F).sum c.budget) * (activeDetectors F).card
          ≤ extractedRadiusFloor F * (activeDetectors F).card := by
      calc
        ((activeDetectors F).sum c.budget) * (activeDetectors F).card
            = (activeDetectors F).sum
                (fun d => c.budget d * (activeDetectors F).card) := by
                rw [Finset.sum_mul]
        _ ≤ (activeDetectors F).sum
                (fun _ => extractedRadiusFloor F) :=
                h_partition_sum
        _ = (activeDetectors F).card * extractedRadiusFloor F := by
                simp [Finset.sum_const]
        _ = extractedRadiusFloor F * (activeDetectors F).card := by
                rw [Nat.mul_comm]
    have h_budget_total :
        (activeDetectors F).sum c.budget ≤ extractedRadiusFloor F :=
      Nat.le_of_mul_le_mul_right
        h_budget_mul
        (Nat.pos_of_ne_zero h_card_zero)
    rw [h_mass]
    exact Nat.le_trans h_reading_le_budget h_budget_total

/--
A partitioned budget certificate produces the admissibility object required by
the restricted physical detector extraction map.
-/
theorem partitionedBudgetCertificate_to_admissible
    {Detector : Type*} [Fintype Detector] [DecidableEq Detector]
    (F : PhysicalDetectorField Detector)
    (c : PartitionedPhysicalDetectorBudgetCertificate F) :
    PhysicalDetectorFieldAdmissible F :=
  ⟨partitionedBudgetCertificate_implies_gate_bound F c⟩

/--
Derived gate bridge: the restricted physical detector gate is obtained from the
partitioned budget certificate, not assumed directly as boundary admissibility.
-/
theorem partitionedBudgetCertificate_feeds_restrictedFiniteDetectorGate_derived
    {Detector : Type*} [Fintype Detector] [DecidableEq Detector]
    (F : PhysicalDetectorField Detector)
    (c : PartitionedPhysicalDetectorBudgetCertificate F) :
    RestrictedFiniteDetectorGate
      (extractedActiveMass F)
      (extractedRadiusFloor F) :=
  (partitionedBudgetCertificate_to_admissible F c).gate_bound

/-- A concrete two-detector test type. -/
inductive TwoDetector
  | d1
  | d2
deriving DecidableEq, Fintype

/-- A nontrivial two-detector physical sampling profile. -/
def twoDetectorExampleField : PhysicalDetectorField TwoDetector where
  reading := fun
    | TwoDetector.d1 => 1
    | TwoDetector.d2 => 1
  radius := fun
    | TwoDetector.d1 => 6
    | TwoDetector.d2 => 6
  active := fun _ => true

/--
A concrete partitioned certificate.

There are two active detectors, budget is 2 at each detector, and
`2 * 2 ≤ 6`.
-/
def twoDetectorPartitionedBudget :
    PartitionedPhysicalDetectorBudgetCertificate twoDetectorExampleField where
  budget := fun
    | TwoDetector.d1 => 2
    | TwoDetector.d2 => 2
  reading_le_budget := by
    intro d _
    cases d <;> native_decide
  budget_le_partition := by
    intro d _
    cases d <;> native_decide

/-- The concrete two-detector instance satisfies the restricted gate. -/
theorem twoDetectorExample_closes_gate :
    RestrictedFiniteDetectorGate
      (extractedActiveMass twoDetectorExampleField)
      (extractedRadiusFloor twoDetectorExampleField) :=
  partitionedBudgetCertificate_feeds_restrictedFiniteDetectorGate_derived
    twoDetectorExampleField
    twoDetectorPartitionedBudget

end RestrictedPhysicalDetectorFieldExtractionMap
end Frontier
end Chronos
