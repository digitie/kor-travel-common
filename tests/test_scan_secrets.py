# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""비밀 검사기의 스냅샷 선택·값 비공개·입력 실패를 검증한다."""

from pathlib import Path
import gzip
import io
import tarfile
from unittest.mock import patch
import json
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/scan_secrets.py"
POLICY = ".secret-scan-patterns"


class RepositoryCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="kt-scan-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "-q")
        for name in (POLICY, ".prod-redaction-patterns"):
            self.write(name, (ROOT / name).read_text(encoding="utf-8"))
        self.write("sample.txt", "안전한 문서\n")
        self.git("add", POLICY, ".prod-redaction-patterns", "sample.txt")
        self.commit()

    def write(self, name, value):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(value, bytes):
            path.write_bytes(value)
        else:
            path.write_text(value, encoding="utf-8", newline="\n")
        return path

    def git(self, *args):
        result = subprocess.run(["git", "-C", str(self.root), *args], capture_output=True, check=True)
        return result.stdout.decode("utf-8").strip()

    def commit(self):
        self.git("-c", "user.name=테스트", "-c", "user.email=test@example.invalid",
                 "commit", "-q", "-m", "검사 fixture")
        return self.git("rev-parse", "HEAD")

    def run_scan(self, *args, script=SCRIPT):
        return subprocess.run([sys.executable, "-B", "-X", "utf8", str(script),
                               "--root", str(self.root), *args], capture_output=True,
                              text=True, encoding="utf-8")


def archive_bytes(entries):
    """시험용 메모리 tar.gz. 링크·선언 크기 시험은 TarInfo를 그대로 전달한다."""
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz", format=tarfile.PAX_FORMAT) as archive:
        for name, content in entries:
            info = name if isinstance(name, tarfile.TarInfo) else tarfile.TarInfo(name)
            if content is None:
                archive.addfile(info)
            else:
                data = content.encode("utf-8") if isinstance(content, str) else content
                info.size = len(data)
                archive.addfile(info, io.BytesIO(data))
    return buffer.getvalue()


def wasm_bytes(payload):
    """ASCII 문자열을 포함한 유효한 WASM custom section."""
    section = b"\x07fixture" + payload
    assert len(section) < 128
    return b"\0asm\x01\0\0\0\0" + bytes([len(section)]) + section


