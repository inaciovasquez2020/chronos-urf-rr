namespace Chronos.RepositoryNativeCarrierSelection

structure RepositoryNativeCarrierSelection where
  TRepo : Type
  ModelTraceCarrier : Nat → Type
  CPDLCCSLWitness : Nat → Type
  embed : (n : Nat) → TRepo → Subtype fun _ : ModelTraceCarrier n => True
  embed_injective : (n : Nat) → Function.Injective (embed n)
  missingCPDLCCSLWitness : (n : Nat) → CPDLCCSLWitness n
  valid : Prop

def selectedCPDL (S : RepositoryNativeCarrierSelection) (n : Nat) : Type :=
  S.CPDLCCSLWitness n

def selectedEmbed (S : RepositoryNativeCarrierSelection) (n : Nat) :
    S.TRepo → Subtype fun _ : S.ModelTraceCarrier n => True :=
  S.embed n

theorem selectedEmbed_injective (S : RepositoryNativeCarrierSelection) (n : Nat) :
    Function.Injective (selectedEmbed S n) :=
  S.embed_injective n

def selected_missingCPDLCCSLWitness
    (S : RepositoryNativeCarrierSelection) (n : Nat) : selectedCPDL S n :=
  S.missingCPDLCCSLWitness n

theorem selected_validity (S : RepositoryNativeCarrierSelection) :
    S.valid → S.valid :=
  fun h => h

theorem selectedEmbed_property
    (S : RepositoryNativeCarrierSelection) (n : Nat) (x : S.TRepo) :
    True :=
  (selectedEmbed S n x).property

end Chronos.RepositoryNativeCarrierSelection
