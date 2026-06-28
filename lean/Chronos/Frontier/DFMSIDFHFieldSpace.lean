namespace Chronos.Frontier

/--
Minimal DFM/SIDFH field-space carrier interface.

This only exposes the state type needed by later probe/operator surfaces.
-/
structure DFMSIDFHFieldSpace where
  State : Type


/--
Minimal spectral probe interface over a DFM/SIDFH field space.
-/
structure DFMSIDFHSpectralProbe (X : DFMSIDFHFieldSpace) where
  Probe : Type


/--
Minimal probe-operator interface at a field-space state.
-/
structure DFMSIDFHProbeOperator (X : DFMSIDFHFieldSpace) (x : X.State) where
  Operator : Type


/--
Minimal renormalized log-determinant datum carrying quotient classes.
-/
structure RenormalizedLogDetDatum where
  QuotientClass : Type
  representsRenormalizedLogDet : QuotientClass → Prop


/--
Minimal finite-jet curvature auxiliary action interface at a field-space state.
-/
structure FiniteJetCurvatureAuxAction
    (X : DFMSIDFHFieldSpace)
    (x : X.State) where
  AuxAction : Type

/--
Minimal finite-jet equivalence witness interface at a quotient-class test site.
-/
structure FiniteJetEquivalenceWitness
    (X : DFMSIDFHFieldSpace)
    (x : X.State)
    (QuotientClass : Type)
    (A : FiniteJetCurvatureAuxAction X x) where
  Witness : Type

/--
Minimal nonlocal renormalized log-determinant interface attached to a spectral
probe.
-/
structure NonlocalRenormalizedLogDet
    {X : DFMSIDFHFieldSpace}
    (S : DFMSIDFHSpectralProbe X) where
  RenormalizedLogDet :
    (x : X.State) →
    DFMSIDFHProbeOperator X x →
    RenormalizedLogDetDatum
  FiniteJetEquivalent :
    (x : X.State) →
    (P : DFMSIDFHProbeOperator X x) →
    (Q : (RenormalizedLogDet x P).QuotientClass) →
    (hdet : (RenormalizedLogDet x P).representsRenormalizedLogDet Q) →
    (A : FiniteJetCurvatureAuxAction X x) →
    FiniteJetEquivalenceWitness
        X
        x
        (RenormalizedLogDet x P).QuotientClass
        A →
    Prop






/--
Minimal spectral nonlocality witness: a detected Green-kernel tail and a
finite-jet exclusion jointly obstruct finite-jet equivalence.
-/
structure SpectralNonlocalityWitness
    {X : DFMSIDFHFieldSpace}
    {S : DFMSIDFHSpectralProbe X}
    (I : NonlocalRenormalizedLogDet S)
    (x : X.State)
    (P : DFMSIDFHProbeOperator X x)
    (Q : (I.RenormalizedLogDet x P).QuotientClass)
    (hdet : (I.RenormalizedLogDet x P).representsRenormalizedLogDet Q)
    (A : FiniteJetCurvatureAuxAction X x)
    (W : FiniteJetEquivalenceWitness
        X
        x
        (I.RenormalizedLogDet x P).QuotientClass
        A) where
  GreenKernelTail : Type
  spectralVariationHasGreenKernelTail : Prop
  finiteJetVariationHasNoGreenKernelTail : Prop
  greenKernelTailObstructsFiniteJetEquivalence :
    spectralVariationHasGreenKernelTail →
    finiteJetVariationHasNoGreenKernelTail →
    ¬ I.FiniteJetEquivalent x P Q hdet A W


/--
Uniform finite-jet spectral nonlocality package.

