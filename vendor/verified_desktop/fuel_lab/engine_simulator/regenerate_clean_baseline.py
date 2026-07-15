import csv
from pathlib import Path

INPUT_PATH = Path(__file__).parent / "data" / "vehicles.csv"
OUTPUT_PATH = Path(__file__).parent / "data" / "vehicles_clean.csv"

FIELDS = [
    "make",
    "model",
    "year",
    "cylinders",
    "displ",
    "fuelType",
    "city08",
    "highway08",
    "comb08",
    "barrels08",
    "co2",
    "co2TailpipeGpm",
    "co2TailpipeAGpm",
    "fuelCost08",
    "eng_dscr",
    "trany",
    "VClass",
]

if not INPUT_PATH.exists():
    raise FileNotFoundError(f"Raw baseline CSV not found at {INPUT_PATH}")

with INPUT_PATH.open(newline='', encoding='utf-8') as inf, OUTPUT_PATH.open('w', newline='', encoding='utf-8') as outf:
    reader = csv.DictReader(inf)
    writer = csv.DictWriter(outf, fieldnames=FIELDS)
    writer.writeheader()
    for row in reader:
        cleaned = {field: row.get(field, '') for field in FIELDS}
        writer.writerow(cleaned)

print(f"Regenerated cleaned baseline CSV at {OUTPUT_PATH} with fields: {', '.join(FIELDS)}")
