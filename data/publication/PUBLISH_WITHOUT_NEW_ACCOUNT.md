# Publish FSOT — No New Account Required

You already have **GitHub** (and optionally **OSF**). You do **not** need Zenodo.

## Option A — GitHub Release (recommended, ~2 minutes)

Uses login you already have for `dappalumbo91/FSOT-2.1-Lean`.

```powershell
cd I:\FSOT-Physical-Archive\02_FSOT-2.1-Lean-Full
python scripts/publish_github_release.py
```

Then in your browser (already logged into GitHub):

1. Open https://github.com/dappalumbo91/FSOT-2.1-Lean/releases/new
2. Tag: `fsot-monograph-v1` → Create from `main`
3. Title: `FSOT Monograph Verification Bundle v1`
4. Drag `data/publication/github_release_v1/FSOT-Monograph-Verification-Bundle-v1.zip`
5. Paste text from `data/publication/github_release_v1/RELEASE_NOTES.md`
6. Click **Publish release**

**Citable URL:** `https://github.com/dappalumbo91/FSOT-2.1-Lean/releases/tag/fsot-monograph-v1`

No DOI, but permanent and accepted for preprint citation. Competitions and GitHub-native workflows use this.

---

## Option B — OSF Storage (existing OSF login, not Preprints)

Your OSF **preprint** was rejected on topic fit. OSF **project storage** is different — no moderation queue.

1. Log into https://osf.io (account you already have)
2. New Project → name: `FSOT Cross-Domain Verification Corpus`
3. Upload folder: `data/publication/zenodo_deposit_v1/files/`
4. Add description + link to GitHub repo
5. Project gets a permanent OSF URL (no preprint review)

This is a **dataset/registry** deposit, not an OSF Preprint submission.

---

## Option C — Already published (zero clicks)

The repo itself is live publication:

- https://github.com/dappalumbo91/FSOT-2.1-Lean
- Commit `50b6d4d` — publication package
- Tag `tier-88-verified-desktop-v1`

Anyone can cite: `dappalumbo91/FSOT-2.1-Lean @ main, commit 50b6d4d`

---

## Why not fully automated?

Zenodo, OSF API, and GitHub Releases API all require a **one-time token** from an account.
There is no reputable DOI service with zero authentication anywhere.

**Minimum friction path:** Option A — GitHub Release, 2 minutes, no new signup.

---

## Zenodo (only if you want a DOI later)

One-time free signup → link GitHub → future releases auto-get DOI.
Not required for the monograph to be public and citable.