# SN Computer Science readiness review — 30 October 2026

## Decision

**Document and package: ready for author review. Journal submission: conditional, not guaranteed.** This version is prepared as an Original Research article for SN Computer Science. The journal's scope includes cryptography, computer and network security, computer and communication networks, computer architecture, and IoT. Scope fit is credible; it does not establish novelty or predict an editorial decision.

The revised paper describes a specific pre-provisioned-PSK, application-layer HTTP exchange and its encrypted telemetry lifecycle on ESP32. Its contribution is an inspectable implementation and bounded characterization. It does not claim a new cryptographic primitive, first ESP32 deployment, general superiority to TLS, post-compromise security, complete replay protection, or production security. Two previous in-scope editorial rejections cited insufficient novelty/scientific significance. The current framing addresses overclaiming, but the novelty threshold remains a material risk. No defensible acceptance percentage can be calculated.

## Verified and packaged

- The archived 100-row latency/cycle campaign was checked against its raw log and analysis; its statistics are synchronized in the manuscript: mean 616.75 ms, sample SD 244.13 ms, 95% CI 568.31–665.19 ms, observed range 525.66–1989.39 ms, and mean 100.33 million elapsed cycles.
- The campaign's logged completions do not establish the all-attempt denominator. The 13.8 KB heap estimate is presented separately as an incomplete historical profile, not as the campaign's peak.
- The manuscript and overview figure distinguish the application exchange from the independently acquired primitive, TLS, heap, endurance, and electrical observations. Synthetic packet illustrations are not represented as live captures.
- Author names, order, first/corresponding-author marker, affiliations, Lahore addresses, corresponding email and ORCID are present. The article has a structured abstract, keywords, declarations, source availability, separate supplementary resources, and editable LaTeX source.
- A clean two-pass package build resolved citations. The final source/PDF package was compiled and its manifest, raw-statistics check, and release assets were verified.
- Figure 1 is a vector schematic generated from editable TikZ, delivered as EPS and PDF. It explains the protocol and acquisition boundaries; it is not an image of the complete code.
- The release offers the subscription route. SN Computer Science is hybrid, and its publisher currently states that no APC applies to the subscription model; the choice is made after acceptance and should be rechecked in the portal.

## Limits that must remain explicit

1. Historical raw records are preserved, but the original measured binary's complete build identity is unavailable. The corrected source/ESP-IDF compiler archive does not prove that it produced the archived measurements. Do not attribute the old campaign to a later firmware commit.
2. The archived telemetry-rotation trace and 100-row campaign are evidence of their recorded historical runs, not a physical rerun of all subsequent harness corrections. A fresh board run is needed only if the manuscript is changed to claim performance or behavior of the corrected firmware.
3. The recovered endurance text supports packet/accepted-flow counts only. It does not establish 17,502 completed handshakes, a complete 36-hour run, zero failures, or an all-attempt success rate. The 8,640 value is schedule arithmetic, not observed completions.
4. Stack usage and static-memory claims lack a complete measured trace tied to the historical ELF/map. The 13.8 KB heap report lacks its full profiling trace. Manual current readings are not integrated high-rate energy measurements; precise per-handshake energy statistics are not claimed.
5. The archived KAT-labelled output is self-consistency evidence, not an independent expected-answer or interoperability test. PCAP files identified as synthetic are illustrations, not live protocol-validation captures.
6. The formal model supports only its encoded payload-confidentiality and client-to-server agreement claims under the stated ideal-cryptography and uncompromised-PSK assumptions. It does not verify post-session PSK compromise, independent directional traffic keys, or general replay/reflection resistance.
7. X25519 and ML-KEM timing and TLS observations came from separate acquisition/configuration boundaries. They do not establish a matched end-to-end efficiency advantage.

These limits are already bounded in the manuscript and supplementary material. A new physical campaign is **not a blanket prerequisite** if authors retain those limits. If stronger corrected-firmware, endurance, memory, energy, KAT/interoperability, or matched-TLS claims are desired, the relevant experiment must be run and archived before adding those claims. The hardware rerun protocol identifies the exact captures and metadata required.

## Before uploading

- Both authors should approve this exact PDF, author order, contributions, declarations, and supplementary files. The corresponding author should confirm the Promaker Institute role is fully disclosed as a potential non-financial interest.
- Confirm the submission portal's article type and subscription route. Upload the manuscript, editable source, separate EPS figure, Online Resource 1, and Online Resource 2 using the correct item types.
- Review the merged portal PDF and the actual uploaded supplements before final approval. No journal submission was made when this package was frozen.

## Frozen identities

- Historical measurement-source commit: `467bbe7a3c5a718d4eec7c882bc00f042487304d`.
- Software/evidence snapshot cited by the paper: `c811b71846bd8ce8d298a42473f3ea305a039e76`.
- Package build commit: `21c9b5ace702c7f4e290656b566b62e45d536313`.
- Current candidate release: `v2.7.1-journal-submission-kit`.
