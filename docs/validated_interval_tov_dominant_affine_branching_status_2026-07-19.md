# Validated Interval TOV Dominant-Affine Branching Status

Date: 2026-07-19

## Verified foundation

- Baseline and cached one-step enclosures were identical.
- Independent branches retained separate states, affine registries, certificates, clocks, and adaptive step sizes.
- Live branches at different integration times were never merged.
- Compactness-domain failures were handled as branch-local recoverable failures.
- Tentative branch operations remained transactional.
- The original validated interval TOV source files remained unchanged.

## Best bounded runs

### Farthest integration coordinate

V4 reached:

- tau: `0.008681466547514465`
- accepted steps on the failing branch: `92`
- branches: `128`

### Highest accepted-step count

V6 reached:

- tau: `0.008541388631086813`
- accepted steps on the failing branch: `103`
- branches: `128`

### Rejected scheduler variant

V7 reached:

- tau: `0.00821652875592201`
- accepted steps on the failing branch: `97`
- branches: `128`
- maximum split depth: `12`

V7 delayed subdivision too long, allowing the affine enclosures to widen before splitting. It was therefore rejected.

## Final boundary

Changing branch-count limits, shared versus local clocks, retry windows, and rejection-debt heuristics did not remove the underlying obstruction.

The unresolved numerical-analysis object is a certified affine reconditioning or generator-reduction method that controls enclosure growth without unsoundly merging independent live branches.

Additional scheduler variants would tighten implementation behavior without materially strengthening a mathematical or scientific claim.

## Preserved verification hashes

- Branch-contract bundle:
  `96453b5c757dce949d7d3dd7d0bcba14a920ecc62898c9c592026efb01d23ffe`
- Validated ODE source:
  `d6e06342e017b390b40c07daf6a755f902b09b396684c675860e0de9bdbd0e3d`
- Enthalpy-logit split source:
  `a1f7b6912ceabb69f6870eb50c01318e8a5524cf7fc0e26873bd6964897bd078`
- Affine centered-residual probe:
  `d9a6aef3f39cac561236a52fd1db16a314c1a01a18da653984038fd3a0129cbb`

## Decision

The dominant-affine branching experiment is frozen at this boundary. No v8 scheduler variant is recommended.
