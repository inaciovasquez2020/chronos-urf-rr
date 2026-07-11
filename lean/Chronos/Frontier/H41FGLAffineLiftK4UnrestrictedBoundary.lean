import Chronos.Frontier.H41FGLAffineLiftK4WalshCertificate

namespace Chronos
namespace Frontier

def H41FGLK4UnrestrictedInterpretation : Prop :=
  (∀ f : Fin 16 → ℚ,
      0 < h41FGLK4RankRate f →
        0 < h41FGLK4FiberMass f) →
    ∀ (α : Type) (r m : α → Nat) (x : α),
      0 < r x → 0 < m x

theorem h41FGLK4UnrestrictedInterpretation_refuted :
    ¬ H41FGLK4UnrestrictedInterpretation := by
  intro hpromotion
  have hunrestricted :
      ∀ (α : Type) (r m : α → Nat) (x : α),
        0 < r x → 0 < m x :=
    hpromotion h41FGLK4RestrictedPositivity
  have hzero : 0 < (0 : Nat) :=
    hunrestricted
      Unit
      (fun _ => 1)
      (fun _ => 0)
      ()
      (Nat.zero_lt_succ 0)
  exact Nat.lt_irrefl 0 hzero

end Frontier
end Chronos
