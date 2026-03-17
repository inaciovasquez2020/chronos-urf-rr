# Reflection Positivity Transfer Operator and Partition Function Bound

## RP Transfer Operator and Spectral Radius

Let the Wilson U(1) action on a toroidal lattice be decomposed across a reflection plane Π

S_B(θ) = S⁺(θ⁺) + S⁻(θ⁻) + S^Π(θ⁺,θ⁻)

For each crossing plaquette the Fourier–Bessel expansion gives

e^{β cos(θ_{e⁺}-θ_{e⁻})}
= e^{-β} ∑_{n∈ℤ} I_n(β) e^{i n θ_{e⁺}} e^{-i n θ_{e⁻}}

Integrating the Λ⁻ variables produces a boundary quadratic form

⟨F · ϑG⟩
= ∫ F(θ⁺) ȳG(θ̃⁺) K(θ⁺,θ̃⁺) dθ⁺ dθ̃⁺

where

K(θ⁺,θ̃⁺)
= ∏_{e∈E_Π} ∑_{n∈ℤ} I_n(β) e^{i n (θ_{e⁺}-θ̃_{e⁺})}

Thus the RP transfer operator factorizes

K = ⊗_{e∈E_Π} K_e

with single-link kernel

K_e(α,α̃)
= ∑_{n∈ℤ} I_n(β) e^{i n (α-α̃)}.

---

## Fourier Diagonalization

For the Fourier basis

e_m(α) = e^{i m α}

we compute

K_e e_m = I_m(β) e_m.

Thus

σ(K_e) = { I_m(β) : m ∈ ℤ }.

Since I_{-m} = I_m and I_m(β) ≥ 0,

‖K_e‖ = sup_m I_m(β) = I_0(β).

---

## Tensor Product Spectrum

For the full operator

K = ⊗_{e∈E_Π} K_e

the eigenfunctions are

∏_{e∈E_Π} e^{i m_e α_e}

with eigenvalues

∏_{e∈E_Π} I_{m_e}(β).

Therefore

‖K‖ = I_0(β)^{|E_Π|}.

---

## Partition Function Bound

Let

f(φ) = e^{β' cos φ}.

The tiled observable is

F = ∏_{p∈P_B} f(φ_p).

The chessboard iteration expresses

⟨F⟩ = ⟨ψ , K^{|P_B|} ψ⟩

for the normalized boundary vector ψ.

Using operator norm submultiplicativity,

|⟨ψ , K^{|P_B|} ψ⟩|
≤ ‖K‖^{|P_B|}.

Since

‖K‖ = I_0(β'),

we obtain

Z_B(β') = ⟨ ∏_p e^{β' cos φ_p} ⟩
≤ I_0(β')^{|P_B|}.

Multiplying by e^{-β'|P_B|} gives

Z_B(β') ≤ (e^{-β'} I_0(β'))^{|P_B|}.

This completes the partition-function subadditivity bound.