For every finite-jet auxiliary action and equivalence witness, it supplies a
spectral nonlocality witness together with the two active hypotheses needed by
that witness.
-/
structure AllFiniteJetSpectralNonlocality
    {X : DFMSIDFHFieldSpace}
    {S : DFMSIDFHSpectralProbe X}
    (I : NonlocalRenormalizedLogDet S)
    (x : X.State)
    (P : DFMSIDFHProbeOperator X x)
    (Q : (I.RenormalizedLogDet x P).QuotientClass)
    (hdet : (I.RenormalizedLogDet x P).representsRenormalizedLogDet Q) where
  witness :
    ∀ A : FiniteJetCurvatureAuxAction X x,
    ∀ W : FiniteJetEquivalenceWitness
        X
        x
        (I.RenormalizedLogDet x P).QuotientClass
        A,
      SpectralNonlocalityWitness I x P Q hdet A W
  spectralTail :
    ∀ A : FiniteJetCurvatureAuxAction X x,
    ∀ W : FiniteJetEquivalenceWitness
        X
        x
        (I.RenormalizedLogDet x P).QuotientClass
        A,
      (witness A W).spectralVariationHasGreenKernelTail
  finiteJetNoTail :
    ∀ A : FiniteJetCurvatureAuxAction X x,
    ∀ W : FiniteJetEquivalenceWitness
        X
        x
        (I.RenormalizedLogDet x P).QuotientClass
        A,
      (witness A W).finiteJetVariationHasNoGreenKernelTail


/--
Pointwise Green-kernel tail criterion.

At one finite-jet test surface, a detected spectral tail together with a
finite-jet no-tail exclusion obstructs finite-jet equivalence.
-/
structure GreenKernelTailCriterion
    {X : DFMSIDFHFieldSpace}
    {S : DFMSIDFHSpectralProbe X}
    (I : NonlocalRenormalizedLogDet S)
    (x : X.State)
    (P : DFMSIDFHProbeOperator X x)
    (Q : (I.RenormalizedLogDet x P).QuotientClass)
    (hdet : (I.RenormalizedLogDet x P).representsRenormalizedLogDet Q)
    (A : FiniteJetCurvatureAuxAction X x)
    (W : FiniteJetEquivalenceWitness
        X
        x
        (I.RenormalizedLogDet x P).QuotientClass
        A) where
  spectralTailDetected : Prop
  finiteJetTailExcluded : Prop
  obstructionSound :
    spectralTailDetected →
    finiteJetTailExcluded →
    ¬ I.FiniteJetEquivalent x P Q hdet A W


/--
A pointwise Green-kernel tail criterion gives a spectral nonlocality witness at
the same finite-jet test surface.
-/
def green_kernel_tail_criterion_to_spectral_nonlocality_witness
    {X : DFMSIDFHFieldSpace}
    {S : DFMSIDFHSpectralProbe X}
    (I : NonlocalRenormalizedLogDet S)
    (x : X.State)
    (P : DFMSIDFHProbeOperator X x)
    (Q : (I.RenormalizedLogDet x P).QuotientClass)
    (hdet : (I.RenormalizedLogDet x P).representsRenormalizedLogDet Q)
    (A : FiniteJetCurvatureAuxAction X x)
    (W : FiniteJetEquivalenceWitness
        X
        x
        (I.RenormalizedLogDet x P).QuotientClass
        A)
    (C : GreenKernelTailCriterion I x P Q hdet A W) :
    SpectralNonlocalityWitness I x P Q hdet A W where
  GreenKernelTail := Unit
  spectralVariationHasGreenKernelTail := C.spectralTailDetected
  finiteJetVariationHasNoGreenKernelTail := C.finiteJetTailExcluded
  greenKernelTailObstructsFiniteJetEquivalence := C.obstructionSound


/--
A pointwise Green-kernel tail criterion refutes finite-jet equivalence once the
two recorded criterion propositions are supplied as proofs.
-/
theorem green_kernel_tail_criterion_to_finite_jet_nonabsorption
    {X : DFMSIDFHFieldSpace}
    {S : DFMSIDFHSpectralProbe X}
    (I : NonlocalRenormalizedLogDet S)
    (x : X.State)
    (P : DFMSIDFHProbeOperator X x)
    (Q : (I.RenormalizedLogDet x P).QuotientClass)
    (hdet : (I.RenormalizedLogDet x P).representsRenormalizedLogDet Q)
    (A : FiniteJetCurvatureAuxAction X x)
    (W : FiniteJetEquivalenceWitness
        X
        x
        (I.RenormalizedLogDet x P).QuotientClass
        A)
    (C : GreenKernelTailCriterion I x P Q hdet A W)
    (hspec : C.spectralTailDetected)
    (hfin : C.finiteJetTailExcluded) :
    ¬ I.FiniteJetEquivalent x P Q hdet A W :=
  C.obstructionSound hspec hfin


