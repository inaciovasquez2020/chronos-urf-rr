import CLR.FiniteGraph

universe u

namespace CLR

inductive Term
  | var : Nat → Term
deriving DecidableEq

inductive Formula
  | falsum : Formula
  | eq : Term → Term → Formula
  | adj : Term → Term → Formula
  | neg : Formula → Formula
  | and : Formula → Formula → Formula
  | ex : Formula → Formula
deriving DecidableEq

def qr : Formula → Nat
  | .falsum => 0
  | .eq _ _ => 0
  | .adj _ _ => 0
  | .neg φ => qr φ
  | .and φ ψ => max (qr φ) (qr ψ)
  | .ex φ => qr φ + 1

def Env (α : Type u) := Nat → α

def update {α : Type u} (ρ : Env α) (x : α) : Env α
  | 0 => x
  | n + 1 => ρ n

def Term.eval {G : FiniteGraph} (ρ : Env G.V) : Term → G.V
  | .var n => ρ n

def Formula.realize {G : FiniteGraph} (ρ : Env G.V) : Formula → Prop
  | .falsum => False
  | .eq t s => t.eval ρ = s.eval ρ
  | .adj t s => G.adj (t.eval ρ) (s.eval ρ)
  | .neg φ => ¬ Formula.realize ρ φ
  | .and φ ψ => Formula.realize ρ φ ∧ Formula.realize ρ ψ
  | .ex φ => ∃ x : G.V, Formula.realize (update ρ x) φ

def TheoryAt (q : Nat) (G : FiniteGraph) : Set Formula :=
  { φ | qr φ ≤ q ∧ ∀ ρ : Env G.V, Formula.realize ρ φ }

end CLR
