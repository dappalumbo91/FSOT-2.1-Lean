#!/usr/bin/env python3
"""Build a Kaggle-ready FSOT prediction / engine pack (dataset + notebook).

Does NOT auto-upload unless --push is passed (requires authenticated kaggle CLI).

  python scripts/build_kaggle_prediction_pack.py
  python scripts/build_kaggle_prediction_pack.py --push

Pack includes:
  - vendor/fsot_compute.py (seed engine, pin D1D38A)
  - prediction manifests + freeze + monitor report
  - slim contested / margin summary JSON
  - notebook that runs the same prereg + scalar checks as the monorepo spine
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "kaggle" / "fsot-prediction-monitor"
DATASET_DIR = OUT / "dataset"
KERNEL_DIR = OUT / "kernel"


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d")


def _copy(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_file():
        shutil.copy2(src, dst)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _slim_margin(src: Path, dst: Path, n: int = 30) -> None:
    if not src.is_file():
        return
    doc = json.loads(src.read_text(encoding="utf-8"))
    rows = doc.get("all_domains") or []
    green = [r for r in rows if r.get("green_gate_pass")]
    green.sort(
        key=lambda r: -(
            r.get("official_pooled_median_error_pct")
            or r.get("pooled_median_error_pct")
            or 0
        )
    )
    slim = {
        "generated_at": doc.get("generated_at") or datetime.now(timezone.utc).isoformat(),
        "benchmark_file_count": doc.get("benchmark_file_count"),
        "green_gate_pass_count": doc.get("green_gate_pass_count"),
        "green_gate_fail_count": doc.get("green_gate_fail_count"),
        "worst_green_top": green[:n],
        "note": "Slim export for Kaggle — full atlas remains on GitHub monorepo.",
    }
    dst.write_text(json.dumps(slim, indent=2), encoding="utf-8")


NOTEBOOK = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python", "pygments_lexer": "ipython3"},
    },
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# FSOT 2.1 — Prediction Monitor (Kaggle mirror)\n",
                "\n",
                "Public, zero-free-parameter seed engine (**pin D1D38A**) + preregistered prediction locks.\n",
                "\n",
                "This notebook mirrors the monorepo prediction spine:\n",
                "1. Load `fsot_compute.py` and validate seed constants\n",
                "2. Load prereg + freeze + monitor registry\n",
                "3. Report near-future survey watches\n",
                "4. Optional online GWOSC probe\n",
                "\n",
                "**Authority:** GitHub monorepo `FSOT-2.1-Lean` — this is a portable mirror, not a retune surface.\n",
            ],
        },
        {
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "outputs": [],
            "source": [
                "from pathlib import Path\n",
                "import json, hashlib, sys\n",
                "import yaml\n",
                "\n",
                "# Kaggle input path when dataset is attached; local fallback for offline smoke\n",
                "CANDIDATES = [\n",
                "    Path('/kaggle/input/fsot-prediction-monitor'),\n",
                "    Path('/kaggle/input/fsot-prediction-monitor/dataset'),\n",
                "    Path('.'),\n",
                "    Path('dataset'),\n",
                "]\n",
                "ROOT = next((p for p in CANDIDATES if (p / 'fsot_compute.py').is_file() or (p / 'vendor' / 'fsot_compute.py').is_file()), Path('.'))\n",
                "if (ROOT / 'vendor' / 'fsot_compute.py').is_file():\n",
                "    ENGINE = ROOT / 'vendor' / 'fsot_compute.py'\n",
                "    DATA = ROOT / 'data' if (ROOT / 'data').is_dir() else ROOT\n",
                "else:\n",
                "    ENGINE = ROOT / 'fsot_compute.py'\n",
                "    DATA = ROOT\n",
                "print('ROOT', ROOT)\n",
                "print('ENGINE', ENGINE, 'sha256', hashlib.sha256(ENGINE.read_bytes()).hexdigest()[:12].upper())\n",
            ],
        },
        {
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "outputs": [],
            "source": [
                "sys.path.insert(0, str(ENGINE.parent))\n",
                "import fsot_compute as fc\n",
                "\n",
                "sha = hashlib.sha256(ENGINE.read_bytes()).hexdigest().upper()\n",
                "pin_ok = sha.startswith('D1D38A')\n",
                "print('pin_prefix', sha[:6], 'pin_match', pin_ok)\n",
                "print('S_cosm', float(fc.S_COSM))\n",
                "print('S_quant', float(fc.S_QUANT))\n",
                "print('K', float(fc.K))\n",
                "print('N_eff sample (wave1 if available)')\n",
                "try:\n",
                "    rows = list(fc.wave1())\n",
                "    for r in rows[:8]:\n",
                "        print(' ', getattr(r, 'name', r), getattr(r, 'value', None), getattr(r, 'target', None))\n",
                "except Exception as e:\n",
                "    print('wave1 skip', e)\n",
                "assert pin_ok, 'Engine pin must start with D1D38A — refuse silent retune'\n",
            ],
        },
        {
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "outputs": [],
            "source": [
                "def load_yaml(name):\n",
                "    p = DATA / name\n",
                "    if not p.is_file():\n",
                "        p = DATA / 'data' / name if (DATA / 'data').is_dir() else p\n",
                "    return yaml.safe_load(p.read_text(encoding='utf-8')) if p.is_file() else {}\n",
                "\n",
                "def load_json(name):\n",
                "    for p in [DATA / name, DATA / 'data' / name]:\n",
                "        if p.is_file():\n",
                "            return json.loads(p.read_text(encoding='utf-8'))\n",
                "    return {}\n",
                "\n",
                "prereg = load_yaml('preregistered_predictions_manifest.yaml')\n",
                "registry = load_yaml('prediction_monitor_registry.yaml')\n",
                "freeze = load_json('toe_prereg_freeze.json')\n",
                "monitor = load_json('prediction_monitor_report.json')\n",
                "margin = load_json('margin_slim.json')\n",
                "\n",
                "preds = prereg.get('predictions') or []\n",
                "print(f\"PRED count: {len(preds)}\")\n",
                "print(f\"domains: {len({p.get('domain') for p in preds})}\")\n",
                "print(f\"future_survey tagged: {sum(1 for p in preds if p.get('future_survey'))}\")\n",
                "print(f\"T5 freeze: {freeze.get('freeze_id')} sha={str(freeze.get('bundle_sha256'))[:16]}…\")\n",
                "print(f\"monitor watches: {(monitor.get('summary') or {}).get('watch_count')}\")\n",
                "print(f\"green (slim): {margin.get('green_gate_pass_count')}/{margin.get('benchmark_file_count')}\")\n",
            ],
        },
        {
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "outputs": [],
            "source": [
                "import pandas as pd\n",
                "\n",
                "rows = []\n",
                "for w in (registry.get('watches') or []):\n",
                "    dd = w.get('data_drop') or {}\n",
                "    rows.append({\n",
                "        'id': w.get('id'),\n",
                "        'title': w.get('title'),\n",
                "        'sector': w.get('sector'),\n",
                "        'urgency': w.get('urgency'),\n",
                "        'fsot_lock': w.get('fsot_lock'),\n",
                "        'unit': w.get('unit'),\n",
                "        'window': dd.get('window'),\n",
                "        'facility': dd.get('facility'),\n",
                "        'pred_ids': ','.join(w.get('pred_ids') or []),\n",
                "    })\n",
                "df = pd.DataFrame(rows)\n",
                "display(df)\n",
                "\n",
                "print('\\nHigh-urgency near-term:')\n",
                "display(df[df.urgency == 'high'][['id', 'title', 'window', 'fsot_lock']])\n",
            ],
        },
        {
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "outputs": [],
            "source": [
                "# Optional: live GWOSC catalog size (requires internet on Kaggle)\n",
                "import urllib.request\n",
                "ONLINE = True  # set False for offline-only\n",
                "if ONLINE:\n",
                "    try:\n",
                "        url = 'https://www.gwosc.org/eventapi/json/GWTC/'\n",
                "        with urllib.request.urlopen(url, timeout=20) as resp:\n",
                "            data = json.loads(resp.read().decode())\n",
                "        events = data.get('events') or {}\n",
                "        n = len(events) if isinstance(events, dict) else data.get('numRows')\n",
                "        print('GWOSC GWTC event entries:', n)\n",
                "        print('FSOT PRED-048: compact-binary panel residual ceiling 0.5% (see monorepo green gate)')\n",
                "    except Exception as e:\n",
                "        print('online probe skipped:', e)\n",
                "else:\n",
                "    print('online disabled')\n",
            ],
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Kill criteria (do not retune)\n",
                "\n",
                "- If a survey posterior **excludes** a frozen lock (e.g. wa, N_eff, H0 bridge), record a kill in the monorepo falsification registry.\n",
                "- Never change `fsot_predicted` without a new `freeze_id`.\n",
                "- Full multiprover + 472-domain atlas: clone GitHub `dappalumbo91/FSOT-2.1-Lean`.\n",
            ],
        },
    ],
}


def build() -> Path:
    if OUT.exists():
        shutil.rmtree(OUT)
    DATASET_DIR.mkdir(parents=True)
    KERNEL_DIR.mkdir(parents=True)

    # Engine + prediction artifacts
    _copy(ROOT / "vendor" / "fsot_compute.py", DATASET_DIR / "fsot_compute.py")
    for name in [
        "preregistered_predictions_manifest.yaml",
        "prediction_monitor_registry.yaml",
        "toe_prereg_freeze.json",
        "prediction_monitor_report.json",
        "contested_observables_closure.json",
        "contested_future_observation_ledger.json",
        "h0_multi_tool_predictions.json",
        "sector_h0_seed.json",
        # domain atlas is large; include summary-only slim via extractor below
    ]:
        src = ROOT / "data" / name
        if src.is_file():
            _copy(src, DATASET_DIR / name)

    # Slim domain atlas: summary + multi-tool H0 preds + top residual holds (not full scalar dump)
    atlas_src = ROOT / "data" / "domain_prediction_atlas.json"
    if atlas_src.is_file():
        atlas = json.loads(atlas_src.read_text(encoding="utf-8"))
        preds = atlas.get("predictions") or []
        slim_preds = [p for p in preds if p.get("kind") == "multi_tool_h0"]
        residual = [p for p in preds if p.get("kind") == "residual_hold"]
        residual.sort(key=lambda p: -(p.get("fsot_predicted") or 0))
        slim_preds.extend(residual[:40])
        slim = {
            "generated_at": atlas.get("generated_at"),
            "summary": atlas.get("summary"),
            "note": "Slim Kaggle export — full atlas on GitHub data/domain_prediction_atlas.json",
            "predictions_preview": slim_preds,
            "bundle_sha256": atlas.get("bundle_sha256"),
        }
        (DATASET_DIR / "domain_prediction_atlas_slim.json").write_text(
            json.dumps(slim, indent=2), encoding="utf-8"
        )

    _slim_margin(ROOT / "data" / "benchmark_margin_audit.json", DATASET_DIR / "margin_slim.json")

    # Dataset metadata (user damianpalumbo from kaggle config)
    ds_meta = {
        "title": "FSOT Prediction Monitor",
        "id": "damianpalumbo/fsot-prediction-monitor",
        "licenses": [{"name": "CC0-1.0"}],
        "keywords": ["physics", "cosmology", "open science", "predictions"],
        "collaborators": [],
        "data": [],
    }
    _write(DATASET_DIR / "dataset-metadata.json", json.dumps(ds_meta, indent=2))
    _write(
        DATASET_DIR / "README.md",
        (
            "# FSOT Prediction Monitor (dataset)\n\n"
            "Seed engine `fsot_compute.py` (pin D1D38A) + preregistered predictions "
            "and near-future survey watches.\n\n"
            "Full system: https://github.com/dappalumbo91/FSOT-2.1-Lean\n"
        ),
    )

    # Kernel notebook + metadata
    nb_path = KERNEL_DIR / "fsot-prediction-monitor.ipynb"
    _write(nb_path, json.dumps(NOTEBOOK, indent=1))
    kernel_meta = {
        "id": "damianpalumbo/fsot-prediction-monitor",
        "title": "FSOT Prediction Monitor",
        "code_file": "fsot-prediction-monitor.ipynb",
        "language": "python",
        "kernel_type": "notebook",
        "is_private": False,
        "enable_gpu": False,
        "enable_tpu": False,
        "enable_internet": True,
        "dataset_sources": ["damianpalumbo/fsot-prediction-monitor"],
        "competition_sources": [],
        "kernel_sources": [],
        "model_sources": [],
    }
    _write(KERNEL_DIR / "kernel-metadata.json", json.dumps(kernel_meta, indent=2))

    # Local smoke: copy engine into kernel folder for offline run without kaggle input mount
    _copy(DATASET_DIR / "fsot_compute.py", KERNEL_DIR / "fsot_compute.py")
    for f in DATASET_DIR.glob("*"):
        if f.name not in {"dataset-metadata.json", "README.md"}:
            _copy(f, KERNEL_DIR / f.name)

    manifest = {
        "built_at": datetime.now(timezone.utc).isoformat(),
        "dataset_dir": str(DATASET_DIR.relative_to(ROOT)).replace("\\", "/"),
        "kernel_dir": str(KERNEL_DIR.relative_to(ROOT)).replace("\\", "/"),
        "files": sorted(p.name for p in DATASET_DIR.iterdir()),
        "push_commands": [
            "kaggle datasets create -p kaggle/fsot-prediction-monitor/dataset --dir-mode zip",
            "kaggle datasets version -p kaggle/fsot-prediction-monitor/dataset -m 'prediction monitor refresh' --dir-mode zip",
            "kaggle kernels push -p kaggle/fsot-prediction-monitor/kernel",
        ],
    }
    _write(OUT / "PACK_MANIFEST.json", json.dumps(manifest, indent=2))
    print(f"Built pack at {OUT}")
    print(f"  dataset files: {manifest['files']}")
    return OUT


def push() -> int:
    """Upload dataset then kernel via kaggle CLI."""
    # Prefer version if dataset exists, else create
    create = subprocess.run(
        [
            "kaggle",
            "datasets",
            "create",
            "-p",
            str(DATASET_DIR),
            "--dir-mode",
            "zip",
        ],
        capture_output=True,
        text=True,
    )
    print(create.stdout)
    print(create.stderr)
    if create.returncode != 0 and "already exists" in (create.stdout + create.stderr).lower():
        ver = subprocess.run(
            [
                "kaggle",
                "datasets",
                "version",
                "-p",
                str(DATASET_DIR),
                "-m",
                f"prediction monitor {_now()}",
                "--dir-mode",
                "zip",
            ],
            capture_output=True,
            text=True,
        )
        print(ver.stdout)
        print(ver.stderr)
        if ver.returncode != 0:
            return ver.returncode
    elif create.returncode != 0:
        # try version as fallback
        ver = subprocess.run(
            [
                "kaggle",
                "datasets",
                "version",
                "-p",
                str(DATASET_DIR),
                "-m",
                f"prediction monitor {_now()}",
                "--dir-mode",
                "zip",
            ],
            capture_output=True,
            text=True,
        )
        print(ver.stdout)
        print(ver.stderr)
        if ver.returncode != 0:
            return create.returncode

    ker = subprocess.run(
        ["kaggle", "kernels", "push", "-p", str(KERNEL_DIR)],
        capture_output=True,
        text=True,
    )
    print(ker.stdout)
    print(ker.stderr)
    return ker.returncode


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--push", action="store_true", help="Upload dataset + kernel via kaggle CLI")
    args = ap.parse_args()
    build()
    if args.push:
        print("Pushing to Kaggle…")
        return push()
    print("Dry pack only. Re-run with --push to upload (authenticated CLI).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
