#!/usr/bin/env python3
"""Propose DOI and arXiv identifiers for citation fields that lack one.

Scans data/*.json the same way as the milestone-2 citation audit: a one-line
string value whose key matches reference, citation, doi, bibliography, paper,
or literature. Values that already contain a DOI, arXiv id, or URL are counted
and skipped. The rest are looked up at Crossref and, when the query is long
enough to be a title, at arXiv.

Writes data/citation_enrichment_proposals.json. This script does not edit
citation fields. High-confidence rows are proposals for review. Nothing below
that bar is applied, because nothing is applied.

  python scripts/enrich_citations.py
  python scripts/enrich_citations.py --scan-only
  python scripts/enrich_citations.py --limit 20

Reruns skip queries already stored in the proposals file.
"""
from __future__ import annotations

import argparse
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = DATA / "citation_enrichment_proposals.json"
UA = "fsot-lean-citation-enrich/1.0 (mailto:dappalumbo91@users.noreply.github.com)"

# Same key rule as FSOT-2.1-Cpp tools/check_citations.py.
CITE_KEYS = re.compile(r"(reference|citation|doi|bibliograph|paper|literature)", re.I)
LINE_RE = re.compile(r'^\s*"([^"]+)"\s*:\s*"(.*)"\s*,?\s*$')
DOI_RE = re.compile(r"\b10\.\d{4,9}/[^\s\"<>\]\}\\,;|`']+", re.I)
ARXIV_RE = re.compile(
    r"arxiv(?:\.org/(?:abs|pdf)/|[:\s]\s*)((?:\d{4}\.\d{4,5}|[a-z\-]+(?:\.[A-Z]{2})?/\d{7}))",
    re.I,
)
URL_RE = re.compile(r"https?://", re.I)
TOKEN_RE = re.compile(r"[a-z0-9]+")
STOP = {
    "the", "a", "an", "of", "and", "for", "in", "on", "with", "to", "from",
    "by", "or", "its", "at", "as", "via", "per",
}

# A proposal is high confidence only when every one of these holds.
# Crossref relevance scores for an exact title are often ~20-40, so the
# bar is title-token containment, not a raw score cutoff.
MIN_QUERY_TOKENS = 4
MIN_CONTAINMENT = 0.85
SECOND_HIT_CONTAINMENT_BELOW = 0.5
CROSSREF_SLEEP_S = 0.2
ARXIV_SLEEP_S = 3.1

KNOWN_UNRESOLVED = {
    "doi": "10.1152/physrev.00019.2014",
    "file": "data/toe_contested_sector_refresh.json",
    "reference": "Human brain metabolic power (physiology)",
    "status": "unresolved",
    "note": (
        "doi.org handle responseCode 100 (not found). Crossref bibliographic "
        "search of the reference string does not return a Physiological Reviews "
        "article. No replacement DOI was assigned."
    ),
}


def has_identifier(value: str) -> bool:
    return bool(DOI_RE.search(value) or ARXIV_RE.search(value) or URL_RE.search(value))


def tokens(text: str) -> list[str]:
    return [t for t in TOKEN_RE.findall(text.lower()) if t not in STOP and len(t) > 1]


def containment(query: list[str], title: str) -> float:
    if not query:
        return 0.0
    got = set(tokens(title))
    return sum(1 for t in query if t in got) / len(query)


