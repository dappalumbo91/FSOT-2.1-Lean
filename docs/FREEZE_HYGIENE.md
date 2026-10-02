# Freeze hygiene

These notes sit beside the freeze files. The files they describe were not edited.

## Ledger A hash

`predictions/LEDGER_A_FREEZE.yaml` had a generated-at comment of 2026-09-14T22:02:50.487368+00:00 and no hash. The yaml is unchanged. `predictions/LEDGER_A_FREEZE_SHA256.json` records SHA-256 `2ebfc79ec18aca0ac39ecf2481a49d8286ef113d60bee3fc3541c7a13ac49455` of those bytes, taken at 2026-10-02T05:13:52.095679+00:00. The header pin inside the yaml is AEB2AD.

## Two mapping freezes

`predictions/toe_prereg_freeze.json` (`TOE-PREREG-20260909`, frozen 2026-09-09T16:11:09.786611+00:00) is the sector preregistration hashed against pin D1D38A. It was not edited.

`predictions/domain_freezes/AEB2AD_mapping.json` is a new freeze of the current core and extension mapping (407 domains) at live pin AEB2AD. `mapping_sha256` is `a2161f46bf7e805b7097d86732065988be42648bff33bf675ad9525f55f7b26b`, authority SHA-256 `aeb2adad6e80f487772c5df90a2e3dda71624ab831a6a83b94ab471ac9aac170`, frozen at 2026-10-02T05:13:52.330636+00:00. Both freezes stay.

New freezes are written by `scripts/freeze_domain.py`. A second run refuses to overwrite.

`scripts/evidence_tiers.py` reads that mapping file as one dated freeze per domain. The 407 domains move from exploratory to frozen pending. The 14 sector predictions in the untouched preregistration were already frozen pending, so the domain table is 421 frozen pending and 0 confirmed. Record counts are unchanged: exploratory 359,782, frozen pending 0, confirmed held-out 0, structural/identity 140,100. Confirmed held-out stays the accuracy claim. No data release dated after 2026-10-02 is recorded, so nothing promotes.

## Preregistration date

`predictions/preregistered_predictions_manifest.yaml` says `registered_at: 2026-07-10`. That claim is left as written.

Git history does not show the file on that day. The first commit that adds it is `dfebff1c305a8a205325e6edbefbe56839ce7eb7` on 2026-08-01T14:54:57-04:00, at `data/preregistered_predictions_manifest.yaml` (and a copy under `data/publication/zenodo_deposit_v1/files/data/`). Commit `7f29b189fb50c5c23b4fbe7afda95f4e4320bd3d` on 2026-08-06T09:25:17-04:00 moves it to `predictions/preregistered_predictions_manifest.yaml`.

No email and no timestamped upload earlier than that git add were found in this repository. Copies of the same `2026-07-10` string in the Kaggle pack and in `results/literature/2026-08-17_crossref.json` repeat the manifest. They are not a separate clock. The date with evidence is the git add, 2026-08-01.

## Two values of w_a

`predictions/toe_prereg_freeze.json` sector `PRED-wa` is **-1.018**. That is the D1D38A preregistered sector prediction. It stays.

`predictions/LEDGER_A_FREEZE.yaml` row `Dark_energy_wa` is **-0.808109771581081** (anchor -0.8081, expression `-gamma*e*phi/pi`). That is the Ledger A closed form under the yaml's AEB2AD header.

They are different objects. The current live closed form is the Ledger A value on pin AEB2AD. The preregistration is the older sector prediction and is not rewritten to match it.
