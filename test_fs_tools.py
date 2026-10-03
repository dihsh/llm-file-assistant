"""
test_fs_tools.py - Unit test suite for fs_tools.py functions.
"""

import os
import shutil
import unittest
from pathlib import Path
from fs_tools import read_file, list_files, write_file, search_in_file

RESUMES_DIR = Path("resumes")
TEST_OUTPUT_DIR = Path("test_output")


class TestFSTools(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        TEST_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        if TEST_OUTPUT_DIR.exists():
            shutil.rmtree(TEST_OUTPUT_DIR, ignore_errors=True)

    # ------------------ read_file Tests ------------------
    def test_read_txt_file(self):
        res = read_file(str(RESUMES_DIR / "resume_alex_kumar.txt"))
        self.assertEqual(res["status"], "success")
        self.assertIn("Alex Kumar", res["content"])
        self.assertEqual(res["metadata"]["extension"], ".txt")
        self.assertGreater(res["metadata"]["size_bytes"], 0)
        self.assertIsNone(res["error"])

    def test_read_pdf_file(self):
        res = read_file(str(RESUMES_DIR / "resume_john_doe.pdf"))
        self.assertEqual(res["status"], "success")
        self.assertIn("John Doe", res["content"])
        self.assertEqual(res["metadata"]["extension"], ".pdf")
        self.assertGreaterEqual(res["metadata"]["page_count"], 1)
        self.assertIsNone(res["error"])

    def test_read_docx_file(self):
        res = read_file(str(RESUMES_DIR / "resume_jane_smith.docx"))
        self.assertEqual(res["status"], "success")
        self.assertIn("Jane Smith", res["content"])
        self.assertEqual(res["metadata"]["extension"], ".docx")
        self.assertIsNone(res["error"])

    def test_read_nonexistent_file(self):
        res = read_file("resumes/non_existent_file.pdf")
        self.assertEqual(res["status"], "error")
        self.assertIn("File not found", res["error"])
        self.assertEqual(res["content"], "")

    def test_read_unsupported_file_extension(self):
        dummy_bin = TEST_OUTPUT_DIR / "test.bin"
        dummy_bin.write_bytes(b"\x00\x01\x02\x03")
        res = read_file(str(dummy_bin))
        self.assertEqual(res["status"], "error")
        self.assertIn("Unsupported file extension", res["error"])

    # ------------------ list_files Tests ------------------
    def test_list_all_files(self):
        files = list_files(str(RESUMES_DIR))
        self.assertGreaterEqual(len(files), 8)
        names = [f["name"] for f in files]
        self.assertIn("resume_john_doe.pdf", names)
        self.assertIn("resume_jane_smith.docx", names)
        self.assertIn("resume_alex_kumar.txt", names)

    def test_list_files_filtered_pdf(self):
        files = list_files(str(RESUMES_DIR), extension=".pdf")
        self.assertGreater(len(files), 0)
        for f in files:
            self.assertEqual(f["extension"], ".pdf")

    def test_list_files_filtered_docx_without_dot(self):
        # Should work even if user supplies 'docx' instead of '.docx'
        files = list_files(str(RESUMES_DIR), extension="docx")
        self.assertGreater(len(files), 0)
        for f in files:
            self.assertEqual(f["extension"], ".docx")

    def test_list_files_nonexistent_directory(self):
        files = list_files("non_existent_directory_12345")
        self.assertEqual(files, [])

    # ------------------ write_file Tests ------------------
    def test_write_file_creates_parent_dirs(self):
        nested_file = TEST_OUTPUT_DIR / "nested" / "sub" / "output.txt"
        test_content = "Summary of John Doe's resume:\n- Senior Python Engineer\n- 7+ years experience"

        res = write_file(str(nested_file), test_content)
        self.assertEqual(res["status"], "success")
        self.assertGreater(res["bytes_written"], 0)
        self.assertTrue(nested_file.exists())
        self.assertEqual(nested_file.read_text(encoding="utf-8"), test_content)

    # ------------------ search_in_file Tests ------------------
    def test_search_in_file_found(self):
        res = search_in_file(str(RESUMES_DIR / "resume_john_doe.pdf"), "FastAPI")
        self.assertEqual(res["status"], "success")
        self.assertGreater(res["total_matches"], 0)
        self.assertTrue(any("FastAPI" in m["snippet"] or "fastapi" in m["snippet"].lower() for m in res["matches"]))

    def test_search_case_insensitivity(self):
        res_upper = search_in_file(str(RESUMES_DIR / "resume_alex_kumar.txt"), "PYTHON")
        res_lower = search_in_file(str(RESUMES_DIR / "resume_alex_kumar.txt"), "python")
        self.assertEqual(res_upper["status"], "success")
        self.assertEqual(res_lower["status"], "success")
        self.assertEqual(res_upper["total_matches"], res_lower["total_matches"])
        self.assertGreater(res_upper["total_matches"], 0)

    def test_search_keyword_not_found(self):
        res = search_in_file(str(RESUMES_DIR / "resume_sarah_patel.txt"), "NonExistentKeywordXYZ123")
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["total_matches"], 0)
        self.assertEqual(res["matches"], [])

    def test_search_empty_keyword(self):
        res = search_in_file(str(RESUMES_DIR / "resume_sarah_patel.txt"), "   ")
        self.assertEqual(res["status"], "error")
        self.assertEqual(res["total_matches"], 0)


if __name__ == "__main__":
    unittest.main()
