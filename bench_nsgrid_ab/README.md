# nsgrid A/B benchmark — OLD (serial) vs NEW (OpenMP) neighbour search

Compares `lib.nsgrid.FastNS.search` before/after the OpenMP parallelization,
on **real** AdK water-oxygen coordinates (bundled `water_pos.npy`/`water_box.npy`),
tiled into supercells to scale N while preserving the real spatial distribution.

The **new** code is whatever MDAnalysis you have installed (so install this branch
editable first); the **old** code is the `develop` version of `nsgrid.pyx`, vendored
here as `nsgrid_old.pyx` and compiled into a standalone `nsgrid_old` module.

## Setup (once)
From the repo root, with a compiler + Cython available:
```bash
pip install -e package/          # installs the NEW nsgrid (this branch)
```

## Run

**Linux / WSL / macOS (has OpenMP — shows real thread scaling):**
```bash
cd bench_nsgrid_ab
bash run.sh
```

**Native Windows (PowerShell/CMD):**
```bat
cd bench_nsgrid_ab
run.bat
```
> On native Windows, MSVC builds MDAnalysis **without** OpenMP, so the new code runs
> **serial** and you'll see ~1× — this run's job is to confirm it *builds under MSVC*
> and stays *correct*. For thread scaling on a Windows box, run `run.sh` inside **WSL**.

## Knobs
- `BENCH_TILES="1 2 3"` — supercell sizes to test (1→11k, 2→89k, 3→299k atoms). Default `1 2`.
- `BENCH_CUTOFF=12.0` — neighbour cutoff in Å.

## Reading the output
Each line is one (threads, N): the OLD serial time, the NEW time, and `speedup vs OLD`.
OLD is thread-independent (serial); NEW should drop as threads increase. Example from a
16-core run:
```
OMP=  1  N=  11,084  OLD(serial)=  3800 ms   NEW=  3427 ms   speedup vs OLD =  1.11x
OMP= 16  N=  11,084  NEW=   265 ms   speedup vs OLD = 14.34x
```
The new code is a drop-in: it returns the **same pairs** as the old (verified separately),
just grouped by atom rather than in the old traversal order.
