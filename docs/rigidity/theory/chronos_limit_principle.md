# Chronos Limit Principle

## Statement

Let A be a computation that operates by bounded-locality refinement on a structure of size n.

If each refinement step reveals at most O(1) bits of information, then the total information extracted after t steps is

I_total ≤ O(t).

If the initial uncertainty of the configuration space satisfies

H ≥ Ω(n),

then resolving that uncertainty requires

t ≥ Ω(n).

## Interpretation

Computation based on bounded-locality refinement has a fixed information bandwidth.

Therefore the time required to resolve global uncertainty must scale with the size of the system.

## Role in Chronos

The Chronos Limit Principle explains why EntropyDepth barriers translate into algorithmic time lower bounds.
