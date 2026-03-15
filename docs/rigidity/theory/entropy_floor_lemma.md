# Entropy Floor Lemma

## Statement

Let a refinement system operate on a bounded-degree graph family using FO^k-local rules.

If the number of distinguishable configuration types grows linearly with |V(G)|, then the entropy of the configuration distribution admits a linear lower bound.

## Formal Consequence

Let H_t denote the entropy of the configuration distribution after t refinement steps.

If configuration diversity satisfies

|Types(G)| ≥ c|V(G)|

for some constant c > 0, then

H_t ≥ Ω(|V(G)|).

## Mechanism

Configuration diversity prevents collapse of the configuration distribution under bounded-locality refinement.

Therefore the refinement process cannot eliminate entropy faster than constant rate per step.

## Role in Chronos

Configuration explosion  
→ entropy floor  
→ EntropyDepth lower bound.
