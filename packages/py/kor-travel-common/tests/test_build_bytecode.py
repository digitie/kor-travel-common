# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
"""실제 stdlib 대신 작은 전용 디렉터리에서 빌드 경계를 검증한다."""

import dis
import importlib.util
import marshal
import os
import py_compile
import struct
import subprocess
import sys
from pathlib import Path

import pytest

from kortravelcommon import build_bytecode


@pytest.fixture
def stdlib(tmp_path, monkeypatch):
    root = tmp_path / "stdlib"
    root.mkdir()
    (root / "sample.py").write_text('"""보존할 docstring."""\nVALUE = 1\nassert VALUE\n')
    monkeypatch.setattr(build_bytecode.sysconfig, "get_path", lambda name: str(root))
    monkeypatch.setattr(sys, "pycache_prefix", None)
    return root


def cache(source):
    return Path(importlib.util.cache_from_source(str(source), optimization=""))


def test_checked_hash_optimize_zero_and_environment_unchanged(stdlib, monkeypatch):
    before = dict(os.environ)
    monkeypatch.setattr(sys, "dont_write_bytecode", True)
    assert build_bytecode.main(["--stdlib"]) == 0
    raw = cache(stdlib / "sample.py").read_bytes()
    assert raw[:4] == importlib.util.MAGIC_NUMBER
    assert struct.unpack("<I", raw[4:8])[0] == 3
    assert raw[8:16] == importlib.util.source_hash((stdlib / "sample.py").read_bytes())
    code = marshal.loads(raw[16:])
    assert code.co_consts[0] == "보존할 docstring."
    assert any(i.opname == "LOAD_ASSERTION_ERROR" for i in dis.get_instructions(code))
    assert sys.dont_write_bytecode is True
    assert os.environ == before


def test_compileall_parameters_single_worker(stdlib, monkeypatch):
    calls = []
    monkeypatch.setattr(
        build_bytecode.compileall,
        "compile_dir",
        lambda *args, **kwargs: calls.append((args, kwargs)) or True,
    )
    assert build_bytecode.main(["--stdlib"]) == 0
    args, kwargs = calls[0]
    assert args == (str(stdlib),)
    assert kwargs["workers"] == 1
    assert kwargs["force"] is True
    assert kwargs["optimize"] == 0
    assert kwargs["invalidation_mode"] is py_compile.PycInvalidationMode.CHECKED_HASH
    assert kwargs["limit_sl_dest"] == str(stdlib)


def test_old_timestamp_cache_is_replaced_with_checked_hash(stdlib):
    source = stdlib / "sample.py"
    py_compile.compile(str(source), invalidation_mode=py_compile.PycInvalidationMode.TIMESTAMP)
    assert struct.unpack("<I", cache(source).read_bytes()[4:8])[0] == 0
    assert build_bytecode.main(["--stdlib"]) == 0
    assert struct.unpack("<I", cache(source).read_bytes()[4:8])[0] == 3


def test_source_change_same_size_mtime_invalidates_hash(stdlib):
    source = stdlib / "sample.py"
    assert build_bytecode.main(["--stdlib"]) == 0
    raw = cache(source).read_bytes()
    before = source.stat()
    source.write_text(source.read_text().replace("VALUE = 1", "VALUE = 2"))
    os.utime(source, ns=(before.st_atime_ns, before.st_mtime_ns))
    child = subprocess.run(
        [
            sys.executable, "-I", "-B", "-c",
            "import sys;sys.path.insert(0,sys.argv[1]);import sample;assert sample.VALUE == 2",
            str(stdlib),
        ],
        capture_output=True, timeout=10,
    )
    assert child.returncode == 0, child.stderr
    assert cache(source).read_bytes() == raw


@pytest.mark.parametrize(
    "excluded", ["site-packages", "dist-packages", "test", "tests", "idle_test"]
)
def test_excludes_nested_packages_and_test_trees(stdlib, excluded):
    target = stdlib / "nested" / excluded
    target.mkdir(parents=True)
    (target / "invalid.py").write_text("syntax error =")
    assert build_bytecode.main(["--stdlib"]) == 0
    assert not (target / "__pycache__").exists()
    assert cache(stdlib / "sample.py").exists()


def test_compile_failure_is_nonzero_not_silently_passed(stdlib, capsys):
    (stdlib / "bad.py").write_text("invalid =")
    assert build_bytecode.main(["--stdlib"]) == 1
    captured = capsys.readouterr()
    assert captured.err == "표준 라이브러리 bytecode 준비에 실패했습니다.\n"
    assert captured.out == ""


def test_compileall_false_is_nonzero(stdlib, monkeypatch):
    monkeypatch.setattr(build_bytecode.compileall, "compile_dir", lambda *a, **k: False)
    assert build_bytecode.main(["--stdlib"]) == 1


