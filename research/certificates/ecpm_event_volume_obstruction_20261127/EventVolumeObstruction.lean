import Mathlib.MeasureTheory.Measure.Lebesgue.EqHaar
import Mathlib.MeasureTheory.Measure.Haar.Unique
import Mathlib.MeasureTheory.Measure.Prod
import Mathlib.MeasureTheory.Measure.WithDensity
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Tactic.Module
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.NormNum
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic
import Mathlib.Tactic.Ring
import Mathlib.MeasureTheory.Constructions.BorelSpace.Order
import Mathlib.Tactic

namespace Chronos.ECPM.EventVolume

structure Vec where
  t : ℝ
  x : ℝ
  y : ℝ
  z : ℝ

def sq (v : Vec) : ℝ :=
  v.t ^ 2 - v.x ^ 2 - v.y ^ 2 - v.z ^ 2

def dot (u v : Vec) : ℝ :=
  u.t * v.t - u.x * v.x - u.y * v.y - u.z * v.z

def sub (u v : Vec) : Vec :=
  ⟨u.t-v.t, u.x-v.x, u.y-v.y, u.z-v.z⟩

def combo2 (a : ℝ) (u : Vec) (b : ℝ) (v : Vec) : Vec :=
  ⟨a*u.t+b*v.t,
   a*u.x+b*v.x,
   a*u.y+b*v.y,
   a*u.z+b*v.z⟩

def combo3 (a b c : ℝ) (u v w : Vec) : Vec :=
  ⟨a*u.t+b*v.t+c*w.t,
   a*u.x+b*v.x+c*w.x,
   a*u.y+b*v.y+c*w.y,
   a*u.z+b*v.z+c*w.z⟩

theorem dot_self (u : Vec) :
    dot u u = sq u := by
  unfold dot sq
  ring

theorem polar (u v : Vec) :
    dot u v =
      (sq u + sq v - sq (sub v u))/2 := by
  unfold dot sq sub
  ring

theorem dot_combo3
    (a b c : ℝ) (u v w r : Vec) :
    dot r (combo3 a b c u v w) =
      a * dot r u + b * dot r v + c * dot r w := by
  unfold dot combo3
  ring

theorem sq_combo3
    (a b c : ℝ) (u v w : Vec) :
    sq (combo3 a b c u v w) =
      a^2 * sq u + b^2 * sq v + c^2 * sq w
      + 2*a*b*dot u v
      + 2*a*c*dot u w
      + 2*b*c*dot v w := by
  unfold sq dot combo3
  ring

theorem time_zero_nonpositive
    (u : Vec) (h : u.t = 0) :
    sq u ≤ 0 := by
  unfold sq
  rw [h]
  nlinarith only [
    sq_nonneg u.x,
    sq_nonneg u.y,
    sq_nonneg u.z]

theorem no_two_orthogonal_positive
    (u v : Vec)
    (hu : 0 < sq u)
    (hv : 0 < sq v)
    (ho : dot u v = 0) : False := by
  have ht : u.t ≠ 0 := by
    intro h
    exact (not_lt_of_ge
      (time_zero_nonpositive u h)) hu

  have ht2 : 0 < u.t ^ 2 := by
    rcases lt_or_gt_of_ne ht with h | h
    · simpa only [pow_two] using
        mul_pos_of_neg_of_neg h h
    · simpa only [pow_two] using mul_pos h h

  let w := combo2 v.t u (-u.t) v

  have hz : w.t = 0 := by
    unfold w combo2
    ring

  have hn : sq w ≤ 0 :=
    time_zero_nonpositive w hz

  have he :
      sq w =
        v.t^2 * sq u + u.t^2 * sq v
        - 2*u.t*v.t*dot u v := by
    unfold w combo2 sq dot
    ring

  rw [ho] at he
  simp only [mul_zero, sub_zero] at he

  have hp :
      0 < v.t^2 * sq u + u.t^2 * sq v :=
    add_pos_of_nonneg_of_pos
      (mul_nonneg (sq_nonneg v.t) hu.le)
      (mul_pos ht2 hv)

  linarith only [hn, he, hp]

-- Four intrinsically ordered events in the product order.

noncomputable def p0 : Vec :=
  ⟨-1/3, -1/3, -1/3, -1/3⟩

noncomputable def p1 : Vec :=
  ⟨-1/8, -1/8, -1/8, -1/8⟩

noncomputable def p2 : Vec :=
  ⟨-1/15, -1/15, -1/15, -1/15⟩

def p3 : Vec :=
  ⟨0, 0, 0, 1⟩

def strictBefore (u v : Vec) : Prop :=
  u.t < v.t ∧ u.x < v.x ∧
  u.y < v.y ∧ u.z < v.z

def intervalVolume (u v : Vec) : ℝ :=
  (v.t-u.t) * (v.x-u.x) *
  (v.y-u.y) * (v.z-u.z)

