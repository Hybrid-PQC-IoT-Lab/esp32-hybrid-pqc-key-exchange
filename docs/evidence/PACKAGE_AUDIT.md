# Attached evidence-package audit

Audit date: 2026-10-30

## Inventory and provenance

The two supplied ZIP central directories contain 147 and 108 files respectively (255 entries total). Claim-bearing source, log, CSV, analysis, protocol, build and submission records were cross-checked against the working repository. Duplicate copies and illustrative images were inventoried but are not treated as independent measurement evidence.

The four-month master archive contains `dual_bench_8h.log` (24,567,508 bytes). Its SHA-256 is `958cf70de291297887b70c49e2e6cb8c90e44fc6f5b48036c4da7758867c4494`, matching the archive's SHA-256 manifest and the preserved working copy. The endurance CSV copies hash to `1b2be16ec261001911dffa59c6328f60e5b757d3ecf93a27331aebd2d1c5f59c`. Evidence Package 5 contains those processed CSV/report materials but not the master tcpdump text; the larger backup supplies the missing input.

Evidence Package 5 has conflicting version metadata. Its root README says release `v2.0-mlkem768-final` and short SHA `df9ce02`; `10_submission/COMMIT.txt` identifies commit `467bbe7a3c5a718d4eec7c882bc00f042487304d` and tag `v2.1-mlkem768-final`. The root README's claims of an external NIST KAT and full claim-to-raw-data traceability are not supported by the included files: the KAT-named log records self-consistency checks, and the package lacks the raw endurance capture.

## Reproduced observations and limits

The independent packet audit reports 203,408 TCP packet lines, 17,502 client-origin SYN events to the two service ports, 16,103 distinct source/destination socket tuples and 14,157 parser-accepted flow records (10,235 on port 8443; 3,922 on port 4443). The new parser output and historical CSV have different schemas, so the verified statement is matching total and per-port counts, not byte-for-byte CSV identity. The capture does not establish cryptographic handshake success, the TLS group on port 4443, device/firmware attribution, a failure denominator, watchdog state or uninterrupted uptime. See `endurance_packet_audit/audit_report.md`.

The `n=100` UART/CSV campaign remains a separate dataset: mean latency 616.75 ms, SD 244.13 ms, 95% t interval 568.31–665.19 ms, and mean elapsed CCOUNT 100.33 million cycles. The captured source build reports ESP-IDF v5.5 at 160 MHz; firmware version is a pre-freeze working build with a truncated ELF digest. The campaign contains 100 `task not found` watchdog API errors; these do not prove hardware watchdog resets. The later corrected harness has not been physically rerun in the supplied evidence.

The 13.8 KB dynamic-allocation profile, primitive timings, electrical notes, small TLS traces, endurance capture and `n=100` campaign are distinct acquisitions. Hybrid TLS has two recorded observations and classical TLS has four; neither is a matched baseline against the custom application protocol. Sparse campaign heap snapshots do not establish a peak. Fixed-window current calculations do not provide a per-handshake energy distribution or synchronized energy integral.

## Code and model checks

The active firmware and server reject an all-zero X25519 shared secret before secret combination. Existing host checks exercise the accumulator logic and server rejection; they are not a physical-binary integration test. AES-GCM is called with no AAD. Server Session IDs use the operating-system CSPRNG. The symbolic ProVerif results concern the encoded payload-confidentiality and one client-to-server injective correspondence queries under an uncompromised PSK; they do not prove post-session PSK-compromise PFS, reverse authentication, concrete nonce safety or implementation-level secrecy. Synthetic PCAPs remain illustrations, not captured protocol validation. Empirical TVLA/DPA and memory-dump resistance are not evidenced.

## Publication implication

The updated manuscript narrows claims to those supported by the supplied evidence and adds three close 2026 studies. A recent X25519/ML-KEM-768 MQTT protocol and ESP32 hybrid-TLS evaluations substantially narrow the novelty space. The current contribution is an implementation-specific PSK-authenticated HTTP/telemetry characterization; editorial wording cannot convert it into a new primitive or a controlled efficiency result. A Q2 outcome therefore cannot be guaranteed. Any later efficiency-comparison claim requires a matched, same-build, same-board experiment with raw attempts and failures retained; no such new measurement is asserted here.
