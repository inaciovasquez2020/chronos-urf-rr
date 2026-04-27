# FGL finite-patch certificate status — 2026-04-27

Status: Conditional.

This file records the executable certificate criterion only.

The FGL proof shell defines the correlation matrix with basis rows and test columns. The executable verifier therefore transposes that matrix and treats the transpose as the linear map

\[
T:E\to F^m.
\]

Given a witness matrix \(N\) whose columns span \(W_{k,R,B}\oplus\langle 1\rangle\), finite-patch FGL is certified exactly when

\[
\ker(T)\subseteq \operatorname{col}(N).
\]

The implemented rank certificate is

\[
\operatorname{rank}([N\ K])=\operatorname{rank}(N),
\]

where columns of \(K\) form a basis of \(\ker(T)\).

The quotient-rank certificate

\[
\operatorname{rank}(T)=\dim(E)-\operatorname{rank}(N)
\]

is valid only when

\[
TN=0.
\]

No finite-patch FGL proof is recorded until `artifacts/fgl/finite_patch_matrices.json` exists and `tools/certify_fgl.py` returns success.
