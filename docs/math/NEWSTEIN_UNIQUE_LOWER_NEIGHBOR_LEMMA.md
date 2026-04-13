# NEWSTEIN_UNIQUE_LOWER_NEIGHBOR_LEMMA

Status: OPEN

## Statement

Let (B_R(r)) be the rooted ball of radius (R) about root (r).
The next missing object is the unique-lower-neighbor lemma:

[
\forall v\in B_R(r)\setminus{r},\quad
#\Bigl{u\in B_R(r):{u,v}\in E \wedge d(r,u)=d(r,v)-1\Bigr}=1.
]

## Role in the closure chain

This is the weakest sufficient local rooted-tree input for rebuilding the parent map.
Once proved, it supports the rooted-tree certificate, local acyclicity, and the local coboundary step.
