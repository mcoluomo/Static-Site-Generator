import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        # Text comparison with equal TextNode objects
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_different_text_type(self):
        # Test comparison with differnt text_type propertys
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_eq_different_text(self):
        # Test comparison with differnt text
        node1 = TextNode("Text 1", TextType.NORMAL)
        node2 = TextNode("Text 2", TextType.NORMAL)
        self.assertNotEqual(node1, node2)

    def test_eq_different_types(self):
        # Test comparison with non-TextNode object
        node = TextNode("Some text", TextType.BOLD)
        not_node = "Some text"
        self.assertNotEqual(node, not_node)

    def test_url_comparison(self):
        # Test nodes with same text/type but different URLs
        node1 = TextNode("Link text", TextType.LINK, "https://example1.com")
        node2 = TextNode("Link text", TextType.LINK, "https://example2.com")
        node3 = TextNode("Link text", TextType.LINK, "https://example1.com")
        self.assertNotEqual(node1, node2)
        self.assertEqual(node1, node3)


if __name__ == "__main__":
    unittest.main()