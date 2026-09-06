"""tools/validate_document_links.py 회귀 시험: 상대 링크만 허용, 절대 링크 오류, 산문 오탐 제외."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "validate_document_links.py"
SPEC = importlib.util.spec_from_file_location("kor_travel_common_document_links", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class DocumentLinkValidation(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="kor-travel-common-links-test-")
        self.root = Path(self.temp.name)
        (self.root / "docs").mkdir()
        (self.root / "docs" / "target.md").write_text("# target\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write(self, name: str, body: str) -> None:
        (self.root / "docs" / name).write_text(body, encoding="utf-8")

    def test_relative_link_passes(self) -> None:
        self.write("a.md", "[t](target.md) [frag](target.md#절) [ext](https://example.com)\n")
        errors, documents, count = MODULE.validate(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(documents, 2)
        self.assertEqual(count, 2)

    def test_missing_target_fails(self) -> None:
        self.write("a.md", "[t](missing.md)\n")
        errors, _, _ = MODULE.validate(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("missing.md", errors[0])

    def test_absolute_link_is_error(self) -> None:
        self.write("a.md", "[w](F:/dev/kor-travel-common/docs/target.md) [l](/mnt/f/dev/x/docs/target.md)\n")
        errors, _, _ = MODULE.validate(self.root)
        self.assertEqual(len(errors), 2)
        self.assertTrue(all("절대 경로" in e for e in errors))

    def test_prose_bracket_paren_is_not_a_link(self) -> None:
        self.write("a.md", "어느 쪽이 이기는지는 [미확인](Tailwind 문서에서 찾지 못했다).\n")
        errors, _, count = MODULE.validate(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(count, 0)

    def test_fenced_block_is_ignored(self) -> None:
        self.write("a.md", "```md\n[x](missing.md)\n```\n")
        errors, _, count = MODULE.validate(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(count, 0)


if __name__ == "__main__":
    unittest.main()
