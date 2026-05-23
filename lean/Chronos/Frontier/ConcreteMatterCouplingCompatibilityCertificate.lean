/-
Concrete matter-coupling compatibility certificate.

Boundary:
This does not prove analytic Einstein-matter bootstrap package,
constraint propagation, energy-condition preservation, continuation until collapse threshold,
restricted collapse-gate trigger, gravity closure,
Chronos-RR, H4.1/FGL, P vs NP, or any Clay problem.
-/

universe u v

namespace Chronos
namespace Frontier

structure ConcreteMatterCouplingDatum where
  State : Type u
  Tensor : Type v
  admissible : State → Prop
  canonicalStress : State → Tensor
  selectedStress : State → Tensor

def SelectedStressPreserved
    (D : ConcreteMatterCouplingDatum) : Prop :=
  ∀ s : D.State, D.admissible s →
    D.selectedStress s = D.canonicalStress s

structure ConcreteMatterCouplingCompatibilityCertificate
    (D : ConcreteMatterCouplingDatum) where
  selected_stress_preserved : SelectedStressPreserved D

theorem concrete_matter_coupling_compatibility_certificate
    {D : ConcreteMatterCouplingDatum}
    (cert : ConcreteMatterCouplingCompatibilityCertificate D) :
    SelectedStressPreserved D :=
  cert.selected_stress_preserved

theorem selected_stress_eq_canonical_of_certificate
    {D : ConcreteMatterCouplingDatum}
    (cert : ConcreteMatterCouplingCompatibilityCertificate D)
    (s : D.State)
    (hs : D.admissible s) :
    D.selectedStress s = D.canonicalStress s :=
  cert.selected_stress_preserved s hs

end Frontier
end Chronos
