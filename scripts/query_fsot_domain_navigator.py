#!/usr/bin/env python3
"""Query FSOT domain navigator — scientific discovery CLI (JSON / text / bibtex)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_domain_navigator_lib import (  # noqa: E402
    build_repro_bundle,
    enrich_panel,
    load_manifest,
    load_navigator,
    panels_for_core,
    problem_route,
    search_fts,
    search_json,
)


def _print_text(payload: dict) -> None:
    kind = payload.get("kind", "result")
    if kind == "panel":
        sci = payload.get("scientific") or {}
        print(f"Panel: {payload['panel']}")
        print(f"  Core domain: {payload.get('routes_to_core')}")
        print(f"  Tier: {payload.get('tier')}  Records: {sci.get('record_count')}  Median: {sci.get('pooled_median_error_pct')}%")
        print(f"  Lean: {payload.get('lean_module')}")
        print(f"  Benchmark: {sci.get('benchmark_path')}")
        if sci.get("sources"):
            print(f"  Sources: {', '.join(sci['sources'][:4])}")
        rep = payload.get("reproduce") or {}
        for label in ("ingest", "build", "verify_panel"):
            if rep.get(label):
                print(f"  {label}: {rep[label]}")
    elif kind == "route":
        print(f"Intent: {payload['intent']} → {payload['core_domain']}")
        print(f"  Keywords: {', '.join(payload.get('keywords') or [])}")
        print(f"  Panels: {', '.join(payload.get('panels') or [])}")
    elif kind == "core":
        print(f"Core domain: {payload['name']}")
        print(f"  Records: {payload.get('empirical_records')}  Median: {payload.get('median_error_pct')}%  Tier: {payload.get('coverage_tier')}")
        print(f"  Subfield breadth: {payload.get('subfields_touched')}/{payload.get('subfields_studied')} ({payload.get('breadth_pct')}%)")
        print(f"  Panels ({len(payload.get('panels') or [])}): {', '.join((payload.get('panels') or [])[:8])}")
    elif kind == "search":
        for hit in payload.get("hits") or []:
            print(f"  [{hit['kind']}] {hit['name']} → {hit.get('core_domain')}")
    elif kind == "bundle":
        print(f"Repro bundle: {payload['bundle_id']}")
        print(f"  Panels: {payload['panel_count']}  Records: {payload['total_empirical_records']}")
        for cmd in payload.get("reproduce_commands") or []:
            print(f"  $ {cmd}")


def _bibtex_panel(payload: dict) -> str:
    panel = payload.get("panel", "unknown").replace("_", "")
    sci = payload.get("scientific") or {}
    year = "2026"
    if sci.get("generated_at"):
        year = str(sci["generated_at"])[:4]
    return (
        f"@misc{{fsot_{panel.lower()},\n"
        f"  title = {{FSOT verification panel: {payload.get('panel')}}},\n"
        f"  author = {{Palumbo, Damian Arthur}},\n"
        f"  year = {{{year}}},\n"
        f"  howpublished = {{\\url{{https://github.com/dappalumbo91/FSOT-2.1-Lean}}}},\n"
        f"  note = {{Records: {sci.get('record_count')}, pooled median error: {sci.get('pooled_median_error_pct')}%}}\n"
        f"}}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Query FSOT domain navigator for scientific reproduction")
    parser.add_argument("--query", "-q", help="Keyword search (FTS)")
    parser.add_argument("--core", help="List panels for a core domain (e.g. Biology)")
    parser.add_argument("--intent", help="Problem route intent (e.g. quantum_entanglement)")
    parser.add_argument("--panel", help="Full scientific detail for one panel")
    parser.add_argument("--bundle", action="store_true", help="Emit reproduction bundle manifest")
    parser.add_argument("--format", choices=("text", "json", "bibtex"), default="text")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild navigator index first")
    args = parser.parse_args()

    if not any([args.query, args.core, args.intent, args.panel]):
        parser.error("Specify --query, --core, --intent, or --panel")

    doc = load_navigator(rebuild=args.rebuild)
    ext = load_manifest()

    if args.bundle:
        bundle = build_repro_bundle(
            core=args.core,
            intent=args.intent,
            panel=args.panel,
            query=args.query,
        )
        if args.format == "json":
            print(json.dumps(bundle, indent=2))
        elif args.format == "bibtex":
            entries = []
            for p in bundle.get("panels") or []:
                entries.append(_bibtex_panel({"kind": "panel", **p}))
            print("\n\n".join(entries))
        else:
            _print_text({"kind": "bundle", **bundle})
        return 0

    if args.panel:
        if args.panel not in ext:
            raise SystemExit(f"Unknown panel: {args.panel}")
        payload = {"kind": "panel", **enrich_panel(args.panel, ext[args.panel])}
    elif args.intent:
        route = problem_route(doc, args.intent)
        if not route:
            raise SystemExit(f"Unknown intent: {args.intent}")
        payload = {"kind": "route", **route}
    elif args.core:
        core_row = next((c for c in doc.get("core_domains") or [] if c["name"] == args.core), None)
        if not core_row:
            raise SystemExit(f"Unknown core domain: {args.core}")
        payload = {
            "kind": "core",
            **core_row,
            "panels": panels_for_core(doc, args.core),
        }
    else:
        from fsot_domain_navigator_lib import DB_PATH

        hits = search_fts(args.query) if DB_PATH.exists() else []
        if not hits:
            hits = search_json(doc, args.query)
        payload = {"kind": "search", "query": args.query, "hits": hits}

    if args.format == "json":
        print(json.dumps(payload, indent=2))
    elif args.format == "bibtex" and payload.get("kind") == "panel":
        print(_bibtex_panel(payload))
    else:
        _print_text(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())