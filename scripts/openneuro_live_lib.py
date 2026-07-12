"""OpenNeuro GraphQL live dataset index."""

from __future__ import annotations

import json
import urllib.request

OPENNEURO_URL = "https://openneuro.org/crn/graphql"


def _graphql(query: str) -> dict:
    req = urllib.request.Request(
        OPENNEURO_URL,
        data=json.dumps({"query": query}).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "FSOT-2.1-Lean/openneuro"},
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        return json.loads(resp.read().decode())


def fetch_openneuro_datasets(*, pages: int = 6, page_size: int = 10) -> list[dict]:
    datasets: list[dict] = []
    for modality in ("EEG", "MRI", "iEEG", "MEG"):
        cursor = None
        for _ in range(pages):
            after = f', after: "{cursor}"' if cursor else ""
            q = (
                "{ datasets(first: %d, modality: \"%s\"%s) {"
                " pageInfo { hasNextPage }"
                " edges { cursor node { id name } } } }"
            ) % (page_size, modality, after)
            payload = _graphql(q)
            block = (payload.get("data") or {}).get("datasets") or {}
            edges = block.get("edges") or []
            for edge in edges:
                node = edge.get("node") or {}
                datasets.append(
                    {
                        "id": node.get("id"),
                        "name": node.get("name"),
                        "modality_filter": modality,
                    }
                )
            page = block.get("pageInfo") or {}
            if not page.get("hasNextPage") or not edges:
                break
            cursor = edges[-1].get("cursor")

    seen: set[str] = set()
    unique: list[dict] = []
    for row in datasets:
        ds_id = str(row.get("id") or "")
        if not ds_id or ds_id in seen:
            continue
        seen.add(ds_id)
        unique.append(row)
    return unique