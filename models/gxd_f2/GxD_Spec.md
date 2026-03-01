GxD — Global × Detectability (Key-to-Keyhole Functional)

Data:
- H finitely generated group with symmetric generating set S and word length ℓ.
- Action H ↷ 𝒮 on a configuration space 𝒮.
- Finite observer family {O_θ : 𝒮 → V_θ}_{θ∈Θ}, with dim(V_θ) ≤ C < ∞.

Definition (observable codebook at radius R):
- Fix θ (or a finite tuple of observers), define
  Code_θ(s;R) := { O_θ(h⋅s) : h ∈ H, ℓ(h) ≤ R }.

Definition (GxD rate):
- For a fixed observer θ:
  GxD_θ(s) := limsup_{R→∞} (1/R) log |Code_θ(s;R)|.

- For an observer family Θ:
  GxD_Θ(s) := sup_{θ∈Θ} GxD_θ(s).

Interpretation:
- GxD_Θ(s) measures the exponential rate at which distinct observable outputs appear as the orbit radius grows.

Auxiliary notions:
- Orbit growth exponent (group entropy wrt S):
  κ(H,S) := limsup_{R→∞} (1/R) log |B_R|, where B_R := {h : ℓ(h) ≤ R}.

- Collision multiplicity at radius R:
  Col_θ(s;R) := max_y |{ h ∈ B_R : O_θ(h⋅s) = y }|.

Theorems (toolkit closure statements):

T1 (Trivial bounds):
- For all θ,s:
  0 ≤ GxD_θ(s) ≤ κ(H,S).

T2 (Finite-collision lower bound):
Assume there exist constants A ≥ 1 and d ≥ 0 such that for all R,
  Col_θ(s;R) ≤ A R^d.
Then
  GxD_θ(s) = κ(H,S).

T3 (Exponential-collision correction):
Assume there exists δ ≥ 0 such that
  limsup_{R→∞} (1/R) log Col_θ(s;R) ≤ δ.
Then
  GxD_θ(s) ≥ κ(H,S) - δ.

T4 (Monotonicity under refinement):
If observer O' refines O (i.e., there exists map π with O = π ∘ O'),
then for all s:
  GxD_O(s) ≤ GxD_O'(s).

T5 (Orbit invariance):
For any g ∈ H:
  GxD_θ(g⋅s) = GxD_θ(s).

Concrete F2 instance (ties to Rflect-F2 model):
- H = F2 with S={a,a^-1,b,b^-1}.
- κ(H,S) = log 3.
- Any θ with polynomial collision bound implies GxD_θ(s)=log 3.
