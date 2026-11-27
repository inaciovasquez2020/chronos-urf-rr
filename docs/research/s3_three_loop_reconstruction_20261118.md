# Sharp three-loop reconstruction in the finite S3 model

2026-11-18. Base: 7c029d0a628202a4f86619b9f05eb90b14e17bec.
Extends the independent-local conjugacy obstruction in
`docs/research/nonabelian_relative_gauge_obstruction_20261113.md`.
This is a paper proof for a finite group, not a continuum spacetime theorem.

## Theorem

For every finite ordered tuple x in S3^k, its simultaneous-conjugacy orbit is
determined by the conjugacy classes of x_i, x_i x_j (i<j), and x_i x_j x_l
(i<j<l). All products use a common root identification. The maximal word
length three is sharp in general, even if all words of length at most two
in entries and their inverses are available.

## Proof

Conjugacy classes distinguish identity, transpositions and nonidentity
3-cycles. For two transpositions their product is identity iff they are
equal. Thus the single and pair observations determine the partition of
transposition indices by equality. Conjugation by S3 induces the full
symmetric group on its three transpositions (the action is faithful and
both groups have order six). Consequently two tuples with equal
observations can first be aligned at every transposition index.

If there are no 3-cycle entries, this completes the argument.
Otherwise, pair products of 3-cycles determine their equality pattern:
the two nonidentity rotations multiply to identity iff distinct.
It therefore suffices to align one 3-cycle entry.

If the tuple contains zero distinct transpositions, conjugation by any
transposition exchanges the two rotations. If it contains exactly one
distinct transposition, conjugation by that transposition exchanges them
while preserving all aligned transpositions. In either case alignment
is possible.

If at least two distinct transpositions occur, fix their indices i,j
and any rotation index l. The triple product with indices sorted can be
cyclically permuted without changing its conjugacy class, so it has class
of ab c or ba c, where a,b are the fixed distinct transpositions and c is
the rotation; the order of a,b is fixed by the indices. The product of
the two transpositions is a nonidentity rotation d. Exactly one of
the two possible rotations c gives dc=1; the other gives a nonidentity
rotation. The triple observation therefore determines c uniquely.
All remaining rotation entries are fixed by their pair equality
pattern. The aligned tuples coincide. Conversely simultaneous
conjugacy preserves every observed class. QED.

Sharpness: let a=(12), b=(23), c=ab and compare (a,b,c) with
(a,b,c^-1). Singles and all length-two words (including inverses,
repeated indices, and either order) have equal classes: mixed
transposition-rotation products are transpositions; rotation squares
are rotations; opposite inverse powers cancel; transposition-only
words are unchanged. No common conjugating element exists, because
the centralizers of the two distinct transpositions intersect only
in the identity. The triple product distinguishes the tuples:
ab c^-1=1 whereas ab c=c^2 != 1.

## Reproducible finite audit

Run the following dependency-free JavaScript with Node.js (or equivalent
standard ECMAScript runtime). The finite bound is k<=5; the paper proof
above has no such bound. Each signature is mapped to its canonical
simultaneous-conjugacy representative. A collision or unexpected orbit
count throws an error.

```javascript
const G=["012","021","102","120","201","210"];
const m=(a,b)=>[...b].map(i=>a[+i]).join("");
const inv=a=>G.find(b=>m(a,b)==="012");
const c=a=>a==="012"?0:m(a,a)==="012"?1:2;
const expected=[3,11,49,251,1393];
let n=0;
for(let k=1;k<=5;k++){
  let seen=new Map();
  let walk=x=>{
    if(x.length<k){for(const a of G)walk([...x,a]);return;}
    let s=x.map(c);
    for(let i=0;i<k;i++)for(let j=i+1;j<k;j++)
      s.push(c(m(x[i],x[j])));
    for(let i=0;i<k;i++)for(let j=i+1;j<k;j++)
      for(let l=j+1;l<k;l++)s.push(c(m(m(x[i],x[j]),x[l])));
    let key=s.join("");
    let canon=G.map(g=>x.map(a=>m(m(g,a),inv(g))).join("")).sort()[0];
    if(seen.has(key)&&seen.get(key)!==canon)throw Error("collision");
    seen.set(key,canon);n++;
  };
  walk([]);
  if(seen.size!==expected[k-1])throw Error("orbit count");
  console.log(k,seen.size);
}
if(n!==9330)throw Error("assignment count");
console.log("PASS",n);
```

Isolated ECMAScript enumeration of the same algorithm returned orbit
counts 3, 11, 49, 251, 1393 and 9330 assignments, with no collision.
The exhaustive audit is not the universal proof.

## Scope

A common-root *mixed* product observation is extra information, not
implied by independently gauge-quotiented loop observations.
This result identifies an exact sufficient and sharp maximum word
length in the abstract S3 model; it does not establish that such
observations are physically measurable or radius-local, nor that the
same bound holds for arbitrary gauge groups. Continuum reconstruction,
physical coupling, and 5D necessity remain OPEN. Lean NOT_RUN;
independent external review and literature novelty NOT_ESTABLISHED.
No local Mac state was inspected.
