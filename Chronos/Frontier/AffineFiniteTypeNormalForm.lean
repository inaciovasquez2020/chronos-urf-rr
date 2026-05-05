namespace Chronos
namespace Frontier

structure ChronosSkeleton (k delta r n rho B : Nat) where
  amul : ((Fin n) -> Bool) -> ((Fin rho) -> Bool)
  b : (Fin rho) -> Bool
  rho_bound : rho <= B

def ChronosCons {k delta r n rho B : Nat}
    (S : ChronosSkeleton k delta r n rho B)
    (W : (Fin n) -> Bool) : Prop :=
  S.amul W = S.b

structure ChronosCertificate {k delta r n rho B : Nat}
    (S : ChronosSkeleton k delta r n rho B) where
  w : (Fin n) -> Bool
  valid : ChronosCons S w

def ChronosEmbedding {k delta r n rho B : Nat}
    {S : ChronosSkeleton k delta r n rho B}
    (C : ChronosCertificate S) : (Fin n) -> Bool :=
  C.w

def ChronosCertificateOfWitness {k delta r n rho B : Nat}
    (S : ChronosSkeleton k delta r n rho B)
    (W : (Fin n) -> Bool)
    (hW : ChronosCons S W) : ChronosCertificate S :=
  { w := W, valid := hW }

theorem chronos_cons_explicit {k delta r n rho B : Nat}
    (S : ChronosSkeleton k delta r n rho B)
    (W : (Fin n) -> Bool) :
    ChronosCons S W = (S.amul W = S.b) :=
  rfl

theorem chronos_certificate_embedding_of_witness {k delta r n rho B : Nat}
    (S : ChronosSkeleton k delta r n rho B)
    (W : (Fin n) -> Bool)
    (hW : ChronosCons S W) :
    ChronosEmbedding (ChronosCertificateOfWitness S W hW) = W :=
  rfl

structure FiniteLocalType (B : Nat) where
  theta : Type
  code : theta -> Fin B
  code_injective : forall a b : theta, code a = code b -> a = b

structure ChronosHistory where
  step : Nat

structure ChronosOneStepData {k delta r n rho B : Nat}
    (S : ChronosSkeleton k delta r n rho B)
    (LT : FiniteLocalType B) where
  tau : ChronosCertificate S -> LT.theta
  y : Nat -> ChronosHistory -> ChronosCertificate S -> Nat
  f : Nat -> ChronosHistory -> LT.theta -> Nat
  factor : forall i H C, y i H C = f i H (tau C)

theorem one_step_factorization {k delta r n rho B : Nat}
    {S : ChronosSkeleton k delta r n rho B}
    {LT : FiniteLocalType B}
    (D : ChronosOneStepData S LT)
    (i : Nat)
    (H : ChronosHistory)
    (C : ChronosCertificate S) :
    D.y i H C = D.f i H (D.tau C) :=
  D.factor i H C

structure AffineFiniteTypeNormalForm
    (k delta r n rho B : Nat) where
  s : ChronosSkeleton k delta r n rho B
  lt : FiniteLocalType B
  stepData : ChronosOneStepData s lt

theorem affine_finite_type_normal_form_is_structural_only
    {k delta r n rho B : Nat}
    (_NF : AffineFiniteTypeNormalForm k delta r n rho B) :
    True :=
  trivial

end Frontier
end Chronos
