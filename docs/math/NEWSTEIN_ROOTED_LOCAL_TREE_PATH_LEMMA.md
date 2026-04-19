# Newstein Rooted-Local Tree-Path Lemma

Status: PROVED

## Statement

Let \(L\) be a rooted local complex and let \(T\subseteq L\) be a spanning tree. Assume:

1. every edge of \(T\) is rooted-local in \(L\);
2. the rooted-local condition is closed under unique tree-path concatenation in \(T\).

Then for every non-tree edge \(e=uv\in E(L)\setminus E(T)\), the unique tree path \(P_T(u,v)\subseteq T\) is rooted-local in \(L\).

## Proof

Fix \(e=uv\in E(L)\setminus E(T)\). Since \(T\) is a tree, there is a unique tree path \(P_T(u,v)\subseteq T\) joining \(u\) and \(v\). By assumption, every edge of \(T\) is rooted-local in \(L\). By closure of rooted-locality under unique tree-path concatenation in \(T\), the concatenation of the rooted-local edges along the unique path \(P_T(u,v)\) is rooted-local. Therefore \(P_T(u,v)\) is rooted-local in \(L\).

## Status

PROVED

## Finish condition

Closed.
