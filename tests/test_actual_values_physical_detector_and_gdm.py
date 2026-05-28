from pathlib import Path

PHYSICAL = Path("lean/Chronos/Frontier/PhysicalDetectorFieldExtractionMap.lean")
GDM = Path("lean/Chronos/Frontier/GDMEmpiricalMassMapBindingTheorem.lean")

def test_physical_detector_actual_value_theorems_exist():
    text = PHYSICAL.read_text()
    for token in [
        "empty_detector_field_actual_values",
        "one_detector_field_actual_values",
        "finite_detector_field_actual_values",
        "extractedActiveMass finiteDetectorFieldWitness = 18",
        "fieldSamples := [2, 5, 11]",
    ]:
        assert token in text

def test_gdm_actual_value_theorems_exist():
    text = GDM.read_text()
    for token in [
        "equal_mass_actual_values",
        "positive_residual_actual_values",
        "exact_binding_actual_values",
        "empiricalResidualMass positiveResidualActualWitness = 15",
        "boundApparentMass exactBindingActualWitness = exactBindingActualWitness.apparentMass",
    ]:
        assert token in text
