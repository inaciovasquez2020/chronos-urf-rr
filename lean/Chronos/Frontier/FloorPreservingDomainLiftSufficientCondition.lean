import Chronos.Frontier.SinkClosureCountermodelDichotomyTarget

namespace Chronos
namespace Frontier

/--
A sufficient condition for the finite-support-to-admissible-domain lift.

It maps each admissible target-domain fiber back to an admissible finite-domain
fiber whose mass is no larger than the target mass. Thus any finite-domain
uniform floor transfers forward.
-/
def FloorPreservingDomainLift
    (Dfinite Dadm : FiberMassDomain) : Prop :=
  ∃ embed : Dadm.Fiber → Dfinite.Fiber,
    (∀ y : Dadm.Fiber, Dadm.admissible y → Dfinite.admissible (embed y)) ∧
      ∀ y : Dadm.Fiber,
        Dadm.admissible y → Dfinite.mass (embed y) ≤ Dadm.mass y

theorem floor_preserving_domain_lift_to_uniform_floor
    (Dfinite Dadm : FiberMassDomain)
    (hLift : FloorPreservingDomainLift Dfinite Dadm)
    (hFinite : FiniteSupportUniformFloorCertificate Dfinite) :
    UniformPositiveFiberMassFloor Dadm := by
  rcases hLift with ⟨embed, hAdmissible, hMass⟩
  rcases hFinite with ⟨epsilon, hEpsilonPos, hFloor⟩
  exact ⟨epsilon, hEpsilonPos, by
    intro y hy
    have hFiniteFloor : epsilon ≤ Dfinite.mass (embed y) :=
      hFloor (embed y) (hAdmissible y hy)
    have hMassTransfer : Dfinite.mass (embed y) ≤ Dadm.mass y :=
      hMass y hy
    exact le_trans hFiniteFloor hMassTransfer⟩

theorem floor_preserving_domain_lift_to_admissible_lift
    (Dfinite Dadm : FiberMassDomain)
    (hLift : FloorPreservingDomainLift Dfinite Dadm) :
    FiniteSupportToAdmissibleDomainLift Dfinite Dadm := by
  intro hFinite
  exact floor_preserving_domain_lift_to_uniform_floor
    Dfinite Dadm hLift hFinite

theorem floor_preserving_domain_lift_resolves_second_sink
    (Dfinite Dadm : FiberMassDomain)
    (hLift : FloorPreservingDomainLift Dfinite Dadm)
    (hFinite : FiniteSupportUniformFloorCertificate Dfinite) :
    UniformPositiveFiberMassSinkResolution Dadm := by
  exact finite_support_lift_resolves_admissible_sink Dfinite Dadm
    (floor_preserving_domain_lift_to_admissible_lift Dfinite Dadm hLift)
    hFinite

def FloorPreservingDomainLiftSufficientConditionStatus : String :=
  "CONDITIONAL_LIFT_SUFFICIENT_CONDITION_ONLY"

def FloorPreservingDomainLiftSufficientConditionBoundary : String :=
  "Does not prove existence of a floor-preserving lift or unrestricted UFEG."

end Frontier
end Chronos
