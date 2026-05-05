namespace Chronos.NativeTraceCarrierInstance

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

structure NativeTraceCarrier (n : Nat) where
  payload : Fin n -> Bool

def nativeTracePredicate (n : Nat) (_t : NativeTraceCarrier n) : Prop :=
  True

def nativeTraceEncode
    (n : Nat)
    (x : Fin n -> Bool) :
    { t : NativeTraceCarrier n // nativeTracePredicate n t } :=
  ⟨⟨x⟩, trivial⟩

def nativeTraceDecode
    (n : Nat)
    (t : { t : NativeTraceCarrier n // nativeTracePredicate n t }) :
    Fin n -> Bool :=
  t.val.payload

theorem nativeTraceDecodeEncode
    (n : Nat)
    (x : Fin n -> Bool) :
    nativeTraceDecode n (nativeTraceEncode n x) = x :=
  rfl

def nativeTraceBinding : NativeCarrierBinding NativeTraceCarrier :=
{
  pNative := nativeTracePredicate
  encode := nativeTraceEncode
  decode := nativeTraceDecode
  decode_encode := nativeTraceDecodeEncode
}

def nativeTraceCPDL : CPDLGate NativeTraceCarrier :=
  nativeBindingCPDL nativeTraceBinding

theorem nativeTraceMissingCPDLCCSLWitness :
    MissingCPDLCCSLWitness nativeTraceCPDL :=
  nativeBinding_missingCPDLCCSLWitness nativeTraceBinding

theorem nativeTraceEmbedInjective (n : Nat) :
    Function.Injective (nativeBindingEmbed nativeTraceBinding n) :=
  nativeBindingEmbed_injective nativeTraceBinding n

end Chronos.NativeTraceCarrierInstance
