#!/usr/bin/env python3
"""GPU-assisted OME-Zarr sampling for Zebrahub developmental imaging (RTX 5070 path)."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "zebrahub_datasets.yaml"


def _gpu_device_name() -> str:
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
            text=True,
            timeout=10,
        )
        return out.strip().splitlines()[0] if out.strip() else "unknown"
    except Exception:
        return "none"


def _torch_info() -> dict[str, Any]:
    try:
        import torch  # noqa: WPS433

        info: dict[str, Any] = {
            "torch_version": torch.__version__,
            "cuda_available": torch.cuda.is_available(),
            "arch_list": list(torch.cuda.get_arch_list()) if torch.cuda.is_available() else [],
        }
        if torch.cuda.is_available():
            info["device_name"] = torch.cuda.get_device_name(0)
            x = torch.zeros(1, device="cuda")
            _ = x + 1
            info["cuda_usable"] = True
        else:
            info["cuda_usable"] = False
        return info
    except Exception as exc:
        return {"cuda_usable": False, "error": str(exc)[:120]}


def _torch_cuda_usable() -> bool:
    return bool(_torch_info().get("cuda_usable"))


def _ome_zarr_scales(url: str) -> list[tuple[str, list[int]]]:
    """Return multiscale paths + shapes, coarsest first."""
    import fsspec  # noqa: WPS433

    mapper = fsspec.get_mapper(url)
    attrs = json.loads(mapper.get(".zattrs"))
    datasets = (attrs.get("multiscales") or [{}])[0].get("datasets") or []
    if not datasets:
        raise ValueError("no multiscales datasets in .zattrs")
    scales: list[tuple[str, list[int]]] = []
    for entry in reversed(datasets):
        path = str(entry["path"])
        zarray = json.loads(mapper.get(f"{path}/.zarray"))
        scales.append((path, list(zarray.get("shape") or [])))
    return scales


def _coarse_ome_zarr_path(url: str) -> tuple[str, list[int]]:
    scales = _ome_zarr_scales(url)
    return scales[0]


def _best_tile_for_scale(
    arr: Any,
    shape: list[int],
    *,
    t_index: int = 0,
    z_index: int = 0,
) -> tuple[Any, int]:
    """Pick center XY tile with highest mean across representative z-slices."""
    import numpy as np  # noqa: WPS433

    ndim = len(shape)
    if ndim < 2:
        raise ValueError("unexpected_shape")

    t_idx = min(t_index, shape[0] - 1) if ndim >= 5 else 0
    c_idx = 0
    z_idx = min(z_index, shape[2] - 1) if ndim >= 5 else 0
    y_dim = shape[-2]
    x_dim = shape[-1]
    y0 = max(0, y_dim // 2 - 16)
    y1 = min(y_dim, y_dim // 2 + 16)
    x0 = max(0, x_dim // 2 - 16)
    x1 = min(x_dim, x_dim // 2 + 16)

    def _read_tile(z_slot: int) -> np.ndarray:
        if ndim == 5:
            return np.asarray(arr[t_idx, c_idx, z_slot, y0:y1, x0:x1], dtype=np.float32)
        if ndim == 4:
            return np.asarray(arr[t_idx, z_slot, y0:y1, x0:x1], dtype=np.float32)
        return np.asarray(arr[y0:y1, x0:x1], dtype=np.float32)

    z_slots = [z_idx]
    if ndim >= 4:
        z_dim = shape[2] if ndim == 5 else shape[1]
        step = max(1, z_dim // 8)
        z_slots = list({0, z_idx, z_dim // 2, max(0, z_dim - 1)})
        z_slots.extend(range(0, z_dim, step))
    tile = _read_tile(z_slots[0])
    for z_slot in z_slots[1:]:
        z_cap = (shape[2] if ndim == 5 else shape[1]) - 1
        candidate = _read_tile(min(z_slot, z_cap))
        if candidate.mean() > tile.mean():
            tile = candidate
            z_idx = min(z_slot, z_cap)
    return tile, z_idx


def _sample_zarr_tile(url: str, *, t_index: int = 0, z_index: int = 0) -> dict[str, Any]:
    """Sample a small XY tile from OME-Zarr; prefer coarsest scale with signal."""
    import numpy as np  # noqa: WPS433

    try:
        import fsspec  # noqa: WPS433
        import zarr  # noqa: WPS433
    except ImportError as exc:
        return {"error": f"missing_dep: {exc}", "mean_intensity": None}

    try:
        store = fsspec.get_mapper(url)
        root = zarr.open(store, mode="r")
        best_tile: np.ndarray | None = None
        best_meta: dict[str, Any] = {}
        best_mean = -1.0

        for scale_path, shape in _ome_zarr_scales(url):
            if len(shape) < 2:
                continue
            tile, z_idx = _best_tile_for_scale(
                root[scale_path], shape, t_index=t_index, z_index=z_index
            )
            mean_val = float(tile.mean()) if tile.size else 0.0
            if mean_val > best_mean:
                best_mean = mean_val
                best_tile = tile
                best_meta = {
                    "zarr_scale_path": scale_path,
                    "z_index_used": z_idx,
                    "volume_shape": shape,
                }
            if mean_val > 1e-4:
                break

        if best_tile is None or not best_tile.size:
            return {"error": "no_signal", "mean_intensity": None}

        mean_val = float(best_tile.mean())
        std_val = float(best_tile.std())
        max_val = float(best_tile.max())

        result: dict[str, Any] = {
            "mean_intensity": round(mean_val, 6),
            "std_intensity": round(std_val, 6),
            "max_intensity": round(max_val, 6),
            "tile_shape": list(best_tile.shape),
            "backend": "numpy_cpu",
            **best_meta,
        }

        if _torch_cuda_usable():
            import torch  # noqa: WPS433

            gpu_t = torch.from_numpy(best_tile).cuda()
            result["mean_intensity"] = round(float(gpu_t.mean().item()), 6)
            result["std_intensity"] = round(float(gpu_t.std().item()), 6)
            result["max_intensity"] = round(float(gpu_t.max().item()), 6)
            result["backend"] = "torch_cuda"

        return result
    except Exception as exc:
        return {"error": f"sample_failed: {exc}"[:160], "mean_intensity": None}


def sample_imaging_datasets() -> dict[str, Any]:
    import yaml  # noqa: WPS433

    from tier95_zebrahub_development_lib import cache_root  # noqa: WPS433

    spec = yaml.safe_load(DATA.read_text(encoding="utf-8")) if DATA.exists() else {}
    torch_meta = _torch_info()
    gpu_name = _gpu_device_name()
    cuda_ok = bool(torch_meta.get("cuda_usable"))
    cap = 2 if not os.environ.get("FSOT_TIER95_DEEP") else len(spec.get("imaging_zarr") or [])

    samples: list[dict] = []
    for entry in (spec.get("imaging_zarr") or [])[:cap]:
        ds_id = str(entry.get("id") or "")
        url = str(entry.get("url") or "")
        if not url:
            continue
        row = _sample_zarr_tile(url)
        samples.append(
            {
                "dataset_id": ds_id,
                "zarr_url": url,
                "gpu_device": gpu_name,
                "cuda_usable": cuda_ok,
                **row,
            }
        )

    return {
        "source": "zebrahub_ome_zarr_gpu_sample",
        "gpu_device": gpu_name,
        "cuda_usable": cuda_ok,
        "torch": torch_meta,
        "cuda_note": (
            "RTX 5070 (sm_120) requires torch>=2.11+cu128; "
            "install: pip install torch --index-url https://download.pytorch.org/whl/cu128"
        ),
        "sample_count": len(samples),
        "external_cache": str(cache_root()),
        "samples": samples,
    }


if __name__ == "__main__":
    print(json.dumps(sample_imaging_datasets(), indent=2))