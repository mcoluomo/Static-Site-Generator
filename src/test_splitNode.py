import unittest
from textnode import TextNode, TextType
from splitNode import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_delimiter(self):
        node = TextNode("This is a test", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], node)

    def test_single_delimiter(self):
        node = TextNode("This is a `test", TextType.TEXT)
        with self.assertRaises(Exception):
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
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_string_with_delimiters_and_nothing_between(self):
         node = TextNode("`` bold", TextType.TEXT)
         with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_delimiter_at_start_and_end(self):
        node = TextNode("`code`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], TextNode("code", TextType.CODE))

        #add nesting delimiters in the future
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

if __name__ == "__main__":
    unittest.main()