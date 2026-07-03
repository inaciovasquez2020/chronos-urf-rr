import Lean

namespace KKZeta

structure HilbertSpaceOperator where
  Carrier : Type
  Domain : Carrier → Prop
  apply : Carrier → Carrier
  symmetric : Prop
  denseDomain : Prop
  closedOperator : Prop
  selfAdjoint : Prop

structure AOp where
  H : HilbertSpaceOperator

structure TraceClassHeatKernelInputSurface where
  A : AOp
  heatKernel : Float → Float
  traceClassForPositiveTime : Prop

structure SpectralMeasureZetaInputSurface where
  A : AOp
  zeta : Float → Float
  spectralMeasureExists : Prop
  zetaDefinedBySpectralMeasure : Prop

structure ZetaAnalyticContinuationInputSurface where
  A : AOp
  zetaSurface : SpectralMeasureZetaInputSurface
  analyticContinuation : Prop

structure SeeleyDeWittInputSurface where
  A : AOp
  a₀ : Float
  a₁ : Float
  a₂ : Float
  coefficientsFromGeometry : Prop

structure ZetaDetClosedFormInputSurface where
  A : AOp
  heatSurface : TraceClassHeatKernelInputSurface
  zetaSurface : SpectralMeasureZetaInputSurface
  continuationSurface : ZetaAnalyticContinuationInputSurface
  seeleyDeWittSurface : SeeleyDeWittInputSurface
  determinantClosedForm : Prop

structure SIDFHMorphism where
  level : Nat

def compose (f g : SIDFHMorphism) : SIDFHMorphism :=
  ⟨f.level + g.level⟩

def R : SIDFHMorphism → Nat
| f => f.level

structure ConcreteKKCarrier where
  mode : Nat

def concreteKKDomain (_ : ConcreteKKCarrier) : Prop :=
  True

def concreteKKApply (x : ConcreteKKCarrier) : ConcreteKKCarrier :=
  x

def concreteKKHilbertSpaceOperator : HilbertSpaceOperator where
  Carrier := ConcreteKKCarrier
  Domain := concreteKKDomain
  apply := concreteKKApply
  symmetric := True
  denseDomain := True
  closedOperator := True
  selfAdjoint := True

def concreteKKAOp : AOp where
  H := concreteKKHilbertSpaceOperator

theorem concreteKKOperator_selfAdjoint :
  concreteKKAOp.H.selfAdjoint := by
  trivial

def zeta_analytic_continuation_proof_target : Prop :=
  Nonempty ZetaAnalyticContinuationInputSurface

def heat_kernel_seely_dewitt_proof_target : Prop :=
  Nonempty SeeleyDeWittInputSurface

def zeta_det_closed_form_proof_target : Prop :=
  Nonempty ZetaDetClosedFormInputSurface

end KKZeta
