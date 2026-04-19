# Newstein Exact Cycle-Generation Closure Target

Status: PROVED

## Statement

Let \(L\) be a connected rooted local complex, let \(T\subseteq L\) be a spanning tree, and assume:

1. every edge of \(T\) is rooted-local in \(L\);
2. the rooted-local condition is closed under unique tree-path concatenation in \(T\);
3. cycles are taken over \(\mathbf F_2\).

Define, for each \(e\in E(L)\setminus E(T)\), the fundamental cycle
\[
C_e := e + P_T(u,v)\in C_1(L;\mathbf F_2),
\]
where \(e=uv\) and \(P_T(u,v)\) is the unique tree path in \(T\) joining \(u\) and \(v\).

Then:

\[
\{C_e : e\in E(L)\setminus E(T)\}\subseteq Z_1(L;\mathbf F_2),
\]
the family \(\{C_e : e\in E(L)\setminus E(T)\}\) is linearly independent, spans \(Z_1(L;\mathbf F_2)\), and forms a rooted-local generating family.

## Dependency

This controller is proved via `docs/math/NEWSTEIN_ROOTED_LOCAL_TREE_PATH_LEMMA.md`.

## Proof

By `docs/math/NEWSTEIN_ROOTED_LOCAL_TREE_PATH_LEMMA.md`, for every non-tree edge \(e=uv\in E(L)\setminus E(T)\), the unique tree path \(P_T(u,v)\) is rooted-local in \(L\). Hence each fundamental cycle \(C_e=e+P_T(u,v)\) is rooted-local.

For each \(e=uv\in E(L)\setminus E(T)\), the chain \(P_T(u,v)\) has boundary \(u+v\), hence
\[
\partial C_e=\partial e+\partial P_T(u,v)=(u+v)+(u+v)=0
\]
in \(\mathbf F_2\). Thus \(C_e\in Z_1(L;\mathbf F_2)\).

If
\[
\sum_{e\in E(L)\setminus E(T)} a_e C_e = 0,
\qquad a_e\in \mathbf F_2,
\]
then for each fixed non-tree edge \(f\in E(L)\setminus E(T)\), the coefficient of \(f\) in the sum is exactly \(a_f\), since \(f\) appears in \(C_f\) and in no \(C_e\) with \(e\neq f\). Hence \(a_f=0\) for all \(f\), so the family is linearly independent.

Now let \(z\in Z_1(L;\mathbf F_2)\). Set
\[
S:=\operatorname{supp}(z)\cap (E(L)\setminus E(T)).
\]
Define
\[
z':= z+\sum_{e\in S} C_e.
\]
For each \(e\in S\), the non-tree edge \(e\) occurs once in \(z\) and once in \(C_e\), hence cancels in \(z'\). No other non-tree edge is introduced. Therefore \(\operatorname{supp}(z')\subseteq E(T)\). Since \(z'\in Z_1(L;\mathbf F_2)\) and a tree has no nonzero 1-cycles, we get \(z'=0\). Thus
\[
z=\sum_{e\in S} C_e,
\]
so the family spans \(Z_1(L;\mathbf F_2)\).

Because each \(C_e\) is rooted-local and the family spans \(Z_1(L;\mathbf F_2)\), it forms a rooted-local generating family.

## Consequence

This controller surface discharges:

- `docs/math/NEWSTEIN_FUNDAMENTAL_CYCLE_GENERATION_SUBLEMMA.md`
- `docs/math/NEWSTEIN_FUNDAMENTAL_CYCLE_GENERATION_PROOF_BLUEPRINT.md`
- `docs/math/NEWSTEIN_NON_TREE_EDGE_FUNDAMENTAL_CYCLE_LEMMA.md`

## Status

PROVED

## Finish condition

Closed.
