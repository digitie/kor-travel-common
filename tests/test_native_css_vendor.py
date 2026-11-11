# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)

"""공통 CSS 산출물의 실제 bytes·고지·공개 source 동봉 계약을 검사한다."""
import base64
import hashlib
import io
import json
from pathlib import Path
import tarfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class NativeCssVendorTests(unittest.TestCase):
    def test_canonical_vendor_version_and_bytes(self):
        registry = json.loads((ROOT / "versions.json").read_text())
        artifact = json.loads((ROOT / "frontend-artifacts.json").read_text())["packages"]["lightningcss"]
        self.assertEqual(artifact["version"], registry["axes"]["lightningcss"]["exact"])
        data = (ROOT / "vendor" / artifact["filename"]).read_bytes()
        self.assertEqual(artifact["integrity"], "sha512-" + base64.b64encode(hashlib.sha512(data).digest()).decode())

    def test_pack_preserves_licenses_and_modified_source(self):
        artifact = json.loads((ROOT / "frontend-artifacts.json").read_text())["packages"]["lightningcss"]
        with tarfile.open(ROOT / "vendor" / artifact["filename"]) as package:
            names = package.getnames()
            metadata = json.load(package.extractfile("package/package.json"))
            provenance = json.load(package.extractfile("package/NATIVE-FIX-PROVENANCE.json"))
            self.assertEqual(metadata["version"], artifact["version"])
            self.assertEqual(metadata["license"], "MPL-2.0")
            self.assertFalse(any(field in metadata for field in ("os", "cpu", "libc")))
            self.assertEqual(package.extractfile("package/LICENSE").read(),
                             (ROOT / "LICENSES/upstream/lightningcss-1.33.0.txt").read_bytes())
            self.assertEqual(provenance, json.loads((ROOT / "vendor/lightningcss-provenance.json").read_text()))
            notice = package.extractfile("package/wasm/NAPI-WASM-NOTICE").read().decode()
            self.assertIn("MIT", notice)
            self.assertIn("Devon Govett", notice)
            self.assertIn("upstream npm package", notice)
            source = package.extractfile("package/native-source.tar.gz").read()
            self.assertEqual(hashlib.sha256(source).hexdigest(), provenance["sourceSHA256"])
            for path, key in (("package/lightningcss.linux-x64-gnu.node", "binarySHA256"),
                              ("package/wasm/lightningcss_node.wasm", "wasmSHA256")):
                self.assertEqual(hashlib.sha256(package.extractfile(path).read()).hexdigest(), provenance[key])
        with tarfile.open(fileobj=io.BytesIO(source)) as archive:
            members = archive.getnames()
            for name in ("LICENSE", "Cargo.lock", "vendor/serde-content/LICENSE-MIT",
                         "vendor/serde-content/LICENSE-APACHE", "vendor/serde-content/UPSTREAM.md"):
                self.assertIn(name, members)
            self.assertFalse(any(name.endswith("pinvi-native-postcss.css") for name in members))
        self.assertEqual(len([name for name in names if name.endswith(".node")]), 1)
        self.assertEqual(len([name for name in names if name.endswith(".wasm")]), 1)


if __name__ == "__main__":
    unittest.main()
