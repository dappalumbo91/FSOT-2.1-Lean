# GitHub / README Sync Audit

**Audited:** 2026-09-09T16:11:15.041415+00:00
**Local HEAD:** `7a0f3e8` | **Origin:** `55b288d`
**Ahead of origin:** 17 | **Behind:** 0

**Cross-proof:** overall_ok=True github_ready=True
**Ready for expansive README run:** `True`

## Actions required

1. **[high]** git add + commit + push pending verification artifacts
   - 225 working-tree changes; ahead of origin by 17

2. **[medium]** python scripts/build_readme_thesis_expansion.py
   - {'exists': True, 'written_count': 0, 'pending_count': 7, 'pending_ids': ['cross_verification', 'api_resources', 'literature', 'domain_atlas', 'formula_corpus', 'contested_observables', 'verified_desktop'], 'sections_on_disk': 7}

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
