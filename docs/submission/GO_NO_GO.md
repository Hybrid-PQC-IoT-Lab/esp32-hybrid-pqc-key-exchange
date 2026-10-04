# Journal-readiness decision — 5 October 2026

**NO-GO for upload; GO for completing the submission preparation.**

The paper has value as an applied embedded-security research prototype with real archived observations. The contribution is implementation and evaluation rather than a new primitive or a general protocol-security proof. Its practical basis supports a journal submission after evidence and author-intake items close; it does not by itself establish high-impact novelty or acceptance.

## What is complete

- Historical n=100 values are synchronized through benchmark macros: 616.75 ms mean, 244.13 ms sample SD, 568.31–665.19 ms 95% CI, 525.66–1989.39 ms range and 100.33M elapsed cycles.
- 13.8 KB is a separately reported historical heap allocation, not a campaign peak.
- Earlier audit corrected metadata/watchdog/RNG/KAT/PCAP wording and narrowed unsupported security claims. Host/native tests and ESP-IDF v5.5 CI for db93361 passed in the earlier audit; those unchanged firmware tests were not unnecessarily repeated for author-document changes.
- First/corresponding author metadata, postal address, seven keywords, <=250-word abstract, roles, funding and disclosed institutional relationship are prepared.
- Live JISA guide, indexing page, metrics and publishing-choice page have been checked. JISA is the primary target; JSA is a backup.

## Real remaining blockers and risks

1. Corrected firmware has no identified new physical campaign in the supplied working set. The user's fork is at 1bd76b11ba0904b0abf0a893b0fb391a857e3be1, dated 30 September, and predates corrected audit commit db93361. Linking that fork does not establish a later rerun. Recover existing identified logs or follow HARDWARE_RERUN.md.
2. Final source/PDF/evidence must be frozen from one identified revision after validation. Published rc1 remains the earlier archive, not this updated author version. No old release/tag was overwritten.
3. Final author approval, Sohaim biography/photo and full affiliation address, permissions, declaration-tool output and finalized AI disclosure remain intake items.
4. The 40-reference bibliography still needs a full metadata-and-claim check. RFC 10024 and RFC 9954 were verified as real current RFCs during this pass; this does not certify the other references or novelty coverage.
5. Shared telemetry keys across directions and acknowledged reflection risk may concern security reviewers. Do not claim complete replay resistance or production security. Further redesign would change the evaluated protocol and require fresh validation.
6. TLS comparison uses different security/configuration boundaries; sparse heap and manual power evidence cannot support strong matched-efficiency conclusions. Retain qualified wording or acquire the specific stronger evidence.

**Editorial readiness estimate: 65/100.** Author/intake preparation has improved, but unresolved physical provenance and technical contribution risks still dominate. This score is a judgment, not a calibrated acceptance probability. No numerical acceptance probability is supported. Confidence is high in raw-CSV statistics and document consistency; lower in absent historical peak-memory/endurance evidence.

## Versions

- Original measurement-source freeze: 467bbe7a3c5a718d4eec7c882bc00f042487304d.
- Corrected archived candidate: db93361b46043ea50a2080d3b095de9baa9f756a.
- Archived release: https://github.com/Hybrid-PQC-IoT-Lab/esp32-hybrid-pqc-key-exchange/releases/tag/v2.2.0-journal-audit-rc1.
- Author/source changes in this kit are a subsequent working revision. Data Availability now labels rc1 as an archived candidate rather than claiming this revised manuscript is its frozen asset.
- Current editor source remains output/ESP32_PQC_Journal_Audit_v2.2.0_rc1/source/docs/research_paper.tex.

Compiler result is recorded separately in COMPILE_STATUS.md. No journal submission has been made.
