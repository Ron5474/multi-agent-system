# tests/test_file_reader.py
import pytest
from pathlib import Path


def test_read_text_file(tmp_path):
    f = tmp_path / "notes.txt"
    f.write_text("hello world")
    from tools.file_reader import read_file
    assert read_file(str(f)) == "hello world"


def test_read_missing_file_returns_error():
    from tools.file_reader import read_file
    result = read_file("/nonexistent/file.txt")
    assert "not found" in result.lower()


def test_list_files_returns_all(tmp_path):
    (tmp_path / "a.txt").write_text("")
    (tmp_path / "b.txt").write_text("")
    (tmp_path / "c.pdf").write_text("")
    from tools.file_reader import list_files
    result = list_files(str(tmp_path))
    assert len(result) == 3


def test_list_files_filters_by_extension(tmp_path):
    (tmp_path / "a.txt").write_text("")
    (tmp_path / "b.pdf").write_text("")
    from tools.file_reader import list_files
    result = list_files(str(tmp_path), extension="txt")
    assert len(result) == 1
    assert result[0].endswith(".txt")


def test_list_files_missing_dir_returns_empty():
    from tools.file_reader import list_files
    assert list_files("/nonexistent/dir") == []
