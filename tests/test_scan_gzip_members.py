# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""단일 gzip 경계·헤더·trailer·크기·값 비공개 계약의 회귀 시험."""

import gzip
import hashlib
import json
import struct
from unittest.mock import patch
import zlib

from test_scan_secrets import RepositoryCase, ROOT, archive_bytes, fixture_policy


def gzip_member(content, *, name=b"", comment=b"", extra=b"", header_crc=False):
    """선택 metadata와 올바른 CRC를 가진 작은 단일 gzip fixture."""
    flags = (8 if name else 0) | (16 if comment else 0) | (4 if extra else 0) | (2 if header_crc else 0)
    header = b"\x1f\x8b\x08" + bytes([flags]) + b"\0" * 4 + b"\0\xff"
    if extra:
        header += struct.pack("<H", len(extra)) + extra
    if name:
        header += name + b"\0"
    if comment:
        header += comment + b"\0"
    if header_crc:
        header += struct.pack("<H", zlib.crc32(header) & 0xffff)
    compressor = zlib.compressobj(wbits=-zlib.MAX_WBITS)
    body = compressor.compress(content) + compressor.flush()
    return header + body + struct.pack("<II", zlib.crc32(content), len(content))


class GzipMemberBoundaryTests(RepositoryCase):
    def setUp(self):
        super().setUp()
        self.raw = gzip.decompress(archive_bytes([("safe.txt", "safe")]))
        self.marker = "api_" + "key=generated-gzip-canary database." + "internal"
        self.scripts = [ROOT / "tools/scan_secrets.py", ROOT / "tools/check_prod_redaction.py"]

    def check_both(self, data, expected):
        self.write("vendor/lib.tgz", data)
        for script in self.scripts:
            with self.subTest(tool=script.name):
                result = self.run_scan("--all", script=script)
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
                self.assertNotIn(self.marker, result.stdout + result.stderr)
                self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_single_member_first_header_metadata_is_scanned(self):
        for field in ["name", "comment", "extra"]:
            with self.subTest(field=field):
                self.check_both(gzip_member(self.raw, **{field: self.marker.encode()}), 1)

    def test_second_empty_member_metadata_is_rejected(self):
        for field in ["name", "comment", "extra"]:
            with self.subTest(field=field):
                second = gzip_member(b"", **{field: self.marker.encode()})
                self.check_both(gzip_member(self.raw) + second, 2)

    def test_safe_empty_or_nonempty_concatenated_members_are_rejected(self):
        for second in [b"", self.raw]:
            with self.subTest(empty=not second):
                self.check_both(gzip_member(self.raw) + gzip_member(second), 2)

    def test_nested_source_cannot_hide_a_second_gzip_header(self):
        nested = gzip_member(self.raw) + gzip_member(b"", name=self.marker.encode())
        self.check_both(archive_bytes([("package/source.tar.gz", nested)]), 2)

    def test_gzip_padding_and_nonmember_trailing_bytes_are_rejected(self):
        for suffix in [b"\0" * 8, b"\0" + self.marker.encode(), b"not-another-member"]:
            self.check_both(gzip_member(self.raw) + suffix, 2)

    def test_single_member_with_magic_in_extra_and_valid_header_crc_is_allowed(self):
        data = gzip_member(self.raw, name=b"public.tar", comment=b"public source",
                           extra=b"\x1f\x8b\x08\0embedded-magic", header_crc=True)
        self.check_both(data, 0)

    def test_corrupt_crc_size_header_crc_and_truncated_trailer_are_rejected(self):
        safe = gzip_member(self.raw)
        bad_crc, bad_size = bytearray(safe), bytearray(safe)
        bad_crc[-8] ^= 1
        bad_size[-4] ^= 1
        bad_header = bytearray(gzip_member(self.raw, header_crc=True))
        bad_header[10] ^= 1
        for data in [bytes(bad_crc), bytes(bad_size), bytes(bad_header), safe[:-1], safe[:-8]]:
            self.check_both(data, 2)

    def test_single_member_expansion_limits_include_exact_boundary(self):
        from tools import _scan
        data = gzip_member(self.raw)
        for setting in ["MAX_ARCHIVE_BYTES", "MAX_EXPANDED_BYTES"]:
            with self.subTest(setting=setting):
                with patch.object(_scan, setting, len(self.raw)):
                    self.assertTrue(list(_scan.scan_parts("lib.tgz", data, {}, _scan.ArchiveBudget())))
                with patch.object(_scan, setting, len(self.raw) - 1):
                    with self.assertRaises(_scan.ScanError):
                        list(_scan.scan_parts("lib.tgz", data, {}, _scan.ArchiveBudget()))

    def test_digest_exception_does_not_allow_a_second_gzip_header(self):
        for policy, rule in [(".secret-scan-patterns", "SECRET-ASSIGNMENT"),
                             (".prod-redaction-patterns", "INTERNAL-HOST")]:
            record = {"path": "vendor/lib.tgz!/safe.txt", "rules": [rule],
                      "sha256": hashlib.sha256(b"safe").hexdigest(), "reason": "공개 fixture 고정 bytes"}
            text = fixture_policy(policy) + "\n[[allowlist]]\n" + "\n".join(
                key + "=" + json.dumps(value, ensure_ascii=False) for key, value in record.items()) + "\n"
            self.write(policy, text)
        self.check_both(gzip_member(self.raw), 0)
        self.check_both(gzip_member(self.raw) + gzip_member(b"", name=self.marker.encode()), 2)
