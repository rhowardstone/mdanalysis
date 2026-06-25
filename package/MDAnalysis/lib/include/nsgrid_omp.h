#ifndef NSGRID_OMP_H
#define NSGRID_OMP_H

/* Thin OpenMP shim for nsgrid.pyx.
 *
 * When the extension is compiled with OpenMP support the build defines
 * PARALLEL (mirroring calc_distances.h) and we use the real <omp.h>
 * routines.  Otherwise we provide trivial serial stubs so that nsgrid still
 * compiles and runs (single threaded) on toolchains without OpenMP.
 */

#ifdef PARALLEL
#include <omp.h>
#else
static inline int omp_get_max_threads(void) { return 1; }
static inline int omp_get_thread_num(void) { return 0; }
#endif

#endif /* NSGRID_OMP_H */