def scan() -> tuple[list[dict], dict]:
    """Return distinct missing queries and the audit-style counts."""
    grouped: dict[str, dict] = {}
    total = 0
    with_id = 0
    distinct: set[str] = set()
    distinct_with: set[str] = set()
    for path in sorted(DATA.glob("*.json")):
        rel = path.relative_to(ROOT).as_posix()
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for ln, line in enumerate(lines, 1):
            match = LINE_RE.match(line)
            if not match or not CITE_KEYS.search(match.group(1)):
                continue
            key = match.group(1)
            if key.endswith(("_pct", "_ms", "_s", "_ns")):
                continue
            val = match.group(2)
            total += 1
            distinct.add(val)
            identified = has_identifier(val)
            if identified:
                with_id += 1
                distinct_with.add(val)
                continue
            row = grouped.get(val)
            if row is None:
                row = {
                    "query": val,
                    "occurrences": 0,
                    "examples": [],
                }
                grouped[val] = row
            row["occurrences"] += 1
            if len(row["examples"]) < 5:
                row["examples"].append({"file": rel, "line": ln, "field": key})
    summary = {
        "citation_field_values": total,
        "values_with_identifier": with_id,
        "distinct_values": len(distinct),
        "distinct_with_identifier": len(distinct_with),
        "distinct_missing": len(grouped),
    }
    return list(grouped.values()), summary


def _http_json(url: str) -> tuple[int | str, dict | None]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return exc.code, None
    except Exception as exc:  # noqa: BLE001
        return f"ERR:{type(exc).__name__}", None


