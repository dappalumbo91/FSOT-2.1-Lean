#!/usr/bin/env python3
"""Ingest Riess+2022 Table 2 (full NIR) + public host redshifts.

Table 2 photometry: PantheonPlusSH0ES/DataRelease SH0ES_Data/table2.tex
(local copy data/sh0es_r22_table2.tex if present).

Redshifts: Pantheon+ zCMB (Carr+2022 / Scolnic+2022) for calibrator SNe,
NED heliocentric Velocity as a host-level cross-check converted to CMB
with the Planck 2018 solar dipole. Not a Riess per-host H0 table.
"""

from __future__ import annotations

import json
import math
import time
import urllib.request
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TEX = DATA / "sh0es_r22_table2.tex"
DAT = DATA / "sh0es_r22_full_nir_cepheids.dat"
REDSHIFT_OUT = DATA / "sh0es_host_redshifts.json"
COORD_PATH = DATA / "sh0es_host_coordinates.json"

TABLE2_URL = (
    "https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/"
    "main/SH0ES_Data/table2.tex"
)
PANTHEON_URL = (
    "https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/"
    "main/Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon+SH0ES.dat"
)

# Riess+2022 Table 6 μ_host (Cepheid-only, no SN in any host). Published
# approximation — not lstsq_results.txt, not an independent TRGB modulus.
TABLE6_MU_HOST = {
    "M101": 29.178,
    "M1337": 32.920,
    "N0105": 34.527,
    "N105A": 34.527,
    "N0691": 32.830,
    "N0976": 33.709,
    "N976A": 33.709,
    "N1015": 32.563,
    "N1309": 32.541,
    "N1365": 31.378,
    "N1448": 31.287,
    "N1559": 31.491,
    "N2442": 31.450,
    "N2525": 32.051,
    "N2608": 32.612,
    "N3021": 32.464,
    "N3147": 33.014,
    "N3254": 32.331,
    "N3370": 32.120,
    "N3447": 31.936,
    "N3583": 32.804,
    "N3972": 31.635,
    "N3982": 31.722,
    "N4038": 31.603,
    "N4424": 30.844,
    "N4536": 30.835,
    "N4639": 31.812,
    "N4680": 32.599,
    "N5468": 33.116,
    "N5584": 31.772,
    "N5643": 30.546,
    "N5728": 33.094,
    "N5861": 32.223,
    "N5917": 32.363,
    "N7250": 31.628,
    "N7329": 33.246,
    "N7541": 32.500,
    "N7678": 33.187,
    "U9391": 32.848,
}

# Table 6 SN names used to match Pantheon+ CID.
TABLE6_SN = {
    "M101": ["2011fe"],
    "M1337": ["2006D"],
    "N105A": ["2007A"],
    "N0691": ["2005W"],
    "N976A": ["1999dq"],
    "N1015": ["2009ig"],
    "N1309": ["2002fk"],
    "N1365": ["2012fr"],
    "N1448": ["2001el", "2021pit"],
    "N1559": ["2005df"],
    "N2442": ["2015F"],
    "N2525": ["2018gv"],
    "N2608": ["2001bg"],
    "N3021": ["1995al"],
    "N3147": ["2021hpr", "1997bq", "2008fv"],
    "N3254": ["2019np"],
    "N3370": ["1994ae"],
    "N3447": ["2012ht"],
    "N3583": ["ASASSN-15so", "15so"],
    "N3972": ["2011by"],
    "N3982": ["1998aq"],
    "N4038": ["2007sr"],
    "N4424": ["2012cg"],
    "N4536": ["1981B"],
    "N4639": ["1990N"],
    "N4680": ["1997bp"],
    "N5468": ["1999cp", "2002cr"],
    "N5584": ["2007af"],
    "N5643": ["2013aa", "2017cbv"],
    "N5728": ["2009Y"],
    "N5861": ["2017erp"],
    "N5917": ["2005cf"],
    "N7250": ["2013dy"],
    "N7329": ["2006bh"],
    "N7541": ["1998dh"],
    "N7678": ["2002dp"],
    "U9391": ["2003du"],
}

ANCHORS = {"N4258", "M31", "LMC", "SMC"}

# Planck 2018 CMB dipole (solar motion wrt CMB).
CMB_APEX_L_DEG = 264.021
CMB_APEX_B_DEG = 48.253
CMB_V_KMS = 369.82
C_KMS = 299792.458

