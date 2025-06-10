import unittest

from generate_website import TitleNotFoundError, extract_title


class TestExtractTitle(unittest.TestCase):
    def test_valid_title(self):
        self.assertEqual(extract_title("# My Title"), "My Title")

    def test_valid_title_with_trailing_space(self):
        self.assertEqual(extract_title("# My Title "), "My Title ")

    def test_title_with_special_characters(self):
        self.assertEqual(extract_title("# T!t1e @ 2025"), "T!t1e @ 2025")

    def test_title_with_only_hash(self):
        self.assertEqual(extract_title("# "), "")

    def test_no_title(self):
        with self.assertRaises(TitleNotFoundError):
            extract_title("No heading here")

    def test_title_not_at_start(self):
        with self.assertRaises(TitleNotFoundError):
            extract_title("Some text\n# Not a title")

    def test_multiple_hashes(self):
        with self.assertRaises(TitleNotFoundError):
            extract_title("## Subtitle")

    def test_empty_string(self):
        with self.assertRaises(TitleNotFoundError):
            extract_title("")

    def test_whitespace_only(self):
        with self.assertRaises(TitleNotFoundError):
            extract_title("   ")


if __name__ == "__main__":
    unittest.main()
