namespace Chronos
namespace Frontier

/--
Observational context classes for the gravity strand.

This file records public black-hole observation classes as motivation only.
It is not used as a proof input and does not promote any gravity theorem.
-/
inductive BlackHoleObservationClass where
  | stellarCollapseThreshold
  | supermassiveGrowthConstraint
  | episodicJetFeedback
  | mergerRestructuring
  | activeResearchVenue
  deriving Repr, DecidableEq

/--
A source-level observational context record.

`usableAsProofInput = False` is intentional: these records motivate theorem
targets but do not certify any Lean theorem, analytic estimate, collapse gate,
cosmic-censorship claim, hoop-conjecture claim, Chronos-RR claim, H4.1/FGL
claim, P-vs-NP claim, or Clay-problem claim.
-/
structure BlackHoleObservationalMotivation where
  sourceName : String
  sourceURL : String
  observationClass : BlackHoleObservationClass
  gravityMotivation : String
  usableAsProofInput : Bool
  deriving Repr

def nasaNEOWISEFailedSupernovaMotivation : BlackHoleObservationalMotivation :=
  { sourceName := "NASA NEOWISE M31-2014-DS1 failed-supernova black-hole birth context"
    sourceURL := "https://science.nasa.gov/blogs/science-news/2026/02/12/archival-data-from-nasas-neowise-tracks-star-turning-into-black-hole/"
    observationClass := BlackHoleObservationClass.stellarCollapseThreshold
    gravityMotivation := "Motivates collapse-threshold and inward-failure framing for restricted gravity-collapse targets."
    usableAsProofInput := false }

def chandraSMBHGrowthSlowdownMotivation : BlackHoleObservationalMotivation :=
  { sourceName := "Chandra supermassive black-hole growth slowdown context"
    sourceURL := "https://chandra.harvard.edu/photo/2026/bhgrowth/"
    observationClass := BlackHoleObservationClass.supermassiveGrowthConstraint
    gravityMotivation := "Motivates feeding-capacity and growth-rate constraint framing for black-hole systems."
    usableAsProofInput := false }

def j1007EpisodicAGNMotivation : BlackHoleObservationalMotivation :=
  { sourceName := "J1007+3540 reborn black-hole episodic AGN jet context"
    sourceURL := "https://www.space.com/astronomy/black-holes/reborn-black-hole-seen-erupting-across-1-million-light-years-of-space-like-a-cosmic-volcano"
    observationClass := BlackHoleObservationClass.episodicJetFeedback
    gravityMotivation := "Motivates boundary-environment feedback and regime-switching language for gravity frontiers."
    usableAsProofInput := false }

def abell402BCGMergerMotivation : BlackHoleObservationalMotivation :=
  { sourceName := "Abell 402-BCG ultramassive black-hole pair merger context"
    sourceURL := "https://www.sciencenews.org/article/largest-pair-black-holes-collision"
    observationClass := BlackHoleObservationClass.mergerRestructuring
    gravityMotivation := "Motivates merger-driven geometry and matter-restructuring context."
    usableAsProofInput := false }

def aasSMBH2026VenueMotivation : BlackHoleObservationalMotivation :=
  { sourceName := "AAS Supermassive Black Holes and Blue Notes 2026 venue context"
    sourceURL := "https://aas.org/events/2025-09/supermassive-black-holes-and-blue-notes-international-conference"
    observationClass := BlackHoleObservationClass.activeResearchVenue
    gravityMotivation := "Records active scientific context for event-horizon observations, feeding, feedback, and SMBH formation/growth."
    usableAsProofInput := false }

def blackHoleObservationalMotivationRegistry :
    List BlackHoleObservationalMotivation :=
  [ nasaNEOWISEFailedSupernovaMotivation
  , chandraSMBHGrowthSlowdownMotivation
  , j1007EpisodicAGNMotivation
  , abell402BCGMergerMotivation
  , aasSMBH2026VenueMotivation
  ]

def blackHoleObservationalMotivationRegistryStatus : String :=
  "OBSERVATIONAL_MOTIVATION_REGISTRY_ONLY_NO_THEOREM_PROMOTION"

theorem blackHoleObservationalMotivationRegistry_notProofInput :
    nasaNEOWISEFailedSupernovaMotivation.usableAsProofInput = false ∧
    chandraSMBHGrowthSlowdownMotivation.usableAsProofInput = false ∧
    j1007EpisodicAGNMotivation.usableAsProofInput = false ∧
    abell402BCGMergerMotivation.usableAsProofInput = false ∧
    aasSMBH2026VenueMotivation.usableAsProofInput = false := by
  simp [
    nasaNEOWISEFailedSupernovaMotivation,
    chandraSMBHGrowthSlowdownMotivation,
    j1007EpisodicAGNMotivation,
    abell402BCGMergerMotivation,
    aasSMBH2026VenueMotivation
  ]

end Frontier
end Chronos
