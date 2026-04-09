# FGL terminal assumption

## Status
Conditional.

The sole remaining assumption for unconditional finite-patch H4.1 is:

\[
\mathrm{FGL}(k,R,B):
\qquad
V_{k,R,B}\cap \bigl(W_{k,R,B}\oplus \langle 1\rangle\bigr)^{\perp}=\{0\}.
\]

Equivalent basis form:
\[
\forall b\in \mathcal B_{k,R,B}\setminus \bigl(W_{k,R,B}\oplus \langle 1\rangle\bigr),
\quad
\exists \chi\in W_{k,R,B}\ \text{such that}\ \langle b,\chi\rangle\neq 0
\ \lor\
\langle b,1\rangle\neq 0.
\]

Equivalent matrix form:
\[
\forall b\in \mathcal B_{k,R,B}\setminus \bigl(W_{k,R,B}\oplus \langle 1\rangle\bigr),
\quad
\bigl(\langle b,\chi\rangle\bigr)_{\chi\in \Xi_{k,R,B}\cup\{1\}}\neq 0.
\]

Once \(\mathrm{FGL}(k,R,B)\) is proved,
the finite-patch form of H4.1 is unconditional.
