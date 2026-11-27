import SpacelikeFrame
import PhysicalMomentsBase
import Mathlib.MeasureTheory.Measure.Lebesgue.VolumeOfBalls

open MeasureTheory Set
open scoped ENNReal

namespace Chronos.FourEvent

noncomputable section

theorem unit_diamond_volume :
    (volume : Measure Event) diamond =
      ENNReal.ofReal (Real.pi/24) := by
  have hD :
      diamond =
        Chronos.MinkowskiDiamond.diamond
          (0 : Event)
          Chronos.MinkowskiDiamond.tip := by
    ext p
    change
      (‖p.2‖ < p.1 ∧ ‖p.2‖ < 1-p.1) ↔
      (‖p.2-0‖ < p.1-0 ∧
        ‖0-p.2‖ < 1-p.1)
    simp [norm_neg]

  have hd :
      Module.finrank ℝ Space = 3 := by
    simp [Space]

  have hm :=
    Chronos.NormalizedMoments.physical_diamond_mass
      (volume : Measure Space) hd

  rw [hD,Measure.volume_eq_prod,hm,
    EuclideanSpace.volume_closedBall_fin_three]

  simp only [ENNReal.ofReal_one,one_pow,one_mul]

  rw [← ENNReal.ofReal_mul
    (show 0 ≤ Real.pi*4/3 by positivity)]

  congr 1
  ring

private def upperNull : Set Event :=
  {p | ‖p.2‖ = 1-p.1}

private theorem upperNull_measurable :
    MeasurableSet upperNull := by
  unfold upperNull
  exact
    (isClosed_eq
      (f := fun p : Event => ‖p.2‖)
      (g := fun p : Event => 1-p.1)
      (by fun_prop)
      (by fun_prop)).measurableSet

theorem upperNull_volume_zero :
    (volume : Measure Event) upperNull = 0 := by
  rw [Measure.volume_eq_prod,
    Measure.prod_apply_symm upperNull_measurable]

  have h (v : Space) :
      (fun t : ℝ => (t,v)) ⁻¹' upperNull =
        {1-‖v‖} := by
    ext t
    change ‖v‖ = 1-t ↔ t = 1-‖v‖
    constructor <;> intro he <;> linarith

  simp_rw [h,measure_singleton,lintegral_zero]

private def bothFuture (x y : Event) : Set Event :=
  {p | Precedes x p ∧ Precedes y p}

private theorem bothFuture_measurable
    (x y : Event) :
    MeasurableSet (bothFuture x y) := by
  change MeasurableSet
    ({p : Event | ‖p.2-x.2‖ ≤ p.1-x.1} ∩
      {p : Event | ‖p.2-y.2‖ ≤ p.1-y.1})

  exact
    (isClosed_le
      (f := fun p : Event => ‖p.2-x.2‖)
      (g := fun p : Event => p.1-x.1)
      (by fun_prop)
      (by fun_prop)).measurableSet.inter
    (isClosed_le
      (f := fun p : Event => ‖p.2-y.2‖)
      (g := fun p : Event => p.1-y.1)
      (by fun_prop)
      (by fun_prop)).measurableSet

private theorem physical_lens_ae
    (x y : Event) (hx : x ∈ diamond) :
    (@Inter.inter (Set Event) inferInstance
      (bothFuture x y) diamond) =ᵐ[volume]
      threeLens x y (1,0) := by

  have hnull :
      ∀ᵐ p : Event ∂volume, p ∉ upperNull :=
    measure_eq_zero_iff_ae_notMem.mp
      upperNull_volume_zero

  filter_upwards [hnull] with p hp

  apply propext
  change
    (Precedes x p ∧ Precedes y p) ∧
      (‖p.2‖ < p.1 ∧ ‖p.2‖ < 1-p.1) ↔
    Precedes x p ∧ Precedes y p ∧
      Precedes p (1,0)

  constructor
  · rintro ⟨⟨hxp,hyp⟩,hl,hu⟩
    refine ⟨hxp,hyp,?_⟩
    change ‖(0 : Space)-p.2‖ ≤ 1-p.1
    simpa [norm_neg] using hu.le

  · rintro ⟨hxp,hyp,htop⟩

    have hl : ‖p.2‖ < p.1 := by
      have hx' : ‖x.2‖ < x.1 := hx.1
      change ‖p.2-x.2‖ ≤ p.1-x.1 at hxp

      have he :
          p.2 = (p.2-x.2)+x.2 := by abel

      calc
        ‖p.2‖ =
            ‖(p.2-x.2)+x.2‖ := by rw [← he]
        _ ≤ ‖p.2-x.2‖+‖x.2‖ :=
          norm_add_le _ _
        _ < p.1 := by linarith

    have hu : ‖p.2‖ ≤ 1-p.1 := by
      change ‖(0 : Space)-p.2‖ ≤ 1-p.1 at htop
      simpa [norm_neg] using htop

    have hn : ‖p.2‖ ≠ 1-p.1 := hp

    exact ⟨⟨hxp,hyp⟩,hl,lt_of_le_of_ne hu hn⟩

theorem physical_futureMass_lens
    (x y : Event) (hx : x ∈ diamond) :
    futureMass x y =
      (ENNReal.ofReal (Real.pi/24))⁻¹ *
        volume (threeLens x y (1,0)) := by

  change uniform (bothFuture x y) = _

  unfold uniform

  rw [Measure.smul_apply,smul_eq_mul,
    Measure.restrict_apply
      (bothFuture_measurable x y),
    unit_diamond_volume,
    measure_congr (physical_lens_ae x y hx)]

theorem physical_spacelike_futureMass
    (x y : Event)
    (hx : x ∈ diamond)
    (hy : y ∈ diamond)
    (hs : invariantSq (y-x) < 0) :
    ∃ a b T : ℝ,
      0 < a ∧ 0 ≤ b ∧ a+b < T ∧
      invariantSq (y-x) = -4*a^2 ∧
      invariantSq ((1,0)-x) +
        invariantSq ((1,0)-y) =
          2*(T^2-a^2-b^2) ∧
      (invariantSq ((1,0)-x) -
        invariantSq ((1,0)-y))^2 =
          16*a^2*b^2 ∧
      futureMass x y =
        ENNReal.ofReal
          ((T+2*a)*((T-a)^2-b^2)^2/T) := by

  have hxt : StrictBefore x (1,0) := by
    change ‖(0 : Space)-x.2‖ < 1-x.1
    simpa [norm_neg] using hx.2

  have hyt : StrictBefore y (1,0) := by
    change ‖(0 : Space)-y.2‖ < 1-y.1
    simpa [norm_neg] using hy.2

  obtain ⟨a,b,T,ha,hb,hT,h1,h2,h3,hv⟩ :=
    spacelike_lens_volume_exact_invariants
      x y (1,0) hxt hyt hs

  refine ⟨a,b,T,ha,hb,hT,h1,h2,h3,?_⟩

  rw [physical_futureMass_lens x y hx,hv]

  have hp : 0 < Real.pi/24 := by positivity
  have ht : 0 < T := by linarith

  rw [← ENNReal.ofReal_inv_of_pos hp,
    ← ENNReal.ofReal_mul (inv_nonneg.mpr hp.le)]

  congr 1

  field_simp [Real.pi_ne_zero,ne_of_gt ht] <;> ring

#print axioms unit_diamond_volume
#print axioms upperNull_volume_zero
#print axioms physical_futureMass_lens
#print axioms physical_spacelike_futureMass

end

end Chronos.FourEvent
