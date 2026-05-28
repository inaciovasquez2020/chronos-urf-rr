import Chronos.Frontier.GDMGravityDarkMatterDeficitModel

/-!
# GDM residual identification theorem

This file records the finite nonnegative GDM residual-identification theorem.

Boundary: finite nonnegative model only; no observational evidence; no galaxy
rotation curve fit; no lensing fit; no empirical residual measurement; no dark
matter replacement; no Lambda-CDM refutation; no modified gravity theorem; no
Einstein-matter theorem; no collapse theorem; no Cosmic Censorship; no Hoop
Conjecture; no quantum gravity; no unrestricted Chronos-RR; no unrestricted
H4.1/FGL; no P vs NP; no Clay problem.
-/

namespace Chronos
namespace Frontier

/-- A finite nonnegative accounting instance for the GDM residual model. -/
structure GDMResidualIdentificationModel where
  baryonicMass : Nat
  geometricDeficitMass : Nat
  observedMass : Nat
  observedMass_eq :
    observedMass = baryonicMass + geometricDeficitMass

/--
Inside the finite nonnegative GDM accounting model, the dark-matter-like residual
`observedMass - baryonicMass` is exactly the geometric deficit mass.
-/
theorem gdmResidualIdentification
    (M : GDMResidualIdentificationModel) :
    M.observedMass - M.baryonicMass = M.geometricDeficitMass := by
  rw [M.observedMass_eq]
  exact Nat.add_sub_cancel_left M.baryonicMass M.geometricDeficitMass

/--
The identified residual is nonnegative because it is represented by a natural
geometric deficit mass in the finite nonnegative model.
-/
theorem gdmResidualIdentification_nonnegative
    (M : GDMResidualIdentificationModel) :
    0 ≤ M.observedMass - M.baryonicMass := by
  exact Nat.zero_le _

end Frontier
end Chronos
