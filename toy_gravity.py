from __future__ import annotations

from dataclasses import dataclass
import math
import sys
import unittest

import numpy as np
from scipy.integrate import solve_bvp


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
    print(f"G_V_M_PER_S2 := {model.gravity():.12g}")
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

    print(
        "BOUNDARY := positive-energy toy model, "
        "not a derived carbon-gravity theory"
    )


if __name__ == "__main__":
    if "--test" in sys.argv:
        sys.argv = [sys.argv[0]]
        unittest.main(verbosity=2)
    else:
        report()
