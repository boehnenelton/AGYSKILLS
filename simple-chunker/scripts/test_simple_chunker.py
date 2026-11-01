#!/data/data/com.termux/files/usr/bin/python3
"""
Unit tests for simple_chunker.py
"""

import base64
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest

from simple_chunker import (
    generate_quick_chunk_document,
    execute_quick_chunk_command,
    execute_unchunk_command,
    execute_inspect_chunk_info,
    execute_cat_file_content,
    create_bejson_field_map_cache,
)


class TestSimpleChunker(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.sample_dir = Path(self.test_dir) / "sample_project"
        self.sample_dir.mkdir(parents=True)
        (self.sample_dir / "main.py").write_text("print('hello world')\n", encoding="utf-8")
        (self.sample_dir / "notes.md").write_text("# Project Notes\nQuick chunk test.", encoding="utf-8")
        sub = self.sample_dir / "sub"
        sub.mkdir()
        (sub / "config.json").write_text('{"setting": "test"}', encoding="utf-8")

        # Binary file
        (self.sample_dir / "data.bin").write_bytes(b"\x00\x01\x02\x03\xff")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_chunk_basic_document(self):
        doc = generate_quick_chunk_document(self.sample_dir)
        self.assertEqual(doc["Format"], "BEJSON")
        self.assertEqual(doc["Format_Version"], "104a")
        self.assertEqual(doc["Schema_Name"], "Chunked-104a")
        fmap = create_bejson_field_map_cache(doc)
        self.assertIn("Relative_Path", fmap)
        self.assertIn("File_Content", fmap)

        rel_idx = fmap["Relative_Path"]
        paths = [r[rel_idx] for r in doc["Values"]]
        self.assertIn("main.py", paths)
        self.assertIn("notes.md", paths)
        self.assertIn(os.path.join("sub", "config.json"), paths)
        # Binary should be skipped by default
        self.assertNotIn("data.bin", paths)

    def test_chunk_with_binary_and_context(self):
        doc = generate_quick_chunk_document(
            self.sample_dir,
            chunk_context_instruction="Test context instruction",
            include_binary_files_flag=True,
        )
        fmap = create_bejson_field_map_cache(doc)
        rel_idx = fmap["Relative_Path"]
        paths = [r[rel_idx] for r in doc["Values"]]

        # First record must be context
        self.assertEqual(paths[0], "!-CONTEXT.txt")
        self.assertEqual(doc["Values"][0][fmap["File_Content"]], "Test context instruction")
        self.assertIn("data.bin", paths)

    def test_roundtrip_unchunk(self):
        out_chunk = Path(self.test_dir) / "output.104a.bejson.txt"
        exit_code = execute_quick_chunk_command(
            target_path=str(self.sample_dir),
            output_path=str(out_chunk),
            context_note="Roundtrip context note",
        )
        self.assertEqual(exit_code, 0)
        self.assertTrue(out_chunk.exists())

        restore_dir = Path(self.test_dir) / "restored"
        unchunk_exit = execute_unchunk_command(
            chunk_file_path=str(out_chunk),
            output_destination=str(restore_dir),
        )
        self.assertEqual(unchunk_exit, 0)
        self.assertTrue((restore_dir / "main.py").exists())
        self.assertEqual((restore_dir / "main.py").read_text(encoding="utf-8"), "print('hello world')\n")
        self.assertTrue((restore_dir / "sub" / "config.json").exists())

    def test_unchunk_to_zip(self):
        out_chunk = Path(self.test_dir) / "output.104a.bejson.txt"
        execute_quick_chunk_command(target_path=str(self.sample_dir), output_path=str(out_chunk))

        restore_dir = Path(self.test_dir) / "restored_zip"
        unchunk_exit = execute_unchunk_command(
            chunk_file_path=str(out_chunk),
            output_destination=str(restore_dir),
            zip_output_flag=True,
        )
        self.assertEqual(unchunk_exit, 0)
        zip_file = restore_dir.with_suffix(".zip")
        self.assertTrue(zip_file.exists())


if __name__ == "__main__":
    unittest.main()
