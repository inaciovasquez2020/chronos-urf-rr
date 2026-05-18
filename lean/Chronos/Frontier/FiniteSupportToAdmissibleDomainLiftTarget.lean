import Chronos.Frontier.FiniteSupportUniformFloorToTarget

namespace Chronos
namespace Frontier

/--
Open target for the second global URF sink.

A finite-support-to-admissible-domain lift is exactly the missing bridge
from a finite-support uniform-floor certificate to an admissible-domain
uniform positive fiber-mass floor.
-/
def FiniteSupportToAdmissibleDomainLift
    (Dfinite Dadm : FiberMassDomain) : Prop :=
  FiniteSupportUniformFloorCertificate Dfinite →
    UniformPositiveFiberMassFloor Dadm

/--
Countermodel exit for the second global URF sink.

It consists of a finite-support floor certificate together with a
countermodel excluding any uniform positive floor on the admissible target.
-/
def FiniteSupportLiftFailureCountermodel
    (Dfinite Dadm : FiberMassDomain) : Prop :=
  FiniteSupportUniformFloorCertificate Dfinite ∧
    NoUniformPositiveFiberMassFloorCountermodel Dadm

theorem finite_support_lift_transfers_floor
    (Dfinite Dadm : FiberMassDomain)
    (hLift : FiniteSupportToAdmissibleDomainLift Dfinite Dadm)
    (hFinite : FiniteSupportUniformFloorCertificate Dfinite) :
    UniformPositiveFiberMassFloor Dadm := by
  exact hLift hFinite

theorem finite_support_lift_resolves_admissible_sink
    (Dfinite Dadm : FiberMassDomain)
    (hLift : FiniteSupportToAdmissibleDomainLift Dfinite Dadm)
    (hFinite : FiniteSupportUniformFloorCertificate Dfinite) :
    UniformPositiveFiberMassSinkResolution Dadm := by
  exact uniform_positive_floor_closure_resolves_sink Dadm
    (finite_support_lift_transfers_floor Dfinite Dadm hLift hFinite)

theorem finite_support_lift_failure_countermodel_excludes_lift
    (Dfinite Dadm : FiberMassDomain)
    (hFail : FiniteSupportLiftFailureCountermodel Dfinite Dadm) :
    ¬ FiniteSupportToAdmissibleDomainLift Dfinite Dadm := by
  intro hLift
  rcases hFail with ⟨hFinite, hCounter⟩
  have hFloor : UniformPositiveFiberMassFloor Dadm :=
    finite_support_lift_transfers_floor Dfinite Dadm hLift hFinite
  exact countermodel_excludes_uniform_positive_floor Dadm hCounter hFloor

def FiniteSupportToAdmissibleDomainLiftTargetStatus : String :=
  "OPEN_LIFT_TARGET_SURFACE_ONLY"

def FiniteSupportToAdmissibleDomainLiftTargetBoundary : String :=
  "Does not prove a finite-support-to-admissible-domain lift or unrestricted UFEG."

end Frontier
end Chronos
