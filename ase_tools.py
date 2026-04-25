"""
ASE Utility Module
This module provides helper functions to bridge pymatgen structures
with the Atomic Simulation Environment (ASE) and streamline common tasks.

It includes functions to:
- Convert pymatgen Structure objects into ASE Atoms objects (json_to_ase)
- Write structures in VASP POSCAR format using ASE (write_poscar)
- Visualize structures via ASE GUI tools (view_structure)

Notes: The conversion applies symmetry standardization before creating the ASE object. POSCAR output is generated from ASE Atoms and reflects a conventional standardized representation rather than the raw input structure (primitive unit cell).
"""

from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from ase.io import write
from ase import Atoms
from ase.visualize import view

def json_to_ase(structure):
    """
    Convert a pymatgen Structure to ASE Atoms using a symmetry-standardized conventional cell.
    Returns an ASE object with fractional coordinates and periodic boundary conditions.
    """
    structure = SpacegroupAnalyzer(structure).get_conventional_standard_structure()
    return Atoms(
        symbols=[str(site.specie) for site in structure],
        scaled_positions=structure.frac_coords,
        cell=structure.lattice.matrix,
        pbc=True
    )

def write_poscar(atoms, formula, space_group, mp_id):
    """Write ASE Atoms to a VASP POSCAR file with a standardized name using fractional coordinates"""
    vasp_name = f"POSCAR-{formula}-{space_group}-{mp_id}"
    write(vasp_name, atoms, format="vasp", direct=True) 

def view_structure(atoms):
    """Display structure using ASE gui visualization tool."""
    view(atoms)
