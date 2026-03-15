# EntropyDepth Implication for SAT

## Statement

Let F be a family of SAT instances encoded as bounded-degree constraint graphs.

Suppose the associated configuration space has entropy

H(F) ≥ c n

for some constant c > 0, where n is the number of variables.

If each refinement step reveals at most O(1) information about the configuration space, then any refinement-based algorithm must satisfy

t ≥ Ω(n)

steps to determine satisfiability.

## Interpretation

Local reasoning procedures cannot collapse the configuration uncertainty faster than constant rate.

Therefore SAT instances whose configuration entropy grows linearly force linear refinement depth.

## Structural Chain

Cycle rigidity  
→ configuration explosion  
→ entropy floor  
→ EntropyDepth lower bound  
→ Chronos wall  
→ SAT refinement lower bound.
