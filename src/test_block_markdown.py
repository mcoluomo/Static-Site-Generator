import unittest

from block_markdown import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)
from htmlnode import HTMLNode


class TestBloclMarkdown(unittest.TestCase):
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

    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_only_whitespace(self):
        self.assertEqual(markdown_to_blocks("   \n  \n\n  "), [])

    def test_single_block(self):
        self.assertEqual(markdown_to_blocks("A single block."), ["A single block."])

    def test_multiple_blocks_with_extra_newlines(self):
        md = """
Block one


Block two



Block three
"""
        self.assertEqual(
            markdown_to_blocks(md),
            ["Block one", "Block two", "Block three"],
        )

    def test_blocks_with_leading_and_trailing_newlines(self):
        md = """


First block

Second block


"""
        self.assertEqual(
            markdown_to_blocks(md),
            ["First block", "Second block"],
        )

    def test_blocks_with_only_newlines_between(self):
        md = "Block1\n\nBlock2\n\nBlock3"
        self.assertEqual(
            markdown_to_blocks(md),
            ["Block1", "Block2", "Block3"],
        )

    def test_blocks_with_mixed_whitespace(self):
        md = """
   Block one   \n\n   Block two\n\n   Block three   """
        self.assertEqual(
            markdown_to_blocks(md),
            ["Block one", "Block two", "Block three"],
        )

    def test_block_with_only_newlines(self):
        md = "\n\n\n"
        self.assertEqual(markdown_to_blocks(md), [])

    def test_block_with_tabs_and_spaces(self):
        md = "Block1\n\n  \t  \nBlock2"
        self.assertEqual(
            markdown_to_blocks(md),
            ["Block1", "Block2"],
        )

    def test_block_to_block_type_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        self.assertEqual(
            block_to_block_type("#Heading no space"),
            BlockType.PARAGRAPH,
        )  # Not a heading

    def test_block_to_block_type_code(self):
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)
        self.assertEqual(
            block_to_block_type("```python\nprint('hi')\n```"),
            BlockType.CODE,
        )
        self.assertEqual(
            block_to_block_type("``code``"),
            BlockType.PARAGRAPH,
        )  # Not a code block

    def test_block_to_block_type_quote(self):
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">> Nested quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(" >> Not a quote"), BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list(self):
        self.assertEqual(block_to_block_type("- item 1"), BlockType.ULIST)
        self.assertEqual(
            block_to_block_type("-item 2"),
            BlockType.PARAGRAPH,
        )  # No space after dash
        self.assertEqual(
            block_to_block_type(" - item 3"),
            BlockType.PARAGRAPH,
        )  # Leading space

    def test_block_to_block_type_ordered_list(self):
        self.assertEqual(block_to_block_type("1. First item"), BlockType.OLIST)
        self.assertEqual(block_to_block_type("10. Tenth item"), BlockType.OLIST)
        self.assertEqual(
            block_to_block_type("1.First item"),
            BlockType.PARAGRAPH,
        )  # No space after dot
        self.assertEqual(
            block_to_block_type("01. Leading zero"),
            BlockType.OLIST,
        )
        self.assertEqual(
            block_to_block_type("1 . Space before dot"),
            BlockType.PARAGRAPH,
        )

    def test_block_to_block_type_paragraph(self):
        self.assertEqual(
            block_to_block_type("Just a normal paragraph."),
            BlockType.PARAGRAPH,
        )
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("   "), BlockType.PARAGRAPH)
        self.assertEqual(
            block_to_block_type("Some text\nwith newlines"),
            BlockType.PARAGRAPH,
        )

    def test_paragraphs(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
