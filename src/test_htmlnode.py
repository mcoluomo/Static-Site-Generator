import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
        parent = HTMLNode(tag="div", children=[child1, child2])
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
            props={"href": "https://example.com", "target": "_blank"},
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
            props={"href": "https://example.com", "class": "link"},
        )
        html_props = node.props_to_html()
        # Since dict order is not guaranteed, check both possible combinations
        # might change the valid_outputs list in the future
        valid_outputs = [
            ' href="https://example.com" class="link"',
            ' class="link" href="https://example.com"',
        ]
        self.assertIn(html_props, valid_outputs)

    def test_repr_output(self):
        # Test string representation
        node = HTMLNode(tag="p", value="text", children=None, props={"class": "text"})
        expected = "HTMLNODE(p, text, [], {'class': 'text'})"
        self.assertEqual(repr(node), expected)

    def test_leaf_to_html_p(self):
        leaf_node = LeafNode("p", "Hello, world!")
        only_value_node = LeafNode(value="This is a paragraph of text.")
        attribute_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        no_value_node = LeafNode("h1")

        self.assertEqual(leaf_node.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(only_value_node.to_html(), "This is a paragraph of text.")
        self.assertEqual(
            attribute_node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )
        with self.assertRaises(ValueError):
            no_value_node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_value_errors(self):
        parent_node = ParentNode(None, [LeafNode("p", "child")])
        parent_node1 = ParentNode("", [LeafNode("b", "child")])

        with self.assertRaises(ValueError):
            parent_node.to_html()

        with self.assertRaises(ValueError):
            parent_node1.to_html()

    def test_parent_node_with_props(self):
        child = LeafNode("p", "text")
        parent = ParentNode("div", [child], {"class": "container", "id": "main"})
        self.assertEqual(
            parent.to_html(),
            '<div class="container" id="main"><p>text</p></div>',
        )

    def test_parent_multiple_children_and_props(self):
        child1 = LeafNode("p", "first")
        child2 = LeafNode("p", "second")
        parent = ParentNode("div", [child1, child2], {"class": "wrapper"})
        self.assertEqual(
            parent.to_html(),
            '<div class="wrapper"><p>first</p><p>second</p></div>',
        )

    def test_nested_nodes_with_props(self):
        grandchild = LeafNode("span", "text", {"class": "text"})
        child = ParentNode("p", [grandchild], {"class": "paragraph"})
        parent = ParentNode("div", [child], {"id": "wrapper"})
        self.assertEqual(
            parent.to_html(),
            '<div id="wrapper"><p class="paragraph"><span class="text">text</span></p></div>',
        )


if __name__ == "__main__":
    unittest.main()
