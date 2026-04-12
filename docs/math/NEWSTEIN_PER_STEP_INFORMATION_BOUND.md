# Newstein Per-Step Information Bound

## Target statement

In the admissible refinement model,
\[
\Delta I_t \le C
\quad
\text{for every admissible step } t,
\]
for a uniform constant \(C\) independent of \(n\).

## Required model ingredients

### 1. Admissible refinement state

Specify the state space \(S_t\) of the refinement process.

### 2. Transcript observable

Specify the information quantity \(I_t\) measured at step \(t\).

### 3. Locality / bounded-width constraint

Specify the structural restriction forcing each step to access only bounded local data.

### 4. Uniform encoding bound

Prove each admissible update is selected from a class of descriptions of size at most \(2^C\).

## Required subclaims

### 1. Conditional information increment formula

Express
\[
\Delta I_t := I_{t+1}-I_t
\]
as the information added by one admissible update.

### 2. Bounded choice family

Prove the admissible update family at each step has cardinality bounded by a constant depending only on the model parameters.

### 3. Entropy ceiling

Deduce
\[
\Delta I_t \le \log_2 |\mathcal U_t| \le C.
\]

## Deduction

By bounded locality / bounded-width admissibility, each step chooses from a uniformly bounded update family.

Hence one step contributes at most constant information.

Therefore
\[
\Delta I_t \le C.
\]

## Status

This is the critical remaining theorem-level target in the Newstein complexity branch.

## Dependencies discharged by this theorem

1. Input to the transcript lower bound.
2. Completion of the linear-time obstruction branch.
3. Final bridge from quotient-gap separation to refinement complexity.
