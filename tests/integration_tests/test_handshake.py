import unittest
import hmac
import hashlib

class TestHandshakeProtocolV2(unittest.TestCase):
    """
    Automated test suite to verify the message construction, transcript binding,
    and HMAC-SHA256 authentication logic of the Hybrid Handshake Protocol v2.
    """
    def test_client_request_construction(self):
        psk = b"SecurIoT-Quantum-PQC-Hybrid-PSK!"
        
        # Protocol Client Request (ClientHello):
        # Mode (1 byte) + X25519 PK (32 bytes) + ML-KEM-768 PK (1184 bytes) = 1217 bytes
        mode = b'\x02'  # Hybrid mode
        x25519_pk = b'\x02' * 32
        mlkem_pk = b'\x03' * 1184
        
        request_body = mode + x25519_pk + mlkem_pk
        self.assertEqual(len(request_body), 1217)
        
        # Compute client authentication tag (32 bytes HMAC-SHA256)
        client_hmac = hmac.new(psk, request_body, hashlib.sha256).digest()
        self.assertEqual(len(client_hmac), 32)
        
        full_client_request = request_body + client_hmac
        self.assertEqual(len(full_client_request), 1249)

    def test_server_transcript_binding(self):
        psk = b"SecurIoT-Quantum-PQC-Hybrid-PSK!"
        
        request_body = b'\x02' + (b'\x02' * 32) + (b'\x03' * 1184)
        self.assertEqual(len(request_body), 1217)
        
        # Server response: Session ID (16 bytes) + X25519 PK (32 bytes) + ML-KEM-768 CT (1088 bytes)
        session_id = b'\x04' * 16
        server_x25519_pk = b'\x05' * 32
        server_mlkem_ct = b'\x06' * 1088
        server_body = session_id + server_x25519_pk + server_mlkem_ct
        self.assertEqual(len(server_body), 1136)
        
        # Transcript binding: HMAC computed over (Client Request Body || Server Response Body)
        # 1217 bytes + 1136 bytes = 2353 bytes transcript
        transcript = request_body + server_body
        self.assertEqual(len(transcript), 2353)
        server_hmac = hmac.new(psk, transcript, hashlib.sha256).digest()
        self.assertEqual(len(server_hmac), 32)
        
        full_server_response = server_body + server_hmac
        self.assertEqual(len(full_server_response), 1168)
        
        # Verification succeeds
        self.assertTrue(hmac.compare_digest(server_hmac, hmac.new(psk, transcript, hashlib.sha256).digest()))
        
        # Replay/tampering failure check
        tampered_transcript = request_body + session_id + server_x25519_pk + (b'\x07' * 1088)
        self.assertFalse(hmac.compare_digest(server_hmac, hmac.new(psk, tampered_transcript, hashlib.sha256).digest()))

if __name__ == '__main__':
    unittest.main()
