# Cycle Rigidity → EntropyDepth Bridge

## Structural Statement

Let G be a bounded-degree graph family.

Suppose the cycle-incidence matrix C(G) has rank proportional to |V(G)|.

Then FO^k-local refinement systems cannot compress the configuration space beyond constant entropy loss per refinement step.

## Mechanism

Cycle complexity produces a large number of overlapping constraints between neighborhoods.

These constraints force diversification of local configuration types.

Therefore a refinement system must distinguish a growing number of configurations.

## Entropy Consequence

Let H_t be the entropy of the configuration distribution after t refinement steps.

Local refinement yields:

H_{t+1} ≥ H_t − O(1)

Thus reaching a configuration of entropy 0 requires

t ≥ Ω(|V|)

which yields an EntropyDepth lower bound.

## Role in the Chronos Program

Cycle rigidity provides the structural source of entropy that drives the EntropyDepth barrier.
