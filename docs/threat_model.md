# Threat model and verified scope

The supplied symbolic model has an active Dolev–Yao network adversary, idealized
cryptographic functions and a private, uncompromised PSK.

| Property | Evidence and boundary |
|---|---|
| Modeled client/server payload confidentiality | Archived ProVerif output says `not attacker(secret_client_data[])` and `not attacker(secret_server_data[])` are true. |
| Client-to-server injective key agreement | Archived query `inj-event(client_key_derived(k)) ==> inj-event(server_key_derived(k))` is true. Reverse correspondence is not queried. |
| Session-key secrecy | No separate session-key exposure query is encoded; do not quote a nonexistent `k_session` result. |
| Forward secrecy after PSK disclosure | Design rationale only; no PSK-reveal process or query. Requires secure ephemeral erasure and cryptographic assumptions. |
| Quantum resistance | Depends on the ML-KEM security assumptions and the combiner, not a ProVerif proof of quantum hardness. |
| Telemetry replay | Server checks increasing 32-bit counters. Both directions share one key and lack a direction label; reflection/cross-direction replay remains a limitation. |
| Timing/power leakage | Not empirically evaluated. No TVLA, DPA or compiler-level constant-time verification. |
| Device memory dump | Selected client buffers are zeroized. Active session keys, server objects, copies and registers are not covered by a complete erasure proof. |

The public repository PSK is an evaluation constant, not a deployment secret.
Authentication claims assume a private provisioned PSK. Session IDs are generated
server-side using `secrets.token_bytes(16)`. Client nonce random suffixes use
`esp_fill_random`; server acknowledgments use the server OS CSPRNG. Both directions
sharing one traffic key must not be described as providing directional binding.

The corrected code removes simulated ML-KEM fallback output. Host tests do not
replace hardware integration tests. The unchanged formal model does not establish
correctness of the implementation's concrete message parser, IV policy or scheduler.
