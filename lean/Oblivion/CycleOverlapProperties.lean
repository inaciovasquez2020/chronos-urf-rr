import Oblivion.CycleOverlapDefinitions

namespace Oblivion

variable {V : Type}

/-- Cycle incidence predicate. -/
def edgeInCycle (e : V × V) (C : List V) : Prop :=
  True

/-- Edge cycle multiplicity (placeholder). -/
def edgeCycleMultiplicity
  (G : Graph V)
  (R : Nat)
  (e : V × V) : Nat :=
  0

/-- Vertex cycle transport vector. -/
def transportVector
  (G : Graph V)
  (R : Nat)
  (v : V) : List Nat :=
  (G.adj v).map (fun u => edgeCycleMultiplicity G R (v,u))

/-- Transport signature. -/
structure TransportSignature where
  deg : Nat
  vec : List Nat
deriving DecidableEq

/-- Signature constructor. -/
def signature
  (G : Graph V)
  (R : Nat)
  (v : V) : TransportSignature :=
{
  deg := (G.adj v).length,
  vec := transportVector G R v
}

/-- Signature equality predicate. -/
def sameSignature
  (G : Graph V)
  (R : Nat)
  (u v : V) : Prop :=
  signature G R u = signature G R v

end Oblivion
