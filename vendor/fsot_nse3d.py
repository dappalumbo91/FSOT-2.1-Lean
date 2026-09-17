#!/usr/bin/env python3
"""3D incompressible NSE on T^3 — spectral, seed-locked viscosity.

This is the 3D object. Not 2D enstrophy. Not a 1D Riccati cartoon.
Not Clay smoothness on R^3 (finite grid, finite time, one initial datum).
"""
from __future__ import annotations

import math
from typing import Any

import numpy as np

try:
    from fsot_compute import POOF, derived_D_eff
    from fsot_dynamics import viscosity_eff
except ImportError:  # pragma: no cover
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from fsot_compute import POOF, derived_D_eff
    from fsot_dynamics import viscosity_eff


def _wavenumbers(n: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    k = np.fft.fftfreq(n) * n
    kx, ky, kz = np.meshgrid(k, k, k, indexing="ij")
    k2 = kx * kx + ky * ky + kz * kz
    k2_safe = k2.copy()
    k2_safe[0, 0, 0] = 1.0
    return kx, ky, kz, k2_safe


def _project(
    uh: np.ndarray,
    vh: np.ndarray,
    wh: np.ndarray,
    kx: np.ndarray,
    ky: np.ndarray,
    kz: np.ndarray,
    k2_safe: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    div = kx * uh + ky * vh + kz * wh
    uh = uh - kx * div / k2_safe
    vh = vh - ky * div / k2_safe
    wh = wh - kz * div / k2_safe
    uh[0, 0, 0] = 0.0
    vh[0, 0, 0] = 0.0
    wh[0, 0, 0] = 0.0
    return uh, vh, wh


def _dealias(uh: np.ndarray, n: int) -> np.ndarray:
    kcut = n / 3.0
    k = np.fft.fftfreq(n) * n
    kx, ky, kz = np.meshgrid(k, k, k, indexing="ij")
    mask = (np.abs(kx) < kcut) & (np.abs(ky) < kcut) & (np.abs(kz) < kcut)
    return uh * mask


def _taylor_green_ic(n: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """3D Taylor–Green vortex on T^3. Divergence-free. Stretching is 3D (not Beltrami)."""
    x = np.linspace(0.0, 2.0 * math.pi, n, endpoint=False)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    u = np.sin(X) * np.cos(Y) * np.cos(Z)
    v = -np.cos(X) * np.sin(Y) * np.cos(Z)
    w = np.zeros_like(u)
    return u, v, w


def _vorticity(
    uh: np.ndarray,
    vh: np.ndarray,
    wh: np.ndarray,
    kx: np.ndarray,
    ky: np.ndarray,
    kz: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    ox = np.fft.ifftn(1j * ky * wh - 1j * kz * vh).real
    oy = np.fft.ifftn(1j * kz * uh - 1j * kx * wh).real
    oz = np.fft.ifftn(1j * kx * vh - 1j * ky * uh).real
    return ox, oy, oz


def _advect(
    u: np.ndarray,
    v: np.ndarray,
    w: np.ndarray,
    uh: np.ndarray,
    vh: np.ndarray,
    wh: np.ndarray,
    kx: np.ndarray,
    ky: np.ndarray,
    kz: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    ux = np.fft.ifftn(1j * kx * uh).real
    uy = np.fft.ifftn(1j * ky * uh).real
    uz = np.fft.ifftn(1j * kz * uh).real
    vx = np.fft.ifftn(1j * kx * vh).real
    vy = np.fft.ifftn(1j * ky * vh).real
    vz = np.fft.ifftn(1j * kz * vh).real
    wx = np.fft.ifftn(1j * kx * wh).real
    wy = np.fft.ifftn(1j * ky * wh).real
    wz = np.fft.ifftn(1j * kz * wh).real
    nu = -(u * ux + v * uy + w * uz)
    nv = -(u * vx + v * vy + w * vz)
    nw = -(u * wx + v * wy + w * wz)
    return np.fft.fftn(nu), np.fft.fftn(nv), np.fft.fftn(nw)


def nse3d_run(
    n: int = 16,
    n_steps: int = 240,
    mu: float | None = None,
    dt: float | None = None,
    return_histories: bool = False,
) -> dict[str, Any]:
    """3D incompressible NSE on T^3, ABC initial data, seed-locked μ.

    Tracks max |ω|, BKM proxy ∫ max|ω| dt, and 3D stretching production
    ∫ ω_i S_ij ω_j (identically 0 in 2D). Not Clay. Not 2D.
    """
    if mu is None:
        mu = viscosity_eff(float(derived_D_eff("Fluid_Dynamics")))
    mu = float(mu)
    if dt is None:
        dt = 0.4 / n
    u, v, w = _taylor_green_ic(n)
    uh, vh, wh = np.fft.fftn(u), np.fft.fftn(v), np.fft.fftn(w)
    kx, ky, kz, k2 = _wavenumbers(n)
    uh, vh, wh = _project(uh, vh, wh, kx, ky, kz, k2)
    decay = np.exp(-mu * k2 * dt)

    max_om = []
    production = []
    energy = []
    bkm = 0.0
    blow = False
    for _ in range(int(n_steps)):
        u = np.fft.ifftn(uh).real
        v = np.fft.ifftn(vh).real
        w = np.fft.ifftn(wh).real
        ox, oy, oz = _vorticity(uh, vh, wh, kx, ky, kz)
        omag = np.sqrt(ox * ox + oy * oy + oz * oz)
        om_inf = float(omag.max())
        if (not math.isfinite(om_inf)) or om_inf > 1.0e6:
            blow = True
            break
        max_om.append(om_inf)
        bkm += om_inf * dt
        ux = np.fft.ifftn(1j * kx * uh).real
        uy = np.fft.ifftn(1j * ky * uh).real
        uz = np.fft.ifftn(1j * kz * uh).real
        vx = np.fft.ifftn(1j * kx * vh).real
        vy = np.fft.ifftn(1j * ky * vh).real
        vz = np.fft.ifftn(1j * kz * vh).real
        wx = np.fft.ifftn(1j * kx * wh).real
        wy = np.fft.ifftn(1j * ky * wh).real
        wz = np.fft.ifftn(1j * kz * wh).real
        sxx, syy, szz = ux, vy, wz
        sxy = 0.5 * (uy + vx)
        sxz = 0.5 * (uz + wx)
        syz = 0.5 * (vz + wy)
        prod = float(
            np.mean(
                ox * (sxx * ox + sxy * oy + sxz * oz)
                + oy * (sxy * ox + syy * oy + syz * oz)
                + oz * (sxz * ox + syz * oy + szz * oz)
            )
        )
        production.append(prod)
        energy.append(float(0.5 * np.mean(u * u + v * v + w * w)))

        nuh, nvh, nwh = _advect(u, v, w, uh, vh, wh, kx, ky, kz)
        nuh, nvh, nwh = _dealias(nuh, n), _dealias(nvh, n), _dealias(nwh, n)
        nuh, nvh, nwh = _project(nuh, nvh, nwh, kx, ky, kz, k2)
        uh = (uh + dt * nuh) * decay
        vh = (vh + dt * nvh) * decay
        wh = (wh + dt * nwh) * decay
        uh, vh, wh = _project(uh, vh, wh, kx, ky, kz, k2)

    finite = (not blow) and len(max_om) == int(n_steps)
    stretching_3d = bool(production) and max(abs(p) for p in production) > 1e-8
    out: dict[str, Any] = {
        "n": n,
        "n_steps": int(n_steps),
        "dt": dt,
        "t_end": dt * len(max_om),
        "mu": mu,
        "fluid_D": float(derived_D_eff("Fluid_Dynamics")),
        "finite_on_run": finite,
        "blow": blow,
        "max_omega_start": max_om[0] if max_om else None,
        "max_omega_end": max_om[-1] if max_om else None,
        "max_omega_peak": max(max_om) if max_om else None,
        "bkm_proxy": bkm,
        "energy_start": energy[0] if energy else None,
        "energy_end": energy[-1] if energy else None,
        "stretching_production_peak": max(production) if production else None,
        "stretching_is_3d": stretching_3d,
        "spatial_dim": 3,
        "initial": "TaylorGreen3D",
        "clay_claimed": False,
        "poof": float(POOF),
    }
    if return_histories:
        out["history"] = {
            "max_omega": max_om,
            "energy": energy,
            "stretching_production": production,
        }
    return out


def nse3d_measured_compare() -> dict[str, Any]:
    """3D viscous NSE on T^3 is the object. 3D Euler (μ=0) is the wrong orifice.

    Clay is viscous 3D NSE, not Euler. 16^3 Euler energy is not conserved, so
    it is not a theorem that Euler blows. 2D is not used as a stand-in.
    Public compare: viscous Taylor–Green DNS decays at this Re (Brachet).
    """
    visc = nse3d_run(mu=None)
    euler = nse3d_run(mu=0.0)
    nse_damps = (
        visc["energy_end"] is not None
        and visc["energy_start"] is not None
        and visc["energy_end"] < 0.25 * visc["energy_start"]
        and visc["max_omega_end"] is not None
        and visc["max_omega_start"] is not None
        and visc["max_omega_end"] < visc["max_omega_start"]
    )
    e0 = euler["energy_start"] or 0.0
    e1 = euler["energy_end"] or 0.0
    euler_energy_drift_pct = (
        abs(e1 - e0) / max(abs(e0), 1e-30) * 100.0 if e0 else None
    )
    ok = (
        visc["spatial_dim"] == 3
        and visc["stretching_is_3d"]
        and visc["finite_on_run"]
        and nse_damps
        and not visc["clay_claimed"]
    )
    return {
        "nse3d": visc,
        "euler3d_wrong_orifice": {
            "reason": "Clay is viscous NSE. mu=0 is inviscid stuffing. 16^3 Euler is under-resolved.",
            "finite_on_run": euler["finite_on_run"],
            "blow": euler["blow"],
            "max_omega_end": euler["max_omega_end"],
            "energy_start": euler["energy_start"],
            "energy_end": euler["energy_end"],
            "energy_drift_pct": euler_energy_drift_pct,
            "not_a_blowup_theorem": True,
            "spatial_dim": 3,
        },
        "agrees_3d_viscous_tg_dns_decay": bool(visc["finite_on_run"] and nse_damps),
        "stretching_is_3d": visc["stretching_is_3d"],
        "ok": ok,
        "clay_claimed": False,
    }
