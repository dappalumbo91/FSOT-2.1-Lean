"""NOAA/WDC Kyoto Dst hourly ASCII parser (dstYYYY.txt / Q-LOOK_YYYY.txt)."""

from __future__ import annotations

import re
import ssl
import urllib.request

NGDC_DST_BASE = "https://www.ngdc.noaa.gov/stp/space-weather/geomagnetic-data/INDICES/DST/"

HEADER = re.compile(r"^DST(?P<yy>\d{2})(?P<mm>\d{2})[Q*P](?P<dd>\d{2})")
VALS = re.compile(r"-?\d+")


def year_from_yy(yy: int) -> int:
    return (1900 + yy) if yy >= 57 else (2000 + yy)


def parse_dst_text(text: str) -> list[dict]:
    rows: list[dict] = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("DST"):
            continue
        m = HEADER.match(line)
        if not m:
            continue
        year = year_from_yy(int(m.group("yy")))
        month = int(m.group("mm"))
        day = int(m.group("dd"))
        vals = [int(x) for x in VALS.findall(line[m.end() :])]
        if len(vals) < 24:
            continue
        for hour, dst in enumerate(vals[:24]):
            if dst in (999, 9999):
                continue
            rows.append(
                {
                    "time_tag": f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:00:00",
                    "dst": dst,
                }
            )
    return rows


def fetch_dst_year(year: int) -> list[dict]:
    if 2009 <= year <= 2012:
        filename = f"Q-LOOK_{year}.txt"
    else:
        filename = f"dst{year}.txt"
    url = NGDC_DST_BASE + filename
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    text = urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": "FSOT-2.1-Lean/kyoto-dst"}),
        timeout=120,
        context=ctx,
    ).read().decode("utf-8", errors="replace")
    rows = parse_dst_text(text)
    if not rows:
        raise ValueError(f"No Dst rows parsed for {year} from {url}")
    return rows