# Newstein Rooted-Ball Trivialization Reduction

Status: PROVED

## Reduction statement
Assume TreeContractionHomotopy:
\[
\partial h + h \partial = \operatorname{Id} - \operatorname{Retr}_r
\]
on the chain complex of the rooted ball \(B_R(r)\).

Then every \(1\)-cycle \(z \in Z_1(B_R(r);\mathbf F_2)\) is a boundary.

## Proof
Let \(z \in Z_1(B_R(r);\mathbf F_2)\), so \(\partial z = 0\).
Apply the homotopy identity:
\[
z
=
(\partial h + h\partial)(z) + \operatorname{Retr}_r(z).
\]
Since \(\partial z = 0\), this becomes
\[
z = \partial h(z) + \operatorname{Retr}_r(z).
\]
The retraction \(\operatorname{Retr}_r\) sends every \(1\)-chain to \(0\), because the root complex has no nontrivial \(1\)-simplices. Hence
\[
z=\partial h(z).
\]
Therefore \(z\) is a boundary.

## Output
RootedBallTrivialization is reduced to TreeContractionHomotopy plus the vanishing of \(1\)-chains on the root retract.

## Proof status
Proved from TreeContractionHomotopy and vanishing of \(1\)-chains on the root retract.

