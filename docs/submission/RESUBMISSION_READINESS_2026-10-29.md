# Research resubmission edition: 29 October 2026

Manuscript: Design and Experimental Characterization of a PSK-Authenticated Hybrid Key Exchange on ESP32.

## Decision and scope

GO for author review and journal-specific preparation as an experimental implementation-characterization study. This is not a validated claim of improved cryptographic efficiency over a matched baseline. No acceptance probability can be inferred from the archive. A journal must accept this contribution type as well as the topic.

JSA-D-26-02162 and COMNET-D-26-07693 are closed rejections for insufficient novelty/scientific significance. Both decision letters described the topic as within scope. Older COMNET checklists and cover letters in this directory are historical preparation records and must not be reused for a new submission.

## Verified preparation

- All 100 historical UART/CSV records and generated mean, sample SD and Student-t confidence interval agree. No outlier is discarded.
- Separate primitive measurements have 50 key-generation and 49 shared-secret/decapsulation observations. `tools/analyze_primitive_trace.py` regenerates the reported means.
- Two archived hybrid-TLS observations average 1097.3045 ms. Four classical observations and a separate custom excerpt remain exploratory, with unmatched authentication and instrumentation.
- The active code uses ML-KEM-768; protocol lengths, transcript HMAC, HKDF, server-generated Session ID, no-AAD telemetry and all-zero X25519 rejection are described consistently.
- The ProVerif claims are limited to the supplied queries and uncompromised private-PSK assumptions.
- The 13.8 KB historical allocation estimate lacks its complete profiling trace. Stack configuration and campaign snapshots do not establish peak use.
- Endurance is reported as 14,157 parser-accepted CSV rows. 17,502 is a reported SYN count and 8,640 a nominal schedule calculation.
- Nine focused host tests pass; substituted KEM behavior is not native correctness or hardware validation. Corrected compiler artifacts are separately hashed and tied to their own source revision.

## Evidence required only for stronger claims

The archived hardware experiments exist. Additional records or a new, separately identified campaign are needed to establish corrected-firmware physical execution, a controlled efficiency improvement, transient heap/stack peaks, synchronized energy, independent expected-answer/interoperability validation, or empirical side-channel resistance. None is represented as completed by an editorial change. The public evaluation PSK and shared telemetry-direction key are disclosed limitations.

## Final journal gate

- Choose a journal after checking official scope and recent comparable implementation studies.
- Verify a zero-author-fee subscription route for the chosen article type. Do not select paid open access by default.
- Adapt formatting, cover letter and required submission items only after journal selection.
- Both authors approve the frozen revised paper and declarations before the next official submission.
- Use the exact commit/release printed in the packaged PDF and its SHA-256 manifest; do not substitute an older PDF or cover letter.

The package is a reproducible research edition, not an acceptance guarantee or a claim that missing historical evidence has been recreated.
