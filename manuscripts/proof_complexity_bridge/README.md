# Proof-Complexity Bridge (Toolkit Pivot)

Status: active (rebuild invariant class)

Goal: replace FO^k-step “depth” (killed by avalanche counterexamples) with a faithful proof-complexity invariant for SAT:
- Resolution width/size (Ben-Sasson–Wigderson)
- CDCL clause-learning lower bounds via resolution
- Information-work phrased as width growth (not entropy per FO^k step)

Deliverables:
1) Formal model: Resolution / k-DNF resolution / bounded-width resolution.
2) Bridge lemma: any algorithm in the target class induces a refutation (or learning trace) with width w(t).
3) Lower bound engine: width lower bound ⇒ size/time lower bound.
4) Instance families: expander/CSP/XOR gadget families with proven width lower bounds.

Files:
- width_size_tradeoff.tex
- cdcl_to_resolution_bridge.tex
- hard_family_width_lower_bound.tex
