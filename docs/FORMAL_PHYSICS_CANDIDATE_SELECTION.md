# Formal Physics Candidate Selection

Generated: 2026-07-05T01:06:35Z

## Selection Rule

A candidate may be promoted only if it satisfies `docs/PHYSICS_ADMISSION_STANDARD.md`.

## Candidate Scan

| File | Line | Kind | Name | Statement Head |
|---|---:|---|---|---|
| `.lake/packages/batteries/Batteries/Data/RBMap/Basic.lean` | 177 | `theorem` | `All.imp` | `theorem All.imp (H : ∀ {x : α}, p x → q x) : ∀ {t : RBNode α}, t.All p → t.All q ` |
| `.lake/packages/batteries/Batteries/Data/RBMap/Basic.lean` | 181 | `theorem` | `all_iff` | `theorem all_iff {t : RBNode α} : t.all p ↔ t.All (p ·) := by ` |
| `.lake/packages/batteries/Batteries/Data/RBMap/Basic.lean` | 192 | `theorem` | `any_iff` | `theorem any_iff {t : RBNode α} : t.any p ↔ t.Any (p ·) := by ` |
| `.lake/packages/batteries/Batteries/Data/RBMap/Basic.lean` | 247 | `theorem` | `cmpLT_iff` | `theorem cmpLT_iff [Std.TransCmp cmp] : cmpLT cmp x y ↔ cmp x y = .lt := ` |
| `.lake/packages/batteries/Batteries/Data/RBMap/Basic.lean` | 256 | `theorem` | `cmpEq_iff` | `theorem cmpEq_iff [Std.TransCmp cmp] : cmpEq cmp x y ↔ cmp x y = .eq := ⟨fun ⟨h⟩ => h, (⟨·⟩)⟩ ` |
| `.lake/packages/batteries/Batteries/Data/RBMap/WF.lean` | 27 | `theorem` | `All.trivial` | `theorem All.trivial (H : ∀ {x : α}, p x) : ∀ {t : RBNode α}, t.All p ` |
| `.lake/packages/batteries/Batteries/Data/RBMap/WF.lean` | 31 | `theorem` | `All_and` | `theorem All_and {t : RBNode α} : t.All (fun a => p a ∧ q a) ↔ t.All p ∧ t.All q := by ` |
| `.lake/packages/batteries/Batteries/Data/RBMap/WF.lean` | 37 | `theorem` | `cmpLT.trans` | `theorem cmpLT.trans (h₁ : cmpLT cmp x y) (h₂ : cmpLT cmp y z) : cmpLT cmp x z := ` |
| `.lake/packages/batteries/Batteries/Data/RBMap/WF.lean` | 40 | `theorem` | `cmpLT.trans_l` | `theorem cmpLT.trans_l {cmp x y} (H : cmpLT cmp x y) {t : RBNode α} ` |
| `.lake/packages/batteries/Batteries/Data/RBMap/WF.lean` | 43 | `theorem` | `cmpLT.trans_r` | `theorem cmpLT.trans_r {cmp x y} (H : cmpLT cmp x y) {a : RBNode α} ` |
| `.lake/packages/batteries/Batteries/Data/RBMap/WF.lean` | 46 | `theorem` | `cmpEq.lt_congr_left` | `theorem cmpEq.lt_congr_left (H : cmpEq cmp x y) : cmpLT cmp x z ↔ cmpLT cmp y z := ` |
| `.lake/packages/batteries/Batteries/Data/RBMap/WF.lean` | 49 | `theorem` | `cmpEq.lt_congr_right` | `theorem cmpEq.lt_congr_right (H : cmpEq cmp y z) : cmpLT cmp x y ↔ cmpLT cmp x z := ` |
| `.lake/packages/batteries/Batteries/Data/RBMap/WF.lean` | 55 | `theorem` | `reverse_eq_iff` | `theorem reverse_eq_iff {t t' : RBNode α} : t.reverse = t' ↔ t = t'.reverse := by ` |
| `.lake/packages/batteries/Batteries/Data/RBMap/WF.lean` | 121 | `theorem` | `setBlack_idem` | `theorem setBlack_idem {t : RBNode α} : t.setBlack.setBlack = t.setBlack := by cases t <;> rfl ` |
| `.lake/packages/batteries/Batteries/Data/RBMap/WF.lean` | 162 | `theorem` | `insert_setBlack` | `theorem insert_setBlack {t : RBNode α} : ` |
| `.lake/packages/batteries/Batteries/Data/RBMap/WF.lean` | 226 | `theorem` | `balance1_eq` | `theorem balance1_eq {l : RBNode α} {v : α} {r : RBNode α} ` |
| `.lake/packages/batteries/Batteries/Data/RBMap/WF.lean` | 231 | `theorem` | `balance2_eq` | `theorem balance2_eq {l : RBNode α} {v : α} {r : RBNode α} ` |
| `.lake/packages/batteries/Batteries/Data/RBMap/WF.lean` | 270 | `theorem` | `Balanced.insert` | `theorem Balanced.insert {t : RBNode α} (h : t.Balanced c n) : ` |
| `.lake/packages/batteries/Batteries/Data/RBMap/WF.lean` | 450 | `theorem` | `DelProp.redred` | `theorem DelProp.redred (h : DelProp c t n) : ∃ n', RedRed (c = black) t n' := by ` |
| `.lake/packages/batteries/Batteries/Data/RBMap/WF.lean` | 516 | `theorem` | `WF.out` | `theorem WF.out {t : RBNode α} (h : t.WF cmp) : t.Ordered cmp ∧ ∃ c n, t.Balanced c n := by ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 33 | `theorem` | `parentD_eq` | `theorem parentD_eq {arr : Array UFNode} {i} (h) : ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 36 | `theorem` | `rankD_eq` | `theorem rankD_eq {arr : Array UFNode} {i} (h) : rankD arr i = arr[i].rank := dif_pos _ ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 38 | `theorem` | `parentD_of_not_lt` | `theorem parentD_of_not_lt : ¬i < arr.size → parentD arr i = i := (dif_neg ·) ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 40 | `theorem` | `lt_of_parentD` | `theorem lt_of_parentD : parentD arr i ≠ i → i < arr.size := ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 43 | `theorem` | `parentD_set` | `theorem parentD_set {arr : Array UFNode} {x v i h} : ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 50 | `theorem` | `rankD_set` | `theorem rankD_set {arr : Array UFNode} {x v i h} : ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 124 | `theorem` | `parent'_lt` | `theorem parent'_lt (self : UnionFind) (i : Nat) (h) : self.arr[i].parent < self.size := by ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 127 | `theorem` | `parent_lt` | `theorem parent_lt (self : UnionFind) (i : Nat) : self.parent i < self.size ↔ i < self.size := by ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 133 | `theorem` | `rank_lt` | `theorem rank_lt {self : UnionFind} {i : Nat} : self.parent i ≠ i → ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 136 | `theorem` | `rank'_lt` | `theorem rank'_lt (self : UnionFind) (i h) : self.arr[i].parent ≠ i → ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 143 | `theorem` | `rank'_lt_rankMax` | `theorem rank'_lt_rankMax (self : UnionFind) (i : Nat) (h) : (self.arr[i]).rank < self.rankMax := by ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 150 | `theorem` | `rankD_lt_rankMax` | `theorem rankD_lt_rankMax (self : UnionFind) (i : Nat) : ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 154 | `theorem` | `lt_rankMax` | `theorem lt_rankMax (self : UnionFind) (i : Nat) : self.rank i < self.rankMax := rankD_lt_rankMax .. ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 156 | `theorem` | `push_rankD` | `theorem push_rankD (arr : Array UFNode) : rankD (arr.push ⟨arr.size, 0⟩) i = rankD arr i := by ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 160 | `theorem` | `push_parentD` | `theorem push_parentD (arr : Array UFNode) : parentD (arr.push ⟨arr.size, 0⟩) i = parentD arr i := by ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 198 | `theorem` | `parent_root` | `theorem parent_root (self : UnionFind) (x : Fin self.size) : ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 205 | `theorem` | `parent_rootD` | `theorem parent_rootD (self : UnionFind) (x : Nat) : ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 213 | `theorem` | `rootD_parent` | `theorem rootD_parent (self : UnionFind) (x : Nat) : self.rootD (self.parent x) = self.rootD x := by ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 222 | `theorem` | `rootD_lt` | `theorem rootD_lt {self : UnionFind} {x : Nat} : self.rootD x < self.size ↔ x < self.size := by ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 226 | `theorem` | `rootD_eq_self` | `theorem rootD_eq_self {self : UnionFind} {x : Nat} : self.rootD x = x ↔ self.parent x = x := by ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 230 | `theorem` | `rootD_rootD` | `theorem rootD_rootD {self : UnionFind} {x : Nat} : self.rootD (self.rootD x) = self.rootD x := ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 233 | `theorem` | `rootD_ext` | `theorem rootD_ext {m1 m2 : UnionFind} ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 242 | `theorem` | `le_rank_root` | `theorem le_rank_root {self : UnionFind} {x : Nat} : self.rank x ≤ self.rank (self.rootD x) := by ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 251 | `theorem` | `lt_rank_root` | `theorem lt_rank_root {self : UnionFind} {x : Nat} : ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 278 | `theorem` | `findAux_root` | `theorem findAux_root {self : UnionFind} {x : Fin self.size} : ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 288 | `theorem` | `findAux_s` | `theorem findAux_s {self : UnionFind} {x : Fin self.size} : ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 298 | `theorem` | `rankD_findAux` | `theorem rankD_findAux {self : UnionFind} {x : Fin self.size} : ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 312 | `theorem` | `parentD_findAux` | `theorem parentD_findAux {self : UnionFind} {x : Fin self.size} : ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 326 | `theorem` | `parentD_findAux_rootD` | `theorem parentD_findAux_rootD {self : UnionFind} {x : Fin self.size} : ` |
| `.lake/packages/batteries/Batteries/Data/UnionFind/Basic.lean` | 335 | `theorem` | `parentD_findAux_lt` | `theorem parentD_findAux_lt {self : UnionFind} {x : Fin self.size} (h : i < self.size) : ` |

## Current Selection

No theorem is promoted here. This document records candidates only; promotion requires compiler verification plus observable mapping, domain of validity, and quantitative consequence documentation.

## Experimental Prediction Status

`OPEN_GAP := no admitted theorem yet derives a measurable physical observable consequence.`
