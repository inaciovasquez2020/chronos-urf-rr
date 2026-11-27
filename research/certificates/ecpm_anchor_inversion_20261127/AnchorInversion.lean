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


namespace Chronos.ECPM.EventVolume

structure Basis4 where
  e0 : Vec
  e1 : Vec
  e2 : Vec
  e3 : Vec

structure Gram4 where
  g00 : ℝ
  g11 : ℝ
  g22 : ℝ
  g33 : ℝ
  g01 : ℝ
  g02 : ℝ
  g03 : ℝ
  g12 : ℝ
  g13 : ℝ
  g23 : ℝ

def linear4 (D : Basis4) (b : Vec) : Vec :=
  ⟨b.t*D.e0.t+b.x*D.e1.t+b.y*D.e2.t+b.z*D.e3.t,
   b.t*D.e0.x+b.x*D.e1.x+b.y*D.e2.x+b.z*D.e3.x,
   b.t*D.e0.y+b.x*D.e1.y+b.y*D.e2.y+b.z*D.e3.y,
   b.t*D.e0.z+b.x*D.e1.z+b.y*D.e2.z+b.z*D.e3.z⟩

def dualGram (D : Basis4) : Gram4 :=
  ⟨sq D.e0, sq D.e1, sq D.e2, sq D.e3,
   dot D.e0 D.e1,
   dot D.e0 D.e2,
   dot D.e0 D.e3,
   dot D.e1 D.e2,
   dot D.e1 D.e3,
   dot D.e2 D.e3⟩

def quadratic (H : Gram4) (b : Vec) : ℝ :=
    H.g00*b.t^2
  + H.g11*b.x^2
  + H.g22*b.y^2
  + H.g33*b.z^2
  + 2*H.g01*b.t*b.x
  + 2*H.g02*b.t*b.y
  + 2*H.g03*b.t*b.z
  + 2*H.g12*b.x*b.y
  + 2*H.g13*b.x*b.z
  + 2*H.g23*b.y*b.z

def readBack (A : Basis4) (v : Vec) : Vec :=
  ⟨dot A.e0 v,
   dot A.e1 v,
   dot A.e2 v,
   dot A.e3 v⟩

def chronological (u v : Vec) : Prop :=
  u.t < v.t ∧ 0 < sq (sub v u)

noncomputable def anchorFeatures
    {E : Type*}
    (S : E → E → ℝ)
    (a0 a1 a2 a3 a4 x : E) : Vec :=
  ⟨(S x a0+S a0 a1-S x a1)/2,
   (S x a0+S a0 a2-S x a2)/2,
   (S x a0+S a0 a3-S x a3)/2,
   (S x a0+S a0 a4-S x a4)/2⟩

def observedQ
    {E : Type*}
    (H : Gram4) (b : E → Vec)
    (x y : E) : ℝ :=
  quadratic H (sub (b y) (b x))

theorem linear4_sq
    (D : Basis4) (b c : Vec) :
    sq (sub (linear4 D c) (linear4 D b)) =
      quadratic (dualGram D) (sub c b) := by
  simp only [sq, sub, linear4, quadratic, dualGram, dot]
  ring

theorem linear4_time
    (D : Basis4) (b : Vec) (k : ℝ)
    (h0 : D.e0.t = k)
    (h1 : D.e1.t = 0)
    (h2 : D.e2.t = 0)
    (h3 : D.e3.t = 0) :
    (linear4 D b).t = k*b.t := by
  change
    b.t*D.e0.t + b.x*D.e1.t +
      b.y*D.e2.t + b.z*D.e3.t = k*b.t
  rw [h0,h1,h2,h3]
  ring

theorem linear4_injective
    (A D : Basis4)
    (hleft : ∀ r : Vec,
      readBack A (linear4 D r) = r) :
    Function.Injective (linear4 D) := by
  intro u v huv
  calc
    u = readBack A (linear4 D u) :=
      (hleft u).symm
    _ = readBack A (linear4 D v) :=
      congrArg (readBack A) huv
    _ = v := hleft v

