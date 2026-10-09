# Reference metadata check â€” 5 October 2026

All 40 bibliography entries were extracted. Publisher-deposited Crossref metadata was retrieved for 34 DOI records. Retrieved titles matched the cited work; NIST records sometimes omit the standard number/subtitle from their metadata. Authors, dates, pages and volume/issue returned by the service are preserved in REFERENCE_METADATA_CHECK.json for final review.

Three requests returned rate limits: b2 (FIPS 203), b6 (Cortex-M4 Kyber implementation) and b9 (SP 800-227). The b18 DOI was not returned by Crossref. These responses do not establish that the references are false. The b18 paper was located in the author's primary IACR ePrint PDF; its cited author/title are consistent. NIST's primary page confirms the SP 800-227 title, authors, September 2025 publication and DOI. b7 and b28 have no cited DOI and require document-level checks.

Primary sources checked separately:

- RFC 10024: https://www.rfc-editor.org/info/rfc10024/
- RFC 9954: https://www.rfc-editor.org/info/rfc9954/
- NIST SP 800-227: https://csrc.nist.gov/pubs/sp/800/227/final
- Side-channel paper: https://eprint.iacr.org/2019/948.pdf

No bibliography identifier was changed solely because of a rate limit or failed metadata retrieval. Matching a DOI/title is not a full claim audit or a novelty search. In particular, Cortex-M4 optimization papers must not be described as ESP32 experiments, and integrated TLS papers must not be described as standalone kernels. The introductory contribution comparison was narrowed accordingly.

## Revision check on 6 October 2026

All44 S1 bibliography URLs were requested from their primary DOI/publisher or standards sources.41 returned content; b11, b14 and b3 requests remain unavailable in this environment. Access records are saved in REFERENCE_PRIMARY_ACCESS.json. HTTP access is not full metadata or claim-support verification; anti-bot pages may return successful status. No reference is declared false solely due to failed access. X-Wing has been corrected to its published IACR Communications in Cryptology1(1),2024 record. Full text support for every claim is not certified.
