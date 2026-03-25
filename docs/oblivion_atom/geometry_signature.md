# Geometry Signature Diagnostic

For a rooted vertex \(v_0\) and radius \(R\), define

- \(B_R(v_0)\) : radius-\(R\) ball
- \(|B_R|\) : number of vertices in the ball
- \(\beta_1(B_R)\) : first Betti number (cycle rank)
- \(\rho(R) = \beta_1(B_R) / |B_R|\)

The tuple

\[
(|B_R|,\beta_1(B_R),\rho(R))_{R=1}^{R_{\max}}
\]

is the **geometry signature** of the graph around \(v_0\).

## Interpretation

Tree-like geometry  
\[
\beta_1(B_R)=0,\quad \rho(R)=0
\]

2-dimensional sheet  
\[
|B_R| \sim R^2,\quad \beta_1(B_R)\sim R^2,\quad \rho(R)\approx \text{constant}
\]

Expander geometry  
\[
|B_R| \sim \Delta^R,\quad \beta_1(B_R)\sim \Delta^R,\quad \rho(R)\approx \text{constant}
\]

## Purpose in Oblivion Atom

The geometry signature distinguishes the regimes responsible for
cycle-overlap rank growth and FO^k type diversity.

Scripts:

- `geometry_signature_scan.py`
- `graph_geometry_plot.py`

Outputs:

- `geometry_rr_R12.png`
- `geometry_twolift_R12.png`
