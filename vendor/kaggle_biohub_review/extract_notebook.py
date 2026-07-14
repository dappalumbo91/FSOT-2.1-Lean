#!/usr/bin/env python3
import base64
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "extracted"
OUT.mkdir(exist_ok=True)

nb = json.loads((ROOT / "fsot-biohub-v47-fastsubmit.ipynb").read_text(encoding="utf-8"))

for cell in nb["cells"]:
    src = "".join(cell.get("source", []))
    m = re.search(r"# Write (.+?) to the working dir.*?\n_B64 = \"([^\"]+)\"", src, re.S)
    if not m:
        continue
    fname = m.group(1).strip()
    data = base64.b64decode(m.group(2))
    path = OUT / fname
    path.write_bytes(data)
    print(f"wrote {fname} ({len(data)} bytes)")
    if fname.endswith(".zip"):
        with zipfile.ZipFile(path, "r") as zf:
            zf.extractall(OUT / fname.replace(".zip", ""))

src = "".join(nb["cells"][11].get("source", []))
(OUT / "kaggle_main_runner.py").write_text(src, encoding="utf-8")
print(f"wrote kaggle_main_runner.py ({len(src)} chars)")