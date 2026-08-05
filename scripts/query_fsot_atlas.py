#!/usr/bin/env python3
"""Query data/fsot_atlas.sqlite (open-science residual atlas)."""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "fsot_atlas.sqlite"


def _conn() -> sqlite3.Connection:
    if not DB.exists():
        raise SystemExit(f"Missing {DB} — run: python scripts/build_fsot_atlas_sqlite.py")
    c = sqlite3.connect(str(DB))
    c.row_factory = sqlite3.Row
    return c


def cmd_stats(c: sqlite3.Connection) -> None:
    meta = dict(c.execute("SELECT key, value FROM meta").fetchall())
    print("FSOT Atlas SQLite")
    for k in ("generated_at", "pin_prefix", "green_domains", "margin_domains", "policy"):
        if k in meta:
            print(f"  {k}: {meta[k]}")
    n_dom = c.execute("SELECT COUNT(*) FROM domains").fetchone()[0]
    n_rec = c.execute("SELECT COUNT(*) FROM records").fetchone()[0]
    n_form = c.execute("SELECT COUNT(*) FROM formulas").fetchone()[0]
    n_cit = c.execute("SELECT COUNT(*) FROM citations").fetchone()[0]
    n_open = c.execute("SELECT COUNT(*) FROM open_sources").fetchone()[0]
    n_gap = c.execute("SELECT COUNT(*) FROM high_value_gaps WHERE status IN ('gap','partial')").fetchone()[0]
    n_skip = c.execute("SELECT COUNT(*) FROM high_value_gaps WHERE status LIKE 'skipped%'").fetchone()[0]
    print(f"  domains: {n_dom}  records: {n_rec}  formulas: {n_form}")
    print(f"  citations: {n_cit}  open_sources: {n_open}")
    print(f"  high_value_gaps (open/partial): {n_gap}  skipped_credentials: {n_skip}")
    print("  by family:")
    for row in c.execute(
        "SELECT family, COUNT(*) AS n, SUM(green_gate_pass) AS g FROM domains GROUP BY family ORDER BY n DESC"
    ):
        print(f"    {row['family']}: {row['n']} (green={row['g']})")


def cmd_search(c: sqlite3.Connection, q: str, limit: int) -> None:
    rows = c.execute(
        """
        SELECT d.domain, d.family, d.file_name, d.pooled_median_error_pct, d.green_gate_pass, d.record_count
        FROM fts_domains f
        JOIN domains d ON d.id = f.rowid
        WHERE fts_domains MATCH ?
        LIMIT ?
        """,
        (q, limit),
    ).fetchall()
    if not rows:
        # fallback LIKE
        rows = c.execute(
            """
            SELECT domain, family, file_name, pooled_median_error_pct, green_gate_pass, record_count
            FROM domains
            WHERE domain LIKE ? OR file_name LIKE ?
            LIMIT ?
            """,
            (f"%{q}%", f"%{q}%", limit),
        ).fetchall()
    for r in rows:
        print(
            f"{r['domain']:40} fam={r['family']:22} green={r['green_gate_pass']} "
            f"med={r['pooled_median_error_pct']} n={r['record_count']} file={r['file_name']}"
        )


def cmd_family(c: sqlite3.Connection, family: str, limit: int) -> None:
    rows = c.execute(
        """
        SELECT domain, file_name, pooled_median_error_pct, max_scalar_error_pct, record_count, green_gate_pass
        FROM domains WHERE family = ? ORDER BY domain LIMIT ?
        """,
        (family, limit),
    ).fetchall()
    for r in rows:
        print(
            f"{r['domain']:40} med={r['pooled_median_error_pct']} max={r['max_scalar_error_pct']} "
            f"n={r['record_count']} green={r['green_gate_pass']}"
        )


def cmd_domain(c: sqlite3.Connection, domain: str, limit: int) -> None:
    d = c.execute("SELECT * FROM domains WHERE domain = ? OR file_name = ?", (domain, domain)).fetchone()
    if not d:
        d = c.execute(
            "SELECT * FROM domains WHERE domain LIKE ? OR file_name LIKE ? LIMIT 1",
            (f"%{domain}%", f"%{domain}%"),
        ).fetchone()
    if not d:
        print("domain not found")
        return
    print(dict(d))
    rows = c.execute(
        """
        SELECT property, name, computed, measured, error_pct, formula, eval_kind
        FROM records WHERE domain_id = ? ORDER BY error_pct DESC LIMIT ?
        """,
        (d["id"], limit),
    ).fetchall()
    print(f"--- records (up to {limit}) ---")
    for r in rows:
        print(
            f"  {r['property'] or r['name']}: err={r['error_pct']} "
            f"c={r['computed']} m={r['measured']} [{r['eval_kind']}] {r['formula']}"
        )


def cmd_gaps(c: sqlite3.Connection) -> None:
    print("Open-science high-value gaps (auth=none preferred):")
    for r in c.execute(
        "SELECT id, family, status, title, open_url, auth FROM high_value_gaps ORDER BY status, family"
    ):
        flag = "SKIP" if str(r["status"]).startswith("skipped") else r["status"]
        print(f"  [{flag}] {r['id']:28} {r['family']:22} {r['title'][:50]}")
        print(f"         {r['open_url']}")


def cmd_open_sources(c: sqlite3.Connection, limit: int) -> None:
    for r in c.execute("SELECT id, family, auth, url FROM open_sources ORDER BY family, id LIMIT ?", (limit,)):
        print(f"{r['id']:32} {r['family']:28} auth={r['auth']} {r['url'][:70]}")


def main() -> int:
    p = argparse.ArgumentParser(description="Query FSOT residual atlas SQLite")
    p.add_argument("--stats", action="store_true")
    p.add_argument("--search", type=str, help="FTS/LIKE search")
    p.add_argument("--family", type=str, help="Filter family name")
    p.add_argument("--domain", type=str, help="Show domain + sample records")
    p.add_argument("--gaps", action="store_true", help="List high-value open gaps")
    p.add_argument("--open-sources", action="store_true")
    p.add_argument("--limit", type=int, default=30)
    args = p.parse_args()

    c = _conn()
    if args.stats or not any([args.search, args.family, args.domain, args.gaps, args.open_sources]):
        cmd_stats(c)
    if args.search:
        cmd_search(c, args.search, args.limit)
    if args.family:
        cmd_family(c, args.family, args.limit)
    if args.domain:
        cmd_domain(c, args.domain, args.limit)
    if args.gaps:
        cmd_gaps(c)
    if args.open_sources:
        cmd_open_sources(c, args.limit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
