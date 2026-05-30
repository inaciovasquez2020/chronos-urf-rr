"""
ModifiedRamjetFiniteTrajectoryModel
Status: MATHEMATICAL_MODEL_ONLY_NO_ENGINE_VALIDATION

Implements all 10 missing mathematical objects identified in the status report.
No empirical engine validation. No wind-tunnel validation. No flight-test validation.
No thermal survivability proof. No orbital capability claim.
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from enum import Enum, auto

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
g0        = 9.80665         # m/s²
R_air     = 287.05          # J/(kg·K)

# ISA atmosphere coefficients (troposphere + stratosphere + mesosphere proxy)
_ATM_LAYERS = [
    # (h_base_m, T_base_K, lapse_K_per_m, P_base_Pa)
    (0.0,      288.15, -0.0065,  101_325.0),
    (11_000.0, 216.65,  0.0,      22_632.1),
    (20_000.0, 216.65,  0.001,     5_474.89),
    (32_000.0, 228.65,  0.0028,    868.019),
    (47_000.0, 270.65,  0.0,       110.906),
    (51_000.0, 270.65, -0.0028,     66.9389),
    (71_000.0, 214.65, -0.002,       3.95642),
    (86_000.0, 186.87,  0.0,         0.3734),   # proxy ceiling
]

# ---------------------------------------------------------------------------
# OBJECT 2 — Atmosphere model  ρ(h), T(h), P(h)
# ---------------------------------------------------------------------------
def atmosphere(h: float) -> tuple[float, float, float]:
    """
    Standard atmosphere model.
    Returns (density_kg_m3, temperature_K, pressure_Pa).
    Properties:
      ρ(h) ≥ 0
      ρ(h) decreases with altitude
      ρ(h) ≈ 0 above 86 km ceiling
    """
    h = max(0.0, h)
    if h >= 86_000.0:
        return 0.0, 186.87, 0.0

    h_b, T_b, lapse, P_b = _ATM_LAYERS[0]
    for layer in _ATM_LAYERS[1:]:
        if h < layer[0]:
            break
        h_b, T_b, lapse, P_b = layer

    dh = h - h_b
    if abs(lapse) < 1e-12:
        T   = T_b
        P   = P_b * math.exp(-g0 * dh / (R_air * T_b))
    else:
        T   = T_b + lapse * dh
        P   = P_b * (T / T_b) ** (-g0 / (lapse * R_air))

    rho = P / (R_air * T)
    return max(rho, 0.0), T, max(P, 0.0)


# ---------------------------------------------------------------------------
# Engine mode enum
# ---------------------------------------------------------------------------
class EngineMode(Enum):
    RAMJET_ATMOSPHERIC         = auto()
    SCRAMJET_ATMOSPHERIC       = auto()
    ROCKET_ASSISTED_SCRAMJET   = auto()
    HYBRID_AIRBREATHER_ROCKET  = auto()
    VACUUM_ROCKET              = auto()
    UNPOWERED_COAST            = auto()


# ---------------------------------------------------------------------------
# OBJECT 7 — Mode-transition law
# ---------------------------------------------------------------------------
@dataclass
class TransitionLaw:
    ramjet_ignition_speed_ms:   float = 500.0     # ~Mach 1.5 at SL
    scramjet_min_speed_ms:      float = 1_500.0   # ~Mach 5
    rocket_assist_speed_ms:     float = 2_500.0   # supplemental rocket kicks in
    vacuum_altitude_m:          float = 80_000.0  # effective vacuum threshold
    T_max_K:                    float = 2_300.0   # thermal limit

    def select_mode(
        self,
        v: float,
        h: float,
        fuel: float,
        oxidizer: float,
        T_wall: float,
        preferred_mode: EngineMode,
    ) -> EngineMode:
        """
        Deterministic mode selector.
        mode(t) is uniquely determined by vehicle state.
        Invariant: ramjet/scramjet → INACTIVE if h ≥ vacuum_altitude_m
        or ρ(h)≈0.
        """
        rho, _, _ = atmosphere(h)
        atmospheric = (h < self.vacuum_altitude_m) and (rho > 1e-6)
        has_fuel    = fuel > 0.0
        has_ox      = oxidizer > 0.0
        thermal_ok  = T_wall <= self.T_max_K

        if not thermal_ok:
            return EngineMode.UNPOWERED_COAST   # trajectory invalid if wall melts

        if not has_fuel:
            return EngineMode.UNPOWERED_COAST

        # Vacuum: only rocket possible
        if not atmospheric:
            if has_ox:
                return EngineMode.VACUUM_ROCKET
            return EngineMode.UNPOWERED_COAST

        # Atmospheric branches
        if v < self.ramjet_ignition_speed_ms:
            # Below ignition speed — no airbreathing; use rocket assist if available
            if has_ox:
                return EngineMode.ROCKET_ASSISTED_SCRAMJET
            return EngineMode.UNPOWERED_COAST

        if v < self.scramjet_min_speed_ms:
            return EngineMode.RAMJET_ATMOSPHERIC

        if v < self.rocket_assist_speed_ms:
            return EngineMode.SCRAMJET_ATMOSPHERIC

        # High-speed: hybrid airbreather + rocket mode
        if has_ox:
            return EngineMode.HYBRID_AIRBREATHER_ROCKET
        return EngineMode.SCRAMJET_ATMOSPHERIC


# ---------------------------------------------------------------------------
# OBJECT 1 — Modified Ramjet Thrust Curve
# T_air(v, h, mode)
# ---------------------------------------------------------------------------
@dataclass
class ModifiedRamjetThrustCurve:
    """
    Weakest sufficient model: T_air bounded, nonneg, atmospheric-only, mode-compatible.
    T_air(v, h, mode) ≥ 0
    T_air(v, h, mode) = 0  if ρ(h) = 0
    T_air(v, h, mode) = 0  below ignition speed
    T_air(v, h, mode) ≤ peak_thrust_N
    """
    peak_thrust_N:           float = 50_000.0
    peak_efficiency_mach:    float = 8.0
    ramjet_ignition_speed:   float = 500.0
    speed_of_sound_ref:      float = 295.0    # ~SL at altitude

    def T_air(self, v: float, h: float, mode: EngineMode) -> float:
        rho, _, _ = atmosphere(h)
        if rho < 1e-9:
            return 0.0
        if v < self.ramjet_ignition_speed:
            return 0.0
        if mode in (EngineMode.VACUUM_ROCKET, EngineMode.UNPOWERED_COAST):
            return 0.0

        # Mach-dependent efficiency: Gaussian peak around peak_efficiency_mach
        mach = v / self.speed_of_sound_ref
        efficiency = math.exp(-0.5 * ((mach - self.peak_efficiency_mach) / 3.0) ** 2)

        # Density ratio relative to sea-level
        rho_sl, _, _ = atmosphere(0.0)
        density_ratio = rho / rho_sl

        base_thrust = self.peak_thrust_N * efficiency * math.sqrt(density_ratio)

        return max(0.0, min(base_thrust, self.peak_thrust_N))


# ---------------------------------------------------------------------------
# OBJECT 8 — Vacuum rocket propulsion model
# Tsiolkovsky + finite-burn thrust
# ---------------------------------------------------------------------------
@dataclass
class VacuumRocketModel:
    """
    T_vacuum(t), I_sp, exhaust_velocity.
    Δv = v_e · ln(m_initial / m_final)   [Tsiolkovsky]
    """
    I_sp_s:                float = 450.0          # specific impulse (s), LOX/LH2-class
    vacuum_thrust_N:       float = 20_000.0       # continuous vacuum thrust
    rocket_assist_thrust_N: float = 15_000.0

    @property
    def exhaust_velocity(self) -> float:
        """v_e = I_sp · g0"""
        return self.I_sp_s * g0

    def delta_v_tsiolkovsky(self, m_initial: float, m_final: float) -> float:
        """Ideal Δv for a rocket burn."""
        if m_final <= 0 or m_initial <= m_final:
            return 0.0
        return self.exhaust_velocity * math.log(m_initial / m_final)

    def T_vacuum(self, has_oxidizer: bool, has_fuel: bool) -> float:
        if has_oxidizer and has_fuel:
            return self.vacuum_thrust_N
        return 0.0

    def T_rocket_atm(
        self,
        mode: EngineMode,
        has_fuel: bool,
        has_oxidizer: bool,
    ) -> float:
        """
        Atmospheric rocket-assist thrust.

        Invariant target:
          mode burns oxidizer in atmosphere ⇒ rocket-assist thrust > 0
        """
        if not (has_fuel and has_oxidizer):
            return 0.0
        if mode == EngineMode.ROCKET_ASSISTED_SCRAMJET:
            return self.rocket_assist_thrust_N
        if mode == EngineMode.HYBRID_AIRBREATHER_ROCKET:
            return self.rocket_assist_thrust_N
        return 0.0


# ---------------------------------------------------------------------------
# OBJECT 3 — Drag model
# D(v, h) = ½ ρ v² C_D A
# ---------------------------------------------------------------------------
@dataclass
class DragModel:
    """
    D(v,h) ≥ 0
    D(v,h) grows at least quadratically in high-density hypersonic flight.
    """
    reference_area_m2: float = 2.0
    C_D_subsonic:      float = 0.25
    C_D_transonic:     float = 0.50
    C_D_supersonic:    float = 0.30
    C_D_hypersonic:    float = 0.20

    def C_D(self, v: float, h: float) -> float:
        # More accurate: a ≈ sqrt(gamma * R * T)
        _, T, _ = atmosphere(h)
        a = math.sqrt(1.4 * R_air * max(T, 100.0))
        mach = v / a
        if mach < 0.8:
            return self.C_D_subsonic
        if mach < 1.2:
            # transonic spike
            return self.C_D_subsonic + (self.C_D_transonic - self.C_D_subsonic) * (mach - 0.8) / 0.4
        if mach < 5.0:
            # supersonic decay
            return self.C_D_supersonic + (self.C_D_transonic - self.C_D_supersonic) * math.exp(-(mach - 1.2) / 2.0)
        # hypersonic
        return self.C_D_hypersonic

    def drag(self, v: float, h: float) -> float:
        rho, _, _ = atmosphere(h)
        return 0.5 * rho * v**2 * self.C_D(v, h) * self.reference_area_m2


# ---------------------------------------------------------------------------
# OBJECT 6 — Thermal survival inequality
# T_wall(v, h, t) ≤ T_max
# ---------------------------------------------------------------------------
@dataclass
class ThermalModel:
    """
    Stagnation heating proxy: q_dot = k · sqrt(ρ) · v³
    Integrated wall temperature via simple RC thermal model.
    Invariant: T_wall(t) ≤ T_max for valid trajectory.
    """
    k_heating:       float = 1.83e-4    # empirical Sutton-Graves constant proxy
    thermal_mass:    float = 5_000.0    # J/K — vehicle wall heat capacity
    radiative_coeff: float = 50.0       # W/K — approximation
    ambient_K:       float = 250.0      # reference sink temperature

    def heat_flux(self, v: float, h: float) -> float:
        """q_dot = k · sqrt(ρ(h)) · v³  [W/m²]"""
        rho, _, _ = atmosphere(h)
        return self.k_heating * math.sqrt(rho) * v**3

    def d_T_wall_dt(self, v: float, h: float, T_wall: float) -> float:
        """
        dT_wall/dt = (q_dot · A_ref - Q_radiated) / C_th
        """
        q_in  = self.heat_flux(v, h)
        q_out = self.radiative_coeff * (T_wall - self.ambient_K)
        return (q_in - q_out) / self.thermal_mass

    def is_thermally_valid(self, T_wall: float, T_max: float) -> bool:
        return T_wall <= T_max


# ---------------------------------------------------------------------------
# OBJECT 5 — Mass depletion
# ---------------------------------------------------------------------------
@dataclass
class MassModel:
    """
    m(t) = dry_mass + fuel_mass(t) + oxidizer_mass(t)
    Invariant: m(t) > 0 on valid trajectory.
    """
    dry_mass_kg:      float = 1_200.0
    fuel_mass_kg:     float = 800.0
    oxidizer_mass_kg: float = 400.0

    # flow rates
    fuel_flow_atm_kg_s:  float = 3.0    # airbreathing mode
    fuel_flow_vac_kg_s:  float = 2.0    # vacuum rocket fuel flow
    oxidizer_flow_kg_s:  float = 4.0    # rocket oxidizer flow

    @property
    def total_mass(self) -> float:
        return self.dry_mass_kg + self.fuel_mass_kg + self.oxidizer_mass_kg

    def mass_flow_rate(self, mode: EngineMode) -> tuple[float, float]:
        """Returns (fuel_flow, oxidizer_flow) in kg/s for current mode."""
        if mode == EngineMode.UNPOWERED_COAST:
            return 0.0, 0.0
        if mode in (EngineMode.RAMJET_ATMOSPHERIC, EngineMode.SCRAMJET_ATMOSPHERIC):
            return self.fuel_flow_atm_kg_s, 0.0
        if mode == EngineMode.ROCKET_ASSISTED_SCRAMJET:
            return self.fuel_flow_atm_kg_s, self.oxidizer_flow_kg_s * 0.3
        if mode == EngineMode.HYBRID_AIRBREATHER_ROCKET:
            return self.fuel_flow_atm_kg_s, self.oxidizer_flow_kg_s * 0.5
        if mode == EngineMode.VACUUM_ROCKET:
            return self.fuel_flow_vac_kg_s, self.oxidizer_flow_kg_s
        return 0.0, 0.0


# ---------------------------------------------------------------------------
# OBJECT 4 — Equation of motion (acceleration)
# dv/dt = (T - D) / m
# ---------------------------------------------------------------------------
def acceleration(
    thrust_N: float,
    drag_N:   float,
    mass_kg:  float,
    gravity_component: float = 0.0,
) -> float:
    """
    dv/dt = (T(v,h,mode) - D(v,h) - gravity_loss) / m(t)
    Requires mass > 0.
    """
    assert mass_kg > 0.0, "mass must be positive"
    return (thrust_N - drag_N - gravity_component) / mass_kg


# ---------------------------------------------------------------------------
# OBJECT 1 (state) — Vehicle state container
# ---------------------------------------------------------------------------
@dataclass
class VehicleState:
    """
    State(t) = { v(t), h(t), m(t), fuel(t), oxidizer(t), T_wall(t), mode(t) }
    """
    v:         float = 0.0        # speed m/s
    h:         float = 33_000.0   # altitude m
    fuel:      float = 800.0      # kg
    oxidizer:  float = 400.0      # kg
    T_wall:    float = 293.0      # K
    mode:      EngineMode = EngineMode.RAMJET_ATMOSPHERIC
    time:      float = 0.0        # s
    dry_mass:  float = 1_200.0    # kg

    @property
    def mass(self) -> float:
        return self.dry_mass + self.fuel + self.oxidizer

    def is_valid(self, T_max: float) -> bool:
        return (
            self.mass > self.dry_mass       # has propellant
            and self.fuel >= 0.0
            and self.oxidizer >= 0.0
            and self.T_wall <= T_max
            and self.v >= 0.0
        )


# ---------------------------------------------------------------------------
# OBJECT 9 — Top-speed definition
# ---------------------------------------------------------------------------
@dataclass
class TopSpeedResult:
    """
    Precise top-speed definitions (replaces 'undefined; possibly very large').
    All are computed over a finite valid trajectory satisfying all constraints.
    """
    atmospheric_peak_speed_ms:  float = 0.0   # max v before thermal fail / drag eq.
    post_burn_coast_speed_ms:   float = 0.0   # v at burnout
    trajectory_valid:           bool  = True
    termination_reason:         str   = ""
    max_mach:                   float = 0.0

    def report(self) -> str:
        lines = [
            "=== TopSpeedResult ===",
            f"  atmospheric_peak_speed : {self.atmospheric_peak_speed_ms:,.1f} m/s"
            f"  ({self.atmospheric_peak_speed_ms/340:.2f} Mach approx SL)",
            f"  post_burn_coast_speed  : {self.post_burn_coast_speed_ms:,.1f} m/s",
            f"  max_mach_achieved      : {self.max_mach:.2f}",
            f"  trajectory_valid       : {self.trajectory_valid}",
            f"  termination_reason     : {self.termination_reason}",
        ]
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# OBJECT 10 — Computational finite-trajectory reachability certificate
#
# Certificate:
#   Given bounded thrust, positive dry mass, finite fuel,
#   nonneg drag, thermal threshold, and valid transition law,
#   the explicit finite Euler run returns a finite sampled max speed.
#
# Computation strategy: explicit Euler integration with invariant checks.
# The loop terminates because:
#   (a) fuel is finite and strictly decreasing while powered
#   (b) thermal failure is a hard stop
#   (c) time is bounded by t_max
#   Therefore the sampled trajectory is finite, and max(history.v) exists.
#   This is not a formal continuous-time theorem.
# ---------------------------------------------------------------------------

@dataclass
class TrajectoryIntegrator:
    """
    Finite trajectory integrator.
    Implements the minimal math package:
      1. State(t) evolution
      2. Force computation
      3. ValidTrajectory invariants
      4. ComputableTopSpeed
    """
    thrust_curve:   ModifiedRamjetThrustCurve = field(default_factory=ModifiedRamjetThrustCurve)
    vacuum_rocket:  VacuumRocketModel         = field(default_factory=VacuumRocketModel)
    drag_model:     DragModel                 = field(default_factory=DragModel)
    thermal_model:  ThermalModel              = field(default_factory=ThermalModel)
    mass_model:     MassModel                 = field(default_factory=MassModel)
    transition_law: TransitionLaw             = field(default_factory=TransitionLaw)
    dt:             float                     = 0.5     # integration timestep (s)
    t_max:          float                     = 600.0   # maximum flight time (s)

    def run(self, initial: VehicleState, verbose: bool = False) -> tuple[TopSpeedResult, list[dict]]:
        """
        Integrate trajectory. Returns (TopSpeedResult, history).
        Terminates when: fuel exhausted, thermal limit exceeded, or t_max reached.
        """
        state   = VehicleState(**initial.__dict__)
        history = []
        result  = TopSpeedResult()
        peak_v  = 0.0

        for step in range(int(self.t_max / self.dt)):
            t = step * self.dt

            # ---- mode selection ----
            mode = self.transition_law.select_mode(
                v=state.v, h=state.h,
                fuel=state.fuel, oxidizer=state.oxidizer,
                T_wall=state.T_wall,
                preferred_mode=state.mode,
            )
            state.mode = mode

            # ---- ValidTrajectory check ----
            if not state.is_valid(self.transition_law.T_max_K):
                result.trajectory_valid  = False
                result.termination_reason = (
                    f"invalid_state at t={t:.1f}s "
                    f"(fuel={state.fuel:.1f} ox={state.oxidizer:.1f} "
                    f"T_wall={state.T_wall:.0f}K)"
                )
                break

            # ---- thrust ----
            has_fuel = state.fuel > 0.0
            has_oxidizer = state.oxidizer > 0.0

            T_air = self.thrust_curve.T_air(state.v, state.h, mode)
            T_rocket_atm = self.vacuum_rocket.T_rocket_atm(
                mode=mode,
                has_fuel=has_fuel,
                has_oxidizer=has_oxidizer,
            )
            T_vac = (
                self.vacuum_rocket.T_vacuum(has_oxidizer, has_fuel)
                if mode == EngineMode.VACUUM_ROCKET
                else 0.0
            )
            T_net = T_air + T_rocket_atm + T_vac

            fuel_dot, ox_dot = self.mass_model.mass_flow_rate(mode)
            if mode != EngineMode.UNPOWERED_COAST and (fuel_dot > 0.0 or ox_dot > 0.0):
                assert T_net > 0.0, (
                    "thrust/mass-flow incoherence: powered mode consumes propellant "
                    "without positive total thrust"
                )

            # ---- drag ----
            D = self.drag_model.drag(state.v, state.h)

            # ---- gravity component (simplified: horizontal flight) ----
            # For purely horizontal cruise: gravity loss ≈ 0 in v equation
            grav = 0.0

            # ---- acceleration → velocity update ----
            a     = acceleration(T_net, D, state.mass, grav)
            dv    = a * self.dt
            state.v = max(0.0, state.v + dv)

            # ---- mass depletion ----
            state.fuel      = max(0.0, state.fuel    - fuel_dot * self.dt)
            state.oxidizer   = max(0.0, state.oxidizer - ox_dot  * self.dt)

            # ---- thermal update ----
            dT = self.thermal_model.d_T_wall_dt(state.v, state.h, state.T_wall)
            state.T_wall = state.T_wall + dT * self.dt

            # ---- peak tracking ----
            if state.v > peak_v:
                peak_v = state.v
                result.atmospheric_peak_speed_ms = peak_v

            state.time = t

            if verbose and step % 20 == 0:
                rho, _, _ = atmosphere(state.h)
                a_sound   = math.sqrt(1.4 * R_air * max(atmosphere(state.h)[1], 1.0))
                mach      = state.v / a_sound
                print(
                    f"t={t:6.1f}s  v={state.v:8.1f}m/s  Mach={mach:5.2f}  "
                    f"T_wall={state.T_wall:6.0f}K  mode={mode.name:30s}  "
                    f"fuel={state.fuel:6.1f}kg  T={T_net:8.1f}N  D={D:8.1f}N"
                )

            history.append({
                "t": t, "v": state.v, "h": state.h,
                "T_wall": state.T_wall, "fuel": state.fuel,
                "oxidizer": state.oxidizer, "thrust": T_net, "drag": D,
                "mode": mode.name,
            })

            # ---- fuel exhaustion termination ----
            if state.fuel <= 0 and state.oxidizer <= 0:
                result.termination_reason    = f"propellant_exhausted at t={t:.1f}s"
                result.post_burn_coast_speed_ms = state.v
                break

        else:
            result.termination_reason    = f"t_max={self.t_max}s reached"
            result.post_burn_coast_speed_ms = state.v

        # Final Mach
        _, T_amb, _ = atmosphere(initial.h)
        a_sound = math.sqrt(1.4 * R_air * max(T_amb, 1.0))
        result.max_mach = result.atmospheric_peak_speed_ms / a_sound

        return result, history


# ---------------------------------------------------------------------------
# Script-level fix: Path(__file__)  (not Path(file))
# ---------------------------------------------------------------------------
def verify_model_status():
    """
    Repo-packaging self-check. Confirms model status and boundary locks.
    """
    from pathlib import Path
    this_file = Path(__file__)

    status = {
        "model_name"  : "ModifiedRamjetFiniteTrajectoryModel",
        "status"      : "MATHEMATICAL_MODEL_ONLY_NO_ENGINE_VALIDATION",
        "source_file" : str(this_file),
        "boundary_locks": [
            "no_empirical_engine_validation",
            "no_wind_tunnel_validation",
            "no_flight_test_validation",
            "no_thermal_survivability_proof",
            "no_orbital_capability_claim",
            "no_vacuum_ramjet_operation_claim",
            "no_new_propulsion_physics_claim",
        ],
        "objects_implemented": [
            "1_modified_ramjet_thrust_curve",
            "2_atmosphere_model",
            "3_drag_model",
            "4_acceleration_equation",
            "5_mass_depletion",
            "6_thermal_survival_inequality",
            "7_mode_transition_law",
            "8_vacuum_rocket_propulsion",
            "9_top_speed_definition",
            "10_REACHABILITY_THEOREM_COMPUTATIONAL_ONLY",
        ],
    }
    return status


# ---------------------------------------------------------------------------
# Entry point — demonstration run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 70)
    print("ModifiedRamjetFiniteTrajectoryModel")
    print("Status: MATHEMATICAL_MODEL_ONLY_NO_ENGINE_VALIDATION")
    print("=" * 70)

    import json
    status = verify_model_status()
    print("\n--- Model Status ---")
    print(json.dumps(status, indent=2))

    # Build integrator with proxy defaults
    integrator = TrajectoryIntegrator(
        dt=1.0,
        t_max=500.0,
    )
    integrator.mass_model = MassModel(
        dry_mass_kg=1_200.0,
        fuel_mass_kg=800.0,
        oxidizer_mass_kg=400.0,
    )

    # Initial state: already at ignition speed (e.g. air-launched)
    initial = VehicleState(
        v=600.0,          # m/s — above ramjet ignition
        h=33_000.0,       # m — cruise altitude
        fuel=800.0,
        oxidizer=400.0,
        T_wall=350.0,
        mode=EngineMode.RAMJET_ATMOSPHERIC,
        dry_mass=1_200.0,
    )

    print("\n--- Running Trajectory Integration ---")
    result, history = integrator.run(initial, verbose=True)

    print()
    print(result.report())

    # Demonstrate Tsiolkovsky Δv for vacuum burn (Object 8)
    vac = VacuumRocketModel(I_sp_s=450.0, vacuum_thrust_N=20_000.0)
    m_i = 1_200.0 + 400.0 + 400.0   # dry + remaining fuel + full oxidizer
    m_f = 1_200.0                     # dry mass only
    dv_tsiol = vac.delta_v_tsiolkovsky(m_i, m_f)
    print(f"\n--- Tsiolkovsky Δv (vacuum stage) ---")
    print(f"  m_initial = {m_i:.1f} kg")
    print(f"  m_final   = {m_f:.1f} kg")
    print(f"  Isp       = {vac.I_sp_s:.0f} s")
    print(f"  v_e       = {vac.exhaust_velocity:.1f} m/s")
    print(f"  Δv        = {dv_tsiol:,.1f} m/s  ({dv_tsiol/1000:.2f} km/s)")

    print("\n--- Reachability Theorem Status ---")
    print("  ∵ T bounded, m(t) ≥ m_dry > 0, burn_time < ∞,")
    print("    D(v,h) ≥ 0, thermal_valid checked each step.")
    print("  ∴ REACHABILITY_THEOREM_COMPUTATIONAL_ONLY.")
