# Newstein Rooted-Ball Trivialization

## Status
Conditional target.

## Lemma
Fix \(r\). Let \(B_n\) be the torus-of-expanders base and let \(\phi_H\) be the twisted \(2\)-lift cocycle. Assume:

1. every torus gadget has side length \(L > 2r+1\);
2. the expander backbone has girth \(> 2r+1\);
3. \(\phi_H\) evaluates to \(0\) on every cycle contained in every radius-\(r\) ball.

Then for every vertex \(x \in V(B_n)\), the restriction \(\phi_H|_{B_r^{B_n}(x)}\) is a coboundary. Therefore the twisted and trivial \(2\)-lifts are isomorphic on every radius-\(r\) rooted ball:
\[
\widetilde B_r^{\,\mathrm{tw}}(x)\cong \widetilde B_r^{\,\mathrm{triv}}(x).
\]

## Consequence
The multisets of rooted radius-\(r\) neighborhoods in \(G_n\) and \(H_n\) coincide. Hence any invariant factoring through rooted radius-\(r\) type agrees on \(G_n,H_n\). In particular,
\[
\operatorname{Type}_{k,r}(G_n)=\operatorname{Type}_{k,r}(H_n).
\]

## Remaining proof obligations
1. prove every radius-\(r\) ball in \(B_n\) is homotopy-equivalent to a graph with only triangle relations;
2. prove vanishing of \(\phi_H\) on those local cycles implies coboundary on the ball;
3. formalize the lift isomorphism induced by the local transfer function.

## Overclaim guard
No proof of the lemma is claimed here.
