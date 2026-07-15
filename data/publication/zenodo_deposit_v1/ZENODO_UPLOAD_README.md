# Zenodo Upload Guide — FSOT Monograph v1

## What is Zenodo?

[Zenodo](https://zenodo.org) is a **free, permanent open-research archive** operated by CERN.
It is **not a journal** and **not arXiv** — there are **no endorsers**, no PhD requirement,
and no topic gatekeepers. When you click Publish, Zenodo assigns a **DOI** (a citable permanent
link like `10.5281/zenodo.1234567`) that never expires.

Researchers use Zenodo for: preprints, datasets, software releases, thesis chapters, and
full reproducibility bundles — exactly what FSOT needs.

## What you upload (prepared in this folder)

Staged files: `21` items in `files/`
Metadata: `zenodo_metadata.json` (copy-paste into the deposit form)
Manifest: `zenodo_deposit_manifest.json`

GitHub commit pinned: `2d3a49aae13167e8ee87688dc001847e24d99098`

## Step-by-step (first time, ~30 minutes)

1. Go to **https://zenodo.org** → Sign up (email or ORCID).
2. Click **Upload** (top menu) → **New upload**.
3. Drag the entire **`files/`** folder into the upload area.
4. Fill the form using values from **`zenodo_metadata.json`**:
   - Title, description, keywords, license (CC-BY-4.0)
   - Resource type: **Publication → Preprint**
5. Under **Related identifiers**, add:
   - Identifier: `https://github.com/dappalumbo91/FSOT-2.1-Lean`
   - Relation: *is supplement to* | Type: *Software*
6. When you have a PDF of the monograph, add it to the upload (optional for v1).
7. Click **Publish**. Zenodo issues your DOI immediately.

## After publish

- Add the DOI to your GitHub README.
- Cite as: dappalumbo91 (2026). *Fluid Spacetime Omni-Theory...* Zenodo. DOI:10.5281/...
- OSF can mirror the same DOI link as a registry entry (no re-review needed).

## Cost

**Free.** No APC. No subscription.

## AI disclosure

Included in the description field (see `author_note` in manifest). Zenodo does not reject
AI-assisted deposits; transparency is sufficient.
