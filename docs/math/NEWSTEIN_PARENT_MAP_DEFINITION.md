# NEWSTEIN_PARENT_MAP_DEFINITION

Status: OPEN

## Definition

Assume the unique-lower-neighbor property holds on the rooted ball (B_R(r)):

[
\forall v\in B_R(r)\setminus{r},\quad
#\Bigl{u\in B_R(r):{u,v}\in E \wedge d(r,u)=d(r,v)-1\Bigr}=1.
]

Define the parent map
[
p : B_R(r)\setminus{r}\to B_R(r)
]
by declaring (p(v)) to be the unique vertex satisfying
[
{p(v),v}\in E
\quad\text{and}\quad
d(r,p(v))=d(r,v)-1.
]

## Immediate consequences

For every (v\in B_R(r)\setminus{r}),
[
{p(v),v}\in E,
\qquad
d(r,p(v))=d(r,v)-1,
\qquad
p(v)\in B_R(r).
]

## Role in the closure chain

This definition is the next structural step after the unique-lower-neighbor lemma.
It rebuilds the canonical parent operator needed for the rooted-tree certificate, local acyclicity, and the local coboundary criterion.
