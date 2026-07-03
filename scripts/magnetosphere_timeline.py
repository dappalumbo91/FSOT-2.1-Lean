"""Magnetosphere timeline helpers — multi-resolution Kp alignment to hourly Dst."""

from __future__ import annotations

from datetime import datetime
from typing import Iterable


def parse_time_tag(tag: str) -> datetime:
    return datetime.fromisoformat(tag)


def build_kp_series(kp_records: Iterable[dict]) -> list[tuple[datetime, float]]:
    series: list[tuple[datetime, float]] = []
    for row in kp_records:
        tag = row.get("time_tag") or ""
        if not tag:
            continue
        series.append((parse_time_tag(tag), float(row.get("kp") or 0.0)))
    series.sort(key=lambda x: x[0])
    return series


def kp_slot_3h(dst_tag: str, kp_by_tag: dict[str, float]) -> float:
    if dst_tag in kp_by_tag:
        return kp_by_tag[dst_tag]
    try:
        hour = int(dst_tag[11:13])
    except ValueError:
        return 0.0
    day = dst_tag[:10]
    slot = (hour // 3) * 3
    return kp_by_tag.get(f"{day}T{slot:02d}:00:00", 0.0)


def kp_interpolated_1h(
    dst_tag: str,
    kp_by_tag: dict[str, float],
    kp_series: list[tuple[datetime, float]],
) -> float:
    if dst_tag in kp_by_tag:
        return kp_by_tag[dst_tag]
    target = parse_time_tag(dst_tag)
    for idx, (ts, kp) in enumerate(kp_series):
        if ts == target:
            return kp
        if ts > target and idx > 0:
            t0, k0 = kp_series[idx - 1]
            t1, k1 = ts, kp
            span = (t1 - t0).total_seconds()
            if span <= 0:
                return k0
            frac = (target - t0).total_seconds() / span
            return k0 + (k1 - k0) * frac
    return kp_slot_3h(dst_tag, kp_by_tag)


def kp_rolling_max(
    dst_tag: str,
    kp_series: list[tuple[datetime, float]],
    *,
    window_hours: int,
) -> float:
    target = parse_time_tag(dst_tag)
    vals: list[float] = []
    for ts, kp in kp_series:
        delta_h = (target - ts).total_seconds() / 3600.0
        if 0.0 <= delta_h <= float(window_hours):
            vals.append(kp)
    if not vals:
        return 0.0
    return max(vals)