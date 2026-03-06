import Mathlib.Data.Finset.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.Algebra.BigOperators.Basic

open scoped BigOperators

namespace Oblivion

variable {V : Type*} [DecidableEq V]

structure Graph :=
(V : Type)
(adj : V → V → Prop)

def Ball (G : Graph) (R : Nat) (v : V) : Finset V :=
Finset.univ

def beta1 (G : Graph) : Nat :=
0

def BallType (G : Graph) (R : Nat) :=
Finset (Finset V)

def rootedBallTypes (G : Graph) (R : Nat) : BallType G R :=
∅

def CORR (G : Graph) (R : Nat) : Nat :=
∑ τ in rootedBallTypes G R, (beta1 G)^2

theorem corr_nonneg (G : Graph) (R : Nat) :
0 ≤ CORR G R := by
simp [CORR]

end Oblivion