theorem witness_ordered :
    strictBefore p0 p1 ∧
    strictBefore p1 p2 ∧
    strictBefore p2 p3 := by
  norm_num [strictBefore, p0, p1, p2, p3]

private theorem sqrt_from_square
    (v s : ℝ) (hs : 0 ≤ s)
    (h : v = s^2) : Real.sqrt v = s := by
  rw [h, Real.sqrt_sq hs]

theorem witness_squared_intervals :
    Real.sqrt (intervalVolume p0 p1) = 25/576 ∧
    Real.sqrt (intervalVolume p0 p2) = 16/225 ∧
    Real.sqrt (intervalVolume p0 p3) = 2/9 ∧
    Real.sqrt (intervalVolume p1 p2) = 49/14400 ∧
    Real.sqrt (intervalVolume p1 p3) = 3/64 ∧
    Real.sqrt (intervalVolume p2 p3) = 4/225 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  all_goals
    apply sqrt_from_square
    · norm_num
    · norm_num [intervalVolume, p0, p1, p2, p3]

-- No three displacement vectors in signature (+---)
-- realize all six required squared intervals.

theorem no_minkowski_realization
    (a b c : Vec)
    (h01 : sq a = 25/576)
    (h02 : sq b = 16/225)
    (h03 : sq c = 2/9)
    (h12 : sq (sub b a) = 49/14400)
    (h13 : sq (sub c a) = 3/64)
    (h23 : sq (sub c b) = 4/225) : False := by

  have hab : dot a b = 1/18 := by
    rw [polar, h01, h02, h12]
    norm_num

  have hac : dot a c = 7/64 := by
    rw [polar, h01, h03, h13]
    norm_num

  have hbc : dot b c = 31/225 := by
    rw [polar, h02, h03, h23]
    norm_num

  let w := combo3 (3137/25) (-100) 1 a b c

  have ho : dot a w = 0 := by
    dsimp only [w]
    rw [dot_combo3, dot_self, h01, hab, hac]
    norm_num

  have hw : sq w = 1877/4800 := by
    dsimp only [w]
    rw [sq_combo3, h01, h02, h03, hab, hac, hbc]
    norm_num

  have ha : 0 < sq a := by
    rw [h01]
    norm_num

  have hp : 0 < sq w := by
    rw [hw]
    norm_num

  exact no_two_orthogonal_positive a w ha hp ho

-- End-to-end event-volume obstruction.

theorem product_volume_not_minkowski
    (a b c : Vec)
    (h01 : sq a = Real.sqrt (intervalVolume p0 p1))
    (h02 : sq b = Real.sqrt (intervalVolume p0 p2))
    (h03 : sq c = Real.sqrt (intervalVolume p0 p3))
    (h12 : sq (sub b a) =
      Real.sqrt (intervalVolume p1 p2))
    (h13 : sq (sub c a) =
      Real.sqrt (intervalVolume p1 p3))
    (h23 : sq (sub c b) =
      Real.sqrt (intervalVolume p2 p3)) : False := by
  rcases witness_squared_intervals with
    ⟨e01, e02, e03, e12, e13, e23⟩
  exact no_minkowski_realization a b c
    (h01.trans e01)
    (h02.trans e02)
    (h03.trans e03)
    (h12.trans e12)
    (h13.trans e13)
    (h23.trans e23)

#print axioms dot_self
#print axioms polar
#print axioms dot_combo3
#print axioms sq_combo3
#print axioms time_zero_nonpositive
#print axioms no_two_orthogonal_positive
#print axioms witness_ordered
#print axioms witness_squared_intervals
#print axioms no_minkowski_realization
#print axioms product_volume_not_minkowski


-- Every strictly ordered product interval has positive volume.

theorem volume_pos (u v : Vec)
    (h : strictBefore u v) :
    0 < intervalVolume u v := by
  rcases h with ⟨ht, hx, hy, hz⟩
  unfold intervalVolume
  exact mul_pos
    (mul_pos
      (mul_pos (sub_pos.mpr ht) (sub_pos.mpr hx))
      (sub_pos.mpr hy))
    (sub_pos.mpr hz)

theorem coordinate_split_bound
    (x z y : ℝ)
    (h1 : x < z) (h2 : z < y) :
    0 ≤ 4*(z-x)*(y-z) ∧
    4*(z-x)*(y-z) ≤ (y-x)^2 := by
  constructor
  · exact mul_nonneg
      (mul_nonneg (by norm_num) (sub_nonneg.mpr h1.le))
      (sub_nonneg.mpr h2.le)
  · nlinarith only [sq_nonneg ((z-x)-(y-z))]

-- Upper bound valid for every interior event,
-- not merely the finite witness.