theorem positive_lorentzian_reconstruction
    {E : Type*}
    (rel : E → E → Prop)
    (S : E → E → ℝ)
    (b : E → Vec)
    (A D : Basis4)
    (H : Gram4)
    (k : ℝ)
    (hG : H = dualGram D)
    (hleft : ∀ r : Vec,
      readBack A (linear4 D r) = r)
    (hb : Function.Injective b)
    (hk : 0 < k)
    (h0 : D.e0.t = k)
    (h1 : D.e1.t = 0)
    (h2 : D.e2.t = 0)
    (h3 : D.e3.t = 0)
    (hord : ∀ x y,
      rel x y ↔
        (b x).t < (b y).t ∧
          0 < observedQ H b x y)
    (hvol : ∀ x y, rel x y →
      observedQ H b x y = S x y) :
    ∃ f : E → Vec,
      Function.Injective f ∧
      (∀ x y,
        rel x y ↔ chronological (f x) (f y)) ∧
      (∀ x y,
        sq (sub (f y) (f x)) =
          observedQ H b x y) ∧
      (∀ x y, rel x y →
        sq (sub (f y) (f x)) = S x y) := by

  let f : E → Vec := fun x => linear4 D (b x)

  have hmetric : ∀ x y,
      sq (sub (f y) (f x)) =
        observedQ H b x y := by
    intro x y
    change sq (sub
      (linear4 D (b y))
      (linear4 D (b x))) =
        quadratic H (sub (b y) (b x))
    rw [hG]
    exact linear4_sq D (b x) (b y)

  have htime : ∀ x, (f x).t = k*(b x).t := by
    intro x
    exact linear4_time D (b x) k h0 h1 h2 h3

  refine ⟨f, ?_, ?_, hmetric, ?_⟩

  · intro x y hxy
    apply hb
    exact linear4_injective A D hleft hxy

  · intro x y
    rw [hord x y]
    unfold chronological
    rw [htime x, htime y, hmetric x y]

    constructor
    · rintro ⟨ht,hq⟩
      exact ⟨mul_lt_mul_of_pos_left ht hk,hq⟩

    · rintro ⟨ht,hq⟩
      refine ⟨?_,hq⟩
      by_contra! hn
      have hle :=
        mul_le_mul_of_nonneg_left hn hk.le
      exact (not_lt_of_ge hle) ht

  · intro x y hxy
    exact (hmetric x y).trans (hvol x y hxy)

#print axioms linear4_sq
#print axioms linear4_time
#print axioms linear4_injective
#print axioms positive_lorentzian_reconstruction

end Chronos.ECPM.EventVolume


namespace Chronos.ECPM.EventVolume

noncomputable def triA (H : Gram4) : ℝ :=
  Real.sqrt (-H.g11)

noncomputable def triB (H : Gram4) : ℝ :=
  -H.g12 / triA H

noncomputable def triC (H : Gram4) : ℝ :=
  -H.g13 / triA H

noncomputable def triD (H : Gram4) : ℝ :=
  Real.sqrt (-H.g22 - (triB H)^2)

noncomputable def triE (H : Gram4) : ℝ :=
  (-H.g23 - triB H * triC H) / triD H

noncomputable def triF (H : Gram4) : ℝ :=
  Real.sqrt (-H.g33 - (triC H)^2 - (triE H)^2)

noncomputable def triU (H : Gram4) : ℝ :=
  -H.g01 / triA H

noncomputable def triV (H : Gram4) : ℝ :=
  (-H.g02 - triB H * triU H) / triD H

noncomputable def triW (H : Gram4) : ℝ :=
  (-H.g03 - triC H * triU H -
    triE H * triV H) / triF H

noncomputable def triK (H : Gram4) : ℝ :=
  Real.sqrt
    (H.g00 + (triU H)^2 +
      (triV H)^2 + (triW H)^2)

def pivotPositive (H : Gram4) : Prop :=
  0 < -H.g11 ∧
  0 < -H.g22 - (triB H)^2 ∧
  0 < -H.g33 - (triC H)^2 - (triE H)^2 ∧
  0 < H.g00 + (triU H)^2 +
    (triV H)^2 + (triW H)^2

def triangularFrame
    (k u v w a b c d e f : ℝ) : Basis4 :=
  ⟨⟨k,u,v,w⟩,
   ⟨0,a,0,0⟩,
   ⟨0,b,d,0⟩,
   ⟨0,c,e,f⟩⟩

theorem gram4_eq_of_fields
    (H K : Gram4)
    (h00 : H.g00 = K.g00)
    (h11 : H.g11 = K.g11)
    (h22 : H.g22 = K.g22)
    (h33 : H.g33 = K.g33)
    (h01 : H.g01 = K.g01)
    (h02 : H.g02 = K.g02)
    (h03 : H.g03 = K.g03)
    (h12 : H.g12 = K.g12)
    (h13 : H.g13 = K.g13)
    (h23 : H.g23 = K.g23) :
    H = K := by
  cases H
  cases K
  simp_all