class SecretScanTests(RepositoryCase):
    def test_safe_tree_and_untracked_secret(self):
        self.assertEqual(self.run_scan("--all").returncode, 0)
        sample_value = "generated-" + "sensitive-value"
        self.write("new.txt", "api_" + "key=" + sample_value)
        result = self.run_scan("--all")
        self.assertEqual(result.returncode, 1)
        self.assertNotIn(sample_value, result.stdout + result.stderr)
        finding = json.loads(result.stdout.splitlines()[0])
        self.assertEqual(finding, {"path": "new.txt", "line": 1, "rule": "SECRET-ASSIGNMENT"})

    def test_short_quoted_password(self):
        self.write("sample.txt", 'password="' + 'a' + '"')
        self.assertEqual(self.run_scan().returncode, 1)

    def test_private_key_and_provider_tokens(self):
        for value in ("-----BE" + "GIN RSA PRIVATE KEY-----", "AK" + "IA" + "A" * 16,
                      "gh" + "p_" + "a" * 36, "pbkdf2_" + "sha256$1000$salt$YWJjZA=="):
            with self.subTest(kind=value[:2]):
                self.write("sample.txt", value)
                result = self.run_scan()
                self.assertEqual(result.returncode, 1)
                self.assertNotIn(value, result.stdout + result.stderr)

    def test_placeholders_and_field_names(self):
        self.write("sample.txt", 'API_KEY=<비밀>\npassword="${PASSWORD}"\n'
                   'api_key, secret, token, password, passwd\nhttps://<user>:<password>@example.invalid\n')
        self.assertEqual(self.run_scan().returncode, 0)

    def test_staged_blob_not_working_copy_or_working_policy(self):
        self.write("sample.txt", "api_" + "key=" + "abcdefghijk")
        self.git("add", "sample.txt")
        self.write("sample.txt", "치환 완료")
        self.write(POLICY, 'version=1\n[[patterns]]\nid="NO-MATCH"\nregex="never-[0-9]{6}-detect"\n')
        self.assertEqual(self.run_scan("--staged").returncode, 1)
        self.assertEqual(self.run_scan("--all").returncode, 0)

    def test_commit_blob_not_index_or_working_copy(self):
        base = self.git("rev-parse", "HEAD")
        self.write("sample.txt", "tok" + "en=" + "abcdefghijk")
        self.git("add", "sample.txt")
        self.commit()
        self.write("sample.txt", "치환 완료")
        self.git("add", "sample.txt")
        self.assertEqual(self.run_scan("--base", base).returncode, 1)

    def test_empty_change_and_invalid_ref_fail(self):
        self.assertEqual(self.run_scan("--staged").returncode, 2)
        self.assertEqual(self.run_scan("--base", "missing-ref").returncode, 2)
        self.assertEqual(self.run_scan("--base", "HEAD").returncode, 2)

    def test_invalid_policy_never_echoes_input(self):
        marker = "do-not-" + "print-this-value"
        for content in (marker, 'version=1\npatterns=[]',
                        'version=1\n[[patterns]]\nid="BAD-ID"\nregex="["\n',
                        'version=1\n[[patterns]]\nid="BAD-ID"\nregex=".*"\n'):
            self.write(POLICY, content)
            result = self.run_scan()
            self.assertEqual(result.returncode, 2)
            self.assertNotIn(marker, result.stdout + result.stderr)

    def test_missing_and_binary_input_fail(self):
        for content in (b"\xff\xfe", b"abc\0def"):
            self.write("sample.txt", content)
            self.assertEqual(self.run_scan().returncode, 2)
        (self.root / "sample.txt").unlink()
        self.assertEqual(self.run_scan().returncode, 2)

    def test_deep_policy_regex_fails_without_traceback(self):
        marker = "review-" + "private-marker"
        expression = "(" * 700 + marker + ")" * 700
        for filename, script in ((POLICY, SCRIPT), (".prod-redaction-patterns", ROOT / "tools/check_prod_redaction.py")):
            self.write(filename, 'version=1\n[[patterns]]\nid="TEST-RULE"\nregex="' + expression + '"\n')
            result = self.run_scan(script=script)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("Traceback", result.stdout + result.stderr)
            self.assertNotIn(marker, result.stdout + result.stderr)

    def test_sensitive_filename_and_parent_never_print(self):
        marker = "AK" + "IA" + "A" * 16
        for name in (marker + ".txt", marker + "/sample.txt"):
            path = self.write(name, "안전한 본문")
            for content in ("안전한 본문", marker):
                path.write_text(content, encoding="utf-8")
                result = self.run_scan()
                self.assertEqual(result.returncode, 2)
                self.assertNotIn(marker, result.stdout + result.stderr)
            path.unlink()

    def test_exact_rule_exception_and_bad_allowlist(self):
        original = (ROOT / POLICY).read_text(encoding="utf-8")
        self.write("sample.txt", "api_" + "key=" + "abcdefghijk")
        extra = '\n[[allowlist]]\npath="sample.txt"\nrules=["SECRET-ASSIGNMENT"]\nreason="검사 fixture"\n'
        self.write(POLICY, original + extra)
        result = self.run_scan()
        self.assertEqual(result.returncode, 0)
        self.assertIn("명시적 예외 1건", result.stdout)
        for invalid in (extra.replace("sample.txt", "*.txt"), extra.replace("sample.txt", "../outside"),
                        extra.replace("검사 fixture", ""), extra.replace("SECRET-ASSIGNMENT", "UNKNOWN")):
            self.write(POLICY, original + invalid)
            self.assertEqual(self.run_scan().returncode, 2)

    def test_symlink_and_submodule_index_fail(self):
        blob = self.git("hash-object", "-w", "sample.txt")
        self.git("update-index", "--add", "--cacheinfo", "120000," + blob + ",link.txt")
        self.assertEqual(self.run_scan("--staged").returncode, 2)
        self.git("update-index", "--cacheinfo", "120000," + blob + ",sample.txt")
        self.git("update-index", "--force-remove", "link.txt")
        self.assertEqual(self.run_scan("--staged").returncode, 2)
        head = self.git("rev-parse", "HEAD")
        self.git("update-index", "--add", "--cacheinfo", "160000," + head + ",submodule")
        self.assertEqual(self.run_scan("--staged").returncode, 2)

    def test_newline_filename_and_subdirectory_root_fail(self):
        from tools._scan import ScanError, path_name
        for name in ("bad\nname.txt", "../outside", b"bad\xff.txt"):
            with self.assertRaises(ScanError):
                path_name(name)
        child = self.root / "child"
        child.mkdir()
        self.assertEqual(self.run_scan("--root", str(child)).returncode, 2)


