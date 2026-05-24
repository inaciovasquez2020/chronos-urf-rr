namespace Chronos
namespace Frontier

/--
Derived black-hole scale values map only.

This records seven value layers derived from the Schwarzschild radius scale:

1. light crossing time
2. horizon area
3. surface gravity
4. mean density
5. tidal gradient
6. Hawking temperature
7. optical domain sweep by mass

Boundary: scale values only. It is not a theorem input and does not prove
gravity closure, the physical Einstein-matter flux identity, Chronos-RR,
H4.1/FGL, P vs NP, or any Clay problem.
-/
structure BlackHoleDerivedScaleValuesMap where
  schwarzschildRadiusFormula : String
  lightCrossingTimeFormula : String
  horizonAreaFormula : String
  surfaceGravityFormula : String
  meanDensityFormula : String
  tidalGradientFormula : String
  hawkingTemperatureFormula : String
  opticalDomainSweep : String
  admissibleUse : String
  forbiddenUse : List String
  scaleValuesOnlyNotTheoremInput : Prop

def blackHoleDerivedScaleValuesMap :
  BlackHoleDerivedScaleValuesMap where
    schwarzschildRadiusFormula := "r_s = 2GM/c^2"
    lightCrossingTimeFormula := "t_s = r_s/c and t_100 = 100 r_s/c"
    horizonAreaFormula := "A = 4*pi*r_s^2"
    surfaceGravityFormula := "kappa = c^4/(4GM)"
    meanDensityFormula := "rho = 3M/(4*pi*r_s^3)"
    tidalGradientFormula := "tidal scale = 2GM/r_s^3"
    hawkingTemperatureFormula := "T_H = hbar*c^3/(8*pi*G*M*k_B)"
    opticalDomainSweep := "domain = {10 r_s, 100 r_s, 1000 r_s}"
    admissibleUse := "derived scale values for interpreting dimensionless optical metric profiles at black-hole scales"
    forbiddenUse := [
      "theorem input",
      "gravity closure evidence",
      "physical Einstein-matter flux identity proof",
      "restricted analytic estimate package assumption proof",
      "Chronos-RR evidence",
      "H4.1/FGL evidence",
      "P vs NP evidence",
      "Clay-problem evidence"
    ]
    scaleValuesOnlyNotTheoremInput := True

theorem black_hole_derived_scale_values_map_boundary_closed :
  blackHoleDerivedScaleValuesMap.scaleValuesOnlyNotTheoremInput := by
  trivial

example :
  blackHoleDerivedScaleValuesMap.lightCrossingTimeFormula =
    "t_s = r_s/c and t_100 = 100 r_s/c" := by
  rfl

example :
  blackHoleDerivedScaleValuesMap.horizonAreaFormula =
    "A = 4*pi*r_s^2" := by
  rfl

example :
  blackHoleDerivedScaleValuesMap.opticalDomainSweep =
    "domain = {10 r_s, 100 r_s, 1000 r_s}" := by
  rfl

end Frontier
end Chronos
