#!/usr/bin/env python3
"""Export BibTeX citations for FSOT domain panels and verified desktop bundles."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_domain_navigator_lib import (  # noqa: E402
    VERIFIED_DESKTOP_INTENTS,
    VERIFIED_DESKTOP_PANELS,
    bibtex_panel_entry,
    enrich_panel,
    load_manifest,
    load_navigator,
    panels_for_core,
    problem_route,
)

DEFAULT_OUT = ROOT / "data" / "domain_citations"


def _panels_for_bundle(bundle: str, *, core: str | None, intent: str | None) -> list[str]:
    if bundle == "verified_desktop":
        return list(VERIFIED_DESKTOP_PANELS)
    doc = load_navigator()
    if intent:
        route = problem_route(doc, intent)
        if not route:
            raise SystemExit(f"Unknown intent: {intent}")
        return list(route.get("panels") or [])
    if core:
        return panels_for_core(doc, core)
    raise SystemExit("Specify --bundle verified_desktop, --intent, or --core")


def main() -> int:
    parser = argparse.ArgumentParser(description="Export BibTeX citations for FSOT panels")
    parser.add_argument("--bundle", choices=("verified_desktop",), help="Predefined citation bundle")
    parser.add_argument("--intent", help="Problem route intent slug")
    parser.add_argument("--core", help="Core domain name")
    parser.add_argument("--panel", action="append", dest="panels", help="Single panel (repeatable)")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT, help="Output directory")
    parser.add_argument("--stdout", action="store_true", help="Print BibTeX to stdout instead of file")
    args = parser.parse_args()

    ext = load_manifest()
    panel_names: list[str] = []
    if args.panels:
        panel_names = list(dict.fromkeys(args.panels))
    elif args.bundle or args.intent or args.core:
        panel_names = _panels_for_bundle(args.bundle or "", core=args.core, intent=args.intent)
    else:
        parser.error("Specify --bundle verified_desktop, --intent, --core, or --panel")

    entries: list[str] = []
    for name in panel_names:
        if name not in ext:
            print(f"Warning: unknown panel {name}", file=sys.stderr)
            continue
        entries.append(bibtex_panel_entry(name, enrich_panel(name, ext[name])))

    bibtex = "\n\n".join(entries) + ("\n" if entries else "")
    if args.stdout:
        print(bibtex, end="")
        return 0

    slug = args.bundle or args.intent or args.core or "panels"
    out_dir = args.output
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{slug}.bib"
    header = (
        f"% FSOT domain citations — generated {datetime.now(timezone.utc).isoformat()}\n"
        f"% Repository: https://github.com/dappalumbo91/FSOT-2.1-Lean\n"
    )
    out_path.write_text(header + bibtex, encoding="utf-8")
    print(f"Wrote {out_path} ({len(entries)} entries)")
    if args.bundle == "verified_desktop":
        print(f"  intents: {', '.join(VERIFIED_DESKTOP_INTENTS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())