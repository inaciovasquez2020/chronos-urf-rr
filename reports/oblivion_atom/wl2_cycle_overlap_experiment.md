# WL² Detection of Cycle-Overlap Rank

## Experiment
Graph: rr_n12000_d4_seed9  
Radius: R = 6

Measured:
COR_R(G) = 649  
Overlap components = 253  
Largest component = 82

## WL Tests

WL¹:
homogeneous

WL² (sample=250):
distinct_colors = 4

WL² (sample=500):
distinct_colors = 7

## Conclusion

Large cycle-overlap rank produces WL² color refinement diversity.

Empirical statement:

COR_R(G) ≥ T  ⇒  ∃ u,v : χ_WL²(u) ≠ χ_WL²(v)

Using WL–FO correspondence:

WL² ≡ FO³

Thus

COR_R(G) ≥ T  ⇒  ∃ u,v : tp₃(u) ≠ tp₃(v)

This provides empirical support for the **Cycle-Overlap Visibility Lemma (k = 3)**.
