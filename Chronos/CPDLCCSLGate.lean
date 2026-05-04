namespace Chronos

universe u

/-- Chronos primitive validity-predicate layer. -/
structure CPDLGate (TChr : Nat → Type u) where
  PChr : (n : Nat) → TChr n → Prop

/-- CPDL-valid Chronos primitive objects. -/
def ValidChr {TChr : Nat → Type u} (G : CPDLGate TChr) (n : Nat) : Type u :=
  { t : TChr n // G.PChr n t }

/-- CCSL: valid Chronos objects contain an injective Boolean cube. -/
structure CCSLGate {TChr : Nat → Type u} (G : CPDLGate TChr) where
  bitsEmbed : (n : Nat) → ((Fin n → Bool) → ValidChr G n)
  bitsInjective :
    ∀ n, Function.Injective (bitsEmbed n)

/-- CPDL + CCSL supplies the nonuniform valid-certificate carrier. -/
structure CPDLCCSLGate (TChr : Nat → Type u) where
  cpdl : CPDLGate TChr
  ccsl : CCSLGate cpdl

/-- The exact remaining witness required to close CPDL+CCSL for a chosen carrier. -/
def MissingCPDLCCSLWitness {TChr : Nat → Type u} (G : CPDLGate TChr) : Prop :=
  ∀ n, ∃ e : (Fin n → Bool) → ValidChr G n, Function.Injective e

/-- CPDL+CCSL construction from the missing witness. -/
noncomputable def CPDLCCSLGate.ofWitness
    {TChr : Nat → Type u}
    (G : CPDLGate TChr)
    (h : MissingCPDLCCSLWitness G) :
    CPDLCCSLGate TChr :=
{
  cpdl := G
  ccsl :=
  {
    bitsEmbed := fun n => Classical.choose (h n)
    bitsInjective := fun n => Classical.choose_spec (h n)
  }
}

/-- CCSL lower-bound injection theorem. -/
theorem ccsl_injective
    {TChr : Nat → Type u}
    (G : CPDLCCSLGate TChr)
    (n : Nat) :
    Function.Injective (G.ccsl.bitsEmbed n) :=
  G.ccsl.bitsInjective n

/-- CPDL validity is preserved by every CCSL embedded bitstring. -/
theorem cpdl_validity_of_ccsl_embedding
    {TChr : Nat → Type u}
    (G : CPDLCCSLGate TChr)
    (n : Nat)
    (x : Fin n → Bool) :
    G.cpdl.PChr n ((G.ccsl.bitsEmbed n x).val) :=
  (G.ccsl.bitsEmbed n x).property

end Chronos
