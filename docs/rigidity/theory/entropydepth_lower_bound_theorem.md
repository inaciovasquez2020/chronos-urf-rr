# EntropyDepth Lower Bound Theorem

## Statement

Let G be a bounded-degree graph family and consider any FO^k-local refinement system operating on G.

If the configuration entropy satisfies

H(G) ≥ c|V(G)|

for some constant c > 0, and each refinement step reduces entropy by at most O(1), then the number of refinement steps required to reach a terminal configuration satisfies

t ≥ Ω(|V(G)|).

## Interpretation

Local refinement systems cannot eliminate large-scale configuration entropy quickly.

The bounded locality of refinement rules imposes a constant-rate limit on entropy reduction.

## Consequence

The refinement depth required to collapse the configuration space grows at least linearly with the graph size.

This quantity is the EntropyDepth of the instance.

## Role in Chronos

Cycle rigidity  
→ configuration explosion  
→ entropy floor  
→ EntropyDepth lower bound.
