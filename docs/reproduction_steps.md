# Reproduction guide

## 1. Recompute the archived n=100 statistics

```bash
python3 tools/analyze_submission.py --check
```

This checks all 100 numerical CSV rows against UART, checks HMAC/key-derivation
counts and verifies the generated manuscript values. It uses sample SD and a
two-sided Student t interval with 99 degrees of freedom. No outliers are removed.

## 2. Native cryptographic self-consistency

```bash
make -C firmware/components/mlkem768
python3 -m pip install -r server/requirements.txt
python3 -m unittest discover -s tests
python3 tools/test_mlkem768_kat.py
```

The legacy filename is retained. This suite checks fixed-seed round trips,
modified-ciphertext behavior and 100 randomized exchanges. It does not compare
published authoritative expected-answer vectors or certify NIST compliance.

## 3. Formal model

```bash
proverif docs/evidence/hybrid_pqc_fixed.pv
```

The archived transcript reports these queries true:

```text
not attacker(secret_client_data[])
not attacker(secret_server_data[])
inj-event(client_key_derived(k)) ==> inj-event(server_key_derived(k))
```

No post-PSK-compromise, reverse authentication or concrete GCM query is supplied.

## 4. Hardware build and rerun

Use ESP-IDF v5.5 to match the recorded campaign. The original full sdkconfig,
toolchain invocation, complete ELF hash and flashed binary were not archived.
The checked-in defaults request 160 MHz, and `pqc_task` has 32,768 stack bytes.

Put local `WIFI_SSID`, `WIFI_PASS` and `SERVER_HOST` definitions in the ignored
`firmware/main/wifi_config.local.h`. Build the native server library first.

```bash
python3 server/server.py --host 0.0.0.0 --port 8443
# In an ESP-IDF terminal:
cd firmware
idf.py set-target esp32
idf.py build
idf.py -p YOUR_SERIAL_PORT flash monitor
```

The application invokes a 100-attempt hybrid campaign directly in `main.c`.
The separate `BENCHMARK_ITERATIONS` macro is not the campaign count.
Follow [HARDWARE_RERUN.md](submission/HARDWARE_RERUN.md) to retain failures,
exact build provenance, stack data and telemetry rotation evidence.

## 5. Endurance limitations

`tools/analyze_endurance_log.py` expects the original master tcpdump log, not the
processed CSV. That raw input is not included, so end-to-end regeneration is
unavailable. Preserve the existing CSV and historical report; do not run a parser
on synthetic PCAPs and call the output a new physical campaign.

Accepted CSV rows can be regenerated separately with `python3 tools/summarize_endurance_csv.py`; this does not reconstruct missing attempts. Electrical worksheet arithmetic is regenerated with `python3 benchmarks/energy_calculation.py`. Consult `docs/evidence/EVIDENCE_STATUS.md`.

## 6. Package one frozen commit

Use `tools/build_submission_package.py` after committing source corrections.
It reads tracked files from Git's object database, writes the exact source SHA
into the exported manuscript identity file, and creates a SHA-256 manifest.
The PDF is a derived build artifact. Historical measurement files remain unchanged.
