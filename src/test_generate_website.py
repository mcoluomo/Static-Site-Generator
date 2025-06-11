import tempfile
import unittest
from pathlib import Path

from generate_website import TitleNotFoundError, extract_title


class TestExtractTitle(unittest.TestCase):
    def write_temp_markdown(self, content):
        with tempfile.NamedTemporaryFile(
            delete=False,
            mode="w",
            encoding="utf-8",
            suffix=".md",
        ) as tmp:
            tmp.write(content)
            return tmp.name

    def test_valid_title(self):
        path = self.write_temp_markdown("# My Title")
        self.assertEqual(extract_title(path), "My Title")
        Path(path).unlink()

    def test_valid_title_with_trailing_space(self):
        path = self.write_temp_markdown("# My Title ")
        self.assertEqual(extract_title(path), "My Title ")
        Path(path).unlink()

    def test_title_with_special_characters(self):
        path = self.write_temp_markdown("# T!t1e @ 2025")
        self.assertEqual(extract_title(path), "T!t1e @ 2025")
        Path(path).unlink()

    def test_title_with_only_hash(self):
        path = self.write_temp_markdown("# ")
        self.assertEqual(extract_title(path), "")
        Path(path).unlink()

    def test_no_title(self):
        path = self.write_temp_markdown("No heading here")
        with self.assertRaises(TitleNotFoundError):
            extract_title(path)
        Path(path).unlink()

    def test_title_not_at_start(self):
        path = self.write_temp_markdown("Some text\n# Not a title")
        with self.assertRaises(TitleNotFoundError):
            extract_title(path)
        Path(path).unlink()

    def test_multiple_hashes(self):
        path = self.write_temp_markdown("## Subtitle")
        with self.assertRaises(TitleNotFoundError):
            extract_title(path)
        Path(path).unlink()

    def test_empty_string(self):
        path = self.write_temp_markdown("")
        with self.assertRaises(TitleNotFoundError):
            extract_title(path)
        Path(path).unlink()

    def test_whitespace_only(self):
        path = self.write_temp_markdown("   ")
        with self.assertRaises(TitleNotFoundError):
            extract_title(path)
        Path(path).unlink()


if __name__ == "__main__":
    unittest.main()
