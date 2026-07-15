import json
from pathlib import Path
path = Path('results/refined_grounded_hemp.json')
obj = json.loads(path.read_text())
best = max(obj['records'], key=lambda r: r['fsot_score'])
print(best['fuel_profile_id'])
print(best['fsot_score'])
print(best['renewable_rank'], best['fuel_cost_per_kwh'], best['thermal_efficiency'], best['co_g_per_h'], best['nox_g_per_h'])
