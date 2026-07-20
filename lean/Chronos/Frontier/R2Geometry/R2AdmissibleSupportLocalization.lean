import Chronos.Frontier.R2Geometry.R2FacePathMetricBound
import Chronos.Frontier.R2Geometry.R2MetricDiameterObstructionKernel

/-!
# Admissible filling-support localization

This module derives the global localization hypothesis used by the genuine
metric obstruction kernel from:

* a uniform metric diameter bound on every two-face; and
* a uniform bound on overlap-path lengths between any two nonzero faces in an
  admissible filling.

The remaining concrete geometric task is to prove the bounded overlap-path
property for the intended R2 filling class.
-/

noncomputable section

namespace Chronos
namespace Frontier

open R2FillingGeometry

variable
  (G : R2FillingGeometry)
  (Adm : (G.Face2 →₀ F2) → Prop)
  (ε : ℝ)
  (N : Nat)

/--
Any two nonzero faces in an admissible filling are connected by an overlapping
face path of length at most `N`.
-/
def AdmissibleDualPathBound : Prop :=
  ∀ F,
    Adm F →
    ∀ first,
      F first ≠ 0 →
      ∀ last,
        F last ≠ 0 →
        ∃ length,
          length ≤ N ∧
          FacePath G first last length

/--
The face-path metric bound is monotone in path length when the uniform face
diameter bound is nonnegative.
-/
theorem facePathMetricBound_mono
    (hε : 0 ≤ ε)
    {firstLength secondLength : Nat}
    (hLength : firstLength ≤ secondLength) :
    FacePathMetricBound ε firstLength ≤
      FacePathMetricBound ε secondLength := by
  have hCast :
      (firstLength : ℝ) ≤ (secondLength : ℝ) := by
    exact_mod_cast hLength

  have hCoefficient :
      2 * (firstLength : ℝ) + 1 ≤
        2 * (secondLength : ℝ) + 1 := by
    linarith

  simpa [FacePathMetricBound] using
    mul_le_mul_of_nonneg_right hCoefficient hε

/--
Uniform face diameter and bounded dual overlap paths imply a global metric
localization bound for every admissible filling support.
-/
theorem admissibleLocalized_of_dualPathBound
    (hε : 0 ≤ ε)
    (hFaceDiameter : FaceDiameterBound G ε)
    (hDualPath : AdmissibleDualPathBound G Adm N) :
    AdmissibleLocalized G Adm (FacePathMetricBound ε N) := by
  intro F hAdm x hx y hy

  rcases hx with
    ⟨first, hFirstNonzero, hxFirst⟩

  rcases hy with
    ⟨last, hLastNonzero, hyLast⟩

  obtain
    ⟨length, hLength, hPath⟩ :=
    hDualPath
      F
      hAdm
      first
      hFirstNonzero
      last
      hLastNonzero

  have hPathMetric :
      dist x y ≤ FacePathMetricBound ε length :=
    face_path_metric_bound
      G
      ε
      hFaceDiameter
      hPath
      hxFirst
      hyLast

  have hBoundMonotone :
      FacePathMetricBound ε length ≤
        FacePathMetricBound ε N :=
    facePathMetricBound_mono
      ε
      hε
      hLength

  exact le_trans hPathMetric hBoundMonotone

/--
A boundary separated beyond the uniform dual-path metric bound cannot be
filled by an admissible two-chain.
-/
theorem diameter_separation_filling_obstruction_of_dualPathBound
    (hε : 0 ≤ ε)
    (hFaceDiameter : FaceDiameterBound G ε)
    (hDualPath : AdmissibleDualPathBound G Adm N)
    (c : G.Face1 →₀ F2)
    (hSeparated :
      G.Separated c (FacePathMetricBound ε N)) :
    ¬ G.Fillable Adm c :=
  diameter_separation_filling_obstruction
    G
    Adm
    (FacePathMetricBound ε N)
    (admissibleLocalized_of_dualPathBound
      G
      Adm
      ε
      N
      hε
      hFaceDiameter
      hDualPath)
    c
    hSeparated

end Frontier
end Chronos
