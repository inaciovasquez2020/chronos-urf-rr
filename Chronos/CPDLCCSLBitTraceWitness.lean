namespace Chronos.BitTraceWitness

universe u

structure CPDLGate (TChr : Nat -> Type u) where
  PChr : (n : Nat) -> TChr n -> Prop

def ValidChr {TChr : Nat -> Type u} (G : CPDLGate TChr) (n : Nat) : Type u :=
  { t : TChr n // G.PChr n t }

structure CCSLGate {TChr : Nat -> Type u} (G : CPDLGate TChr) where
  bitsEmbed : (n : Nat) -> ((Fin n -> Bool) -> ValidChr G n)
  bitsInjective : forall n, Function.Injective (bitsEmbed n)

structure CPDLCCSLGate (TChr : Nat -> Type u) where
  cpdl : CPDLGate TChr
  ccsl : CCSLGate cpdl

def MissingCPDLCCSLWitness {TChr : Nat -> Type u} (G : CPDLGate TChr) : Prop :=
  forall n, exists e : (Fin n -> Bool) -> ValidChr G n, Function.Injective e

abbrev BitTraceTChr (n : Nat) : Type :=
  Fin n -> Bool

def bitTraceCPDL : CPDLGate BitTraceTChr :=
{
  PChr := fun _ _ => True
}

def bitTraceEmbed (n : Nat) : (Fin n -> Bool) -> ValidChr bitTraceCPDL n :=
  fun x => ⟨x, trivial⟩

theorem bitTraceEmbed_injective (n : Nat) :
    Function.Injective (bitTraceEmbed n) := by
  intro x y h
  exact congrArg Subtype.val h

theorem bitTrace_missingCPDLCCSLWitness :
    MissingCPDLCCSLWitness bitTraceCPDL := by
  intro n
  exact ⟨bitTraceEmbed n, bitTraceEmbed_injective n⟩

def bitTraceCCSL : CCSLGate bitTraceCPDL :=
{
  bitsEmbed := bitTraceEmbed
  bitsInjective := bitTraceEmbed_injective
}

def bitTraceCPDLCCSLGate : CPDLCCSLGate BitTraceTChr :=
{
  cpdl := bitTraceCPDL
  ccsl := bitTraceCCSL
}

theorem bitTrace_cpdl_validity (n : Nat) (x : Fin n -> Bool) :
    bitTraceCPDL.PChr n ((bitTraceEmbed n x).val) :=
  trivial

theorem bitTrace_ccsl_injective (n : Nat) :
    Function.Injective (bitTraceCCSL.bitsEmbed n) :=
  bitTraceEmbed_injective n

end Chronos.BitTraceWitness
