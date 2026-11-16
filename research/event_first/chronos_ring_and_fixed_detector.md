# Chronos physical analog and fixed-detector cutoff

## Build specification

Use a closed, uniform acoustic duct with circumference L. Put a pulse driver at the origin and matched pressure probes at L/6 and L/3 along the loop. Use a common trigger and record both traces. Measure the propagation speed c in the assembled loop. Set the decision deadline to L/(4c) after the source trigger. In the ideal one-dimensional wave model, the first fronts reach the two probes at L/(6c) and L/(3c). This leaves L/(12c) clearance on either side of the deadline.

Use a narrow source port and operate in the duct's frequency range below the first transverse-mode cutoff. Calibrate the driver, probes, and acquisition chain first. Record a driver-off trace and swap the probes to check channel bias. Include source duration, port and probe size, trigger uncertainty, measured group delay, and speed uncertainty in the timing budget. Keep their combined tolerance below L/(12c). Measure the signal and noise floors on the assembled hardware before applying an amplitude decision. Duct losses, reflections at taps, and electromagnetic pickup are experimental variables.

With y = 2πx/L and T = 2πct/L, the ideal rescaled equation is the circle wave equation. A unit impulsive forcing with zero initial field gives the ideal normalized step of 1/2 after its first front. The waveform depends on the driver transfer function. Validate that transfer function before comparing measured amplitudes with the ideal step. For ideal point forcing, at T = π/2 and angles π/3 and 2π/3, the least symmetric Fourier cutoff giving absolute error below 1/480 at both probes is 75. The arithmetic replay checks this ideal comparison. The duct demonstrates the circle timing mechanism in one spatial dimension. The Chronos local scalar calculation below includes three additional spatial directions. Hardware has not been built or measured.

## Fixed local Chronos detector

Use the merged Chronos model with nominal conformal delay π/2, ordinary spatial centers coincident, and angular separations π/3 and 2π/3. Fix any matching, separable, nonnegative smooth profiles of unit integral with time half-width and combined spatial support radius at most 1/6000 in conformal units. This is a fixed-aperture design. The result is uniform over those profiles.

The detector reports a signal when the response magnitude exceeds 1/240. With readout error strictly below 1/480, use near magnitude greater than 1/160 and far magnitude less than 1/480 as the acceptance margins. The first cutoff meeting both margins is N = 13 (27 Fourier indices, or one zero mode and 13 conjugate pairs). Each smaller cutoff fails at least one of the two margins throughout this profile family. The result uses a fixed deadline. It evaluates the detector decision under the prescribed margin criterion.

For point supports, the contribution from a pair of modes ±n is −n J₁(nπ/2) cos(nδ)/(2π³). The zero mode vanishes inside the ordinary light cone. Let ρ = 1/6000. Write τ for the time offset difference, α for the angular offset difference, and z for the ordinary proper separation. Then |τ| and |α| are at most 2ρ, |z − π/2| ≤ 3ρ, and |z − π/2 − τ| ≤ 2ρ². Matching profiles give E[τ] = E[α] = 0.

The Bessel integral gives |J₁|, |J₁′| and |J₁″| at most one. On z ≥ 1, the paired radial coefficient and its first two derivatives have bounds n/36, n(n+1)/36 and n(n²+2n+2)/36. Taylor expansion about the nominal delay and angle cancels the linear terms in τ and α after averaging. The replay bounds the remaining radial shift, the two quadratic remainders and the product of the two first differences. It also encloses the Bessel series and π. The original certificate used ρ = 10⁻⁸.

## Exact arithmetic replay

```python
from fractions import Fraction as F

p = F("3.14159265358979323846")
pi_error = F(1, 10**20)
def atan_bracket(x):
    terms = [(-1)**k * x**(2*k+1) / (2*k+1) for k in range(24)]
    lower = sum(terms)
    return lower, lower + x**49 / 49

a_lo, a_hi = atan_bracket(F(1, 5))
b_lo, b_hi = atan_bracket(F(1, 239))
# Machin's identity: pi = 16 atan(1/5) - 4 atan(1/239).
assert p-pi_error < 16*a_lo-4*b_hi <= 16*a_hi-4*b_lo < p+pi_error
rho = F(1, 6000)
cosines = (F(1), F(1, 2), F(-1, 2), F(-1), F(-1, 2), F(1, 2))

def bessel_j1(x):
    term = x / 2
    total = term
    for k in range(1, 81):
        term *= -x*x / (4*k*(k+1))
        total += term
    ratio = x*x / (4*81*82)
    assert ratio < 1
    return total, abs(term * ratio)

near = far = radius = F(0)
for n in range(14):
    if n:
        value, error = bessel_j1(n*p/2)
        weight = -n*value / (2*p**3)
        near += weight * cosines[n % 6]
        far += weight * cosines[(2*n) % 6]
        radius += n*(error + (n+1)*pi_error)/54
        radius += rho**2 * (
            2*n*(n+1) + F(9, 2)*n*(n*n+2*n+2)
            + 6*n*n*(n+1) + 2*n**3
        ) / 36
    if n < 13:
        assert abs(near)+radius < F(1, 160) or abs(far)-radius > F(1, 480)
    else:
        assert abs(near)-radius > F(1, 160)
        assert abs(far)+radius < F(1, 480)
print("FIXED_LOCAL_CUTOFF = 13")

sine_cosine_sum = F(0)
for n in range(76):
    if n % 2:
        sine_cosine_sum += (-1)**((n-1)//2) * cosines[n % 6] / n
    distances = sorted(F(1, 4) - sine_cosine_sum / endpoint
                       for endpoint in (p-pi_error, p+pi_error))
    low, high = distances
    if n < 75:
        assert low > F(1, 480) or high < -F(1, 480)
    else:
        assert -F(1, 480) < low <= high < F(1, 480)
print("IDEAL_RING_CUTOFF = 75")
```

The fixed local cutoff applies to the declared narrow profiles and margin criterion. The ideal ring cutoff applies to the specified point-forcing circle model and absolute waveform error at the two declared samples. A physical coupling to a cosmological circle remains open.