@pytest.mark.parametrize("args", [[], ["--stdlib", "/tmp"], ["--stdlib", "--path", "/tmp"]])
def test_no_arbitrary_source_path_or_default_action(args, monkeypatch):
    monkeypatch.setattr(
        build_bytecode, "_compile_stdlib", lambda: pytest.fail("명시하지 않은 컴파일")
    )
    with pytest.raises(SystemExit) as error:
        build_bytecode.main(args)
    assert error.value.code == 2


def test_missing_or_empty_stdlib_is_nonzero(stdlib):
    (stdlib / "sample.py").unlink()
    assert build_bytecode.main(["--stdlib"]) == 1


def test_invalid_stdlib_path_is_nonzero(stdlib, monkeypatch):
    monkeypatch.setattr(build_bytecode.sysconfig, "get_path", lambda name: str(stdlib / "missing"))
    assert build_bytecode.main(["--stdlib"]) == 1


def test_stdlib_file_is_nonzero(stdlib, monkeypatch):
    monkeypatch.setattr(
        build_bytecode.sysconfig, "get_path", lambda name: str(stdlib / "sample.py")
    )
    assert build_bytecode.main(["--stdlib"]) == 1


def test_symlinked_outside_source_and_directory_are_not_compiled(stdlib, tmp_path):
    outside = tmp_path / "stdlib-lookalike"
    outside.mkdir()
    (outside / "external.py").write_text("VALUE = 7")
    (stdlib / "link.py").symlink_to(outside / "external.py")
    (stdlib / "linked_dir").symlink_to(outside, target_is_directory=True)
    assert build_bytecode.main(["--stdlib"]) == 0
    assert not cache(stdlib / "link.py").exists()
    assert not (outside / "__pycache__").exists()


def test_internal_source_symlink_stays_inside_scope(stdlib):
    (stdlib / "link.py").symlink_to(stdlib / "sample.py")
    assert build_bytecode.main(["--stdlib"]) == 0
    assert cache(stdlib / "link.py").is_file()


def test_external_cache_directory_link_rejected_before_any_compile(stdlib, tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    (stdlib / "__pycache__").symlink_to(outside, target_is_directory=True)
    assert build_bytecode.main(["--stdlib"]) == 1
    assert list(outside.iterdir()) == []


def test_existing_cache_file_symlink_is_rejected(stdlib, tmp_path):
    target = tmp_path / "sentinel"
    target.write_bytes(b"unchanged")
    cache(stdlib / "sample.py").parent.mkdir()
    cache(stdlib / "sample.py").symlink_to(target)
    assert build_bytecode.main(["--stdlib"]) == 1
    assert target.read_bytes() == b"unchanged"


def test_external_pycache_prefix_is_rejected_without_environment_change(
    stdlib, tmp_path, monkeypatch
):
    prefix = tmp_path / "redirect"
    monkeypatch.setattr(sys, "pycache_prefix", str(prefix))
    assert build_bytecode.main(["--stdlib"]) == 1
    assert sys.pycache_prefix == str(prefix)
    assert not prefix.exists()


@pytest.mark.skipif(not hasattr(os, "geteuid") or os.geteuid() == 0, reason="비root 권한 경계")
def test_nonroot_readonly_stdlib_fails(stdlib):
    stdlib.chmod(0o555)
    try:
        assert build_bytecode.main(["--stdlib"]) == 1
        assert not cache(stdlib / "sample.py").exists()
    finally:
        stdlib.chmod(0o755)


@pytest.mark.skipif(not hasattr(os, "geteuid") or os.geteuid() == 0, reason="비root 권한 경계")
def test_nonroot_unreadable_subdirectory_is_not_silently_skipped(stdlib):
    hidden = stdlib / "hidden"
    hidden.mkdir()
    (hidden / "hidden.py").write_text("VALUE = 1")
    hidden.chmod(0o000)
    try:
        assert build_bytecode.main(["--stdlib"]) == 1
        assert not cache(stdlib / "sample.py").exists()
    finally:
        hidden.chmod(0o755)


def test_import_is_opt_in_and_core_only():
    child = subprocess.run(
        [
            sys.executable, "-I", "-B", "-c",
            "import sys;sys.path.insert(0,sys.argv[1]);"
            "import kortravelcommon.build_bytecode;"
            "assert not any(n.split('.')[0] in {'dagster','sqlalchemy','grpc'} "
            "for n in sys.modules)",
            str(Path(build_bytecode.__file__).parents[1]),
        ],
        capture_output=True, timeout=10,
    )
    assert child.returncode == 0, child.stderr
