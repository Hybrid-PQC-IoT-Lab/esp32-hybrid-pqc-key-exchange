# Computer Networks software article candidate

Date: 5 October 2026. The authors selected SJR Q1 as an acceptable journal ranking.
Article type: Open-Source Software Article. Publication route: subscription.
No Computer Networks submission has been completed for this candidate.

## Scope

The main manuscript focuses on the software architecture, interfaces, installation,
reuse and historically supported results. Extended mathematical discussion and
historical comparisons are retained in Supplementary Material S1. The main article
does not claim new primitive design, first ESP32 feasibility or production security.
The official guide calls software articles micro-articles but does not state a
separate numerical page/word cap in the inspected article-type section. Concision
is an editorial choice here, not a claimed journal-specific page limit.

## Evidence

- The historical 100-record UART/CSV consistency check passes. All observations
  remain; mean 616.75 ms, sample SD 244.13 ms, t95 CI 568.31–665.19 ms,
  mean elapsed CCOUNT 100.33 million. Independent 13.8 KB allocation remains
  separate; a campaign transient peak is not established.
- Two current Windows host tests pass for framing/HMAC and missing-native-backend
  behavior, covering both server entry points. Their KEM output is substituted.
- Full Windows discovery runs eight tests and has one error because its native
  shared library is a Linux binary. No current native KEM test success is claimed.
  Ubuntu has Python but no identified gcc/make/ProVerif on PATH in this session.
- Original self-consistency and ProVerif logs remain historical and qualified.
- Corrected-firmware hardware execution, exact historical ELF/source mapping,
  direction-separated traffic-key validation and matched TLS-PSK measurements
  remain unestablished. Follow HARDWARE_RERUN.md for claims needing new evidence.

## Review gate

GO for author review of a bounded software article. Before official submission:
both authors must approve this adapted version; publication of its candidate
archive and upload to Computer Networks must be authorized; confirm journal
declarations and final legal terms at the final submission step. Both authors'
biographies are supplied for review. Sohaim's separate photo was identified and
approved for journal use by the corresponding author on 5 October 2026.

The public evaluation PSK is not a production credential. Directional telemetry
reflection/replay remains a real limitation, not a resolved security property.
The previous JSA rejection for insufficient novelty is disclosed in the cover
letter. The software category does not guarantee acceptance.

## Sources checked

https://www.sciencedirect.com/journal/computer-networks/publish/guide-for-authors
https://submit.elsevier.com/COMNET
https://www.scimagojr.com/journalsearch.php?q=26811&tip=sid&clean=0

SCImago reports SJR 2025 1.144, Q1 in Computer Networks and Communications.
The Elsevier transfer offer lists subscription publication without publishing
charge. Paid open access, MethodsX and Data in Brief are excluded from this plan.
Ranking databases are distinct; this is not a claim of current JCR Q1.
