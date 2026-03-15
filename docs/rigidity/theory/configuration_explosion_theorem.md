# Configuration Explosion Theorem

## Statement

Let G be a bounded-degree graph family with cycle-incidence rank growing linearly in |V(G)|.

Then the number of distinct local configuration types generated under FO^k-local refinement grows superlinearly with the number of vertices.

## Mechanism

Overlapping cycles create combinatorial constraints among neighborhoods.

These constraints propagate through refinement steps and generate an expanding set of distinguishable configurations.

## Consequence

Let N_t be the number of configuration types after t refinement steps.

Then

N_t ≥ N_0 + Ω(t)

and configuration diversity cannot collapse under bounded-locality refinement.

## Role

Configuration explosion provides the combinatorial driver that converts cycle rigidity into entropy growth.

Cycle rigidity  
→ configuration explosion  
→ entropy floor  
→ EntropyDepth lower bound.
