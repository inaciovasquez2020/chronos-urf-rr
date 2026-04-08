# H4.1 finite-patch correlation lemma

## Status
Conditional.

## Canonical finite-patch lemma
For every fixed natural numbers \(k,R,B\), let \(\mathcal P_{k,R,B}\) be the canonical finite class of affine-lift \(K_4\) patches formed by unions of at most \(B\) radius-\(R\) patches, and let \(X(\mathcal P_{k,R,B})\) denote the corresponding finite history space.

Then every nonzero FO\(^k\)-local basis function on \(X(\mathcal P_{k,R,B})\) has nonzero correlation with either:
1. the constant function, or
2. some bounded-support dual parity character.

Equivalently, if \(f : X(\mathcal P_{k,R,B}) \to \mathbb{R}\) is FO\(^k\)-local and orthogonal to the constant function and to every bounded-support dual parity character, then \(f = 0\).

## Consequence
Assuming this lemma, every FO\(^k\)-visible local difference on a union of at most \(B\) radius-\(R\) patches induces a nontrivial bounded-support dual dependency, yielding the finite-patch form of H4.1.

## Minimal proof obligations
1. Define \(X(\mathcal P_{k,R,B})\).
2. Define the FO\(^k\)-local observable space \(V_{k,R,B}\).
3. Define the bounded-support dual-character space \(W_{k,R,B}\).
4. Prove \(V_{k,R,B} \cap (W_{k,R,B} \oplus \langle 1\rangle)^\perp = \{0\}\).
5. Deduce \(V_{k,R,B} \subseteq W_{k,R,B} \oplus \langle 1\rangle\).

## Promotion target
Finite-patch Fourier completeness implies H4.1.
