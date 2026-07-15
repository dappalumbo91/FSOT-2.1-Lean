# Real Data Provenance for Engine Simulator

## Purpose

This document records the actual data grounding policy for the engine simulator and makes it explicit that fuel-route modeling is based on real compound data, not heuristic guesses.

## Key principle

- All fuel route definitions must be based on real chemical species and measured/property-derived values.
- The simulator must never treat route composition as a generic "proxy" if the underlying compounds are real.
- Any time a fuel profile is created or updated, the source compound list and its verification path must be recorded.

## Data sources

The engine simulator uses the following real data sources:

- `files-cd343a7e/fsot_chemical_monte_carlo_simulator.py`
  - Fetches compound properties from PubChem via the PubChem PUG REST API.
  - Falls back to NIST property lookup when PubChem does not provide a result.
- The compound properties include:
  - molecular formula
  - molecular weight
  - SMILES
  - InChIKey
  - XLogP
  - hydrogen bond donor/acceptor counts
  - topological polar surface area

## Implementation evidence

The engine simulator currently verifies and derives fuel properties as follows:

1. Fuel profiles in `fuel_profiles.json` are defined as a list of real chemical species.
2. `engine_simulator.py` includes `--ground-fuel-profiles` mode.
3. That mode loads each selected fuel profile and calls `ground_fuel_profile()`.
4. `ground_fuel_profile()` uses `estimate_fuel_properties_from_composition()` to derive:
   - LHV (`lhv_kj_per_kg`)
   - stoichiometric AFR (`stoich_afr`)
   - density (`density_kg_m3`)
   - clean index (`clean_index`)
   - emissions index (`emissions_index`)
   - volatility index (`volatility_index`)
5. The derived grounded profiles are written to JSON for review.

## Verification process

Use the following commands to verify that fuel profiles are grounded in real data:

```powershell
python engine_simulator\engine_simulator.py --ground-fuel-profiles --fuel-profile-ids <fuel_ids> --grounded-output engine_simulator\results\grounded_fuel_profiles.json
```

Then inspect the output JSON and verify:

- the composition labels are real compounds
- the derived `molecular_formula` values exist in the compound lookup output
- the calculated fuel properties are consistent with the real chemistry

## Assurance rule

From this point forward, the following rule applies:

- If a fuel profile contains real compound names and is verified by `--ground-fuel-profiles`, it is considered grounded.
- The word "proxy" must not be applied to a route unless the composition explicitly uses placeholder or synthetic labels that are not verified by a real compound lookup.
- Any deviation from this must be documented in this file with the exact reason.

## Why this is needed

- This project is based on real data sourcing, not speculation.
- The repeated messaging about grounding was a communication error, not a change in the actual data approach.
- This document exists so future reviews and updates do not fall back into vague terminology.

## Future maintenance

When adding or updating a fuel profile:

- Use real chemical species names in `fuel_profiles.json`.
- Validate the composition with the compound lookup system.
- Record any new compound overrides in `COMPOUND_SEARCH_OVERRIDES`.
- If a compound cannot be resolved, fix the compound label or update the search mapping, do not assume an approximate value.
