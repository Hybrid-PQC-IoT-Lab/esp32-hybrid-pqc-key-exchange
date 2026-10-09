# Final consistency audit, 6 October 2026

## Decision

GO for author review of bounded software and archived-observation claims.
NO-GO for a fully validated security/performance claim or a claim that every
historical experiment used the corrected frozen firmware. Acceptance cannot be
predicted from this audit. The existing Computer Networks submission is preserved;
this candidate has not replaced its files or created another submission.

## Corrections and verification

- 100 archived UART/CSV observations match. Mean instrumented latency616.7478ms,
  sample SD244.12824ms, Student-t95% CI568.30746 to665.18814ms. The wider cycle
  measurement interval averages100,330,347.16cycles; it is a different boundary.
- Independent13.8KB allocation report separated from campaign snapshots. The
  latter do not establish peak heap;32KiB is configured stack, not measured usage.
- AES-GCM has no AAD. Shared directional keys and reflection remain disclosed.
- X25519 all-zero rejection exists. Three focused host checks pass; the firmware
  logic emulation does not establish native board execution or constant-time use.
- Two server framing/HMAC checks pass using substituted KEM output. Native ML-KEM
  was unavailable locally, so these are not end-to-end KEM conformance tests.
- Four evidence-analysis tests pass: accepted-row accounting, duplicate-ID
  rejection, energy window arithmetic and rejection of nonfinite inputs.
- Endurance CSV has14,157 accepted rows,10,235 Hybrid-PQC and3,922 Classical-TLS
  stored labels.17,502 is a reported TCP SYN count;8,640 is schedule arithmetic.
  Neither replaces an observed completed-handshake count or all-attempt denominator.
- Energy helper now reads the electrical worksheet and exposes assumed current
  and window.0.75J describes150mA at5V for1s; it is not an absolute handshake bound
  when recorded duration can exceed1s. No measured mean/SD/CI is generated.
- Formal claims limited to the actual private-PSK symbolic model. Later PSK
  compromise, concrete GCM nonces and complete bidirectional replay protection
  are not established. KAT-labelled files remain self-consistency evidence.
- Sequence and architecture drawings now match HTTP exchange without a Finished
  flight and the aiohttp/native server. New diagrams are vector PDF/SVG.
- All44 S1 bibliography primary URLs were requested:41 returned content,3 did
  not. HTTP retrieval is not claim support verification. Prior metadata checks
  and corrected X-Wing entry are recorded in REFERENCE_AUDIT.md. Do not describe
  the entire bibliography as conclusively verified.
- Corrected compiler archive at db93361 contains verified ELF/map/bin/sdkconfig.
  Its firmware and server Git trees equal this revision's trees. This supports
  source/build consistency, not historical measurement-binary identity or a new
  physical execution. Four recorded artifact hashes and archive hash match.

## Remaining evidence and exact next steps

1. Recover the full historical boot digest, ELF/map/sdkconfig and complete run
   metadata. If unrecoverable, flash an identified corrected build and record a
   fresh100-attempt campaign retaining all failures, runtime clock, timestamps,
   ELF/bin hashes and analysis output. Keep it separate from the historical data.
2. Capture successful telemetry49,50 and rotation, plus three-consecutive-error
   termination and recovery on the board. Save serial and live wire traces.
3. Recover dual_bench_final_complete.log and the original master tcpdump; recount
   attempts, completions and failures with explicit criteria. If unavailable,
   rerun endurance with monotonic timestamps, resets/watchdog events, attempt and
   completion IDs and full logs. Do not infer zero failure from accepted rows.
4. Recover transient heap/stack/static-memory traces and matching historical
   binary. Otherwise perform a fresh instrumented allocation/stack measurement
   and identify which acquisition and build produced each value.
5. Retain worksheet-based energy estimates only. Integrated energy claims require
   calibrated high-rate synchronized voltage/current traces covering each full
   handshake, sample-rate/device metadata, and integration analysis.
6. Run independent expected-answer or interoperability tests on the native
   ML-KEM-768 backend, preserving vector source/version and full output. Label
   self-consistency separately. Recover matched authenticated TLS baselines and
   negotiated-group/configuration evidence before making controlled comparisons.
7. Direction-separated keys and authenticated role/session metadata would change
   the protocol. Implement and validate them as a new revision with fresh board
   evidence before claiming replay/reflection resistance or production security.
8. Finish primary-source claim support checks for each reference, including
   inaccessible entries, and author approval of this revised candidate.

A missing original record does not prove that the experiment never happened.
Editorial consistency does not manufacture the missing record.