class ArchiveSecretScanTests(RepositoryCase):
    def assert_private_failure(self, result, marker="", status=2):
        self.assertEqual(result.returncode, status, result.stdout)
        self.assertNotIn("Traceback", result.stdout + result.stderr)
        if marker:
            self.assertNotIn(marker, result.stdout + result.stderr)

    def test_safe_nested_source_and_native_payloads_without_extraction(self):
        source = archive_bytes([("src/README.md", "안전한 원본 문서")])
        native = b"\x7fELF\x02\x01\x01" + b"\0" * 57 + b"public-interface\0"
        self.write("vendor/lib.tgz", archive_bytes([
            ("package/source.tar.gz", source), ("package/addon.node", native),
            ("package/code.wasm", wasm_bytes(b"safe-bytes")),
            ("package/fixture.jpeg", b"\xff\xd8\xff\0public-caption\0"),
        ]))
        self.assertEqual(self.run_scan("--all").returncode, 0)
        self.assertFalse((self.root / "package").exists())

    def test_compressed_nested_text_secret_is_detected_without_value(self):
        marker = "generated-" + "archive-sensitive"
        content = "공개 문서\napi_" + "key=" + marker
        nested = archive_bytes([("src/settings.txt", content)])
        self.write("vendor/lib.tgz", archive_bytes([("package/source.tar.gz", nested)]))
        result = self.run_scan("--all")
        self.assert_private_failure(result, marker, status=1)
        findings = [json.loads(line) for line in result.stdout.splitlines()[:-1]]
        self.assertIn({"path": "vendor/lib.tgz!/package/source.tar.gz!/src/settings.txt",
                       "line": 2, "rule": "SECRET-ASSIGNMENT"}, findings)

    def test_native_wasm_and_image_ascii_are_scanned_not_skipped(self):
        marker = "generated-" + "native-sensitive"
        payload = ("api_" + "key=" + marker).encode()
        formats = {
            "code.wasm": wasm_bytes(b"\0" + payload + b"\0"),
            "addon.node": b"\x7fELF\x02\x01\x01" + b"\0" * 57 + payload + b"\0",
            "image.jpeg": b"\xff\xd8\xff\0" + payload + b"\0",
        }
        for name, content in formats.items():
            with self.subTest(kind=name):
                self.write("vendor/lib.tgz", archive_bytes([("package/" + name, content)]))
                result = self.run_scan()
                self.assert_private_failure(result, marker, status=1)
                findings = [json.loads(line) for line in result.stdout.splitlines()[:-1]]
                self.assertTrue(any(item["path"] == "vendor/lib.tgz!/package/" + name and "byte" in item for item in findings))

    def test_path_traversal_absolute_drive_and_invalid_utf8_fail(self):
        for name in ("../outside", "/absolute", "C:/drive", r"a\bad", "a//b",
                     "a/../b", "./inside", "\udcff.txt"):
            with self.subTest(path_kind=name[:1]):
                self.write("vendor/lib.tgz", archive_bytes([(name, "safe")]))
                self.assert_private_failure(self.run_scan())

    def test_links_devices_fifo_unknown_and_sparse_types_fail(self):
        for kind in (tarfile.SYMTYPE, tarfile.LNKTYPE, tarfile.FIFOTYPE,
                     tarfile.CHRTYPE, tarfile.BLKTYPE, tarfile.GNUTYPE_SPARSE, b"Z"):
            with self.subTest(kind=kind):
                member = tarfile.TarInfo("package/entry")
                member.type, member.linkname = kind, "../target"
                self.write("vendor/lib.tgz", archive_bytes([(member, None)]))
                self.assert_private_failure(self.run_scan())

    def test_duplicate_members_and_invalid_text_are_not_silently_ignored(self):
        cases = [
            archive_bytes([("a.txt", "safe"), ("a.txt", "safe")]),
            archive_bytes([("a.txt", b"\xff\xfe")]),
            archive_bytes([("a.txt", b"safe\0hidden")]),
        ]
        for data in cases:
            self.write("vendor/lib.tgz", data)
            self.assert_private_failure(self.run_scan())

    def test_declared_huge_member_rejected_before_payload_read(self):
        from tools._scan import MAX_MEMBER_BYTES
        member = tarfile.TarInfo("package/huge.txt")
        member.size = MAX_MEMBER_BYTES + 1
        self.write("vendor/lib.tgz", gzip.compress(member.tobuf() + b"\0" * 1024))
        self.assert_private_failure(self.run_scan())

    def test_depth_bomb_is_bounded(self):
        data = archive_bytes([("safe.txt", "safe")])
        for _ in range(5):
            data = archive_bytes([("nested.tar.gz", data)])
        self.write("vendor/lib.tgz", data)
        self.assert_private_failure(self.run_scan())

    def test_expanded_total_member_and_input_limits_without_large_fixture(self):
        from tools import _scan
        data = archive_bytes([("a.txt", "safe"), ("b.txt", "safe")])
        for setting, limit in (("MAX_ARCHIVE_BYTES", 1024), ("MAX_EXPANDED_BYTES", 1024),
                               ("MAX_ARCHIVE_MEMBERS", 1), ("MAX_INPUT_BYTES", 32)):
            with self.subTest(limit=setting), patch.object(_scan, setting, limit):
                with self.assertRaises(_scan.ScanError):
                    list(_scan.scan_parts("lib.tgz", data, {}, _scan.ArchiveBudget()))
        self.write("sample.txt", "x" * 100)
        for staged in (False, True):
            self.git("add", "sample.txt")
            snapshot = _scan.Snapshot(self.root, staged, None)
            with patch.object(_scan, "MAX_INPUT_BYTES", 20), self.assertRaises(_scan.ScanError):
                snapshot.read("sample.txt")

    def test_corrupt_crc_truncated_archive_and_trailing_payload_fail(self):
        safe = archive_bytes([("safe.txt", "safe")])
        corrupt = bytearray(safe)
        corrupt[-8] ^= 1
        with gzip.GzipFile(fileobj=io.BytesIO(safe)) as stream:
            raw = stream.read()
        marker = "generated-" + "trailing-sensitive"
        for content in (bytes(corrupt), safe[:-9], b"not-a-tar", gzip.compress(raw + marker.encode())):
            self.write("vendor/lib.tgz", content)
            self.assert_private_failure(self.run_scan(), marker)

    def test_gzip_metadata_and_pax_metadata_are_scanned(self):
        marker = "generated-" + "metadata-sensitive"
        key = "api_" + "key="
        raw = io.BytesIO()
        with tarfile.open(fileobj=raw, mode="w") as archive:
            info = tarfile.TarInfo("safe.txt")
            archive.addfile(info, io.BytesIO())
        compressed = io.BytesIO()
        with gzip.GzipFile(fileobj=compressed, mode="wb", filename=key + marker) as stream:
            stream.write(raw.getvalue())
        self.write("vendor/lib.tgz", compressed.getvalue())
        self.assert_private_failure(self.run_scan(), marker, status=1)
        info = tarfile.TarInfo("safe.txt")
        info.pax_headers = {"comment": key + marker}
        self.write("vendor/lib.tgz", archive_bytes([(info, b"safe")]))
        self.assert_private_failure(self.run_scan(), marker, status=1)

    def test_sensitive_member_paths_never_print(self):
        marker = "gh" + "p_" + "A" * 36
        self.write("vendor/lib.tgz", archive_bytes([("package/" + marker + "/data.txt", "safe")]))
        self.assert_private_failure(self.run_scan(), marker)

    def test_staged_and_commit_archives_do_not_read_working_copy(self):
        base = self.git("rev-parse", "HEAD")
        sensitive_archive = archive_bytes([("settings.txt", "api_" + "key=" + "generated-sensitive")])
        self.write("vendor/lib.tgz", sensitive_archive)
        self.git("add", "vendor/lib.tgz")
        self.write("vendor/lib.tgz", archive_bytes([("safe.txt", "safe")]))
        self.assertEqual(self.run_scan("--staged").returncode, 1)
        self.assertEqual(self.run_scan("--all").returncode, 0)
        self.commit()
        self.git("add", "vendor/lib.tgz")
        self.assertEqual(self.run_scan("--base", base).returncode, 1)

    def test_outer_archive_allowlist_does_not_allow_all_member_values(self):
        self.write("vendor/lib.tgz", archive_bytes([("a.txt", "api_" + "key=" + "generated-sensitive")]))
        original = (ROOT / POLICY).read_text(encoding="utf-8")
        self.write(POLICY, original + '\n[[allowlist]]\npath="vendor/lib.tgz"\nrules=["SECRET-ASSIGNMENT"]\nreason="표면 파일 예외"\n')
        self.assertEqual(self.run_scan().returncode, 1)

    def test_unknown_binary_and_wrong_native_signature_still_fail(self):
        for name, data in (("unknown.bin", b"\xff\0native"), ("fake.node", b"\xffnot-native"),
                           ("wasm.txt", wasm_bytes(b"safe")), ("source.zip", b"PK\3\4\0")):
            path = self.write(name, data)
            self.assert_private_failure(self.run_scan())
            path.unlink()

    def test_no_filesystem_extraction_api_is_used(self):
        from tools import _scan
        data = archive_bytes([("nested/file.txt", "safe")])
        with patch.object(tarfile.TarFile, "extract", side_effect=AssertionError("추출 금지")), \
             patch.object(tarfile.TarFile, "extractall", side_effect=AssertionError("추출 금지")):
            self.assertTrue(list(_scan.scan_parts("lib.tgz", data, {}, _scan.ArchiveBudget())))


    def test_v8_corresponding_source_fixture_ascii_is_scanned(self):
        marker = "generated-" + "v8-sensitive"
        payload = ("api_" + "key=" + marker).encode()
        native = b'\xff\x0f"' + bytes([len(payload)]) + payload
        self.write("vendor/lib.tgz", archive_bytes([("source/compiled-results.bin", native)]))
        self.assert_private_failure(self.run_scan(), marker, status=1)

    def test_unicode_text_members_stay_utf8_and_are_not_ascii_filtered(self):
        marker = "생성된" + "비밀문자열"
        text = "pass" + "word=" + json.dumps(marker, ensure_ascii=False)
        self.write("vendor/lib.tgz", archive_bytes([("source/settings.txt", text)]))
        self.assert_private_failure(self.run_scan(), marker, status=1)
