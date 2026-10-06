# Evidence status and corrections

This note supersedes interpretations in preserved historical reports. Original logs,
CSV, PCAP and formal-model files remain unchanged. Packaging them with newer source
does not identify the binary used in the experiment.

| Claim | Supported evidence and limit |
|---|---|
| Historical timing |100 UART/CSV observations match; boot160MHz/IDF5.5. Full historical binary/source identity unavailable. |
| Corrected harness |Host checks and ESP-IDF5.5 compiler archive at db93361 exist. Archive and four artifact hashes verified; historical logs do not validate corrected hardware execution. |
| Rotation |Historical trace exists. Current code counts successful decrypted responses; three consecutive errors also end a session. |
| Endurance |14,157 accepted CSV rows:10,235 Hybrid-PQC and3,922 Classical-TLS labels. Later narrative identifies latter as hybridTLS; negotiation capture missing. |
| 17,502 |Reported TCP SYN count; original master tcpdump missing. Not verified completed handshakes. |
| 8,640 |Nominal36h dual-device15s schedule arithmetic, not observed completion count. |
| Stability |CSV cannot establish all-attempt success, zero watchdog events/loss, uninterrupted duration or heap stability. |
| Memory |32KiB configured stack; measured usage missing. Independent13.8KB report lacks full trace; historical section sizes lack matching ELF/map. |
| Power |Manual fixed-window estimates, not integrated traces.0.75J assumes150mA for1s; some handshakes exceed1s. |
| Model |Encoded payload secrecy/client-to-server injective correspondence under ideal crypto/private uncompromised PSK. SID/mode/concrete nonce/later compromise not modeled. |
| Correctness |KAT-labelled log is self-consistency, not external expected-answer validation/certification. |
| PCAP |Synthetic illustrations, not live validation. |

Original endurance report240MHz/classical-TLS/zero-failure/heap-stability descriptions
remain historical claims. TCP FIN/payload criteria do not prove cryptographic
authentication. Different acquisition campaigns and frame definitions are separate.

Use `python3 tools/summarize_endurance_csv.py` for accepted-row counts and
`python3 benchmarks/energy_calculation.py` for worksheet arithmetic. Original
endurance parser needs missing `dual_bench_final_complete.log`.

On6October2026,33 evidence files in original main and personal fork were identical.
A performed experiment without original records is unverified; this does not prove
the experiment never occurred. Both telemetry directions still share one key with
no AAD; reflection remains unresolved. Production security is not established.

The corrected compiler archive includes ELF, map, binary and sdkconfig.
CORRECTED_BUILD_PROVENANCE.json records their identity. The package builder checks
that its frozen firmware and server trees match that compiler source commit.
Source equality does not prove that this binary produced historical observations.
