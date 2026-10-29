"""Recompute operation means from the archived, separate primitive acquisition."""
import json
import re
import statistics
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = root / 'data/raw_logs/energy_esp32_mlkem768_usb_proof.txt'
groups = {}
for name, micros, cycles in re.findall(r'BENCHMARK \[([^]]+)\]: (\d+) us, (\d+) cycles', source.read_text(errors='replace')):
    groups.setdefault(name, []).append((int(micros), int(cycles)))
if not groups:
    raise SystemExit('No primitive observations found')
print(json.dumps({'source': source.relative_to(root).as_posix(),
    'boundary': 'Separate acquisition; unequal operation counts; excludes server encapsulation. Not a complete-handshake decomposition.',
    'operations': {name: {'n': len(rows), 'mean_ms': statistics.mean(r[0] for r in rows) / 1000,
                          'mean_cycles': statistics.mean(r[1] for r in rows)}
                   for name, rows in groups.items()}}, indent=2))
