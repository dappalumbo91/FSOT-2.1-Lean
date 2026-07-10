"""FRB repeater catalog helpers — CHIME tunnel-energy classifier."""

from __future__ import annotations

import csv
import io
import json
import ssl
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

# Official site often returns 503; GCS bucket 403; IOP ApJS supplement is a stable excerpt.
CHIME_CATALOG_URLS: list[str] = [
    "https://www.chime-frb.ca/catalog/CHIME_FRB_catalog.csv",
    "https://storage.googleapis.com/chimefrb-dev.appspot.com/catalog1/chimefrbcat1.csv",
    "https://storage.googleapis.com/chimefrb-dev.appspot.com/catalog2/chimefrbcat2.csv",
]

IOP_CATALOG2_EXCERPT_URL = (
    "https://iopscience.iop.org/0067-0049/283/1/34/suppdata/apjsae3828t1_ascii.txt"
    "?doi=10.3847/1538-4365/ae3828"
)

VIZIER_CHIME_CAT1_URL = "https://cdsarc.cds.unistra.fr/ftp/cats/J/ApJS/257/59/chimefrb.dat"


def load_seed(seed_path: Path) -> list[dict[str, Any]]:
    doc = json.loads(seed_path.read_text(encoding="utf-8"))
    return list(doc.get("frbs") or [])


def load_literature_seed(path: Path | None = None) -> list[dict[str, Any]]:
    lit_path = path or Path(__file__).resolve().parents[1] / "data" / "frb_literature_seed.json"
    if not lit_path.exists():
        return []
    return load_seed(lit_path)


def tunnel_energy_proxy(row: dict[str, Any]) -> float:
    dm = float(row.get("dm_pc") or 0.0)
    width = float(row.get("width_ms") or 0.0)
    fluence = float(row.get("fluence_jy_ms") or 1.0)
    return dm * width * fluence


def _float_cell(raw: object, default: float = 0.0) -> float:
    if raw is None:
        return default
    text = str(raw).strip()
    if not text or text in ("...", "cdots", "—", "-"):
        return default
    try:
        return float(text)
    except ValueError:
        return default


def _normalize_name(raw: object) -> str | None:
    if raw is None:
        return None
    text = str(raw).strip()
    if not text or text in ("...", "cdots"):
        return None
    return text.replace(" ", "")


def _row_from_chime_csv(row: dict[str, str]) -> dict[str, Any] | None:
    name = (
        _normalize_name(row.get("tns_name"))
        or _normalize_name(row.get("name"))
        or _normalize_name(row.get("FRB"))
        or _normalize_name(row.get("source"))
    )
    if not name:
        return None
    repeater_name = str(row.get("repeater_name") or row.get("repeater") or "").strip()
    repeater_raw = repeater_name.lower()
    repeater = repeater_raw not in ("", "...", "cdots", "nan", "none", "false", "0")
    if repeater_name.lower() in ("false", "0", "no"):
        repeater = False
    dm = _float_cell(row.get("dm_fitb") or row.get("bonsai_dm") or row.get("dm") or row.get("DM"))
    width = _float_cell(row.get("width_fitb") or row.get("bc_width") or row.get("width") or row.get("Width"), 1.0)
    fluence = _float_cell(row.get("fluence") or row.get("Fluence"), 0.1)
    ra = _float_cell(row.get("ra") or row.get("RA"), default=-1.0)
    return {
        "name": name,
        "repeater": repeater,
        "ra_deg": None if ra < 0 else ra,
        "dm_pc": dm,
        "width_ms": width,
        "fluence_jy_ms": fluence,
        "period_s": None,
    }


