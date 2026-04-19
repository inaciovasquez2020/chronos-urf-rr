# SiMSLV Local Triangle Predicate

Status: OPEN

## Definition

Fix a rooted radius-\(r\) ball \(B_r(x)\) in the witness-layer \(2\)-complex.

Define the locality-preserving triangle predicate
\[
\Phi_2(u,v,w)
\]
to mean:

1. \(u,v,w \in B_r(x)\).
2. The edges \((u,v)\), \((v,w)\), and \((u,w)\) are present in the witness-layer \(1\)-skeleton.
3. The \(2\)-simplex \([u,v,w]\) is declared admissible in the local witness-layer structure.
4. For every \(I \subseteq \{0,1,2\}\), if
\[
y_t=
\begin{cases}
p(x_t), & t\in I,\\
x_t, & t\notin I,
\end{cases}
\]
then
\[
\Phi_2(x_0,x_1,x_2)\Longrightarrow \Phi_2(y_0,y_1,y_2)
\]
whenever the substituted triple remains in the same rooted radius-\(r\) ball.

## Role

This predicate is intended to canonically detect exactly the local \(2\)-simplices whose boundaries generate
\[
Z_1(B_r(x);\mathbb F_2).
\]

## Finish condition

Replace this OPEN definition file by a theorem-level local predicate specification sufficient to support the fundamental cycle-generation lemma and triangle-vanishing theorem.
