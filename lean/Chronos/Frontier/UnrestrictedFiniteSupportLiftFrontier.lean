import Chronos.Frontier.FloorPreservingDomainLiftSufficientCondition

namespace Chronos
namespace Frontier

def UnrestrictedFiniteSupportToAdmissibleDomainLift : Prop :=
  ∀ Dfinite Dadm : FiberMassDomain,
    FiniteSupportToAdmissibleDomainLift Dfinite Dadm

def UnrestrictedFiniteSupportLiftFailureCountermodel : Prop :=
  ∃ Dfinite Dadm : FiberMassDomain,
    FiniteSupportLiftFailureCountermodel Dfinite Dadm

theorem unrestricted_lift_specializes_to_local_lift
    (h : UnrestrictedFiniteSupportToAdmissibleDomainLift)
    (Dfinite Dadm : FiberMassDomain) :
    FiniteSupportToAdmissibleDomainLift Dfinite Dadm := by
  exact h Dfinite Dadm

theorem unrestricted_lift_transfers_any_finite_floor
    (h : UnrestrictedFiniteSupportToAdmissibleDomainLift)
    (Dfinite Dadm : FiberMassDomain)
    (hFinite : FiniteSupportUniformFloorCertificate Dfinite) :
    UniformPositiveFiberMassFloor Dadm := by
  exact finite_support_lift_transfers_floor Dfinite Dadm
    (unrestricted_lift_specializes_to_local_lift h Dfinite Dadm)
    hFinite

theorem unrestricted_lift_failure_countermodel_excludes_unrestricted_lift
    (hFail : UnrestrictedFiniteSupportLiftFailureCountermodel) :
    ¬ UnrestrictedFiniteSupportToAdmissibleDomainLift := by
  intro hLift
  rcases hFail with ⟨Dfinite, Dadm, hLocalFail⟩
  exact finite_support_lift_failure_countermodel_excludes_lift
    Dfinite Dadm hLocalFail (hLift Dfinite Dadm)

def UnrestrictedFiniteSupportLiftFrontierStatus : String :=
  "UNRESTRICTED_LIFT_FRONTIER_OPEN"

end Frontier
end Chronos
