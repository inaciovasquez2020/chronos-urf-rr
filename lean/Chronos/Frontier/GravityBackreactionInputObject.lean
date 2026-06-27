namespace Chronos
namespace Frontier

/--
A minimal input object for gravity progress.

This is not a gravity theorem.  It isolates the weakest missing
scientific structure needed before a metric-backreaction theorem can be
claimed.
-/
structure GravityBackreactionInputObject where
  emergentMetric : Type
  matterSector : Type
  backreactionLaw : emergentMetric → matterSector → emergentMetric

/--
Boundary: existence of this input object alone does not derive gravity.
-/
theorem gravity_backreaction_input_object_not_solution
    (G : GravityBackreactionInputObject) :
    Nonempty G.emergentMetric → Nonempty G.matterSector →
    Nonempty G.emergentMetric := by
  intro hMetric _hMatter
  exact hMetric

end Frontier
end Chronos
