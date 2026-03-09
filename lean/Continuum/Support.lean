import «Continuum».Basic

namespace Continuum

axiom totalSupport_lower_of_uniform
  (F : SupportFamily) {s : Rat}
  (hs : HasUniformSupportLower F s) :
  (s * F.m) ≤ F.totalSupport

axiom gramLowerDiagonal_lower_of_uniform
  (F : SupportFamily) {a : Rat}
  (ha : HasUniformNormLower F a) :
  (a * a * F.m) ≤ F.gramLowerDiagonal

axiom diagonal_dominates_gram
  (F : SupportFamily) :
  F.gramLowerDiagonal ≤
    ((List.range F.m).bind fun i =>
      (List.range F.m).map fun j =>
        (if h : i = j then (F.normSq i) * (F.normSq j) else 0))).foldl (· + ·) 0

axiom overlap_identity
  (F : SupportFamily) :
  F.overlapSquare =
    F.totalSupport +
    (((List.range F.m).bind fun i =>
      (List.range F.m).filterMap fun j =>
        if i = j then none else some (F.overlapMass i j))).foldl (· + ·) 0)

axiom offDiagonalOverlap_bound
  (F : SupportFamily) {K : Rat}
  (hK : HasControlledOverlap F K) :
  (((List.range F.m).bind fun i =>
      (List.range F.m).filterMap fun j =>
        if i = j then none else some (F.overlapMass i j))).foldl (· + ·) 0)
  ≤ (K - 1) * F.totalSupport

end Continuum
