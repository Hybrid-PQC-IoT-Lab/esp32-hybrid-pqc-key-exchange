# Packet-capture audit

This analysis reports packet-level observations from the supplied tcpdump text. It does not establish a cryptographic handshake, a TLS version/group, physical device identity, or an all-attempt success rate.

## Provenance and reproduced counts

- Input: `dual_bench_8h.log` (24,567,508 bytes), SHA-256 `958cf70de291297887b70c49e2e6cb8c90e44fc6f5b48036c4da7758867c4494`.
- Parsed TCP packet lines: 203,408.
- Client-origin SYN events to the two service ports: 17,502; distinct source/destination socket tuples among those events: 16,103. Repeated SYN events are not deduplicated into attempts.
- Parser-accepted flow records: 14,157: 10,235 associated with TCP port 8443 and 3,922 associated with TCP port 4443.
- The parser groups traffic into 4 windows using a gap greater than 120 seconds; the summed first-to-last packet spans are 19.00 hours. These spans are not proof of uninterrupted board uptime.

## Window counts

| Window | First packet | Last packet | Span (h) | Port 8443 accepted records | Port 4443 accepted records |
|---:|---|---|---:|---:|---:|
| 1 | 2026-09-09 08:24:23.651742 | 2026-09-09 11:16:34.160596 | 2.87 | 661 | 0 |
| 2 | 2026-09-09 12:31:41.135774 | 2026-09-09 15:08:52.100206 | 2.62 | 599 | 325 |
| 3 | 2026-09-09 16:45:26.961608 | 2026-09-09 22:10:04.714614 | 5.41 | 7121 | 2725 |
| 4 | 2026-09-10 03:09:34.628637 | 2026-09-10 11:15:19.811735 | 8.10 | 1854 | 872 |

## Interpretation limits

The historical analysis script labels port 8443 as the custom hybrid endpoint and port 4443 as Classical TLS. A later manuscript labels port 4443 as wolfSSL hybrid TLS 1.3. The packet text and this parser identify ports and payload heuristics only; they do not resolve that disagreement. Separate USB serial excerpts show small classical and hybrid TLS acquisitions, but they do not map the port-4443 endurance traffic to a negotiated TLS group or to a specific build.

A parser-accepted record is not a cryptographic-success assertion. The difference between SYN events, distinct socket tuples, and parser-accepted records must not be converted into a failure rate: SYN retransmissions, parser criteria, capture gaps, and endpoint attribution are not fully resolved. Turnaround values from the historical CSV are not complete TLS handshake latency. This capture does not establish a board model/clock, watchdog behavior, heap stability, or a matched performance comparison.

The generated CSV preserves accepted records with neutral port-based labels. The original supplied CSV and raw capture remain unchanged.
