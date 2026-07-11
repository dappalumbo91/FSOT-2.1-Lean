#!/usr/bin/env python3
"""One-off: verify TranscendentalBoundsNative.thy builds in Isabelle."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THY_DIR = ROOT / "verification" / "isabelle"
ISA_HOME = Path(r"C:\Users\damia\Desktop\Isabelle2025-2")
BASH = ISA_HOME / "contrib" / "cygwin" / "bin" / "bash.exe"


def cygpath(win_path: Path) -> str:
    resolved = win_path.resolve()
    drive = resolved.drive.rstrip(":").lower()
    tail = resolved.as_posix().split(":", 1)[-1]
    return f"/cygdrive/{drive}{tail}"


def main() -> int:
    root = THY_DIR / "ROOT"
    backup = THY_DIR / "ROOT.bak_native_test"
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
        f"cd '{cygpath(ISA_HOME)}' && "
        f"bin/isabelle build -D '{cygpath(THY_DIR)}' -v FSOT_NativeTest"
    )
    try:
        r = subprocess.run(
            [str(BASH), "--login", "-c", cmd],
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