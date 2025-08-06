import os
import tempfile
from unittest.mock import patch

from ...tools.file_tools import (
    list_local_text_files,
    read_local_text_file,
    append_note_to_text_file,
)


class TestFileTools:
    def test_list_local_text_files(self):
        with tempfile.TemporaryDirectory() as test_dir:
            with patch.dict("os.environ", {"FILE_TOOLS_TARGET_DIR": test_dir}):
                test_filename = "test_note.txt"
                test_note = "Test note content"
                test_file_path = os.path.join(test_dir, test_filename)
                with open(test_file_path, "w", encoding="utf-8") as f:
                    f.write(test_note)
                result = list_local_text_files.invoke({})
                assert test_filename in result

    def test_list_local_text_files_but_none_exist(self):
        with tempfile.TemporaryDirectory() as test_dir:
            with patch.dict("os.environ", {"FILE_TOOLS_TARGET_DIR": test_dir}):
                result = list_local_text_files.invoke({})
                assert "No text files found in target directory." in result

    def test_list_local_text_files_if_directory_does_not_exist(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            new_subdirectory = os.path.join(temp_dir, "new_subdir")
            with patch.dict("os.environ", {"FILE_TOOLS_TARGET_DIR": new_subdirectory}):
                result = list_local_text_files.invoke({})
                assert "No text files" in result

    def test_read_local_text_file_nonexistent(self):
        with tempfile.TemporaryDirectory() as test_dir:
            with patch.dict("os.environ", {"FILE_TOOLS_TARGET_DIR": test_dir}):
                result = read_local_text_file.invoke({"filename": "nonexistent.txt"})
                assert "error" in result.lower() or "not found" in result.lower()

    def test_read_local_text_file(self):
        with tempfile.TemporaryDirectory() as test_dir:
            with patch.dict("os.environ", {"FILE_TOOLS_TARGET_DIR": test_dir}):
                test_filename = "test_note"
                test_content = "This is a test file"
                test_file_path = os.path.join(test_dir, test_filename + ".txt")
                with open(test_file_path, "w", encoding="utf-8") as f:
                    f.write(test_content)
                result = read_local_text_file.invoke({"filename": test_filename})
                assert test_content in result

    def test_read_local_text_file_but_it_is_empty(self):
        with tempfile.TemporaryDirectory() as test_dir:
            with patch.dict("os.environ", {"FILE_TOOLS_TARGET_DIR": test_dir}):
                test_filename = "test_note.txt"
                test_file_path = os.path.join(test_dir, test_filename)
                open(test_file_path, "w").close()
                result = read_local_text_file.invoke({"filename": test_filename})
                assert "empty" in result.lower()

    def test_append_note_to_new_text_file(self):
        with tempfile.TemporaryDirectory() as test_dir:
            with patch.dict("os.environ", {"FILE_TOOLS_TARGET_DIR": test_dir}):
                test_filename = "test_note.txt"
                test_note = "Test note content"
                test_file_path = os.path.join(test_dir, test_filename)
                result = append_note_to_text_file.invoke(
                    {"filename": test_filename, "note": test_note}
                )
                assert "success" in result.lower() or "appended" in result.lower()
                assert os.path.exists(test_file_path)
                with open(test_file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()
                    assert test_note in file_content

    def test_append_note_to_existing_file(self):
        with tempfile.TemporaryDirectory() as test_dir:
            with patch.dict("os.environ", {"FILE_TOOLS_TARGET_DIR": test_dir}):
                test_filename = "test_existing_note.txt"
                original_content = "Original file content"
                new_note = "New note to append"
                test_file_path = os.path.join(test_dir, test_filename)
                with open(test_file_path, "w", encoding="utf-8") as f:
                    f.write(original_content)
                result = append_note_to_text_file.invoke(
                    {"filename": test_filename, "note": new_note}
                )
                assert "success" in result.lower() or "appended" in result.lower()
                assert os.path.exists(test_file_path)
                with open(test_file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()
                    assert original_content in file_content
                    assert new_note in file_content
                    assert file_content.endswith(f"{new_note}\n")

    @patch.dict("os.environ", {}, clear=True)
    def test_list_local_text_files_missing_environment_variable(self):
        result = list_local_text_files.invoke({})
        assert "FILE_TOOLS_TARGET_DIR" in result
        assert "not set" in result.lower()

    @patch.dict("os.environ", {}, clear=True)
    def test_read_local_text_file_missing_environment_variable(self):
        result = read_local_text_file.invoke({"filename": "test_note.txt"})
        assert "FILE_TOOLS_TARGET_DIR" in result
        assert "not set" in result.lower()

    @patch.dict("os.environ", {}, clear=True)
    def test_append_note_to_text_file_missing_environment_variable(self):
        result = append_note_to_text_file.invoke(
            {"filename": "test_note.txt", "note": "Test note content"}
        )
        assert "FILE_TOOLS_TARGET_DIR" in result
        assert "not set" in result.lower()
