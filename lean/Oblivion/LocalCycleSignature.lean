import Mathlib.Data.Finset.Basic

namespace Oblivion

structure Graph where
  V : Type
  adj : V → V → Prop

def Ball (G : Graph) (R : Nat) (v : G.V) : Finset G.V :=
  ∅

structure Cycle where
  support : Finset Nat

def LocalCycles (G : Graph) (R : Nat) (v : G.V) :=
  Finset (Cycle)

structure CycleSignature where
  cycles : Finset Cycle

def localSignature (G : Graph) (R : Nat) (v : G.V) : CycleSignature :=
  ⟨∅⟩

def signaturesDiffer
  (G : Graph) (R : Nat) (u v : G.V) : Prop :=
  localSignature G R u ≠ localSignature G R v

end Oblivion
