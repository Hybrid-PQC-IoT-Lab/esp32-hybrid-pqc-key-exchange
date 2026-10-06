# Evidence index and provenance

Manuscript: **A Secure Hybrid Post-Quantum Cryptographic Key Exchange for ESP32 IoT Devices**.

Primary repository: https://github.com/Hybrid-PQC-IoT-Lab/esp32-hybrid-pqc-key-exchange

Original archived source commit
`467bbe7a3c5a718d4eec7c882bc00f042487304d`.
The historical tag was later moved to `670448651276740e0d58931f388ca32035cb6245`; the corrected branch includes those later documentation/test changes.
The corrected package's `BUILD_PROVENANCE.json` identifies its exact source commit.
Packaging existing measurements from a new commit does not make them executions
of that commit.

| Artifact | Supported interpretation |
|---|---|
| `hybrid_handshake_100_runs_raw.log` | ESP-IDF v5.5, 160 MHz, 100 logged handshakes and 100 watchdog-reset API errors. Boot version identifies a pre-freeze working build, not the exact final source. |
| `hybrid_handshake_100_runs.csv` | Numeric observations match UART rows. Run numbers 1–100 represent acquisition order; original raw IDs are all zero. |
| `campaign_reanalysis.json` | Generated sample statistics, source hashes and measurement boundaries. |
| `hybrid_handshake_100_runs_server.log` | Preserved server-side context, separate from the UART timeline. |
| `telemetry_50_packets_key_rotation_proof.log` | Archived telemetry and rotation sequence. No new firmware run is implied. |
| `hybrid_pqc_fixed.pv` and `proverif_verification_output.txt` | Two secret-payload queries and one client-to-server injective correspondence under a private PSK. No later PSK disclosure or concrete GCM modeling. |
| `mlkem768_kat_verification.log` | Historical self-consistency output. Its KAT/IND-CCA2 wording is not external-vector validation or a timing proof. Raw output is preserved. |
| `memory_footprint_analysis.md` | Separately reported 13.8 KB profile, 32 KiB configured stack and explicit trace limitations. |
| `power_energy_calculations.csv` | Preserved manual current worksheet and fixed-duration calculations; not integrated energy measurements. |
| `endurance_summary.csv` | 14,157 processed accepted sessions. The master tcpdump source used by the parser is not supplied. |
| `endurance_test_report.md` | Historical endurance summary; raw capture, all attempts and four sitting boundaries cannot all be reconstructed from the accepted-row CSV. |
| `../../data/sanitized_pcaps/` | Synthetic Scapy illustrations only. |

The formerly linked `energy_bench_2026-09-04.md` and
`/home/kali/dual_bench_final_complete.log` are absent from the working set. They
are not represented as downloadable evidence.

Handshake bodies: ClientHello 1,249 bytes; ServerHello 1,168 bytes; total 2,417
bytes before HTTP/TCP/IP framing. Session IDs come from the server OS CSPRNG.
