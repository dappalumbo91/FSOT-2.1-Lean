# FSOT tech index (names only)

**Status:** unpublished working list. These are **titles of private designs**. Specs, wattages, parts lists, and build files are **not** in this repo. Each item will get its own simulation repo later. Until then this is a *to-do index*, not a product catalog.

**How to read a row:** the name is public; the *fold* is the FSOT 2.1 interface that design will score against when a simulation exists. Epistemic is `unpublished` unless a *separate* residual panel already exists for the *concept* (not the gadget).

| Name | Fold (later score) | Notes |
|------|--------------------|-------|
| Quantum Vacuum Energy Harvester (QVEH) | quantum vacuum / Casimir | law_11 family |
| Compact Integrated Quantum Vacuum EnerFrame | quantum vacuum | same fold |
| Neo-Benben Household Energy Unit | vacuum / fuel-lab concept | unpublished |
| Palumbo Perpetual Flux Generator | fuel-lab concept | unpublished |
| Dual-Surface Quantum Fluid Barrier | domain coupling / valve | unpublished |
| Fluidic Warp Drive | BH→WH valve (C2) | unpublished |
| Warp Portal | BH→WH valve (C2) | unpublished |
| Mini 10D-WRPS-D | BH→WH valve (C2) | unpublished |
| Warp Drive (E10D-WD) | BH→WH valve (C2) | unpublished |
| Warp disc (starate) | BH→WH valve (C2) | unpublished |
| Electromagnetic Propulsion Ring | propulsion fold | unpublished |
| Aetherion spacecraft | propulsion / atmosphere | unpublished |
| Aetherion Colossus | propulsion / atmosphere | unpublished |
| GXT-01 | observer / embodiment | unpublished |
| GXT-01 Cryogenic Cooling | thermal / vacuum sink | unpublished |
| Standalone electromagnetic field generator | magnetosphere analog | unpublished |
| Mini-Oxoflash | atmosphere / ozone (law_26) | unpublished |
| The Oxoflash | atmosphere / ozone (law_26) | unpublished |
| OxoHive | atmosphere / ozone (law_26) | unpublished |
| Mars Terraforming Blueprint | atmosphere / ozone (law_26) | unpublished |
| NeutriFusion Reactor | fusion panel family | unpublished |
| The Sun Pocket | fusion panel family | unpublished |
| Seawater Plasma Fusion Reactor (SPFR) | fusion panel family | unpublished |
| Double Helix Plasma | plasma fold | unpublished |
| The Quantum Solar Panel | electrical-power fold | unpublished |
| wood-PoofCone Thermo-Plasma Speaker | acoustics / POOF–SUCTION (C9) | unpublished |
| FlexiThread | materials fold | unpublished |
| Rubber-Aluminum Nanocomposite | materials fold | unpublished |
| FSUFT-Vibranium Synthesizer | materials fold | unpublished |
| GigaFlux Armor | materials fold | unpublished |
| Memorphium | materials fold | unpublished |
| MetaForge 3D Printer | manufacturing fold | unpublished |
| Holoflex | observer / display | unpublished |
| Quantum Fluid Tricorder | observer / living-FSOT | unpublished |
| Quantum noise reducer | observer / noise as fluid | unpublished |
| FSUFT 8.3 Verifier (F8V) | observer / measurement | unpublished |
| NanoHLSD | observer / embodiment | unpublished |
| FSUFT-U Plant Growth Stimulator | agroecology fold | unpublished |
| The Blob | civic / metabolism analog | unpublished |
| Planetary Gear Board | as-above-so-below (C12) | unpublished |
| BlackHole WhiteHole Cycle | already scored | BlackHole_WhiteHole_Cycle_Live_Panel — concept residual, not a gadget spec |
| Decoding the Philosopher's Stone (6.0) | interpretive philosophy | not a device |

Machine copy: [`tech_blueprints_registry.json`](tech_blueprints_registry.json).

Regenerate names (does **not** ingest private files into public docs):

```powershell
python scripts/build_tech_blueprints_registry.py
```
