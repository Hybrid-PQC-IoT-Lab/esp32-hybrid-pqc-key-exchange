# ML-KEM-768 self-consistency cases

`tools/test_mlkem768_kat.py` retains its historical filename. It checks two
fixed-seed round trips, altered-ciphertext behavior and 100 randomized round trips.
It prints digests but does not compare them with independently sourced expected
answers. No NIST CAVP/ACVP validation or timing-leakage proof is claimed.

From the repository root:

```bash
make -C firmware/components/mlkem768
python3 tools/test_mlkem768_kat.py
```

`docs/evidence/mlkem768_kat_verification.log` is preserved historical output.
Its original KAT and no-timing-oracle labels are narrower than the evidence and
are superseded by the scope statement above. New host outputs belong in the
generated validation directory, separately from hardware evidence.
