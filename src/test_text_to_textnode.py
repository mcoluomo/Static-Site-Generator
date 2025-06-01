import unittest

from text_to_textnode import text_to_textnodes
from textnode import TextNode, TextType


class TestTextToTextnodeEdgeCases(unittest.TestCase):
    def test_text_to_textnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image",
                    TextType.IMAGE,
                    "https://i.imgur.com/fJRm4Vk.jpeg",
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )


    def test_plain_text_only(self):
        text = "Just plain text"
        self.assertListEqual(
            text_to_textnodes(text),
            [TextNode("Just plain text", TextType.TEXT)],
        )

    def test_single_bold(self):
        text = "This is **bold** text"
        self.assertListEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_single_italic(self):
        text = "This is _italic_ text"
        self.assertListEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_single_code(self):
        text = "This is `code` text"
        self.assertListEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_multiple_formatting_types(self):
        text = "**bold** and _italic_ and `code`"
        self.assertListEqual(
            text_to_textnodes(text),
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
        )

    def test_formatting_at_start_end(self):
        self.assertListEqual(
            text_to_textnodes("**bold** text"),
            [TextNode("bold", TextType.BOLD), TextNode(" text", TextType.TEXT)],
        )
        self.assertListEqual(
            text_to_textnodes("text **bold**"),
            [TextNode("text ", TextType.TEXT), TextNode("bold", TextType.BOLD)],
        )
        self.assertListEqual(
            text_to_textnodes("**bold**"),
            [TextNode("bold", TextType.BOLD)],
        )
        self.assertListEqual(
            text_to_textnodes("`code`"),
            [TextNode("code", TextType.CODE)],
        )
        self.assertListEqual(
            text_to_textnodes("_italic_"),
            [TextNode("italic", TextType.ITALIC)],
        )

    def test_multiple_same_formatting(self):
        self.assertListEqual(
            text_to_textnodes("**a** **b**"),
            [
                TextNode("a", TextType.BOLD),
                TextNode("b", TextType.BOLD),
            ],
        )
        self.assertListEqual(
            text_to_textnodes("`a` `b`"),
            [
                TextNode("a", TextType.CODE),
                TextNode("b", TextType.CODE),
            ],
        )
        self.assertListEqual(
            text_to_textnodes("_a_ _b_"),
            [
                TextNode("a", TextType.ITALIC),
                TextNode("b", TextType.ITALIC),
            ],
        )

    def test_unclosed_formatting(self):
        with self.assertRaises(ValueError):
            text_to_textnodes("**bold")

        with self.assertRaises(ValueError):
            text_to_textnodes("`code")

        with self.assertRaises(ValueError):
            text_to_textnodes("_italic")

    def test_empty_formatting(self):
        self.assertListEqual(
            text_to_textnodes("****"),
            [TextNode("****", TextType.TEXT)],
        )
        self.assertListEqual(
            text_to_textnodes("``"),
            [TextNode("``", TextType.TEXT)],
        )
        self.assertListEqual(
            text_to_textnodes("__"),
            [TextNode("__", TextType.TEXT)],
        )

    def test_images(self):
        self.assertListEqual(
            text_to_textnodes("![alt](url)"),
            [TextNode("alt", TextType.IMAGE, "url")],
        )
        self.assertListEqual(
            text_to_textnodes("Text ![alt](url) more"),
            [
                TextNode("Text ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "url"),
                TextNode(" more", TextType.TEXT),
            ],
        )
        self.assertListEqual(
            text_to_textnodes("![alt1](url1) ![alt2](url2)"),
            [
                TextNode("alt1", TextType.IMAGE, "url1"),
                TextNode("alt2", TextType.IMAGE, "url2"),
            ],
        )

    def test_links(self):
        self.assertListEqual(
            text_to_textnodes("[text](url)"),
            [TextNode("text", TextType.LINK, "url")],
        )
        self.assertListEqual(
            text_to_textnodes("Text [text](url) more"),
            [
                TextNode("Text ", TextType.TEXT),
                TextNode("text", TextType.LINK, "url"),
                TextNode(" more", TextType.TEXT),
            ],
        )
        self.assertListEqual(
            text_to_textnodes("[a](1) [b](2)"),
            [
                TextNode("a", TextType.LINK, "1"),
                TextNode("b", TextType.LINK, "2"),
            ],
        )

    def test_images_and_links_mixed(self):
        self.assertListEqual(
            text_to_textnodes("![alt](img) and [text](url)"),
            [
                TextNode("alt", TextType.IMAGE, "img"),
                TextNode(" and ", TextType.TEXT),
                TextNode("text", TextType.LINK, "url"),
            ],
        )

    def test_formatting_images_links_mixed(self):
        self.assertListEqual(
            text_to_textnodes("**bold** _italic_ `code` ![alt](img) [text](url)"),
            [
                TextNode("bold", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
                TextNode("code", TextType.CODE),
                TextNode("alt", TextType.IMAGE, "img"),
                TextNode("text", TextType.LINK, "url"),
            ],
        )

    def test_whitespace_and_empty_string(self):
        self.assertListEqual(
            text_to_textnodes(""),
            [],
        )
        self.assertListEqual(
            text_to_textnodes("   "),
            [],
        )
        self.assertListEqual(
            text_to_textnodes(" **bold** "),
            [
                TextNode("bold", TextType.BOLD),
            ],
        )
        self.assertListEqual(
            text_to_textnodes(" [text](url) "),
            [
                TextNode("text", TextType.LINK, "url"),
            ],
        )

    def test_malformed_markdown(self):
        self.assertListEqual(
            text_to_textnodes("![alt](url"),
            [TextNode("![alt](url", TextType.TEXT)],
        )
        self.assertListEqual(
            text_to_textnodes("[text](url"),
            [TextNode("[text](url", TextType.TEXT)],
        )

        with self.assertRaises(ValueError):
            text_to_textnodes("`code")

        with self.assertRaises(ValueError):
            text_to_textnodes("**bold")

    def test_adjacent_formatting_images_links(self):
        self.assertListEqual(
            text_to_textnodes("**a****b**"),
            [TextNode("a", TextType.BOLD), TextNode("b", TextType.BOLD)],
        )
        self.assertListEqual(
            text_to_textnodes("`a``b`"),
            [TextNode("a", TextType.CODE), TextNode("b", TextType.CODE)],
        )
        self.assertListEqual(
            text_to_textnodes("![a](1)![b](2)"),
            [TextNode("a", TextType.IMAGE, "1"), TextNode("b", TextType.IMAGE, "2")],
        )
        self.assertListEqual(
            text_to_textnodes("[a](1)[b](2)"),
            [TextNode("a", TextType.LINK, "1"), TextNode("b", TextType.LINK, "2")],
        )

    def test_formatting_inside_images_links(self):
        self.assertListEqual(
            text_to_textnodes("![**alt**](url)"),
            [TextNode("**alt**", TextType.IMAGE, "url")],
        )
        self.assertListEqual(
            text_to_textnodes("[_text_](url)"),
            [TextNode("_text_", TextType.LINK, "url")],
        )

    def test_multiple_lines(self):
        self.assertListEqual(
            text_to_textnodes("Line 1\n**bold**\nLine 3"),
            [
                TextNode("Line 1\n", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode("\nLine 3", TextType.TEXT),
            ],
        )

    def test_unicode_and_special_characters(self):
        self.assertListEqual(
            text_to_textnodes("**böld** _itälïc_ [lïnk](ürl) ![îmg](ürl)"),
            [
                TextNode("böld", TextType.BOLD),
                TextNode("itälïc", TextType.ITALIC),
                TextNode("lïnk", TextType.LINK, "ürl"),
                TextNode("îmg", TextType.IMAGE, "ürl"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
