"""Host checks against both server entry points; not hardware measurements."""
import asyncio
import hmac
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey

ROOT = Path(__file__).resolve().parents[1]


def load_server(name):
    spec = importlib.util.spec_from_file_location('tested_' + name, ROOT / 'server' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestSubmissionFixes(unittest.TestCase):
    def test_real_parser_and_response_transcript(self):
        for entry in ('server', 'app'):
            module = load_server(entry)
            server = module.HybridPQCServer()
            public = X25519PrivateKey.generate().public_key().public_bytes_raw()
            unsigned = b'\x02' + public + bytes(1184)
            request = unsigned + hmac.digest(module.HANDSHAKE_PSK, unsigned, 'sha256')
            self.assertEqual(len(request), 1249)
            # A substitute KEM output isolates framing/authentication for this test.
            with patch.object(server, '_perform_mlkem_encaps', return_value=(bytes(1088), bytes(32))):
                response = asyncio.run(server.handle_handshake(None, None, request))
            self.assertEqual(len(response), 1168)
            expected = hmac.digest(module.HANDSHAKE_PSK, unsigned + response[:-32], 'sha256')
            self.assertTrue(hmac.compare_digest(response[-32:], expected))
            wrong = hmac.digest(module.HANDSHAKE_PSK, request + response[:-32], 'sha256')
            self.assertFalse(hmac.compare_digest(response[-32:], wrong))
            tampered = request[:-1] + bytes([request[-1] ^ 1])
            self.assertEqual(asyncio.run(server.handle_handshake(None, None, tampered)), b'')

    def test_missing_native_library_fails_without_simulation(self):
        for entry in ('server', 'app'):
            module = load_server(entry)
            with patch.object(module, 'libmlkem', None):
                with self.assertRaises(RuntimeError):
                    module.HybridPQCServer()._perform_mlkem_encaps(bytes(1184))


if __name__ == '__main__':
    unittest.main()
