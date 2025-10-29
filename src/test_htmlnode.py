import unittest

from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(None, None, None, {"href": "https://www.google.com", "target": "_blank"})
        node2 = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), node2)
    def test_neq(self):
        node = HTMLNode(None, None, None, None)
        node2 = HTMLNode("p", None, None, None)
        self.assertNotEqual(node, node2)
    def test_neq2(self):
        node = HTMLNode("a", None, None, None)
        node2 = HTMLNode("p", None, None, None)
        self.assertNotEqual(node, node2)
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_prop(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
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
    def test_to_html_parent_without_children(self):
        with self.assertRaises(ValueError):
            parent_node = ParentNode("span", None, {"href": "https://www.google.com"})
            parent_node.to_html()
    def test_to_html_parent_no_tag(self):
        with self.assertRaises(ValueError):
            child_node = LeafNode("b", "child")
            parent_node = ParentNode(None, [child_node], {"href": "https://www.google.com"})
            parent_node.to_html()


if __name__ == "__main__":
    unittest.main()