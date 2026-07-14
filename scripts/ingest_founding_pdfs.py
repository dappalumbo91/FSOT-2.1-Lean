#!/usr/bin/env python3
"""Extract text from founding PDFs (06_Founding-Archives or legacy drive roots)."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "vendor" / "founding_corpus" / "pdf_extracted"
MANIFEST_PATH = ROOT / "vendor" / "founding_corpus" / "pdf_ingest_manifest.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import founding_archive_roots, rel_repo_path  # noqa: E402

MIN_CHARS_OK = 200
HALLUCINATION_ACCURACY_PAT = re.compile(
    r"99\.999|100\.0{3,}\s*%|zero\s*percent|0%\s*difference|billion\s*data\s*points|"
    r"4\.578\s*billion|11\.828\s*billion",
    re.I,
)


def _safe_name(path: Path) -> str:
    h = hashlib.sha256(str(path).encode("utf-8")).hexdigest()[:12]
    stem = re.sub(r"[^\w\-]+", "_", path.stem)[:60]
    return f"{stem}__{h}"


def _extract_pdf(pdf_path: Path) -> tuple[str, int, str | None]:
    if PdfReader is None:
        raise SystemExit("Install pypdf: pip install pypdf")
    try:
        reader = PdfReader(str(pdf_path))
        pages = []
        for page in reader.pages:
            try:
                pages.append(page.extract_text() or "")
            except Exception:
                pages.append("")
        text = "\n\n".join(pages).strip()
        return text, len(reader.pages), None
    except Exception as exc:
        return "", 0, str(exc)


def _fallback_sources(pdf_path: Path) -> list[Path]:
    """When .fsot_updated.pdf is corrupt, try sibling canonical copies."""
    candidates: list[Path] = []
    name = pdf_path.name
    parent = pdf_path.parent
    if name.endswith(".fsot_updated.pdf"):
        stem = name[: -len(".fsot_updated.pdf")]
        candidates.extend([
            parent.parent / f"{stem}.pdf",
            parent / f"{stem}.pdf",
            parent.parent / f"{stem}.docx",
            parent / f"{stem}.docx",
        ])
    candidates.extend([
        pdf_path.with_suffix(".docx"),
        pdf_path.parent.parent / pdf_path.name,
    ])
    seen: set[str] = set()
    out: list[Path] = []
    for cand in candidates:
        key = str(cand).lower()
        if key in seen or cand == pdf_path:
            continue
        seen.add(key)
        if cand.exists() and cand.is_file():
            out.append(cand)
    return out


def _extract_with_fallback(pdf_path: Path) -> tuple[str, int, str | None, str | None]:
    text, page_count, err = _extract_pdf(pdf_path)
    if not err and len(text) >= MIN_CHARS_OK:
        return text, page_count, None, None
    for alt in _fallback_sources(pdf_path):
        if alt.suffix.lower() == ".docx":
            alt_text, alt_pages, alt_err = _extract_docx(alt)
        else:
            alt_text, alt_pages, alt_err = _extract_pdf(alt)
        if not alt_err and len(alt_text) >= MIN_CHARS_OK:
            return alt_text, alt_pages, None, str(alt)
    return text, page_count, err, None


def _extract_docx(docx_path: Path) -> tuple[str, int, str | None]:
    try:
        import zipfile
        import xml.etree.ElementTree as ET

        with zipfile.ZipFile(docx_path) as zf:
            xml = zf.read("word/document.xml")
        root = ET.fromstring(xml)
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        paras = []
        for para in root.iterfind(".//w:p", ns):
            parts = [node.text for node in para.iterfind(".//w:t", ns) if node.text]
            if parts:
                paras.append("".join(parts))
        text = "\n\n".join(paras).strip()
        return text, max(len(paras), 1), None
    except Exception as exc:
        return "", 0, str(exc)


def ingest_pdfs(
    roots: list[Path] | None = None,
    out_dir: Path = OUT_DIR,
    manifest_path: Path = MANIFEST_PATH,
) -> dict:
    roots = roots or founding_archive_roots()
    if not roots:
        raise SystemExit(
            "No founding archive roots found. Bundle 06_Founding-Archives on the drive "
            "or set FSOT_FOUNDING_ROOT."
        )
    out_dir.mkdir(parents=True, exist_ok=True)

    entries: list[dict] = []
    ok = 0
    low_yield = 0
    failed = 0

    for root in roots:
        if not root.exists():
            continue
        for pdf in sorted(root.rglob("*.pdf")):
            text, page_count, err, fallback_source = _extract_with_fallback(pdf)
            rel_root = "fsuft_aasb" if "fsuft aasb" in str(pdf).lower() else "fsot_tech"
            out_name = _safe_name(pdf)
            out_txt = out_dir / f"{out_name}.txt"
            accuracy_flags = bool(HALLUCINATION_ACCURACY_PAT.search(text)) if text else False

            status = "ok"
            note = None
            if err:
                status = "error"
                failed += 1
            elif len(text) < MIN_CHARS_OK:
                status = "low_yield"
                low_yield += 1
            else:
                ok += 1
                out_txt.write_text(text, encoding="utf-8")
                if fallback_source:
                    note = f"Extracted via fallback source: {fallback_source}"

            if accuracy_flags:
                note = (
                    (note + " | " if note else "")
                    + "Founding accuracy percentages are not trusted unless re-verified in FSOT 2.1"
                )

            entries.append({
                "source_pdf": str(pdf),
                "fallback_source": fallback_source,
                "founding_root": rel_root,
                "output_txt": rel_repo_path(out_txt) if status == "ok" else None,
                "page_count": page_count,
                "char_count": len(text),
                "status": status,
                "error": err,
                "accuracy_claim_flags": accuracy_flags,
                "note": note,
            })

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pdf_count": len(entries),
        "extracted_ok": ok,
        "low_yield": low_yield,
        "failed": failed,
        "accuracy_flagged_pdfs": sum(1 for e in entries if e.get("accuracy_claim_flags")),
        "entries": entries,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"PDFs: {len(entries)} | ok={ok} low_yield={low_yield} failed={failed}")
    print(f"Manifest: {manifest_path}")
    return manifest


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=OUT_DIR)
    ap.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    args = ap.parse_args()
    m = ingest_pdfs(out_dir=args.out, manifest_path=args.manifest)
    return 0 if m["extracted_ok"] > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())