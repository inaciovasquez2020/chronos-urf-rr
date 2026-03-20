import Lean.CLR.EFGame
import Lean.CLR.foEquivSetoid
import Lean.CLR.CycleSpace
import Lean.CLR.FOType

universe u

def rootedBallToCycleData' (A : RootedBallSig) : LocalCycleData where
  V := A.V
  edge := A.adj

def zeroCycle' (A : RootedBallSig) : cycleVec (rootedBallToCycleData' A) :=
  fun _ => 0

def cycleRep' (A : RootedBallSig) :
    LocalCycleQuot (rootedBallToCycleData' A) :=
  Quotient.mk _ (zeroCycle' A)

axiom cycleRep_respects_foEquiv
  (Δ R k q : Nat) :
  ∀ {A B : RootedBallSig},
    fo_equiv_k_q_on_balls Δ R k q A B →
    HEq (cycleRep' A) (cycleRep' B)

