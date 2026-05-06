# Chronos Repository-Native Certified Depth Bridge — 2026-05-06

Status: REPOSITORY_NATIVE_DEPTH_BRIDGE_FORMALIZED

## Closed surface

- `RepositoryNativeDepth` is defined from `RepositoryNativeCarrierIso.depthAnnotation`.
- `EmbedSearchFamilyRepositoryNative` lands in the repository-native certified carrier by using `I.backward n x.query`.
- `embeddingCorrect` is proved by `I.right_inv`.
- `EmbedSearchFamilyPreservesObstructions` preserves:
  - `k = n ∨ k ≤ n`
  - `2 * C.linearConstant ≤ Δ`
  - `n ≤ r`
- `RepositoryNativeCertifiedDepthLowerBound` is proved without explicit certificate depth.
- The file is prelude-only and does not import `Mathlib`.

## Required admissibility inputs

- `hk : k = n ∨ k ≤ n`
- `hrn : n ≤ r`

## Boundary

- Does not assert theorem-level Chronos closure.
- Does not assert H4.1 closure.
- Does not assert FGL closure.
- Does not assert P vs NP closure.
- `FRONTIER_OPEN` is preserved.
