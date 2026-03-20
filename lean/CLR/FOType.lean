import Lean.CLR.EFGame
import Lean.CLR.LocalCycle

universe u

def FOType (Δ R k q : Nat) := Quot (foEquivSetoid Δ R k q)

def rootedBallToCycleData (A : RootedBallSig) : LocalCycleData where
  V := A.V
  edge := A.adj

def zeroCycle (A : RootedBallSig) : cycleVec (rootedBallToCycleData A) :=
  fun _ => 0

def cycleRep (A : RootedBallSig) :
    LocalCycleQuot (rootedBallToCycleData A) :=
  Quotient.mk _ (zeroCycle A)
