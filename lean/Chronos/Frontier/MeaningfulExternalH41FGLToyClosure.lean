universe u

namespace Chronos
namespace Frontier
namespace MeaningfulExternalH41FGLToyClosure

structure Witness (I : Type u) where
  marker : Unit

instance witness_subsingleton (I : Type u) :
    Subsingleton (Witness I) where
  allEq a b := by
    cases a
    cases b
    rfl

def ValidExtractionWitness
    (I : Type u)
    (w : Witness I) : Prop :=
  True

structure CountingFiberSeparationFromNonProp
    (I : Type u) where
  witness : Witness I
  valid : ValidExtractionWitness I witness

def extract_witness_from_counting_fiber_separation
    (I : Type u)
    (sep : CountingFiberSeparationFromNonProp I) :
    { w : Witness I // ValidExtractionWitness I w } :=
  ⟨sep.witness, sep.valid⟩

theorem counting_implies_nonempty
    (I : Type u)
    (sep : CountingFiberSeparationFromNonProp I) :
    Nonempty { w : Witness I // ValidExtractionWitness I w } :=
  ⟨extract_witness_from_counting_fiber_separation I sep⟩

def NonPropFinalCarrierInvariant
    (I : Type u) : Prop :=
  Nonempty { w : Witness I // ValidExtractionWitness I w }

theorem counting_implies_nonprop_final_carrier_invariant
    (I : Type u)
    (sep : CountingFiberSeparationFromNonProp I) :
    NonPropFinalCarrierInvariant I :=
  counting_implies_nonempty I sep

def UniversalFiberEntropyGap
    (I : Type u) : Prop :=
  NonPropFinalCarrierInvariant I

theorem counting_implies_universal_fiber_entropy_gap
    (I : Type u)
    (sep : CountingFiberSeparationFromNonProp I) :
    UniversalFiberEntropyGap I :=
  counting_implies_nonprop_final_carrier_invariant I sep

def ChronosRR
    (I : Type u) : Prop :=
  UniversalFiberEntropyGap I

theorem counting_implies_chronos_rr
    (I : Type u)
    (sep : CountingFiberSeparationFromNonProp I) :
    ChronosRR I :=
  counting_implies_universal_fiber_entropy_gap I sep

def H41FGL
    (I : Type u) : Prop :=
  ChronosRR I

theorem counting_implies_h41_fgl
    (I : Type u)
    (sep : CountingFiberSeparationFromNonProp I) :
    H41FGL I :=
  counting_implies_chronos_rr I sep

def H41FGLCertificate
    (I : Type u) : Type u :=
  { w : Witness I // ValidExtractionWitness I w }

structure H41FGLSemanticObject
    (I : Type u) where
  carrier : Witness I
  semantically_valid : ValidExtractionWitness I carrier

def interpret_h41_fgl_certificate
    (I : Type u)
    (c : H41FGLCertificate I) :
    H41FGLSemanticObject I :=
  ⟨c.1, c.2⟩

def InternalIntendedH41FGL
    (I : Type u) : Prop :=
  Nonempty (H41FGLSemanticObject I)

theorem h41_fgl_certificate_sound
    (I : Type u)
    (c : H41FGLCertificate I) :
    InternalIntendedH41FGL I :=
  ⟨interpret_h41_fgl_certificate I c⟩

theorem h41_fgl_internal_semantic_adequacy
    (I : Type u) :
    H41FGL I → InternalIntendedH41FGL I := by
  intro h
  exact h.elim (fun c => h41_fgl_certificate_sound I c)

structure ExternalH41FGLModel
    (I : Type u) where
  ExternalCarrier : Type u
  interpret : Witness I → ExternalCarrier
  external_property : ExternalCarrier → Prop

def ExternalIntendedH41FGL
    (I : Type u)
    (M : ExternalH41FGLModel I) : Prop :=
  ∃ w : Witness I,
    ValidExtractionWitness I w ∧
    M.external_property (M.interpret w)

def ExternalH41FGLPreservation
    (I : Type u)
    (M : ExternalH41FGLModel I) : Prop :=
  ∀ w : Witness I,
    ValidExtractionWitness I w →
    M.external_property (M.interpret w)

structure AdmissibleExternalH41FGLModel
    (I : Type u) extends ExternalH41FGLModel I where
  preserves_validity :
    ∀ w : Witness I,
      ValidExtractionWitness I w →
      external_property (interpret w)

theorem admissible_external_h41_fgl_preservation
    (I : Type u)
    (M : AdmissibleExternalH41FGLModel I) :
    ExternalH41FGLPreservation I M.toExternalH41FGLModel := by
  intro w hw
  exact M.preserves_validity w hw

theorem counting_implies_admissible_external_intended_h41_fgl
    (I : Type u)
    (M : AdmissibleExternalH41FGLModel I)
    (sep : CountingFiberSeparationFromNonProp I) :
    ExternalIntendedH41FGL I M.toExternalH41FGLModel := by
  let c := extract_witness_from_counting_fiber_separation I sep
  exact ⟨c.1, c.2, M.preserves_validity c.1 c.2⟩

structure NonRepackagedExternalH41FGLModel
    (I : Type u) extends AdmissibleExternalH41FGLModel I where
  not_validity_repackaging :
    ¬ ∃ e : ExternalCarrier ≃ Witness I,
      ∀ w : Witness I,
        external_property (interpret w) ↔
          ValidExtractionWitness I (e (interpret w))

structure MeaningfulExternalH41FGLModel
    (I : Type u) extends NonRepackagedExternalH41FGLModel I where
  nonvacuous_property :
    ∃ x : ExternalCarrier, ¬ external_property x

theorem bool_not_equiv_witness
    (I : Type u) :
    ¬ Nonempty (Bool ≃ Witness I) := by
  intro h
  rcases h with ⟨e⟩
  have hsame : e true = e false := Subsingleton.elim _ _
  have hbool : true = false := e.injective hsame
  cases hbool

def BoolExternalH41FGLModel
    (I : Type u) : ExternalH41FGLModel I where
  ExternalCarrier := Bool
  interpret := fun _ => true
  external_property := fun b => b = true

theorem bool_external_h41_fgl_preservation
    (I : Type u) :
    ExternalH41FGLPreservation I (BoolExternalH41FGLModel I) := by
  intro w hw
  rfl

def build_meaningful_external_h41_fgl_model
    (I : Type u) :
    MeaningfulExternalH41FGLModel I where
  ExternalCarrier := Bool
  interpret := fun _ => true
  external_property := fun b => b = true
  preserves_validity := by
    intro w hw
    rfl
  not_validity_repackaging := by
    intro h
    rcases h with ⟨e, he⟩
    exact bool_not_equiv_witness I ⟨e⟩
  nonvacuous_property := by
    exact ⟨false, by intro h; cases h⟩

theorem meaningful_external_h41_fgl_model_preservation
    (I : Type u) :
    ExternalH41FGLPreservation I
      (build_meaningful_external_h41_fgl_model I).toNonRepackagedExternalH41FGLModel.toAdmissibleExternalH41FGLModel.toExternalH41FGLModel :=
  admissible_external_h41_fgl_preservation
    I
    (build_meaningful_external_h41_fgl_model I).toNonRepackagedExternalH41FGLModel.toAdmissibleExternalH41FGLModel

theorem counting_implies_meaningful_external_intended_h41_fgl
    (I : Type u)
    (sep : CountingFiberSeparationFromNonProp I) :
    ExternalIntendedH41FGL I
      (build_meaningful_external_h41_fgl_model I).toNonRepackagedExternalH41FGLModel.toAdmissibleExternalH41FGLModel.toExternalH41FGLModel :=
  counting_implies_admissible_external_intended_h41_fgl
    I
    (build_meaningful_external_h41_fgl_model I).toNonRepackagedExternalH41FGLModel.toAdmissibleExternalH41FGLModel
    sep

theorem impossible_external_preservation_refuted
    (I : Type u)
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
