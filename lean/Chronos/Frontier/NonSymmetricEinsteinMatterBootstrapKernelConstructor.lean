import Chronos.Frontier.GravityClosureKernelTarget

namespace Chronos
namespace Frontier

/--
The structure-level constructor for the bootstrap kernel.

This closes only the constructor from explicit supplied fields. It does not
supply the PDE theorem proving that genuine four-dimensional non-symmetric
Einstein-matter data satisfy those fields.
-/
theorem nonSymmetricEinsteinMatterBootstrapKernel_constructor
    {D : FourDimensionalNonSymmetricEinsteinMatterData}
    (h4 : D.spacetimeDimension = 4)
    (hnon : D.nonSymmetricMetric)
    (hfield : D.einsteinMatterSystem)
    (henergy : D.energyConditionPreserved)
    (hcont : D.wellposedContinuation)
    (hgate : D.collapseCriterion) :
    NonSymmetricEinsteinMatterBootstrapKernel D :=
  {
    dimension_four := h4
    nonsymmetric := hnon
    field_system := hfield
    energy_condition := henergy
    continuation := hcont
    collapse_gate := hgate
  }

/--
The previously isolated target is propositionally inhabited once all six
field-level hypotheses are supplied.
-/
theorem gravityClosureKernelTarget_from_supplied_fields :
    GravityClosureKernelTarget := by
  intro D h4 hnon hfield henergy hcont hgate
  exact nonSymmetricEinsteinMatterBootstrapKernel_constructor
    h4 hnon hfield henergy hcont hgate

/--
The collapse gate follows from the supplied-field constructor.
-/
theorem collapseGate_from_supplied_bootstrap_fields
    {D : FourDimensionalNonSymmetricEinsteinMatterData}
    (h4 : D.spacetimeDimension = 4)
    (hnon : D.nonSymmetricMetric)
    (hfield : D.einsteinMatterSystem)
    (henergy : D.energyConditionPreserved)
    (hcont : D.wellposedContinuation)
    (hgate : D.collapseCriterion) :
    D.collapseCriterion :=
  collapseGate_from_bootstrapKernel
    (nonSymmetricEinsteinMatterBootstrapKernel_constructor
      h4 hnon hfield henergy hcont hgate)

end Frontier
end Chronos
