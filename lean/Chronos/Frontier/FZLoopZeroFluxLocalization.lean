namespace Chronos.Frontier

structure FZLoop where
  sectors : List Nat
deriving Repr, DecidableEq

def FZLoop.fluxSum : List Nat -> Nat
  | [] => 0
  | q :: qs => q + FZLoop.fluxSum qs

def FZLoop.locallyZero : List Nat -> Prop
  | [] => True
  | q :: qs => q = 0 ∧ FZLoop.locallyZero qs

def FZLoop.totalFlux (L : FZLoop) : Nat :=
  FZLoop.fluxSum L.sectors

theorem FZLoop.zero_flux_localization_list :
    ∀ qs : List Nat, FZLoop.fluxSum qs = 0 -> FZLoop.locallyZero qs
  | [], _ => True.intro
  | q :: qs, h => by
      have hz := Nat.add_eq_zero_iff.mp h
      exact And.intro hz.left (FZLoop.zero_flux_localization_list qs hz.right)

theorem FZLoop.zero_flux_localization (L : FZLoop) :
    L.totalFlux = 0 -> FZLoop.locallyZero L.sectors := by
  intro h
  exact FZLoop.zero_flux_localization_list L.sectors h

def fzLoopZeroFluxLocalizationStatus : String :=
  "FZLOOP_ZERO_FLUX_LOCALIZATION_PROVED_FINITE_NONNEGATIVE_MODEL_ONLY"

theorem fzLoopZeroFluxLocalizationStatus_eq :
    fzLoopZeroFluxLocalizationStatus =
      "FZLOOP_ZERO_FLUX_LOCALIZATION_PROVED_FINITE_NONNEGATIVE_MODEL_ONLY" := rfl

end Chronos.Frontier
