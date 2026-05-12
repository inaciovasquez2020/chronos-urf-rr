import Chronos.Frontier.RepositoryNativeIsFiniteRepresentedAtomInstantiation

namespace Chronos

/--
Repository-native zero-arity interface closure.

This uses only zero-arity-restricted fields.
It does not use the inadmissible unrestricted field

  FiniteRegistry r →
  RegistryGenerates r z →
  IsFiniteRepresentedAtom z

without the hypothesis `z.arity = 0`.
-/
theorem carrierRegistryGenerates_of_registryGenerates
    (registryGenerates :
      ∀ z : Carrier, ∃ r : Registry, RegistryGenerates r z) :
    ∀ z : Carrier,
      z.arity = 0 →
      ∃ r : Registry, RegistryGenerates r z := by
  intro z _hz
  exact registryGenerates z


theorem finiteRegistryCarrier_of_finiteRegistry
    (finiteRegistry :
      ∀ r : Registry, FiniteRegistry r) :
    ∀ z : Carrier, ∀ r : Registry,
      z.arity = 0 →
      RegistryGenerates r z →
      FiniteRegistry r := by
  intro _z r _hz _hgen
  exact finiteRegistry r


theorem representedZeroArityOfArityZero_closed
    (representedZeroArityRegistryPair :
      ∀ z : Carrier,
        z.arity = 0 →
        RepresentedZeroArityRegistryPair z) :
    ∀ z : Carrier, ∀ r : Registry,
      z.arity = 0 →
      RegistryGenerates r z →
      RepresentedZeroArityRegistryPair z := by
  intro z _r hz _hgen
  exact representedZeroArityRegistryPair z hz


theorem finiteRepresentedAtomOfFiniteRegistry_closed
    (isFiniteRepresentedAtom :
      ∀ z : Carrier,
        z.arity = 0 →
        RepresentedZeroArityRegistryPair z →
        IsFiniteRepresentedAtom z)
    (representedZeroArityRegistryPair :
      ∀ z : Carrier,
        z.arity = 0 →
        RepresentedZeroArityRegistryPair z) :
    ∀ z : Carrier, ∀ r : Registry,
      z.arity = 0 →
      RegistryGenerates r z →
      FiniteRegistry r →
      IsFiniteRepresentedAtom z := by
  intro z _r hz _hgen _hfin
  exact isFiniteRepresentedAtom z hz (representedZeroArityRegistryPair z hz)


theorem repositoryNativeZeroArityInterface_closed
    (registryGenerates :
      ∀ z : Carrier, ∃ r : Registry, RegistryGenerates r z)
    (finiteRegistry :
      ∀ r : Registry, FiniteRegistry r)
    (representedZeroArityRegistryPair :
      ∀ z : Carrier,
        z.arity = 0 →
        RepresentedZeroArityRegistryPair z)
    (isFiniteRepresentedAtom :
      ∀ z : Carrier,
        z.arity = 0 →
        RepresentedZeroArityRegistryPair z →
        IsFiniteRepresentedAtom z) :
    RepositoryNativeZeroArityInterface :=
by
  exact
    { carrierRegistryGenerates :=
        carrierRegistryGenerates_of_registryGenerates registryGenerates

      finiteRegistryCarrier :=
        finiteRegistryCarrier_of_finiteRegistry finiteRegistry

      representedZeroArityOfArityZero :=
        representedZeroArityOfArityZero_closed representedZeroArityRegistryPair

      finiteRepresentedAtomOfFiniteRegistry :=
        finiteRepresentedAtomOfFiniteRegistry_closed
          isFiniteRepresentedAtom
          representedZeroArityRegistryPair }


theorem repositoryNativeZeroArityInterface_implies_zeroArityCarrierExhaustiveness
    (I : RepositoryNativeZeroArityInterface) :
    ∀ z : Carrier,
      z.arity = 0 →
      RepresentedZeroArityRegistryPair z ∧ IsFiniteRepresentedAtom z := by
  intro z hz
  obtain ⟨r, hgen⟩ := I.carrierRegistryGenerates z hz
  exact
    ⟨ I.representedZeroArityOfArityZero z r hz hgen,
      I.finiteRepresentedAtomOfFiniteRegistry z r hz hgen
        (I.finiteRegistryCarrier z r hz hgen) ⟩


theorem zeroArityCarrierExhaustiveness_closed
    (registryGenerates :
      ∀ z : Carrier, ∃ r : Registry, RegistryGenerates r z)
    (finiteRegistry :
      ∀ r : Registry, FiniteRegistry r)
    (representedZeroArityRegistryPair :
      ∀ z : Carrier,
        z.arity = 0 →
        RepresentedZeroArityRegistryPair z)
    (isFiniteRepresentedAtom :
      ∀ z : Carrier,
        z.arity = 0 →
        RepresentedZeroArityRegistryPair z →
        IsFiniteRepresentedAtom z) :
    ∀ z : Carrier,
      z.arity = 0 →
      RepresentedZeroArityRegistryPair z ∧ IsFiniteRepresentedAtom z := by
  exact
    repositoryNativeZeroArityInterface_implies_zeroArityCarrierExhaustiveness
      (repositoryNativeZeroArityInterface_closed
        registryGenerates
        finiteRegistry
        representedZeroArityRegistryPair
        isFiniteRepresentedAtom)

end Chronos
