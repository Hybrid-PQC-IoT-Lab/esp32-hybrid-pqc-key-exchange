# Journal-readiness audit

**Verdict: NO-GO for journal submission; GO for author review and the specified hardware rerun.**

Audit updated: 5 October 2026. This verdict concerns the corrected candidate,
not an assertion that it is a newly hardware-validated release. The exported
package's `BUILD_PROVENANCE.json` records the exact corrected commit.

## Working set verified

- At the first audit, tag `v2.1-mlkem768-final` identified commit `467bbe7a3c5a718d4eec7c882bc00f042487304d`. On 4 October it instead resolves to `670448651276740e0d58931f388ca32035cb6245`. Exact commit hashes, rather than that moved tag alone, are used for provenance.
- Uploaded `research_paper_9.pdf`, the repository PDF and the evidence ZIP's PDF have SHA-256 `3a95ae9c4feca696084fd67a78eee4cf13c287bd2dd8212e9b1381f5bb104b58`, matching the GitHub release asset digest.
- Uploaded Evidence Package 4 has SHA-256 `c9f2d65f04ee89d3cbc2feb5a3e3308967ed40dffc4b93f11a8fe1281b6ccfdb`, matching the release ZIP digest.
- The supplied TeX copies agree after newline normalization. Original measurement files are preserved in Git and checked against the original commit by the packaging tool.
- The latest primary repository is `Hybrid-PQC-IoT-Lab/esp32-hybrid-pqc-key-exchange`, at `670448651276740e0d58931f388ca32035cb6245`. Its later documentation, dependency and wire-format test changes have been reconciled into this candidate.
- The primary release downloaded on 4 October has PDF SHA-256 `794cc1f743971680f4a046e3a56bc76d11066a62a5e04d5e1eb0409bf064355a` and evidence ZIP SHA-256 `a84d636bbd1c92a6f3f627ec58e4cc9f705be2abf818a8e27206e3c036e87557`. Its TeX is identical to the latest repository TeX after newline normalization. Compared with uploaded Evidence Package 4, 103 files are byte-identical; only the manuscript source/PDF and three submission/provenance README/COMMIT files changed. No fresh measurements were introduced. Its COMMIT.txt names `b3af7e4b38a2a522581301e253aee7d7945541fa`, whereas the moved tag names `6704486`; the new package explicitly records one source commit.

## Corrections completed

| Item | Finding and correction |
|---|---|
| n=100 latency | 616.7478 ms mean; sample SD 244.1282405 ms; Student t 95% CI 568.3074607–665.1881393 ms; range 525.66–1989.39 ms. No outliers removed. |
| Cycle count | Mean 100.33034716M; sample SD 39.06089356M; CI 92.57981845–108.08087587M; range 85.756999–319.954713M. Labeled elapsed CCOUNT, not isolated CPU cost. |
| Success count | 100 numerical records match UART; campaign window has 100 successful HMAC checks and 100 derived keys, with no logged handshake retries/failures. The 100 watchdog API errors are separately disclosed. |
| Measurement boundaries | Latency sums two intervals; the cycle counter spans a wider region. Primitive means from a separate trace are not subtracted from the campaign mean. |
| Heap and stack | 13.8 KB retained as a separate reported profile, not an n=100 peak. Campaign snapshot delta is 22.24 B mean / 440 B maximum. Stack is 32 KiB configured; no supported 9.2 KB high-water result. Context/message arrays are stack objects. |
| Build metadata | ESP-IDF v5.5 and 160 MHz are in the boot log. Unarchived mbedTLS version/complete compiler command are not invented. |
| Watchdog | Removed unsubscribed-task reset calls; retained outer delays. Paper no longer claims a hardware-validated watchdog feed fix or constant-time proof. |
| Benchmark harness | Correct run IDs, float samples/sample SD, failed-attempt denominator, error propagation, and no local-only fallback counted as a successful network handshake. |
| Server fallback | Missing native ML-KEM library now fails the operation instead of returning random stand-in ciphertext/secret. |
| Protocol wording | Session ID comes from server `secrets.token_bytes(16)`. Server HMAC covers the 1,217-byte unsigned client body plus unsigned server response. Total handshake bodies are 2,417 bytes. Old nonce-bearing tests corrected. |
| Security | Actual three ProVerif queries stated; no post-PSK-compromise query or physical-side-channel proof claimed. Directional reflection remains explicit; selected buffer zeroization is only partial memory-exposure mitigation. |
| KAT/PCAP | Fixed-seed and randomized self-consistency terminology; synthetic Scapy PCAPs clearly labeled. Historical logs remain unchanged, including their obsolete labels. |
| Energy | 0.75 J is a 1.0 s × 150 mA × 5 V calculation, not a bound for a 1.98939 s sample. The worksheet's separate 142 mA TLS transient is disclosed. No invented power trace. |
| Author/version metadata | First/corresponding-author placeholders and separate declarations prepared. Exported Data Availability uses an exact source commit and candidate release, while preserving original measurement provenance. |

