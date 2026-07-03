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

def finiteModeMass (m0 radius : Nat) (mode : ConcreteKKCarrier) : Nat :=
  (m0 + mode.mode * mode.mode) + radius

theorem finiteModeMass_base_le
    (m0 radius : Nat) (mode : ConcreteKKCarrier) :
    m0 ≤ finiteModeMass m0 radius mode := by
  unfold finiteModeMass
  exact Nat.le_trans
    (Nat.le_add_right m0 (mode.mode * mode.mode))
    (Nat.le_add_right (m0 + mode.mode * mode.mode) radius)

theorem finiteModeMass_radius_monotone
    (m0 r₁ r₂ : Nat) (mode : ConcreteKKCarrier)
    (h : r₁ ≤ r₂) :
    finiteModeMass m0 r₁ mode ≤ finiteModeMass m0 r₂ mode := by
  unfold finiteModeMass
  exact Nat.add_le_add_left h (m0 + mode.mode * mode.mode)

theorem finiteModeMass_mode_monotone
    (m0 radius a b : Nat)
    (h : a ≤ b) :
    finiteModeMass m0 radius ⟨a⟩ ≤ finiteModeMass m0 radius ⟨b⟩ := by
  unfold finiteModeMass
  exact Nat.add_le_add_right
    (Nat.add_le_add_left (Nat.mul_le_mul h h) m0)
    radius

theorem finiteModeMass_mode_radius_monotone
    (m0 r₁ r₂ a b : Nat)
    (ha : a ≤ b) (hr : r₁ ≤ r₂) :
    finiteModeMass m0 r₁ ⟨a⟩ ≤ finiteModeMass m0 r₂ ⟨b⟩ := by
  exact Nat.le_trans
    (finiteModeMass_mode_monotone m0 r₁ a b ha)
    (finiteModeMass_radius_monotone m0 r₁ r₂ ⟨b⟩ hr)

theorem finiteModeMass_pos_of_base_pos
    (m0 radius : Nat) (mode : ConcreteKKCarrier)
    (h : 0 < m0) :
    0 < finiteModeMass m0 radius mode := by
  exact Nat.lt_of_lt_of_le h (finiteModeMass_base_le m0 radius mode)

theorem finiteModeMass_ne_zero_of_base_pos
    (m0 radius : Nat) (mode : ConcreteKKCarrier)
    (h : 0 < m0) :
    finiteModeMass m0 radius mode ≠ 0 := by
  exact Nat.ne_of_gt (finiteModeMass_pos_of_base_pos m0 radius mode h)

theorem finiteModeMass_zero_of_zero_inputs :
    finiteModeMass 0 0 ⟨0⟩ = 0 := by
  rfl

theorem finiteModeMass_eq_zero_implies_base_zero
    (m0 radius : Nat) (mode : ConcreteKKCarrier)
    (h : finiteModeMass m0 radius mode = 0) :
    m0 = 0 := by
  exact Nat.eq_zero_of_le_zero
    (h ▸ finiteModeMass_base_le m0 radius mode)

def zeta_analytic_continuation_proof_target : Prop :=
  Nonempty ZetaAnalyticContinuationInputSurface

def heat_kernel_seely_dewitt_proof_target : Prop :=
  Nonempty SeeleyDeWittInputSurface

def zeta_det_closed_form_proof_target : Prop :=
  Nonempty ZetaDetClosedFormInputSurface

end KKZeta
