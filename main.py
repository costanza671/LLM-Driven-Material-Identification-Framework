# Terminal output formatting utilities
from termcolor import colored

# Disable noisy logs progress-bars for cleaner terminal output
import os
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GRPC_TRACE"] = ""
os.environ["TQDM_DISABLE"] = "1"

# Project modules (LLM parsing, Materials Project API, ASE utilities, I/O tools)
from ai_parser import llm_parse_material
from mp_client import mp_query_material
from ase_tools import json_to_ase, write_poscar, view_structure
from write_structure_json import write_json
from io_c2x import convert_with_c2x
from logger_function import log_section


if __name__ == "__main__":

    # -----------------------
    # Step 1: Receive natural language description of the target material from user
    # -----------------------
    text = input(colored("Enter material description -->", "cyan", attrs=["reverse", "blink"]))

    # Load API keys required for LLM and Materials Project access
    llm_key = os.getenv("GOOGLE_API_KEY")
    mp_key = os.getenv("MP_API_KEY")

    # Fail early if credentials are missing
    if not llm_key or not mp_key:
       raise ValueError("Missing API keys")

    # -----------------------
    # Step 2: Parse user text using LLM
    # -----------------------
    parsed = llm_parse_material(text, llm_key)

    # -----------------------
    # Step 3: Query Materials Project database
    # -----------------------
    mp_data = mp_query_material(parsed, mp_key)

    # Exit if no matching structure is found
    if not mp_data:
        print("No structure found")
        exit()

    # Extract structure from Materials Project output
    structure = mp_data["structure"]

    # Convert from dict to pymatgen Structure when data is in JSON form (e.g. API or file input)
    # This is needed because only pymatgen Structure objects support lattice, symmetry, and coordinate operations and downstream tools (POSCAR writing, symmetry analysis, and ASE conversion) 
    if isinstance(structure, dict):
       structure = Structure.from_dict(structure)
 
    # Extract identifiers used for file naming
    formula = mp_data["formula"]
    mp_id = mp_data["material_id"].replace("-", "")
    space_group = mp_data["space_group"].replace("/", "")

    # -----------------------
    # Step 4: Export structure to JSON, convert structure to ASE object and write structure in POSCAR format
    # -----------------------
    json_name = f"{formula}-{space_group}-{mp_id}.json"
    write_json(mp_data, structure,formula, space_group, mp_id)    

    atoms = json_to_ase(structure)
    write_poscar(atoms, formula, space_group, mp_id)

     
    # -----------------------
    # Step 5: Write simulation input files with c2x (This step must be skipped if not wanted)
    # -----------------------
    convert_with_c2x(formula, space_group, mp_id) #If you do not want to use c2x conversion just comment this line)

    # -----------------------
    # Final Log Report
    # -----------------------
    # Print final execution in a formatted report to terminal using the log_section module 
    log_section("User Query", text)

    log_section("Llm (Gemini) Response", parsed)

    log_section("Materials Project summary", {
       key: value for key, value in mp_data.items()
       if key != "structure"
    })

    log_section("ASE Structure Loaded")
    print(atoms.get_chemical_symbols())
    print(atoms.get_scaled_positions())
    print(atoms.get_cell())

    log_section("Output Files", json_name)
    print("Electronic structure inputs written as: POSCAR, QE, and CIF formats") #Adjust this line if you are not using c2x for producing QE and CIF files
    print("")

    # -----------------------
    # Visualisation of the Loaded Structure
    # -----------------------
    # Open interactive structure viewer (ASE gui)
    view_structure(atoms)

