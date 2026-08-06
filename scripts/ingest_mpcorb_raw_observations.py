#!/usr/bin/env python3
"""Fetch raw MPC optical observations for a stratified minor-planet sample.

Uses the official MPC Observations API (ADES JSON) — granular data that orbits
are based on, not literature summaries.

Storage (external drive preferred — large):
  G:/FSOT-PublicData/anomaly_observables/mpcorb_raw_observations/

Monorepo keeps a lightweight pointer + sample index only.

API: https://data.minorplanetcenter.net/api/get-obs
  GET with JSON body: {"desigs": ["1"], "output_format": ["ADES_DF"]}
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MPCORB = ROOT / "vendor" / "mpcorb" / "MPCORB.DAT"
EXTERNAL = Path(r"G:\FSOT-PublicData\anomaly_observables\mpcorb_raw_observations")
LOCAL_FALLBACK = ROOT / "vendor" / "mpcorb" / "raw_observations"
POINTER = ROOT / "predictions" / "external_data_pointers.json"
API = "https://data.minorplanetcenter.net/api/get-obs"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _storage_root() -> Path:
    if EXTERNAL.parent.is_dir() or Path("G:/").exists():
        try:
            EXTERNAL.mkdir(parents=True, exist_ok=True)
            return EXTERNAL
        except OSError:
            pass
    LOCAL_FALLBACK.mkdir(parents=True, exist_ok=True)
    return LOCAL_FALLBACK


def parse_mpcorb_sample_line(line: str) -> dict | None:
    if len(line) < 141 or line.startswith("Des"):
        return None
    try:
        a = float(line[92:103].strip())
        e = float(line[70:79].strip())
        n = float(line[80:91].strip())
        i = float(line[59:68].strip())
        peri = float(line[37:46].strip())
        node = float(line[48:57].strip())
        M = float(line[26:35].strip())
    except ValueError:
        return None
    if a <= 0 or n <= 0:
        return None
    des = line[0:7].strip()
    # numbered objects preferred for API: packed number in des
    u_raw = line[105:106].strip()
    u = int(u_raw) if u_raw.isdigit() else None
    rms = None
    try:
        rs = line[137:141].strip()
        if rs:
            rms = float(rs)
    except ValueError:
        pass
    n_obs = None
    try:
        os_ = line[117:122].strip()
        if os_:
            n_obs = int(os_)
    except ValueError:
        pass
    epoch_packed = line[20:25].strip()
    q = a * (1.0 - e)
    flags_hex = line[161:165].strip() if len(line) >= 165 else ""
    neo = False
    if flags_hex:
        try:
            neo = bool(int(flags_hex, 16) & 2048)
        except ValueError:
            pass
    if neo or q < 1.3:
        regime = "neo"
    elif a > 30:
        regime = "distant"
    elif 2.0 < a < 3.5:
        regime = "main_belt"
    elif 3.5 <= a <= 5.5:
        regime = "outer_belt"
    else:
        regime = "other"
    # designation for API: numbered asteroids use permanent number
    api_desig = des.lstrip("0") if des.isdigit() or (des[:1].isdigit()) else des
    # unpack numbered: "00001" -> "1"
    if des.replace(" ", "").isdigit():
        api_desig = str(int(des.replace(" ", "")))
    return {
        "des_packed": des,
        "api_desig": api_desig,
        "a": a,
        "e": e,
        "i": i,
        "n": n,
        "peri": peri,
        "node": node,
        "M": M,
        "epoch_packed": epoch_packed,
        "U": u,
        "rms_catalog_arcsec": rms,
        "n_obs_catalog": n_obs,
        "regime": regime,
        "neo": neo,
    }


def stratified_sample(path: Path, per_cell: int = 4, max_total: int = 80) -> list[dict]:
    """Sample objects across regime × U cells for raw-obs validation."""
    buckets: dict[str, list[dict]] = {}
    with path.open("rt", encoding="latin-1", errors="replace") as f:
        for line in f:
            row = parse_mpcorb_sample_line(line)
            if not row:
                continue
            # prefer objects with enough obs for meaningful O-C
            if (row.get("n_obs_catalog") or 0) < 20:
                continue
            u = row.get("U")
            if u is None:
                u_key = "U?"
            elif u <= 2:
                u_key = "U0-2"
            elif u <= 5:
                u_key = "U3-5"
            else:
                u_key = "U6-9"
            key = f"{row['regime']}|{u_key}"
            buckets.setdefault(key, [])
            if len(buckets[key]) < per_cell:
                buckets[key].append(row)
            # early exit if full
            if sum(len(v) for v in buckets.values()) >= max_total and all(
                len(v) >= per_cell for v in buckets.values()
            ):
                # keep scanning lightly? just break if we have enough total
                if sum(len(v) for v in buckets.values()) >= max_total:
                    break
    out: list[dict] = []
    for key in sorted(buckets.keys()):
        out.extend(buckets[key][:per_cell])
    return out[:max_total]


def fetch_obs(desig: str, timeout: int = 120) -> dict:
    body = json.dumps(
        {"desigs": [desig], "output_format": ["ADES_DF", "OBS80"]}
    ).encode()
    req = urllib.request.Request(
        API,
        data=body,
        method="GET",
        headers={
            "User-Agent": "FSOT-2.1-Lean/raw-obs-ingest",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if not isinstance(data, list) or not data:
        return {"ok": False, "error": "empty_response", "desig": desig}
    item = data[0]
    ades = item.get("ADES_DF") or []
    return {
        "ok": True,
        "desig": desig,
        "n_obs": len(ades),
        "ADES_DF": ades,
        "OBS80": item.get("OBS80"),
        "fetched_at": _now(),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Ingest raw MPC observations for sample")
    ap.add_argument("--per-cell", type=int, default=3)
    ap.add_argument("--max-objects", type=int, default=48)
    ap.add_argument("--sleep", type=float, default=0.35, help="seconds between API calls")
    ap.add_argument("--timeout", type=int, default=180)
    args = ap.parse_args()

    if not MPCORB.is_file():
        print(f"Missing {MPCORB}")
        return 1

    store = _storage_root()
    obs_dir = store / "objects"
    obs_dir.mkdir(parents=True, exist_ok=True)

    sample = stratified_sample(MPCORB, per_cell=args.per_cell, max_total=args.max_objects)
    print(f"Sample size: {len(sample)} → store {store}")

    results = []
    for i, obj in enumerate(sample):
        desig = obj["api_desig"]
        out_path = obs_dir / f"{desig.replace('/', '_')}.json"
        print(f"[{i+1}/{len(sample)}] {desig} ({obj['regime']} U={obj.get('U')})…", end=" ")
        try:
            payload = fetch_obs(desig, timeout=args.timeout)
            if not payload.get("ok"):
                print("FAIL", payload.get("error"))
                results.append({**obj, "fetch_ok": False, "error": payload.get("error")})
                continue
            # thin save: keep optical obs only with ra/dec/time; cap size
            ades = payload.get("ADES_DF") or []
            optical = []
            for o in ades:
                if (o.get("Obstype") or "optical") not in ("optical", None):
                    continue
                ra, dec, t = o.get("ra"), o.get("dec"), o.get("obstime")
                if ra is None or dec is None or t is None:
                    continue
                optical.append(
                    {
                        "obstime": t,
                        "ra_deg": float(ra) if ra is not None else None,
                        "dec_deg": float(dec) if dec is not None else None,
                        "stn": o.get("stn"),
                        "mag": o.get("mag"),
                        "band": o.get("band"),
                        "mode": o.get("mode"),
                        "astcat": o.get("astcat"),
                        "rmsra": o.get("rmsra"),
                        "rmsdec": o.get("rmsdec"),
                        "ref": o.get("ref"),
                    }
                )
            record = {
                "orbit": obj,
                "n_obs_api": payload.get("n_obs"),
                "n_optical_kept": len(optical),
                "observations": optical,
                "fetched_at": payload.get("fetched_at"),
                "source": API,
            }
            out_path.write_text(json.dumps(record), encoding="utf-8")
            print(f"ok n_api={payload.get('n_obs')} optical={len(optical)}")
            results.append(
                {
                    **obj,
                    "fetch_ok": True,
                    "n_obs_api": payload.get("n_obs"),
                    "n_optical_kept": len(optical),
                    "path": str(out_path).replace("\\", "/"),
                }
            )
        except urllib.error.HTTPError as e:
            print(f"HTTP {e.code}")
            results.append({**obj, "fetch_ok": False, "error": f"HTTP {e.code}"})
        except Exception as e:
            print(f"ERR {e}")
            results.append({**obj, "fetch_ok": False, "error": str(e)})
        time.sleep(args.sleep)

    index = {
        "generated_at": _now(),
        "storage_root": str(store).replace("\\", "/"),
        "api": API,
        "sample_size": len(sample),
        "fetched_ok": sum(1 for r in results if r.get("fetch_ok")),
        "objects": results,
    }
    (store / "sample_index.json").write_text(json.dumps(index, indent=2), encoding="utf-8")

    # monorepo pointer
    ptr = {}
    if POINTER.is_file():
        try:
            ptr = json.loads(POINTER.read_text(encoding="utf-8"))
        except Exception:
            ptr = {}
    ptr.setdefault("external_root", "G:/FSOT-PublicData")
    ptr.setdefault("datasets", {})
    ptr["datasets"]["mpcorb_raw_observations"] = {
        "path": str(store).replace("\\", "/"),
        "index": str(store / "sample_index.json").replace("\\", "/"),
        "updated_at": _now(),
        "fetched_ok": index["fetched_ok"],
        "sample_size": index["sample_size"],
    }
    POINTER.parent.mkdir(parents=True, exist_ok=True)
    POINTER.write_text(json.dumps(ptr, indent=2), encoding="utf-8")

    # lightweight monorepo copy of index only
    mono = ROOT / "data" / "mpcorb_raw_obs_sample_index.json"
    mono.write_text(json.dumps(index, indent=2), encoding="utf-8")
    print(f"Index: {store / 'sample_index.json'}")
    print(f"Monorepo index: {mono}")
    print(f"OK {index['fetched_ok']}/{index['sample_size']}")
    return 0 if index["fetched_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
