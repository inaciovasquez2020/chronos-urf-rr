import JointRapidityMeasure
import PhysicalRapidityKernel

open MeasureTheory Set
open scoped ENNReal InnerProductSpace

namespace Chronos.FourEvent

noncomputable section

abbrev RadialPlane := ℝ × ℝ

def radialProperSq
    (p : RadialPlane) : ℝ :=
  (1-p.1)^2-p.2^2

def radialSeparation
    (p q : RadialPlane)
    (c : ℝ) : ℝ :=
  (q.1-p.1)^2-p.2^2-q.2^2+
    2*p.2*q.2*c

def logRadius (P : ℝ) : ℝ :=
  -Real.log (Real.sqrt P)

def invariantCos (P R S : ℝ) : ℝ :=
  (P+R-S) /
    (2*Real.sqrt P*Real.sqrt R)

def relativeEta (P R S : ℝ) : ℝ :=
  let k := invariantCos P R S
  Real.log (k+Real.sqrt (k^2-1))

def rapidityMassFormula
    (lam mu eta : ℝ) : ℝ≥0∞ :=
  ENNReal.ofReal
    (Real.exp (-2*lam-2*mu-2*eta) *
      (1+2*(Real.cosh eta-
        Real.cosh (lam-mu))/Real.sinh eta))

def massFromInvariants
    (P R S : ℝ) : ℝ≥0∞ :=
  rapidityMassFormula
    (logRadius P)
    (logRadius R)
    (relativeEta P R S)

private theorem exp_logRadius
    (P : ℝ) (hP : 0 < P) :
    Real.exp (-logRadius P) =
      Real.sqrt P := by
  unfold logRadius
  rw [neg_neg,
    Real.exp_log (Real.sqrt_pos.2 hP)]

private theorem invariantCos_gt_one
    (P R S : ℝ)
    (hP : 0 < P)
    (hR : 0 < R)
    (hS : S < 0) :
    1 < invariantCos P R S := by

  have hp : 0 < Real.sqrt P :=
    Real.sqrt_pos.2 hP

  have hr : 0 < Real.sqrt R :=
    Real.sqrt_pos.2 hR

  have hd :
      0 < 2*Real.sqrt P*Real.sqrt R :=
    mul_pos (mul_pos (by norm_num) hp) hr

  unfold invariantCos

  apply (lt_div_iff₀ hd).2

  nlinarith [
    Real.sq_sqrt hP.le,
    Real.sq_sqrt hR.le,
    sq_nonneg (Real.sqrt P-Real.sqrt R)]

