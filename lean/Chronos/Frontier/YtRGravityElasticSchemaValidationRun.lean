import Chronos.Frontier.AuthenticYtRGravityElasticDatasetPayloadBinding

namespace Chronos
namespace Frontier

structure YtRGravityElasticSchemaValidationRun where
  binding : AuthenticYtRGravityElasticDatasetPayloadBinding
  schemaDeclared : Bool
  requiredFieldsPresent : Bool
  unitsValidated : Bool
  finiteRowsValidated : Bool
  missingnessPolicyRecorded : Bool
deriving Repr, DecidableEq

def YtRGravityElasticSchemaValidationRun.completed
    (r : YtRGravityElasticSchemaValidationRun) : Prop :=
  r.binding.completed ∧
  r.schemaDeclared = true ∧
  r.requiredFieldsPresent = true ∧
  r.unitsValidated = true ∧
  r.finiteRowsValidated = true ∧
  r.missingnessPolicyRecorded = true

theorem ytr_gravity_elastic_schema_validation_run_closed
    (r : YtRGravityElasticSchemaValidationRun)
    (h_binding : r.binding.completed)
    (h_schema : r.schemaDeclared = true)
    (h_fields : r.requiredFieldsPresent = true)
    (h_units : r.unitsValidated = true)
    (h_finite : r.finiteRowsValidated = true)
    (h_missing : r.missingnessPolicyRecorded = true) :
    r.completed := by
  simp [
    YtRGravityElasticSchemaValidationRun.completed,
    h_binding,
    h_schema,
    h_fields,
    h_units,
    h_finite,
    h_missing
  ]

end Frontier
end Chronos
