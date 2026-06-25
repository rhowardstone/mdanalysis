@echo off
REM A/B benchmark on native Windows. NOTE: MSVC builds MDAnalysis WITHOUT OpenMP,
REM so the new code runs SERIAL here -- this run confirms it BUILDS and is correct
REM and times old-vs-new serial. For real thread scaling, use WSL/Linux + run.sh.
cd /d "%~dp0"
echo == building OLD (develop) nsgrid as nsgrid_old ==
python build_old.py
echo.
echo == old vs new (serial on Windows) ==
set OMP_NUM_THREADS=1
python ab.py both
