import importlib.util
import os
from pathlib import Path


MODEL_PATH = Path(
    os.environ.get(
        "MODEL",
        Path(__file__).resolve().parents[1] / "tools/modified_ramjet_finite_trajectory_model.py",
    )
).resolve()

import sys

spec = importlib.util.spec_from_file_location("modified_ramjet_model", MODEL_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)

EngineMode = mod.EngineMode
ModifiedRamjetThrustCurve = mod.ModifiedRamjetThrustCurve
TrajectoryIntegrator = mod.TrajectoryIntegrator
TransitionLaw = mod.TransitionLaw
VacuumRocketModel = mod.VacuumRocketModel
VehicleState = mod.VehicleState
verify_model_status = mod.verify_model_status


def test_rocket_assisted_scramjet_below_ramjet_ignition_produces_positive_rocket_thrust():
    thrust_curve = ModifiedRamjetThrustCurve()
    rocket = VacuumRocketModel(rocket_assist_thrust_N=15_000.0)

    mode = EngineMode.ROCKET_ASSISTED_SCRAMJET
    v = 100.0
    h = 33_000.0

    T_air = thrust_curve.T_air(v, h, mode)
    T_rocket_atm = rocket.T_rocket_atm(mode, True, True)
    T_net = T_air + T_rocket_atm

    assert T_air == 0.0
    assert T_rocket_atm > 0.0
    assert T_net > 0.0


def test_powered_mass_flow_implies_positive_total_thrust_unless_unpowered_coast():
    integrator = TrajectoryIntegrator()
    state = VehicleState(
        v=100.0,
        h=33_000.0,
        fuel=800.0,
        oxidizer=400.0,
        T_wall=350.0,
        mode=EngineMode.ROCKET_ASSISTED_SCRAMJET,
        dry_mass=1_200.0,
    )

    mode = EngineMode.ROCKET_ASSISTED_SCRAMJET
    fuel_dot, ox_dot = integrator.mass_model.mass_flow_rate(mode)

    T_air = integrator.thrust_curve.T_air(state.v, state.h, mode)
    T_rocket_atm = integrator.vacuum_rocket.T_rocket_atm(
        mode=mode,
        has_fuel=state.fuel > 0.0,
        has_oxidizer=state.oxidizer > 0.0,
    )
    T_net = T_air + T_rocket_atm

    assert mode != EngineMode.UNPOWERED_COAST
    assert fuel_dot > 0.0 or ox_dot > 0.0
    assert T_net > 0.0


def test_hybrid_airbreather_rocket_mode_is_reachable():
    law = TransitionLaw()

    mode = law.select_mode(
        v=3_000.0,
        h=33_000.0,
        fuel=800.0,
        oxidizer=400.0,
        T_wall=350.0,
        preferred_mode=EngineMode.SCRAMJET_ATMOSPHERIC,
    )

    assert mode == EngineMode.HYBRID_AIRBREATHER_ROCKET


def test_vacuum_altitude_boundary_forces_vacuum_rocket():
    law = TransitionLaw(vacuum_altitude_m=80_000.0)

    mode = law.select_mode(
        v=3_000.0,
        h=80_000.0,
        fuel=800.0,
        oxidizer=400.0,
        T_wall=350.0,
        preferred_mode=EngineMode.SCRAMJET_ATMOSPHERIC,
    )

    assert mode == EngineMode.VACUUM_ROCKET


def test_air_thrust_does_not_double_count_rocket_assist():
    thrust_curve = ModifiedRamjetThrustCurve()

    v = 2_600.0
    h = 33_000.0

    T_scramjet = thrust_curve.T_air(v, h, EngineMode.SCRAMJET_ATMOSPHERIC)
    T_rocket_assisted = thrust_curve.T_air(v, h, EngineMode.ROCKET_ASSISTED_SCRAMJET)
    T_hybrid = thrust_curve.T_air(v, h, EngineMode.HYBRID_AIRBREATHER_ROCKET)

    assert T_rocket_assisted == T_scramjet
    assert T_hybrid == T_scramjet
    assert T_scramjet <= thrust_curve.peak_thrust_N


def test_reachability_status_is_computational_only():
    status = verify_model_status()

    assert status["status"] == "MATHEMATICAL_MODEL_ONLY_NO_ENGINE_VALIDATION"
    assert "10_REACHABILITY_THEOREM_COMPUTATIONAL_ONLY" in status["objects_implemented"]
    assert "10_reachability_theorem_computational" not in status["objects_implemented"]