theorem cancel_real_right
    (r s l : ℝ)
    (hl : l ≠ 0)
    (h : r*l = s*l) : r = s := by
  have hz : (r-s)*l = 0 := by
    rw [sub_mul,h,sub_self]
  exact sub_eq_zero.mp
    ((mul_eq_zero.mp hz).resolve_right hl)

theorem triangular_injective
    (k u v w a b c d e f : ℝ)
    (hk : 0 < k)
    (ha : 0 < a)
    (hd : 0 < d)
    (hf : 0 < f) :
    Function.Injective
      (linear4 (triangularFrame
        k u v w a b c d e f)) := by

  intro p q hpq

  have ht := congrArg Vec.t hpq
  have hx := congrArg Vec.x hpq
  have hy := congrArg Vec.y hpq
  have hz := congrArg Vec.z hpq

  simp only [linear4,triangularFrame,
    mul_zero,add_zero] at ht hx hy hz

  have et : p.t = q.t :=
    cancel_real_right p.t q.t k (ne_of_gt hk) ht

  have ez : p.z = q.z := by
    rw [et] at hz
    apply cancel_real_right p.z q.z f (ne_of_gt hf)
    linarith only [hz]

  have ey : p.y = q.y := by
    rw [et,ez] at hy
    apply cancel_real_right p.y q.y d (ne_of_gt hd)
    linarith only [hy]

  have ex : p.x = q.x := by
    rw [et,ez,ey] at hx
    apply cancel_real_right p.x q.x a (ne_of_gt ha)
    linarith only [hx]

  cases p
  cases q
  simp_all


private theorem triangular_frame_from_scalars
    (H : Gram4)
    (k u v w a b c d e f : ℝ)
    (hk : 0 < k)
    (ha : 0 < a)
    (hd : 0 < d)
    (hf : 0 < f)
    (haa : a^2 = -H.g11)
    (hdd : d^2 = -H.g22-b^2)
    (hff : f^2 = -H.g33-c^2-e^2)
    (hkk : k^2 = H.g00+u^2+v^2+w^2)
    (hab : a*b = -H.g12)
    (hac : a*c = -H.g13)
    (hde : d*e = -H.g23-b*c)
    (hau : a*u = -H.g01)
    (hdv : d*v = -H.g02-b*u)
    (hfw : f*w = -H.g03-c*u-e*v) :
    ∃ D : Basis4, ∃ k : ℝ,
      dualGram D = H ∧
      0 < k ∧
      D.e0.t = k ∧
      D.e1.t = 0 ∧
      D.e2.t = 0 ∧
      D.e3.t = 0 ∧
      Function.Injective (linear4 D) := by

  have hg :
      dualGram
        (triangularFrame k u v w a b c d e f)
        = H := by
    apply gram4_eq_of_fields
    all_goals
      simp only [dualGram,triangularFrame,sq,dot]
    · nlinarith only [hkk]
    · nlinarith only [haa]
    · nlinarith only [hdd]
    · nlinarith only [hff]
    · nlinarith only [hau]
    · nlinarith only [hdv]
    · nlinarith only [hfw]
    · nlinarith only [hab]
    · nlinarith only [hac]
    · nlinarith only [hde]

  exact ⟨
    triangularFrame k u v w a b c d e f,
    k,hg,hk,rfl,rfl,rfl,rfl,
    triangular_injective k u v w a b c d e f
      hk ha hd hf⟩