private theorem log_cosh_inverse
    (k : ℝ) (hk : 1 < k) :
    0 < Real.log
      (k+Real.sqrt (k^2-1)) ∧
    Real.cosh
      (Real.log (k+Real.sqrt (k^2-1))) = k := by

  let w := Real.sqrt (k^2-1)

  have hn : 0 ≤ k^2-1 := by
    nlinarith [sq_nonneg (k-1)]

  have hw0 : 0 ≤ w :=
    Real.sqrt_nonneg _

  have hw : w^2 = k^2-1 :=
    Real.sq_sqrt hn

  have hplus : 1 < k+w := by
    linarith

  have hp : 0 < k+w := by
    linarith

  have hi : (k+w)⁻¹ = k-w := by
    field_simp [hp.ne'] <;> nlinarith

  have hexp :
      Real.exp (Real.log (k+w)) = k+w :=
    Real.exp_log hp

  change
    0 < Real.log (k+w) ∧
      Real.cosh (Real.log (k+w)) = k

  constructor

  · exact Real.log_pos hplus

  · rw [Real.cosh_eq,Real.exp_neg,
      hexp,hi]
    ring

theorem invariant_relative_rapidity
    (P R S : ℝ)
    (hP : 0 < P)
    (hR : 0 < R)
    (hS : S < 0) :
    0 < relativeEta P R S ∧
    Real.cosh (relativeEta P R S) =
      invariantCos P R S :=
  log_cosh_inverse
    (invariantCos P R S)
    (invariantCos_gt_one P R S hP hR hS)

theorem invariant_separation_recovery
    (P R S : ℝ)
    (hP : 0 < P)
    (hR : 0 < R)
    (hS : S < 0) :
    S =
      (Real.exp (-logRadius P))^2 +
      (Real.exp (-logRadius R))^2 -
      2*(Real.exp (-logRadius P) *
        Real.exp (-logRadius R)) *
        Real.cosh (relativeEta P R S) := by

  have hp : 0 < Real.sqrt P :=
    Real.sqrt_pos.2 hP

  have hr : 0 < Real.sqrt R :=
    Real.sqrt_pos.2 hR

  rw [exp_logRadius P hP,
    exp_logRadius R hR,
    Real.sq_sqrt hP.le,
    Real.sq_sqrt hR.le,
    (invariant_relative_rapidity
      P R S hP hR hS).2]

  unfold invariantCos

  field_simp [hp.ne',hr.ne'] <;> ring

theorem tipInvariant_radial
    (x : Event) :
    invariantSq ((1,0)-x) =
      radialProperSq (x.1,‖x.2‖) := by

  change
    (1-x.1)^2-‖(0:Space)-x.2‖^2 =
      (1-x.1)^2-‖x.2‖^2

  rw [zero_sub,norm_neg]

private theorem radialProperSq_pos
    (x : Event) (hx : x ∈ diamond) :
    0 < radialProperSq
      (x.1,‖x.2‖) := by

  have ht : ‖x.2‖ < 1-x.1 :=
    hx.2

  have ha :
      0 < 1-x.1-‖x.2‖ :=
    sub_pos.mpr ht

  have hb :
      0 < 1-x.1+‖x.2‖ := by
    linarith [norm_nonneg x.2]

  have hh := mul_pos ha hb

  unfold radialProperSq

  dsimp only

  nlinarith

theorem radialSeparation_eq
    (x y : Event)
    (hx : x.2 ≠ 0)
    (hy : y.2 ≠ 0) :
    radialSeparation
      (x.1,‖x.2‖)
      (y.1,‖y.2‖)
      (⟪spatialDirection x,y.2⟫_ℝ /
        ‖y.2‖) =
      invariantSq (y-x) := by

  have hx0 : 0 < ‖x.2‖ :=
    norm_pos_iff.mpr hx

  have hy0 : 0 < ‖y.2‖ :=
    norm_pos_iff.mpr hy

  have hc :
      ‖x.2‖*‖y.2‖*
        (⟪spatialDirection x,y.2⟫_ℝ /
          ‖y.2‖) =
      ⟪x.2,y.2⟫_ℝ := by

    unfold spatialDirection

    rw [real_inner_smul_left]

    field_simp [hx0.ne',hy0.ne'] <;> ring

  change
    (y.1-x.1)^2-
      ‖x.2‖^2-‖y.2‖^2+
      2*‖x.2‖*‖y.2‖*
        (⟪spatialDirection x,y.2⟫_ℝ /
          ‖y.2‖) =
    (y.1-x.1)^2-‖y.2-x.2‖^2

  rw [norm_sub_sq_real,
    real_inner_comm x.2 y.2]

  calc
    _ = (y.1-x.1)^2-
        ‖x.2‖^2-‖y.2‖^2+
        2*(‖x.2‖*‖y.2‖*
          (⟪spatialDirection x,y.2⟫_ℝ /
            ‖y.2‖)) := by ring

    _ = _ := by rw [hc]; ring

theorem physical_massFromInvariants
    (x y : Event)
    (hx : x ∈ diamond)
    (hy : y ∈ diamond)
    (hs : invariantSq (y-x) < 0) :
    futureMass x y =
      massFromInvariants
        (radialProperSq (x.1,‖x.2‖))
        (radialProperSq (y.1,‖y.2‖))
        (invariantSq (y-x)) := by

  let P := radialProperSq (x.1,‖x.2‖)
  let R := radialProperSq (y.1,‖y.2‖)
  let S := invariantSq (y-x)

  have hp : 0 < P :=
    radialProperSq_pos x hx

  have hr : 0 < R :=
    radialProperSq_pos y hy

  have heta :
      0 < relativeEta P R S :=
    (invariant_relative_rapidity
      P R S hp hr hs).1

  have hP :
      invariantSq ((1,0)-x) =
        (Real.exp (-logRadius P))^2 := by

    rw [tipInvariant_radial,
      exp_logRadius P hp,
      Real.sq_sqrt hp.le]


  have hR :
      invariantSq ((1,0)-y) =
        (Real.exp (-logRadius R))^2 := by

    rw [tipInvariant_radial,
      exp_logRadius R hr,
      Real.sq_sqrt hr.le]


  have hsep :=
    invariant_separation_recovery
      P R S hp hr hs

  exact physical_spacelike_rapidity_mass
    x y hx hy hs
    (logRadius P) (logRadius R)
    (relativeEta P R S)
    heta hP hR hsep

def spacelikeRadialKernel
    (a : JointInput) : ℝ≥0∞ :=
  let P := radialProperSq a.1
  let R := radialProperSq a.2.1
  let S := radialSeparation
    a.1 a.2.1 a.2.2
  if S < 0 then
    (massFromInvariants P R S)^2
  else 0

theorem spacelikeRadialKernel_measurable :
    Measurable spacelikeRadialKernel := by

  have hS :
      Continuous
        (fun a : JointInput =>
          radialSeparation
            a.1 a.2.1 a.2.2) := by
    unfold radialSeparation
    fun_prop

  have hset :
      MeasurableSet
        {a : JointInput |
          radialSeparation
            a.1 a.2.1 a.2.2 < 0} :=
    (isOpen_lt hS continuous_const).measurableSet

  unfold spacelikeRadialKernel

  dsimp only

  apply Measurable.ite hset _ measurable_const

  unfold massFromInvariants rapidityMassFormula
    logRadius relativeEta invariantCos
    radialProperSq radialSeparation

  fun_prop

theorem uniform_diamond_ae :
    ∀ᵐ x : Event ∂uniform,
      x ∈ diamond := by

  have hd : MeasurableSet diamond := by

    change MeasurableSet
      {x : Event |
        ‖x.2‖ < x.1 ∧
        ‖x.2‖ < 1-x.1}

    exact
      (isOpen_lt
        (f := fun x : Event => ‖x.2‖)
        (g := fun x : Event => x.1)
        (by fun_prop)
        (by fun_prop)).measurableSet.inter
      (isOpen_lt
        (f := fun x : Event => ‖x.2‖)
        (g := fun x : Event => 1-x.1)
        (by fun_prop)
        (by fun_prop)).measurableSet

  have hz : uniform diamondᶜ = 0 := by

    unfold uniform

    rw [Measure.smul_apply,
      Measure.restrict_apply hd.compl]

    simp

  have h :=
    measure_eq_zero_iff_ae_notMem.mp hz

  filter_upwards [h] with x hx

  simpa using hx

def spacelikeMoment : ℝ≥0∞ :=
  ∫⁻ x : Event,
    ∫⁻ y : Event,
      (if invariantSq (y-x) < 0 then
        (futureMass x y)^2
      else 0)
    ∂uniform ∂uniform

theorem spacelikeMoment_joint_reduction :
    spacelikeMoment =
      ENNReal.ofReal (16 : ℝ) *
        ∫⁻ p in rapidityRegion,
          rapidityWeight p *
            secondRapidityAverage
              spacelikeRadialKernel
              (rapidityRadial p) := by

  unfold spacelikeMoment

  calc
    _ =
      ∫⁻ x : Event,
        ∫⁻ y : Event,
          spacelikeRadialKernel
            ((x.1,‖x.2‖),
              ((y.1,‖y.2‖),
                ⟪spatialDirection x,y.2⟫_ℝ /
                  ‖y.2‖))
          ∂uniform ∂uniform := by

      apply lintegral_congr_ae

      filter_upwards
        [uniform_diamond_ae,spatial_nonzero_ae]
        with x hx hx0

      apply lintegral_congr_ae

      filter_upwards
        [uniform_diamond_ae,spatial_nonzero_ae]
        with y hy hy0

      have hsep :=
        radialSeparation_eq x y hx0 hy0

      unfold spacelikeRadialKernel

      dsimp only

      rw [hsep]

      by_cases hs : invariantSq (y-x) < 0

      · simp only [if_pos hs]

        rw [physical_massFromInvariants
          x y hx hy hs]

      · simp only [if_neg hs]

    _ = _ :=
      joint_physical_rapidity_integral
        spacelikeRadialKernel
        spacelikeRadialKernel_measurable

#print axioms invariant_relative_rapidity
#print axioms invariant_separation_recovery
#print axioms tipInvariant_radial
#print axioms radialSeparation_eq
#print axioms physical_massFromInvariants
#print axioms spacelikeRadialKernel_measurable
#print axioms uniform_diamond_ae
#print axioms spacelikeMoment_joint_reduction

end

end Chronos.FourEvent
