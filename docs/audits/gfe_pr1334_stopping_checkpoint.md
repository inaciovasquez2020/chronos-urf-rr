# PR #1334 — source-table curvature-audit coverage

Source: `tools/gfe/derive_gfe_axial_quadratic_action.sh`, inspected at remote HEAD `55a0405dfa0ad831f8ae6c04ad06c96b6b68e875`.

**Coverage: 13/28 nonzero source-table monomials have prior reported curvature-comparison receipts; 15/28 lack an identified independent comparison receipt.**

This matrix inventories prior local receipts. It does not independently rerun the expensive full curvature calculations, authenticate source code provenance, or establish complete action verification. The 28-term table-to-Euler algebraic audit is a distinct, conditional check.

| Monomial | Status | Scope / receipt |
|---|---|---|
| `k0^2` | Reported curvature comparison | M=1, ell=2, r>2 (angular degree bound conditional) `gfe_corrected_sixjet_certificate_receipt.txt` |
| `k0_r*k0` | Reported curvature comparison | M=1, ell=2, r>2 (angular degree bound conditional) `gfe_corrected_sixjet_certificate_receipt.txt` |
| `k0_r*k1_rt` | **OPEN** | No identified receipt |
| `k0_r*k1_t` | **OPEN** | No identified receipt |
| `k0_r^2` | Reported curvature comparison | M=1, ell=2, r>2 (angular degree bound conditional) `gfe_corrected_sixjet_certificate_receipt.txt` |
| `k0_rr*k0` | Reported curvature comparison | M=1, ell=2, r>2 (angular degree bound conditional) `gfe_corrected_sixjet_certificate_receipt.txt` |
| `k0_rr*k0_r` | Reported curvature comparison | M=1, ell=2, r>2 (angular degree bound conditional) `gfe_corrected_sixjet_certificate_receipt.txt` |
| `k0_rr*k1_rt` | **OPEN** | No identified receipt |
| `k0_rr*k1_t` | **OPEN** | No identified receipt |
| `k0_rr^2` | Reported curvature comparison | M=1, ell=2, r>2 (angular degree bound conditional) `gfe_corrected_sixjet_certificate_receipt.txt` |
| `k0_rt*k0_t` | **OPEN** | No identified receipt |
| `k0_rt*k1` | Reported curvature comparison | M=1, ell=2, r=3 (angular degree bound conditional) `gfe_mixed_h0rt_h1_certificate_receipt.txt` |
| `k0_rt*k1_tt` | Reported curvature comparison | M=1, ell=2, r=3 (angular degree bound conditional) `gfe_h0rt_h1tt_angle_receipt.txt` |
| `k0_rt^2` | **OPEN** | No identified receipt |
| `k0_t*k1` | Reported curvature comparison | M=1, ell=2, r=3 (angular degree bound conditional) `gfe_mixed_h0t_h1_audit_receipt.txt` |
| `k0_t*k1_r` | **OPEN** | No identified receipt |
| `k0_t*k1_tt` | **OPEN** | No identified receipt |
| `k0_t^2` | Reported curvature comparison | M=1, ell=2, r=3 (angular degree bound conditional) `gfe_time_h0t_squared_certificate_receipt.txt` |
| `k1^2` | **OPEN** | No identified receipt |
| `k1_r*k1` | **OPEN** | No identified receipt |
| `k1_r^2` | **OPEN** | No identified receipt |
| `k1_rt*k0` | **OPEN** | No identified receipt |
| `k1_rt*k1_t` | Reported curvature comparison | M=1, ell=2, r=3 (angular degree bound conditional) `gfe_h1rt_h1t_exact_receipt.txt` |
| `k1_rt^2` | **OPEN** | No identified receipt |
| `k1_t*k0` | Reported curvature comparison | M=1, ell=2, r=3 (angular degree bound conditional) `gfe_reciprocal_mixed_certificate_receipt.txt` |
| `k1_t^2` | Reported curvature comparison | M=1, ell=2, r=3 (angular degree bound conditional) `gfe_time_h1t_squared_certificate_receipt.txt` |
| `k1_tt*k1` | **OPEN** | No identified receipt |
| `k1_tt^2` | **OPEN** | No identified receipt |

## Additional tested zero slot

`k0_rt*k1_t` (absent from published table): previously reported five-angle zero check, not counted among the 28 nonzero monomials.

## Release gate / stopping point

- Preserve PR #1334 as DRAFT and retain independent mathematical review.
- This audit branch is documentation-only; do not merge or promote the PR, change assumptions, or claim the complete Schwarzschild axial action is verified.
- Next priority: one of the 15 uncovered time-dependent monomials, using isolated jets, exact angular holdouts, and immutable curvature source hashes.
- All-mode and independent second-implementation checks remain OPEN.
- No local Git repository inspection or CI rerun was performed during the original coverage inventory.
- The CSV records SHA256 values for receipts from the conversation workspace; those receipts are not included in this documentation-only branch.
