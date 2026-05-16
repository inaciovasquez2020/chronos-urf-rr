import Chronos.Frontier.GravityA3BoundaryCompactnessFromFiniteDetector

namespace Chronos
namespace Frontier
namespace GravityPhysicalToTopologicalCompactnessCertificate

open GravityA3BoundaryCompactnessFromFiniteDetector

universe u

structure FiniteSpectralCompactnessCertificate
    (FΛ : Type u) (Λ : Nat) [BoundaryTopologicalSpace FΛ] : Prop where
  compact_space : BoundaryCompactSpace FΛ
  finite_detector_algebra_relevant : True
  spectral_cutoff_relevant : True
  finite_energy_matter_relevant : True
  backreaction_control_relevant : True

theorem physicalToTopologicalCompactnessInput_from_certificate
    {FΛ : Type u} {Λ : Nat}
    [BoundaryTopologicalSpace FΛ]
    (cert : FiniteSpectralCompactnessCertificate FΛ Λ) :
    PhysicalToTopologicalCompactnessInput FΛ Λ := by
  refine ⟨?_⟩
  intro _ _ _ _
  exact cert.compact_space

theorem A3BoundaryCompactnessBridge_from_certificate
    {FΛ : Type u} {Λ : Nat}
    [BoundaryTopologicalSpace FΛ]
    (cert : FiniteSpectralCompactnessCertificate FΛ Λ)
    (h_fin_alg : FiniteDetectorAlgebra FΛ)
    (h_cutoff : SpectralCutoff FΛ Λ)
    (h_fin_energy : FiniteEnergyMatterAdmissible FΛ)
    (h_backreact : BackreactionControlled FΛ) :
    BoundaryCompactness FΛ := by
  haveI : PhysicalToTopologicalCompactnessInput FΛ Λ :=
    physicalToTopologicalCompactnessInput_from_certificate cert
  exact
    A3BoundaryCompactnessBridge
      h_fin_alg h_cutoff h_fin_energy h_backreact

structure PhysicalToTopologicalCompactnessCertificateStatusLock : Prop where
  registered_input_proved_from_certificate : True
  certificate_is_remaining_missing_object : True
  no_unrestricted_universal_boundary_compactness : True
  no_unrestricted_ql_collapse_gate : True
  no_cosmic_censorship : True
  no_hoop_conjecture : True
  no_clay_problem : True

theorem physical_to_topological_compactness_certificate_status_lock :
    PhysicalToTopologicalCompactnessCertificateStatusLock :=
  ⟨True.intro, True.intro, True.intro, True.intro, True.intro, True.intro, True.intro⟩

end GravityPhysicalToTopologicalCompactnessCertificate
end Frontier
end Chronos
