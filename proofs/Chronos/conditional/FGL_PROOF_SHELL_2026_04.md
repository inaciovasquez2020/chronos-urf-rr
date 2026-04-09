# FGL proof shell

## Status
Conditional.

## Canonical theorem
For fixed \(k,R,B\),
\[
\mathrm{FGL}(k,R,B):
\qquad
V_{k,R,B}\cap\bigl(W_{k,R,B}\oplus \langle 1\rangle\bigr)^{\perp}=\{0\}.
\]

## Equivalent forms
\[
V_{k,R,B}\subseteq W_{k,R,B}\oplus \langle 1\rangle.
\]

\[
\forall b\in \mathcal B_{k,R,B}\setminus \bigl(W_{k,R,B}\oplus \langle 1\rangle\bigr),\quad
\exists \chi\in W_{k,R,B}\ \text{such that}\ \langle b,\chi\rangle\neq 0
\ \lor\
\langle b,1\rangle\neq 0.
\]

## Consequence
\[
\mathrm{FGL}(k,R,B)\Longrightarrow \text{finite-patch H4.1}.
\]


## Proof obligations
1. Fix an explicit canonical basis \(\mathcal B_{k,R,B}\) of \(V_{k,R,B}\).
2. Fix an explicit generating family \(\Xi_{k,R,B}\) of \(W_{k,R,B}\).
3. Form the correlation matrix
\[
M_{k,R,B}:=\bigl(\langle b,\chi\rangle\bigr)_{b\in\mathcal B_{k,R,B},\ \chi\in\Xi_{k,R,B}\cup\{1\}}.
\]
4. Prove every row indexed by
\[
b\notin W_{k,R,B}\oplus \langle 1\rangle
\]
is nonzero.
5. Conclude \(\mathrm{FGL}(k,R,B)\).
