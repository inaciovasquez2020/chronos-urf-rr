# Four-event Minkowski causal-order certificate (2026-11-24)

Scope: four IID uniform points in a unit Alexandrov interval in 3+1-dimensional flat Minkowski spacetime. The Chronos objective is the probability that the first two elements in a uniformly selected linear extension of the induced poset are comparable; it is not the induced 2+2 probability.

Candidate exact paper-level results, supported by symbolic and rational certificates:

- M22 = 80*pi^2/21 - 552689/14700.
- p42 = 32*pi^2/7 - 13239637/294000.
- All 16 unlabeled poset probabilities are printed as exact expressions, with rational positivity and normalization checks.

## Derivation outline

For spacelike points at (0,+/-a,0,0), a residual transverse Lorentz boost places the upper endpoint at (t,b,0,0), with t >= a+abs(b). Integrating the allowed time thickness over the transverse disk and splitting the axial coordinate at 0 and b gives Vcap = pi*(t+2*a)*((t-a)^2-b^2)^2/(24*t). For comparable pairs the common future is the later point's future; their contribution to M22 is 1/17640.

Write the proper times to the upper endpoint as exp(-lambda), exp(-mu), their relative rapidity as eta, and their rapidities relative to the diamond axis as xi,zeta. The spacelike domain is 0<=xi<=lambda, 0<=zeta<=mu, abs(xi-zeta)<=eta<=xi+zeta, eta>abs(lambda-mu). The orientation-integrated product measure is 8*pi^2*exp(-4*lambda-4*mu)*sinh(xi)*sinh(zeta)*sinh(eta). The normalized common-future volume is exp(-2*lambda-2*mu-2*eta)*(1+2*(cosh(eta)-cosh(lambda-mu))/sinh(eta)).

Set m=lambda+mu, delta=lambda-mu, s=xi+zeta, d=xi-zeta. Integrate m from s+abs(d-delta) to infinity and s from eta to infinity; split the remaining square abs(d),abs(delta)<=eta along d=delta. The certificate evaluates the exponential monomials exactly, then uses x=exp(-2*eta) and the logarithmic moment integral of x^n*(-log x)/(1-x), equal to pi^2/6 minus the nth second-order harmonic number.

The finite-poset certificate enumerates 219 labeled posets and 16 isomorphism classes. Its rank-15 moment system has rank 16 after adding M22. Substitution yields the exact objective and class probabilities. The lower-level script's OPEN markers refer to that script in isolation, before the final geometric moment is supplied.

## Reproduction

From this directory, with Python 3.13.5 and SymPy 1.14.0 already available, run:

    shasum -a 256 -c SHA256SUMS
    python3 -B chronos_exact_m22_audit.py > /tmp/chronos_exact_m22_recheck.txt
    diff -u chronos_exact_m22_audit_receipt.txt /tmp/chronos_exact_m22_recheck.txt

The full audit was run successfully before publication; the receipt reproduced byte-for-byte. The certificate checks symbolic integration and finite algebra, not machine-checked justification of every geometric premise. Rapidity substitution and measure arguments are paper-level. No Lean verification, independent human peer review, priority/novelty claim, general dependent-growth result, or general spacetime reconstruction theorem is asserted. External AI assistance contributed to the rapidity integration; the symbolic calculation was separately reconstructed. This research checkpoint is proposed for review, not a release.

Base revision: 1d5209c8a67b8f9a46fb8ba8b8b3a9ec61bf04ab.
