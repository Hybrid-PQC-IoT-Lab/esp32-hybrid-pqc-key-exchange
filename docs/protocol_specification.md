# Hybrid Post-Quantum Key Exchange Protocol Specification

## 1. Overview
The protocol establishes a hybrid session key (forward secrecy is a design rationale, not a queried post-compromise result) between an ESP32 edge client and a backend server by combining:
1. **Classical ECDH**: X25519 (Curve25519, RFC 7748).
2. **Post-Quantum KEM**: ML-KEM-768 (NIST FIPS 203, Kyber-768).
3. **Key Derivation Function**: HKDF-SHA256 (RFC 5869).
4. **Mutual Authentication & Transcript Binding**: HMAC-SHA256 with Pre-Shared Key (PSK).
5. **Authenticated Telemetry**: AES-256-GCM with 32-bit monotonic counters and 64-bit random IV suffixes.

---

## 2. Handshake Message Formats

### Message 1: Client Handshake Request (`POST /handshake`)
```
+--------+---------------------+---------------------+----------------------+
| Mode   | X25519 Ephemeral PK | ML-KEM-768 PK       | Client HMAC-SHA256   |
| 1 byte | 32 bytes (if hybrid)| 1184 bytes (hybrid) | 32 bytes             |
+--------+---------------------+---------------------+----------------------+
```
* **Mode**:
  - `0x00`: Classical X25519 only (65 bytes total).
  - `0x01`: PQC ML-KEM-768 only (1,217 bytes total).
  - `0x02`: Hybrid (X25519 + ML-KEM-768, 1,249 bytes total).
* **Public Keys**: Ephemeral public keys corresponding to the chosen mode.
* **Client HMAC**: $\text{HMAC-SHA256}_{PSK}(\text{Mode} \parallel \text{Public Keys})$.

### Message 2: Server Handshake Response
```
+-----------------+---------------------+----------------------+----------------------+
| Session ID      | X25519 Ephemeral PK | ML-KEM-768 CT        | Server Transcript    |
| 16 bytes        | 32 bytes (if hybrid)| 1088 bytes (hybrid)  | HMAC-SHA256 (32 B)   |
+-----------------+---------------------+----------------------+----------------------+
```
* **Session ID**: 16-byte random session identifier generated server-side by Python `secrets.token_bytes(16)` (OS CSPRNG).
* **Server Ephemeral PK**: Server's ephemeral X25519 public key.
* **ML-KEM-768 Ciphertext**: 1088-byte ciphertext encapsulated against client's `mlkem_pk`.
* **Server Transcript HMAC**:
  $$\text{HMAC-SHA256}_{PSK}(\text{Client Request Without Its HMAC} \parallel \text{Session ID} \parallel \text{Server Ephemeral Keys/Ciphertext})$$
  This binds the authenticated server response to the client request, under an uncompromised private PSK. It does not establish directional telemetry security.

---

## 3. Key Derivation
Upon successful decapsulation and ECDH computation:
1. **Shared Secret Concatenation**:
   $$SS_{hybrid} = SS_{X25519} \parallel SS_{ML-KEM-768} \quad (\text{64 bytes})$$
   *(Note: RFC 7748 Section 6.1: Weak/all-zero $SS_{X25519}$ values are rejected in constant time prior to HKDF combination).*
2. **HKDF Extraction**:
   $$PRK = \text{HKDF-Extract}(\text{salt}=\text{"HybridPQC-ESP32-Session-v1"}, IKM=SS_{hybrid})$$
3. **HKDF Expansion**:
   $$K_{session} = \text{HKDF-Expand}(PRK, \text{info} = \text{"session-key"}, L = 32)$$
4. **Zeroization**: Immediately following key derivation, selected client ephemeral buffers are wiped using `mbedtls_platform_zeroize`. This is not proof that every copy, server object or live session key is erased.

---

## 4. Authenticated Telemetry (`POST /api/telemetry`)
```
+-----------------+---------------------+-----------------------+--------------------+
| Session ID      | GCM IV              | Encrypted Payload     | GCM Tag            |
| 16 bytes        | 12 bytes            | Variable length       | 16 bytes           |
+-----------------+---------------------+-----------------------+--------------------+
```
* **GCM IV**: 12 bytes = 4-byte big-endian monotonic sequence counter + 8-byte random salt ($IV = \text{Counter}_{32} \parallel \text{Random}_{64}$).
* **Additional Authenticated Data (AAD)**: None (`NULL, 0`). Sequence counter integrity and packet ordering are enforced directly through the GCM IV Galois counter computation and the 16-byte authentication tag.
* **Anti-Replay**: The server strictly enforces that the incoming sequence counter exceeds the highest sequence counter recorded for that session ($C_{\text{recv}} > C_{\text{last}}$). Replayed or out-of-order packets are dropped immediately.

## 5. Formal abstraction

The archived ProVerif model captures the two ephemeral components and response binding to the client parameters. It omits the concrete SID, mode byte, HKDF salt/info encodings, nonce/counter state and later PSK compromise. Its three queries do not prove complete byte-level or telemetry conformance.

## 6. Scope limitations

The hybrid handshake bodies total 1,249 + 1,168 = 2,417 bytes, excluding HTTP/TCP/IP framing. Both telemetry directions use the same key, without a direction label or separate traffic keys. Monotonic counters do not prevent directional reflection. The client checks the response counter against its request counter; this is not general cross-direction replay protection.

The server transcript prefix excludes the client authentication tag: 1,217 request bytes in hybrid mode, followed by the 1,136-byte unsigned server response. The complete request and response bodies remain 1,249 and 1,168 bytes.
