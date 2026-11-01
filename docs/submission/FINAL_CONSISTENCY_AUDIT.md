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

## GitHub and supplied-archive cross-check, 2 November 2026

- The public repository resolves the `v2.7.1-journal-submission-kit` release
  tag to source commit `b4b718cd359f0c134fc7bfc619172c01bdf6eb49`. GitHub marks
  that release as a prerelease and `immutable: false`; cite the full commit SHA
  as the reproducible source identity, not the mutable tag. The default `main`
  branch is at `670448651276740e0d58931f388ca32035cb6245`, an earlier
  30 September snapshot, so it is not the release candidate.
- The attached Evidence Package 5 `hybrid_handshake_100_runs.csv` SHA-256 is
  `a3744338b3ffa847bd9f79a84a4f912b7e20967b21c5442d47818bf66a4e3af3` and its
  raw UART-log hash is `41cb43703cd7f7e0dcef6d009d9087666176bd0fcd63dbc96358ea44e82e5025`.
  Both match the corresponding local evidence files in the repository. The
  paper's captured-endurance SHA-256
  `958cf70de291297887b70c49e2e6cb8c90e44fc6f5b48036c4da7758867c4494` matches
  `data/raw_logs/dual_bench_8h.log` and its `SHA256SUMS.txt` entry.
- The attached Evidence Package 5 is not the current manuscript package:
  its `10_submission/COMMIT.txt` identifies commit `467bbe7` and tag
  `v2.1-mlkem768-final`, while the archive's root README names an older
  `v2.0-mlkem768-final`. Do not substitute its bundled `research_paper.tex`
  or PDF for the revised local manuscript. Its raw campaign CSV is usable and
  matches the cited dataset; its old manuscript and historical claims are not
  the current submission version.
- GitHub's v2.7.1 release kit ZIP is present locally and its SHA-256 matches
  the published asset. However, the release's `Main_Manuscript.pdf` has SHA-256
  `b35984b3a06f4daf066be2321ebff7205624381a269610417d43dd07d9f0aff8` and size
  329,835 bytes, while the revised local manuscript PDF has SHA-256
  `dabccfdf88df35c30fb0cbba42b6053bf39e0c93d3a168c08c13df9cea8e72be` and size
  2,515,535 bytes after removing the stale release-page pointer. They are different
  files. The revised local `.tex` also has
  uncommitted manuscript edits relative to commit `b4b718c`. Therefore, use
  the revised local manuscript source and its recompiled PDF for author review;
  do not download the release's manuscript PDF as the current version. The
  code/evidence snapshot cited by the paper is present at the pinned commit,
  but the latest manuscript itself has not been published in that release.
- A read-only scan of the supplied ZIPs and tracked repository files found no
  private-key PEM blocks, private SSH key files, or SSH public-key lines. The
  checked SHA-256 identifiers matched their referenced files. This check is
  about those artifacts only; it is not a scan of browser or machine-wide
  credentials.

### Action recorded

The manuscript availability wording and software reference identify the exact
source commit, and no longer point readers to the stale v2.7.1 release page as
the current manuscript location. The revised source, figure and compiled PDF
are being published on a new dated submission-candidate branch. The existing
v2.7.1 prerelease and its release assets remain unchanged and do not contain
this revised manuscript PDF.
