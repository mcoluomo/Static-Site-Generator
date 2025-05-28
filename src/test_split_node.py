import unittest

from split_node import (
    extracted_image,
    extracted_link,
    split_nodes_delimiter,
    split_nodes_image,
)
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_delimiter(self):
        node = TextNode("This is a test", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], node)

    def test_single_delimiter(self):
        node = TextNode("This is a `test", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_even_delimiters(self):
        node = TextNode("This is a `test`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], TextNode("This is a ", TextType.TEXT))
        self.assertEqual(result[1], TextNode("test", TextType.CODE))

    def test_multiple_delimiters(self):
        node = TextNode("`code1` text `code2`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], TextNode("code1", TextType.CODE))
        self.assertEqual(result[1], TextNode(" text ", TextType.TEXT))
        self.assertEqual(result[2], TextNode("code2", TextType.CODE))

    def test_delimiter_at_start(self):
        node = TextNode("`code`text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], TextNode("code", TextType.CODE))
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
        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])

    def test_string_with_only_delimiter(self):
        node = TextNode("``", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_string_with_delimiters_and_nothing_between(self):
        node = TextNode("`` bold", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_delimiter_at_start_and_end(self):
        node = TextNode("`code`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], TextNode("code", TextType.CODE))

        # add nesting delimiters in the future

    """
    def test_nested_delimiters(self):
        node = TextNode("text `code1 `code2`` more", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], TextNode("text ", TextType.TEXT))
        self.assertEqual(result[1], TextNode("code1 ", TextType.CODE))
        self.assertEqual(result[2], TextNode("code2", TextType.TEXT))
        self.assertEqual(result[3], TextNode(" more", TextType.TEXT))
    """

    def test_double_split(self):
        node = TextNode("_text_ `code` more", TextType.TEXT)
        result1 = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result1), 3)
        self.assertEqual(result1[0], TextNode("_text_ ", TextType.TEXT))
        self.assertEqual(result1[1], TextNode("code", TextType.CODE))
        self.assertEqual(result1[2], TextNode(" more", TextType.TEXT))

        result2 = split_nodes_delimiter(result1, "_", TextType.ITALIC)
        self.assertEqual(len(result2), 3)
        self.assertEqual(result2[0], TextNode("text", TextType.ITALIC))
        self.assertEqual(result2[1], TextNode("code", TextType.CODE))
        self.assertEqual(result2[2], TextNode(" more", TextType.TEXT))


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


if __name__ == "__main__":
    unittest.main()
