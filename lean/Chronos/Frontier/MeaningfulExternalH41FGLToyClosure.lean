namespace Chronos
namespace Frontier
namespace MeaningfulExternalH41FGLToyClosure

structure Witness (I : Type) where
  marker : Unit

instance witness_subsingleton (I : Type) :
    Subsingleton (Witness I) where
  allEq a b := by
    cases a
    cases b
    rfl

def ValidExtractionWitness
    (I : Type)
    (_w : Witness I) : Prop :=
  True

structure CountingFiberSeparationFromNonProp
    (I : Type) where
  witness : Witness I
  valid : ValidExtractionWitness I witness

def extract_witness_from_counting_fiber_separation
    (I : Type)
    (sep : CountingFiberSeparationFromNonProp I) :
    { w : Witness I // ValidExtractionWitness I w } :=
  ⟨sep.witness, sep.valid⟩

theorem counting_implies_nonempty
    (I : Type)
    (sep : CountingFiberSeparationFromNonProp I) :
    Nonempty { w : Witness I // ValidExtractionWitness I w } :=
  ⟨extract_witness_from_counting_fiber_separation I sep⟩

def NonPropFinalCarrierInvariant
    (I : Type) : Prop :=
  Nonempty { w : Witness I // ValidExtractionWitness I w }

theorem counting_implies_nonprop_final_carrier_invariant
    (I : Type)
    (sep : CountingFiberSeparationFromNonProp I) :
    NonPropFinalCarrierInvariant I :=
  counting_implies_nonempty I sep

def UniversalFiberEntropyGap
    (I : Type) : Prop :=
  NonPropFinalCarrierInvariant I

theorem counting_implies_universal_fiber_entropy_gap
    (I : Type)
    (sep : CountingFiberSeparationFromNonProp I) :
    UniversalFiberEntropyGap I :=
  counting_implies_nonprop_final_carrier_invariant I sep

def ChronosRR
    (I : Type) : Prop :=
  UniversalFiberEntropyGap I

theorem counting_implies_chronos_rr
    (I : Type)
    (sep : CountingFiberSeparationFromNonProp I) :
    ChronosRR I :=
  counting_implies_universal_fiber_entropy_gap I sep

def H41FGL
    (I : Type) : Prop :=
  ChronosRR I

theorem counting_implies_h41_fgl
    (I : Type)
    (sep : CountingFiberSeparationFromNonProp I) :
    H41FGL I :=
  counting_implies_chronos_rr I sep

def H41FGLCertificate
    (I : Type) : Type :=
  { w : Witness I // ValidExtractionWitness I w }

structure H41FGLSemanticObject
    (I : Type) where
  carrier : Witness I
  semantically_valid : ValidExtractionWitness I carrier

def interpret_h41_fgl_certificate
    (I : Type)
    (c : H41FGLCertificate I) :
    H41FGLSemanticObject I :=
  ⟨c.1, c.2⟩

def InternalIntendedH41FGL
    (I : Type) : Prop :=
  Nonempty (H41FGLSemanticObject I)

theorem h41_fgl_certificate_sound
    (I : Type)
    (c : H41FGLCertificate I) :
    InternalIntendedH41FGL I :=
  ⟨interpret_h41_fgl_certificate I c⟩

theorem h41_fgl_internal_semantic_adequacy
    (I : Type) :
    H41FGL I → InternalIntendedH41FGL I := by
  intro h
  rcases h with ⟨c⟩
  exact h41_fgl_certificate_sound I c

structure ExternalH41FGLModel
    (I : Type) where
  ExternalCarrier : Type
  interpret : Witness I → ExternalCarrier
  external_property : ExternalCarrier → Prop

def ExternalIntendedH41FGL
    (I : Type)
    (M : ExternalH41FGLModel I) : Prop :=
  ∃ w : Witness I,
    ValidExtractionWitness I w ∧
    M.external_property (M.interpret w)

def ExternalH41FGLPreservation
    (I : Type)
    (M : ExternalH41FGLModel I) : Prop :=
  ∀ w : Witness I,
    ValidExtractionWitness I w →
    M.external_property (M.interpret w)

structure AdmissibleExternalH41FGLModel
    (I : Type) where
  M : ExternalH41FGLModel I
  preserves_validity :
    ∀ w : Witness I,
      ValidExtractionWitness I w →
      M.external_property (M.interpret w)

theorem admissible_external_h41_fgl_preservation
    (I : Type)
    (A : AdmissibleExternalH41FGLModel I) :
    ExternalH41FGLPreservation I A.M := by
  intro w hw
  exact A.preserves_validity w hw

theorem counting_implies_admissible_external_intended_h41_fgl
    (I : Type)
    (A : AdmissibleExternalH41FGLModel I)
    (sep : CountingFiberSeparationFromNonProp I) :
    ExternalIntendedH41FGL I A.M := by
  let c := extract_witness_from_counting_fiber_separation I sep
  exact ⟨c.1, c.2, A.preserves_validity c.1 c.2⟩

def InjectiveMap
    {α β : Type}
    (f : α → β) : Prop :=
  ∀ {x y : α}, f x = f y → x = y

structure NonRepackagedExternalH41FGLModel
    (I : Type) where
  A : AdmissibleExternalH41FGLModel I
  not_validity_repackaging :
    ¬ ∃ f : A.M.ExternalCarrier → Witness I, InjectiveMap f

structure MeaningfulExternalH41FGLModel
    (I : Type) where
  N : NonRepackagedExternalH41FGLModel I
  nonvacuous_property :
    ∃ x : N.A.M.ExternalCarrier, ¬ N.A.M.external_property x

theorem bool_not_injects_witness
    (I : Type) :
    ¬ ∃ f : Bool → Witness I, InjectiveMap f := by
  intro h
  rcases h with ⟨f, hf⟩
  have hsame : f true = f false := Subsingleton.elim _ _
  have hbool : true = false := hf hsame
  cases hbool

def BoolExternalH41FGLModel
    (I : Type) : ExternalH41FGLModel I where
  ExternalCarrier := Bool
  interpret := fun _ => true
  external_property := fun b => b = true

theorem bool_external_h41_fgl_preservation
    (I : Type) :
    ExternalH41FGLPreservation I (BoolExternalH41FGLModel I) := by
  intro w hw
  rfl

def build_meaningful_external_h41_fgl_model
    (I : Type) :
    MeaningfulExternalH41FGLModel I where
  N :=
    { A :=
        { M := BoolExternalH41FGLModel I
          preserves_validity := by
            intro w hw
            rfl }
      not_validity_repackaging := by
        intro h
        exact bool_not_injects_witness I h }
  nonvacuous_property := by
    exact ⟨false, by intro h; cases h⟩

theorem meaningful_external_h41_fgl_model_preservation
    (I : Type) :
    ExternalH41FGLPreservation I
      (build_meaningful_external_h41_fgl_model I).N.A.M :=
  admissible_external_h41_fgl_preservation
    I
    (build_meaningful_external_h41_fgl_model I).N.A

theorem counting_implies_meaningful_external_intended_h41_fgl
    (I : Type)
    (sep : CountingFiberSeparationFromNonProp I) :
    ExternalIntendedH41FGL I
      (build_meaningful_external_h41_fgl_model I).N.A.M :=
  counting_implies_admissible_external_intended_h41_fgl
    I
    (build_meaningful_external_h41_fgl_model I).N.A
    sep

theorem impossible_external_preservation_refuted
    (I : Type)
    (sep : CountingFiberSeparationFromNonProp I) :
    ¬ ExternalH41FGLPreservation I
      { ExternalCarrier := Witness I
        interpret := fun w => w
        external_property := fun _ => False } := by
  intro preserve
  let c := extract_witness_from_counting_fiber_separation I sep
  exact preserve c.1 c.2

end MeaningfulExternalH41FGLToyClosure
end Frontier
end Chronos
