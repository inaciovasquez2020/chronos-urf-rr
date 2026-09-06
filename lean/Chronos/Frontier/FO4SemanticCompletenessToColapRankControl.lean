import Chronos.Frontier.FO4SemanticCompletenessSurface

namespace Chronos
namespace Frontier
namespace FO4SemanticCompletenessToColapRankControl

open FO4HomogeneousOpenProblem
open FO4ColapROpenProblem
open FO4RadiusRTypeEnumerationSurface
open FO4SemanticCompletenessSurface

def rankWitnessNeighborhood
    (X : FO4HomogeneousInput)
    (ρ : ColapR X.G X.R)
    (i : Fin ρ.rank) : FO4RadiusRNeighborhood X.G :=
  ⟨(ρ.basisWitness i).left.center, X.R⟩

noncomputable def semanticRankTypeSignature
    (Delta R : Nat)
    (hsem : SemanticCompleteFO4RadiusRTypeCodes Delta R)
    (X : FO4HomogeneousInput)
    (hDelta : X.Delta = Delta)
    (hR : X.R = R)
    (hdeg : X.degree_bounded)
    (ρ : ColapR X.G X.R) : FO4RankTypeSignature X ρ where
  typeCount := FO4RadiusRTypeBound Delta R
  typeOf := fun i =>
    let N := rankWitnessNeighborhood X ρ i
    let hN : BoundedDegreeRadiusRNeighborhood Delta R X N :=
      ⟨hDelta, hR, hR, hdeg⟩
    let T := Classical.choose (hsem X hDelta hR hdeg N hN)
    ⟨T.type_code.code, T.type_code.code_lt_bound⟩

def UniformSemanticFO4FiberBound
    (Delta R : Nat)
    (hsem : SemanticCompleteFO4RadiusRTypeCodes Delta R) : Prop :=
  ∃ M : Nat,
    ∀ X : FO4HomogeneousInput,
      ∀ hDelta : X.Delta = Delta,
      ∀ hR : X.R = R,
      ∀ hHom : FO4Homogeneous X,
      ∀ ρ : ColapR X.G X.R,
        ∃ h : FO4BoundedFiberEncoding X ρ
          (semanticRankTypeSignature Delta R hsem X hDelta hR hHom.1 ρ),
          h.fiberBound ≤ M

theorem uniformSemanticFO4FiberBound_impossible_of_unconstrained_rank
    (Delta R : Nat)
    (hsem : SemanticCompleteFO4RadiusRTypeCodes Delta R) :
    ¬ UniformSemanticFO4FiberBound Delta R hsem := by
  intro hU
  rcases hU with ⟨M, hM⟩
  let G : GraphDatum :=
    { vertex := Unit
      adj := fun _ _ => False }
  let X : FO4HomogeneousInput :=
    { Delta := Delta
      R := R
      G := G
      degree_bounded := True
      radius_R_FO4_indistinguishable := True }
  have hHom : FO4Homogeneous X := ⟨trivial, trivial⟩
  let w : RadiusRCycleWitness G :=
    { center := ()
      support := fun _ => False
      radius_R_local := True
      cycle_witness := True }
  let inc : CycleOverlapIncidence G R :=
    { left := w
      right := w
      overlaps_within_radius := True }
  let N : Nat := FO4RadiusRTypeBound Delta R * M + 1
  let ρ : ColapR X.G X.R :=
    { coeff := fun _ => F2.zero
      finite_support := True
      rank := N
      basisWitness := fun _ => inc }
  rcases hM X rfl rfl hHom ρ with ⟨henc, hfiber_le⟩
  have hrank : ρ.rank ≤ FO4RadiusRTypeBound Delta R * henc.fiberBound := by
    simpa [semanticRankTypeSignature] using rank_le_typeCount_mul_fiberBound henc
  have hle : N ≤ FO4RadiusRTypeBound Delta R * M := by
    simpa [ρ] using
      Nat.le_trans hrank
        (Nat.mul_le_mul_left (FO4RadiusRTypeBound Delta R) hfiber_le)
  have hbad : FO4RadiusRTypeBound Delta R * M + 1 ≤ FO4RadiusRTypeBound Delta R * M := by
    simpa [N] using hle
  exact Nat.not_succ_le_self _ hbad

def ColapRankControlFromSemanticCompleteness (Delta R : Nat) : Prop :=
  ∀ hsem : SemanticCompleteFO4RadiusRTypeCodes Delta R,
    UniformSemanticFO4FiberBound Delta R hsem →
      ∃ C : Nat,
        ∀ X : FO4HomogeneousInput,
          X.Delta = Delta →
          X.R = R →
          FO4Homogeneous X →
          ColapRankBoundedAt X C

theorem semanticCompletenessToColapRankControl
    (Delta R : Nat) :
    ColapRankControlFromSemanticCompleteness Delta R := by
  intro hsem hfiber
  rcases hfiber with ⟨M, hM⟩
  refine ⟨FO4RadiusRTypeBound Delta R * M, ?_⟩
  intro X hDelta hR hHom ρ
  rcases hM X hDelta hR hHom ρ with ⟨henc, hfiber_le⟩
  calc
    ρ.rank ≤ FO4RadiusRTypeBound Delta R * henc.fiberBound := by
      simpa [semanticRankTypeSignature] using rank_le_typeCount_mul_fiberBound henc
    _ ≤ FO4RadiusRTypeBound Delta R * M :=
      Nat.mul_le_mul_left (FO4RadiusRTypeBound Delta R) hfiber_le

def FO4CycleOverlapRankBoundConditional : Prop :=
  ∀ hsem : FO4SemanticCompletenessHypothesis,
    (∀ Delta R : Nat, UniformSemanticFO4FiberBound Delta R (hsem Delta R)) →
      ∀ Delta R : Nat,
        ∃ C : Nat,
          ∀ X : FO4HomogeneousInput,
            X.Delta = Delta →
            X.R = R →
            FO4Homogeneous X →
            ColapRankBoundedAt X C

theorem fo4CycleOverlapRankBoundConditional :
    FO4CycleOverlapRankBoundConditional := by
  intro hsem hfiber Delta R
  exact semanticCompletenessToColapRankControl Delta R (hsem Delta R) (hfiber Delta R)

def FrontierStatus : String :=
  "CONDITIONAL_BOUNDED_FIBER_COLAP_RANK_CONTROL"

def Boundary : String :=
  "Semantic completeness constructs the finite rank-to-FO4 type signature, but the current unconstrained Nat rank makes every uniform semantic fiber bound impossible. No raw COR overlap-compression theorem, unconditional ColapR rank bound, rigidity closure, P vs NP, or Clay problem is proved."

def NextMissingLemma : String :=
  "CanonicalCorrectedColapRank: replace unconstrained rank with a finite-dimensional F2 rank derived from corrected overlap data that quotients translation/orbit replication; only then can a uniform semantic fiber bound be meaningfully attempted."

end FO4SemanticCompletenessToColapRankControl
end Frontier
end Chronos
