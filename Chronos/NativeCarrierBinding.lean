namespace Chronos.NativeBinding

universe u

structure CPDLGate (TNative : Nat -> Type u) where
  PChr : (n : Nat) -> TNative n -> Prop

def ValidChr {TNative : Nat -> Type u} (G : CPDLGate TNative) (n : Nat) : Type u :=
  { t : TNative n // G.PChr n t }

def MissingCPDLCCSLWitness {TNative : Nat -> Type u} (G : CPDLGate TNative) : Prop :=
  forall n, exists e : (Fin n -> Bool) -> ValidChr G n, Function.Injective e

structure NativeCarrierBinding (TNative : Nat -> Type u) where
  pNative : (n : Nat) -> TNative n -> Prop
  encode : (n : Nat) -> (Fin n -> Bool) -> { t : TNative n // pNative n t }
  decode : (n : Nat) -> { t : TNative n // pNative n t } -> (Fin n -> Bool)
  decode_encode : forall n x, decode n (encode n x) = x

def nativeBindingCPDL {TNative : Nat -> Type u}
    (B : NativeCarrierBinding TNative) : CPDLGate TNative :=
{
  PChr := B.pNative
}

def nativeBindingEmbed {TNative : Nat -> Type u}
    (B : NativeCarrierBinding TNative)
    (n : Nat) :
    (Fin n -> Bool) -> ValidChr (nativeBindingCPDL B) n :=
  B.encode n

theorem nativeBindingEmbed_injective {TNative : Nat -> Type u}
    (B : NativeCarrierBinding TNative)
    (n : Nat) :
    Function.Injective (nativeBindingEmbed B n) := by
  intro x y h
  have hdecode :
      B.decode n (B.encode n x) =
      B.decode n (B.encode n y) := by
    exact congrArg (B.decode n) h
  rw [B.decode_encode n x, B.decode_encode n y] at hdecode
  exact hdecode

theorem nativeBinding_missingCPDLCCSLWitness {TNative : Nat -> Type u}
    (B : NativeCarrierBinding TNative) :
    MissingCPDLCCSLWitness (nativeBindingCPDL B) := by
  intro n
  exact ⟨nativeBindingEmbed B n, nativeBindingEmbed_injective B n⟩

theorem nativeBinding_validity {TNative : Nat -> Type u}
    (B : NativeCarrierBinding TNative)
    (n : Nat)
    (x : Fin n -> Bool) :
    B.pNative n ((nativeBindingEmbed B n x).val) :=
  (nativeBindingEmbed B n x).property

end Chronos.NativeBinding
