import unittest

from inline_markdown import (
    extracted_image,
    extracted_link,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_delimiter(self):
        node = TextNode("This is a test", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], node)

    def test_single_delimiter_raises(self):
        node = TextNode("This is a `test", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_multiple_delimiters(self):
        node = TextNode("`code1` text `code2`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], TextNode("code1", TextType.CODE))
        self.assertEqual(result[1], TextNode(" text ", TextType.TEXT))
        self.assertEqual(result[2], TextNode("code2", TextType.CODE))

    def test_delimiter_at_start(self):
        node = TextNode("` code`text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], TextNode(" code", TextType.CODE))
        self.assertEqual(result[1], TextNode("text", TextType.TEXT))

    def test_delimiter_at_end(self):
        node = TextNode("text`code`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], TextNode("text", TextType.TEXT))
        self.assertEqual(result[1], TextNode("code", TextType.CODE))

    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [])

    def test_string_with_only(self):
        node = TextNode("``", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            [],
        )

    def test_string_with_delimiters_and_nothing_between(self):
        node = TextNode("`` bold", TextType.TEXT)
        # The function splits as ['', '', ' bold']
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            [
                TextNode(" bold", TextType.TEXT),
            ],
        )

    def test_delimiter_at_start_and_end(self):
        node = TextNode("`code`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 1)

    def test_double_split(self):
        node = TextNode("_text_ `code` more", TextType.TEXT)
        result1 = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            result1,
            [
                TextNode("_text_ ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" more", TextType.TEXT),
            ],
        )
        result2 = split_nodes_delimiter(result1, "_", TextType.ITALIC)
        self.assertEqual(
            result2,
            [
                TextNode("text", TextType.ITALIC),
                TextNode("code", TextType.CODE),
                TextNode(" more", TextType.TEXT),
            ],
        )


class TestExtractedFunctions(unittest.TestCase):
    def test_extracted_image_basic(self):
        text = "This is an image ![alt text](image.png) in markdown."
        self.assertEqual(extracted_image(text), [("alt text", "image.png")])

    def test_extracted_image_multiple(self):
        text = "![img1](a.png) and ![img2](b.jpg)"
        self.assertEqual(extracted_image(text), [("img1", "a.png"), ("img2", "b.jpg")])

    def test_extracted_image_no_match(self):
        text = "No images here!"
        self.assertEqual(extracted_image(text), [])

    def test_extracted_image_empty_alt(self):
        text = "![](img.png)"
        self.assertEqual(extracted_image(text), [("", "img.png")])

    def test_extracted_link_basic(self):
        text = "This is a [link](url.com) in markdown."
        self.assertEqual(extracted_link(text), [("link", "url.com")])

    def test_extracted_link_multiple(self):
        text = "[one](1) and [two](2)"
        self.assertEqual(extracted_link(text), [("one", "1"), ("two", "2")])

    def test_extracted_link_no_match(self):
        text = "No links here!"
        self.assertEqual(extracted_link(text), [])

    def test_extracted_link_ignores_images(self):
        text = "![alt](img.png) and [real](url)"
        self.assertEqual(extracted_link(text), [("real", "url")])

    def test_extracted_link_empty_text(self):
        text = "[]()"
        self.assertEqual(extracted_link(text), [("", "")])


class TestSplitNodesImagesAndLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image",
                    TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            new_nodes,
        )

    def test_split_images_no_image(self):
        node = TextNode("Just text", TextType.TEXT)
        self.assertListEqual(split_nodes_image([node]), [node])

    def test_split_images_single_image_surrounded(self):
        node = TextNode("Start ![alt](url) end", TextType.TEXT)
        self.assertListEqual(
            split_nodes_image([node]),
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "url"),
                TextNode(" end", TextType.TEXT),
            ],
        )

    def test_split_images_image_at_start(self):
        node = TextNode("![alt](url) after", TextType.TEXT)
        self.assertListEqual(
            split_nodes_image([node]),
            [
                TextNode("alt", TextType.IMAGE, "url"),
                TextNode(" after", TextType.TEXT),
            ],
        )

    def test_split_images_image_at_end(self):
        node = TextNode("before ![alt](url)", TextType.TEXT)
        self.assertListEqual(
            split_nodes_image([node]),
            [
                TextNode("before ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "url"),
            ],
        )

    def test_split_images_only_image(self):
        node = TextNode("![alt](url)", TextType.TEXT)
        self.assertListEqual(
            split_nodes_image([node]),
            [
                TextNode("alt", TextType.IMAGE, "url"),
            ],
        )

    def test_split_images_multiple_images(self):
        node = TextNode("A ![a](1) B ![b](2) C", TextType.TEXT)
        self.assertListEqual(
            split_nodes_image([node]),
            [
                TextNode("A ", TextType.TEXT),
                TextNode("a", TextType.IMAGE, "1"),
                TextNode(" B ", TextType.TEXT),
                TextNode("b", TextType.IMAGE, "2"),
                TextNode(" C", TextType.TEXT),
            ],
        )

    def test_split_images_empty_alt(self):
        node = TextNode("![ ](url)", TextType.TEXT)
        self.assertListEqual(
            split_nodes_image([node]),
            [
                TextNode(" ", TextType.IMAGE, "url"),
            ],
        )

    def test_split_images_empty_url(self):
        node = TextNode("![alt]()", TextType.TEXT)
        self.assertListEqual(
            split_nodes_image([node]),
            [
                TextNode("alt", TextType.IMAGE, ""),
            ],
        )

    def test_split_images_adjacent_images(self):
        node = TextNode("![a](1)![b](2)", TextType.TEXT)
        self.assertListEqual(
            split_nodes_image([node]),
            [
                TextNode("a", TextType.IMAGE, "1"),
                TextNode("b", TextType.IMAGE, "2"),
            ],
        )

    def test_split_images_special_characters(self):
        node = TextNode("![a!@#](u!@#)", TextType.TEXT)
        self.assertListEqual(
            split_nodes_image([node]),
            [
                TextNode("a!@#", TextType.IMAGE, "u!@#"),
            ],
        )

    def test_split_images_malformed_image(self):
        node = TextNode("![alt](url", TextType.TEXT)
        self.assertListEqual(
            split_nodes_image([node]),
            [TextNode("![alt](url", TextType.TEXT)],
        )

    def test_split_images_empty_string(self):
        node = TextNode("", TextType.TEXT)
        # split_nodes_image returns [] for empty string
        self.assertListEqual(split_nodes_image([node]), [])

    def test_split_images_whitespace(self):
        node = TextNode("   ", TextType.TEXT)
        # split_nodes_image returns [] for whitespace-only string
        self.assertListEqual(split_nodes_image([node]), [])

    def test_split_links_no_link(self):
        node = TextNode("Just text", TextType.TEXT)
        self.assertListEqual(split_nodes_link([node]), [node])

    def test_split_links_single_link_surrounded(self):
        node = TextNode("Start [alt](url) end", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("alt", TextType.LINK, "url"),
                TextNode(" end", TextType.TEXT),
            ],
        )

    def test_split_links_link_at_start(self):
        node = TextNode("[alt](url) after", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("alt", TextType.LINK, "url"),
                TextNode(" after", TextType.TEXT),
            ],
        )

    def test_split_links_link_at_end(self):
        node = TextNode("before [title](url)", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("before ", TextType.TEXT),
                TextNode("title", TextType.LINK, "url"),
            ],
        )

    def test_split_links_only_link(self):
        node = TextNode("[alt](url)", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("alt", TextType.LINK, "url"),
            ],
        )

    def test_split_links_multiple_links(self):
        node = TextNode("A [a](1) B [b](2) C", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("A ", TextType.TEXT),
                TextNode("a", TextType.LINK, "1"),
                TextNode(" B ", TextType.TEXT),
                TextNode("b", TextType.LINK, "2"),
                TextNode(" C", TextType.TEXT),
            ],
        )

    def test_split_links_empty_alt(self):
        node = TextNode("[](url)", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("", TextType.LINK, "url"),
            ],
        )

    def test_split_links_empty_url(self):
        node = TextNode("[alt]()", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("alt", TextType.LINK, ""),
            ],
        )

    def test_split_links_adjacent_links(self):
        node = TextNode("[a](1)[b](2)", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("a", TextType.LINK, "1"),
                TextNode("b", TextType.LINK, "2"),
            ],
        )

    def test_split_links_special_characters(self):
        node = TextNode("[a!@#](u!@#)", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("a!@#", TextType.LINK, "u!@#"),
            ],
        )

    def test_split_links_malformed_link(self):
        node = TextNode("[alt](url", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [TextNode("[alt](url", TextType.TEXT)],
        )

    def test_split_links_image_not_link(self):
        node = TextNode("![alt](img.png) and [real](url)", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("![alt](img.png) and ", TextType.TEXT),
                TextNode("real", TextType.LINK, "url"),
            ],
        )

    def test_split_links_empty_string(self):
        node = TextNode("", TextType.TEXT)
        # split_nodes_link returns [] for empty string
        self.assertListEqual(split_nodes_link([node]), [])

    def test_split_links_whitespace(self):
        node = TextNode("   ", TextType.TEXT)
        # split_nodes_link returns [] for whitespace-only string
        self.assertListEqual(split_nodes_link([node]), [])

    def test_split_links_with_whitespace(self):
        node = TextNode("   [alt](url)     ", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("alt", TextType.LINK, "url"),
            ],
        )

    def test_split_links_text_and_link_with_whitespace(self):
        node = TextNode("   before [alt](url) after   ", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("   before ", TextType.TEXT),
                TextNode("alt", TextType.LINK, "url"),
                TextNode(" after   ", TextType.TEXT),
            ],
        )


if __name__ == "__main__":
    unittest.main()
