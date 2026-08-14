# Corrected AEH=1/2 exact P/Q and GQQ certificate

Date: 2026-08-14

Status: certified within the exact guarded six-state ordinary-generator
surface. This phase stops at the leading coordinate projector and the exact
finite-parameter GQQ classification.

## Leading structure and projector selection

The authoritative corrected principal Laurent coefficient has rank two,
square zero, image

\[
\operatorname{im}G_{-1}=\langle e_3,e_6\rangle,
\]

and a four-dimensional kernel. Its minimal polynomial is (z^2), with two
nilpotent Jordan blocks of size two and two blocks of size one. Thus the
rank-two image is a canonical invariant subspace, but (G_{-1}) alone does
not select a complementary projection. The additional selection criterion is
the authoritative companion state grading: (e_3,e_6) are the two
highest-derivative coordinates. It gives

\[
P_0=\operatorname{diag}(1,1,0,1,1,0),\qquad
Q_0=\operatorname{diag}(0,0,1,0,0,1).
\]

Exact arithmetic verifies the full complementary-projector algebra, with
rank (P_0=4), rank (Q_0=2). The actual leading commutator is not zero:

\[
[G_{-1},P_0]=G_{-1}\ne0.
\]

## Exact blocks and parameter meaning

Here “finite parameter” means the repository's descriptor coupling
\(\beta\). No certified repository-local identity equating the historical
Fredholm variable (q) with \(\beta\) was found. The artifact exports every
entry of all four exact blocks as a polynomial numerator in \(\beta\) over
the exact common denominator inherited from the corrected Laurent generator.
The state orders are

\[
P=(h0r0,h0r1,h1r0,h1r1),\qquad Q=(h0r2,h1r2).
\]

The original ordinary-generator guard is copied without alteration.

## Exact GQQ classification

The machine-readable artifact gives the four simplified rational entries,
their denominators, and

\[
\det G_{QQ}=
\frac{\Delta}{r^2(r-2M)^2(-16M\beta+5r^3)(8M\beta+5r^3)},
\]

where the exact polynomial \(\Delta\) is exported in full. On the ordinary
generator guard, (G_{QQ}) has rank two exactly when \(\Delta\ne0\), and
the exported two-sided inverse is valid on that additional locus. When
\(\Delta=0\), its lower-left entry is nonzero on the ordinary-generator
guard, so its rank is exactly one; exact kernel and range generators are
exported. This is a symbolic classification, not a finite-grid test.

## Historical and Fredholm boundaries

The schematic historical triangular map (D), with
\(f=1-2M/r\), does not equal the corrected exact GQQ, even at \(\beta=0\),
in the stated Q-coordinate order. Its proposed inverse (N) nevertheless
passes both symbolic compositions as an internal check of that historical
pair. Therefore `HISTORICAL_D_MATCH := corrected-different`.

The existing corrected-AEH-half (q^3) Fredholm obstruction is retained and
is not weakened. Its (q), transformed graph center, and inner block are not
connected to the present \(\beta\)-coordinate blocks by a certified exact
map, so no compatibility transfer or source-formula reuse is claimed.

This certificate constructs no invariant projector beyond (P_0), no
complement estimate, no Fredholm resolution, no horizon/outgoing closure,
and no projected-220 transfer.

Artifacts and verifier:

- `artifacts/chronos/gfe_corrected_AEH_half_pq_gqq.json`
- `artifacts/chronos/gfe_corrected_AEH_half_pq_gqq_receipt.txt`
- `tools/gfe/derive_gfe_corrected_pq_gqq.py`
- `tests/test_gfe_corrected_pq_gqq.py`
