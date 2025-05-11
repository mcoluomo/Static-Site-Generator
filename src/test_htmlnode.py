import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_text_only_node(self):
        # Test node with only text (no tag)
        node = HTMLNode(value="Hello world")
        self.assertIsNone(node.tag)
        self.assertEqual(node.value, "Hello world")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_parent_with_children(self):
        # Test node with children (no value)
        child1 = HTMLNode(tag="p", value="First")
        child2 = HTMLNode(tag="p", value="Second")
        parent = HTMLNode(
            tag="div",
            children=[child1, child2]
        )
        self.assertEqual(parent.tag, "div")
        self.assertIsNone(parent.value)
        self.assertEqual(len(parent.children), 2)
        self.assertEqual(parent.children[0].value, "First")
        self.assertEqual(parent.children[1].value, "Second")

    def test_node_with_attributes(self):
        # Test node with HTML attributes
        node = HTMLNode(
            tag="a",
            value="Click me",
            props={"href": "https://example.com", "target": "_blank"}
        )
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Click me")
        self.assertEqual(len(node.props), 2)
        self.assertEqual(node.props["href"], "https://example.com")
        self.assertEqual(node.props["target"], "_blank")


    def test_props_to_html(self):
        # Test properties conversion to HTML
        node = HTMLNode(
            tag="a",
            value="Click me",
            props={"href": "https://example.com", "class": "link"}
        )
        html_props = node.props_to_html()
        # Since dict order is not guaranteed, check both possible combinations
    # might change the valid_outputs list in the future
        valid_outputs = [
            ' href="https://example.com" class="link"',
            ' class="link" href="https://example.com"'
        ]
        self.assertIn(html_props, valid_outputs)

    def test_repr_output(self):
        # Test string representation
        node = HTMLNode(
            tag="p",
            value="text",
            children=None,
            props={"class": "text"}
        )
        expected = 'HTMLNODE(p, text, [], {\'class\': \'text\'})'
        self.assertEqual(repr(node), expected)



    def test_leaf_to_html_p(self):
        leafNode = LeafNode("p", "Hello, world!")
        onlyValueNode = LeafNode(value="This is a paragraph of text.")
        attributeNode = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        noValueNode = LeafNode("h1")


        self.assertEqual(leafNode.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(onlyValueNode.to_html(), "This is a paragraph of text.")
        self.assertEqual(
            attributeNode.to_html(),
            '<a href="https://www.google.com">Click me!</a>'
        )
        with self.assertRaises(ValueError):
            noValueNode.to_html()

if __name__ == "__main__":
    unittest.main()