NED_NAME = {
    "M101": "M101",
    "M1337": "Mrk 1337",
    "N105A": "NGC 105",
    "N0691": "NGC 691",
    "N976A": "NGC 976",
    "N1015": "NGC 1015",
    "N1309": "NGC 1309",
    "N1365": "NGC 1365",
    "N1448": "NGC 1448",
    "N1559": "NGC 1559",
    "N2442": "NGC 2442",
    "N2525": "NGC 2525",
    "N2608": "NGC 2608",
    "N3021": "NGC 3021",
    "N3147": "NGC 3147",
    "N3254": "NGC 3254",
    "N3370": "NGC 3370",
    "N3447": "NGC 3447",
    "N3583": "NGC 3583",
    "N3972": "NGC 3972",
    "N3982": "NGC 3982",
    "N4038": "NGC 4038",
    "N4258": "NGC 4258",
    "N4424": "NGC 4424",
    "N4536": "NGC 4536",
    "N4639": "NGC 4639",
    "N4680": "NGC 4680",
    "N5468": "NGC 5468",
    "N5584": "NGC 5584",
    "N5643": "NGC 5643",
    "N5728": "NGC 5728",
    "N5861": "NGC 5861",
    "N5917": "NGC 5917",
    "N7250": "NGC 7250",
    "N7329": "NGC 7329",
    "N7541": "NGC 7541",
    "N7678": "NGC 7678",
    "U9391": "UGC 9391",
    "M31": "M31",
    "LMC": "LMC",
    "SMC": "SMC",
}


def _download(url: str, dest: Path, timeout: int = 120) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "FSOT-2.1-Lean/sh0es-ingest"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        dest.write_bytes(resp.read())


def convert_table2(tex_path: Path, dat_path: Path) -> OrderedDict[str, int]:
    counts: OrderedDict[str, int] = OrderedDict()
    lines_out = [
        "Host\tra\tdec        ID    period V-I  sigma  H  sigma  metal-8.69  HST",
        "------------------------------------------------------------------------------",
    ]
    for line in tex_path.read_text(encoding="utf-8", errors="replace").splitlines():
        if "&" not in line or line.strip().startswith("\\"):
            continue
        parts = [x.strip() for x in line.replace("\\\\", "").split("&")]
        if len(parts) < 11:
            continue
        host = parts[0]
        try:
            ra = float(parts[1])
            dec = float(parts[2])
            ident = parts[3]
            period = float(parts[4])
            vi = float(parts[5])
            s_vi = float(parts[6])
            hmag = float(parts[7])
            s_h = float(parts[8])
            metal = float(parts[9])
        except ValueError:
            continue
        if period <= 0:
            continue
        note = parts[10] if len(parts) > 10 else "HST"
        counts[host] = counts.get(host, 0) + 1
        lines_out.append(
            f"{host} {ra:.5f} {dec:.6f} {ident} {period:g} {vi:.2f} {s_vi:.2f} "
            f"{hmag:.2f} {s_h:.2f} {metal:.2f} {note}"
        )
    dat_path.write_text("\n".join(lines_out) + "\n", encoding="utf-8")
    return counts


def _norm_cid(cid: str) -> str:
    s = cid.strip().strip('"').upper().replace("SN", "").replace(" ", "")
    s = s.replace("ASASSN-", "ASASSN")
    return s


