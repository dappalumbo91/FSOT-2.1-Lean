# Reality OS sibling repository

The **standalone Reality OS** lives in a separate project so it can become a real operating system without carrying the full multiprover atlas.

| | |
|--|--|
| **GitHub** | https://github.com/dappalumbo91/FSOT-Reality-OS |
| **Sibling path (local)** | `C:\Users\damia\Desktop\FSOT-Reality-OS` |
| **Role** | Host kernel CLI + Linux OS build lab |
| **This monorepo** | Formula authority, residual atlas, multiprover, research leaves |

Upstream pin and `vendor/fsot_compute.py` remain authoritative here.  
When the pin or residual factors change, sync into the Reality OS repo per its `docs/UPSTREAM_FSOT.md`.

Reality OS inside this tree (`scripts/run_fsot_reality_os.py`) remains the **monorepo-integrated** entry; the sibling repo is for **independent reproduction and OS engineering**.
