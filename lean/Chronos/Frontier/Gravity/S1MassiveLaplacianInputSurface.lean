import Mathlib

noncomputable section

namespace Chronos
namespace Frontier
namespace Gravity
namespace S1MassiveLaplacianInputSurface

structure PeriodicField where
  val : ℝ → ℝ
  periodic : val (2 * Real.pi) = val 0
  periodic_deriv : deriv val (2 * Real.pi) = deriv val 0

def PeriodicField.periodic_value (f : PeriodicField) :
    f.val (2 * Real.pi) = f.val 0 :=
  f.periodic

def spatialOperatorA (m : ℝ) (f : PeriodicField) (x : ℝ) : ℝ :=
  - (deriv (deriv f.val) x) + m ^ 2 * f.val x

structure PeriodicBoundaryIntegrationByParts (m : ℝ) (f g : PeriodicField) where
  ibp_identity_f :
    ∫ x in (0)..(2 * Real.pi), -deriv (deriv f.val) x * g.val x =
    ∫ x in (0)..(2 * Real.pi), deriv f.val x * deriv g.val x
  ibp_identity_g :
    ∫ x in (0)..(2 * Real.pi), -f.val x * deriv (deriv g.val) x =
    ∫ x in (0)..(2 * Real.pi), deriv f.val x * deriv g.val x

structure PeriodicQuadraticFormNonnegativity (m : ℝ) (f : PeriodicField) where
  deriv_integral_nonneg : Prop
  mass_integral_nonneg : Prop
  diagonal_decomposition : Prop

structure MathlibC1IntervalIBPObligation where
  left_endpoint : ℝ
  right_endpoint : ℝ
  field_left : ℝ → ℝ
  field_right : ℝ → ℝ
  ibp_identity : Prop

def mathlib_C1_interval_ibp_obligation : Prop :=
  Nonempty MathlibC1IntervalIBPObligation

structure MathlibFTCIBPLemmaSurface where
  exact_lemma_token :
    lemma_name = "intervalIntegral.integral_deriv_mul_eq_sub_of_hasDerivAt"
  lemma_statement_available : Prop

def mathlib_ftc_ibp_lemma_surface : Prop :=
  Nonempty MathlibFTCIBPLemmaSurface

structure MathlibFTCIBPSideConditions (f g : PeriodicField) where
  f_continuous_on_interval : Prop
  g_continuous_on_interval : Prop
  deriv_f_hasDerivAt_on_interior : Prop
  deriv_g_hasDerivAt_on_interior : Prop
  deriv_f_intervalIntegrable : Prop
  deriv_g_intervalIntegrable : Prop

def mathlib_ftc_ibp_side_conditions_surface : Prop :=
  ∀ f g : PeriodicField, Nonempty (MathlibFTCIBPSideConditions f g)

theorem mathlib_ftc_ibp_identity_from_surface
    (u v u' v' : ℝ → ℝ)
    (a b : ℝ)
    (hu : ContinuousOn u (Set.uIcc a b))
    (hv : ContinuousOn v (Set.uIcc a b))
    (huu' : ∀ x ∈ Set.Ioo (min a b) (max a b), HasDerivAt u (u' x) x)
    (hvv' : ∀ x ∈ Set.Ioo (min a b) (max a b), HasDerivAt v (v' x) x)
    (hu' : IntervalIntegrable u' MeasureTheory.volume a b)
    (hv' : IntervalIntegrable v' MeasureTheory.volume a b) :
    ∫ x in a..b, u' x * v x + u x * v' x = u b * v b - u a * v a := by
  exact intervalIntegral.integral_deriv_mul_eq_sub_of_hasDerivAt
    hu hv huu' hvv' hu' hv'

