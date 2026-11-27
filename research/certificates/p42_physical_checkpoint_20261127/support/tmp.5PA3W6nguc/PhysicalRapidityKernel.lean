import PhysicalLensMass
import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp

open MeasureTheory Set
open scoped ENNReal

namespace Chronos.FourEvent

theorem physical_spacelike_rapidity_mass
    (x y : Event)
    (hx : x ∈ diamond)
    (hy : y ∈ diamond)
    (hs : invariantSq (y-x) < 0)
    (lam μ η : ℝ)
    (hη : 0 < η)
    (hP : invariantSq ((1,0)-x) =
      (Real.exp (-lam))^2)
    (hR : invariantSq ((1,0)-y) =
      (Real.exp (-μ))^2)
    (hsep : invariantSq (y-x) =
      (Real.exp (-lam))^2 +
        (Real.exp (-μ))^2 -
          2*(Real.exp (-lam)*Real.exp (-μ))*
            Real.cosh η) :
    futureMass x y =
      ENNReal.ofReal
        (Real.exp (-2*lam-2*μ-2*η) *
          (1+2*(Real.cosh η -
            Real.cosh (lam-μ))/Real.sinh η)) := by

  obtain ⟨a,b,T,ha,hb,hT,h1,h2,h3,hmass⟩ :=
    physical_spacelike_futureMass x y hx hy hs

  let P := (Real.exp (-lam))^2
  let R := (Real.exp (-μ))^2
  let p := Real.exp (-lam)*Real.exp (-μ)
  let c := Real.cosh η
  let s := Real.sinh η

  have hp : 0 < p := by
    dsimp [p]
    positivity

  have hsinh : 0 < s :=
    Real.sinh_pos_iff.mpr hη

  have ht : 0 < T := by linarith

  change invariantSq ((1,0)-x) = P at hP
  change invariantSq ((1,0)-y) = R at hR
  change invariantSq (y-x) = P+R-2*p*c at hsep

  rw [hsep] at h1
  rw [hP,hR] at h2 h3

  have ha4 :
      4*a^2 = 2*p*c-P-R := by
    linarith only [h1]

  have hT2 :
      T^2 = (P+R)/2+a^2+b^2 := by
    linarith only [h2]

  have hPR : P*R = p^2 := by
    dsimp [P,R,p]
    ring

  have hsum : P+R+4*a^2 = 2*p*c := by
    linarith only [ha4]

  have hcoshsq : c^2-1 = s^2 := by
    dsimp [c,s]
    linarith only [Real.cosh_sq_sub_sinh_sq η]

  have hkey : (2*a*T)^2 = (p*s)^2 := by
    calc
      _ = 4*a^2*T^2 := by ring
      _ = ((P-R)^2+
          8*a^2*(P+R)+16*a^4)/4 := by
        rw [hT2,h3]
        ring
      _ = (P+R+4*a^2)^2/4-P*R := by
        ring
      _ = p^2*(c^2-1) := by
        rw [hsum,hPR]
        ring
      _ = _ := by
        rw [hcoshsq]
        ring

  have hL : 0 < 2*a*T := by positivity
  have hRight : 0 < p*s := mul_pos hp hsinh

  have hcross : 2*a*T = p*s := by
    have h :=
      (sq_eq_sq_iff_abs_eq_abs _ _).mp hkey
    simpa only [abs_of_pos hL,
      abs_of_pos hRight] using h

  have hbase :
      (T-a)^2-b^2 = p*(c-s) := by
    nlinarith only [hT2,hcross,ha4]

  have hratio :
      2*a/T = 2*(c-(P+R)/(2*p))/s := by
    calc
      _ = 4*a^2/(2*a*T) := by
        field_simp [ne_of_gt ha,ne_of_gt ht] <;> ring
      _ = (2*p*c-P-R)/(p*s) := by
        rw [ha4,hcross]
      _ = _ := by
        field_simp [ne_of_gt hp,
          ne_of_gt hsinh] <;> ring

  have hkernel :
      (T+2*a)*((T-a)^2-b^2)^2/T =
        p^2*(c-s)^2*
          (1+2*(c-(P+R)/(2*p))/s) := by
    calc
      _ = ((T-a)^2-b^2)^2*
          (1+2*a/T) := by
        field_simp [ne_of_gt ht] <;> ring
      _ = _ := by
        rw [hbase,hratio]
        ring

  have hA :
      Real.exp (-lam)*Real.exp (lam-μ) =
        Real.exp (-μ) := by
    rw [← Real.exp_add]
    congr 1
    ring

  have hB :
      Real.exp (-μ)*Real.exp (-(lam-μ)) =
        Real.exp (-lam) := by
    rw [← Real.exp_add]
    congr 1
    ring

  have hcosh :
      P+R = 2*p*Real.cosh (lam-μ) := by
    dsimp [P,R,p]
    rw [Real.cosh_eq]
    calc
      _ =
        Real.exp (-lam)*
          (Real.exp (-μ)*Real.exp (-(lam-μ))) +
        Real.exp (-μ)*
          (Real.exp (-lam)*Real.exp (lam-μ)) := by
        rw [hA,hB]
        ring
      _ = _ := by ring

  have hdelta :
      (P+R)/(2*p) = Real.cosh (lam-μ) := by
    apply (div_eq_iff
      (show 2*p ≠ 0 by positivity)).mpr
    linarith only [hcosh]

  have hExp :
      p^2*(c-s)^2 =
        Real.exp (-2*lam-2*μ-2*η) := by
    calc
      _ = (p*(c-s))^2 := by ring
      _ = _ := by
        dsimp [p,c,s]
        rw [Real.cosh_sub_sinh,
          ← Real.exp_add,
          ← Real.exp_add,
          pow_two,
          ← Real.exp_add]
        congr 1
        ring

  rw [hmass,hkernel,hdelta,hExp]

#print axioms physical_spacelike_rapidity_mass

end Chronos.FourEvent
