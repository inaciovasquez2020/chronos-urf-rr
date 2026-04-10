# Lean Critical Closure Checklist

## Critical graph-side closure items

### 1. Invariant layer
- define `IR : ℕ → Graph → ℕ`
- define local cycle-span denominator
- prove quotient-rank well-formedness
- prove invariance under graph isomorphism

### 2. Local tree / ball layer
- prove balls are acyclic under girth bound
- prove local cycle-span vanishes on tree balls
- prove FO\(^k\)-homogeneity from radius-\(R\) ball uniformity

### 3. Growth layer
- prove `localTwoComplexH1Rank_growth`
- prove unboundedness of `IR R G` along constructive cover family

### 4. Explicit witness layer
- define explicit witness pair `Gplus`, `Gminus`
- prove `EF_equiv_R_k Gplus Gminus`
- prove `IR R Gplus ≠ IR R Gminus`
- package as `W5_rank_separation`

### 5. Non-factorization layer
- define `FOkRDefinable`
- prove EF/local-type equality implies equal image under every `FOkRDefinable`
- derive contradiction from witness separation
- package as non-factorization theorem

## Repository hygiene condition

Critical modules must satisfy:
- zero `axiom`
- zero `sorry`
- zero `admit`

in the modules implementing:
- EF
- cycle / quotient
- separation
- normalization interfaces used by the graph-side package

## Conditional boundary

The following remain outside unconditional graph-side closure:
- `ED`
- universality embedding
- Final Wall finite closure beyond the graph-side package

They require additional definitions or new mathematics before Lean closure.

## Immediate executable order

1. `IR` definition
2. local tree/ball lemmas
3. `localTwoComplexH1Rank_growth`
4. `W5_rank_separation`
5. non-factorization theorem