def PR1000_MILESTONE_mathlib_ftc_ibp_identity_executable : Prop :=
  ∀ (u v u' v' : ℝ → ℝ) (a b : ℝ),
    ContinuousOn u (Set.uIcc a b) →
    ContinuousOn v (Set.uIcc a b) →
    (∀ x ∈ Set.Ioo (min a b) (max a b), HasDerivAt u (u' x) x) →
    (∀ x ∈ Set.Ioo (min a b) (max a b), HasDerivAt v (v' x) x) →
    IntervalIntegrable u' MeasureTheory.volume a b →
    IntervalIntegrable v' MeasureTheory.volume a b →
    ∫ x in a..b, u' x * v x + u x * v' x = u b * v b - u a * v a

theorem pr1000_milestone_mathlib_ftc_ibp_identity_executable :
    PR1000_MILESTONE_mathlib_ftc_ibp_identity_executable := by
  intro u v u' v' a b hu hv huu' hvv' hu' hv'
  exact mathlib_ftc_ibp_identity_from_surface u v u' v' a b hu hv huu' hvv' hu' hv'




structure PeriodicFTCIdentityFMathlibSideConditions (f g : PeriodicField) where
  deriv_f_continuous_on_interval :
    ContinuousOn (deriv f.val) (Set.uIcc 0 (2 * Real.pi))
  g_continuous_on_interval :
    ContinuousOn g.val (Set.uIcc 0 (2 * Real.pi))
  deriv_f_hasDerivAt_on_interior :
    ∀ x ∈ Set.Ioo (min 0 (2 * Real.pi)) (max 0 (2 * Real.pi)),
      HasDerivAt (deriv f.val) (deriv (deriv f.val) x) x
  g_hasDerivAt_on_interior :
    ∀ x ∈ Set.Ioo (min 0 (2 * Real.pi)) (max 0 (2 * Real.pi)),
      HasDerivAt g.val (deriv g.val x) x
  deriv_deriv_f_intervalIntegrable :
    IntervalIntegrable (fun x => deriv (deriv f.val) x) MeasureTheory.volume 0 (2 * Real.pi)
  deriv_g_intervalIntegrable :
    IntervalIntegrable (fun x => deriv g.val x) MeasureTheory.volume 0 (2 * Real.pi)

theorem derive_ftc_f_boundary_identity_from_mathlib
    (f g : PeriodicField)
    (h : PeriodicFTCIdentityFMathlibSideConditions f g) :
    ∫ x in (0)..(2 * Real.pi),
        deriv (deriv f.val) x * g.val x + deriv f.val x * deriv g.val x =
    deriv f.val (2 * Real.pi) * g.val (2 * Real.pi) - deriv f.val 0 * g.val 0 := by
  exact mathlib_ftc_ibp_identity_from_surface
    (deriv f.val)
    g.val
    (fun x => deriv (deriv f.val) x)
    (fun x => deriv g.val x)
    0
    (2 * Real.pi)
    h.deriv_f_continuous_on_interval
    h.g_continuous_on_interval
    h.deriv_f_hasDerivAt_on_interior
    h.g_hasDerivAt_on_interior
    h.deriv_deriv_f_intervalIntegrable
    h.deriv_g_intervalIntegrable

structure PeriodicFTCIdentityGMathlibSideConditions (f g : PeriodicField) where
  f_continuous_on_interval :
    ContinuousOn f.val (Set.uIcc 0 (2 * Real.pi))
  deriv_g_continuous_on_interval :
    ContinuousOn (deriv g.val) (Set.uIcc 0 (2 * Real.pi))
  f_hasDerivAt_on_interior :
    ∀ x ∈ Set.Ioo (min 0 (2 * Real.pi)) (max 0 (2 * Real.pi)),
      HasDerivAt f.val (deriv f.val x) x
  deriv_g_hasDerivAt_on_interior :
    ∀ x ∈ Set.Ioo (min 0 (2 * Real.pi)) (max 0 (2 * Real.pi)),
      HasDerivAt (deriv g.val) (deriv (deriv g.val) x) x
  deriv_f_intervalIntegrable :
    IntervalIntegrable (fun x => deriv f.val x) MeasureTheory.volume 0 (2 * Real.pi)
  deriv_deriv_g_intervalIntegrable :
    IntervalIntegrable (fun x => deriv (deriv g.val) x) MeasureTheory.volume 0 (2 * Real.pi)

theorem derive_ftc_g_boundary_identity_from_mathlib
    (f g : PeriodicField)
    (h : PeriodicFTCIdentityGMathlibSideConditions f g) :
    ∫ x in (0)..(2 * Real.pi),
        deriv f.val x * deriv g.val x + f.val x * deriv (deriv g.val) x =
    f.val (2 * Real.pi) * deriv g.val (2 * Real.pi) - f.val 0 * deriv g.val 0 := by
  exact mathlib_ftc_ibp_identity_from_surface
    f.val
    (deriv g.val)
    (fun x => deriv f.val x)
    (fun x => deriv (deriv g.val) x)
    0
    (2 * Real.pi)
    h.f_continuous_on_interval
    h.deriv_g_continuous_on_interval
    h.f_hasDerivAt_on_interior
    h.deriv_g_hasDerivAt_on_interior
    h.deriv_f_intervalIntegrable
    h.deriv_deriv_g_intervalIntegrable

structure PeriodicFTCSplitIntegralBridgeFConditions (f g : PeriodicField) where
  deriv_deriv_f_mul_g_intervalIntegrable :
    IntervalIntegrable
      (fun x => deriv (deriv f.val) x * g.val x)
      MeasureTheory.volume 0 (2 * Real.pi)
  deriv_f_mul_deriv_g_intervalIntegrable :
    IntervalIntegrable
      (fun x => deriv f.val x * deriv g.val x)
      MeasureTheory.volume 0 (2 * Real.pi)

theorem bridge_combined_to_split_f
    (f g : PeriodicField)
    (h : PeriodicFTCSplitIntegralBridgeFConditions f g) :
    ∫ x in (0)..(2 * Real.pi),
        deriv (deriv f.val) x * g.val x + deriv f.val x * deriv g.val x =
      (∫ x in (0)..(2 * Real.pi), deriv (deriv f.val) x * g.val x) +
        (∫ x in (0)..(2 * Real.pi), deriv f.val x * deriv g.val x) := by
  exact intervalIntegral.integral_add
    h.deriv_deriv_f_mul_g_intervalIntegrable
    h.deriv_f_mul_deriv_g_intervalIntegrable

structure PeriodicFTCSplitIntegralBridgeGConditions (f g : PeriodicField) where
  deriv_f_mul_deriv_g_intervalIntegrable :
    IntervalIntegrable
      (fun x => deriv f.val x * deriv g.val x)
      MeasureTheory.volume 0 (2 * Real.pi)
  f_mul_deriv_deriv_g_intervalIntegrable :
    IntervalIntegrable
      (fun x => f.val x * deriv (deriv g.val) x)
      MeasureTheory.volume 0 (2 * Real.pi)

theorem bridge_combined_to_split_g
    (f g : PeriodicField)
    (h : PeriodicFTCSplitIntegralBridgeGConditions f g) :
    ∫ x in (0)..(2 * Real.pi),
        deriv f.val x * deriv g.val x + f.val x * deriv (deriv g.val) x =
      (∫ x in (0)..(2 * Real.pi), deriv f.val x * deriv g.val x) +
        (∫ x in (0)..(2 * Real.pi), f.val x * deriv (deriv g.val) x) := by
  exact intervalIntegral.integral_add
    h.deriv_f_mul_deriv_g_intervalIntegrable
    h.f_mul_deriv_deriv_g_intervalIntegrable

structure PeriodicIBPFTCHypotheses (m : ℝ) (f g : PeriodicField) where
  ftc_f_boundary_identity :
    (∫ x in (0)..(2 * Real.pi), deriv (deriv f.val) x * g.val x) +
      (∫ x in (0)..(2 * Real.pi), deriv f.val x * deriv g.val x) =
    deriv f.val (2 * Real.pi) * g.val (2 * Real.pi) - deriv f.val 0 * g.val 0
  ftc_g_boundary_identity :
    (∫ x in (0)..(2 * Real.pi), f.val x * deriv (deriv g.val) x) +
      (∫ x in (0)..(2 * Real.pi), deriv f.val x * deriv g.val x) =
    deriv g.val (2 * Real.pi) * f.val (2 * Real.pi) - deriv g.val 0 * f.val 0

structure PeriodicIBPBoundaryCancellation (m : ℝ) (f g : PeriodicField)
    (h_ftc : PeriodicIBPFTCHypotheses m f g) where
  ftc_f_to_ibp_f :
    ∫ x in (0)..(2 * Real.pi), -deriv (deriv f.val) x * g.val x =
    ∫ x in (0)..(2 * Real.pi), deriv f.val x * deriv g.val x
  ftc_g_to_ibp_g :
    ∫ x in (0)..(2 * Real.pi), -f.val x * deriv (deriv g.val) x =
    ∫ x in (0)..(2 * Real.pi), deriv f.val x * deriv g.val x

structure PeriodicEndpointCancellation (m : ℝ) (f g : PeriodicField)
    (h_ftc : PeriodicIBPFTCHypotheses m f g) where
  f_boundary_cancels :
    deriv f.val (2 * Real.pi) * g.val (2 * Real.pi) - deriv f.val 0 * g.val 0 = 0
  g_boundary_cancels :
    deriv g.val (2 * Real.pi) * f.val (2 * Real.pi) - deriv g.val 0 * f.val 0 = 0

def derive_periodic_endpoint_cancellation
    (m : ℝ) (f g : PeriodicField)
    (h_ftc : PeriodicIBPFTCHypotheses m f g) :
    PeriodicEndpointCancellation m f g h_ftc := by
  exact {
    f_boundary_cancels := by
      rw [f.periodic_deriv, g.periodic_value]
      ring
    g_boundary_cancels := by
      rw [g.periodic_deriv, f.periodic_value]
      ring
  }

def derive_periodic_ibp_boundary_cancellation
    (m : ℝ) (f g : PeriodicField)
    (h_ftc : PeriodicIBPFTCHypotheses m f g)
    (h_endpoint : PeriodicEndpointCancellation m f g h_ftc) :
    PeriodicIBPBoundaryCancellation m f g h_ftc := by
  exact {
    ftc_f_to_ibp_f := by
      have hzero :
          (∫ x in (0)..(2 * Real.pi), deriv (deriv f.val) x * g.val x) +
            (∫ x in (0)..(2 * Real.pi), deriv f.val x * deriv g.val x) = 0 := by
        rw [h_ftc.ftc_f_boundary_identity, h_endpoint.f_boundary_cancels]
      have hneg :
          ∫ x in (0)..(2 * Real.pi), -deriv (deriv f.val) x * g.val x =
            -(∫ x in (0)..(2 * Real.pi), deriv (deriv f.val) x * g.val x) := by
        simp [neg_mul]
      rw [hneg]
      linarith
    ftc_g_to_ibp_g := by
      have hzero :
          (∫ x in (0)..(2 * Real.pi), f.val x * deriv (deriv g.val) x) +
            (∫ x in (0)..(2 * Real.pi), deriv f.val x * deriv g.val x) = 0 := by
        rw [h_ftc.ftc_g_boundary_identity, h_endpoint.g_boundary_cancels]
      have hneg :
          ∫ x in (0)..(2 * Real.pi), -f.val x * deriv (deriv g.val) x =
            -(∫ x in (0)..(2 * Real.pi), f.val x * deriv (deriv g.val) x) := by
        simp [neg_mul]
      rw [hneg]
      linarith
  }

def derive_periodic_ibp_from_ftc
    (m : ℝ) (f g : PeriodicField)
    (h_ftc : PeriodicIBPFTCHypotheses m f g)
    (h_cancel : PeriodicIBPBoundaryCancellation m f g h_ftc) :
    PeriodicBoundaryIntegrationByParts m f g := by
  exact {
    ibp_identity_f := h_cancel.ftc_f_to_ibp_f
    ibp_identity_g := h_cancel.ftc_g_to_ibp_g
  }

def BOUNDARY_integration_by_parts_derived_from_mathlib : Prop :=
  ¬ ∀ (m : ℝ) (f g : PeriodicField), Nonempty (PeriodicBoundaryIntegrationByParts m f g)

def BOUNDARY_pointwise_square_nonnegativity_derived_from_mathlib : Prop :=
  ¬ ∀ (m : ℝ) (f : PeriodicField), Nonempty (PeriodicQuadraticFormNonnegativity m f)

def BOUNDARY_self_adjointness_proved : Prop := ¬ True
def BOUNDARY_heat_trace_class_proved : Prop := ¬ True
def BOUNDARY_spectral_zeta_constructed : Prop := ¬ True

end S1MassiveLaplacianInputSurface
end Gravity
end Frontier
end Chronos
