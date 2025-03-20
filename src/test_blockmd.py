import unittest

from blockmd import markdown_to_blocks


class TestInlineMd(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
  """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty_input(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_single_block(self):
        md = "Just one paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just one paragraph"])

    def test_markdown_to_blocks_multiple_newlines(self):
        md = """First paragraph


Second paragraph"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First paragraph", "Second paragraph"])

    def test_markdown_to_blocks_whitespace_only(self):
        md = """

        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_code_blocks(self):
        md = """Regular paragraph

```
code block
```
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Regular paragraph", "```\ncode block\n```"])
