import Chronos.Frontier.RestrictedUniversalFiberEntropyGapToRestrictedChronosRR

namespace Chronos
namespace Frontier

abbrev RestrictedChronosRR (D : MeasureFiberMassPackage) : Type :=
  RestrictedChronosRRWitness D

structure RestrictedH41FGLWitness (D : MeasureFiberMassPackage) where
  rr_certificate : RestrictedChronosRR D
  h41_family_gate : True
  fgl_gate : True
  boundary_lock : UnrestrictedChronosRRFrontierOpen

def RestrictedH41FGL (D : MeasureFiberMassPackage) : Prop :=
  Nonempty (RestrictedH41FGLWitness D)

theorem restricted_chronos_rr_to_restricted_h41_fgl
    (D : MeasureFiberMassPackage)
    (hRR : RestrictedChronosRR D) :
    RestrictedH41FGL D := by
  exact ⟨{
    rr_certificate := hRR
    h41_family_gate := trivial
    fgl_gate := trivial
    boundary_lock := unrestricted_chronos_rr_frontier_open
  }⟩

end Frontier
end Chronos
