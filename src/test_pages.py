import unittest

from pages import extract_title


class TestPages(unittest.TestCase):
    def test_extract_title(self):
        inp = "# My Blog Post\n\nThis is a blog post"
        self.assertEqual(extract_title(inp), "My Blog Post")

    def test_extract_title_with_multiple_lines(self):
        inp = "Some text\n# My Blog Post\n\nThis is a blog post"
        self.assertEqual(extract_title(inp), "My Blog Post")

    def test_extract_title_with_multiple_hashes(self):
        inp = "# My ## Blog Post\n\nThis is a blog post"
        self.assertEqual(extract_title(inp), "My ## Blog Post")

    def test_extract_title_no_title(self):
        inp = "This is a blog post without a title"
        with self.assertRaises(ValueError):
            extract_title(inp)


if __name__ == "__main__":
    unittest.main()
