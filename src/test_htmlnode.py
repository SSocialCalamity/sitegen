import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()