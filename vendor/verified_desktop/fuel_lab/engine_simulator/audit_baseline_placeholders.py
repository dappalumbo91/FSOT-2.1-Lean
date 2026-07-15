import csv
from pathlib import Path

path = Path(__file__).parent / "data" / "vehicles_clean.csv"
counts = {
    "co2_neg": 0,
    "mpg_neg": 0,
    "co2_blank": 0,
    "mpg_blank": 0,
}
rows = []

with path.open(newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader, 1):
        co2 = row.get('co2', '').strip()
        mpg = ''
        for key in ['comb08', 'city08', 'highway08', 'comb08u', 'city08u', 'highway08u']:
            val = row.get(key, '').strip()
            if val:
                mpg = val
                break
        bad_co2 = co2 != '' and co2.startswith('-')
        bad_mpg = mpg != '' and mpg.startswith('-')
        if bad_co2 or bad_mpg or co2 == '' or mpg == '':
            rows.append({
                'line': i,
                'year': row.get('year'),
                'make': row.get('make'),
                'model': row.get('model'),
                'displ': row.get('displ'),
                'fueltype': row.get('fuelType'),
                'comb08': row.get('comb08'),
                'city08': row.get('city08'),
                'highway08': row.get('highway08'),
                'co2': co2,
            })
            if bad_co2:
                counts['co2_neg'] += 1
            if bad_mpg:
                counts['mpg_neg'] += 1
            if co2 == '':
                counts['co2_blank'] += 1
            if mpg == '':
                counts['mpg_blank'] += 1

print(counts)
cross = [row for row in rows if 'Crossfire' in row['model']]
print('crossfire placeholder rows', len(cross))
for row in cross[:20]:
    print(row)
