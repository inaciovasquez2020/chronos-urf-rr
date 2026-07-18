from __future__ import annotations

from dataclasses import dataclass
import math
import sys
import unittest

import numpy as np
from scipy.integrate import solve_bvp


def carbon_coupling_from_trace_energy(
    q_c_toy_j: float,
    trace_energy_j: float,
) -> float:
    """Return beta_C from Q_C^toy = beta_C E_tr."""
    if not math.isfinite(q_c_toy_j):
        raise ValueError("q_c_toy_j must be finite")
    if not math.isfinite(trace_energy_j) or trace_energy_j <= 0.0:
        raise ValueError("trace_energy_j must be finite and positive")
    return q_c_toy_j / trace_energy_j


def toy_charge_from_carbon_coupling(
    beta_c: float,
    trace_energy_j: float,
) -> float:
    """Return Q_C^toy from Q_C^toy = beta_C E_tr."""
    if not math.isfinite(beta_c):
        raise ValueError("beta_c must be finite")
    if not math.isfinite(trace_energy_j) or trace_energy_j <= 0.0:
        raise ValueError("trace_energy_j must be finite and positive")
    return beta_c * trace_energy_j


REJECTED_PHYSICAL_FORCE_ENHANCEMENT = 3.51890277916e-6


EXPERIMENTAL_NO_GO_ACCELERATION_M_S2 = 1.65254352794e-51
REFERENCE_CARBON_MASS_KG = 1000.0
REFERENCE_OBSERVER_RADIUS_M = 10.0
REFERENCE_TOY_CHARGE_J = 0.1


def normalization_compatible_no_go_acceleration(
    q_c_toy_j: float,
    trace_energy_j: float,
    source_mass_kg: float,
    observer_radius_m: float,
    G: float = 6.67430e-11,
) -> float:
    """Conditional universal, massless, long-range scalar acceleration."""
    if source_mass_kg <= 0.0:
        raise ValueError("source_mass_kg must be positive")
    if observer_radius_m <= 0.0:
        raise ValueError("observer_radius_m must be positive")
    beta_c = carbon_coupling_from_trace_energy(
        q_c_toy_j,
        trace_energy_j,
    )
    return (
        2.0
        * beta_c**2
        * G
        * source_mass_kg
        / observer_radius_m**2
    )


@dataclass(frozen=True)
class CarbonControlDifferentialErrorBudget:
    statistical_m_s2: float = 0.0
    mass_matching_m_s2: float = 0.0
    position_matching_m_s2: float = 0.0
    multipole_m_s2: float = 0.0
    electric_m_s2: float = 0.0
    magnetic_m_s2: float = 0.0
    thermal_m_s2: float = 0.0
    vibration_m_s2: float = 0.0
    background_gravity_m_s2: float = 0.0

    def __post_init__(self) -> None:
        for name, value in vars(self).items():
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(
                    f"{name} must be finite and nonnegative"
                )

    def total_sigma_m_s2(self) -> float:
        return math.sqrt(
            sum(value**2 for value in vars(self).values())
        )

    def satisfies_five_sigma(
        self,
        signal_m_s2: float = EXPERIMENTAL_NO_GO_ACCELERATION_M_S2,
    ) -> bool:
        if signal_m_s2 <= 0.0:
            raise ValueError("signal_m_s2 must be positive")
        return 5.0 * self.total_sigma_m_s2() <= signal_m_s2


@dataclass(frozen=True)
class Parameters:
    # DIMENSIONS
    #
    # y, L, r, x                 : metre
    # n = log(N), phi            : dimensionless
    # eta, q_C                   : dimensionless
    # C_partial, Q_C             : joule
    # A, kappa                   : joule metre
    # mu2, mphi2, lambda4        : joule / metre
    # M                          : kilogram
    # E_C                        : joule
    # G                          : m^3 kg^-1 s^-2
    # c, c_s                     : metre / second

    L: float = 1.0

    A: float = 2.0
    kappa: float = 3.0
    mu2: float = 10.0
    mphi2: float = 1.0
    lambda4: float = 0.5

    eta: float = 0.2
    q_C: float = 0.1
    C_partial: float = 1.0

    G: float = 6.67430e-11
    c: float = 299_792_458.0
    c_s: float = 10_000_000.0

    M: float = 1_000.0
    E_C: float = 1.0e9

    r: float = 10.0
    x: float = 0.6

    @property
    def Q_C(self) -> float:
        """
        Carbon boundary charge:

            Q_C = q_C C_partial

        Dimension: joule.
        """
        return self.q_C * self.C_partial

    def validate(self) -> None:
        positive = (
            "L",
            "A",
            "kappa",
            "mu2",
            "mphi2",
            "lambda4",
            "G",
            "c",
            "c_s",
            "M",
            "r",
        )

        for name in positive:
            if getattr(self, name) <= 0.0:
                raise ValueError(f"{name} must be positive")

        if not 0.0 < self.x <= self.L:
            raise ValueError("x must lie in (0,L]")


