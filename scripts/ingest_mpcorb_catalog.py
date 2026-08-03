#!/usr/bin/env python3
"""Download + snapshot MPCORB / AllCometEls (IAU Minor Planet Center).

Public free sources (no credentials):
  https://minorplanetcenter.net/iau/MPCORB/MPCORB.DAT.gz
  https://minorplanetcenter.net/iau/MPCORB/AllCometEls.txt
  https://minorplanetcenter.net/iau/MPCORB/NEA.txt
  https://minorplanetcenter.net/iau/MPCORB/Distant.txt

Catalog updates daily — this script records SHA-256 + object counts for the snapshot.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import shutil
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "vendor" / "mpcorb"
MANIFEST = ROOT / "data" / "mpcorb_ingest_manifest.json"

FILES = {
    "MPCORB.DAT.gz": "https://minorplanetcenter.net/iau/MPCORB/MPCORB.DAT.gz",
    "AllCometEls.txt": "https://minorplanetcenter.net/iau/MPCORB/AllCometEls.txt",
    "NEA.txt": "https://minorplanetcenter.net/iau/MPCORB/NEA.txt",
    "Distant.txt": "https://minorplanetcenter.net/iau/MPCORB/Distant.txt",
}


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _download(url: str, dest: Path, timeout: int = 600) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(url, headers={"User-Agent": "FSOT-2.1-Lean/mpcorb-ingest"})
    with urllib.request.urlopen(req, timeout=timeout) as resp, tmp.open("wb") as out:
        shutil.copyfileobj(resp, out, length=1 << 20)
    tmp.replace(dest)


def _count_mpcorb_gz(path: Path) -> int:
    n = 0
    with gzip.open(path, "rt", encoding="latin-1", errors="replace") as f:
        for line in f:
            if len(line) < 103:
                continue
            # data rows: designation in cols 1-7; skip pure header prose
            head = line[:7].strip()
            if not head:
                continue
            # skip long prose paragraphs
            if line.startswith(" ") and not any(ch.isdigit() for ch in head):
                # many comet-like? MPCORB data lines usually start with digit or letter designation
                pass
            # Fixed-width orbit lines have a in cols 93-103 as float-like
            try:
                float(line[92:103].strip())
                float(line[70:79].strip())
            except ValueError:
                continue
            n += 1
    return n


def _count_text_orbits(path: Path) -> int:
    n = 0
    with path.open("rt", encoding="latin-1", errors="replace") as f:
        for line in f:
            if len(line.strip()) < 40:
                continue
            # skip comments
            if line.lstrip().startswith("#"):
                continue
            n += 1
    return n


def main() -> int:
    ap = argparse.ArgumentParser(description="Ingest MPCORB + comet catalogs")
    ap.add_argument("--skip-download", action="store_true", help="Use existing vendor/mpcorb files")
    ap.add_argument("--timeout", type=int, default=600)
    args = ap.parse_args()

    RAW.mkdir(parents=True, exist_ok=True)
    files_meta: dict[str, dict] = {}

    for name, url in FILES.items():
        dest = RAW / name
        if not args.skip_download or not dest.exists():
            print(f"Downloading {name} ...")
            try:
                _download(url, dest, timeout=args.timeout)
            except Exception as e:
                if dest.exists():
                    print(f"  download failed ({e}); keeping existing {dest}")
                else:
                    print(f"  FAILED {name}: {e}")
                    continue
        else:
            print(f"Using existing {dest}")

        size = dest.stat().st_size
        digest = _sha256(dest)
        entry: dict = {
            "path": str(dest.relative_to(ROOT)).replace("\\", "/"),
            "url": url,
            "bytes": size,
            "sha256": digest,
        }
        if name.endswith(".gz"):
            entry["orbit_rows_parsed"] = _count_mpcorb_gz(dest)
            # optional decompress snapshot for offline tools
            dat = RAW / "MPCORB.DAT"
            if not dat.exists() or dat.stat().st_mtime < dest.stat().st_mtime:
                print("  decompressing MPCORB.DAT ...")
                with gzip.open(dest, "rb") as src, dat.open("wb") as out:
                    shutil.copyfileobj(src, out, length=1 << 20)
            if dat.exists():
                entry["decompressed"] = {
                    "path": str(dat.relative_to(ROOT)).replace("\\", "/"),
                    "bytes": dat.stat().st_size,
                    "sha256": _sha256(dat),
                }
        else:
            entry["line_count_approx"] = _count_text_orbits(dest)
        files_meta[name] = entry
        print(f"  {name}: {size} bytes  sha256={digest[:16]}…  rows≈{entry.get('orbit_rows_parsed') or entry.get('line_count_approx')}")

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "IAU Minor Planet Center (Harvard-Smithsonian CfA)",
        "attribution": (
            "MPCORB / AllCometEls © Minor Planet Center. Free public download; "
            "include header attribution when redistributing (see file header)."
        ),
        "docs": {
            "format": "https://minorplanetcenter.net/iau/info/MPOrbitFormat.html",
            "index": "https://minorplanetcenter.net/iau/MPCORB.html",
        },
        "note": (
            "Catalog updates daily. Object counts change. For bit-for-bit identity with a "
            "published third-party run, match their SHA-256 snapshot date."
        ),
        "files": files_meta,
        "mpcorb_object_count": (files_meta.get("MPCORB.DAT.gz") or {}).get("orbit_rows_parsed"),
        "comet_line_count": (files_meta.get("AllCometEls.txt") or {}).get("line_count_approx"),
    }
    MANIFEST.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {MANIFEST}")
    print(f"  MPCORB objects: {doc.get('mpcorb_object_count')}")
    print(f"  Comet lines:    {doc.get('comet_line_count')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
