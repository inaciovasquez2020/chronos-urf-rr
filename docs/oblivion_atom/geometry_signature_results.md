# Geometry Signature Results

## Random 4-Regular Graph

File: `geometry_rr_R12.png`

Observed behavior:

- Ball size grows exponentially
- Cycle rank grows proportionally
- Density stabilizes

\[
|B_R| \approx \Delta^R,\quad \beta_1(B_R) \approx c\,|B_R|
\]

Interpretation: **expander geometry**

Implication:

Cycle-overlap rank grows rapidly, forcing FO^k type diversity.

---

## Two-Lift Expander

File: `geometry_twolift_R12.png`

Observed behavior:

- Similar exponential growth
- Stable cycle density
- No sheet-like regime

Interpretation: **expander-of-expanders**

Implication:

Large COR regime consistent with Oblivion Atom hypothesis.

---

## Diagnostic Conclusion

The geometry signature separates three regimes:

| Geometry | Growth | Cycle Density |
|---------|--------|---------------|
| Tree | exponential | 0 |
| Sheet | polynomial | constant |
| Expander | exponential | constant |

The tested graphs fall in the **expander regime**, which supports
the cycle-overlap → FO^k diversity mechanism.