theorem exists_triangular_frame
    (H : Gram4)
    (hp : pivotPositive H) :
    ∃ D : Basis4, ∃ k : ℝ,
      dualGram D = H ∧
      0 < k ∧
      D.e0.t = k ∧
      D.e1.t = 0 ∧
      D.e2.t = 0 ∧
      D.e3.t = 0 ∧
      Function.Injective (linear4 D) := by

  unfold pivotPositive at hp
  rcases hp with ⟨hA,hD,hF,hK⟩

  let a := triA H
  let b := triB H
  let c := triC H
  let d := triD H
  let e := triE H
  let f := triF H
  let u := triU H
  let v := triV H
  let w := triW H
  let k := triK H

  have ha : 0 < a := Real.sqrt_pos.2 hA
  have hd : 0 < d := Real.sqrt_pos.2 hD
  have hf : 0 < f := Real.sqrt_pos.2 hF
  have hk : 0 < k := Real.sqrt_pos.2 hK

  have haa : a^2 = -H.g11 :=
    Real.sq_sqrt hA.le

  have hdd : d^2 = -H.g22-b^2 :=
    Real.sq_sqrt hD.le

  have hff : f^2 = -H.g33-c^2-e^2 :=
    Real.sq_sqrt hF.le

  have hkk : k^2 = H.g00+u^2+v^2+w^2 :=
    Real.sq_sqrt hK.le

  have hab : a*b = -H.g12 := by
    change a*(-H.g12/a) = -H.g12
    field_simp [ne_of_gt ha]

  have hac : a*c = -H.g13 := by
    change a*(-H.g13/a) = -H.g13
    field_simp [ne_of_gt ha]

  have hde : d*e = -H.g23-b*c := by
    change
      d*((-H.g23-b*c)/d) = -H.g23-b*c
    field_simp [ne_of_gt hd]

  have hau : a*u = -H.g01 := by
    change a*(-H.g01/a) = -H.g01
    field_simp [ne_of_gt ha]

  have hdv : d*v = -H.g02-b*u := by
    change
      d*((-H.g02-b*u)/d) = -H.g02-b*u
    field_simp [ne_of_gt hd]

  have hfw : f*w = -H.g03-c*u-e*v := by
    change
      f*((-H.g03-c*u-e*v)/f) =
        -H.g03-c*u-e*v
    field_simp [ne_of_gt hf]

  exact triangular_frame_from_scalars
    H k u v w a b c d e f
    hk ha hd hf
    haa hdd hff hkk
    hab hac hde hau hdv hfw


-- The embedding frame is now constructed from H,
-- rather than supplied as an assumed realization.

theorem positive_reconstruction_from_pivots
    {E : Type*}
    (rel : E → E → Prop)
    (S : E → E → ℝ)
    (b : E → Vec)
    (H : Gram4)
    (hp : pivotPositive H)
    (hb : Function.Injective b)
    (hord : ∀ x y,
      rel x y ↔
        (b x).t < (b y).t ∧
          0 < observedQ H b x y)
    (hvol : ∀ x y, rel x y →
      observedQ H b x y = S x y) :
    ∃ f : E → Vec,
      Function.Injective f ∧
      (∀ x y,
        rel x y ↔ chronological (f x) (f y)) ∧
      (∀ x y,
        sq (sub (f y) (f x)) =
          observedQ H b x y) ∧
      (∀ x y, rel x y →
        sq (sub (f y) (f x)) = S x y) := by

  rcases exists_triangular_frame H hp with
    ⟨D,k,hG,hk,h0,h1,h2,h3,hD⟩

  let f : E → Vec := fun x => linear4 D (b x)

  have hmetric : ∀ x y,
      sq (sub (f y) (f x)) =
        observedQ H b x y := by
    intro x y
    change
      sq (sub (linear4 D (b y))
        (linear4 D (b x))) =
      quadratic H (sub (b y) (b x))
    rw [← hG]
    exact linear4_sq D (b x) (b y)

  have htime : ∀ x, (f x).t = k*(b x).t := by
    intro x
    exact linear4_time D (b x) k h0 h1 h2 h3

  refine ⟨f,?_,?_,hmetric,?_⟩

  · intro x y hxy
    exact hb (hD hxy)

  · intro x y
    rw [hord x y]
    unfold chronological
    rw [htime x,htime y,hmetric x y]

    constructor
    · rintro ⟨ht,hq⟩
      exact ⟨mul_lt_mul_of_pos_left ht hk,hq⟩
    · rintro ⟨ht,hq⟩
      refine ⟨?_,hq⟩
      by_contra! hn
      have hle :=
        mul_le_mul_of_nonneg_left hn hk.le
      exact (not_lt_of_ge hle) ht

  · intro x y hxy
    exact (hmetric x y).trans (hvol x y hxy)

#print axioms gram4_eq_of_fields
#print axioms cancel_real_right
#print axioms triangular_injective
#print axioms exists_triangular_frame
#print axioms positive_reconstruction_from_pivots

end Chronos.ECPM.EventVolume

namespace Chronos.ECPM.EventVolume

def anchorCoordDot (u v : Vec) : ℝ :=
  u.t*v.t + u.x*v.x + u.y*v.y + u.z*v.z