def load_pantheon_calibrators(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8", errors="replace")
    rows: list[dict] = []
    header: list[str] | None = None
    for line in text.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split()
        if header is None:
            header = parts
            continue
        if len(parts) < len(header):
            continue
        rec = dict(zip(header, parts))
        try:
            is_cal = int(float(rec.get("IS_CALIBRATOR", "0")))
        except ValueError:
            is_cal = 0
        if is_cal != 1:
            continue
        try:
            rows.append(
                {
                    "cid": rec.get("CID", ""),
                    "zCMB": float(rec["zCMB"]),
                    "zHEL": float(rec["zHEL"]),
                    "zHD": float(rec["zHD"]),
                    "vpec": float(rec.get("VPEC", "0") or 0),
                    "host_ra": float(rec.get("HOST_RA", "nan")),
                    "host_dec": float(rec.get("HOST_DEC", "nan")),
                    "ceph_dist": float(rec.get("CEPH_DIST", "nan")),
                }
            )
        except (KeyError, ValueError):
            continue
    return rows


def match_pantheon(sns: list[str], cals: list[dict]) -> dict | None:
    want = {_norm_cid(s) for s in sns}
    hits = [r for r in cals if _norm_cid(r["cid"]) in want]
    if not hits:
        # substring (1999dq vs 99dq)
        hits = [
            r
            for r in cals
            if any(_norm_cid(r["cid"]).endswith(w) or w.endswith(_norm_cid(r["cid"])) for w in want)
        ]
    if not hits:
        return None
    zcmb = sum(h["zCMB"] for h in hits) / len(hits)
    zhel = sum(h["zHEL"] for h in hits) / len(hits)
    return {
        "zCMB": zcmb,
        "zHEL": zhel,
        "n_lc": len(hits),
        "cids": sorted({h["cid"] for h in hits}),
        "host_ra": hits[0]["host_ra"],
        "host_dec": hits[0]["host_dec"],
    }


def _eq_to_gal(ra_deg: float, dec_deg: float) -> tuple[float, float]:
    """J2000 equatorial → galactic (degrees)."""
    ra = math.radians(ra_deg)
    dec = math.radians(dec_deg)
    # IAU 1958 galactic pole
    ra0 = math.radians(192.85948)
    dec0 = math.radians(27.12825)
    l0 = math.radians(122.93192)
    sin_b = math.sin(dec) * math.sin(dec0) + math.cos(dec) * math.cos(dec0) * math.cos(ra - ra0)
    b = math.asin(max(-1.0, min(1.0, sin_b)))
    y = math.cos(dec) * math.sin(ra - ra0)
    x = math.sin(dec) * math.cos(dec0) - math.cos(dec) * math.sin(dec0) * math.cos(ra - ra0)
    l = l0 - math.atan2(y, x)
    l = l % (2 * math.pi)
    return math.degrees(l), math.degrees(b)


def helio_to_cmb(v_hel: float, ra_deg: float, dec_deg: float) -> float:
    l, b = _eq_to_gal(ra_deg, dec_deg)
    l0 = math.radians(CMB_APEX_L_DEG)
    b0 = math.radians(CMB_APEX_B_DEG)
    lg = math.radians(l)
    bg = math.radians(b)
    cosang = math.sin(bg) * math.sin(b0) + math.cos(bg) * math.cos(b0) * math.cos(lg - l0)
    return v_hel + CMB_V_KMS * cosang


def ned_query(name: str) -> dict | None:
    try:
        from astroquery.ipac.ned import Ned
    except Exception:
        return None
    try:
        t = Ned.query_object(name)
    except Exception:
        return None
    if t is None or len(t) == 0:
        return None
    row = t[0]
    try:
        vel = float(row["Velocity"])
    except Exception:
        vel = float("nan")
    try:
        z = float(row["Redshift"])
    except Exception:
        z = float("nan")
    try:
        ra = float(row["RA"])
        dec = float(row["DEC"])
    except Exception:
        ra = dec = float("nan")
    return {
        "ned_name": str(row["Object Name"]),
        "v_helio_kms": vel,
        "z_ned": z,
        "ra_deg": ra,
        "dec_deg": dec,
    }


def _coord_lookup() -> dict[str, dict]:
    if not COORD_PATH.is_file():
        return {}
    doc = json.loads(COORD_PATH.read_text(encoding="utf-8"))
    out: dict[str, dict] = {}
    for h in doc.get("hosts", []):
        out[str(h.get("name") or "")] = h
    return out


def main() -> int:
    if not TEX.is_file():
        print(f"Downloading Table 2 → {TEX}")
        _download(TABLE2_URL, TEX)
    counts = convert_table2(TEX, DAT)
    print(f"Wrote {DAT}  hosts={len(counts)} stars={sum(counts.values())}")
    for host, n in counts.items():
        print(f"  {host:8s} {n:4d}")

    pan_path = Path.home() / "AppData" / "Local" / "Temp" / "Pantheon+SH0ES.dat"
    if not pan_path.is_file():
        print(f"Downloading Pantheon+ → {pan_path}")
        _download(PANTHEON_URL, pan_path)
    cals = load_pantheon_calibrators(pan_path)
    print(f"Pantheon+ calibrator light curves: {len(cals)}")

    coords = _coord_lookup()
    hosts: dict[str, dict] = {}
    sn_hosts = [h for h in counts if h not in ANCHORS]
    for host in list(counts.keys()):
        rec: dict = {
            "host": host,
            "n_cepheids": int(counts[host]),
            "is_anchor": host in ANCHORS,
            "ned_name": NED_NAME.get(host, host),
        }
        t6_key = host if host in TABLE6_MU_HOST else None
        if t6_key:
            rec["mu_table6"] = TABLE6_MU_HOST[t6_key]
        sns = TABLE6_SN.get(host, [])
        rec["sns"] = sns
        if sns:
            pan = match_pantheon(sns, cals)
            if pan:
                rec["zCMB"] = pan["zCMB"]
                rec["zHEL"] = pan["zHEL"]
                rec["cz_cmb_kms"] = pan["zCMB"] * C_KMS
                rec["pantheon_cids"] = pan["cids"]
                rec["pantheon_n_lc"] = pan["n_lc"]
                if math.isfinite(pan["host_ra"]) and pan["host_ra"] > -90:
                    rec["ra_deg"] = pan["host_ra"]
                    rec["dec_deg"] = pan["host_dec"]
            else:
                rec["pantheon_match"] = False
        ned = ned_query(NED_NAME.get(host, host))
        time.sleep(0.25)
        if ned:
            rec["ned"] = ned
            rec.setdefault("ra_deg", ned["ra_deg"])
            rec.setdefault("dec_deg", ned["dec_deg"])
            if math.isfinite(ned["v_helio_kms"]) and math.isfinite(ned.get("ra_deg", float("nan"))):
                rec["ned_v_cmb_kms"] = helio_to_cmb(
                    ned["v_helio_kms"], ned["ra_deg"], ned["dec_deg"]
                )
        # fill coords from existing file if still missing
        for alias in (host, rec.get("ned_name"), f"NGC{host[1:]}" if host.startswith("N") else ""):
            if alias and alias in coords:
                rec.setdefault("ra_deg", coords[alias].get("ra_deg"))
                rec.setdefault("dec_deg", coords[alias].get("dec_deg"))
        if "zCMB" not in rec and rec.get("ned_v_cmb_kms") is not None:
            rec["cz_cmb_kms"] = rec["ned_v_cmb_kms"]
            rec["zCMB"] = rec["ned_v_cmb_kms"] / C_KMS
            rec["z_source"] = "NED_helio_plus_Planck2018_dipole"
        elif "zCMB" in rec:
            rec["z_source"] = "Pantheon+_zCMB"
        hosts[host] = rec
        print(
            f"  {host:8s} zCMB={rec.get('zCMB')} cz={rec.get('cz_cmb_kms')} "
            f"src={rec.get('z_source')} pan={rec.get('pantheon_cids')}"
        )

    n_sn = sum(1 for h, r in hosts.items() if not r["is_anchor"])
    n_z = sum(1 for h, r in hosts.items() if not r["is_anchor"] and r.get("zCMB") is not None)
    doc = {
        "schema_version": "1.0",
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "source": [
            "Riess+2022 Table 2 (PantheonPlusSH0ES/DataRelease table2.tex)",
            "Pantheon+ zCMB (Scolnic+2022 / Carr+2022) for IS_CALIBRATOR=1",
            "NED Velocity + Planck 2018 CMB dipole as host-level cross-check",
            "Riess+2022 Table 6 μ_host (Cepheid-only published approximation)",
        ],
        "policy": [
            "Riess does not publish per-host H0=cz/d",
            "do not treat lstsq_results.txt fitted mu as measured",
            "do not retune sector_h0_seed.json rho",
            "individual nearby H0_i is peculiar-velocity noise",
        ],
        "c_kms": C_KMS,
        "sigma_vpec_kms": 250.0,
        "n_table2_hosts": len(counts),
        "n_table2_cepheids": int(sum(counts.values())),
        "n_sn_hosts": n_sn,
        "n_sn_hosts_with_z": n_z,
        "hosts": hosts,
    }
    REDSHIFT_OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {REDSHIFT_OUT}  SN hosts with z: {n_z}/{n_sn}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