/--
Uniform analytic package supplying a Green-kernel tail criterion at every
finite-jet test surface.

This remains a criterion package: it records the pointwise analytic input; it
does not construct the analytic Green-kernel estimates.
-/
structure AnalyticGreenKernelTailCriterionPackage
    {X : DFMSIDFHFieldSpace}
    {S : DFMSIDFHSpectralProbe X}
    (I : NonlocalRenormalizedLogDet S)
    (x : X.State)
    (P : DFMSIDFHProbeOperator X x)
    (Q : (I.RenormalizedLogDet x P).QuotientClass)
    (hdet : (I.RenormalizedLogDet x P).representsRenormalizedLogDet Q) where
  criterionAt :
    ∀ A : FiniteJetCurvatureAuxAction X x,
    ∀ W : FiniteJetEquivalenceWitness
        X
        x
        (I.RenormalizedLogDet x P).QuotientClass
        A,
      GreenKernelTailCriterion I x P Q hdet A W
  spectralTailAt :
    ∀ A : FiniteJetCurvatureAuxAction X x,
    ∀ W : FiniteJetEquivalenceWitness
        X
        x
        (I.RenormalizedLogDet x P).QuotientClass
        A,
      (criterionAt A W).spectralTailDetected
  finiteJetNoTailAt :
    ∀ A : FiniteJetCurvatureAuxAction X x,
    ∀ W : FiniteJetEquivalenceWitness
        X
        x
        (I.RenormalizedLogDet x P).QuotientClass
        A,
      (criterionAt A W).finiteJetTailExcluded


/--
A uniform analytic Green-kernel tail criterion package yields all finite-jet
spectral nonlocality.
-/
def analytic_green_kernel_tail_package_to_all_finite_jet_nonabsorption
    {X : DFMSIDFHFieldSpace}
    {S : DFMSIDFHSpectralProbe X}
    (I : NonlocalRenormalizedLogDet S)
    (x : X.State)
    (P : DFMSIDFHProbeOperator X x)
    (Q : (I.RenormalizedLogDet x P).QuotientClass)
    (hdet : (I.RenormalizedLogDet x P).representsRenormalizedLogDet Q)
    (Pkg : AnalyticGreenKernelTailCriterionPackage I x P Q hdet) :
    AllFiniteJetSpectralNonlocality I x P Q hdet where
  witness :=
    fun A W =>
      green_kernel_tail_criterion_to_spectral_nonlocality_witness
        I x P Q hdet A W (Pkg.criterionAt A W)
  spectralTail :=
    fun A W =>
      Pkg.spectralTailAt A W
  finiteJetNoTail :=
    fun A W =>
      Pkg.finiteJetNoTailAt A W



/--
Pointwise analytic Green-kernel estimate input surface.

This is weaker than an internal proof of Green-kernel estimates: it records the
two estimate-side propositions and the obstruction implication at one finite-jet
test surface.
-/
structure AnalyticGreenKernelEstimateInputSurface
    {X : DFMSIDFHFieldSpace}
    {S : DFMSIDFHSpectralProbe X}
    (I : NonlocalRenormalizedLogDet S)
    (x : X.State)
    (P : DFMSIDFHProbeOperator X x)
    (Q : (I.RenormalizedLogDet x P).QuotientClass)
    (hdet : (I.RenormalizedLogDet x P).representsRenormalizedLogDet Q)
    (A : FiniteJetCurvatureAuxAction X x)
    (W : FiniteJetEquivalenceWitness
        X
        x
        (I.RenormalizedLogDet x P).QuotientClass
        A) where
  spectralTailEstimate : Prop
  finiteJetTailExclusionEstimate : Prop
  estimatesObstructFiniteJetEquivalence :
    spectralTailEstimate →
    finiteJetTailExclusionEstimate →
    ¬ I.FiniteJetEquivalent x P Q hdet A W


