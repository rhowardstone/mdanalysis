"""A/B benchmark: OLD (develop, serial) vs NEW (this branch, OpenMP) nsgrid.search.

Uses REAL water-oxygen coordinates from the MDAnalysis AdK test system
(bundled as water_pos.npy / water_box.npy), tiled into supercells to scale N
while keeping the real spatial distribution.

Run via run.sh / run.bat, which sets OMP_NUM_THREADS and calls:
    python ab.py both       # threads=1: time OLD + NEW, save OLD baseline
    python ab.py newonly    # time NEW at the current OMP_NUM_THREADS, vs baseline
"""
import os, sys, json, time
import numpy as np
import MDAnalysis  # noqa: F401  (ensures the package import path is set up)
from MDAnalysis.lib.mdamath import triclinic_vectors, triclinic_box
from MDAnalysis.lib.nsgrid import FastNS as FastNS_new

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import nsgrid_old  # built by build_old.py

CUTOFF = float(os.environ.get("BENCH_CUTOFF", "12.0"))
KS = [int(k) for k in os.environ.get("BENCH_TILES", "1 2").split()]  # supercell factors
mode = sys.argv[1] if len(sys.argv) > 1 else "both"
omp = os.environ.get("OMP_NUM_THREADS", "?")
BASE = os.path.join(HERE, "old_baseline.json")

pos0 = np.load(os.path.join(HERE, "water_pos.npy")).astype(np.float32)
box0 = np.load(os.path.join(HERE, "water_box.npy")).astype(np.float32)
vecs = triclinic_vectors(box0)

def supercell(K):
    reps = [pos0 + (kx*vecs[0]+ky*vecs[1]+kz*vecs[2]).astype(np.float32)
            for kx in range(K) for ky in range(K) for kz in range(K)]
    p = np.ascontiguousarray(np.concatenate(reps), dtype=np.float32)
    sv = vecs * K
    return p, triclinic_box(sv[0], sv[1], sv[2])

def best(fn, n):
    b = 1e9
    for _ in range(n):
        t = time.perf_counter(); fn(); b = min(b, time.perf_counter() - t)
    return b * 1e3

baseline = {}
if mode == "newonly" and os.path.exists(BASE):
    baseline = json.load(open(BASE))

for K in KS:
    pos, box = supercell(K)
    N = len(pos)
    reps = 3 if K == 1 else 1
    tn = best(lambda: FastNS_new(CUTOFF, pos, box=box).search(pos), reps)
    if mode == "both":
        to = best(lambda: nsgrid_old.FastNS(CUTOFF, pos, box=box).search(pos), reps)
        baseline[str(N)] = to
        print(f"OMP={omp:>3}  N={N:>8,}  OLD(serial)={to:9.1f} ms   NEW={tn:9.1f} ms   "
              f"speedup vs OLD = {to/tn:5.2f}x")
    else:
        to = baseline.get(str(N))
        sp = f"{to/tn:5.2f}x" if to else "  n/a"
        print(f"OMP={omp:>3}  N={N:>8,}  NEW={tn:9.1f} ms   speedup vs OLD = {sp}")

if mode == "both":
    json.dump(baseline, open(BASE, "w"))
