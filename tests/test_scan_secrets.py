# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""비밀 검사기의 스냅샷 선택·값 비공개·입력 실패를 검증한다."""

from pathlib import Path
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
