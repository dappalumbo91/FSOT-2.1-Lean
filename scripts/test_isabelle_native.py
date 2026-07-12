#!/usr/bin/env python3
"""One-off: verify TranscendentalBoundsNative.thy builds in Isabelle."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import isabelle_install_roots  # noqa: E402

THY_DIR = ROOT / "verification" / "isabelle"


def _resolve_isabelle_home() -> Path:
    roots = isabelle_install_roots()
    if not roots:
        raise SystemExit("Isabelle not found. Set ISABELLE_HOME.")
    return roots[0]


def cygpath(win_path: Path) -> str:
    resolved = win_path.resolve()
    drive = resolved.drive.rstrip(":").lower()
    tail = resolved.as_posix().split(":", 1)[-1]
    return f"/cygdrive/{drive}{tail}"


def main() -> int:
    isa_home = _resolve_isabelle_home()
    bash = isa_home / "contrib" / "cygwin" / "bin" / "bash.exe"
    if not bash.exists():
        raise SystemExit(f"Isabelle cygwin bash not found under {isa_home}")

    root = THY_DIR / "ROOT"
    original = root.read_text(encoding="utf-8") if root.exists() else ""
    root.write_text(
        "session FSOT_NativeTest = HOL +\n"
        "  sessions\n"
        '    "HOL-Decision_Procs"\n'
        "  theories\n"
        "    TranscendentalBoundsNative\n",
        encoding="utf-8",
    )
    cmd = (
        f"cd '{cygpath(isa_home)}' && "
        f"bin/isabelle build -D '{cygpath(THY_DIR)}' -v FSOT_NativeTest"
    )
    try:
        r = subprocess.run(
            [str(bash), "--login", "-c", cmd],
            capture_output=True,
            timeout=900,
        )
        out = (r.stdout or b"") + (r.stderr or b"")
        print(out[-8000:].decode("utf-8", errors="replace"))
        return r.returncode
    finally:
        root.write_text(original, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())