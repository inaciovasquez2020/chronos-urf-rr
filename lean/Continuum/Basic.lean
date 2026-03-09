namespace Continuum

structure SupportFamily where
  m : Nat
  supportMass : Nat → Rat
  overlapMass : Nat → Nat → Rat
  normSq : Nat → Rat

def totalSupport (F : SupportFamily) : Rat :=
  ((List.range F.m).map F.supportMass).foldl (· + ·) 0

def overlapSquare (F : SupportFamily) : Rat :=
  let diag := ((List.range F.m).map F.supportMass).foldl (· + ·) 0
  let off :=
    ((List.range F.m).bind fun i =>
      (List.range F.m).filterMap fun j =>
        if i = j then none else some (F.overlapMass i j)).foldl (· + ·) 0
  diag + off

def gramLowerDiagonal (F : SupportFamily) : Rat :=
  ((List.range F.m).map fun i => (F.normSq i) * (F.normSq i)).foldl (· + ·) 0

def HasUniformNormLower (F : SupportFamily) (a : Rat) : Prop :=
  ∀ i, i < F.m → a ≤ F.normSq i

def HasUniformSupportLower (F : SupportFamily) (s : Rat) : Prop :=
  ∀ i, i < F.m → s ≤ F.supportMass i

def HasControlledOverlap (F : SupportFamily) (K : Rat) : Prop :=
  F.overlapSquare ≤ K * F.totalSupport

def Admissible (F : SupportFamily) (s a K : Rat) : Prop :=
  HasUniformSupportLower F s ∧ HasUniformNormLower F a ∧ HasControlledOverlap F K

end Continuum
