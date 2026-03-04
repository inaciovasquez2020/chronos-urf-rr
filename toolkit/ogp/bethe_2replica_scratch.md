# bethe_2replica_scratch.md
# Two-Replica Bethe Functional for Hard-Core (Independent Set) Overlap Curvature
# Status: Differentiation Target (Frozen)

---

# 0. Scope

Define the explicit objects whose second derivative in the overlap direction yields the curvature constant

κ_Bethe(ρ,Δ) = −ψ''(ν₂)

where

ψ(q) = (1/n) log |Ω(q)|

and Ω(q) denotes pairs of independent sets with overlap q.

No claims beyond algebraic setup.

---

# 1. Base Model (Single Replica)

Graph: Δ-regular or locally tree-like with degree Δ.

Independent sets

Ω = { σ ∈ {0,1}^V : ∀(i,j)∈E, σ_i σ_j = 0 }

Hard-core weight

μ(σ) = (1/Z) λ^{Σ_i σ_i}

Partition function

Z = Σ_{σ∈Ω} λ^{|σ|}

Cavity fixed point (RS)

Let u denote the cavity occupied probability.

u = λ (1−u)^(Δ−1) / (1 + λ (1−u)^(Δ−1))

---

# 2. Two-Replica Configuration Space

Two configurations

σ¹, σ² ∈ Ω

Local joint state at vertex i

x_i = (σ_i¹, σ_i²) ∈ {00,01,10,11}

Joint state weights

w(00) = 1  
w(01) = λ  
w(10) = λ  
w(11) = λ²

Overlap

q = (1/n) Σ_i σ_i¹ σ_i²

---

# 3. Edge Compatibility Constraint

Hard-core constraint applies independently to both replicas.

Allowed pairs (a,b),(c,d) satisfy

ac = 0  
bd = 0

Compatibility indicator

I_allowed((a,b),(c,d)) = 1_{ac=0} * 1_{bd=0}

---

# 4. Iteration A — Microcanonical Bethe Functional

Joint probabilities

p00  
p01  
p10  
p11

Constraints

p00 + p01 + p10 + p11 = 1

ρ = p10 + p11 = p01 + p11

q = p11

Vertex entropy

H = − Σ p_ab log p_ab

Weight contribution

W = (p01 + p10 + 2 p11) log λ

Edge penalty (proxy form)

E = log(1 − p11²)

Bethe functional

Φ₂(q) = H + W + (Δ/2) E

Curvature target

κ_Bethe(q) = − d²Φ₂ / dq²

---

# 5. Iteration B — Canonical Overlap Coupling

Introduce overlap field η.

Partition function

Z₂(η) = Σ_{σ¹,σ²∈Ω} λ^{|σ¹|+|σ²|} exp(η Σ_i σ_i¹ σ_i²)

Free energy

φ₂(η) = (1/n) log Z₂(η)

Overlap expectation

q(η) = dφ₂ / dη

Curvature relation

d²φ₂ / dη² = dq / dη

Legendre dual

ψ(q) = φ₂(η) − η q

Curvature

κ_Bethe(q) = 1 / φ₂''(η(q))

---

# 6. Iteration C — 4-State Cavity Recursion

Messages

m = (m00,m01,m10,m11)

Weights

w(00)=1  
w(01)=λ  
w(10)=λ  
w(11)=λ² e^η

Compatibility matrix

Allowed if

ac = 0  
bd = 0

Recursion

m_x ∝ w(x) * ( Σ_y m_y I_allowed(x,y) )^(Δ−1)

Normalization

Σ_x m_x = 1

Vertex normalization

Z_v = Σ_x w(x) ( Σ_y m_y I_allowed(x,y) )^Δ

Edge normalization

Z_e = Σ_{x,y} m_x m_y I_allowed(x,y)

Bethe free energy

φ₂(η) = log Z_v − (Δ/2) log Z_e

---

# 7. Iteration D — Linear Response

Define recursion operator

T(m)

Jacobian

J = D T(m)

RS stability condition

spectral_radius(J) < 1

Overlap susceptibility

χ_ov = dq / dη

Linear response

dq/dη = ⟨u , (I − J)^{-1} v⟩

Curvature

κ_Bethe = 1 / χ_ov

---

# 8. Iteration E — Large-Δ Asymptotic Calibration

Scaling regime

λ = Θ(1/Δ)

Typical density

ρ ≈ (log Δ) / Δ

Overlap expansion

Φ₂(q) ≈ Φ₂(q*) + (1/2) κ_Bethe (q − q*)²

Expected scale

κ_Bethe = Θ(Δ)

Used only for sanity calibration.

---

# 9. LIB Interface

Barrier functional

B(A) = − log Φ(A)

Conductance

Φ(A) = Q(A,Aᶜ) / π(A)

Mixing bound

t_mix ≥ exp(c κ_Bethe n)

c depends on spectral-gap reduction.

Regularization convention

Φ(A) → max(Φ(A), ε)

to avoid divergence near bottlenecks.

---

# 10. Closure Target

To close the hinge:

1) solve the cavity fixed point m  
2) compute φ₂(η)  
3) compute dq/dη  
4) invert to obtain κ_Bethe

κ_Bethe feeds directly into the LIB spectral-gap barrier constant.
