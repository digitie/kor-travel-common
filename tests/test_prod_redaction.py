# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""주소 guard의 대역·예약 호스트·조사 파일 검사를 검증한다."""

from test_scan_secrets import RepositoryCase, ROOT, archive_bytes, wasm_bytes


SCRIPT = ROOT / "tools/check_prod_redaction.py"


class ProdRedactionTests(RepositoryCase):
    def test_private_ranges_and_internal_hosts(self):
        values = ["10." + "2.3.4", "172." + "16.2.3", "172." + "31.2.3",
                  "192." + "168.1.2", "fd" + "12::1", "fe" + "80::1",
                  "database." + "internal", "service." + "corp"]
        for value in values:
            with self.subTest(value_type=value[:2]):
                self.write("docs/survey/sample.md", "연결: " + value + ". 다음 문장")
                result = self.run_scan(script=SCRIPT)
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertNotIn(value, result.stdout + result.stderr)

    def test_reserved_names_public_ranges_and_filenames(self):
        values = ["172." + "15.1.2", "172." + "32.1.2", "192." + "169.1.2",
                  "203." + "0.113.1", "127." + "0.0.1", "host.docker.internal",
                  "gateway.docker.internal", ".env.local", "notes.local.md",
                  "prod-guide.md", "<prod-host>", "192.168.*"]
        self.write("sample.txt", "\n".join(values))
        self.assertEqual(self.run_scan(script=SCRIPT).returncode, 0)

    def test_project_domain_shape_and_dynamic_dns(self):
        for value in ("weather-api." + "node.example.net", "demo." + "duckdns.org"):
            self.write("sample.txt", "https://" + value)
            self.assertEqual(self.run_scan(script=SCRIPT).returncode, 1)

    def test_staged_redaction_cannot_hide_previous_index_value(self):
        self.write("sample.txt", "192." + "168.1.2")
        self.git("add", "sample.txt")
        self.write("sample.txt", "<prod-address>")
        self.assertEqual(self.run_scan("--staged", script=SCRIPT).returncode, 1)
        self.assertEqual(self.run_scan("--all", script=SCRIPT).returncode, 0)

    def test_scope_limits_the_selected_files(self):
        self.write("docs/safe.md", "공개 문서")
        self.write("private/sample.txt", "192." + "168.1.2")
        scoped = self.run_scan("--all", "--scope", "docs/", script=SCRIPT)
        self.assertEqual(scoped.returncode, 0, scoped.stdout)
        outside = self.run_scan("--all", "--scope", "private", script=SCRIPT)
        self.assertEqual(outside.returncode, 1, outside.stdout)

    def test_nested_checkout_is_not_caller_input(self):
        self.git("init", "-q", "nested-checkout")
        self.write("nested-checkout/private.txt", "192." + "168.1.2")
        self.assertEqual(self.run_scan("--all", script=SCRIPT).returncode, 0)

    def test_sensitive_filename_and_parent_never_print(self):
        marker = "192." + "168.1.2"
        for name in (marker + ".txt", marker + "/sample.txt"):
            path = self.write(name, "안전한 본문")
            for content in ("안전한 본문", marker):
                path.write_text(content, encoding="utf-8")
                result = self.run_scan(script=SCRIPT)
                self.assertEqual(result.returncode, 2)
                self.assertNotIn(marker, result.stdout + result.stderr)
            path.unlink()


class ArchiveProdRedactionTests(RepositoryCase):
    def test_compressed_text_and_native_ascii_addresses_are_detected_privately(self):
        address = "192." + "168.7.9"
        for name, content in (("source.txt", ("연결 " + address).encode()),
                              ("engine.wasm", wasm_bytes(b"\0" + address.encode() + b"\0"))):
            nested = archive_bytes([(name, content)])
            self.write("vendor/lib.tgz", archive_bytes([("package/source.tar.gz", nested)]))
            result = self.run_scan("--all", script=SCRIPT)
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertNotIn(address, result.stdout + result.stderr)
            self.assertIn("PRIVATE-IPV4", result.stdout)
            if name.endswith(".wasm"):
                self.assertIn('"byte":', result.stdout)

    def test_production_member_name_is_never_disclosed(self):
        marker = "192." + "168.7.9"
        self.write("vendor/lib.tgz", archive_bytes([("package/" + marker + "/file.txt", "safe")]))
        result = self.run_scan(script=SCRIPT)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn(marker, result.stdout + result.stderr)

    def test_invalid_archive_does_not_disclose_native_string_or_traceback(self):
        marker = "192." + "168.7.9"
        self.write("vendor/lib.tgz", b"\x1f\x8b" + marker.encode())
        result = self.run_scan(script=SCRIPT)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn(marker, result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_plain_unknown_binary_remains_failure(self):
        self.write("unknown.data", b"\xff\xfe")
        self.assertEqual(self.run_scan(script=SCRIPT).returncode, 2)
