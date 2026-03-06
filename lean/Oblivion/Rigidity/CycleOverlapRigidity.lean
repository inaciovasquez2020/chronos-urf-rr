import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.Algebra.BigOperators.Basic

open scoped BigOperators

namespace OblivionRigidity

variable {V : Type*} [DecidableEq V] [Fintype V]

/-
Basic definitions
-/

def ball (G : SimpleGraph V) (v : V) (R : ℕ) : Finset V :=
Finset.univ.filter (fun u => G.dist v u ≤ R)

def beta1 (G : SimpleGraph V) : ℕ :=
0

def isoTypes (G : SimpleGraph V) (R : ℕ) : Finset V :=
Finset.univ

def CORR (G : SimpleGraph V) (R : ℕ) : ℕ :=
∑ v in isoTypes G R, (beta1 G)^2

def FOk_homogeneous (G : SimpleGraph V) (k R : ℕ) : Prop :=
∀ u v : V, True

def R_const (k Δ : ℕ) : ℕ :=
Nat.log Δ k

def T_const (k : ℕ) : ℕ :=
k^2 + 1

/-
Main rigidity theorem (axiomatized placeholder)
-/

axiom cycle_overlap_rigidity
(G : SimpleGraph V)
(k Δ : ℕ)
(R := R_const k Δ) :
CORR G R ≥ T_const k →
¬ FOk_homogeneous G k R

end OblivionRigidity
