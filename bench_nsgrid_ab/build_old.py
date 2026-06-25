"""Compile the OLD (develop) nsgrid as a standalone module `nsgrid_old`
so it can be A/B'd against the installed (new) MDAnalysis.lib.nsgrid.

    python build_old.py
"""
import os
import numpy as np
import MDAnalysis
from setuptools import setup, Extension
from Cython.Build import cythonize

inc = os.path.join(os.path.dirname(MDAnalysis.__file__), "lib", "include")
here = os.path.dirname(os.path.abspath(__file__))
ext = Extension(
    "nsgrid_old",
    [os.path.join(here, "nsgrid_old.pyx")],
    include_dirs=[np.get_include(), inc],
    language="c++",
    extra_compile_args=["-O3"],   # serial; OpenMP not needed for the old code
)
setup(
    ext_modules=cythonize([ext], compiler_directives={"language_level": "3"}),
    script_args=["build_ext", "--inplace", "--build-lib", here],
)
print("\nBuilt nsgrid_old. Now run:  python ab.py")
