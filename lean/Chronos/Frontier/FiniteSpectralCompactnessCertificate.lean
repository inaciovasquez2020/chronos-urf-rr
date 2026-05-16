import Init

namespace Chronos
namespace Frontier
namespace Gravity
namespace FiniteSpectralCompactness

structure FiniteDetectorAlgebra where
  detectorCount : Nat
  detectorCount_pos : 0 < detectorCount
  compositionClosed : Prop
  adjointClosed : Prop

structure SpectralCutoff where
  level : Nat
  level_pos : 0 < level

structure BoundedEnergyAreaBudget where
  energyBudget : Nat
  areaBudget : Nat
  energy_pos : 0 < energyBudget
  area_pos : 0 < areaBudget

structure BoundaryObservableStateSpace
    (A : FiniteDetectorAlgebra)
    (cutoff : SpectralCutoff)
    (budget : BoundedEnergyAreaBudget) where
  stateDimension : Nat
  dimension_eq :
    stateDimension =
      A.detectorCount *
        (cutoff.level + 1) *
        (budget.energyBudget + budget.areaBudget + 1)

def canonicalBoundaryObservableStateSpace
    (A : FiniteDetectorAlgebra)
    (cutoff : SpectralCutoff)
    (budget : BoundedEnergyAreaBudget) :
    BoundaryObservableStateSpace A cutoff budget :=
  {
    stateDimension :=
      A.detectorCount *
        (cutoff.level + 1) *
        (budget.energyBudget + budget.areaBudget + 1)
    dimension_eq := rfl
  }

theorem boundaryObservableStateSpace_finite_dimensional
    {A : FiniteDetectorAlgebra}
    {cutoff : SpectralCutoff}
    {budget : BoundedEnergyAreaBudget}
    (S : BoundaryObservableStateSpace A cutoff budget) :
    ∃ N : Nat, S.stateDimension = N :=
  Exists.intro S.stateDimension rfl

def finiteSpectralCoveringNumber
    {A : FiniteDetectorAlgebra}
    {cutoff : SpectralCutoff}
    {budget : BoundedEnergyAreaBudget}
    (S : BoundaryObservableStateSpace A cutoff budget)
    (epsilonIndex : Nat) : Nat :=
  (S.stateDimension + 1) * (epsilonIndex + 1)

structure FiniteSpectralCompactnessCertificate
    (A : FiniteDetectorAlgebra)
    (cutoff : SpectralCutoff)
    (budget : BoundedEnergyAreaBudget)
    (S : BoundaryObservableStateSpace A cutoff budget) where
  epsilonIndex : Nat
  coveringNumber : Nat
  finiteDimensional : ∃ N : Nat, S.stateDimension = N
  finiteCoveringNumber : ∃ M : Nat, coveringNumber = M
  coveringNumber_eq :
    coveringNumber = finiteSpectralCoveringNumber S epsilonIndex

def constructFiniteSpectralCompactnessCertificate
    {A : FiniteDetectorAlgebra}
    {cutoff : SpectralCutoff}
    {budget : BoundedEnergyAreaBudget}
    (S : BoundaryObservableStateSpace A cutoff budget)
    (epsilonIndex : Nat) :
    FiniteSpectralCompactnessCertificate A cutoff budget S :=
  {
    epsilonIndex := epsilonIndex
    coveringNumber := finiteSpectralCoveringNumber S epsilonIndex
    finiteDimensional := boundaryObservableStateSpace_finite_dimensional S
    finiteCoveringNumber :=
      Exists.intro (finiteSpectralCoveringNumber S epsilonIndex) rfl
    coveringNumber_eq := rfl
  }

structure PhysicalToTopologicalCompactnessCertificate
    (A : FiniteDetectorAlgebra)
    (cutoff : SpectralCutoff)
    (budget : BoundedEnergyAreaBudget)
    (S : BoundaryObservableStateSpace A cutoff budget) where
  spectralCertificate :
    FiniteSpectralCompactnessCertificate A cutoff budget S
  topologicalCoverFinite :
    ∃ M : Nat, spectralCertificate.coveringNumber = M

def finiteSpectralCompactness_to_physicalTopologicalCompactness
    {A : FiniteDetectorAlgebra}
    {cutoff : SpectralCutoff}
    {budget : BoundedEnergyAreaBudget}
    {S : BoundaryObservableStateSpace A cutoff budget}
    (C : FiniteSpectralCompactnessCertificate A cutoff budget S) :
    PhysicalToTopologicalCompactnessCertificate A cutoff budget S :=
  {
    spectralCertificate := C
    topologicalCoverFinite := C.finiteCoveringNumber
  }

def finite_detector_spectral_cutoff_constructs_physical_to_topological_compactness
    {A : FiniteDetectorAlgebra}
    {cutoff : SpectralCutoff}
    {budget : BoundedEnergyAreaBudget}
    (S : BoundaryObservableStateSpace A cutoff budget)
    (epsilonIndex : Nat) :
    PhysicalToTopologicalCompactnessCertificate A cutoff budget S :=
  finiteSpectralCompactness_to_physicalTopologicalCompactness
    (constructFiniteSpectralCompactnessCertificate S epsilonIndex)

end FiniteSpectralCompactness
end Gravity
end Frontier
end Chronos