/--
A pointwise analytic Green-kernel estimate input surface yields the corresponding
pointwise Green-kernel tail criterion.
-/
def analytic_green_kernel_estimate_input_surface_to_green_kernel_tail_criterion
    {X : DFMSIDFHFieldSpace}
    {S : DFMSIDFHSpectralProbe X}
    (I : NonlocalRenormalizedLogDet S)
    (x : X.State)
    (P : DFMSIDFHProbeOperator X x)
    (Q : (I.RenormalizedLogDet x P).QuotientClass)
    (hdet : (I.RenormalizedLogDet x P).representsRenormalizedLogDet Q)
    (A : FiniteJetCurvatureAuxAction X x)
    (W : FiniteJetEquivalenceWitness
        X
        x
        (I.RenormalizedLogDet x P).QuotientClass
        A)
    (E : AnalyticGreenKernelEstimateInputSurface I x P Q hdet A W) :
    GreenKernelTailCriterion I x P Q hdet A W where
  spectralTailDetected := E.spectralTailEstimate
  finiteJetTailExcluded := E.finiteJetTailExclusionEstimate
  obstructionSound := E.estimatesObstructFiniteJetEquivalence


/--
Uniform analytic Green-kernel estimate input surface.

This narrows the analytic boundary from an opaque constructed criterion package
to pointwise estimate inputs at every finite-jet test surface. It still does not
prove those estimates internally.
-/
structure UniformAnalyticGreenKernelEstimateInputSurface
    {X : DFMSIDFHFieldSpace}
    {S : DFMSIDFHSpectralProbe X}
    (I : NonlocalRenormalizedLogDet S)
    (x : X.State)
    (P : DFMSIDFHProbeOperator X x)
    (Q : (I.RenormalizedLogDet x P).QuotientClass)
    (hdet : (I.RenormalizedLogDet x P).representsRenormalizedLogDet Q) where
  estimateAt :
    ∀ A : FiniteJetCurvatureAuxAction X x,
    ∀ W : FiniteJetEquivalenceWitness
        X
        x
        (I.RenormalizedLogDet x P).QuotientClass
        A,
      AnalyticGreenKernelEstimateInputSurface I x P Q hdet A W


/--
Certified uniform analytic Green-kernel estimate input surface.

This strengthens the uniform estimate-input surface only by adding proof
witnesses for the two pointwise estimate propositions. It still leaves the
analytic Green-kernel estimates as external inputs rather than proving them
internally.
-/
structure CertifiedUniformAnalyticGreenKernelEstimateInputSurface
    {X : DFMSIDFHFieldSpace}
    {S : DFMSIDFHSpectralProbe X}
    (I : NonlocalRenormalizedLogDet S)
    (x : X.State)
    (P : DFMSIDFHProbeOperator X x)
    (Q : (I.RenormalizedLogDet x P).QuotientClass)
    (hdet : (I.RenormalizedLogDet x P).representsRenormalizedLogDet Q) where
  estimateAt :
    ∀ A : FiniteJetCurvatureAuxAction X x,
    ∀ W : FiniteJetEquivalenceWitness
        X
        x
        (I.RenormalizedLogDet x P).QuotientClass
        A,
      AnalyticGreenKernelEstimateInputSurface I x P Q hdet A W
  spectralTailEstimateAt :
    ∀ A : FiniteJetCurvatureAuxAction X x,
    ∀ W : FiniteJetEquivalenceWitness
        X
        x
        (I.RenormalizedLogDet x P).QuotientClass
        A,
      (estimateAt A W).spectralTailEstimate
  finiteJetTailExclusionEstimateAt :
    ∀ A : FiniteJetCurvatureAuxAction X x,
    ∀ W : FiniteJetEquivalenceWitness
        X
        x
        (I.RenormalizedLogDet x P).QuotientClass
        A,
      (estimateAt A W).finiteJetTailExclusionEstimate


/--
A certified uniform analytic Green-kernel estimate input surface yields the
uniform Green-kernel tail criterion package.
-/
def certified_uniform_analytic_green_kernel_estimate_input_surface_to_tail_criterion_package
    {X : DFMSIDFHFieldSpace}
    {S : DFMSIDFHSpectralProbe X}
    (I : NonlocalRenormalizedLogDet S)
    (x : X.State)
    (P : DFMSIDFHProbeOperator X x)
    (Q : (I.RenormalizedLogDet x P).QuotientClass)
    (hdet : (I.RenormalizedLogDet x P).representsRenormalizedLogDet Q)
    (C : CertifiedUniformAnalyticGreenKernelEstimateInputSurface I x P Q hdet) :
    AnalyticGreenKernelTailCriterionPackage I x P Q hdet where
  criterionAt :=
    fun A W =>
      analytic_green_kernel_estimate_input_surface_to_green_kernel_tail_criterion
        I x P Q hdet A W (C.estimateAt A W)
  spectralTailAt :=
    fun A W =>
      C.spectralTailEstimateAt A W
  finiteJetNoTailAt :=
    fun A W =>
      C.finiteJetTailExclusionEstimateAt A W


