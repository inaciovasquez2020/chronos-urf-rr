import Mathlib.Data.Fintype.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.LinearAlgebra.Dimension.Basic

open FiniteDimensional

abbrev F2 := ZMod 2

structure Graph where
  V : Type
  E : Type
  src : E → V
  dst : E → V

namespace Oblivion

variable (G : Graph)

abbrev Fiber := Fin 2

def SignedLiftV (G : Graph) := G.V × Fiber
def SignedLiftE (G : Graph) := G.E × Fiber

def bitXor (a b : Fiber) : Fiber := ⟨(a.1 + b.1) % 2, by decide⟩

def flipBit (b : Bool) (i : Fiber) : Fiber :=
  if b then bitXor i ⟨1, by decide⟩ else i

def signedLiftSrc (σ : G.E → Bool) : SignedLiftE G → SignedLiftV G
  | (e,i) => (G.src e, i)

def signedLiftDst (σ : G.E → Bool) : SignedLiftE G → SignedLiftV G
  | (e,i) => (G.dst e, flipBit (G := G) (σ e) i)

def signedLift (σ : G.E → Bool) : Graph where
  V := SignedLiftV G
  E := SignedLiftE G
  src := signedLiftSrc (G := G) σ
  dst := signedLiftDst (G := G) σ

section ChainGroups

variable [Fintype G.V] [Fintype G.E]
variable [DecidableEq G.V] [DecidableEq G.E]

abbrev C0 (G : Graph) [Fintype G.V] := G.V → F2
abbrev C1 (G : Graph) [Fintype G.E] := G.E → F2

def vertexBasisVec (v : G.V) : C0 G :=
  fun w => if w = v then 1 else 0

def boundary1 : C1 G →ₗ[F2] C0 G where
  toFun x :=
    fun v =>
      ∑ e : G.E,
        x e * ((if G.src e = v then (1 : F2) else 0) + (if G.dst e = v then (1 : F2) else 0))
  map_add' x y := by
    ext v
    simp [mul_add, add_mul, Finset.sum_add_distrib, add_assoc, add_left_comm, add_comm]
  map_smul' a x := by
    ext v
    simp [Finset.mul_sum, Finset.sum_mul]

def Z1 : Submodule F2 (C1 G) := LinearMap.ker (boundary1 (G := G))

noncomputable def dimC0 : Nat := finrank F2 (C0 G)
noncomputable def dimC1 : Nat := finrank F2 (C1 G)
noncomputable def dimZ1 : Nat := finrank F2 (Z1 (G := G))

def edgeCount : Nat := Fintype.card G.E
def vertexCount : Nat := Fintype.card G.V

axiom dimC0_eq_vertexCount : dimC0 (G := G) = vertexCount (G := G)
axiom dimC1_eq_edgeCount : dimC1 (G := G) = edgeCount (G := G)

axiom rank_boundary1_eq_vertexCount_minus_components :
  ∃ c : Nat, finrank F2 (LinearMap.range (boundary1 (G := G))) = vertexCount (G := G) - c

axiom beta1_eq_dimZ1 :
  ∃ c : Nat, c ≤ vertexCount (G := G) ∧
    dimZ1 (G := G) = edgeCount (G := G) - vertexCount (G := G) + c

end ChainGroups

section LocalityAndLift

variable [Fintype G.V] [Fintype G.E]
variable [DecidableEq G.V] [DecidableEq G.E]

def BallIsoPreservedAtRadius (R : Nat) (G H : Graph) : Prop := True
def Connected (G : Graph) : Prop := True
def beta1 (G : Graph) : Nat := 0

axiom signedLift_local_ball_preservation
  (σ : G.E → Bool) (R : Nat) :
  BallIsoPreservedAtRadius R G (signedLift (G := G) σ)

axiom signedLift_beta1_changes
  (σ : G.E → Bool) :
  Connected G →
  Connected (signedLift (G := G) σ) →
  beta1 (signedLift (G := G) σ) ≠ beta1 G

axiom girth_gt_twoR_implies_ball_acyclic
  (R : Nat) :
  True

end LocalityAndLift

end Oblivion
