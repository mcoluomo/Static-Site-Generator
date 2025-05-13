import unittest

from textnode import TextNode, TextType, text_node_to_html_node


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
        node1 = TextNode("Text 1", TextType.TEXT)
        node2 = TextNode("Text 2", TextType.TEXT)
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

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_text_node_to_html_node_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {})

    def test_text_node_to_html_node_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")
        self.assertEqual(html_node.props, {})

    def test_text_node_to_html_node_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")
        self.assertEqual(html_node.props, {})

    def test_text_node_to_html_node_code(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code")
        self.assertEqual(html_node.props, {})

    def test_text_node_to_html_node_link(self):
        node = TextNode("Click me", TextType.LINK, "https://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(html_node.props, {"href": "https://www.example.com"})

    def test_text_node_to_html_node_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src": "image.png", "alt": "Alt text"})

    def test_text_node_to_html_node_invalid(self):
        # Create an invalid TextNode with undefined text_type
        with self.assertRaises(ValueError):
            text_node_to_html_node("invalid node")

if __name__ == "__main__":
    unittest.main()