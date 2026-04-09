# Local Indistinguishability Certificate

## Target
Certify that the witness pair (G_n^+, G_n^-) is FO^k-locally indistinguishable at radius R.

## Required Components
1. rooted ball extraction
2. local type encoding
3. witness-pair comparison interface
4. finite certificate format
5. radius and parameter registry

## Core Statement
For fixed k and R, and for all n in the witness family:
Type_{k,R}(G_n^+) = Type_{k,R}(G_n^-)

## Blocking Gap
Need explicit rooted-ball encoding and certified witness-family instances.
