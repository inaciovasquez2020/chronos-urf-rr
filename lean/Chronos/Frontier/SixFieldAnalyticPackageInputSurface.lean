namespace Chronos
namespace Frontier

universe u

structure EinsteinMatterPDEModel : Type (u + 1) where
  Spacetime : Type u
  FieldState : Type u
  MatterState : Type u
  EvolutionLaw : FieldState → MatterState → Prop
  ConstraintLaw : FieldState → MatterState → Prop

structure GaugeFixing (M : EinsteinMatterPDEModel.{u}) : Type (u + 1) where
  GaugeState : Type u
  gaugeCondition : M.FieldState → GaugeState → Prop
  gaugeAdmissible : GaugeState → Prop

structure InitialDataClass
    (M : EinsteinMatterPDEModel.{u})
    (G : GaugeFixing M) : Type (u + 1) where
  InitialDatum : Type u
  realizesField : InitialDatum → M.FieldState
  realizesMatter : InitialDatum → M.MatterState
  satisfiesConstraints :
    ∀ I : InitialDatum,
      M.ConstraintLaw (realizesField I) (realizesMatter I)
  satisfiesGauge :
    ∀ I : InitialDatum,
      ∃ γ : G.GaugeState,
        G.gaugeAdmissible γ ∧ G.gaugeCondition (realizesField I) γ

structure EnergyFunctional
    (M : EinsteinMatterPDEModel.{u})
    (G : GaugeFixing M)
    (C : InitialDataClass M G) : Type (u + 1) where
  EnergyValue : Type u
  energy : C.InitialDatum → EnergyValue
  energyFinite : C.InitialDatum → Prop
  controlsEvolution : C.InitialDatum → Prop

structure BootstrapEnergyCloses
    {M : EinsteinMatterPDEModel.{u}}
    {G : GaugeFixing M}
    {C : InitialDataClass M G}
    (E : EnergyFunctional M G C) : Prop where
  closesBootstrap :
    ∀ I : C.InitialDatum,
      E.energyFinite I → E.controlsEvolution I

structure SixFieldAnalyticPackageInputSurface : Type (u + 1) where
  model : EinsteinMatterPDEModel.{u}
  gauge : GaugeFixing model
  initialDataClass : InitialDataClass model gauge
  energyFunctional : EnergyFunctional model gauge initialDataClass
  bootstrapEnergyCloses : BootstrapEnergyCloses energyFunctional

theorem SixFieldAnalyticPackageInputSurface.has_bootstrap_closure
    (S : SixFieldAnalyticPackageInputSurface.{u}) :
    BootstrapEnergyCloses S.energyFunctional :=
  S.bootstrapEnergyCloses

end Frontier
end Chronos
