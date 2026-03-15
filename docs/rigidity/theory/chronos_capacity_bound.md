# Chronos Capacity Bound

## Statement

Let a refinement algorithm operate on a structure of size n using bounded-locality rules.

Suppose the algorithm maintains an internal state of bounded information capacity C.

Then the total information that can be accumulated after t refinement steps satisfies

I_total ≤ C + O(t).

## Interpretation

The algorithm’s state cannot accumulate unlimited global information in a single step.

Information must enter the system gradually through refinement interactions with the structure.

## Consequence

If the configuration entropy of the structure satisfies

H ≥ Ω(n),

then any refinement-based algorithm requires

t ≥ Ω(n)

steps to resolve the configuration space.

## Role in Chronos

The capacity bound complements the entropy conservation principle and establishes the information-bandwidth limitation of refinement computation.
