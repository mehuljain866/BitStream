"""Regression tests for BitStream's binary container and safe extraction."""
import hashlib
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

import index


class ContainerTests(unittest.TestCase):
    def test_normal_container_round_trip(self):
        payload = b"\x00\xffbinary\x00payload"
        container = index._make_container(payload, index.MODE_NORMAL)
        self.assertEqual(index._parse_container(container, index.MODE_NORMAL), payload)

    def test_steg_container_round_trip(self):
        payload = b"steganography payload"
        container = index._make_container(payload, index.MODE_STEG)
        self.assertEqual(index._parse_container(container, index.MODE_STEG), payload)

    def test_checksum_rejects_corruption(self):
        container = bytearray(index._make_container(b"payload", index.MODE_NORMAL))
        container[-1] ^= 1
        with self.assertRaisesRegex(ValueError, "integrity"):
            index._parse_container(bytes(container))

    def test_truncated_payload_rejected(self):
        container = index._make_container(b"payload", index.MODE_NORMAL)
        with self.assertRaisesRegex(ValueError, "truncated"):
            index._parse_container(container[:-2])

    def test_invalid_signature_rejected(self):
        with self.assertRaisesRegex(ValueError, "does not contain"):
            index._parse_container(b"not a BitStream video")


class ExtractionSafetyTests(unittest.TestCase):
    def test_zip_slip_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            archive = root / "evil.zip"
            with zipfile.ZipFile(archive, "w") as zf:
                zf.writestr("../outside.txt", "bad")
            with self.assertRaisesRegex(ValueError, "Unsafe archive path"):
                index._safe_extract(archive, root / "out")
            self.assertFalse((root / "outside.txt").exists())

    def test_normal_zip_extract(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            archive = root / "ok.zip"
            with zipfile.ZipFile(archive, "w") as zf:
                zf.writestr("folder/file.txt", "hello")
            index._safe_extract(archive, root / "out")
            self.assertEqual((root / "out/folder/file.txt").read_text(), "hello")


if __name__ == "__main__":
    unittest.main()
