namespace Chronos.Frontier.RepositoryNativeConditionalBridge

universe u v z c

structure BridgeCarrier where
  W : Type u
  X : Type v
  Y : Type z
  Enc : W → X
  Extract : Y → W
  Search : X → Y → Prop

namespace BridgeCarrier

def SearchRecover (C : BridgeCarrier.{u,v,z}) : C.W → C.W → Prop :=
  fun w z => z = w

def RecoveryLocalized (C : BridgeCarrier.{u,v,z}) : Prop :=
  ∀ (w : C.W) (y : C.Y),
    C.Search (C.Enc w) y →
    C.SearchRecover w (C.Extract y)

structure SearchSolver (C : BridgeCarrier.{u,v,z}) where
  solve : C.X → C.Y
  correct : ∀ x : C.X, C.Search x (solve x)

structure RecoverySolver (C : BridgeCarrier.{u,v,z}) where
  solve : C.W → C.W
  correct : ∀ w : C.W, C.SearchRecover w (solve w)

def InducedRecoverySolver
  (C : BridgeCarrier.{u,v,z})
  (hLoc : RecoveryLocalized C)
  (S : SearchSolver C) :
  RecoverySolver C where
    solve := fun w => C.Extract (S.solve (C.Enc w))
    correct := by
      intro w
      exact hLoc w (S.solve (C.Enc w)) (S.correct (C.Enc w))

structure ConditionalBridgeContract
  (C : BridgeCarrier.{u,v,z})
  (Cost : Type c) where
  le : Cost → Cost → Prop
  le_trans : ∀ {a b d : Cost}, le a b → le b d → le a d
  localized : RecoveryLocalized C
  searchCost : SearchSolver C → Cost
  recoveryCost : RecoverySolver C → Cost
  inducedCostDominance :
    ∀ S : SearchSolver C,
      le (recoveryCost (InducedRecoverySolver C localized S)) (searchCost S)

def RecoveryLowerBound
  (C : BridgeCarrier.{u,v,z})
  {Cost : Type c}
  (B : ConditionalBridgeContract C Cost)
  (lower : Cost) : Prop :=
  ∀ R : RecoverySolver C, B.le lower (B.recoveryCost R)

def SearchLowerBound
  (C : BridgeCarrier.{u,v,z})
  {Cost : Type c}
  (B : ConditionalBridgeContract C Cost)
  (lower : Cost) : Prop :=
  ∀ S : SearchSolver C, B.le lower (B.searchCost S)

theorem ConditionalBridgeClaritySolved
  (C : BridgeCarrier.{u,v,z})
  {Cost : Type c}
  (B : ConditionalBridgeContract C Cost)
  (lower : Cost)
  (hRecovery : RecoveryLowerBound C B lower) :
  SearchLowerBound C B lower := by
  intro S
  exact B.le_trans
    (hRecovery (InducedRecoverySolver C B.localized S))
    (B.inducedCostDominance S)

end BridgeCarrier

variable (Wraw : Type u)
variable (Xraw : Type v)
variable (Yraw : Type z)

variable (Enc_n : Wraw → Xraw)
variable (Extract_n : Yraw → Wraw)
variable (Search_Fn : Xraw → Yraw → Prop)

def C_Chronos : BridgeCarrier.{u,v,z} where
  W := Wraw
  X := Xraw
  Y := Yraw
  Enc := Enc_n
  Extract := Extract_n
  Search := Search_Fn

theorem chronos_recovery_localized
  (h : ∀ (w : Wraw) (y : Yraw),
    Search_Fn (Enc_n w) y → Extract_n y = w) :
  BridgeCarrier.RecoveryLocalized
    (C_Chronos Wraw Xraw Yraw Enc_n Extract_n Search_Fn) := by
  intro w y hy
  exact h w y hy

variable (Cost : Type c)

variable
  (le : Cost → Cost → Prop)
  (le_trans : ∀ {a b d : Cost}, le a b → le b d → le a d)

variable
  (searchCost :
    BridgeCarrier.SearchSolver
      (C_Chronos Wraw Xraw Yraw Enc_n Extract_n Search_Fn) → Cost)

variable
  (recoveryCost :
    BridgeCarrier.RecoverySolver
      (C_Chronos Wraw Xraw Yraw Enc_n Extract_n Search_Fn) → Cost)

theorem chronos_conditional_bridge_instantiated
  (hLoc : ∀ (w : Wraw) (y : Yraw),
    Search_Fn (Enc_n w) y → Extract_n y = w)
  (hCost :
    ∀ S : BridgeCarrier.SearchSolver
      (C_Chronos Wraw Xraw Yraw Enc_n Extract_n Search_Fn),
      le
        (recoveryCost
          (BridgeCarrier.InducedRecoverySolver
            (C_Chronos Wraw Xraw Yraw Enc_n Extract_n Search_Fn)
            (chronos_recovery_localized Wraw Xraw Yraw Enc_n Extract_n Search_Fn hLoc)
            S))
        (searchCost S))
  (lower : Cost)
  (hRecovery :
    BridgeCarrier.RecoveryLowerBound
      (C_Chronos Wraw Xraw Yraw Enc_n Extract_n Search_Fn)
      {
        le := le
        le_trans := @le_trans
        localized := chronos_recovery_localized Wraw Xraw Yraw Enc_n Extract_n Search_Fn hLoc
        searchCost := searchCost
        recoveryCost := recoveryCost
        inducedCostDominance := hCost
      }
      lower) :
  BridgeCarrier.SearchLowerBound
    (C_Chronos Wraw Xraw Yraw Enc_n Extract_n Search_Fn)
    {
      le := le
      le_trans := @le_trans
      localized := chronos_recovery_localized Wraw Xraw Yraw Enc_n Extract_n Search_Fn hLoc
      searchCost := searchCost
      recoveryCost := recoveryCost
      inducedCostDominance := hCost
    }
    lower := by
  exact
    BridgeCarrier.ConditionalBridgeClaritySolved
      (C_Chronos Wraw Xraw Yraw Enc_n Extract_n Search_Fn)
      {
        le := le
        le_trans := @le_trans
        localized := chronos_recovery_localized Wraw Xraw Yraw Enc_n Extract_n Search_Fn hLoc
        searchCost := searchCost
        recoveryCost := recoveryCost
        inducedCostDominance := hCost
      }
      lower
      hRecovery

end Chronos.Frontier.RepositoryNativeConditionalBridge
