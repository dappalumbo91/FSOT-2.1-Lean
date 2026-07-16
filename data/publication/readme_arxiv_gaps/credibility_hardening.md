### 9.6 Hard credibility expansion

FSOT credibility is not rhetorical — every pillar must reproduce independently. The hardening audit aggregates formal triangulation, benchmark gates, parameter honesty, wet-lab biology, live catalog ingest, and skeptic replication into one scorecard.

| Artifact | Role |
|----------|------|
| [`data/publication/CREDIBILITY_HARDENING_AUDIT.md`](data/publication/CREDIBILITY_HARDENING_AUDIT.md) | Multi-pillar green gate (formal + empirical + lean routes + Tier 96) |
| [`data/publication/LEAN_ROUTE_CREDIBILITY_EXPANSION.md`](data/publication/LEAN_ROUTE_CREDIBILITY_EXPANSION.md) | Under-covered Lean route benchmarks |
| [`data/publication/live_ingest_schedule.yaml`](data/publication/live_ingest_schedule.yaml) | Weekly live catalog refresh policy |
| [`data/publication/credibility_hardening_audit.json`](data/publication/credibility_hardening_audit.json) | Machine-readable pillar ledger |
| [`docs/SKEPTIC_REPLICATION_KIT.md`](docs/SKEPTIC_REPLICATION_KIT.md) | 15-minute independent falsification path |

Regenerate: `python scripts/build_credibility_depth_bundle.py` (lean routes + live ingest + wet-lab + Tier 96 + hardening audit).

**Scheduled live ingest:** `data/publication/live_ingest_schedule.yaml` — weekly `build_live_ingest_refresh_bundle.py`.
