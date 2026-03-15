# Chronos / EntropyDepth Quickstart

## Purpose

This document provides a minimal entry point for readers of the Chronos rigidity framework.

## Core Idea

Local refinement algorithms extract only bounded information per step.

If the configuration entropy of a system grows linearly with its size, then resolving that uncertainty requires a linear number of refinement steps.

## Structural Chain

Cycle Rigidity  
→ Configuration Explosion  
→ Entropy Floor  
→ EntropyDepth ≥ Ω(n)  
→ Chronos Wall.

## Key Files

- THEORY_INDEX.md
- STRUCTURE.md
- DEPENDENCY_DAG.md

## Experiments

See:

experiments/

for empirical evidence supporting cycle rigidity and configuration growth.

## Lean Formalization

Lean proof skeletons are located in:

lean/Oblivion/Rigidity/

These files contain the formal verification layer of the rigidity results.
