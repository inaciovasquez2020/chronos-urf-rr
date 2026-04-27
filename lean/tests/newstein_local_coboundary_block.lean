namespace Newstein

constant PropG : Type

constant GeodesicInterpolationClosure : Prop
constant TreePathRootedLocality : Prop
constant FundamentalCycleGeneration : Prop
constant LocalCoboundaryCriterion : Prop

theorem geodesic_to_local_coboundary
    (geodesic_to_tree_path :
      GeodesicInterpolationClosure -> TreePathRootedLocality)
    (tree_path_to_fundamental_cycle :
      TreePathRootedLocality -> FundamentalCycleGeneration)
    (fundamental_cycle_to_local_coboundary :
      FundamentalCycleGeneration -> LocalCoboundaryCriterion) :
    GeodesicInterpolationClosure -> LocalCoboundaryCriterion :=
by
  intro hgeo
  have htp : TreePathRootedLocality := geodesic_to_tree_path hgeo
  have hfc : FundamentalCycleGeneration := tree_path_to_fundamental_cycle htp
  exact fundamental_cycle_to_local_coboundary hfc

end Newstein