def _parse_iop_catalog2_excerpt(text: str) -> list[dict[str, Any]]:
    """Parse ApJS Catalog 2 supplementary excerpt (tab blocks)."""
    lines = [ln for ln in text.splitlines() if ln.strip()]
    start = next((i for i, ln in enumerate(lines) if "tns_name" in ln and "ra" in ln), None)
    if start is None:
        return []
    header = [c.strip() for c in lines[start].split("\t") if c.strip()]
    rows_meta: list[dict[str, str]] = []
    i = start + 1
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("ra_dec_notes") or ln.startswith("low_ft_68"):
            break
        if ln.strip() and not ln.startswith("\t(deg)"):
            cells = ln.split("\t")
            if cells and cells[0].strip().startswith("FRB"):
                row = {header[j]: cells[j].strip() if j < len(cells) else "" for j in range(len(header))}
                rows_meta.append(row)
        i += 1

    dm_header_idx = next((j for j, ln in enumerate(lines) if ln.startswith("low_ft_68")), None)
    dm_rows: list[list[str]] = []
    if dm_header_idx is not None:
        j = dm_header_idx + 2
        while j < len(lines) and not lines[j].startswith("bc_width"):
            if lines[j].strip():
                dm_rows.append(lines[j].split("\t"))
            j += 1

    out: list[dict[str, Any]] = []
    for idx, meta in enumerate(rows_meta):
        merged = dict(meta)
        if idx < len(dm_rows) and len(dm_rows[idx]) >= 6:
            merged["dm_fitb"] = dm_rows[idx][5]
            merged["snr_fitb"] = dm_rows[idx][4]
            if len(dm_rows[idx]) >= 1:
                merged["fluence"] = dm_rows[idx][0]
        parsed = _row_from_chime_csv(merged)
        if parsed:
            out.append(parsed)
    return out


def _urlopen_text(url: str, timeout: float = 45.0) -> str:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 FSOT-lab/1.1"})
    ctx = ssl.create_default_context()
    try:
        import certifi  # type: ignore

        ctx.load_verify_locations(certifi.where())
    except ImportError:
        pass
    with urlopen(req, timeout=timeout, context=ctx) as resp:
        return resp.read().decode("utf-8", errors="replace")


def fetch_chime_catalog(url: str, timeout: float = 45.0) -> list[dict[str, Any]]:
    """Fetch CHIME FRB catalog CSV when network available."""
    text = _urlopen_text(url, timeout=timeout)
    if "tns_name" in text and "\t" in text and "Excerpt from Catalog" in text:
        return _parse_iop_catalog2_excerpt(text)
    reader = csv.DictReader(io.StringIO(text))
    out: list[dict[str, Any]] = []
    for row in reader:
        parsed = _row_from_chime_csv(row)
        if parsed:
            out.append(parsed)
    return out


def merge_catalog_rows(*groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Merge FRB rows by name; later groups enrich earlier seed fields."""
    by_name: dict[str, dict[str, Any]] = {}
    for group in groups:
        for row in group:
            name = str(row.get("name") or "")
            if not name:
                continue
            base = by_name.get(name) or {}
            merged = {**base, **row}
            for key in ("ra_deg", "dm_pc", "width_ms", "fluence_jy_ms", "period_s"):
                if merged.get(key) is None and base.get(key) is not None:
                    merged[key] = base[key]
            by_name[name] = merged
    return list(by_name.values())


def fetch_chime_catalog_with_fallback(
    urls: list[str] | None = None,
    timeout: float = 45.0,
) -> tuple[list[dict[str, Any]], str, list[str]]:
    """Try all CHIME catalog sources; merge every successful fetch."""
    candidates = list(urls or [])
    for u in (IOP_CATALOG2_EXCERPT_URL, *CHIME_CATALOG_URLS, VIZIER_CHIME_CAT1_URL):
        if u and u not in candidates:
            candidates.append(u)

    errors: list[str] = []
    merged: list[dict[str, Any]] = []
    sources: list[str] = []
    for url in candidates:
        try:
            rows = fetch_chime_catalog(url, timeout=timeout)
            if rows:
                merged = merge_catalog_rows(merged, rows)
                sources.append(url)
            else:
                errors.append(f"{url}: empty catalog")
        except OSError as exc:
            errors.append(f"{url}: {exc}")
    if merged:
        return merged, "+".join(sources[:3]) + (f"+{len(sources)-3}more" if len(sources) > 3 else ""), errors
    return [], "seed_only", errors