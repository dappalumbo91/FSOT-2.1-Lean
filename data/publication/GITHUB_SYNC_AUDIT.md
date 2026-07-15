# GitHub / README Sync Audit

**Audited:** 2026-07-15T17:17:34.166616+00:00
**Local HEAD:** `f811b28` | **Origin:** `f811b28`
**Ahead of origin:** 0 | **Behind:** 0

**Cross-proof:** overall_ok=True github_ready=True
**Ready for expansive README run:** `True`

## Actions required

1. **[high]** git add + commit + push pending verification artifacts
   - 64 working-tree changes; ahead of origin by 0

2. **[medium]** python scripts/build_readme_thesis_expansion.py
   - {'exists': True, 'written_count': 0, 'pending_count': 7, 'pending_ids': ['cross_verification', 'api_resources', 'literature', 'domain_atlas', 'formula_corpus', 'contested_observables', 'verified_desktop'], 'sections_on_disk': 7}

3. **[medium]** Track and push publication support files
   - ['data/publication/PUBLISH_WITHOUT_NEW_ACCOUNT.md', 'data/publication/github_release_v1/FSOT-Monograph-Verification-Bundle-v1.zip', 'data/publication/github_release_v1/RELEASE_NOTES.md', 'data/publication/readme_expansion_manifest.yaml', 'data/publication/readme_sections/api_resources.md', 'data/publication/readme_sections/contested_observables.md', 'data/publication/readme_sections/cross_verification.md', 'data/publication/readme_sections/domain_atlas.md', 'data/publication/readme_sections/formula_corpus.md', 'data/publication/readme_sections/literature.md', 'data/publication/readme_sections/verified_desktop.md', 'scripts/publish_github_release.py']

## Expansive run pipeline

```bash
cd I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full
python scripts/sync_verified_desktop_projects.py
python scripts/run_publication_verification_bundle.py --full-cross-proof
python scripts/export_publication_domain_atlas.py
python scripts/build_readme_thesis_expansion.py
python scripts/audit_github_readme_sync.py
```

Full JSON: `data/publication/GITHUB_SYNC_AUDIT.json`
