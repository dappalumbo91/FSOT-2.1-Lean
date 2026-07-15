"""Magnetosphere timeline helpers — multi-resolution Kp alignment to hourly Dst."""

from __future__ import annotations

import bisect
from datetime import datetime, timedelta
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
    *,
    kp_times: list[datetime] | None = None,
) -> float:
    if dst_tag in kp_by_tag:
        return kp_by_tag[dst_tag]
    if not kp_series:
        return kp_slot_3h(dst_tag, kp_by_tag)
    target = parse_time_tag(dst_tag)
    times = kp_times or [ts for ts, _ in kp_series]
    idx = bisect.bisect_right(times, target)
    if idx < len(kp_series) and kp_series[idx][0] == target:
        return kp_series[idx][1]
    if idx > 0 and idx < len(kp_series):
        t0, k0 = kp_series[idx - 1]
        t1, k1 = kp_series[idx]
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
    kp_times: list[datetime] | None = None,
) -> float:
    if not kp_series:
        return 0.0
    target = parse_time_tag(dst_tag)
    times = kp_times or [ts for ts, _ in kp_series]
    end = bisect.bisect_right(times, target)
    if end == 0:
        return 0.0
    start = bisect.bisect_left(times, target - timedelta(hours=window_hours))
    window = kp_series[start:end]
    if not window:
        return 0.0
    return max(kp for _, kp in window)


def dst_storm_predicted(
    dst_nt: float,
    *,
    dst_thr: float,
    adj_dst: float,
    union_classifier: bool = True,
) -> bool:
    """Storm when Dst crosses operational G-scale or FSOT-adjusted threshold."""
    if union_classifier:
        return dst_nt <= dst_thr or dst_nt <= adj_dst
    return dst_nt <= adj_dst


def kp_storm_predicted(
    kp: float,
    *,
    kp_thr: float,
    adj_kp: float,
    union_classifier: bool = True,
) -> bool:
    """Storm when Kp crosses NOAA G-scale or FSOT fusion-adjusted threshold."""
    if union_classifier:
        return kp >= kp_thr or kp >= adj_kp
    return kp >= adj_kp


def hp_storm_predicted(
    hp_nt: float,
    *,
    hp_thr: float,
    adj_hp: float | None = None,
    union_classifier: bool = False,
) -> bool:
    """GOES Hp (nT) storm classifier — NOAA G-scale uses Hp≥80 nT.

    Unlike Dst union mode, FSOT adj must not widen below the NOAA label band
    (otherwise Hp 75–80 nT false positives vs measured_storm at 80 nT).
    """
    if union_classifier and adj_hp is not None:
        return float(hp_nt) >= hp_thr or float(hp_nt) >= max(hp_thr, adj_hp)
    return float(hp_nt) >= hp_thr


def coupled_dst_kp_storm_predicted(
    dst_nt: float,
    kp: float,
    *,
    dst_thr: float,
    adj_dst: float,
    kp_thr: float,
    adj_kp: float,
    union_classifier: bool = True,
) -> bool:
    """Coupled Dst×Kp storm leg — union mode fixes Dst margin-band false negatives."""
    return dst_storm_predicted(
        dst_nt, dst_thr=dst_thr, adj_dst=adj_dst, union_classifier=union_classifier
    ) or kp_storm_predicted(
        kp, kp_thr=kp_thr, adj_kp=adj_kp, union_classifier=union_classifier
    )


def southward_bz_predicted(
    bz_gsm_nt: float,
    *,
    bz_thr: float,
    adj_bz: float,
    union_classifier: bool = True,
) -> bool:
    """Southward Bz when crossing operational or FSOT electron-adjusted threshold."""
    if union_classifier:
        return bz_gsm_nt < bz_thr or bz_gsm_nt < adj_bz
    return bz_gsm_nt < adj_bz