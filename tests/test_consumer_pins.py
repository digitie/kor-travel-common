# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""consumers.pins.json과 consumer_smoke 입력 경계 회귀 시험."""

from __future__ import annotations

import copy
import hashlib
import io
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
PINS_PATH = ROOT / "consumers.pins.json"
SCRIPT = ROOT / "tools" / "consumer_smoke.py"
SPEC = importlib.util.spec_from_file_location("kor_travel_common_consumer_smoke", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
SMOKE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = SMOKE
SPEC.loader.exec_module(SMOKE)


class ConsumerPinsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = json.loads(PINS_PATH.read_text(encoding="utf-8"))
        self.sources = SMOKE.validate_pins(self.data)
        self.temp = tempfile.TemporaryDirectory(prefix="kor-travel-common-consumer-smoke-")
        self.root = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)

    def make_tgz(self, name: str, *, engines: dict[str, str] | None = None,
                 dependencies: dict[str, str] | None = None,
                 license_name: str = "GPL-3.0-or-later",
                 repository: str = SMOKE.DEFAULT_ARTIFACT_REPOSITORY + ".git",
                 license_body: bytes | None = None,
                 include_notices: bool = True,
                 notice_body: bytes = b"kor-travel-common third-party notice.\n",
                 third_party_body: bytes = b"No bundled third-party notices.\n") -> Path:
        package = {
            "name": name,
            "version": "0.1.0",
            "license": license_name,
            "repository": {"type": "git", "url": repository},
        }
        if engines:
            package["engines"] = engines
        if dependencies:
            package["dependencies"] = dependencies
        path = self.root / (name.rsplit("/", 1)[-1] + ".tgz")
        with tarfile.open(path, "w:gz") as archive:
            body = json.dumps(package).encode("utf-8")
            info = tarfile.TarInfo("package/package.json")
            info.size = len(body)
            archive.addfile(info, io.BytesIO(body))
            index = b"module.exports = {};\n"
            info = tarfile.TarInfo("package/index.js")
            info.size = len(index)
            archive.addfile(info, io.BytesIO(index))
            if license_body is None:
                license_body = (ROOT / "LICENSE").read_bytes()
            info = tarfile.TarInfo("package/LICENSE")
            info.size = len(license_body)
            archive.addfile(info, io.BytesIO(license_body))
            if include_notices:
                info = tarfile.TarInfo("package/NOTICE")
                info.size = len(notice_body)
                archive.addfile(info, io.BytesIO(notice_body))
                info = tarfile.TarInfo("package/THIRD_PARTY_NOTICES.md")
                info.size = len(third_party_body)
                archive.addfile(info, io.BytesIO(third_party_body))
        return path

    def digest(self, path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def test_registry_schema_sha_approval_and_no_pinvi(self):
        self.assertEqual(self.data["schema"], SMOKE.SCHEMA)
        self.assertEqual({entry["role"] for entry in self.sources},
                         {"map-tokens", "weather-tokens", "map-ui", "airport-ui"})
        self.assertTrue(all(len(entry["revision"]) == 40 for entry in self.sources))
        self.assertTrue(all(entry["approval"]["status"] == "approved" for entry in self.sources))
        self.assertTrue(all("pinvi" not in entry["url"] for entry in self.sources))

    def test_registry_rejects_short_sha_and_unapproved_pin(self):
        mutated = copy.deepcopy(self.data)
        mutated["sources"][0]["revision"] = "c494e22"
        with self.assertRaises(SMOKE.SmokeInputError):
            SMOKE.validate_pins(mutated)
        mutated = copy.deepcopy(self.data)
        mutated["sources"][0]["approval"]["status"] = "pending"
        with self.assertRaises(SMOKE.SmokeInputError):
            SMOKE.validate_pins(mutated)

    def test_asset_url_rejects_branch_and_non_github_url(self):
        with self.assertRaises(SMOKE.SmokeInputError):
            SMOKE.validate_asset_url("https://github.com/digitie/kor-travel-map/archive/main.tgz")
        with self.assertRaises(SMOKE.SmokeInputError):
            SMOKE.validate_asset_url("https://example.invalid/candidate.tgz")

    def test_normal_tarball_digest_metadata_and_actual_npm_install(self):
        package = "@kor-travel/tokens"
        tarball = self.make_tgz(package)
        digest = self.digest(tarball)
        self.assertEqual(SMOKE.validate_asset(
            tarball, digest, package, SMOKE.DEFAULT_ARTIFACT_REPOSITORY), digest)
        npm = shutil.which("npm")
        if npm is None:
            self.fail("npm이 없어 정상 tarball 설치 gate를 실행할 수 없음")
        app = self.root / "normal-install"
        app.mkdir()
        (app / "package.json").write_text('{"name":"fixture","private":true}\n', encoding="utf-8")
        result = subprocess.run([
            npm, "install", "--ignore-scripts", "--offline", "--no-audit", "--fund=false",
            "--package-lock=false", "--no-save", str(tarball),
        ], cwd=app, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr[-2000:])
        self.assertTrue((app / "node_modules" / "@kor-travel" / "tokens" / "package.json").is_file())

    def test_digest_mismatch_and_missing_asset_fail(self):
        package = "@kor-travel/tokens"
        tarball = self.make_tgz(package)
        with self.assertRaises(SMOKE.SmokeInputError):
            SMOKE.validate_asset(tarball, "0" * 64, package,
                                 SMOKE.DEFAULT_ARTIFACT_REPOSITORY)
        with self.assertRaises(SMOKE.SmokeInputError):
            SMOKE.validate_asset(self.root / "missing.tgz", "0" * 64, package,
                                 SMOKE.DEFAULT_ARTIFACT_REPOSITORY)

    def test_asset_file_and_metadata_limits_are_enforced(self):
        package = "@kor-travel/tokens"
        tarball = self.make_tgz(package)
        digest = self.digest(tarball)
        with mock.patch.object(SMOKE, "MAX_ASSET_BYTES", 1):
            with self.assertRaises(SMOKE.SmokeInputError):
                SMOKE.validate_asset(tarball, digest, package,
                                     SMOKE.DEFAULT_ARTIFACT_REPOSITORY)
        with mock.patch.object(SMOKE, "MAX_METADATA_BYTES", 1):
            with self.assertRaises(SMOKE.SmokeInputError):
                SMOKE.validate_asset(tarball, digest, package,
                                     SMOKE.DEFAULT_ARTIFACT_REPOSITORY)
        link = self.root / "asset-link.tgz"
        try:
            link.symlink_to(tarball)
        except OSError:
            return
        with self.assertRaises(SMOKE.SmokeInputError):
            SMOKE.validate_asset(link, digest, package,
                                 SMOKE.DEFAULT_ARTIFACT_REPOSITORY)

    def test_invalid_tarball_install_is_a_real_failure(self):
        package = "@kor-travel/tokens"
        tarball = self.make_tgz(package, engines={"node": ">=999.0.0"})
        digest = self.digest(tarball)
        self.assertEqual(SMOKE.validate_asset(
            tarball, digest, package, SMOKE.DEFAULT_ARTIFACT_REPOSITORY), digest)
        npm = shutil.which("npm")
        if npm is None:
            self.fail("npm이 없어 설치 실패 gate를 실행할 수 없음")
        app = self.root / "failed-install"
        app.mkdir()
        (app / "package.json").write_text('{"name":"fixture","private":true}\n', encoding="utf-8")
        result = subprocess.run([
            npm, "install", "--ignore-scripts", "--offline", "--no-audit", "--fund=false",
            "--engine-strict", "--package-lock=false", "--no-save", str(tarball),
        ], cwd=app, capture_output=True, text=True, encoding="utf-8")
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_asset_url_and_metadata_are_bound_to_common_artifact_repository(self):
        package = "@kor-travel/tokens"
        tarball = self.make_tgz(package)
        digest = self.digest(tarball)
        self.assertEqual(SMOKE.validate_asset_url(
            "https://github.com/digitie/kor-travel-common/releases/download/tokens-v0.1.0/kor-travel-tokens-0.1.0.tgz",
            SMOKE.DEFAULT_ARTIFACT_REPOSITORY),
            "https://github.com/digitie/kor-travel-common/releases/download/tokens-v0.1.0/kor-travel-tokens-0.1.0.tgz")
        with self.assertRaises(SMOKE.SmokeInputError):
            SMOKE.validate_asset_url(
                "https://github.com/digitie/kor-travel-map/releases/download/tokens-v0.1.0/kor-travel-tokens-0.1.0.tgz",
                SMOKE.DEFAULT_ARTIFACT_REPOSITORY)
        with self.assertRaises(SMOKE.SmokeInputError):
            bad_license = self.make_tgz(package, license_name="MIT")
            SMOKE.validate_asset(bad_license, self.digest(bad_license), package,
                                 SMOKE.DEFAULT_ARTIFACT_REPOSITORY)

    def test_archive_requires_canonical_gpl_and_nonempty_notices(self):
        package = "@kor-travel/tokens"
        for kwargs in (
                {"license_body": b"MIT License\n"},
                {"include_notices": False},
                {"notice_body": b""},
                {"third_party_body": b""}):
            with self.subTest(kwargs=kwargs):
                tarball = self.make_tgz(package, **kwargs)
                with self.assertRaises(SMOKE.SmokeInputError):
                    SMOKE.validate_asset(tarball, self.digest(tarball), package)

    def test_archive_links_are_rejected(self):
        package = "@kor-travel/tokens"
        path = self.root / "link.tgz"
        with tarfile.open(path, "w:gz") as archive:
            body = b'{"name":"@kor-travel/tokens","version":"0.1.0","license":"GPL-3.0-or-later","repository":{"url":"https://github.com/digitie/kor-travel-common"}}'
            info = tarfile.TarInfo("package/package.json")
            info.size = len(body)
            archive.addfile(info, io.BytesIO(body))
            info = tarfile.TarInfo("package/LICENSE")
            info.size = 3
            archive.addfile(info, io.BytesIO(b"GPL"))
            link = tarfile.TarInfo("package/link")
            link.type = tarfile.SYMTYPE
            link.linkname = "../../outside"
            archive.addfile(link)
        with self.assertRaises(SMOKE.SmokeInputError):
            SMOKE.validate_asset(path, self.digest(path), package,
                                 SMOKE.DEFAULT_ARTIFACT_REPOSITORY)


if __name__ == "__main__":
    unittest.main()
