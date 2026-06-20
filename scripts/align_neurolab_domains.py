#!/usr/bin/env python3
"""Align NeuroLab 35-domain table in fsot_compute.py to Lean ledger params."""

from __future__ import annotations

import argparse
import importlib.util
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
ALIGNMENT_PATH = ROOT / "data" / "neurolab_ledger_alignment.yaml"
SYNC_SCRIPT = ROOT / "scripts" / "sync_lab_compute_mirrors.py"

sys.path.insert(0, str(ROOT / "scripts"))
from domain_scalar_oracle import DOMAINS, raw_S  # noqa: E402


def load_alignment() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required: pip install PyYAML")
    return yaml.safe_load(ALIGNMENT_PATH.read_text(encoding="utf-8"))


def format_delta_psi(val: float) -> str:
    s = f"{val:g}"
    if "." in s:
        return f'mpf("{s}")'
    return f"mpf({s})"


def patch_domain_line(line: str, cfg: dict) -> str:
    """Rewrite a DomainConfig(...) line preserving the C interpretation constant."""
    m = re.match(
        r'^(\s*)DomainConfig\("([^"]+)",\s*(\d+),\s*(\d+),\s*mpf(?:\("([^"]+)"\)|\(([^)]+)\)),\s*'
        r'mpf(?:\("([^"]+)"\)|\(([^)]+)\)),\s*(True|False),\s*(.+)\),?\s*$',
        line,
    )
    if not m:
        raise ValueError(f"Cannot parse DomainConfig line: {line.strip()}")

    indent, name, _d, _h, _dp1, _dp2, _dt1, _dt2, _obs, c_expr = m.groups()
    d_eff = cfg["D_eff"]
    hits = cfg["hits"]
    delta_psi = format_delta_psi(float(cfg["delta_psi"]))
    observed = "True" if cfg["observed"] else "False"
    return (
        f'{indent}DomainConfig("{name}",{d_eff:>3d},  {hits}, {delta_psi},   mpf(1), '
        f"{observed},  {c_expr}),"
    )


def apply_alignment(compute_path: Path, overrides: dict, dry_run: bool) -> list[str]:
    lines = compute_path.read_text(encoding="utf-8").splitlines(keepends=True)
    changed: list[str] = []
    out: list[str] = []

    for line in lines:
        m = re.search(r'DomainConfig\("([^"]+)"', line)
        if m and m.group(1) in overrides:
            name = m.group(1)
            new_line = patch_domain_line(line.rstrip("\n"), overrides[name]) + "\n"
            if new_line != line:
                changed.append(name)
            out.append(new_line)
        else:
            out.append(line)

    if changed and not dry_run:
        backup = compute_path.with_suffix(compute_path.suffix + ".pre_ledger_align")
        shutil.copy2(compute_path, backup)
        compute_path.write_text("".join(out), encoding="utf-8")
    return changed


def verify_bridge(overrides: dict, compute_path: Path) -> list[str]:
    spec = importlib.util.spec_from_file_location("aligned_compute", compute_path)
    if spec is None or spec.loader is None:
        return ["cannot load patched compute module"]
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)

    issues: list[str] = []
    for nb_name, cfg in overrides.items():
        lean = cfg.get("lean_domain")
        if not lean or lean not in DOMAINS:
            continue
        lean_val = raw_S(DOMAINS[lean])
        nb_val = float(mod.domain_scalar(nb_name))
        nb_raw = nb_val / float(mod.K)  # domain_scalar returns K·raw_S
        if (lean_val > 0) != (nb_raw > 0):
            issues.append(
                f"{nb_name} sign mismatch vs {lean}: lean={lean_val:.4f} nb_raw={nb_raw:.4f}"
            )
        rel = abs(nb_raw - lean_val) / max(abs(lean_val), 1e-9)
        if rel > 0.02:
            issues.append(f"{nb_name} raw_S drift vs {lean}: {rel:.2%}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Align NeuroLab domains to Lean ledger")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-sync", action="store_true")
    args = parser.parse_args()

    payload = load_alignment()
    authority = Path(payload["authority_path"])
    overrides = payload.get("overrides", {})

    if not authority.exists():
        raise SystemExit(f"Authority missing: {authority}")

    changed = apply_alignment(authority, overrides, args.dry_run)
    action = "Would update" if args.dry_run else "Updated"
    print(f"{action} {len(changed)} domain(s) in {authority}")
    for name in changed:
        lean = overrides[name].get("lean_domain", "?")
        print(f"  {name} → ledger:{lean}")

    if args.dry_run:
        return 0

    issues = verify_bridge(overrides, authority)
    if issues:
        print("Alignment verification issues:")
        for item in issues:
            print(f"  - {item}")
        return 1

    if not args.skip_sync and SYNC_SCRIPT.exists():
        subprocess.run([sys.executable, str(SYNC_SCRIPT)], check=True)

    stamp = datetime.now(timezone.utc).isoformat()
    print(f"Ledger alignment complete at {stamp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())