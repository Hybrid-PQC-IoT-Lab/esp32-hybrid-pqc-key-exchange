# Existing practical evidence recheck — 5 October 2026

## Confirmed completed work

The corresponding author reports that Sohaim completed and pushed the requested practical tests, and cross-checked the references. The visible GitHub evidence supports the existence of the archived hardware campaign and telemetry rotation demonstration:

- hybrid_handshake_100_runs.csv: 100 observations, preserved with its raw UART and server logs.
- telemetry_50_packets_key_rotation_proof.log: successful packet sequence 49 acknowledgment, rotation threshold, and a subsequent successful authenticated handshake.
- Actual boot metadata records ESP-IDF v5.5 and 160 MHz.

Remote branches/releases were rechecked on all three known repositories. The current upstream main is 670448651276740e0d58931f388ca32035cb6245; the corresponding-author fork is at 1bd76b11ba0904b0abf0a893b0fb391a857e3be1. These three evidence files have exactly the same Git blob hashes as the evidence already audited. No additional branch or new measurement file was found in those repository listings.

## Meaning of build identification

Build identification means knowing which software was running when a measurement was made. It does not mean that the laboratory experiment is missing. The archived boot identifies a 30 September build with a historical version string and a truncated ELF digest. Those observations cannot establish hardware execution of the later 5 October audit corrections to watchdog calls and benchmark failure accounting.

The existing observations remain usable as historical measurements, with their documented scope and limitations. An upload need not be blocked merely because every later documentation or harness correction has not been remeasured. Before final upload, the manuscript and artifact descriptions must clearly distinguish the measured historical implementation from later unmeasured corrections.

First seek the original build/ELF/map/configuration or operator record if stronger exact-build provenance is needed. Require a new corrected-build campaign only if the final paper claims that the corrected firmware was physically validated, uses new measurements from it, or makes a behavior claim not supported by existing traces. A protocol redesign or stronger measured-peak/energy claim separately requires evidence for that change.

## References and author files

Reference cross-checking by Sohaim is recorded as author-reported completed work. Independent DOI metadata retrieval and source checks remain documented in REFERENCE_AUDIT.md; a failed retrieval is not evidence of a false reference. Final editorial review of citation placement/claim scope remains part of manuscript approval, not a demand to repeat all reference work.

Sohaim's biography is being supplied. The remaining intake items and updated PDF compilation are tracked separately. No additional hardware experiment or new result has been invented.

## Inspectable evidence links

- https://github.com/muhammadsohaimmuqtada/esp32-hybrid-pqc-key-exchange/blob/670448651276740e0d58931f388ca32035cb6245/docs/evidence/hybrid_handshake_100_runs_raw.log
- https://github.com/muhammadsohaimmuqtada/esp32-hybrid-pqc-key-exchange/blob/670448651276740e0d58931f388ca32035cb6245/docs/evidence/telemetry_50_packets_key_rotation_proof.log
