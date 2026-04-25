"""
Conversion utilities using c2x.
This module provides functions to convert VASP POSCAR files into other formats (e.g., Quantum ESPRESSO input and CIF) using the external c2x command-line tool.
"""
import subprocess

def convert_with_c2x(formula, space_group, mp_id):
    """Convert a POSCAR file to QE input (.in) and CIF formats using c2x."""
    subprocess.run(["c2x", "--qef", f"POSCAR-{formula}-{space_group}-{mp_id}", f"{formula}-{space_group}-{mp_id}.in"], check=True)
    subprocess.run(["c2x", "--cif", f"POSCAR-{formula}-{space_group}-{mp_id}", f"{formula}-{space_group}-{mp_id}.cif"], check=True)

