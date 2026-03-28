import Mathlib.Data.Finset.Basic

-- Finite state space of EF-types
structure State where
  id : ℕ

-- Transition function
constant step : State → State

-- Finite set of states (axiomatized)
constant S : Finset State

-- Axiom: pigeonhole repetition
axiom exists_repeat :
  ∀ (s₀ : State), ∃ i j, i < j ∧ (Nat.iterate step i s₀) = (Nat.iterate step j s₀)
