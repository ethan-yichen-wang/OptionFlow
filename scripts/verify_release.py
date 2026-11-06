"""Read-only public file and aggregate-result check; no fitting or target reads."""
from pathlib import Path
import csv
from decimal import Decimal
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / 'PUBLIC_MANIFEST.json').read_text(encoding='utf-8'))
failures = []
for relative, expected in manifest['files'].items():
    path = ROOT / relative
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        failures.append(relative)
def read(name):
    with (ROOT / 'reports/tables' / name).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))
primary = read('T5_primary_readable.csv')
core = read('T3_primary_readable.csv')
assert len(primary) == 8 and len(core) == 4
assert all(Decimal(r['Delta_MSE_ci95_lower']) < 0 < Decimal(r['Delta_MSE_ci95_upper']) for r in primary)
assert all(Decimal(r['p_Holm']) == 1 for r in core)
assert all(Decimal(r['Delta_MSE_bp2']) == Decimal(r['Delta_MSE'])*100000000 for r in primary)
assert all(Decimal(r['R2_OS_percent']) == Decimal(r['R2_OS'])*100 for r in primary)
print(json.dumps({'status': 'failed' if failures else 'passed', 'public_files_checked': len(manifest['files']),
                  'core_inference_terms': len(core), 'primary_forecast_comparisons': len(primary),
                  'empirical_models_refitted': 0, 'target_rows_read': 0, 'failures': failures}, indent=2))
raise SystemExit(bool(failures))