/--
A certified uniform analytic Green-kernel estimate input surface yields all
finite-jet spectral nonlocality.
-/
def certified_uniform_analytic_green_kernel_estimate_input_surface_to_all_finite_jet_nonabsorption
    {X : DFMSIDFHFieldSpace}
    {S : DFMSIDFHSpectralProbe X}
    (I : NonlocalRenormalizedLogDet S)
    (x : X.State)
    (P : DFMSIDFHProbeOperator X x)
    (Q : (I.RenormalizedLogDet x P).QuotientClass)
    (hdet : (I.RenormalizedLogDet x P).representsRenormalizedLogDet Q)
    (C : CertifiedUniformAnalyticGreenKernelEstimateInputSurface I x P Q hdet) :
    AllFiniteJetSpectralNonlocality I x P Q hdet :=
  analytic_green_kernel_tail_package_to_all_finite_jet_nonabsorption
    I x P Q hdet
    (certified_uniform_analytic_green_kernel_estimate_input_surface_to_tail_criterion_package
      I x P Q hdet C)

/--
Analytic construction assumption surface for the uniform Green-kernel tail
criterion package.

This is the current analytic boundary: it records that the Green-kernel tail
criterion package has been analytically constructed, without proving the
Green-kernel estimates internally.
-/
structure AnalyticGreenKernelTailConstructionAssumptions
    {X : DFMSIDFHFieldSpace}
    {S : DFMSIDFHSpectralProbe X}
    (I : NonlocalRenormalizedLogDet S)
    (x : X.State)
    (P : DFMSIDFHProbeOperator X x)
    (Q : (I.RenormalizedLogDet x P).QuotientClass)
    (hdet : (I.RenormalizedLogDet x P).representsRenormalizedLogDet Q) where
  constructedPackage :
    AnalyticGreenKernelTailCriterionPackage I x P Q hdet



/--
A certified uniform analytic Green-kernel estimate input surface supplies the
analytic construction-assumption package by constructing its uniform tail
criterion package.
-/
def certified_uniform_analytic_green_kernel_estimate_input_surface_to_construction_assumptions
    {X : DFMSIDFHFieldSpace}
    {S : DFMSIDFHSpectralProbe X}
    (I : NonlocalRenormalizedLogDet S)
    (x : X.State)
    (P : DFMSIDFHProbeOperator X x)
    (Q : (I.RenormalizedLogDet x P).QuotientClass)
    (hdet : (I.RenormalizedLogDet x P).representsRenormalizedLogDet Q)
    (C : CertifiedUniformAnalyticGreenKernelEstimateInputSurface I x P Q hdet) :
    AnalyticGreenKernelTailConstructionAssumptions I x P Q hdet where
  constructedPackage :=
    certified_uniform_analytic_green_kernel_estimate_input_surface_to_tail_criterion_package
      I x P Q hdet C

/--
The analytic construction-assumption surface yields all finite-jet spectral
nonlocality by exposing its constructed uniform criterion package.
-/
def analytic_green_kernel_tail_construction_assumptions_to_all_finite_jet_nonabsorption
    {X : DFMSIDFHFieldSpace}
    {S : DFMSIDFHSpectralProbe X}
    (I : NonlocalRenormalizedLogDet S)
    (x : X.State)
    (P : DFMSIDFHProbeOperator X x)
    (Q : (I.RenormalizedLogDet x P).QuotientClass)
    (hdet : (I.RenormalizedLogDet x P).representsRenormalizedLogDet Q)
    (A : AnalyticGreenKernelTailConstructionAssumptions I x P Q hdet) :
    AllFiniteJetSpectralNonlocality I x P Q hdet :=
  analytic_green_kernel_tail_package_to_all_finite_jet_nonabsorption
    I x P Q hdet A.constructedPackage

end Chronos.Frontier