class ToyGravityModel:
    r"""
    Exact nonlinear one-dimensional scalar-lapse toy model.

    Write

        N(y) = exp(n(y)),

    so N is positive without a weak-field approximation.

    Positive bulk energy:

        E = integral_0^L [
              A/2 n'^2
            + kappa/2 phi'^2
            + mu2/2 (n - eta (c_s/c)^2 phi)^2
            + mphi2/2 phi^2
            + lambda4/4 phi^4
        ] dy.

    For

        A, kappa, mu2, mphi2, lambda4 >= 0,

    every summand is nonnegative, hence E >= 0.

    Euler-Lagrange equations:

        -A n'' + mu2(n - eta (c_s/c)^2 phi) = 0,

        -kappa phi''
        + mphi2 phi
        + lambda4 phi^3
        - eta (c_s/c)^2 mu2(n - eta (c_s/c)^2 phi)
        = 0.

    Boundary conditions:

        n'(0) = 0,
        n'(L) = 0,
        phi(0) = 0,
        kappa phi'(L) = Q_C.
    """

    def __init__(self, parameters: Parameters = Parameters()):
        parameters.validate()
        self.p = parameters
        self.solution = None

    def equations(
        self,
        coordinate: np.ndarray,
        state: np.ndarray,
    ) -> np.ndarray:
        del coordinate

        n, n_prime, phi, phi_prime = state
        locking_error = (
            n
            - self.p.eta
            * (self.p.c_s / self.p.c) ** 2
            * phi
        )

        n_second = self.p.mu2 * locking_error / self.p.A

        phi_second = (
            self.p.mphi2 * phi
            + self.p.lambda4 * phi**3
            - self.p.eta
            * (self.p.c_s / self.p.c) ** 2
            * self.p.mu2
            * locking_error
        ) / self.p.kappa

        return np.vstack(
            (
                n_prime,
                n_second,
                phi_prime,
                phi_second,
            )
        )

    def boundary_residual(
        self,
        left: np.ndarray,
        right: np.ndarray,
    ) -> np.ndarray:
        return np.array(
            [
                left[1],
                right[1],
                left[2],
                self.p.kappa * right[3] - self.p.Q_C,
            ]
        )

    def solve(self) -> "ToyGravityModel":
        coordinate = np.linspace(0.0, self.p.L, 201)

        guess = np.zeros((4, coordinate.size))
        guess[2] = self.p.Q_C * coordinate / self.p.kappa
        guess[3] = self.p.Q_C / self.p.kappa

        solution = solve_bvp(
            self.equations,
            self.boundary_residual,
            coordinate,
            guess,
            tol=1.0e-8,
            max_nodes=20_000,
        )

        if not solution.success:
            raise RuntimeError(solution.message)

        self.solution = solution
        return self

    def fields(self, coordinate: float | np.ndarray) -> np.ndarray:
        if self.solution is None:
            raise RuntimeError("solve() must be called first")

        return self.solution.sol(coordinate)

    def energy_densities(
        self,
        coordinate: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        n, n_prime, phi, phi_prime = self.fields(coordinate)

        locking_error = (
            n
            - self.p.eta
            * (self.p.c_s / self.p.c) ** 2
            * phi
        )

        lapse_density = (
            0.5 * self.p.A * n_prime**2
            + 0.5 * self.p.mu2 * locking_error**2
        )

        scalar_density = (
            0.5 * self.p.kappa * phi_prime**2
            + 0.5 * self.p.mphi2 * phi**2
            + 0.25 * self.p.lambda4 * phi**4
        )

        return lapse_density, scalar_density

    def total_bulk_energy(self) -> float:
        coordinate = np.linspace(0.0, self.p.L, 2001)
        lapse_density, scalar_density = self.energy_densities(coordinate)

        return float(
            np.trapezoid(
                lapse_density + scalar_density,
                coordinate,
            )
        )

    def effective_mass(self) -> float:
        return self.p.M + self.p.E_C / self.p.c**2

    def base_gravity(self) -> float:
        return self.p.G * self.effective_mass() / self.p.r**2

    def gravity(self) -> float:
        n_at_x = float(self.fields(self.p.x)[0])
        # Internal toy observable only; not a physical carbon-force prediction.

        # Exact nonlinear lapse correction:
        #
        #     g_V = G M_eff exp(n(x)) / r^2.
        return self.base_gravity() * math.exp(n_at_x)

    def alpha_exact(self) -> float:
        sound_ratio_squared = (self.p.c_s / self.p.c) ** 2

        return (
            (self.p.L / self.p.x)
            * (self.gravity() / self.base_gravity() - 1.0)
            / sound_ratio_squared
        )

    def coupled_green_kernel(
        self,
        source_coordinate: float,
    ) -> float:
        """
        Exact Green kernel for the coupled linearized boundary problem.

        For forcing s(y) in

            delta_phi'' = linear_terms + s(y),

        the lapse response satisfies

            delta_n(x) = integral_0^L K_x(y) s(y) dy.
        """
        from scipy.linalg import expm

        if not 0.0 <= source_coordinate <= self.p.L:
            raise ValueError(
                "source_coordinate must lie in [0,L]"
            )

        sound_ratio_squared = (
            self.p.c_s / self.p.c
        ) ** 2

        beta = (
            self.p.eta
            * sound_ratio_squared
        )

        evolution = np.array(
            [
                [0.0, 1.0, 0.0, 0.0],
                [
                    self.p.mu2 / self.p.A,
                    0.0,
                    -self.p.mu2 * beta / self.p.A,
                    0.0,
                ],
                [0.0, 0.0, 0.0, 1.0],
                [
                    -beta * self.p.mu2 / self.p.kappa,
                    0.0,
                    (
                        self.p.mphi2
                        + self.p.mu2 * beta**2
                    )
                    / self.p.kappa,
                    0.0,
                ],
            ],
            dtype=float,
        )

        initial_basis = np.array(
            [
                [1.0, 0.0],
                [0.0, 0.0],
                [0.0, 0.0],
                [0.0, 1.0],
            ],
            dtype=float,
        )

        boundary_projection = np.array(
            [
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, self.p.kappa],
            ],
            dtype=float,
        )

        observation = np.array(
            [1.0, 0.0, 0.0, 0.0],
            dtype=float,
        )

        source_direction = np.array(
            [0.0, 0.0, 0.0, 1.0],
            dtype=float,
        )

        transition_at_L = expm(
            evolution * self.p.L
        )

        boundary_matrix = (
            boundary_projection
            @ transition_at_L
            @ initial_basis
        )

        terminal_source = (
            boundary_projection
            @ expm(
                evolution
                * (
                    self.p.L
                    - source_coordinate
                )
            )
            @ source_direction
        )

        initial_correction = np.linalg.solve(
            boundary_matrix,
            terminal_source,
        )

        correction = float(
            observation
            @ expm(evolution * self.p.x)
            @ initial_basis
            @ initial_correction
        )

        direct = 0.0

        if source_coordinate <= self.p.x:
            direct = float(
                observation
                @ expm(
                    evolution
                    * (
                        self.p.x
                        - source_coordinate
                    )
                )
                @ source_direction
            )

        return direct - correction

    def coupled_green_norm_arb_enclosure(
        self,
        subdivisions_per_segment: int = 128,
        precision_bits: int = 192,
    ):
        """
        Outward-rounded Arb enclosure of

            integral_0^L |K_x(y)| dy.
        """
        from flint import arb, arb_mat, ctx

        if subdivisions_per_segment <= 0:
            raise ValueError(
                "subdivisions_per_segment must be positive"
            )

        if precision_bits < 64:
            raise ValueError(
                "precision_bits must be at least 64"
            )

        previous_precision = ctx.prec
        ctx.prec = precision_bits

        try:
            def exact(value: float):
                return arb(repr(value))

            L = exact(self.p.L)
            x = exact(self.p.x)
            A_energy = exact(self.p.A)
            kappa = exact(self.p.kappa)
            mu2 = exact(self.p.mu2)
            mphi2 = exact(self.p.mphi2)
            eta = exact(self.p.eta)
            c_s = exact(self.p.c_s)
            c = exact(self.p.c)

            sound_ratio_squared = (c_s / c) ** 2
            beta = eta * sound_ratio_squared

            evolution = arb_mat(
                [
                    [0, 1, 0, 0],
                    [
                        mu2 / A_energy,
                        0,
                        -(mu2 * beta) / A_energy,
                        0,
                    ],
                    [0, 0, 0, 1],
                    [
                        -(beta * mu2) / kappa,
                        0,
                        (
                            mphi2
                            + mu2 * beta**2
                        )
                        / kappa,
                        0,
                    ],
                ]
            )

            initial_basis = arb_mat(
                [
                    [1, 0],
                    [0, 0],
                    [0, 0],
                    [0, 1],
                ]
            )

            boundary_projection = arb_mat(
                [
                    [0, 1, 0, 0],
                    [0, 0, 0, kappa],
                ]
            )

            observation = arb_mat(
                [[1, 0, 0, 0]]
            )

            source_direction = arb_mat(
                [
                    [0],
                    [0],
                    [0],
                    [1],
                ]
            )

            transition_at_L = (
                evolution * L
            ).exp()

            transition_at_x = (
                evolution * x
            ).exp()

            boundary_matrix = (
                boundary_projection
                * transition_at_L
                * initial_basis
            )

            observation_initial = (
                observation
                * transition_at_x
                * initial_basis
            )

            lower_sum = arb(0)
            upper_sum = arb(0)

            segments = (
                (arb(0), x, True),
                (x, L, False),
            )

            for (
                segment_start,
                segment_end,
                direct_enabled,
            ) in segments:
                segment_length = (
                    segment_end
                    - segment_start
                )

                for index in range(
                    subdivisions_per_segment
                ):
                    left = (
                        segment_start
                        + segment_length
                        * index
                        / subdivisions_per_segment
                    )

                    right = (
                        segment_start
                        + segment_length
                        * (index + 1)
                        / subdivisions_per_segment
                    )

                    source_coordinate = left.union(right)
                    cell_width = right - left

                    terminal_source = (
                        boundary_projection
                        * (
                            evolution
                            * (
                                L
                                - source_coordinate
                            )
                        ).exp()
                        * source_direction
                    )

                    initial_correction = (
                        boundary_matrix.solve(
                            terminal_source
                        )
                    )

                    correction = (
                        observation_initial
                        * initial_correction
                    )[0, 0]

                    direct = arb(0)

                    if direct_enabled:
                        direct = (
                            observation
                            * (
                                evolution
                                * (
                                    x
                                    - source_coordinate
                                )
                            ).exp()
                            * source_direction
                        )[0, 0]

                    kernel_ball = direct - correction

                    lower_sum += (
                        kernel_ball.abs_lower()
                        * cell_width
                    )

                    upper_sum += (
                        kernel_ball.abs_upper()
                        * cell_width
                    )

            return lower_sum.lower().union(
                upper_sum.upper()
            )
        finally:
            ctx.prec = previous_precision

    def coupled_green_linf_to_point_norm(self) -> float:
        """
        Computed L-infinity-to-point operator norm:

            ||K_x||_1 = integral_0^L |K_x(y)| dy.
        """
        from scipy.integrate import quad

        left, _ = quad(
            lambda y: abs(
                self.coupled_green_kernel(y)
            ),
            0.0,
            self.p.x,
            epsabs=1.0e-14,
            epsrel=1.0e-11,
            limit=200,
        )

        right, _ = quad(
            lambda y: abs(
                self.coupled_green_kernel(y)
            ),
            self.p.x,
            self.p.L,
            epsabs=1.0e-14,
            epsrel=1.0e-11,
            limit=200,
        )

        return float(left + right)

    def phi_sup_energy_bound(self) -> float:
        """
        Analytic bound obtained from the stationary energy identity:

            D = Q_C phi(L),

        where

            D >= kappa integral_0^L phi'(y)^2 dy.

        Since phi(0)=0,

            ||phi||_infinity
                <= sqrt(L integral phi'^2)
                <= |Q_C| L / kappa.
        """
        return (
            abs(self.p.Q_C)
            * self.p.L
            / self.p.kappa
        )

    def alpha_cubic_green_operator_arb_enclosure(
        self,
        subdivisions_per_segment: int = 256,
        precision_bits: int = 256,
    ):
        """
        Fully outward-rounded Arb enclosure of the cubic-response
        upper bound.
        """
        from flint import arb, ctx

        previous_precision = ctx.prec
        ctx.prec = precision_bits

        try:
            def exact(value: float):
                return arb(repr(value))

            L = exact(self.p.L)
            x = exact(self.p.x)
            c_s = exact(self.p.c_s)
            c = exact(self.p.c)
            lambda4 = exact(abs(self.p.lambda4))
            kappa = exact(self.p.kappa)
            Q_C = exact(abs(self.p.Q_C))

            extraction_scale = (
                L
                / x
                / (c_s / c) ** 2
            )

            phi_supremum_bound = (
                Q_C
                * L
                / kappa
            )

            maximum_cubic_source = (
                lambda4
                / kappa
                * phi_supremum_bound**3
            )

            green_norm_enclosure = (
                self.coupled_green_norm_arb_enclosure(
                    subdivisions_per_segment=(
                        subdivisions_per_segment
                    ),
                    precision_bits=precision_bits,
                )
            )

            return (
                extraction_scale
                * green_norm_enclosure
                * maximum_cubic_source
            )
        finally:
            ctx.prec = previous_precision

    def alpha_total_remainder_arb_enclosure(
        self,
        subdivisions_per_segment: int = 256,
        precision_bits: int = 256,
    ):
        """
        Outward-rounded upper-bound enclosure for

            |alpha_exact - alpha_coupled_linear|.

        The bound is the sum of the certified cubic field-response
        bound and the analytic exponential Taylor-remainder bound.
        """
        from flint import arb, ctx

        if precision_bits < 64:
            raise ValueError(
                "precision_bits must be at least 64"
            )

        previous_precision = ctx.prec
        ctx.prec = precision_bits

        try:
            def exact(value: float):
                return arb(repr(value))

            L = exact(self.p.L)
            x = exact(self.p.x)
            eta = exact(abs(self.p.eta))
            c_s = exact(self.p.c_s)
            c = exact(self.p.c)
            Q_C = exact(abs(self.p.Q_C))
            kappa = exact(self.p.kappa)

            sound_ratio_squared = (c_s / c) ** 2

            phi_supremum_bound = (
                Q_C
                * L
                / kappa
            )

            n_absolute_bound = (
                eta
                * sound_ratio_squared
                * phi_supremum_bound
            )

            extraction_scale = (
                L
                / x
                / sound_ratio_squared
            )

            exponential_bound = (
                extraction_scale
                * arb("0.5")
                * n_absolute_bound.exp()
                * n_absolute_bound**2
            )

            cubic_bound = (
                self.alpha_cubic_green_operator_arb_enclosure(
                    subdivisions_per_segment=(
                        subdivisions_per_segment
                    ),
                    precision_bits=precision_bits,
                )
            )

            return cubic_bound + exponential_bound
        finally:
            ctx.prec = previous_precision

    def alpha_cubic_green_operator_bound(self) -> float:
        """
        A posteriori Green-operator bound for lambda4 phi^3.
        """
        maximum_source = (
            abs(self.p.lambda4)
            / self.p.kappa
            * self.phi_sup_energy_bound() ** 3
        )

        extraction_scale = (
            self.p.L
            / self.p.x
            / (
                self.p.c_s
                / self.p.c
            ) ** 2
        )

        certified_enclosure = (
            self.coupled_green_norm_arb_enclosure(
                subdivisions_per_segment=256,
                precision_bits=256,
            )
        )

        certified_green_norm_upper = float(
            certified_enclosure.upper()
        )

        return (
            extraction_scale
            * certified_green_norm_upper
            * maximum_source
        )

    def alpha_exponential_remainder_bound(self) -> float:
        """
        Outward-rounded exponential remainder bound using

            ||phi||_infinity <= |Q_C| L / kappa

        and the maximum-principle estimate

            ||n||_infinity
                <= |eta| (c_s/c)^2 ||phi||_infinity.
        """
        from flint import arb, ctx

        previous_precision = ctx.prec
        ctx.prec = 256

        try:
            def exact(value: float):
                return arb(repr(value))

            L = exact(self.p.L)
            x = exact(self.p.x)
            eta = exact(self.p.eta)
            c_s = exact(self.p.c_s)
            c = exact(self.p.c)
            Q_C = exact(abs(self.p.Q_C))
            kappa = exact(self.p.kappa)

            sound_ratio_squared = (c_s / c) ** 2

            phi_supremum_bound = (
                Q_C
                * L
                / kappa
            )

            n_absolute_bound = (
                abs(eta)
                * sound_ratio_squared
                * phi_supremum_bound
            )

            extraction_scale = (
                L
                / x
                / sound_ratio_squared
            )

            remainder_bound = (
                extraction_scale
                * arb("0.5")
                * n_absolute_bound.exp()
                * n_absolute_bound**2
            )

            return float(
                remainder_bound.upper()
            )
        finally:
            ctx.prec = previous_precision

    def alpha_coupled_linear_response(self) -> float:
        """Exact first-order response of the coupled boundary problem."""
        from scipy.linalg import expm

        sound_ratio_squared = (self.p.c_s / self.p.c) ** 2
        beta = self.p.eta * sound_ratio_squared

        evolution = np.array(
            [
                [0.0, 1.0, 0.0, 0.0],
                [
                    self.p.mu2 / self.p.A,
                    0.0,
                    -self.p.mu2 * beta / self.p.A,
                    0.0,
                ],
                [0.0, 0.0, 0.0, 1.0],
                [
                    -beta * self.p.mu2 / self.p.kappa,
                    0.0,
                    (
                        self.p.mphi2
                        + self.p.mu2 * beta**2
                    )
                    / self.p.kappa,
                    0.0,
                ],
            ],
            dtype=float,
        )

        initial_basis = np.array(
            [
                [1.0, 0.0],
                [0.0, 0.0],
                [0.0, 0.0],
                [0.0, 1.0],
            ],
            dtype=float,
        )

        boundary_projection = np.array(
            [
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, self.p.kappa],
            ],
            dtype=float,
        )

        transition_at_L = expm(evolution * self.p.L)

        initial_coefficients = np.linalg.solve(
            boundary_projection
            @ transition_at_L
            @ initial_basis,
            np.array(
                [
                    0.0,
                    self.p.Q_C,
                ],
                dtype=float,
            ),
        )

        state_at_x = (
            expm(evolution * self.p.x)
            @ initial_basis
            @ initial_coefficients
        )

        n_linear_at_x = float(state_at_x[0])

        return (
            self.p.L
            / self.p.x
            * n_linear_at_x
            / sound_ratio_squared
        )

    def alpha_linear_limit(self) -> float:
        # Small-field boundary-flux approximation:
        #
        #     alpha ~= eta Q_C L / kappa.
        return self.p.eta * self.p.Q_C * self.p.L / self.p.kappa

    def maximum_ode_residual(self) -> float:
        if self.solution is None:
            raise RuntimeError("solve() must be called first")

        coordinate = np.linspace(0.0, self.p.L, 1001)
        state = self.fields(coordinate)

        numerical_derivative = self.solution.sol(coordinate, 1)
        equation_derivative = self.equations(coordinate, state)

        return float(
            np.max(
                np.abs(
                    numerical_derivative - equation_derivative
                )
            )
        )


