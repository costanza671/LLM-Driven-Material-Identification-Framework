import json

def write_json(mp_data, structure, formula, space_group, mp_id):
    """
    Save Materials Project data + raw structure (lossless) to JSON.
    """

    structure_json = {
        "formula": mp_data["formula"],
        "material_id": mp_data["material_id"],
        "space_group": mp_data["space_group"],
        "crystal_system": str(mp_data["crystal_system"]),
        "energy_above_hull": mp_data["energy_above_hull"],

        # RAW pymatgen structure (LOSSLESS)
        "structure": structure.as_dict()
    }

    json_name = f"{formula}-{space_group}-{mp_id}.json"

    with open(json_name, "w") as f:
        json.dump(structure_json, f, indent=2)
