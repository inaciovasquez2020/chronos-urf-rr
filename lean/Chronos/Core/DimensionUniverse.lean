structure DimensionUniverse where
  Space : Type
  dimension : Space → Int
  separation : Space → Space → Real


def DimensionUniverse.nontrivial (U : DimensionUniverse) : Prop :=
  ∃ x y : U.Space, U.separation x y ≠ 0

def DimensionUniverse.dimension_jump (U : DimensionUniverse) (x y : U.Space) : Int :=
  U.dimension y - U.dimension x


def DimensionUniverse.curvature_surrogate (U : DimensionUniverse) (x y : U.Space) : Int :=
  U.separation x y + U.dimension_jump x y