theorem product_midpoint_upper
    (u w v : Vec)
    (huw : strictBefore u w)
    (hwv : strictBefore w v) :
    min (intervalVolume u w) (intervalVolume w v)
      ≤ intervalVolume u v / 16 := by

  rcases huw with ⟨ht1, hx1, hy1, hz1⟩
  rcases hwv with ⟨ht2, hx2, hy2, hz2⟩

  rcases coordinate_split_bound
    u.t w.t v.t ht1 ht2 with ⟨htn, ht⟩

  rcases coordinate_split_bound
    u.x w.x v.x hx1 hx2 with ⟨hxn, hx⟩

  rcases coordinate_split_bound
    u.y w.y v.y hy1 hy2 with ⟨hyn, hy⟩

  rcases coordinate_split_bound
    u.z w.z v.z hz1 hz2 with ⟨hzn, hz⟩

  have htx :=
    mul_le_mul ht hx hxn (sq_nonneg (v.t-u.t))

  have hyz :=
    mul_le_mul hy hz hzn (sq_nonneg (v.y-u.y))

  have hall :=
    mul_le_mul htx hyz
      (mul_nonneg hyn hzn)
      (mul_nonneg
        (sq_nonneg (v.t-u.t))
        (sq_nonneg (v.x-u.x)))

  have hb :
      256 * intervalVolume u w * intervalVolume w v
        ≤ (intervalVolume u v)^2 := by
    calc
      _ =
        ((4*(w.t-u.t)*(v.t-w.t)) *
         (4*(w.x-u.x)*(v.x-w.x))) *
        ((4*(w.y-u.y)*(v.y-w.y)) *
         (4*(w.z-u.z)*(v.z-w.z))) := by
           unfold intervalVolume
           ring
      _ ≤
        ((v.t-u.t)^2 * (v.x-u.x)^2) *
        ((v.y-u.y)^2 * (v.z-u.z)^2) := hall
      _ = _ := by
        unfold intervalVolume
        ring

  have huv : strictBefore u v :=
    ⟨lt_trans ht1 ht2,
     lt_trans hx1 hx2,
     lt_trans hy1 hy2,
     lt_trans hz1 hz2⟩

  let T := intervalVolume u v
  let L := intervalVolume u w
  let R := intervalVolume w v

  have hT : 0 < T := volume_pos u v huv
  have hT16 : 0 < T/16 := by linarith only [hT]

  change 256 * L * R ≤ T^2 at hb
  change min L R ≤ T/16

  by_contra h

  have hm : T/16 < min L R :=
    lt_of_not_ge h

  have hL : T/16 < L :=
    lt_of_lt_of_le hm (min_le_left L R)

  have hR : T/16 < R :=
    lt_of_lt_of_le hm (min_le_right L R)

  have hLp : 0 < L := lt_trans hT16 hL

  have hp : (T/16)*(T/16) < L*R := by
    calc
      _ < L*(T/16) :=
        mul_lt_mul_of_pos_right hL hT16
      _ < L*R :=
        mul_lt_mul_of_pos_left hR hLp

  nlinarith only [hb, hp]

noncomputable def eventMidpoint (u v : Vec) : Vec :=
  ⟨(u.t+v.t)/2,
   (u.x+v.x)/2,
   (u.y+v.y)/2,
   (u.z+v.z)/2⟩

theorem eventMidpoint_ordered
    (u v : Vec) (h : strictBefore u v) :
    strictBefore u (eventMidpoint u v) ∧
    strictBefore (eventMidpoint u v) v := by
  rcases h with ⟨ht, hx, hy, hz⟩
  unfold strictBefore
  refine ⟨⟨?_, ?_, ?_, ?_⟩, ⟨?_, ?_, ?_, ?_⟩⟩
  all_goals
    dsimp [eventMidpoint]
    linarith

theorem eventMidpoint_volumes (u v : Vec) :
    intervalVolume u (eventMidpoint u v)
        = intervalVolume u v / 16 ∧
    intervalVolume (eventMidpoint u v) v
        = intervalVolume u v / 16 := by
  constructor <;>
    unfold intervalVolume eventMidpoint <;>
    ring

-- Exact attainment of the global upper bound.

theorem product_midpoint_scaling
    (u v : Vec) (h : strictBefore u v) :
    (∀ w : Vec,
      strictBefore u w →
      strictBefore w v →
      min (intervalVolume u w) (intervalVolume w v)
        ≤ intervalVolume u v / 16) ∧
    (∃ w : Vec,
      strictBefore u w ∧
      strictBefore w v ∧
      min (intervalVolume u w) (intervalVolume w v)
        = intervalVolume u v / 16) := by
  constructor
  · intro w h1 h2
    exact product_midpoint_upper u w v h1 h2
  · rcases eventMidpoint_ordered u v h with ⟨h1,h2⟩
    rcases eventMidpoint_volumes u v with ⟨e1,e2⟩
    refine ⟨eventMidpoint u v, h1, h2, ?_⟩
    rw [e1, e2, min_self]

#print axioms volume_pos
#print axioms coordinate_split_bound
#print axioms product_midpoint_upper
#print axioms eventMidpoint_ordered
#print axioms eventMidpoint_volumes
#print axioms product_midpoint_scaling


end Chronos.ECPM.EventVolume
