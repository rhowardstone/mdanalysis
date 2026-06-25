#!/usr/bin/env bash
# A/B benchmark: OLD vs NEW nsgrid.search across thread counts, on real water data.
# Linux / WSL / macOS (anywhere the build has OpenMP). Run from this directory:
#     bash run.sh
set -e
cd "$(dirname "$0")"

echo "== building OLD (develop) nsgrid as nsgrid_old =="
python build_old.py >/dev/null

MAXT=$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)
THREADS="1"
for t in 2 4 8 16; do [ "$t" -le "$MAXT" ] && THREADS="$THREADS $t"; done
echo "== machine cores: $MAXT ; testing OMP_NUM_THREADS = $THREADS =="
echo "   (set BENCH_TILES=\"1 2 3\" for bigger systems; default is 1 2)"
echo

OMP_NUM_THREADS=1 python ab.py both
for T in $THREADS; do
    [ "$T" = "1" ] && continue
    OMP_NUM_THREADS=$T python ab.py newonly
done
