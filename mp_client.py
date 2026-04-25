from mp_api.client import MPRester # Materials Project API client (used for querying crystal structure database)

def mp_query_material(parsed, mp_key):
    """
    Query and rank materials from the Materials Project database.
    The function:
    1. Searches materials by chemical formula
    2. Optionally filters by space group if provided
    3. Uses prototype as a weak structural hint (if no space group is given)
    4. Ranks candidates using:
        - structural compatibility (if applicable)
        - thermodynamic stability (energy above hull)
    5. Returns the best matching material entry
    """

    # Connect to Materials Project API using the provided key
    with MPRester(mp_key) as mpr:

        # Retrieve all materials matching the formula
        results = mpr.materials.summary.search(
            formula=parsed["formula"]
        )

        # If no candidates exist, return early
        if not results:
            return None

        # Extract structure constraints from parsed JSON result
        structure = parsed.get("structure", {}) or {}
        sg_symbol = structure.get("space_group_symbol")
        prototype = (structure.get("prototype") or "").lower()

        # Filter by space group (if available)
        if sg_symbol:
            candidates = [
                candidate for candidate in results
                if candidate.symmetry.symbol == sg_symbol
            ]

            # Fallback to all results if no exact match exists
            if not candidates:
                candidates = results
        else:
            candidates = results

        # Define ranking function for candidate selection
        def rank(candidate):
            """
            Ranking function used to select the best Materials Project candidate.
            The score is tuple (structure_rank, energy_above_hull) used for sorting candidates.
            Structure ranking:
             - If no space group constraint is provided, a weak prototype hint may be used
             - Prototype match lowers the rank (preferred = 0, mismatch = 1)
             - If a space group is specified, structural ranking is neutral (0 for all)
            Energetic ranking:
             - Energy above hull is used as a secondary criterion
             - Lower values indicate more thermodynamically stable phases
            """

            sym = str(candidate.symmetry.symbol).lower()

            # Structural ranking:
            # - If no space group constraint is provided, optionally use prototype as a weak hint
            # - If prototype matches symmetry string → best rank (0), otherwise penalize (1)
            # - If space group is provided, this signal is ignored
            if not sg_symbol and prototype:
                if prototype in sym:
                    structure_rank = 0
                else:
                    structure_rank = 1
            else:
                structure_rank = 0

            # Energetic ranking:
            # Lower energy above hull indicates a more stable (and thus preferred) phase
            energy_rank = candidate.energy_above_hull

            # Combined ranking key:
            # 1. structure match priority
            # 2. thermodynamic stability
            return (structure_rank, energy_rank)

        # Select best candidate
        best = min(candidates, key=rank)

        # Return structured material information
        return {
            "material_id": best.material_id,
            "formula": best.formula_pretty,
            "space_group": best.symmetry.symbol,
            "crystal_system": best.symmetry.crystal_system,
            "energy_above_hull": best.energy_above_hull,
            "structure": best.structure
        }