@dataclass(frozen=True)
class MeasuredCarbonProfiles:
    """Externally supplied CT density and residual-stress arrays.

    Positive stress values use the pressure sign convention.  No homogeneous
    density or zero-stress fallback is constructed by this class.
    """

    ct_radius_m: np.ndarray
    ct_density_kg_m3: np.ndarray
    stress_radius_m: np.ndarray
    residual_radial_stress_pa: np.ndarray
    residual_tangential_stress_pa: np.ndarray

    def __post_init__(self) -> None:
        names = (
            "ct_radius_m",
            "ct_density_kg_m3",
            "stress_radius_m",
            "residual_radial_stress_pa",
            "residual_tangential_stress_pa",
        )
        arrays: dict[str, np.ndarray] = {}
        for name in names:
            value = getattr(self, name)
            if not isinstance(value, np.ndarray):
                raise TypeError(f"{name} must be a numpy array")
            array = np.array(value, dtype=float, copy=True)
            if array.ndim != 1 or array.size < 4:
                raise ValueError(
                    f"{name} must be one-dimensional with at least four values"
                )
            if not np.all(np.isfinite(array)):
                raise ValueError(f"{name} must contain only finite values")
            array.setflags(write=False)
            arrays[name] = array
            object.__setattr__(self, name, array)

        if arrays["ct_radius_m"].shape != arrays["ct_density_kg_m3"].shape:
            raise ValueError("CT radius and density arrays must have equal shape")
        if (
            arrays["stress_radius_m"].shape
            != arrays["residual_radial_stress_pa"].shape
        ):
            raise ValueError(
                "stress radius and radial-stress arrays must have equal shape"
            )
        if (
            arrays["stress_radius_m"].shape
            != arrays["residual_tangential_stress_pa"].shape
        ):
            raise ValueError(
                "stress radius and tangential-stress arrays must have equal shape"
            )

        for radius_name in ("ct_radius_m", "stress_radius_m"):
            radius = arrays[radius_name]
            if radius[0] != 0.0:
                raise ValueError(f"{radius_name} must start at zero")
            if not np.all(np.diff(radius) > 0.0):
                raise ValueError(f"{radius_name} must be strictly increasing")

        if not math.isclose(
            float(arrays["ct_radius_m"][-1]),
            float(arrays["stress_radius_m"][-1]),
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ):
            raise ValueError(
                "CT and stress arrays must end at the same sample radius"
            )
        if np.any(arrays["ct_density_kg_m3"] <= 0.0):
            raise ValueError("CT density must be positive")

    @property
    def radius_m(self) -> float:
        return float(self.ct_radius_m[-1])

    def density(self, radius_m: np.ndarray) -> np.ndarray:
        radius = np.asarray(radius_m, dtype=float)
        return np.where(
            radius <= self.radius_m,
            np.interp(
                radius,
                self.ct_radius_m,
                self.ct_density_kg_m3,
            ),
            0.0,
        )

    def radial_stress(self, radius_m: np.ndarray) -> np.ndarray:
        radius = np.asarray(radius_m, dtype=float)
        return np.where(
            radius <= self.radius_m,
            np.interp(
                radius,
                self.stress_radius_m,
                self.residual_radial_stress_pa,
            ),
            0.0,
        )

    def tangential_stress(self, radius_m: np.ndarray) -> np.ndarray:
        radius = np.asarray(radius_m, dtype=float)
        return np.where(
            radius <= self.radius_m,
            np.interp(
                radius,
                self.stress_radius_m,
                self.residual_tangential_stress_pa,
            ),
            0.0,
        )

    def mass_kg(self) -> float:
        return float(
            4.0
            * math.pi
            * np.trapezoid(
                self.ct_radius_m**2 * self.ct_density_kg_m3,
                self.ct_radius_m,
            )
        )

    def flat_trace_energy_j(self, c: float) -> float:
        grid = np.unique(
            np.concatenate(
                (
                    self.ct_radius_m,
                    self.stress_radius_m,
                )
            )
        )
        trace_density = (
            self.density(grid) * c**2
            - self.radial_stress(grid)
            - 2.0 * self.tangential_stress(grid)
        )
        value = float(
            4.0
            * math.pi
            * np.trapezoid(
                grid**2 * trace_density,
                grid,
            )
        )
        if value <= 0.0:
            raise ValueError("integrated trace energy must be positive")
        return value


