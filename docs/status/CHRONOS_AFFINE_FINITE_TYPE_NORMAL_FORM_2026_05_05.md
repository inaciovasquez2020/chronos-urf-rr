# Chronos Affine-Finite-Type Normal Form

Status: STRUCTURAL_LOCALIZATION_ONLY  
Theorem closure: false  
FRONTIER_OPEN: true  

## Implemented objects

1. `ChronosSkeleton`
2. `ChronosCons(S,W) := S.A.mulVec W = S.b`
3. `ChronosCertificateOfWitness`
4. `ChronosEmbedding`
5. `FiniteLocalType`
6. `ChronosOneStepData`
7. `one_step_factorization`
8. `AffineFiniteTypeNormalForm`

## Boundary

This artifact does not prove Chronos ED lower bounds.

It does not prove:

- existence of a nontrivial skeleton `S_n`;
- rank optimality beyond the stored skeleton bound;
- verifier acceptance for repository certificates;
- entropy lower bound;
- Fano lower bound;
- theorem-level Chronos closure;
- H4.1/FGL closure;
- P vs NP closure.

## Remaining theorem-level obligations

1. Construct repository-specific `S_n`.
2. Bind `S_n.A` and `S_n.b` to actual verifier fields.
3. Prove the repository verifier accepts every `C(W)`.
4. Prove the affine family has entropy `Ω(n)`.
5. Prove admissible repository refinement steps instantiate `ChronosOneStepData.factor`.
