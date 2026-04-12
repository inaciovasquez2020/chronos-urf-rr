# Newstein Parent Depth Decrement Proof Blueprint

## Status
OPEN

## Objective
Prove, for every non-root vertex \(v\) of the rooted tree \(T\),
\[
\operatorname{depth}_T(\operatorname{par}_T(v))=\operatorname{depth}_T(v)-1.
\]

## Inputs
1. A rooted tree \(T\) with root \(r\).
2. The parent map \(\operatorname{par}_T\) on non-root vertices.
3. The depth function \(\operatorname{depth}_T(v)=d_T(r,v)\).
4. Uniqueness of simple paths in trees.

## Micro-fix route
### Step 1
Show that for every non-root vertex \(v\), the vertex \(\operatorname{par}_T(v)\) lies on the unique \(r\)-to-\(v\) path.

### Step 2
Show that the unique \(r\)-to-\(v\) path is the concatenation of:
- the unique \(r\)-to-\(\operatorname{par}_T(v)\) path, and
- the edge \((\operatorname{par}_T(v),v)\).

### Step 3
Take lengths of the concatenated path and conclude
\[
d_T(r,v)=d_T(r,\operatorname{par}_T(v))+1.
\]

### Step 4
Rewrite in depth notation to obtain
\[
\operatorname{depth}_T(\operatorname{par}_T(v))=\operatorname{depth}_T(v)-1.
\]

## Immediate downstream discharge
\[
\mathrm{ParentDepthDecrement\ proof}
\Longrightarrow
\mathrm{RootedDistanceMonotonicity}.
\]

## Locked next theorem
The next theorem to rebuild after this proof is the rooted-distance monotonicity statement.