## Remaining submission blockers

1. **Physical validation of corrected firmware.** Host tests cannot establish ESP32 execution. Run the 100-attempt campaign and 50-packet rotation procedure in [HARDWARE_RERUN.md](HARDWARE_RERUN.md) from a clean, identified build. Keep every attempt and original log. Do not reuse the archived 616.75 ms as a new-build result.
2. **Authorship and declarations.** Replace the first/corresponding-author placeholders, confirm author order and contributions with all authors, and supply funding, conflicts, ethics applicability and author approval. No author identity or approval has been inferred.
3. **Evidence for a strong memory-efficiency conclusion.** The original 13.8 KB baseline/peak/recovery trace and ELF/map are incomplete. The candidate discloses this and makes a narrower reported-profile claim. To retain a measured-peak or matched TLS memory advantage as a principal contribution, complete the memory procedure below; editorial changes cannot supply this evidence.
4. **Target-journal intake check.** Journal of Systems Architecture is the contextual candidate. Its current author-guide page returned access errors during this audit, so journal-specific abstract length, review-anonymity, required files and formatting have not been certified. The existing IEEE-style layout was retained. Resolve these against the live official guide before upload.

## Limitations that do not justify invented reruns

- The original endurance master tcpdump file is absent. The processed 14,157-row CSV is preserved. Recover the raw capture if exact SYN totals, sitting boundaries and reset-free execution are to be independently revalidated; otherwise retain only clearly attributed processed/report-level observations. A new 19-hour experiment is not automatically required for the narrowed claims.
- A slow manual multimeter does not establish transient energy maxima. New synchronized power traces are needed only for stronger measured-energy or campaign-wide-bound claims. The candidate labels the existing values as calculations.
- Directional traffic keys, a direction label and expanded formal modeling are future protocol changes; they were not silently introduced into a benchmark revision.
- External ML-KEM expected-answer validation, multi-board variability and side-channel testing remain research limitations. The current self-consistency checks are not renamed as certification.

## Validation and assessment

The validation directory contains host-test/build records and, when available,
GitHub CI status for the exact source commit. The local native library passed
two fixed-seed round trips, a modified-ciphertext check and 100 randomized rounds.
Eight Python tests passed. Compiled benchmark host assertions passed for sample
SD, ordinal IDs, missing/failed handshakes, no-success campaigns and CPU conversion.
The PDF was rebuilt using bundled Tectonic and its layout inspected. The native editor compiler was unavailable; the terminal build succeeded. ESP-IDF v5.5 CI compilation also passed for the corrected firmware; exact final-commit CI records accompany the package. The unchanged ProVerif model/output
were inspected; ProVerif was not rerun locally. No ESP32 was flashed or measured.

**Domain:** embedded IoT systems and applied post-quantum protocol implementation.
**Contribution:** system integration and inspectable experimental artifacts; a new
cryptographic primitive or general security proof is not established.
**Audience:** embedded-systems/IoT-security researchers. A systems journal or
implementation-focused conference is a plausible format after the blockers close.

**Readiness estimate: 65/100**, an editorial judgment reflecting improved consistency
but incomplete build-to-measurement provenance, physical validation and authorship.
Acceptance probability cannot be responsibly quantified from these materials or
an unverified journal acceptance rate. For JSA, the main editorial risk is whether
the systems contribution and controlled baseline evidence are sufficient. Confidence
is high in the CSV reanalysis and identified source inconsistencies, and limited in
unarchived physical profiles. This is not a full novelty search or a blanket
verification of all 40 bibliography entries.

## Official sources checked

- [Original release](https://github.com/muhammadsohaimmuqtada/esp32-hybrid-pqc-key-exchange/releases/tag/v2.1-mlkem768-final).
- [ESP-IDF v5.5 watchdog documentation](https://docs.espressif.com/projects/esp-idf/en/v5.5/esp32/api-reference/system/wdts.html): reset calls require task subscription; yielding permits idle-task execution.
- [JSA author guide](https://www.sciencedirect.com/journal/journal-of-systems-architecture/publish/guide-for-authors): retrieval failed, journal-specific compliance remains unverified.
- [Elsevier AI policy](https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals): disclose substantive AI assistance and retain author responsibility.
- [Elsevier highlights guidance](https://www.elsevier.support/publishing/answer/how-do-i-include-highlights-with-my-manuscript): candidate highlights are supplied separately, subject to the journal's requirements.
