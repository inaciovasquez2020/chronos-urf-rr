#!/usr/bin/env python3
"""Fail-closed exact-rational November 15 harmonic enclosure replay.

No saved matrix logs, hard-coded t/s values, or local absolute paths.
Research evidence only; does not establish geometric assumptions or solve p_(4,2).
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import subprocess
import sys
import tempfile
import shutil
import os
from sympy import Matrix, simplify, Rational

ROOT = Path(__file__).resolve().parent
PINNED_GIT_BLOBS = {
    "chronos_mixed_uv_dipole_exact_20261115.py": "0b120079c94cbf069c70e24304ecf96d611aa5de",
    "chronos_mixed_uv_octupole_exact_20261115.py": "89595f7d3c7857f896d89117f66bfd0bb6590493",
    "chronos_two_sided_harmonic_trace_certificate_20261115.py": "adaa9ff27b10dc049af39d4e71b9474feb7a6529",
    "chronos_mixed_uv_quadrupole_replay_20261115.py": "39fcda74df962793075a4d769c38587bf5e88836",
}
for name, expected in PINNED_GIT_BLOBS.items():
    raw=(ROOT/name).read_bytes()
    got=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest()
    if got != expected:
        raise SystemExit("SOURCE_BLOB_MISMATCH: "+name)
print("GIT_BLOB_PINS := 4/4 PASS",flush=True)

with tempfile.TemporaryDirectory(prefix="chronos-uv-replay-") as tmp:
    wd=Path(tmp)
    for name in PINNED_GIT_BLOBS:
        shutil.copyfile(ROOT/name,wd/name)
    # Existing baseline implementation imports the old, unported filename.
    shutil.copyfile(ROOT/"chronos_mixed_uv_quadrupole_replay_20261115.py",
                    wd/"chronos_mixed_uv_quadrupole_exact_20261115.py")
    original="chronos_mixed_uv_octupole_bounds_20261115.py"
    shutil.copyfile(ROOT/original,wd/original)
    env=os.environ.copy()
    env["PYTHONNOUSERSITE"]="1"
    try:
        proc=subprocess.run([sys.executable,"-E","-B",str(wd/original)],
                            cwd=wd,env=env,capture_output=True,text=True,
                            timeout=180,check=False)
    except subprocess.TimeoutExpired:
        raise SystemExit("INCOMPLETE_TIMEOUT: baseline angular enclosure")
    if proc.returncode:
        print(proc.stdout)
        print(proc.stderr,file=sys.stderr)
        raise SystemExit("BASELINE_REPLAY_FAILED")
    lines=proc.stdout.splitlines()
    def first(prefix):
        hits=[s.split(" ",1)[1] for s in lines if s.startswith(prefix+" ")]
        if len(hits)!=1:
            raise AssertionError(("BASELINE_MARKER",prefix,len(hits)))
        return F(hits[0])
    lo,hi=first("EXACT_LOWER"),first("EXACT_UPPER")
    modes={}
    for line in lines:
        if line.startswith("MODE "):
            parts=line.split()
            assert len(parts)>=6 and parts[2]=="TRACE_COMPRESSION" and parts[4]=="SQUARE_TRACE"
            ell=int(parts[1])
            assert ell not in modes
            modes[ell]=(F(parts[3]),F(parts[5]))
    assert set(modes)==set(range(1,6))
    assert F("0.085411426525")<lo<hi<F("0.085428074196")
    print("BASELINE_REPLAY := PASS",flush=True)

    sys.path.insert(0,str(wd))
    import chronos_mixed_uv_dipole_exact_20261115 as dip
    import chronos_mixed_uv_quadrupole_exact_20261115 as quad

    mons=((0,0),(1,0),(0,1),(2,0),(1,1),(0,2),(3,0),(2,1),(1,2),(0,3))
    def compress(module,ell):
        for i,j in mons:
            if j==0:
                if ell==1:
                    expected=module.kappa(i)*(module.d-module.c)/Rational(2)*(module.c*module.d)**(2*i+2)
                else:
                    expected=module.kappa(i)*(module.d-module.c)**2/Rational(4)*(module.c*module.d)**(2*i+2)
                assert simplify(module.action(i,j)-expected)==0,("ACTION",ell,i,j)
        G=Matrix([[module.gram(*a,*b) for b in mons] for a in mons])
        B=Matrix([[module.energy(*a,*b) for b in mons] for a in mons])
        assert G==G.T and B==B.T and G.det()!=0
        X=G.inv()*B
        t,s=F(str(X.trace())),F(str((X*X).trace()))
        assert 0<s<t*t
        print("MODE_EXACT",ell,"DIM",len(mons),"T",t,"S",s,flush=True)
        return t,s

    for ell,module in [(1,dip),(2,quad)]:
        t,s=compress(module,ell)
        oldt,olds=modes[ell]
        assert t>oldt and s>olds
        mult=F(6,5)*(2*ell+1)
        lo+=mult*(s-olds)
        hi+=mult*((s-olds)-(t*t-oldt*oldt))
    assert lo>F("0.08541223417") and hi<F("0.08542295380") and lo<hi
    print("CERTIFIED_DECIMAL_LOWER := 0.08541223417",flush=True)
    print("CERTIFIED_DECIMAL_UPPER := 0.08542295380",flush=True)
    print("EXACT_RATIONAL_ENCLOSURE := PASS",flush=True)
    print("P42_EXACT := OPEN",flush=True)
    print("LEAN := NOT_RUN",flush=True)