def applyAnchorGram (H : Gram4) (v : Vec) : Vec :=
  ⟨H.g00*v.t+H.g01*v.x+H.g02*v.y+H.g03*v.z,
   H.g01*v.t+H.g11*v.x+H.g12*v.y+H.g13*v.z,
   H.g02*v.t+H.g12*v.x+H.g22*v.y+H.g23*v.z,
   H.g03*v.t+H.g13*v.x+H.g23*v.y+H.g33*v.z⟩

def anchorE0 : Vec := ⟨1,0,0,0⟩
def anchorE1 : Vec := ⟨0,1,0,0⟩
def anchorE2 : Vec := ⟨0,0,1,0⟩
def anchorE3 : Vec := ⟨0,0,0,1⟩

noncomputable def measuredAnchorGram {E : Type*} (S : E → E → ℝ)
    (a0 a1 a2 a3 a4 : E) : Gram4 :=
  ⟨S a0 a1, S a0 a2, S a0 a3, S a0 a4,
   (S a0 a1+S a0 a2-S a1 a2)/2,
   (S a0 a1+S a0 a3-S a1 a3)/2,
   (S a0 a1+S a0 a4-S a1 a4)/2,
   (S a0 a2+S a0 a3-S a2 a3)/2,
   (S a0 a2+S a0 a4-S a2 a4)/2,
   (S a0 a3+S a0 a4-S a3 a4)/2⟩

theorem anchor_quadratic_apply (H : Gram4) (v : Vec) :
    quadratic H v = anchorCoordDot v (applyAnchorGram H v) := by
  simp only [quadratic, anchorCoordDot, applyAnchorGram]
  ring

theorem anchor_quadratic_sub (H : Gram4) (u v : Vec) :
    quadratic H (sub u v) = quadratic H u + quadratic H v -
      2 * anchorCoordDot u (applyAnchorGram H v) := by
  simp only [quadratic, sub, anchorCoordDot, applyAnchorGram]
  ring

private theorem anchor_vec_ext {u v : Vec}
    (ht : u.t = v.t) (hx : u.x = v.x)
    (hy : u.y = v.y) (hz : u.z = v.z) : u = v := by
  cases u
  cases v
  simp_all

theorem measured_anchor_columns {E : Type*} (S : E → E → ℝ)
    (hs : ∀ x y, S x y = S y x) (hz : ∀ x, S x x = 0)
    (a0 a1 a2 a3 a4 : E) :
    let G := measuredAnchorGram S a0 a1 a2 a3 a4
    let b := anchorFeatures S a0 a1 a2 a3 a4
    b a0 = ⟨0,0,0,0⟩ ∧
    b a1 = applyAnchorGram G anchorE0 ∧
    b a2 = applyAnchorGram G anchorE1 ∧
    b a3 = applyAnchorGram G anchorE2 ∧
    b a4 = applyAnchorGram G anchorE3 := by
  dsimp only
  refine ⟨?_,?_,?_,?_,?_⟩
  all_goals
    apply anchor_vec_ext <;>
      simp only [anchorFeatures, measuredAnchorGram, applyAnchorGram,
        anchorE0, anchorE1, anchorE2, anchorE3, hz,
        hs a1 a0, hs a2 a0, hs a3 a0, hs a4 a0,
        hs a2 a1, hs a3 a1, hs a4 a1, hs a3 a2, hs a4 a2, hs a4 a3] <;>
      ring

