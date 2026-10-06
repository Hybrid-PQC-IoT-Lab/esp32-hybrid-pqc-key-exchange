# Physical work required before a stronger GO verdict

## First check existing evidence before repeating physical work

The archived 100-handshake campaign and 50-packet rotation proof already exist and have been verified. Obtain the original build/ELF/map/configuration or operator record first. The following procedure is required only when claiming physical validation of the later corrected firmware, reporting new results from it, or testing a behavior not established by existing logs. Historical measurements may be retained with clear attribution and explicit limits. See EXISTING_EVIDENCE_RECHECK.md.

## A. Corrected-firmware campaign and rotation (conditional)

1. Use one identified ESP32-D0WD-V3 board and ESP-IDF v5.5. Record the board model/revision, supply, Wi-Fi conditions and server OS/library versions. Keep credentials out of the public package.
2. Build from the exact candidate commit with a clean tree. Save `git rev-parse HEAD`, `git status --porcelain`, `idf.py --version`, the compiler version, full sdkconfig, build log, ELF, map, flashed binary and their SHA-256 digests. If a fix is needed, create a new commit and identify that build; do not silently reuse a tag.
3. Build the native ML-KEM server library, start `python3 server/server.py --host 0.0.0.0 --port 8443`, and save its full output. Confirm the native backend is available. Do not accept simulated cryptography.
4. Flash the identified firmware and capture the complete UART boot-to-completion log at 115200 baud. The boot must report ESP-IDF v5.5 and 160 MHz. The application runs 100 hybrid attempts automatically.
5. Retain every successful CSV record and every failed-attempt message. Valid IDs now identify attempted runs 1–100; gaps correspond to failures. Do not rerun only slow cases or discard outliers. Report successes and failures separately. No `task not found` watchdog-reset errors should occur; if a watchdog timeout or reset occurs, retain the trace and stop calling the corrected build validated.
6. Keep the emitted configured stack size and minimum-free-stack reading. This value is not a heap peak. Archive it with the exact IDF API/build context.
7. Let the telemetry loop produce 50 successful encrypted acknowledgments (about 250 seconds at the configured 5-second interval, plus connection time). Save UART and server logs showing the sequence, the rotation threshold and the next handshake. Check the actual crypto IV counters separately from JSON telemetry sequence numbers.
8. Parse the new observations into a **new** CSV. Do not overwrite the historical n=100 files. Recompute sample SD, mean CI, extrema and cycle statistics using the new experiment's actual successful-sample count; the existing analysis tool deliberately accepts only the archived 100-record dataset. Synchronize manuscript values only after validating the new acquisition.

**Deliverables:** exact build metadata + ELF/map/binary hashes + full UART/server logs + per-attempt CSV + analysis output + 50-packet rotation trace.

## B. Heap peak and memory comparison (required for measured-peak claims)

1. In a separately identified profiling build, enable ESP-IDF heap tracing or a documented local minimum-free-heap measurement that covers all live allocations inside a handshake, including temporary HTTP and cryptographic allocations.
2. Define the measurement window and memory capability mask. Record before/within/after values and distinguish whole-system Wi-Fi activity from allocations attributable to the handshake. Establish any tracing overhead separately.
3. Preserve the allocation trace, raw memory logs, peak-live-byte calculation, configured task stack, stack high-water mark, ELF/map and tool output. Treat decimal KB and binary KiB consistently.
4. Repeat the same measurement boundaries for custom hybrid, certificate-based TLS and, if claiming security-equivalent efficiency, TLS-PSK. Record library/configuration differences and the sample count rather than imposing the old 13.8/38.5/49.0 KB numbers.

The existing `peak_heap_bytes` CSV field is a sparse snapshot delta and must not be repurposed as a validated transient peak.

## C. Optional stronger energy claims

Use a calibrated power analyzer or suitable synchronized voltage/current acquisition across the whole handshake. Record sample rate, bandwidth, shunt value, supply rail, timestamps and calibration. Compute energy by integrating measured power over each actual handshake interval, retaining slow runs. Measure input and regulator-output rails separately if making regulator claims. A multimeter's apparent peak is not a transient upper bound.

## D. Recoverable evidence, without a physical rerun

Retrieve the original `dual_bench_final_complete.log` from the experiment owner's machine if it still exists. Hash it and rerun the parser against that file. The synthetic PCAPs cannot replace it. If it cannot be recovered, narrow the endurance claims to what the processed CSV and attributed historical report support; a replacement physical run is a new campaign with its own provenance.
