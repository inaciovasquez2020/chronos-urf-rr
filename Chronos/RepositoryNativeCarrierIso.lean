namespace Chronos.RepositoryNativeCarrierIso

universe u

structure CPDLGate (TRepo : Nat -> Type u) where
  PChr : (n : Nat) -> TRepo n -> Prop

def ValidChr {TRepo : Nat -> Type u} (G : CPDLGate TRepo) (n : Nat) : Type u :=
  { t : TRepo n // G.PChr n t }

def MissingCPDLCCSLWitness {TRepo : Nat -> Type u} (G : CPDLGate TRepo) : Prop :=
  forall n, exists e : (Fin n -> Bool) -> ValidChr G n, Function.Injective e

structure ModelTraceCarrier (n : Nat) where
  payload : Fin n -> Bool

def modelTracePredicate (n : Nat) (_t : ModelTraceCarrier n) : Prop :=
  True

def modelTraceEncode
    (n : Nat)
    (x : Fin n -> Bool) :
    { t : ModelTraceCarrier n // modelTracePredicate n t } :=
  ⟨⟨x⟩, trivial⟩

def modelTraceDecode
    (n : Nat)
    (t : { t : ModelTraceCarrier n // modelTracePredicate n t }) :
    Fin n -> Bool :=
  t.val.payload

theorem modelTraceDecodeEncode
    (n : Nat)
    (x : Fin n -> Bool) :
    modelTraceDecode n (modelTraceEncode n x) = x :=
  rfl

structure RepositoryNativeCarrierIso (TRepo : Nat -> Type u) where
  pRepo : (n : Nat) -> TRepo n -> Prop
  toRepo :
    (n : Nat) ->
    { t : ModelTraceCarrier n // modelTracePredicate n t } ->
    { r : TRepo n // pRepo n r }
  fromRepo :
    (n : Nat) ->
    { r : TRepo n // pRepo n r } ->
    { t : ModelTraceCarrier n // modelTracePredicate n t }
  from_to :
    forall n t, fromRepo n (toRepo n t) = t

def repoCPDL {TRepo : Nat -> Type u}
    (I : RepositoryNativeCarrierIso TRepo) : CPDLGate TRepo :=
{
  PChr := I.pRepo
}

def repoEmbed {TRepo : Nat -> Type u}
    (I : RepositoryNativeCarrierIso TRepo)
    (n : Nat) :
    (Fin n -> Bool) -> ValidChr (repoCPDL I) n :=
  fun x => I.toRepo n (modelTraceEncode n x)

theorem repoEmbed_injective {TRepo : Nat -> Type u}
    (I : RepositoryNativeCarrierIso TRepo)
    (n : Nat) :
    Function.Injective (repoEmbed I n) := by
  intro x y h
  have hfrom :
      I.fromRepo n (I.toRepo n (modelTraceEncode n x)) =
      I.fromRepo n (I.toRepo n (modelTraceEncode n y)) := by
    exact congrArg (I.fromRepo n) h
  rw [I.from_to n (modelTraceEncode n x), I.from_to n (modelTraceEncode n y)] at hfrom
  have hpayload := congrArg Subtype.val hfrom
  exact congrArg ModelTraceCarrier.payload hpayload

theorem repo_missingCPDLCCSLWitness {TRepo : Nat -> Type u}
    (I : RepositoryNativeCarrierIso TRepo) :
    MissingCPDLCCSLWitness (repoCPDL I) := by
  intro n
  exact ⟨repoEmbed I n, repoEmbed_injective I n⟩

theorem repo_validity {TRepo : Nat -> Type u}
    (I : RepositoryNativeCarrierIso TRepo)
    (n : Nat)
    (x : Fin n -> Bool) :
    I.pRepo n ((repoEmbed I n x).val) :=
  (repoEmbed I n x).property

end Chronos.RepositoryNativeCarrierIso