-- Inverse identity and four explicit columns imply every radial measurement.
theorem anchor_radial_recovery {E : Type*} (S : E → E → ℝ)
    (hs : ∀ x y, S x y = S y x) (hz : ∀ x, S x x = 0)
    (a0 a1 a2 a3 a4 : E) (H : Gram4)
    (hinv : ∀ v, applyAnchorGram H
      (applyAnchorGram (measuredAnchorGram S a0 a1 a2 a3 a4) v) = v)
    (hr : ∀ x, quadratic H (anchorFeatures S a0 a1 a2 a3 a4 x) = S x a0) :
    ∀ x,
      observedQ H (anchorFeatures S a0 a1 a2 a3 a4) x a0 = S x a0 ∧
      observedQ H (anchorFeatures S a0 a1 a2 a3 a4) x a1 = S x a1 ∧
      observedQ H (anchorFeatures S a0 a1 a2 a3 a4) x a2 = S x a2 ∧
      observedQ H (anchorFeatures S a0 a1 a2 a3 a4) x a3 = S x a3 ∧
      observedQ H (anchorFeatures S a0 a1 a2 a3 a4) x a4 = S x a4 := by
  intro x
  rcases measured_anchor_columns S hs hz a0 a1 a2 a3 a4 with
    ⟨h0,h1,h2,h3,h4⟩
  have hq0 : quadratic H (anchorFeatures S a0 a1 a2 a3 a4 a0) = 0 := by
    rw [hr, hz]
  have hq1 := hr a1
  have hq2 := hr a2
  have hq3 := hr a3
  have hq4 := hr a4
  have hi1 := hinv anchorE0
  have hi2 := hinv anchorE1
  have hi3 := hinv anchorE2
  have hi4 := hinv anchorE3
  have flip (u v : Vec) : quadratic H (sub u v) = quadratic H (sub v u) := by
    simp only [quadratic, sub]
    ring
  refine ⟨?_,?_,?_,?_,?_⟩
  all_goals
    unfold observedQ
    rw [flip, anchor_quadratic_sub, hr x]
  · rw [hq0, h0]
    simp [anchorCoordDot, applyAnchorGram]
  · rw [hq1, h1, hi1, hs a1 a0]
    simp only [anchorCoordDot, anchorE0, anchorFeatures]
    ring
  · rw [hq2, h2, hi2, hs a2 a0]
    simp only [anchorCoordDot, anchorE1, anchorFeatures]
    ring
  · rw [hq3, h3, hi3, hs a3 a0]
    simp only [anchorCoordDot, anchorE2, anchorFeatures]
    ring
  · rw [hq4, h4, hi4, hs a4 a0]
    simp only [anchorCoordDot, anchorE3, anchorFeatures]
    ring

theorem anchor_coefficients_unique (G H : Gram4) (c b : Vec)
    (hinv : ∀ v, applyAnchorGram H (applyAnchorGram G v) = v)
    (h : applyAnchorGram G c = b) : c = applyAnchorGram H b := by
  calc
    c = applyAnchorGram H (applyAnchorGram G c) := (hinv c).symm
    _ = applyAnchorGram H b := congrArg (applyAnchorGram H) h

theorem anchor_reconstruction_from_measured_gram {E : Type*}
    (rel : E → E → Prop) (S : E → E → ℝ)
    (hs : ∀ x y, S x y = S y x) (hz : ∀ x, S x x = 0)
    (a0 a1 a2 a3 a4 : E) (H : Gram4)
    (hinv : ∀ v, applyAnchorGram H
      (applyAnchorGram (measuredAnchorGram S a0 a1 a2 a3 a4) v) = v)
    (hp : pivotPositive H)
    (hr : ∀ x, quadratic H (anchorFeatures S a0 a1 a2 a3 a4 x) = S x a0)
    (hb : Function.Injective (anchorFeatures S a0 a1 a2 a3 a4))
    (hord : ∀ x y, rel x y ↔
      (anchorFeatures S a0 a1 a2 a3 a4 x).t <
        (anchorFeatures S a0 a1 a2 a3 a4 y).t ∧
      0 < observedQ H (anchorFeatures S a0 a1 a2 a3 a4) x y)
    (hobs : ∀ x y, rel x y →
      observedQ H (anchorFeatures S a0 a1 a2 a3 a4) x y = S x y) :
    ∃ f : E → Vec,
      Function.Injective f ∧
      (∀ x y, rel x y ↔ chronological (f x) (f y)) ∧
      (∀ x y, rel x y → sq (sub (f y) (f x)) = S x y) ∧
      (∀ x,
        sq (sub (f a0) (f x)) = S x a0 ∧
        sq (sub (f a1) (f x)) = S x a1 ∧
        sq (sub (f a2) (f x)) = S x a2 ∧
        sq (sub (f a3) (f x)) = S x a3 ∧
        sq (sub (f a4) (f x)) = S x a4) := by
  rcases positive_reconstruction_from_pivots rel S
    (anchorFeatures S a0 a1 a2 a3 a4) H hp hb hord hobs with
    ⟨f,hf,ho,hm,hv⟩
  refine ⟨f,hf,ho,hv,?_⟩
  intro x
  simpa only [hm] using anchor_radial_recovery S hs hz a0 a1 a2 a3 a4 H hinv hr x

#print axioms anchor_coefficients_unique
#print axioms anchor_reconstruction_from_measured_gram
#print axioms anchor_quadratic_apply
#print axioms anchor_quadratic_sub
#print axioms measured_anchor_columns
#print axioms anchor_radial_recovery

end Chronos.ECPM.EventVolume
