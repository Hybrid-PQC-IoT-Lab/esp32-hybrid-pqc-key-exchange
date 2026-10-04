# Scoped correction record

Base: `467bbe7a3c5a718d4eec7c882bc00f042487304d` (`v2.1-mlkem768-final`).

1. Recomputed n=100 results from matching CSV/UART fields with sample SD and Student t CI; centralized manuscript values in a generated TeX file.
2. Distinguished separate heap profiles, configured stack allocation, sparse campaign heap sampling and missing peak/high-water traces.
3. Corrected ESP-IDF to observed v5.5; withheld unarchived mbedTLS/build metadata.
4. Narrowed watchdog claims; removed reset calls from an unsubscribed task, retaining existing delays.
5. Fixed run IDs erased by result initialization, integer-truncated latency SD, implicit retries, hard-coded zero failure rate and ignored handshake failures. All attempts remain in the denominator.
6. Prevented server generation of random substitute ML-KEM outputs when the native library is unavailable.
7. Corrected Session ID RNG, 32-bit counter wording, self-consistency terminology, synthetic-PCAP provenance, actual ProVerif queries and side-channel/memory scope.
8. Corrected 2,417-byte handshake size and separated fixed-window energy calculations from campaign claims; withdrew unsupported same-campaign baseline rows and the misattributed RISC-V comparison row.
9. Prepared first/corresponding-author placeholders, exact-commit packaging, declarations, checklist and hardware rerun instructions.

Raw logs, CSV observations, synthetic PCAPs, formal model and historical solver
output are preserved. The old release/tag is not moved or overwritten. Corrections
do not constitute new hardware measurements or a security redesign.
