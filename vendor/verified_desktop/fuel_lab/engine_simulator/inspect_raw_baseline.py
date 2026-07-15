import csv
from pathlib import Path

p = Path(__file__).parent / 'data' / 'vehicles.csv'
fields = ['make', 'model', 'year', 'displ', 'fuelType', 'comb08', 'city08', 'highway08', 'co2', 'co2TailpipeGpm', 'co2TailpipeAGpm']
count = 0
with p.open(newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if 'Crossfire' in row.get('model', ''):
            print({k: row.get(k, '') for k in fields})
            count += 1
            if count >= 40:
                break
print('crossfire rows', count)
