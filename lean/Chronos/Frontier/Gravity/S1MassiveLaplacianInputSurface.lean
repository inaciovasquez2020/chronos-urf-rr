import Mathlib

noncomputable section

namespace Chronos
namespace Frontier
namespace Gravity
namespace S1MassiveLaplacianInputSurface

structure PeriodicField where
  val : ℝ → ℝ
  periodic : val 0 = val 0
  periodic_value : val (2 * Real.pi) = val 0
  periodic_deriv : deriv val (2 * Real.pi) = deriv val 0

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
