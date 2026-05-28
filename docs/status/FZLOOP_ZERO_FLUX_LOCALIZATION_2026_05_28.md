# FZloop Zero-Flux Localization — 2026-05-28

Status: `FZLOOP_ZERO_FLUX_LOCALIZATION_PROVED_FINITE_NONNEGATIVE_MODEL_ONLY`

## Object

`FZloop` is a finite cyclic nonnegative flux-sector model.

## Proved internal lemma

If the total FZloop flux is zero, then every nonnegative flux sector is zero.

Lean theorem:

`FZLoop.zero_flux_localization`

## Intended gravity use

This is a localization primitive for restricted stationary gravity estimates: if a Komar/Hawking-type boundary flux decomposes into nonnegative sectors and the total boundary flux vanishes, then every sector must vanish.

## Boundary

This artifact proves only a finite nonnegative model lemma.

It does not prove a Komar sign theorem, a Hawking mass theorem, the restricted estimate, the coercive estimate, an analytic estimate, an Einstein-matter theorem, a collapse theorem, Cosmic Censorship, the Hoop Conjecture, quantum gravity, unrestricted Chronos-RR, unrestricted H4.1/FGL, P vs NP, or any Clay problem.