class DimensionlessRadialCarbonModel:
    """Full nonlinear static spherical scalar-metric model.

    The prescribed source is anisotropic: CT density rho, radial stress p_r,
    and tangential stress p_t.  The state is (u, nu, chi, dchi/dx), where
    x=r/R, u=m/M, h=1-Cu/x, C=2GM/(Rc^2), and
    chi=phi/(beta_C C).  This scaling retains every nonlinear scalar-gradient
    term while avoiding underflow at beta_C approximately 10^-21.
    """

    def __init__(
        self,
        profiles: MeasuredCarbonProfiles,
        q_c_toy_j: float = 0.1,
        *,
        G: float = 6.67430e-11,
        c: float = 299_792_458.0,
        outer_radius_ratio: float = 20.0,
    ) -> None:
        if outer_radius_ratio <= 1.0:
            raise ValueError("outer_radius_ratio must exceed one")
        self.profiles = profiles
        self.q_c_toy_j = float(q_c_toy_j)
        self.G = float(G)
        self.c = float(c)
        self.outer_radius_ratio = float(outer_radius_ratio)
        self.radius_m = profiles.radius_m
        self.mass_kg = profiles.mass_kg()
        if self.mass_kg <= 0.0:
            raise ValueError("profile mass must be positive")
        self.compactness = (
            2.0
            * self.G
            * self.mass_kg
            / (self.radius_m * self.c**2)
        )
        if not 0.0 < self.compactness < 1.0:
            raise ValueError("sample compactness must lie in (0,1)")
        self.trace_energy_j = profiles.flat_trace_energy_j(self.c)
        self.beta_c = carbon_coupling_from_trace_energy(
            self.q_c_toy_j,
            self.trace_energy_j,
        )
        self._x_min = 1.0e-7
        self._inside_solution = None
        self._outside_solution = None
        self._nu_shift = 0.0
        self._chi_shift = 0.0

    def _source_hats(
        self,
        x: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        x_array = np.asarray(x, dtype=float)
        radius_m = x_array * self.radius_m
        inside = x_array <= 1.0
        mass_scale = (
            4.0
            * math.pi
            * self.radius_m**3
            / self.mass_kg
        )
        rho_hat = np.where(
            inside,
            mass_scale * self.profiles.density(radius_m),
            0.0,
        )
        stress_scale = mass_scale / self.c**2
        p_r_hat = np.where(
            inside,
            stress_scale * self.profiles.radial_stress(radius_m),
            0.0,
        )
        p_t_hat = np.where(
            inside,
            stress_scale * self.profiles.tangential_stress(radius_m),
            0.0,
        )
        return rho_hat, p_r_hat, p_t_hat

    def equations(
        self,
        x: float,
        state: np.ndarray,
    ) -> np.ndarray:
        u, nu, chi, chi_prime = state
        del nu, chi
        safe_x = max(float(x), self._x_min)
        h = 1.0 - self.compactness * u / safe_x
        if h <= 0.0:
            raise RuntimeError("radial solution crossed h=0")

        rho_hat, p_r_hat, p_t_hat = self._source_hats(
            np.array([safe_x])
        )
        rho_value = float(rho_hat[0])
        p_r_value = float(p_r_hat[0])
        p_t_value = float(p_t_hat[0])

        scalar_mass_factor = self.beta_c**2 * self.compactness
        u_prime = (
            safe_x**2 * rho_value
            + scalar_mass_factor
            * safe_x**2
            * h
            * chi_prime**2
        )
        h_prime = -self.compactness * (
            u_prime / safe_x - u / safe_x**2
        )
        nu_prime = (
            0.5
            * self.compactness
            * (u + safe_x**3 * p_r_value)
            / (safe_x**2 * h)
            + 0.5
            * self.beta_c**2
            * self.compactness**2
            * safe_x
            * chi_prime**2
        )
        trace_hat = rho_value - p_r_value - 2.0 * p_t_value
        chi_second = (
            0.5 * trace_hat / h
            - (
                2.0 / safe_x
                + nu_prime
                + 0.5 * h_prime / h
            )
            * chi_prime
        )
        return np.array(
            (
                u_prime,
                nu_prime,
                chi_prime,
                chi_second,
            )
        )

    def _solve_once(self) -> None:
        from scipy.integrate import solve_ivp

        rho_hat, p_r_hat, p_t_hat = self._source_hats(
            np.array([self._x_min])
        )
        trace_hat = float(
            rho_hat[0] - p_r_hat[0] - 2.0 * p_t_hat[0]
        )
        initial_state = np.array(
            [
                float(rho_hat[0]) * self._x_min**3 / 3.0,
                0.0,
                trace_hat * self._x_min**2 / 12.0,
                trace_hat * self._x_min / 6.0,
            ]
        )

        inside = solve_ivp(
            self.equations,
            (self._x_min, 1.0),
            initial_state,
            rtol=1.0e-10,
            atol=1.0e-12,
            dense_output=True,
            max_step=1.0 / 400.0,
        )
        if not inside.success:
            raise RuntimeError(inside.message)

        outside = solve_ivp(
            self.equations,
            (1.0, self.outer_radius_ratio),
            inside.y[:, -1],
            rtol=1.0e-10,
            atol=1.0e-12,
            dense_output=True,
            max_step=(self.outer_radius_ratio - 1.0) / 400.0,
        )
        if not outside.success:
            raise RuntimeError(outside.message)

        right = outside.y[:, -1]
        h_right = 1.0 - (
            self.compactness
            * right[0]
            / self.outer_radius_ratio
        )
        self._chi_shift = (
            -right[2]
            - self.outer_radius_ratio * right[3]
        )
        self._nu_shift = 0.5 * math.log(h_right) - right[1]
        self._inside_solution = inside
        self._outside_solution = outside

    def solve(self) -> "DimensionlessRadialCarbonModel":
        for _ in range(4):
            self._solve_once()
            trace_energy_j = self.covariant_trace_energy_j()
            beta_c = carbon_coupling_from_trace_energy(
                self.q_c_toy_j,
                trace_energy_j,
            )
            previous_beta_c = self.beta_c
            self.trace_energy_j = trace_energy_j
            self.beta_c = beta_c
            if math.isclose(
                beta_c,
                previous_beta_c,
                rel_tol=1.0e-12,
                abs_tol=0.0,
            ):
                return self
        raise RuntimeError(
            "carbon-coupling fixed point did not converge"
        )

    @property
    def solution_success(self) -> bool:
        return (
            self._inside_solution is not None
            and self._outside_solution is not None
            and self._inside_solution.success
            and self._outside_solution.success
        )

    def fields(
        self,
        x: float | np.ndarray,
    ) -> np.ndarray:
        if not self.solution_success:
            raise RuntimeError("solve() must be called first")
        x_array = np.atleast_1d(np.asarray(x, dtype=float))
        if np.any(x_array < self._x_min) or np.any(
            x_array > self.outer_radius_ratio
        ):
            raise ValueError(
                "x lies outside the solved radial interval"
            )

        result = np.empty((4, x_array.size), dtype=float)
        inside_mask = x_array <= 1.0
        if np.any(inside_mask):
            result[:, inside_mask] = self._inside_solution.sol(
                x_array[inside_mask]
            )
        if np.any(~inside_mask):
            result[:, ~inside_mask] = self._outside_solution.sol(
                x_array[~inside_mask]
            )
        result[1] += self._nu_shift
        result[2] += self._chi_shift
        if np.ndim(x) == 0:
            return result[:, 0]
        return result

    def physical_scalar_fields(
        self,
        x: float | np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        state = self.fields(x)
        scale = self.beta_c * self.compactness
        return scale * state[2], scale * state[3]

    def covariant_trace_energy_j(self) -> float:
        x = np.linspace(self._x_min, 1.0, 4001)
        u, nu, _, _ = self.fields(x)
        h = 1.0 - self.compactness * u / x
        radius_m = x * self.radius_m
        trace_density = (
            self.profiles.density(radius_m) * self.c**2
            - self.profiles.radial_stress(radius_m)
            - 2.0 * self.profiles.tangential_stress(radius_m)
        )
        value = float(
            4.0
            * math.pi
            * np.trapezoid(
                np.exp(nu)
                * radius_m**2
                * trace_density
                / np.sqrt(h),
                radius_m,
            )
        )
        if value <= 0.0:
            raise RuntimeError(
                "covariant trace energy became nonpositive"
            )
        return value

    def universal_long_range_acceleration_difference(
        self,
        observer_radius_m: float,
    ) -> float:
        if observer_radius_m <= self.radius_m:
            raise ValueError("observer must lie outside the sample")
        return (
            2.0
            * self.beta_c**2
            * self.G
            * self.mass_kg
            / observer_radius_m**2
        )


class ToyGravityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = ToyGravityModel().solve()
        cls.p = cls.model.p

    def test_boundary_conditions(self) -> None:
        residual = self.model.boundary_residual(
            self.model.fields(0.0),
            self.model.fields(self.p.L),
        )

        self.assertLess(
            float(np.max(np.abs(residual))),
            1.0e-8,
        )

    def test_coupled_equations(self) -> None:
        self.assertLess(
            self.model.maximum_ode_residual(),
            1.0e-7,
        )

    def test_pointwise_energy_positivity(self) -> None:
        coordinate = np.linspace(0.0, self.p.L, 2001)

        lapse_density, scalar_density = (
            self.model.energy_densities(coordinate)
        )

        self.assertGreaterEqual(
            float(np.min(lapse_density)),
            -1.0e-14,
        )

        self.assertGreaterEqual(
            float(np.min(scalar_density)),
            -1.0e-14,
        )

        self.assertGreaterEqual(
            self.model.total_bulk_energy(),
            0.0,
        )

    def test_charge_scaling_reduces_but_does_not_remove_naive_error(
        self,
    ) -> None:
        relative_errors: list[float] = []

        for q_c in (0.1, 0.05, 0.025):
            model = ToyGravityModel(
                Parameters(q_C=q_c)
            ).solve()

            exact = model.alpha_exact()
            linear = model.alpha_linear_limit()

            self.assertNotEqual(linear, 0.0)

            relative_errors.append(
                abs(exact - linear) / abs(linear)
            )

        self.assertGreater(
            relative_errors[0],
            relative_errors[1],
        )

        self.assertGreater(
            relative_errors[1],
            relative_errors[2],
        )

        # The error approaches a nonzero value near 20.93%.
        # Therefore the current boundary-flux expression is not
        # the exact linearized coupled-system coefficient.
        self.assertGreater(
            relative_errors[-1],
            0.20,
        )

    def test_positive_lapse_and_gravity(self) -> None:
        coordinate = np.linspace(0.0, self.p.L, 2001)
        n = self.model.fields(coordinate)[0]

        self.assertTrue(np.all(np.exp(n) > 0.0))
        self.assertGreater(self.model.gravity(), 0.0)

    def test_phi_sup_energy_bound(self) -> None:
        coordinate = np.linspace(
            0.0,
            self.p.L,
            4001,
        )

        numerical_phi_sup = float(
            np.max(
                np.abs(
                    self.model.fields(coordinate)[2]
                )
            )
        )

        analytic_bound = (
            self.model.phi_sup_energy_bound()
        )

        self.assertLessEqual(
            numerical_phi_sup,
            analytic_bound + 1.0e-15,
        )

    def test_arb_green_norm_enclosure(self) -> None:
        from flint import arb

        enclosure = (
            self.model
            .coupled_green_norm_arb_enclosure(
                subdivisions_per_segment=128,
                precision_bits=192,
            )
        )

        floating_value = (
            self.model
            .coupled_green_linf_to_point_norm()
        )

        self.assertTrue(
            enclosure.contains(
                arb(repr(floating_value))
            )
        )

        self.assertFalse(
            enclosure.contains(
                arb(0)
            )
        )

    def test_green_mesh_and_quadrature_convergence(
        self,
    ) -> None:
        from scipy.integrate import quad

        def kernel_norm(tolerance: float) -> float:
            left, _ = quad(
                lambda y: abs(
                    self.model.coupled_green_kernel(y)
                ),
                0.0,
                self.p.x,
                epsabs=tolerance,
                epsrel=tolerance,
                limit=400,
            )

            right, _ = quad(
                lambda y: abs(
                    self.model.coupled_green_kernel(y)
                ),
                self.p.x,
                self.p.L,
                epsabs=tolerance,
                epsrel=tolerance,
                limit=400,
            )

            return float(left + right)

        norm_coarse = kernel_norm(1.0e-8)
        norm_medium = kernel_norm(1.0e-10)
        norm_fine = kernel_norm(1.0e-12)

        coarse_change = abs(
            norm_medium - norm_coarse
        )

        fine_change = abs(
            norm_fine - norm_medium
        )

        self.assertLessEqual(
            fine_change,
            coarse_change + 1.0e-14,
        )

        self.assertLess(
            fine_change,
            1.0e-11,
        )

        extraction_scale = (
            self.p.L
            / self.p.x
            / (
                self.p.c_s
                / self.p.c
            ) ** 2
        )

        nonlinear_n_at_x = float(
            self.model.fields(self.p.x)[0]
        )

        linear_n_at_x = (
            self.model.alpha_coupled_linear_response()
            / extraction_scale
        )

        actual_delta_n = (
            nonlinear_n_at_x
            - linear_n_at_x
        )

        mesh_errors: list[float] = []

        for node_count in (
            501,
            1001,
            2001,
            4001,
        ):
            coordinate = np.linspace(
                0.0,
                self.p.L,
                node_count,
            )

            phi = self.model.fields(coordinate)[2]

            cubic_source = (
                self.p.lambda4
                / self.p.kappa
                * phi**3
            )

            kernel = np.array(
                [
                    self.model.coupled_green_kernel(y)
                    for y in coordinate
                ]
            )

            reconstructed_delta_n = float(
                np.trapezoid(
                    kernel * cubic_source,
                    coordinate,
                )
            )

            mesh_errors.append(
                abs(
                    reconstructed_delta_n
                    - actual_delta_n
                )
            )

        self.assertLessEqual(
            mesh_errors[2],
            mesh_errors[0] + 1.0e-16,
        )

        self.assertLessEqual(
            mesh_errors[3],
            mesh_errors[1] + 1.0e-16,
        )

        self.assertLess(
            mesh_errors[-1],
            2.0e-11,
        )

    def test_exact_green_kernel_and_operator_norm(
        self,
    ) -> None:
        coordinate = np.linspace(
            0.0,
            self.p.L,
            8001,
        )

        phi = self.model.fields(coordinate)[2]

        cubic_source = (
            self.p.lambda4
            / self.p.kappa
            * phi**3
        )

        kernel = np.array(
            [
                self.model.coupled_green_kernel(y)
                for y in coordinate
            ]
        )

        reconstructed_delta_n = float(
            np.trapezoid(
                kernel * cubic_source,
                coordinate,
            )
        )

        extraction_scale = (
            self.p.L
            / self.p.x
            / (
                self.p.c_s
                / self.p.c
            ) ** 2
        )

        nonlinear_n_at_x = float(
            self.model.fields(self.p.x)[0]
        )

        linear_n_at_x = (
            self.model.alpha_coupled_linear_response()
            / extraction_scale
        )

        actual_delta_n = (
            nonlinear_n_at_x
            - linear_n_at_x
        )

        self.assertAlmostEqual(
            reconstructed_delta_n,
            actual_delta_n,
            delta=1.0e-12,
        )

        actual_alpha_remainder = abs(
            extraction_scale
            * actual_delta_n
        )

        operator_bound = (
            self.model
            .alpha_cubic_green_operator_bound()
        )

        self.assertLessEqual(
            actual_alpha_remainder,
            operator_bound + 1.0e-15,
        )

    def test_cubic_field_response_bound(self) -> None:
        coordinate = np.linspace(
            0.0,
            self.p.L,
            2001,
        )

        state = self.model.fields(coordinate)
        n_at_x = float(self.model.fields(self.p.x)[0])
        phi_max = float(np.max(np.abs(state[2])))

        sound_ratio_squared = (
            self.p.c_s / self.p.c
        ) ** 2

        beta = (
            self.p.eta
            * sound_ratio_squared
        )

        extraction_scale = (
            self.p.L
            / self.p.x
            / sound_ratio_squared
        )

        field_linearized_alpha = (
            extraction_scale
            * n_at_x
        )

        actual_field_remainder = abs(
            field_linearized_alpha
            - self.model.alpha_coupled_linear_response()
        )

        # Let (delta_n, delta_phi) be the difference between
        # the nonlinear and coupled-linear solutions.
        #
        # Multiplying the difference equations by delta_n
        # and delta_phi gives the coercive energy identity
        #
        #   E_delta
        #     = -lambda4 integral phi^3 delta_phi.
        #
        # Therefore
        #
        #   sqrt(E_delta)
        #     <= |lambda4| ||phi||_infinity^3
        #        sqrt(L / mphi2).
        #
        # The one-dimensional pointwise estimate
        #
        #   |delta_n(x)|
        #     <= sqrt(E_delta) [
        #          1 / sqrt(L mu2)
        #        + |beta| / sqrt(L mphi2)
        #        + sqrt(L / A)
        #     ]
        #
        # then bounds the extracted alpha remainder.

        square_root_energy_bound = (
            abs(self.p.lambda4)
            * phi_max**3
            * math.sqrt(
                self.p.L
                / self.p.mphi2
            )
        )

        pointwise_lapse_factor = (
            1.0
            / math.sqrt(
                self.p.L
                * self.p.mu2
            )
            + abs(beta)
            / math.sqrt(
                self.p.L
                * self.p.mphi2
            )
            + math.sqrt(
                self.p.L
                / self.p.A
            )
        )

        certified_bound = (
            extraction_scale
            * square_root_energy_bound
            * pointwise_lapse_factor
        )

        self.assertLessEqual(
            actual_field_remainder,
            certified_bound + 1.0e-15,
        )

    def test_exponential_remainder_bound(self) -> None:
        n_at_x = float(self.model.fields(self.p.x)[0])
        sound_ratio_squared = (
            self.p.c_s / self.p.c
        ) ** 2

        extraction_scale = (
            self.p.L
            / self.p.x
            / sound_ratio_squared
        )

        field_linearized_alpha = (
            extraction_scale * n_at_x
        )

        actual_remainder = abs(
            self.model.alpha_exact()
            - field_linearized_alpha
        )

        certified_bound = (
            self.model.alpha_exponential_remainder_bound()
        )

        self.assertLessEqual(
            actual_remainder,
            certified_bound + 1.0e-15,
        )

    def test_alpha_extraction_identity(self) -> None:
        n_at_x = float(self.model.fields(self.p.x)[0])

        expected = (
            (self.p.L / self.p.x)
            * (math.exp(n_at_x) - 1.0)
            / (self.p.c_s / self.p.c) ** 2
        )

        self.assertAlmostEqual(
            self.model.alpha_exact(),
            expected,
            places=12,
        )


    def test_carbon_charge_normalization_map(self) -> None:
        trace_energy_j = self.p.M * self.p.c**2
        beta_c = carbon_coupling_from_trace_energy(
            self.p.Q_C,
            trace_energy_j,
        )
        self.assertEqual(
            toy_charge_from_carbon_coupling(
                beta_c,
                trace_energy_j,
            ),
            self.p.Q_C,
        )


    def test_measured_carbon_profiles_require_arrays(self) -> None:
        radius = np.linspace(0.0, 0.5, 9)
        density = np.full_like(radius, 1420.0)
        stress = np.zeros_like(radius)
        with self.assertRaises(TypeError):
            MeasuredCarbonProfiles(
                radius.tolist(),
                density,
                radius,
                stress,
                stress,
            )
        profiles = MeasuredCarbonProfiles(
            radius,
            density,
            radius,
            stress,
            stress,
        )
        self.assertGreater(profiles.mass_kg(), 0.0)
        self.assertGreater(
            profiles.flat_trace_energy_j(self.p.c),
            0.0,
        )


    def test_full_dimensionless_radial_model(self) -> None:
        reference_mass_kg = 1000.0
        reference_density_kg_m3 = 1420.0
        reference_radius_m = (
            3.0
            * reference_mass_kg
            / (4.0 * math.pi * reference_density_kg_m3)
        ) ** (1.0 / 3.0)
        radius = np.linspace(0.0, reference_radius_m, 401)
        density = np.full_like(
            radius,
            reference_density_kg_m3,
        )
        stress = np.zeros_like(radius)
        profiles = MeasuredCarbonProfiles(
            radius,
            density,
            radius,
            stress,
            stress,
        )
        radial_model = DimensionlessRadialCarbonModel(
            profiles
        ).solve()
        self.assertTrue(radial_model.solution_success)
        state = radial_model.fields(
            np.array([1.0e-6, 1.0, 20.0])
        )
        self.assertTrue(np.all(np.isfinite(state)))
        self.assertGreater(radial_model.trace_energy_j, 0.0)
        self.assertEqual(
            toy_charge_from_carbon_coupling(
                radial_model.beta_c,
                radial_model.trace_energy_j,
            ),
            radial_model.q_c_toy_j,
        )


    def test_experimental_no_go_registry(self) -> None:
        trace_energy_j = (
            REFERENCE_CARBON_MASS_KG * self.p.c**2
        )
        computed = normalization_compatible_no_go_acceleration(
            REFERENCE_TOY_CHARGE_J,
            trace_energy_j,
            REFERENCE_CARBON_MASS_KG,
            REFERENCE_OBSERVER_RADIUS_M,
            self.p.G,
        )
        self.assertTrue(
            math.isclose(
                computed,
                EXPERIMENTAL_NO_GO_ACCELERATION_M_S2,
                rel_tol=1.0e-12,
                abs_tol=0.0,
            )
        )
        budget = CarbonControlDifferentialErrorBudget(
            statistical_m_s2=(
                EXPERIMENTAL_NO_GO_ACCELERATION_M_S2 / 10.0
            )
        )
        self.assertTrue(budget.satisfies_five_sigma())


def report() -> None:
    model = ToyGravityModel().solve()
    p = model.p

    coordinate = np.linspace(0.0, p.L, 2001)
    lapse_density, scalar_density = (
        model.energy_densities(coordinate)
    )

    n_at_x, _, phi_at_x, _ = model.fields(p.x)

    print("RESULT := nonlinear toy scalar-lapse model converged")
    print(f"Q_C_J := {p.Q_C:.12g}")
    print(f"N_AT_X := {math.exp(float(n_at_x)):.12g}")
    print(f"PHI_AT_X := {float(phi_at_x):.12g}")
    print(f"BULK_ENERGY_J := {model.total_bulk_energy():.12g}")

    print(
        "MIN_LAPSE_DENSITY_J_PER_M := "
        f"{np.min(lapse_density):.12g}"
    )

    print(
        "MIN_SCALAR_DENSITY_J_PER_M := "
        f"{np.min(scalar_density):.12g}"
    )

    print(
        f"MAX_ODE_RESIDUAL := "
        f"{model.maximum_ode_residual():.12g}"
    )

    print(f"M_EFFECTIVE_KG := {model.effective_mass():.12g}")
    print(f"G_BASE_M_PER_S2 := {model.base_gravity():.12g}")
    print(f"TOY_G_V_M_PER_S2 := {model.gravity():.12g}")
    print("PHYSICAL_FORCE_ENHANCEMENT := REJECTED")
    print(
        "REJECTED_PHYSICAL_FORCE_ENHANCEMENT := "
        f"{REJECTED_PHYSICAL_FORCE_ENHANCEMENT:.12g}"
    )
    alpha_exact = model.alpha_exact()
    alpha_coupled_linear = (
        model.alpha_coupled_linear_response()
    )

    actual_total_remainder = abs(
        alpha_exact
        - alpha_coupled_linear
    )

    total_remainder_enclosure = (
        model.alpha_total_remainder_arb_enclosure(
            subdivisions_per_segment=256,
            precision_bits=256,
        )
    )

    total_remainder_certified_upper = float(
        total_remainder_enclosure.upper()
    )

    print(f"ALPHA_EXACT := {alpha_exact:.12g}")

    print(
        "ALPHA_COUPLED_LINEAR := "
        f"{alpha_coupled_linear:.12g}"
    )

    print(
        "ACTUAL_TOTAL_REMAINDER := "
        f"{actual_total_remainder:.12g}"
    )

    print(
        "TOTAL_REMAINDER_CERTIFIED_UPPER := "
        f"{total_remainder_certified_upper:.12g}"
    )

    print(
        "TOTAL_REMAINDER_ARB_ENCLOSURE := "
        f"{total_remainder_enclosure.str(30)}"
    )

    print(
        f"ALPHA_LINEAR_LIMIT := "
        f"{model.alpha_linear_limit():.12g}"
    )

    print("NORMALIZATION_MAP := Q_C_TOY = BETA_C * E_TR")
    print(
        "RADIAL_MODEL_INPUT := "
        "EXTERNAL_CT_DENSITY_AND_RESIDUAL_STRESS_ARRAYS_REQUIRED"
    )
    print(
        "EXPERIMENTAL_NO_GO_ACCELERATION_M_PER_S2 := "
        f"{EXPERIMENTAL_NO_GO_ACCELERATION_M_S2:.12g}"
    )
    print(
        "FIVE_SIGMA_DIFFERENTIAL_BUDGET_M_PER_S2 := "
        f"{EXPERIMENTAL_NO_GO_ACCELERATION_M_S2 / 5.0:.12g}"
    )
    print(
        "BOUNDARY := toy enhancement rejected physically; "
        "no-go bound is conditional on universal massless long-range coupling"
    )


if __name__ == "__main__":
    if "--test" in sys.argv:
        sys.argv = [sys.argv[0]]
        unittest.main(verbosity=2)
    else:
        report()