def _http_bytes(url: str) -> tuple[int | str, bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/atom+xml"})
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, b""
    except Exception as exc:  # noqa: BLE001
        return f"ERR:{type(exc).__name__}", b""


def crossref_hits(query: str) -> list[dict]:
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(
        {
            "query.bibliographic": query[:500],
            "rows": 3,
        }
    )
    for attempt in range(4):
        status, doc = _http_json(url)
        if status == 429:
            time.sleep(2.0 * (attempt + 1))
            continue
        if status != 200 or not doc:
            return []
        hits = []
        qtok = tokens(query)
        for item in doc.get("message", {}).get("items") or []:
            title = (item.get("title") or [""])[0]
            year = ((item.get("issued") or {}).get("date-parts") or [[None]])[0][0]
            hits.append(
                {
                    "doi": item.get("DOI"),
                    "title": title,
                    "year": year,
                    "container": (item.get("container-title") or [""])[0],
                    "score": item.get("score"),
                    "containment": round(containment(qtok, title), 4),
                }
            )
        return hits
    return []


def arxiv_hits(query: str) -> list[dict]:
    # Title search. Short labels are not sent here.
    phrase = " ".join(tokens(query)[:12])
    if not phrase:
        return []
    url = (
        "http://export.arxiv.org/api/query?"
        + urllib.parse.urlencode(
            {"search_query": f'ti:"{phrase}"', "start": 0, "max_results": 3}
        )
    )
    status, body = _http_bytes(url)
    if status != 200 or not body:
        return []
    ns = {"a": "http://www.w3.org/2005/Atom"}
    try:
        root = ET.fromstring(body)
    except ET.ParseError:
        return []
    qtok = tokens(query)
    hits = []
    for entry in root.findall("a:entry", ns):
        title = " ".join((entry.findtext("a:title", "", ns) or "").split())
        if not title or title == "Error":
            continue
        raw_id = (entry.findtext("a:id", "", ns) or "").split("/abs/")[-1]
        arxiv_id = re.sub(r"v\d+$", "", raw_id)
        published = entry.findtext("a:published", "", ns) or ""
        year = int(published[:4]) if published[:4].isdigit() else None
        hits.append(
            {
                "arxiv_id": arxiv_id,
                "title": title,
                "year": year,
                "containment": round(containment(qtok, title), 4),
            }
        )
    return hits


def judge(query: str, crossref: list[dict], arxiv: list[dict]) -> tuple[str, str]:
    qtok = tokens(query)
    best_c = crossref[0] if crossref else None
    second_c = crossref[1] if len(crossref) > 1 else None
    best_a = arxiv[0] if arxiv else None
    best = None
    source = ""
    if best_c and (not best_a or best_c["containment"] >= best_a["containment"]):
        best, source = best_c, "crossref"
        second = second_c
    elif best_a:
        best, source = best_a, "arxiv"
        second = arxiv[1] if len(arxiv) > 1 else None
    else:
        return "none", "No Crossref or arXiv hit."
    if len(qtok) < MIN_QUERY_TOKENS:
        return "low", (
            f"Query has {len(qtok)} content tokens, under {MIN_QUERY_TOKENS}. "
            "Short labels are not auto-matched."
        )
    if best["containment"] < MIN_CONTAINMENT:
        return "low", (
            f"Best {source} containment {best['containment']} is under {MIN_CONTAINMENT}."
        )
    if second is not None and second["containment"] >= SECOND_HIT_CONTAINMENT_BELOW:
        if source == "crossref":
            s1 = best_c.get("score") or 0
            s2 = (second_c or {}).get("score") or 0
            if not (s1 and s2 and s1 >= 1.1 * s2):
                return "low", (
                    "A second hit also overlaps the query, and the score margin "
                    "is under 1.1."
                )
        else:
            return "low", "A second arXiv hit also overlaps the query."
    return "high", (
        f"Top {source} title contains {best['containment']} of the query tokens, "
        f"the query has {len(qtok)} content tokens, and the next hit is separated."
    )


def load_existing() -> dict[str, dict]:
    if not OUT.exists():
        return {}
    doc = json.loads(OUT.read_text(encoding="utf-8"))
    return {row["query"]: row for row in doc.get("proposals") or [] if row.get("query")}


def write_out(summary: dict, proposals: list[dict]) -> None:
    counts = {"high": 0, "low": 0, "none": 0}
    for row in proposals:
        counts[row["confidence"]] = counts.get(row["confidence"], 0) + 1
    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "auto_applied": False,
        "high_confidence_rule": {
            "min_query_tokens": MIN_QUERY_TOKENS,
            "min_token_containment": MIN_CONTAINMENT,
            "second_hit_containment_below": SECOND_HIT_CONTAINMENT_BELOW,
            "crossref_score_margin": 1.1,
            "statement": (
                "High confidence requires at least 4 content tokens, containment "
                "of those tokens in the top title of at least 0.85, and a next hit "
                "below 0.50 containment (or a Crossref score at least 1.1 times the "
                "runner-up). Rows under that bar are not applied. This file applies none."
            ),
        },
        "scan": summary,
        "counts": counts,
        "known_unresolved": [KNOWN_UNRESOLVED],
        "proposals": proposals,
    }
    text = json.dumps(doc, indent=2, ensure_ascii=True, allow_nan=False) + "\n"
    OUT.write_text(text, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scan-only", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()
    missing, summary = scan()
    print(json.dumps(summary))
    if args.scan_only:
        return 0
    done = load_existing()
    proposals = list(done.values())
    looked = 0
    for row in missing:
        if row["query"] in done:
            continue
        if args.limit and looked >= args.limit:
            break
        qtok = tokens(row["query"])
        cref = crossref_hits(row["query"])
        time.sleep(CROSSREF_SLEEP_S)
        ax = []
        if len(qtok) >= MIN_QUERY_TOKENS:
            ax = arxiv_hits(row["query"])
            time.sleep(ARXIV_SLEEP_S)
        confidence, reason = judge(row["query"], cref, ax)
        proposal = {
            "query": row["query"],
            "occurrences": row["occurrences"],
            "examples": row["examples"],
            "confidence": confidence,
            "apply": False,
            "reason": reason,
            "crossref": cref[:2],
            "arxiv": ax[:2],
        }
        proposals.append(proposal)
        done[row["query"]] = proposal
        looked += 1
        if looked % 25 == 0:
            write_out(summary, proposals)
            print(f"checkpoint {looked} new, {len(proposals)} stored", flush=True)
    proposals.sort(key=lambda r: (-r["occurrences"], r["query"]))
    write_out(summary, proposals)
    counts: dict[str, int] = {}
    for row in proposals:
        counts[row["confidence"]] = counts.get(row["confidence"], 0) + 1
    print("wrote", OUT.relative_to(ROOT).as_posix(), "counts", counts, "new", looked)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
