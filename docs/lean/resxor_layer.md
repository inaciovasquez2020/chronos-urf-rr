# ResXor Lean Formalization Layer

## Purpose

The **ResXor layer** provides the Lean formalization infrastructure for reasoning about
XOR-style constraints and cut-vector algebra over $\mathbb{Z}_2$ within the
Chronos–URF refinement framework.

It supplies the algebraic primitives required for:

* GF(2) reasoning in resolution-style arguments
* cycle parity constraints
* cut-vector representations of vertex subsets
* rank exposure arguments used in Chronos / EntropyDepth experiments

This module serves as the **base algebra layer** connecting:

```
Cycle overlap structures
        ↓
GF(2) parity relations
        ↓
Resolution XOR constraints
        ↓
EntropyDepth / Chronos rigidity experiments
```

---

## Core Structures

### Bit Encoding

Logical membership predicates are encoded as elements of $\mathbb{Z}_2$.

```lean
def bit (P : Prop) [Decidable P] : ZMod 2 :=
if P then 1 else 0
```

This enables translation between Boolean predicates and algebraic parity.

---

### Cut Vector Representation

For vertex subsets (U, W \subseteq V):

```lean
def cutVec (U W : Finset V) : V → ZMod 2 :=
fun v => bit (v ∈ U) + bit (v ∈ W)
```

The resulting function assigns each vertex the parity of membership in
two subsets.

Interpretation:

* `0` : vertex belongs to neither or both
* `1` : vertex belongs to exactly one set

This is the algebraic representation of a **symmetric difference cut**.

---

### XOR Set Operator

```lean
def xorSet (U W : Finset V) : Finset V :=
(U \ W) ∪ (W \ U)
```

This defines the symmetric difference of two vertex sets.

The relationship between the algebraic and combinatorial views is:

[
v ∈ U \oplus W \quad \Longleftrightarrow \quad
\text{cutVec}(U,W)(v) = 1
]

---

## Intended Use in Chronos

The ResXor layer is used to formalize parity reasoning appearing in:

* Tseitin-style XOR constraints
* GF(2) rank exposure experiments
* cycle parity constraints
* Oblivion Atom overlap relations

Typical reasoning pattern:

```
Cycle overlap
      ↓
Parity constraint system
      ↓
GF(2) linear structure
      ↓
Resolution / refinement hardness
```

---

## Integration Targets

This module is designed to support the following formal layers:

| Layer          | Role                          |
| -------------- | ----------------------------- |
| `ResXor`       | GF(2) algebra primitives      |
| `CycleParity`  | cycle parity constraints      |
| `OverlapRank`  | overlap → rank arguments      |
| `EntropyDepth` | refinement information bounds |
| `Chronos`      | rigidity framework            |

---

## Status

**Version:** v1
**Repository Tag:** `lean-resxor-v1`

Current guarantees:

* Lean module compiles successfully
* Base algebra primitives implemented
* Compatible with current Lean toolchain

Future extensions will include:

* GF(2) rank reasoning
* XOR constraint systems
* Tseitin parity constructions
* cycle-space linear algebra

---

## Role in the URF Program

The ResXor formalization layer supplies the algebraic substrate for
expressing **parity-based rigidity arguments** that appear across the
Chronos / EntropyDepth / Oblivion Atom framework.

It provides the formal bridge between:

* combinatorial graph structure
* GF(2) algebra
* resolution complexity
* entropy-based lower bounds

This layer therefore functions as the **GF(2) algebra kernel** of the
Lean verification stack used in the Chronos–URF program.

