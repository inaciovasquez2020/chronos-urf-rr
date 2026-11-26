# Chronos priority dossier — 2026-11-26

Status: paper proof, exact finite arithmetic replay; Lean NOT_RUN; independent human review OPEN; novelty NOT_ESTABLISHED; public disclosure of this version NOT_DONE.

- `manuscript.pdf` / `manuscript.tex`: four-page research preprint draft and editable LaTeX source.
- `original_certificate.md`, `verify_original.py`, `original_receipt.txt`: preserved three-birth result; input checksums verified before copying.
- `verify_general.py`, `general_receipt.txt`: independent rational enumeration of natural-label classes, all-dimension moment formula checks (d=2..100) and universal discrepancy identity on a finite rational simplex.
- `SHA256SUMS`: binds the included files.

## Reproduction (macOS, no installation or downloads)
From the extracted folder, with Python 3 available:

```sh
shasum -a 256 -c SHA256SUMS &&
python3 -B verify_original.py | diff -u original_receipt.txt - &&
python3 -B verify_general.py | diff -u general_receipt.txt -
```
Run without Python optimization. A checksum or diff failure is a stop condition. The PDF was compiled twice with pdflatex and all four pages visually inspected. No Lean executable was available in the isolated environment; no Lean proof was claimed. Historical repository head from prior audit: 8ada6fe6715806fabbe43115b7d337f45df99f5a; not refreshed in this task. No local Mac audit or remote modifications.

## Priority statement for author review
The claim is the exact finite-prefix tradeoff for order-invariant maximal-birth processes, not the general causal set hypothesis, classical growth, or the established probabilistic contraction principle. The all-dimension result is a lower bound; attainability is proved here only in dimension four. Relevant literature searches checked titles and abstracts concerning order invariance, continuum limits, finite sprinkled-poset probabilities, and link sampling biases. They do not establish absence of equivalent earlier work.

Before public deposit: review authorship and AI-assistance disclosure, independently scrutinize the geometric moment calculation and theorem statement, compare full texts of cited prior work, and if pursuing the formal-verification gate, verify the exact theorem and audit axioms with the repository toolchain. Once approved, deposit the PDF and source/certificate files as a dated version on Zenodo; cite the version-specific DOI. No DOI is assigned by this dossier. Use arXiv for dissemination subject to its submission requirements. Do not label publication, correctness, independent review or priority as established until the respective evidence exists.
